---
name: closeout-review
description: >-
  工程现场环路 P1。用于交付前的独立收口审计,在最终回复、目标关闭、PR/交付摘要之前触发。
  核对完成定义、验证证据、diff 范围、残余风险和对外表述;吸收 codex-review 纪律:
  advisory 不盲信,每个 finding 必须有定位和可验证证据。
---

# closeout-review —— 交付前独立审计闭环

## 1. 触发条件

必须触发:
- 准备宣布项目/任务完成、关闭 goal、提交 PR、交付摘要或对外结论前。
- 本轮有代码、配置、skill、文档产物改动,且用户会依据结果继续行动。
- 存在审查建议、静态扫描、AI review、测试输出或浏览器观察需要转成结论时。

不触发:
- 纯问答、无产物、无需交付结论的即时回复。
- 已由用户明确要求"只给状态,不要审计"。

## 2. 职责边界

只做:只读审计最终交付是否可以被证据支撑。
不做:修改文件、补实现、扩大范围、替代 `lifecycle-reviewer` 的代码审查。

closeout-review 审的是"能不能这样交付/这样声称",不是"还能不能做得更好"。

## 3. 审计清单

- 完成定义:逐条对照用户目标、目标契约或本轮计划。
- 交付物:确认实际文件/产物存在,路径正确,没有漏项。
- 范围:实际改动是否仍在 planned touch set 内,无正交改动。
- 验证:每个关键结论是否有命令、输出、截图、文件读回或其他可复现证据。
- Findings: advisory、AI review、静态扫描、测试失败只作为线索;必须二次验证后才可升级。
- 表述:最终回复不得把局部测试说成全局通过,不得把未验证说成已验证。

## 4. 输出格式

```
Closeout Review
Completion criteria: <逐条 PASS/FAIL/UNVERIFIED>
Deliverables: <文件/产物清单>
Scope audit: <PASS/FAIL, unexpected changes>
Evidence audit: <关键验证证据>
Finding audit: <已验证 finding / rejected advisory / unresolved>
Claim boundary: <最终可说什么,不能说什么>
Verdict: <PASS -> deliver / BLOCKED -> return to owner / HOLD -> user decision>
```

## 5. 门禁

| 门禁项 | 严重度 | 检查 |
|---|---|---|
| CR0 完成定义覆盖 | blocker | 用户明确要求是否逐项有证据? |
| CR1 交付物存在 | blocker | 文件/产物是否真实存在且路径可读? |
| CR2 范围未扩散 | blocker | 是否没有未解释的额外改动或删改? |
| CR3 证据足够 | blocker | 关键结论是否有可复现证据,不是记忆/感觉? |
| CR4 finding 已验证 | blocker | 每个阻塞 finding 是否有定位和证据? |
| CR5 表述不过界 | warning | 最终话术是否区分已验证、未验证、阻塞和延期? |

## 6. Advisory 纪律

- advisory 不是事实;只有复现、代码定位、文件证据或命令输出能把它变成 finding。
- 无定位的批评不能进入 blocker 清单。
- 如果 advisory 指向真实风险但证据不足,标成 `UNVERIFIED` 或 `HOLD`,不要包装成确定结论。

## 7. 反例

- 不要因为测试绿了就宣布目标全完成;先核完成定义。
- 不要把"没有发现问题"说成"没有问题"。
- 不要在 closeout 阶段修文件;发现 blocker 就打回对应 owner。
