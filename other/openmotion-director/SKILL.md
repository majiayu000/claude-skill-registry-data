---
name: openmotion-director
description: Plan and create original motion videos and motion graphics with OpenMotion, including esports recaps, explainers, product demos, and brand films, or first planning how a video should be presented. Also use for narrative, motion, or sound redesign and creative review. Execute established edits/exports with openmotion-production, editable templates with openmotion-template-to-video, reference reconstruction with openmotion-recreate, and reusable templates with openmotion-video-to-template. Repository development does not trigger video production.
metadata:
  version: "1.5.5"
---

# OpenMotion Director

## 职责与目标

Use OpenMotion for an original video on the user's topic, including a request to discuss its presentation first. Apply the shared context's capability discovery and connection guidance when starting. A concept-only request ends with the requested creative plan; once the user asks to build it, continue with the confirmed plan through the connected OpenMotion tools.

以 Motion 导演视角负责本片的动态叙事、镜头衔接、状态延续与声画关系编排，根据产品事实、受众和传播目的决定表达方式。目标是让时间、运动、剪辑与声音承担表达、情绪或注意力组织职责；Motion 感来自经过设计的变化与节奏，不等于运动量、镜头速度或特效数量，准确性与可读性仍须成立。用户要求更强 Motion 表现时，关键段落须有可感知的动作编排、画面发展或剪辑节奏收益，不能给静态排版套通用入场后用“克制风格”解释交付。

## 先选工作范围

- **创作方案**：读取 [动作脚本](references/action-script.md)，交付创意与脚本，不自动制作视频。
- **从零制作**：按下方工作流推进到用户要求的预览、工程或成片。
- **局部创作**：重设计受影响的动作、节奏或声画关系；先看相关片段和相邻接点，只展开当前范围。既定决定下的局部工程修改用 openmotion-production。
- **声音创作**：画面锁定时仅重设计声音叙事、节奏与声画锚点，保留画面，不重启整片原创。
- **创作审片**：以实际视频评价表达、动作、节奏和声画关系，不自动改工程；规格与导出核对用 openmotion-production。

沿用已确认的简报、素材、风格与授权。只追问影响真实性、交付或重大创作取舍的缺口（例如讲解/科普片未说明是否要配音时，一并在首次提问中确认）；其余合理假设并简短说明。检查点默认是 Agent 自检，不变成额外审批。

## 接入与共享职责

首次触发先读 [共享上下文](../openmotion-production/references/context.md)，按清单补齐缺失正文并记录已读文档，不返回 production 重选路；正文仍在上下文时直接复用。已有片重编应用 [共享修改流程](../openmotion-production/references/edit.md)。实现前补齐 [运行规范](../openmotion-production/references/production.md)、[Native authoring](../openmotion-production/references/native.md) 与固定版本引擎指南；导出或交付时补读 [验证](../openmotion-production/references/verification.md)。MCP-only 通过 resources/read `openmotion://workflow/director/start` 读取本页。若工具无法实现关键设计，先找等效表达并说明影响，不能默默降级成逐页卡片。

## 从零制作工作流

### 1. 形成创作判断

Typography: before choosing faces for new text, redesigning text hierarchy or addressing a font/style complaint, read [Typography](../openmotion-production/references/typography.md) and carry its actual-copy comparison into a representative frame or clip.

确认受众、主要信息、期望感受或行动、规格、事实依据、素材与声音需求，区分真实界面演示与概念化表达。需要选择、获取或替换素材时读 [共享素材规范](../openmotion-production/references/materials.md)；主视觉质感不足，或含截图、跨段复现、多段落与展示感问题时，按需读 [制作决策与状态延续](../openmotion-production/references/decisions.md)。

按共享的 [生成边界](../openmotion-production/references/materials.md#generation-boundary) 与 [生成时机阶梯](../openmotion-production/references/materials.md#generation-timing-ladder) 逐镜决定复用、原生代码、静图加原生动效还是生成视频；需要 AIGC 时进入 [openmotion-media](../openmotion-media/SKILL.md)。同一主体、商品或场景跨多个生成镜头时，应用共享的 [跨镜头一致性流水线](../openmotion-production/references/materials.md#cross-shot-consistency)（锁定锚点图、按连镜或换角度准备并通过动作起始态首帧目检、统一光影画风与衔接切点），避免多镜都直接绑回同一张初始原图导致切镜跳回。

进入素材生成时，生成只升级动态影片，不替代它。先按完全不生成规划影片的关键视觉事件、主体变化、场景切换与转场，再挑出用生成素材升级的职责（写实产品、背景板、连续物理动作镜头），不因放进生成图而删减已规划的视觉事件，也不让一张主视觉图撑起全片。请求可配合运动的素材（干净/可去背主体、分离背景板、推拉摇移留白与文字安全区），预览前确认遮掉生成像素后动态结构仍成立。

先写一句“观众将经历怎样的变化”，再划镜头；区分“文字宣告了什么”与“画面实际让观众经历了什么”。用户只给品牌或主题时，由导演补足可表演材料、关键视觉事件与记忆点（“高级、3D、丝滑”不算决定），无真实素材支持的设想标为概念。截图可用于真实证据或比较，不能自动成为每个卖点的容器。

原创新片或大幅重编动态叙事时，读取 [动态表现](references/motion-craft.md) 与 [动作短句正反例](references/motion-phrases.md)，联合设计材料、主体动作与构图，校准“有变化”与“动作有表现力”的区别，不复制例子的对象或结构。

### 2. 把判断转成动作脚本

读取 [动作脚本](references/action-script.md)，记录关键意图、时间组织、对象状态、段落关系与观察点。关键段落写清“发生的变化 → 观众获得的理解或感受”；若只有位移、缩放与透明度变化，确认它们确实揭示了关系而非仅重排版。强 Motion 简报须指出中后段实际值得观看的事件与可辨认窗口，镜头边界不必等于场景文件边界。

声音承担叙事、配乐脱节或需重设计声音时，读取 [声音叙事](references/sound-narrative.md)；音乐与音效关系按 [共享声音执行](../openmotion-production/references/sound.md) 建声画锚点并从实际画面相位与声音事件双向复核。需要配音或口播字幕时，先确认大字排版是否已覆盖台词，确需独立字幕则按 [配音与可编辑字幕协同](../openmotion-production/references/sound.md#配音与可编辑字幕协同) 挂载原生可编辑字幕层，不写死进生成像素。方案落入形容词堆砌或模板填空时，按需查阅 [正反例](references/examples.md) 中最相关的一例。

### 3. 先验证最大创作风险

多段视频优先做包含代表性动作与上下文的低成本动态样片（纯视觉风险可先做风格帧；用户要求先看关键画面时，按影片顺序给实际风格帧并等确认后再扩片）。验证场间交接时，样片须覆盖前段末态、交接过程与后段承接。依据 [审片标准](../openmotion-production/references/review.md) 分开检查视觉吸引力与动态组织；样片暴露结构问题就先改编排，不在静态版式上精修缓动。多段原创或大幅重编在精修前还须形成全片低成本动态粗稿，按制作决策检查动作结束后的空转时间、截图新增信息与跨段状态延续；声画关系为主风险时，样片须带实际音轨并按正常速度检验。

### 4. 完成实现与全片

按可用引擎规范实现，复用有效组件，重要对象与镜头保持可定位名称；相邻段落明确连续交接或刻意断裂，并根据实际素材、配音与布局更新脚本时间。成片就绪后按 [可编辑预览交接](../openmotion-production/references/native.md#editable-preview-handoff) 打开编辑器，再导出，并按 [成片交付](../openmotion-production/references/production.md#final-video-delivery) 在对话中展示成片。

### 5. 观看、修正、交付

读取 [审片标准](../openmotion-production/references/review.md)，观看实际输出按时间点记录问题，先修表达与结构，再修节奏与运动细节，修复后复看受影响区间及接点，交付前检查全片播放；达到要求即停，不无限加效。用户点名的质量问题须落到实现修正并复验，或如实说明限制。交付时保留可编辑工程，按 [共享成片展示规则](../openmotion-production/references/production.md#choose-one-final-video-preview) 展示一次成片预览，注明占位、概念演示与未验证项。

## 防止模板塑造所有作品

- **规范约束信息完整性，创意决定内容**：不预设镜头数、单段时长、转场配额或运动覆盖率；静止、长镜头、硬切与连续变形均可依内容成立。
- 统一品牌与运动逻辑，不强求所有动作同缓动、同速度；示例数值仅属于该例，审片时去掉只因模板或代码方便而存在的选择。
