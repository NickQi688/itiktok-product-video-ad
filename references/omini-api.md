# KIE.ai Media API

This skill includes a local helper for KIE.ai media generation:

```bash
python /Users/a9999/.codex/skills/tiktok-product-video-ad/scripts/kie_media.py \
  --job-config "/path/to/jobs.json"
```

`scripts/omini_video.py` remains as a backward-compatible wrapper for `--provider omini`.

## API Key

Use either environment variable:

```bash
export KIE_API_KEY="..."
# or
export OMINI_API_KEY="..."
```

Do not write API keys into project prompt files or job JSON files.

## Supported Providers

| provider | model | output | key input fields |
| --- | --- | --- | --- |
| `omini` | `gemini-omni-video` | video | `prompt`, `image_urls`, `video_list`, `duration`, `aspect_ratio`, `resolution` |
| `seedance` | `bytedance/seedance-2` | video | `prompt`, `reference_image_urls`, `first_frame_url`, `last_frame_url`, `reference_video_urls`, `reference_audio_urls`, `duration`, `aspect_ratio`, `resolution`, `generate_audio`, `web_search` |
| `seedance-fast` | `bytedance/seedance-2-fast` | video | same as `seedance`, with `480p`/`720p` resolution |
| `gpt-image-t2i` | `gpt-image-2-text-to-image` | image | `prompt`, `aspect_ratio`, `resolution` |
| `gpt-image-i2i` | `gpt-image-2-image-to-image` | image | `prompt`, `input_urls`, `aspect_ratio`, `resolution` |

All providers use KIE's async task flow:

1. Upload local files to KIE file upload.
2. `POST /api/v1/jobs/createTask`.
3. Poll `GET /api/v1/jobs/recordInfo`.
4. Download the first returned media URL.
5. Write a manifest with task IDs, URLs, and output paths.

## Job Config

```json
{
  "jobs": [
    {
      "provider": "seedance",
      "name": "video1",
      "markdown": "/absolute/path/to/script.md",
      "video": 1,
      "duration": 8,
      "aspect_ratio": "9:16",
      "resolution": "720p",
      "references": [
        "/absolute/path/to/storyboard.png",
        "/absolute/path/to/product.png"
      ],
      "generate_audio": false,
      "web_search": false,
      "output_dir": "/absolute/path/to/output"
    }
  ]
}
```

For markdown video jobs, the script extracts:

- `### 视频 1 omini 视频生成提示词`
- `### 视频 1 负面提示词`
- `### 视频 2 omini 视频生成提示词`
- `### 视频 2 负面提示词`

For image jobs, use `prompt` or `prompt_file` directly.

## Dry Run

Use `--dry-run` to upload references and verify payload shape without creating paid generation tasks:

```bash
python /Users/a9999/.codex/skills/tiktok-product-video-ad/scripts/kie_media.py \
  --job-config "/path/to/jobs.json" \
  --dry-run
```

## Examples

Run current Coolizi videos with Gemini Omni:

```bash
python /Users/a9999/.codex/skills/tiktok-product-video-ad/scripts/kie_media.py \
  --job-config "/Users/a9999/Documents/qukauiqiji/tiktok视频/视频脚本/空调/04-Coolizi欧洲高温omini拆分版-2条10秒内/omini-jobs.json"
```

Run current Coolizi videos with Seedance 2.0:

```bash
python /Users/a9999/.codex/skills/tiktok-product-video-ad/scripts/kie_media.py \
  --job-config "/Users/a9999/Documents/qukauiqiji/tiktok视频/视频脚本/空调/04-Coolizi欧洲高温omini拆分版-2条10秒内/kie-jobs.seedance.json"
```

Run current Coolizi videos with Seedance 2.0 Fast:

```bash
python /Users/a9999/.codex/skills/tiktok-product-video-ad/scripts/kie_media.py \
  --job-config "/Users/a9999/Documents/qukauiqiji/tiktok视频/视频脚本/空调/04-Coolizi欧洲高温omini拆分版-2条10秒内/kie-jobs.seedance-fast.json"
```

Run GPT Image 2 examples:

```bash
python /Users/a9999/.codex/skills/tiktok-product-video-ad/scripts/kie_media.py \
  --job-config "/Users/a9999/Documents/qukauiqiji/tiktok视频/视频脚本/空调/04-Coolizi欧洲高温omini拆分版-2条10秒内/kie-jobs.gpt-image-examples.json"
```

## Reference Order

For product ad videos:

1. Storyboard image first.
2. Product/detail images after.
3. Optional reference videos/audio only when the chosen provider supports them.

Seedance modes are mutually exclusive in the upstream API: first-frame, first+last-frame, and multimodal reference-to-video should not be mixed unless the provider supports the exact combination needed.
