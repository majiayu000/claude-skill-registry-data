---
name: science-rebuttal-playbook
description: Use immediately after receiving reviewer reports, when a revision decision says major revision, or when you disagree with a reviewer; covers the numbered-response structure, how to split fixable from arguable points, why unprincipled compliance backfires, and how to escalate a genuine disagreement to the editor.
---

# 审稿回应：先分类，再逐条

## 第一步：切条与分类（不要直接开始写）

把评审意见粘进 `science_rebuttal`，它会切成编号条目并按类型标注：

| 类型 | 特征用语 | 做法 |
|---|---|---|
| **new-experiment** | additional experiments / should test / in vivo | 能补就补；不能补降级为 limitation 并说明不影响主结论 |
| **statistics** | sample size / power / CI / multiple comparison | 一律重跑，给效应量 + 95% CI + 校正方法 |
| **claim-strength** | overclaim / not supported / too strong | 降低表述强度，并在讨论里给替代解释 |
| **prior-work** | should cite / already reported | 补引用并写清增量；确属已知就改成"确认并扩展" |
| **clarity** | unclear / confusing / rewrite | 重写该段，回应里引改后原句 + page/line |
| **method-detail** | provide more detail / reagent / version | 补到可复现粒度，移到 SI 并在正文加指引 |
| **disagreement** | fundamentally flawed / not convincing | 先复述关切，再给证据，必要时请编辑裁决 |

分类是关键词启发式，可能误判——**每条都要自己确认**，尤其是"统计质疑"和"过度声称"这两类，判错方向的代价最大。

## 第二步：逐条回应的四段结构

每条都按这个顺序写：

1. **复述关切**（用自己的话）：证明你读懂了。不复述就等于没读。
2. **我们的判断**：同意 / 部分同意 / 不同意——先给结论。
3. **依据**：数据、补充分析、或引文。不同意时必须给数据，不能只给观点。
4. **改动定位**：`p.X, l.YY` 与 `图 Z`。没有定位的回应等于没改。

## 第三步：三个反直觉的规则

**1. 顺从换不来好感，只会引来新一轮要求。**
无原则地"我们已全部修改"会让审稿人认为你没思考，下一轮提更多。对不成立的批评，用数据辩；辩不动的，明确写"我们保留意见，理由如下"，请编辑裁决。

**2. "补实验"要分流，不要全接。**
全接 = 延长 3–6 个月且可能改变结论。分流判据：
- 补了能改变主结论 → 必须补
- 补了只影响泛化范围 → 降级为 limitation，在讨论里写清边界
- 技术上做不到 → 说明限制，并给替代证据（不同队列/不同方法/文献支持）

**3. 统计质疑不要用文字回应。**
"我们已增加说明"是最差的回应。必须重跑并给：效应量、95% CI、精确 n、校正方法、以及修正后的数值对比（改前 → 改后）。

## 第四步：分歧升级到编辑的写法

当与审稿人根本分歧时，单独一段写给编辑：

```
我们与 Reviewer 2 在 X 上存在实质分歧，焦点是 Y。
我们的立场基于：（1）…（数据/引文）（2）…
审稿人的立场可能是：（客观复述，不曲解）
若编辑认为需要，我们愿意补做 Z（预计 N 周）。
```

关键：**客观复述对方立场**。曲解审稿人是最快失去编辑信任的方式。

## 硬规矩

- 回应信与修改稿必须能逐条对上；审稿人会核对。
- 不要删改审稿人没提到的部分（会造成新的不一致）。
- 每轮回应都保留历史版本：`submission_event` 里记 `review_returned` 与 `decision`，`docs/` 里存回应原件。
- 拒稿后的下一步用 `science_submission_route` 的决策分支，不要凭情绪决定降档还是重投。
