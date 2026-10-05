---
name: minimax-h3-keyframe-video-prompt
description: "Narrow downstream MiniMax H3 specialist for pure I2VA, FL2VA, and L2VA boundary-frame prompts. Use only after minimax-h3-creative-director verifies that the user explicitly declared the images as literal first/last frames and that they have no character, identity, person, object, costume, scene, style, voice, action, camera, or other reusable reference responsibility. Otherwise use full-reference consistency, even when first/last-frame semantics are desired."
---

# MiniMax H3 Keyframe Video Prompt

Design a continuous visual path from or toward concrete boundary frames. Treat a boundary image as an actual target frame, not merely a loose style reference.

## Routing Contract

New MiniMax H3 requests should enter through `minimax-h3-creative-director`. Use this skill only for explicitly declared boundary-only images. If the user did not explicitly say first frame, last frame, starting frame, ending frame, or an equivalent literal boundary role, use `minimax-h3-reference-video-prompt`. If any image also defines or preserves a character, identity, person, object, costume, scene, style, voice, action, camera, composition, or other reusable trait, use full-reference even if the user also calls it a first or last frame.

## Official Format Authority

Before drafting, read `../h3-prompt-writing/SKILL.md` and `../h3-prompt-writing/references/base-en.txt`. Treat those official MiniMax files as the canonical prompt-format specification. If this skill or its local references conflict with them, follow the official files.

Read `references/keyframe-rules.md` before drafting.

## Confirmed Multishot Handoff

When the director supplies a confirmed `multishot_plan`, treat its shot count, timing, content, framing, performance, camera, transitions, sound, and continuity decisions as already answered. Do not ask those questions again. Map every confirmed shot into the official keyframe prompt while preserving exact boundary-frame alignment. Reopen a decision only when the plan is physically impossible, contradicts a boundary image, or exceeds the effective duration.

## Mandatory Format

Always return the exact mode-specific picture-alignment instruction followed by the official three fields. Never return a free-form natural-language paragraph, keyword list, shortened prompt, or alternate schema as the final English prompt.

## Interactive Direction Check

Before drafting, use the host's structured-choice tool whenever the eligible pure-keyframe brief is sparse, the intended transformation is underspecified, two or more of duration, motion path, visual treatment, camera strategy, dialogue/sound, or ending behavior are missing, or the user delegates creative direction to the AI.

In OpenCode, call the built-in `question` tool rather than printing Markdown options. In Codex, use the available structured user-input tool; if unavailable, ask one concise plain-text question.

Ask as many related questions as the current decision stage requires; normally 1-5, but three is not a per-call, per-turn, or per-session ceiling. A strict yes/no question may contain exactly two options; every other choice question must contain at least five materially different, feasible options. Put the context-specific recommendation first with `(Recommended)` in its label, explain each consequence in one sentence, omit `Other`, and enable multiple selection only for genuinely combinable choices. Before every `question` tool call, count the options in the actual payload. If any non-binary choice has fewer than five, do not submit it; expand it with meaningful alternatives or make it open-ended. Do not create near-duplicates merely to reach five.

Prioritize:

- Boundary role when one image is ambiguous: first frame or last frame
- Motion strength: subtle natural motion, clear narrative action, dramatic transformation
- Camera strategy: continuous single shot, restrained cuts, dynamic montage
- Landing behavior: exact stable hold, arrive on the final instant, transition through the frame

For a sparse or delegated brief, ask enough high-impact questions in one batch to establish the current stage, normally 3-5. Do not treat "improvise" as permission to skip questions. Skip only when the user explicitly prohibits questions, then disclose the chosen direction.

## Select the Mode

- Explicit first-frame-only image with no reusable reference role -> I2VA.
- Explicit first-and-last-frame pair with no reusable reference role -> FL2VA.
- Explicit last-frame-only image with no reusable reference role -> L2VA.

If boundary wording is absent, ambiguous, or merely inferred, do not ask the user to confirm this specialist. Route directly to `minimax-h3-reference-video-prompt`.

If the same boundary image or any other asset must also control identity, character, object, action, style, scene, sound, editing, or pacing, use `minimax-h3-reference-video-prompt` and express the first/last-frame relationship inside the full-reference prompt. Do not mix API `first_frame`/`last_frame` roles with `reference_*` roles.

## Workflow

1. Confirm the boundary role, exact integer duration, and intended final action or transformation. Keep the official online target within 4-15 seconds, 24 FPS, and 7000 prompt characters; obey narrower local-workflow limits when known.
2. Inspect supplied images when available. Record identity, clothing, pose, object states, composition, camera angle, lighting, and spatial relationships.
3. Define the motion path before writing prose.
4. Keep subject identity and persistent attributes consistent unless the user explicitly requests transformation.
5. Prefer a single continuous transition for FL2VA and usually for L2VA. Two boundary images do not automatically create a cut. Add cuts only when explicitly requested or essential.
6. Write the exact alignment instruction, then the three core fields.
7. Validate that the target boundary frame is reached at the exact endpoint rather than early.
8. Return the required bilingual output.

## Motion Paths

### I2VA

Use: first-frame anchor -> action onset -> continuous development -> result or reaction.

### FL2VA

Use: first-frame state -> observable intermediate changes -> progressively narrowing differences -> exact last-frame state.

Do not merely describe two static images. Explain how poses, objects, lighting, camera, and composition transform between them.

### L2VA

Use: plausible preceding state -> explicit causal action -> gradual convergence -> exact final-frame landing.

Do not begin in the final state. Infer a compatible earlier state and show how it becomes the reference frame.

## Required Prompt Structure

Place the mode-specific alignment instruction first, followed by one blank line and:

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

Use the exact official alignment forms in `references/keyframe-rules.md`.

## Output Contract

Return `### English Prompt`, one `text` code block containing only the complete English prompt, then `### 中文翻译` with a complete Chinese translation outside code blocks.

## Language Policy

Write all descriptive and instructional prose in the English prompt in English. Preserve non-English source wording only when exactness is required for:

- Dialogue, voiceover, speech, singing, or lyrics inside `<d>[Language] ...</d>`
- Visible signs, captions, subtitles, labels, interfaces, titles, logos, or messages
- Exact personal names, place names, brands, organizations, product/work titles, account names, and handles
- Filenames, URLs, model names, picture labels, and control tokens

Do not use non-English wording for style, composition, appearance, lighting, actions, transitions, camera movement, sound design, or music unless it is literal content to be spoken or shown.

Translate every completed prompt instruction into Chinese after the English code block, including the meaning of dialogue, lyrics, and visible text. Keep field names, picture labels, `[Shot N]`, timestamps, `(Sx)`, and control tags visible alongside their Chinese explanations. Preserve exact proper nouns and source literals, adding Chinese meaning where useful. Treat the Chinese section as explanatory rather than executable.

Add `### 采用的假设` before the English prompt only when useful. Keep the executable English prompt within the official 7000-character maximum; choose detail according to transition complexity and remove repetition.

## Quality Gate

- The selected mode matches the supplied boundary frames.
- The alignment instruction is exact and uses the effective duration with exactly two decimal places where required.
- The initial state matches the first-frame image when one exists.
- Intermediate changes are visible, causal, and feasible within the duration.
- Identity, clothing, key objects, spatial relations, and persistent colors remain continuous.
- The final pose, object state, camera angle, lighting, spacing, and composition land on the last frame when one exists.
- The final frame is reached at the end, not held prematurely.
- Dialogue fits its shot duration, and any cross-cut speech relationship is explicit.
- Required visible text is quoted exactly.
- The prompt does not contradict one-take versus cuts or music versus `N/A`.
- The final English prompt is no more than 7000 characters.
- Dialogue, sound, and camera follow the shared MiniMax H3 rules, and the Chinese section translates every prompt component without adding content.
