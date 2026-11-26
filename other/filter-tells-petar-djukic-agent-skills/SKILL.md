---
name: filter-tells
description: 'Detect and fix AI writing patterns recursively. Use when: reviewing text for AI tells, cleaning AI-generated drafts, checking for CoT leakage, measuring text perplexity and burstiness, making text sound human, fixing opening diversity. Triggers: filter-tells, ai detection, ai writing, perplexity, burstiness, CoT leakage, humanize text, opening diversity, sentence starts.'
argument-hint: 'Path to markdown file to analyze and fix'
---

# filter-tells: AI Writing Detection and Correction

Detects mechanically, removes editorially, and hands voice restoration to
`match-voice`. Three detection layers — lexical, structural, semantic — flag
passages; Claude then rewrites them under the convergence rules below, and
re-scans. There is no deterministic strip: a banned word is a one-word swap,
but a cadence tell needs the sentence rewritten, and that is judgment.

Filtering leaves prose that is *neutral* — no tells, but no voice either. When
the passage has to sound like the author, that is `match-voice`'s job.

*Renamed from `de-ai` (2026-07). The old name implied the skill only removed;
it detects, and the removal is editorial.*

## Standing Warning: Scripts Are Blind to Rhetorical Patterns

The two scripts (`detect-lexical.sh`, `detect-structural.py`) measure surface metrics only — banned words, opening diversity, sentence length variance, dash density. They **cannot** detect the rhetorical patterns that constitute most of the AI signal in real prose:

- Declarative pairs ("X is Y. Z is W.")
- Definition-by-enumeration ("X extends in two ways")
- Meta-narrative bridges ("The analogy breaks in one place")
- Triple parallels ("clearer instructions, tighter constraints, fewer ambiguous cases")
- Comprehensive enumerated sweeps in parentheses

Partial exception: `detect-structural.py` now has a `detect_antithesis` check that catches the lexically-marked subset of negation-then-affirmation ("X is not Y. It is Z.", "The meter was.") and clipped antithesis fragments. It does not catch the purely semantic reversal ("Same quality out. Different bill." used without a negation word). Prompt 6 in Step 3 covers that remainder. Treat the regex as a recall aid, not full coverage of the pattern. `detect_semicolon_aphorisms` likewise flags the lexically-markable balanced semicolon pair ("The checker produces the bound; the language is the form that makes it possible.") as semantic-pass candidates — advisory, since human semicolons are legitimate at native rates (GH-496).

A `clean` or `minor-issues` verdict from the structural script means the surface checks passed. It does **not** mean the prose is in voice. Step 3 (semantic analysis by Opus) is the only layer that catches the rhetorical AI tells the scripts still miss. Skipping Step 3 produces false-negative reports.

The blindness runs in **both directions**. The scripts flag the bland AI direction (low burstiness, repetitive openings). Text iteratively rewritten against these very detectors overshoots into the opposite register — uniformly maximal polish, epigram-closing paragraphs, coined formulae, word salads — and passes every surface check while reading as obviously machine-made ("the LinkedIn voice"). The structural script now emits overshoot metrics (`plain_sentence_rate`, `punch_clustering`, `salad_rate`, repeated formulae, `suspicious-overshoot` verdict), but the judgment lives in Prompt 0 (cold read) and Prompt 7 (overshoot assessment). A `minor-issues` verdict on a document with prior filter-tells history deserves MORE suspicion, not less.

**Do not infer voice quality from the structural script's verdict label.** Voice is a judgment, not a statistic.

**Long unattended runs on a local Ollama:** set `OLLAMA_WAIT_SERVER=600` — a supervised server can be reaped mid-run, and the transport then polls for its return instead of failing the paragraph (GH-173). Hosted (cohere:) models are unaffected.

## When to Use

- Before publishing any document drafted or edited by AI
- When reviewing a file for AI writing tells
- When a document "feels" AI-written but you can't pinpoint why
- After AI-assisted writing sessions to clean the output
- To check for CoT (chain-of-thought) leakage in final text

## Prerequisites

- Python 3.8+ available
- The target file is a markdown file
- The writing-style-guide.md is present in `templates/`

## Procedure

### Step 0: Cold Read (Model, BEFORE the scripts)

Run Prompt 0 from [perplexity-prompts.md](./references/perplexity-prompts.md) on the document before looking at any script output. The cold read answers what no metric can: could a plain reader follow this on one pass, and is the register appropriate for the venue? Record the COLD_VERDICT — it anchors nothing and is anchored by nothing.

### Step 1: Lexical scan (no model)

```bash
bash <filter-tells>/scripts/detect-lexical.sh <file-or-dir> ...
```

Line-numbered matches by category — banned words, clichés, false emphasis,
narrative-pivot frames, mechanical transitions. Instant and free. Accepts files
or directories (`*.md` recursively).

**Venue lexicons (GH-337).** The catalog splits into core tells (always on:
chat residue, AI clichés, mechanical transitions, narrative pivots, ornate
register, filler measurement) and venue-keyed lists selected with
`--lexicon=NAME` — `newsletter` (default; the full banned-word list), `book`
and `industry` (share the newsletter word lists; their deltas are
prose/structural rules living in tighten-style's hedge policy and the
semantic pass, not word lists), `academic` (drops the newsletter banned
words — "critical" and "fundamental" are ordinary methods-section
vocabulary — keeps only the non-statistical false-emphasis adverbs, and adds
paper-template tells like "novel framework" and "pave the way"), and `none`
(core only). When the document has a venue profile
(`writing-voice/venues/`, see the writing-voice rule), pass its
`tell_lexicon` value; `drive.py --lexicon` threads it through the rewrite
loop's re-scans via `FILTER_TELLS_LEXICON`.

Two categories are scored by **density** rather than per hit, because their
words are legitimate individually and only the rate says anything.
**Ornate register** flags above 4.0 per 500 words. **Conversational filler** —
`just`, `actually`, `really`, `basically`, `simply` — is the register a rewrite
lands in when it stops sounding corporate, and it is **reported, not gated**.

Both densities count **occurrences**, not matching lines. A markdown paragraph
is one long line, so a line-based count scored three flourishes in a paragraph
as one, and undercounted worst on the long paragraphs the measure is for
(GH-242). The 4.0 ornate threshold survived that correction unchanged: across
193 documents in three corpora — this repository's rules and skills, and the
reference `writing-voice` corpus — one file exceeds it, and that file is
[banned-patterns.md](./references/banned-patterns.md), which flags itself because
it lists the patterns.

That asymmetry is a calibration result, not an oversight. The banned-word list
holds `leverage` and `robust`, false emphasis holds `crucially` and `notably`,
and filler was the one machine register with nothing in front of it — a rewrite
that traded corporate vocabulary for chatty filler passed every check (GH-233).
The obvious fix, a threshold, does not survive contact with the corpus:

| prose | filler per 500 words |
|---|---|
| this repository's documentation, 17 files | 0.0–1.7 |
| the author's own articles | 0.2–0.3 |
| the two machine rewrites that prompted the check | 2.8 and 6.8 |
| the reference venue-voice corpus — Dan Luu, Evans, Krugman, Rands, Yegge, Fowler | 2.1–15.6 |

Every value that catches the rewrites also condemns every essay in the anchor
corpus, which is the register a punchy rewrite is steering toward. A level tells
you which register a document is in; it cannot tell you the document got worse.

So filler is judged on **movement against the document's own earlier rate**:

```bash
python3 <agent-dir>/scripts/register_markers.py --compare <before> <after>
```

which reports `filler/500w  0.3 -> 2.8  REGRESSED`. Set `FILLER_DENSITY_MAX` to
gate on an absolute level when you already know the register you want.

Two other categories need calibration rather than obedience.
**Marketing/hype vocabulary** (`venue-jargon`) is human register flagged as
venue-inappropriate jargon, not as an AI tell — and never flag quoted text or a
source's own title. **CoT candidates** are patterns that may be scaffolding and
may be ordinary prose; they do not fail the scan. Carry them to Step 3, where
the removal test decides: delete the sentence and re-read the paragraph, and if
nothing is lost it was scaffolding.

[reading-scan-output.md](./references/reading-scan-output.md) lists the
candidate patterns and what each metric means.

### Step 2: Structural analysis (no model)

```bash
python3 <filter-tells>/scripts/detect-structural.py <file-or-dir> ...
```

Default threshold `strict`; `--threshold=medium` for drafts, `relaxed` for
early notes. A verdict of `likely-ai`, `suspicious`, or `suspicious-overshoot`
sends you to Step 3. See
[reading-scan-output.md](./references/reading-scan-output.md) for the metric
signals, and [opening-diversity-fixes.md](./references/opening-diversity-fixes.md)
when `opening_diversity` fires — it is the hardest to fix, since it means
rewriting sentence openings across the document.

**The corpus invocation (multi-chapter works).** The coinage and
repeated-formulae detectors count across every file of one invocation, so a
per-chapter scan cannot see a phrase coined across a book or a paper's
chapter set — twenty uses of one formula, spread over ten files, never
reaches any single file's threshold. For a work of more than one chapter,
also run the script once over the whole set:

```bash
python3 <filter-tells>/scripts/detect-structural.py <chapter files or dir>
```

Carry the cross-file coinage, repeated-formulae, and aphorism candidates to
Step 3 beside the per-file results. A repository's protected-terms file
names the terms of art that are repetition by design, not coinage; judge
candidates against it before seeding Step 3 (GH-495).

**Voice distance — the positive check.** The named detectors are a denylist: a
tell must be known to be caught. Distance from a human corpus is the
complement, catching deviations nobody has named yet.

```bash
python3 <match-structure>/scripts/style.py --db <db> corpus     # writes voice-profile.json
python3 <filter-tells>/scripts/detect-structural.py <files> --voice-profile=<db-dir>/voice-profile.json
```

**A document that passes every named check but sits far from the corpus
profile (any |z| ≥ 2) is NOT clean.** Report "passes named checks;
voice-distance high" and route to Step 3 with the deviating metrics and their
direction as seeds. No corpus, no check — say so in one line and continue.

**Burstiness (sentence-length dispersion).** The structural metrics carry
`sentence_length_cv` alongside the mean, stdev, min, and max, and the
voice-distance block scores CV against the corpus. Only stdev is thresholded
— CV is reported, because the flags above are calibrated on stdev and moving
them is a separate decision. Quote CV when comparing documents or registers:
stdev alone conflates dispersion with sentence length, so a paper and a
newsletter differ on it without differing in uniformity.

Report CV before and after a rewrite pass, next to the Pangram score. On a
plain stylometric model the two discriminative features are AI-phrase density
and burstiness; this skill attacks the first, and the second only shows up if
someone measures it. The canonical before/after number is
`style.py burstiness <draft.md> --baseline <before.md> --text` — the CV here
runs lower, since `split_sentences()` drops fragments under four words and
those are the ones that widen the spread. Keep both sides of a comparison on
one tool.

### Step 3: Semantic Analysis (Requires Opus) — MANDATORY

If Pass 1 or Pass 2 found *any* issue, Step 3 is required, not optional. The scripts are blind to rhetorical patterns. Reporting a verdict without Step 3 is a procedural error and produces false negatives.

Step 3 may be skipped only when Pass 1 and Pass 2 both return zero matches and zero issues.

Load the prompts from [perplexity-prompts.md](./references/perplexity-prompts.md) and run against the target text:

Load the prompts from [perplexity-prompts.md](./references/perplexity-prompts.md)
and the index of which does what — and which are mandatory when — from
[prompt-catalog.md](./references/prompt-catalog.md).

#### Required output of Step 3

The final report from Step 3 must follow [`assets/report-template.md`](./assets/report-template.md) and must include:

1. The rewrite priority list from Prompt 5's output, structured by issue with line references.
2. Explicit confirmation that Step 3 was run (which prompts were applied, summary findings from each).
3. An honest plain-language verdict. Options: "in voice — no rewrite needed", "isolated issues — spot edits only", "pervasive rhetorical patterns — section rewrite needed", "heavy AI fingerprints — paragraph-by-paragraph rewrite needed", "over-corrected — needs plain-prose rewrite toward the venue register".

Freeform summaries without these elements are not a valid Step 3 output.

### Step 4: Targeted Rewrite

For each flagged passage (in priority order from Prompt 5):

1. Load the [rewrite instructions](./references/rewrite-instructions.md)
2. Load the project's voice reference for this document type, if one exists — for example a `.claude/rules/<voice>.md` file the project provides (per-format voice guides are common: one for articles, one for long-form, etc.). If the project defines none, infer the target voice from existing published work in the same venue. Do not assume any specific file name.
3. For CoT leaks: remove the flagged sentence and re-read the paragraph. If no information is lost, the sentence is a true CoT leak — delete it. If information is lost, the sentence uses CoT-style wording on real content — reword to remove the scaffolding phrase while preserving the content.
4. Rewrite ONLY the flagged passage using the rewrite prompt template
5. Constraints: preserve meaning, match author voice, don't introduce new AI patterns
6. For a `.tex` source: apply the rewrite to the source file in place at the flagged line (the detex prose view is analysis-only, never an edit target). Preserve surrounding `\citep`/`\ref`/comments/math/macros; never reconstruct the file or round-trip through markdown. See "Editing LaTeX sources in place" in the rewrite instructions.

The headless driver (`scripts/drive.py`) does this step for flagged paragraphs only, computing their candidates concurrently (`--jobs` / `FILTER_TELLS_JOBS`, default 4; the first runs alone so a missing key or dead server costs one call; the splice stays sequential, GH-433). `--rewrite-scope all` restores the old whole-document pass for a likely-ai verdict. Every candidate goes through a splice gate before it lands (GH-411):

- A model's "Here's the rewritten paragraph:" lead-in is stripped.
- match-voice's mechanical gate refuses lost or invented citations, numbers, quoted spans, and markup, and a rise in dashes.
- `critique.mechanical` refuses introduced banned words, a new antithesis or tricolon, and lost protected terms (`<stem>.protected-terms.txt` when present).
- A critic model judges meaning entailment. A `repair` verdict gets one retry with the critique as constraints, and a `reject` keeps the original. The critic is the rewrite model unless `--critic-model` names another; `--no-critique` gates mechanically only.
- Canonical-block paragraphs (`writing-voice/canonical-blocks.txt` or `--canonical-blocks`) are never sent.

Refusals are recorded per pass as `gate-refused` errors with their reasons.

On tight post-pipeline drafts the ungated pass leaked prompt diction, invented facts, and deleted canonical lines. Its 2026-08 bake-off winners were measured on raw drafts and have not been re-measured in this regime.

### Step 5: Recursive Validation

After each rewrite:

1. Re-run `detect-lexical.sh` on the rewritten section
2. Re-run `detect-structural.py` on the rewritten section
3. If issues remain AND count decreased: iterate (max 3 total passes)
4. If issues remain AND count same or increased: STOP, flag for human review
5. If clean on both scripts: the rewrite has passed the **surface** check — proceed, but do not treat this as approval of the rewrite's rhetoric

The scripts confirm surface metrics only (banned words, opening diversity, length variance). They are blind to most rhetorical patterns — including ones a rewrite can *introduce*, such as parallelism that moves from sentence heads to tails. A green Step 5 is necessary, not sufficient. The rewrite is not accepted until it clears the independent Step 6 check below; Step 5 green is not that approval.

### Step 6: Final Semantic Verification (independent evaluator)

The agent that wrote the rewrites cannot be the only judge of them. It shares the blind spots that produced them — it broke a mirror pair's heads and kept its tails, and its own re-read reads the result as fixed. This is the maker–checker gap: an auditor who watched the code get written blesses the blind spots that wrote it. So Step 6 runs as an **independent evaluation, in a fresh context**.

Run it as a separate session or agent that sees ONLY the final rewritten text and the Step 3 report — never the rewrite history, the reasoning, or the diffs. (In Claude Code, spawn a subagent for this; in any tool, at minimum start a clean context and do not carry the rewrite conversation into it. Portability: the requirement is a maker≠checker separation, not a specific mechanism.)

Give the evaluator this stance: **assume the rewrites introduced new patterns.** Its job is to find them, not to confirm the fix. Specifically:
- Enumerate every parallelism, mirror pair, or echo in the rewritten passages — checking **both ends** of each sentence, heads and tails, since a rewrite commonly relocates parallelism from the front to the back (run the Prompt 6 / antithesis and Prompt 3 Part-B enumerations on the rewritten spans specifically).
- Check for new patterns the rewrite introduced (banned words, mechanical transitions, CoT leaks).
- **Did the rewrites sand off texture?** Over-compression is its own tell (rewrite-instructions.md §3b): confirm dated/personal asides, first-person hedges, deliberate two-beat rhythms, and conversational gestures survived; that clipped fragments did not stack at adjacent paragraph or section boundaries; and that `sentence_length_std` held or rose. If the prose reads "too sleek," restore slack — a reverted over-edit is a fix, not a regression.
- Consistency between rewritten and preserved sections; overall flow.
- For a `.tex` source, verify against the edited `.tex` itself (analysis runs on its detex prose view); the in-place edits live in the source file, and untouched lines keep their numbers, so any still-flagged finding maps to source as before.

**The co-judge leg (cross-family).** A fresh context closes the maker–checker gap; it does not close the family gap: an evaluator of the same model family shares the register that produced the rewrites, and a family rates its own epigrams as fine. When the host has a second-family transport configured — the Ollama transport match-voice and the ross read already use — run the Step 6 stance there too: send each rewritten or suspect passage through the second family with Prompt 8, and treat a span **either** family flags as flagged. The report names which families judged. No transport configured, no leg — say so in one line, as the ross read does (GH-494).

Anything the independent evaluator flags goes back through Step 4. A rewrite is accepted only when a checker that never saw it made pass it clean.

## Voice injection (when the repository defines a target voice)

A writing repository may carry a `writing-voice/` directory of exemplars — the
contract, manifest schema, and `author-voice`/`venue-voice` roles are in this
repository's writing-voice rule. When one is discoverable from the file under
review, measure against it and steer rewrites toward it. **Absent, all of this
is skipped and behaviour is exactly as before.**

The scripts live in `match-structure`, where exemplar retrieval belongs with
the rest of the profile work.

```bash
python3 <match-structure>/scripts/voice_anchors.py discover <file>
python3 <match-structure>/scripts/voice_anchors.py profile --for <file>
python3 <filter-tells>/scripts/detect-structural.py <file> \
  --voice-profile=<repo>/writing-voice/.voice-profile.json
python3 <match-structure>/scripts/voice_anchors.py anchors --text <passage-file>|- --for <file> -k 3
```

With the profile passed in, `voice_distance` reports each metric as a distance
from the author's own register rather than against fixed thresholds — the same
mechanism a match-structure corpus profile uses, one flag with two sources. The
profile caches in `writing-voice/.voice-profile.json` and rebuilds when a
sample's mtime changes; `--force` overrides.

**Anchors are the point of the feature.** Before rewriting a flagged passage,
retrieve the topically nearest exemplars (tf-idf over paragraphs, stdlib,
preferring `author-voice`) and inject them into the rewrite prompt's
`{voice_anchors}` slot — see rewrite-instructions.md. A rewrite with no target
register aims only at *not tripping detectors*, and that is the documented
cause of overshoot into uniform polish. Anchors give it a register that exists.

Pass the same anchors into Prompt 7. Drift toward heavier polish is an
overshoot signal even when every surface check passes: the anchors make "too
sleek" measurable against something concrete.

## Author-baseline calibration (idiolect.yaml)

Some constructions the structural pass treats as AI tells are, at the right
rate, this author's voice: the colon-verdict, the em-dash aside, the "X, not
Y" antithesis. When `writing-voice/idiolect.yaml` is discoverable from the
file under review (auto-discovery walks up from the first input;
`--voice-dir=` overrides, `--no-voice-calibration` opts out), those
constructions flag only **above the author-calibrated ceiling** — the
marker's essay target plus the bank's ±30% tolerance — instead of on sight.
The idiolect file's marker list drives the calibrated set; the generic flat
thresholds stay in force for every other check and for every repository
without an idiolect file, where behaviour is exactly as before.

Calibrated flags are distinguishable in the output: the issue carries
`"calibration": "author-ceiling"` and its detail says *reduce toward the
target, not to zero* with the allowed count for the document — so a rewrite
pass steered by the flag trims the excess instead of eliminating the
construction. A ceiling below the flat threshold never tightens the check;
the flat threshold is the floor.

**Migration note.** The motivating counter-example is the Strategy Theatre
antithesis 15→1 reduction: an uncalibrated antithesis flag steered a rewrite
that cut fifteen instances down to one, and some of the fifteen were the
author (the idiolect measures "X, not Y" at 2.29/1000 in the journal against
0.24 native — the construction is the voice, the *excess* is the tell).
Ceilings come from `idiolect.yaml`, never hand-written here: re-measure the
corpus upstream and this pass follows.

## Scoped mode (GH-209): scan only what the pipeline changed

`scripts/scoped_scan.py` runs the lexical and structural scans over only
the paragraphs the humanize chain's drivers report as changed — the
pre-terminal recheck of humanize Phase 4b. Scope comes from the drivers'
own artifacts (drive.py's `changed_paragraphs` manifest line, tighten.py's
`<out>.tighten.json` sidecar, accent-dial's edit log) or an explicit
`--changed "1,3,7-9"`. It builds a scoped view, runs both detectors on
it, and maps every view paragraph back to its source lines; `--lexicon`
and `--voice-dir` pass through, and voice-dir discovery walks up from the
ARTICLE path, not the temp view. Repairs stay editorial per Step 4, and
they route through the rewrite transport. The scoped scan never gates
author text: an untouched paragraph is out of scope by construction. An
empty scope exits 2 with a message — nothing changed means nothing to
scan.

## Paragraph extraction (shared)

`scripts/md_paragraphs.py` is the canonical markdown paragraph extractor for
the prose skills, and lives here because filter-tells is what the others already
import from. It classifies every body line — prose, heading, figure,
figure-caption, table, table-caption (pandoc `Table:` lines, GH-465), code,
reference, blockquote, list, rule, blank — and
returns prose blocks with the source line ranges a rewrite can be spliced back
into. `match-voice/scripts/drive.py` imports it rather than carrying its own
parser (GH-167); a sibling import works because every agent surface carries
the full skill set.

```bash
python3 .cursor/skills/filter-tells/scripts/md_paragraphs.py <file.md> [--json] [--coverage-only]
```

`--coverage-only` prints the classification tally, which is the answer to "did
the driver skip paragraphs, or does the document just not have any there?"

Two splitters stay separate on purpose, each with the reason recorded at its
definition: `detect-structural.py` runs on flattened text including detexed
LaTeX and its boundaries are baked into the eval baseline, and
`match-structure/scripts/style.py` chunks exemplars for comparison and never needs
line fidelity.

## External check (Pangram — optional, uploads the document)

Every detector above was written by reading model output and writing down what
it does. That makes "the detectors stopped firing" a circular answer to "did
the rewrite work?" — this skill grading its own homework. Pangram has never
seen our denylist, so its result is evidence rather than an echo. It is the
only outside measurement here, and the only step that sends text off the
machine.

**Consent first, every document — grantable in standing form.** See the
upload rule in the `writing-voice/` directory rule: the operator can
record a standing, revocable grant (`writing-voice/pangram-consent.yaml`,
`consent: standing`; env `PANGRAM_CONSENT` overrides either way), under
which the drivers score by default and `--no-pangram` opts a run out
(GH-210). A key in the environment is still not consent. No grant and no
per-document yes, or no key, means skip and say so — never substitute a
local result for it.

```bash
python3 <agent-dir>/scripts/pangram.py --check                      # key + reachability, spends nothing
python3 <agent-dir>/scripts/pangram_report.py payload --article <file.md>   # prose-only payload + span map
python3 <agent-dir>/scripts/pangram.py --text <file>.payload.txt --json > before.json
python3 <agent-dir>/scripts/pangram_report.py report --response before.json --spans <file>.payload.spans.json
```

What this skill takes is a point-in-time reading. The before/after comparison
belongs to match-voice, whose driver captures the baseline before it rewrites
anything (`drive.py --pangram`) — the one moment it can still be captured. Both
skills invoke the same two scripts from the shared root; neither owns them.

Only prose is submitted — the shared extractor drops code fences, tables, and front matter, which both keeps non-prose from skewing a prose detector
and holds down cost, since billing counts started 1,000-word blocks. A full
before/after comparison costs two scans. What an account allows is the
account's business and no limit is enforced here, so check rather than
remember: `pangram.py --check` confirms the key and the endpoint without
spending a scan, and the API reports 402 when credits run out and 429 when
requests arrive too fast.

Read the result as three document fractions (`fraction_ai`,
`fraction_ai_assisted`, `fraction_human`) plus per-paragraph scores. There is
no single AI score. And per the Verdict Validity Rules below, a favourable
result never issues a clean verdict on its own.

## Calibration (eval corpus)

The scripts are calibrated against the labeled corpus in
[eval/](./eval/README.md): `python3 eval/run_eval.py` reports per-detector
fire rates on human vs ai classes and diffs against the committed baseline.
Every new detector passes the gate there before merge (fires on an ai sample;
fires on ≤20% of human samples; no existing human-class rate rises). Only the author populates the
human class.

Threshold provenance lives in [references/detector-thresholds.md](./references/detector-thresholds.md): every numeric gate with its justification or an explicit "uncalibrated" marker, the boundaries between overlapping detectors, and the standing noise-audit results.

## Failure taxonomy

[references/failure-taxonomy.md](./references/failure-taxonomy.md) maps every
detector, prompt, and pattern class to its linguistic level (lexical /
syntactic / rhetorical / discourse / pragmatic) and lists the known-empty
territory. New tells are classified there before their detector is written.

## Prevention (drafting time)

When the user is about to DRAFT — not repair — hand the model
[references/drafting-guidance.md](./references/drafting-guidance.md) as part of
the drafting context instead of running this pipeline after the fact. It is
the compact DO-form counterpart to banned-patterns.md: the tells are cheaper
to prevent than to remove, and every confirmed failure class feeds both files
(the pair rule in banned-patterns.md "Updating This List"). The detection
pipeline still runs on the result; prevention lowers the pass count, it does
not replace verification.

## Abstract Mode

Abstracts are read ~100x more than the body and have the most rigid,
best-documented structure — the easiest text to diagnose and repair.
Trigger: the user asks to check or fix an abstract, or a publication-verdict
run encounters one. Standards: `references/abstract-standards.md`.

**Analyze (default):**

1. Mechanical checks:
   ```bash
   python3 .cursor/skills/filter-tells/scripts/abstract-check.py <paper.md> \
     --body <results.md> <other-chapters.md...> --limit 200
   ```
   Locates the abstract (LaTeX environment, front matter, heading, or
   whole file), counts words against the venue limit (default 200), runs
   the number-traceability check against the body, and sweeps
   self-containedness (citations, section/figure references).
2. Run Prompt 10 (move map: one row per sentence — move, conforming,
   action), plus Prompt 8 and Prompt 9 Part B on the abstract's sentences.
3. Report the move map and verdict: conforming | repairable | rebuild.

**Fix (opt-in, only on a failing verdict):** run Prompt 11 — rebuild move
by move from body excerpts (written-last principle: intro -> moves 1-2,
results numbers verbatim -> move 3, conclusion -> move 4; never reuse
failed phrasing). Then verify: abstract-check.py traceability must pass
(any number absent from the body rejects the rewrite), re-run Prompt 10
(max 3 passes), and run the standard scans for register regressions.

## Convergence Rules

- Rewrites must never be validated by script metrics alone — that is how overshoot happens. After each rewrite pass, re-run Prompt 0 on the rewritten section; a rewrite that improves the metrics but worsens the cold read is a regression. An external detector score counts as a metric here: a falling `fraction_ai` alongside a worse cold read is still a regression.
- Maximum 3 rewrite iterations per passage
- If iteration N finds >= issues as iteration N-1, stop immediately
- Never rewrite direct quotations
- Never rewrite formal specifications or requirement statements
- When in doubt, flag for human rather than risk meaning loss

## Verdict Validity Rules

- A "clean" or "in voice" verdict requires Step 3 to have been run and to have returned no high-priority issues. Verdicts issued without Step 3 are invalid.
- A `clean` or `minor-issues` label from the structural script is not a substitute for Step 3. The label is a surface-metric summary, not a voice assessment.
- **An external detector result is not a verdict either.** A Pangram `Human Written`, a low `fraction_ai`, or an empty flagged list does not certify a document and does not substitute for Step 3. It is one more input to the read, and it errs in both directions — a false negative on polished AI prose, a false positive on a terse human author writing in an unusual register. "Pangram says human, so it is clean" is the same procedural failure as anchoring on the structural script.
- "Looks mostly fine" / "largely in voice" / similar freeform softening language is not a valid verdict. Use one of the four plain-language options from Step 3's required output.
- If you anchor on the structural script's verdict and skip Step 3, the report is a procedural failure regardless of how the prose actually reads.

## Model Selection

**Use Opus for ALL passes.** Rationale:
- Detection requires deep model self-awareness (simpler models can't recognize their own patterns)
- Rewriting requires preserving technical meaning while transforming style
- Validation must be strict enough to achieve convergence
- Cost per document is low (sections are small, 3 iterations max)

## Reference Documents

- [Banned patterns database](./references/banned-patterns.md)
- [CoT leakage patterns](./references/cot-leakage-patterns.md)
- [Opening diversity fixes](./references/opening-diversity-fixes.md)
- [Perplexity proxy prompts](./references/perplexity-prompts.md)
- [Rewrite instructions](./references/rewrite-instructions.md)
- [Report template](./assets/report-template.md)

## Quick Mode (Lexical + Structural Only)

For in-progress drafts where you want a fast surface-pass without burning model calls:

```bash
bash .cursor/skills/filter-tells/scripts/detect-lexical.sh <file-or-dir>
python3 .cursor/skills/filter-tells/scripts/detect-structural.py <file-or-dir> --json
```

Quick Mode is for working drafts. It is **not** valid for a publication verdict. Quick Mode catches the surface-detectable patterns. The rhetorical patterns that account for most of the AI signal are invisible to the scripts and require Step 3. Do not report a verdict based on Quick Mode output alone.

Working and specification documents are the exception that most needs more than Quick Mode: a system requirements document or design doc another session will execute is exactly where compressed-conversation phrases accumulate (undefined coinages, metaphors for mechanisms, editorializing adjectives). When the scripts surface `coinage_candidates` or `editorializing` hits on such a document, run Prompt 8 (whole-document, mandatory) and Prompt 8b before signing off — a spec that ships private vocabulary to an executor who was not in the conversation is a defect Quick Mode cannot rule on.
