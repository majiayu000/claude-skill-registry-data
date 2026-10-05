---
name: casting
description: "Create a Chinese screen-role casting package from a six-field role card: one pure-white, face-first casting portrait for approval, then only selected identity-bound full-body, expression-grid, or turnaround assets. Use for short-drama, film, and casting-character roles; unlike `create-character` (relationship 0.84), choose this for actor-style face selection and a confirmation gate, and choose `create-character` for a canonical multi-panel production pack and scenes. Do not use for real-person edits, game-role NPC concepts, or generic character sheets."
---

# Casting

## Catalog

- Display name: Casting
- Categories: Character
- Status: Ready
- Featured: yes
- Route label: GPT Image 2 face-first casting package
- Tone: violet
- Short description: Select and approve a screen-ready Chinese character face before deriving optional studio assets.

- Similar skills: create-character, create-npc
## What this skill does

- Converts a role card or script description into a Chinese screen character.
- Generates exactly one vertical, pure-white, front-facing casting portrait first.
- Stops for explicit face approval. Only then creates user-selected full-body, 3×3 expression-grid, and/or turnaround assets.
- Uses separately controlled high-end CG rendering for 漫剧, 3D漫剧, 3D角色, 三维, CG, or 三渲二 requests.

## How to use

Request the six role-card fields when available: person type, build, facial features, skin/hair/makeup, temperament, and intended character type. A script or freeform description is acceptable. Complete only reasonable omissions and state them in one sentence before submission.

Do not reproduce a protected character or edit a real person. References must be supplied. Bind only an accepted public image URL, in supplied order—never invent a URL or asset token. Clothing must not override the requested face, skin, expression, or bone-structure intent.

#### Example

```text
为民国悬疑短剧选一个26岁女记者：身形清瘦，偏窄长脸、平直微挑眉、长眼微上扬，暖白细腻肤色和低盘发，表面温柔但在隐藏锋芒。先出纯白底定脸；我确认后再选全身或表情。
```

## User-facing output

- Media type: Approval-gated image casting package
- Default quantity: One face-setting portrait
- Optional quantity: One selected full-body, expression grid, and/or turnaround board
- Content: Chinese screen-role character on a pure-white background
- Default layout: Vertical 3:4 portrait; selected 3:4 derivatives; 16:9 turnaround board
- Model policy: GPT Image 2 Medium/2K after current-schema verification
- Downstream use: Short-drama, film, comic, and story production casting references

## Route and execution

Use `gpt-image` / GPT Image 2 at Medium/2K. Before a real run, inspect the current official CLI or native Agent schema: the local catalog marks identity consistency and multi-reference support unknown. If public image references are unsupported, stop before derivatives and explain that safe identity continuity cannot be claimed.

## Portrait and approval workflow

1. Default to polished photographic realism. Trigger CG mode immediately only for the listed CG terms; never mix photographic and CG surface wording.
2. For multiple roles, choose one or two differentiating facial/temperament anchors per role. For a single role, follow the brief instead of converging on a generic influencer face.
3. Read [portrait prompt blocks](references/portrait-prompt-blocks.md). Compile one Chinese-led prompt in this order: CHARACTER, SKIN, OUTFIT, then the three locked blocks unchanged. Use CG replacements only in CG mode.
4. Submit one GPT Image 2 task: `quality: "medium"`, `imageSize: "2K"`, vertical `3:4`, `batchCount: 1`, and a persisted operation key. Poll its accepted execution to terminal state; do not replace an unknown create outcome.
5. Inspect before presentation: seamless `#ffffff`; front-facing head-and-neck crop; balanced facial structure; refined natural skin or intended CG surface; clear ears/hair; logo-free clothing; exactly one character.
6. Ask whether the face is approved. If it is not, alter only the failed constraints and submit one linked revision. Never create a derivative before explicit approval.

## Approved expansion

Offer **full-body portrait**, **3×3 expression grid**, and **turnaround board** only after approval. Explain that turnaround needs full body first; do not prepare operation keys or submit unselected assets.

- **Full body:** bind the approved portrait URL in both documented reference fields; use vertical `3:4`, head-to-toe framing, and the applicable written head-to-body and negative constraints from the reference. Women default to seven heads; ordinary men to eight; dominant male leads only may use 8.5–9; antagonists remain realistic; children use 3–4.
- **Expression grid:** bind the approved portrait; use one vertical `3:4` 3×3 grid. Default sequence: neutral, restrained smile, anger, sadness, joy, tearful grief, surprise, intense anger, confusion. Keep orientation, identity, hair, and skin consistent.
- **Turnaround:** bind approved portrait and full-body URLs in that order. Use a 16:9 board with front/profile/back full bodies plus front face close-up. On a board that combines body views with a face close-up, default to neck-to-feet front/profile/back body studies with the heads omitted cleanly at the neck, and make the approved face close-up large and unobstructed as the sole facial-detail reference. Small repeated heads can compete with that reference and introduce inconsistent facial details. Keep clothing, body proportions, and feet complete; anatomical head-to-body ratios still govern the underlying figure, not the visible cropped height. This presentation rule applies only to combined boards: standalone full-body portraits retain head-to-toe framing, and an explicit request for complete heads takes precedence. After one material revised attempt, report any layout limitation and offer separate views rather than fabricating consistency.

For each derivative use a new operation key and `batchCount: 1`; reference URLs must match in `input.images` and `params.images`. Poll each accepted execution. A known terminal or visual failure may receive one linked, materially revised retry; reconcile unknown results by the existing key.

## Visual invariants

- Every asset uses seamless pure white `#ffffff`: no gray, off-white, colored, textured, gradient background.
- Photographic skin is clean, refined, realistic, and naturally textured—neither rough/enlarged pores nor plastic glass skin—under soft volumetric face light.
- Describe the fictional subject as `Chinese`, and use state-based temperament rather than stereotypes.
- Keep apparel logo-free and restrained. Tops remain loose over the waistband; default male trousers are full-length straight or gently wide-leg, unless the card requires otherwise.
- Do not alter the locked composition, rendering, and sharpness blocks or add the known harmful focus phrases listed in the reference.

## Acceptance

- Report role, reference bindings, rendering mode, operation key, execution ID, and terminal state; report only successful assets as delivered.
- Pass only when requested original role identity, white background, framing/proportion, no logos, coherent hair/skin/wardrobe, and the approved face remain observable. On combined boards, verify that the face close-up is large and clear and that body studies do not introduce competing small faces; intentional neck crops are valid only for that layout. State model layout/reference limitations plainly.
