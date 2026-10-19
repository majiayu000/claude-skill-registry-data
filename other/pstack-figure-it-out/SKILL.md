---
name: pstack-figure-it-out
description: "Design and execute an evidence-based workflow for a large migration or unusual multi-part task. Use when no narrower procedure fits and the work needs explicit phases, checkpoints, and auditable progress."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/figure-it-out
  upstream-commit: e5136d82418d2db3165ea1050d17577cd618cc05
  adaptation: portable-chat-inherited
---

# Figure it out

Create the smallest workflow that can prove the requested outcome. Scale rigor to the real risk and unknowns.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Frame

State scope, the observable completion condition, preserved contracts, environment prerequisites, and known blockers. Distinguish diagnosis, implementation, and publication according to the request.

Inspect existing tools before building a new harness. Capture the pre-change baseline. Start with the riskiest unknown, not the easiest volume of edits.

## Design the units

Choose small independently verifiable units. Separate reads, experiments, edits, integration, and final verification. Use a script or codemod for deterministic repetitive work when that is simpler than manual edits.

Give concurrent writers separate owned outputs or worktrees; integrate centrally. Limit workers and resource-heavy checks to the host's controls. Direct work is the default when coordination costs more than it saves.

Record major decisions and evidence in an existing local trail or a compact TSV. Keep it out of publication unless the user requests it.

## Execute experiments

For each uncertain unit, state a hypothesis, make the smallest authorized change, and compare against the real completion condition. Keep a supported improvement. Remove only your own rejected changes, preserving concurrent user work.

A result is verified, not verified, or inconclusive. After two failures under the same premise, write that premise down and test it directly before trying another variant. Choose an observation that would differ if the premise were false, and preserve the observation and result in the trail. Make the check rerunnable when useful. Follow contradictory evidence to a different cause; if the check is unavailable, record the premise as unverified rather than treating another retry as proof.

Improve a flawed observation method explicitly rather than weakening the acceptance criterion.

## Close

Integrate with the relevant current base when authorized. Recheck risks introduced by that integration without repeating unrelated proven work. Validate the end-to-end outcome, not just each component.

Report the units completed, evidence, decisions, remaining gaps, and precise stopping condition. This workflow has no automatic commits, PRs, deployment, perpetual loop, or scheduling.
