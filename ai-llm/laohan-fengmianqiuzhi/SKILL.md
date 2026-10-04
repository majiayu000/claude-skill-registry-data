---
name: laohan-fengmianqiuzhi
version: 1.19.0
description: 根据真人AI口播稿和 Jeffrey 身份参考图，按文案冲突选择1个最匹配模板，生成1张9:16视觉母版，并产出3:4/4:3/16:9三张真实尺寸封面，共享到四平台7个逻辑入口。Use when 用户说“生成封面提示词”“做封面”“封面”“封面图”“封面词”或工作流进入⑥。
---

# 真人口播封面直接生成

目标：从口播稿提炼一个跨平台可成立的点击钩子，只使用秋芝方向，按文案冲突选择1个最匹配模板，直接生成1张“人物＋场景＋准确中文标题”的9:16视觉母版，再以同一视觉主张按真实画布重新构图生成3张真实尺寸封面（3:4/4:3/16:9），共享到四平台7个逻辑入口。三个比例必须分别重新构图和生成，不把裁切或发布页临时取景当成适配。不要拆成无字底图、排字脚本、评分器或多阶段合成。

## 输入与边界

- `episode-config.schema_version` 为4；身份reference或稿件绑定不满足时停止，不自行改合同。
- 读取当前 `01-口播稿.md`、`12-发布/多平台发布内容.md`和锁定的抖音发布信息。
- 人物参考固定为本期 `05-封面/reference/jeffrey-reference.jpg`，并作为 image reference 传给生图模型。
- ⑥先生成3张9:16完整候选，再为默认01生成3张共享真实尺寸封面；Jeffrey明确改选02或03时，⑫前必须为新rank重新生成这3张，旧rank成品不能混用。不允许简单裁掉人物、主物件或标题。
- 不在 prompt 中写“模仿某博主风格”。只使用 `references/douyin-cover-study.md` 的秋芝观察和 `references/qiuzhi-template-library.md`。
- 默认只生成3个秋芝方向候选；拉斐尔和柱子哥方向暂不进入默认输出。
- 三张按推荐程度从高到低排列为`01 → 02 → 03`。没有Jeffrey明确改选时，后续发布自动化优先使用`01`作为发布封面的源候选。

## 执行

### 1. 提炼封面文字

从口播稿提炼：

- `主标题`：4—10个汉字，最多两行；保留真正影响理解的产品名。
- `辅助短句`：0—8个汉字；主标题已经说清楚时不要添加。
- `画面事件`：Jeffrey正在做什么，他面对什么具体问题或结果。

禁止“AI神器”“效率翻倍”等可套用到任何选题的空话。封面文字不能超出口播稿事实。

### 2. 选择1个最匹配的秋芝模板

完整读取 `references/douyin-cover-study.md` 的秋芝部分和 `references/qiuzhi-template-library.md`，先按口播核心冲突筛选模板。

1. 先在内部筛出语义最匹配的5—8个模板。
2. 最终选择**1个**语义最命中本期钩子的模板；输出为单张封面（v1.19起不再产出3张排序候选）。
3. 遵守`1个基础模板 + 最多1个主物件机制`。
4. 上一期已用过的模板族原则上避免重复（防重复规则）。
5. 禁止凭“AI感”默认选择宇航员、驾驶舱、未来办公室或实验室；`CONDITIONAL_ONLY`仍只在语义明确匹配时使用。

每条提示词都必须一次性描述：

1. 9:16抖音完整封面；
2. Jeffrey的身份、位置、表情、动作和服装；
3. 与本期直接相关的一个主场景或主物件；
4. 主标题和可选辅助短句的准确原文、断行、位置、颜色、粗黑描边；
5. 该方向对应的版式规律；
6. 禁止错字、多余文字、平台UI、水印、二维码、额外人物和无关装饰。

## 2.5 生成前身份分析（v1.17，源自老韩AI产品DH Cover v4）

固定身份约束句已废弃。生成前必须先用视觉模型分析本期 `jeffrey-reference.jpg`，**动态提取**真实可见特征写进每条提示词：脸型、发型、眼镜款式、胡须形态、痣位置、肤色、当前着装、神态。禁止再写"参考照片中的同一位真人"作为唯一身份描述。身份分析特征随参考图更换而更新，不得跨期复用旧描述。

**面部保真红线（Jeffrey 2026-09-20）**：头部必须photoreal原样保留reference照片的真实皮肤纹理、毛孔与五官结构，禁止Q版化、3D风格化、磨皮或任何变脸；提示词须显式写明"face rendered photorealistic exactly as the reference photo, real skin texture, no beautification, no stylization"。可变项仅有：服装、表情、动作、场景、道具、头身配比。
**大头感的唯一合法来源=身体缩小**：头部保持自然真实比例与形状（禁面部变宽、变大、五官放大、漫画化），Q版反差全部由3D身体的缩小实现。

## 2.6 单张画面合同（v1.17，源自DH Cover v4）

- **比例硬合同**：头顶到下巴占画面高度16%—26%，人物总体占48%—72%；近景腰部以上英雄镜头，禁止全身或人物缩在底部。
- **表情张力条款**：表情必须具有惊讶、兴奋、笃定或质疑等明确张力；**普通微笑或放松站立不合格**。
- **动作短语合同**：人物动作写成4—40字完整短语，且包含托举、打开、操作、检验、指向或对抗之一，不能只写"操作"。
- **版式不固定**：由所选模板指定近景广角、低机位、强透视或主物件前伸；不固定"人物下半部+顶部横排"。
- **冷暖对比**：至少形成冷暖或明暗两种强对比主题色，人物和主物件有明确轮廓分离；禁止整张单一蓝色、拼贴分区、孤立证件照、多个Jeffrey。
- **广告KV三件套（2026-09-20实拍对比得出，缺则只到秋芝的75%）**：①真人头边缘加暖金色glow镶边（把真脸"焊"进3D场景的接缝隐藏术）；②人物周围环绕3-4个小发光3D挂件（主题元素，填满人物周围空间）；③整体高饱和亮泽finish（写明HIGH-SATURATION punchy colors, bright glossy finish），禁电影暗调。
- **光照与镜头通用合同（2026-09-20 S5验收遗漏审计补入，每张必带、与模板族无关——未写死的维度=AI随机）**：
  1. **人物三光系统**：a)主题物件发光染脸（写明光从哪个方向染在脸上，如"lure glow lighting his face from below-left"）；b)冷色rim light勾人物轮廓（"strong cool rim light outlining his silhouette"）；c)体积光god rays入画。三光缺一，人物就"平"。
  2. **前伸动作视角**：人物必须有一手/主物件**朝镜头前伸**（"toward the viewer/lifting toward the camera"），制造自拍式透视动感；禁止静态对称正面站桩构图。
  3. **挂件弧形布局**：环绕元素写明"in a loose arc around him, filling the space around him"；禁上下对称呆板分布。
  4. **氛围粒子**：dust particles/bubbles/light beams 至少其一。
  5. **饱和度普适**：任何题材（含noir/悬疑/危机暗色系）都保持HIGH-SATURATION与明度基准，只换色相，不降明度。

## 2.7 质量门禁（v1.17，字段化逐张复核）

每张生成后逐字段复核，任一为假即只改原提示词重生该张（每张最多重采2次）：
`exactTitle`（逐字符放大比对，含英文拼写）／`samePerson`／`singlePerson`／`faceProminent`（脸≥画面1/6）／`expressiveAction`／`expressionContrast`／`heroObjectClear`／`compositionIntegrated`／`thumbnailLegible`／`noExtraText`／`noWatermark`。

**文字错字教训（C07实录）**：已发布封面英文标题生成成"vibe coking"（应为coding），而人工复核记录误写"零错误"——AI画字错字率不可信人工粗看。所有文字必须放大逐字符检查，英文单词必须逐字母拼读比对。

## 2.8 秋芝2046真实样本观察（Jeffrey 2026-09-20提供9张桌面截图，最高赞50万）

- **大头Q版合成**：photoreal真人头（原脸）+ 3D卡通身体，头身比明显偏大头；不是全写实人。
- **超大3D错落标题**：黄/白字面+粗黑描边+硬阴影，部分字3D挤出；按语义层级错落排布（字有大小差），占上方1/3—1/2；中英混排（"AI 导演""Hermes 教程""抖音 Agent""超级豆包""Seed 2.1 实测""AI 短剧"）。
- **道具=标题的视觉翻译**：手持主物件朝镜头（电影放映机、发光手机、笔记本、魔法帽、平板）。
- **高饱和3D主题场景**：太空月球、雪山飞马、火箭发射、海滩、魔法舞台——每期换世界观，体积光+轮廓光。
- **人物居中大幅**：胸像/半身占40—60%，瞪眼张嘴惊喜表情直视镜头。
- **平台角标**：角落放"共创/前沿科技激发计划/独家"类小标（可选项，非必须）。
## 2.9 已验证基线样张与标准提示词模板（v1.17定版）

- `samples/baseline-cover-03-kv.png`＝Jeffrey认可的官方基线（"03KV版不错"），`samples/baseline-cover-03-kv-prompt.txt`为其完整生成提示词（Seedream 5.0 lite，seed=33，identity reference）。
- **标准提示词模板结构**（新期只替换主题变量，骨架不动）：`KV定调(HIGH-SATURATION punchy glossy)` → `HEADLINE标题合同(两行错落/白+语义色3D挤出/宽88-94%/英文眉题)` → `CENTER人物合同(photoreal头硬保真+身份分析动态特征+脸16-26%人物48-72%+表情张力+动作短语+主物件=标题视觉翻译)` → `环绕发光挂件×4(主题元素弧形)` → `SCENE主题世界观(冷暖对比/体积光/轮廓分离)` → `文字精确渲染约束+负面清单`。
- 生成后必须走2.7质量门禁（exactTitle逐字符放大比对为第一关）。
- **场景叙事段护栏**：场景+动作+道具+光影的目标20—100字、硬上限200（超限截断风险拒）；三候选差异化=3个不同模板族×3种sceneId（stage舞台大屏/handheld手持道具/dramatic戏剧场景）。
- **03公式守恒（2026-09-21 Jeffrey裁定：S5/S20两次退化反例后确立）**：`samples/baseline-cover-03-kv-prompt.txt`为母版，新期**只允许替换五个槽位**——{主题场景世界观}{主物件}{标题组}{服装主题化设计}{表情}——其余句子（自拍式前伸手臂透视、HIGH-SATURATION KV定调、三光系统、比例数字、负面清单）**逐字保留**。两条硬规则：①服装必须按主题升级设计（如发光电路纹样连帽衫），**禁止沿用reference照片的日常装**；②姿势必须动态前伸（自拍式手臂朝镜头/主物件举向镜头），**禁止站立指点等站桩构图**。反例存档：S5侦探（对称站桩）、S20选择台（素polo+指点）均因破坏公式被Jeffrey判退化。- 生成后必须走2.7质量门禁（exactTitle逐字符放大比对为第一关）。
- **场景叙事段护栏**：场景+动作+道具+光影的目标20—100字、硬上限200（超限截断风险拒）；三候选差异化=3个不同模板族×3种sceneId（stage舞台大屏/handheld手持道具/dramatic戏剧场景）。
- **三光系统句式（组装时逐字复制进prompt，2026-09-21 S20实测：漏写即丢光效）**：
  `LIGHTING ON CHARACTER (mandatory three-light system): 1) strong cool rim light outlining his entire silhouette and catching the edges of his hair, separating him from the background; 2) the {主题光} glow lighting his face from the {方向} (dual-side color wash if split scene); 3) a soft top light keeping his face the brightest area of the whole cover.` 并在SCENE段保留 `volumetric god rays` 与 `floating dust particles catching the light`。

- **已否决路线（Jeffrey 2026-09-20，勿再试）**："生成无头身体+贴真人照片头"的合成式被否决——贴片感强、头身衔接假、表情只能沿用素材照。本skill维持单pass生图路线（Seedream+identity reference），质量靠2.5-2.8节合同与门禁保证（03KV样张已验证可用）。

共用文字约束：

```text
Render only the following Chinese cover text, exactly as written, with no missing, substituted or extra characters: “[主标题]” and, only when provided, “[辅助短句]”. The Chinese text must be large, crisp, correctly spelled and readable at phone-thumbnail size. Do not render any other words, letters or numbers.
```

### 3. 直接生成1张母版

- 用1条提示词调用 image provider，并传入 Jeffrey reference。
- 生成9:16完整成图，保存为`cover-qiuzhi-9x16.<ext>`；`ext`只允许png、jpg、jpeg或webp。
- 完整成图直接保存到 `05-封面/` 根目录；不创建 `backgrounds/`，不运行后排字脚本。
- 如果中文错字、人物不像或主题画错，只修正原提示词并重生（同prompt换seed最多重采2次）。
- 母版真实、可解码、9:16，并且3张共享尺寸成品全部真实可解码、尺寸正确后，才满足⑥机械门槛。人物身份、标题准确度、主题一致性、缩略图安全区必须在当前任务中逐张视觉复看后如实报告，但不新增review文件或生产阶段。

### 4. 一次生成3张共享尺寸真实成品

在 `cover-prompts.md` 末尾增加 `## 四平台封面成品`，分别编写3条完整生成提示词、调用 image provider、传入同一 Jeffrey reference。三张保持同一视觉主张、主标题、人物和主物件，但必须按真实画布、安全区和断行分别重新构图：

- 3:4：`cover-qiuzhi-3x4.<ext>`，必须1080×1440；共享到抖音竖封面、视频号个人主页卡片和小红书。
- 4:3：`cover-qiuzhi-4x3.<ext>`，必须1440×1080；共享到抖音横封面、视频号分享卡片和B站首页推荐。
- 16:9：`cover-qiuzhi-16x9.<ext>`，必须1920×1080；用于B站个人空间。

只生成这3个物理文件，同比例平台直接复用；平台属性差异由各自标题、介绍、话题和发布字段承担。三张封面仍绑定同一母版与SHA；不得把任一比例简单中心裁切、扩边或在发布页拖动取景后冒充另一比例。

## 2.10 表情与服装变体（换表情/换装的成熟方案，源自产品v2.1）

reference照片表情/服装单一时（如只有微笑证件照），先用 Qwen-Image-Edit-2509 img2img 生成当期变体，标准中文句式：

> 保持画面中同一个人的面部完全不变：{identity_description}。只改变着装、表情和姿态：{personAction}。半身像，面向镜头，自然真实人像摄影质感，纯深灰色干净背景，均匀柔和布光。画面中不得出现任何文字、水印或第二个人。

变体失败回落原始帧；变体结果同样过2.7门禁。已知权衡：img2img有轻微AI重绘感（与人物保真的优先级由当期判断）。

## 2.11 路线结论（产品v2→v4全循环验证，详见references/dh-cover-product-lessons.md）

分层合成（背景+真人贴片+程序字）exactTitle 100%但**融合度天花板达不到秋芝式**——秋芝风的"人物入景+道具遮挡+统一光影"只有整图生成能拿到（与本skill"单pass正解"结论互证；柱子哥真实环境风用分层=laohan-fengmianzhuzige env_photo）。标题字体备选：SmileySans-Oblique（OFL，APP已验证）。Provider已A/B定案：Seedream 5.0 lite。

- 生成后必须走2.7质量门禁（exactTitle逐字符放大比对为第一关）。
- **场景叙事段护栏**：场景+动作+道具+光影的目标20—100字、硬上限200（超限截断风险拒）；三候选差异化=3个不同模板族×3种sceneId（stage舞台大屏/handheld手持道具/dramatic戏剧场景）。

- **已否决路线（Jeffrey 2026-09-20，勿再试）**："生成无头身体+贴真人照片头"的合成式被否决——贴片感强、头身衔接假、表情只能沿用素材照。本skill维持单pass生图路线（Seedream+identity reference），质量靠2.5-2.8节合同与门禁保证（03KV样张已验证可用）。

共用文字约束：

```text
Render only the following Chinese cover text, exactly as written, with no missing, substituted or extra characters: “[主标题]” and, only when provided, “[辅助短句]”. The Chinese text must be large, crisp, correctly spelled and readable at phone-thumbnail size. Do not render any other words, letters or numbers.
```

### 3. 直接生成3张

- 用3条提示词分别调用 image provider，并传入同一张 Jeffrey reference。
- 三张都生成9:16完整成图，按推荐顺序保存为`cover-01-qiuzhi-9x16.<ext>`、`cover-02-qiuzhi-9x16.<ext>`、`cover-03-qiuzhi-9x16.<ext>`；`ext`只允许png、jpg、jpeg或webp。
- 完整成图直接保存到 `05-封面/` 根目录；不创建 `backgrounds/`，不运行后排字脚本。
- 如果中文错字、人物不像或主题画错，只修正原提示词并重生该张；不要增加新流程。
- 三张排序候选真实、可解码、9:16且命名符合顺序，并且默认01的3张共享尺寸成品全部真实可解码、尺寸正确后，才满足⑥机械门槛。人物身份、标题准确度、主题一致性、缩略图安全区必须在当前任务中逐张视觉复看后如实报告，但不新增review文件或生产阶段。
- Jeffrey可明确改选02或03；没有明确改选时，发布准备默认从01适配平台所需封面比例，不能静默改用02或03。

### 4. 一次生成3张共享尺寸真实成品

在 `cover-prompts.md` 末尾增加 `## 四平台封面成品`，并为当前发布rank分别编写3条完整生成提示词、调用 image provider、传入同一 Jeffrey reference。三张保持同一视觉主张、主标题、人物和主物件，但必须按真实画布、安全区和断行分别重新构图：

- 3:4：`cover-<rank>-qiuzhi-3x4.<ext>`，必须1080×1440；共享到抖音竖封面、视频号个人主页卡片和小红书。
- 4:3：`cover-<rank>-qiuzhi-4x3.<ext>`，必须1440×1080；共享到抖音横封面、视频号分享卡片和B站首页推荐。
- 16:9：`cover-<rank>-qiuzhi-16x9.<ext>`，必须1920×1080；用于B站个人空间。

只生成这3个物理文件，同比例平台直接复用；平台属性差异由各自标题、介绍、话题和发布字段承担。三张封面仍绑定同一rank源图与SHA；不得把任一比例简单中心裁切、扩边或在发布页拖动取景后冒充另一比例。

## 输出

写入 `05-封面/cover-prompts.md`：

```markdown
---
schema_version: 3
script_hash: <01-口播稿.md sha256>
distribution_locked_at: <ISO-8601>
prompt_executor: cover-prompt-strategy
image_provider: <实际provider>
reference_mode: REQUIRED
reference_asset: reference/jeffrey-reference.jpg
reference_sha256: <sha256>
strategy: QIUZHI_SINGLE_MASTER_THREE_SIZES
primary_aspect_ratio: "9:16"
required_generated_candidate_count: 1
required_physical_cover_count: 3
required_logical_cover_usage_count: 7
default_publish_candidate: cover-qiuzhi-9x16
---

## 封面文字
- 主标题：<准确原文与断行>
- 辅助短句：<原文或无>
- 事实绑定：<对应口播稿哪一判断>

## 01｜秋芝方向｜最推荐
- 模板族：<族名>
- 模板：<S编号＋模板名>
- 推荐理由：<为什么最适合本期钩子>
<一条可直接生成完整封面的英文提示词>

## 02｜秋芝方向｜第二推荐
- 模板族：<与01不同的族名>
- 模板：<S编号＋模板名>
- 推荐理由：<为什么排第二>
<一条可直接生成完整封面的英文提示词>

## 03｜秋芝方向｜第三推荐
- 模板族：<与01、02不同的族名>
- 模板：<S编号＋模板名>
- 推荐理由：<为什么排第三>
<一条可直接生成完整封面的英文提示词>
```

不要宣称复制某个账号的CTR或独特风格。这里只借鉴公开封面中可观察的通用版式规律。
