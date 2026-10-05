---
name: minimax-h3-text-video-prompt
description: "Downstream MiniMax H3 specialist for professional text-to-video (T2VA) prompts using the official three-field format. Use after minimax-h3-creative-director routes a request with no image, video, or audio reference asset, or when this skill is explicitly invoked for a text-only idea, script, or storyboard requiring an audiovisual timeline and Chinese translation."
---

# MiniMax H3 Text-to-Video Prompt

Turn a text-only video concept into a precise MiniMax H3 T2VA timeline. Write observable audiovisual instructions rather than a plot summary or a keyword pile.

## Routing Contract

New MiniMax H3 requests should enter through `minimax-h3-creative-director`. If invoked directly, apply the official authority below and proceed without requiring a second routing round. Redirect to the keyframe or full-reference specialist when supplied assets materially control the result.

## Official Format Authority

Before drafting, read `../h3-prompt-writing/SKILL.md` and `../h3-prompt-writing/references/base-en.txt`. Treat those official MiniMax files as the canonical prompt-format specification. If this skill or its local references conflict with them, follow the official files.

Read `references/official-rules.md` before drafting.

## Confirmed Multishot Handoff

When the director supplies a confirmed `multishot_plan`, treat its shot count, timing, content, framing, performance, camera, transitions, sound, and continuity decisions as already answered. Do not ask those questions again. Map every confirmed shot into `integrated_multimodal_description` without dropping or silently changing choices. Reopen a decision only when the plan is physically impossible, internally contradictory, or exceeds the effective duration.

## Mandatory Format

Always return the official three-field prompt. Never return a free-form natural-language paragraph, keyword list, abbreviated prompt, or alternate schema as the final English prompt, even when the user's input is informal or brief. Expand the request into the required structure.

## Interactive Direction Check

Before drafting, use the host's structured-choice tool when any of these conditions applies. This is mandatory, not optional:

- The brief is short, generic, or contains only a subject and a basic action.
- Two or more of duration, scene/event progression, visual style, camera/edit rhythm, dialogue/voice, sound/music, or ending are missing.
- A vague phrase has multiple materially different interpretations.
- The user says to improvise, decide freely, surprise them, or let the AI choose.
- Duration, visual treatment, action intensity, camera rhythm, or sound direction would substantially change the result.

In OpenCode, call the built-in `question` tool rather than printing Markdown options. In Codex, use the available structured user-input tool; if none is available, ask one concise plain-text question.

Ask as many related questions as the current decision stage requires; normally 1-5, but three is not a per-call, per-turn, or per-session ceiling. A strict yes/no question may contain exactly two options; every other choice question must contain at least five materially different, feasible options. Put the context-specific recommendation first and suffix its label with `(Recommended)`. Give every option a one-sentence consequence. Do not add `Other`; OpenCode supplies custom input automatically. Use multiple selection only when choices can genuinely be combined. Before every `question` tool call, count the options in the actual payload. If any non-binary choice has fewer than five, do not submit it; expand it with meaningful alternatives or make it open-ended. Do not create near-duplicates merely to reach five.

Prefer questions about:

- Visual medium and style: live-action cinematic, animation, stylized commercial, documentary, and similar directions
- Narrative/action intensity: restrained, balanced, dynamic
- Camera rhythm: one continuous shot, limited cinematic cuts, fast montage
- Sound direction: natural ambience only, restrained score, prominent audiovisual design

For a sparse or delegated brief, ask enough high-impact questions in one batch to establish the current stage, normally 3-5, rather than silently completing the concept. Do not ask about minor details after those answers establish the direction. Skip questions only when the user explicitly says not to ask; a request to "freely create" or "improvise" requires questions rather than skipping them.

## Workflow

1. Extract or reasonably infer duration, aspect ratio, visual style, subjects, setting, action arc, dialogue, sound, and desired ending. Keep the official online target within 4-15 seconds, 24 FPS, and 7000 prompt characters; obey narrower local-workflow limits when known.
2. Run the interactive direction check when required. Never invent dialogue, lyrics, or visible text.
3. Budget actions and cuts to fit the requested duration. Prefer one coherent action arc over many incomplete events.
4. Establish style, composition, subject appearance and position, environment, lighting, and initial state at `[Shot 1]`.
5. Describe visible state changes in playback order: initial state -> action onset -> continuous development -> result or reaction.
6. Add cuts only when they introduce a meaningful change in subject, space, state, viewpoint, or time. Otherwise use camera movement.
7. Assign stable `(S1)`, `(S2)` IDs only to actual vocal sources. Preserve user-provided words and punctuation inside `<d>[Language] ...</d>`.
8. Separate synchronized audiovisual events, overall physical soundscape, and audience-only music.
9. Perform the quality checks below, then return the required bilingual output.

## Required Prompt Structure

Produce exactly these three fields in this order:

```text
integrated_multimodal_description: [Shot 1] ...

overall_soundscape: ...

non_diegetic_music: ...
```

Do not add an image-alignment instruction for T2VA.

## Output Contract

Return:

1. `### English Prompt`
2. One `text` code block containing only the final English prompt
3. `### 中文翻译`
4. A complete Chinese translation outside any code block

## Language Policy

Write every instruction in the English prompt in English except content that must remain exact:

- Dialogue, voiceover, speech, singing, and lyrics inside `<d>[Language] ...</d>`
- Text visibly present in the video, including signs, captions, subtitles, labels, interfaces, titles, logos, and messages
- Proper nouns whose exact spelling matters, including personal names, place names, brands, organizations, product/work titles, account names, and handles
- Literal identifiers such as filenames, URLs, model names, reference labels, and control tokens

Do not use Chinese or another non-English language for scene description, style, composition, appearance, lighting, action, camera, editing, sound design, or music unless the user explicitly requires that literal wording to appear or be spoken in the video.

Translate every descriptive part of the completed prompt into Chinese after the English code block, including the meaning of dialogue, lyrics, and visible text. Keep structural identifiers such as field names, `[Shot N]`, timestamps, `(Sx)`, and control tags visible alongside their Chinese meanings so the translation can be mapped line by line. Preserve exact proper nouns and source literals, adding a Chinese explanation where useful. The Chinese section is explanatory and is not an executable MiniMax prompt.

If assumptions materially help the user, place a short `### 采用的假设` section before the English prompt. Do not put explanations or alternatives inside the English code block.

Keep the executable English prompt within the official 7000-character maximum. Use the detail required for professional control while removing repetition, contradictions, and details that cannot affect visible or audible output.

## Quality Gate

Before answering, verify that:

- `[Shot 1]` has no timestamp; later cut times are strictly increasing and inside the duration.
- Every shot establishes the current composition before describing changes.
- Actions have a physically understandable start, progression, and result.
- Camera terms are mechanically correct and written as natural English actions.
- Dialogue is exact, speaker IDs are stable, and voiceover cannot cause unintended lip movement.
- Dialogue length is feasible for its shot; cross-cut speech explicitly continues as a J-cut or L-cut when applicable.
- Every required title, sign, logo, caption, subtitle, slogan, or interface label is quoted exactly.
- `overall_soundscape` does not repeat dialogue, singing, or diegetic music.
- `non_diegetic_music` specifies instrumentation, tempo/rhythm, and dynamics, or is `N/A`.
- The prompt does not contradict itself about one-take versus cuts or music versus `N/A`.
- The final English prompt is no more than 7000 characters.
- The Chinese translation covers every English instruction and every literal verbal or visible element without introducing new creative content.
