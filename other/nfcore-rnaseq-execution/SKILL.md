---
name: nfcore-rnaseq-execution
description: >-
  Use when you have bulk RNA-seq FASTQs and need STAR BAMs / gene counts
  via nf-core/rnaseq (Docker, star_salmon) — samplesheet, container UID,
  disk, resource caps, -resume, cleanup. For the TE-specific recipe also
  load star-te-preprocessing. For 10x velocity alignment use
  starsolo-spliced-unspliced. For annotation/DE use annotate-bulk-rnaseq-data.
license: MIT
---

# nf-core/rnaseq Execution

## Overview

Operational runbook for executing **nf-core/rnaseq** (Nextflow, Docker profile, `star_salmon`) reproducibly on a workstation/HPC where disk and container UID are the real failure points. It owns the *generic run mechanics*: samplesheet construction, the Docker `NXF_UID`/`NXF_GID` trick, putting work/temp on the big ephemeral disk, `maxForks` resource caps, `-resume`, and the post-run verify + cleanup discipline (the Golden Rule).

It does **not** own the science of what the aligner does — the TE-compatible STAR args, `te_star.config`, and featureCounts recipe live in `star-te-preprocessing`, which this skill points to (SSoT: point, never copy).

The canonical recipe is reconstructed from the proven 13036-DM and AdaW_eWAT_WL runs, which used `-r 3.20.0`. The current latest is `-r 3.26.0`. **Pin `-r` explicitly every run** — changing the version can shift STAR/tool defaults, so the TE recipe must be re-validated against whichever version a run pins (a Phase V decision; this skill does not assert which version the next run uses).

## Routing

```
Need to run nf-core/rnaseq on bulk FASTQs?
│
└─ Is this a TE (transposable-element) run?
   (signal: grouped-SAF featureCounts, multimapper retention,
    a te_star.config with --extra_star_align_args)
   ├─ YES → use THIS skill for run mechanics AND ALSO load
   │        star-te-preprocessing for the canonical
   │        --extra_star_align_args + featureCounts + te_star.config.
   └─ NO  → use THIS skill alone; omit --extra_star_align_args.
```

(Non-RNA-seq cases — single-cell velocity, count-matrix DE — are covered by frontmatter `contraindications`.)

---

## Quick Start

Shortest reproducible path. Substitute `PROJ` and the data/outdir paths.

```bash
# 1. Docker must run as YOU, not 1000:1000 — export BEFORE launch (see Pitfalls).
export NXF_UID=$(id -u)
export NXF_GID=$(id -g)

# 2. Temp dir on the big ephemeral disk, owned by you, bind-mounted to container /tmp.
sudo mkdir -p /data2/nxf_tmp && sudo chown "$USER" /data2/nxf_tmp && chmod 775 /data2/nxf_tmp

PROJ=14839-DM
DATA=/data1/users/antonz/data/DMLab/incoming/${PROJ}/data
OUT=/data1/users/antonz/data/.../${PROJ}/results_mm39_TE

# 3. Build the samplesheet with the shipped, tested helper (handles multi-lane).
#    Same sample id on multiple rows -> nf-core concatenates the reads. strandedness
#    defaults to `auto` (pipeline infers + verifies via MultiQC; see below).
#    Add --seq-platform ILLUMINA to append a seq_platform column (BAM PL tag).
scripts/make_samplesheet.sh "$DATA" auto > "$DATA/samplesheet.csv"

#    Not Illumina-with-lane? Name the grammar — it is never guessed. See "Samplesheet
#    grammars" below, which also carries the single-end rule.
#      --pattern novogene            <sample>_{1,2}.fq.gz
#      --pattern bare --single-end   <sample>.fastq.gz, one sample per file

mkdir -p /data2/nf-work/${PROJ}/work

# 4. GENERIC launch skeleton (plain bulk RNA-seq). For a TE run, add the
#    -c te_star.config and --extra_star_align_args '...' from star-te-preprocessing.
nextflow run nf-core/rnaseq -r 3.26.0 -profile docker \
  -c <config> \
  --project "${PROJ}" \
  --input "$DATA/samplesheet.csv" \
  --outdir "$OUT" \
  --aligner star_salmon \
  --fasta /data1/shared/ref/mouse/Ensembl/mm39/GRCm39.genome.fa.gz \
  --gtf   /data1/shared/ref/mouse/Ensembl/mm39/gencode.vM37.primary_assembly.annotation.gtf.gz \
  --save_reference --save_align_intermeds --skip_qualimap \
  -work-dir /data2/nf-work/${PROJ}/work \
  -with-report "$OUT/../report.html" \
  -with-timeline "$OUT/../timeline.html" \
  -with-dag "$OUT/../flowchart.png" \
  -resume
```

The modern interactive launcher is equivalent and prompts/validates params:
`nf-core pipelines launch nf-core/rnaseq -r 3.26.0`. The classic `nextflow run` above is what the dataset records reproduce verbatim — both are supported.

**For TE runs**, `<config>` is `star-te-preprocessing/references/te_star.config` and you append the full `--extra_star_align_args '...'` string — both **owned by `star-te-preprocessing`**. Load that skill and copy the config as a frozen run snapshot; do not maintain a second editable copy.

**Verify the launch:** the banner resolves to your pinned `-r` (e.g. `[3.26.0]`); `report.html`/`timeline.html`/`flowchart.png` appear; containers write files owned by you (not root/1000).

> Full option detail (samplesheet columns, strandedness=auto, fq lint, BAM reprocessing, rRNA removal incl. GPU path) lives in **`references/nfcore-options.md`**.

---

## Samplesheet grammars

`scripts/make_samplesheet.sh` reads **one flat directory** and matches every FASTQ in it against **one** grammar, named with `--pattern`:

| `--pattern` | Filenames | Sample name |
|---|---|---|
| `illumina` (default) | `<sample>_S<n>[_L<lane>]_R{1,2}_001.fastq.gz` | the part before `_S<n>` |
| `novogene` | `<sample>_{1,2}.fq.gz` | the part before `_{1,2}` |
| `bare` | `<sample>.fastq.gz` \| `<sample>.fq.gz` | the whole stem; requires `--single-end` |

The lane field is optional inside `illumina`, so BCLConvert output with and without `_L00N` reads the same way.

Three rules, each of which exists because of a specific way this fails:

- **The grammar is named, never guessed,** and there is no fallback from one to the next. A directory that half-matched would otherwise produce a plausible samplesheet covering part of the data.
- **Every FASTQ in the directory is accounted for.** A file the grammar does not match is an error. A narrow `*_R1_001.fastq.gz` glob is precisely how an orphan R2, or a second naming convention in the same directory, goes unnoticed.
- **Single-end is never inferred from absent mates.** `--single-end` is required. A truncated transfer that dropped every R2 would otherwise yield a clean single-end samplesheet for a paired-end experiment, and the run would finish and report wrong numbers. Under `--single-end`, a present mate is a contradiction and an error.

`bare` strips only the extension, on purpose: real single-end submissions name files `<run>_<well>_<index>.fastq.gz`, so stems like `RUN_1_1` and `RUN_16_16` occur, and a "trailing `_1`/`_2` is a mate marker" heuristic would maul exactly the data this mode serves. It does warn on stderr when stems pair as `X_1`/`X_2`, which is what picking `bare` on a paired directory looks like.

macOS AppleDouble `._*` files are excluded before classification, with the count reported on stderr — one arrives beside every file a Mac touches, and they match every `*_R1_001.fastq.gz` glob.

**Merging across directories is the caller's job.** The script reads one directory and never rewrites a derived sample name. When two sequencing runs of the same libraries must merge — a depth top-up on a second flowcell, say — run it once per directory and combine with an **explicit mapping table** (`source_run`, `derived_sample`, `canonical_sample`), committed with the run record. A regex buried in a shell pipeline cannot tell a reviewer months later *why* a row carries the sample name it does; a table can. Then assert per-sample source membership, not just the row and sample totals: 21 samples and 42 rows is equally consistent with one sample carrying two rows from the same flowcell.

---

## Pipeline Architecture

Two storage tiers, deliberately separated:

| Tier | Path | Role | Lifetime |
|---|---|---|---|
| **Results** (stable) | `/data1/.../<proj>/results_mm39_TE/` | Raw FASTQ + **published** STAR/Salmon outputs | Durable — NEVER cleaned by housekeeping |
| **Work** (ephemeral) | `/data2/nf-work/<proj>/work/` | Nextflow task scratch, intermediate SAM/BAM | Disposable after a sample is verified complete |
| **Temp** | `/data2/nxf_tmp/` → container `/tmp` | Java/STAR temp, bind-mounted | Disposable |

`te_star.config` enforces this: `workDir = /data2/nf-work/${params.project}/work`, Docker `-v /data2/nxf_tmp:/tmp`, and `NXF_OPTS=-Djava.io.tmpdir=/tmp`, `TMPDIR=/tmp`, `NXF_TEMP=/tmp`. The split exists because STAR SAM/BAM temp files are 50–80 GB each and `/data2` (a 7.3 T HDD) hits disk pressure → exit 137.

---

## Disk / Housekeeping

**Prevention (baked into the config):**
- `maxForks` caps: global `12`, `STAR_ALIGN maxForks=2`, `STAR_GENOMEGENERATE=1` → fewer simultaneous huge temp files.
- `--skip_qualimap` — Qualimap thrashes on HDDs.
- `--save_align_intermeds = true` — **load-bearing**: keeps the unsorted `Aligned.out.bam` that TE featureCounts consumes, and writes `<outdir>/samplesheets/samplesheet_with_bams.csv` for cheap reprocessing (see options cheatsheet). Do not disable for TE work.

**Post-run cleanup (logic; the historical scripts live in per-dataset `/scratch` dirs and can be templated):**
- **verify** (`verify_samples.sh` logic): a sample is **COMPLETE** only if all 6 published BAMs exist (`Aligned.out.bam`, `Aligned.toTranscriptome.out.bam`, `sorted.bam`+`.bai`, `markdup.sorted.bam`+`.bai`) — else `NOT_STARTED`/`INCOMPLETE`.
- **cleanup** (`cleanup_completed_samples.sh` logic): for COMPLETE samples whose work `.exitcode == 0`, delete large work files (`*.bam`/`*.sam`/`*.fastq.gz`) and STAR/Picard temp dirs (`_STARtmp`/`_STARpass1`/`_STARgenome`/`tmp`); **keep** `.command.*`, `.exitcode`, `versions.yml` so `-resume` still works. Always dry-run first (`DRY_RUN=1`) before `DRY_RUN=0`.

> **The Golden Rule:** never delete a work file that (a) lacks a published equivalent, (b) belongs to a failed process (`exitcode ≠ 0`), or (c) belongs to an unverified/incomplete sample. Incomplete samples' work dirs MUST be preserved for `-resume`.

---

## Verification Checklist

After the run, confirm:

- [ ] **Revision pinned:** log shows your intended `-r` (e.g. `[3.26.0]`).
- [ ] **Ownership correct:** files in the outdir/work dir are owned by you, not `root`/`1000`.
- [ ] **All samples COMPLETE:** verify step reports every sample with all 6 BAMs present; `.exitcode == 0`.
- [ ] **TE input present** (TE runs): `star_salmon/<sample>/Aligned.out.bam` (unsorted) exists in the outdir.
- [ ] **Deliverables emitted:** `report.html`, `timeline.html`, `flowchart.png`, `multiqc_report.html`, `versions.yml`.
- [ ] **Strandedness recorded:** capture the inferred call from MultiQC's "Strandedness checks" section and reconcile it with the featureCounts gene `-s` used downstream.
- [ ] **Cleanup safe:** only verified-complete, exit-0 work dirs were pruned; incomplete ones preserved.

---

## Common Pitfalls

### Pitfall: GENCODE GTF halts the biotype featureCounts

- **Symptom:** `SUBREAD_FEATURECOUNTS` exits 255 with `ERROR: failed to find the gene identifier attribute in the 9th column of the provided GTF file.`
- **Cause:** `featurecounts_group_type` defaults to `gene_biotype`, the Ensembl spelling. GENCODE writes `gene_type`.
- **Fix:** set `featurecounts_group_type = 'gene_type'` for GENCODE, `'gene_biotype'` for Ensembl. Confirm first: `zcat ann.gtf.gz | head -1 | grep -o 'gene_type\|gene_biotype'`.

### Pitfall: a bare boolean flag fails schema validation

- **Symptom:** the run stops in ~30 s with `--save_reference (true): Value is [string] but should be [boolean]`.
- **Cause:** Nextflow 26.x passes a bare `--flag` as the string `"true"`, and nf-core 3.26.0 type-checks parameters against its JSON schema.
- **Fix:** declare booleans in a `params {}` block in a `-c` config, where Groovy types them.

### Pitfall: a retryable exit code masks a deterministic error

- **Symptom:** the reported failure names a resource or scheduler problem while the real cause sits in the `Command error:` block above it.
- **Cause:** tools reuse exit codes an `errorStrategy` treats as transient. featureCounts exits 255 on a fatal GTF error, and 255 also marks a node-level container failure. Each retry escalates `cpus` and `memory` by `task.attempt`, so attempt 3 can request more than the partition holds.
- **Fix:** read the `Command error:` block first, and treat the terminal message as the last symptom. Size the queue-selection threshold to the schedulable memory a node offers: subtract Slurm's `MemSpecLimit` from `RealMemory`, and confirm with `sbatch --test-only -p <queue> --mem <N>M --wrap true`.

### Pitfall: Containers run as 1000:1000 → permission crash

- **Symptom:** `touch: .command.trace: Permission denied`; outputs owned by root/`1000`.
- **Cause:** `NXF_UID`/`NXF_GID` not exported **before** `nextflow run`, so `docker.runOptions` falls back to `-u 1000:1000`.
- **Fix:** `export NXF_UID=$(id -u); export NXF_GID=$(id -g)` BEFORE launch. Do **not** use `NXF_DOCKER_OPTS="-u ..."` — wrong mechanism; rely on the config's `docker.runOptions`.

### Pitfall: `/data2/nxf_tmp` missing or wrong ownership

- **Symptom:** container `/tmp` write failures, exit 1.
- **Cause:** the bind-mount source doesn't pre-exist or isn't owned by you.
- **Fix:** `sudo mkdir -p /data2/nxf_tmp && sudo chown $USER /data2/nxf_tmp && chmod 775` before launch.

### Pitfall: fq lint stops the workflow

- **Symptom:** an `FQ_LINT` / `FQ_LINT_AFTER_TRIMMING` error halts the run.
- **Cause:** fq lint runs by default at start and after each FASTQ-manipulating step; a lint error is fatal. The paired-read-name check (`P001`) is the usual false-positive — but it is already disabled by default (`--disable-validator P001`).
- **Fix:** if a different validator misfires on usable FASTQs, disable it via `--extra_fqlint_args` (see options cheatsheet) rather than skipping lint wholesale.

### Pitfall: strandedness assumed instead of read off MultiQC

- **Symptom:** gene counts look wrong / antisense-dominated.
- **Cause:** strandedness is **per-library** (genes were `-s 2` for 13036-DM but `-s 1` for AdaW). `auto` lets the pipeline infer it, but the downstream featureCounts gene `-s` is set manually and must match.
- **Fix:** `auto` subsamples 1M reads, infers strand via Salmon, and reports it in MultiQC's "Strandedness checks" (Salmon vs RSeQC, pass/fail). Read the inferred value there and set the gene `-s` to match; record it.
- **Read both inferences.** `multiqc_report_data/multiqc_strand_check_summary_table.txt` holds `salmon_inferred`, `rseqc_inferred` and a per-library `status`. Agreement across all libraries is the evidence to record.
- **Forward-stranded libraries occur.** XRS106 read `forward` on both inferences for 21 of 21 libraries, Salmon `expected_format: ISF` at 98.8–99.6% sense. `forward` maps to featureCounts `-s 1`, Salmon `ISF`, HTSeq `--stranded=yes`; `reverse` maps to `-s 2`, `ISR`, `--stranded=reverse`.
- **The TE sense/antisense channels follow the dataset.** A reverse-stranded library counts sense at `-s 2` and antisense at `-s 1`; a forward-stranded one mirrors that, sense at `-s 1` and antisense at `-s 2`. Derive both from the measured value per dataset.
- **A forward reading describes the chemistry, and coverage identifies the assay.** Check Qualimap `5'-3' bias` alongside it: a value near 1 with comparable `5' bias` and `3' bias` marks a full-length library, and a 3'-tag assay concentrates coverage at the 3' end.

### Pitfall: deleting work files breaks `-resume` (or loses data)

- **Symptom:** `-resume` re-runs everything; or an incomplete sample's intermediates are gone.
- **Cause:** cleanup ran on unverified/failed/incomplete work dirs, or removed `.command.*`/`.exitcode`.
- **Fix:** apply the Golden Rule; keep `.command.*`/`.exitcode`/`versions.yml`; dry-run first. `-resume` is always used.

### Pitfall: exit-code vocabulary

- **Symptom:** task fails with a numeric code.
- **Cause/Fix:** `137` = OOM (disk/RAM — check `/data2` free space, lower `maxForks`); `1` = I/O/write failure (check `/tmp` mount, ownership); `104` = STAR wrong read-ID format (often a failed gzip decompression).

---

## Resources

- **nf-core/rnaseq docs:** https://nf-co.re/rnaseq/3.26.0
- **Nextflow docs:** https://www.nextflow.io/docs/latest/
- **Options cheatsheet:** `references/nfcore-options.md` (samplesheet, strandedness=auto, fq lint, BAM reprocessing, rRNA/GPU)
- **TE recipe + canonical config:** `star-te-preprocessing/references/te_star.config` (owner — do not duplicate)
- **Per-dataset provenance template:** `references/dataset-record-template.md` (instantiate per run)
- **Samplesheet generator:** `scripts/make_samplesheet.sh` — three grammars, explicit single-end; see "Samplesheet grammars" (tested; `tests/run_skill_tests.sh`)

---

## When not to use

- Do not use for 10x single-cell velocity alignment. Use starsolo-spliced-unspliced instead.
- Do not use for count-matrix annotation, DE, enrichment, or interpretation. Use annotate-bulk-rnaseq-data, then the appropriate downstream skill.
- Do not use for chromatin or ATAC preprocessing. Use cellranger-arc-multiome or snapatac2-atac-preprocessing.

---

## See also

- `star-te-preprocessing` — Co-load for TE runs; owns the TE-compatible STAR `--extra_star_align_args` + featureCounts SAF recipe (`te_star.config`) this skill points to
- `annotate-bulk-rnaseq-data` — Next step (downstream); annotate / build DGEList / run DE on the resulting count matrices
