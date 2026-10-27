---
name: label-function-analysis
description: >-
  "What is this label DOING?" - Unbundle a loaded label (extremist, denier,
  conspiracy theorist, apologist, shill) into observation, intent, mechanism,
  and actor; autopsy the debate axis the label enforces; run cui-bono on the
  label itself; test whether the replacement axis is falsifiable. Use when
  (1) a label is carrying an argument that evidence should carry, (2) a
  source or thesis is dismissed by category rather than content, (3) both
  camps ping-pong on an axis that never resolves, (4) you catch the analysis
  reaching for a respectability label instead of a reason. Does NOT trigger
  for: labels used descriptively with the evidence attached.
---

# Label-Function Analysis

**Seed question:** *What is this label DOING?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Principle

A loaded label is a compressed verdict whose evidence nobody has to produce.
Its two working parts: BUNDLING (heterogeneous claims fused so the weakest
member discredits the strongest) and AXIS-ENFORCEMENT (the label keeps a
debate on an axis that may be dead — both camps invested in an opposition
that no longer cuts reality where it folds). Analyzing the label's FUNCTION
is not defending what it points at (Principle P6 (the-frame-leaks-upstream):
the respectability tic is the frame talking).

**The anti-pattern this counters:**
```
❌ "That's conspiracist" doing the work a citation should do
❌ Rebutting a label by claiming its mirror ("no, THEY are the deniers")
❌ Debates that feel obligatory and sterile at once — the dead-axis signature
```

**The pattern this enforces:**
```
✅ Unbundle: observation / intent / mechanism / actor — which is evidenced?
✅ Autopsy the axis: what does this opposition make unaskable?
✅ Cui bono of the LABEL: who is spared work while it circulates?
✅ Falsifiable replacement axis — or the analysis is just re-labeling
```

## The Analysis

1. **Unbundle the label.** For the label as used HERE: which observation,
   which intent-claim, which mechanism-claim, which actor-claim is it
   asserting? Which of those has evidence attached in this use?
2. **Axis autopsy.** What debate-axis does the label enforce? Test for death:
   would any admissible evidence move either camp along it? What questions
   does the axis make unaskable?
3. **Cui bono of the label.** Who is spared evidential work while the label
   circulates? Which positions does it cheaply bundle together? (Symmetric:
   labels favored by power AND labels flung at it.)
4. **Replacement axis + falsifiability test.** Name the axis that would cut
   where reality folds — and state what evidence would move a claim along
   it. A replacement axis nothing could move is a new label in axis costume.

## Pattern-Library Source (cross-plugin)

This skill operationalizes the vasana-system pattern
`label-bundling-dead-axis` — reference it as `vasana-system:pattern-library`,
pattern `label-bundling-dead-axis`, resolved from the user's canonical
pattern-library location (default `~/ClaudeShared/pattern-library/patterns/`)
with the vasana-system plugin's bundled copy as fallback. Do NOT hard-path
into another plugin's install directory — install layouts differ and the
canonical location is the supported seam. If neither resolves (vasana-system
not installed), proceed with this skill's own protocol above and note the
pattern file was unavailable — the skill is self-sufficient; the pattern file
adds worked cross-domain material, not required steps.

## Mandatory Output Slots

| Slot | Contents | Invalid when |
|------|----------|--------------|
| **Unbundled label** | The four components as asserted in THIS use, each marked evidenced / unevidenced | Generic dictionary analysis of the label; components without the evidenced-mark |
| **Axis autopsy** | The enforced axis; the death test result; what it makes unaskable | Axis named but not tested |
| **Label cui-bono** | Who is spared work; what gets bundled — both directions | One camp's labels only |
| **Replacement axis** | Named, with what evidence would move a claim along it | Unfalsifiable; or missing |

## Cross-References

- **kernel-shell** — the label often IS the shell's delivery mechanism;
  unbundle the label, then atomize the thesis
- **cui-bono** — the label cui-bono step is cui-bono's method on a linguistic
  object (see also Language/Power Analysis there)
- **frame-rotation / salience rotation** — when the axis autopsy stalls,
  rotate what the coverage headlined vs ignored
- **[[vasana-system:pattern-library]]** — source pattern
  `label-bundling-dead-axis` (sibling plugin; optional, see above)

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
