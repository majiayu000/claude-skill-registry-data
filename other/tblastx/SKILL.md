---
name: tblastx
description: Use when searching nucleotide sequences against a nucleotide database using translated protein comparison. Useful for detecting distant evolutionary relationships between nucleotide sequences.
disable-model-invocation: true
user-invocable: true
---

# tblastx

## Quick Start
- **Command:** `tblastx -query <nucleotide_file> -db <nucleotide_db> -out <results>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/tblastx`
- **Version:** 2.17.0+
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Compare nucleotide queries against nucleotide targets at the translated-protein level.
- Detect coding-region homology between divergent nucleotide sequences when `blastn` is too insensitive.
- Compare transcripts, contigs, or coding fragments across distant taxa.
- Prefer `blastn` for close nucleotide homology and `blastx` or `tblastn` when only one side should be translated.

## Common Patterns

```bash
# 1) Standard translated-vs-translated search against a nucleotide BLAST database
tblastx \
  -query transcripts.fa \
  -db nt_db \
  -outfmt "6 qaccver saccver pident length evalue bitscore qcovhsp frames" \
  -evalue 1e-5 \
  -max_target_seqs 20 \
  -num_threads 8
```

```bash
# 2) One-off query-vs-subject comparison with explicit genetic codes
tblastx \
  -query transcripts.fa \
  -subject targets.fa \
  -query_gencode 11 \
  -db_gencode 11 \
  -outfmt 7
```

```bash
# 3) Restrict query orientation when strand is known
tblastx \
  -query transcripts.fa \
  -db nt_db \
  -strand plus \
  -outfmt 6
```

## Recommended Workflow

1. Confirm that both query and target data are nucleotide and biologically expected to contain coding signal.
2. Decide whether the target is a BLAST database or a one-off FASTA subject.
3. Set `-query_gencode` and `-db_gencode` explicitly when organellar or nonstandard codes are plausible.
4. Treat hits as translated coding evidence and validate them with ORF-aware or annotation-aware follow-up tools.

## Guardrails

- Both query and target must be nucleotide sequences.
- `-db` and `-subject` are mutually exclusive.
- `tblastx` is computationally expensive because both sides are translated in six frames.
- Use `-help` rather than `--help`; `--version` also errors in this BLAST+ build.
- `-remote` is incompatible with local threading.
