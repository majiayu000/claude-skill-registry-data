---
name: wechat-article-writer
description: Project-level WeChat article drafting workflow for turning source materials, repo intakes, product notes, screenshots, or existing markdown into a publishable Chinese公众号 draft. Use for writing, rewriting, evidence-gating, title options, platform adaptation, and image planning before optional publishing.
---

# WeChat Article Writer

Use this skill for the writing part of the project. Use `wechat-mp-writer` when the user also wants intake automation or publishing.

## Required Context

Read these project files when drafting from product or repo material:

- `docs/content-agent/workflow.md`
- `docs/content-agent/agent-prompt.md`
- `docs/content-agent/rules/writing-rules.md` if present and relevant
- The source ledger or intake summary for the current article

## Drafting Flow

1. Normalize inputs.
   - Identify source files, URLs, screenshots, README files, and user notes.
   - Ask focused questions only when a missing fact would materially change the article.
2. Build evidence.
   - Maintain verified, reasonable inference, unverified, and do-not-publish labels.
   - Do not turn unverified hypotheses into factual claims.
3. Choose article angle.
   - Prefer product-backed, concrete workplace or technical value.
   - Avoid generic "AI tool recommendation" framing unless the user explicitly wants it.
4. Write a WeChat draft.
   - Start with a concrete scene, contradiction, or strong conclusion.
   - Keep paragraphs scannable without flattening depth.
   - Make the authorial "I" light and functional.
   - Use source-backed technical details and product decisions.
5. Produce title options and visual plan.
   - Use `wechat-title-strategist` before selecting the final title.
   - Reject titles that are merely accurate but lack either depth or open-rate pull.
   - Avoid stale AI discourse ("别再写 Prompt", "Prompt 已死", generic "AI 时代来了") unless the article's evidence makes that phrasing newly valuable.
   - Use `wechat-visual-director` to create distinct cover/body visual routes.
   - Separate cover prompt from body illustration prompts.
   - Recommend screenshots where they carry more evidence than generated art.
6. Run a final risk gate.
   - Remove secrets, private customer data, unverifiable superiority claims, and sensitive internal strategy.

## Output Contract

Unless the user narrows the request, return or create:

- Final WeChat title
- Article markdown
- Evidence notes for major claims
- Cover direction
- Body image plan
- Self-review and remaining open questions

Do not publish from this skill directly; hand off to `wechat-mp-writer` or `baoyu-post-to-wechat`.
