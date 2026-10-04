---
name: using-cortex
description: >
  Use when the user asks to check the cortex vault, refers to earlier work
  ("last time", "that project", "we discussed", "之前那個", "上次的"), asks
  to resume something from a previous session, or names a topic the
  SessionStart hook listed for this vault. Routes the request to the
  cortex-query skill so the answer is grounded in the user's own notes
  instead of re-derived. Do not use for general questions, for fresh work
  with no prior-context signal, or when the user has asked to skip the
  vault.
---

# Using Cortex — When to Consult the Vault

The cortex vault is the user's own knowledge base: distilled Notes,
Projects, and Raw session records. This skill decides **when**
consulting it is warranted, and hands the actual search to the
`cortex-query` skill.

Retrieval is worth doing when there is a concrete signal that prior context
exists. It is not worth doing on speculation — an unprompted search costs
the user tokens and latency, and surfacing unrelated notes pollutes the
answer.

## Search the vault when any of these is true

1. **Explicit request.** The user asks for it: "check cortex", "查一下
   cortex", "有沒有記錄過", "do I have notes on this".
2. **Reference to prior work.** The user points at something earlier:
   "之前那個", "上次的", "我記得有", "我們討論過", "that ticket", "the
   project we set up", "continue where we left off".
3. **Listed topic.** The request names a topic that the SessionStart hook
   actually listed for this vault. The list is authoritative — match
   against what it showed, not against a guess about what might exist.
4. **Resuming a session.** The user asks to pick up, continue, or hand off
   work from a previous session.

In each case, invoke the `cortex-query` skill rather than searching the
vault directly — that skill knows the retrieval infrastructure, including
`cortex-vec` and its fallbacks.

## Do not search the vault when

- The user has not given any of the four signals above. A question being
  difficult, technical, or open-ended is **not** a signal.
- The user picked **option 4 ("直接開始工作")** from the SessionStart menu,
  or skipped the menu. That choice means "do not go to the vault"; honour
  it for the rest of the session unless the user later asks.
- The user says "don't check cortex", "just answer directly", or similar.
- The task is self-contained: editing code in the current repo, answering
  from the current turn, or anything the conversation already supplies.

When in doubt, **answer directly**. If the answer would have been better
with vault context, the user can ask — and signal 1 then applies.

## How to apply

1. Check the four signals against the user's actual message. If none
   matches, proceed without the vault and do not mention it.
2. If one matches, invoke `cortex-query`.
3. If results are relevant, ground the answer in them and cite the source
   page. If nothing relevant comes back, say so briefly and continue.

## Anti-patterns

- ❌ Searching on every message, or at conversation start, "just in case".
- ❌ Treating a hard question as implicit permission to search.
- ❌ Overriding the user's option 4 / "skip the vault" choice.
- ❌ Grepping the vault directly instead of going through `cortex-query`.
- ❌ Announcing "let me check cortex" when no signal applies.

## Why This Skill Exists

The individual cortex skills fire on their own explicit phrases. This skill
adds the small set of cases where the user has clearly gestured at prior
work without naming a command — so the vault gets consulted when it will
actually help, and stays out of the way otherwise.
