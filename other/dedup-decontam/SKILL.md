---
name: dedup-decontam
description: "Deduplicate and decontaminate text corpora for LLM training: MinHash/LSH near-duplicate detection, n-gram and embedding-based decontamination, planted-item tests with pass/fail criteria. Use when preparing a training or evaluation dataset and you must remove duplicates and test-set leakage; not for single-document similarity."
compatibility: Python 3.10+, numpy optional; verified 2026-10-14
license: MIT
---
# Dedup and Decontamination

Trigger: prepare a text corpus for LLM training or evaluation and you must
remove duplicates and prevent test-set leakage.

## Procedure (numbered — follow in order)
1. **Normalize** — lowercase, collapse whitespace, strip BOM/zero-width chars,
   canonicalize URLs. Hash the normalized bytes for exact dedup first. One
   shared normalizer (`scripts/normalize.py`) for every comparison.
2. **Exact dedup** — keep the first occurrence of each SHA-256; log duplicates.
3. **Near-dedup with MinHash/LSH** — tokenize into shingles (default 5-gram),
   compute k=128 MinHash signatures, band into b bands of r rows, hash each band
   into buckets, compare only bucket-mates with Jaccard. Threshold ~0.8 by default.
4. **n-gram decontamination** — for each test prompt, slide an n-gram window
   (default 13 for common benchmarks) over the corpus; any exact n-gram match
   is leakage. Mark the document, do not silently drop.
5. **Embedding decontamination** — embed documents and test prompts with the same
   model, compute cosine similarity; flag pairs above the pinned threshold
   (default 0.92). Re-tune per model; never hardcode the threshold in logic.
6. **Planted-item tests** — before shipping, plant 5 known duplicates and 5
   near-duplicates; the pipeline must find 5/5 exact and >=4/5 near. If it fails,
   the detector is broken.
7. **Report** — emit a JSON manifest: kept/dropped/flagged counts, per-item
   reason, and the planted-item pass/fail.

## Decision tables
- **Jaccard threshold**: 0.95 -> near-identical; 0.8 -> loose; 0.5 -> LSH tuning.
- **LSH bands/rows**: the LSH threshold is t ~= (1/b)^(1/r) with b*r = k. For
  k=128 the only *achievable* thresholds are (b=128,r=1)=0.008, (b=64,r=2)=0.125,
  (b=32,r=4)=0.420, (b=16,r=8)=0.707, (b=8,r=16)=0.878. Values such as 0.85,
  0.94 or 0.95 are **not reachable** with any factorisation of 128 -- the old
  table claimed (b=8,r=16) gave 0.94, which is false (it gives 0.878). To hit
  0.94 use k=256 (b=8, r=32 -> 0.937) or k=512 (b=8, r=64 -> 0.966). Pick by
  the target threshold, not by speed; `bands_for()` WARNs when the target is
  unreachable. Override with `--bands`/`--rows` (must multiply to k).
- **n-gram size**: 13 for MMLU-style; 8 for code; 5 for prose.
- **Embedding threshold**: 0.92 cosine for all-MiniLM-L6-v2; lower = noisier,
  higher = misses. Model-dependent — calibrate on a held-out clean set.
- **Embedding action**: above threshold -> flag for review; never auto-drop.

## Near-miss triggers (stop and re-check before proceeding)
- Two documents that differ only in BOM/zero-width/case are reported as distinct
  -> the normalizer is applied after hashing instead of before; fix the pipeline order.
- k < 64 -> MinHash estimate is unstable; the planted-item test will fail.
- n-gram decontamination uses raw chars while the benchmark is BPE-tokenized ->
  you will miss real leakage and over-report false positives; match the tokenization.
- `ngram_decontam.py` shipped its own private `normalize()` alongside the import from `normalize.py` -> the pipeline had two normalizers that could drift apart, so exact-dedup hashes one canonical form while n-gram scanning uses another. The private copy is deleted; `ngram_decontam.normalize` is now `normalize.normalize`, a single source of truth.
- Planted-item test passes while real duplicates are missed -> LSH bands/rows are
  tuned wrong; re-run with explicit `--bands`/`--rows` for the target threshold.
- Embedding threshold copied from another model's blog post -> it does not transfer;
  calibrate on a held-out clean set for this model.

## Pitfalls from research
- P1: MinHash with too few permutations (k<16) gives unstable estimates; use >=64.
- P2: LSH banding with wrong b/r silently misses similarities below the threshold;
  always validate with planted items.
- P3: Normalization differences (whitespace, case) create false negatives; normalize
  before any comparison.
- P4: n-gram decontamination on raw text misses tokenized matches; decontaminate on
  the same tokenization the benchmark uses.
- P5: Dropping all flagged documents without review destroys corpus size; flag first,
  drop only confirmed leakage.
- P6: Embedding similarity is model-dependent; a threshold tuned on one embedding
  model does not transfer. Re-tune per model.

## Verification checklist
- [ ] Planted-item test passes: 5/5 exact, >=4/5 near.
- [ ] k >= 64, seed pinned and logged.
- [ ] Normalization is deterministic and documented.
- [ ] Every dropped item has a reason in the manifest.
- [ ] n-gram size matches the benchmark's tokenization.
- [ ] There is exactly one normalizer in the pipeline (`normalize.normalize`); no script defines its own.
- [ ] Embedding threshold is pinned per model, not hardcoded in logic.
- [ ] Embedding threshold calibrated on a held-out clean set with `scripts/embed_decontam.py --calibrate-out`; the pin is re-derived on every model change.

## Worked examples

### Good — near-duplicate pair kept, exact dropped
Corpus: 100k docs. Pair A/B differ in 2 of 5 words and share a 64-gram
signature at band 14. Threshold table says `jaccard >= 0.95` => drop one.

1. Normalize both (lowercase, strip punctuation, split on whitespace).
2. MinHash 128 bands, LSH query returns A as a candidate for B.
3. Exact check: 5/5 6-grams match => exact duplicate, drop B, record reason.
4. Near check: jaccard 0.96 on 6-grams => above threshold, drop B.

Result: one canonical copy, every drop recorded with a reason.

### Bad — threshold set to "whatever makes the test pass"
Setting `jaccard_threshold = 0.5` to keep more items.

Why it fails: at 0.5 the decontamination is decorative — the benchmark's
planted items are still present in the output. The planted-item test
(5 exact + 5 near) exists precisely to catch this: it would fail 5/5 near.

### Bad — embedding threshold pinned to a model version
`EMBED_THRESHOLD = 0.85` hardcoded for `text-embedding-3-large`.

Why it fails: the threshold moves with the model. Pin it per model in the
config and re-derive it on every model change; the script reads the pin,
never a constant.
## Related skills
- [verifiable-environments](../verifiable-environments/SKILL.md) — the planted-item test pattern in this skill is the same shape as a bypass-register check.
- [skill-authoring-evals](../skill-authoring-evals/SKILL.md) — the corpus and the eval set are both data; author the evals that measure this skill with the meta-skill, and record the with_skill/without_skill baseline.

## References
- procedures: references/procedures.md
- planted-item tests: references/planted-item-tests.md
- DESIGN: references/DESIGN.md
- EVALS: references/EVALS.md
- SOURCES: references/SOURCES.md
