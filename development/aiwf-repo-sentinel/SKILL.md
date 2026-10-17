---
name: aiwf-repo-sentinel
description: Use before coding, debugging, refactoring, review, or generated-code cleanup in an existing repository to protect user changes, detect the real runtime and package manager, prevent duplicate architecture and broad diffs, preserve tests and API contracts, and require honest validation.
---

# AIWF Repo Sentinel

## Core Rule

Search before creating. Modify the repo-native path. Prove the result with the cheapest relevant check.

## Preflight

1. Verify the real project root and read `AGENTS.md`, `PROJECT_SKILLS.md`, README, architecture notes, and current handoff or plan.
2. Inspect existing changes before editing. In git repos, use `git status --short` and a focused diff; never overwrite or revert user work.
3. Identify language and framework versions, lockfile or package manager, build entrypoint, test commands, shell and OS, generated files, schemas, and CI assumptions.
4. Search for the existing route, component, service, helper, type, style, config, and tests before adding files.

Read `references/preflight-checklist.md` when the repo is unfamiliar. Read `references/windows-powershell-commands.md` for Windows-safe command patterns.

## Patch Rules

- Keep the change inside the requested behavior and existing ownership boundaries.
- Do not create `*_new`, `*_fixed`, copies, backup trees, parallel routers, duplicate clients, second style systems, or replacement apps to avoid understanding the current code.
- Obey existing lockfiles and runtimes. Do not switch package manager, generator, framework, language standard, or major dependency as a hidden fix.
- Preserve public API, schema, serialization, generated-client, and configuration contracts unless the task explicitly changes them.
- Keep async work non-blocking and resource lifetimes explicit. Add the focused language or framework skill for implementation details.
- Do not introduce unsafe parsing, shell execution, HTML injection, broad CORS, secret exposure, or untrusted model/data loading. Add `aiwf-security-guardrails` when a security boundary is touched.
- Stop and explain before a broad rewrite, migration, destructive operation, production change, or edit that weakens security or test coverage.

## Test Integrity

Do not make checks pass by deleting tests, removing assertions, adding unexplained skips or expected failures, replacing behavior with mocks, increasing timeouts to hide hangs, disabling strict modes, or adding broad ignore directives.

When a test is wrong, show the contract or behavior that proves it before changing the test. Add a regression test for a fixed bug when the repo has a suitable test surface.

## Validation

Choose checks in this order where relevant:

1. Parse, compile, or format check for touched files.
2. Narrow typecheck or unit test.
3. Broader affected suite.
4. API/schema generation or contract diff.
5. Browser, device, service, or runtime smoke.
6. Build or package.

Do not claim success when validation did not run. State the command, result, and reason for any skipped check.

## Output

Report changed files and purpose, commands and results, contract impact, and remaining risk. Keep the report proportional to the patch.
