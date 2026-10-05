---
name: hmmpgmd
description: Use when running HMMER master or worker daemon services that front `phmmer`, `hmmsearch`, and `hmmscan` against cached databases.
disable-model-invocation: true
user-invocable: true
---

# hmmpgmd

## Quick Start

- **Command:** `hmmpgmd [options]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/hmmpgmd`
- **Full reference:** See `references/help.md` for the current startup failure; daemon behavior below is grounded in the local man page

## When To Use This Tool

- Use `hmmpgmd` when you need a persistent HMMER service rather than one-shot command-line searches.
- It stands in front of `phmmer`, `hmmsearch`, and `hmmscan`, caching one or more sequence databases and or HMM databases in memory for repeated client queries.
- Run one instance as a master and one or more others as workers when you want the master to distribute queries and merge results.

## Common Patterns

```bash
# Start a master with cached sequence and HMM databases
hmmpgmd --master --seqdb seqdb.hmmpgmd --hmmdb models.hmm
```

```bash
# Start a worker that connects to the master and uses 8 threads
hmmpgmd --worker 10.0.0.5 --seqdb seqdb.hmmpgmd --hmmdb models.hmm --cpu 8
```

```bash
# Pin non-default client and worker ports
hmmpgmd --master --seqdb seqdb.hmmpgmd --cport 51381 --wport 51382
```

## Recommended Workflow

1. Prepare at least one database: a sequence database in hmmpgmd format via `esl-reformat`, an HMM database from `hmmbuild`, or both.
2. Start the master first and wait until it reports that data are loaded into memory and the master is ready.
3. Start workers with the same database paths so they can load identical content and register with the master.
4. Only after master and workers are stable should clients submit `phmmer`, `hmmsearch`, or `hmmscan` style queries.
5. Keep master and workers running as long-lived services instead of treating them like one-shot jobs.

## Guardrails

- The local executable currently fails to start because `libopenblas.so.0` is missing, so live `-h` validation is unavailable in this environment.
- `--seqdb` expects hmmpgmd-formatted protein sequence data, not raw FASTA; the local man page points to `esl-reformat` for creating that format.
- Workers must be able to access the same database file paths as the master.
- This is a daemon layer, not a general client. You still need separate client code to submit `@--seqdb` or `@--hmmdb` style queries.
