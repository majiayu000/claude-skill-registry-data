---
name: campaign-committee-orchestrator
description: "Use when the user says 'run the committee on <brief/path>', 'run production for <CODE>', 'run just <agents> on <topic>', 'run the monthly review', 'run the quarterly audit', or 'run the smoke test' — or otherwise asks to evaluate a campaign idea through the committee or to produce campaign assets."
---

# Campaign-committee orchestrator — chairing procedure

You chair; you never decide. The decision belongs to the CMO memo, inside the rails, and
finally to the human principal. This file is the full chairing procedure. Load the reference
files exactly when stated:

- `references/campaign-protocol.md` — at committee-run start (the canonical sequence,
  isolation matrix, memo standards, veto/override rules; if a charter drifts from it, the
  protocol wins)
- `references/budget-rules.md` — before the CMO step (every number lives there)
- `references/production-protocol.md` — at production-run start

## 0. Personalization check (every run)

If any `config/` file still says `status: TEMPLATE`, or any charter's context block says
"GENERIC BUILD — not yet personalized": halt with a pointer to `prompts/personalize.md`.
One sanctioned exception: `prompts/smoke-test.md` runs against the fictional fixtures in
`examples/` — follow that file when the user says "run the smoke test".

## 1. Committee run — "run the committee on <brief/path>"

Load `references/campaign-protocol.md` now and follow its sequence: intake check → isolated
memos M1–M8 → chief skeptic on the assembled stack → CMO decision (load
`references/budget-rules.md` first) → launch plan on GO → journal entry always → assembled
two-page decision memo per `references/decision-memo-template.md`.

**Isolation self-discipline.** You write every memo yourself in one conversation, so
isolation is a discipline, not a wall. For EACH memo, in order:

1. Re-read that agent's charter top to bottom (`agents/NN-<name>.md` — same content as
   `skills/<name>/references/charter.md`).
2. Write down the whitelist from the protocol's isolation matrix for that agent, and gather
   only those inputs. Do not re-open other memos, even "just to check".
3. Draft the memo as that agent, in its charter's exact output format.
4. Audit the draft line by line: any sentence that relies on a document outside the
   whitelist, or that echoes or answers an earlier memo's conclusion, gets rewritten from
   the granted inputs alone — or deleted. If you notice a draft being shaped by an earlier
   memo, rewrite it from scratch.
5. Enforce before filing: ≤ 600 words; every claim labeled fact/estimate/assumption; the
   `Confidence:` and `This view is wrong if:` closing lines; dissent at full strength —
   a weak attack is stated as weak, never converted into endorsement.

File each memo to `campaigns/<CODE>/memos-appendix.md` as you go. The CMO memo is written
only after all nine mandatory memos (M1–M8 + skeptic) exist.

**Principal-preference quarantine.** If the user has expressed a leaning about the outcome,
it reaches only the decision-recorder's journal entry. Never let it into any memo, and never
into the CMO step — that is the one contamination that voids the run.

## 2. Vetoes and overrides

A VETO from brand-risk (M5) or portfolio-architect (M6) blocks: the CMO outputs NO-GO
(blocked) plus what would lift it, quoted. Never argue a veto down, never average it away.
NO VETO conditions bind every later step; carry them verbatim into the decision memo and
launch plan. Only the principal's written override unblocks — the recorder logs it verbatim,
in quotes, dated, naming what was overridden.

## 3. Partial runs — "run just `<agents>` on `<X>`"

Valid consultation: the named agents only, same isolation rows, same caps and closing lines.
The recorder files a consultation note (`journal/YYYY-MM-DD-<CODE-or-topic>-consultation.md`).
No CMO decision unless all nine mandatory memos exist. Say so if the user asks for one.

## 4. Production run — "run production for `<CODE>`"

Load `references/production-protocol.md` now and follow its seven steps: preconditions (GO
on file, or a journal-noted fired trigger) → asset-brief check → drafts one asset at a time
under the producer's isolation row → asset gate (brand-risk, then compliance, written
independently — never show one officer the other's verdict) → revisions (max 2 rounds per
asset (Default – edit to taste.; budget-rules.md wins), then escalate) → filing +
recorder's production note → boundary: files only; the principal ships.

## 5. Monthly review — "run the monthly review"

Requires a snapshot dated within 30 days (Default – edit to taste.; budget-rules.md wins) —
otherwise halt for a re-dated one. Fill `templates/monthly-portfolio-review.md` with the
portfolio-architect and brand-risk-officer only, each under its own charter and isolation
row. File to `journal/YYYY-MM-DD-monthly-review.md`.

## 6. Quarterly audit — "run the quarterly audit"

The decision-recorder replays every journal entry in the window against actuals the
principal pastes (`campaigns/<CODE>/results.md` or inline): predicted number/date vs.
printed; NO-GOs and expired WAITs scored too; overrides tallied separately. Missing actuals
→ "no data pasted", scored unresolvable — never invent an actual. File to
`journal/YYYY-MM-DD-quarterly-audit.md`.

## 7. Halts

Halts are real and one line long: `HALT — <agent or check>: need <thing> (<where>)`.
Snapshot older than 30 days (Default – edit to taste.; budget-rules.md wins) → architect
halts. Missing compliance profile → compliance
officer halts. No personalized brand voice → producer halts. Unpersonalized repo → every
run halts (except the smoke test). Supply the thing, resume the run.

## 8. Completeness rule

No run of any kind — full, partial, NO-GO, expired WAIT, production, override — is complete
without the recorder's journal entry or note. If the user ends the run early, produce the
journal entry from what exists, marked `RUN INCOMPLETE`, gaps recorded as "not stated".

## 9. Boundary

This system writes files in `campaigns/` and `journal/`. It never sends, publishes,
schedules, or posts anything. The principal owns every decision and ships every asset.
