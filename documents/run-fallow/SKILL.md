---
name: run-fallow
description: Run the `fallow` CLI (installed globally, config at .fallowrc.json in repo root) to analyze this codebase for dead code, duplication, complexity/health, and security candidates — and keep .fallowrc.json itself accurate (ignorePatterns, thresholds, entry points) when findings are noisy because the config is stale rather than the code being wrong. Use before refactoring, before opening a PR, when the user asks to "check for dead code", "find unused exports/deps", "find duplication", "check complexity/hotspots", "audit changed files", wants a codebase health report, or a fallow finding looks like a false positive. Always invoke with `--format json` and parse the output programmatically — never eyeball raw human-format output for anything beyond a quick spot check.
---

# Run Fallow

`fallow` is a read-only static analyzer for this TS/JS codebase (docs: https://www.fallow.tools/docs/). It is already installed globally and configured via [.fallowrc.json](../../../.fallowrc.json) at the repo root. It never modifies files unless you explicitly run `fallow fix` or `fix-apply`.

## Core rule: always use `--format json`

Human output is for a person skimming a terminal. For anything you're going to reason about or summarize, run with `--format json` (alias `--output json`) and parse it — don't paste raw JSON into a plan or response. Pipe to a file first:

```bash
fallow --format json > /tmp/fallow.json
```

Then read specific keys with `python3 -c "import json; ..."` or `jq`, rather than dumping the whole file. Fallow's JSON payloads can be tens of thousands of lines on a repo this size; only extract what you need.

Other formats exist (`human`, `sarif`, `compact`, `markdown`) — use `markdown` only when the output is going straight into a doc a human will read (e.g. a PR comment), not when you need to reason about the data yourself.

## Command map

| Agent intent                                      | Command                                                         |
| ------------------------------------------------- | --------------------------------------------------------------- |
| Full sweep (dead code + dupes + health)           | `fallow --format json`                                          |
| Unused files/exports/deps/types                   | `fallow dead-code --format json`                                |
| Prove a symbol is safe to delete                  | `fallow dead-code --trace <file>:<export> --format json`        |
| Prove a dependency is unused                      | `fallow dead-code --trace-dependency <name> --format json`      |
| Duplication / copy-paste                          | `fallow dupes --format json`                                    |
| Complexity + maintainability                      | `fallow health --format json`                                   |
| Rank what to refactor first                       | `fallow health --hotspots --targets --format json`              |
| File-level risk scores                            | `fallow health --file-scores --format json`                     |
| Enforce this repo's ≤10 cyclomatic rule           | `fallow health --max-cyclomatic 10 --complexity --format json`  |
| Review a PR / changed files only                  | `fallow audit --format json` (exits non-zero on fail verdict)   |
| Human-readable orientation brief for a diff       | `fallow audit --brief` (always exits 0)                         |
| Architecture rules before editing a file          | `fallow guard <files>`                                          |
| Security candidates (unverified, need review)     | `fallow security --format json`                                 |
| Feature flags in use                              | `fallow flags --format json`                                    |
| Inspect one file/symbol before editing            | `fallow inspect --file <path> --format json`                    |
| Project shape (entry points, plugins, boundaries) | `fallow list --entry-points --files --boundaries --format json` |
| Explain a rule without running analysis           | `fallow explain <issue-type>`                                   |

Scope any of the above to changed files with `--changed-since <ref>` where supported, instead of re-running full-repo analysis for small edits.

## Reading this codebase's fallow config

[.fallowrc.json](../../../.fallowrc.json) sets `entry: ["src/index.*", "src/main.*"]` (Gatsby's real entry points — `gatsby-*.js` — are ignored), and `duplicates.minOccurrences: 3`. Don't assume defaults; check this file (or `fallow config`) before interpreting a result as a false positive.

## This codebase's own bar (from CLAUDE.md)

Fallow's default complexity threshold (`--max-cyclomatic 20`) is looser than this repo's actual standard: **cyclomatic complexity ≤ 10 per function** (see [CLAUDE.md](../../../CLAUDE.md)), no switch-case, no classes/OOP, functional components only. When reporting complexity findings for this repo, always pass `--max-cyclomatic 10` — the default threshold will under-report violations against the repo's real bar.

## Updating `.fallowrc.json`

The config is not fixed — edit it whenever a finding is wrong or noisy because the config is stale, not because the code is actually fine. Signs it's a config problem rather than a real finding:

- An `ignorePatterns` entry references a filename that no longer exists (e.g. the file was renamed `.js` → `.ts`) — check with `fallow config --format json` (prints the fully resolved config) against `ls`/`find` for the real filename, then fix the pattern.
- The same false positive would recur on every run (e.g. a build-plugin file fallow can't trace into) — prefer an `ignorePatterns` or `ignoreDependencies` entry over repeating a `fallow-ignore-next-line` comment across many files.
- Generated/vendored code (e.g. shadcn `src/components/ui/*` boilerplate) is dragging down health/complexity signal for code nobody hand-maintains — exclude it rather than refactor it.
- `duplicates.minOccurrences`, complexity thresholds, or `entry` no longer match how the project actually builds (new entry point added, framework upgrade changed conventions).

Before hand-editing:

1. `fallow config --format json` — see the actual resolved config (not just the raw file, in case of `extends`).
2. `fallow config-schema --format json` — confirm the field name/shape before adding a new key; don't guess at schema.
3. For a bigger drift (e.g. after a framework upgrade, or on a project with no config yet), `fallow recommend --format json` proposes a project-tailored config split into `auto` (safe to apply), `default` (overridable), and `taste` (ask the user) — prefer this over a blind rewrite when more than one or two keys are stale.

After editing, re-run the relevant command and confirm the finding actually disappeared and nothing legitimate got silenced along with it. Treat editing `.fallowrc.json` as a normal source change: it's already tracked in git, so a diff is enough — no extra confirmation step beyond what you'd do for any other file — but call out in your summary _why_ the config changed, since a wrong scope change can hide a real issue later.

## Workflow for a refactor or PR-quality check

1. `fallow guard <files>` on any file you're about to touch, to know which architecture boundary rules apply.
2. `fallow health --max-cyclomatic 10 --complexity --targets --format json` to find and rank what actually needs splitting.
3. Make the change.
4. `fallow audit --format json` (or `--changed-since <base>`) to confirm the diff doesn't introduce new dead code, duplication, or complexity regressions before opening a PR.

## Don't

- Don't run `fallow fix` / `fix-apply` without explicit user confirmation — it mutates files.
- Don't treat `security` output as verified vulnerabilities — it's explicitly an unverified candidate list; verify each one manually before acting.
- Don't re-run a full-repo `fallow` sweep for a one-file edit — scope with `--file`/`--changed-since` or use `fallow inspect`/`fallow guard` instead.
