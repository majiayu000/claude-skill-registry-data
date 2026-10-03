---
name: bug-from-user
description: Convert a vague user complaint into a reproducible bug report a solo dev can act on. Use when the user pastes a confusing customer message, says "user says it's broken but I can't repro", "this email makes no sense", or wants to triage a bug report.
---

# Bug from User / 用户反馈转 Bug

## When to use

- A user has reported a problem in **prose** (email, Discord, Twitter DM, support ticket).
- The dev cannot tell from the message:
  - what was expected vs. what actually happened
  - the steps to reproduce
  - whether it's a real bug, user error, or a feature request in disguise
- The dev wants a **GitHub issue** or **internal note** they can later sit down and fix.

## When NOT to use

- The user has already produced a **clean, reproducible report**. Don't re-process it.
- The complaint is **subjective** ("it's slow", "it's ugly") with no measurable claim — that's a UX or perf investigation, not a bug.
- The user is **asking for a feature** (e.g. "can you add X?") — file as feature request, not bug.

## The four-question conversion

For any prose complaint, reduce it to:

1. **Trigger** — what did the user *do* (action, click, command, input)?
2. **Expected** — what did they expect to happen?
3. **Actual** — what actually happened?
4. **Surface** — where did it happen (URL, screen, version, browser, OS)?

If any of the four is missing, **flag it as a follow-up question** rather than guessing.

## Output format

```markdown
### Bug: <one-sentence headline, user-perspective>

**Trigger:**
1. <step>
2. <step>

**Expected:** <what they expected>

**Actual:** <what actually happened>

**Surface:** <version / browser / OS / URL>

**Confidence:** <high | medium | low>
- high: report is self-contained, can repro from this alone
- medium: 1–2 reasonable assumptions made
- low: significant guessing — ask user to confirm

**Follow-ups (if any):**
- <question to ask the user>
```

## Worked example

**Input (raw user email):**
> "hey i tried buying the pro plan tonight and the website just kept loading forever, i refreshed a few times then gave up. using safari on my macbook"

**Output:**
```markdown
### Bug: Pro plan checkout hangs on Safari (macOS)

**Trigger:**
1. Visit pricing page on Safari (macOS).
2. Click "Pro plan" purchase button.
3. Observe checkout flow.

**Expected:** Stripe checkout opens within a few seconds.

**Actual:** Page stays in loading state indefinitely; refresh does not recover.

**Surface:** Safari on macOS. Version of Safari and macOS unknown. Pricing page URL unknown (likely /pricing).

**Confidence:** medium
- Assumed pricing page URL is /pricing.
- Assumed checkout uses Stripe.

**Follow-ups:**
- Which Safari version + macOS version?
- Does Chrome on the same machine reproduce it?
- Browser console errors (if comfortable opening DevTools)?
```

## Anti-patterns to avoid

- **Don't assume severity** — "P0 outage" without evidence is alarmist.
- **Don't guess root cause** in the report — that's the dev's job after reading. The report describes symptoms.
- **Don't promise a fix timeline** — that goes in the reply email, not the bug report.

---

## 中文版

### 何时使用

- 用户用**散文**报了一个问题（邮件、Discord、推特 DM、工单）。
- 看不出：
  - 期望 vs 实际
  - 复现步骤
  - 是真 bug、用户操作问题、还是变相的功能请求

### 何时不使用

- 用户已经写好了**清晰可复现**的报告——别重新加工。
- 抱怨是**主观**的（"慢"、"丑"），没有可测指标——那是 UX/性能调研，不是 bug。
- 用户是**要功能**——按 feature request 处理。

### 四问转化法

把任何散文压成 4 个问题：

1. **触发**——用户做了什么动作？
2. **期望**——他们期望发生什么？
3. **实际**——实际发生了什么？
4. **环境**——在哪里发生（URL、屏幕、版本、浏览器、系统）？

任意一项缺失 → **列为待问**，不要猜。

### 输出

```markdown
### Bug: <一句话标题，用户视角>

**触发：**
1. <步骤>
2. <步骤>

**期望：** <…>

**实际：** <…>

**环境：** <…>

**置信度：** <high | medium | low>

**待问：**
- <…>
```

### 反模式

- **不要乱定优先级**——没证据就"P0"是恐慌。
- **不要在报告里猜根因**——根因是开发读完之后的事，报告只描述现象。
- **不要承诺修复时间**——那写在回复邮件里，不写在 bug 单里。
