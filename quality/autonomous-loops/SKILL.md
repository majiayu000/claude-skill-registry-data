---
name: autonomous-loops
description: Patterns and architectures for autonomous Codex development loops, from simple sequential pipelines to RFC-driven multi-agent DAG systems. Use when building.
---

# Autonomous Loops

Compatibility note: `autonomous-loops` is retained for existing workflows. Prefer `continuous-agent-loop` for new loop guidance when that skill is available.

Use this skill to design autonomous Codex workflows that can run across multiple iterations without losing safety, scope, or validation.

## When To Use

- Build unattended or semi-unattended development workflows.
- Choose the right loop architecture for a task.
- Create CI/CD-style continuous implementation pipelines.
- Run parallel agents with clear ownership and merge coordination.
- Preserve context across loop iterations without overloading the prompt.
- Add quality gates and cleanup passes to autonomous work.

## Loop Mode Spectrum

| Mode | Complexity | Best for |
| --- | --- | --- |
| Sequential pipeline | Low | Scripted development steps and repeatable routines |
| NanoClaw-style REPL | Low | Persistent interactive sessions |
| Infinite agent loop | Medium | Parallel spec-driven generation |
| Continuous PR loop | Medium | Multi-day iteration with CI checks |
| Cleanup pass | Add-on | Quality cleanup after implementation |
| RFC-driven DAG | High | Large features split across coordinated work units |

## 1. Sequential Pipeline

Break routine development into a series of focused noninteractive `codex exec` calls. Each call receives a clear prompt, works against the filesystem state left by the previous step, and exits when done.

```bash
#!/bin/bash
set -e

codex exec "Read docs/auth-spec.md. Implement OAuth2 login in src/auth/. Write focused tests."
codex exec "Review the changed files. Remove unnecessary defensive code and tests that only verify language behavior. Keep real business logic tests."
codex exec "Run build, lint, type checks, and tests. Fix failures without adding new features."
codex exec "Create a conventional commit for the completed work."
```

Design rules:

- Keep each step narrow.
- Let filesystem state carry progress between steps.
- Use explicit validation steps rather than hoping the implementation prompt does everything.
- Stop the pipeline on failure so bad output does not cascade.

## 2. Persistent REPL Loop

A persistent loop stores conversation history in a local session file and sends the relevant history into each noninteractive run.

Use it when exploration matters more than strict automation. Avoid it for CI because context grows and reproducibility drops.

Recommended structure:

1. Store session state in a markdown file under `.codex/` or another project-local path.
2. Append each user request and agent response.
3. Summarize or compact when the file grows too large.
4. Keep irreversible actions behind explicit confirmation.

## 3. Infinite Agent Loop

Use a coordinator prompt plus worker prompts to generate many independent outputs from one spec.

Coordinator responsibilities:

- Read the spec and output directory.
- Find the highest existing iteration number.
- Assign each worker a unique direction, scope, and output path.
- Launch workers in small batches.
- Inspect outputs for collisions and quality issues.

Worker responsibilities:

- Follow the assigned scope exactly.
- Read the shared spec and current directory snapshot.
- Produce only the assigned output.
- Avoid changing files owned by another worker.

Batching guidance:

| Count | Strategy |
| --- | --- |
| 1-5 | Run all workers together |
| 6-20 | Batch in groups of about 5 |
| Open-ended | Run waves of 3-5 and evaluate after each wave |

## 4. Continuous PR Loop

A production loop can create a branch, implement a scoped change, validate it, open a PR, wait for CI, fix failures, and merge when checks pass.

Required guardrails:

- Maximum run count.
- Maximum elapsed time.
- Maximum spend or compute budget when applicable.
- Clear stop condition.
- Human approval for risky operations such as merge, deploy, or destructive migrations.

Typical flow:

1. Sync main branch.
2. Create a scoped iteration branch.
3. Run implementation prompt.
4. Run cleanup prompt.
5. Run tests and static checks.
6. Open or update PR.
7. Wait for CI.
8. Fix CI failures in a bounded loop.
9. Ask for merge approval when policy requires it.

## 5. Cleanup Pass

Add a cleanup pass after implementation. This catches overbroad code, unnecessary abstractions, brittle tests, and defensive clutter.

Prompt shape:

```text
Review only files changed in this iteration. Remove unnecessary complexity,
duplicate logic, and tests that only verify framework or language behavior.
Keep meaningful behavior tests. Run the relevant checks after cleanup.
```

## 6. RFC-Driven DAG

For large work, write an RFC that defines independent work units and dependency edges. Then run workers for nodes whose dependencies are complete.

RFC should include:

- Goal and non-goals.
- Work units with file ownership.
- Dependency graph.
- Validation for each unit.
- Integration order.
- Rollback plan.

Coordinator loop:

1. Parse the RFC into nodes.
2. Start only nodes with satisfied dependencies.
3. Assign each worker a disjoint write set.
4. Collect patches and validation results.
5. Resolve conflicts before starting dependent nodes.
6. Run integration checks after each merge group.

## Choosing A Mode

- Use a sequential pipeline when the work is linear and predictable.
- Use a persistent loop when the task is exploratory.
- Use an infinite agent loop when outputs are independent and spec-driven.
- Use a continuous PR loop when repository automation and CI are available.
- Use an RFC-driven DAG when parallel work has real dependencies.

## Anti-Patterns

- Running autonomous loops without a stop condition.
- Letting multiple workers edit the same files without ownership.
- Skipping validation between iterations.
- Asking one prompt to implement, review, test, commit, and merge with no gates.
- Carrying large context forward instead of passing compact artifacts.
- Treating a successful local run as permission to deploy or merge without policy approval.

## Changelog

- [2026-05-11] [LANGUAGE] Converted the skill from Chinese to English while preserving Codex loop guidance.
