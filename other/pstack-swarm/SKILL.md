---
name: pstack-swarm
description: "Coordinate bounded parallel coverage over independent slices using the active chat model. Use only when the user explicitly requests swarm or pstack-swarm."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/swarm
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Swarm

Partition the work, collect every required result, and return one evidence-based report. The host chooses supported execution facilities; this skill does not require cloud workers.

Run this workflow only when the user explicitly names swarm or pstack-swarm, including a request within pstack-mode. A request for broad coverage, parallel work, or rigor alone is not opt-in. A router or another skill cannot supply that opt-in. Without it, cover the task directly without starting a swarm.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Frame

Define the overall completion condition and required slices. Use separate slices for coverage; use identical briefs only for an explicitly useful race or comparison. State the selection rule before a race: first proven pass, compare all, or best candidate.

Choose a bounded worker count from the request, task seams, host concurrency, and local resource limits. Never hide parallel heavy subprocesses inside one resource slot. Identify shared mutable state before dispatch.

Each brief stands alone: goal, owned scope, exact version/base, allowed effects, verification method, and report contract. Independent writers get separate outputs or worktrees. A shared browser, database fixture, or integration branch has one owner.

## Run and collect

Dispatch only supported, authorized inherited-model workers. If delegation or guaranteed model inheritance is unavailable, cover the slices sequentially and disclose that fallback.

Wait for terminal results. Inspect artifacts and important cited evidence. A worker report lacking its required version or method is incomplete; clarify once or record a gap. Dropouts and unavailable environments are never passes.

Workers return PASS, ISSUES, or BLOCKED with evidence. Proven defects name every relevant trigger and mechanism. The parent owns integration and final verification.

## Deliver

A compact table of slices, versions, results, verified evidence, and gaps. Distinguish worker-reported outcomes from parent-verified conclusions. Follow the declared race rule and do not claim total coverage when a required slice is missing.
