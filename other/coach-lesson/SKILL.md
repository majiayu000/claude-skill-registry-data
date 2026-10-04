---
name: coach-lesson
description: >
  Author a complete both-seats coaching lesson for a BBA-NATIVE bidding scenario
  and produce all served artifacts in one consistent pass: curate the pool →
  tokenized coaching-curated/<scn>.pbn → gated promote to served coaching/<scn>.pbn →
  resolve to South=student coaching-non-rotated/<scn>.pbn (bridge-classroom) →
  update both toc.json files. Invoke as `/coach-lesson <Scenario>` (e.g.
  `/coach-lesson Fourth_Suit_Forcing`). Use ONLY for conventions BBA bids natively
  (its bba/<scn>.pbn [Auction] is the answer key — Basics, New_Minor_Forcing,
  Fourth_Suit_Forcing). For conventions BBA CANNOT bid (Spiral Raises), use the
  py/spiral_auction.py substitution path instead — not this skill.
---

# coach-lesson — bootstrap a full coaching lesson for a BBA-native bidding scenario

> **⚠️ ROTATION TOKENS ARE RETIRED (2026-06-28).** Bridge Classroom never supported
> or used them. **Author every lesson token-free, directly from the fixed South =
> student seat** — South's calls in second person ("you bid 4\C"), partner's in third
> ("your partner answers 4\S"). NO `@S`/`@v(...)` tokens. Because the prose is already
> South-fixed, the `nonrotate.py` resolve step below is OBSOLETE — the three layers
> (`coaching-curated/`, `coaching/`, `coaching-non-rotated/`) are now the SAME
> token-free file (like the defense sets: byte-identical). Where the steps below say
> "tokenized" / "rotation pronoun tokens" / "resolve rotation tokens," ignore that and
> author/keep plain South-fixed prose. See `coaching-curated/GENERATOR.md` (updated).

`$ARGUMENTS` is the scenario name (a `btn/<Scenario>.btn` stem, e.g.
`Fourth_Suit_Forcing`). Call it `<scn>` below. Run everything from the project root.

## Precondition check (do this first)
1. Confirm `btn/<scn>.btn` exists and its `# bba-works:` is `true` (BBA bids the
   convention natively). If BBA can't bid it, STOP — this is the spiral-auction path,
   not this skill.
2. Confirm the dealer pipeline through `bba/` is present: `bba/<scn>.pbn` and
   `bba-filtered/<scn>.pbn`. If missing, the upstream pipeline (`dlr→pbn→rotate→bba→
   filter`) must run first (Windows VM for bba) — flag to David; don't fake it.
3. Read `btn/<scn>.btn`'s `/*@chat */` block — it is the convention's source of truth
   (what each call shows, plus any partnership-agreement caveats). Read the
   bridgebum/reference URL it cites if present.
4. Note the **seats**: most of these deal `dealer north`, so North opens and **South
   (the student) makes the hero call**. Verify by reading a few `bba/<scn>.pbn`
   `[Auction]` blocks and mapping calls to seats by dealer.

The sibling **New_Minor_Forcing** is the canonical worked example of this whole flow —
inspect its artifacts when unsure.

## Phase 1 — Curate (→ bba-curated/<scn>.pbn)
Grade the filtered pool and annotate it, exactly as for New_Minor_Forcing (design:
`notes/plans/pbn-curation-plan.md`).
- Layer A features: `python3 -P py/curate.py <scn>` (resumable; reads the `.btn`
  `# curate:` directive).
- Layer B grading: fan out subagents to grade each board's BIDDING
  (textbook / standard / judgment / reject) per the rubric in `notes/plans/pbn-curation-plan.md`;
  write verdicts to `bba-curated/<scn>-graded.json`. Borderline-but-defensible calls
  are **judgment + also_ok**, never reject (board-137 calibration).
- Annotate: `python3 -P py/annotate.py <scn>` → inserts `{Curate ...}` blocks into
  `bba-curated/<scn>.pbn`.

## Phase 2 — Author the tokenized lesson (→ coaching-curated/<scn>.pbn)
This is the rich, both-seats, rotation-ready artifact. Voice + structure spec:
`coaching-curated/GENERATOR.md`. Read it.
1. `python3 -P py/coach.py packets <scn> "bidding=textbook,judgment" "diff<=3" -n 30`
   → selects ~30 decision-rich boards, writes packets to `coaching-curated/.work/`.
2. Subagents author the prose per packet using the **rotation pronoun tokens** so the
   lesson renders for either seat (`@S` / `@s`, `@Your` / `@your`, `@v(base|third)` —
   parens, not braces; use `@S` at most once per chunk). Rules:
   - one `[BID <call>]` anchor per **N/S non-pass call** (both seats get anchors here —
     rotation may seat the student in either); a framing-only intro before the first;
   - describe what each call SHOWS by agreement — never the actor's concrete hidden
     holding during the auction;
   - `[ACCEPT <call>]` on any genuine judgment alternative;
   - close each board with `[show NS]` + a short result reflection; suit symbols
     `\S \H \D \C`; plain commas.
   Write `coaching-curated/.work/<scn>-coach*.json` as `{board, coaching}` objects.
3. `python3 -P py/coach.py splice <scn>` → builds `coaching-curated/<scn>.pbn`.
4. `python3 -P py/coach.py validate <scn>` → must report **0 issues** (marker
   structure + suit-quality + ordering lint; "solid" only when the suit truly is
   AKQ-solid — see GENERATOR.md).

## Phase 3 — Promote to served (→ coaching/<scn>.pbn)
`python3 -P py/promote.py <scn>` — gated copy of coaching-curated → coaching. It only
promotes if all gates pass; it reports blocked scenarios and exits non-zero on any
block. **Only commit YOUR scenario's promoted file**; if promote.py syncs other
eligible scenarios too, flag them, don't claim them.

## Phase 4 — Resolve to South=student (→ coaching-non-rotated/<scn>.pbn)
Two commands — `nonrotate.py` does the resolve+fold deterministically, then
`bridge_classroom.py` makes it renderer-ready:

    python3 -P py/nonrotate.py <scn>
    python3 -P py/bridge_classroom.py <scn>

`nonrotate.py` reads `coaching-curated/<scn>.pbn` and writes
`coaching-non-rotated/<scn>.pbn`, doing both transforms the non-rotated file needs:
1. **Resolves rotation tokens** for a fixed South seat (the trainer's `fill_pronouns`
   rule, but position-aware so a mid-sentence `@S` reads "you", not "You"): South's
   calls render 2nd person, partner's (North's) 3rd person.
2. **Folds partner's calls**: keeps a `[BID <call>]` anchor on **every South call and
   only South's calls** (each on its own line); merges each partner call into the
   adjacent South chunk in 3rd person (prepended when South is the responder, appended
   when South is the opener — it detects which from the auction); and anchors South's
   **auction-ending Pass** as `[BID Pass] … you pass; <contract> is the final contract.`
   `[ACCEPT]` markers ride along inside their South chunk.

`bridge_classroom.py` then strips the pre-auction `{Shape}/{HCP}/{Curate}` blocks,
renumbers `[Board]` 1..n, preserves `[OriginalBoard]`, and ensures the block opens with
`[show S]`. Both scripts are idempotent; re-run `nonrotate.py` (it rebuilds from
curated) whenever the curated prose changes, then `bridge_classroom.py`.

(Reference clean output: `coaching-non-rotated/Fourth_Suit_Forcing.pbn` or
`Spiral_Raises_Wolpert.pbn`. The old `New_Minor_Forcing.pbn`, `Basic_Overcall.pbn`,
`Basic_Takeout_Double.pbn` predate the fold and still carry un-folded partner anchors —
a defect to fix by re-running `nonrotate.py`, not a model to copy.)

## Phase 5 — Verify (all must pass before declaring done)
- **Anchor check** (the load-bearing gate): parse each non-rotated board's auction by
  dealer-seat; assert every `[BID]` maps to a South call, every South non-pass call is
  anchored, and **no partner call carries an anchor**. (Reuse the parse-by-seat check
  used to audit the existing files.)
- `coaching-non-rotated/<scn>.pbn` has **0** `@S/@v(/@Your` tokens left.
- All boards parse via `endplay` (the trainer's loader) in all three of
  coaching-curated / coaching / coaching-non-rotated.
- No hidden-hand reveal mid-auction; suit symbols render; ~4 coaching beats/board.
- **toc.json**: add the lesson to BOTH `coaching-curated/toc.json` and
  `coaching-non-rotated/toc.json` under the right category (e.g. "Minor/Major
  Sequences"): `id: <scn>`, a human `name`, one-line `description`, `difficulty`.
  Re-validate both as JSON.
- **Intro PDF (don't skip):** BC's "Intro" button fetches
  `<baseUrl>/<scn>_Intro.pdf` and only appears when that PDF exists — a new lesson
  shows NO intro until you generate it. Ensure `btn/<scn>.btn` has a real
  `/*@chat*/` body (a stub title yields an empty intro), then run
  `python3 build-scripts-mac/generate-intro-pdfs.py` (reportlab; deterministic) and
  commit `coaching-non-rotated/<scn>_Intro.pdf`.

## Report
List the boards chosen, the validate + anchor-check results, the promote.py output
(what it promoted/blocked), and any judgment calls. Commit only when David asks
("commit" = commit + push). Committing a coaching change means committing its
regenerated derived files too (curated + served + non-rotated + toc), or GitHub serves
stale and the menu shows MISSING/ORPHAN.

---
**First use:** `/coach-lesson Fourth_Suit_Forcing` — after 1♣/1♦/1♥, a 1-level
response, and a new suit by opener, the **fourth suit is artificial and game-forcing**;
dealer North, so South (student) makes the 4SF call; BBA bids it natively
(21GF-SPECIALS NS / 21GF-GIB EW).
