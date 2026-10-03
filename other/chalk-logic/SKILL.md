---
name: chalk-logic
description: Create Chalk Logic concept-led chalkboard illustrations from briefs. Use for sparse wordless chalkboard explanations, non-diagram editorial chalk compositions, or prompt-only Chalk Logic recipes.
---

# Chalk Logic

Turn one idea into one quiet white-chalk proposition on an even green board. Render by default when image generation and inspection are available; otherwise return the compiled prompt and recipe.

## Visual contract

Treat every bullet as both a generation rule and a QA gate:

- **One proposition:** communicate one process, relationship, structure, cycle, accumulation, attenuation, or observational premise. Give it one unmistakable reading path.
- **Quiet field:** keep roughly 65%-75% of the board empty. Raise this to 76%-86% for a single sparse sequence or observational vignette. Preserve generous outer margins and a compact concept-bearing motif.
- **Even board:** fill the canvas edge to edge with a flat, dry, desaturated schoolroom-green board. Use microscopic matte grain that stays quiet at thumbnail size. The frame contains only the board and the concept-bearing chalk motif.
- **Mineral hand:** draw only with warm-white mineral chalk. Use three restrained contrast levels: faint construction or context, readable structure, and very few brighter contacts. Show pressure variation, slightly broken stroke edges, occasional double strokes, and tiny deposits.
- **Coherent strokes:** draw semantic paths as continuous gestures, with material breakup limited to stroke edges and endpoints. Use intersections only when they carry a clear causal or structural meaning.
- **Exact but handmade:** make the composition deliberate and the marks human. Build recognizable forms from observed silhouettes and functional anatomy; build abstract forms from specific spatial behavior.
- **Wordless default:** render zero text, letters, numerals, equations, pseudo-writing, signatures, logos, or watermarks. If the user explicitly requires text, use only their exact wording as one short phrase or up to three micro-labels with six words total.
- **Original topology:** satisfy the anchor delta declared in Step 3 and build the composition from the concept's own mechanism.
- **Two-scale clarity:** make the proposition legible at thumbnail size and reward full-size inspection with quiet material detail.
- **Authored restraint:** keep every mark in the proposition. Use the fewest structural forms that preserve the intended reading.

## Formats

- Use `16:9` for a default landscape illustration.
- Use `1:1` for an open cycle or compact accumulation.
- Use `4:5` for a branching study, exploded object, or poster.
- Use approximately `2.2:1` only when a long transformation benefits from an ultrawide field.
- Honor exact dimensions supplied by the user and compose natively for them.

## Composition families

Choose exactly one primary family.

| Family | Best for | Positive grammar |
| --- | --- | --- |
| Directional progression | transformation, attenuation, accumulation | one left-to-right or diagonal sequence; encode change through spacing, density, scale, repetition, or pressure |
| Open cycle | recurrence, phases, sleep, renewal | three to five unequal stages around a large central void, joined by one incomplete loop or return gesture |
| Source to branches | mechanisms, dispersal, alternatives | one compact source with three to five asymmetrical non-crossing trajectories, differentiated by recognizable form |
| Axial observation | construction, anatomy, assembly | one recognizable object separated into a small exact part count along one shared axis with sparse alignment traces |
| Environmental flow | absorption, transfer, growth | one restrained boundary or field and one continuous causal route shown through density and pressure |
| Quiet vignette | reflection, attention, absence, pause | one compact off-center object constellation in a vast field, carried by placement and emptiness without diagram scaffolding |

## Steps

### 1. Lock the brief

Identify the concept, intended explanation, emotional temperature, output format, text policy, and execution mode. Express output format as exact pixel dimensions when supplied, otherwise as a ratio. Set execution mode to `rendered` only when image generation and image inspection are both available.

If the user prohibits images in the current conversation, establish one fresh isolated worker before selecting `rendered`. Route anchor viewing, generation, candidate viewing, repairs, and image QA through that worker. Require it to return text findings and local file paths only. Use `prompt-only` when requested or when any required capability or isolated worker is unavailable.

Completion criterion: all six brief values and the execution context are explicit; an image-free rendered run has an established isolated worker; and any unavailable capability is recorded for delivery.

### 2. Distill the reading path

Choose one composition family and state one internal visual sentence: what the viewer encounters first, what changes or relates, and where attention ends. Choose one **semantic carrier** such as spacing, density, scale, repetition, pressure, or object arrangement to carry the meaning.

Completion criterion: the sentence contains one coherent proposition, one ordered reading path, one primary family, and one named semantic carrier without unrelated subplots.

### 3. Anchor the quality

Read [references/example-index.md](references/example-index.md) completely. Select one or two entries according to its anchor-selection rules. Record one shared anchor delta for the new composition:

- for each selected anchor, three identity traits with observable target evidence to preserve;
- one target topology for the new composition;
- exactly two independent target axes chosen from subject, format, viewpoint, direction, count, focal placement, or semantic carrier;
- for every selected anchor, its source value mapped to the same target topology and two target-axis values; each target must differ observably from that anchor's source value.

For rendered runs, visually inspect only the selected local examples. For prompt-only runs, the text index is sufficient. Treat examples as quality evidence, not image-generation inputs. When the user asks to keep images out of the conversation, perform inspection in the fresh isolated context established in Step 1 and return file links only.

Completion criterion: one or two anchors are selected; each records three observable preserved traits and source-to-target mappings for the shared topology plus two independent target axes; the three target values are identical across all mappings and observably different from every mapped source value; and rendered runs have visually inspected every selected anchor.

### 4. Declare the recipe

Choose exactly one value for each axis:

- format;
- family;
- proposition;
- reading path;
- semantic carrier;
- topology;
- motif placement;
- recognition cues or abstract mark vocabulary;
- counts or states: exact values when meaningful, otherwise `not fixed`;
- anchor-change targets: the two target values from Step 3 without anchor names or provenance;
- quiet-space target;
- chalk contrast hierarchy;
- mood;
- text: `wordless`, or the exact supplied wording plus its scale and placement.

Completion criterion: all fourteen axes have one choice and support the same proposition.

### 5. Compile the image prompt

Write four compact paragraphs containing only information that should become pixels:

1. State canvas, ratio, even green board, and quiet-space target.
2. State the proposition, family, semantic carrier, topology, exact counts where meaningful, reading path, recognition cues, placement, and both anchor-change target values.
3. State warm-white chalk behavior, three-level contrast, coherent line behavior, and mood.
4. State the text policy and only the subject-specific hard exclusions needed to prevent a likely misread.

Keep internal titles, recipes, filenames, provenance, anchor analysis, and QA notes outside the image prompt.

Completion criterion: every recipe axis maps into the prompt as a target pixel property; any fixed count or state is explicit; any requested text includes exact wording, scale, and placement; the prompt describes one visual proposition; and the board, chalk, line, mood, and text gates are explicit.

For `prompt-only`, skip Steps 6 and 7 and continue to Step 8 with status `PROMPT_ONLY`.

### 6. Generate one candidate

Use the execution context selected in Step 1 and the built-in image-generation capability. For image-free conversations, the isolated worker performs every image-bearing operation. Generate at exact requested pixel dimensions when the capability supports them. Otherwise generate at the same native ratio and resample only when the ratio matches exactly; if neither path can satisfy the requested dimensions, switch to `prompt-only` and record the capability note. If the user supplied an inspiration image, use it only for the requested directional cue and preserve an original topology.

Completion criterion: for an exact-dimension request, file metadata matches both requested pixel dimensions exactly; for a ratio request, file metadata matches the requested ratio.

### 7. Inspect and repair

Inspect the candidate at full size and thumbnail size in the execution context selected in Step 1. Check every visual-contract bullet, all fourteen recipe axes, and each recorded anchor delta. Record `N/A` for `Exact counts` only when the recipe says `not fixed`; record `N/A` for any other gate that does not apply.

If several gates fail, select the first failure in this precedence:

1. requested format;
2. text policy;
3. proposition;
4. family;
5. reading path;
6. causal order;
7. semantic carrier;
8. exact counts;
9. recognition cues;
10. topology and anchor-change targets;
11. preserved anchor traits;
12. quiet-space target;
13. motif placement;
14. thumbnail clarity;
15. full-size material detail;
16. coherent strokes;
17. even board;
18. mineral hand;
19. chalk contrast hierarchy;
20. mood;
21. authored restraint.

Pass the selected gate to [references/repair-playbook.md](references/repair-playbook.md) and apply its correction for repair pass 1. Reinspect all twenty-one gates. For pass 2, select the first remaining failure by the same precedence and apply its mapped correction. Replace the topology only when `Topology and anchor-change targets` is the selected gate. Reinspect all twenty-one gates and stop after pass 2.

When a second fresh isolated subagent is available, use it for final visual QA. Pass only the candidate and gates, request text-only findings, and keep prior judgments out of its context. In an image-free run, the isolated worker owns this dispatch and returns only the verdict.

Completion criterion: every gate was inspected exhaustively. Set `DONE` when all pass; after the repair limit, set `DONE_WITH_CONCERNS` and enumerate every remaining failed gate.

### 8. Deliver

For rendered runs, present the accepted image or an ordinary file link according to the user's display preference, followed by the exact prompt sequence, complete recipe, and status. The prompt sequence contains the initial generation prompt plus every repair instruction in order. Save project-bound images into the user's workspace before delivery. Never present bundled reference images as generated work. For prompt-only runs, deliver the compiled prompt, complete recipe, and `PROMPT_ONLY` status without an image. If prompt-only is a capability fallback rather than the user's request, add one concise capability note.

Completion criterion: a rendered run includes the inspected candidate, exact prompt sequence, all fourteen recipe axes, and `DONE` or `DONE_WITH_CONCERNS`; `DONE_WITH_CONCERNS` also includes every remaining failed gate. A prompt-only run includes the compiled prompt, all fourteen recipe axes, `PROMPT_ONLY`, and any required capability note.

## Output shape

For `PROMPT_ONLY`, omit the Image line. Omit every unused repair line and conditional field.

````markdown
**Image**

[Chalk Logic illustration](absolute-image-path)

**Exact prompt sequence**

```text
Initial: [exact generation prompt]

Repair 1: [exact instruction, when used]

Repair 2: [exact instruction, when used]
```

**Recipe**

- Format: [ratio or dimensions]
- Family: [family]
- Proposition: [visual sentence]
- Reading path: [choice]
- Semantic carrier: [spacing/density/scale/repetition/pressure/object arrangement]
- Topology: [spatial structure]
- Motif placement: [choice]
- Recognition cues or marks: [choice]
- Counts or states: [exact values/not fixed]
- Anchor-change targets: [target value 1; target value 2]
- Quiet space: [percentage]
- Chalk hierarchy: [three levels]
- Mood: [emotional temperature]
- Text: [wordless or exact wording, scale, and placement]
- Status: [DONE/DONE_WITH_CONCERNS/PROMPT_ONLY]

[Concerns: required only for DONE_WITH_CONCERNS]

[Capability note: only when PROMPT_ONLY is a fallback]
````
