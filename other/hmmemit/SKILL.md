---
name: hmmemit
description: Use when sampling synthetic sequences, alignments, or consensus sequences from one or more profile HMMs.
disable-model-invocation: true
user-invocable: true
---

# hmmemit

## Quick Start

- **Command:** `hmmemit [-options] <hmmfile>`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmemit`
- **Help reference:** See `references/help.md` for `--help` failure behavior and `hmmemit -h` output

## When To Use This Tool

- Use `hmmemit` when you need synthetic positives or consensus representatives derived from profile HMMs.
- Default mode samples unaligned sequences from the core probability model; `-a` emits alignments, `-c` emits simple consensus sequences, `-C` emits thresholded fancy consensus sequences, and `-p` samples from the fully configured search profile.
- It is useful for benchmark generation, smoke tests, demo data, or sanity-checking what a model prefers.

## Common Patterns

```bash
# Sample one sequence per model from the core model
hmmemit profiles.hmm > samples.fa
```

```bash
# Emit 20 aligned synthetic sequences per model
hmmemit -a -N 20 profile.hmm > emitted.sto
```

```bash
# Emit plurality-rule consensus sequences
hmmemit -c profile.hmm > consensus.fa
```

```bash
# Sample homolog-like sequences from the fully configured search profile
hmmemit -p -L 800 --glocal -N 10 profile.hmm > profile-samples.fa
```

## Recommended Workflow

1. Decide whether you want sampled sequences, alignments, or consensus output.
2. Set `-N` and `--seed` before generating benchmark data so the run is reproducible and large enough for the test you care about.
3. Use `-p` only when you explicitly want search-profile behavior such as local or glocal configuration and length modeling.
4. Redirect the emitted output immediately into a named FASTA or Stockholm file.
5. If you generated multiple models' output from a library, keep the original HMM names so downstream provenance remains clear.

## Guardrails

- `-h` works; `--help` and `--version` are rejected by the local executable.
- Despite the short usage string saying `<hmmfile (single)>`, runtime testing shows the tool will iterate across a multi-model HMM library and emit output for each model.
- `-L`, `--local`, `--unilocal`, `--glocal`, and `--uniglocal` only apply with `-p`.
- `--minl` and `--minu` only make sense with `-C`.
- `hmmfile` may be `-` to read a profile stream from stdin.
