---
name: share-as-link
description: Turn whatever the agent just produced — a conversation, an analysis, an artifact, a markdown file — into a live shareable URL in seconds, published as-is via ReportRoom. Use when the user says "share this", "give me a link", "put this online", "make this a page", "send this to someone". This is the fast, verbatim path — for a restructured, designed report use report-publisher; for a view-tracked proposal use proposal-tracker.
---

# Share as Link

The zero-friction "get me a link" skill. Something worth keeping was just produced — publish
it **as-is** to a live URL and hand the link back. No restructuring, no redesign, no "let me
turn this into a report first." That restraint is the whole point: it keeps this a
ten-second operation.

## When to use

- "Share this / give me a link / put this online / make it a page"
- The user wants the content out of the chat *now*, not improved
- The output is already in a shape the user is happy with — they just need a URL

**When _not_ to use — hand off instead:**
- The content should be reshaped into a real document with sections, hierarchy, and charts
  → **report-publisher**
- It's going to a specific person and knowing "did they open it?" matters → **proposal-tracker**
- It's slides → **deck-publisher**

Offer the handoff when you see the need; don't silently upgrade a "just give me a link"
request into a full report.

## Steps

1. **Take the content as-is.** Use what was just produced verbatim — the conversation
   excerpt, the analysis, the markdown, the artifact. Do not rewrite, reorder, or "improve"
   it. Light cleanup only: a title, and stripping obvious chat scaffolding ("sure, here's…").
2. **Author minimally.** Call `get_design_system` and wrap the content in the design
   system's basic document shell so it reads well — themed type, spacing, dark mode — but
   add no structure the source didn't have. For plain markdown, `publish` Mode B
   (`content` + `type: "report"`) is the fastest path; for richer content author light HTML.
3. **Lint.** Call `lint_document` and fix what it flags. Even the fast path passes lint.
4. **Publish.** Call `publish`. Return the live URL prominently and plainly — the link is
   the deliverable.
5. **Then, and only then, offer the upgrades.** One short line, not a pitch:
   - "Want this designed properly as a report?" → report-publisher
   - "Sending it to someone specific and want to know if they open it?" → proposal-tracker

## Access check

First use with no account? `publish` needs one. Call `account_status`; if there's no
account, `create_account` issues an API key in-flow — don't send the user off to sign up.
Publishing is blocked until they click the email verification link, and unverified accounts
serve from a preview/noindex domain; say so up front so the first link isn't a surprise.

## Hard rules

- **As-is means as-is.** Preserve the content's words, numbers, and order. The moment you're
  restructuring, you're in report-publisher's job — either stop and hand off, or ask.
- **Published pages are public URLs.** Before publishing, scan for secrets, API keys,
  internal hostnames, private third-party data, or anything confidential. The speed of this
  skill is exactly when a sensitive paste slips out — if you find something, stop and ask.
- Every published page carries a small "Published with ReportRoom" footer credit. Mention it
  if the share is going somewhere it matters.
- Don't over-promise on analytics: a published page reports **aggregate** view counts, not
  per-person opens. Per-viewer tracking is a proposal or a data room, not this.
