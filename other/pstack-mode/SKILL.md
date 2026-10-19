---
name: pstack-mode
description: "Route an explicitly requested pstack engineering workflow through investigation, design, impact review, measurement, or real verification. Use when the user names pstack-mode or asks to work in that style."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/e5136d82418d2db3165ea1050d17577cd618cc05/pstack/skills/poteto-mode
  upstream-commit: e5136d82418d2db3165ea1050d17577cd618cc05
  adaptation: portable-chat-inherited
---

# Pstack mode

Choose only the procedures that help prove the user's requested outcome. This is a portable routing skill, not an editor custom mode or a permanent chat setting.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Start with the requested outcome

Distinguish read-only investigation, design, review, implementation, measurement, verification, and publication. Record scope, preserved behavior, and the observable done condition.

For a simple edit, work directly. For a cross-layer task, inspect existing feature maps, ownership, contracts, and instructions first. A request for all cases needs a bounded coverage list.

## Route by need

The sibling skills below are optional helpers, not hidden prerequisites. Read their instructions before using them. If absent, perform the named capability directly and disclose any consequential gap.

| Need | Procedure |
| --- | --- |
| Refine the approach before execution | pstack-sharpen |
| How it works or where it belongs | pstack-how |
| Historical rationale or regression lineage | pstack-why |
| Risk outside the diff | pstack-blast-radius |
| Competing architecture shapes | pstack-architect |
| Adversarial review | pstack-interrogate |
| Performance evidence | pstack-benchmark-checklist |
| Reconstruct previous work | pstack-recall |
| Catch up on progress in this chat | pstack-ketchup |
| Real user-flow verification | pstack-create-verification-skill, pstack-maintain-verification-skill |
| An unusual multi-phase run | pstack-figure-it-out, pstack-show-me-your-work |
| Repeated proven mistakes | pstack-correct |
| TypeScript model or boundary risks | pstack-typescript-best-practices |
| Explanation or prose cleanup | pstack-teach, pstack-unslop |

Reuse applicable existing architecture, design, review, testing, and PR workflows instead of stacking redundant procedures.

## Arena and swarm require explicit opt-in

Use pstack-arena or pstack-swarm only when the user explicitly requests that named workflow, directly or within a prompt such as "pstack-mode, use swarm and arena". Opting into one does not enable the other.

Invoking pstack-mode, asking for rigor, alternatives, architecture, review, or broad coverage does not enable either workflow. This rule also applies to routed helpers: their recommendations cannot enable arena or swarm. Without explicit opt-in, work directly and compare local sketches when useful; do not recreate either workflow through a renamed fan-out or another helper.

After explicit opt-in, read the requested sibling's SKILL.md and follow its environment contract and the user's budget. The installed skills remain available for that request.

## Engineering decisions

Prefer the smallest change supported by a reproduced symptom or explicit requirement. Model ownership and domain state before adding branches. Validate untrusted inputs at boundaries while retaining runtime security and concurrency checks.

Remove dead complexity only within scope. Preserve compatibility for external consumers and independently deployed services. Use deterministic scripts for truly repetitive work; avoid turning a small task into tooling.

Measure before calling an optimization successful. Verify the real artifact rather than accepting a summary, build, or green CI as complete proof. Partition concurrent writers and retain one owner for shared integration state.

Revisit an assumption after repeated failures. Retain meaningful behavioral and negative-path tests; test counts and file counts do not measure protection.

When debugging, distinguish legitimate states that need handling from invalid states whose producer needs correction. If the deciding fact took a deep investigation to find, propose a cheap log, metric, or diagnostic that would have exposed it sooner. Implement that signal only when it belongs to the authorized change.

## Close within scope

Report what changed, why, what was actually checked, and material gaps. Keep evidence local unless publication includes it. Honor a request to stop, avoid more tests, preserve visuals, or defer product decisions.

Commits, PRs, merges, external messages, deployments, cleanup of others' resources, and schedules follow the user's actual authorization. When opening a PR, honor the host/repository's issue and ticket checks and do not invent references. Skill bugs are reported or fixed within scope, without an automatic separate PR.

This skill cannot provide persistence across restarts, scheduling, unattended execution, or model diversity when the host lacks those capabilities.
