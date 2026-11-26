---
name: match-voice
description: >-
  Rewrite paragraphs of a draft in the author's voice using a second model
  family served by Ollama, with a verification gate before any text is spliced
  back. Retrieves voice anchors from the repository's writing-voice/ exemplars,
  sends paragraph plus anchors to a local (or cloud) Ollama model, then gates
  the result on citation/number preservation, meaning entailment, anchor
  similarity, and register. Triggers: voice rewrite, rewrite in my voice,
  ollama rewrite, rewrite paragraphs, local model rewrite, sound like my
  earlier papers, rewrite against writing-voice.
---

*Renamed from `voice-rewrite` (2026-07). **The name `match-voice` previously
belonged to the stylometry skill, now `match-structure`** — if you invoked
`match-voice` before this date expecting measurement, you want
`match-structure`. This skill rewrites.*

# match-voice (Ollama rewrites, Claude judges)

## The objective, and its constraint

**Minimize the Pangram AI score — subject to the gate holding and the anchors
being appropriate to the draft.** The constraint is not decoration. Optimizing
the score alone has a known optimum, and it is not prose you want.

Recorded run (GH-219): a hand-written, twice-hand-edited published article went
from **AI 77.8% to AI 0.0%**, Mixed to Human, all 25 paragraphs "improved". By
the score alone, a total success. What it produced:

| before | after |
|---|---|
| The grouping does two jobs. | Grouping serves two primary purposes. First, … |
| Let the orchestrator run git, not the agents. | Git operations are executed by the orchestrator rather than the agents. |
| One structural detail deserves attention before it becomes a bug. | A specific structural detail must be noted. |

The local register metrics moved the other way in the same run:
`passive_enabling_per_500w` 0.0 → 0.5, `salad_rate_per_100` 5.5 → 8.3,
`opening_diversity` 0.72 → 0.67. Academic passive-voice prose scores zero.

> Pangram scores here were measured on the `default` model, before the client switched to `pangram-4` on 2026-09-01 (GH-406). Compare them with each other, never with a current score; see "Which detector model a score came from" in the writing-voice rule.

Two facts sit behind this. Pangram rated the author's own hand-written prose
77.8% AI, and `filter-tells` catches only 24% of real AI documents (GH-192).
The first was a `default`-model reading. On `pangram-4` 4.1, three of the
author's pre-AI papers read 0.000 AI (GH-406). Those are different texts,
so the 77.8% figure is not refuted, but it may not hold on the current model.
**Neither detector is a reliable proxy for "reads as human" on its own.** The
score is evidence, and a score that falls while the register metrics worsen is
evidence of the wrong thing.

The cause of that run was anchors, not the objective: retrieval was showing the
model IEEE papers for a punchy blog post (GH-216). Fix the anchors and the
objective is reachable without the failure mode — which is why the driver now
reports the anchors it selected, not only the pool it selected them from,
before it starts.

There is deliberately **no automatic quality gate on the Pangram number**. One
run is not a threshold, and inventing one from it would be the overfitting
GH-188 warned about.

A later run measured the same divergence while the score moved a long way
(GH-233). An article fell 58 points, 81.1% to 23.3%, and in the same run
`sentence_length_std` fell 8.9 → 8.3, `dash_density_per_500w` rose 1.4 → 2.0,
`antithesis_pairs` rose 1 → 3, bold lead-ins fell 11 → 8, and ` just ` went
1 → 10. A 58-point improvement is the most persuasive number this pipeline has
produced, and the prose underneath it got worse on five measures at once. Read
the register report beside the score, never instead of it.

The rewriting model is deliberately **not** Claude. filter-tells detects and steers
within the Claude loop (GH-156); this skill hands the rewrite itself to a
different model family so the prose decorrelates from Claude's own lexical
fingerprints, instead of Claude grading its own homework. Claude keeps the
job it is good at: judging whether the result is faithful.

That division is the point. **Verification is not optional** — an 8B model
rewriting technical prose will drop a citation, round a number, or quietly
strengthen a claim. Nothing is spliced into a draft until the gate passes.

## Prerequisites

- A `writing-voice/` directory of exemplars (contract: the repository's
  writing-voice rule; roles `author-voice` / `venue-voice`). Without it this
  skill has no target and should not run — use plain filter-tells instead.
- A reachable Ollama endpoint with the model pulled, at
  `http://localhost:11434` by default.
- For the `--pangram` measurement only, a Pangram API key. It resolves through
  `<agent-dir>/scripts/credentials.py` in order: an explicit `--api-key`, then
  `PANGRAM_API_KEY`, then the nearest `.secrets/keys.json` found by walking up
  from the working directory (contract: the repository's secrets rule). So
  `env | grep -i pangram` coming back empty settles nothing — the file is where
  the key usually lives, and checking the environment first is what makes a
  configured key look missing. Ask the loader instead:
  `python3 <agent-dir>/scripts/credentials.py` reports which services are
  configured, printing names and never values.

**Model choice.** Default `cohere:command-a-03-2025` — the GH-138/142 bake-off
winner: it drives a draft toward human where the gemma family *raises* the
Pangram score, and runs clean through the gate. It needs a Cohere key
(`COHERE_API_KEY`, `COHERE_SECRETS_FILE`, or `cohere` in the repository's
`.secrets/`), sends the paragraph to Cohere's API, and bills per token.
**A keyless machine, or one where the draft must not leave it, sets `--model
gemma4:12b`** (or `MATCH_VOICE_MODEL`) — the local GH-163 winner that runs
anywhere; `gemma4:31b-mlx` reaches the top tier on a 32 GB Apple Silicon box
without egress, `gemma4:31b-cloud` when the memory is not there. There is no
silent fallback: a `cohere:` default with no key stops with remediation. Sizes,
the full ranking, and the Cohere decision are in
[model-choice.md](./references/model-choice.md) and
[cohere-bakeoff.md](../bake-off/references/cohere-bakeoff.md)
(the harness is the `bake-off` skill since GH-205).

Check the endpoint before starting:

```bash
python3 <skill>/scripts/rewrite.py --check --text /dev/null
```

If this fails, **report it and stop**. The skill never falls back to a Claude
rewrite: that would defeat the decorrelation it exists for.

## When not to run it

Two kinds of draft do not benefit, and each costs a whole run to find out.

**Prose already cleaned by hand.** Measured on two articles that had been
through the full filter-tells battery and an editing pass before the run: the
pipeline put back what the cleanup had taken out. ` just ` went 1 → 10 and
1 → 15, ` actually ` 1 → 7 and 0 → 15, bold lead-ins fell 11 → 8, and
`antithesis_pairs` rose 1 → 3 (GH-233). A second model re-emitting finished
prose finds little to repair and adjusts register anyway. The wins this skill
can show were measured on drafts that had not been hand-tightened, and they do
not transfer to prose that has.

**An article about AI writing.** One document did not shift by a point — 8 of 8
segments flagged before and after — through the same run that moved a sibling
article 58 points. Its vocabulary *is* the flagged lexicon: it quotes
"leverage", "robust", "seamless" and "delve", explains burstiness, and carries a
table of AI artifacts. No rewrite reaches that, because the subject matter is
what the detector measures. Expect no movement and spend the scans elsewhere.

## Steering the anchors

The driver reports both the pool and the anchors retrieval actually chose,
**before** rewriting anything:

```
anchors: 52 exemplars available from .../writing-voice
         pool {'author-voice': 24, 'venue-voice': 28}
         selected 15 anchors over 5 of 27 paragraphs
         roles {'author-voice': 11, 'venue-voice': 4}
         top sources Djukic-2009-rrm.md x4, Djukic-2005-lifetime.md x3, ...
```

Read the `selected` block, not the `pool` line. They answer different questions
and only the second one predicts the output: the pool says what retrieval *may*
reach, the selection says what it *chose*. A pool of 22 author-voice against 91
venue-voice looks healthy and still hands a how-to paragraph two IEEE papers out
of three anchors — the GH-215 failure on a corpus assembled to prevent it, which
is why the pool line alone could not catch it (GH-233).

The pre-run block samples the first few paragraphs and says so. For the real
selection over every paragraph, with no model called and no draft written:

```bash
python3 <skill>/scripts/drive.py --article draft.md --dry-run
```

Judge on sources as well as roles. `{'venue-voice': 2, 'author-voice': 1}` reads
balanced while every anchor is a paper.

A flag that filters nothing is reported as inert rather than left to look like a
control — `--stratum pre-ai` on a corpus whose diction-eligible samples are all
pre-AI is a no-op, and following it as the register control produces the
register it was meant to avoid (GH-234, idea-factory#355).

| you want | flags |
|---|---|
| default — nearest passages, author-voice weighted | none |
| diction-safe only (exclude AI-era samples) | `--stratum pre-ai` — inert, and reported as such, when the corpus holds no AI-era diction samples |
| **punch: the pre-AI peer essays** | `--role venue-voice --anchor-tags clipped` |
| **one specific author's voice** | `--author Yegge` — hard pin, not a weight; empty pool if no exemplars carry that author |
| see the real selection before spending tokens | `--dry-run` |
| **register that topic will not find** | `--anchor-tags economics` |
| shape references, deliberately | `--anchor-tags structure-only` |
| a specific corpus | `--voice-dir <path>` |
| no voice steering at all | `--no-anchors` — skips retrieval entirely; contradicts `--role`/`--anchor-tags`/`--stratum` |

The last combination is what a repository README means by "anchor on the Yegge
and Beck samples". `--stratum pre-ai` alone is often not enough: it removes the
AI-era samples, but if the remaining peer essays are not *topically* near the
draft, the academic papers still win on similarity. Forcing the role is how you
say "punch matters more than topic here".

**Tags are the axis similarity cannot reach.** Retrieval matches topic, and the
register that fits an article is often the one least topically similar — on a
113-exemplar corpus, an economics paragraph ranked the Krugman samples no
better than 25th of 2,420. Tags select the pool and similarity ranks within it,
so `--anchor-tags economics` returns Krugman at a *third* the similarity score
of the software essays it displaced. Measured (GH-229): that swap took a
published article from an external score of 100% to 17.9% while holding the
passive rate at the author's own level.

`structure-only` samples are held out of diction anchoring unless you ask for
them by name — they are shape references, and their prose is often the register
you are escaping.

Anchors used per paragraph, with scores, land in `results.json` — so a bad mix
is diagnosable after the fact without re-running retrieval by hand.

## Driver (whole-article orchestration)

`scripts/drive.py` runs the per-paragraph pipeline over a full article and
assembles the gate-passing rewrites into a sibling `<article>.vr-draft.md`:

```bash
python3 <skill>/scripts/drive.py --article <path.md> --model gemma4:31b-cloud
python3 <skill>/scripts/drive.py --article <path.md> --coverage-only   # no model calls
python3 <skill>/scripts/drive.py --article <path.md> --pangram         # + before/after, uploads
```

- **Coverage audit is mandatory output.** Every body line is classified
  (prose / heading / figure / table / code / reference / blockquote / list /
  rule / blank); any unclassifiable line is reported as a WARNING and
  `--coverage-only` exits nonzero. Added after a real question — "did the
  driver skip the first paragraphs?" — that an ad-hoc driver could not answer.
  Run `--coverage-only` first when in doubt; the paragraph map is the answer.
- Retries are failure-classified automatically (copy → anti-copy note,
  number/citation loss → preserve-numbers note, register → banned-vocab note).
- Every pass-1 candidate is critiqued against its original before the gate
  and repaired once on a `repair` verdict (step 2b below); the run report
  prints pass-1 vs pass-2 acceptance.
- The driver applies the MECHANICAL gate only. The emitted draft is a set of
  candidates: run the meaning-entailment review (references/prompts.md) on each
  accepted paragraph, and filter-tells over the assembled file, before treating the
  draft as accepted.
- Kept-original paragraphs are listed with their failure category. A kept
  original is a correct outcome, and the keeps double as an internal control
  in redistribution experiments (the 2026-07 Pangram run: flagged residue
  mapped to the kept paragraphs).
- `--pangram` measures whether the rewrite worked, and is the only way to get
  the comparison — see [Did it work?](#did-it-work-the---pangram-measurement)
  below for what it costs and what it discloses.

## The pipeline (per paragraph)

Paragraph is the unit of work. The skill never restructures across
paragraphs.

**1. Retrieve anchors.**

```bash
python3 <skill>/scripts/retrieve.py --text <paragraph-file> --for <draft> -k 3 --json > anchors.json
python3 <skill>/scripts/retrieve.py --text <paragraph-file> --for <draft> -k 3 > anchors.txt
```

Top-k topically nearest exemplar passages, `author-voice` preferred.
**Retrieval is lexical (tf-idf), so anchors match the author's vocabulary, not
necessarily the paragraph's subject** — a meta-paragraph about fragmented
literatures may pull scheduling papers. That is fine and often correct: the
anchors exist to carry register, not content. Do not treat an off-topic anchor
as a retrieval failure.
Retrieval is the filter-tells `voice_anchors` implementation imported from the
sibling skill — built once, imported twice, so the two skills cannot drift.

**2. Rewrite.**

```bash
python3 <skill>/scripts/rewrite.py --text <paragraph-file> --anchors anchors.txt \
  [--model gemma4:12b] [--endpoint http://localhost:11434] [--temperature 0.7] [--timeout 300]
```

**2b. Critique, then repair once (the driver's default; GH-77).** The
single-shot loop accepted whatever cleared the mechanical gate, and on the
Strategy Theatre run a cold review then threw away 56 of 71 rewrites — term
swaps breaking a referent chain, register smoothed to generic, hypotheticals
made definite, refrains reworded, staged contrasts and banned words. Every
class is detectable against the ORIGINAL before acceptance, so the driver
now critiques pass 1 before gating it:

```bash
python3 <skill>/scripts/critique.py --original <paragraph-file> --candidate <candidate> \
  [--protected-terms draft.protected-terms.txt] [--model gemma4:12b]
```

The verdict is structured, never prose — `{meaning_deltas, term_swaps,
register_drift, banned_words, new_antithesis, new_tricolon,
new_nominalization, new_colon (GH-458),
quoted_span_changes, verdict: accept|repair|reject, source}`. The mechanical
fields are regexes against the original (protected terms lost, filter-tells
banned words introduced, antithesis or tricolon counts that rose, a quoted
span that did not survive); the critic model supplies `meaning_deltas` and
`register_drift`. `repair` sends the paragraph back **once** with the
critique rendered as explicit constraints ("keep the word 'exposure'; do not
replace it with 'justification'"; "the phrase in quotation marks must
survive verbatim"); `reject` keeps the original (`rejected-critique`);
`accept` and an unparseable critic answer both go straight to the gate —
the harness never discards a rewrite silently. Pass 2 is gated, not
critiqued again. `--critic-model` picks the judge (default: the rewrite
model; a second family is better when pulled); `--no-critique` is the old
single-shot path, and an A/B against it is the point of the report line:

```
critique: pass 1 accepted 31, pass 2 accepted 22, repaired 29, rejected 4, unparsed 1 (of 67 critiqued)
```

If pass 2 does not beat pass 1, that is a finding to record against the
prompt ([critique-prompt.md](./references/critique-prompt.md)), not a number
to hide. `results.json` keeps `pass1`, `critique`, `pass2`, and `pass` per
paragraph so survival can be measured after a cold review, and the manifest
records the counts under `critique:`.

**3. Gate — all four checks, fail closed.**

```bash
python3 <skill>/scripts/verify.py --original <paragraph-file> --rewrite <candidate> \
  --anchors-json anchors.json
```

| Check | Who | Fails on |
|---|---|---|
| Citations, numbers, terms | `verify.py` | a key or figure lost, altered, or invented |
| Citation syntax family | `verify.py` | `[@key]` silently rewritten as `\citep{key}` — the key survives but the build breaks |
| Inline markup | `verify.py` | a `**bold**`, `*italic*`, `` `code` ``, or `[link](url)` span count that moves in either direction, or a bold lead-in returned as plain prose — same class as citation syntax. Dropped spans cost a section of lead-ins three of six; added spans were the largest single class of harness reverts (7 of 34), and a link flattened to a bare parenthetical URL was another. Added emphasis is now unwrapped before the gate sees it (GH-240), so this row fires on markup the strip cannot undo |
| Em-dashes | `verify.py` | a dash the original did not have — manufactured punch, measured at 7 → 10 and 7 → 15 across two articles against a house limit of 2.0 per 500 words |
| Anchor similarity | `verify.py` (match-structure shingles) | a long verbatim run copied from an exemplar |
| Introduced inflation | `verify.py` (`inflation_lexicon.txt` beside it; `--inflation-lexicon` overrides) | a booster, stock connective, or buried-verb frame the rewrite introduces and the original does not carry — "Consequently,", "key", "demands the use of". Direction-aware: on an author corpus plainer than the venue floor the transport inflates, and anchor similarity does not measure direction; two 2026-11-17 runs shipped exactly this class (GH-477) |
| Meaning entailment | **Claude**, per references/prompts.md | any claim weakened, added, or re-scoped |
| Register | filter-tells lexical scan on the candidate | banned words — one machine register traded for another |

`verify.py` exits nonzero on violation so the loop can gate on it directly.
It is the *mechanical* half only; a clean exit is necessary, not sufficient —
run the entailment judgment and the filter-tells scan before accepting.

**3b. Two-model mode (optional).** Run the same paragraph and anchors through
both cloud models, gate both candidates, and have the Claude judge pick the
better rewrite (or keep the original if neither is faithful). The pairing that
paid off in evaluation is `gemma4:31b-cloud` + `kimi-k2.6:cloud`: when they
disagree about whether a sentence needs changing at all, the more conservative
answer is usually right.

**4. Splice or keep.** On a clean gate, accept. Otherwise retry with a
failure-specific note (`--retry-note`, table in references/prompts.md) up to
N times (default 2), then **keep the original paragraph and record why**. A
kept original is a correct outcome; expect a meaningful reject rate from an 8B
model and do not assume success.

**5. Report.** A per-paragraph table: accepted / retried / kept-original, with
gate failures by category. Rewrites are proposed as a diff for review by
default; applying them directly is opt-in.

## Protected terms and canonical blocks

Two guards the per-paragraph gate cannot express on its own, because both
are properties of the article (GH-77).

**Protected terms** are the article's referent chain: words and phrases that
recur in three or more paragraphs **and that this article leans on harder than
ordinary prose does**, plus any sentence repeated verbatim across paragraphs
(a refrain). The largest failure class in the GH-189 measured run
was a term-of-art swap — exposure → justification, decision plane →
decision, detector → tool — that passed every per-paragraph check because
the chain it broke ran across paragraphs. On the first run the driver derives
the list to `<stem>.protected-terms.txt` beside the article and says so; on
every later run it reads that file and never overwrites it, so it is yours to
edit — one term per line, `#` comments. The rewrite model receives the terms
the current paragraph carries as a keep-verbatim rule, `verify.py` rejects a
candidate that loses one (`protected-term`, fatal), and the retry note names
the lost terms. `--protected-terms FILE` points at another list;
`--no-protected-terms` turns the guard off. The manifest records the path,
the count, and whether this run derived it.

```bash
python3 <skill>/scripts/protected_terms.py draft.md          # show what would be derived
python3 <skill>/scripts/protected_terms.py draft.md --write  # write it if absent
```

### Added emphasis is unwrapped, not rejected (GH-240)

Rule 3 of the rewrite prompt used to state the markup contract in the preserve
direction only — keep every bold span, and if the paragraph opens on a bold
lead-in your rewrite does too — without ever forbidding the model from adding
one. It described the pattern and omitted the prohibition. Over 16 measured
candidates on paragraphs carrying no bold at all, **9 came back with exactly
one bold span wrapping the opening sentence**, and `verify.py` killed every one
as fatal. The same defect is on record for a different model family (GH-156,
gemma), which puts it in the prompt rather than any one model.

Two halves to the fix. Rule 3 now states the negative, in the shape rule 7
already used for em-dashes. And `rewrite.strip_added_emphasis(original,
candidate)` unwraps emphasis the original did not have, before the gate runs:
a candidate whose only defect is a wrapper around its first sentence is
otherwise shippable. The strip runs one way only — a paragraph that already
carries bold or italic keeps it, nothing removes a span the original had, and
code spans are never touched.

### Distinctiveness, and why recurrence alone was not enough (GH-239)

Recurrence cannot tell a term of art from a common verb. On a 48-paragraph
article the recurrence rule derived 142 terms, **128 of them ordinary words**
— `means`, `read`, `record`, `name`, `leave`, `look`, `wrong` — and since a
lost protected term is fatal, no paraphrase could pass the gate at all. Two
passes over eleven paragraphs accepted three candidates between them; the
gate was defending the word "means" while the backticked identifiers it was
supposed to be guarding came back untouched every time.

So a candidate term now also has to be *distinctive*: its paragraph share in
this article at least `MIN_OVERREP` (0.7) times its document share across the
voice corpus, which the driver already has open. A term the corpus has never
seen is kept outright. Spelled numbers are dropped, since `verify.py` runs a
`numbers` check over them and protecting them too meant a rewrite that
rendered a count differently took two fatals for one thing. Refrains skip the
test — a sentence repeated verbatim is a chain whatever its words are.

Measured on that article: 142 terms → 44, every common-word false positive
gone and no real term of art lost (`touchpoint` 17.5x, `constitution` 13.1x,
`validator` 13.1x, against `find` 0.1x, `look` 0.1x, `means` 0.0x). Over the
16 saved candidates from those two passes, this fix plus GH-240 took the gate
from 4 candidates passing to 10, and every remaining rejection is a real
defect — a manufactured em-dash, an invented quoted span, six lost citation
numbers.

Residue worth knowing: rare inflected verbs (`lacking`, `enumerates`,
`validates`) still clear the test, because the corpus happens not to use them
much. Three of 44 is a list a person can read, which is the point — the file
stays hand-editable.

Without a corpus the test cannot run and derivation falls back to recurrence
alone. The run says which happened.

**Canonical blocks** are pasted, not written — an AI-disclosure line, a
subscribe line, a "Start Here" pointer — and are never sent to the model.
They are not span-locked because they are inserted at paste time, so the
registry lives beside the corpus at `writing-voice/canonical-blocks.txt`
(found by walking up from the article) or is passed with
`--canonical-blocks FILE`. One pattern per line: a plain case-insensitive
substring, or `re:<regex>`. Matching paragraphs get status `canonical`,
stay verbatim in the draft, and are counted in the manifest.

## Configuration

| Setting | Flag | Default |
|---|---|---|
| Endpoint | `--endpoint` / `OLLAMA_ENDPOINT` | `http://localhost:11434` |
| `OLLAMA_WAIT_SERVER` | seconds to wait for a mid-run Ollama restart (default 0) | set 600 for unattended batches — a supervised local server can be reaped mid-run and the retry backoff alone cannot ride out its restart (GH-173) |
| `OLLAMA_THINK` | Ollama `think` field for every driver: `false` / `true`, unset sends none (default unset) | set `false` for a local reasoning model whose reasoning lands in the answer — `ornith-1.5:35b` opened every rewrite with "The user wants me to..." until it was (GH-409). A stage that passes `think=` itself keeps its own value; `--check` reports the setting |
| Model | `--model` / `MATCH_VOICE_MODEL` | `cohere:command-a-03-2025` (local fallback `gemma4:12b`) |
| Temperature | `--temperature` | 0.7 |
| Timeout (s) | `--timeout` / `MATCH_VOICE_TIMEOUT` | 300 (cold loads are slow) |
| Live Cohere contract smoke | `COHERE_LIVE_TESTS=1` | off: the offline suite and the release gate never call Cohere; set it to run `testdata/test_cohere_contract.py`'s live tests (GH-447) |
| Concurrent paragraphs | `--jobs` / `MATCH_VOICE_JOBS` | 4; 1 is sequential. Each call still carries one paragraph, and the draft does not depend on it (GH-433) |
| Anchors per paragraph | `-k` | 3 |
| Max copied run (words) | `--max-shared-run` | 8 |
| Standing style directive | `--style-note` | off |
| Paragraph selection | `--paragraphs` | all rewritable paragraphs |
| Protected terms | `--protected-terms` / `--no-protected-terms` | `<stem>.protected-terms.txt`, derived on first run |
| Canonical blocks | `--canonical-blocks` | `writing-voice/canonical-blocks.txt` by walk-up |
| Critic model | `--critic-model` / `--no-critique` | the rewrite model; critique on |
| External check | `--pangram` | off (the flag is the consent) |

### Cohere backend (opt-in)

A `cohere:` model id routes to Cohere's hosted v2 `/chat` API instead of
Ollama — for example `--model cohere:command-a-03-2025`. It is additive: the
Ollama path stays the default, and nothing routes to Cohere unless the model id
asks for it. Because the transport lives in `generate()`, the same prefix works
from `drive.py`, filter-tells, and burstiness — no stage grows its own client.

- **Reasoning variants are allowed; do not starve the thinking budget.**
  Cohere returns reasoning in its own `type: "thinking"` content block, and the
  backend reads blocks by type, so a scratchpad cannot reach the prose whatever
  the model is called (GH-154). The refusals this replaces — a `"reasoning"`
  name substring and a denylist naming `command-a-plus` — rested on the opposite
  belief and are gone (GH-155). What does put a scratchpad in the answer is a
  thinking budget too small to finish inside: `token_budget: 1` produced a
  2-character thinking block and a 6590-character answer opening
  `<EOS_TOKEN>We need to rewrite the passage:`. The default sends no `thinking`
  field, and a configured `COHERE_THINKING_BUDGET` is clamped up to
  `COHERE_MIN_THINKING_BUDGET`. Output is still sanitized of stray
  instruction-echo lines as defense in depth.
- **`COHERE_THINKING=disabled` is opt-in and usually wrong.** Disabling thinking
  on a reasoning model gives a deterministic 422 `INVALID_TOOL_GENERATION` on a
  prompt the size of match-voice's (7/7 measured; 4/4 clean on a short prompt).
  That 422 is not retried — it fails identically every time — and `check_server`
  warns when the variable is set.
- **Its critic defaults to the rewrite model.** GH-140 had forced a gemma
  critic because Cohere critiqued itself into unparsable verdicts (GH-138: 9 of
  24); retested on the corrected pipeline, 12/12 parse (GH-181), so the
  pre-GH-140 default is restored and a pure-Cohere run needs no Ollama at all.
  `--critic-model` / `COHERE_CRITIC_MODEL` still override.
  Transient API errors (429/5xx/timeout, and 422s other
  than `INVALID_TOOL_GENERATION`) are retried (`COHERE_MAX_RETRIES`, default 3).
- **Key** comes from `COHERE_API_KEY`, then the JSON file named by
  `COHERE_SECRETS_FILE` (key `cohere`), then service `cohere` in the
  `.secrets/` directory found by walking up from the working directory
  (the secrets rule; GH-429). Never hardcoded, never committed. The
  no-Claude-fallback contract holds: a missing key or an unreachable endpoint
  stops the run, it does not silently fall back.
- **It is a hosted API**, so the paragraph text leaves the machine (as the
  `:cloud` Ollama models already do) and billing is per token. Whether Cohere
  should be a *default* anywhere is gated on the bake-off (GH-138); this is the
  backend it runs through.

`--style-note "active voice, plain diction"` sends a standing directive to
the rewrite model on every attempt, first included; retries append their
failure-classified note after it. Use it when a run's register drifts in a
known direction — the measured case is gpt-oss `--no-anchors` doubling the
passive rate — and you want to push back without anchors. Recorded in the
provenance YAML as `style_note`.

`--paragraphs "3,7,12-15"` restricts the rewrite to the listed 1-based
paragraph indices; everything else passes through untouched (status
`unselected`). This is the second-pass workflow: a `--pangram` run ends its
still-flagged worklist with a ready-to-paste `next pass: --paragraphs "..."`
line, so the paragraphs that stayed flagged can be re-rolled without spending
model calls on — or risking regressions in — the ones that already cleared.
An invalid selection (malformed, out of range) exits 2 before any scan or
model call. The selection is recorded in the provenance YAML.

**Readability guard.** After the register-markers comparison (the `--pangram`
path), the run prints one WARN line per metric whose relative increase
crosses its ceiling — passive +50%, nominalization +25%, filler +50% on the
per-1,000-word rates — or `readability guard: clean`. Advisory only: the
gate governs fidelity and nothing hard-fails on style drift, but a doubling
passive rate should not look like a 0.1 uptick. Triggered warnings are
recorded in the provenance YAML under `guard:`.

## Did it work? (the --pangram measurement)

Who writes the words is the biggest single lever on the score — the
2026-07-26 evidence is in
[references/authorship-lever.md](./references/authorship-lever.md),
re-homed from write-article (GH-214).

The gate holds **double-quoted spans verbatim** (GH-223): a span lost,
altered, or invented is fatal — tighten paraphrased documentation quotes
inside quotation marks on the same paragraphs two runs straight before
this check existed. Scare-quoted single words (under 4 chars) stay out
of scope.

The gate also rejects **introduced first person** (GH-221): a candidate
carrying I/we/my/our where the original paragraph has none is refused —
an anchored seed imports the anchor author's register, and the measured
worst case put invented claims in the author's mouth ("I might not
understand, being too thick-skulled...", the-qwerty-endpoint,
2026-09-01). An original with any first person keeps the check silent.

The gate proves a candidate preserved citations, numbers, and meaning. It
cannot tell you whether the prose stopped reading as machine-written, and
filter-tells cannot settle that either — its detectors are the denylist the
rewrite was steering around, so their silence is close to tautological. An
external detector answers from outside, and the driver runs it:

```bash
python3 <skill>/scripts/drive.py --article draft.md --pangram
```

It scans the article before touching a paragraph, scans the assembled draft at
the end, and reports `fraction_ai` before → after with the paragraphs that
moved. That ordering is why the measurement lives in the driver rather than in
a procedure to follow afterwards: **the baseline cannot be reconstructed once
the paragraphs are replaced**, so a run started without the flag has
nothing to compare against later. Decide before the run, not after reading the
draft.

**Passing the flag is the consent**, and it is asked for per document. The
scan uploads the article and the draft to a third party that retains both —
the opposite of the local-first reason this skill exists — so the driver never
uploads on its own, not even with a key sitting in the environment. See the
upload rule in the `writing-voice/` directory rule before answering. A full
comparison costs two scans. How much of an allowance that spends depends on the
account, and nothing here enforces a ceiling: run `pangram.py --check` first,
which confirms the key and the endpoint and spends nothing, and read the
account's own answer from the API — 402 for exhausted credits, 429 for too many
requests. Do not plan a session around a remembered daily number.

**It measures prose only.** Both scans submit the payload the shared extractor
builds, with front matter, tables, and code fences dropped — the text a rewrite
can change. Scanning the whole file by hand includes that machinery
and returns a different number, and the difference is not the rewrite. Two
readings of one document are comparable only when both cover the same text, so
the run manifest records `scope: prose-only` beside the pair.

Without the flag, or without a key, the driver runs unchanged and says the
check was skipped. That is the normal state, not a degraded one; if the
baseline scan fails the second one is not spent either.

The still-flagged paragraph list is the useful output: the worklist for
another pass, pointing at the passages the rewrite did not fix. Read it as
evidence and not a verdict — filter-tells's Verdict Validity Rules apply here
too, and a favourable number certifies nothing on its own.

The two scripts underneath, `<agent-dir>/scripts/pangram.py` and
`pangram_report.py`, sit at the shared scripts root. filter-tells invokes the
same pair for a point-in-time reading; neither skill owns them.

## The burstiness pass (`burstiness.py`)

A second entry point that shares this skill's transport and its gate, and
changes something else entirely: sentence-length variance, measured as the
coefficient of variation of sentence lengths. It is the second of the two
editable features a plain stylometric detector keys on. filter-tells attacks
the first, AI-phrase density; nothing attacked this one.

```bash
$RUN <skill>/scripts/burstiness.py --article draft.md            # arm B
$RUN <skill>/scripts/burstiness.py --article draft.md --control  # arm C
$RUN <skill>/scripts/burstiness.py --article draft.md --dry-run  # no model call
```

Measured across three documents, three arms each, prose-only on Pangram
3.3.2 (GH-129; full report in
[references/burstiness-validation.md](./references/burstiness-validation.md)):

| document | arm B | arm C (control) |
|---|---|---|
| gain article, original state (0.445 baseline) | **0.259** | 0.436 |
| gain article, pipeline state (0.381 baseline) | **0.291** | 0.411 |
| raw-ish fresh draft (0.744 baseline) | **0.324** | 1.000 |
| raw draft at the ceiling (1.000 baseline) | 1.000 | 1.000 |

CV rose in arm B and held in arm C on every document. Two patterns worth
knowing before running it: a saturated baseline has no room to fall, so the
pass does nothing measurable on a raw 100% draft — run it on documents
already through the chain; and the control's own effect sorts by input,
near-null on pipeline-state prose and harmful on raw prose, so the
attribution only reads cleanly where the pass belongs anyway.

**`--control` is not an option, it is the method.** Arm C is what licenses the
claim that the drop is burstiness rather than a second model's diction; run it
alongside arm B on every new draft, or the comparison attributes nothing. When
the control moves CV by more than 0.02 the report says so, because a control
that reshapes rhythm has stopped being one.

What the gate refuses, in order: an empty response, a candidate outside the
0.5x-1.6x word band (grown means content added, shrunk means summarised), a
lost `[[LOCK-n]]` anchor token, an added defect class, and any fatal finding
from `verify.py` — citations, numbers, markup, terms of art. A rejected
paragraph keeps its original text and the report names the reason. Nothing is
repaired.

The banned constructions are checked as a **delta**, never a level: the pass
may not introduce a tricolon, an "X, not Y", or an em-dash, and it also has no
business removing the author's own. Em-dashes are normalized to the sentence
break they were imitating before the gate runs, since that is the edit the
pass wanted anyway.

**Placement (GH-133, decided 2026-08-28):** a standalone pre-terminal pass in
this skill, run inside the GH-57 cycle like every other generative stage —
optional, author-in-the-loop, its regressions caught by the caller's review
phase and the author's picks downstream (GH-208). The filter-tells-sub-check half of the question
resolved by function: the *measurement* is a filter-tells/humanize report line
and a match-structure subcommand (GH-130), and the *generation* cannot live in
filter-tells at all, because filter-tells is Claude-side detection and prose
generation is cross-family by the pipeline's own rule. Locked spans are
excised before the model sees a paragraph and spliced back byte-identical, and
the written file is re-checked against the manifest before the run reports
success. The author read arm B on both informative documents and signed it
(GH-132) — with the note that the gate cannot see reattributed judgment
("He called the request very dumb" returning as "It was very dumb"), which is
one more reason the caller's review phase downstream is not optional.

Measure the effect with match-structure:

```bash
$RUN <match-structure>/scripts/style.py burstiness draft-bursty.md \
  --baseline draft.md --text
```

Standing caveat: 0.259 is "Mixed", not "Human", and the venue's detector is not
Pangram. The score is a proxy. The durable reason to want burstiness is that
prose which alternates long and short reads better, so do not tune past what
the author's ear approves.

## Relationship to the other prose skills

- **filter-tells** detects the tells and, with `writing-voice/`, steers its own
  rewrites toward the same anchors. Use filter-tells when Claude should do the
  rewriting; use this skill when you want a different model's prose.
- **match-structure** owns voice profiling and the similarity guard this skill
  reuses for the copy check, and the `burstiness` subcommand that measures what
  the burstiness pass moves.
- Run filter-tells over the finished draft afterward regardless — a local model's
  output is not exempt from the tells.

## Dependencies

The pixi environment (PyYAML) plus a reachable Ollama. Retrieval and the
similarity guard import their implementations from the sibling filter-tells and
match-structure skills, which every agent surface carries.
