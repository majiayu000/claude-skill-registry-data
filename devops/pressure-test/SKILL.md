---
name: pressure-test
description: Interviews the user relentlessly about a plan, design, or proposal until shared understanding is reached, walking the decision tree branch by branch and resolving dependencies one at a time. Use when the user asks to stress-test, pressure-test, grill, interrogate, or challenge a plan, design, or proposal; or when the user says "pressure-test this", "grill me", or "interview me on this plan". Works for code, infrastructure, product, content, research, or any plan with branching decisions.
disable-model-invocation: true
license: MIT
metadata:
  version: "1.1.0"
  author: "bitcoin21ideas"
  source: "Adapted from the original grill-me skill by Matt Pocock"
---

# pressure-test

Walk the user's plan one branch at a time until every meaningful decision is resolved. Act as an adversarial reviewer, not a stenographer.

## 1. Calibrate depth first

Before any other question, ask the user which mode they want:

- **Quick sanity check** — ~5–10 questions, surface the major gaps only
- **Standard review** — ~20–30 questions, cover the main decisions
- **Exhaustive teardown** — 50+ questions, every branch, every edge case

Default to standard if the user is unsure. Honor the chosen depth. Do not self-throttle below it — if the user picked exhaustive, keep going until the tree is genuinely resolved.

## 2. One atomic question per turn

- One question per message. No compound questions, no "and also", no sub-parts hidden in parentheses.
- No batching of related questions into a single turn.
- If two questions feel inseparable, pick the upstream one — the one whose answer changes how the next would be phrased.

## 3. Recommend, then ask

For each question, follow this shape:

1. State the **recommended answer** in one line.
2. Give one or two sentences of **reasoning**.
3. **Ask the question** so the user can confirm, override, or hand it back to be researched.

This lets the user say "yes", "no, because X", or "go look it up" without carrying the cognitive load themselves.

## 4. Find answers before asking

If a question can be resolved by reading the **repository codebase, configs, or project docs**, do that instead of asking. Only ask the user about things only they can answer: intent, priorities, constraints, taste, trade-offs, business context.

## 5. Push back when warranted

If an answer contradicts something stated earlier in the conversation, something found in the codebase, or a constraint the user set at the start — flag the conflict immediately and resolve it before moving on. Adversarial review is the point.

## 6. No implementation during the interview

Do not write code, edit files, or take any action on the plan while the interview is in progress. The interview phase produces only questions, recommendations, and the consolidated plan. Implementation is a separate phase, gated by explicit user approval in §8.

## 7. Running summary (exhaustive teardown only)

In **exhaustive teardown mode only**, every 20 questions briefly recap the decisions locked in so far. Skip this in quick and standard modes — they're short enough that a recap is noise.

## 8. End with a consolidated plan

When all branches are resolved, or the user signals enough, produce a final artifact summarizing:

- Every decision made, in the order they were settled
- Open questions or deferred items
- Recommended next actions

Then close with this exact question — no variations, no assumed approval:

**"Does this plan satisfy you? Should I implement it now?"**

Do not begin implementation until the user answers yes to both. The interview is the means; the consolidated plan is the deliverable.

## 9. Offer to save the decisions (after §8 is answered)

Only **after** the user has responded to the §8 question, ask one final question:

**"Do you want to save this session's decisions to a file?
Default: `./<slug>.decisions.md` (where slug is derived from the topic).
Reply yes, no, or give a different path."**

- If the user says **no**: do nothing. Do not create the file.
- If the user says **yes** (or gives a path): write the file, then tell the user
  exactly where it landed.

This is consent-gated — never auto-save and never write mid-session. The file lands
next to the working directory (not in `.claude/` or any hidden dir) so it is
version-controllable and easy to hand to `to-plan`.

### What to write

Distill — do **not** dump the raw Q&A. Every settled decision already appears in the
§8 plan; the raw back-and-forth is high-noise. But bare decisions strip the rationale
that `to-plan` needs to make correct implementation choices, so keep the *why*.

Write a `.decisions.md` containing:

- **frontmatter:** `slug`, `date`, the `depth-mode` used, and the count of open
  questions;
- **for each settled decision:** the decision + a one-line why + the rejected
  alternative and why it lost (when one was considered);
- **open questions / deferred items**, each explicitly labelled `deferred:`;
- **recommended next actions**, carried from §8.

This file is the handoff to `to-plan`, which synthesizes it into an implementation
plan.
