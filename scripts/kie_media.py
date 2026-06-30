#!/usr/bin/env python3
"""Unified KIE.ai media generation helper.

Supported providers:
- omini: Gemini Omni Video
- seedance: Bytedance Seedance 2.0
- seedance-fast: Bytedance Seedance 2.0 Fast
- gpt-image-t2i: GPT Image 2 text-to-image
- gpt-image-i2i: GPT Image 2 image-to-image
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


CREATE_TASK_URL = "https://api.kie.ai/api/v1/jobs/createTask"
RECORD_INFO_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-stream-upload"

SUCCESS_STATES = {"SUCCESS", "SUCCEEDED", "COMPLETED", "COMPLETE", "DONE"}
FAILED_STATES = {"FAIL", "FAILED", "ERROR", "CANCELLED", "CANCELED"}


@dataclass(frozen=True)
class Provider:
    model: str
    kind: str
    default_resolution: str
    default_duration: int | None = None


PROVIDERS: dict[str, Provider] = {
    "omini": Provider("gemini-omni-video", "video", "720p", 8),
    "seedance": Provider("bytedance/seedance-2", "video", "720p", 8),
    "seedance-fast": Provider("bytedance/seedance-2-fast", "video", "720p", 8),
    "gpt-image-t2i": Provider("gpt-image-2-text-to-image", "image", "1K", None),
    "gpt-image-i2i": Provider("gpt-image-2-image-to-image", "image", "1K", None),
}


class KieError(RuntimeError):
    pass


def read_api_key() -> str:
    key = os.environ.get("KIE_API_KEY") or os.environ.get("OMINI_API_KEY")
    if not key:
        raise KieError("Missing API key. Set KIE_API_KEY or OMINI_API_KEY.")
    return key


def auth_headers(api_key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"}


def json_headers(api_key: str) -> dict[str, str]:
    headers = auth_headers(api_key)
    headers["Content-Type"] = "application/json"
    return headers


def require_success_response(response: requests.Response, action: str) -> dict[str, Any]:
    try:
        payload = response.json()
    except Exception as exc:
        raise KieError(f"{action} returned non-JSON response: {response.text[:500]}") from exc

    if response.status_code >= 400:
        raise KieError(f"{action} failed with HTTP {response.status_code}: {payload}")

    code = payload.get("code")
    if code not in (None, 200, "200", 0, "0"):
        raise KieError(f"{action} failed with vendor code {code}: {payload}")

    return payload


def upload_file(path: Path, api_key: str, timeout: int) -> str:
    if not path.exists():
        raise KieError(f"Reference file not found: {path}")

    content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    with path.open("rb") as handle:
        files = {"file": (path.name, handle, content_type)}
        response = requests.post(
            UPLOAD_URL,
            headers=auth_headers(api_key),
            files=files,
            timeout=timeout,
        )

    payload = require_success_response(response, f"Upload {path.name}")
    data = payload.get("data")
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        for key in ("url", "fileUrl", "downloadUrl"):
            if data.get(key):
                return str(data[key])
    raise KieError(f"Upload response did not include a file URL: {payload}")


def maybe_upload(ref: str, api_key: str, timeout: int) -> str:
    if ref.startswith(("http://", "https://", "asset://")):
        return ref
    return upload_file(Path(ref).expanduser().resolve(), api_key, timeout)


def maybe_upload_many(refs: list[str], api_key: str, timeout: int) -> list[str]:
    return [maybe_upload(str(ref), api_key, timeout) for ref in refs]


def resolve_job_path(job: dict[str, Any], value: str) -> str:
    if value.startswith(("http://", "https://", "asset://")):
        return value
    path = Path(value).expanduser()
    if path.is_absolute():
        return str(path)
    config_dir = job.get("__config_dir")
    if config_dir:
        return str((Path(config_dir) / path).resolve())
    return str(path.resolve())


def resolve_job_paths(job: dict[str, Any], values: list[str]) -> list[str]:
    return [resolve_job_path(job, str(value)) for value in values]


def extract_markdown_section(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^### {re.escape(heading)}\s*\n(?P<body>.*?)(?=^### |^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if not match:
        raise KieError(f"Could not find markdown section: ### {heading}")
    return match.group("body").strip()


def prompt_from_markdown(path: Path, video: int) -> tuple[str, str]:
    markdown = path.read_text(encoding="utf-8")
    prompt = extract_markdown_section(markdown, f"视频 {video} omini 视频生成提示词")
    negative = extract_markdown_section(markdown, f"视频 {video} 负面提示词")
    return prompt, negative


def read_prompt(job: dict[str, Any], args: argparse.Namespace) -> tuple[str, str]:
    if job.get("prompt"):
        prompt = str(job["prompt"])
    elif job.get("prompt_file"):
        prompt = Path(resolve_job_path(job, str(job["prompt_file"]))).read_text(encoding="utf-8").strip()
    elif job.get("markdown") or args.markdown:
        markdown = Path(resolve_job_path(job, str(job.get("markdown") or args.markdown)))
        video = int(job.get("video") or args.video)
        prompt, extracted_negative = prompt_from_markdown(markdown, video)
        negative = str(job.get("negative_prompt") or args.negative_prompt or extracted_negative)
        return prompt, negative
    else:
        raise KieError("Job needs prompt, prompt_file, or markdown.")

    negative = str(job.get("negative_prompt") or args.negative_prompt or "")
    return prompt, negative


def safe_status(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    data = payload.get("data")
    if isinstance(data, dict):
        for key in ("status", "state", "taskStatus", "generateStatus"):
            if data.get(key) is not None:
                return str(data[key])
    for key in ("status", "state", "taskStatus", "generateStatus"):
        if payload.get(key) is not None:
            return str(payload[key])
    return ""


def parse_jsonish(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def collect_urls(value: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            urls.append(value)
        return urls
    if isinstance(value, list):
        for item in value:
            urls.extend(collect_urls(item))
        return urls
    if isinstance(value, dict):
        for item in value.values():
            urls.extend(collect_urls(item))
    return urls


def extract_media_urls(payload: dict[str, Any], kind: str) -> list[str]:
    data = payload.get("data")
    candidates: list[Any] = []
    if isinstance(data, dict):
        for key in ("resultJson", "result", "output", "outputs", "videoUrls", "videos", "imageUrls", "images"):
            if key in data:
                candidates.append(parse_jsonish(data[key]))
    candidates.append(payload)

    urls: list[str] = []
    for candidate in candidates:
        urls.extend(collect_urls(candidate))

    if kind == "video":
        extensions = (".mp4", ".mov", ".webm", ".m4v")
    else:
        extensions = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff")

    seen: set[str] = set()
    preferred: list[str] = []
    fallback: list[str] = []
    for url in urls:
        path = urlparse(url).path.lower()
        target = preferred if path.endswith(extensions) else fallback
        if url not in seen:
            seen.add(url)
            target.append(url)
    return preferred or fallback


def build_input(
    *,
    provider_name: str,
    provider: Provider,
    prompt: str,
    negative: str,
    job: dict[str, Any],
    args: argparse.Namespace,
    api_key: str,
) -> dict[str, Any]:
    full_prompt = prompt.strip()
    if negative.strip():
        full_prompt = f"{full_prompt}\n\nNegative prompt / 禁止事项:\n{negative.strip()}"

    aspect_ratio = str(job.get("aspect_ratio") or args.aspect_ratio)
    resolution = str(job.get("resolution") or provider.default_resolution)
    input_payload: dict[str, Any] = {
        "prompt": full_prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }

    if provider.kind == "video":
        duration = int(job.get("duration") or args.duration or provider.default_duration or 8)
        input_payload["duration"] = str(duration) if provider_name == "omini" else duration

    if provider_name == "omini":
        refs = resolve_job_paths(job, list(job.get("references") or args.references or []))
        if refs:
            input_payload["image_urls"] = maybe_upload_many(refs, api_key, args.timeout)
        if job.get("video_list"):
            input_payload["video_list"] = job["video_list"]
        return input_payload

    if provider_name in {"seedance", "seedance-fast"}:
        refs = resolve_job_paths(job, list(job.get("references") or job.get("reference_image_urls") or args.references or []))
        if refs:
            input_payload["reference_image_urls"] = maybe_upload_many(refs, api_key, args.timeout)
        if job.get("first_frame_url"):
            input_payload["first_frame_url"] = maybe_upload(resolve_job_path(job, str(job["first_frame_url"])), api_key, args.timeout)
        if job.get("last_frame_url"):
            input_payload["last_frame_url"] = maybe_upload(resolve_job_path(job, str(job["last_frame_url"])), api_key, args.timeout)
        if job.get("reference_video_urls"):
            input_payload["reference_video_urls"] = maybe_upload_many(resolve_job_paths(job, job["reference_video_urls"]), api_key, args.timeout)
        if job.get("reference_audio_urls"):
            input_payload["reference_audio_urls"] = maybe_upload_many(resolve_job_paths(job, job["reference_audio_urls"]), api_key, args.timeout)
        input_payload["generate_audio"] = bool(job.get("generate_audio", args.generate_audio))
        input_payload["web_search"] = bool(job.get("web_search", False))
        if "return_last_frame" in job:
            input_payload["return_last_frame"] = bool(job["return_last_frame"])
        if "nsfw_checker" in job:
            input_payload["nsfw_checker"] = bool(job["nsfw_checker"])
        return input_payload

    if provider_name == "gpt-image-t2i":
        return input_payload

    if provider_name == "gpt-image-i2i":
        refs = resolve_job_paths(job, list(job.get("input_urls") or job.get("references") or args.references or []))
        if not refs:
            raise KieError("gpt-image-i2i requires input_urls or references.")
        input_payload["input_urls"] = maybe_upload_many(refs, api_key, args.timeout)
        return input_payload

    raise KieError(f"Unsupported provider: {provider_name}")


def create_task(api_key: str, model: str, input_payload: dict[str, Any], timeout: int) -> str:
    response = requests.post(
        CREATE_TASK_URL,
        headers=json_headers(api_key),
        json={"model": model, "input": input_payload},
        timeout=timeout,
    )
    payload = require_success_response(response, "Create KIE task")
    data = payload.get("data")
    if isinstance(data, dict):
        for key in ("taskId", "task_id", "id"):
            if data.get(key):
                return str(data[key])
    raise KieError(f"Create task response did not include taskId: {payload}")


def record_info(api_key: str, task_id: str, timeout: int) -> dict[str, Any]:
    response = requests.get(
        RECORD_INFO_URL,
        headers=auth_headers(api_key),
        params={"taskId": task_id},
        timeout=timeout,
    )
    return require_success_response(response, "Query KIE task")


def poll_for_result(api_key: str, task_id: str, kind: str, args: argparse.Namespace) -> dict[str, Any]:
    start = time.monotonic()
    last_payload: dict[str, Any] | None = None
    while True:
        payload = record_info(api_key, task_id, args.timeout)
        last_payload = payload
        status = safe_status(payload).upper()
        elapsed = int(time.monotonic() - start)
        print(f"[kie] task={task_id} status={status or 'UNKNOWN'} elapsed={elapsed}s", flush=True)

        if status in SUCCESS_STATES or extract_media_urls(payload, kind):
            return payload
        if status in FAILED_STATES:
            raise KieError(f"Task failed: {json.dumps(payload, ensure_ascii=False)[:2000]}")
        if elapsed >= args.max_wait:
            raise KieError(
                f"Timed out after {args.max_wait}s waiting for task {task_id}. "
                f"Last payload: {json.dumps(last_payload, ensure_ascii=False)[:2000]}"
            )
        time.sleep(args.poll_interval)


def download(url: str, output_path: Path, timeout: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with output_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def load_job_config(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    jobs = payload.get("jobs") if isinstance(payload, dict) else payload
    if not isinstance(jobs, list):
        raise KieError("Job config must be a JSON list or an object with a jobs list.")
    for job in jobs:
        if isinstance(job, dict):
            job.setdefault("__config_dir", str(path.parent.resolve()))
    return jobs


def run_job(job: dict[str, Any], args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    provider_name = str(job.get("provider") or args.provider)
    if provider_name not in PROVIDERS:
        raise KieError(f"Unsupported provider {provider_name}. Choose: {', '.join(PROVIDERS)}")
    provider = PROVIDERS[provider_name]
    model = str(job.get("model") or provider.model)
    name = str(job.get("name") or f"{provider_name}-{int(time.time())}")
    prompt, negative = read_prompt(job, args)
    input_payload = build_input(
        provider_name=provider_name,
        provider=provider,
        prompt=prompt,
        negative=negative,
        job=job,
        args=args,
        api_key=api_key,
    )

    printable_payload = {"model": model, "input": input_payload}
    print(f"[kie] prepared {name}: provider={provider_name} model={model}", flush=True)
    if args.dry_run:
        return {
            "name": name,
            "provider": provider_name,
            "dry_run": True,
            "payload": printable_payload,
        }

    task_id = create_task(api_key, model, input_payload, args.timeout)
    payload = poll_for_result(api_key, task_id, provider.kind, args)
    urls = extract_media_urls(payload, provider.kind)
    if not urls:
        raise KieError(f"Task {task_id} completed but no {provider.kind} URL was found.")

    output_dir = Path(resolve_job_path(job, str(job.get("output_dir") or args.output_dir)))
    suffix = Path(urlparse(urls[0]).path).suffix
    if not suffix:
        suffix = ".mp4" if provider.kind == "video" else ".png"
    output_path = output_dir / f"{name}{suffix}"
    download(urls[0], output_path, args.timeout)

    return {
        "name": name,
        "provider": provider_name,
        "model": model,
        "task_id": task_id,
        "url": urls[0],
        "output_path": str(output_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate images/videos through KIE.ai.")
    parser.add_argument("--job-config", help="JSON file containing one or more jobs.")
    parser.add_argument("--provider", default="omini", choices=sorted(PROVIDERS))
    parser.add_argument("--markdown", help="Markdown file containing omini prompt sections.")
    parser.add_argument("--video", type=int, default=1, help="Video number to extract from markdown.")
    parser.add_argument("--prompt", help="Direct prompt text.")
    parser.add_argument("--prompt-file", help="Prompt text file.")
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--references", nargs="*", default=[], help="Local paths, URLs, or asset:// refs.")
    parser.add_argument("--duration", type=int)
    parser.add_argument("--aspect-ratio", default="9:16")
    parser.add_argument("--resolution")
    parser.add_argument("--output-dir", default="生成媒体/kie")
    parser.add_argument("--manifest", default="生成媒体/kie/manifest.json")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--poll-interval", type=int, default=15)
    parser.add_argument("--max-wait", type=int, default=1800)
    parser.add_argument("--generate-audio", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Upload refs and build payload, but do not create tasks.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        api_key = read_api_key()
        if args.job_config:
            jobs = load_job_config(Path(args.job_config).expanduser().resolve())
        else:
            job: dict[str, Any] = {
                "provider": args.provider,
                "references": args.references,
            }
            if args.markdown:
                job["markdown"] = args.markdown
                job["video"] = args.video
            elif args.prompt:
                job["prompt"] = args.prompt
            elif args.prompt_file:
                job["prompt_file"] = args.prompt_file
            else:
                parser.error("Provide --job-config, --markdown, --prompt, or --prompt-file.")
            if args.duration:
                job["duration"] = args.duration
            if args.resolution:
                job["resolution"] = args.resolution
            job["aspect_ratio"] = args.aspect_ratio
            job["output_dir"] = args.output_dir
            jobs = [job]

        results = [run_job(job, args, api_key) for job in jobs]
        manifest_path = Path(args.manifest).expanduser().resolve()
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(results, ensure_ascii=False, indent=2))
        print(f"[kie] manifest={manifest_path}")
        return 0
    except Exception as exc:
        print(f"[kie] error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
