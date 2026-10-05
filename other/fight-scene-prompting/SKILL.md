---
name: fight-scene-prompting
description: Design, compile, or repair fight and action-scene storyboards or video-generation prompts in this repository. Use for 打斗、战斗、追逐、近身攻防、兵器交锋、魔法对轰、大招、战斗镜头节奏、打击感、空间连续性和战斗 Take 返修；not for ordinary dialogue scenes or isolated low-risk contact with no action sequence.
---

# 战斗场景提示词导演

Turn an approved dramatic beat into executable action: readable intent, changing advantage, causal contact, visible force, motivated camera coverage, and a reconstructable exit state. Do not substitute spectacle for story function.

## Route the work

1. Follow the repository `AGENTS.md`, the `$manju-story-studio` entrypoint, and the target series continuity before changing story or production files.
2. Confirm the combatants, objective, power imbalance, location GEO, entry/exit states, required contact/injury/damage results, props/weapons, audio policy, target backend, and generation duration.
3. Read only the reference needed for the task:
   - Choreography, rhythm, shot density, camera, common action vocabulary, impact, environmental damage, expressions, or motion blur: [choreography-and-cinematography.md](references/choreography-and-cinematography.md).
   - Convert an approved fight into a Shotlist or final model-neutral prompt plan: [prompt-compilation.md](references/prompt-compilation.md).
   - Diagnose a generated fight or revise after a failed Take: [repair-playbook.md](references/repair-playbook.md).
4. For a final production prompt, also use `$manju-story-studio`'s `references/shot-prompts-and-repair.md`, then its tool-format route. This Skill owns fight staging; the parent Skill owns repository contracts, asset wiring, model capability verification, audio layers, prompt-package validation, and Take logging.

## Invariants

- Separate the **story fight**, **generation envelope**, **edit shot**, and **action beat**. A numbered prompt section may contain several camera states; never infer real shot density from headings alone.
- Give every exchange an observable causal chain: `source of force -> launch/attack -> defense or miss -> exact contact -> deformation/material response -> displacement -> next usable state`.
- Build rhythm from contrast. Slow phases reveal decision, weight transfer, resistance, or energy accumulation; fast phases compress reaction time; contact may hard-stop before recoil. Do not distribute actions at one uniform tempo.
- Let characters travel through the set. Preserve continuity with named landmarks, cumulative damage, movement vectors, and motivated crossings rather than rigid left/right or meter-by-meter cages.
- Change framing or camera position only when it reveals new spatial, tactical, emotional, impact, or scale information. Carry action direction across cuts and motivate cuts with contact, occlusion, foreground passage, glare, debris, whip movement, or a deliberate axis transition.
- Keep the face, torso, feet, weapon/contact point, and decisive deformation readable at the moment they matter. Direct motion blur to fast limbs, trailing cloth/hair, background, and debris; restore clarity at anticipation, contact, and recovery.
- Treat misses as physical events. The force continues into a wall, floor, pillar, prop, or air wake; environmental damage records direction, power, and prior position.
- When extending a fight, add route, tactic, reversal, scale, or environmental consequences instead of stretching existing exchanges. Distribute repeated misses across distinct named surfaces when one landmark starts attracting every attack; each strike leaves one persistent, reconstructable result.
- Use expression inserts at decisions and reversals, not as decoration: target acquisition, recognition, failed attack, unexpected resistance, pain-to-anger change, dust reveal, or post-impact judgment.
- Do not end with an arbitrary white flash. Show charge/contact, compression or instability, release, colored/material-specific expansion, debris or shockwave, then the exit state required by the next shot. Full-frame dust is optional; use it only when a covered transition is deliberately needed, and then let it grow from the blast and damaged set before it becomes opaque.
- Follow the parent Skill's universal prompt opening: every non-H3 fight-generation prompt starts with `导演背景：你是资深漫剧导演兼动作导演` and executable priorities—causality, route, identity/counts, force result, and match-cut continuity—not generic prestige adjectives. H3 is the exception: preserve its official schema and compiler rules first. Put fatal global locks such as no visible subtitles/text near the front as well as in success criteria.
- Use the smallest sufficient reference set. Identity and location references do not automatically solve action. Do not add a storyboard or intermediate keyframe unless the user requests it or a diagnosed composition/GEO failure justifies it and the backend benefits from it.
- Preserve the requested sound policy. If BGM is forbidden, still specify synchronized impact SFX, movement sounds, ambience, purposeful withdrawal of sound, and the exit audio phase.

## Deliverable standard

A fight plan or prompt is ready only when another operator can answer: who is trying to achieve what, where each exchange occurs, how force travels, what the camera contributes, how fast and slow phases differ, which damage persists, where each combatant ends, and what the next shot inherits.

For production files, run the parent Skill's strict prompt lint and repository validation. Log generated evidence before promoting a backend-specific number, frame count, shot density, or reference strategy into a universal rule.
