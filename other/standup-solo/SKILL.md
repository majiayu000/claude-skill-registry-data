---
name: standup-solo
description: Run a 5-minute personal standup for a solo dev — what shipped yesterday, what's blocked, what's next today. Use when the user asks for a daily check-in, says "what should I work on today", "what did I do yesterday", or wants to break out of a productivity slump.
---

# Standup Solo / 单兵每日站会

## When to use

- The user is a solo operator (no team to standup with).
- They want **5 minutes of forced reflection**, not a project management session.
- They have access to whatever notes / commits / messages they made yesterday.

## When NOT to use

- The user wants a **multi-day retrospective** — that's [postmortem-solo](../postmortem-solo/SKILL.md).
- They want to **plan a sprint** — too granular, use a planning skill instead.
- They are clearly **burned out** — pushing them through standup theater is harmful. Suggest rest.

## The three questions

A solo standup is **three questions, hard limits**:

1. **What did I actually finish yesterday?** (Past, concrete, observable. "Worked on X" doesn't count — what was *done*?)
2. **What's blocked or about to block me?** (Anything where the next step depends on someone or something outside my control.)
3. **What is the *one* most important thing today?** (Singular. Force the user to commit.)

## Output format

```markdown
## Standup — YYYY-MM-DD

**Yesterday (shipped):**
- <thing 1>
- <thing 2>

**Yesterday (started but not finished):**
- <thing> — <why not done>

**Blocked:**
- <thing> — <waiting on what / who>

**Today's #1:**
> <one sentence, action-form>

**Today's #2 and #3 (only if #1 finishes):**
- <thing>
- <thing>
```

## Inputs the user can provide

To make output sharp, the user can paste any of:

- Yesterday's git log: `git log --since="yesterday" --author=<me> --oneline`
- Sent emails / Slack DMs from yesterday
- A screenshot of yesterday's todo app
- Just a stream-of-consciousness brain dump

If the dev gives nothing, ask **one question only**: *"What did you work on yesterday — give me 3 bullets, ugly is fine."*

## Worked example

**Input (raw):**
> "yesterday i fixed a bug in the auth flow, started on the new pricing page but it's like 60% done, also replied to like 8 customer emails. today i need to finish pricing page and figure out why stripe webhooks are firing twice."

**Output:**
```markdown
## Standup — 2026-04-30

**Yesterday (shipped):**
- Fixed bug in auth flow.
- Replied to 8 customer support emails.

**Yesterday (started but not finished):**
- New pricing page — ~60% done; carry over to today.

**Blocked:**
- (none reported)

**Today's #1:**
> Ship pricing page to production (the remaining 40% — copy, layout, deploy).

**Today's #2 and #3 (only if #1 finishes):**
- Investigate duplicate Stripe webhook firings.
```

## Anti-patterns

- **Don't list hopes as accomplishments.** "Worked on X" is not "shipped X". If it's not visible to a user, it didn't ship.
- **Don't have 5 #1 priorities.** That's 0 priorities.
- **Don't carry blocked items silently.** If a thing has been blocked 3+ days, escalate or kill it — note this in the standup.

---

## 中文版

### 何时使用

- 单兵作战，没团队可以开站会。
- 想要 **5 分钟强制反省**，不是项目管理会议。
- 手头有昨天的笔记/提交/消息可参考。

### 何时不使用

- 想要**跨多日回顾**——那是 postmortem-solo。
- 想要**冲刺规划**——颗粒度不够，换规划类技能。
- 已经明显**燃尽**——继续表演站会有害，建议休息。

### 三个问题

1. **昨天我到底完成了什么？**（过去时、具体、可观测。"在做 X"不算，要看做完了什么。）
2. **什么阻塞了我，或快要阻塞？**（下一步依赖外部人或外部物的所有事。）
3. **今天最重要的*一件*事是什么？**（单数。强制承诺。）

### 输出

```markdown
## 站会 — YYYY-MM-DD

**昨日已交付：**
- <项 1>
- <项 2>

**昨日开了头没做完：**
- <项> — <为何没做完>

**阻塞：**
- <项> — <等谁/等什么>

**今日 #1：**
> <一句话，动词开头>

**今日 #2 和 #3（仅当 #1 完成后再做）：**
- <项>
- <项>
```

### 反模式

- **别把"在做"当成"做完了"**——用户看不到的功能 = 没交付。
- **别有 5 个最高优先级**——那等于没优先级。
- **别让阻塞项静默累积**——超过 3 天就要升级或砍掉。
