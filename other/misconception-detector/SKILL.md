---
name: misconception-detector
description: Use when diagnosing a repeated conceptual mistake and designing a targeted correction loop to replace the faulty mental model.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [assessment, misconceptions, correction, mental-models]
status: stable
---

# Purpose

Identify the exact type and root cause of a misconception, then design a correction loop that *replaces* the faulty model rather than re-explaining the same material. Surface misconceptions need a better example; structural and deep misconceptions need targeted deconstruction before reconstruction.

# Activation

- Learner makes the same conceptual error repeatedly. `check-understanding` or `challenge-generator` flagged a pattern. Learner's explanation reveals a plausible but incorrect mental model. Learner believes they understand but consistently applies it wrong.
- **Skip if**: one-time execution mistake with no conceptual root. Concept hasn't been taught yet → `teach-concept`. Issue is environmental → `debug-teacher`.
- **Routing**: run before `check-understanding` recheck when persistent error detected. Pair with `socratic-mode` for deep misconceptions. Log to `weak-area-tracker`.

# Inputs

- Learner's incorrect statement/reasoning, concept being misunderstood, prior error history, correct mental model.

# Misconception Types

- **Surface**: wrong terminology/label, underlying model partially correct → fix with clear definition + contrast example.
- **Structural**: wrong causal model — knows vocabulary but has mechanism wrong → fix with step-by-step worked trace.
- **Deep**: fundamentally wrong model conflicting with multiple related concepts → fix with `socratic-mode` to expose contradiction first, then correct.

# Workflow

1. **Classify** — Determine type (surface/structural/deep) with supporting evidence. State classification before proceeding.
2. **Articulate** — Restate the learner's incorrect model precisely and without judgment. Confirm with learner that this represents their belief.
3. **Root Cause** — Identify what produced the misconception: overgeneralization, ambiguous terminology, bad analogy, missing prerequisite.
4. **Deconstruct** — Surface: correct definition + contrast. Structural: step-by-step mechanism trace. Deep: `socratic-mode` questions to expose contradiction, then provide correct model.
5. **Install Correct Model** — State the replacement model explicitly. Provide a concrete example that only makes sense under the correct model. Contrast with what the incorrect model would have predicted.
6. **Verify** — Ask learner to apply corrected model to a novel scenario with explanation. If error persists: escalate to `socratic-mode`.
7. **Reinforce** — Log to `weak-area-tracker`. Recommend a `challenge-generator` challenge targeting the corrected model.

# Rules

- DO: classify before correcting — type determines strategy.
- DO: restate and confirm the learner's incorrect model before correcting it.
- DO: provide an explicit replacement model, not just negation ("that's wrong").
- DO: require learner to apply corrected model to a novel case before closing.
- DON'T: correct by repeating the original explanation louder or longer.
- DON'T: assume the misconception — confirm with learner first.
- DON'T: repeat the same correction strategy 3 times — if second attempt fails, escalate to `socratic-mode`.
- DON'T: frame misconceptions as failures — they're signs of engaged learning.

# Output

Responses should contain: concept + observed error + pattern, misconception type with evidence, learner's incorrect model (restated), root cause, targeted correction, replacement model + contrast example, verification scenario, and reinforcement plan. Format naturally.

# Checklist

- [ ] Misconception type classified with evidence.
- [ ] Learner's incorrect model restated and confirmed.
- [ ] Replacement model explicitly provided with contrast example.
- [ ] Verification requires novel application.
