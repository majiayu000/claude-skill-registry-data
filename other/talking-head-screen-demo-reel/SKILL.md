---
name: talking-head-screen-demo-reel
description: Use when creating or analyzing Instagram Reels/TikToks/Shorts that combine a founder-style talking head with live screen recordings, Chrome extension/SaaS demos, cursor proof, kinetic captions, and a comment-keyword CTA.
---

# Talking-Head Screen Demo Reel

## Source pattern
Learned from Arshman Khalid Reel `DY6UXkINLri` / Clicko LinkedIn Chrome-extension demo. Use this when the user wants a Reel where the creator speaks directly to camera while actual product/browser footage runs behind them, with fast proof edits and small punchy captions.

## Core principle
This style sells a tool/workflow by making the viewer feel: **“I watched the creator use it in real time.”** The talking head supplies trust and momentum; the screen footage supplies proof; captions emphasize only the stressed phrase, not every word.

## Design system
- **Canvas:** 1080×1920 vertical, full-frame screen/demo footage or talking-head shot.
- **Talking head base shot:** warm desk setup, medium close-up from chest upward, direct eye contact, expressive hand gestures, visible microphone/keyboard/desk props. Face occupies upper/middle; hands enter frame often.
- **Overlay talking head:** when screen recording is the main shot, use a cutout/rectangular PIP of the creator at bottom-center/bottom-left, roughly 35–50% canvas width, no elaborate frame, preserving desk background. Keep creator large enough to read expressions.
- **Background footage:** actual browser/app/LinkedIn/Chrome-extension screen recordings, not generic B-roll. Use dark-mode browser where possible for contrast. Alternate with occasional high-quality macro B-roll of keyboard/hands to make the demo tactile.
- **Caption style:** all-caps white sans, bold condensed/Inter-like, 1–4 words per hit, centered near lower third or over the creator's torso. Black stroke/drop shadow; no big caption box. Captions appear as phrase chunks synced to speech stress: `WANT TO`, `THEN YOU`, `CALLED`, `WRITE, EDIT`, `TAB`, `THE ENTIRE`, `POST ABOUT`, `FREE`.
- **Special hook typography:** first seconds may include one larger stylized phrase overlay with mixed emphasis, e.g. white small setup words + orange/red italic serif for the pain/desire + LinkedIn/tool logo. Do not use this for every caption.
- **Colors:** warm amber talking-head environment; dark navy/black UI backgrounds; white captions; orange/red for pain or desire words; product green/purple highlights only when present in the UI.
- **Motion:** hard jump cuts every 0.5–2s; quick push-ins on UI; crop jumps from full page to relevant panel; mouse/selection/highlight actions as motion; PIP creator continues gesturing while screen changes behind.
- **Transitions:** mostly straight cuts and punch-ins. Avoid fancy wipes. Let the screen action be the transition: open extension, double-tap key, highlight text, command popup appears, result replaces paragraph.
- **Audio:** fast live/talking-head delivery or clean VO with low/no music. SFX can be subtle: keyboard tap, pop for extension panel, click for caption hits. Voice is dominant.

## Beat template for any topic/tool
| Time | Beat | Visual | Caption behavior |
|---|---|---|---|
| 0–5s | Pain + audience hook | Talking head warm desk, hands moving | 1–3 word stressed captions + one big stylized desire phrase |
| 5–10s | Tool promise | Website/extension/store page; creator PIP appears | Tool name and verbs as chunks |
| 10–16s | Use-case setup | Actual target page/document/product context | Captions name the task/problem |
| 16–24s | First action | Screen recording plus tactile keyboard shot | Caption only the trigger action/key combo |
| 24–32s | Proof result #1 | Extension reads/analyzes/generates a structured output | Caption the result category, not the whole output |
| 32–42s | Friction removed | Highlight confusing term/text; tool explains inline | Captions emphasize “right there”, “no new tab”, etc. |
| 42–52s | Magic command | Voice/text prompt popup over actual page | Keep prompt visible; caption the command verb |
| 52–63s | Rewrite/improvement | Select weak text; command popup; improved replacement | Captions mark before/after quality shift |
| 63–69s | Time saved + CTA | Return to talking head or final proof screen | Big simple CTA word: `FREE`, `COMMENT [KEYWORD]` |

## Script formula
1. `If you want [desirable outcome], but you're tired of [specific friction], you need [free/simple tool/workflow].`
2. `It lets you [verb 1], [verb 2], [verb 3] without [annoying context switch].`
3. `Let's say I want to [specific job-to-be-done].`
4. `I have [real source/page/doc] open, but [starting friction].`
5. `So I [trigger/key/action].`
6. `[Tool] reads/analyzes [source] and gives [structured result].`
7. `When I don't understand [term/problem], I [highlight/select] and it explains/fixes it right there.`
8. `Now watch this: [speak/type exact prompt].`
9. `It generates [first output]; then I improve [specific weak part] by asking for [stronger angle/style].`
10. `The whole thing took [short time]. Comment “[keyword]” and I'll send it.`

## Production pipeline
1. **Choose the concrete demo:** one workflow the viewer already wants, not a generic tour. Example: `turn competitor profile into LinkedIn post`, `turn support tickets into feature ideas`, `turn messy notes into investor update`.
2. **Write proof-first script:** every sentence should map to an on-screen action: page open, click, highlight, command, generated text, replacement.
3. **If starting from existing talking-head footage:** extract the transcript first, identify each factual claim/thesis, then build a proof-asset map before planning captions. Do not simply subtitle the talking head. Convert the middle into source/UI/diagram proof while preserving the creator as full-screen only for hook, thesis, and CTA.
4. **Record talking head:** warm desk, 4K/1080 vertical or cropped horizontal, strong eye contact, energetic gestures, slight jump cuts. Capture clean lav/USB mic audio.
5. **Record screen:** vertical-safe browser recording. Zoom browser to 125–150%; use dark mode when possible; enlarge extension popups/results; hide sensitive data.
6. **Capture tactile inserts:** 1–2 macro shots of keyboard/mouse/finger action for trigger moments.
7. **Edit assembly:** start with talking head, then alternate full-screen UI + PIP creator. Use jump cuts and crop zooms every 0.5–2s. Show actual results long enough to read the key line.
8. **Caption pass:** add only stressed phrase chunks, all-caps white with black stroke/drop shadow. Place over torso/lower third. For hook, add one larger stylized text/logo composition.
9. **Motion pass:** add subtle push-in on UI screenshots, cursor-follow crops, quick scale punches on caption hits, and small pop/click SFX for command panels.
10. **Remotion polish pass when requested:** if the user asks for the polished Remotion version, return to Remotion rather than treating an FFmpeg fallback as final. Use `OffthreadVideo` for reused full-screen/PIP footage, keep embedded video layers muted, preserve one clean audio track, and run a Remotion still-frame check before the full render.
11. **CTA:** keyword comment CTA in the final 2–4s, spoken and optionally captioned. Keep it simple: `Comment [KEYWORD] and I'll send it.`
12. **QA:** mobile contact sheet must prove captions are readable, UI text/key results visible, PIP does not cover important UI, and there is a meaningful visual change every 1–2 seconds. For Remotion renders, also run ffprobe, decode, blackdetect, and contact-sheet checks before delivery.

## Reference adaptations
- Pipeline playbook: `~/ai-video-pipeline/style-playbooks/talking-head-screen-demo-reel-pipeline.md` — reusable production spec for recreating the Arshman/Clicko talking-head + browser-proof style for any topic.
- `references/openai-finance-adaptation.md` — concrete mapping from raw OpenAI personal-finance talking-head footage into this screen-proof/PIP style, including crop notes, proof assets, caption chunks, and timestamped edit map.
- `references/remotion-polished-render-pattern.md` — session note on producing the polished Remotion version after an FFmpeg proof draft, including `OffthreadVideo`, still-frame preflight, runtime-swap communication, and final QA checks.

## Topic adaptation examples
- AI research tool: page/paper open → highlight confusing method → ask for summary → generate post/thread.
- SaaS analytics: dashboard open → ask why metric dropped → tool explains causes → drafts action plan.
- Career/job search: job post open → extension extracts requirements → rewrites resume bullet → drafts recruiter DM.
- Founder ops: customer call transcript open → extract objections → rewrite landing page section → produce follow-up email.

## Common mistakes
- Using fake B-roll or static cards instead of real screen proof.
- Making captions full subtitles; this style uses short stressed phrase chunks.
- Making the PIP too small; the face must remain emotionally legible.
- Cutting away before the generated result is readable.
- Overdesigning transitions; use real cursor/selection/product actions as the motion.
- Hooking with the tool name instead of the viewer pain/outcome.
- Showing too many features; choose one concrete workflow with 2–3 proof moments.

## Verification checklist
- [ ] Hook names audience + pain in first 5s.
- [ ] Actual product/browser footage appears by ~8–10s.
- [ ] Talking head returns or stays as PIP often enough to preserve trust.
- [ ] Every feature claim is shown with real UI action/result.
- [ ] Captions are 1–4 words, all-caps, high contrast, and synced to stressed words.
- [ ] There is a visual change every 0.5–2s.
- [ ] Final CTA uses one keyword and clear benefit.
