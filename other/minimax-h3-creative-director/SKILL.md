---
name: minimax-h3-creative-director
description: "Primary mandatory entrypoint for every MiniMax H3 video-generation request. Use before any other H3 skill for creation, animation, extension, editing, restyling, reference, or prompt review. It reads the official h3-prompt-writing specification, defaults image-based work to full-reference consistency, permits pure keyframe mode only for explicitly declared boundary-only images, and enforces a non-skippable multishot question workflow for explicit multishot requests or accepted 10-second-plus proposals before routing to the final formatting specialist."
---

# MiniMax H3 Creative Director

Act as the mandatory front door for MiniMax H3 work. Establish official format authority, choose the correct generation path, and invoke the matching specialist without making the user understand internal routing.

## Mandatory Official Read Order

Before analyzing or drafting any H3 prompt:

1. Read `../h3-prompt-writing/SKILL.md` first.
2. Inventory the request and supplied assets.
3. Read `../h3-prompt-writing/references/base-en.txt` for T2VA, I2VA, FL2VA, or L2VA; read `../h3-prompt-writing/references/ref-en.txt` for reference generation, editing, continuation, or audio/reference work. Read both when routing is ambiguous or mixed.
4. Read `references/official-capabilities-and-routing.md` for official limits, asset roles, contradiction checks, and routing policy.

Treat the official `h3-prompt-writing` files as canonical for prompt syntax. Treat the official-manual reference as canonical for product capabilities and operating limits. If a downstream skill conflicts with either authority, follow the official source.

## Routing Decision

Choose exactly one final prompt-format specialist:

- No reference assets, or text/script/storyboard only -> `minimax-h3-text-video-prompt`.
- Pure keyframe exception -> `minimax-h3-keyframe-video-prompt` only when all conditions are true: the user explicitly calls each relevant image a literal first frame, last frame, or first-and-last-frame pair; the images serve only as boundary frames; and no image is expected to preserve or reference a character, identity, person, object, costume, scene, style, voice, action, camera, or other reusable trait.
- Default for every other request containing an image -> `minimax-h3-reference-video-prompt`, including ambiguous image roles, ordinary image animation, character/person/object consistency, and any request where a boundary image also supplies reusable visual identity or content.
- Mixed images/videos/audio, source-video editing, continuation, voice/audio control, or any other reference relationship -> `minimax-h3-reference-video-prompt`.
- Existing prompt that must be checked, repaired, converted, or polished -> `minimax-h3-prompt-reviewer`.

`minimax-h3-multishot-planner` is an optional planning subskill, not a competing final specialist. Invoke it before the selected text, keyframe, or reference specialist when the multishot gate below requires it. Pass its confirmed shot plan to the final specialist as binding creative input.

Apply reference-consistency priority. Do not route to pure keyframe mode merely because there are one or two images, because the user says "animate this image," or because a first/last-frame interpretation seems plausible. If any pure-keyframe condition is absent or uncertain, route to full-reference without asking the user to downgrade. Full-reference can express a referenced image as a prompt-level first, key, or last frame while preserving character and object consistency.

After resolving creative questions and the multishot gate, read the selected final specialist's `SKILL.md` and required references, then execute it in the same task flow. Do not stop after announcing the route unless the user requested analysis only.

## Direction Check

Use OpenCode's `question` tool before drafting whenever any condition below applies:

- The request is short or supplies only a subject plus a basic action.
- Two or more important creative axes are missing: exact duration, scene/event progression, visual medium/style, camera/edit rhythm, dialogue/voice, sound/music, or ending state.
- A reference task does not clearly state desired action, scene progression, preservation priorities, audio treatment, or endpoint.
- The user asks the AI to improvise, decide freely, surprise them, fill in the details, or otherwise choose the creative direction.
- The user supplies an image with only a vague instruction such as "make it move" or "generate a video."
- Whether source video should be edited, continued, or merely imitated
- Whether audio should be reused exactly, partially reused, used as timbre/style reference, or replaced
- Whether the user wants one continuous take or intentional cuts

Ask as many related questions as the current decision stage requires; normally use 1-5 in a general direction batch. Three is not a per-call, per-turn, or per-session ceiling. Recommend the strongest option and use the user's answers to complete the brief. Do not replace required questions with hidden assumptions. The only exception is an explicit instruction not to ask questions; then choose the most coherent interpretation and disclose material assumptions.

For every H3 choice question, a strict yes/no decision may use exactly two options. Every other choice question must provide at least five materially different, feasible options, with the strongest context-specific recommendation first and `(Recommended)` appended to its label. Explain the consequence of every option, keep each option label within five words, do not add `Other`, and never pad a list with near-duplicates. If five meaningful alternatives cannot be produced, ask an open-ended question instead of a short choice list.

Immediately before every `question` tool call, audit the proposed payload. If any non-binary question has fewer than five options, do not submit it; expand it to at least five meaningful choices or convert it to an open-ended question. This preflight is mandatory.

Do not ask whether an ambiguous image should use pure keyframe mode. The routing default already resolves that ambiguity in favor of full-reference consistency.

## Multishot Gate

Resolve this gate after effective duration is known and before invoking the final prompt-format specialist:

- If the user explicitly requests multiple shots, scenes, cuts, montage, a sequence, or shot-by-shot design, invoke `minimax-h3-multishot-planner` directly without asking whether multishot is desired.
- If the user explicitly requests one continuous shot, one take, or no cuts, skip the multishot planner regardless of duration.
- If duration is at least 10 seconds and the user has not expressed a single-shot or multishot preference, ask one binary question: whether to use a multishot structure. Recommend yes or no according to action density, continuity risk, and the user's goal rather than always recommending multishot.
- If the user accepts, invoke `minimax-h3-multishot-planner`; if the user declines, record a single-shot constraint and continue.
- If duration is below 10 seconds and no multishot preference is stated, do not ask this gate question and continue without the planner.
- If duration is unknown, resolve duration first, then evaluate the gate. Exactly 10 seconds counts as at least 10 seconds.

The planner must first ask shot count, then plan every shot interactively. Once the user confirms its structured shot plan, pass that plan unchanged to the selected text, keyframe, or reference specialist. Do not repeat questions already answered during multishot planning.

### Non-skippable multishot state machine

Loading a Skill with the `skill` tool only places its instructions in context; it does not execute that Skill. Never treat `skill({ name: "minimax-h3-multishot-planner" })` as completion of multishot planning.

When multishot is selected, enforce these states in order:

1. `multishot_selected`: load `minimax-h3-multishot-planner`.
2. `planner_loaded`: the next interactive action must establish shot count. If count was not explicitly supplied, the next tool call must be `question`; do not load a final specialist.
3. `shot_count_confirmed`: plan Shot 1 through the final shot sequentially. The planner must issue the required per-shot `question` calls and receive answers for each shot.
4. `shots_confirmed`: build the complete `multishot_plan` and ask the final binary confirmation.
5. `multishot_plan_confirmed`: only now may a text, keyframe, reference, or reviewer Skill be loaded.

Hard blocker: while multishot is selected, do not load or invoke `minimax-h3-text-video-prompt`, `minimax-h3-keyframe-video-prompt`, `minimax-h3-reference-video-prompt`, or `minimax-h3-prompt-reviewer` until a complete confirmed `multishot_plan` exists in the conversation. If the planner was loaded but no shot questions were asked, remain in `planner_loaded`; do not advance.

## Creative Brief

Before drafting, internally establish:

- Asset-role map: upload order, stable label, intended role, and traits that must remain unchanged
- Core creative line: subject, location, event/action, genre/style, and camera/edit strategy
- Timeline: duration, shot boundaries, shot size, composition, action, camera, dialogue, sound effects, and endpoint
- Preservation ledger: identity, clothing, objects, scene, text, voice, audio, and untouched source-video content
- Delivery target: official online product/API or local ComfyUI workflow, because runtime limits may differ

Do not expose this internal brief unless it helps the user.

## Mandatory Gates

- Keep the official online target within 4-15 seconds, 24 FPS, and 7000 prompt characters. If a known local workflow has a narrower supported range, obey the runtime-specific range instead.
- Assign an explicit role to every important uploaded asset. Never write vague references such as "use all references."
- In pure keyframe mode, state each explicitly declared boundary role. In full-reference mode, a referenced image may be described in the prompt as a first, key, or last frame while still preserving its character/object/reference responsibilities.
- Fit spoken words to the available shot time. Name on-screen versus off-screen speakers, preserve exact dialogue/lyrics, and state when speech continues across a cut. Use J-cut or L-cut only when its audio relationship is explicit.
- Specify exact visible text, logo wording, captions, interface labels, or slogans; never paraphrase content that must appear verbatim.
- Prefer observable action, composition, light, camera mechanics, and audible events over metaphors or adjective stacks.
- For a physical orbit, use a mechanically coherent lateral camera move plus counter-pan when appropriate instead of relying only on the word "orbit."
- Reject contradictions: one-take plus multiple cuts, music requested plus `non_diegetic_music: N/A`, face consistency without a usable identity reference, or excessive events for the duration.
- H3 generates native stereo audio. Do not treat sound as an optional afterthought.

## Response Policy

Return the specialist's copy-ready English prompt and complete Chinese translation. Keep routing commentary brief. Do not produce multiple competing prompt schemas unless the user explicitly asks for alternatives.
