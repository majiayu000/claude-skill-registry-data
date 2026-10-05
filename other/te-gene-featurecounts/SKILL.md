---
name: te-gene-featurecounts
description: >-
  Use when you have nf-core/rnaseq star_salmon BAMs and a pre-built TE SAF,
  and need gene + TE subfamily count matrices. Env-locked featureCounts
  driver: integer Random-One TE counting, row-bound with gene counts. For
  STAR alignment use star-te-preprocessing. For the TE SAF use
  te-reference-saf-build. For annotation use annotate-bulk-rnaseq-data.
license: MIT
---

# TE + Gene featureCounts Counting (env-locked, packaged)

## Overview

This skill is the **self-contained, runnable** step that turns nf-core/rnaseq STAR
`star_salmon` BAMs into **gene + TE subfamily count matrices**, crystallized with its own
minimal, version-pinned Docker container (`te-fc:2.0.2`, featureCounts v2.0.2). It vendors
the two-pass featureCounts driver (frozen copies) and a parameterized Docker wrapper that
handles the proven symlink-staging + identical-path bind-mount pattern. Unlike
`star-te-preprocessing` (which owns the alignment + counting *contract* and the canonical
STAR string), this skill owns the **executable counting artifact**: the locked image, the
driver, the wrapper, and the QC gate the matrices must pass.

**When to use this skill:**
- You have nf-core/rnaseq `star_salmon` BAMs (full or lean `markdup.sorted.bam`) and a
  pre-built grouped TE SAF, and need gene + TE subfamily count matrices.
- You want a reproducible, env-locked counting run (pinned featureCounts v2.0.2).
- You need the exact Docker staging recipe so `bam_fin` symlinks resolve and column names
  come out clean.

**When NOT to use this skill:**
- Building the TE SAF → `te-reference-saf-build`.
- Running STAR / producing the Random-One BAMs → `star-te-preprocessing`.
- Annotating / DGEList / DE on the matrices → `annotate-bulk-rnaseq-data`.
- Locus-level TE quantification → SQuIRE / Telescope (out of scope).

---

## Decision Tree

```
Have star_salmon BAMs + a grouped TE SAF, need count matrices?
│
├─ Want integer subfamily-level TE + gene counts, reproducibly?
│     →  THIS skill: run scripts/run_te_counting.sh in te-fc:2.0.2
│
├─ Need to build the TE SAF first?            →  te-reference-saf-build
├─ Need to produce the Random-One BAMs first? →  star-te-preprocessing
├─ Want fractional 1/n ("Strategy B")?        →  Equally accurate (Teissandier), non-default. STAR --outSAMmultNmax 100 + featureCounts -M --fraction → non-integer → limma-voom/round. Default = integer Random-One.
├─ Want locus-level / copy-resolved TE?       →  SQuIRE / Telescope (out of scope)
└─ Already have matrices, want annotation/DE? →  annotate-bulk-rnaseq-data
```

---

## The locked-env contract

- **Image:** `te-fc:2.0.2` — minimal Debian-slim + **only** featureCounts **v2.0.2**
  (subread). No R, no Python. Built from `env/Dockerfile` via `env/build.sh`.
- **Why v2.0.2 from the official binary:** v2.0.2 is the exact version the in-house production
  runs used (verified from raw headers `# Program:featureCounts v2.0.2`). bioconda **skipped**
  packaging subread 2.0.2 (it jumps 2.0.1 → 2.0.3), so the pin is satisfied by installing the
  official subread-2.0.2 Linux release binary (the same standalone binary the precedent image
  `scdock-r-dev:v0.2` shipped). Build fails closed if the banner is not `v2.0.2`.
- **Image lineage:** legacy `scdock-r-dev:v0.2` also has v2.0.2 (the original runs). The newer
  `scdock-r-dev:v0.5.x` images do **NOT** contain featureCounts (only MultiQC's parser). Use
  the locked `te-fc:2.0.2` for all new runs.

```bash
# Build the locked image (idempotent; aborts if < 5G free on /):
bash env/build.sh
docker run --rm te-fc:2.0.2 featureCounts -v   # -> featureCounts v2.0.2
```

---

## Quick Start

```bash
# One command does staging + identical-path mount + both passes + combined matrix,
# all inside te-fc:2.0.2:
scripts/run_te_counting.sh \
  --bam-dir   /data2/nf-results/<proj>/results_mm39_TE/star_salmon \
  --bam-glob  '*.markdup.sorted.bam' \          # lean nf-core run; default '*.bam'
  --gene-gtf  <outdir>/genome/gencode.vM37.primary_assembly.annotation.filtered.gtf \
  --te-saf    /data1/shared/ref/mouse/Ensembl/mm39/GRCm39_rmsk_TE_GROUPED_all_noExon.saf \
  --gene-s    2 \                               # GENE strandedness — VERIFY per library
  --out-dir   <OUT_DIR> \
  --threads   12
```

**Verify it worked (the QC gate — full checklist below):**

```bash
M=<OUT_DIR>/featurecounts_TE/te_counts_matrix.txt
awk 'NR>1{for(i=2;i<=NF;i++) if($i!=int($i)){print "FRACTIONAL!"; exit 1}}' "$M"  # integer
head -1 "$M"; wc -l "$M"   # ~1,243 TE meta-features (mm39), Subfamily:Family:Class rows
```

---

## Progressive Depth

### Basic Usage — the wrapper

`scripts/run_te_counting.sh` is the entry point. It:
1. Symlinks the matched BAMs into `<OUT_DIR>/bam_fin/` (no copies).
2. Bind-mounts the symlink-**target** dir(s) at an **identical host=container path**
   (`-v $REAL:$REAL:ro`) so links resolve inside the container and the driver's awk parser
   keys clean `<sample>` column names off the BAM basename.
3. Runs the vendored `runFeatureCounts_TE_and_genes.sh` (TE pass → gene pass → row-bind) in
   `te-fc:2.0.2` as `-u $(id -u):$(id -g)`.

Required args: `--bam-dir --gene-gtf --te-saf --gene-s --out-dir`. Optional: `--threads`
(12), `--te-strand` (`unstranded` | `sense_antisense`; default `unstranded`), `--bam-glob`
(`*.bam`), `--image` (`te-fc:2.0.2`). `--te-strand sense_antisense` gives stranded,
bidirectional-preserving TE counts (sense + antisense channels) — the more principled
best-practice for a joint gene+TE matrix on a stranded library (grade B / mechanistic, not a
benchmarked standard). `unstranded` (`-s 0`) is a valid standalone option that matches the
dominant tool's default (TEtranscripts `--stranded no`); the field genuinely splits and
mode-switching is not required.

### Intermediate Usage — strandedness (the error-prone variable)

The **gene** `-s` is **library-specific and must be verified per dataset** — never hardcode.
Confirm against MultiQC inferred strandedness, RSeQC/Salmon, AND the featureCounts header
(`Strand specific : reversely stranded`). In-house dUTP/TruSeq libraries ran `-s 2` (reverse);
a forward library would run `-s 1`.

**TE strandedness is context-dependent and the field is SPLIT — `-s 0` is neither a universal
rule nor retroactively wrong.** Two myths to avoid in *both* directions:
- The old "always `-s 0` to capture bidirectional TE transcription" framing is mis-attributed to
  Teissandier 2019 (it benchmarks *multimapper handling only* — the word "strand" appears once, as
  a fixed `-s 0` parameter — and says nothing about strand choice).
- But "stranded is THE field standard" is *also* an over-claim. The dominant tool
  (TEtranscripts/TEcount) **defaults to `--stranded no` (unstranded)**; best-practice literature
  (TE-Seq 2025, doi:10.1186/s13100-025-00381-w) *recommends* stranded for directional libraries.
  So stranded-for-joint is **best-practice / mechanistic (grade B), not a benchmarked standard**,
  and the field genuinely splits between tool default and best-practice.

Also do **not** claim `-s 0` buys better TE *sensitivity*: that has **never been benchmarked
head-to-head** (grade GAP). The one study simulating both modes (Savytska 2022,
doi:10.3389/fgene.2022.1026847) found **stranded FDR (54.9%) ≤ unstranded (58.7%)** — `-s 0` is a
sensitivity-for-specificity *trade*, not a gain. Real TE bidirectionality is **class-specific**
(L1-ASP/ORF0 and LTR/ERV antisense are real; SINE/intronic antisense is largely passive host
read-through), not a uniform property of TE loci.

Choose by goal (options with grades, not a mandate):

- **Standalone TE-family quantification or a genuinely non-directional library →** `-s 0`
  (unstranded), the wrapper default (`--te-strand unstranded`). **Defensible (grade B):** matches
  the dominant tool's default. Counts TE reads on either strand; cost is a specificity *trade*,
  not a sensitivity gain.
- **JOINT gene+TE matrix on a STRANDED library →** the **more principled best-practice** is a
  single consistent stranded convention: count TEs at the **same strandedness as genes** and
  preserve bidirectional biology via a **sense/antisense split** rather than collapsing to `-s 0`.
  Use `--te-strand sense_antisense`: for a reverse library this emits a TE-**sense** matrix
  (`-s 2`, matched to genes) and a TE-**antisense** matrix (`-s 1`), keeping bidirectional signal
  *and* gene-comparability. **Grade B / mechanistic — better FDR in the one benchmark and
  separates autonomous from passive TE transcription, but NOT proven superior for TE DE.**
  Mode-switching (unstranded TEs + stranded genes) is **not required**.

**Standalone vs joint (gene+TE) strandedness — short note.** The in-house production runs used TE
`-s 0`. That remains a **defensible standalone choice**: it matches TEtranscripts' default and
stays valid in hindsight. For the *definitive joint* gene+TE analysis, a stranded recount
(`-s 2` / sense+antisense) is the more principled option (grade B; see the evidence-graded
reconciliation, note 13). When you combine gene+TE for joint normalization/DE, the caveats
below are **graded options**, not mandates (see "Evidence & open questions"):

- **Size factors from genes only** (DESeq2 `estimateSizeFactors(dds, controlGenes = isGene)`, or
  equivalently edgeR `calcNormFactors(method="TMM")` on a genes-only `DGEList` with the resulting
  `norm.factors` applied to the combined object): **grade B / contested.** Same gene anchor, two
  estimators (median-of-ratios vs TMM). TE-Seq advocates genes-only; the dominant tool
  TEtranscripts **pools** genes+TEs. Reasonable but non-universal — sanity-check against pooled
  factors.
- **Sense/antisense split:** **grade B / SQuIRE-specific** design ("the only TE tool to output
  strandedness of each transcript"), defensible to mirror, not a field standard.
- **Within-feature-type, across-sample DE only; never compare gene-vs-TE magnitude within a
  sample; no TPM/FPKM for TE meta-features** (a summed multi-locus subfamily has no single
  length): **grade C / mechanistic inference** — sound and consistent with tool behavior, but not
  stated in any TE primary source.

This handoff caveat travels with the matrix to `annotate-bulk-rnaseq-data`.

### Advanced Usage — the vendored driver (the code is the spec)

`scripts/runFeatureCounts_TE_and_genes.sh` (gene pass delegates to `scripts/runFeatureCounts.sh`)
are **frozen, vendored copies** of the TE-RNAseq-toolkit drivers — self-contained so the skill
is a runnable artifact (a deliberate reversal of the prior version-pointer ADR). Comments were
corrected vs the originals (grouped no-exon SAF; integer Random-One; no `--fraction`; TE `-s`
context-dependent); **code logic is byte-identical**. Underlying invocations:

```
TE (unstranded, default):     featureCounts -M -F SAF -a <SAF> -o te_counts_raw.txt -s 0 -p --countReadPairs -B -C -T <t> <BAMs>
TE (sense, reverse lib):      featureCounts -M -F SAF -a <SAF> -o te_counts_sense_raw.txt -s 2 -p --countReadPairs -B -C -T <t> <BAMs>   # INTEGER Random-One (no --fraction)
TE (antisense, reverse lib):  featureCounts -M -F SAF -a <SAF> -o te_counts_antisense_raw.txt -s 1 -p --countReadPairs -B -C -T <t> <BAMs>   # INTEGER Random-One (no --fraction)
Gene:                         featureCounts -a <GTF> -o counts_matrix.txt -p --countReadPairs -B -C -s <0|1|2> -t exon -g gene_id -T <t> <BAMs>
```

### Library layout

Those invocations show the paired-end form. `runFeatureCounts_TE_and_genes.sh -L se` drops
`-p --countReadPairs -B -C` from every pass, and `runFeatureCounts.sh -p ''` does the same for a
standalone gene run. `-L` defaults to `pe`, so existing calls are unchanged.

```
TE, single-end:    featureCounts -M -F SAF -a <SAF> -o te_counts_raw.txt -s <n> -T <t> <BAMs>
Gene, single-end:  featureCounts -a <GTF> -o counts_matrix.txt -s <n> -t exon -g gene_id -T <t> <BAMs>
```

Each dropped flag is meaningless on single-end input: `-p --countReadPairs` counts one fragment per
mate pair, `-B` requires both ends aligned, and `-C` excludes pairs whose ends land on different
chromosomes. A single-end read has one end, so featureCounts already counts it once.

`qc/tools/04_core_regime_witness.sh` and `qc/tools/07_silent_attribution.sh` take `--layout se` for
the same purpose, and `tests/strand_qc/run_regression.sh` already carries `se` and `se_noM` kernels.

> Note: **all** TE passes — primary unstranded AND the optional sense/antisense auxiliaries
> (`--te-strand sense_antisense`) — are integer Random-One (`-M`, no `--fraction`): one kernel
> everywhere, integer because STAR Random-One emits one alignment/read. The fractional route
> (`-M --fraction` → non-integer → round()/limma-voom before DESeq2) is a labeled **non-default
> alternative**, Strategy-B, requiring STAR `--outSAMmultNmax 100` — see the Decision Tree.

- **TE pass:** `-M` (multi-mappers counted — REQUIRED under Random-One: STAR keeps `NH>1` on the
  single emitted line, so featureCounts discards multimappers without `-M`), **NO `--fraction`**
  → integer Random-One (preferred for joint DESeq2; feeds it natively without a lossy `round()`).
  SAF `GeneID = Subfamily:Family:Class` → ~1,243 subfamily meta-features. TE `-s` is chosen by
  context (see "Intermediate Usage" above; field is split): `-s 0` unstranded (matches the
  dominant tool's default) for standalone work, or stranded sense/antisense
  (`--te-strand sense_antisense`) matched to genes — the more principled best-practice (grade B)
  for a joint matrix.
- **Gene pass:** multi-mappers excluded (featureCounts default), `-s` per library.
- **Flags deliberately NOT added on the grouped exon-subtracted SAF:** `--primary` (redundant
  under Random-One — one primary line already emitted), `-O` (can double-assign reads across
  overlapping subfamilies → overestimate), `--largestOverlap` (silently drops tie reads). Keep
  the lean set above. `--runRNGseed` is pinned upstream (STAR) for reproducible Random-One.
- **Combine:** row-binds gene + TE into `combined_gene_TE_counts.tsv` (valid only because
  exonic TE loci were subtracted from the SAF → no double-counting).

The full end-to-end runbook (inputs, lean BAM path, staging recipe, QC gate, handoff) lives in
**`references/te-counting-workflow.md`**.

---

## Outputs

| File | Path |
|---|---|
| TE subfamily matrix | `<OUT>/featurecounts_TE/te_counts_matrix.txt` |
| Gene matrix | `<OUT>/fc_genes/count_matrices_fc/sorted_counts_matrix.txt` |
| Combined (row-bind) | `<OUT>/combined_gene_TE_counts.tsv` |

Representative dims (one mm39 cohort): TE 1,243 × 45; gene 78,317 × 45; combined 79,560 × 45.

---

## Verification Checklist (the QC gate)

After running, confirm before handoff:

- [ ] **Integer TE counts** — no fractional values (Random-One, no `--fraction`).
- [ ] **TE label shape** — every TE row is 3-field `Subfamily:Family:Class` (exactly 2 colons).
- [ ] **Sample order == samplesheet** — matrix columns match samplesheet order 1:1; gene header
      == TE header.
- [ ] **No zero-libsize samples** — every per-sample gene and TE total is nonzero.
- [ ] **TE proportion = a library-specific sanity band, NOT a hard threshold.** Expect internal
      consistency across replicates; flag *wild* outliers, not an absolute number. When TEs are
      counted `-s 0` (unstranded) against a stranded gene denominator, the mismatch **inflates**
      TE% (the gene denominator drops antisense/ambiguous reads the unstranded TE pass keeps), so
      "TE %" is a QC sanity band, **not a biological transcriptome fraction** — an in-house dataset
      sat in the high-single-digit percent range under standalone `-s 0`, internally consistent
      across replicates and offset from a different-tissue reference (a different tissue runs
      lower, as expected). A stranded TE recount (`--te-strand sense_antisense`) puts TE
      and gene rows on one orientation convention (the more principled best-practice for a joint
      matrix, grade B); it still does not license gene-vs-TE within-sample magnitude comparison
      (grade C — see "Evidence & open questions").
- [ ] **featureCounts version** — raw headers read `# Program:featureCounts v2.0.2`.
- [ ] **Strand-split foot-guns acknowledged** — never sum sense+anti (`FLAG-SUM-CHANNELS`),
      never s0-denominate the ERV/sat/DNA tail (`FLAG-S0-DENOM-ERV`), gene≠TE kernel
      (`FLAG-KERNEL-MISMATCH`); see `docs/QC.md`.
- [ ] **QC a new TE dataset end-to-end** — `qc/run_qc.sh BAM_DIR SAF STRAND OUTDIR` runs the
      strand-split QC suite (the `-R CORE` regime witness, closure-table audit, `-O` silent-loss
      attribution, young gate, SAF-geometry concordance) and prints a consolidated GREEN/RED block.

---

## Evidence & open questions

Grade tags used across this skill (and the two it hands to): **A** peer-reviewed standard ·
**B** tool default or single strong pipeline's recommendation · **C** sound mechanistic inference,
not stated in a TE primary source · **D** folklore / mis-imported · **GAP** no adequate primary
source — open. Authoritative basis: the evidence-graded reconciliation (note 13).

Key claims by grade:
- **A (intact):** `-M` required under Random-One; integer Random-One feeds DESeq2; random-one ≈
  `-M --fraction`, unique-only undercounts young families (Teissandier 2019); do NOT add
  `--primary`/`-O`/`--largestOverlap`; `--runRNGseed` pinned; `te-fc:2.0.2` pin; no TPM for genes
  cross-sample DE; the joint gene+TE *matrix* is a reviewed construct.
- **B:** stranded-for-joint is best-practice, not a benchmarked standard (field SPLITS —
  TEtranscripts defaults `--stranded no`); genes-only size factors (DESeq2
  `controlGenes = isGene` or edgeR `calcNormFactors(method="TMM")` on a genes-only `DGEList`,
  applied to the combined object; TEtranscripts pools instead); sense/antisense split
  (SQuIRE-specific).
- **C:** no gene-vs-TE within-sample magnitude comparison; no TPM/FPKM for TE meta-features.
- **GAP:** "unstranded → better TE sensitivity" — **never benchmarked**; the only both-mode study
  (Savytska 2022) found stranded FDR ≤ unstranded.

Explicit gaps (do not paper over):
- **No ground-truth gold standard** — every TE benchmark rests on simulation (no dataset has known
  per-locus TE counts).
- **TE strandedness is under-benchmarked** — exactly one both-mode study, FDR-only.
- **Gene–TE disambiguation is unsolved** — intron retention / exonized fragments / read-through
  inflate TE counts; no consensus fix.
- **The in-house gene `s0/s2 ≈ 0.95` figure is an EMPIRICAL in-house measurement** (one dataset,
  internal note), not a literature value.

Long-read note: short-read **subfamily-level** quant (this skill) is **current**, not legacy
(new tools still baseline against TEtranscripts). Long-read (ONT/PacBio) **complements** — it owns
locus identity / isoform / chimera resolution — but lacks the depth for sensitive differential
*abundance*; the flagship hybrid (LocusMasterTE 2025) injects long-read TPM into a short-read EM.
It is **not a replacement** for short-read TE DE.

---

## Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `featureCounts: not found` in container | Used `scdock-r-dev:v0.5.x` (no subread) | Use `te-fc:2.0.2` (or legacy `scdock-r-dev:v0.2`). |
| BAM symlinks fail to open inside container | Target dir not mounted, or mounted at a different path | Mount the symlink-target dir at an **identical host=container path** (`run_te_counting.sh` does this). |
| Column names are full paths, not sample names | BAMs passed by a path the awk parser can't reduce to a basename | Use the identical-path mount + `bam_fin/` symlinks so the basename parser yields `<sample>`. |
| Fractional values in TE matrix | `--fraction` was added | Remove it; this recipe is integer `-M` Random-One. |
| Gene counts ~half expected / near zero | Wrong gene `-s` (forward vs reverse) | Set `--gene-s` from MultiQC + featureCounts header, per library. Never assume 1 vs 2. |
| Combined matrix double-counts a region | SAF still contains exonic TE loci | Use the `*_noExon.saf` from `te-reference-saf-build`. |

---

## Resources

- **Locked image:** `env/Dockerfile` + `env/build.sh` → `te-fc:2.0.2` (featureCounts v2.0.2).
- **Vendored drivers:** `scripts/runFeatureCounts_TE_and_genes.sh`, `scripts/runFeatureCounts.sh` (frozen, comments corrected).
- **Wrapper:** `scripts/run_te_counting.sh` (staging + identical-path mount + run).
- **Runbook:** `references/te-counting-workflow.md` (end-to-end, QC gate, handoff).
- **Smoke tests:** `tests/run_skill_tests.sh` (image present, v2.0.2, synthetic integer matrix).
- **Strand-split QC + regression:** `tests/strand_qc/run_regression.sh` (synthetic truth table in `te-fc:2.0.2` + regime-classifier fixture, importing the suite's shared classifier); reference `references/strand-split-qc.md`.
- **Runnable QC suite:** `qc/run_qc.sh BAM_DIR SAF STRAND OUTDIR` — the parameterized, operator-invoked "QC a new TE dataset end-to-end" suite (the `-R CORE` regime witness, closure-table audit, `-O` silent-loss attribution, young gate, SAF-geometry concordance, DE_precheck). Container/bedtools tools skip gracefully when absent. See `qc/README.md`.
- **QC doctrine:** the strand-split invariant, the `excess/ambiguous` directional meter, the working principles, the warning-flag taxonomy, and the GREEN/RED gate live in the toolkit `docs/QC.md`.
- **subread/featureCounts:** https://subread.sourceforge.net/ (release 2.0.2).

---

## When not to use

- Recipe is integer Random-One everywhere (-M, NO --fraction) — primary AND the optional sense/antisense aux passes. Fractional 'Strategy B' is an equally-valid alternative (Teissandier) but a different config (STAR all-alignments --outSAMmultNmax 100 + -M --fraction, non-integer) — see the Decision Tree.
- Do not use for locus-level / copy-resolved TE quantification. The grouped SAF is subfamily-level; use SQuIRE/Telescope instead.
- Do not use to build the TE SAF or run STAR. The SAF is built by te-reference-saf-build and the Random-One BAMs by star-te-preprocessing; this skill begins at pre-built BAMs + SAF.
- Do not run featureCounts from scdock-r-dev:v0.5.x — those images lack subread. Use the locked te-fc:2.0.2 (or legacy scdock-r-dev:v0.2).
- Do not perform DE, annotation, or DGEList assembly here. Hand the matrices to annotate-bulk-rnaseq-data.

---

## See also

The canonical chain is `te-reference-saf-build` + `star-te-preprocessing` → **`te-gene-featurecounts`** → `annotate-bulk-rnaseq-data`. For locus-level / copy-resolved TE quantification (out of scope here), see SQuIRE/Telescope (external).

- `te-reference-saf-build` — Prerequisite; builds the grouped, exon-subtracted TE SAF this skill consumes
- `star-te-preprocessing` — Prerequisite; produces the BAMs and owns the alignment/counting contract
- `annotate-bulk-rnaseq-data` — Next step; annotate matrices, parse TE IDs, build combined DGEList
