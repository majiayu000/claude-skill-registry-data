---
name: te-reference-saf-build
description: >-
  Use when setting up a NEW genome build / species for TE-compatible
  RNA-seq preprocessing (build-once, shared across datasets). Builds the
  TE GTF + subfamily SAF + exon-subtracted no-exon SAF from the
  TEtranscripts RepeatMasker GTF. For per-dataset alignment+counting use
  star-te-preprocessing. For locus-level TE references use SQuIRE/Telescope.
license: MIT
---

# TE Reference SAF Build (build-once, shared)

## Overview

This skill is the canonical, version-pinned home for **building the shared TE
reference artifacts** that TE-compatible bulk RNA-seq preprocessing consumes: the
TEtranscripts TE GTF, the grouped subfamily SAF, and the exon-subtracted no-exon
SAF. These artifacts are built **~once per genome build** and **shared across every
dataset** — all reference mm39 runs (13036-DM, AdaW_eWAT_WL, 14839-DM) point at the
*same* files under `/data1/shared/ref/mouse/Ensembl/mm39/`. The build recipe was
previously homeless: the toolkit owned zero build code, and the recipe lived only as
inline awk/bedtools prose in per-dataset `/scratch` READMEs.
This skill gives that recipe a single source of truth and an owned, tested executable
(`scripts/build_te_saf.sh`).

The headline differentiator from `star-te-preprocessing`: this skill owns the
**build-once construction** of the reference artifacts; `star-te-preprocessing` owns
the **per-dataset usage contract** (what the BAM/count matrix must satisfy) and
consumes what this skill produces. Cadence and audience differ — a reader running
preprocessing on every dataset should not have to load rare-path build instructions.

**When to use this skill:**
- Setting up a NEW genome build or species for TE preprocessing (e.g. moving from
  mm39 to a new mouse build, or to human GRCh38).
- The shared `*_GROUPED_all_noExon.saf` does not yet exist for your build, or you
  must rebuild it (e.g. a new gene-GTF release changed the exon set).
- You need the version-pinned, reviewer-transparent recipe + script for these
  artifacts rather than copy-pasting awk/bedtools out of an old README.

**When NOT to use this skill:**
- Per-dataset alignment + counting (every run) → use `star-te-preprocessing`.
- Locus-level / copy-resolved TE quantification → out of scope; use SQuIRE/Telescope.
- Building a combined gene+TE GTF or a Dfam annotation → not this recipe.

---

## Decision Tree

```
Need a TE reference for RNA-seq?
│
├─ Building artifacts for a NEW genome build / species (build-once, shared)?
│     →  THIS skill (TE GTF → grouped SAF → no-exon SAF)
│
├─ The shared *_GROUPED_all_noExon.saf already exists for your build?
│     →  Do NOT rebuild. Point star-te-preprocessing at the existing file.
│
├─ Aligning/counting a specific dataset against an existing reference?
│     →  star-te-preprocessing (per-dataset recipe + contract)
│
└─ Need locus-level / copy-resolved TE expression?
      →  out of scope → SQuIRE / Telescope (locus-level annotations)
```

---

## Build-once cadence

These are **shared, build-once** artifacts. Before building, check whether the
canonical file already exists for your build:

```bash
ls -la /data1/shared/ref/mouse/Ensembl/mm39/GRCm39_rmsk_TE_GROUPED_all_noExon.saf
```

If it exists, **do not rebuild** — every dataset reuses the same file (rebuilding
risks a silently different artifact across datasets). Rebuild only when the genome
build changes, the TE GTF source changes, or the gene GTF (and thus the exon set)
changes. Record every build in a provenance record
(`references/reference-build-record-template.md`).

---

## The three artifacts

For mm39 / GENCODE vM37, the canonical names and home directory are (match these
EXACTLY — `star-te-preprocessing/references/te-counting-workflow.md:139-141`):

| Artifact | Canonical filename (under `/data1/shared/ref/mouse/Ensembl/mm39/`) | Role |
|---|---|---|
| TE GTF | `GRCm39_Ensembl_rmsk_TE.gtf.gz` | **Downloaded** (TEtranscripts), not built. Source of `gene_id`/`family_id`/`class_id`. |
| Grouped SAF (all) | `GRCm39_rmsk_TE_GROUPED_all.saf` | **Intermediate.** One row per locus; `GeneID` = `Subfamily:Family:Class`. |
| Grouped no-exon SAF | `GRCm39_rmsk_TE_GROUPED_all_noExon.saf` | **The counting input.** Grouped SAF with exonic loci subtracted. |

> The grouped `_all.saf` is an intermediate; the **`_noExon.saf` is the load-bearing
> shared artifact** fed to `featureCounts`. Do NOT use the stale name
> `GRCm39_rmsk_TE_formatted.saf` (it appears in the toolkit driver's usage examples
> but matches no production run — artifact 08 §A.2; fixing that stale ref is a
> deferred toolkit task, not this skill's job).

For a new species/build, substitute the build prefix (e.g. `GRCh38_...`) but keep
the `_GROUPED_all` / `_GROUPED_all_noExon` suffixes and the `Subfamily:Family:Class`
`GeneID` convention.

---

## Build recipe

Three steps. Steps 2–3 are owned end-to-end by `scripts/build_te_saf.sh`; step 1 is
a manual download. The verbatim awk/bedtools below is lifted from the canonical
READMEs (`13036-DM/README.md`, `AdaW_eWAT_WL/README.md`).

### Step 1 — acquire the TE GTF (DOWNLOAD, not build)

The TE annotation is the **TEtranscripts pre-generated RepeatMasker GTF** — *not*
Dfam, *not* built locally, *not* combined with the gene GTF. It carries `gene_id`
(repName / subfamily), `family_id`, and `class_id` per locus (`13036-DM/README.md:264`,
`AdaW_eWAT_WL/README.md:88-90`):

```bash
# Source: TEtranscripts (https://www.mghlab.org/software/tetranscripts), pre-generated
# by their team. mm39 file: GRCm39_Ensembl_rmsk_TE.gtf.gz (TEtranscripts Dropbox).
TE_GTF=/data1/shared/ref/mouse/Ensembl/mm39/GRCm39_Ensembl_rmsk_TE.gtf.gz
# Download into place, then RECORD the source URL + date + checksum in the build record.
md5sum "$TE_GTF"   # capture for provenance
```

> Acquisition gap (artifact 08 §B.1): the source is documented but there is **no
> scripted fetch and no recorded checksum** in any prior run. When you build a new
> reference, capture the exact download URL, date, and md5 in the build record so the
> artifact is reproducible.

### Step 2 — grouped SAF via awk (`GeneID = Subfamily:Family:Class`)

One row per TE locus, but the SAF `GeneID` is the **group label** — so featureCounts
sums all loci sharing a label into one subfamily meta-feature (~1,243 groups for
mm39). The SAF column format is `GeneID Chr Start End Strand` (1-based, tab-separated),
exactly what the toolkit's `runFeatureCounts_TE_and_genes.sh -F SAF` consumes.
Verbatim from `13036-DM/README.md:162-171` (identical at `AdaW_eWAT_WL/README.md:100-108`):

```bash
zcat "$TE_GTF" |
awk 'BEGIN{OFS="\t"; print "GeneID\tChr\tStart\tEnd\tStrand"}
     $0 !~ /^#/ {
       match($0,/gene_id "([^"]+)"/,g);      # subfamily / repName
       match($0,/family_id "([^"]+)"/,f);    # family
       match($0,/class_id "([^"]+)"/,c);     # class (LINE/LTR/SINE/DNA/RC/...)
       gid = g[1] ":" f[1] ":" c[1];         # TEtranscripts-like label
       print gid, $1, $4, $5, $7
     }' > "$SAF_ALL"
```

The 3-field order `Subfamily:Family:Class` is canon — it is the exact label that
`te_utils.R::parse_te_id` consumes downstream. Construct it in this order or
annotation breaks. (Requires GNU awk for the 3-arg `match()`.)

### Step 3 — no-exon SAF via `bedtools subtract`

Subtract gene exons from the TE intervals so a read counts as gene OR TE, never both
— the hard precondition for a valid combined gene+TE matrix. Verbatim from
`13036-DM/README.md:187-262` (condensed at `AdaW_eWAT_WL/README.md:119-144`):

```bash
# 3a) Exon BED (0-based) from the GENE GTF
awk 'BEGIN{OFS="\t"} $3=="exon"{print $1,$4-1,$5,".",".",$7}' "$GENE_GTF" > exons.bed

# 3b) TE BED from the grouped SAF (0-based), GeneID carried as the BED name
awk 'BEGIN{OFS="\t"} NR>1{print $2,$3-1,$4,$1,".",$5}' "$SAF_ALL" > te_grouped.bed

# 3c) Normalize contig names FIRST (both with-chr or both without). Ensembl mm39 has
#     no 'chr' prefix; mismatched naming SILENTLY yields zero overlap (a silent trap).
sed -E 's/^chr//' exons.bed > exons.tmp && mv exons.tmp exons.bed

# 3d) Sort both (LC_ALL=C, -k1,1 -k2,2n) — bedtools is faster/correct on sorted input
LC_ALL=C sort -k1,1 -k2,2n exons.bed      -o exons.bed
LC_ALL=C sort -k1,1 -k2,2n te_grouped.bed -o te_grouped.bed

# 3e) Subtract, then VERIFY 0 residual overlap
bedtools subtract  -a te_grouped.bed -b exons.bed > te_grouped_noExon.bed
bedtools intersect -a te_grouped_noExon.bed -b exons.bed -u | wc -l   # MUST be 0

# 3f) Rebuild SAF (Start back to 1-based)
awk 'BEGIN{OFS="\t"; print "GeneID\tChr\tStart\tEnd\tStrand"}
     {print $4,$1,$2+1,$3,$6}' te_grouped_noExon.bed > "$SAF_NOEXON"
```

> **Exon-BED provenance gotcha (artifact 08 §A.3, §B.3):** the exon BED MUST come from
> the SAME gene GTF/build as the rest of the pipeline. Both prior mm39 runs borrowed a
> *filtered* gene GTF from a **sibling project's** outdir
> (`.../13441-DM/results_mm39_TE/genome/...filtered.gtf`,
> `13036-DM/README.md:190`) — coupling the no-exon SAF's provenance to a fourth
> project's run. **Recommended instead:** derive the exon BED freshly from the canonical
> gene GTF for the build (e.g. `gencode.vM37.primary_assembly.annotation.gtf(.gz)`).
> `scripts/build_te_saf.sh` does exactly this — it takes the gene GTF as an input and
> derives the exon BED itself, never hardcoding a sibling-project path.

Group count should stay ~1,243 after subtraction.

### Owned executable

`scripts/build_te_saf.sh` is the SSoT executable owner of steps 2–3:

```bash
scripts/build_te_saf.sh \
  --te-gtf   /data1/shared/ref/mouse/Ensembl/mm39/GRCm39_Ensembl_rmsk_TE.gtf.gz \
  --gene-gtf /data1/shared/ref/mouse/Ensembl/mm39/gencode.vM37.primary_assembly.annotation.gtf.gz \
  --out-dir  /data1/shared/ref/mouse/Ensembl/mm39 \
  --prefix   GRCm39_rmsk_TE
# -> <out-dir>/<prefix>_GROUPED_all.saf  and  <out-dir>/<prefix>_GROUPED_all_noExon.saf
```

It accepts gzipped or plain GTFs, derives the exon BED from `--gene-gtf`, normalizes
contig names, runs the subtract + 0-overlap verification, and writes the canonical
filenames. `--keep-classes '^(LINE|SINE|LTR|RC)$'` optionally whitelists classes
(retro-only); the default keeps **all** classes (the canonical decision).

---

## Science rationale (pointer, not a copy)

Building these artifacts is a science-laden, once-per-build decision exercise — not a
mechanical format conversion. The full theory lives in **TE-RNAseq-toolkit v2.0.3 —
`docs/METHODOLOGY.md`** (version-pinned; do not duplicate). The builder must internalize:

- **Subfamily grouping is the deliberate quantification unit, not a shortcut**
  (`METHODOLOGY.md:85-87`). The grouped `GeneID = Subfamily:Family:Class` is what
  *causes* featureCounts to pool all loci of a subfamily into one meta-feature
  (~1,243 for mm39). Locus-unique GeneIDs instead give ~3.7M rows with signal diluted
  and lower statistical power — that needs a different tool (Telescope/SQuIRE),
  `METHODOLOGY.md:86-87,177`.
- **Exon subtraction is a hard precondition, not optional cleanup**
  (`METHODOLOGY.md:76-83`). Without `_noExon`, a read in a gene-embedded TE is counted
  twice, inflating library size and breaking normalization/FDR. Always *verify 0
  residual overlap* after subtracting (step 3e).
- **Integer Random-One coupling** (`METHODOLOGY.md:17-29`). The SAF is paired with the
  STAR Random-One contract (`--outSAMmultNmax 1`) so each fragment contributes exactly
  1 count; this is why featureCounts uses `-M` *without* `--fraction`. The interval SAF
  itself is format-agnostic, but the builder must know which counting contract it feeds.
- **Class composition (keep-all vs retro-only)** (`METHODOLOGY.md` + `13036-DM/README.md:287`).
  The canonical no-exon SAF keeps **all** RepeatMasker classes (LINE/SINE/LTR/DNA/RC/
  Simple_repeat/...); a builder *may* whitelist retrotransposons (`^(LINE|SINE|LTR|RC)$`)
  to stop simple/low-complexity repeats dominating counts, but the canonical decision is
  "keep all, filter downstream."
- **Stated limitation to disclose** (`METHODOLOGY.md:174-179`): the subfamily artifact
  cannot claim *which* specific insertion is active; Random-One is stochastic per read.
  Fit for subfamily-activity questions only.

---

## Outputs, naming convention, provenance

For each build, you produce (canonical mm39 names; substitute the build prefix for
other species):

- `GRCm39_Ensembl_rmsk_TE.gtf.gz` — the downloaded TEtranscripts TE GTF.
- `GRCm39_rmsk_TE_GROUPED_all.saf` — grouped SAF (intermediate).
- `GRCm39_rmsk_TE_GROUPED_all_noExon.saf` — exon-subtracted grouped SAF (the
  shared counting input).

**Naming convention:** `<BUILD>_rmsk_TE_GROUPED_all[_noExon].saf`, `GeneID =
Subfamily:Family:Class`, columns `GeneID Chr Start End Strand` (1-based, TSV). Home
directory: `/data1/shared/ref/<species>/<provider>/<build>/`.

**Provenance note:** record every build using
`references/reference-build-record-template.md` — genome build, TE-GTF source URL +
date + md5, gene GTF used for the exon BED, the exact `build_te_saf.sh` command,
output paths + md5s, and the class-composition choice. This closes the
acquisition/build provenance gaps that artifact 08 flagged.

---

## Verification Checklist

After building, confirm:

- [ ] **Grouped SAF labels:** `cut -f1 *_GROUPED_all.saf | tail -n +2 | head` shows
  `Subfamily:Family:Class` (e.g. `L1Md_A:L1:LINE`).
- [ ] **Group count sane:** `cut -f1 *_GROUPED_all.saf | tail -n +2 | sort -u | wc -l`
  ≈ 1,243 for mm39 (a few-k for other mammalian builds).
- [ ] **0 residual exon overlap:** `bedtools intersect -a te_grouped_noExon.bed -b
  exons.bed -u | wc -l` is **0**.
- [ ] **Group count preserved:** unique groups in `_noExon.saf` ≈ unchanged after
  subtraction.
- [ ] **Column format:** header is `GeneID\tChr\tStart\tEnd\tStrand`; Start is 1-based.
- [ ] **Provenance recorded:** a filled `reference-build-record-template.md` exists with
  source URL, md5s, and the exact build command.

---

## Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `bedtools subtract` removes nothing (0 overlaps where many expected) | Contig naming mismatch (`chr1` vs `1`) — silent zero-overlap trap | Normalize BOTH BEDs to the same convention first (step 3c); Ensembl mm39 has no `chr`. |
| Downstream `parse_te_id` fails / unparseable labels | SAF `GeneID` not in 3-field `Subfamily:Family:Class` order | Build with the verbatim awk in step 2; keep `gene_id:family_id:class_id` order. |
| `match($0,/.../,arr)` errors | awk is mawk, not GNU awk (3-arg `match` is gawk) | Use `gawk`; the build script checks for it. |
| Different no-exon SAF across datasets | Rebuilt with a different gene GTF / borrowed sibling-project GTF | Build once per genome build; derive the exon BED from the canonical gene GTF; record provenance. |
| Simple/low-complexity repeats dominate counts | Kept all classes when retro-only was wanted | Optional `--keep-classes '^(LINE|SINE|LTR|RC)$'`; canonical default is keep-all, filter downstream. |

---

## Handoff to star-te-preprocessing

Once `*_GROUPED_all_noExon.saf` exists for the build, hand it to
`star-te-preprocessing` as the TE SAF (`-e`) for the featureCounts TE pass. That
skill owns the per-dataset usage contract (Random-One STAR args, integer `-M` no
`--fraction`, strandedness discipline). Do not rebuild the reference per dataset —
all datasets on the same build reuse this one file.

---

## Resources

- **Build script (owned):** `scripts/build_te_saf.sh` — steps 2–3 as a deterministic, awk/bedtools-only executable.
- **Build record template:** `references/reference-build-record-template.md`.
- **Downstream consumer:** `star-te-preprocessing/SKILL.md` and `star-te-preprocessing/references/te-counting-workflow.md`.
- **Methodology / rationale** (subfamily vs locus, exon subtraction, Random-One, class composition): TE-RNAseq-toolkit **v2.0.3** — `docs/METHODOLOGY.md` (version-pinned; pointed to, not copied).
- **TE GTF source:** TEtranscripts — https://www.mghlab.org/software/tetranscripts
- **TE-ID parser** (label `Subfamily:Family:Class`): TE-RNAseq-toolkit — `R/te_utils.R::parse_te_id`.

---

## When not to use

- Do not use per-dataset — these artifacts are built once per genome build and reused across every dataset. For the per-run alignment+counting recipe use star-te-preprocessing.
- Do not use for locus-level TE references — this builds subfamily-grouped SAFs (one meta-feature per subfamily). For copy-resolved/locus-level annotations use Telescope or SQuIRE.
- Do not use to build a combined gene+TE GTF or a Dfam annotation — the TE source here is the TEtranscripts pre-generated RepeatMasker GTF, kept separate from the gene GTF.

---

## See also

This skill sits **upstream** of `star-te-preprocessing` in the handoff graph:
`te-reference-saf-build → star-te-preprocessing → annotate-bulk-rnaseq-data → bulk-rnaseq-gsea`. For locus-level / copy-resolved TE quantification (out of scope here), see SQuIRE/Telescope (external).

- `star-te-preprocessing` — Next step; downstream consumer of the no-exon SAF for per-dataset STAR alignment + featureCounts
