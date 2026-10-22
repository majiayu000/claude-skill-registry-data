---
name: oracle
description: >-
  Gets a second-model review by bundling a prompt and selected repository files into one request for
  another AI (API or browser), for debugging, refactoring, or design questions. Use when an
  independent model's opinion would help; treat its answer as advisory.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
license: MIT
---

# Oracle (CLI) — Second-Model Review

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

## When to Use

- Getting a second-model review of code, architecture, or design
- Bundling prompts and files into a single request for another AI model
- Cross-validating agent output with an independent model

Oracle bundles your prompt + selected files into one "one-shot" request so another model can answer with real repo context (API or browser automation). Treat outputs as advisory: verify against the codebase + tests.

## Main Use Case

Default workflow: `--engine browser` targeting GPT-5 Pro in ChatGPT. This is the "human in the loop" path.

## Commands

```bash
# Show help
npx -y @steipete/oracle --help

# Preview (no tokens spent)
npx -y @steipete/oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"

# Token/cost sanity
npx -y @steipete/oracle --dry-run summary --files-report -p "<task>" --file "src/**"

# Browser run (main path; long-running is normal)
npx -y @steipete/oracle --engine browser --model gpt-5-pro -p "<task>" --file "src/**"

# Manual paste fallback (assemble bundle, copy to clipboard)
npx -y @steipete/oracle --render --copy -p "<task>" --file "src/**"
```

## Attaching Files (`--file`)

`--file` accepts files, directories, and globs. Pass it multiple times:

```bash
# Include directory glob
--file "src/**"

# Include specific file
--file src/index.ts

# Exclude (prefix with !)
--file "src/**" --file "!src/**/*.test.ts" --file "!**/*.snap"
```

Default-ignored dirs: `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp`.

## Budget + Observability

- Target: keep total input under ~196k tokens.
- Use `--files-report` and/or `--dry-run json` to spot the token hogs before spending.

## Sessions + Reattachment

Sessions stored under `~/.oracle/sessions`. Runs may detach or take a long time.

```bash
# Don't re-run; reattach
oracle status --hours 72
oracle session <id> --render
```

## Prompt Template (high signal)

Oracle starts with **zero** project knowledge. Always include:

- Project briefing (stack + build/test commands + platform constraints).
- "Where things live" (key directories, entrypoints, config files).
- Exact question + what you tried + the error text (verbatim).
- Constraints ("don't change X", "must keep public API", "perf budget").
- Desired output ("return patch plan + tests", "list risky assumptions", "give 3 options with tradeoffs").

## Safety

- Don't attach secrets by default (`.env`, key files, auth tokens).
- Prefer "just enough context": fewer files + better prompt beats whole-repo dumps.
- **API runs require explicit user consent** before starting because they incur usage costs.
