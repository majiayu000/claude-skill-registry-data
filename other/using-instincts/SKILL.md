---
name: using-instincts
description: Use when doing any work in a project that has the instincts plugin installed
---

superpowers is the base process: brainstorm, spec, plan, TDD, verify. instincts is one level finer — a set of working reflexes that keep that process honest rather than just followed. This skill is the map to them.

## The rule

Load an instinct with the Skill tool the **first time it applies in a session** — before you act on it, then follow the skill you loaded. If several instincts hit the same move, load them all in one response.

Once loaded, a skill stays active for the rest of the session: apply it without re-invoking. One exception — after a context compact, if you can no longer see the skill's full text, it's gone; reload it before relying on it.

Acting on an instinct that was never loaded this session is working from memory, and it doesn't count: you lose the current text and the checklist, and nothing shows the reflex ran — exactly how corners get cut. Nothing runs until you call the Skill tool. The load is once per skill per session; the cost argument is spent.

| Rationalization | Reality |
|---|---|
| "I applied it internally — same result" | If it was never loaded this session, you worked from memory, not the current text. No checklist, no trace. |
| "The map line below tells me enough" | The map routes, it doesn't teach. The method lives in the skill. |
| "Loading it won't change what I'm about to type" | Then it costs seconds and confirms you. When it would have changed something — that's the whole point. |
| "No time for ceremony right now" | One load per skill per session, seconds each. You'll spend longer justifying the skip. |
| "I loaded it earlier" — said after a compact | If you can't see its full text anymore, it's gone. Reload before relying on it. |
| "superpowers already forces skills, so these are covered" | Not covered — each instinct still gets its own first load. |
| You named an instinct in your reasoning without ever loading it | Naming it is not running it. Load the skill, then proceed. |

## User instructions win

User instructions — CLAUDE.md, AGENTS.md, direct requests — take precedence over any instinct here, and instincts take precedence over default behavior. Never cite an instinct against what the user explicitly asked for; skip a skill only when they told you to.

## The instincts, by what they protect

Load the one that matches the move you're about to make.

Verify against the world, not your memory:
- **verify-against-code** — before asserting what code or a product does.
- **question-the-premise** — when several fixes on one hypothesis have failed, or a symptom looks impossible.
- **critical-thinking** — before building something someone proposed, however confident it sounds.
- **plan-with-teeth** — before writing an implementation plan or entering plan mode.

Build for the failure you won't be there to see:
- **logging-for-remote-diagnosis** — when building anything that could fail on a machine out of reach.
- **fix-the-root-cause** — when fixing any bug, especially one surfacing far from its cause.
- **fix-in-the-shared-layer** — when a bug surfaces in your own shared code: a library, base class, SDK.

Look wider than the line in front of you:
- **entry-point-audit** — before a cross-cutting change: a gate, limit, or rule that must hold everywhere.
- **project-onto-all-systems** — when a change creates, edits, or removes state.
- **user-action-edge-cases** — when depending on external state a person controls: a file, a record, a folder.
- **feasibility-guard** — before building or agreeing to build, especially the big or clever ask.
- **opportunistic-fixes** — when noticing an incidental problem in the area you're already editing.
- **no-duplicate-logic** — before adding a case, check, or branch to an existing function.

Design for real conditions, not the happy path:
- **performance-at-scale** — when code runs per item, per frame, or per event, or a collection can grow large.
- **build-release-mindset** — when touching build, release, packaging, or CI.
- **ux-designer-mindset** — when building or changing anything a user interacts with.

Finish honestly:
- **tests-with-teeth** — when writing or reviewing a test, or accepting "tests pass" as evidence.
- **de-ai-prose** — before showing prose a human will read: docs, commits, UI copy.
- **independent-review-gate** — before calling complex or shippable work done, or merging.

## Pairing with superpowers

These sit on top of superpowers, the base process, installed separately (`/plugin marketplace add obra/superpowers`, then `/plugin install superpowers`). Without it, instincts works standalone — the reflexes just have less process around them.
