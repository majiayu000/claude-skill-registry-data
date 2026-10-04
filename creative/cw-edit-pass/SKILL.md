---
name: cw-edit-pass
version: 1.0.0
description: Run a developmental then line-edit pass on a fiction draft, big issues before small.
author: matrixx0070
tags: [creative-writing, fiction, editing, revision, line-edit]
capabilities: []
---

## When to use

Use this when you have a complete draft (scene, chapter, or story) and need to revise it in the right order — structure and character before sentences. Best after the draft is done, not while writing it.

**Not for:** generating a new outline (use cw-story-outline), building a character from scratch (use cw-character), drafting fresh scenes (use cw-scene), or inventing world rules (use cw-worldbuilding).

## Method

1. Read once for impression only — no fixing. Note where attention drifted and where it gripped. Decision point: fix drift zones structurally before touching any prose.
2. Developmental pass first (never invert the order): check premise clarity, scene goals, causal chain (therefore/but), stakes escalation, and whether the ending pays off the setup.
3. Character pass: does each want/need/flaw stay consistent, and does the arc actually turn? Flag actions that serve plot over character.
4. Scene pass: every scene needs a goal, conflict, and turn; cut or merge scenes that only transition.
5. Only now, line-edit. Cut filter words, hunt weak verbs + adverbs (replace with strong verbs), vary sentence rhythm, and delete throat-clearing openers. Decision point: if a fix at this level would be erased by a structural change, stop and go back up a level.
6. Copyedit pass: grammar, tense consistency, dialogue punctuation, name/detail continuity.
7. Kill-your-darlings sweep: cut the cleverest line if it doesn't serve the scene. Track cuts in a hold file rather than deleting outright.

## Example

Draft: a 3,000-word story. Impression: drifts in the middle. Developmental: middle drifts because scene 3 has no goal — merge it into scene 4. Character: the protagonist forgives too easily; add a cost. Scene: scene 5 ends late — cut the goodbye. Line: "She quickly ran" → "She bolted"; delete "she noticed the door was open" → "The door stood open." Copyedit: fix a tense slip. Darling: cut a beloved metaphor that stalls the climax (moved to hold file).

## Pitfalls

- Line-editing prose that a later structural cut will delete — wasted effort, top-down avoids it.
- Polishing sentences in a scene that should be cut entirely.
- Overwriting the author's voice into generic "correct" prose.
- Deleting darlings permanently with no hold file, losing lines you may reuse.

## Output format

```
IMPRESSION (drift/grip zones): <...>

DEVELOPMENTAL: premise <ok/fix> | causality <...> | stakes <...> | ending payoff <...>
CHARACTER: consistency <...> | arc turns? <...>
SCENE: scenes to cut/merge <...>
LINE: verbs <...> | filters cut <...> | rhythm <...>
COPYEDIT: <continuity/grammar flags>
DARLINGS (to hold file): <...>

PRIORITIZED FIX LIST (top-down):
1. <structural>  2. <character>  3. <scene>  4. <line>
```
