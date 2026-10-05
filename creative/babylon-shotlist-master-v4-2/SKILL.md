---
name: babylon-shotlist-master-v4-2
description: Compile story ideas, reference assets, or full screenplays into concise Seedance 2.0 single-shot prompts and self-contained HTML shotlists. Use for Chinese, English, or bilingual prompt writing; multi-reference responsibility mapping; causal camera direction; transitions; revisions; and production-ready batch breakdowns.
---

# 巴比龙分镜大师 4.2 开源版

把用户的故事、镜头要求和参考素材编译成可执行的 Seedance 2.0 提示词。把信息放在唯一负责它的位置，优先说明变化，不复述参考素材已经给出的静态外观。

## 工作约定

- 先识别交付类型，再组织文字。不要让用户先学习摄影术语。
- 先建立可见的剧情因果，再决定机位、切点和运动；摄影服务信息揭示与角色选择。
- 多参考素材先分配职责。人物图负责身份和既有造型，地点图负责空间，其他素材各自只承担已声明的主职责。
- 同类素材超过一份时，按剧情中的人物、地点、时段、天气和关键道具自动匹配；只有两个候选同等成立时才询问。
- 同一事实只完整写一次。后续只写变化、临时状态或连续性结果。
- 使用正向、场景相关的目标状态。不要附与本镜头无关的泛化负向清单。
- 不自动加入 8K、IMAX、60fps、创作者姓名、长人物描述或宣传式质量词。

## 七层编译结构

最终提示词从以下编译层中取用，顺序固定，但没有最低层数：

1. **任务卡 / Task Card**：语言、目标时长、画幅、速度及交付类型；平台默认已经足够时可省略已知规格。
2. **素材契约 / Asset Contract**：标签、唯一主职责、当前状态和必要的冲突裁决。
3. **剧情节拍 / Story Beats**：开场状态、可见触发、反应与选择、反作用、结尾新状态。
4. **画面调度 / Frame Direction**：把空间、主体位置、动作方向、接触点、机位、景别和摄影机响应写成一组协同指令。
5. **表演与环境反馈 / Performance & World Response**：只保留能让情绪、力量、材质或环境反应变得可见的细节。
6. **光色声 / Light · Color · Sound**：声明实际光源及变化、承担叙事的颜色、声音入点，以及需要生成的短风格锚点。
7. **连续性与交付 / Continuity & Delivery**：锁定跨段会变化的状态，并给出单发提示词或批量 HTML 的最终要求。

简单镜头只选必要层。没有参考素材就省略素材层；没有关键光色声变化就不为其凑句；稳定单镜头不强行增加连续性声明。用户要求保留自定义区块名或前缀时逐字保留，但内部仍按七层顺序推理。

## 语言模式

- **中文模式**：层名和正文使用简体中文。
- **英文模式**：使用上面的英文层名和直接、自然的英文。
- **中英双语模式**：每个中文层后紧跟信息等价的英文；不得生成两套不同镜头。
- 用户未指定语言时跟随其当前语言。`@tag`、FOV、时间码、单位、文件名和对白原文默认不翻译。

## 模式分流

### 单发模式

用于一个镜头、一场短戏、一次转场或一条可直接粘贴的提示词。

1. 读取 [输入契约](reference/INPUT_CONTRACT.md) 和 [视觉路由](reference/VISUAL_ROUTER.md)，提取目标、参考职责与风格依据。
2. 普通单人、单动作镜头直接按本文件规则编译；只有复杂因果、多人走位、对话节奏或明显运镜时才读取 [故事编译器](reference/STORY_COMPILER.md) 与 [镜头蓝图](reference/SHOT_BLUEPRINT.md)。
3. 只有多段、转场或容易漂移的临时状态才读取 [序列连续性](reference/SEQUENCE_CONTINUITY.md)。
4. 只有明显高风险内容才读取 [安全改写](reference/SAFE_REWRITE.md)。
5. 按 [交付模式](reference/DELIVERY_MODES.md) 输出；普通单镜头是一段连续提示词，不显示内部七层标题。

用户未指定时长、画幅或速度时，先继承当前项目或平台已有设置；没有可继承设置时省略这些参数，不为补全规格而询问，也不要添加无关动作。只有镜头可行性、身份映射或剧情结果存在实质冲突时才用一个短问题确认。

### 批量模式

用于整部剧本、多场景项目、分镜清单或投产 HTML。

1. 完整读取剧本，建立场次、人物、地点、道具、对白和临时状态索引。
2. 用 [输入契约](reference/INPUT_CONTRACT.md) 建立项目素材契约。
3. 用 [故事编译器](reference/STORY_COMPILER.md) 按状态变化拆出剧情单元并决定合并或拆分。
4. 用 [视觉路由](reference/VISUAL_ROUTER.md) 在项目级确定每条提示词的风格来源。
5. 用 [镜头蓝图](reference/SHOT_BLUEPRINT.md) 逐单元编译必要层，用 [序列连续性](reference/SEQUENCE_CONTINUITY.md) 传递状态和转场。
6. 高风险段落按 [安全改写](reference/SAFE_REWRITE.md) 保留剧情功能并降低不必要的露骨呈现。
7. 按 [交付模式](reference/DELIVERY_MODES.md) 和 [HTML 模板](templates/HTML_TEMPLATE.md) 生成独立文件。

批量模式可以分轮核对素材身份和关键空间，但不要要求用户逐镜头选择风格或技术参数。

## 三路视觉决策

执行 [视觉路由](reference/VISUAL_ROUTER.md) 中的优先级：

1. 用户指定完整视觉方向或风格图时，以它作为基础；若用户只调整局部属性，则只覆盖该属性，不替换其余视觉依据。
2. 没有完整新风格且存在场景图时，由场景图统一视觉语言，不生成额外风格前导。
3. 只有前两类依据都不存在时，才根据剧情用途、类型、情绪、节奏及现有素材媒介自动选择一种方向。

这是内部决策，不向用户展示风格菜单，也不为了常规风格选择暂停工作。

## 修改已有结果

- 先把用户明确要求修改的事实标为可变项。
- 标签、身份、已确认空间、原对白和用户指定前缀默认锁定。
- 只传播到直接受影响的节拍、时间、位置、光线、声音和连续性状态。
- 返回完整新版；修改摘要最多五行。

## 交付检查

- 每个素材是否只有一个清楚的主职责？
- 是否删除了参考素材已经表达的外貌、服装、材质和陈设？
- 触发、选择、反作用和结尾状态是否都能被画面或声音感知？
- 摄影机是否由可见事件触发，并在信息读清后停止？
- 主体动作、摄影机响应和环境反馈是否能在目标时长内完成？
- 是否只有一个基础视觉来源，且用户的局部覆盖只改变指定属性？
- 是否只保留真正改变执行的层？
- 输出语言、标签、时长、画幅和交付文件是否符合任务卡？

## 参考导航

- [reference/INPUT_CONTRACT.md](reference/INPUT_CONTRACT.md) — 输入归一化、标签与素材职责
- [reference/STORY_COMPILER.md](reference/STORY_COMPILER.md) — 剧情因果、节拍密度与场景拆分
- [reference/SHOT_BLUEPRINT.md](reference/SHOT_BLUEPRINT.md) — 画面、摄影、表演与环境响应
- [reference/VISUAL_ROUTER.md](reference/VISUAL_ROUTER.md) — 三路视觉优先级与短风格锚点
- [reference/SEQUENCE_CONTINUITY.md](reference/SEQUENCE_CONTINUITY.md) — 多镜头、转场、空间和临时状态
- [reference/SAFE_REWRITE.md](reference/SAFE_REWRITE.md) — 高风险内容与正向约束
- [reference/DELIVERY_MODES.md](reference/DELIVERY_MODES.md) — 单发、批量、语言和 HTML 交付
- [templates/HTML_TEMPLATE.md](templates/HTML_TEMPLATE.md) — 自包含 HTML 骨架
