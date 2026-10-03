---
name: ink-satire-figures
description: "把主题、标题、判断或情节编译成「黑白讽刺画」生图提示词——传统中国连环画、小人书式单线白描，纯白纸面、纯黑墨线、严格九十度侧视、抽象符号化表情，朴拙幽默的市井人物。主题只决定人物身份、动作、道具和情节。用户提到黑白讽刺画、连环画风、小人书、白描人物、单线白描、市井漫画、讽刺漫画配图、传统中国人物漫画，或要为文章或社媒配一张传统中国人物漫画时使用。先转译核心动作再编译单条确定性提示词。不用于彩色插画、日式漫画、美式漫画、写实肖像、铅笔素描或照片。"
---

# Ink Satire Figures（黑白讽刺画）

把**一个主题或情节**编译成**一条**可直接交给图像模型的提示词。风格锁死：传统中国连环画（小人书）式单线白描，纯白纸面、纯黑墨线、严格九十度侧视、抽象符号化表情，人物带朴拙、幽默、轻微夸张的市井气质。

核心原则：**主题只换情节，不换画法。** 这套风格的全部辨识度来自四件事——白描一次成线、侧脸符号化、接触真实、纯黑白。任何把线画成素描排线、把侧脸转成正面、把互动画成并排摆放、让灰调爬进画面的冲动都要压住。

## 画幅

默认 3:4 竖版，出图参数 `1536×2048`、quality `high`。用户指定其他比例时遵循，这是 Composition 基座里唯一可改的一项：

| 场景 | 比例 | size |
|---|---|---|
| 文章/社媒配图（默认） | 3:4 | `1536×2048` |
| 方形社媒卡 | 1:1 | `2048×2048` |
| 横版内嵌 | 4:3 | `2048×1536` |

横向展开的双人互动、绳索拉扯、搬运或长道具，可以适当缩小人物，但动作关系必须清楚、四周留白必须充足——这些已经锁在 Composition 基座里，不用额外写。

## 锁死的风格内核

无论画什么内容，下面四段逐字进每一条提示词，不改写不精简。**成组产出时每一条都要重复**——模型只看得见单条，共享规则不会自动继承。只有 Composition 基座开头的画幅一项跟随比例设置变。

**Scene 基座**

```
flat opaque pure white paper background filling all four corners of the frame, completely blank; no environment, no architecture, no furniture, no landscape, no decorative patterns, no background figures; if the action needs context, keep only one or two instantly recognizable props directly tied to the core action, nothing else; five to eight short, loose black ground strokes of slightly uneven length directly under the figures' feet to suggest the ground.
```

**Key details 基座**

```
traditional Chinese lianhuanhua (pocket comic-book) style, single-line ink drawing; figures built from a few large continuous contour lines, with slightly oversized heads, simplified torsos and simplified limbs; each line drawn like one confident pass of a black brush or dip pen — outer silhouettes use medium-thick, clear, forceful black lines, while facial features, clothing folds and prop interiors use slightly thinner lines; lines are fluid and economical with a slight natural wobble and hand-drawn irregularity, never re-traced, never sketchy search lines, never smooth mechanical vector curves; edges stay sharp and crisp with no softening, no ink bleeding, no texture erosion; strict black-and-white: pure black ink lines, a few solid black fills and the pure white paper — no grey, no colour, no gradients, no shading, no hatching, no cross-hatching, no screentone dots, no grain, no paper texture, no brush noise, no ageing effects; faces are highly abstract and symbolic — the profile eye is a single short arc or a small black dot, the eyebrow a single short arc, the nose a simple hooked profile line, the mouth one short curve or a simple black-and-white shape, the ear carries only one or two summary lines inside; no realistic eyeballs, no eye bags, no teeth, no gums, no heavy wrinkles, no nostril detail, no skin texture, no sweat drops, no facial muscles; clothing is loose, generalized, mostly white, with at most one to three fold lines per sleeve, torso or trouser leg that only explain the direction of the action; no fabric realism, no dense cloth wrinkles, no stitching, no lighting, no volume on clothes; hands are simplified lianhuanhua symbols — the palm reads as one shape, fingers as a few short arcs that read the grip, support, push, pull, point or carry of the action; no fingernails, no knuckles, no palm lines, no tendons, no fingers fusing together, no palm floating next to a prop; solid black fills reserved for hair, shoes, the inside of an open mouth or one key visual anchor, while clothing and large props stay mostly white; mood: naive, humorous, mildly exaggerated, everyday-life folk satire.
```

**Composition 基座**

```
3:4 vertical; flat eye-level side observation, no bird's-eye view, no worm's-eye view, no wide-angle distortion, no dramatic perspective, no strong foreground-background scaling; the main figure or interacting group centered, occupying about 65% to 85% of the frame width and 75% to 88% of the frame height, with extra white space in front of the figure in the direction of the action; full-body framing — head, both hands, key props, contact points and both feet fully inside the frame, never cropped at wrists, fingers, elbows, knees, ankles or mid-prop; for wide two-figure interactions, rope pulling, carrying or long props the figures may sit slightly smaller, but the action relationship stays instantly readable and the white margins around all four sides stay generous.
```

**Constraints 基座**

```
no text, letters, numbers or symbols anywhere in the image; no modern western caricature grimaces, no realistic portraits, no real human anatomy, no muscle lines, no detailed facial anatomy, no dense wrinkles, no sweat drops, no explosion symbols, no dense action lines; no frontal or three-quarter faces — strict 90-degree side profiles only, each face shows exactly one eye, one eyebrow and one ear, never a second eye, a second brow or the other ear; no photographs, no 3D rendering, no anime, no manga, no western superhero comics, no fashion illustration, no smooth vector art, no pencil shading, no watercolour, no oil painting, no realistic sketching; no greyscale shading, no volume lighting, no gradients, no screentones, no hatching, no cross-hatching, no paper grain, no scan noise, no ageing texture; no dense interior detailing, no repeated outlines, no mechanical prop details that clash with the figure's line style; no complex backgrounds, no architecture, no furniture arrangements, no landscapes, no decorative borders, no titles, no captions, no speech bubbles, no text labels, no signatures, no seals, no logos, no watermarks; no transparent background — the background must be fully opaque, even pure white; no unrelated figures, no extra props, no extra arms, no extra hands, no extra fingers, no fused limbs, no floating props, no broken ropes, no ambiguous contact.
```

## 情节转译（把主题变成画面）

先把主题判定成一种情节，再决定人物配置。主题只提供人物身份、动作、道具和情节，风格由上面的基座全权接管。

| 情节类型 | 画面配置 | 要点 |
|---|---|---|
| 单人动作 / 劳作 | 一人侧视，朝向即动作方向，一件道具 | 核心动作一眼读懂 |
| 单人状态 | 一人侧视，靠轮廓与身体倾斜表态 | 状态靠姿态，不靠鬼脸 |
| 双人交接 / 对话 | 两人相向，中间递接物或手势，接触点画实 | 递接物两端都必须被手接触 |
| 双人同担 / 同行 | 两人同向，共同扛、抬、拉一件道具 | 四只手都落在道具上 |
| 双人对抗 / 拉扯 | 两人相向，绳索或物件居中，两端手部接触 | 绳要绷直，手要握住 |
| 搀扶 / 拥抱 | 两人身体接触，手扶肩、背或手臂 | 身体轮廓互嵌，接触位置明确 |
| 人与动物 | 一人加一只动物，视线或牵引关系 | 牵绳、喂食、抚摸的接触点画实 |

**朝向规则**：单人自由朝向，由动作方向决定；双人要么同向（共同目标），要么相向（交接、对话、对抗、拉扯），由情节关系决定。无论朝哪边，每张脸都只有一只眼睛、一侧眉毛、一个耳朵、侧面的鼻子——正面脸和四分之三脸一律不许出现。

**轮廓性格**：人物的性格必须先通过剪影和姿态被读懂。从轮廓里选一种，不追求真实人体比例：

| 性格 | 轮廓写法 |
|---|---|
| 圆胖 | 圆弧外轮廓、压缩头身比、凸出的肚子弧线 |
| 瘦长 | 竖长条轮廓、细长四肢 |
| 驼背 | 脊柱前弯大弧线、头前伸 |
| 挺直 | 竖直轴线、平肩 |
| 矮小 | 整体压缩、四肢短 |

**剪影测试**：把人物涂成纯黑剪影后，核心动作仍应能够辨认。写 Subject 之前先在心里过一遍这个测试。

**接触点铁律**：人物之间存在递交、搀扶、拥抱、推拉、争夺或共同搬运时，必须把关系画出来——双手、绳子、水流、篮子、工具或其他连接物必须准确接触，不能只把人物和物件并排摆放。Subject 段要写到「哪只手、碰哪件东西、接触位置在哪」，例如 `both hands grip the carrying pole in front of and behind the shoulder, the pole resting exactly on the shoulder`。

**道具**：最多两件，一眼能叫出名字，只保留识别所需的外轮廓和关键结构；复杂道具服从人物线稿的简化程度，不画机械纹理和密集结构线。

**黑块**：纯黑实心块只用于头发、鞋子、张开的嘴巴内部或一处关键视觉重心。每张图点名给谁。

## Input

从用户输入推断，不要求填表：

1. **主题**：人物身份、动作、道具或情节。一句话即可。
2. **比例**：默认 3:4，用户指定才换。
3. **单张 / 成组**：成组时先列清每张讲哪一段，避免两张讲同一件事。

## Workflow

1. **读主题** → 判定情节类型（单人动作 / 双人互动 / 人物与动物），查情节转译表。
2. **定核心动作**：一句话说清这个动作，必须能一眼读懂。
3. **定人物配置与朝向**：一至两名主要人物，只在主题确实需要时加入一只动物或一个关键道具；朝向由情节定。
4. **定轮廓性格**：从圆胖 / 瘦长 / 驼背 / 挺直 / 矮小里选一种，做剪影测试。
5. **定接触点**：手与手、手与道具、连接物的接触位置写到具体。
6. **定道具与黑块**：道具≤两件、一眼叫名；点名黑块给头发 / 鞋子 / 嘴内 / 重心。
7. **按七槽编译**：`Use case → Scene → Subject → Key details → Composition → Text in image → Constraints`，四段基座逐字照抄，只写 Subject。铁律和骨架见 `references/compile-contract.md`。
8. **输出**：决策摘要 + 一条完整提示词 + 一句转译理由。用户只要 prompt 时省略解释。

## Output Format

````markdown
## 已定决策
- 情节类型：
- 人物配置与朝向：
- 轮廓性格：
- 接触点：
- 道具：
- 黑块：
- 比例：

## 完整提示词
```text
...
```

## 转译理由
...
````

## Quality Gates

- **严格侧脸**：每张脸一睛、一眉、一耳，无正面、无四分之三。侧脸画出第二只眼睛或另一侧眉毛，即失败。
- **剪影可读**：人物涂黑后核心动作仍可辨认。剪影读不出动作，先改姿态再写。
- **纯黑白**：黑线、黑块、白纸，无灰、无彩、无渐变、无网点、无排线、无颗粒、无纸纹。出图发灰即失败。
- **白底不透明**：背景是不透明均匀纯白，四角纯白，无透明区域。
- **接触真实**：手与道具接触、绳不断、担不悬空。人物和物件并排摆放等于没画关系。
- **全身入镜**：头、双手、关键道具、接触位置、双脚完整入镜，不在手腕、手指、肘、膝、脚踝或道具中间裁切。
- **画面零文字**：无标题、说明、对白框、标签、签名、印章、标志、水印。
- **一次成线**：不重复描边、不出现草稿搜索线、不成光滑矢量曲线。
- **风格禁入**：无照片、3D、动漫、日漫、美漫、时尚插画、矢量、铅笔素描、水彩、油画、写实速写。
- 本 skill 只产出提示词，不编造已生成的图片结果。

## Read

- 编译契约（铁律 + 成品骨架）：`references/compile-contract.md`
- 转译示例（决策表 + 成品 prompt）：`references/examples.md`
