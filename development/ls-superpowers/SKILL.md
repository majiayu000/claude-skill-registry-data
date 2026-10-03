---
name: ls-superpowers
description: Use when mapping upstream Superpowers skill names to LocalSetup-native skills and workflows without activating duplicate upstream runtime tooling.
metadata:
  version: "1.1"
extensions:
  external_skill:
    source_kind: router
    source_url: https://github.com/obra/superpowers
    source_path: <repository inventory>
    source_commit: d884ae04edebef577e82ff7c4e143debd0bbec99
    source_ref: v6.1.1
    source_sha256: 14160b0f47047b1d8df87e05f166991f1e8a3ecb4a12a45be30ccb133dae9315
    license: MIT
    import_date: "2026-07-03"
    vetting_status: provenance-recorded-no-bundled-tooling-executed
---

# Superpowers Router

This skill is a compact provenance and routing layer for upstream Superpowers release `v6.1.1`.
LocalSetup-native skills remain canonical when workflows overlap.

## Routing Matrix

| Upstream Superpowers skill | LocalSetup route |
|---|---|
| `brainstorming` | `ls-workflow-planning-critic-loop` |
| `dispatching-parallel-agents` | LocalSetup controller subagent policy / planning workflow |
| `executing-plans` | LocalSetup controller worker/tester/reviewer flow |
| `finishing-a-development-branch` | `ls-workflow-repo-finalizer`, `ls-git-workflows`, `ls-github-publishing-workflow` |
| `receiving-code-review` | `ls-receiving-code-review` |
| `requesting-code-review` | `ls-requesting-code-review` |
| `subagent-driven-development` | LocalSetup controller subagent policy / `ls-workflow-planning-critic-loop` |
| `systematic-debugging` | `ls-debug-pro` |
| `test-driven-development` | `ls-tdd-guide`, `ls-test-runner` |
| `using-git-worktrees` | `ls-git-workflows` plus repo single-checkout policy |
| `using-superpowers` | `ls-superpowers` |
| `verification-before-completion` | `ls-framework-compliance` |
| `writing-plans` | `ls-workflow-planning-critic-loop` |
| `writing-skills` | `ls-skill-creator`, `ls-skill-importer`, `ls-skill-normalizer`, `ls-skill-vetter` |

## Import Policy

- Use this skill to translate upstream Superpowers names into LocalSetup-native workflows.
- Do not reimplement TDD, debugging, planning, worktree, review, or subagent orchestration here.
- Existing LocalSetup skills are the active runtime guidance for overlapping workflows.
- The upstream release is kept as inert provenance under [references/upstream/manifest.yaml](./references/upstream/manifest.yaml).

## Runtime Boundary

Upstream scripts, plugins, hooks, tests, package metadata, webserver tooling, and the staged `AGENTS.md -> CLAUDE.md` symlink are not active LocalSetup runtime surfaces.
Only inert markdown/license provenance was imported under `references/upstream/`.

## Provenance

- Source: `https://github.com/obra/superpowers`
- Release/ref: `v6.1.1`
- Commit: `d884ae04edebef577e82ff7c4e143debd0bbec99`
- License: `MIT`
- Inventory hash: `14160b0f47047b1d8df87e05f166991f1e8a3ecb4a12a45be30ccb133dae9315`
- Manifest: [references/upstream/manifest.yaml](./references/upstream/manifest.yaml)
