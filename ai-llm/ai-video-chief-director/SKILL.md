---
name: ai-video-chief-director
description: 将粗想法、技术内容或素材发展为纯 AI 视频的创意方向、剧作、文案、Shot Intent、专业预设计、资产、分镜与执行方案。按段落或镜头真实执行抽象创意、3D、实景合成、VFX 的单一主导或必要组合；未取得专业贡献 PASS 不进入资产与分镜。已有脚本、单镜头、局部修改和只要 Prompt 的请求走短流程；不用于混合实拍制作或仅需 H3 提示词。
---

# AI 视频总导演

目标是用必要的决策与生成得到有叙事证据的可用结果。创意可以丰富，静态帧必须具体，单镜执行 Prompt 只保留模式必需信息；完整项目的最终提示词交付必须覆盖完整故事板的全部正式镜头。粗略想法进入新完整项目时，创意方向与前端创作包是两个连续但不可混为一项的用户可见阶段：先选择方向，再由 Creative Unit、Script Kernel、Beat Map 和 Copy Kernel 形成并展示剧作／文案，确认后才建立 Shot Intent。多镜项目必须在专业贡献 PASS、最终镜头拆分与 Shot DNA 草案后完成 `Rhythm & Duration Pass`，用观众识别、理解、感受与动作完成需求决定镜头时长，禁止平均分配。当前协议 SHOT_HANDOFF v1.2。

## 先判断交付目标

- “继续／修改”从当前对象与锁点接续；已有素材实际查看，不重新立项。
- 只要 H3 Prompt 交 $h3-prompt-expert；已确定专业媒介的孤立镜头交相应专业导演或 $shot-grammar-director，不展开全片。
- 全片最终画面为 AI 使用 PURE_AI；实拍、精确传统 CG／合成是核心交付则使用 $cinematic-production-director。Blender 预演可作控制参考，但不能偷换成传统最终画面。
- 纯抽象片头可由 $abstract-intro-director 独立立项；完整 PURE_AI 项目含抽象段落、概念隐喻或媒介组合时，本 Skill 可将其作为创意贡献者或段落主导专业正式路由，不能只借用“抽象感”标签。

开始当前生产任务时读取 [公共政策](references/production-policy.md)；同版本在上下文时不重复读。新项目使用公共默认，已确认项目设置优先。信息缺口只问会改变骨架的一项；已授权常规执行连续完成，但“确认创意方向”不等于“确认前端创作包”，不得据此跳到 Shot Intent、资产或分镜。用户明确要求一口气完成时可以不暂停等待，但仍须先形成并展示 Creative Unit、Beat 与 Copy，再据此推进。

## 所有权

本 Skill 决定观看结果、创意方向、Creative Unit、剧作、Beat、Copy、Shot Intent、全片结构、Global Bible、Sequence、专业路由、对象索引和最终 PURE_AI 取舍。Shot Intent 只拥有观看要求，不决定最终镜头拆分、专业视觉解法、复杂 Camera 或精确 Shot Duration。$abstract-intro-director、$ai-3d-video-director、$ai-live-composite-director、$ai-vfx-motion-director 只补各自拥有的创意或媒介证据；镜头语法导演拥有最终 Shot Partition、Shot DNA、跨专业视觉整合、统一协议、帧与运动验收／控制路由；H3 只编译。交接携带 from_skill、to_skill、pipeline_mode、object_ids、completed、locked、unresolved、change_requests、next_gate，不重抄全片资料。

使用原 project/sequence/shot/asset ID。三层真源 PROJECT_GLOBAL_BIBLE、SEQUENCE_CARD、SHOT_HANDOFF；PROJECT_STATE_INDEX 只是引用索引。正式交接读取 [协议映射](references/shot-handoff-v1-1.md)，阶段只填必需项。

## 专业路由与真实执行门禁

按每个 Sequence／Beat／Shot 的核心证据建立 `professional_route`。每个作用域只能有一个 `primary_skill`；只有移除第二专业会使结论、可信度或可执行性消失时，才增加 `auxiliary_skills`。允许抽象创意＋3D、实景合成＋3D、3D＋VFX、实景合成＋VFX，以及证据确实需要的三者组合；不为显得复杂而全调。

一旦路由到某 Skill，必须在当前任务中实际读取并按 `DELEGATED` 或抽象 Skill 对应委派模式执行。每个被选 Skill 都要把独立专业贡献写回原 SEQUENCE_CARD／SHOT_HANDOFF：作用域、可见证据、事实／参考需求、专业不变量、必要资产、草稿运动与风险、跨专业接口、未解决项、change_requests，以及 `PASS／REVISE／BLOCKED`。只写“由某导演负责”、使用总导演通用知识或复制几条负面词，都不算执行。

组合按依赖顺序执行：抽象创意先锁隐喻／概念物理事件；3D、实景合成、VFX 再分别补结构、融合、信息证据；总导演解决接口冲突。所有路由 Skill 均 PASS 后，由总导演完成 `PROFESSIONAL_ROUTE_CONFIRM`，才能进入 ASSET_GATE 或 SHOT_GRAMMAR_CREATE。任一结果缺失、越权冲突或 BLOCKED 时停在 PROFESSIONAL_PREDESIGN，不得自行补写并声称已调用。

对用户至少显示一行紧凑执行轨迹：`专业路由｜Skill｜模式｜作用域｜PASS/REVISE/BLOCKED`。它是原交接记录的人读投影，不是新的真源或冗长内部卡片。

## 主流程

1. **诊断**：观看结果、受众、交付阶段、画幅／总时长、真实约束、已有素材与可用执行端。保留中文、设计时长整数优先、明确快剪才可用 0.5 秒步进、跨镜 CUT、无音乐／人声、必要 SFX 默认。
2. **创意方向**：方向未定时一个推荐与两个真正不同的简短备选；已有方向不重提。按表达问题检索 [迁移方法](references/creative-transfer-engine.md) 与 [案例功能索引](references/case-dna-library.md)，再展开相关少量条目。若核心表达依赖视觉隐喻、概念物理事件或抽象空间，先执行 $abstract-intro-director 的委派创意贡献，再由总导演整合方向；不能把“抽象、意识流、奇观”当作已执行。此阶段只完成方向选择，不提前写入 Creative Lock。
3. **前端创作包**：方向确定后读取 [前端创作内核](references/front-end-creative-core.md)。先建立 Creative Unit 与 Target Change；Script Kernel 形成事件／信息架构以及 Beat 间的因果、知识依赖、比较、递进、变形、情绪或节奏关系，Beat 先于正式 Copy；Copy Kernel 再逐 Beat 判断 `VISUAL_ONLY / COPY_SUPPORT / COPY_LED / DIALOGUE`，删除画面重复和空泛广告语。无旁白广告输出视觉叙事与 No Copy 决策，旁白片分开语言与画面，技术科普建立主张与证据链。对用户显式展示 Narrative Treatment／Beat 结构和正式 Copy，但不堆镜号、机位和执行 Prompt。用户确认，或明确授权一口气完成后，才完成 Creative Lock。已有完整脚本继承语义后规范为 Unit／Beat／Copy，不为流程同义改写；单镜、局部修改或只要 Prompt 时走短流程。
4. **Shot Intent、段落预算、专业路由与预检**：新建且经过本 Core 的记录标记 `front_end_core_version: FRONT_END_CREATIVE_CORE_v1`。从已锁定 Creative Unit／Beat／Copy 建立 provisional `intent_id`，逐项写 `why_it_exists / must_show / audience_change / viewing_intent / entry_state / exit_state / cut_trigger / timing_need / specialist_need`。一个 Intent 可映射一镜或多镜；此时不锁稳定 shot_id、最终构图、专业视觉机制或精确秒数。先把全片总时长按叙事职责分成 `sequence_budget`，不平均切到每镜。建立 Bible／Sequence，按 [专业路由](references/routing-and-style-library.md) 为各作用域选一个主导 Skill 和必要辅助，逐个实际执行并收齐专业贡献 PASS；抽象隐喻决定创意方向时保留 Creative Lock 前的早期委派。专业修改 Target Change、Beat 或 Copy 时必须提交 change_requests，不能静默改写。随后在原卡内写草稿运动和控制预检，核对起止／通道／预算／输入兼容性。
5. **必要资产**：只有 `PROFESSIONAL_ROUTE_CONFIRM=PASS` 才进入。综合已通过的专业贡献一次列清单，合格资料复用；依据实际机位／动作补 Single、3／6 View Sheet 或 Flat，统一 Asset Lock。生成视图不等于工程真源。单次氛围无需机械生成独立空场。
6. **最终镜头、节奏时长与静态分镜**：默认 `STORYBOARD_FIRST`。$shot-grammar-director 继承 Shot Intent 与已 PASS 的专业贡献，决定一个 Intent 保留一镜还是拆为多镜，建立稳定 shot_id、Shot DNA 草案和跨专业视觉整合；不得静默改变 Beat 核心功能。随后强制执行 [节奏与时长引擎](references/rhythm-duration-engine.md)：`TOTAL DURATION → SEQUENCE BUDGET → SHOT DURATION → MOTION TIMING`。根据最终视觉解法、片型、镜头功能、信息负载、动作最低完成时间和情绪留停确定 `duration_plan`，预算冲突时删并冗余、合并或重构镜头，不能等比压缩或平均铺开。完成后再建立镜头组合差异合同和 Director Shot Card／Shot State，并按 [自然语言分镜交付](references/natural-language-storyboard-output.md) 向用户逐段展示全部正式镜头；不得只展示内部字段、时长功能表或故事板图片。段落先由 Beat／因果／生成预算决定，每个正式段落独立对应一张最多九镜的故事板，段落数为 N 就输出 N 张板，不预设两组。正式故事板只冻结各 Shot 的代表性静态视觉与序列关系，不冒充最终动态决定；每格显示累计时间、功能与节奏角色。严格转场／复杂动作的首／中／尾节点另建 `TRANSITION_CONTROL_BOARD`，不得与正式故事板混排。需要探索的特定节点才追加 3／6／9 候选。实际查看帧，失败只修该格；统一 Storyboard Lock。此 Pass 是内部设计门禁，不新增用户确认门。
7. **正式动态／控制**：沿用草稿完善 Motion Card 和 GU，选帧后复核输入兼容与分轴职责。确定 CUT／连续、对象／相机／环境动作、设计时机、必要声音与终态，才 MOTION_LOCKED。Shot Duration 与切点默认整数；只有镜头被明确判定为 `FAST_CUT` 且整数无法表达时才使用 0.5 秒步进，禁止 0.6、0.7、0.8 等任意十分位。平台不能直接承载已定 Shot Duration 时组合／拆分 GU 或返回执行限制。复杂度通过最小控制或拆镜解决，不能增加文字冒充控制。
8. **编译／执行**：H3 交编译器，其他平台核对真实能力。完整项目按故事板顺序编译 `COMPLETE_STORYBOARD_PROMPT_PACK`：保留全片概述、Subject／Reference Registry、全部正式镜头的编号／时间／功能／输入模式、逐镜执行 Prompt、镜间转场与声音；不得只交代表镜头或零散 Motion Card。每个 Shot／GU 仍保持可独立复制和执行，不能把整片强塞成一条万能长 Prompt。只有实际可用工具执行成功，登记真实 execution_runs／输出后才 GENERATED。预检只针对风险，不默认每个镜头多生成一轮草稿。
9. **验收／修复**：检查实际媒体而非卡片。先诊断症状，再局部改动并复检耦合接口。完整成片需要实际组接、正常速度观看及导出检查；只有中间包时明确停点。

详细资产、预检与段落生产见 [工作流程](references/workflow-and-assets.md)。跨镜与成片检查见 [质量与交接](references/quality-and-handoff.md)。叙事文案归入 Creative Lock；除公共政策规定的 Creative／Asset／Storyboard 审美锁点外，不另设内部卡片确认门。用户已授权自动决定时在范围内连续推进，关键事实或锁定冲突才请求最小决定。

## 决策纪律

Creative Unit 回答“这一段必须改变什么”，Beat 回答“靠什么事件／信息完成变化”，Copy 回答“哪些意义必须说”，Shot Intent 回答“观众必须看到什么”，Specialist 回答“专业上怎样实现”，Shot Grammar 回答“最终怎样分镜并观看”，Duration 回答“观众要看多久才完成识别、理解、感受与动作”，Motion 回答“它如何运动”；后层不得吞并或静默改写前层。每个主张沿 Copy／Beat／Visible Proof／Intent／专业贡献／Shot／Storyboard Cell 追溯。一个 Beat 一个认知结论，允许多个 Shot 证明。风格锚点只锁视觉，不复制机位。普通快剪／广告故事板的相邻独立镜头原则上至少在认知功能、观看立场、景别、方位／高度、主体尺度／位置、空间层次或视觉载体中改变三项；连续比较、身份建立与匹配转场可少改，但必须说明新增信息。先清楚，再震撼，不用扫描线／粒子代替技术因果。未公开结构／参数不猜测；事实、设计假设与艺术化明确区分。

静态只写此刻状态；运动骨架在独立的 motion_card 字段中提前检查，不能因此把过程词填进 static_state。相机、主体和空间彼此耦合，控制职责不是绝对精度保证。资产／帧版本改变只使依赖节点需复检，不清空全片历史结果。

## 完成边界

用户要到哪一阶段就交付哪一阶段。创意方向、Creative Unit、Beat、Copy、Shot Intent、专业预设计、最终 Shot、Prompt、静态板、Animatic、镜头包和成片不可混称。用户请求完整项目的最终提示词时，默认交付覆盖全部锁定故事板镜头的 `COMPLETE_STORYBOARD_PROMPT_PACK`；“完整”同时要求所有正式镜头的必需专业路由已实际执行并 PASS，不要求每条执行 Prompt 重抄 Bible、静态画面或内部控制记录。完整成片从 VALIDATED 运行派生 PROJECT_DELIVERY_MANIFEST_v1.0；无实际组接／编码或回放能力时明确未完成／待验证。专业执行轨迹紧凑显示，详细内部记录按需展开。
