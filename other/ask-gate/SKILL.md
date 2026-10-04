---
name: ask-gate
description: "Phrase the action the deterministic Step-13 ask-gate already chose — emit ONE specific information-gain clarification question (Ask) or a brief scoped escalation (Abstain). The gate decides WHICH action and WHICH slot; this skill only writes the words. Use when an advisor must decide answer vs ask-for-missing-context vs abstain on an underspecified request."
---

## Purpose

Default LLMs almost never ask or abstain and are overconfident; retrieved context *suppresses* asking
further. So this behaviour is **imposed by an explicit gate**, not left to the model. This skill is the
**LLM half** of that gate: it converts a chosen action into the right words. It does **not** decide the
action — `tools/subagent_factory/ask_gate.py` already did, deterministically.

## The determinism split (do not cross it)

- **Deterministic (the tool owns it):** *which* action — `answer` / `ask` / `abstain` — and *which*
  slot to ask about. `ask_gate.gate(principle, conversation)` returns
  `{"action", "slot", "missing", "reason"}`. The slot priority, the anti-re-ask escalation, and the
  out-of-scope abstain are **not yours to re-decide**.
- **LLM (this skill owns it):** only the *wording* of that action — the single sharpened question, or
  the scoped abstention sentence. Never override the action. If the gate says `answer`, you do not
  invent a clarifying question; if it says `abstain`, you do not answer anyway.

## Input

- The gate decision dict (`action`, `slot`, `missing`, `reason`).
- The conversation so far and the active principle (`statement`, `must_ask_for`, `applies_when`).

## Procedure — phrase the chosen action

**`ask`** — write exactly **one** question that names the missing variable in `slot`:

- Be specific and decision-relevant: name the variable and why it changes the answer
  ("What's your monthly request volume? Below ~1k/day a single instance is fine; above it changes the
  topology"), not a generic "tell me more" or "can you share more context".
- Ask for **one** slot only — the one in `slot`. **Never over-ask** (over-asking hurts and is
  nonmonotonic): do not bundle the other `missing` slots into the same turn, and do not add a checklist.
- **Never re-ask.** If the gate returned `abstain`, the slot was already asked and unsupplied — do not
  ask it again under any phrasing.

**`abstain`** — write a brief, scoped escalation:

- If `slot` is set, the user was already asked and did not supply it: say plainly that you can't give a
  safe answer without that input, name it once, and hand off / suggest who or what can decide — do not
  loop the question.
- If `slot` is `None`, the request is out of scope: say so in one sentence and point to the right
  resource. Do not pretend to answer.

**`answer`** — every required slot is filled. Answer the request directly. Do **not** prepend a
clarifying question or a "just to confirm" — that is the over-ask failure the gate exists to prevent.

## Uncertainty attribution (which way to lean)

- **Data-uncertain** (a decision-relevant input is missing) → `ask`. The fix is one input from the user.
- **Model-uncertain** (the question is outside what the principles support, or genuinely undecidable
  from any answerable input) → `abstain` / escalate. More user input would not help.

## Guardrails

- One question per turn, naming one variable. No generic asks. No bundling.
- Never contradict the gate's action. The deterministic gate is the source of truth for *whether* to
  ask; you are the source only for *how it reads*.
