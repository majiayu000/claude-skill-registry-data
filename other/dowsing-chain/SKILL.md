---
name: dowsing-chain
description: >-
  Emperor Time's ring-finger chain — intuition made procedure. Router for four
  aspects: task dowsing, system dowsing, lie detection, and excavate (lost or
  alien codebases). Use when asked to find work, scan for agents, rule on
  contradictions, or survey Pascal/ASM/COBOL/ROM trees. Load one aspect file
  at a time per the Invocation Ritual.
metadata:
  version: 0.4.1
  part-of: emperor-time
  kind: router
---

# Dowsing Chain — router

> *The pendulum doesn't guess. It swings toward what is actually there.*

Dowsing looks like intuition from the outside. Inside, it is a disciplined
sweep: every candidate task and every detected agent must be backed by observed
evidence. **You may not invent work.** A dowsed task with no evidence behind it
is a hallucination wearing a pendulum.

## Selection table — read exactly one

| Your situation | Aspect file |
|---|---|
| "Find something worth doing" / vague goal to scope / between tasks with standing self-assign authority / triaging a codebase | `task-dowsing.md` |
| Lost / ancient / unmarked tree / Pascal / assembly / COBOL / ROM / floppy image | `excavate.md` |
| Building the enlistable-agent roster / "what agents are on this machine?" / pre-Steal-Chain scan / an unknown CLI needs profiling | `system-dowsing.md` |
| A source contradicts another (docs vs code, comment vs behavior, agent claim vs observation, memory vs terminal) and you must rule | `lie-detection.md` |

Multiple situations at once → run them as separate selections in sequence
(excavate often *triggers* lie detection when a comment disagrees with a binary).

## Chain-wide laws (apply in every aspect)

1. **Evidence per swing** — every finding cites a quote, a `file:line`, or a
   command output captured this session. "Seems like" findings are discarded
   before they reach any report.
2. **Read-only chain** — dowsing observes; it never fixes, installs, or signs
   in. Anything worth changing becomes a task candidate for the client (or the
   waterfall), never an in-place edit "while scanning".
3. **One artifact per session** — a dowsing run ends in exactly one output
   (candidate table / roster / ruling / SURVEY.md), recorded in the ledger. An unrecorded
   sweep is lifespan spent on nothing (Vow of Worthy Spend).
4. **Skipped probes are declared** — inapplicable or unrunnable probes are
   listed as skipped in the artifact, so absence of findings is never mistaken
   for absence of problems.
5. **No home language** — `references/language-agnostic.md`. The files pick the language.
