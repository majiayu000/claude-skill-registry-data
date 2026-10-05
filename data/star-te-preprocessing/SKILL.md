---
name: star-te-preprocessing
description: >-
  Use when bulk RNA-seq alignment must preserve TE signal for DE, or need
  the preprocessing contract a TE matrix must satisfy: STAR "Random-One"
  args + subfamily SAF + integer -M counting. For run mechanics use
  nfcore-rnaseq-execution. For locus-level TE use SQuIRE/Telescope. For
  annotation use annotate-bulk-rnaseq-data and the TE-RNAseq-toolkit.
license: MIT
---

# STAR + featureCounts TE-Compatible Preprocessing (Random-One)

## Overview

This skill is the opinionated, durable recipe that makes a bulk RNA-seq STAR alignment **transposable-element compatible**: it retains multi-mapping reads (TEs are repetitive, so unique-only mapping systematically undercounts TEs — a young-family-biased loss, ~10–21% of multimappers overall and much higher for young L1/SVA/ERV families, not a flat 80–90% — `METHODOLOGY.md`) while emitting **exactly one alignment per read**, so every fragment contributes exactly one **integer** count. It owns the canonical `--extra_star_align_args` "Random-One" string and its per-flag TE rationale, the grouped subfamily SAF + bedtools exon-subtraction contract, and the integer `featureCounts -M` counting discipline. It is the missing, now-canonical handoff between nf-core/rnaseq and the TE-RNAseq-toolkit — previously written down only in per-project `/scratch` READMEs (artifact `03-te-rnaseq-toolkit-map.md` §D).

The headline differentiator from adjacent skills: this skill owns the **alignment + counting CONTRACT** (what the BAM and count matrix must satisfy), not the pipeline mechanics and not the downstream R analysis.

**When to use this skill:**
- You are aligning bulk RNA-seq and the output must support downstream TE differential expression (subfamily-level).
- You need the exact `--extra_star_align_args` string and the per-flag justification for a new dataset.
- You need to build the grouped, exon-subtracted TE SAF or set `featureCounts` strandedness/multimapper flags correctly.
- You need to verify a run satisfies the preprocessing contract before handing matrices downstream.

**When NOT to use this skill:**
- Generic nf-core run mechanics (samplesheet, `NXF_UID/GID`, `/data2` work dirs, `-resume`, cleanup) → use `nfcore-rnaseq-execution`.
- Locus-level / copy-resolved TE quantification → out of scope; use SQuIRE or Telescope (EM-based, `METHODOLOGY.md:47-50`).
- Annotating count matrices, parsing TE IDs into a DGEList, DE or enrichment → use `annotate-bulk-rnaseq-data` and the TE-RNAseq-toolkit.

---

## Decision Tree

```
Need TE-aware counts from bulk RNA-seq?
│
├─ Want integer, subfamily-level, family-level-accurate counts?
│     →  THIS skill (Random-One: --outSAMmultNmax 1 + featureCounts -M, NO --fraction)
│
├─ Want fractional 1/n multimapper apportionment ("Strategy B")?
│     →  Equally accurate to Random-One (Teissandier 2019, grade A) — a valid alternative,
│        just not the opinionated default here. To use it: STAR --outSAMmultNmax 100 (emit
│        ALL alignments) + featureCounts -M --fraction → NON-INTEGER counts → limma-voom
│        (or round() for DESeq2). See TE-RNAseq-toolkit docs/METHODOLOGY.md "Strategy B".
│        Default stays Random-One integer (DESeq2-clean, smaller BAMs, deterministic w/ seed).
│
├─ Want locus-level / copy-resolved TE expression?
│     →  out of scope → SQuIRE / Telescope (EM)
│
└─ Just running the pipeline (no TE signal needed)?
      →  nfcore-rnaseq-execution alone (omit --extra_star_align_args)
```

---

## Quick Start

The Random-One recipe is two artifacts: (1) the STAR args passed to nf-core, and (2) the two-pass `featureCounts` driver. The nf-core run itself is owned by `nfcore-rnaseq-execution`; this skill owns the TE-specific portion.

```bash
# 1) STAR: pass the canonical Random-One string as nf-core --extra_star_align_args
#    (see "The Canonical STAR Recipe" below for the verbatim string + per-flag rationale).
#    nf-core run mechanics (UID, work dir, -resume) → nfcore-rnaseq-execution.
#    Per-project Groovy config is the OWNED artifact: references/te_star.config

# 2) featureCounts: two passes via the authoritative driver (do NOT hand-roll the flags)
#    TE-RNAseq-toolkit v2.0.3 — scripts/runFeatureCounts_TE_and_genes.sh
runFeatureCounts_TE_and_genes.sh \
  -i  STAR_BAM_DIR \
  -o  OUT_BASE \
  -g  gencode.vM37.primary_assembly.annotation.filtered.gtf \
  -e  GRCm39_rmsk_TE_GROUPED_all_noExon.saf \
  -S  2                     # GENE strandedness — verify per library, do NOT assume
                            # TE strandedness is context-dependent; the field is SPLIT (NOT fixed
                            # -s 0): -s 0 matches the dominant tool's default (TEtranscripts
                            # --stranded no) for standalone / non-directional libs; stranded
                            # sense/antisense (--te-strand sense_antisense) matched to genes is the
                            # more principled best-practice (grade B) for a joint gene+TE matrix
```

**Verify it worked (the contract — see full checklist below):**

```bash
# Integer TE counts (no fractional values from --fraction):
awk 'NR>1{for(i=2;i<=NF;i++) if($i!=int($i)){print "FRACTIONAL!"; exit 1}}' te_counts_matrix.txt

# TE matrix is subfamily-level grouped, Subfamily:Family:Class labels (~1,243 rows for mm39):
head -1 te_counts_matrix.txt; wc -l te_counts_matrix.txt   # expect ~1,243 meta-features
```

---

## Progressive Depth

### Basic Usage — The Canonical STAR Recipe

The **canonical** string is the 13036-DM / AdaW_eWAT_WL "Random-One" variant (`02-nfcore-operational-knowledge.md:41`, byte-identical across both reference runs). Pass it **verbatim** to nf-core as `--extra_star_align_args`:

> **Pipeline version matters:** this string was validated on nf-core/rnaseq **`-r 3.20.0`**. On a newer pipeline version (e.g. current latest `-r 3.26.0`) the STAR defaults / `--extra_star_align_args` interaction must be **re-validated** before trusting the recipe — do **not** silently change the canonical string. Run mechanics + the pinned version live in `nfcore-rnaseq-execution`.

```text
--twopassMode Basic --alignEndsType EndToEnd --outSAMunmapped None --alignSJoverhangMin 8 --alignSJDBoverhangMin 1 --outFilterMismatchNoverLmax 0.06 --outFilterMismatchNmax 999 --alignIntronMin 20 --alignIntronMax 1000000 --alignMatesGapMax 1000000 --outFilterScoreMinOverLread 0.4 --outFilterMatchNminOverLread 0.4 --outFilterType BySJout --outFilterMultimapNmax 100 --winAnchorMultimapNmax 200 --outMultimapperOrder Random --outSAMmultNmax 1 --outSAMprimaryFlag OneBestScore --runRNGseed 777
```

**Flag → TE purpose** (source: `02-nfcore-operational-knowledge.md` §B.1):

| STAR flag | Value | TE-analysis purpose |
|---|---|---|
| `--outFilterMultimapNmax` | `100` | **Retain multi-mappers** up to 100 loci. Without this, repeat reads are dropped and TE signal vanishes. |
| `--winAnchorMultimapNmax` | `200` | Allow many candidate anchors in repetitive sequence (must exceed the filter cap). |
| `--outMultimapperOrder` | `Random` | Randomize among equally-good hits so the single emitted alignment is unbiased across copies. |
| `--outSAMmultNmax` | `1` | **Emit exactly ONE alignment per read** (Random-One). Each read appears once in the BAM → **integer** counts; `featureCounts` needs no `--fraction`. |
| `--outSAMprimaryFlag` | `OneBestScore` | One primary per read even on score ties — never multiple primaries. |
| `--runRNGseed` | `777` | Reproducible random selection across re-runs. |
| `--alignEndsType` | `EndToEnd` | No soft-clipping → prevents spurious partial matches inside repeats. |
| `--twopassMode` | `Basic` | Discover novel SJs in pass 1; better splice accuracy on the gene side. |
| `--outFilterType` | `BySJout` | Prefer alignments consistent with known/learned SJs. |
| `--outFilterScoreMinOverLread` | `0.4` | ≥40% of read mappable by score — permissive enough to keep repeat reads. |
| `--outFilterMatchNminOverLread` | `0.4` | ≥40% of read must match; avoids tiny anchors in repeats. |
| `--outFilterMismatchNoverLmax` | `0.06` | ≤6% mismatches/read (relax to 0.08–0.10 if alignment rate <70%). |
| `--outFilterMismatchNmax` | `999` | Defers to the relative cap above. |
| `--alignSJoverhangMin 8` / `--alignSJDBoverhangMin 1` | | Reasonable SJ support for novel/annotated junctions. |
| `--alignIntronMin 20` / `--alignIntronMax 1000000` / `--alignMatesGapMax 1000000` | | Mammalian intron/gap ranges. |
| `--outSAMunmapped` | `None` | Drop unmapped reads → smaller BAM. |

The per-project Groovy config (`references/te_star.config`) carries references, BAM retention (`save_align_intermeds = true`), Docker UID trick, `/data2` temp redirection, and resource caps — the **TE-specific STAR behavior lives in `--extra_star_align_args`, not in the config**.

> **Deprecated evolution footnote:** older datasets (13441-DM, 13444-DM) used `--outSAMprimaryFlag AllBestScore` + `--outSAMtype BAM Unsorted` and **lacked `--outSAMmultNmax 1`** → those BAMs emit *multiple* primaries per read and are **NOT comparable** to integer Random-One counts (`02-nfcore-operational-knowledge.md` §C). Use the canonical string above for all new runs.

### Intermediate Usage — The Preprocessing Contract

The output must satisfy the following for downstream TE DE (condensed from `03-te-rnaseq-toolkit-map.md` §B). This is the contract this skill OWNS; the exact `featureCounts` flags are owned by the driver (see Advanced).

1. **Aligner = STAR**, via nf-core `--aligner star_salmon`. Gene counts come from `featureCounts` on the STAR BAM (Salmon quant is incidental).
2. **Random-One multimapper retention** — `--outFilterMultimapNmax 100` + `--outSAMmultNmax 1` + `--outMultimapperOrder Random` + `--outSAMprimaryFlag OneBestScore` + `--runRNGseed 777`.
3. **Input to counting = BAM.** `featureCounts` consumes the STAR genome BAM(s). Unsorted BAM is acceptable (`METHODOLOGY.md:52-53`); featureCounts pairs reads internally.
4. **BAM retention is load-bearing.** `save_align_intermeds = true` keeps the unsorted `Aligned.out.bam`; do not delete published BAMs from the outdir (cleanup touches only the work dir).
5. **Two annotations:** gene **GTF** (GENCODE, the nf-core *filtered* variant) + a separate grouped TE **SAF** (not a combined GTF, not Dfam).
6. **Grouped subfamily SAF.** Built from the TEtranscripts `GRCm39_Ensembl_rmsk_TE.gtf.gz`; the SAF `GeneID` is the TE group label **`Subfamily:Family:Class`** (e.g. `L1Md_A:L1:LINE`) → ~1,243 subfamily meta-features, not locus-level.
7. **Non-overlapping annotations.** TE loci overlapping gene exons are removed with `bedtools subtract` → `*_noExon.saf`, so a read counts as gene OR TE, never both. This is the precondition for a valid combined matrix.
8. **Strandedness:** genes `-s` is **library-specific** (verify); TE `-s` is **context-dependent and the field is SPLIT, NOT a fixed `-s 0`** — `-s 0` for standalone TE quantification or a non-directional library (matches the dominant tool's default, TEtranscripts `--stranded no`), or **stranded TEs matched to genes with a sense/antisense split** (`--te-strand sense_antisense`) as the more principled best-practice for a joint gene+TE matrix on a stranded library (grade B / mechanistic, NOT a benchmarked standard; preserves bidirectional biology without discarding strand). Mode-switching is not required. Multi-mappers **included `-M`** in either case. (Alignment itself is strand-agnostic — this choice is made at the featureCounts step, not in STAR.)
9. **Integer count semantics.** `-M` WITHOUT `--fraction` → integer Random-One (the opinionated default). Fractional "Strategy B" (`-M --fraction` over all-alignment BAMs) is an equally-accurate alternative (Teissandier 2019) — non-integer, use limma-voom/round; see the Decision Tree.
10. **TE-ID label = `Subfamily:Family:Class`** — the same label `annotate-bulk-rnaseq-data` and `te_utils.R::parse_te_id` consume. Construct the SAF `GeneID` with this label so it parses downstream.
11. **Paired-end flags** `-p --countReadPairs -B -C` (fragments, both-ends-mapped, no chimeras).
12. **QC gate:** TE proportion (TE/total reads) consistent across replicates (AdaW: 3.8–6.0%); wild variation flags a technical problem.

**SAF build (grouped, exon-subtracted):** start from the TEtranscripts GTF, collapse to subfamily groups with `Subfamily:Family:Class` `GeneID`, then subtract exonic loci with `bedtools subtract` to produce `GRCm39_rmsk_TE_GROUPED_all_noExon.saf`. The no-exon SAF is the one fed to the TE counting pass.

**Strandedness discipline (the most error-prone per-dataset variable):** the samplesheet uses `strandedness=auto` so nf-core infers it, but the downstream **gene** `featureCounts -s` value is set **manually** and must match. 13036-DM used genes `-s 2` (reverse); AdaW used genes `-s 1` (forward). **Always** confirm with the MultiQC inferred strandedness and the `featureCounts` header before trusting gene counts. TE `-s` is **chosen by goal, not fixed (and the field is split)**: `-s 0` for standalone / non-directional libraries (matches the dominant tool's default), or stranded sense/antisense matched to genes as the more principled best-practice (grade B) for a joint gene+TE matrix on a stranded library (see `te-gene-featurecounts` for the full standalone-vs-joint note and its "Evidence & open questions" grades). Alignment is strand-agnostic, so the STAR recipe is unchanged either way.

### Advanced Usage — featureCounts (point to the authoritative driver)

The exact `featureCounts` flags are NOT restated here as an editable copy — the **code is the spec**:

> **Authoritative:** TE-RNAseq-toolkit **v2.0.3** — `scripts/runFeatureCounts_TE_and_genes.sh` (gene pass delegates to `scripts/runFeatureCounts.sh`).

The contract the script enforces (authoritative pointer above):

- **TE pass:** `featureCounts -M -F SAF -a TE_SAF -s <0|2 sense|1 antisense> -p --countReadPairs -B -C` — `-M` counts multi-mappers (REQUIRED under Random-One — STAR keeps `NH>1` on the single emitted line, so featureCounts drops them without `-M`); **no `--fraction`** → integer counts. TE `-s` is context-dependent and the field is split: `-s 0` (unstranded) for standalone / non-directional libs (matches the dominant tool's default), or stranded sense/antisense (`--te-strand sense_antisense`, e.g. `-s 2`+`-s 1` for a reverse lib) matched to genes as the more principled best-practice (grade B) for a joint matrix — NOT a fixed `-s 0`. The script explicitly notes `--fraction` "was removed to facilitate integer counting" (`runFeatureCounts_TE_and_genes.sh:23-24`).
- **Gene pass:** `featureCounts -a GTF -s <0|1|2> -t exon -g gene_id -p --countReadPairs -B -C` — multi-mappers **excluded** (featureCounts default), strandedness **per library** (the script's `-S` flag).
- **Combine:** the driver row-binds the gene matrix + TE matrix into `combined_gene_TE_counts.tsv` (valid only because exonic TEs were subtracted → no double-counting).

> **Note on the `sense_antisense` branch:** the primary TE matrix is integer (`-M`, no `--fraction`); the driver's optional `--te-strand sense_antisense` branch emits *auxiliary* TE-sense (`-s 2` for a reverse lib, matched to genes) and TE-antisense (`-s 1`) matrices and currently runs those with `--fraction` (so they are non-integer and need `round()` before DESeq2). This sense/antisense split is **the more principled best-practice (grade B / SQuIRE-specific) for keeping bidirectional TE biology in a joint gene+TE matrix on a stranded library** — it preserves strand instead of collapsing to `-s 0` — but it is not a benchmarked standard, and `-s 0` (matching the dominant tool's default) remains a valid standalone option. (Whole-library fractional "Strategy B" for the primary matrix remains documented-but-not-current in `docs/METHODOLOGY.md`; do not adopt it for the primary integer matrix without an explicit reason.)

### TE counting (post-alignment) — the end-to-end runbook

The runnable, **env-locked** counting workflow — the two-pass `featureCounts` driver, its own pinned container (`te-fc:2.0.2`, featureCounts v2.0.2), the BAM symlink/identical-path Docker staging recipe, and the QC gate — now lives in the **`te-gene-featurecounts`** packaged skill (`references/te-counting-workflow.md` here is a thin pointer to it). This skill (`star-te-preprocessing`) still owns the alignment + counting **contract** and the canonical STAR string; `te-gene-featurecounts` owns the executable counting artifact. SAF *construction* is owned by `te-reference-saf-build`.

---

## Verification Checklist

After running this skill, confirm:

- [ ] **STAR args verbatim:** the run's `--extra_star_align_args` is byte-identical to the canonical string above (in particular `--outSAMmultNmax 1` and `--outSAMprimaryFlag OneBestScore` are present).
- [ ] **BAMs retained:** unsorted `star_salmon/*/Aligned.out.bam` and sorted BAMs exist in the outdir (`save_align_intermeds = true`).
- [ ] **Integer TE counts:** no fractional values in `te_counts_matrix.txt` (Random-One, no `--fraction`).
- [ ] **Subfamily-level, correct label:** TE rows are `Subfamily:Family:Class` (e.g. `L1Md_A:L1:LINE`), ~1,243 meta-features for mm39.
- [ ] **Non-overlapping SAF:** the TE SAF is the `*_noExon.saf` (exonic loci subtracted via `bedtools subtract`).
- [ ] **Strandedness verified:** gene `-s` matches MultiQC inferred strandedness + `featureCounts` header; TE `-s` chosen by goal, field-split-aware (`-s 0` standalone — matches the dominant tool's default; or stranded sense/antisense matched to genes as the more principled best-practice for a joint matrix) — neither assumed `-s 0` nor over-claimed as a stranded "standard".
- [ ] **QC gate:** TE proportion consistent across replicates (~3.8–6.0% in the reference projects).

---

## Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Fractional values in TE matrix | `--fraction` was added (Strategy B) | Remove `--fraction`; use integer `-M` only. This recipe is Random-One. |
| TE counts much higher than expected; multiple BAM lines per read | STAR ran without `--outSAMmultNmax 1` (e.g. the deprecated `AllBestScore` variant) | Re-run STAR with the canonical Random-One string; old `AllBestScore` BAMs are not comparable. |
| Gene counts ~half expected (or near zero) | Wrong gene `-s` (forward vs reverse mismatch) | Set gene `-s` from MultiQC inferred strandedness + featureCounts header, per library. Never assume 1 vs 2. |
| Combined matrix double-counts a region | TE SAF still contains exonic loci | Use the `*_noExon.saf` (run `bedtools subtract` against gene exons first). |
| TE signal vanishes / only ~10–20% TE reads kept | Multimappers dropped (`--outFilterMultimapNmax` too low or absent) | Use `--outFilterMultimapNmax 100 --winAnchorMultimapNmax 200`. |
| Downstream `parse_te_id` fails / labels unparseable | SAF `GeneID` not in `Subfamily:Family:Class` form | Build the grouped SAF with the 3-field `Subfamily:Family:Class` label that `te_utils.R::parse_te_id` expects. |

---

## Resources

- **Owned canonical config:** `references/te_star.config` (provenance: 13036-DM / AdaW canonical runs, 2026-06-08).
- **TE-counting workflow (runnable, env-locked):** the **`te-gene-featurecounts`** packaged skill — pinned container `te-fc:2.0.2` (featureCounts v2.0.2), vendored two-pass driver, Docker staging recipe, QC gate. `references/te-counting-workflow.md` here is a thin pointer to it.
- **featureCounts driver:** vendored (frozen) into `te-gene-featurecounts/scripts/` (provenance: TE-RNAseq-toolkit `scripts/runFeatureCounts_TE_and_genes.sh`).
- **Methodology / rationale** (Random-One vs Fractional vs EM, subfamily vs locus, combined vs separate): TE-RNAseq-toolkit — `docs/METHODOLOGY.md`.
- **TE-ID parser** (label definition `Subfamily:Family:Class`): TE-RNAseq-toolkit — `R/te_utils.R::parse_te_id`.
- **nf-core/rnaseq:** https://github.com/nf-core/rnaseq (run at `-r 3.20.0`, `-profile docker`, `--aligner star_salmon`).
- **STAR:** https://github.com/alexdobin/STAR — Random-One strategy cited to Nat. Commun. (2022).

---

## When not to use

- Do not use for locus-level TE quantification (Random-One assignments are stochastic per locus). Use SQuIRE/Telescope instead.
- This recipe is integer Random-One (no --fraction). Fractional 'Strategy B' is an equally-valid alternative (Teissandier) but a different config (STAR all-alignments + -M --fraction) — see the Decision Tree; don't just bolt --fraction onto this integer recipe.
- Do not use for generic nf-core/rnaseq run mechanics (samplesheet, Docker UID, work dirs). Use nfcore-rnaseq-execution instead.
- Do not use for count-matrix annotation, DGEList assembly, or DE. Use annotate-bulk-rnaseq-data and the TE-RNAseq-toolkit instead.

---

## See also

The canonical handoff chain is `star-te-preprocessing → te-gene-featurecounts → annotate-bulk-rnaseq-data → bulk-rnaseq-gsea`. For locus-level / copy-resolved TE quantification (out of scope here — EM-based), see SQuIRE/Telescope (external); for downstream TE DE/enrichment/plotting, see the TE-RNAseq-toolkit (external).

- `te-reference-saf-build` — Upstream; produces the no-exon SAF this skill's featureCounts pass consumes
- `nfcore-rnaseq-execution` — Prerequisite; generic nf-core/rnaseq run mechanics (samplesheet, Docker UID, work dirs, `-resume`, cleanup) that runs the pipeline consuming these STAR args
- `te-gene-featurecounts` — Next step; runs the actual TE+gene counting (env-locked container, two-pass driver, staging), turning the BAMs this skill's contract describes into count matrices
- `annotate-bulk-rnaseq-data` — Downstream; annotate count matrices, parse TE IDs, build combined gene+TE DGEList
