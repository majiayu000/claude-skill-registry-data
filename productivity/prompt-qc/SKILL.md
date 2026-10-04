---
name: prompt-qc
description: Quality-check generation prompts for self-containment, canon, model-specific format, reference labels, exact text and dialogue, timing, camera contradictions, continuity, and prompt slop.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Prompt QC

## Workflow

1. Read core contract, style rules, dramaturgy rules when the source is visual, continuity rules, reference asset rules, prompt packet schema, the source brief, and the target adapter skill.
2. Check each prompt for:
   - source ID present
   - target model and mode correct
   - every subject and reference identified with the correct role
   - no "same as before" dependency
   - exact visible text and dialogue preserved
   - duration and timeline agree
   - camera instructions are physically compatible and motivated by the shot brief
   - lighting does not contradict itself
   - character, wardrobe, prop, and location continuity match canon
   - no canonical `must_not_be` trait is requested
   - required speech/movement/stillness intent is not accidentally contradicted
   - required visible-dialogue line, speaker, mouth visibility, cut policy, and timing survive adaptation
   - required end-frame state and capture behavior survive without conflicting camera instructions
   - negative constraints do not fight positive instructions
   - model-specific fields and section order are correct
   - for MiniMax H3, `h3_base_skill` is `h3-prompt-writing`, the applicable style skill was selected (or explicitly recorded as `none`), the style overlay did not replace the H3 field structure, the final prompt follows the selected base/Ref2VA guide, and `scripts/minimax_h3_prompt_validator.py` passes for the actual mode and duration before generation
3. Fix prompt-level defects directly. Escalate canon conflicts to the upstream artifact.
4. Run the style checker over prompt files.

## Done

Every prompt can be handed alone to a generation operator with its named reference media and still produce the intended task definition.
