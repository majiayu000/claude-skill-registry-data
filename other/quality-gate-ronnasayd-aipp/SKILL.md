---
name: quality-gate
description: Run or explain the ratchet-style quality gate (scripts/quality-gate.js) for Node/TS projects — lint violations, code duplication %, test coverage %, and files over a line-count limit compared against a frozen baseline. Use when the user says "run the quality gate", "check quality-gate.js", "set up the ratchet gate", "update the baseline", "why did the quality gate fail", or wants to wire it into CI so PRs never regress quality metrics silently.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "3.0.0"
---

# Quality Gate

Ratchet-style quality gate for Node/TS projects. Runs eslint, jscpd, and jest itself (auto-run,
default on — prefers the project's local `node_modules/.bin/<tool>`, falls back to `npx <tool>`
when not installed), compares the results against a frozen, granular `baseline.json`, and fails on
any regression (even 0.1 point) in any leaf metric. Never improves the baseline on its own — only
`--update-baseline` advances it.

Script: `<skills-dir>/quality-gate/scripts/quality-gate.js` (this repo).

## Zero-config invocation

No paths to pass. Copy the script anywhere convenient and run it against the target project root:

```bash
node quality-gate.js --root /path/to/project
```

That's it. Everything else is automatic:

- **Intermediate collector reports** (eslint/jscpd/coverage JSON) are written to a fresh,
  collision-free directory under the OS tmp dir (`/tmp/quality-gate-<pid>-<random>` on Linux/macOS)
  and **deleted at the end of the run**, whether it passes, fails, or errors.
- **Durable output** — `baseline.json` and `quality-gate-report.md` — lives in a `.quality-gate/`
  directory at the target project's root (override with `--persist-dir`). This is the only thing
  that survives a run.

```
project root/
  .quality-gate/
    baseline.json              <- survives, is the ratchet's memory
    quality-gate-report.md     <- survives, latest run's report
```

## Flags

```
--root <path>          default: cwd                (target project to gate)
--max-lines <n>        default: 500                 (line-count threshold for "large file")
--persist-dir <path>   default: .quality-gate        (relative to --root; holds baseline+report — the only durable output)
--work-dir <path>      default: a fresh dir under the OS tmp dir (auto-deleted at the end)
--update-baseline      overwrite baseline.json with current metrics (advances the ratchet)
--no-auto-run          disable self-running eslint/jscpd/jest — require pre-generated reports in --work-dir
```

Only two directories are ever configurable — `--persist-dir` (what survives) and `--work-dir`
(scratch space). There is no way to point individual eslint/jscpd/coverage report paths anywhere
else; their filenames are fixed inside those two directories.

Passing `--work-dir` explicitly opts out of auto-cleanup — the script assumes you're managing that
directory yourself (e.g. a CI cache step) and leaves it alone. Only the default, auto-generated tmp
work-dir gets deleted automatically.

`--update-baseline` never triggers implicitly — only explicit. Use it right after a merged
refactor that legitimately improved the numbers.

Use `--no-auto-run` when you'd rather run eslint/jscpd/jest as separate, individually-logged CI
steps, or already have cached reports from a prior step — combine with `--work-dir` pointing at
wherever those reports were written.

| Situation                                            | Behavior                                                           |
| ---------------------------------------------------- | ------------------------------------------------------------------ |
| No `baseline.json` yet                               | Creates it from current metrics, prints a bootstrap notice, exit 0 |
| `baseline.json` exists, nothing regressed            | Writes `quality-gate-report.md`, exit 0                            |
| `baseline.json` exists, something regressed          | Writes `quality-gate-report.md` with per-metric delta, exit 1      |
| `baseline.json` malformed (bad JSON / missing field) | Fails naming the bad field, does NOT overwrite the file            |
| A report file is missing and `--no-auto-run` is set  | Fails naming the exact missing file, no subprocess spawned         |

## Reading the report

`quality-gate-report.md` has a `Status` line, then four sections in order:

- **Coverage** — 4-row table (lines/statements/functions/branches), baseline/current/Δ.
- **Duplication** — percentage + fragment count, baseline/current.
- **Violations** — total lint rule violations + oversized-file count, baseline/current/Δ.
- **Regressions** — bullet list of concrete per-file/per-rule regressions (a file that grew while
  already over the line limit, a complexity rule whose violations increased in a specific file),
  "None." when empty (never omitted — an absent section would be ambiguous with "didn't run").

`baseline.json` itself is granular too: coverage/duplication as separate fields, eslint broken
into `total` + `byRule` + `byComplexityRule` (complexity, max-depth, max-lines,
max-lines-per-function, max-params, max-statements), and `files`/`perFileByComplexityRule` maps
for oversized-file and per-file complexity regression tracking. Any single leaf regressing fails
the whole run — same ratchet philosophy as before, now over ~15-20 fields instead of 4.

## Wiring into CI (GitHub Actions)

Single step — the script runs eslint/jscpd/jest itself, no path flags needed:

```yaml
- run: node <path-to>/quality-gate.js --root .
  # non-zero exit here fails the job — that's the gate
- if: always()
  run: cat .quality-gate/quality-gate-report.md # or use it to post a PR comment
```

`.quality-gate/baseline.json` is the ratchet's memory — commit it to the repo so it persists
across CI runs. No cleanup step needed: intermediate collector output already lived in `/tmp` and
was deleted before the script returned.

Never prompts for input — behaves identically local and in CI (same auto-run collectors, same
deterministic exit code).

## Troubleshooting

- **"required file not found: .../eslint-report.json"** → with auto-run enabled (the default),
  this means the collector itself failed to produce output (e.g. eslint has no valid config in
  the target project) — check stderr from the run. With `--no-auto-run`, the report is expected
  to already exist inside `--work-dir`; the script never runs the collector for you in that mode.
- **"malformed baseline"** → someone hand-edited or truncated `baseline.json`, or the project is
  still on an older flat baseline shape. The script refuses to auto-overwrite a corrupt baseline —
  fix the named field manually, or delete `baseline.json` and let the script re-bootstrap from
  current metrics (loses ratchet history, same as any bootstrap).
- **Gate fails on a PR that only touched unrelated files** → any of the ~15-20 leaf metrics
  regressing anywhere in the repo fails the whole run; there's no per-file scoping in this
  version (see spec's "Accepted consequences").
- **Baseline feels stuck / too strict after a real improvement** → run with `--update-baseline`
  once, deliberately, after merging.
- **Want to inspect intermediate eslint/jscpd/coverage output** → pass your own `--work-dir`; the
  script won't delete a work-dir you supplied explicitly.
