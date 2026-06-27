# Prompt Templates

Use these templates as starting points. Fill placeholders from product images, product notes, competitor breakdowns, and user requirements.

## 1. Intake Question

```text
要做几秒？有没有指定创意/卖点/语言/地区/禁止内容？
需要我只交付“分镜图 + 视频提示词”，还是也尝试生成视频/API payload？
没有的话我按 TikTok 9:16、8-10 秒、强钩子带货节奏来做。
```

## 2. Context Summary Template

```text
产品锁定：
- 空调机身外观：
- 颜色/材质：
- 控制面板/LED 显示区：
- 出风口/进风口/格栅：
- 电源线/插头：
- 遥控器：
- 挂架/支架/安装结构：
- LOGO/标识/包装：
- 其他配件：
- 必须避免改变：

核心卖点：
- 免安装/Plug & Play：
- 制冷/冷风：
- 制热/暖风：
- 遥控/触控：
- 静音/睡眠：
- 便携/租房友好：
- 节能/低耗：
- 其他：

对标结构：
- 开头钩子：
- 镜头节奏：
- 转化路径：
- 可借鉴但不能照抄：

投放要求：
- 时长：
- 画幅：
- 语言/地区：
- 视频模型：
- 禁止内容：
```

## 3. Script + Storyboard Generation Prompt

```text
你是 TikTok 带货短视频导演兼专业分镜师。请基于以下产品信息、参考图、卖点、对标拆解和投放要求，同时生成脚本、分镜头提示词、分镜图提示词、视频生成提示词和负面提示词。

输出必须包含：
1. 项目设定
2. 完整导演脚本
3. 分镜头脚本表格
4. 每镜头视频模型提示词
5. 分镜图生成提示词
6. 连续视频总提示词
7. 负面提示词

规则：
- 视频时长为 {{duration}} 秒，画幅为 {{aspectRatio}}。
- 10 秒以内默认 6-7 个镜头。
- 节奏采用空调类 TikTok 投放广告：炎热/寒冷痛点钩子 -> 免安装/插电/挂墙 -> 遥控或触控开机 -> 冷风/暖风功能证明 -> 舒适反应 -> 转化收口。
- 每个镜头必须写清时间、画面、动作、运镜、字幕/口播、目的。
- 产品必须始终保持同一件商品。
- 严格锁定空调机身外观、颜色、材质、控制面板、LED 显示区、出风口/进风口、格栅、LOGO/标识、电源线、遥控器、挂架/支架、配件、比例和所有可见细节。
- 对标视频只学习结构、节奏、转场、钩子和转化路径，不照抄原视频人物、品牌、商品、文案和具体画面。
- 不得编造未提供或不可见的功能、认证、价格、销量和效果。
- 输出适合直接复制给图片模型和视频模型使用。

产品信息：
{{productContext}}

产品图/细节图说明：
{{productImageNotes}}

产品锁定：
{{productLock}}

核心卖点：
{{sellingPoints}}

对标视频拆解：
{{competitorReferences}}

用户创意/要求：
{{creativeDirection}}
```

## 4. Storyboard Image Prompt

```text
生成一张专业电商视频制作导演分镜流程图，用于 {{duration}} 秒 {{aspectRatio}} TikTok 竖屏广告。必须是单张完整图片，不是多张独立图片。

参考图用途：
- 产品图/拆解图是商品一致性依据。
- 分镜内容是画面结构依据。

完整排版分为 3 大模块：
1. 顶部项目总览栏。
2. 核心分镜表格。
3. 底部专业技术规范栏。

核心分镜区为 {{grid}} 排版，共 {{shotCount}} 个镜头；如有空余格，用作产品锁定参考。

商品一致性要求：
{{productLock}}

顶部项目总览栏：
{{projectOverview}}

分镜内容：
{{shotList}}

底部专业技术规范：
- 真实商业摄影质感。
- 明亮自然光。
- 稳定透视。
- 浅景深。
- 快速但清晰的 TikTok 节奏。
- 转场干净。
- 动作克制并服务商品展示。

文字要求：
- 只使用极短标签或数字标注。
- 不得出现乱码、无意义文字、水印。
- 文字不得遮挡商品。

禁止事项：
{{negativePrompt}}
```

## 5. Final Video Prompt

```text
生成 {{duration}} 秒 {{aspectRatio}} TikTok 竖屏带货广告，{{style}}。

参考素材使用规则：
- 第一张参考图是分镜头结构依据，必须按分镜顺序生成视频。
- 产品图/拆解图是商品一致性依据。
- 对标视频只参考节奏、镜头推进和转化路径，不照抄人物、品牌、文案和具体画面。

产品锁定：
{{productLock}}

视频内容：
{{timedShotPrompt}}

画面要求：
- 真实商业摄影质感。
- 明亮自然光。
- 干净场景。
- 稳定透视。
- 转场利落。
- 产品始终清晰可辨认。
- 字幕简洁，不遮挡商品。
- 不要夸张科幻特效；功能气流或动效必须克制。
- 人物动作自然，不需要面对镜头口播，除非用户要求。

负面提示词：
{{negativePrompt}}
```

## 6. Negative Prompt Template

```text
空调机身变形，产品颜色改变，材质改变，比例错误，控制面板位置错误，控制面板消失，LED 显示区错乱，出风口消失，出风口形状改变，格栅变形，电源线消失，遥控器变形，LOGO/标识错乱，多个不同空调，额外品牌，复杂安装，打孔施工，电钻，未提供的水箱/排水管/软管，未提供的配件，未提供的功能，脏乱背景，低画质，粗糙 3D 模型，动漫风格，夸张科幻特效，乱码文字，水印，人物变脸，手指畸形，字幕遮挡商品。
```

## 7. API Payload Template

```json
{
  "prompt": "{{finalVideoPrompt}}",
  "negative_prompt": "{{negativePrompt}}",
  "reference_images": [
    "{{storyboardImageUrlOrPath}}",
    "{{productImageUrlOrPath}}",
    "{{detailImageUrlOrPath}}"
  ],
  "reference_videos": [
    "{{optionalCompetitorVideoUrlOrPath}}"
  ],
  "duration": {{duration}},
  "aspect_ratio": "{{aspectRatio}}",
  "resolution": "{{resolution}}",
  "audio": false
}
```

Provider mapping:
- Seedance / Seedance Mini: map `reference_images` to `reference_image_urls`; storyboard image first, product images after it.
- Providers without negative prompt support: merge the negative prompt into the main prompt as “禁止事项”.
- Providers without reference video support: omit `reference_videos` and keep competitor insights only in text.
