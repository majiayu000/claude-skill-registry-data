---
name: uefn-epic-skills
description: Says when to read Epic's own editor skills (PCG, Sequencer, MetaSound, materials, lighting, GenMedia, Dataflow) that the UEFN MCP serves, and which skill wins when both Epic's and the kit's apply. Use when a job touches procedural placement, cinematics, audio graphs, materials, lighting or generated media through the MCP.
kind: discipline
last_reviewed: 2026-11-03
sources: [original]
---

# Epic's editor skills and the kit's skills

Since UEFN 43.00 the MCP serves skills written by Epic: a list with `ToolsetRegistry_AgentSkillToolset_ListSkills` and the full text with `GetSkills` (by name). They teach how the Unreal editor tools behave. They say nothing about devices, Verse, mechanics or publishing: that is the kit's part.

## When to use
- The job needs PCG graphs, Sequencer or cinematics, MetaSound, materials, outdoor lighting, Dataflow, scene captures or generated media (GenMedia) through the MCP.
- You are about to call tools of one of those families and do not know their rules.

**When not to use:** placing or configuring devices, Verse code, a mechanic, a genre, a delivery check. The kit's own skills decide those (`uefn-level-devices`, `uefn-verse-build`, `mechanics`, `uefn-disciplines`).

## Who wins
| The job | First read | Then |
|---|---|---|
| Place or configure a device, wire events, write Verse | the kit's skill | Epic's skills only for the editor tool that carries it |
| What to build, how it should play | the kit (genre, concept, recipe) | - |
| PCG, scatter, biomes, shape grammar | Epic's PCG skills | the kit's `level-design-uefn` for layout and pacing |
| Sequencer, cameras, keyframes | Epic's Sequencer skills | `camera-audio-uefn` for what the camera should do |
| MetaSound, materials, lighting | Epic's skill of that family | `uefn-materials`, `uefn-vfx-niagara` for UEFN limits |
| Screenshots as evidence | Epic's scene capture skill | `qa-regression` for what to look for |
| Generated images, meshes, audio, video | Epic's GenMedia skills | the owner confirms before anything is imported or kept |

A rule written for UEFN (a "restricted editor" line, a UEFN-only path) outranks a general Unreal habit. When Epic's text and a kit rule disagree on placing, saving or undo, stop and tell the owner; do not pick silently.

## Workflow
1. Once per session, if the job is in the table: call `ListSkills` (names and first lines only). Do not read all of them.
2. Call `GetSkills` for the one or two skills of the family you need. Read them in your own context; do not paste them into notes or the kit (they are Epic's text).
3. Do the work with the kit's guards on: lab rules, the editor lock, no unfiltered `find_assets`.
4. If a skill names a tool that is not in the map (`python Claude/hooks/mcp_map.py --find WORDS`), tell the owner and use what the map has.

## Rules (symptom, cause, remedy)
- Floating props: a physical prop placed at a raw height. Snap props, characters and rocks to the ground; leave lights, triggers, volumes and cameras where requested (Epic's placing skill says the same).
- Sequencer refused: spawnable bindings, Director Blueprints or FBX export do not exist in UEFN. Use possessable bindings and keep the sequence simple.
- PCG graph not found: the instant graphs live in a different path in UEFN and the asset search may not see plugin content. Try the last known path, then search by name; "does not exist" is not proof.
- Bulk reading: all 30 skills read at once cost about 213 000 characters. Read only the family you need.
- Generated media kept without asking: GenMedia results have provenance and naming rules. Ask the owner before importing.

Details and the current list: `references/epic-skills-list.md`.
