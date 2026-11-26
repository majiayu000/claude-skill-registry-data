---
name: match-structure
description: >-
  Paragraph and sentence-level style metrics for a research corpus.
  Computes quantitative profiles (sentence/paragraph distributions,
  burstiness as coefficient of variation of sentence length, passive
  voice, hedging, word/phrase/idiom frequencies, per-section
  metrics), corpus aggregation, term over/underuse comparison, and a
  plagiarism similarity guard (n-gram shingling with baseline exclusion).
  Provides voice anchor retrieval from writing-voice exemplars via tf-idf.
  The section-level driver (compare, blueprint, rewrite) moved to
  match-outline. Triggers: style profile, quantitative metrics, sentence
  stats, frequency tables, plagiarism check, similarity check, voice
  anchors, corpus profile, word frequency, burstiness, sentence length
  variance.
---

*Split from the original match-structure (GH-291, 2026-07): the
section-level driver (compare, blueprint extraction, section-by-section
rewrite) moved to `match-outline`. This skill retains the quantitative
metrics engine, corpus aggregation, frequency analysis, and the similarity
guard that other prose skills import.*

# Match structure (paragraph/sentence-level metrics)

This skill provides the quantitative style measurement layer that other
prose skills depend on. It profiles markdown papers at the sentence and
paragraph level — distributions, passive voice, hedging, citation density,
word and phrase frequencies, stock idiom usage — and aggregates those into
a corpus profile. It also provides the similarity plagiarism guard used by
`match-outline`'s rewrite mode and `match-voice`'s verify step.

## Where things live

- **Corpus:** `<db-dir>/papers/*.md` — the markdown conversions fetched by
  `update-references`, selected via entries in `references.yaml`. Default
  selection is entries with `status: summarized`; pass `--all` to `style.py
  corpus` to include every entry with an `md_path`.
- **Quantitative profile:** `<db-dir>/voice-profile.json`, written by
  `style.py corpus`. Regenerate only when the corpus changes.
- **Voice anchors:** passage-level tf-idf retrieval from `writing-voice/`
  exemplars, via `voice_anchors.py`.
- **Venue profiles:** `writing-voice/venues/<name>.yaml` — per-venue parameter
  bundles (anchor query, blueprint, targets, tell lexicon, gates) consumed by
  humanize/filter-tells/tighten-style. Schema in the `writing-voice` repository
  rule; loader/validator is `venue_profile.py`.

## Running the scripts

```bash
RUN="pixi run --manifest-path <skill>/../../pixi.toml python"
```

## style.py subcommands

```bash
$RUN <skill>/scripts/style.py --db <db-path> profile <paper.md>   # one paper, full JSON
$RUN <skill>/scripts/style.py --db <db-path> corpus                # aggregate, write voice-profile.json
$RUN <skill>/scripts/style.py --db <db-path> compare <draft.md>    # metric deltas vs corpus
$RUN <skill>/scripts/style.py freq <paper.md>                      # frequency tables only
$RUN <skill>/scripts/style.py similarity <file> --against <sources> [--baseline <draft>]
$RUN <skill>/scripts/style.py burstiness <draft.md> [--baseline <before.md>] [--per-paragraph] [--text]
```

### `burstiness` — sentence-length dispersion

`profile` already carries every burstiness field; `burstiness` is the compact
view of the same numbers, for the places a report wants one line rather than a
page of JSON. It prints sentence count, mean, stdev, CV, min, max, median,
p10, p90, and a word-length histogram.

CV — stdev over mean — is the scale-free form, and the one to quote. Stdev
alone conflates dispersion with register: a paper averaging 28-word sentences
carries a larger stdev than a newsletter averaging 14 without being any less
uniform. The percentiles and the histogram say *where* the variance sits,
which is what a rewrite pass needs, since a document can hit a CV target by
growing one 60-word sentence and that is not the same prose as one that
alternates.

`--baseline <before.md>` adds a `delta` block over every scalar, which is the
before/after column in the humanize report. `--per-paragraph` adds a row per
multi-sentence paragraph so a rewrite can find the flat stretches instead of
reshaping prose that already varies. `--text` renders one line per document
instead of JSON.

Which fields aggregate: `sentence_length_cv`, `_median`, `_p10`, and `_p90`
are in `METRIC_KEYS`, so they appear in corpus profiles, `compare` deltas, and
venue `targets`. Min and max are not — a sample's extrema move with sample
size rather than with style, and averaging them across a corpus produces a
number that means nothing. The histogram is a dict and does not average at
all.

filter-tells reports its own `sentence_length_cv` in the structural scan. It
runs slightly lower than this one, because that script drops sentence
fragments under four words and those are exactly the ones that widen the
spread. For a before/after comparison, keep both sides on one tool.

## voice_anchors.py subcommands

```bash
$RUN <skill>/scripts/voice_anchors.py discover <file>
$RUN <skill>/scripts/voice_anchors.py profile [--voice-dir D | --for file] [--force]
$RUN <skill>/scripts/voice_anchors.py anchors --text <file>|- [--for file] [-k N] [--role R]
```

## venue_profile.py subcommands

```bash
$RUN <skill>/scripts/venue_profile.py discover <file>            # find venues/ via walk-up
$RUN <skill>/scripts/venue_profile.py list --for <file>          # available venue names
$RUN <skill>/scripts/venue_profile.py show --venue N --for <file> # validated profile JSON
$RUN <skill>/scripts/venue_profile.py validate <profile.yaml>
$RUN <skill>/scripts/venue_profile.py bootstrap --voice-dir D --tags a,b [--role R] [--stratum pre-ai]
$RUN <skill>/scripts/venue_profile.py bootstrap --voice-dir D --tags a,b --venue N --write
$RUN <skill>/scripts/venue_profile.py set-anchors --venue N --voice-dir D --arm "tags~clipped" [--composite X]
```

Python consumers import `venue_profile.resolve(start_path=..., venue=...)`,
which raises on schema errors — a broken profile is refused, never partially
applied.

`bootstrap` (GH-339) measures a corpus slice — a manifest query
(role/tags/stratum) or an explicit `--files` list — with the same metric
engine as `style.py corpus`, and emits the profile's
`targets`/`targets_std`/`targets_provenance` block; `--write` merges it into
an existing `venues/<name>.yaml` (author the profile first). Profiles are
measured, never hand-written. `set-anchors` records an anchor query into a
profile with provenance — from tune-anchors arm expressions (repeatable
`--arm`, parsed by tune-anchors' own parser so the syntax cannot drift) or
from explicit `--role/--tags/--stratum/--author` flags.

## Consumers

- **match-outline** — imports `style` for corpus selection, the similarity
  guard, and the `CITATION_RE` pattern. Uses `gpt-oss:120b-cloud` via
  Ollama for whole-document structural rewriting.
- **match-voice** — imports `style.similarity_report` for the rewrite
  verification gate; imports `voice_anchors` for anchor retrieval.
- **filter-tells** — consumes `voice-profile.json` as a detector input
  (`--voice-profile=<path>`); uses `voice_anchors.py` for anchor retrieval
  and baseline profiling.
- **tighten-style** — imports `style` for nominalization density metrics.
- **tune-anchors** — imports `voice_anchors` for the anchor tuning workflow.

## Dependencies

`style.py` is stdlib-only except PyYAML. `voice_anchors.py` uses PyYAML.
No model calls — this is the deterministic half of the analysis pipeline.
