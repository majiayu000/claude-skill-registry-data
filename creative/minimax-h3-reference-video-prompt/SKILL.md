---
name: minimax-h3-reference-video-prompt
description: "Default downstream MiniMax H3 specialist for every image-based request unless the user explicitly declares boundary-only first/last frames with no reusable reference role. Use the official six-section full-reference format for character/person/object consistency, scene/style/action/camera/storyboard/voice/audio reference, source-video editing or continuation, ambiguous image roles, ordinary image animation, and prompt-level first/key/last-frame anchoring."
---

# MiniMax H3 Full-Reference Video Prompt

Convert mixed reference assets and user intent into a traceable six-section full-reference prompt. Make every asset role explicit and write the target video as a detailed audiovisual timeline.

## Routing Contract

New MiniMax H3 requests should enter through `minimax-h3-creative-director`. This is the default specialist for any request containing images. Route away only when the user explicitly declares pure first/last boundary roles and no image also carries identity, character, person, object, costume, scene, style, action, camera, composition, or another reusable reference responsibility. Ambiguity stays here. Full-reference may use prompt-level first/key/last-frame anchoring while maintaining consistency.

## Official Format Authority

Before drafting, read `../h3-prompt-writing/SKILL.md` and `../h3-prompt-writing/references/ref-en.txt`. Consult `../h3-prompt-writing/references/base-en.txt` for the shared shot, camera, dialogue, visible-text, and sound rules when needed. Treat these official MiniMax files as the canonical prompt-format specification. If this skill or its local references conflict with them, follow the official files.

Read `references/reference-rules.md` before drafting.

## Confirmed Multishot Handoff

When the director supplies a confirmed `multishot_plan`, treat its shot count, timing, content, framing, performance, camera, transitions, sound, active references, and continuity decisions as already answered. Do not ask those questions again. Map every confirmed shot into `detailed_description`, keep reference labels and responsibilities stable, and carry the continuity ledger into retention and preservation instructions. Reopen a decision only when the plan is physically impossible, conflicts with a source asset, or exceeds the effective duration.

## Official Input Envelope

For the official online product/API, keep output within 4-15 seconds at 24 FPS and the prompt within 7000 characters. Accept at most 9 images, 3 videos, 3 audio files, and 12 mixed files total. Each video or audio file must be 2-15 seconds; combined video duration and combined audio duration must each be at most 15 seconds. Audio cannot be the only reference type. Respect the documented per-file and API-body limits. Treat local ComfyUI constraints separately when they are narrower.

## Mandatory Format

Always return the official six sections in their required order. Never return a free-form natural-language paragraph, keyword list, abbreviated prompt, base three-field prompt, or alternate schema as the final English prompt for a full-reference task.

## Interactive Direction Check

Before assigning labels or drafting, use the host's structured-choice tool whenever the brief is sparse; gives only an image plus a generic motion request; omits two or more of action progression, scene treatment, preservation priorities, visual style, camera/editing, dialogue/voice, sound/music, or endpoint; leaves a decisive reference responsibility unclear; or asks the AI to improvise.

In OpenCode, call the built-in `question` tool rather than displaying Markdown options. In Codex, use the available structured user-input tool; if unavailable, ask one concise plain-text question.

Ask as many related questions as the current decision stage requires; normally 1-5, but three is not a per-call, per-turn, or per-session ceiling. A strict yes/no question may contain exactly two options; every other choice question must contain at least five materially different, feasible options. Put the context-specific recommendation first and append `(Recommended)` to its label. Explain the consequence of each choice, omit `Other`, and use multiple selection only when roles can truly be combined. Before every `question` tool call, count the options in the actual payload. If any non-binary choice has fewer than five, do not submit it; expand it with meaningful alternatives or make it open-ended. Do not create near-duplicates merely to reach five.

Prioritize:

- Task relationship: reference generation, source-video editing, continuation, or a combination
- Asset responsibility: identity/appearance, clothing/scene, action/camera, storyboard/keyframe, audio/voice/music
- Fidelity policy: strict preservation, balanced adaptation, attribute transfer, broad stylistic reference
- Prompt-level picture anchor: no concrete anchor, first frame, intermediate keyframe, last frame
- Audio policy: direct reuse, partial reuse, timbre/style reference, newly designed sound

For sparse or delegated briefs, ask enough high-impact questions in one batch to establish the current stage, normally 3-5, even when the asset itself is visually clear. Do not ask the user to classify every asset; default images to character/object/scene consistency and ask about the desired creative outcome. Skip questions only when the user explicitly prohibits them. A request to improvise still requires questions.

## Workflow

1. Inventory every supplied image, video, audio asset, upload order, and text requirement; validate the official input envelope, then run the interactive direction check when required.
2. Map what each asset contributes: identity, appearance, clothing, object, environment, style, pose, action, camera, storyboard, edit source, continuation point, voice, sound, music, or rhythm.
3. Distinguish reusable visible content from source files. Assign stable `<Subject N>`, `<Picture N>`, `<Video N>`, and `<Audio N>` labels only where their defined roles apply.
4. Determine all applicable task types: `keyframe completion`, `reference generation`, `video editing`, `video continuation`, `audio reuse`, and `audio reference`.
5. Determine the retention relationship for every label.
6. Build the shot and sound timeline in playback order. Prove where each important reference first appears or takes effect.
7. Validate label consistency, source provenance, temporal feasibility, speaker identity, audio continuity, and any keyframe landing.
8. Return the required bilingual output.

## Prompt-Level Keyframe Anchoring

Allow a full-reference task to designate a referenced image as a concrete first frame, keyframe, edited keyframe, last frame, or composition anchor. Define it as a standalone `<Picture N>` and state its exact role, for example:

```text
<Picture 2> is the last frame of [Shot 3], defining the final pose, object placement, camera angle, lighting, and composition.
```

Combine `keyframe completion` with other task types in `summary` when appropriate. In `detailed_description`, describe a continuous path into or out of the anchored picture rather than repeating static image descriptions.

When a picture both anchors a boundary frame and preserves a person, character, object, costume, scene, style, or composition, keep the task in full-reference. Define both responsibilities explicitly instead of moving to the pure keyframe specialist.

Observe the current API distinction: prompt-level keyframe semantics are supported by the full-reference format, but an API request must not mix `first_frame`/`last_frame` roles with any `reference_*` role. When mixed reference assets are required, pass images as `reference_image` and express the concrete frame relationship in the prompt. Do not claim that the API role itself is a hard keyframe role.

## Required Prompt Structure

Produce exactly these six sections in order:

```text
subject_definitions:

summary:

retention_analysis:

detailed_description:

overall_soundscape:

non_diegetic_music:
```

Write all six sections in English, preserving the original language only for dialogue, lyrics, and text visibly present in the scene.

## Drafting Standard

- Define content units, not every source file mechanically.
- Assign every important uploaded asset an explicit role, including whether audio is reused fully, reused by track/time segment, or referenced only for timbre/style.
- Describe each shot's current composition, subject appearance and position, environment, lighting, actions, state changes, camera movement, sound, and active reference relationship.
- Keep reference definitions stable across all six sections.
- Do not reduce `detailed_description` to a plot summary or a list of reference links.
- Scale detail to the task's complexity while keeping the executable English prompt within the official 7000-character maximum.
- Never invent dialogue, lyrics, visible text, or unintelligible source words. Use `[unclear]` for unintelligible spans.
- Preserve exact transcripts or lyrics when speech, singing, or source audio must remain. Fit dialogue to shot duration and state cross-cut continuation explicitly.
- For source-video editing, maintain a preservation ledger for all content that must remain unchanged.

## Output Contract

Return:

1. `### English Prompt`
2. One `text` code block containing only the complete six-section English prompt
3. `### 中文翻译`
4. A complete Chinese translation outside code blocks

## Language Policy

Write all six sections in English except exact literal content that must remain in its source form:

- Dialogue, voiceover, speech, singing, and lyrics inside `<d>[Language] ...</d>`
- Text visibly present in the scene, including signs, captions, subtitles, labels, interfaces, titles, logos, and messages
- Exact personal names, place names, brands, organizations, product/work titles, account names, and handles
- Filenames, URLs, asset names, model names, reference labels, and control tokens

Write subject definitions, reference relationships, visual description, actions, camera, editing, sound design, and music in English. Do not retain non-English prose merely because the user's request was written in that language.

After completing all six English sections, translate every prompt component into Chinese, including the meaning of dialogue, lyrics, visible text, task types, retention relationships, and sound descriptions. Keep field names, task/relationship markers, `<Subject N>`, `<Picture N>`, `<Video N>`, `<Audio N>`, `[Shot N]`, timestamps, `(Sx)`, and control tags visible alongside Chinese explanations. Preserve exact proper nouns and source literals, adding Chinese meaning where helpful. The Chinese section is explanatory and not an executable prompt.

Add `### 采用的假设` before the English prompt only if materially useful.

## Quality Gate

- Every important asset has one clear role; no asset is referenced vaguely as part of "all materials."
- A `<Subject N>` denotes reusable visible content; `<Picture N>` denotes a concrete frame or planning anchor; `<Video N>` denotes a whole-video source or temporal structure; `<Audio N>` denotes an audio signal or audio reference.
- Task types match actual use rather than mere asset presence.
- Each retention marker belongs to the correct visual or audio vocabulary.
- Every label used later is defined once and retains the same meaning.
- Keyframe anchors name the shot and frame role, and the timeline reaches them coherently.
- Actual speakers have stable `(Sx)` IDs; audio-only verbal cues do not create fictitious speakers.
- Dialogue fits its shot duration; full and partial audio reuse identify exact source scope.
- Required visible text, logos, captions, slogans, and interface labels are quoted exactly.
- Sound layers are placed in the correct section.
- The prompt does not contradict one-take versus cuts or music versus `N/A`.
- The final English prompt is no more than 7000 characters.
- The Chinese translation covers every section and literal verbal or visible element without introducing new creative content.
