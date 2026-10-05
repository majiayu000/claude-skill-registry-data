---
name: remediation
description: |
  Discipline for repairing a false claim once it has propagated: select what
  depends on it, produce a replacement, and accept with an expiring verdict.
  Trigger when:
  - A claim, citation, premise, or documented fact is found wrong and its
    downstream consequences must be traced and fixed.
  - A refutation, a failed re-run, a retracted external source, or a human
    correction lands against something already closed or already promoted.
  - Prompt contains: /remediation, remediation, retraction, false claim,
    propagated error, scrub, correction propagation, born-false,
    became-false, currency verdict, impeachment queue.
---

# REMEDIATION — Repairing a Propagated False Claim

**Select → Produce → Accept**

## Why this exists

Detection is not correction, and correction is the expensive half. Two
measurements bound this discipline rather than motivate it hypothetically:

- Authors directly notified that work they had cited was retracted still
  mostly failed to correct it: of 86 authors successfully e-mailed, 51%
  replied, and at one year only **9 of 86** had published a formal
  correction (Avenell, Bolland, Gamble & Grey, *Accountability in Research*,
  DOI 10.1080/08989621.2022.2082290 — grounded in this record at
  `.ledger/log/2026-08-24-the-number-was-narrower.md` [AV2], which corrects
  an earlier rounded restatement; the raw counts are cited here rather than
  a derived percentage for the same reason that entry gives).
- In a 2026 multi-agent pipeline with none of the human explanations
  available — no fatigue, no incentive, no institutional friction — **87 of
  266** caught cases had the gate correctly suppress the injected error and
  the downstream agent still fail to propagate the correction
  (`.ledger/log/2026-08-24-avenell-in-silicon.md` [AS4]).

A discipline that stops at "flag it" reproduces both results. This one does
not stop there. It is a **named, loaded** discipline rather than
documentation because this project has independently and repeatedly
measured that a procedure carried only in memory is a procedure not
consulted — the same failure class the two citations above measure at
larger scale.

> **Verification Dual anchor.** REMEDIATION closes on both paths at once,
> per constraint. Where a deterministic evaluator exists — a re-runnable
> check, a query over the corpus, `git diff` against an anchor — it is used
> and named. Where none can exist — locating a hand-authored sentence
> outside the corpus, judging whether a scope actually covers a dependent
> set — the constraint says so explicitly and names the witness or human
> closer that discharges it instead ([rules.md §2](../../rules.md#2-prime-invariants)).

## Scope

REMEDIATION is not constraint-authoring (`/spec`) and not the general
category model for durable artifacts (`/record`) — it composes both. `/spec`
is loaded because every step below is normative (MUST/SHOULD) and carries
its evaluator, the same discipline `/spec`'s CONNECT step imposes on test
invariants. `/record` is loaded because the artifacts this procedure
produces — a tech-debt entry, a refutation entry, a decision record — are
themselves durable-record categories with their own homes and contracts.

Trigger condition: a claim previously treated as settled — closed
(`proved`/`cited`) or merely asserted in prose, code, or conditioning — is
now known to be false, and something else in the system was built on it.
If nothing was built on it, this is a one-entry correction and this
discipline is unnecessary ceremony (Focus-before-ceremony,
[ambient.md](../../ambient.md#the-focus-level-selector)) — SELECT still
runs, briefly, to confirm that.

## Ontology

- **Claim** — a proposition treated as backing something else. Two homes,
  with different repair economics (PRODUCE, below):
  - **corpus claim** — a `.ledger` entry with an `id`, reachable by
    derivation edges (`because`, `depends`).
  - **out-of-corpus claim** — a sentence in repository documentation, a
    code comment, a type name, a conditioning file, or an `AGENTS.md`
    requirement. No edge tracks what depends on it.
- **Dependent** — an artifact whose correctness rests, transitively, on a
  Claim.
- **Species** — whether a false claim was **born-false** (never true — the
  backing did not hold at its own anchor) or **became-false** (true when
  written, false because the record grew around it). Derived, never
  authored, mirroring the record's existing rule that openness is derived
  rather than stated (`docs/entries.md`, "the pen law").
- **Currency verdict** — a claim of the form "nothing under scope S has
  changed since commit A" — the only form "still clean" is ever entitled to
  take (ACCEPT, below).

## Machinery status — read before citing a command

Everything under **SELECT** below runs against `master` today.
`dependents_of` exists and is verified: an independent `jq` recursive
reverse-walk over the extracted corpus returned the same **44** dependents
of `write-path:W1` that the hand-written view returns
(`.ledger/log/2026-08-24-jq-suffices.md` [JQ1]).

Everything under **PRODUCE**'s born-false/became-false routing and
**ACCEPT**'s currency verdict depends on machinery that, as of this
writing, lives on branch `feat/refutation-and-currency` and is **not yet
merged to master** — verified directly: `ledger/gate/currency.py` and the
`refutes` field are absent from `master`'s tree
(`ledger/contracts/entry.ncl` on master carries no `refutes` field outside
a comment; `ledger/gate/currency.py` does not exist on master). The design
is not speculative — it is an architect ruling
(`.ledger/deposits/expiry-mechanics/architect-seat/2026-08-24-ruling-expiry-mechanics.md`)
plus a compiled model with no `sorryAx`
(`.ledger/log/2026-08-24-refutation-is-one-anchored-edge.md` [RF1]) — but a
walk following this skill **before that branch merges** cannot invoke the
corpus views for species and currency, and must apply the same rule by
hand, as each constraint below states.

## Act 1 — SELECT: which artifacts depend on the false claim

**SEL-1.** For a corpus claim, the walk MUST enumerate its dependent set
via `dependents_of`, never via `grep` — grep answers about text, the corpus
answers about extracted entries, and they disagree
(`.ledger/log/2026-08-24-the-record-was-queryable-all-along.md` [QA3]/[QA5]).
*Evaluator (proved, machine):*
```
python3 ledger/derive/extract_entries.py .ledger -o /tmp/corpus.json
nickel export /tmp/corpus.json --apply-contract ledger/contracts/entries_query.ncl \
  | jq '.dependents_of[] | select(.id=="<claim-id>").dependents'
```
Grounded by `ledger/gate/test_dependents_query.sh` (multi-hop, mixed edge
kinds, cycle, external exclusion, empty-leaf cases) and the independent
`jq` cross-check above.

**SEL-2.** For an out-of-corpus artifact, no edge exists to walk — this is
the hard case named up front, not papered over. The walk MUST establish the
universe before claiming coverage (`git ls-files` for the repository,
`git -C .ledger ls-files log/` for the corpus proper) and then search by
citation or content — a decorrelated searcher (semantic search, `grepai`,
or a fresh-context agent) looking for the claim's substance, its id, or its
distinguishing phrase. *Evaluator: none deterministic exists — closes
adversarially, by the searcher's report, which MUST state what it searched
and what it could not rule out (SEL-5 names the residual gap this leaves).*

**SEL-3.** SELECT's output MUST be a list of dependents with their
location (corpus id, or file:line), never a bare count — a count with no
enumerable members cannot be handed to PRODUCE. *Evaluator: structural
(agent-check)* — the deposit's dependent list carries a location per row
or is explicitly empty; a bare integer with no enumerable members fails a
zero-context read of the deposit (`/record`'s Gate 2 sensibility read).

**SEL-4.** A dependent classified `external` by `dependents_of` (support
that left the corpus) is NOT resolved by this discipline's machinery — its
provenance is outside the record's reach by construction. It MUST be
listed as a residual, not silently dropped. *Evaluator: structural* — the
count of rows in the residual list tagged `external` matches
`dependents_of`'s own external-tagged member count for the same claim; a
mismatch is a dropped dependent.

**SEL-5.** Semantic re-derivation — the false claim re-expressed in words
sharing no substring with the original — is not solved by SEL-2 or
anything else in this skill. Say so at report time rather than implying
SELECT was exhaustive; see Honest Limits. *Evaluator: presence* — the
final report's Honest Limits section states this gap explicitly; an
evaluator can confirm the sentence is present, never that SELECT actually
found every semantically-equivalent restatement — that half closes by
nothing this skill supplies.

## Act 2 — PRODUCE: a replacement free of the false claim

**PRO-1.** Each dependent MUST be classified **composed** (regenerated by
fixing its source — a Nickel view, a generated YAML, a `chain_floor`-style
derived read) or **hand-authored** (prose, a decision, a manually written
comment) before it is touched. This classification is what determines the
cost of the whole exercise, per
`.ledger/log/2026-08-24-remediation-factors.md` [RM3]: composed artifacts
are free to re-derive; hand-authored ones must be found and edited one at a
time, and SELECT already found them. *Evaluator: structural, partial* — an
edge from the dependent to a named generator/tool (a `because` ref — the
`derives-from::` prose token — or a build-script relationship) is evidence
for composed; its absence is evidence for hand-authored, never proof — a
hand-authored artifact that happens to cite a tool is still hand-authored,
so a wrong classification on that basis is a reviewable, not a
machine-caught, error.

**PRO-2 — composed dependent.** MUST fix the source and regenerate; MUST
NOT hand-edit the generated artifact directly — that edit is overwritten
(or silently diverges from) the next regeneration, which is drift
reintroducing itself. *Evaluator: diff between the freshly regenerated
artifact and the previously hand-patched one is empty.*

**PRO-3 — hand-authored dependent.** MUST be located (SELECT already did
this) and edited directly; there is no source to regenerate from.
*Evaluator: none deterministic beyond the edit itself — closes by the
editing walk's own commit, reviewed at the same bar any code-edit floor
review applies ([ambient.md §Code-Edit Constraints](../../ambient.md#code-edit-constraints)).*

**Species routing.** Determine species before choosing a repair path for
the false claim's OWN entry (not its dependents — those are PRO-1/2/3
regardless of species). Given a refuting claim `R` anchored at `r_anchor`
targeting claim `C`:

| condition on `C` | species | why |
| :--- | :--- | :--- |
| `C` carries no `check`/`witness` anchor | `unclassifiable-refutation` | no anchor to compare against — never guessed |
| `C.axes.monotone == true` | `born-false`, always | a monotone claim once true stays true; a later refutation convicts `C`'s own birth anchor mechanically, no comparison needed |
| `r_anchor == C`'s anchor | `born-false` | same record state; nothing grew between them |
| `r_anchor` extends `C`'s anchor (ancestor) | `became-false` | true when written, falsified by growth |

*Evaluator (once `feat/refutation-and-currency` merges, proved/machine):*
the `refutations` view in `entries_query.ncl` derives this per row, never
authored as a label (`.ledger/log/2026-08-24-refutation-is-one-anchored-edge.md`
RF3/RF4). *Until then:* apply the table by hand; verify the ancestor
relationship with `git merge-base --is-ancestor <r_anchor> HEAD` rather than
assuming it.

**PRO-4 — became-false.** MUST either re-establish the claim or let it
lapse; MUST NOT silently leave it marked current. Re-establishment is
species-of-backing-dependent, not "re-run the same check" unconditionally
(architect ruling [R5]): a **corroborated** claim is re-established by
re-running the named check and re-anchoring — the command quantifies over
its scope by construction. A **vouched** claim is re-established by the
witness re-vouching; a re-vouch MAY narrow to the delta
(`git diff --name-only <at> HEAD -- <scope>`) but the chain of narrowed
re-vouches MUST floor on a full-scope re-vouch periodically, or it drifts
arbitrarily far from any full read — the same defect `chain_floor` exists
to expose, at the currency grain. *Evaluator:* the re-run's exit code
(corroborated) or the witness's new `Witness{name, at}` entry (vouched —
closes by witness, not machine).

**PRO-5 — born-false, target OPEN (`unclosed`/`synthesis`).** No closure
was ever claimed, so there is no collision to adjudicate. MUST repair by
content: author a corrected entry; the original may be superseded
(`supersedes`, which "types nothing — any entry may be retired unanswered
by a survivor," `ledger/contracts/entry.ncl:747`). *Evaluator: machine for
the edge, agent-check for the content* — a dangling or cyclic `supersedes`
is refused by `EntryStore` (`SupersessionTerminates`, `entry.ncl:926`); the
corrected content itself closes the same way any new claim does, by its
own backing.

**PRO-6 — born-false, target CLOSED (`proved`/`cited`).** MUST NOT repair
by content alone. A snapshot-sound closure and a true refutation at the
same anchor are jointly impossible (the `impeachment` theorem,
`.ledger/log/2026-08-24-refutation-is-one-anchored-edge.md` RF3) — the
model proves the pair contradictory and **cannot itself say which party
lied**. The walk MUST:
1. Author the anchored `refutes` edge (this is what makes the collision
   derivable at all — an unanchored "C is false" is itself the model's
   canonical non-monotone expiring claim, refused by `RefutesAnchored`).
2. MUST NOT auto-resolve the collision. Route it to a human closer — never
   an agent's own reading of which side is right (RF4: "routed to a human
   closer, never auto-resolved by this view or any other").
3. The human's ruling is recorded as a **new** entry, since the ledger is
   append-only (`docs/entries.md`: "a deposit is amended by a new entry").
   If the ruling finds the original evidence event unsound, that new entry
   MUST `supersede` the original — this IS the grade withdrawal an
   append-only record can perform: not an in-place edit of the old grade,
   a superseding record that retires it.
*Evaluator (once merged):* `impeachment_queue` — every `refutations` row
whose target is `corroborated`/`vouched` and species `born-false`.
*Until merged:* apply the routing-table test by hand and halt for the same
human closer; do not proceed past step 2 without one.

## Act 3 — ACCEPT: nothing dependent remains unrepaired

**This can never be permanently true.** A new dependent can always appear
after SELECT ran, so "everything is clean" is a claim with an expiry, never
a standing fact — this is a theorem
(`.ledger/log/2026-08-24-remediation-factors.md` [RM4],
`current_state_does_not_bank`), not a limitation of this discipline's
diligence. ACCEPT's output MUST be phrased as a currency verdict, never as
an unqualified "done."

**ACC-1.** A currency verdict is current iff nothing under its declared
scope (a git pathspec) has changed since its anchor commit.
*Evaluator (once merged, proved/machine):* `ledger/gate/currency.py
--anchor <at> --scope <pathspec> --repo .` — exit 0 current, 1 lapsed
(changed paths named), 2 anchor-not-an-ancestor (orphaned, not lapsed), 3
environment error. *Until merged*, the underlying evaluator is the same
command the wrapper runs: `git diff --quiet <at> HEAD -- <pathspec>`.

**ACC-2 — scope MUST cover the dependent set.** The scope is a git
pathspec and MUST cover the home files of `dependents_of(C)` as computed at
the anchor (architect ruling [R4]) — the anchor and the coverage are both
obligations, neither is optional. A pathspec over-approximates the
dependent set by design (an irrelevant change costing one extra re-run is
the cheap failure direction; a real dependent outside the scope producing a
false "current" is the expensive one). **This is unclosed today, and it is
tracked, not papered over**: no evaluator in this system decides whether a
given scope actually covers a claim's real dependent set — every theorem
behind the currency machinery holds just as well for a deliberately narrow
scope as for a correct one
(`.ledger/tech-debt/currency-scope-adequacy-unclosed.yaml`). The scope is
authored by the party who benefits from it being narrow, so it does not
close on its own author's word — a currency verdict's scope MUST be
confirmed by a second, decorrelated party against the actual
`dependents_of` output before the verdict is treated as current, until the
tracked coverage check lands. *Evaluator: none machine-checkable exists
today (the tracked gap itself) — closes adversarially, by a decorrelated
reviewer's confirmation that the pathspec's glob set is a superset of
`dependents_of(C)`'s reported locations.*

**ACC-3.** On lapse, the walk MUST NOT re-assert currency silently.
Re-establishment follows PRO-4's species-of-backing split exactly (a scrub
verdict is itself a non-monotone claim, and the currency machinery is that
claim's cure applied — `.ledger/log/2026-08-24-where-the-findings-land.md`
[WL3]). *Evaluator: PRO-4's, inherited* — the re-run's exit code
(corroborated) or a new `Witness{name, at}` entry (vouched); this
constraint adds no evaluator of its own, only the obligation to invoke
PRO-4's rather than skip it.

**ACC-4 — block attaches to USE, not to existence.** A commit that changes
a live verdict's scope MUST NOT itself be blocked — lapsing is normal
operation. What MUST block: a promotion into repository documentation or
agent conditioning whose support chain bottoms out at a lapsed verdict, and
a gate CLOSE whose satisfying claim rests on one. A corpus-wide lapse sweep
gating every commit is explicitly REJECTED (over-blocking degrades a
blocking gate into a reporting one — the same failure mode OCSP soft-fail
demonstrated at internet scale, cited in the architect ruling [EX6]/[R6]).
*Evaluator:* today, `terminal_freshness.py` checks only that a cure is
*declared*, by its own stated limit — not that it is current. Extending it
to check currency is the natural next step this discipline does not itself
build; name it as a dependency if this discipline is invoked before that
extension lands.

## Routing summary

```
false claim found
  │
  ▼
SELECT
  ├─ in corpus ─────────▶ dependents_of(C)                    [SEL-1, machine]
  └─ out of corpus ─────▶ search by citation/content           [SEL-2, adversarial]
  │
  ▼
list of dependents with locations, external rows kept as residual  [SEL-3, SEL-4]
  │
  ▼
PRODUCE ── each dependent: composed? ──yes──▶ fix source, regenerate [PRO-2]
  │                            │
  no                           no
  │                            ▼
  ▼                     hand-edit directly [PRO-3]
determine C's species (table above)
  │
  ├─ became-false ──────────▶ re-establish or let lapse [PRO-4]
  ├─ born-false, C open ────▶ repair by content, may supersede [PRO-5]
  ├─ born-false, C closed ──▶ HALT: refutes edge → human closer →
  │                            superseding entry withdraws the grade [PRO-6]
  └─ unclassifiable ────────▶ HALT: no anchor to compare, do not guess
  │
  ▼
ACCEPT: currency verdict {scope, at}, scope covers dependents_of(C),
        confirmed by a second party [ACC-1..4] — expires by construction
```

## MANDATORY HALT points

1. **Unclassifiable refutation** (`C` has no anchor). Do not guess a
   species from missing evidence; the target may need re-anchoring before
   this discipline can proceed at all.
2. **Born-false on a closed claim.** Never auto-resolve the impeachment
   collision. Route to a human closer and wait.
3. **A dependent found `external`.** Its provenance left the corpus by
   construction — surface it as a residual, do not attempt to repair what
   the record cannot reach.
4. **A scope the author cannot show covers `dependents_of(C)`.** ACC-2's
   coverage confirmation is not optional ceremony; an unconfirmed scope is
   an unverified currency verdict wearing a verified one's clothes.

## Honest limits

- **The measured ceiling for correction propagation across every studied
  field is 5–20%, and it has been flat for decades.** State this plainly
  when reporting a remediation's outcome. It is a **worst-cell** reading —
  no trace, no check, no generator, no pen, unexpiring verdicts, every axis
  at its worst simultaneously (`.ledger/log/2026-08-24-remediation-factors.md`
  [RM5]) — not a bound on what this discipline's cure class can achieve,
  but also not something this discipline has demonstrated beating. Do not
  claim victory over the literature's number from having followed this
  procedure once.
- **Scope adequacy is unsolved**, tracked in
  `.ledger/tech-debt/currency-scope-adequacy-unclosed.yaml`. Every
  guarantee ACCEPT states holds exactly as well for a mis-scoped verdict as
  for a correct one. ACC-2's decorrelated-confirmation requirement is a
  stopgap on top of that tech-debt entry's own discharge condition, not a
  substitute for it.
- **Semantic re-derivation is not solved by anything here.** SEL-2's
  citation/content search finds a claim restated in recognizable language;
  a claim re-expressed in words sharing no substring with the original can
  pass through undetected. This is named, not hidden, per SEL-5.
- **Born-false/became-false routing and currency verdicts depend on
  unmerged machinery** (`feat/refutation-and-currency`). Every constraint
  above states its fallback; the fallback is a human/manual application of
  the same rule, not a weaker rule.

## Prime Directives

1. **SELECT_BEFORE_PRODUCE.** Never edit a dependent found by intuition
   alone when `dependents_of` can enumerate it. Grep is for text; the
   corpus answers about entries, and the two disagree.
2. **CLASSIFY_BEFORE_EDIT.** A dependent is composed or hand-authored
   before it is touched, not discovered to be one after the fact.
3. **SPECIES_BEFORE_REPAIR.** Born-false and became-false take different
   repairs; applying became-false's "re-establish or lapse" to a born-false
   claim, or born-false's impeachment routing to a became-false one, is a
   protocol violation, not a shortcut.
4. **NEVER_AUTO_WITHDRAW_A_CLOSED_GRADE.** An agent walk MUST NOT decide,
   on its own reading, that a closed claim's grade is wrong and act on that
   decision without a human closer. The model proves the collision
   contradictory; it does not name which party lied, and neither does this
   discipline.
5. **ACCEPT_EXPIRES.** "Clean" is never asserted without a scope and an
   anchor. An unqualified "remediation complete" is a protocol violation of
   the same shape RM4 names as a theorem, not a judgment call this
   discipline defers to the walk.

### Protocol Violations (FORBIDDEN)

| Violation | Why It's Wrong |
| :--- | :--- |
| Editing a hand-authored dependent found only by memory, skipping `dependents_of` | Grep-shaped recall disagrees with the corpus; the two answer different questions |
| Hand-patching a composed (generated) dependent | The next regeneration overwrites or silently diverges from the patch |
| Auto-resolving a born-false-on-closed collision | The model proves it contradictory and undecidable from inside; only a human closer breaks the tie |
| Repairing content on a closed claim without the `refutes` edge | An unanchored "C is false" is itself the model's own non-monotone expiring claim, not a verdict |
| Reporting "clean" with no scope or anchor | Accept is a theorem-bounded expiry, never a standing fact |
| A currency verdict whose scope was never confirmed against `dependents_of` | The scope's author benefits from narrowness; it does not close on that author's word alone |

## Position in the workflow chain

```
false claim found → REMEDIATION (Select → Produce → Accept)
                          │              │            │
                          ▼              ▼            ▼
                    /record's       /spec's        /record's
                  tech-debt/         VERIFIED      tech-debt for
                  category for     tagging for      the scope-
                  the residual      each repair      adequacy gap,
                  and unclassed     constraint's     currency
                  gaps this pass    own evaluator    verdict entries
                  surfaces
```

REMEDIATION is invoked wherever a walk of any kind discovers a claim it
relied on is false — not only from within `/spec`. A council seat finding a
born-false claim in a deposit under review, a `/core` worker whose test
invariant was derived from a since-refuted premise, and a `/campaign`
reconcile finding a worker's IBC rested on stale premises all load this
same discipline rather than improvising a one-off fix.
