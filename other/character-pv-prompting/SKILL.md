---
name: character-pv-prompting
description: Create, rewrite, audit, or repair production-ready prompts, poster/keyframe asset plans, and edit plans for a single-character PV, OC showcase, character reveal trailer, anime/game character PV, or still-illustration/2.5D character MAD. Use for 人物PV、角色PV、OC PV、角色登场片、人物展示视频、高密度二维MG人物片、人物PV海报/主视觉、尾帧锁字、15秒以上人物PV拼接，或优化这类视频的节奏、卡点、画面控制、动态排版、转场和最终身份卡；do not use for story/season trailers, ensemble cast reels, product ads, ordinary dialogue scenes, general music videos, character design sheets, or a fight sequence with no character-introduction goal.
---

# 人物 PV 提示词导演

Follow the repository `AGENTS.md`, the `$manju-story-studio` entrypoint, and the target series continuity before changing story or production files. This Skill owns single-character PV creative structure, related poster/keyframe planning, rhythm, frame control, text-lock strategy, and multi-segment handoff design. The parent Skill owns repository contracts, asset registration/wiring, model capability verification, tool-native compilation, strict validation, and Take logging.

Create a PV that makes one character memorable without requiring plot context. The audience should retain who the character is, their attitude, one signature action or ability, and one final identity image.

## Route the request

1. Identify whether the user wants a new prompt, a rewrite/audit, or repair after a generated result. Preserve their named model, duration, aspect ratio, language, style, story facts, and required shots.
2. Inspect supplied character images or video references before describing them. If no reference exists, turn the user's character description into a compact identity lock. Do not infer visual facts from filenames.
3. Resolve only the inputs that materially change the result: one-sentence audience memory, character identity/state, signature activation/action, runtime/format, visual grammar, semantic-text policy, audio direction, target model/tool, delivery mode, and the role of every supplied or proposed image. Make labeled, reversible defaults for low-risk omissions instead of blocking.
4. Choose one primary motion strategy:
   - **Performance-led animation:** one signature physical action carries the reveal; graphics frame and punctuate it.
   - **Still-art / 2.5D packaging:** character movement stays subtle; layered parallax, crop changes, masks, typography, texture, and light carry the energy.
   - Use a hybrid only when the generation/edit pipeline can keep the layers separate and identity stable.
5. Read [rhythm-and-frame-control.md](references/rhythm-and-frame-control.md) when designing or repairing the creative structure. Read [poster-keyframes-and-segmentation.md](references/poster-keyframes-and-segmentation.md) when the request includes a source poster, a new visual poster, exact visible text, a first/last frame, a model limit, or a PV longer than one reliable generation unit. Read [prompt-blueprint.md](references/prompt-blueprint.md) when compiling the final prompt.
6. Deliver the model-neutral creative core: image prompts for assets that must be generated, one video-prompt plan per generation unit, and a stitch/post plan when the final edit spans units. Then return to `$manju-story-studio` for capability resolution, reference wiring, tool-native compilation and strict preflight. Preserve a user-named tool and its constraints; when no tool is named, the parent Skill applies the repository default. Do not claim unsupported model capabilities from memory.

## Non-negotiable design rules

- Build a reveal ladder: discriminating fragment or silhouette -> partial identity -> activation -> signature image -> readable final identity card. The first shot may hook, but should not spend every reveal.
- Design three rhythm levels: whole-film energy arc, information-changing edit beats, and sound-synchronized micro-accents. BPM alone is not direction.
- Distinguish continuous movement from a new layout state. A pan, zoom, hair sway, or ring rotation does not count as fresh content when the crop, anchor, background system, container, palette state, and shot role stay the same. During an intended acceleration, specify short state changes and deliberate holds instead of merely asking the camera to move faster.
- Alternate shot roles when density matters: identity fragment, face/attitude, prop or outfit detail, full silhouette, graphic-only punctuation, editorial multi-panel, hero pose, and final card. Adjacent beats with the same role need a clear information upgrade or should be merged.
- Use contrast. Restraint makes acceleration legible; a brief hold or sound withdrawal gives an impact weight; the hero image and final card need more reading time than connective flashes.
- Give each edit beat one primary information change and each frame one dominant visual anchor. Merge decorative repeats; split frames where face, prop, title, particles, and background all compete.
- Record shot size, anchor position/scale, gaze or facing, negative space/text zone, layer order, one supporting action, dominant motion vector, one camera or layout move, transition carrier, and exit composition.
- Make every transition causal. Match shape, color ownership, movement vector, occlusion/mask, repeated motif, gaze, or sound from the previous exit into the next entry. An effect name by itself is not a transition plan.
- Derive the palette, motif family, silhouette logic, texture, and typography from the character. Never copy a source example's fixed colors, symbols, BPM, shot count, or named visual style as a universal recipe.
- Assign every image one role before writing the video prompt: identity/style reference, first-frame composition, last-frame composition, motion reference, or post-only overlay. An identity poster is not automatically a first frame; anchoring it as one can force an over-literal, static opening.
- Build a related poster from the character's locked face, hair, outfit, prop, attitude, palette ownership, and motif family. Preserve those invariants while changing pose, framing, negative space, and graphic arrangement to serve the intended asset role.
- Separate semantic text from graphic texture. If names or claims must be readable and the video model is unproven at text, generate a clean visual plate and add type in post, or pre-render and visually verify an exact-text last-frame image. Do not ask the video model to invent spelling during motion.
- Protect identity with a motion budget. High-risk still references get breathing, gaze, hair/cloth drift, hand tension, prop response, and layer motion; use complex full-body action only when the selected mode and references support it.
- Separate the final edit cuts from generation units. Do not force dense sub-second cuts, readable typography, multiple locations, and complex character motion into one generation merely because the final PV is short.
- Bind audio instructions to visible events. State dialogue/voice, synchronized SFX, ambience, and BGM or intentional silence separately; silence and freezes must still specify what remains alive on screen.
- For music-led PVs, compile an audio-hit map. Give the important accents exact times, name the sound, the visual preparation, the impact frame, and the rebound or hold. Do not assign every beat the same flash, shake, or cut.
- For graphic 2D PVs, define the space law before the shot list: what is flat, what may overlap, which axes may distort, how silhouettes/inversion/masks behave, and which 3D cues are forbidden. Treat the world as a controlled design system rather than a generic background.
- Give continuous character action a clear information job and endpoint. When the same action, framing, and background role persist across several beats, shorten it or interrupt it with a new crop, color owner, layout container, graphic-only punctuation, or reaction; camera motion alone does not cure repetition.
- Treat `15 seconds` as a routing checkpoint, not a universal technical limit. Verify the active backend. Keep a short PV in one generation unit only when its identity, action, layout and text complexity are reliable together. Split a longer or overloaded PV into profile-valid units at a motivated full-frame occlusion, graphic field, impact, or other reconstructible handoff.
- End on a completed pose and clean silhouette with controlled background motion, deliberate text space, sufficient reading time, and an explicit cut or audio-tail exit.

## Output contract

For a new PV, provide:

1. A concise assumption/creative-lock block only when choices were not supplied.
2. An asset-role plan and paste-ready poster/keyframe prompts when new identity/style, first-frame, or exact-text last-frame images are required.
3. One paste-ready video prompt per generation unit containing the identity lock, motion strategy, visual grammar/space law, rhythm arc, time-coded shots, layout-state changes, audio-hit map, frame control, causal transitions, text policy, final card, and short observable failure list.
4. For multi-unit PVs, a segment table with generated duration, reused/trimmed overlap, entry/exit state, audio phase, reference wiring, and final runtime math.
5. A separate post-production note only for layers the model should not generate or reliably hold, such as semantic typography, edit-only sub-second cuts, or a deterministic final-card reveal.

For an audit or repair, first name the failure in observable terms and assign it to identity, rhythm, frame hierarchy, camera/layout, transition, motion overload, typography, audio, or final-card readability. Change the smallest responsible layer; do not rewrite the character concept unless the user asks.

Source examples are study material, not reusable prompt text. The linked Feishu corpus explicitly permits skill refinement and marks its prompts non-commercial; do not reproduce, resell, or present those prompts as this Skill's original examples.
