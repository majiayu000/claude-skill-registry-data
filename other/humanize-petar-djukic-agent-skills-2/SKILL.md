---
name: humanize
description: >-
  The laundering chain: one generative pass that moves AI-drafted prose
  toward human-passing on Pangram. Stages in order — filter-tells
  (semantic cleanup), seeded match-voice (anchored Cohere seed, iterate
  only while the score falls), optional burstiness, tighten-style (word
  recovery), optional accent-dial, inject-vernacular (terminal). Pure
  function: structurally diverged draft in, laundered draft plus report
  out; the caller owns structure (match-outline), review (reverse-outline,
  critic-panel, voice-critic, cold review), and the decision to cycle.
  Venue mode (--venue <name>) resolves stage parameters from a
  writing-voice/venues/ profile. Locked spans respected by every stage;
  after the terminal stage models read but never write. Triggers:
  humanize, humanize article, make it human, full rewrite pipeline,
  rewrite for pangram, humanize for venue, laundering chain.
---

# Humanize (the laundering chain)

One generative pass over a draft: semantic cleanup, a seeded diction
rewrite, word recovery, optional accent, then the deterministic terminal
stage. The chain is a **pure function** — structurally diverged draft in,
laundered draft plus a measurement report out. It runs once per
invocation. Structure, review, author edits, and the decision to run the
chain again belong to the caller (GH-208): a workflow command invokes
match-outline before this chain when the form needs changing, runs the
read-only instruments after it, and reads this chain's seed-reach report
to decide whether another cycle would pay.

The verified effect on a fresh AI draft (2026-07-29, working gate) is
100% AI -> Mixed: 23.8% AI / 76.2% AI-assisted, mean window 0.993 ->
0.576. On well-edited prose the gain is real but small — see the
calibration data at the end.

## The chain

| stage | what it does | what happens without it |
|---|---|---|
| filter-tells semantic cleanup | collapse antithesis pairs, remove CoT leakage, cut recap ballast, fix banned words | Pangram score stays at 100% AI even after match-voice, because the rhetorical patterns survive diction changes |
| seeded match-voice | one anchored Cohere seed pass, then iterate --no-anchors only while the score falls (GH-194) | unseeded, the rewriter substitutes its own diction instead of stripping the old fingerprint: measured 0.609 gated, against 0.370 seeded, on the same article |
| burstiness (optional) | raises sentence-length variance through the rewrite transport, behind the same gate | CV stays put; on a plain stylometric model dispersion is one of the two discriminative features |
| tighten-style | gives back the words the rewrite costs, through the second model family, without giving back the score | the draft reads leisurely (2,378 -> 2,502 words on the worktrees run) |
| accent-dial (optional) | dials a gated, ranked fraction of EN->SR->EN round-trip edits into structurally clean text | the strongest single Pangram move recorded on strategy-theatre (0.708 -> 0.150) is left on the table |
| inject-vernacular (terminal) | deterministic idiolect operators restore the author's markers; nothing samples | the author's signature constructions stay at machine rates |

## Input contract: structurally diverged prose

The chain does not restructure. **match-voice gate-rejects everything
(distance 0.0) when the input's sentence structure is still the drafting
model's** — the ablation rows in the calibration data (unverified, but
consistent with every measured run). Divergence is the caller's job,
before the chain runs:

- **match-outline** is the structural tool — section-level rewriting
  against a blueprint. It is a document rewriter, not a prose stage, and
  it carries its own risk class: verify content preservation after it,
  including figure blocks (a 2026-08-31 run dropped an entire figure
  while reporting "all citations and numbers preserved" — see
  match-outline's SKILL.md).
- A venue profile's `structural_step` field is **consumed by the
  caller**, not by this chain: it names the structural tool the caller
  should run (or `skip`) before invoking humanize.
- Well-edited human prose is acceptable input without a structural pass —
  expect low seed reach and a small gated gain (strategy-theatre: 19 of
  125 paragraphs changed, and that was enough).

A run on undiverged input is not an error; it reports itself through the
gate stats (kept-original dominating, distance near 0.0) and the caller
reads that as "run the structural step first."

## What the caller owns

The chain reports; the caller decides. After the terminal stage, the
caller's review phase runs the read-only instruments — reverse-outline
(annotate + rank), critic-panel and its rule-based application
(critic-apply, GH-206), cold review (GH-207), voice-critic — and the
author picks and edits. None of that is this skill's procedure. Critic
picks and author edits are new prose that has never been laundered, so a
caller that applies them re-enters the chain in a new cycle; re-entering
is the 're-running from a pre-terminal checkpoint' the terminal contract
allows.

**Seed reach is the cycle signal, and this chain must report it**: the
count of paragraphs the seed pass changed, out of total. Measured
indicators from the strategy-theatre runs, for the caller's decision:

| indicator | chain worked | chain failed |
|---|---|---|
| seed reach (paragraphs changed) | 19 of 125 | 16 of 125, 36 gate-rejected |
| gated survival at cold review | 51% mid-edit, 35% well-edited | 39% and scoring worse |

When the seed cannot move the text, the article has converged and further
chain runs only shuffle between detector buckets.

## The terminal invariant (GH-57)

`inject-vernacular` is terminal **for its cycle**. Within a cycle nothing
writes after it. **After the terminal stage, models may read but never
write.** The evidence is the Strategy Theatre provenance logs: every
generative pass regresses text toward the model's distribution center —
match-voice injected bold lead-ins despite instructions, tighten-style
invented a sentence, and a rerun rewrote hand-cleaned prose 8/8 times
until the entailment gate rejected all of it. A defect found after the
terminal stage is fixed by the author's hand, or by re-running from a
pre-terminal checkpoint — never by an additional model repair on the
final text.

Three rules the order encodes:

1. **Locks travel the whole chain.** Spans marked `<!-- lock -->` …
   `<!-- /lock -->` at drafting are excised by the shared drivers before
   any model call and spliced back byte-identical after, in every stage —
   protection is mechanical, enforced in `prose_document.py` /
   `md_paragraphs.py`, never by prompts.
2. **inject-vernacular is terminal because it is deterministic.** It
   applies the idiolect.yaml operator bank by substitution and
   restoration only; nothing samples, so it cannot regress the text
   toward a model's center — which qualifies it to run after every stage
   that can.
3. **Snark and disproportion are born at drafting and locked.** No stage
   in this chain inserts them: mechanical joke insertion is prohibited by
   design. voice-critic audits them in the caller's review phase (L0–L5
   scale, receipt-first, density caps) and flags to the author gate; it
   never edits.

## Why anchors on the seed and none on the iterator

The GH-194 measurement (see Model pins below) made the anchored Cohere
seed the mechanism: the anchored pass does the work, and iteration adds
little. The `--no-anchors` iterator remains for payloads that keep
falling: anchors constrain an iterator into register patterns Pangram
catches, so the iterator runs free while the seed carries the register.

## Prerequisites

- A Cohere key (`COHERE_API_KEY`, `COHERE_SECRETS_FILE`, or `cohere` in `.secrets/`) — every stage's
  *default* model is `cohere:command-a-03-2025` since GH-176–190, except
  accent-dial (deliberate `gemma4:31b-cloud`, see Phase 4)
- Ollama endpoint reachable — required by the keyless fallbacks and the
  recorded July recipe
- A `writing-voice/` directory with exemplars
- For Pangram measurement: an API key configured per the match-voice
  credential contract (`.secrets/keys.json` with `"pangram"` entry)

### Model pins vs stage defaults (GH-193, re-pinned GH-194)

Stage defaults are Cohere; the recorded July recipe pinned other models,
and those pins are the experiment — do not "fix" a pinned command to the
default. Whether Cohere arms beat the pins was GH-194 (2026-08-31, two
published payloads, seed+iterator isolated on raw articles, prose-only
Pangram):

(Dated 2026-08-31; superseded by the 2026-09-01 detector-model switch — see
the Calibration data note. The authorship findings stand; the numbers do not.
The arm ranking itself is a `default`-model result. It has not been re-run on
`pangram-4` (GH-406). Both payloads are published newsletter articles, and
the newsletter venue never uploads, so the re-run needs the operator to
override that rule for the experiment. Until then, treat "the seed is
usually the result" and the stop-at-first-upturn expectations below as
measured on the old model.)

| arm (seed -> iterator) | loop (base 1.000) | prompts (base 0.913) | mean |
|---|--:|--:|--:|
| pinned: gemma-anchored -> gpt-oss | 1.000 (never moved) | 0.734 (3 passes) | 0.867 |
| cohere-anchored -> gpt-oss | 0.896 | 0.913 | 0.904 |
| gemma-anchored -> cohere | 1.000 | 0.909 | 0.955 |
| **cohere -> cohere** | **0.802** | **0.735** | **0.768** |

**The recommended strategy is a single Krugman-anchored Cohere seed
pass** (`--model cohere:command-a-03-2025 --author Krugman`), with
further no-anchor passes only if the score still falls: it tied the
pinned recipe's 3-pass endpoint on one payload in ONE pass, was the only
arm to move the other payload at all, and needs no Ollama. The pinned
recipe is iterator-driven, the Cohere strategy seed-driven. The
multi-family "foreign fingerprint" thesis did not replicate: both mixed
arms were worse than either pure arm, and **a gpt-oss pass after a Cohere
seed actively destroys the seed's gain (0.896 -> 0.996) — never mix them
in that order.**

Limits: n=2 payloads, arms isolated on raw articles, stop-on-upturn
sampled once per pass.

## Contract-field protection (GH-362)

YAML spec files carry contract fields (section_goal, goals, acceptance
criteria, metadata) whose values are terse, lowercase phrases the repo's
audit tools grep for. The chain protects them in two layers:

**Exclude keys.** Both tighten.py and drive.py accept `--exclude-keys` with
dot-separated key-path globs. For YAML files, the default exclusion list is
`section_goal`, `goals.*.goal`, `acceptance.*`, `meta.*`, `metrics.*`
(GH-227: a rewrite pass once replaced a `metrics.*.computed` value with
a pasted model refusal that shipped unnoticed). These paragraphs
get status `excluded-key` and never reach the rewriter. Pass `--exclude-keys`
with no arguments to disable the default.

**Guard phrases.** verify.py accepts `--must-preserve` with exact phrases
that must survive rewriting unchanged. A candidate that loses a guard phrase
is rejected (fatal finding) and the original text is kept. Use this for
claims-integrity markers like "recorded as planned", "no number is cited",
"submission-status care" that the repo's claims audit greps for.

**ASCII normalization.** verify.py normalizes typographic unicode (curly
quotes, non-breaking hyphens and spaces, en-dashes) to ASCII before running
any check. A rewrite that reintroduces them is caught by the gate rather
than silently passing.

When running the chain on spec YAML, the exclude-keys defaults apply
automatically. For guard phrases, pass them explicitly on the drive.py or
tighten.py command line, or configure them in the venue profile.

**A caller-supplied protected-terms file (GH-481).** When the caller
hands the chain a protected-terms file (polish-prose extracts one from
the piece's focus brief: posture verbs, definition terms of art, pinned
spellings and ids), every stage's transport runs with it — match-voice
`--protected-terms`, and its terms passed as guard phrases where a stage
takes only `--must-preserve` — and the chain derives no list of its own
beside it. The file is the piece's exact vocabulary; a swap the gate
would read as a synonym ("checked" → "verified") is the GH-477 damage
class this exists to stop.

## Procedure

### Phase 0: Discover, resolve the venue, measure the baseline

1. Discover `writing-voice/` by walking up from the article path.
   Error if not found.

2. **Venue mode (GH-336).** If the user named a venue (`--venue <name>`,
   or "humanize this for the book/newsletter/..."), resolve the profile:

   ```bash
   $RUN <match-structure>/scripts/venue_profile.py show \
     --venue <name> --for <article.md>
   ```

   A profile that fails validation is refused — report the errors and stop;
   never fall back to guessing. From the resolved profile:

   | profile field | governs |
   |---|---|
   | `structural_step` | **the caller's pre-chain step, not this chain** — report it so the caller can confirm it ran (or was skipped) |
   | `anchor_query` | the seed's anchor selection (Phase 2) |
   | `targets`, `hedge_policy` | tighten-style's floor: pass `--venue <name>` to tighten.py in Phase 3 |
   | `tell_lexicon` | the lexical catalog: pass `--lexicon=<value>` in Phase 1 |
   | `gates` | which measurements run: no `pangram` gate → skip every Pangram scan in every phase, standing grant or not (when the gate IS present, uploads run under the consent rule — per document, or the operator's standing grant, GH-210) |
   | `citations` | which citation markers to spot-check after each stage (`[1]` numbered vs pandoc `[@citekey]` — both must survive every rewrite verbatim) |

   List venues with `venue_profile.py list --for <article.md>` when the
   user asks what is available. No venue named, or no `venues/` directory
   → ask for the anchor selection interactively; everything else takes
   its default.

3. Capture baseline measurements:

   ```bash
   # Pangram baseline (one-shot scan; uploads the prose, costs a scan)
   $RUN <agent-dir>/scripts/pangram_report.py scan --article <article.md>

   # Style baseline
   $RUN <match-structure>/scripts/style.py profile <article.md>

   # Burstiness baseline (one line; the full numbers are in the profile)
   $RUN <match-structure>/scripts/style.py burstiness <article.md> --text
   ```

   Record the baseline Pangram scores (human %, mean window score,
   verdict), the full `text_metrics()` output, and the burstiness line.
   These are the "baseline" column in the final report. **Print the CV
   next to the Pangram score at every measurement point below, not only
   in the final table** — sentence-length dispersion and AI-phrase
   density are the two features a plain stylometric model uses, and a
   step that moves the score without moving CV moved something else
   (GH-129: a diction-only control arm held CV at 0.621 and Pangram at
   0.436, while the same model reshaping rhythm took CV to 0.690 and
   Pangram to 0.259). In venue mode, capture the Pangram baseline only
   when the profile's gates include `pangram`. Under a standing consent
   grant (GH-210) the drivers score every stage by default — which is what
   the stop-at-the-upturn rule needs — and `--no-pangram` opts a run out.
   **Hold the Pangram
   framing constant across every measurement in a run** — slice, whole,
   and prose-only payload scores of the same article are not comparable
   (measured spread on one article: 0.225 / 0.913 / 1.000).

### Phase 1: filter-tells semantic cleanup

Run the lexical and structural scans on the input. Block-locked regions
never enter the scans' prose view, and semantic edits are applied through
the lock-respecting drivers — a locked antithesis or authored snark span
is not filter-tells' to collapse. With `writing-voice/idiolect.yaml`
discoverable, the structural scan calibrates to the author baseline:
native constructions flag only above the author ceiling, and calibrated
flags say reduce toward the target, not to zero.

```bash
bash <filter-tells>/scripts/detect-lexical.sh <article.md>
$RUN <filter-tells>/scripts/detect-structural.py <article.md>
```

In venue mode pass `--lexicon=<tell_lexicon>` to detect-lexical.sh — the
newsletter banned-word list must not drive edits on an academic methods
section, and the academic lexicon adds paper-template tells the default
list does not carry.

Apply the semantic edits following the filter-tells Step 3 procedure. The
edits that matter most for this chain:

1. **Antithesis pairs** — collapse every negation-flip pair into a single
   sentence. These are the dominant AI rhetorical pattern. Target: 0 pairs.
2. **CoT leakage** — delete bridge sentences that add no information.
   Apply the removal test: delete the sentence, re-read the paragraph.
   If nothing is lost, it was scaffolding.
3. **Recap ballast** — compress paragraphs that restate earlier points
   without adding new information.
4. **Banned words** — swap any remaining banned words (check the lexical
   scan output).
5. **Author-stance narration** — sentences written from the author's chair:
   scope negotiation ("here we deal with", "this article covers"), and system
   facts stated as author experience ("waiting for my approval"). Rewrite as
   claims about the system ("a human approves it before it exists"). The
   bridge sentence and the learning-objectives paragraph are the sanctioned
   exceptions; everything else in this register goes.

After editing, re-run both scans to confirm:
- Structural verdict: MINOR-ISSUES or better (was LIKELY-AI)
- Antithesis pairs: 0
- No banned words

Measure after filter-tells (Pangram + profile + burstiness against the
baseline). Record as the "after-tells" column, Pangram and CV together.

### Phase 2: seeded match-voice

**Run the seed. It is the mechanism, not an enhancement.** A single
unseeded match-voice pass has only its own distribution to push against,
so it substitutes diction instead of stripping it.

#### 2.1 Seed — Cohere, anchored (the GH-194 default)

```bash
$RUN <match-voice>/scripts/drive.py \
  --article <cleaned.md> \
  --model cohere:command-a-03-2025 \
  --author <the author whose register fits> \
  --voice-dir <repo>/writing-voice \
  --pangram \
  --out <seed.md>
```

`--author` works by filename inference where the manifest carries no author
field — the anchor pool line reports `(inferred from filenames)` — so the
old anchor-by-tags-only guidance (GH-98 era) is superseded; tags remain the
tool when no single author fits. Verify the pool either way:

```bash
$RUN <match-structure>/scripts/voice_anchors.py tags --voice-dir <repo>/writing-voice
```

**With a Cohere seed, the seed is usually the result** (GH-194: every
Cohere arm's floor was the seed itself). Measure it; that score is the
baseline for 2.2. **Record seed reach** — paragraphs changed out of
total, from the driver's accepted/kept table — it is the caller's cycle
signal and a required line in the report.

**A flat or slightly worse seed score does not discard the seed when its
reach is healthy (GH-224).** The seed's contribution is divergence that
Phase 3 exploits, and its own Pangram reading measures that poorly.
Measured on the-qwerty-endpoint, same payload, one day apart:

| run | seed (reach) | after tighten | final |
|---|---|---|---|
| 2026-09-01 | 0.930 (11/19) | **0.548** | **0.542** |
| 2026-09-02 | 0.991 — flat-to-worse (9/19), seed discarded on score | 0.697 | 0.673 |

Discarding the flat seed cost 0.13 mean window at the end of the chain.
So: a seed with healthy reach (the measured healthy runs sat near 9–11
of 19) **stays in the lineage** through Phase 3, and the floor decision
compares post-tighten measurements when both lineages were run — or
simply accepts the seeded composition when only one was. A seed with
collapsed reach (the converged-article signal, strategy-theatre's 16/125
with mass gate rejection) is still set aside on its score.

#### 2.2 Iterate — only while the score still falls

```bash
PREV=<seed.md>
for i in 01 02 03 04; do
  $RUN <match-voice>/scripts/drive.py --article $PREV \
    --model cohere:command-a-03-2025 --no-anchors --pangram \
    --canonical-blocks <repo>/writing-voice/canonical-blocks.txt \
    --out pass$i.md
  PREV=pass$i.md   # read the score; STOP at the first upturn
done
```

Expect this loop to stop at pass 1 — iteration earned nothing in any
GH-194 Cohere arm. It stays in the recipe because stop-on-upturn makes a
zero-gain loop cost exactly one pass, and a payload that does respond gets
its passes.

Three rules, all load-bearing:

1. **Score every pass and stop at the first upturn.** Never run a fixed
   count. Past the floor each pass concentrates the iterator's own
   signature and the score climbs back (the U-curve: 0.992 -> 0.579 ->
   0.432 -> 0.489 -> … -> 0.700 by pass 10, stay-on-track 2026-07-29).
2. **The publish candidate is the floor pass, not the last pass** — with
   the GH-224 amendment above: between the seed and its input, the floor
   is judged after Phase 3, not on the seed's own reading. Keep every
   pass on disk with its provenance.
3. **The floor pass's score is raw until the caller's cold review gates
   it.** Every stage measured this way lost most of its gain at review —
   the raw floor and the gated floor are different numbers, and only the
   gated one counts. Cold review belongs to the caller's review phase
   (GH-207).

**Pass `--canonical-blocks` explicitly** when the article is staged
anywhere but its repo: discovery walks up from the article path, so a run
staged in a scratch directory silently has no registry and will rewrite
the disclosure and subscribe lines.

**Recorded July configuration (alternative).** The pre-GH-194 pinned
recipe — anchored `gemma4:31b-cloud` seed, then a `gpt-oss:120b-cloud`
no-anchors iterator — is the arm the calibration tables below measured
through July. It is iterator-driven where the Cohere strategy is
seed-driven, lost the GH-194 head-to-head (mean 0.867 vs 0.768), and a
gpt-oss pass after a Cohere seed actively undoes the seed (0.896 ->
0.996) — never mix them in that order. Reach for it when an
iterator-grind on an already-clean draft is specifically wanted;
substitute the model names into the commands above. Pangram ships new
detector versions over time, so re-measure before reusing any recipe.

#### 2.3 Ablation: the unseeded single pass

Retained as a named ablation; choosing it is a deviation a run has to
state and justify (measured 0.609 gated against 0.370 seeded on the same
article). Inline locks reach the rewriter as opaque `[[LOCK-n]]` anchor
tokens; a rewrite that drops one is refused by the drivers and the
original paragraph is kept.

```bash
$RUN <match-voice>/scripts/drive.py \
  --article <cleaned.md> \
  --model cohere:command-a-03-2025 \
  --no-anchors \
  --pangram \
  --out <output.md>
```

In venue mode, include `--pangram` only when the profile's gates carry
`pangram`; a venue without that gate (academic) is never uploaded to the
external detector.

Check the output for:
- `accepted-mechanical` count (should be most paragraphs, not `kept-original`)
- Distance > 0 (confirms the gate accepted rewrites)
- Pangram verdict and mean window score (when the gate ran)

#### 2.4 Burstiness (optional, same slot)

**The burstiness pass** (GH-129) runs in the match-voice slot:
match-voice's `burstiness.py` raises sentence-length variance through the
rewrite transport, behind the same gate. It earns its position the same
way the seed does — measured only on documents already through the chain.
On pipeline-state prose it moved Pangram 38.1% -> 29.1% (and, at an
earlier state of the same article, 0.445 -> 0.259) with a rhythm-held
control within noise both times; run on a raw draft it can do nothing (a
saturated 100% baseline has no room to fall). The CV printed at each
measurement point is how you see whether it has anything left to do:
match-voice's SKILL.md carries the invocation and the gate details.

Measure after Phase 2 (profile at minimum; Pangram per the venue gates).
Record as the "after-voice" column.

### Phase 3: tighten-style (word recovery)

Run tighten-style **after** the rewrite. The rewrite buys the score and
costs words; this pass gives the words back without giving back the
score.

```bash
$RUN <tighten-style>/scripts/tighten.py --article <floor-pass.md> \
  --out <tightened.md>
```

(In venue mode add `--venue <name>` — the profile's targets become the
sentence floor and its hedge policy sets the TS-08 threshold. Pass
`--out` explicitly: tighten.py's default output name is `<stem>.tightmd`,
which the rest of this chain does not expect.)

Measured (2026-07-26 worktrees run):

| | words | mean sentence | Pangram |
|---|---:|---:|---|
| before match-voice | 2,378 | 17.0 | 77.8% AI |
| after match-voice | 2,502 | 17.8 | 0.0% AI |
| after tighten-style | 2,306 | 16.5 | 0.0% AI |

**The pass must run through the rewrite transport, never by hand.** The
same tightening applied by Claude against the rule catalog took a 0.0%
draft to **77.9%** — same article, same rules, opposite result, because
Claude tightens toward Claude's own register. Read the findings; let the
tool rewrite.

**A second placement exists, and it is the caller's.** A caller may run
tighten-style *before* the chain when the paragraphs are too dense for
the rewriter to clear the mechanical gate (the venue profile's
`structural_step` can name it for exactly that reason). This phase
answers a different question — "the rewrite left the prose leisurely" —
and a run states which placement was used; both is defensible only when
the first was for the gate reason and this one for the word count.

Record as the "after-tighten" column.

### Phase 4: accent-dial (optional)

When the author wants the accent — or the venue profile calls for it —
run accent-dial on the tightened text. It is a generative candidate
source with deterministic application, so it sits **after** every other
sampling stage and **before** the terminal stage.

```bash
python3 <accent-dial>/scripts/accent_dial.py --article <tightened.md> --dial 0.4
```

Three things this chain holds accent-dial to (its SKILL.md carries the
full contract, grain choice, and dial calibration):

- **It composes after structural repair, never instead of it** — the
  round-trip launders diction, not discourse structure, and gemma
  manufactures antithesis, so its output gets a structural recheck.
- **Its model exception stands**: default `gemma4:31b-cloud`
  (`ACCENT_DIAL_MODEL`), deliberately not the pipeline-wide Cohere
  default — the 2026-08-21 A/B showed stronger return-leg translators
  polish the accent away (L2 composite -0.009 vs +0.726) and score worse
  on Pangram (0.247 vs 0.150).
- **Its entailment review gate is mandatory** before the output moves on:
  applied paragraphs are reviewed against their originals and rejected by
  reverting in place — never by a model repair.

Record as the "after-accent" column. Skipped → say so in the
run-completeness check; the chain is complete without it.

### Phase 4b: scoped filter-tells recheck (pre-terminal)

Every sampling stage after Phase 1 can inject phrasing the early scan
never saw — match-voice injected bold lead-ins despite instructions,
tighten-style can raise nominalization, applied critic picks moved
Pangram 0.332 -> 0.421. A full re-scan would re-litigate author text and
invite the over-correction loop filter-tells warns about, so the recheck
is **scoped to the paragraphs the drivers actually changed**, and it runs
here — after the last sampling stage, before the terminal stage — because
the terminal contract forbids repairs after inject-vernacular.

```bash
$RUN <filter-tells>/scripts/scoped_scan.py <current.md> \
  --from-manifest <seed>.generation.yaml \
  --from-manifest <passNN>.generation.yaml \
  --from-tighten <tightened.md>.tighten.json \
  --from-accent-log <dialed.md>.log.json \
  --lexicon <tell_lexicon>       # venue mode
```

The drivers emit the scope themselves: drive.py writes
`changed_paragraphs` into its generation.yaml, tighten.py writes a
`<out>.tighten.json` sidecar, and accent-dial's edit log carries applied
flags (its indices are mapped onto prose paragraph numbers). Findings are
repaired editorially per the filter-tells procedure, through the rewrite
transport — never by hand — and idiolect calibration keeps the scan from
fighting accent-dial's deliberate injections: constructions below the
author ceiling never flag. An empty scope is a stated no-op, not an
error. A paragraph the chain never touched is out of scope by
construction; a tell in author text stays the author's to keep.

### Phase 5: inject-vernacular (terminal)

When the repository carries `writing-voice/idiolect.yaml`, run the
terminal vernacular stage on the Phase 3 (or Phase 4) output:

```bash
$RUN <inject-vernacular>/scripts/inject_vernacular.py <output.md>
```

Deterministic operators only — it restores the author's markers toward
the bank's essay targets and writes an edit log for the survival
analysis; nothing samples. This is the last stage that writes. Everything
after this line — the Phase 7 report, any final Pangram scan, and the
whole of the caller's review phase — reads the text and never modifies
it. A defect found from here on means the author's hand or a re-run from
a pre-terminal checkpoint. No idiolect.yaml → skip this phase; the
invariant then attaches to the end of the last stage that ran.

### Phase 6: run-completeness check

Before the report, state what actually ran. A partial run must report
itself as partial — the failure this prevents is a run that stops at an
unseeded Phase 2, looks complete, and quietly omits the step that does
the work.

| item | required |
|---|---|
| structural precondition | caller's structural step named (match-outline / tighten-style / skip), or the low-divergence signal reported |
| filter-tells | ran; findings triaged into real vs false positives |
| Phase 2 seed | ran, with the model and anchor selection named |
| Phase 2 iteration | every pass scored; stopped at an upturn, not a count |
| floor selection | the publish candidate is the floor pass |
| seed reach | reported (paragraphs changed / total) for the caller's cycle decision |
| tighten-style | ran through the rewrite transport; venue floor named when in venue mode |
| accent-dial | ran with its review gate, or skipped with the reason |
| scoped recheck | ran over the drivers' changed-paragraph lists, or empty-scope reported |
| inject-vernacular | ran, or skipped with the reason |
| canonical blocks | registry found, or passed explicitly |
| locks and markers | verified byte-identical after every stage |
| Pangram framing | one framing used throughout, named |

### Phase 7: Consolidated report

Print a single report. Each metric shows the stage columns —
baseline, after-tells, after-voice, after-tighten, after-accent (when it
ran) — and the total delta (final minus baseline).

In venue mode, head the report with the venue name and add a `target`
column to categories 2–5 wherever the profile's `targets` block carries the
metric — the question the report answers becomes "did the chain land on
the venue's measured register", not only "did the numbers move". Run each
gate from the profile's `gates` list in order and state pass/fail per gate;
omit the Pangram category entirely when that gate is absent.

**1. AI/Human detection (Pangram)** — one row per stage measured: human %,
mean score, verdict, CV.

**2. Readability** — Flesch Reading Ease, Flesch-Kincaid Grade, Gunning
Fog, SMOG Index.

**3. Lexical diversity** — Type-Token Ratio, Corrected TTR, Hapax Ratio,
Yule's K.

**4. Syntactic and structural** — sentence length mean / stdev / CV /
min / max / p10 / median / p90, mean clause length, passive per 100
sentences, paragraph cohesion.

**5. Stylometrics** — function word ratio; hedges, commas, semicolons,
em dashes, colons per 1000 words; top sentence openers.

**6. Filter-tells results** — antithesis pairs, banned words, structural
verdict, before and after cleanup.

**7. Match-voice gate stats** — accepted (mechanical), kept original,
skipped (short), mean distance, **seed reach**.

## File naming convention

| file | stage |
|---|---|
| `<stem>.md` | input (already structurally diverged by the caller; a caller's match-outline output is conventionally `<stem>-rewritten.md`) |
| `<stem>.vr-draft.md` / `<seed.md>` | after the Phase 2 seed |
| `pass<NN>.md` | iterator passes, kept with provenance |
| `<floor>.tight.md` or `--out` name | after tighten-style |
| `<stem>.dial<p>.md` | after accent-dial (when run) |
| `*.generation.yaml` | provenance record per drive.py run |

## When it breaks

- **Every paragraph kept-original with reason `?`:** suspect a gate crash
  before blaming the rewrite model. GH-318 had verify.py crashing on the
  `--no-anchors` anchors JSON, and drive.py recorded every crash as an
  ordinary rejection — runs shipped an untouched copy of the input while
  reporting success (Pangram before == after is the tell). Check the
  provenance YAML: `accepted: 0` with unchanged scores means the gate never
  ran, not that the rewrites failed.
- **match-voice gate rejects everything (distance 0.0):** the input is
  not structurally diverged. Hand the run back to the caller to run
  match-outline (or more aggressive Phase 1 semantic edits) — the
  precondition in the input contract above.
- **tighten-style gate rejects everything:** the prose is already at or
  below the density floor — there is nothing to tighten.
- **Pangram score does not improve:** the semantic cleanup missed rhetorical
  patterns. Re-run filter-tells Step 3 (the full semantic analysis) and look
  for surviving antithesis pairs, tricolon patterns, or CoT leakage.
- **Meaning drift:** rewrites compound; the caller's match-outline pass
  is the largest source of drift. Compare the final output against the
  original (not the intermediate) to catch cumulative losses.
- **Filler regression:** an unanchored iterator can introduce filler.
  Check the stylometrics section of the report.

## Calibration data

**Detector discontinuity, 2026-09-01.** The July/August floors below
are not comparable to current scores, for two separate reasons. First, a
client model switch: until 2026-09-01 `scripts/pangram.py` sent no
`model`, so the API scored on the `default` alias; commit b6c649a
(2026-09-01 23:25 -0400) made `pangram-4` the default, and the two
models disagree on identical text (15.7% vs 64.1% AI). The pair once
cited here as a retrain — a published-pipeline article at 0.2061 mean
window on 2026-08-23, then 0.9955 untouched on 2026-09-02 (substack#323)
— crosses that switch, so it measures the model change, not a vendor
retrain. Second, a vendor version change, separately established and of
unknown date: identical prose read 0.445 on `default` 3.3.2 (2026-08-28)
and 1.000 on 4.1 (2026-11-04). Every score below is a dated record on
`default`. Reuse of any recipe re-measures first. The newsletter venue
retired its pangram gate (paper-stash#85); that decision stands — its
posture is the process disclosure, not the race — only its stated
reason has changed.

The historical runs below were measured under the pre-GH-208 layout, with
match-outline as the chain's own first phase; its role is unchanged — it
ran before filter-tells then, and runs caller-side now.

Tested on `2026-10-29-how-to-break-an-ais-heresy.md` (2,357 words) with
hardcoded Evans how-to blueprint and anchor-tags.

**Gate-bug caveat (GH-318, fixed 2026-07-29).** Through 2026-07-28, verify.py
crashed on the list-format anchors JSON that `--no-anchors` writes, and
drive.py recorded every crash as kept-original. Any `--no-anchors` row from
that window may describe an untouched copy of its input, not a rewrite: the
on-disk provenance for the 2026-07-28 no-anchors runs shows `accepted: 0`
with Pangram before == after. Rows marked *unverified* below predate the fix
and could not be reproduced from provenance; the *verified* row is a
post-fix run with all 35 paragraphs accepted (distance 0.533).

| variant | pipeline | Pangram human % | mean score | status |
|---|---|---|---|---|
| original | none | 0% | 0.993 | verified |
| match-outline only | Kimi rewrite | 0% | 0.993 | verified |
| semantic cleanup only | filter-tells on Kimi rewrite | 0% | 0.993 | verified |
| match-voice venue-voice | Kimi + semantic + Tanenbaum/Martin anchors | 0% | 0.765 | pre-fix, anchored |
| match-voice author 2.5x | Kimi + semantic + Djukic anchors | 26.6% | 0.454 | pre-fix, anchored |
| match-voice Evans how-to | Kimi + semantic + Evans anchors | 0% | 0.955 | pre-fix, anchored |
| match-voice no-anchors | Kimi + semantic + gpt-oss no anchors | 100% | 0.245 | **unverified** (broken-gate window) |
| **match-voice no-anchors (2026-07-29)** | **Kimi + semantic + gpt-oss no anchors** | **0% human, 76.2% AI-assisted, 23.8% AI** | **0.576** | **verified, working gate** |
| no match-outline | semantic + gpt-oss no anchors on original | 0% | 0.993 (gate rejected) | **unverified** — matches the GH-318 crash signature |
| no semantic cleanup | gpt-oss no anchors on original | 0% | 0.993 (gate rejected) | **unverified** — matches the GH-318 crash signature |

The ablation claim (each step necessary) rests on the two unverified rows and
needs re-measurement with the working gate before it can be stated as fact.

All calibration above was measured with match-outline as the structural
step. tighten-style calibration is pending.

**Iteration calibration (2026-07-29, working gate, stay-on-track article,
published as pass02).** Seed: Kimi match-outline + filter-tells + gemma4
match-voice with Krugman anchors (0.992 — anchored passes still do not move
Pangram, but change the fingerprint the iterator erases). Then gpt-oss
no-anchors, iterated; full per-pass data in
idea-factory:substack/2026/Q4/experiments/2026-07-29-gptoss-iter/stats.csv.

| pass | mean window | human % |
|---|---|---|
| seed | 0.992 | 0 |
| 1 | 0.579 | 43 |
| **2** | **0.432** | **55** |
| 4 | 0.418 (floor) | 34 |
| 10 | 0.700 | 0 |

**Well-edited-input regime (2026-08-22, strategy-theatre).** The table
above was measured descending from a fresh AI draft at 0.992, where every
pass had something to strip. Against prose already through two critic
panels and a socratic pass, the same recipe behaves differently and still
works:

| stage | score | note |
|---|---|---|
| article | 0.375 ai / 0.370 human | three rounds of human editing |
| anchored gemma seed | 0.395 / 0.435 | **19 of 125 paragraphs changed** — the gate rejected most rewrites because the text is tight |
| pass 1 (gpt-oss) | 0.251 / 0.615 | floor |
| pass 2 | 0.344 / 0.597 | upturn, stopped |
| floor, cold-reviewed (23 of 65 kept) | 0.370 / 0.550 | the publishable number |

Two lessons. The seed does not need to rewrite wholesale to work — 19
paragraphs of foreign fingerprint were enough. And survival at cold review
falls as input quality rises (21% single-shot, 51% harness on mid-edit
text, 33–35% on well-edited text): the chain's value is front-loaded
onto drafts, and on edited prose the gated gain is real but small.

Same-family iteration is a no-op: kimi match-voice on kimi-derived prose
moved distance 0.05, Pangram 0.993 -> 0.993. The iterator must be a
different family from whatever produced the input.
