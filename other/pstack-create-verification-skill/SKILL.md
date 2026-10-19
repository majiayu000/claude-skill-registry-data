---
name: pstack-create-verification-skill
description: "Generate and prove a project-specific skill for driving real UI, CLI, API, or library behavior. Use when a project needs repeatable user-flow verification or a maintained feature map."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/create-verification-skill
  upstream-commit: e5136d82418d2db3165ea1050d17577cd618cc05
  adaptation: portable-chat-inherited
---

# Create a verification skill

Create portable instructions grounded in the real application, then execute them once. This global generator produces project-specific verification material; it cannot make app-specific selectors universal.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Interview the repository

Find the user's real entry points, existing feature maps and test tools, startup commands, prerequisites, authentication, safe data, readiness signals, and observable results.

Reuse existing application-control mechanisms. Prefer the host's integrated browser for ordinary web inspection when available. Use a reproducible automation runner for tracing, video, isolated sessions, or repeatable scripted checks when needed; explain the capability choice. An unavailable control interface is a stated limitation.

Record checkout/version and server ownership. Reuse a compatible server. Isolate ports, profiles, data, and writable state where required. Check the actual effects of dry-run and test modes.

## Generate

Write a standard SKILL.md with name and description in the user's requested location or the environment's discovered project skill location. If automatic discovery is unknown, use a neutral project documentation location and give the direct file invocation. Do not create product-specific configuration just to register it.

Include concrete, observed procedures:

- Launch: existing command, prerequisites by variable name, required migrations and seed data, usable readiness, version check, and owned teardown.
- Doctor: read-only confirmation that this is the intended healthy instance.
- Drive: real routes, stable selectors, commands, or inputs from this repository.
- Evidence: action, resulting state, relevant persisted or external side effects, and a preserved artifact location.
- Cleanup: remove only owned temporary state and processes; keep evidence.
- Helpers: dependencies and actual invocation for any script shipped.

Build on the existing feature-map index. Cover a bounded initial set of real features and mark the remaining coverage. Each feature identifies entry points, roles, variants, prerequisites, driving recipe, expected observations, and gotchas. Link existing documentation rather than duplicating it.

When the app has initial data setup, prove startup from an empty, task-owned data directory, including its required migrations and seed data. Ready means the mapped flow is usable; a responding port or healthy database can precede completion of initialization. Preserve existing data. If a journey lacks a seed precondition, record the failed or incomplete journey and the missing prerequisite in its gotchas rather than weakening the journey to make it pass.

## Prove and deliver

Execute launch, doctor, one representative mapped feature, capture, and cleanup. Confirm the evidence survives. Failed attempts clean their own residue. Never kill by process name or interrupt pre-existing services.

Use authorized local/test data. Mock only an explicitly isolated or approved external boundary and label what that leaves unverified. UI success alone does not prove persistence.

When proof uses a substitute environment, list the setup steps it performed that the real target will not provide. Those steps remain unverified until exercised on the intended target; local success does not prove remote setup or provider behavior.

If startup or access is blocked, deliver a labeled draft with the exact missing prerequisite; do not repair unrelated product code. State what ran, what is covered, and what remains unverified. Maintenance can use pstack-maintain-verification-skill when installed, or the same source-plus-live audit directly.
