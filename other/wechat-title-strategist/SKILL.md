---
name: wechat-title-strategist
description: Evaluate, rewrite, and select WeChat Official Account article titles for open rate, depth, reader promise, and account tone. Use when drafting, reviewing, publishing, or revising公众号文章标题, especially when titles may be generic, stale, clickbait, AI-flavored, or misaligned with the article's commercial/editorial intent.
---

# WeChat Title Strategist

Use this skill before finalizing any WeChat article title.

## Core Standard

A title must pass at least one primary route:

- **Depth route**: expresses a non-obvious thesis, business insight, structural judgment, or contrarian read.
- **Open-rate route**: creates a concrete curiosity gap, reader pain, useful promise, or timely tension that makes the target reader want to open.

If a title passes neither route, reject it even if it is accurate.

## Hard Rejection Rules

Reject titles that:

- Lead with stale AI discourse such as "别再写 Prompt", "Prompt 已死", "AI 时代来了", unless the article's actual evidence makes that wording newly valuable.
- Use vague academic wording: "浅谈", "思考", "探索", "实践", "趋势分析", "未来已来".
- Sound like generic AI slop: "一文看懂", "重磅", "颠覆", "震撼", "必须收藏", without concrete payoff.
- Contain too many English terms for a general WeChat audience when Chinese wording would be clearer.
- Describe the topic but not the reader's reason to open.
- Promise a conclusion the article does not prove.

## Title Test

For each candidate, score quickly:

- **Reader**: who is supposed to care?
- **Promise**: what will they get after opening?
- **Tension**: what conflict, surprise, or stakes exist?
- **Evidence**: what concrete fact, data point, product, or scene supports it?
- **Tone**: does it raise or lower the account's perceived quality?

Reject if any answer is vague.

## Generation Workflow

1. Extract the article's strongest thesis, reader pain, evidence, and account intent.
2. Generate 8-12 candidates across these buckets:
   - Depth thesis.
   - Business implication.
   - Concrete evidence or number.
   - Reader pain / workplace scene.
   - Contrarian but accurate angle.
   - Straight declarative title.
3. Remove weak or stale candidates using the rejection rules.
4. Return the top 3-5 with one-line rationale and risk.
5. Pick one final title only after it passes the title test.

## Output Format

```markdown
## Title Diagnosis
- Current title: ...
- Verdict: pass/fail
- Main problem: ...

## Candidates
1. ... — [route] [why it works] [risk]

## Recommended
...
```

Keep titles mostly under 30 Chinese characters when possible. A longer title is acceptable only when the extra words add real specificity.
