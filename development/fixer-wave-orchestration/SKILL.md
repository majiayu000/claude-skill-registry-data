---
name: fixer-wave-orchestration
description: "Use when several edit subagents will change one repo at the same time: fanning fixers out over an audit's verified findings list, splitting a feature or refactor by file ownership, or accepting what the wave produced before committing it."
---

# Fixer wave: findings → ownership-split fixers → acceptance

Dispatch and acceptance for any wave of concurrent edit agents in one repo; repeatable per audit round. Scouts find (`shallow-codebase-audit`), per-change acceptance is `verify-delegated-edits`, Kotlin/Android damage probes are `subagent-damage-repair`, and the Android readiness slice plan is `android-readiness-agent-wave`.

## Dispatch
1. Split the work into agent briefs by **exclusive file ownership** — no file appears in two rosters. Consolidate same-file findings into one agent even when themes differ; that agent owns the whole file.
2. Decide cross-agent contracts before dispatch and write them into the shared context — agents cannot negotiate mid-flight. Contract-block format: `subagent-damage-repair` (Prevent it).
3. Each brief carries, per finding or work item: file:line, the verified mechanism (not just the symptom), and the intended fix approach. Plus hard rules: house comment style (say WHY, name the concrete failure), no commits.
4. Build rule, by toolchain: .NET agents may self-check with `dotnet build <sln> --nologo -v minimal` → 0 errors and targeted suites only, under central package management (no inline Version=); Gradle/Android agents run no gradle, lint or adb at all — parallel Gradle runs fight over the lock. Either way an agent's green is not acceptance (Acceptance 3).
5. Test files are owned by nobody: required test edits (constructor arity, signature callers, fixture shapes) are REPORTED by the agent and applied by the parent or assigned explicitly — otherwise an agent's "all green" hides a broken sibling test project.
6. Shared-file hot regions: hub-message the owning agent mid-flight ("keep clear of line N — parent applies that fix there") and apply those yourself after the agent lands.
7. List not-worth-acting findings explicitly as out-of-scope so nobody wanders into them.

## Acceptance (`verify-delegated-edits` applies in full)
1. `git status --porcelain=v1 --untracked-files=all` + `git diff --stat`: touched set == union of rosters; zero deletions; zero scratch files.
2. Read every hunk, then the RAW file at collision regions and concurrency-sensitive changes: **compact diff renderers drop words and can hide a deleted argument line**. A real regression was caught exactly this way — a build stayed green while an optional record parameter was silently omitted. Optional defaults convert compile-time failures into silent null data that tests on fakes cannot see.
3. Gate once, after all agents settle: concurrent edits break sibling builds transiently, so an agent's "0 errors" was measured mid-flight of the others. Kotlin/Android: run the `subagent-damage-repair` probes first. Full gate: build 0 errors + every targeted suite. Flaky/environmental suites: compare failure signatures to the documented baseline and attribute new ones by stashing the agents' files and rerunning (stash-vs-worktree method: `verify-delegated-edits`).
4. When an agent changed a shared helper signature (e.g. `Note(msg)` → `Note(msg, problem)`), grep ALL call sites — a real failure rendered as neutral/informational is the failure mode of missing one.
5. Commit thematically (one commit per fix cluster); straggler test-file updates get a small follow-up commit.

## Shell traps (each cost real time)
- bash expands `$` inside double-quoted `powershell -Command "..."`. Pass code via an env var and invoke with single-quoted bash: `powershell -NoProfile -Command '$env:CHECK | Invoke-Expression'`.
- PowerShell: `'-p:x=' + $var` inside a comma-list is **array + string concat** (commas bind tighter) — the value becomes a stray positional arg (MSB1008). Use expandable strings `"-p:x=$var"`.
