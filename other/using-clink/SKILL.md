---
name: using-clink
description: The entry point for delegating to another AI CLI agent through PAL's clink tool. Decides which of the four clink skills you actually want before you spend a call — executing a scoped subtask, convening a panel for judgment, hunting a bug across agents, or deciding who may do the work at all. Reach for it whenever you are about to delegate, whenever you are choosing between a subagent and a panel, and whenever a delegation came back wrong and you are not sure the routing was right. Triggers include "delegate this", "ask the other AIs", "get a second opinion", "run this in parallel", "which model should review this".
---

# Using Clink

**Pick the instrument before you spend a call.** Each skill below carries its own rules — the model ladder, the provenance rule, the verify-everything discipline. This file only decides which one you are in.

## The routing decision

| You want | Skill |
|---|---|
| A scoped subtask **executed** and handed back done — an implementation, a bulk transform, a focused lookup, a first draft | **`clink-subagents`** |
| **Judgment** — which design wins, what is wrong with this plan, is this code right | **`clink-brainstorm`** |
| To find out **why something is broken**, using more than one agent | **`clink-debug`** |
| To decide **who may do it at all**, and to pick the model from measured scores rather than memory | **`clink-masteragent`** |

**`clink-masteragent` is a precondition, not a fourth option.** Read it before any of the other three; it owns what you may never hand out, and picking a model from recollection instead of the score table is a documented way this goes wrong.

## Work versus judgment is the whole decision

It is the one that gets made backwards, and it is expensive in both directions:

- **A panel convened for a question one worker could answer** burns several lanes to produce an opinion where a fact was wanted.
- **A worker sent to produce judgment** returns a confident answer nobody checked — and if it is a bug hypothesis, `clink-debug` exists precisely because the wrong seat makes a wrong cause harder to reopen.

Ask what you will have when it returns: **finished work, or a position to weigh.** That answers it.

## Resolve the tool name; the prefix is not part of the tool

**The tool is `mcp__<server>__clink`, and `<server>` is the key the CLIENT registered it under — not the server's own name.** Every example in this family spells it `mcp__pal__clink`, which is *this machine's* instance, not the contract.

**Resolve it before the first call, the same way `t4-project-bootstrap` resolves a binary before declaring it missing:**

```sh
claude mcp list        # the key on the left of the colon IS the prefix
# pal: openclink  - ✔ Connected      ->  the tool is mcp__pal__clink
```

**The trap is that the two names drift apart and nothing complains.** On 2026-08-20 this machine reported `pal: openclink` — the server had been renamed to `openclink` and the registration key was still `pal`. An agent reading the rename and "correcting" the spelling would have called `mcp__openclink__clink`, which resolves to nothing, on every one of the four skills at once. That is `#204`, and it is why `PR #206` cannot be merged by flipping the string: **both spellings are wrong on some machine, so the fix is to stop spelling it.**

**The enforcement layer already does this and is the precedent, not the exception.** `hooks/t4-delegation-gate` matches `^mcp__[A-Za-z0-9_.-]+__clink$` and `hooks/t4-clink-boundary` says in its own comment that the name is *"`mcp__pal__clink` on this machine, and something else on a machine that registered it differently."* The hooks were written to survive the rename; the prose was not.

**So when a `clink` call fails to resolve, that is the first thing to check** — before concluding `clink` is unavailable and routing around it. An unresolvable prefix and an absent server produce the same error and need opposite responses, which is the tool-resolution rule one layer up.

## Before you delegate at all

Three things decide whether a delegation is worth making, and all three are in `clink-subagents` — read them there rather than from memory:

- **Can you verify the result?** If not, do not delegate it.
- **Is it self-contained?** The agent has zero context from your conversation.
- **Is it worth the latency?** A read-heavy call against a real repo runs in minutes, not seconds.

## When clink is the wrong tool

If the work is small enough that you would finish it before a call bootstraps, do it yourself. If it needs your full session context or your taste, keep it. Delegation is for offloading effort and running independent chunks in parallel — never for avoiding the thinking.
