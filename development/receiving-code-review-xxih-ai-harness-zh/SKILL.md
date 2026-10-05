---
name: receiving-code-review
description: 当你收到代码评审反馈，并且准备实现建议之前使用；特别是在反馈不清楚或技术上可疑时，它要求技术性核实，而不是表演式认同或盲目照做
---

# 接收代码评审

## 概览

代码评审需要技术判断，不需要情绪表演。

**核心原则：**先验证，再实现；先理解，再行动；技术正确性高于社交舒适感。

## 响应模式

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## 禁止性回应

**绝不要：**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now"（在验证之前）

**替代做法：**
- 用自己的话复述技术要求
- 如果不清楚，就提澄清问题
- 如果反馈不对，就用技术理由反驳
- 或者直接开始做事（行动 > 口头表态）

## 处理不清楚的反馈

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**示例：**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## 按反馈来源处理

### 来自人类协作者
- **可信任** —— 先理解清楚，再实现
- **范围不清仍要问**
- **不要表演式认同**
- **直接进入行动**，或给出技术性确认

### 来自外部 Reviewer
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**人类协作者的规则：**“External feedback - be skeptical, but check carefully”

## 面向“更专业实现”的 YAGNI 检查

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**人类协作者的规则：**“You and reviewer both report to me. If we don't need this feature, don't add it.”

## 实现顺序

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## 何时反驳

当出现以下情况时应反驳：
- 建议会破坏现有行为
- reviewer 缺少完整上下文
- 建议违反 YAGNI（功能根本没被使用）
- 对当前技术栈来说不正确
- 存在兼容性或历史原因
- 与人类协作者已有架构决策冲突

**如何反驳：**
- 用技术理由，不要带情绪防御
- 问具体问题
- 引用已有代码或测试
- 如果涉及架构，拉人类协作者一起判断

**如果你不舒服当场反驳：**可以说："Strange things are afoot at the Circle K"

## 正确认可反馈的方式

当反馈**确实正确**时：
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [直接修复，然后在代码里体现]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ 任何感谢式表达
```

**为什么不要说 thanks：**行动本身就说明你接收到了反馈。直接修就行。

## 如果你之前反驳错了

```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ 长篇道歉
❌ 解释自己为何当时要反驳
❌ 过度辩护
```

简洁、事实化地纠正，然后继续。

## 常见错误

| Mistake | Fix |
|---------|-----|
| Performative agreement | 复述要求或直接行动 |
| Blind implementation | 先对照代码库验证 |
| Batch without testing | 一项一项实现，一项一项测 |
| Assuming reviewer is right | 先检查是否会破坏现有行为 |
| Avoiding pushback | 技术正确性 > 社交舒适 |
| Partial implementation | 不清楚的项先全部澄清 |
| Can't verify, proceed anyway | 说明限制，并请求方向 |

## 真实例子

**表演式认同（坏）：**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**技术验证（好）：**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**YAGNI（好）：**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**不清楚的反馈（好）：**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## GitHub 线程回复

当你要回复 GitHub 的 inline review comment 时，应回复到原评论线程中（`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`），而不是发成顶层 PR 评论。

## 最终结论

**外部反馈 = 需要评估的建议，不是必须照做的命令。**

验证。提问。然后再实现。

不要表演式认同。始终坚持技术严谨。
