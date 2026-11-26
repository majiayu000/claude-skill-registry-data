---
name: tregExtension
description: Reach treg's catalog from log. `tregSearch` finds an endpoint by the job, `tregGet` gives its price and params, and `tregCall` calls it with the key held server-side; a priced endpoint only runs as `tregCallLive` when the owner approved the spend. Use whenever something has to be looked up from an external source (rule 53), such as web search, X or TikTok data, SEO or enrichment.
---

# tregExtension

## The loop

1. **Search by the job.** `tregSearch` { query: ["<what you want done>"] }. Pick one of the endpoints it returns. Never guess an id.
2. **Read it.** `tregGet` { id } shows its price and its params, and a call that works.
3. **Call it.** `tregCall` { id, params: "<json object>" }.
   - A free endpoint answers straight away.
   - A priced one comes back as a dry run with its price. Run it only when the owner asked for that spend: `tregCallLive` { id, params, approvedBy: "<owner>", confirmLive: true }.
4. **Name the source.** Say which endpoint the answer came from (rule 53).

## Hard boundaries

- Nothing that costs money runs unless the owner asked for it (rule 41).
- Every call goes through these tools, never a hand-run `treg` from a shell for log's work (rule 163).
- treg's balance: `balance`. How long a call took: `timing` { call }.

Docs: `docs/extensions/treg.md`. Spec: `docs/specs/treg.md`.
