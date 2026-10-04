---
name: narrative-sensemaking
shapes: [narrative-sensemaking]
description: >
  Some questions are "what happened and what did it mean", not "what is the
  mechanism". Use when an account must be reconstructed rather than measured,
  when a sequential process has a missing or out-of-order step, when a story is
  told to explain a failure, or when a claim sounds authoritative but may be
  structurally impossible before any source is even checked.
---

# Narrative Sensemaking

**Problem shape:** the material is an account — an incident write-up, a user
journey, a roadmap story, a vendor claim, a postmortem — and the work is to
recover its structure: which functions occur in which order, which roles are
filled, where the sequence breaks its own grammar, and whether the account is
even structurally possible. Paradigmatic/causal analysis is the wrong mode here
and produces confident nonsense when forced.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [bruner](../../agents/genius/bruner.md) | the question is "what happened and what did it mean?" — decide narrative vs paradigmatic mode explicitly, then analyze the breach of the canonical script that made the event tellable |
| [propp](../../agents/genius/propp.md) | a sequential process (workflow, pipeline, user journey, incident response) needs its invariant functions extracted, its roles abstracted from their current occupants, and its gaps found by grammar rather than by inspection |
| [ibnkhaldun](../../agents/genius/ibnkhaldun.md) | a claim sounds authoritative but may be structurally impossible — filter on structural plausibility *before* evaluating the source; check whether the reported thing could occur at that scale at all |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. State which mode the account is being read in —
   narrative or paradigmatic — before drawing any conclusion from it.
4. Typical chain: ibnkhaldun filters out the structurally impossible → propp
   extracts the function sequence from what survives → bruner reads what the
   breach meant to the people in it. Run via
   `tools/genius-invoker.sh compose ibnkhaldun propp bruner -- "<problem>"`.
5. If no shape above matches, do not force a genius — use a standard team agent
   (INDEX.md routing rule).

## Refuse when

- A mechanism is available and measurable — a causal question is being smuggled
  in as a story. Route to `causal-audit` or `failure-forensics`.
- The narrative is the deliverable's *purpose* rather than its object: this
  shape analyzes accounts, it does not write persuasive ones.
- Structural analysis is being used to dismiss a first-hand report that has not
  been checked against any record — implausible is not the same as false.
