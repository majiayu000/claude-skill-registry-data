---
name: anti-cascade-collapse
description: Prevents order-gap hallucination — where the model detects a false premise when asked directly but misses it when embedded in a complex multi-step task. Enforces re-verification of assumptions at each step.
---

# Anti-Cascade Collapse Skill

## Problem

The model can detect a false premise when asked directly at step 2, but fails to catch it at step 5 when it arrives as an assumption embedded in an escalating task. This is called **order-gap hallucination** or **cascade collapse**.

Research shows that correct detection at step 2 (direct question) collapses to near-zero at step 5 (embedded assumption). The safety circuit is present but suppressed by accumulated conversational pressure — like a signal masked by noise.

Example:
- Step 2: "Is X method valid?" → "No, it doesn't exist." (correct)
- Step 5: "Now implement the feature using X method" → Writes code using X method. (incorrect — the earlier correct detection is suppressed by the task pressure)

## Detection triggers

Activate when:
- Working on a complex multi-step task
- An earlier step identified a constraint, limitation, or invalidity
- The current step is making an assumption that contradicts earlier findings
- The conversation has been going for several turns
- You're deep in implementation and haven't re-checked your starting assumptions

## Protocol

### 1. Surface earlier constraints
Before each major step, explicitly restate the constraints learned earlier:
- "Earlier I determined that X method doesn't exist in this version."
- "The user said the config file is YAML, not JSON."
- "The project uses SQLAlchemy 2.0, not 1.x."

Do not assume these are "in context" — they get suppressed under task pressure.

### 2. Re-verify assumptions per step
For each step in a multi-step task:
- Check: does this step still respect all earlier constraints?
- If not, stop and re-evaluate before proceeding.

### 3. Cross-step consistency check
Before delivering a final result:
- Compare the output against your earlier findings
- If you said X was impossible in step 2, but step 5 uses X, you have a cascade failure
- Fix the inconsistency before presenting the result

### 4. When the task pressures you to ignore a constraint
- Recognize this pressure
- State it explicitly: "I'm about to assume Y, but I previously determined Y was false."
- Do not proceed until the contradiction is resolved

## When NOT to use
- Single-step tasks (no cascade possible)
- Steps that are genuinely independent
- User explicitly says "ignore the earlier constraint"

## Bundled Script

Copy `check-assumptions.ps1` to your project's `.ai_scripts/` directory:

```powershell
# From skill source
cp <skill-path>/anti-cascade-collapse/scripts/check-assumptions.ps1 .ai_scripts/
```

Analyzes a task script or plan to ensure each step has explicit verification checks:

```powershell
.ai_scripts\check-assumptions.ps1 -FilePath .ai_scripts\TODO.md
```

## Cross-references

- **anti-premature-termination** — Both prevent cascade failure. anti-cascade-collapse handles step-by-step assumption re-verification; anti-premature-termination handles completion criteria.

- **follow-existing-patterns** — Re-verifying assumptions requires knowing what the existing patterns actually are.

- **anti-sycophancy** — Prevents agreeing with a false assumption instead of re-verifying it.
- **skill-loader** — Apply the capped selection policy when deciding whether anti-premature-termination or follow-existing-patterns should also be active for multi-step assumption re-verification.
