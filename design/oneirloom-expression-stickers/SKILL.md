---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-expression-stickers
description: Design chat reaction stickers and emote packs with recognizable character identity, distinct communicative intent, gestures, and optional exact captions. Use for individual stickers or coordinated packs, not character turnarounds, UI icons, or brand logos.
triggers:
  - oneirloom-expression-stickers
  - oneirloom
  - expression
  - stickers

---

# Design expression stickers

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

Create static chat reactions unless the user requests animation. A sticker pack contains individually usable reactions. A contact sheet is a preview, and a character sheet establishes identity. Neither substitutes for individual sticker files.

Follow the shared [graphic-design process](../oneirloom-style-design/SKILL.md). The decisions below specialize its Understand, Observe, and Design stages for stickers. Keep the current user's identity, medium, and deliverable choices ahead of recipe defaults.

## Understand the character and conversation

Identify the preceding message, sender-recipient relationship, sender's purpose and tone, and expected next reply or action. A mood such as happiness does not distinguish receipt from agreement, gratitude from an offer, or friendly teasing from hostility. Try the proposed reaction after a plausible chat turn. Keep an inferred scenario provisional instead of inventing user facts. Resolve available facts first and ask only when missing information blocks a material choice.

Preserve exact supplied copy and the requested output. Distinguish prompts, a single sticker, a concept preview, individual pack files, and animation. Use requested counts, dimensions, and medium. When platform requirements affect delivery, verify the current official specification for the exact asset type and distribution route. Keep hard requirements separate from recommendations. An unknown platform leaves its export profile unresolved; it need not block design. Do not import another platform's counts, dimensions, or encoding.

Inspect the original identity before designing emotions. Record the silhouette, anatomy, part counts and connections, colors, materials, and meaningful accessories. Identify what each part is and does. Separate observed features, user-defined meaning, design inference, and unknown structure. Resolve fixed identity facts and variable expression, including permitted tilt, compression, reach, orientation, and prop movement. Identity continuity does not require an unchanged silhouette. Choose a view supported by known anatomy rather than inventing a hidden side.

When a requested sticker treatment depends on physical craft assembly or a digital shape transformation, read [craft construction](../oneirloom-craft-construction/SKILL.md) or [digital form](../oneirloom-digital-form/SKILL.md) for that decision. This method remains responsible for reaction intent, identity, and individual sticker delivery.

A faceless creature can communicate through posture, appendages, a star, or the tension and position of a net. Use the features that actually exist. Do not add a human face merely because a template mentions expressions. For example, when a supplied dream creature has four tentacles and a dream-catching net, understand how those parts connect and what the net does before changing its gesture. This example is not a default character design.

Reuse an existing usable master reference or suitable accepted view. Use the [character-sheet method](../oneirloom-character-sheet/SKILL.md) only if the task needs unresolved identity construction. An existing usable identity reference does not require a new sheet.

## Observe the references

Assign each reference an identity, pose, style, or layout role, or identify it as an output to critique. One image can have multiple deliberate roles. Style resemblance alone does not establish identity or anatomy. Inspect actual images before consulting a stored recipe. With no image, design from the brief and label the direction as an unobserved proposal. A recipe without an example is not visual evidence.

Check what reads first at the intended chat size and picker-thumbnail size: the silhouette, expression, gesture, prop, or words. Describe form simplification, action direction, crop, visible connections, overlap order, type placement, material, and edge treatment. Explain their relationship instead of substituting a label such as "cute 3D." Distinguish a depicted checkerboard from real transparency. Look for shapes and lettering that disappear against light or dark backgrounds. If only a small source is available, keep exact edge, fine texture, and alpha behavior unknown.

## Design distinct reactions

Make a compact reaction matrix in the existing working notes. Carry the preceding turn, relationship, purpose, tone, and expected reply into each item's design. Resolve its facial or nonfacial cue, connected body action, meaningful prop contact, exact caption or deliberate absence of text, view, crop, and overlap order. Identify the cue that must survive reduction and any caption's relationship to it. This is a design account, not a new file schema or ledger.

Compare nearby intents and plausible misreadings. A restrained receipt acknowledgment may need a different action from an enthusiastic agreement. A forward-held object may imply an offer rather than gratitude. Decide from the current subject and chat context, not a fixed gesture dictionary. Several items can serve the same broad purpose when their tone, intensity, relationship, or expected reply differs deliberately. Revise accidental duplicates instead of changing labels on an unchanged pose.

Set shared identity anchors, rendering style, palette, edge treatment, lettering treatment, and visual scale across the pack. Adapt the crop to the reaction instead of enforcing identical bounding boxes. Preserve meaningful anatomy and prop relationships through the selected simplification. Keep enough space for an outstretched gesture or caption to remain legible.

Read the [template index](templates/index.md) when one of its recipes fits. A pack may combine recipes under the same visual rules. The three generic composition recipes and fourteen source-based Oneirloom adaptations are separate choices, not a required pack size or reaction inventory.

When the user requests or selects the Oneirloom mascot, read the [brand reference](references/oneirloom-brand.md) and choose a relevant source-based adaptation from the index. Its private identity images and sticker outputs are not bundled. Use an authorized reference supplied for the task; if none is available, keep brand-specific visual claims and reference-based production unresolved. Generic sticker design can continue with the user's supplied identity or an explicitly unobserved design brief. Use the [research coverage](references/research-coverage.md) for its source and evidence limits, and the [platform profiles](references/platform-profiles.md) when selecting exports. These branded examples do not replace an unrelated subject's identity or make Oneirloom the default character.

If a material uncertainty remains, choose a few calibration cases that expose it before expanding that direction. A quiet acknowledgment, a strong action, or a relevant occlusion can test different questions. Use only cases needed for the current uncertainty and reuse credible current output evidence. Prompt-only work can propose calibration but cannot claim to have run it. No fixed case count or mandatory approval round is required.

## Produce the requested output

Choose production after the design. For raster generation and edits, use an available native image-generation entry. Honor an explicit vector or code request with actual vector or code work. A raster with clean outlines is not a vector file. Preserve the requested model and medium, and confirm reference or editing support at the actual entry.

Vendor documentation establishes documented capability, not local availability or successful output. Distinguish four operations: multiple input references, multiple candidates for one reaction job, separate jobs for different reactions, and multiple cells inside one grid. Support for one operation does not establish the others. Attribute input roles and specify each intended reaction separately.

When a usable master and a compatible reference entry are available, generate or edit each reaction from the master or an appropriate accepted view. Avoid carrying accumulated changes through a chain of different reactions. Iterative edits within one reaction can preserve its successful parts. Direct generation remains suitable when the design and available identity evidence support it.

Request native alpha only through an entry that supports it. Keep settings such as `transparent_background` outside prompt text, and use them only when confirmed at that entry. A successful call does not establish clean alpha. Do not infer animation, export formats, upload support, or platform acceptance from a static generation capability.

Generate each requested reaction as its own image, or use a supported production path that yields independently inspected files. Use a grid for concept comparison, or conditional export when its actual cells contain adequate separable artwork. A grid alone remains a contact-sheet result. Separate crops count as delivered files only after actual export and inspection of every crop. Check usable resolution, complete edges, cross-cell artwork or captions, duplicated reactions, and alpha where required.

For captions, preserve the exact user text, punctuation, and language. Choose native generation or editable lettering according to text accuracy and the requested workflow. Do not force an external typography tool or a composite path when the selected entry meets the task. Preserve caption literals in both prompt languages rather than translating them into different in-image text.

Use lettering, compositing, or alpha repair when an observed defect or an explicit editable-output requirement justifies it. Masks, code, and layers are not universal prerequisites. Consider subject tuning only for recurring identity failures after representative reference trials, with suitable source material, a compatible backend, and task authorization. Test unused reactions for both identity and expressive range. Repeating the training pose does not resolve the requirement.

### When animation is requested

Design the key poses, transition, readable hold, and ending around the conversational action. Use a purposeful loop when it suits the response or the platform requires it. Movement alone does not make the message clearer. Preserve anatomy, identity, prop contact, lettering, and alpha across frames. Check the first frame as a complete message when the target platform uses it as the static view.

Choose frame count, timing, duration, encoding, and file size from the design and the target platform's actual rules. There is no universal animation profile. With an unknown platform, continue the motion design and any authorized portable production while leaving platform compliance unresolved. Inspect actual encoded playback, including transitions, holds, and the loop join. A storyboard, keyframe grid, or successful encode does not prove tested animation.

## Review and deliver

Judge the intended response and character identity first. Inspect each result at its intended chat and picker sizes for readable action, connected anatomy, justified occlusion, meaningful prop contact, and intact crop. Compare exact lettering character by character, including punctuation and intended line breaks. OCR and similarity scores can assist but do not establish acceptance.

Judge captions and images together. Text may carry the main response; a caption-hidden check only diagnoses the image's contribution. Do not impose independent wordless comprehension on a text-led sticker. Check whether pose and wording contradict each other and whether the type obscures a decisive feature.

Inspect the pack for shared palette, material, lettering, visual scale, and identity continuity, then for useful differences and missing responses. Return to individual files after the overview. When target recipients are available, ask what the sender means before revealing the intended label. Then show the preceding message and ask what reply or action follows. Allow multiple suitable stickers, none, plain text, or no reply. Record the version, context, observed paraphrases, and relevant audience. AI review can identify concerns but cannot claim human comprehension. Missing recipient tests block only that claim.

Check the real alpha channel where required and inspect composites on relevant light and dark backgrounds, adding colored or patterned chat backgrounds when useful. Examine thin appendages, fur, detached marks, text edges, and halos. A PNG extension, painted checkerboard, or clean preview background does not establish transparency. Valid alpha alone does not establish correct cutout edges.

Correct the stage responsible for a miss. A disconnected net or changed identity needs a design or image correction; relabeling the sticker does not repair it. Use the existing [result-diagnosis method](../oneirloom-result-diagnosis/SKILL.md) when a critical miss persists under its bounded correction procedure.

For prompt-only work, return one complete usable Chinese prompt and a semantically equivalent English prompt for each required image, unless the user requests one language. Resolve every template slot into concrete visible construction. Keep the preceding turn, recipient analysis, possible misreadings, and acceptance commentary outside copyable prompts. Carry their consequences into the visible pose, framing, and lettering. Keep entry controls and reference inputs outside too. For a composite path, include necessary asset prompts and assembly guidance.

For a finished pack, inspect every exported file for dimensions, format, complete artwork, caption, requested alpha, and animation behavior where applicable. Deliver the individual files, a preview, and a mapping of each file to its intent and exact caption. Include editable source when requested or required by the chosen path. Preserve source references and known prompts, inputs, entry settings, and output metadata without inventing missing records or requiring a new logging system.

Distinguish semantic use, visual family, file validity, and platform behavior in the delivery status. Report the evidence actually available for each relevant claim. Prompt-only work needs its unrendered status, not a full production checklist. If only a grid exists, label it as a preview with individual exports outstanding. File inspection does not prove chat understanding or platform import. Claim import, display, or review acceptance only after the corresponding event. Uploading and publication require separate authorization.

The public package supplies three generic recipes without example images and fourteen text adaptations with conditional Oneirloom case studies. Use the [identity-transfer instructions](templates/index.md#use-an-adaptation-with-your-own-identity) to apply their methods to a supplied subject. The dated evidence summaries describe 156 selected private local PNG entries, including reused files; those images, identity assets, production records, and delivery archives are not bundled. Their paths preserve provenance only. These historical inspections do not establish the quality of a new result or make unavailable samples inspectable. Structural review alone does not establish image quality.
