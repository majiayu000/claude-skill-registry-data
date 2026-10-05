---
name: create-character
description: "Create an original reusable character through a canonical-first workflow. Generate and review one polished multi-panel character design sheet first; only after the user confirms expansion, create seven separate reference-bound assets for front, back, close-up, lighting, final look, and two scenes. Use for recurring characters in comics, storyboards, images, or video; also owns requests previously phrased as character reference sheets. Do not use for game-role-specific NPC design, small avatars, fashion lookbooks, or changing an existing person's appearance."
---
# Create Character

## Catalog

- Display name: Create Character
- Categories: Character
- Status: Ready
- Route label: Eight-run GPT Image 2 character production pack
- Tone: purple
- Short description: Build one canonical identity, then derive seven consistent character assets from it.
- Similar skills: casting, create-npc
## What this skill does

- Turns a brief or supplied identity reference into one reusable original character.
- Establishes the character with one canonical multi-panel design sheet before any derived image is submitted.
- Produces one canonical identity asset by default, then offers seven identity-bound production assets as an optional confirmed expansion.
- Replaces the former standalone `character-reference-sheet` generation workflow.

## How to use

Provide the role, species, apparent age, world, body and face anchors, hair, wardrobe construction, palette, signature features or props, personality, visual style, and any supplied references. Provide two scene briefs when their content matters; otherwise derive two distinct story-relevant environments from the character's world.

#### Example

```text
Create a complete character pack for Lin, a tired 24-year-old night courier with a blunt black bob, amber raincoat, red parcel bag, and guarded expression. Use a graphic Chinese webcomic style. Scene 1 is a rain-soaked parcel depot; scene 2 is a quiet rooftop at dawn.
```

## Character contract

1. Resolve an original character brief. Reject exact copying of a protected character; references may guide declared traits without reproducing a protected identity or design.
2. Lock the canonical invariants before generation: face and apparent age, hair, body proportions, wardrobe construction and materials, palette, distinctive marks, and signature props.
3. If the user supplies a supplied identity reference, use it to establish the first canonical sheet. Never inherit an unrelated reference background, action, layout, or pose.
4. Keep the same character and default wardrobe across all eight assets. Change only the task-owned property such as viewpoint, crop, lighting, portrait treatment, or scene.

## Two-phase workflow

Plan up to eight atomic image tasks. Persist one stable `operationKey` per submitted task and use `batchCount: 1` for every submission. Do not treat the seven derived tasks as authorized merely because they are listed in the workflow.

1. **Canonical character design sheet — the only default submission.** Read [references/canonical-sheet-prompt.md](references/canonical-sheet-prompt.md), compile its contract with the user's brief and supplied references, and create one polished multi-panel identity sheet. This output may become the canonical identity reference for tasks 2–8.
2. **Full-body front view.** Neutral full-body front view with the complete canonical wardrobe and proportions visible.
3. **Full-body rear view.** Genuine full-body back view showing the canonical hair, garment construction, accessories, and silhouette from behind.
4. **Head close-up.** Head-and-shoulders identity close-up with a readable canonical face, apparent age, hairline, and distinctive marks.
5. **Lighting study.** Show the same canonical character under a deliberate set of different lighting conditions without redesigning the face, hair, body, wardrobe, palette, or props. A controlled multi-panel lighting study is allowed inside this one asset.
6. **Final-look portrait.** Produce the character's definitive makeup, grooming, and wardrobe portrait. Preserve the canonical identity; interpret `定妆照` as a production final-look portrait, not permission to redesign the character.
7. **Character scene 1.** Place the canonical character into the first supplied or story-derived environment with one observable action and intentional composition.
8. **Character scene 2.** Place the same character into the second supplied or story-derived environment with a distinct story beat and composition.

Submit task 1 alone and poll it to terminal success. Visually inspect originality, identity coherence, anatomy, turnaround accuracy, expression consistency, wardrobe construction, material logic, palette, props, and panel usefulness. Return the canonical sheet, the inspection result, and a concise text invariant manifest to the user.

Then stop at a user confirmation gate. Ask whether tasks 2–8 are needed, naming the seven deliverables and their additional generation cost. Do not prepare submission receipts, reserve operation keys, or submit any derived task until the user explicitly confirms the expansion after seeing task 1.

If the user confirms, extract exactly one reusable public image URL from the accepted task-1 result and store it as `canonicalImageUrl`. Build all seven derived requests before submission and assert that every request contains the exact same non-empty reference binding:

```json
{
  "input": { "images": ["<canonicalImageUrl>"] },
  "params": {
    "images": ["<canonicalImageUrl>"],
    "textDescription": "<task-specific prompt>",
    "quality": "medium",
    "imageSize": "2K",
    "batchCount": 1
  }
}
```

Use both documented GPT Image reference locations so the native WeShop tool and official CLI adapter preserve the binding. If `canonicalImageUrl` is missing, non-public, or malformed, do not merely stop and do not regenerate task 1. Recover the accepted task-1 result:

1. Read the durable task-1 ledger entry by its existing `operationKey` and recover its `executionId`.
2. Poll or query that exact `executionId` again and require its recorded terminal status to be Success.
3. Extract the first valid public image URL from `data.executions[*].result[*].image`; if the harness stored a normalized task-1 result or callback, reconcile it against the same execution ID and use that URL.
4. Persist the recovered URL back onto the task-1 record as `canonicalImageUrl`, then rebuild all seven payloads.
5. Verify that both `input.images[0]` and `params.images[0]` equal the recovered URL for every request before submitting the expansion.

A missing Canvas item, missing local download, empty material search, or delayed publication is not a missing generation result; recover from the accepted WeShop execution first. If the exact task-1 execution is terminal Success but repeated read-only reconciliation still returns no valid image URL, report a blocked reference-recovery state and keep tasks 2–8 unsubmitted. Never create another task-1 run merely to obtain the URL.

If either reference field is absent from a prepared derived request, repair that payload from the persisted `canonicalImageUrl` and rerun the complete seven-request preflight. Once all seven payloads pass, persist all seven distinct operation keys before the first create call, then submit tasks 2–8 as one parallel wave of seven independent create-run calls. Do not await an execution receipt, status, or result from one slot before submitting another slot. Collect all seven create receipts after the wave has been launched, then poll the accepted execution IDs independently. Use the native harness's concurrent call facility or launch seven independent official `weshop` CLI processes with equivalent all-settled behavior.

This parallel wave is mandatory for an approved expansion. It is not `batchCount: 7`: each task keeps its own Prompt, `operationKey`, `executionId`, and `batchCount: 1`. A failure or unknown outcome in one slot does not cancel, duplicate, or serialize the other already-planned slots. Only when scene 2 explicitly depends on scene 1's newly generated visible state may that one scene task be held for a second wave; record that dependency instead of silently serializing the whole expansion.

## Route and execution

Use `gpt-image` v1.0 / GPT Image 2 for all eight tasks with one complete `textDescription`, `quality: "medium"`, `imageSize: "2K"`, the task-appropriate supported `aspectRatio`, and `batchCount: 1`.

- Default the canonical sheet and lighting study to a layout-capable ratio selected for readable panels; default the front, back, close-up, final-look portrait, and scene images to `3:4` unless the user requests another supported ratio.
- Do not route any task to Midjourney merely because the user requests manga, anime, comic, concept-art, or another artistic style. Midjourney's four-image response violates the one-result-per-task contract.
- Require a non-empty `executionId` for every accepted submission and poll that exact run to terminal state. The task-1 receipt never authorizes tasks 2–8.
- For an approved expansion, use submission mode `parallel-wave`, concurrency `7`, and `awaitBetweenSubmissions: false`; prepare every payload and durable key before launching the wave.
- An unknown create outcome freezes only that task. Reconcile its existing `operationKey`; never submit a replacement blindly.
- A known terminal or visual failure may replace only the failed slot with a new linked operation key and a materially revised request. Never regenerate accepted slots or increase the eight-task plan.

## Acceptance

Apply a task-1 gate before asking for expansion. If expansion is confirmed, apply one final pack gate after task 8 while preserving the task-1 canonical identity between runs:

- Without expansion approval, exactly one canonical sheet exists and no derived tasks were submitted. With approval, exactly eight separate image assets exist, one per named task; no task returns an unrequested four-image batch.
- Tasks 2–8 visibly preserve the canonical face, age, hair, proportions, wardrobe construction, palette, marks, and signature props.
- Front and rear views are genuine opposing views; the close-up clearly establishes identity.
- Lighting changes illumination rather than character design.
- The final-look portrait reads as the definitive same character.
- Both scene images contain the intended same character, required props, distinct environments or story beats, and no extra duplicate character.

Record each task name, reference bindings, parameters, exact Prompt, operation key, execution ID, terminal state, and any replacement reason.

## User-facing output

- Media type: Image pack
- Default quantity: 1 canonical sheet; optionally expand to 8 total separate images only after post-QA user confirmation; `batchCount: 1` for each submitted task
- Content: Canonical design sheet, full-body front, full-body back, head close-up, lighting study, final-look portrait, scene 1, and scene 2
- Default layout: One canonical multi-panel sheet plus seven separate task-specific images
- Model policy: GPT Image 2 Medium/2K for all eight tasks
- Downstream use: Canonical identity and production references for comics, storyboards, images, and video
