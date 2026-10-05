---
name: new-adr
description: Use this skill when the user asks to create, write, draft, or open a new ADR (architecture decision record). Triggers on phrases like "new ADR", "write an ADR for...", "record this decision", "let's ADR this". Do NOT use for RFCs (use `new-rfc`) or feature specs (use `new-spec`).
---

# Skill: new-adr

Create a new ADR in `docs/adr/` from the template, with the next sequential
number.

## When to invoke

Before invoking, confirm:

1. The decision is about *architecture or shared infrastructure*, not a
   single feature's internals (that's a spec).
2. The decision has been *made or is being formally proposed*. ADRs are not
   a venue for open-ended discussion — that's an RFC.
3. There is a *concrete tradeoff* — at least one viable alternative was
   considered. If there's only one option, you don't need an ADR.
4. The record is *one decision wide*. If you're packing three or more
   load-bearing sub-decisions into a single ADR, stop and ask whether this is
   really one decision — or an umbrella that should be an RFC spawning several
   smaller ADRs. For an ADR, *complete* is not *exhaustive*: the RFC carries the
   debate, the ADR records the durable outcome.

If any of these checks fail, push back rather than proceeding.

## Procedure

1. Find the next number. The bundled helper prints the next 4-digit
   ordinal — `0001` if no ADRs exist yet, max-plus-one otherwise. It
   parses the full digit prefix, so a `00099-foo.md` correctly yields
   `0100` (not `0010`):

   ```bash
   python3 scripts/next-ordinal.py docs/adr
   ```

   (The script lives next to this `SKILL.md` under `scripts/`. Python
   is preferred over `ls | grep | sed | sort` so the snippet works the
   same way on native Windows, macOS, and Linux.)

2. Pick a kebab-case filename title from the user's description. Keep it
   short and declarative — `0007-primary-store-postgres-over-dynamodb.md`,
   not `0007-decision-about-the-database.md`. The H1 title inside the file
   names the problem *and* the chosen solution together — "Primary store
   for user activity: Postgres over DynamoDB" — so the decision is legible
   from the index alone; keep the `ADR-NNNN` ordinal prefix on it. **Keep it short: the title
   *identifies* the decision, it doesn't encode the rationale** — the detail
   belongs in the Decision section, not the H1. A title that compresses the whole
   argument into a clause makes the ADR index hard to scan.

3. Copy this skill's bundled `assets/adr.md` into `docs/adr/` and
   rename to `NNNN-<title>.md`. (Paths are skill-relative — the
   `assets/` folder lives next to this `SKILL.md` wherever your IDE
   installed the skill.)

4. Fill in the frontmatter: status `Proposed`, today's date, the
   `Decision-makers` who own the call, and — when the decision was run past
   others — the `Consulted` (whose input was sought, two-way) and `Informed`
   (who is kept up to date, one-way). Delete the `Consulted`/`Informed` lines
   if neither applies. Keep the metadata *pointer-like* — `Consulted` and
   `Related` are short lists of handles and ADR/RFC/spec references, not prose.
   If a relationship needs explaining, the explanation goes in Context or
   References, never in the frontmatter.

5. **Frame the decision before drafting — offer, don't force.** An ADR records a
   decision *already made*, so the job here is to isolate it cleanly, not to
   re-open it. Read the request:
   - **When the decision is already crisp** (a clear choice, a named driver, an
     obvious tradeoff), infer the frame and go straight to drafting — don't make
     the author answer a questionnaire they've already answered.
   - **When it arrives tangled** (rationale, history, and several sub-decisions
     in one breath — the RFC-residue an ADR should shed), walk a short decision
     frame and reflect it back before drafting: the decision in one sentence; the
     problem it resolves; the alternatives seriously considered; the driver that
     made the chosen option win; what we're giving up; whether it replaces or
     amends a prior ADR.

   Synthesize the frame into the title, the Decision sentence, Context,
   Consequences, and Alternatives below. The frame is a thinking aid, not a
   required form — a half-shaped decision is normal input.

6. Help the user draft the sections. Push back if any is empty or hand-wavy:
   - Context with no constraints listed → ask what's actually constraining
     this choice.
   - Decision without a single declarative sentence at the top → write one.
   - Consequences without honest negatives → ask what we're giving up.
   - Alternatives without rejection reasons → ask why each was rejected.

   Several sections are optional — offer them, don't force them; include each
   when it earns its place and delete it otherwise:
   - **Decision summary** — a first-screen TL;DR (Decision / Because / Applies
     to / Tradeoff accepted / Revisit if) placed before Context. Offer it once
     the ADR is long enough that the decision isn't visible on the first screen
     — a multi-line title, a paragraph of metadata, a long Context push it down;
     skip it on a short ADR, where five restated lines are pure redundancy.
     Every line restates the body, so it never carries new reasoning and is
     never a place to weigh options against each other. When you include it,
     its `Revisit if:` **restates** the Consequences `Revisit if:` line verbatim
     — the two must not diverge.
   - **Decision drivers** — the criteria the choice was judged against. Add it
     when more than one option was viable, so each alternative is rejected
     against a *stated* criterion rather than an ad-hoc reason.
   - **Confirmation** — how conformance with the decision will be verified,
     structured as `Mode` / `Signal` / `Owner`, where `Mode` is one of
     `reviewer-checked | lint/CI | architecture fitness test | periodic audit |
     none`. Where a reader would plausibly expect a conformance mechanism,
     prefer an explicit `Mode: none` (with a one-line reason) over silently
     deleting the section — a non-checkable residual should be visible, not
     hidden. Delete the section only for trivial decisions where no one would
     expect a check.

   One field in the always-present Consequences section is recommended, not
   optional:
   - **Revisit if** — the named trigger for reconsidering the decision (a new
     constraint, a failed confirmation, changed platform support, a scale
     threshold). It lives in Consequences as its canonical home — present even
     when the optional Decision summary is deleted — and is recommended for any
     decision likely to age. For one that genuinely won't, `Revisit if: stable
     — no foreseeable trigger` is a valid explicit value, not a reason to omit
     the line.

7. Update `docs/adr/README.md` to add the new ADR to the table.

8. Leave the status `Proposed`. Once the decision-makers sign off, mark it
   `Accepted`; if they decline it, mark it `Rejected` and keep the file — a
   recorded rejection stops the same option being re-proposed later. After
   `Accepted`, the body is frozen (see Lifecycle below).

## Lifecycle after acceptance

- **Reversing a decision.** Don't edit an accepted ADR. Write a *new* ADR for
  the new decision, set its `Supersedes:` to the old ADR's number, and flip the
  old ADR's status to `Superseded by ADR-NNNN` — status line only, the old body
  stays as history. The cross-reference points both ways.
- **Deprecated vs Superseded.** Mark an ADR `Deprecated` when the decision no
  longer applies and nothing replaces it; `Superseded by ADR-NNNN` when a
  specific later ADR replaces it.
- **Backfilling.** Recording a decision made months ago is fine — reconstruct
  the Context from memory and history, list the people who actually decided as
  `Decision-makers`, and note in References that it's a backfill.

## Anti-patterns to refuse

- "Make this ADR say we're definitely using X" before discussion has happened →
  that's an RFC, not an ADR. An ADR records a decision already made; an open
  debate is an RFC, and the accepted RFC then produces the ADR. Suggest opening
  one instead.
- Editing an accepted ADR's body → ADRs are immutable. A reversal is a *new*
  ADR that supersedes the old one (see Lifecycle above), never an edit.
- A title that carries the whole rationale → shorten it to *identify* the
  decision; the detail lives in the Decision section, and a scannable ADR index
  depends on it.
- Packing several independent load-bearing decisions into one ADR → split them.
  One ADR, one durable decision; an umbrella belongs in an RFC that spawns the
  ADRs.
