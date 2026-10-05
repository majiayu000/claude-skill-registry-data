---
name: working-with-lacquer
description: Fix Lacquer drift, sync or onboard a project, change managed checks, relax a baseline, refuse a dependency update, or retire a project.
---

# Working With Lacquer

Lacquer renders shared content — CLAUDE.md regions, skills, commands, lint
configs, git hooks, CI workflows — from one repo into every project. A project
declares its shape in `.lacquer.toml`; `lacquer sync` writes the content;
`lacquer audit` checks the project against it and is wired into CI.

The rule that explains every mechanism below: **a lacquer-managed file is
identical to the lacquer's copy, or it is excluded. There is no third state.**
A quietly-edited copy is how one project's pre-commit hook ends up weaker than
its CI while looking healthy.

## Is this file mine?

```sh
lacquer audit    # classifies every managed unit, lists the ones that aren't clean
lacquer status   # each CLAUDE region's stamped version vs the lacquer's latest
```

If `audit` lists it, the lacquer owns it. Typically: `.swiftlint.yml`,
`.swiftformat`, `biome.json`, `deno.jsonc`, `.pre-commit-config.yaml`,
`lefthook.yml`, `.github/workflows/<profile>-*.yml`, `.claude/skills/**`,
`.claude/commands/**`, and the `<!-- lacquer:… -->` regions inside `CLAUDE.md`
/ `AGENTS.md`. Text *outside* those markers in a CLAUDE.md is the project's and
is preserved.

## Exit codes

| Code | Means | Fix |
|---|---|---|
| 0 | clean | — |
| 1 | the command failed (bad manifest, I/O, missing profile) | read the message |
| 2 | usage error | — |
| 3 | a managed file was edited locally; sync would clobber it | see below |
| 4 | a project baseline is not met | meet it, or time-box a relaxation |
| 5 | `lacquer doctor`: a check proved it cannot fail | fix the check |
| 6 | a stack on disk is not declared in `.lacquer.toml` | `lacquer adopt` |

## Recipes

**Exit 3 — "a lacquer-managed file was edited in this project."**
Decide which is true, then do that one:

- *The change should apply everywhere* → make it in the lacquer repo, open a PR
  there, then re-sync this project. This is the default and usually the right
  answer.
- *This project genuinely owns the file* → add it to `[project].exclude` with a
  `reason` (and an `until` if it is temporary — see "Exclusions" below). The
  lacquer then neither distributes nor tracks it.
- *The edit was accidental* → `lacquer sync` (or `sync --force` to take the
  lacquer's version over yours).

**Exit 6 — "this project runs a stack .lacquer.toml does not declare."**
A whole toolchain is ungated: no hooks, no CI, no CLAUDE region. Run
`lacquer adopt` — it re-detects and records the stack, additively, preserving
the manifest's comments — then `lacquer sync`. If the path is deliberately
unmanaged (a fixture tree, a scratch package), add it to `[project].exclude`
instead.

**Exit 4 — the baseline.** The standard lives in the lacquer
(`profiles/<p>/baseline.toml`) and is inherited, not restated. A project that
cannot comply *yet* time-boxes it in its own manifest — both fields required, an
expired entry is a hard failure:

```toml
[baseline.relax]
swift_version = { until = "2026-09-01", reason = "pre-Swift-6 audio engine, #142" }
```

Keys: `swift_version`, `warnings_as_errors`, `strict_concurrency`,
`documentation`, `pgtap`.

Exit 4 also fires on an **expired exclusion**, which is the same failure wearing
a different spelling.

**Exclusions.** `[project].exclude` is the other way to opt out, and it is the
one the exit-3 and exit-6 messages point you at. Give every entry a `reason`;
add `until` when the exclusion is temporary:

```toml
[project]
exclude = [
  { path = "lefthook.yml", reason = "monorepo runs hooks from the workspace root" },
  { path = ".github/workflows/ios-ci.yml", reason = "local xcresult fix pending upstream", until = "2026-10-01" },
]
```

The bare form (`exclude = ["lefthook.yml"]`) still loads — no project breaks on
upgrade — but `audit` reports it on every run until it carries a reason.

Choosing between them is the whole decision: `until` present means "we haven't
got to it yet" and turns into a hard failure on that date; `until` absent means
"this project is genuinely different" and is never chased. Do not invent a date
for a permanent divergence — a rubber-stamped expiry you renew forever teaches
the next reader that dates in this file are noise.

`audit` also flags an exclusion that no longer matches anything the lacquer
ships. It suppresses nothing, so it is dead text that still reads like a live
decision — delete it.

**Retirement.** `[project].retired` is the third opt-out, and it is not per-file:

```toml
[project]
retired = { since = "2026-08-18", reason = "not a viable app" }
```

It means **stop the spend, stay consistent.** Everything that holds the repo to
the fleet's shape keeps syncing — PR CI, lint/format configs, `CLAUDE.md`,
`.gitignore`, hooks, skills — so the project still audits clean. Everything that
costs money or attention **on a schedule** stops: any workflow whose `on:` block
carries `schedule:` (read from the workflow's content, not a filename list), plus
`.github/dependabot.yml`. Both fields are required; a malformed entry is a hard
error, not a silent no-op. There is deliberately no `until` — retirement is not
debt with a term, and an expiry would quietly turn a dead project's cron jobs
back on. `status` and `audit` lead with the retirement and its date. Nothing is
deleted: files already in the repo stay until someone removes them by hand.

Reach for `exclude` when this project owns one file. Reach for `retired` when the
project itself is over.

## Auditing every project at once

`lacquer audit` answers a question about ONE project, which is what a project's
CI needs. For "what is true across everything I own", use a roster:

```toml
# fleet.toml — the roster is YOURS, not the lacquer's. Keep it wherever your
# project list belongs; relative paths resolve against the roster file itself.
[[project]]
name = "some-app"
path = "../some-app"
```

```sh
lacquer fleet --roster fleet.toml          # human summary
lacquer fleet --roster fleet.toml --json   # snapshot to diff against a later run
```

Exit 4 if **any** project would fail its own `lacquer audit` — one code, not the
per-project 3/4/6, because a sweep's caller wants "is anything wrong" and the
report already says which project and why.

It is read-only. It never syncs, never opens a PR, never writes to a project.

Two sections of the output earn the sweep on their own:

- **expiring exemptions** — every `until` across the fleet, soonest first. Each
  is a date on which some project's CI starts failing, and without this they are
  invisible until the morning they fire.
- **excluded by more than one project** — when several projects exclude the same
  path, the shared asset is usually what is wrong. This fleet had three projects
  independently working around one lacquer defect, and it was visible only by
  reading three manifests' TOML comments.

A broken project is reported, never skipped: an absent row reads as a healthy
one, and a sweep that quietly drops what it could not parse is worse than no
sweep.

**Before excluding a whole file, check for a seam.** Excluding a managed file to
change a few lines means hand-carrying a full copy of it forever, and that copy
drifts the moment the shared one changes. One project excluded its entire
`web-ci.yml` to declare five build-time secrets; the fix was a slot
(`[project].build_env`) in the shared workflow, not an exclusion. If the reason
you are reaching for `exclude` is "the shared asset has nowhere to put X", add
somewhere to put X in the lacquer instead — that is a one-time change that every
project inherits, versus a permanent local fork.

**A stack the lacquer has no profile for** (Rust, Go, a bare SwiftPM package)
is reported by `audit` on every run and gates nothing — that gap is the
lacquer's. Closing it means adding `profiles/<name>/` upstream. Until then,
nothing is enforcing that code; say so rather than treating the repo as covered.

**Starting a new project.** Name the stack before the code exists, so both
halves are gated from the first commit rather than whichever half gets written
first:

```sh
lacquer init --list-stacks
lacquer init --stack ios-supabase
lacquer sync --fix          # --fix also runs the profiles' autofixers over existing source
```

Every command that reads shipped content needs `LACQUER_ROOT` pointing at the
lacquer checkout (`LACQUER_ROOT=~/Developer/lacquer lacquer sync`).

## Three things that look like fixes and are not

- **Editing the managed file and moving on.** It silently diverges this project
  from every other one, and the next sync reverts it — so the work is lost *and*
  the divergence was real while it lasted.
- **Setting `profiles = []` to quiet a report.** It changes nothing about what
  is enforced; it only stops the report. One repo's Swift sat a month with no
  hooks, no CI, and 191 tests run by nothing, because the manifest said the
  component existed and named no profile.
- **A relaxation with no expiry, or `--force` to make audit stop complaining.**
  A relaxation that cannot expire is a redefinition of the standard. `--force`
  is for adopting the lacquer's version over a local edit, not for silencing a
  finding.

## Project conventions

Read [references/project-rules.md](references/project-rules.md) for the relevant
section when handling this task. Read only what applies; examples do not
authorize releases, deployments or changes outside the user's scope.
Always-loaded safety rules still apply.

- Local Checks Match CI
- Warnings as Errors
