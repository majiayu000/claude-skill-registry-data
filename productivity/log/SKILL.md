---
name: log
description: 'Capture front door. Logs 1..N observations as card files at docs/work/{ID}.md (BUG / DEBT / GAP), gateway-inline — no dispatch. Use when the user says "log this", "track that", "note this down", or types `/super-bootstrap:log <observation>` — and when Claude needs to file its own findings (out-of-scope findings from a review, audit, or returned subagent report). A suspected duplicate is surfaced for the user''s pick (amend / new card / drop), never auto-resolved. Captures raw — the real/worth/now call is triage''s at pickup (`/super-bootstrap:triage`). Does NOT triage. Feature ideas log as GAP.'
tags: [log, capture, cards, pipeline]
---

# Log — Capture Front Door

Muscle-memory capture, run **gateway-inline** in the calling session — no dispatch. Takes one observation or a batch, classifies each into **BUG / DEBT / GAP**, checks against open cards, and writes each clear entry as `docs/work/{ID}.md` in `docs/work/TEMPLATE.md`'s shape. Capture is unconditional about worth (bugs, debt, design gaps, unverified ideas all land); the real/worth/now call runs at `/super-bootstrap:triage` on pickup.

All new cards route through this door — user-initiated and Claude-initiated captures alike. Hand-copying `docs/work/TEMPLATE.md` with the same high-water bump is the same door, by hand.

## When it fires

- **User** — explicit `/super-bootstrap:log <observation>`, or natural-language "log this / track that / note this down". Bare `/super-bootstrap:log` → ask what to capture (one line).
- **Claude** — its own captures: a bug spotted mid-task, out-of-scope findings a review or returned subagent surfaced. Batch them into one pass.

**A card is owed only for deferred or dropped work** — work that exits the current flow incomplete. Work completed in-flow carries no card debt. The trigger is completion-state (observable), not worth.

Out of lane: root-cause investigation (the triage lane), card deletion (the resolving session), rewriting existing blocks (threads are append-only). Feature ideas and unverified hunches are in lane — they log as GAP.

## Procedure

1. Read `docs/work/README.md` — categories, thread contract, and the **ID high-water mark** line. README absent, or present without the high-water line → write nothing; route: "run `/super-bootstrap:harness-bootstrap` to (re-)plant the work substrate, then re-log." When present: read `docs/decisions.md` § Closed Forks, `docs/parked.md`'s header, and `docs/outward/README.md`'s header too — each skipped silently when absent.
2. Classify each entry — **BUG** (broken behavior) / **DEBT** (works but rotting) / **GAP** (design hole or unverified idea). Three gates per entry, in order:
   - **Mover** — ask once, *whose hands move the next step — the repo's, yours, or an outside party's?* The repo → a card, through the gates below. Yours or an outside party's (a taste sitting, a line-by-line review, a portal registration, a reply to wait for) → an outward thread at `docs/outward/OUT-###.md` when the folder exists: origin block only, `docs/outward/TEMPLATE.md`'s shape (H1 `# OUT-### — {summary}`, then `Logged:` / `Source:` / `Next move:` / `Waiting on:` / `Repo tail — fires on:`, plus `Owning card:` when a card waits on that step; drop the template's leading comment), bumping the README's `OUT-000` high-water in the same write. Ask for the repo tail in one line whenever the observation doesn't name one — the answer lands the thread; only an item with no tail at all drops, per the container README. No `docs/outward/` but a flat `docs/outward.md` → the container predates the folder shape: write nothing for that entry and route: "run `/super-bootstrap:harness-bootstrap` — its sync splits `docs/outward.md` into `docs/outward/` — then re-log." Neither present → a card whose `Problem:` line names `waiting on {party}`, which the board's wait override reads. Mixed → split at capture: the repo's remainder is the card, the other step the thread, carrying `Owning card:` when the card waits on that step.
   - **Card shape** — every card names something to **do, fix, or decide**. A standing-watch entry (monitor / revisit later) rephrases as an action; names a trigger + `docs/parked.md` exists → park as `### PARK-###` (bump its `PARK-000` high-water in the same write); otherwise return it with the real fork: wire an observer at the fire-moment, or drop.
   - **Closed forks** — an entry re-walking a `docs/decisions.md` § Closed Forks verdict → surface the fork (its Because + Ref) instead of logging; genuinely new counter-evidence → ask as a reopen question. Never silently re-log a closed direction.
3. **Dedup — the call is the user's, not capture's.** Grep the open cards — plus the `docs/outward/OUT-*.md` threads when present — for each entry's subject (title keywords, `Area:` paths for cards; H1 summary or `Repo tail` path for outward threads); open a suspected match to confirm coverage. A suspected dup — pure duplicate or duplicate-with-new-fact alike — **writes nothing yet**: surface the entry, the covering card or thread (ID + the covering line), and the pick — **amend** (append the new fact) / **new card** (genuinely distinct) / **drop**. Execute the pick: amend → append `## Amendment — {date} · {source}` at the owning card's or outward thread's end, the new fact alone, nothing restated — on an outward thread whose `Next move` / `Waiting on` the fact changes, that block restates those two lines and leads from there.
4. Assign IDs — next per category = max+1 from the README's high-water line, **bumped in the same change** as the card write; an `OUT-###` takes max+1 from `docs/outward/README.md`'s own high-water line the same way. Never derive an ID from the live card files: resolved cards are deleted and their IDs stay consumed.
5. Write each clear entry as `docs/work/{ID}.md` — origin block only, `TEMPLATE.md`'s shape (H1 + `Logged:` / `Source:` / `Problem:` / `Area:` / `Prior:`; drop the template's leading comment). Stamp today's date. Capture the claim faithfully — this is the richest-context moment; the pickup session reads it cold. `Prior:` is a one-line suspected cause at most — later work falsifies it. Scale-module fact fields ride the origin block as further field lines when known at capture.
6. An entry too thin to classify or phrase as a readable card → hold it unwritten and ask its one discriminating question (e.g. "broken now, or works-but-suboptimal?"); the answer lands it.

## Rules

- **Batch over loop.** Classify the whole batch in one pass; clear entries land immediately, dup and too-thin entries surface together — never block clear writes waiting on one fork.
- **Capture, don't gate.** Write every classifiable, non-duplicate entry — unverified ideas included. Worth is triage's call at pickup.
- **Append, never overwrite.** Origin blocks are frozen at capture; the only write to an existing card is a new dated `## Amendment` at end of file — and only on the user's amend pick.
- **Write cards, never investigate.** No root-cause prose, no fix design.
- **Minimum questions.** One discriminating question per genuinely ambiguous entry — capture dies if logging becomes an interrogation.
