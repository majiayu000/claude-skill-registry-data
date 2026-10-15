---
name: product-demo-local-video
description: Create and refine short product-introduction films with LocalVideoGen native dialogue, approved characters, and readable real-app recordings. Use for LazyingArt app promos and preserving an accepted performance while changing branding or end cards; publishing is a separate step.
---

# Product Demo — Local Video

Show one recognizable problem, one real product action, and a small human payoff. The viewer should understand the app before being asked to download it. Use the product requested, not a montage of the portfolio.

## Choose the smallest operation

- **Accepted film, new icon/title/end card:** edit the existing master. Do not regenerate the performance or re-synthesize voices. Preserve its approved audio and unaffected frames; compare hashes where stream copying allows it.
- **New introduction:** capture the actual app and establish one short scene before spending a render. Read [the tested Bunko recipe](references/bunko-native-dialogue.md) for the local H3 starting point, its limitations, and review checks.
- **Publication:** use `lazyedit-publish-workflow` only when publishing is in scope. Creating a film or recording this skill is not permission to post it.

## Creative decisions that matter

- Open with the difficulty or action, not a long logo reveal. Make the benefit visible early.
- For a four-buddy short, two speakers are often enough. Others can react. Distinct identities do not require four sales pitches.
- Give dialogue a conversational reason: hesitation, useful observation, small discovery. Short turns, pauses and believable reactions work better than feature lists or exaggerated testimonial claims.
- Prefer speech generated together with the performance when natural dialogue and timing are wanted. Describe age, warmth and delivery; do not promise exact canonical voice identity without separate evidence.
- Avoid an old spoken guide containing unrelated words. It can contaminate generated dialogue. A requested voice match needs a clean, qualified reference and a separate listening check.
- Keep approved character references separate and identify each clearly. Do not redesign familiar characters without the user's request.
- Generate the scene and emotion; record the software. Model-invented phone text, buttons and results are not product evidence.

## Capture and edit

1. Check the current product, platform and feature. Use a representative action, not idle menus. Configure the requested languages explicitly. Browser footage must not be described as native-store installation footage.
2. Capture genuine UI large enough to read on a phone. Zoom or cut to the useful detail, hold long enough to understand it, then return to a reaction where it helps. Protect private accounts and source content.
3. Read LocalVideoGen's current `AGENTS.md`, `docs/runtime-admission.md` and relevant `docs/local-series-api.md` sections before generating. Respect the shared workstation owner/queue, GPU, RAM and cleanup gates. Reuse verified models and the canonical launcher; never bypass admission or stop a peer's service.
4. Submit within the current agreed render budget, retain the exact job ID, and reconcile that job after a timeout rather than blindly submitting again. Do not switch to paid cloud generation just because local work is slow.
5. Preserve the native dialogue timebase. Cut unwanted lines with picture and audio together at measured boundaries. If a cut breaks meaning or continuity, reassess rather than hiding it with loud music or unnatural speed changes.
6. Put real app capture over or instead of invented screens. Mix quiet owned/licensed music without masking words. Keep the app icon/name legible, with no unnecessary filled box. Use compact genuine store artwork and a restrained end card; avoid oversized homemade store buttons. Preserve correct store URL query parameters.

## Acceptance and delivery

- Transcribe the **actual** retained speech in its language. Compare both missing and extra words, not merely expected-word coverage. Review speaker assignment, listening quality and visible mouth timing separately; ASR does not prove warm voices or perfect lip sync.
- Review scene boundaries, phone/hand continuity, all required identities, invented text, mobile readability and exact app behavior. Use a contact sheet plus closer transition checks; do not infer quality from render completion.
- Full decode, duration/resolution/fps, audio channels and clipping checks must pass. Upscaled export resolution is not native model resolution.
- Keep the accepted master, corrected subtitle source, concise metadata, source/edit manifest and QA. Preserve the immediately previous accepted version when revising. Heavy raw media and private run history stay outside Git.
- For this workstation, deliver reviewed assets under `Nutstore Files/OneTimeSync/LazyingArt/` and coordination notes under `OneTimeSync/LazyPromotion/`. Verify local copy hashes; claim cloud sync only when independently checked.
- Stop only the runtime launched for this task after evidence capture, unless the user is actively reviewing it. An accepted file is the evidence, not an idle GPU process.

Public metadata should discuss the reader's problem and the real product naturally. Do not lead with model names, render settings or “this AI video.” Use required platform synthetic-content controls separately; do not present fictional characters as genuine customer testimonials.

## LazyingArt publication defaults

An approved clean preview is not an instruction to omit subtitles from publication. Unless the owner explicitly requests an exception, use `lazyedit-publish-workflow` to publish with corrected **English, Japanese, Chinese and French** subtitles. Reuse an audio-checked SRT rather than transcribing the accepted film again. In LazyEdit, top-to-bottom `en,ja,zh-Hant,fr` is requested with the bottom-to-top CLI order `--languages fr,zh-Hant,ja,en`.

- **Native portrait:** `--no-portrait-blur-fill`. Preserve the picture's original framing; use outlined subtitles without a filled panel.
- **Landscape adapted for vertical social posts:** enable the normal portrait background-fill layout, keeping the original foreground sharp and the subtitle area readable. Do not apply it twice.
- **Subtitle sizing:** keep the existing Studio/default size unless an accepted reference is specified; then copy that reference's full saved layout, including band height, lift and per-language scales. A font-scale number alone does not determine rendered size. Do not shrink the font or subtitle-band geometry merely to make four languages more compact. Ask before a material typography change. The owner requested the earlier English Bunko layout for the Chinese republication; the smaller-font experiment is not a reusable preset.
- Keep the approved performance, voices, music and end card. Add only the publishing overlays; use the configured Studio logo unless the owner specifies otherwise.
- Prepare with `--no-publish`, inspect the actual four-language text, timing and rendered mobile readability, then publish the inspected output. Check that silent sections stay silent and that subtitles do not cover the main UI.
- If a prior publication is still running, prepare locally but wait for its final receipt before dispatch. Reconcile ambiguous jobs instead of submitting another. A specifically requested subtitled repost is a separate run; leave the earlier post untouched unless its deletion is authorized.

These defaults concern LazyingArt product-introduction films, not unrelated music/player workflows with their own instructions. Save one-shot settings with the publication receipt; do not silently change shared Studio defaults.
