---
name: codebase-status
description: Report what a repository is, what recent conversation history says about it, current application status, and outstanding work
type: analysis
version: v0.12
argument-hint: "[optional repo path, focus, or --no-history]"
---

# Codebase Status

Invoke as `/codebase-status`.

Use this skill when the user asks what a repo or application is, where work was left, what is outstanding, whether it is ready/stable, or wants a detailed status report that combines codebase evidence with local Claude/Codex conversation history.

This is read-only status synthesis. It does not replace `/roadmap`: `roadmap` maintains the task pipeline and priority queue; `codebase-status` explains the actual current state of the repo and relevant prior conversations.

## Process

1. Resolve target repo:
   - Default to the current working directory.
   - If the user provides a path, use that repo.
   - Confirm it is a git worktree when possible; if not, continue with filesystem evidence and report that git evidence is unavailable.
2. Read project orientation:
   - `README.md`, `AGENTS.md`, `CLAUDE.md`, `.agents/project.json`, package/workspace files, app entrypoints, and high-signal docs.
   - Identify project type, main apps/packages, runtime, tests, and likely user-facing or developer-facing purpose.
3. Read planning and status docs when present:
   - `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, `tasks/recurring-todo.md`, `tasks/history.md`, `tasks/lessons.md`, `tasks/phases/`, `specs/`, `spec.md`, and `research/`.
   - Distinguish checked-off work, active work, manual blockers, advisory work, stale docs, and missing docs.
4. Read routing evidence for product, research, or spec repos:
   - When `research/`, `specs/`, `spec.md`, product docs, or prototype artifacts exist, read `docs/pack-workflow-matrix.md` and `docs/skill-next-step-contracts.md` if present.
   - Identify the last completed relevant research/product skill from artifacts, task history, or conversation history. Before recommending another research/product skill, consult that skill's active `SKILL.md` `## Next Steps` contract and any `## Next Steps` section in its output artifact.
   - Treat those route contracts as stronger evidence than a generic status impression. If docs disagree, report the contradiction and prefer the newest active skill contract or route matrix with file evidence.
   - For pack-local recommendations, check `.agents/project.json` `enabled_packs` first. If the target skill's pack is not enabled, recommend `npx skillpacks install <pack-name>` from the project shell, before the skill.
5. Inspect git evidence:
   - `git status --short`
   - current branch and upstream status
   - last 20 commits
   - unpushed commits when an upstream exists
   - changed files in the working tree
6. Inspect codebase health signals:
   - Project structure and primary modules.
   - Test/build/lint scripts from package manifests or equivalent tool files.
   - Obvious TODO/FIXME markers, failing-test notes, disabled tests, and local quality scripts.
   - Do not run expensive commands by default. Run cheap read-only inspections freely; ask or state assumptions before long builds, network installs, destructive commands, or mutation.
7. Find related conversation history unless `--no-history` is passed:
   - Read full available local prompt history, not a sample:
     - `~/.claude/history.jsonl`
     - `~/.codex/history.jsonl`
     - `~/.codex/sessions/**/*.jsonl` for Codex session metadata only when needed to map session IDs to cwd.
   - Filter to records whose project/cwd matches the target repo or whose text mentions the absolute path, repo directory name, package/app name, or repository URL.
   - Exclude system, developer, tool output, injected skill payloads, and base instruction text from examples.
   - Use line-by-line parsing for scale and deduplicate Codex prompt records when compact and rich histories overlap.
   - Extract recent user goals, repeated requests, unresolved questions, blockers, and prior recommendations.
8. Synthesize status:
   - What this repo/app is.
   - What has happened recently.
   - Current implementation status by major area.
   - Outstanding work, grouped as blocking, next execution, advisory, manual/human-only, and uncertain.
   - Mismatches between conversation history, task docs, git history, and code reality.
   - Confidence level for each major conclusion: high, medium, or low, with evidence.
9. Recommend next route (check whether each skill's pack is installed; if not, recommend `npx skillpacks install <pack>` from the project shell, first):
   - Use phase-aware routing before naming a command:
     - If `tasks/todo.md` or active phase docs contain actionable implementation work, recommend the approved task artifact route. Do not route back to research merely because advisory gaps exist.
     - If finished work is dirty, unpushed, unvalidated, or needs packaging/review before handoff, recommend `/ship`.
     - If user-facing product research/prototype artifacts are missing and no implementation/shipping queue is active, follow the canonical AFPS route from the routing evidence: `customer-discovery -> competitive-analysis -> journey-map -> positioning -> user-flow-map -> ux-variations [specific-user-flow] -> ui-interview [specific-ux-variation] -> prototype -> uat --variant-evaluation -> consolidate-prototypes -> research-roadmap --post-prototype -> spec-interview -> research-roadmap --post-spec -> roadmap`. Use `/ui-interview --requirements-only` and `/ux-variations --layout-mode` only when the user explicitly needs a fixed content/data/action contract and layout-only alternatives.
     - If `research/icp.md` and `research/competitive-analysis.md` exist but `research/journey-map.md` is missing, check `customer-lifecycle` availability. If it is not enabled, recommend `npx skillpacks install customer-lifecycle` from the project shell, before `/journey-map`; if enabled, recommend `/journey-map`.
     - Treat `value-prop-canvas` and `lean-canvas` as optional risk-driven detours only. Before recommending either, check `business-research` availability; if it is not enabled, recommend `npx skillpacks install business-research` from the project shell, before `/value-prop-canvas` or `/lean-canvas`. Recommend `/value-prop-canvas` only for contested solution-fit evidence, and `/lean-canvas` only for material business-model risk; do not make either a default blocker before `journey-map`, `positioning`, `user-flow-map`, or layout-mode UX variations.
     - If no research, spec, task, implementation, validation, dirty, or unpushed work remains, recommend `/brainstorm` to discover new AFPS work.
   - Approved task artifact route when the next task is already clear and executable.
   - `/roadmap` when specs exist but sequencing or task queue health needs updating. _(agent-work-admin pack)_
   - `/feature-interview` when the next idea/direction is not yet represented in specs or tasks. _(product-design pack)_
   - `/reconcile-dev-docs audit` or `/reconcile-dev-docs fix tasks` when task docs contradict git/code reality. _(docs-health pack)_
   - `/spec-drift` when specs and code appear out of sync. _(agent-work-admin pack)_
   - `/guide` only for human-only external blockers. _(guided-walkthrough pack)_
   - `/brainstorm` when the repo is complete/current and the next step is discovering a new phase. _(product-design pack)_

## Output

Produce a structured report with:

- **Overview:** repo path, project purpose, project type, primary apps/packages, branch, dirty/unpushed status.
- **History Signal:** number of Claude/Codex prompt records scanned, number matched to this repo, date range, and 3-8 concise real examples.
- **Recent Work:** last commits and task/history evidence.
- **Current Status:** major areas and whether each appears complete, in progress, blocked, stale, or unknown.
- **Outstanding Work:** prioritized list with evidence and recommended owner/skill.
- **Risks And Drift:** contradictions, stale docs, missing tests, manual blockers, or uncertain claims.
- **Recommended Next Step:** one concrete next work item and one command.

End with exactly:

```md
**Next work:** <specific task, blocker, discovery task, or "none">
**Recommended next command:** <one command or route>
```

## Constraints

- Read-only by default. Do not modify files, create commits, run installs, or execute long test suites unless the user explicitly asks.
- Do not include private conversation history unrelated to the target repo.
- Quote only short prompt excerpts. Prefer paraphrase plus timestamp/source/project.
- Do not treat `tasks/record-todo.md` or `tasks/recurring-todo.md` as execution queues unless an item has clearly become concrete work.
- Do not put agent-executable work in `tasks/manual-todo.md` or route it to `/guide`.
- Do not recommend `/roadmap` if the finding is only "tell me the status"; use `/roadmap` only when the task pipeline itself needs queue maintenance or roadmap extension.
- When recommending a pack skill, first check `.agents/project.json` for `enabled_packs`. If the target skill's pack is not enabled, include `npx skillpacks install <pack-name>` from the project shell, as a prerequisite in the recommendation.
- Do not create or modify GitHub Actions workflows.

## Default Shipping Contract

- **Default next-step routing:** when reporting completion, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>` so the next caller has a concrete handoff.
- Normally read-only and should not create or modify tracked repository files.
- If the user explicitly asks this skill to create or modify tracked files, follow `docs/github-delivery-contract.md` and finish with an issue-backed non-primary branch plus ready pull request; do not merge it.
- This contract does not override stricter safety rules about secrets, destructive history changes, release publication/tag confirmation, production deploy confirmation, paid actions, or public visibility changes.
