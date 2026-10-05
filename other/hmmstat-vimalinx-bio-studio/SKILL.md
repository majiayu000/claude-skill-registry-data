---
name: hmmstat
description: Use when you need to inspect and summarize statistics for HMM (profile hidden Markov model) files from the HMMER suite.
disable-model-invocation: true
user-invocable: true
---

# hmmstat

## Quick Start
- **Command:** `hmmstat <hmmfile>`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/hmmstat`
- **Version:** HMMER 3.4
- **Full reference:** See `references/help.md`

## When To Use This Tool

- Sanity-check an HMM file after `hmmbuild` or before `hmmpress`.
- Inspect model counts and basic summary statistics in a profile collection.
- Confirm that a file is parseable as a valid HMMER profile library before heavier downstream jobs.

## Common Patterns

```bash
# 1) Print summary statistics for one HMM collection
hmmstat profiles.hmm
```

```bash
# 2) Inspect a large library and page through the summary
hmmstat Pfam-A.hmm | less -S
```

## Recommended Workflow

1. Run `hmmstat` immediately after generating or downloading a profile collection.
2. Check that the number of models, alphabet expectations, and general summary layout look plausible.
3. If the file is structurally sound, move on to `hmmpress`, `hmmsearch`, `hmmscan`, or `hmmfetch`.
4. If the summary is surprising, inspect the source HMM file before investing compute in longer searches.

## Guardrails

- This is a read-only reporting tool; it does not repair or modify HMM files.
- It expects exactly one positional HMM file argument.
- Use `-h` for help; `--help` and `--version` are not accepted here.
- Treat its text output as a summary for humans first; if you need machine-stable metadata, keep the original HMM file around too.
