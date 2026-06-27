---
name: tiktok-product-video-ad
description: "Use when the user wants to create TikTok video ad assets for portable air conditioners, wall-mounted mini AC units, cooling/heating fans, or AC accessories from product images, product selling points, landing pages, or competitor video breakdowns. Works across agents with or without image/video generation tools: ask for duration, creative idea, requirements, and references, then produce a storyboard prompt or image, final video prompt, negative prompt, and optional API-ready video payload or generated video."
---

# TikTok Product Video Ad

## Purpose

Turn air-conditioner product images, product features, and competitor references into a ready-to-generate TikTok ad package.

Current scope is air-conditioning products: portable AC, wall-mounted mini AC, cooling/heating units, fans with cooling claims, AC deflectors, AC cleaning/maintenance products, and related accessories. Do not broaden into other categories unless the user explicitly asks to extend the skill later.

Default deliverables should be:
- A storyboard image prompt.
- A storyboard image, when image generation is available or requested.
- A final video generation prompt.
- A negative prompt.

Optional deliverables:
- Generated video, only when the user explicitly asks for video production and an API/tool is available and configured.
- API-ready payload when no video API/tool is available.

Optionally save deliverables into the user's project folders when working in a local workspace.

## Start-of-Task Intake

At the start, ask only what is missing and necessary. If the user already provided enough context, proceed.

Required or strongly preferred:
- Duration: default to 8-10 seconds if absent.
- Aspect ratio: default to 9:16 for TikTok.
- Product images: product/detail/exploded-view images used to lock identity.
- Product selling points: use provided notes, landing page extraction, or visible product details.
- Creative direction: ask if they have an idea; otherwise generate one from product + references.
- Requirements: target country/language, mandatory text, forbidden claims, model name.
- Reference videos or breakdowns: use them for structure, pacing, hooks, and transitions only.
- Video production: ask only if relevant; default is prompt/storyboard handoff, not API generation.

Good concise question when context is missing:
“要做几秒？有没有指定创意/卖点/语言/禁止内容？需要我只交付分镜图+视频提示词，还是也尝试生成视频？没有的话我按 TikTok 9:16、8-10 秒、强钩子带货节奏来做。”

## Workflow

Before generating deliverables, load the reusable prompt templates in `references/prompt-templates.md` when the task requires any concrete script, storyboard, image prompt, video prompt, or API payload.

1. Gather context
   - Inspect product images if provided.
   - Read product notes, landing-page extracts, and existing competitor breakdowns.
   - Identify stable product identity: body shape, color, material, control panel, outlet grille, vent direction, logo/markings, wall bracket, accessories, power cord, remote, hose/tank if visible.
   - Flag unsupported claims as “page claim / needs verification”.

2. Choose ad structure
   - Use a direct TikTok sequence: pain hook -> instant setup -> feature proof -> emotional payoff -> conversion close.
   - Keep scenes simple and model-friendly.
   - Use competitor videos for pacing and shot logic, not for copying brand, people, exact text, or exact scene.

3. Generate script and storyboard prompt together
   - Do not make the user wait for a separate script pass unless requested.
   - Treat script, storyboard prompt, final video prompt, and negative prompt as one generation batch.
   - Produce a shot table with time, visual, action, camera, text/audio, and purpose.
   - Produce per-shot video prompts for precise generation.
   - Produce one continuous video prompt.
   - Produce one storyboard image prompt.
   - Save intermediate script/prompt files when a workspace structure exists, but keep the user-facing handoff focused on the storyboard image and video prompt.

4. Generate storyboard image
   - Always produce a storyboard image prompt.
   - If image generation is available and the user wants or implies a storyboard image, call image generation.
   - If image generation is unavailable, give the storyboard prompt clearly so the user or another agent can generate it elsewhere.
   - Use the product image as identity reference in the prompt text: lock exact shape, color, control panel position, outlet, accessories.
   - Prefer one single storyboard board, not separate images.
   - Keep text minimal to avoid gibberish. Use short labels or numeric callouts.

5. Final video prompt
   - Tell the user to upload the storyboard image first and product images/detail images as identity references.
   - The prompt must state:
     - First reference image = storyboard structure.
     - Product/detail images = product consistency.
     - Competitor videos = pacing/reference only, if used.
   - Include exact shot timing for videos under 15 seconds.

6. Optional video production
   - Enter this stage only when the user explicitly requests actual video generation.
   - If a video-generation API/tool is available, use the generated storyboard image and product images as references.
   - If no API/tool is configured, deliver an API-ready payload outline instead of pretending the video was generated.
   - Keep provider-specific parameters isolated so they can be swapped later.
   - Preserve the final prompt as the source of truth.

## Capability Matrix

Adapt to the current agent environment:

| Available capability | What to do |
| --- | --- |
| Text only | Produce script, storyboard image prompt, final video prompt, negative prompt, and optional API payload. |
| Image generation available | Generate the storyboard image and also include/save the storyboard prompt. |
| Video API/tool available | Generate the video only if requested; otherwise stop at prompt/storyboard handoff. |
| Neither image nor video tools available | Deliver prompts in a copy-ready format and explain which references to upload. |
| Another agent will continue | Save or present files with clear names: storyboard prompt, final video prompt, negative prompt, API payload. |

Never make a tool-specific step mandatory. The workflow must remain useful for Codex, Claude Code, browser-only agents, and API-only agents.

## Optional Video API Payload Pattern

When asked to generate or prepare API input, use this generic shape and adapt names to the provider:

```json
{
  "prompt": "final video prompt",
  "negative_prompt": "negative prompt if supported",
  "reference_images": [
    "storyboard image first",
    "main product/detail images"
  ],
  "reference_videos": [
    "competitor reference videos, optional"
  ],
  "duration": 9,
  "aspect_ratio": "9:16",
  "resolution": "720p or provider default",
  "audio": false
}
```

Provider notes:
- Seedance / Seedance Mini: storyboard image first in `reference_image_urls`; product images after it; competitor videos in `reference_video_urls` if supported.
- Gemini-style video models: use storyboard/product images as image references and optional reference video list if supported.
- Other providers: keep storyboard first, product identity references second, and avoid adding unsupported fields.

## Default TikTok Ad Pattern

For 8-10 second ads, use 6-7 shots:

1. 0-1s: Pain hook
2. 1-2.5s: Product setup/use action
3. 2.5-3.5s: Control/detail proof
4. 3.5-5s: Core function visual
5. 5-6.5s: Human comfort/emotional reaction
6. 6.5-8s: Secondary feature or second season/use case
7. 8-10s: Hero product + CTA

Keep each shot visually distinct. Avoid cramming too many product features into one short video.

## Product Lock Rules

Every output must include product consistency rules:
- Same product in every shot.
- Do not change exterior shape, color, material, structure, logo/markings, control panel location, outlet shape, accessories, or proportions.
- Do not invent hidden features, water tanks, hoses, functions, or badges unless visible or provided.
- If reference images conflict, prioritize the clearest product/detail/exploded-view image.
- If the ad uses blue/orange airflow, keep it subtle and not sci-fi.

Air-conditioner-specific lock checklist:
- body silhouette: wall-mounted horizontal unit, vertical unit, portable desktop unit, or accessory shape
- control panel position and style
- display/LED area
- outlet grille shape and position
- inlet grille if visible
- power cord/plug
- remote control
- wall bracket or hook structure
- cooling/heating visual state
- visible labels, badges, or brand marks
- accessories such as screws, brackets, hoses, water tanks, filters, or manuals only if provided

Common AC ad scenes:
- overheated room or weak fan pain hook
- plug in / no drilling / no installation
- touch panel or remote operation
- blue cooling airflow
- orange warm airflow if cold/warm product
- sleep/quiet mode room
- desk, sofa, bedroom, kitchen, rental apartment scenes
- product hero shot + CTA

## Claim Safety

For paid ads, avoid hard factual claims unless verified:
- exact room coverage
- exact temperature output
- exact savings
- “number one”
- review counts
- medical/safety guarantees

Safer phrasing:
- “helps cool your space”
- “portable comfort”
- “no drilling”
- “plug in and use”
- “cool and warm modes”
- “designed for small rooms / personal spaces”

## Storyboard Image Prompt Requirements

Use this structure:
- Single complete storyboard board.
- 3 modules: top project overview, core storyboard grid, bottom technical notes.
- Grid: 4x2 for 7 shots plus one product lock/reference panel.
- Minimal text labels, no long paragraphs.
- Realistic commercial photography, bright natural light, clean background.
- Must preserve product identity.
- Use air-conditioner-relevant scenes unless the user requests another category later.

## Prompt Templates

Use `references/prompt-templates.md` for copy-ready templates covering:
- Intake question.
- Script + storyboard generation.
- Storyboard image generation.
- Final video generation.
- Negative prompt.
- Optional video API payload.

## Final Response Format

Keep final concise:
- Link or display the storyboard image if generated.
- Link to saved script/prompt files if saved.
- Include or point to the storyboard image prompt, final video prompt, and negative prompt.
- If video generation was requested, include the generated video path/link or the exact API-ready payload if generation was unavailable.
- Do not over-explain the process; the useful handoff is “upload these references, use this prompt”.

When saving locally, use the project’s existing folders if present:
- `视频脚本/` for prompts and scripts.
- `产品相关/` for product notes.
- `对标视频拆解/` for competitor breakdowns.
- Generated images remain in the generated image output folder unless the user asks to copy them.
