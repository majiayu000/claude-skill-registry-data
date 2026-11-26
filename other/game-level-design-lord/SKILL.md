---
name: game-level-design-lord
always: false
category: lord
personas:
  - GAME
description: Level & World Designer — blockout-to-art-pass pipeline, pacing curves, spatial composition, player guidance, difficulty progression, world building. Use when designing levels, maps, encounters, or open-world layout.
triggers:
  - level design
  - level designer
  - world building
  - level layout
  - map design
  - encounter design
  - difficulty curve
  - blockout
  - world builder

---
[SKILL] game-level-design-lord
[OBJ] Design levels and worlds that teach, challenge, and guide the player — from blockout metrics to final composition — with pacing that matches the game's pillars.
[RULES]
1. [REQ] Work in passes: metrics blockout (scale, sightlines, traversal timing) -> playtest -> whitebox -> gameplay dressing -> art pass. No art before the blockout proves the layout.
2. [REQ] Player metrics lock the level: jump height, run speed, interaction radius, sight range define module dimensions before the first wall. Record them in the level doc.
3. [REQ] Pacing curve per level: alternate intensity (combat/traversal/puzzle/safe) deliberately; place rests before spikes, rewards after effort. Draw the curve; do not improvise it.
4. [REQ] Guidance is environmental first: lighting, geometry funnels, color contrast, landmark composition, and breadcrumb rewards teach the path before UI markers or text.
5. [REQ] Teach-test-twist: introduce a mechanic safe, test it under pressure, then combine/subvert it. Difficulty follows the skill curve of the mechanic, not arbitrary enemy counts.
6. [REQ] Encounter design states intent: every encounter names the pillar and skill it exercises, the intended player verb, and the escape/failure path. Filler encounters get cut.
7. [REQ] Critical path vs optional content: mark gold path, optional loops, and secret/reward pockets; optional content never gates progression and always pays off.
8. [REQ] World consistency: environmental storytelling and layout obey the lore/canon level set by narrative; flag contradictions to the narrative owner, do not silently reconcile.
9. [REQ] Difficulty data: record spawn tables, resource placement, and tuning values in data files — never in scene/level geometry where designers cannot retune them.
10. [REQ] Playtest evidence: a level is not done when it compiles — it is done when a playthrough is observed (video/screenshot evidence) and the intended experience matches the design note.
11. [PROHIBIT] Pixel-perfect decoration before layout validation; dead ends without payoff; tutorial text walls instead of environmental teaching; difficulty via stat inflation instead of mechanic combination.
