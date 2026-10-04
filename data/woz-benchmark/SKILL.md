---
name: woz-benchmark
description: Compare WOZCODE vs vanilla Claude Code on the user's codebase — real cost, turn, and time savings. TRIGGER on "compare woz", "how much does woz save", "benchmark woz", "woz vs claude", "show me savings", or /woz-benchmark.
allowed-tools: Bash(node *), Bash(git *), Bash(ls *), Bash(test *), Bash(mkdir *), Bash(date *), Write, Read
---

# WOZCODE Savings Benchmark

Run a side-by-side comparison of WOZCODE vs vanilla Claude Code on the user's own codebase. Each prompt runs twice against a fresh copy of the repo with `git reset --hard` between runs, so the target MUST be a clean git repo.

TRIGGER: "compare woz", "how much does woz save", "benchmark woz", "woz vs claude", "show me the savings", "is woz worth it", or `/woz-benchmark`.

## Prerequisites

- User logged in to WOZCODE.
- Target directory is a git repo with a clean working tree.

## Steps

### 1. Gather inputs — BE BRIEF

Ask for all three in ONE short message (< 10 lines). Do not re-explain what the benchmark does — the user already invoked it.

1. **Target directory** — absolute path to a clean git repo to run the test on.
2. **Prompts** — 2–10 real coding tasks. Tell them briefly: "meaty feature/refactor/bugfix work, not one-liners — trivial prompts hide WOZCODE's advantage". If they don't have prompts in mind, offer to suggest some after looking at their repo.
3. **Environment setup** (optional) — one line: "Anything Claude needs already in place (DB seeded, services running, credentials in `.env`)? Skip if the repo is self-contained."

Do NOT ask about the model. Default to `opus` in the YAML config. Only switch to `sonnet` or `haiku` if the user volunteers a different choice in their answer.

### 2. Validate the target

Before writing any config, verify the target is usable:

```bash
test -d <target>
git -C <target> rev-parse --git-dir
git -C <target> status --porcelain
```

If the directory doesn't exist, isn't a git repo, or has uncommitted changes, STOP and tell the user how to fix it.

### 3. Write a temporary benchmark config

Use the Write tool to create a YAML file at `/tmp/woz-benchmark-<timestamp>.yaml` (get the timestamp from `date +%s`). Format:

```yaml
model: opus
maxTurns: 15
prompts:
  - "first prompt from the user"
  - "second prompt from the user"
setup:
  commands:
    - "curl -L https://example.com/dataset.csv -o data/sample.csv"
    - "psql $DATABASE_URL -f seed.sql"
```

Omit the entire `setup:` block if the user didn't give any environment setup commands.

### 4. Run the benchmark

One-line warning: "This'll take several minutes — each prompt runs twice." Then run:

```bash
node "${CODEX_HOME:-$HOME/.codex}/plugins/wozcode/scripts/benchmark.js" --target <target> --config <yaml-path> --user-env
```

`--user-env` loads the user's project `CLAUDE.md` hierarchy on BOTH sides. Do NOT pass `--screenshots`, `--codex`, `--judge`, or `--trace`.

### 5. Present the results as a savings report

The benchmark prints a detailed text report at the end. Relay the full report to the user, then add a clear, sales-oriented savings summary at the top. Compute the deltas from the report's totals.
