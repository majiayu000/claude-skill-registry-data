---
name: h3-prompt-expert
description: 为 MiniMax H3/H3 Max 编译中文视频提示词，支持文生、图生、首尾帧、全能参考和源视频修改。按输入模式保留必需结构并精简重复信息；简单请求直接给 Prompt，不重新设计全片或分镜。
---

# H3 Prompt Expert v6

把已确定意图编译为最小充分 H3 输入。保留用户的主体／相机／环境运动、时机、参考作用、CUT／连续和声音；图像承担已明确的静态信息。单镜请求直接交最短可复制 Prompt；完整项目必须交覆盖全部正式镜头的完整故事版提示词包。内部执行记录和用户交付分开。

## 最短入口

1. 判定输入模式、请求终点和交付范围。直接、简单、明确请求可规范为 provisional_motion_card，compiled_from.source=direct_user_request，不要求上游全片卡或重新生图。完整项目、完整故事版或全片提示词请求进入 `COMPLETE_STORYBOARD_PROMPT_PACK`；正式交接使用仍有效的 MOTION_LOCKED 输入，不擅改资产、VN、GU、时间或导演动作。
2. 核对 [H3 能力](references/h3-platform-capabilities.md) 的相关项。同版本内容已在上下文则复用，实际运行端冲突／未知时核实官方来源。严格首尾和全能参考不能混用；不静默改标签或丢参考。需要实际生成而工具不可用时说明执行缺口，不能虚构已运行。
3. 只读当前模式：文生 [T2VA](references/modes-t2va.md)，首图 [I2VA](references/modes-i2va.md)，首尾 [FL2VA](references/modes-fl2va.md)，尾图 [L2VA](references/modes-l2va.md)，多参考 [Ref2VA](references/modes-all-purpose-reference.md)。保留官方必需字段和对齐语句。
4. 单镜请求直接生成忠实简洁 Prompt；完整项目按故事板顺序逐镜编译，不得只选代表镜头、只交 Motion Card 或用概述替代正式镜头。每个 Shot／GU 的执行正文仍只删除重复的参考外观／环境和无执行价值修饰。普通 5 秒图生约 3—6 行运动正文是目标，不是破坏平台格式或用户动作的硬额度。
5. 完整项目按 [完整故事版提示词包](references/complete-storyboard-prompt-pack.md) 交付全片概述、Subject／Reference Registry、全部正式镜头的时间／功能／输入模式、逐镜可复制 Prompt、转场与声音。完整指覆盖完整，不表示把所有内容合并为一条长 Prompt；只有实际 H3 模式支持并且一次运行确实包含多镜时，才额外提供带 `[Shot N]` 的全片序列 Prompt。

## 需要更多控制时再读取

- 正式上游卡：[交接兼容](references/upstream-shot-handoff.md)、[内部执行包](references/platform-execution-pack.md)。当前 SHOT_HANDOFF v1.2，旧 v1.1 可读取兼容，字段冲突不能猜测覆盖。
- 完整项目、完整故事版或全片提示词：[完整故事版提示词包](references/complete-storyboard-prompt-pack.md)。简单单镜请求不读取。
- 多节点、参考冲突或中高风险：[编译流程](references/core-workflow.md)、[精简与运动语法](references/minimal-motion-compiler.md)、[预检](references/prompt-validator.md)。简单已明确动作不加载全套参考。
- 密集事件／时间冲突：[时间预算](references/temporal-budget.md)；复杂动作／变形：[导演容量](references/director-planning.md)；精确运镜：[相机](references/camera-motion.md)。
- 编辑原视频：[编辑保留](references/editing-preservation.md)；Blender／占位运动替换：[运动母版](references/motion-template-replacement.md)。实际几何影响视差／遮挡，分轴职责不保证独立硬控制。
- 机械／激光／汽车：[工业](references/industrial-visualization.md)；接触／透明化：[物理](references/continuity-physics.md)；精确文字：[文字](references/text-ui-layout.md)；音频／对白：[声音](references/audio-dialogue.md)。
- 骨架歧义：[澄清路由](references/clarification-routing.md)；领域模板仅需要时读 [模式语法](references/pattern-grammars.md)。
- 改 Skill 或复盘：[27 条基准](references/benchmark-cases.md)。一般编译不读测试材料。

## 模式与不变项

T2V 写主体、必要环境／构图／风格和运动；I2V 聚焦运动；首尾帧写可行路径；全能参考保留官方六段结构与必要逐镜信息；源编辑写改什么与保留什么。不把所有模式压成同一模板。

中文正文为默认，官方字段、<Subject / Picture / Video / Audio N>、[Shot N]、时间语法和强制英文对齐句原样保留。用户的对白／画面文字保留原语言；只有明确请求或实际运行端要求才切换英文，不追加双语副本。官方英文推荐记录在内部，不每次添加无关警示。

Subject 使用稳定对象 ID 和最短身份锚点。每份实际素材的功能、作用、控制维度、保留／忽略项、首次生效位置在内部明确；简单单图可压缩为一行。无法读取的附件不能假装看过。

默认整数时间段；只有上游明确 `FAST_CUT` 才可使用 0.5 秒步进，禁止自行产生 0.6、0.7、0.8 等任意十分位 Shot Duration／切点。并行动作合并，后拉并上升可是一条复合轨迹。独立新镜头默认 CUT，同镜动作变化不自动切；简单首尾插值连续，继承原视频切点或用户一镜到底要求。默认无音乐／人声，必要环境／动作 SFX；无有用声音时 N/A。

正向 Prompt 使用官方字段；negative_constraints 是内部列表，独立 negative_prompt 仅运行端确实支持时使用，否则把必要约束自然整合进正向。不要同时输出相互矛盾的正负指令。

## 诊断与完成

编译前实际所需模式、参考和动作可行性必须成立。复杂性只是触发诊断：正式锁定 GU 缺必要控制则 BLOCKED 并返回最小变更；规划请求仍可给可行拆分方案，不能一律空 Prompt 停止。严格锁项不静默降级。

失败先记录症状／时段／已通过项，检查首图、终态、运动、参考职责与模型能力，再选最小实验。在证据支持时局部重编译并记录 parent_run_id／patch_scope；原因来自上游时返回 change_requests，不机械只改一个措辞。复检耦合项，保留无关锁定内容。预算与重试见 [公共政策](references/production-policy.md)。

只有编译通过可记 COMPILED；真实运行与媒体结果由执行方登记，实际图像／视频验收交 shot-grammar-director。输出短不等于模型成功，未生成媒体时不宣称质量已验证。
