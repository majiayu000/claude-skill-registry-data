---
name: codexpiator
description: Entry point for the Codexpiator toolkit. Use only when a software-engineering request's domain is ambiguous, spans multiple domains, or is exploratory - if it clearly matches one specific codexpiator-* skill's own description, prefer that skill directly instead.
---

# Codexpiator Router

Codexpiator is a set of small, single-purpose skills covering the
full span of building and shipping software: frontend, backend,
security, testing, architecture, devops, git/DX, and AI integration.
This router's only job is to classify an incoming request and point
at the right skill (and, inside it, the right file) — never to answer
from here directly with duplicated content.

## Classification table

| Domain | Dispatch to | Example triggers |
|---|---|---|
| Frontend (UI, components, state, styling, forms, routing, a11y) | `codexpiator-frontend` | "how should I structure this component", "state management approach", "form validation", "is this accessible" |
| Backend (APIs, data, auth, jobs, caching, resilience) | `codexpiator-backend` | "design this endpoint", "should I cache this", "how to model this data", "background job for emails" |
| Security (secure coding, authn/authz, injection, secrets, deps) | `codexpiator-security` | "is this safe", "how do I store passwords", "sql injection risk", "secrets management" |
| Testing & QA (strategy, TDD, mocking, CI gates) | `codexpiator-testing-qa` | "what should I test", "TDD for this feature", "flaky test", "what blocks merge" |
| Architecture (structure, patterns, contracts, scaling) | `codexpiator-architecture` | "how to structure this project", "monolith or microservices", "API versioning", "will this scale" |
| DevOps (CI/CD, environments, containers, observability, incidents) | `codexpiator-devops` | "set up CI/CD", "dockerize this", "how to monitor this", "rollback plan" |
| Git / DX (workflow, commits, PRs, review, docs, onboarding) | `codexpiator-dx-git` | "branching strategy", "write a commit message", "review this PR", "onboarding docs" |
| AI integration (LLM patterns, prompting, agent safety, MCP) | `codexpiator-ai-integration` | "integrate an LLM", "prompt engineering", "is this agent safe", "which MCP server" |

**Invoke the matching skill** (through the environment's actual skill-
invocation mechanism, by name — e.g. `codexpiator-frontend` — the same
way a `superpowers:*` skill gets invoked) rather than opening its
`SKILL.md` with a file-read tool. Invoking it properly lets it
activate and point itself at its own specific resource file(s); don't
answer from this table's one-line descriptions alone, and don't copy a
topic skill's content into this router.

A request can span more than one domain (e.g. "add a login feature"
touches frontend, backend, and security). In that case, consult each
relevant skill for its slice rather than picking just one.

## Long or complex work

For anything substantial (multi-step, many files, spans multiple
commits), see `shared/long-task-memory-and-superpowers.md` — write
resumable progress memory to a gitignored project directory, and use
`superpowers:*` skills (writing-plans, executing-plans,
systematic-debugging, TDD, etc.) when available instead of improvising
the process.

## Ask when useful; suggest an audit after significant work

See `shared/collaboration-and-audit-practice.md` — ask a targeted
clarifying question (via `AskUserQuestion` when available) when a
request has real ambiguity, and suggest `/codexpiator-audit` after
completing significant work. Every `codexpiator-*` skill follows this.

## Before answering anything design- or security-audit-shaped

If the request involves visual design, motion/animation, a broad UI
polish pass, redesigning an existing UI, or a deep security audit,
read `shared/external-skills-registry.md` first. It has the exact
procedure for checking whether a more specialized external skill is
available, and the fallback to use when it isn't. Don't skip this
check just because `codexpiator-frontend` or `codexpiator-security`
also has relevant content — the registry decides which one leads.
