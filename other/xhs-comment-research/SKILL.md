---
name: xhs-comment-research
description: Read and analyze Xiaohongshu comments from the user's signed-in Chrome session. Use to collect, export, summarize, or classify comments for content planning, follow-up posts, audience research, reply strategy, and 引流文案。
---

# XHS Comment Research

Use this skill to turn Xiaohongshu comment threads into content intelligence.

## Safety

- Stay read-only except for opening/expanding/scrolling comment UI needed to load text.
- Do not like, reply, delete, pin, report, publish, follow, message, or change settings.
- Do not inspect cookies, local storage, passwords, tokens, or browser profile files.
- Treat comments as user research. Quote sparingly; prefer paraphrase and theme summaries.
- If a captcha, login prompt, or permission prompt appears, stop and ask the user.

## Browser Path

Load `$browser-automation-router`, then use the Chrome plugin when comments require the user's logged-in session.

1. Confirm the Chrome plugin is available and the user has approved access to the intended tab.
2. Reuse an already-open note or creator-manager tab when possible.
3. Verify the visible account, note title, and URL before collecting data.
4. Prefer the plugin's current high-level snapshot, semantic locator, scroll, click, and text-reading operations.
5. Do not load repository-maintained JavaScript snippets or hard-code a selector recipe before inspecting the live page.
6. Use clicks only for harmless UI expansion such as "展开 ... 条回复".
7. If the plugin is unavailable, declare the fallback instead of launching a copied Chrome profile or reading browser state from disk.

## Extraction Workflow

1. Confirm target note title/URL and output folder.
2. Capture visible note metadata:
   - title
   - URL
   - displayed comment count
   - current loaded comment count
3. Identify the live comment scroll region from the current page snapshot and move from top to bottom in small batches.
4. Repeatedly expand visible reply controls when present.
5. Extract comment records from the visible page structure:
   - `id`
   - `isSub`
   - `name`
   - `content`
   - `date`
   - `like`
6. Deduplicate by `id` when available; otherwise by `name + content + date`.
7. Save raw JSON and an analysis markdown file in the article folder.

## Analysis Workflow

Group comments by useful content angles, not generic sentiment:

- engineering-complexity: architecture, components, concurrency, data, maintainability
- local-vs-online: localhost, "works on my machine", environment, deployment
- black-box-debugging: cannot debug, prompt iteration, token burn, frontend/backend diagnosis
- professional-validation: programmer still needed, someone must own review/兜底
- security-and-commercial-risk: security, data, payment, business liability
- pro-ai-non-cs: non-CS can build MVPs, product sense, demand discovery
- identity-conflict: 文科/理科/程序员 identity jokes or disputes
- content-hooks: phrases that can become titles, covers, comments, or follow-up posts

When revising content based on comments:

- Correct any earlier assumption that the comments do not support.
- Start from the actual dominant tension in the thread.
- Separate "what the comments say" from "our content judgment".
- Keep follow-up copy emotionally aware: acknowledge programmers' objections before giving advice to non-CS readers.

## Output Files

Use stable filenames:

- `comments-raw.json`: raw deduplicated comment records and metadata.
- `comment-analysis.md`: summary, themes, evidence snippets, and content implications.
- `content-pack.md`: update only when the user asks to revise the article package.

## Quality Bar

Before claiming the crawl is complete:

- Report loaded versus displayed comment counts.
- Explain if the platform did not expose all comments or if replies were still collapsed.
- Save enough raw data for later re-analysis.
- Do not pretend partial data is complete.

