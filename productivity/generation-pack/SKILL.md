---
name: generation-pack
description: Compile story, screenplay, continuity, shots, references, dialogue, score, and sound needs into model-neutral JSONL generation briefs ready for model-specific adapters.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Generation Pack

## Workflow

1. Read core contract, prompt packet schema, model selection, model routing, canon, continuity, reference manifest, and requested production artifacts.
2. Normalize all generation work into the appropriate JSONL files under `04_generation/`.
3. Keep one task per object. A shot, keyframe, voice line, music cue, or SFX cue is one task.
4. Use stable IDs and explicit reference IDs with roles and preserve rules. Carry character performance constraints, canonical exclusions, capture behavior, visible-dialogue sync, approved dialogue-audio authority, reference authority scopes, end-frame state, and temporal-continuity handoffs when they are relevant to the task.
5. Do not choose model-specific syntax here. Preserve an explicit user model choice when one exists. For video work with no user choice, the downstream default is `minimax-h3`.
6. Mark whether identity, exact text, visible lip sync, approved-audio hash parity, first frame, last frame, end-frame state, visual-only motion tail, reference audio, reference binding, or duration is hard-required. If a selected local route cannot honor a hard requirement, record a blocker rather than deleting the requirement.

## Done

A different agent can route every brief to a model adapter without consulting the original conversation.
