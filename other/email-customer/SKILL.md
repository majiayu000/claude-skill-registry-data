---
name: email-customer
description: Draft a polite-but-firm reply to a tricky customer email — refund request, scope creep, complaint, billing dispute. Use when the user pastes a customer email and asks for a reply, mentions "how do I respond", "user is asking for a refund", "they want a discount", or any awkward customer-facing communication.
---

# Email Customer / 客户邮件回复

## When to use

- The dev is replying to a **real customer** (paying or potential).
- The reply needs to be **polite, firm, and short** — not corporate, not groveling.
- The situation is **awkward**: refund, dispute, scope creep, deadline push, complaint.

## When NOT to use

- A **routine inquiry** ("what's the price?") — answer directly, no skill needed.
- An **abusive or harassing** message — those need a moderation policy, not a charming reply. Suggest: don't engage; if needed, refund and ban.
- A **legal threat** — stop. Don't reply via skill. Suggest the user consult a lawyer first.

## Principles

A good solo-founder reply has four properties:

1. **Acknowledge** the specific concern (not "I understand your frustration").
2. **State the decision** plainly in **one sentence**, near the top.
3. **Give one reason**, no more. (Listing reasons reads as defensive.)
4. **Offer a concrete next step** — a workaround, a partial refund, a deadline, a closing line.

**Avoid:**

- "I'm sorry you feel that way" — not an apology, reads as dismissive.
- "Per our policy" — bureaucratic, hides the human behind procedure.
- Hedging multiple times in one email ("we *might* be able to *possibly* consider…").
- More than ~120 words. If it needs more, it's a phone call or a doc.

## Output format

Always produce:

1. **Subject:** (one short line, no "Re: Re:")
2. **Body:** (≤120 words, plain text, no signature)
3. **Internal note:** (one line for the dev — what they should do *operationally* after sending, e.g. "issue partial refund of $19", "add to email block list")

## Worked examples

### Example 1: Refund request after 60 days, policy is 30

**Customer:**
> "I bought the annual plan 60 days ago and barely used it. Can I get a refund?"

**Output:**

**Subject:** Refund on your annual plan

**Body:**
> Hi <name>,
>
> Refunds on annual plans are limited to the first 30 days, so a full refund isn't something I can offer here.
>
> What I can do: switch you to month-to-month and refund the unused months as account credit, or process a 50% refund on the remaining time. Either is fine — let me know which you'd prefer.
>
> — <you>

**Internal note:** If they pick option 2, refund $X via Stripe. If option 1, downgrade plan in admin and credit their balance.

---

### Example 2: Scope creep on a fixed-price contract

**Customer:**
> "Now that the dashboard is built, can you also add a CSV export and email reports? Should be quick."

**Output:**

**Subject:** Scope on the dashboard work

**Body:**
> Hi <name>,
>
> CSV export and scheduled email reports are both straightforward, but they're outside the original scope. Two paths:
>
> 1. Add them as a small follow-up at $X (≈Y days of work).
> 2. Hand off the codebase as-is and your team adds them later — happy to do a 30-min walkthrough either way.
>
> Let me know which fits better.
>
> — <you>

**Internal note:** If they pick option 1, send a 1-page change order before starting.

---

## Anti-patterns

- **Don't apologize for things that aren't your fault.** "Sorry the API was down" is fine; "Sorry you don't like our pricing" is not.
- **Don't promise a fix without a timeline.** Either commit ("by Friday") or say "I don't have an ETA yet."
- **Don't BCC yourself for "records."** Use a CRM or a notes file. BCC reads weird if the customer ever sees it.

---

## 中文版

### 何时使用

- 在回复**真实客户**（付费的或潜在的）。
- 回复需要**礼貌、坚定、简短**——不官腔，也不卑躬屈膝。
- 场景**棘手**：退款、争执、范围蔓延、延期、投诉。

### 何时不使用

- **日常咨询**（"多少钱？"）——直接回答，不需要这个技能。
- **辱骂或骚扰**邮件——需要的是封禁政策，不是回复技巧。建议：不回应；必要时退款 + 拉黑。
- **法律威胁**——停。先咨询律师，再考虑回复。

### 原则

好的回复有四个特征：

1. **承认**具体的问题（不是泛泛的"我理解您的沮丧"）。
2. **靠前一句**说清决定。
3. **给一个理由**，不要列三个（列多反而显得心虚）。
4. **给一个具体的下一步**——补偿方案、截止时间、收尾语。

**避免：**

- "对您的感受感到抱歉"——不是道歉，听起来像甩锅。
- "依据我们的政策"——官腔，把人藏在流程后面。
- 一封邮件里反复犹豫（"我们*或许*可以*考虑*…"）。
- 超过 ~120 字。再多就该改电话或长文档。

### 输出

1. **主题：**（一行短句）
2. **正文：**（≤120 字，纯文本，不加签名）
3. **内部备注：**（给开发者的操作指引——发完邮件还要做什么，比如"在 Stripe 退 $19"、"加入邮件黑名单"）

### 反模式

- **不要为不是自己的过错道歉。**
- **不要给不带时间的承诺。** 要么"周五前"，要么"暂时没 ETA"。
- **不要 BCC 自己留底。** 用 CRM 或笔记，BCC 万一被客户看到很尴尬。
