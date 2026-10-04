---
name: solar-code
description: >
  Reusable Solar protocol for code modifications in planet-operated repos. Use
  when an intention (RFC, task, direct instruction) must be converted into a
  local, human-reviewable code change. Covers triage, task spec, local change,
  checks, completion evidence, and IDE review. Does not handle PRs, push, or
  CI/CD.
---

# Solar Code

## Purpose

Convert an intention into a local executable code change without reinventing
the rules each time. Provides a canonical flow and repo adoption contract for
repos operated by planets.

## When to Use

Use this skill when:
- A task requires modifying code in a planet-operated repo target.
- A change needs a defined triage level before touching files.
- A planet needs to declare its repo policy (allowlist, restrictions, checks).

Do not use for changes inside `core/skills/` — those are governed by `solar-skill-creator`.

Do not use for:
- PR creation, git push, or GitHub review workflows.
- CI/CD pipeline changes.
- Async workers or queues.
- Multi-repo architectural decisions (use an RFC first).

## Required MCP

None

## Triage

Classify the change before acting:

| Level | Description | Required artifact |
|-------|-------------|-------------------|
| Micro change | 1-2 files, low risk | Clear instruction + repo checks |
| Standard change | Feature or fix with relevant context | Lightweight task spec (Markdown) |
| Multi-repo / high risk | Touches multiple repos or has strategic impact | RFC + task spec + prior review |

## Workflow

1. **Triage** — classify the change level (micro / standard / multi-repo).
2. **Load repo policy** — read the target repo's `CONTRIBUTING.md` file before writing anything.
3. **Write task spec** (if standard or above) — use `references/task-spec.md` as the single source of truth for structure and allowed sections.
4. **Apply change locally** — edit files in the working tree; do not push.
5. **Update completion evidence** — after implementation, record only the facts needed for review and traceability.
6. **Run checks** — only commands declared in the repo policy allowlist.
7. **Human review in IDE** — surface the diff; human decides to keep or discard.

**Default mode:** `local-review`. Branch, push, and PR are optional layers added
only when there is evidence they are needed.

### Authority (supervised autonomy)

- Clear local `solar-code` work under an explicit user mandate is **A2 implicit**
  (scoped working-tree edit + IDE review). Do not ask a second “approve?” for that
  scoped edit.
- **Push, PR, tag, and release** are never A2 implicit — require **A2 formal**
  (and treat irreversible release paths as A4 escalation when appropriate).
- If triage level grows beyond the original mandate, re-triage and get explicit
  approval before continuing (new A2).

## Failure protocol

- If a required check fails: stop, report the failure, do not proceed.
- If the repo policy is missing: ask the user to declare one before writing files.
- If the change scope grows beyond the original triage level: re-triage and get
  explicit approval before continuing.

## Repo adoption contract

Each repo target must declare a policy file at its root. Format: `CONTRIBUTING.md`.
This file defines the "rules of engagement" for both humans and AI agents.

For code repositories adopting this skill, the recommended split is:
- `AGENTS.md` — planet governance, routing, architecture ownership.
- `CONTRIBUTING.md` — repo policy, checks, restrictions, task-spec location.
- `docs/tasks/` — standard-or-higher task specs unless the repo declares a different path.


## References

- `references/task-spec.md` — canonical task spec template with optional completion evidence.
- `references/repo-policy.md` — repo policy template (rename to `CONTRIBUTING.md` when adopting a repo).
- `references/local-review-guide.md` — how to use local-review mode.
