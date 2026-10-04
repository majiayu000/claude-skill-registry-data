---
name: sound-design
description: Design ambience, Foley, hard effects, transitions, perspective, silence, and generated SFX cues tied to scenes and shots, then route cues to Stable Audio 3 or video-native audio when appropriate.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Sound Design

## Workflow

1. Read core contract, film grammar, screenplay, shot briefs, continuity, and score plan.
2. Separate ambience, Foley, hard effects, designed effects, transitions, and intentional silence.
3. Write `04_generation/sfx_cues.jsonl` using `SFX-###` IDs.
4. Each cue states physical source, action, duration, distance or mic perspective, room or exterior character, processing if needed, sync point, and avoid list.
5. Route isolated SFX and ambience to Stable Audio 3. If H3 or LTX is generating native synchronized sound, state which sounds should be generated in-shot and which remain separate post elements.

## Done

Every important on-screen physical action has a sound decision, including the decision to remain silent.
