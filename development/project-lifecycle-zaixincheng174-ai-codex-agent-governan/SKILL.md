---
name: project-lifecycle
description: >-
  在 Codex 中执行任何"项目级"任务时强制启用的总控协议。当任务不是一次性的小问答、
  而是涉及构建/重构/调研/交付一个有产物的工作单元时触发。它把工作切成 5 个阶段
  (AUDIT → DESIGN → BUILD → REVIEW → VERIFY),每阶段由一个固定角色执行,阶段之间
  有分级门禁,门禁未通过不得进入下一阶段。本 skill 是骨架:它不做具体工作,只负责
  调度角色、检查门禁、维护 North Star 不偏航。
  不要在以下场景触发:单轮事实问答、查文档、改一行字、闲聊。
---

# project-lifecycle —— 项目生命周期总控协议

## 1. 触发条件

进入本协议的判定(满足任一即进入):
- 任务会产出一个需要被别人或未来的自己复用的产物(代码模块、文档、分析报告、工具)。
- 任务预计跨越多步、涉及设计决策,而非机械执行。
- 用户用了"做一个 / 构建 / 重构 / 优化 / 调研"这类动词,且对象是一个工作单元。

明确不触发(直接正常回答,不要套这套流程):
- 单轮事实性问答("X 是什么"、"这个报错什么意思")。
- 查一条文档、改一行字、跑一个命令。
- 诊断/调试/性能定位("为什么失败/为什么慢/帮我 debug") —— 先走 `debug-repro-loop`;
  若复现后确认需要重构、新功能或项目级交付,再转入本协议。
- 用户已明确说"快速给我个答案,不要走流程"。

> 反例:用户说"帮我看下这个函数为什么慢" —— 这是诊断,走 `debug-repro-loop`,不是项目。
> 反例:用户说"重写整个结算模块" —— 这是项目,触发。

## 2. 核心规则(不可违背)

### R1 —— 阶段顺序不可跳过
五个阶段必须按 AUDIT → DESIGN → BUILD → REVIEW → VERIFY 顺序执行。
不允许"先写代码再补设计"。唯一的逆向移动是门禁打回(见 R3)。

### R2 —— 角色单一在场
每个阶段只有一个角色"在场"。进入阶段时,第一句话必须显式自报:
`【阶段 N · 角色】我现在是 <角色>,本阶段我<能做什么>,我<不做什么>。`
这是 Codex 环境下没有真权限隔离时的最强约束 —— 用显式承诺替代权限锁。
只读角色(Auditor / Reviewer / Verifier)一旦在场,不得修改任何文件。

### R3 —— 门禁分级,未通过不得前进
每个阶段结束有一道门禁,每个门禁项有严重度:
- `blocker`：硬停。必须修复,修复后重跑该门禁,通过才前进。
- `warning`：软停。记录到《偏差登记》,向用户报告,用户可选择"接受并继续"或"修复"。
门禁中只要存在一个未解决的 `blocker`,下一阶段的角色不得启动。

### R4 —— North Star 不可偏航(最高优先级)
PHASE 0 产出的《目标契约》全程冻结。此后每一个阶段、每一道门禁,
第一项检查永远是 NS 校验：
> "本阶段产出是否仍在为《目标契约》服务?有没有为了把本阶段做漂亮而偏离最终目标?"
**过度优化 = 门禁失败。** 如果某阶段产出超出目标契约所需的复杂度/完美度,
判定为 NS 违例,按 `blocker` 处理。每一步都必须为山顶服务,不是为本阶段的局部最陡服务。

## 3. 阈值与门禁定义

### PHASE 0 — AUDIT(角色:Auditor,只读)
准入:用户提出一个项目级任务。
产出:《目标契约》+《启动门禁报告》。
门禁(全部 blocker):
- G0.0 NS 锚定 —— 《目标契约》是否已写下并能被用户确认?
- G0.1 范围收敛 —— 需求是否单一可陈述?是否明确列出"明确不做什么"?
- G0.2 想清楚才动手 —— 关键设计问题是否已有答案,而非"边做边想"?
- G0.3 风险/依赖识别 —— 已知风险、外部依赖、未知项是否列出?
- G0.4 目标函数明确 —— 在优化什么?短期产出还是长期复利?权衡写清了吗?
任一不过 → 停,产出《待澄清清单》交用户,不进入 DESIGN。

### PHASE 1 — DESIGN(角色:Architect,只读 + 写设计文档)
准入:PHASE 0 门禁全过。
门禁:
- G1.0 NS 校验(blocker) —— 设计是否仍服务目标契约?是否过度设计?
- G1.1 决策留痕(blocker) —— 关键架构决策是否有 ADR 记录(选项/理由/被否方案)?
- G1.2 接口定义(blocker) —— 模块边界、数据结构、接口是否定义?
- G1.3 风险覆盖(warning) —— 是否覆盖 PHASE 0 识别的全部风险?

### Layer-2 Hook — REPO PREFLIGHT(`repo-preflight`,只读)
位置:PHASE 1 门禁通过后、PHASE 2 Builder 写任何文件之前。
职责:扫描仓库事实,确认 repo root、局部指令、工作区状态、预期改动面和最小验证入口。
门禁:
- RP0 正确现场(blocker) —— 当前目录和仓库根是否是目标项目?
- RP1 指令已读(blocker) —— 适用的局部指令是否已读取?
- RP2 工作区归属(blocker) —— 用户已有改动是否被识别并与本轮改动隔离?
- RP3 改动面收敛(blocker) —— planned touch set 是否最小且服务目标契约/设计?
- RP4 验证入口(warning) —— 是否知道最小验证命令?未知必须报告。
存在 blocker → 不得进入 PHASE 2。

### PHASE 2 — BUILD(角色:Builder,全权限)
准入:PHASE 1 门禁全过,且 `repo-preflight` 无 blocker。
约束:严格按 PHASE 1 设计实现。偏离设计必须显式声明并回到 PHASE 1 更新 ADR。
门禁:
- G2.0 NS 校验(blocker) —— 实现是否引入了设计外的"顺手加的"东西?
- G2.1 设计一致(blocker) —— 实现是否与设计文档一致?
- G2.2 完整可运行(blocker) —— 产出是否完整、可独立运行/使用?

### Layer-2 Hook — DIFF SCOPE GUARDIAN(`diff-scope-guardian`,只读)
位置:PHASE 2 Builder 宣称实现完成后、PHASE 3 Reviewer 介入之前。
职责:审计实际 diff 是否超出目标契约、设计文档或 preflight planned touch set。
门禁:
- DG0 NS/设计一致(blocker) —— diff 是否仍服务目标契约和设计,无未声明偏离?
- DG1 范围未扩散(blocker) —— 变更文件是否都在 planned touch set 或有明确理由?
- DG2 无正交改动(blocker) —— 是否没有顺手重构、格式化、重命名、清理无关代码?
- DG3 变更可审(blocker) —— 是否没有冲突标记、明显生成物误入、秘密/凭证模式?
- DG4 验证对应(warning) —— 已跑验证是否覆盖本次改动面?未跑必须报告。
存在 blocker → 打回 PHASE 2,不得进入 PHASE 3。

### PHASE 3 — REVIEW(角色:Reviewer,只读)
准入:PHASE 2 门禁全过,且 `diff-scope-guardian` 无 blocker。
门禁:
- G3.0 NS 校验(blocker) —— 产物整体是否命中目标契约?有无局部最优拼装?
- G3.1 逻辑严密(blocker) —— 逻辑漏洞、边界情况、错误处理。
- G3.2 安全(blocker) —— 是否引入安全/数据风险。
- G3.3 性能/可维护(warning) —— 明显的性能或可维护性问题。
任一 blocker 不过 → 打回 PHASE 2。

### PHASE 4 — VERIFY(角色:Verifier,只读 + 跑测试)
准入:PHASE 3 门禁全过。
门禁:
- G4.0 NS 校验(blocker) —— 交付物是否就是《目标契约》要的东西?
- G4.1 测试通过(blocker) —— 测试/验证手段是否执行且通过?
- G4.2 结论可验证(blocker) —— 关键结论是否有可复现的证据?
- G4.3 交付完整(blocker) —— 交付物清单是否齐全?
全过 → 进入交付前 closeout hook。

### Layer-2 Hook — CLOSEOUT REVIEW(`closeout-review`,只读)
位置:PHASE 4 验证通过后、最终交付/关闭 goal/对外结论之前。
职责:独立核对完成定义、交付物、范围、验证证据、finding 真实性和最终表述边界。
门禁:
- CR0 完成定义覆盖(blocker) —— 用户明确要求是否逐项有证据?
- CR1 交付物存在(blocker) —— 文件/产物是否真实存在且路径可读?
- CR2 范围未扩散(blocker) —— 是否没有未解释的额外改动或删改?
- CR3 证据足够(blocker) —— 关键结论是否有可复现证据?
- CR4 finding 已验证(blocker) —— 每个阻塞 finding 是否有定位和证据?
- CR5 表述不过界(warning) —— 最终话术是否区分已验证、未验证、阻塞和延期?
存在 blocker → 打回对应 owner,不得交付或关闭 goal。

## 4. 执行路径(Codex 中如何运作)

1. 任务进来 → 本 skill 判定是否触发(见 §1)。
2. 触发 → 启动 PHASE 0,调用 `lifecycle-auditor` skill。
3. 每个阶段:角色自报(R2)→ 干活 → 自评门禁 → 输出门禁报告。
4. 门禁有未解决 blocker → 停在本阶段,不调用下一阶段 skill。
5. 门禁仅有 warning → 写入《偏差登记》,报告用户,等用户决定。
6. 全部门禁通过 → 调用下一阶段对应 skill。
7. PHASE 1 通过后、PHASE 2 前 → 调用 `repo-preflight` 作为现场环路。
8. PHASE 2 通过后、PHASE 3 前 → 调用 `diff-scope-guardian` 作为现场环路。
9. PHASE 4 通过后、最终交付前 → 调用 `closeout-review` 作为现场环路。
10. 任一阶段或现场环路 NS/范围/证据校验失败 → 视为 blocker,按 §R4 处理。
11. closeout 通过 → 输出《交付摘要》并关闭。

阶段与 skill 对应:
- PHASE 0 → `lifecycle-auditor`
- PHASE 1 → `lifecycle-architect`
- PHASE 1↔2 hook → `repo-preflight`
- PHASE 2 → `lifecycle-builder`
- PHASE 2 出口 hook → `diff-scope-guardian`
- PHASE 3 → `lifecycle-reviewer`
- PHASE 4 → `lifecycle-verifier`
- PHASE 4 出口 hook → `closeout-review`

诊断类任务默认不进入阶段表:
- Debug / bug / 性能定位 → `debug-repro-loop`

## 5. 状态维护

全程维护一个轻量状态块,每次阶段切换时更新并对用户可见:

```
当前阶段: PHASE N — <名称>
在场角色: <角色>
门禁状态: <未开始 / 进行中 / 通过 / 阻塞(列出未解决 blocker)>
偏差登记: <已接受的 warning 列表>
North Star: <一行目标契约摘要>
```

## 6. 风险边界(本协议的已知失效模式)

- 本协议在 Codex 中靠"显式承诺"而非"权限隔离"维持纪律。若模型不自报角色、
  或只读角色越界改文件,协议即失效 —— 这是 Codex 机制的固有上限,用户应知晓。
- 本协议**不适用**于探索性、开放式的工作(如头脑风暴),那种工作没有可冻结的
  目标契约。强行套用会扼杀探索。此时应明确退出本协议。
- 门禁的严重度分级由模型自评,存在判断误差。`blocker` 与 `warning` 的边界
  由用户在使用中校准,本 skill 提供的是默认值。
- 五阶段对小任务是过重的。§1 的不触发清单必须严格执行,否则协议本身会变成
  你最讨厌的"低质量的繁琐"。

## 7. 反例(以下情况不要这样做)

- 不要在 PHASE 0 还没产出《目标契约》时就开始想技术方案 —— 那是 Architect 的活。
- 不要因为"看起来简单"就跳过 AUDIT 直接 BUILD。
- 不要在 REVIEW 阶段顺手改代码 —— Reviewer 只读,发现问题打回 BUILD。
- 不要把"这个阶段我能不能做得更完美"当成目标 —— 见 R4,那是 NS 违例。
- 不要对单轮问答、查文档这类任务套用本协议。
