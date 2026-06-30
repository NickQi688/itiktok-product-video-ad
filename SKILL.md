---
name: tiktok-product-video-ad
description: "Use when the user wants to create TikTok video ad assets for supported products from product images, selling points, landing pages, or competitor video breakdowns. Current supported product lines: portable/wall-mounted air conditioners and accessories; CoreGLP metabolic-balance dietary supplement. Works across agents with or without image/video generation tools: ask for duration, creative idea, requirements, references, and product line when missing, then produce a storyboard prompt or image, final video prompt, negative prompt, and optional API-ready video payload or generated video."
---

# TikTok Product Video Ad

## Purpose

Turn supported product images, product features, and competitor references into a ready-to-generate TikTok ad package.

Current product lines:
- **AC line**: portable AC, wall-mounted mini AC, cooling/heating units, fans with cooling claims, AC deflectors, AC cleaning/maintenance products, and related accessories.
- **CoreGLP line**: CoreGLP / CoreGLP Metabolic Balance dietary supplement, 30-capsule bottle, German TikTok health/weight-management creative direction.

When the user provides competitor-video breakdowns or product notes, first classify the product line yourself from the content. Put AC-related material into the AC line and CoreGLP / weight-management supplement material into the CoreGLP line. Ask only when the content truly cannot be classified. Do not broaden into other categories unless the user explicitly asks to extend the skill.

Default deliverables should be:
- A storyboard image prompt.
- A storyboard image, when image generation is available or requested.
- A final video generation prompt.
- A negative prompt.

Optional deliverables:
- Generated video, only when the user explicitly asks for video production and an API/tool is available and configured.
- API-ready payload when no video API/tool is available.

Hard safety rule for paid video APIs:
- Never create a video generation task without explicit user confirmation in the same turn.
- Preparing prompts, reference lists, and API payload drafts is safe and does not require confirmation.
- Submitting to any paid video endpoint must be treated as credit-spending and requires a final confirmation after showing model, duration, resolution, audio setting, reference assets, and payload summary.
- If the user provides API keys or asks to “connect” video models, do not assume permission to spend credits.

Optionally save deliverables into the user's project folders when working in a local workspace.

## Start-of-Task Intake

At the start, ask only what is missing and necessary. If the user already provided enough context, proceed.

Required or strongly preferred:
- Product line: infer automatically from the content whenever possible. If it is AC, cooling/heating, fan, air conditioner accessory, installation, airflow, compressor, remote temperature, plug-in cooler, or heatwave cooling content, route to AC line. If it is CoreGLP, metabolic balance, supplement bottle, capsule routine, weight-management, body confidence, calendar routine, or fat/metabolism creative content, route to CoreGLP line. Ask only if classification remains genuinely unclear.
- Duration: default to 8-10 seconds if absent.
- Aspect ratio: default to 9:16 for TikTok.
- Product images: product/detail/exploded-view images used to lock identity.
- Product selling points: use provided notes, landing page extraction, or visible product details.
- Creative direction: ask if they have an idea; otherwise generate one from product + references.
- Requirements: target country/language, mandatory text, forbidden claims, model name.
- Reference videos or breakdowns: use them for structure, pacing, hooks, and transitions only.
- Video production: ask only if relevant; default is prompt/storyboard handoff, not API generation.
- Credit protection: if video API generation is requested, tell the user no video task will be created until they confirm the exact model and payload.

Good concise question when context is missing:
“这是空调还是 CoreGLP？要做几秒？有没有指定创意/卖点/语言/禁止内容？需要我只交付分镜图+视频提示词，还是也尝试生成视频？没有的话我按 TikTok 9:16、8-10 秒、强钩子带货节奏来做。”

## Workflow

Before generating deliverables, load the reusable prompt templates in `references/prompt-templates.md` when the task requires any concrete script, storyboard, image prompt, video prompt, or API payload.

1. Gather context
   - Inspect product images if provided.
   - Read product notes, landing-page extracts, and existing competitor breakdowns.
   - Identify product line and stable product identity. Use the product-specific lock checklist below.
   - Flag unsupported claims as “page claim / needs verification”.

2. Choose ad structure
   - AC line: use a direct TikTok sequence: pain hook -> instant setup -> feature proof -> emotional payoff -> conversion close.
   - CoreGLP line: use a health/lifestyle sequence: relatable body/routine pain hook -> product/routine introduction -> simple daily action -> habit/progress proof -> confidence/lifestyle payoff -> conversion close.
   - Keep scenes simple and model-friendly.
   - Use competitor videos for pacing and shot logic, not for copying brand, people, exact text, or exact scene.

3. Generate script and storyboard prompt together
   - Do not make the user wait for a separate script pass unless requested.
   - Treat script, storyboard prompt, final video prompt, and negative prompt as one generation batch.
   - Produce an action-level shot table with time, visual, action, camera, text/audio, and purpose.
   - Split by action nodes, not by broad story beats. Each shot should carry one main action. AC examples: place product, plug in, press panel, display lights up, airflow starts, paper moves, person reacts, remote click, CTA. CoreGLP examples: look at mirror/clothes, place bottle, open cap, pour capsule, drink water, mark calendar, prepare healthy food, confident outfit moment, hero bottle CTA.
   - Produce per-shot video prompts for precise generation.
   - Produce one continuous video prompt.
   - Produce one storyboard image prompt.
   - Save intermediate script/prompt files when a workspace structure exists, but keep the user-facing handoff focused on the storyboard image and video prompt.

4. Generate storyboard image
   - Always produce a storyboard image prompt.
   - If image generation is available and the user wants or implies a storyboard image, call image generation.
   - If image generation is unavailable, give the storyboard prompt clearly so the user or another agent can generate it elsewhere.
   - Use the product image as identity reference in the prompt text: lock exact product shape, color, material, logo/label, visible functional parts, accessories, and proportions.
   - For CoreGLP, lock bottle shape, cap color, transparent/frosted bottle, teal label, red `METABOLIC BALANCE` stripe, `CoreGLP` wordmark, waist-tape illustration, capsule count, and any visible capsules.
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
   - Before any video-generation API call, present a confirmation block and wait for the user to approve. Do not call the API based only on prior intent.
   - The confirmation block must include:
     - selected model/provider
     - endpoint/action that will create a paid task
     - duration
     - aspect ratio
     - resolution
     - whether audio generation is enabled
     - reference image count and reference video count
     - expected mode, such as text-to-video, first-frame image-to-video, first+last-frame image-to-video, multimodal reference-to-video
     - note that credits/points may be consumed
   - If a video-generation API/tool is available and the user confirms, use the generated storyboard image and product images as references.
   - For KIE.ai providers including omini / Gemini Omni, Seedance 2.0, Seedance 2.0 Fast, GPT Image 2 text-to-image, and GPT Image 2 image-to-image, use `scripts/kie_media.py` and `references/omini-api.md`. `scripts/omini_video.py` remains as a compatibility wrapper for omini.
   - If no API/tool is configured, deliver an API-ready payload outline instead of pretending the video was generated.
   - Keep provider-specific parameters isolated so they can be swapped later.
   - Preserve the final prompt as the source of truth.

## Capability Matrix

Adapt to the current agent environment:

| Available capability | What to do |
| --- | --- |
| Text only | Produce script, storyboard image prompt, final video prompt, negative prompt, and optional API payload. |
| Image generation available | Generate the storyboard image and also include/save the storyboard prompt. |
| Video API/tool available | Generate the video only if requested; otherwise stop at prompt/storyboard handoff. For KIE.ai providers, use `scripts/kie_media.py`. |
| Neither image nor video tools available | Deliver prompts in a copy-ready format and explain which references to upload. |
| Another agent will continue | Save or present files with clear names: storyboard prompt, final video prompt, negative prompt, API payload. |

Never make a tool-specific step mandatory. The workflow must remain useful for Codex, Claude Code, browser-only agents, and API-only agents.

Video API confirmation rule:
- Even when a video API/tool is available, default to producing only the API-ready payload.
- Only submit the task after the user confirms with an explicit approval such as “确认生成”, “可以消耗积分生成”, “run this video generation”, or equivalent.
- If there is any ambiguity, ask again instead of submitting.

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
- Bytedance Seedance 2.0 Fast: use model `bytedance/seedance-2-fast` with `/api/v1/jobs/createTask`. Supports text-to-video, first-frame image-to-video, first+last-frame image-to-video, and multimodal references, but those scenarios are mutually exclusive. Use `duration` 4-15 seconds, `aspect_ratio` such as `9:16`, `resolution` such as `720p`, and default `generate_audio: false` unless the user explicitly confirms audio because audio can increase cost.
- Bytedance Seedance 2.0: use model `bytedance/seedance-2` with `/api/v1/jobs/createTask`. Same mode separation and confirmation requirements as Fast; use it when quality is preferred over speed.
- Gemini Omni Video: use model `gemini-omni-video` with `/api/v1/jobs/createTask`. It accepts `image_urls`, `video_list`, `audio_ids`, `character_ids`, `duration`, `aspect_ratio`, `resolution`, and `seed`. Respect the quota rule: image = 1 unit, video = 2 units, character ID = 1 unit, total ≤ 7. Show this quota calculation in the confirmation block before submitting.
- Seedance / Seedance Mini: storyboard image first in `reference_image_urls`; product images after it; competitor videos in `reference_video_urls` if supported.
- Gemini-style video models: use storyboard/product images as image references and optional reference video list if supported. For Gemini Omni, place storyboard image first in `image_urls` and product/detail images after it. For KIE.ai providers, keep the API key in `KIE_API_KEY` or `OMINI_API_KEY`, not in project files.
- Other providers: keep storyboard first, product identity references second, and avoid adding unsupported fields.

Video API payload examples:

```json
{
  "model": "bytedance/seedance-2-fast",
  "input": {
    "prompt": "final video prompt",
    "reference_image_urls": ["storyboard image first", "product image second"],
    "generate_audio": false,
    "resolution": "720p",
    "aspect_ratio": "9:16",
    "duration": 8
  }
}
```

```json
{
  "model": "gemini-omni-video",
  "input": {
    "prompt": "final video prompt",
    "image_urls": ["storyboard image first", "product image second"],
    "duration": "8",
    "aspect_ratio": "9:16",
    "resolution": "720p"
  }
}
```

## Default TikTok Ad Pattern

For 8-10 second ads, use 8-12 action-level shots. Pick the product-line version.

AC line:

1. Pain hook
2. Pain proof/detail
3. Product enters
4. Product placement or mounting
5. Plug/power connection
6. Touch panel or remote operation
7. Display/indicator response
8. Airflow starts
9. Airflow proof, such as paper/curtain movement
10. Human comfort reaction
11. Secondary feature or mobility proof
12. Hero product + CTA

CoreGLP line:

1. Body/routine pain hook
2. Pain proof/detail, such as clothes, mirror, low energy, or inconsistent routine
3. Product enters
4. Bottle/label close-up
5. Open cap or pour capsule
6. Drink with water
7. Calendar/routine/healthy habit proof
8. Confident lifestyle or outfit payoff
9. UGC hand-held bottle or desk hero
10. CTA

For 12-15 second ads, use 12-18 action-level shots. Keep each shot visually distinct. Avoid cramming multiple product actions into one shot. If stable video generation is the priority, use more shots with fewer actions per shot instead of fewer shots with combined actions.

## Product Line Patterns

### AC Line

Use when the product is a portable/wall-mounted air conditioner, cooling/heating unit, fan, AC accessory, or cleaning/maintenance product.

Common AC ad scenes:
- overheated room or weak fan pain hook
- plug in / no drilling / no installation
- touch panel or remote operation
- blue cooling airflow
- orange warm airflow if cold/warm product
- sleep/quiet mode room
- desk, sofa, bedroom, kitchen, rental apartment scenes
- product hero shot + CTA

### CoreGLP Line

Use when the product is CoreGLP / CoreGLP Metabolic Balance.

Core product identity:
- transparent/frosted plastic supplement bottle
- dark teal/green round cap
- teal/green gradient label
- large cream/white `CoreGLP` wordmark
- red/coral `METABOLIC BALANCE` stripe
- label icons/text may include `Fat burn`, `Digestion`, `Vitality`, `30 CAPSULES`, `DIETARY SUPPLEMENT`, `SCIENTIFIC FORMULA`
- waist/measurement-tape line illustration on the label
- capsules visible inside bottle when applicable

CoreGLP usable creative structures:
- bedtime routine: bottle + water + capsule + nighttime table
- 40+ or adult women’s lifestyle routine: mirror/clothes frustration -> simple evening routine -> calmer morning/confident outfit
- UGC testimonial style: woman holds bottle and explains why she changed her routine
- calendar/progress style: Day 1 / Day 30 / routine marks, without hard weight-loss guarantees
- healthy habit montage: drink water, light meal prep, walk, mirror confidence, product hero
- product dossier style: bottle, cap, capsules, label close-up, hands holding bottle, water glass

CoreGLP competitor structures that can be borrowed:
- jeans/clothes not fitting as a pain hook
- old-photo or album contrast
- simple routine proof: pour capsule, drink water, mark calendar
- confidence payoff: outfit try-on, mirror smile, leaving home
- UGC single-camera rant energy, but without disease or extreme weight-loss claims
- abstract capsule/routine animation, but avoid medical mechanism certainty

CoreGLP compliance defaults:
- Treat all weight-loss, fat-burn, GLP, before/after, “one week”, exact kg/lbs, doctor endorsement, clinical, no-side-effect, disease, hormone, visceral-fat, and drug-comparison claims as unsupported unless the user provides approved claims.
- Prefer softer language: “daily routine”, “metabolic balance support”, “digestion/vitality support”, “wellness routine”, “helps me stay consistent”, “part of my evening routine”.
- Do not imply CoreGLP is a medicine, GLP-1 drug, diabetes/obesity treatment, Ozempic/Wegovy/Mounjaro alternative, or guaranteed fat-loss solution.
- Avoid direct causality between taking a capsule and visible body transformation. Show product as part of a broader routine.
- Avoid minors, pregnancy, eating disorder framing, shame-based body messaging, disease-based weight loss, extreme before/after, and unrealistic timeframes.

## Product Lock Rules

Every output must include product consistency rules:
- Same product in every shot.
- Do not change exterior shape, color, material, structure, logo/markings, label layout, accessories, or proportions.
- Do not invent hidden features, ingredients, accessories, certifications, functions, badges, claims, or mechanisms unless visible or provided.
- If reference images conflict, prioritize the clearest product/detail/exploded-view image.
- If using visual effects, keep them subtle and product-line appropriate: AC airflow should not become sci-fi; CoreGLP wellness/routine visuals should not become medical-treatment effects.

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

CoreGLP-specific lock checklist:
- bottle silhouette and size relative to hand/water glass
- dark teal/green cap
- frosted/transparent bottle with visible capsule mass
- teal/green label color
- `CoreGLP` wordmark
- red `METABOLIC BALANCE` stripe
- waist/measurement-tape illustration
- label claims/icons only if visible or provided
- capsule color/shape if shown
- water glass, capsule, calendar, handbag, bathroom/bedroom/kitchen lifestyle props only when relevant

## Claim Safety

For paid ads, avoid hard factual claims unless verified:
- exact room coverage
- exact temperature output
- exact savings
- “number one”
- review counts
- medical/safety guarantees
- exact weight loss or body transformation
- exact timeframes such as “one week” or “3 days”
- doctor/professor/authority endorsements
- disease, hormone, visceral fat, appetite suppression, GLP-1, or drug replacement claims

Safer phrasing:
- “helps cool your space”
- “portable comfort”
- “no drilling”
- “plug in and use”
- “cool and warm modes”
- “designed for small rooms / personal spaces”
- “part of my evening routine”
- “metabolic balance support”
- “daily wellness routine”
- “supports digestion and vitality” only if product label/approved claims allow it
- “routine over crash diets”

## Storyboard Image Prompt Requirements

Use this structure:
- Single complete storyboard board.
- 3 modules: top project overview, core storyboard grid, bottom technical notes.
- Each shot must be drawn inside an individual 9:16 phone-frame panel, not a horizontal card.
- The overall storyboard board canvas may be portrait, square, or wide as needed for readability and management.
- Use a clean phone-frame contact sheet; prioritize correct 9:16 shot framing inside each panel over forcing the whole board to be 9:16.
- If a board contains multiple shots, each mini-frame should visibly preserve 9:16 proportions.
- Minimal text labels, no long paragraphs.
- Realistic commercial photography, bright natural light, clean background.
- Must preserve product identity.
- Use product-line-relevant scenes.
- Preserve realistic product scale relative to hands, sofa, desk, bed, wall, table, water glass, bag, and people.
- AC: do not make the unit unusually large or tiny. CoreGLP: do not make the bottle unusually large, rewrite the label, or turn it into a different supplement brand.

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
- `对标视频拆解-CoreGLP 产品/` for CoreGLP competitor breakdowns when that folder exists.
- Generated images remain in the generated image output folder unless the user asks to copy them.
