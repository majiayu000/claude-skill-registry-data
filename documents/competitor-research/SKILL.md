---
name: competitor-research
description: Map a product's competitive landscape — direct + adjacent competitors, their positioning, naming conventions, and white-space. Persists findings to a per-product competitors file so it compounds over time. Use before naming, positioning, pricing, or GTM — and as the collision baseline for name-clearance.
---

# competitor-research

## When you activate

- Before **naming** a product (this is phase 1 of `name-product` — it seeds themes and the collision baseline).
- Before positioning, pricing, or GTM.
- Whenever the user asks "who else does this", "competitors", "landscape", "who are we up against".

## What you produce

1. A **competitor table** — direct + adjacent + incumbents.
2. A **naming-conventions read** — what patterns the category uses (to fit or to break).
3. The **white-space** — positioning angles nobody owns.
4. A persisted file: `products/<slug>/competitors.md` (create/update, dedupe) so the picture **compounds** across sessions.

## Protocol

1. **Frame.** One line: what the product does · its category · its ICP. (Pull from the product config / positioning brief if it exists.)
2. **Find, three rings** (WebSearch, a few angles each):
   - **Direct** — same job-to-be-done for the same user.
   - **Adjacent** — overlapping capability or audience (these still cause name collisions).
   - **Incumbents** — the big, generic players everyone compares against.
3. **For each competitor, capture:** name · URL · one-line what-they-do · positioning angle · **naming pattern** (coined? descriptive? founder-name? compound? suffix?).
4. **Synthesize:**
   - Naming conventions in the space — and whether to **conform** (legibility) or **contrast** (distinctiveness).
   - Positioning white-space — angles/wording nobody owns.
   - The **collision baseline** — the exact names/roots a new name must avoid (hand this to `name-clearance`).
5. **Persist.** Write/merge `products/<slug>/competitors.md` with a dated section. Dedupe against prior entries; note what's new.
6. **Machine-readable twin (added for market-xray, 2026-08-16).** Also write/refresh `products/<slug>/research/competitors.csv` — columns `name,url,type,notes` (`type`: direct/adjacent) — the same deduped set. market-xray's stage 2 reads it to build `targets.json` after the operator prunes; standalone runs of this skill keep it current too.

## Output format

Markdown: a competitor table, then three short lists — *naming patterns*, *white-space*, *names/roots to avoid*. Keep it scannable. Cite URLs.

## Notes

- This is a living asset — each run appends and refines, so coverage improves over time.
- Run it **before** generating names: it both inspires themes and defines what must be cleared.
