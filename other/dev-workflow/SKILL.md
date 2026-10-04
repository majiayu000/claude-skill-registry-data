---
name: dev-workflow
description: Route planning, design, prototypes, implementation, review, commits, and pull requests through a project's delivery lifecycle. Use when no project-local workflow overrides it.
---

# Dev Workflow

A **delivery loop** makes the next irreversible action explicit: understand → decide → prove → build → verify → review → commit → PR. Route the request to its earliest needed stage; do not skip uncertainty to start coding.

## 1. Prefer the project

Before routing, read the nearest `AGENTS.md` and inspect project-local `.agents/skills/`, `.pi/skills/`, and delivery/planning documentation.

- If the project provides a lifecycle/router skill or documented planning convention, load and follow it. It overrides this skill, including its artifact names and approval gates.
- Otherwise, use this fallback and the shared skills it names.

Completion: the chosen workflow and its plan/artifact location are named before work begins.

## 2. Route

Announce the stage and one-line reason, then load only the referenced skill or artifact.

| Stage | Use for | Action |
|---|---|---|
| **Understand** | unfamiliar area, product/domain ambiguity, broad effort | Load `wayfinder` for multi-session discovery; use `research`, `domain-modeling`, `grill-me`, or `grill-with-docs` as the uncertainty requires. |
| **Plan** | feature, requirements, task breakdown, durable decision | Gather targeted evidence, then write a plan and wait for approval. |
| **Prototype** | UI or behavior/state ambiguity | Load `prototype`; use it to answer one question, then capture the answer in the plan rather than promoting the throwaway code. |
| **Build** | approved plan or small reversible change | Load `implement`; add `tdd` when a red-green loop will de-risk the slice. |
| **Diagnose** | failure, regression, or unexpected behavior | Load `diagnosing-bugs`; propose the root cause and test before changing source. |
| **Review** | changed code, PR, or release readiness | Load `code-review`; resolve blocking findings before committing. |
| **Commit** | stage, save, checkpoint | Load `mc-commit`; obtain user confirmation before committing. |
| **PR** | create, update, or prepare a pull request | Load `mc-pr` after the tree is clean and verification is fresh. |

Use `harness-routing` whenever execution mode, model role, subagents, or worktrees matter. It owns harness-specific choices; this skill does not.

## 3. Plan fallback

For work that merits durable planning and has no project convention:

1. Inspect the relevant code and existing plans. State the goal, acceptance checks, scope, risks, open decisions, and proposed seams.
2. For meaningful product, domain, or edge-case uncertainty, load `grill-me` or `grill-with-docs` before approval; use the latter when repository/domain documents should constrain the decision. For UI work, always offer a `prototype`; for non-UI work, offer one only when an experiment will settle a real design question faster than discussion.
3. Choose a unique kebab-case `<slug>`. Write a human-readable `plans.<slug>.md` and its machine-readable companion `plans.<slug>.json` in the repository's established planning location, or the repository root if none exists. Add `plans.<slug>.progress.md` when delivery spans multiple sessions.
4. Put the brief, decisions, task order, acceptance checks, verification hints, dependencies, and out-of-scope items in the Markdown. Put the same task identities, status, dependencies, and verification fields in JSON. Keep Markdown and JSON consistent.
5. Present the plan, prototype result if any, and unresolved risks. Wait for explicit approval before source changes.

Completion: the approved plan identifies every task, its acceptance check, and its dependency state.

## 4. Deliver the approved slice

Implement the smallest dependency-ready slice. Keep one mutation owner; use `harness-routing` for any justified delegation. Before changing a tangled area, either make the smallest verified simplifying extraction or record a scoped follow-up instead of compounding it.

After each slice:

1. Inspect the diff and run the plan's applicable verification after the last source change.
2. Update `plans.<slug>.json` only when its recorded evidence is fresh and the task's acceptance check passes. Append exact commands and outcomes to `plans.<slug>.progress.md` when present.
3. Run `code-review` at the risk boundary or whenever the user asks. Present changed files, behavior evidence, checks, findings, and remaining risks; then ask for commit approval.

Completion: every completed task has fresh evidence; no source change follows that evidence.

## 5. Manage context aggressively

Treat context budget as a first-class constraint, especially on smaller-context models.

- Prefer focused prompts over large dumps of code or logs. Read files directly, summarize the important parts, and keep the next turn tight.
- When a task is getting large or long-running, compact the state into a short summary before continuing: what changed, what is still uncertain, what remains to verify, and what the next step is.
- If the conversation is growing stale or the repo is large, start a fresh plan/progress file or a new subagent session rather than forcing the same context window to carry everything.
- Use a new subagent when a task is broad, independent, or needs a fresh context slice; do not keep piling more context onto a single turn.
- When the task becomes hard enough to need a stronger model, switch explicitly with `/mf target <name>` or a manual model override, rather than letting the session drift.

## Guardrails

- Project instructions, conventions, and local skills always win.
- A passing check and a review are separate evidence.
- Do not commit or open a PR without fresh applicable verification and the required user approval.
- Use the narrowest skill that owns the concern; this router owns sequence, not the underlying specialty.
- When delegating to Pi tidy subagents, keep the child on the current selected family/provider unless the user explicitly asks for a different harness or model. Do not silently switch to Claude bridge or another provider just because delegation is happening.
