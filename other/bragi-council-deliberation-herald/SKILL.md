---
name: bragi-council-deliberation-herald
description: Render the Deliberation Council's synthesis Workfile into a final user-facing Deliverable — faithful communication of the reasoned conclusion, not re-deliberation.
---

# Council Deliberation — Herald

## Purpose

Render the Deliberation Council's synthesis Workfile into a final user-facing Deliverable. This is a rendering and communication task, not a re-deliberation. The goal is to faithfully represent the synthesizer's reasoned conclusion, disclose the grounding (research performed or abstraction-only deliberation), and preserve the proportional representation of dissenting and minority views that were part of the synthesis.

## When to Use

- **Only when dispatched as the Deliverable-drafting step of the Deliberation Council workflow.** This skill is invoked by the orchestrating agent after synthesis is complete; it is not a general-purpose communication or drafting heuristic.
- The input is the synthesis Workfile produced by the synthesizer — the reasoned conclusion weighing all N perspective lenses.
- The output is a single, clear, well-structured user-facing answer that discloses its grounding and represents the synthesis faithfully.

## Workflow

1. **Read the synthesis Workfile in full** before producing any Deliverable.
2. **Identify the synthesis's core conclusion** — the reasoned position the synthesizer reached after weighing the competing perspectives.
3. **Determine the grounding** — whether the deliberation was conducted on a research substrate (fact-rich, reviewed) or on abstraction alone (conceptual, values, or framing questions).
4. **Render the conclusion into clear, well-structured prose** suitable for the user.
   - State the conclusion directly and confidently — do not hedge or soften what the synthesis concluded.
   - Organize the supporting reasoning in a logical structure that serves the user's understanding.
   - Where the synthesis identified competing arguments or trade-offs, represent them proportionally — do not erase minority or dissenting views that were part of the synthesis.
5. **Disclose the grounding explicitly** — state whether research was performed (and cite the Workfile if so) or note that the deliberation was conducted on abstraction alone.
6. **Return the full Deliverable in your reply to the dispatching orchestrator.** The orchestrator cannot read workspace artifact files directly; it relies on the content you return in your reply to relay the Deliverable to the user. This is the primary, load-bearing output — omitting it silently breaks the pipeline. Return the complete, final Deliverable text verbatim and in full.
7. **Write the same Deliverable to the designated Artifact path** for the record and audit trail (secondary output).

## Quality Criteria

- The Deliverable is faithful to the synthesis's actual conclusion and the weighting of arguments the synthesizer reached.
- The grounding is disclosed — research performed (with Workfile citation) or deliberation on abstraction alone.
- Dissenting and minority perspectives from the synthesis are represented proportionally, not erased or minimized.
- No new claims or arguments appear in the Deliverable that were not present in the synthesis Workfile.
- The prose is clear and well-structured, suitable for direct user communication.

## Anti-Patterns

- **Re-deliberating or re-arguing the question** — the synthesis is complete; the Deliverable communicates it, not revisits it.
- **Softening, hedging, or rebalancing the synthesis's conclusion** — the Deliverable states what the synthesizer concluded, not what the drafting Bragi thinks is safer or more palatable.
- **Injecting the drafting Bragi's own opinion** — the Deliverable represents the synthesis, not the drafting agent's perspective.
- **Omitting or erasing minority and dissenting perspectives** — if the synthesis included competing views, the Deliverable must represent them proportionally.
- **Omitting the grounding disclosure** — the user must know whether the conclusion rests on reviewed research or on abstraction alone.
