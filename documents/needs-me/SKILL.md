---
name: needs-me
description: "Session opener for the work that needs you. Scans what is open — cards, the test queue, outward threads, parked items when present — at origin-block grain, cuts it into three or four lenses that exist in this repo right now and asks which one (a free slot takes any focus in prose), then recommends up to five items in that lens with why they need you. A prose argument is the focus and skips the question. Items that need no one are counted, not listed — they belong to /super-bootstrap:autorun. Read-only."
tags: [needs-me, pickup, attention, session-opener]
---

# needs-me — what deserves your attention now

A recommender, not a board. The full list is the card folder itself; this door answers one question — *what is worth my sitting down for* — and hands the pick straight into pickup.

## Scan

`docs/work/` absent → "No runway installed. Run `/super-bootstrap:setup`." and stop.

Otherwise read, inline, cheap:

- every open card's origin block plus its latest `## ` heading (`docs/work/{BUG,DEBT,GAP}-###.md`) — Problem line + where the thread stopped;
- `docs/test-queue.md` § Pending entries, `docs/outward/OUT-*.md` origin + latest block, `docs/parked.md` entries — each only when the file exists;
- `docs/overview.md` Problem / User — the product anchor the ranking leans on.

Root `SESSION-STATE/` holds carry files → print `{N} carries in flight → /super-bootstrap:session-continue` before the lens question; the carries themselves stay unread. The pointer line prints whether or not the lens question runs.

Sort every item by the test in `${CLAUDE_PLUGIN_ROOT}/shared/user-wall.md`: **needs you** or **runs without you**. Only the first set goes further.

## Lenses — cut live, never fixed

Partition the needs-you set into three or four lenses that exist in *this* repo today, one concern each, named by what the user would sit down to do. Illustrations only — never a menu to copy: *decisions that unblock parked autorun work* · *product-anchor / taste items worth a long session* · *verify on device* · *outward — your move*. Each option carries a count and one line. Ask once with `AskUserQuestion`; its built-in Other slot takes a focus in prose. Empty needs-you set → skip the question and print `Nothing needs you right now.`, then § Recommend's two count lines (the `{M}` line only when any).

A prose argument (`/super-bootstrap:needs-me 只看 product`, `不碰 business`) is the focus — apply it, skip the question.

## Recommend

Deep-read the candidates in the chosen lens — past the origin, through the cold-reader read set `docs/work/README.md` § Thread contract names. Print at most five lines, leverage first (what its resolution unblocks, then how close it sits to the product anchor):

```
{ID}  {title}  — {why you, ≤ 8 words}
…
{N} items run without you → /super-bootstrap:autorun
{M} look done or premise-dead: {IDs} → offered for resolve at /super-bootstrap:session-close        (omit when none)
```

Reply with an ID and the session is in pickup — framing line + route per `CLAUDE.md`, no re-scan.

## Rules

- **Read-only.** Never edits, never runs git.
- **Needs-you only.** An item that runs without the user is the count line, never a row — `/super-bootstrap:autorun` owns it.
- **No board, no footer, no sub-verbs.** Zero rows in the lens → say so and name the next-fullest lens in one line.
