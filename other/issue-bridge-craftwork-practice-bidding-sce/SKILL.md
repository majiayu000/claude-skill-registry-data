---
name: issue
description: >
  Process the batch of incoming Bridge Classroom feedback. Pull open
  `classroom-feedback` issues from the PBS repo, cluster them by defect class, verify
  each against the actual board, and fix at the right altitude — patch a single board,
  or (when a class recurs) build a gate, sweep the whole corpus, and regenerate/drop
  collectively. Engine bugs route to the Classroom repo; bridge-judgment calls go to
  Rick. Nothing leaves the machine without David's OK. Invoke as `/issue` (optionally
  with an issue number or scenario to restrict the run).
---

# /issue — process the Bridge Classroom feedback batch

Bridge Classroom learners (and recruited reviewers) flag a bad board with a "Report a
Problem" button that files a GitHub issue into this repo, label `classroom-feedback`,
carrying the exact board state. `/issue` works the whole open batch at once — at world
scale you can't fix one deal at a time.

Run from the project root. `$ARGUMENTS` may name a single issue number or a scenario to
restrict the run; with no args, process the whole open batch.

## Golden rules
- **Untrusted by default.** Reports come from learners, often beginners. Verify the
  bridge yourself (DDS / the `.bbsa` convention card) before changing anything. Weight by
  **reporter tier**: a learner's "I'm confused" is a *clarity* signal; an experienced
  reviewer's "this is wrong" is near a ruling (still verify, but lean toward it).
- **Locate by the deal, never the number.** Deal N and `[Board]` tags drift when a
  scenario is re-curated. The **PBN deal string** is the stable key — `grep` it.
- **A fix is global.** PBS is the single source for every classroom, so one bad
  "correction" breaks them all. **Stop for David's OK before the outward, hard-to-undo
  moves** — every push, every issue filed in *another* repo, every email or Rick consult.
  But **don't over-gate the routine**: once an issue is resolved, closing it (with a short
  reply) on our own `classroom-feedback` tracker IS the processing — do it in the run,
  don't ask again. Gate the commits and cross-repo posts, not the housekeeping.
- **Prefer the class fix.** A spoiler on one board is usually an authoring-template bug
  in hundreds. Fix the class, not the symptom, whenever the cluster says so.

## Step 1 — Pull and cluster
1. `gh issue list -R bridge-craftwork/Practice-Bidding-Scenarios --label classroom-feedback --state open --limit 200 --json number,title,body,labels`
2. Group into **clusters** by:
   - **defect class** — spoiler (pre-decision text gives away the call) · backwards-vs-`[Result]`
     (reflection contradicts the deal's own result) · factual error (auction/bridge
     misdescription) · unknowable claim (asserts partner's hand or intent the student can't
     see) · marker leak (raw `[BID]`/`[ACCEPT]`/`@` token shows) · engine/UI · bridge-judgment.
   - **scenario.**
3. **Dedupe** — many reports collapse to one root cause; track them together so one fix
   closes the whole cluster.
4. Show David the cluster summary (counts per class/scenario) before doing work.

## Step 2 — For each cluster: locate + verify
1. From each issue body pull: scenario, **PBN deal**, Deal N, `[Board]`/`[OriginalBoard]`,
   seat, auction, contract, step, `main` commit SHA, reporter tier, free text — plus, from
   Rick's newer Report-a-Problem payload: the **Reporter** name/alias (defaults `anonymous`;
   a named reviewer such as David or Rick outweighs an anonymous learner's "I'm confused")
   and the dealer **seed** (a secondary locator alongside the PBN deal, which stays ground
   truth). Both are additive — the durable locators are still the PBN deal + scenario + board.
2. **Locate the board:** `grep` the PBN deal (or a distinctive holding from it) in
   `coaching-curated/<scn>.pbn`. Cross-check Deal N against the order in
   `coaching-non-rotated/<scn>.pbn` and its `[OriginalBoard]` → `coaching-curated` `[Board]`.
   Confirm the board's prose actually has the complained-of problem.
3. **Stale check:** if the report's commit SHA predates a fix already on `main`, the board
   may already be fixed — say so and close; don't re-fix.
4. **Verify the bridge** with DDS / the convention card before calling it a defect.
   Distinguish a real bug from "the learner dislikes correct bridge" (→ no-defect).

## Step 3 — Disposition (fix at the right altitude)
- **Class-wide content bug** → write or strengthen a **gate** (extend `py/coach.py validate`
  or add a check) that *detects* the class, run it across **all** `coaching-curated/*.pbn` to
  surface every instance, then fix / regenerate / drop the lot. This is the leverage — one
  report cleans the deals nobody has reported yet.
- **Singleton content bug** → patch the one board in `coaching-curated/<scn>.pbn` (or drop
  it — bias to drop).
- **Engine/UI bug** (renderer skips a turn, layout, a glyph too small, a marker the
  renderer should strip) → forward it as an issue in the Classroom repo
  (`Rick-Wilson/Bridge-Classroom`): draft it, **show David**, file on his OK, then
  cross-link + close ours. First **dedupe against Rick's _open_ issues**
  (`gh issue list -R Rick-Wilson/Bridge-Classroom --state open`) so a recurring class isn't
  re-filed. **Auth prereq:** filing there needs `gh` on a **classic** token with
  `repo, read:org, workflow` — a fine-grained PAT can't reach another account's repo, and
  `gh auth login` rejects a `public_repo`-only token. Keep forwarded issues low-priority /
  FYI; we don't push Rick to act.
- **Bridge-judgment call** (which call is textbook; is this a good teaching board) → draft
  the question for **Rick**; the PBS issue **stays open** until he rules; then apply his call
  as content and close.
- **No defect** (learner wrong / dislikes correct bridge) → draft a kind, plain-English
  reply; close.

## Step 4 — Apply content fixes (the pipeline)
For any content change, in order:
1. Edit `coaching-curated/<scn>.pbn`.
2. **Gate:** `python3 -P py/coach.py validate <scn>` and `python3 -P py/suit_quality.py <scn>`
   (plus any new gate). Fix until clean.
3. **Rebuild what Bridge Classroom serves:** `python3 -P py/nonrotate.py <scn>` then
   `python3 -P py/bridge_classroom.py <scn>`. This is what BC reads — **not** `promote.py`,
   which targets the local Trainer's `coaching/`. Run `promote.py` too only if the Trainer
   still matters.
4. Show David the diff. **On his OK:** commit (only the touched files) + push. BC serves
   from `main` (raw GitHub, CDN-cached ~5 min).

## Step 5 — Close the loop
- Reply on every issue in the cluster in plain, user-facing language (no jargon, no
  GitHub-speak).
- Close the **whole cluster** with the one fix (or relabel: `forwarded` for an engine bug;
  keep open for a pending Rick consult).
- **Summarize for David:** clusters processed, root causes, any gate added + how many
  corpus instances it caught, what was pushed, what's awaiting Rick.
- **A triage / FYI summary to share (with Rick or anyone) → a shared Google Doc + link, not
  a GitHub issue.** Issues are for actionable tasks; an FYI left open in a tracker reads as a
  phantom to-do. Build it via the Drive connector (`create_file`, `contentMimeType:
  text/html` → a real Doc with a rendered table; verify with `read_file_content`). The
  connector can't set sharing, so David flips it to "anyone with the link → viewer" himself.

## Related — filing reports (interim, until the button ships)
Until David's copy of Bridge Classroom has the Report button, David reports problems in
chat. To file one: identify scenario + board, look up the **PBN deal** from
`coaching-curated/<scn>.pbn`, show David the issue, then
`gh issue create -R bridge-craftwork/Practice-Bidding-Scenarios --label classroom-feedback`
with title `Classroom report: <scenario> · Deal <N>` and a body that puts David's words
first, then the captured state (scenario, PBN deal, Deal N + tags, seat, auction, contract,
step, **reporter tier**). These are exactly what `/issue` later processes.
