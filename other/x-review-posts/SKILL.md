---
name: x-review-posts
description: Use when a user asks to inspect published X/Twitter posts, Articles, Threads or an account through links, a browser, Chrome MCP, screenshots or exports and suggest concrete improvements to their content and publishing choices.
---

# Review published X content

For a new natural-language request, use `x-assistant` first when installed. If this workflow was explicitly selected, delegated with `routed_by: x-assistant`, or installed alone, execute directly; do not route back.

Use [the evidence guide](references/knowledge-guide.md), [browsing procedure](references/browsing.md) and [observation contract](references/observations.md). Answer in the user's language. This specialist provides content review, not a causal verdict from view counts.

For claims about the present algorithm, first read the dated-update procedure in [the knowledge guide](references/knowledge-guide.md). Apply relevant current updates alongside historical claims, and state the reviewed revision when it matters.

## Collect

Reuse confirmed URLs and prior observations. Follow the user's scope. With no count specified, review the latest 20 authored non-pinned items, plus the pinned item and up to five recent Articles, deduplicating actual content identities. This is a workload default, not posting advice. Related author Thread parts, corrections and quoted sources are supporting material. For an explicitly larger scope, continue in batches rather than present the default sample as the whole history.

Expand full text, enter Article bodies and view meaningful images/video. Record exact coverage and source method. Do not substitute a search snippet for the unread page. When Python is available, run `python3 scripts/summarize_posts.py --input observations.json` for precision, identity and age checks; otherwise use the observation contract directly. Keep Article/carrier metrics separate and retain unavailable data as unknown.

## Review

Screen every evidence topic for applicability and evaluate all applicable entries against the actual posts. Keep the per-post check ledger. Quote real openings, measure available text with `python3 scripts/inspect_draft.py --text post.txt` or the evidence guide's no-Python fallback, and examine promise versus delivery, evidence, reader use, format, images, links, replies, duplication and corrections.

For media, distinguish observed content from proposed changes. Confirmed no-image posts still require a material-specific image recommendation or reason for text-only treatment. Unviewed media stays unknown. When suggesting several images, specify each one's content and order; the first independently communicates the most useful finding. Explain supported media mechanisms without a guaranteed upload bonus.

Compare posts only with appropriate metric scopes, topics, ages, promotion/pinning and observation windows. Low public views do not identify a hidden label, cold-start state or suppression. Where reach diagnosis is requested, pass the observation record to that workflow if available, or apply the relevant corpus conditions directly.

## Deliver

Give priority actions, collection scope and unread portions, then per-post findings with actual evidence, specific changes, reasons and original citations. Include usable opening revisions for the two or three posts most worth changing; concentrate on the one post for a single-post request. Explain whether an action means revising existing text, issuing a correction or publishing genuinely new material. Existing repeated introductions are a reason to check added value before recommending more promotion. Do not claim to have changed live content.
