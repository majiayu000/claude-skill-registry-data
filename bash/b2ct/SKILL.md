---
name: b2ct
description: Use when converting ViennaRNA-style sequence-plus-dot-bracket records on stdin into RNA connectivity-table output.
disable-model-invocation: true
user-invocable: true
---

# b2ct

b2ct is a small legacy ViennaRNA converter that turns a sequence plus structure record into CT-format rows. The only confirmed healthy path in this environment is stdin-driven conversion to stdout.

## Quick Start

- **Command:** `b2ct`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/b2ct`
- **Confirmed positive path:** `printf '>test\nAAAA\n.... (0.00)\n' | b2ct`

## When To Use This Tool

- Convert a ViennaRNA / RNAfold-like record into CT rows for downstream structure tooling.
- Inspect a single dot-bracket structure in a tabular partner-index layout.
- Turn ephemeral stdin structure output into a file you can archive or pass downstream.

## Common Patterns

```bash
# 1) Convert a simple structure record from stdin
printf '>test\nAAAA\n.... (0.00)\n' | b2ct
```

```bash
# 2) Save CT output to a file
printf '>test\nAAAA\n.... (0.00)\n' | b2ct > test.ct
```

```bash
# 3) Reuse an existing RNAfold-style output file through stdin redirection
b2ct < fold.out > fold.ct
```

## Recommended Workflow

1. Normalize the input to the ViennaRNA-style three-line form: record name, sequence, and dot-bracket structure with optional energy in parentheses.
2. Feed the record through stdin or shell redirection rather than relying on a positional filename.
3. Capture stdout into a `.ct` file if you need to reuse the result.
4. Verify sequence length and bracket balance before trusting the CT table downstream.

## Guardrails

- No real help or version interface was observed: bare `b2ct` and `b2ct -h` were both silent in local testing.
- The confirmed positive path is stdin to stdout. In contrast, `b2ct fold.out` exited `0` but produced no stdout and no sidecar file in repeated smoke tests.
- Live good input `printf '>test\nAAAA\n.... (0.00)\n' | b2ct` emitted CT rows beginning with `4 ENERGY = 0.0    test`.
- An invalid sample with mismatched sequence and structure lengths emitted `sequence and structure have unequal length`.
- Binary strings also expose an `unbalanced brackets` error path, so bracket balance matters even if you do not hit it in the happy path.
- The converter writes CT text to stdout on the confirmed path; it does not automatically create a `.ct` file for you.
