# Prompt Templates

Use these templates as starting points. Fill placeholders from product images, product notes, competitor breakdowns, and user requirements.

## 1. Intake Question

```text
这是空调还是 CoreGLP？要做几秒？有没有指定创意/卖点/语言/地区/禁止内容？
需要我只交付“分镜图 + 视频提示词”，还是也尝试生成视频/API payload？
没有的话我按 TikTok 9:16、8-10 秒、强钩子带货节奏来做。
```

## 2. Context Summary Template

```text
产品线：
- AC line / CoreGLP line：

产品锁定：
- 商品外观：
- 颜色/材质：
- 关键结构/包装：
- LOGO/标识/包装：
- 标签/可见文字：
- 其他配件：
- 必须避免改变：

核心卖点：
- 主痛点：
- 使用场景：
- 产品动作：
- 情绪转变：
- 转化利益点：
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
- 合规边界：
```

### AC Product Context Add-on

```text
空调锁定：
- 机身外观：
- 控制面板/LED 显示区：
- 出风口/进风口/格栅：
- 电源线/插头：
- 遥控器：
- 挂架/支架/安装结构：
- 冷风/暖风视觉状态：

空调卖点：
- 免安装/Plug & Play：
- 制冷/冷风：
- 制热/暖风：
- 遥控/触控：
- 静音/睡眠：
- 便携/租房友好：
- 节能/低耗：
```

### CoreGLP Product Context Add-on

```text
CoreGLP 锁定：
- 透明/磨砂瓶身：
- 深墨绿色圆盖：
- 青绿色渐变标签：
- CoreGLP 大字：
- 红色 METABOLIC BALANCE 横条：
- Fat burn / Digestion / Vitality 图标文字：
- 30 CAPSULES / DIETARY SUPPLEMENT / SCIENTIFIC FORMULA：
- 腰腹卷尺线稿：
- 胶囊、水杯、手部、日历等道具：

CoreGLP 卖点/创意：
- 睡前 routine：
- 代谢平衡支持：
- 消化/活力支持：
- 40+ 或成年女性生活方式：
- UGC 真实口播：
- 日历打卡/习惯坚持：
- 自信穿搭/镜前状态：

CoreGLP 合规边界：
- 不使用具体 kg/lbs 减重承诺：
- 不使用 one week / 3 days / 1 month 等强结果承诺：
- 不使用医生背书、临床、无副作用、疾病治疗、GLP-1 替代：
- 不把产品和明显身材变化做直接因果绑定：
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
- 10 秒以内默认 6-10 个动作级镜头；12-15 秒默认 10-16 个动作级镜头。
- 先判断产品线并采用对应节奏：
  - AC line：炎热/寒冷痛点钩子 -> 免安装/插电/挂墙 -> 遥控或触控开机 -> 冷风/暖风功能证明 -> 舒适反应 -> 转化收口。
  - CoreGLP line：身材/习惯/routine 痛点钩子 -> 产品瓶身/睡前 routine -> 胶囊+水/日历打卡/健康生活动作 -> 更轻松自信的生活方式 payoff -> 产品定格/CTA。
- 每个镜头必须写清时间、画面、动作、运镜、字幕/口播、目的。
- 产品必须始终保持同一件商品。
- 严格锁定产品外观、颜色、材质、LOGO/标识、标签文字、配件、比例和所有可见细节。
- AC line 还必须锁定控制面板、LED 显示区、出风口/进风口、格栅、电源线、遥控器、挂架/支架。
- CoreGLP line 还必须锁定透明/磨砂瓶身、深墨绿色盖子、青绿色标签、红色 `METABOLIC BALANCE` 横条、`CoreGLP` 字样、腰腹卷尺图形、胶囊和水杯等道具比例。
- 对标视频只学习结构、节奏、转场、钩子和转化路径，不照抄原视频人物、品牌、商品、文案和具体画面。
- 不得编造未提供或不可见的功能、认证、价格、销量和效果。
- CoreGLP line 不得输出具体减重数字、极端前后对比、疾病/药物/GLP-1 替代表达、医生背书、临床证明、无副作用承诺，除非用户提供合规批准文本。
- 输出适合直接复制给图片模型和视频模型使用。

产品信息：
{{productContext}}

产品图/细节图说明：
{{productImageNotes}}

产品锁定：
{{productLock}}

核心卖点：
{{sellingPoints}}

合规边界：
{{claimSafety}}

对标视频拆解：
{{competitorReferences}}

用户创意/要求：
{{creativeDirection}}
```

## 4. Storyboard Image Prompt

```text
生成一张专业电商视频制作导演分镜流程图，用于 {{duration}} 秒 {{aspectRatio}} TikTok 竖屏广告。必须是单张完整图片，不是多张独立图片。整张分镜总览图比例可根据内容管理需要自适应，但每一个镜头框必须是清晰的 9:16 手机竖屏画面。

参考图用途：
- 产品图/拆解图是商品一致性依据。
- 分镜内容是画面结构依据。

完整排版分为 3 大模块：
1. 顶部项目总览栏。
2. 核心分镜表格。
3. 底部专业技术规范栏。

核心分镜区为 {{grid}} 排版，共 {{shotCount}} 个镜头；每个镜头必须放在独立 9:16 手机竖屏画框里，不要画成横向卡片。整张总览图可以为竖版、方版或宽版，以便排版清晰。如有空余格，用作产品锁定参考。

商品一致性要求：
{{productLock}}

产品尺度要求：
- 产品与手、沙发、桌面、床、墙面和人物之间的比例必须真实可信。
- 近景可以放大细节，但必须明确是微距/特写，不能让商品整体尺寸看起来异常巨大。
- AC line：放置在沙发旁、桌面旁或卧室场景时，保持便携小空调/紧凑空调的合理尺寸。
- CoreGLP line：放置在手中、床头柜、厨房台面、水杯旁或包里时，保持真实膳食补充剂瓶尺寸；不要把瓶身放大成水壶或改成其他品牌。

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
- 每个镜头框为 9:16 竖屏构图。
- 转场干净。
- 动作克制并服务商品展示。
- CoreGLP line 不做夸张身材变形，不做直接医疗机制图，除非用户明确要概念动画且合规允许。

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

合规边界：
{{claimSafety}}

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
- CoreGLP line：可以展示产品作为日常 routine 的一部分，但不要表现为服用后立即改变体型；避免具体减重数字、疾病、药物替代和夸张 before/after。

负面提示词：
{{negativePrompt}}
```

## 6. Negative Prompt Template

### AC Negative Prompt

```text
空调机身变形，产品颜色改变，材质改变，比例错误，控制面板位置错误，控制面板消失，LED 显示区错乱，出风口消失，出风口形状改变，格栅变形，电源线消失，遥控器变形，LOGO/标识错乱，多个不同空调，额外品牌，复杂安装，打孔施工，电钻，未提供的水箱/排水管/软管，未提供的配件，未提供的功能，脏乱背景，低画质，粗糙 3D 模型，动漫风格，夸张科幻特效，乱码文字，水印，人物变脸，手指畸形，字幕遮挡商品。
```

### CoreGLP Negative Prompt

```text
产品瓶身变形，瓶盖颜色改变，透明瓶身消失，青绿色标签改变，CoreGLP 字样错乱，METABOLIC BALANCE 红色横条消失，腰腹卷尺图案改变，胶囊形状错误，多个不同品牌补充剂，额外药品品牌，乱码标签，虚假医生背书，医院诊疗场景，针剂药物，Ozempic/Wegovy/Mounjaro 暗示，GLP-1 药物替代，疾病治疗画面，极端前后身材变形，具体减重公斤或磅数，one week miracle，夸张马甲线突变，厌食或疾病暴瘦，未成年人，孕妇，脏乱背景，低画质，粗糙 3D，手指畸形，面部变形，字幕遮挡产品。
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
