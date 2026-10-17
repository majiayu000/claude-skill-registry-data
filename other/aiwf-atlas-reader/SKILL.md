---
name: aiwf-atlas-reader
description: AIWF Atlas Reader protocol skill for Atlas Reader LoRA repo work, AIWF Atlas source docs, training records, evaluation plans, installer or training scripts, source/citation checks, no-wins status preservation, and measured-result verification. Use when working on Atlas Reader, Atlas LoRA adapter, Atlas protocol behavior, context-pack construction, Qwen LoRA failures, or comparing chat attachment behavior against agent protocol or LoRA-trained behavior.
---

# AIWF Atlas Reader

Use this skill when the user asks to work on the Atlas Reader LoRA repo, AIWF Atlas source docs, training records, evaluation plans, installer scripts, or training scripts.

## Operating Rules

1. Preserve no-wins status unless measured logs exist.
2. Treat report templates as templates.
3. Use source and citation files before adding factual claims.
4. Prefer small, reviewable changes.
5. Do not promote milestones automatically.
6. Distinguish chat attachment baseline, agent protocol behavior, and LoRA-trained behavior.

## Required Checks

Before claiming a result, confirm the repo contains a real output file or run log.

If no run log exists, use:

```text
not run yet
not verified yet
template only
prepared for testing
```

## Comparison Logic

If agent-guided behavior looks better than chat attachment behavior, mark that as an agent-protocol observation only.

If a LoRA fails on Qwen, do not conclude that Atlas failed. Check:

- base model choice
- chat template
- record formatting
- rank
- target modules
- learning rate
- dropout
- training data quality
- eval split
- context-pack construction

## Output

Be direct, source-aware, and practical.

No hype. No fake wins. Unknown means instrument it.
