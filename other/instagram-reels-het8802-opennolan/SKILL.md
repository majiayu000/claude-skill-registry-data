---
name: instagram-reels
description: Use when creating, critiquing, researching, or scripting Instagram Reels, TikToks, YouTube Shorts, short-form talking-head videos, hooks, or creator-pattern analysis for AI/tech/startup content.
---

# Instagram Reels

## OpenNolan mirror rule
When the user shares Instagram algorithm, user psychology, engagement, hook, carousel, or editing lessons, store durable learning in the relevant social-media skill **and** mirror it into OpenNolan repo-local files under `~/projects/OpenNolan/skills/social-media/` so their local synced AI agent can use it. Use real Markdown/support files, not symlinks. Session-specific details belong in `references/`; class-level operating rules belong in `SKILL.md`. See `references/opennolan-social-media-mirror.md`.

## Core principle
Treat short-form as **attention engineering**, not video summarization. The first 2–5 seconds must combine a visual hook, spoken hook, and audio/SFX cue; the rest must reward the hook with useful, emotionally legible payoff.

## Source library learned from shared Instagram posts
These are distilled from posts/reels the user explicitly said to “Learn this.” Update this section whenever the user shares more legit Instagram creators/posts.

### Reusable hook families
Use these four hook families instead of rewriting from scratch:

| Family | When to use | What it should do |
|---|---|---|
| Tips/Tools | Tactical AI tools, workflows, prompt systems, startup playbooks | Create a save-worthy how-to for cold followers |
| Storytelling | Personal founder lessons, failures, experiments, credibility | Build trust and human bond |
| Mindset | Founder/operator worldview, contrarian beliefs, identity | Signal authority and attract aligned people |
| Psychological | Myth-busting, pattern interrupt, debate bait, surprising stats | Trigger attention, comments, and rewatch |

### Topic + angle before hook
Before writing hooks, validate:
1. **Topic:** What is the concrete AI/tech/startup signal?
2. **Angle:** Why should a founder/operator care today?
3. **Viewer tension:** What anxiety, opportunity, status move, or practical gain does it touch?
4. **Format:** Is this best as news teardown, tutorial, myth-bust, list, story, or checklist?

Do not open with “X launched Y” unless that phrasing itself creates tension. Convert news into founder/operator implications.

### Retention psychology / Instagram algorithm model
Use this as the operating model for future lessons the user shares about engaging Reels. Preserve new psychology/algorithm observations here or in a narrow sub-skill, not only in chat memory.

- Instagram distribution is behavior-led: prioritize watch time, completion rate, replays, shares per view, saves per view, and comment intent. Likes are weaker than retention/share signals.
- The first seconds must create an **open loop**: a surprising claim, status threat, hidden mechanism, unfinished framework, or visible transformation. The viewer should feel “I need the next beat.”
- Retention comes from **micro-payoffs** every 1–2 seconds: new proof, contradiction, visual change, numbered step, UI reveal, or pattern interrupt.
- Shares come from identity and utility: make viewers think “my founder/AI friend needs this” or “this makes me look smart/helpful.”
- Saves come from structured artifacts: checklists, frameworks, prompt stacks, workflow maps, before/after systems, exact tool chains.
- Comments come from controlled tension: contrarian but defensible claims, myth-busting, “which would you choose?”, or naming a common mistake.
- Rewatch comes from dense but legible pacing: enough information that a second watch is useful, not so much that the first watch is confusing.
- Visual attention resets should be meaningful, not random: motion should clarify the idea or advance the story.

### Engineered friction / correction-bait awareness
Learned from Tanishaa Bhansali Reel `DVxV0gqgTrf` (Mar 2026): some high-engagement Reels deliberately create **minor friction** that viewers want to correct, decode, pause, replay, or comment on. Treat this as Instagram psychology to understand and use ethically — prefer playful/transparent versions over deceptive or brand-damaging mistakes.

The 7 friction levers shown:
1. Add a small typo on purpose → viewers comment corrections.
2. Say something slightly wrong → viewers feel compelled to point it out.
3. Flash a screenshot/resource for ~0.5s → viewers pause, screenshot, or rewatch.
4. Put a random object in the background → viewers comment “what is that?”
5. Use a weird prop as the mic → instantly creates visual oddity and rewatch value.
6. Cut right before the answer/reveal → creates an unresolved loop and comments.
7. Wear something distracting/backwards/mismatched → viewers notice and point it out.

Reusable ethical adaptations for your AI/tech content:
- Use **intentional mystery props** tied to the topic (e.g., sticky note labeled “$10M bottleneck,” old keyboard, redacted roadmap) rather than fake factual errors.
- Use **pause-worthy proof flashes**: quick prompt, GitHub diff, API bill, dashboard, or checklist glimpse — then offer the full resource via CTA.
- Use **controlled near-mistakes** only when harmless and self-aware, e.g. “Did you catch the wrong assumption?” instead of mislabeling facts.
- Use **cut-before-reveal** sparingly; pay off the answer in comments/follow-up or it becomes frustrating clickbait.
- Add a final meta-question: “Which mistake did you catch?” / “Which tab would you pause on?” to convert attention into comments.

Why it works: annoyance, curiosity, correction impulse, and confusion are engagement triggers. But for your brand, use friction to increase participation and rewatch, not to erode trust.

### First 2–5 seconds: visual + spoken + SFX
Every Reel script should specify:
- **Visual hook brick:** movement, prop, A/B comparison, screen recording, crash zoom, match cut, frame collage, unusual first image, etc.
- **Spoken hook brick:** contrarian, problem, warning, secret reveal, case study, list, question, ranking, scenario.
- **Audio/SFX cue:** whoosh, bass hit, stamp, notification ping, silence, cash register, glitch, etc.

Example: `A-vs-B sticky notes + contrarian/problem + stamp SFX` → “AI assistant ❌ / Invoice chaser ✅”.

#### Second-hook SFX lesson
Learned from Tanishaa Bhansali Reel `DYqo3PbBBYN` (Jun 2026): sound effects act as a **second hook** after the visual/spoken hook. For Reels/OpenNolan edits, map common SFX to emotional function instead of sprinkling random sounds:
- `fahhhh` / fail sting = epic fail, bad output, wrong-way comparison.
- `whoosh` = zoom-in, zoom-out, swipe, transition, card travel.
- `riser` = suspense before a reveal, strong point, stat/punchline buildup.
- `pop/click` = overlay, bullet, label, UI card, cursor/tap microinteraction.
- `crickets` = awkward silence, joke pause, dead-room moment.

Timing rules: SFX should start 10–20 ms before the visual it accents; risers should end exactly on the reveal frame; comedy sounds need a short pause/hold to read; dialogue-heavy Reels should stay around one SFX every ~2 seconds. OpenNolan implementation detail is saved in `opennolan-video-production` reference `references/second-hook-sfx-reel.md`.

### Mobile safe-zone layout lesson
Learned from Bhavini Panjwani Reel `DY4p39tskeY` (Jun 2026): creators should design vertical Reels around Instagram UI/cropping safe zones, not just aesthetics. The Reel is a 15s talking-head tutorial with translucent overlays that point to where content belongs.

Reusable layout rules:
- Keep the **human face/torso and primary action** inside a tall central safe zone. This is where the viewer’s eye should rest and where camera zoom-in/zoom-out can happen without cutting off the subject.
- Put the **main hook text** in the upper-middle/upper-third, not at the extreme top. Leave space above for platform chrome and avoid burying the hook under profile/audio UI.
- Put **captions/subtitles** in a lower-middle band above the bottom UI stack, not at the very bottom. Avoid placing key words where comments/caption/share buttons overlap.
- Avoid the side rails and bottom corners for important information: the right rail competes with like/comment/share buttons; the left/lower areas compete with profile/caption/audio overlays; bottom UI can hide CTAs.
- Leave extra breathing room if the edit uses digital zooms, because zooming magnifies edge/cropping mistakes.

Reusable explainer format:
- Use color-coded overlays (`green = safe`, `yellow/teal = hook/caption bands`, `red = avoid`) directly on the footage.
- Narration can be extremely simple: “this is your safe zone / this is where the hook goes / this is where captions go / don’t put anything here.” The value comes from visual clarity, not clever copy.
- Pace one spatial rule every 2–3 seconds; pair each rule with a pointing gesture, dotted arrow, or rectangle highlight so it is instantly screenshot-worthy.
- Use this checklist before exporting your Reels/OpenNolan/Remotion videos: face/subject safe, hook readable in upper-middle, subtitles above bottom UI, no key text in side rails, CTA not hidden by buttons.

### Greg Isenberg / Roberto Nickson short-form production system
Learned from Greg Isenberg's public Roberto Nickson masterclass and X thread (Oct 2025): the polished "programmatic" look is mostly a **templated assembly line**, not a magic one-click generator. Reusable rules:
- Script first for tension: line 1 hooks; line 2 introduces conflict; then alternate context/conflict.
- Record quickly with teleprompter; do not over-optimize the take.
- Edit like dopamine engineering: something changes every few seconds—jump cut, caption hit, pattern interrupt, screen-recording move, generated B-roll, SFX.
- Use contextual generated visuals instead of generic stock when possible. Publicly cited stack includes Apple Notes, Prompter Pro, OBS, Screen Studio, Downie, optimized Premiere workflow, Nano Banana, Kling, Sora 2; Greg has also cited ChatGPT + Veo/CapCut/Final Cut and Remotion-inside-Codex in related posts.
- Key implementation lesson: Remotion/FFmpeg should be used as a deterministic assembler around a strong design system, shot vocabulary, captions, B-roll, and sound design—not as a blank React canvas that invents taste on demand.

#### Greg-style Remotion implementation
Use this when the user asks for Greg Isenberg-like Instagram Reels, Hyperagent-style AI product reels, or clean editorial programmatic videos.

**Canonical local assets and demo:**
- Asset kit root: `~/greg-style-kit`
- Zip archive: `~/greg-style-kit.zip`
- Asset preview: `~/greg-style-kit/previews/asset-preview.png`
- Asset ledger: `~/greg-style-kit/asset-ledger.json`
- Working demo Remotion project: `~/greg-style-demo`
- Final 10s demo: `~/greg-style-demo/greg-style-demo-10s-final.mp4`
- Demo source: `~/greg-style-demo/src/Composition.tsx`, `Root.tsx`, `index.css`
- Demo QA contact sheet: `~/greg-style-demo/contact-sheet-final.jpg`

**Existing reusable assets:**
- Fonts: `~/greg-style-kit/fonts/Fraunces/` and `~/greg-style-kit/fonts/Inter/` from Google Fonts OFL. Use Fraunces or Georgia-like serif for editorial hooks; Inter/DM Sans-like sans for UI labels.
- Palette: `~/greg-style-kit/palettes/greg-editorial.json`.
- Backgrounds: `~/greg-style-kit/backgrounds/warm-paper.png`, `subtle-noise.png`, `mint-gradient.png`.
- Icons: `~/greg-style-kit/icons/robot-agent.svg`, `document.svg`, `checklist.svg`, `map-pin.svg`, `browser.svg`, `dollar.svg`, `cursor.svg`.
- Shapes: `~/greg-style-kit/shapes/dashed-container.svg`, `pill-label.svg`, `rounded-node.svg`, `progress-bar.svg`.
- SFX placeholders: `~/greg-style-kit/sfx/soft-pop.wav`, `whoosh.wav`, `click.wav`, `riser.wav`. Replace with ElevenLabs/generated SFX when keys exist.
- Starter components: `~/greg-style-kit/templates/*.tsx` (`workflow-diagram`, `multi-agent-map`, `truth-card`, `ai-output-card`, `talking-head-quote`, etc.).

**Asset provenance / how the first kit was created:**
- Background PNGs were generated locally: warm paper base, subtle noise overlay, mint gradient.
- SVG icons/shapes were drawn as original simple vector primitives using the Greg-style palette; do not copy Greg's actual thumbnails/assets.
- Fonts are open Google Fonts. The Fraunces + Inter pairing recreates the editorial serif + clean product UI contrast.
- SFX were simple local synthesized placeholders because `ELEVENLABS_API_KEY` / `XI_API_KEY` was missing.
- The 10s demo was built in Remotion at 1080×1920, 30fps, 300 frames, then verified with `npm run lint`, `ffprobe`, `ffmpeg -f null`, black-frame detection, and contact-sheet visual QA.

**Design schema / visual grammar:**
- Canvas: vertical 9:16, 1080×1920, off-white warm paper. Avoid black/cyberpunk unless the script explicitly needs contrast.
- Core colors from `greg-editorial.json`: `paper #F5EFE6`, `paperWarm #F7EDE7`, `mint #9FD8B5`, `mintStrong #68B894`, `teal #4FAE91`, `forest #173D35`, `forestDeep #0E2B25`, `coral #D96D5F`, `gold #F4C84A`, `mauve #B98BB8`, `charcoal #111111`, `gray #898984`, `whiteWarm #FFF8EC`.
- Color semantics: forest = authority/text; mint/teal = AI/product/building; coral = failure/rejection/warning, use rarely; gold = save/payoff/badge; mauve = secondary UI border/shadow.
- Typography: oversized Fraunces/serif hooks with tight line height (0.9–0.96) and negative letter spacing; Inter/sans for pills, labels, UI nodes, captions.
- Layout: large headline in upper-left; 72–90px safe margins; secondary UI object lower-right; avoid center-stacking everything. Preserve negative space.
- Motifs: rounded product cards, pill labels, dashboard/browser frames, dashed connector paths, workflow nodes, small agent mascots, cursor movement, progress bars, checklist bars.
- Motion grammar: soft spring pop on node reveal; dashed connector draw-on; micro push-in on each scene; caption phrase pop; cards slide 40–70px then settle; dashboard scan/cursor pass; final checklist stagger.
- Transitions: prefer quick 4–8 frame fades/wipes or object-driven transitions. Avoid long crossfades that create ghosted unreadable frames. Always contact-sheet QA.

**When creating new assets from scratch:**
- Use existing SVGs/shapes for generic UI metaphors; create new simple SVGs only when the concept is abstract/systemic (agent, workflow, checklist, database, money, browser, map).
- For specific topical images inside the reel—founder portrait style, product scene, unusual metaphor, B-roll still, cinematic object, company/product illustration—prefer **Codex CLI with native `$imagegen` / image-generation capability** to create AI-generated images, then use Remotion as the assembler. Do not default to hand-coded placeholder art for these topical assets.
- For storyboards or “help me visualize the whole video” deliverables, do **not** default to a PIL/HTML/programmatic contact sheet as the final visual unless the user asks for deterministic wireframes. Create a text beat sheet if useful, then use native `$imagegen` to produce a polished AI-generated storyboard/contact sheet in the editorial AI-product style.
- Store generated topical assets under the project, e.g. `~/<reel-project>/public/generated/` with descriptive names and a small `asset-ledger.json` recording prompt, source, and usage.
- Treat text embedded in AI-generated images as decorative/background unless it is clearly legible after mobile QA; add primary readable text as Remotion overlays.
- Keep copyrighted/reference material out of the final. Use Greg/other creators as style references only; recreate schema, not assets.

**Remotion build pattern:**
1. Scaffold or reuse a project: `npx create-video@latest --yes --blank --no-tailwind <project>` then `npm i`.
2. Copy or symlink `~/greg-style-kit` into `public/greg-style-kit`.
3. Register a 1080×1920, 30fps composition. For 10s: `durationInFrames={300}`.
4. Load fonts in CSS from `../public/greg-style-kit/fonts/...`.
5. Build scenes as deterministic components: background, headline card, workflow map, dashboard mock, proof frame, final checklist.
6. Use `spring()` and `interpolate()` with clamped ranges. Keep transitions short and test frame timing.
7. If scene components use absolute frame gates (`sceneOpacity(f, start, end)`), do **not** wrap them in `<Sequence from={...}>` unless you normalize the child frame; Remotion shifts `useCurrentFrame()` inside sequences and can produce blank/empty scenes. Either render absolute-timed scenes directly or make each scene timeline local.
8. Render stills first (`npx remotion still <Comp> --frame=<n> --scale=0.25`) before full MP4, including at least one mid/late scene to catch timing bugs.
9. Render MP4 with h264 (`npx remotion render <Comp> out.mp4 --codec=h264 --crf=18`).
10. Verify: `npm run lint`; `ffprobe`; `ffmpeg -v error -i out.mp4 -f null -`; blackdetect; create a contact sheet and visually inspect.
11. Reference implementation for turning a daily AI/tech script into a 27s Greg-style informational Reel: `references/openai-credits-greg-remotion-reel.md`.
12. Reference implementation for turning a source Reel + drafted script into a 49s Greg-style OpenAI Ads Manager Reel with VO, scene structure, project path, and QA commands: `references/openai-ads-greg-remotion-reel.md`.

**Captivation / retention overlay:**
- Every 1–2 seconds, something meaningful must change: headline state, card reveal, connector draw, dashboard fill, cursor pass, caption hit, visual proof, or SFX.
- Each visual beat should answer “why should I keep watching?” not just decorate the script.
- Use the expectation-vs-reality loop: set an obvious expectation, then beat it with a non-obvious mechanism, example, or contradiction.
- Make visuals save-worthy: frameworks, checklist, workflow maps, before/after, dashboard proof, exact steps.
- Add contrast beats: warm calm design + one coral/red “failure” or “wrong way” moment increases emotional legibility.
- If using voiceover later, align visual reveals to sentence turns, not arbitrary seconds.
- For Greg-style programmatic reels with VO, do not narrate every on-screen word. Rewrite to a tight creator-native VO, choose an energetic social voice, process the VO to video length, then mux with the Remotion export. See `references/openai-credits-greg-remotion-reel.md` for the ElevenLabs timing/muxing pattern and the `-shortest` early-audio pitfall.

### Source-backed evidence montage Reel
Learned from 100xEngineers Reel `DYhssDhN-ti` (May 2026): use `source-backed-reel-evidence-montage` when a Reel needs narration tightly supported by source screenshots, highlighted article text, product clips, terminal/code proof, official notes, and talking-head authority. Core lesson: every factual phrase should map to a visible proof asset; article screenshots should show source context first, then crop/highlight the exact supporting words.

### “Same tool, better setup” AI-design skills Reel
Learned from Nate Herk Reel `DYU6TXpDxtt` / TikTok `7639793885929164045` (May 2026): “Stop making boring designs with Claude Code. Master these 3 skills!”

Reusable hook + structure:
- Hook: “If your Claude Code designs look average, it’s not Claude. It’s your setup.” This reframes blame from model capability to operator setup.
- Structure: numbered skill list (`#1`, `#2`, `#3`) + talking head + fast design-reference cuts + visible proof of polished websites/UI examples.
- Retention device: each skill names a concrete missing capability, then shows visual proof immediately.
- CTA/positioning: “Same tool, completely different output” — sell the setup/system, not a new model.

The three actual skills are saved in `claude-code-design-skills`:
1. Emil Kowalski design = motion/easing/microinteractions so UI feels alive.
2. Impeccable design = layout/spacing/typography cleanup in one design-polish pass.
3. Taste Skill = real design references so AI stops generating generic websites.

Use this pattern for AI/tooling content when the lesson is: the tool is not enough; the workflow/context/reference system creates the quality gap.

#### InsiderForce kinetic whiteboard caption style
Learned from InsiderForce Reel `DYxBWLIHFM5` (May 2026), “Three Claude Code skills that make you look like a designer overnight.” Use when you want a clean faceless AI/design Reel where text, VO, and product mockups carry the whole video.

Reusable visual grammar:
- Background: matte off-white/very light gray with faint grid/texture, subtle watermark, and soft drop shadows. Use sparse decorative brand props (red starburst/sun icon, grayscale 3D hand/object, key, black circular logo badge) as parallax/background accents.
- Typography: bold black condensed/geometric sans for key nouns; light gray trailing words for unrevealed/secondary caption text. Use all-caps for section titles and emphasized payoff words.
- Caption motion: each voiceover clause appears as kinetic typography. The current word/phrase snaps or slides into high-contrast black while nearby unfinished words are gray/blurred. Important phrases get a short black pill/highlight or enlarged stacked words (`HUMAN DESIGNER`, `AESTHETIC OPINION`, `/polish`, `FOLLOWERS`).
- Layout: keep generous negative space; anchor text center/top-left depending on beat; pair explanatory bullets on one side with a floating phone/UI card on the other. Cards float with 3D-ish shadows and small scale/position changes.
- Transition language: quick blur/zoom wipes between sections; vertical card swipes; object-driven slides; no talking head required. Motion should feel like a clean animated presentation deck rather than stock B-roll.
- Beat structure: hook title builds word-by-word → numbered skill card → problem list → solution/payoff phrase → repeat for 3 skills → keyword CTA/product mockup → follow-gate ending.
- Replication note: in Remotion/HyperFrames, implement text as tokenized timed spans with per-token opacity/translate/blur, not ordinary subtitles. Align each phrase reveal to VO word timings; add micro SFX/pop/whoosh on section titles, bullets, and card entrances.
- Smoothing technique learned from the first OpenNolan/HyperFrames replica: avoid meme-like `0.09s` scale yoyo pops, large `translateY`, heavy blur, and `back.out` card overshoot. Use a premium soft-settle instead: reveal key words over roughly `0.28–0.36s`, begin `0.06–0.10s` before spoken stress, limit initial y motion to `12–18px`, blur to `2–3px`, scale payoff text only to `1.03–1.04`, then settle to `1.0` over `0.18–0.25s`; start floating-card ambient drift only after entrance animations settle.
- OpenNolan implementation note: when the user asks to turn this into an OpenNolan reusable style, create both a Layer 2 creative skill and a YAML style playbook, validate the style schema, and update OpenNolan's skill index. When they ask for the actual video, use the HyperFrames production run/pitfall checklist in `references/opennolan-kinetic-whiteboard-captions.md` before rendering and delivering the MP4 + QA contact sheet. Pay special attention to the smoother-motion pitfall: avoid abrupt yoyo pops and bouncy proof-card entrances; use slower soft-settle word/payoff reveals and delayed ambient drift for the premium whiteboard vibe.

Why it works:
- The viewer gets a readable “animated notes” version of the voiceover, but only the key words dominate, so it avoids subtitle fatigue.
- Every 0.5–1.5 seconds something changes: word reveal, bullet addition, phone/card movement, blur wipe, or title reset.
- The white background and repeated brand props create continuity while UI mockups provide proof and topic specificity.

#### Talking-head screen demo Reel style
Learned from Arshman Khalid Reel `DY6UXkINLri` / Clicko Chrome-extension demo (May 2026): use `talking-head-screen-demo-reel` when you want a Reel where the creator talks to camera while actual browser/product footage runs behind them, with creator PIP, dark UI proof, tactile keyboard inserts, short all-caps phrase captions, and a comment-keyword CTA.

### Pixel RPG product explainer style
Learned from Reel `DY5SPASumP8` (May 2026): use when you want an OpenNolan/HyperFrames/Remotion AI-tool tutorial that feels like a playable mini-world rather than a plain SaaS explainer. Full session reference: `references/dy5spas-pixel-rpg-product-explainer.md`.

Reusable visual grammar:
- Hook with a top-down pixel/RPG world-state: avatar, old computer/tool node, purple crystal/quest object, beige tile/off-white map, and threat labels (`Layoffs`, `Automation`, `Budget Cuts`, `Competition`) radiating from a cracked portal.
- Turn proof into layered desktop windows: browser/news/report cards slide in from different edges, overlap with soft shadows, and highlight only one phrase per card.
- Teach with a level system: `There are 3 levels` → connection diagram → trend map → prompt/result loop → checklist/plan/proof board.
- Use editorial serif kinetic captions as phrase collages, not bottom subtitles. Key nouns get mint/purple/coral color hits and tiny scale emphasis; setup words stay smaller/black/italic.
- Prompt bars are hero UI objects: black rounded pill, green rim glow, app icons, typed prompt text, result card above.
- Transform AI output into tangible artifacts: 7-day checklist, 30-day plan, post grid, profile/proof board. The final payoff should be proof-of-work/identity, not a generic CTA.
- Motion vocabulary: `rpg-walk`, `portal-crack`, `desktop-window-stack`, `phrase-collage-build`, `keyword-color-hit`, `dotted-connector-draw`, `radial-tag-populate`, `prompt-bar-type`, `response-to-artifact`, `proof-grid-land`.
- OpenNolan implementation created from this session: `skills/creative/pixel-rpg-product-explainer.md` and `styles/pixel-rpg-product-explainer.yaml` in the OpenNolan repo; validate with the style schema and `load_playbook('pixel-rpg-product-explainer')` before use.

Why it works:
- It makes an abstract AI workflow feel spatial and game-like: connect, prompt, retrieve, plan, publish.
- It alternates light map/caption scenes with dark UI/proof scenes for attention resets.
- It preserves utility: product screenshots and generated artifacts prove the workflow instead of decorating it.

### Visual hierarchy “fix this edit” tutorial Reel
Learned from Aevy Video School Reels `DZHvGrfSQ4t` and `DZNSZJ0TTb9` (Jun 2026), caption/title “This is how we will fix this edit”: design/editing tutorials become more compelling when they are framed as a **visible repair arc**, not abstract advice.

Reusable structure:
- Hook with a viewer comment bubble asking the exact question (`How exactly would you fix this?`) while the creator talks to camera. The comment supplies social proof and a clean problem statement.
- Isolate the bad edit as a simplified canvas/wireframe/silhouette so the flaw is obvious before teaching.
- Start with the **actual flaw**, not a generic principle. In `DZNSZJ0TTb9`, the bad mental-health survey map fails because it mixes generic teal gradient, weak/hidden title hierarchy, random yellow doodles, poorly connected stat callout, and decorative avatars that do not reinforce the data story.
- Flash quick “principle receipts” such as typography anatomy, design-principle cards, color-palette references, moodboards/Midjourney prompts, or the actual editing timeline/waveform; circle one detail only.
- Rebuild the frame one layer at a time: hero geography/object first, title/date second, stat/data callout third, emotional/supporting asset fourth, background texture/shape last. The core lesson is: **motion cannot rescue unclear hierarchy**.
- Use a **controlled palette** derived from the topic instead of random bright colors. For sensitive/serious content, a darker grounded background plus warm highlight color can feel more credible than default social-media neon.
- Treat data visuals as a story system: title establishes subject/context, date establishes source/time, map/shape anchors location, percentage/stat gets one clear focal treatment, supporting illustration/avatars add emotion only after the core hierarchy reads.
- Use hand-drawn yellow/blue circles, top-right creator PIP, snap cuts, punch-ins, and final poster reveal.
- Final visual languages observed: (1) bright green background, deep blue curved blob, royal-blue bold text, grayscale cutout people/objects, strong scale contrast; (2) dark teal/yellow India map, small white survey title/date, soft texture/starburst accents, blurred/spotlight data callout, warm illustrated faces for emotional context.

OpenNolan implementation created in the OpenNolan repo: `skills/creative/visual-hierarchy-edit-fix.md` and `styles/visual-hierarchy-edit-fix.yaml`. Detailed notes are in `opennolan-video-production` reference `references/aevy-visual-hierarchy-edit-fix-reel.md`.

### Expression-to-effect visual dictionary Reel
Learned from Aevy Video School Reel `DW8cy5gS1Qh` (Apr 2026), caption “Stop keyframing everything”: technical tutorials can become highly save-worthy when each beat shows the **motion outcome first**, then reveals the exact expression/formula as a large bracketed label.

Reusable structure:
- Hook: “Stop doing the manual/basic version.” Show the boring workflow or keyframed result first.
- Repeat 5 mini-lessons: desired effect → playful visual demo → bracketed command/formula label → tiny “apply to X” usage line.
- Use memorable visual metaphors instead of generic UI: offset object grid, pendulum swing, stop-motion walker, floating pixel blocks, neon flicker.
- Text hierarchy: oversized tan/brown italic bracket label (`[ Wiggle ]`) > formula > small target line > minimal bottom subtitles.
- CTA: show real destination proof (profile/community/resource screen) with a red highlight around the join/link target.

OpenNolan implementation detail is saved in `opennolan-video-production` reference `references/after-effects-expression-cheatsheet-reel.md`.

### Hook/content fit matrix
Learned from Chase Dimond / @chasehunterdimond IG post `DZJWCnBzhbf` (Jun 2026): the fastest way to improve hooks is to **match the hook psychology to the content type**, not reuse one generic hook style.

Reusable matrix:
- Educational/tutorial posts need **curiosity + a useful learning promise**. Use shells like “Here’s how to...” / “Let me save you hours...” and show a checklist, workflow map, prompt/result card, or screen proof immediately.
- Storytelling posts need **emotion and personal stakes**. Use shells like “I learned this the hard way...” and show a face/reaction, before-after, personal artifact, or timeline.
- Contrarian/myth-busting posts need **tension**. Use shells like “You may not agree with this...” / “Everyone says X, but...” and show expectation-vs-reality, A/B cards, red X/green check, or a debate prompt.
- Authority/proof posts need **evidence-first credibility**. Use shells like “I tested this...” / “Here’s the proof...” and open with receipts, dashboards, source screenshots, metrics, or result montages.

Treat hook/content mismatch as a retention bug: a proof-heavy post opened with vague curiosity feels weak; a personal story opened with generic “how-to” copy feels emotionally flat. OpenNolan copy of this lesson is saved at `~/projects/OpenNolan/skills/creative/references/hook-content-fit-matrix-dzjwcnbzhbf.md` and wired into `skills/creative/short-form.md`.

### Low-friction “hooks that always work” phrase bank
Learned from Richard Ens Jr / @richardensjr Reel `DWzni9xEcxL` (Apr 6, 2026): the Reel is a simple save-bait list with creator holding up 10 fingers + cover text “10 hooks that always work,” then one hook phrase per beat. Use these as **opening phrase shells**, not final scripts; adapt them to AI/tech/founder stakes with a concrete payoff in the next line.

Reinforced by a shared Claude prompt carousel / slide 3: when a morning script hook feels flat, run a **5-angle hook rewrite pass** before finalizing. Rewrite the same core idea as: (1) bold claim, (2) personal confession/experiment, (3) surprising stat or quantified shift, (4) direct question, and (5) “you’ve been doing X wrong” correction. Pick the version with the clearest founder/operator tension, then make the next line immediately prove it so it does not feel like clickbait. Session detail and retrieval fallback: `references/claude-content-prompts-dyeb85.md`.

Reinforced by a shared hook-library carousel (May 2026): package hooks as a **hook library / swipe file** with a keyword CTA (“Comment HOOKS”) and a cover promise like “10 hooks that stop the scroll.” For Reels, this means hook posts should feel like a stealable asset, not generic advice: one hook shell per beat, each immediately adapted to your niche.

The 10 reusable phrase shells:
1. “Nobody mentions this.”
2. “I wish I knew this earlier.”
3. “Pause for a second.”
4. “Ever notice this pattern?”
5. “Here’s the real truth.”
6. “Let me save you hours.”
7. “This may surprise you.”
8. “You need this now.”
9. “You may not agree with this.”
10. “I just figured this out.”

Why this works:
- Each shell creates a micro open-loop: hidden info, regret, interruption, pattern recognition, truth reveal, time-saving, surprise, urgency, disagreement, or fresh discovery.
- The list format is inherently save-worthy and lets the viewer quickly map each phrase to their own niche.
- The phrase alone is not enough; immediately follow with specificity: `Nobody mentions this: the best AI agent businesses are not selling agents — they are selling recovered time in one painful workflow.`
- Best use: convert generic creator hooks into founder/operator versions by adding a concrete audience, pain, time horizon, or workflow.

### Platform-role matrix Reel: “Reels bring in, carousels teach, stories convert”
Learned from Aayush Swamy / @iamaayushswamy Reel `DWUCCNVjCYT` (Mar 25, 2026): a strong educational Reel can be a **role matrix** comparing 3 content formats against audience stage, objective, cadence, and content examples.

Reusable framework:
- Hook/central thesis: `Stories = followers + connection + leads`, `Carousels = engagement + education + saves/shares`, `Reels = non-followers + reach + education/storytelling + authority`.
- Use a persistent top header with the three categories (`STORY / CAROUSEL / REELS`) and highlight the active category in a contrast color on every beat. This reduces cognitive load while allowing fast pacing.
- Pair every claim with proof overlays: analytics screenshots, audience breakdowns, link clicks, saves/shares, story interactions, or post examples. The proof makes generic content-strategy advice feel earned.
- Beat order that worked: audience reached → business objective → trust/education role → posting cadence → concrete content examples.
- Suggested cadence from the Reel: Stories 2–3/day; carousels 2–3/week; Reels 3–6/week depending on style.
- Example ending taxonomy: Stories = personal life, client results, testimonials; Carousels = screenshotable guides/lists + client results; Reels = educational + storytelling content.

Adaptation for your AI/tech/startup content:
- Reels: bring in cold founders/operators with story/news teardowns and useful AI workflow demos.
- Carousels: package the exact frameworks/checklists/prompt stacks people save and share.
- Stories: build trust with behind-the-scenes experiments, proof, polls, offers, and direct CTAs.
- For any “which channel/content type/tool should I use?” topic, use this matrix pattern: same persistent header, active highlight, metric/proof card, then concrete cadence/examples.

### Expectation vs reality storytelling loop
Learned from Kallaway / @kallawaymarketing Reel `DYkGzaYMdkC` (May 20, 2026): retention comes from repeatedly beating the viewer's expectation.

Use this loop inside scripts:
1. **Anchor expectation:** say something clear enough that the viewer can guess what is coming next.
2. **Beat expectation:** deliver a reality that is more interesting, shocking, contrarian, specific, or useful than the obvious guess.
3. **Repeat:** each beat should reset a new expectation, then exceed it again until the story/payoff completes.

Practical writing rule: if the next line is merely what the viewer already expects, rewrite it into a non-obvious mechanism, number, example, or contradiction.

AI/tech examples:
- Expected: “AI agents save time.” → Better reality: “The real win is not speed; it is turning forgotten follow-ups into automatic revenue recovery.”
- Expected: “OpenAI launched a new model.” → Better reality: “The model update matters less than the new workflow it unlocks for one-person SaaS teams.”
- Expected: “Use this AI tool.” → Better reality: “Use it only for the ugly middle step humans skip: turning messy notes into buyer-ready proof.”

Reusable thumbnail/cover pattern from the same Reel: `How to make BETTER [outcome]` + episode number + collage of proof/examples + visible transformation metric (`10K → 1.2M`) + human teacher frame. Use for recurring educational series like “How to make BETTER HOOKS ep 3” or “How to make BETTER AI DEMOS ep 2”.

### One-of-one positioning matrix Reel
Learned from Kallaway / @kallawaymarketing Reel `DY-F7HluecL` (Jun 2026), “5 ways to position your personal brand to survive the AI era.” Use when the user asks for creator-positioning, category-design, personal-brand, or “AI era differentiation” content.

Reusable content framework:
- Core thesis: in the AI era, generic creators/tools get commoditized; survival comes from **one-of-one positioning**. You do not need to win every dimension — aim to be top 3 in one bucket inside your niche.
- Five positioning buckets: `Premium visual experience` (watching feels better than everyone else), `Originality` (ideas are consistently differentiated), `Tactical usefulness` (viewers can implement and get promised results), `Rarity` (uncommon combination of skills/experiences), and `Aura` (likability/charisma/identity pull).
- Use named examples per bucket to make abstract strategy concrete: Roberto/RPF for premium tech visual packaging, Naval/Balaji for startup originality, Hormozi for tactical usefulness, Donald Glover for rarity, and a charismatic creator/operator for aura.
- Script move: define one bucket in one sentence → ask “who comes to mind?” → show example/proof → return to the matrix and light up the next bucket. This gives a repeatable loop without feeling like a plain listicle.
- Ending: reduce pressure by saying the viewer only needs one bucket, then offer a worksheet/diagnostic CTA (`Comment BRAND`) that turns the framework into a lead magnet.

Reusable visual grammar:
- Dark studio talking-head base with large creator frame, plus mini PIP of the speaker during graphic/proof scenes.
- Persistent branded header (`PERSONAL BRANDING`) and subtitle; a white/red glowing path-map with `Step 01`–`Step 05` acts as the spatial framework. Each bucket lights up red as the narration reaches it.
- Alternate dark matrix scenes with bright white proof-card scenes: vertical phone/post mockups, creator examples, screenshots, pyramids, worksheet preview. This contrast resets attention every few seconds.
- Typography: red all-caps labels for section/category names, white body labels, occasional editorial serif italic for bucket names/examples. Keep subtitles short and centered near bottom, not full sentence captions.
- Motion: path draw-on, glowing node activation, card float/slide, quick cut back to talking head for authority, then proof overlay. Avoid random B-roll; every visual either anchors the framework or proves one bucket.

Adaptation for your AI/tech/startup content:
- Use this to help founders/operators choose their distribution moat: e.g. `premium AI product demos`, `original AI-market theses`, `tactical workflow breakdowns`, `rare SWE+cloud+AI+founder combo`, or `builder aura`.
- Good hook shell: “If your AI content sounds like everyone else’s, pick one of these five moats.”
- Make the CTA a diagnostic asset: “Comment BRAND for the positioning worksheet” / “DM MOAT for the AI-builder positioning map.”

### Dopamine Ladder retention framework
Learned from Kallaway / @kallawaymarketing Reel `DY4l4A5u4UG` (May 28, 2026) and extended by Kallaway YouTube video `jtmstMt4WLc`, “How to Become a Storytelling Genius (Dopamine Ladders)” (22:25, Nov 20 2025): treat high-retention content as a **ladder of dopamine states**, not just a hook plus information. The six rungs are `Stimulation → Captivation → Anticipation → Validation → Affection → Revelation`.

Core loop: `question → anticipation → answer → new question`. Great Reels repeatedly open a curiosity gap, delay the answer just enough, then pay it off with a non-obvious answer before opening the next gap.

Reusable writing model:
1. **Stimulation:** create a “visual stun gun” in the first 1–2 seconds — color, motion, brightness, contrast, attractive/expressive face, shocking visual, or unusual composition. This earns the stop before conscious comprehension; the long-form video frames it as bottom-up visual processing in roughly 200ms. Use a recognizable visual identity/palette/motion style, because copied visual patterns desensitize viewers.
2. **Captivation:** immediately implant an open question the viewer wants answered. Diagnose weak hooks by asking whether the question is (a) interesting/non-obvious enough and (b) relevant to the ideal viewer. A big question fails if the audience does not care; a relevant question fails if it is too obvious.
3. **Anticipation:** do not answer too quickly. Keep the viewer guessing by showing clues, partial frameworks, escalating levels, examples, misdirection/head fakes, or near-payoff proof. Anticipation is strongest when the viewer feels close to figuring it out; irrelevant complexity breaks the loop.
4. **Validation:** close the loop with a satisfying, non-obvious answer. For educational AI/tech content, validation is the practical insight, mechanism, or workflow the viewer can use. Do not leave major loops open; it creates frustration and lowers trust.
5. **Affection:** repeated good videos make the viewer like/trust the creator/messenger, not just the individual topic. Build affection with consistent POV, face, voice, taste, energy, smiles/passion, polished vibe, and repeatedly solving the viewer’s real problems.
6. **Revelation:** the highest rung is when the creator’s face/name itself becomes the hook — a Pavlovian expectation of value before the viewer watches. This comes from consistently hitting the first four rungs across many videos. First four rungs optimize the message/video; last two optimize the messenger/creator brand.

Visual structure to reuse:
- Alternate talking-head authority shots with clean explanatory graphics every few seconds.
- Use a persistent metaphor graphic — here, a red ladder with labeled rungs — so the framework feels concrete and save-worthy.
- Use white educational slides for examples/proof and dark talking-head shots for intimacy/authority; the contrast acts as an attention reset.
- Emphasize key phrases as bold all-caps labels in red/black blocks: `VISUAL STUN GUN`, `Ask interesting QUESTION`, `Give Non-Obvious ANSWER`.
- Show examples as small phone/post screenshots with arrows and labels; proof beats should appear immediately after each abstract claim.
- End with a keyword CTA that promises the deeper asset: `Comment “Dopamine” to get full video`.

Adaptation for your AI/tech/startup content:
- Use this framework for educational meta-content, AI workflow breakdowns, and creator/business strategy videos.
- Example AI Reel ladder: stimulation = unusual AI output/UI collapse; captivation = “why do most AI demos feel fake?”; anticipation = reveal 3 demo layers; validation = “the problem is not the model, it is missing workflow proof”; affection = your recurring builder/operator POV; revelation = a repeated “the hidden system behind AI products” series.
- Before publishing, ask: what is the stun gun, what is the open question, how long do we delay the answer, and is the answer genuinely non-obvious?

## Script shape for AI/tech/startup videos
1. **Hook:** compressed, tension-first line. Avoid generic AI hype.
2. **Pattern:** what the news/signal reveals.
3. **Proof:** 1–3 source-backed facts; avoid overclaiming.
4. **Founder lesson:** convert to product, career, or opportunity insight.
5. **Concrete examples:** names, workflows, numbers, before/after.
6. **Takeaway/CTA:** ask for a checklist, comment keyword, or save-worthy follow-up.

## Notion storage workflow for one-off and scheduled scripts
When the user asks for a one-off Reel/TikTok/Short script from an Instagram video/post, or when a scheduled Instagram AI/Tech Script Engine job creates a daily talking script, write the script locally first, then store it in Notion when access is available:
1. Target hub: Notion page `Content Ideas`.
2. Date grouping: find or create a real child page under `Content Ideas` named exactly today's date in your local timezone in `MM/DD/YYYY` format, e.g. `06/02/2026`. Do not use the older `Individual ideas` toggle or `Weeks` for one-off or daily scripts unless the user explicitly asks.
3. Create a real child page inside that date page named exactly `{topic} - {YYYY-MM-DD}` using the current date unless the user specifies another date. Do not use `link_to_page`/linked-page blocks.
4. Put the full script inside that page, including topic/angle, visual hook, spoken script, on-screen text, shot list, caption, source links, and any `Asset/B-roll brief for follow-up cron` section.
5. Verify the Notion write by fetching/confirming the created daily page and script page ID/URL before claiming success.
6. If Notion access is blocked, keep the local markdown deliverable and clearly tell the user `Notion storage blocked` with the exact blocker (for example integration auth, invalid Notion API token, missing `Content Ideas`, or page-creation failure). Do not silently skip storage and do not imply the script was saved in Notion.
7. For exact Notion API implementation details for the daily-page structure, consult the `productivity/notion` support file `references/content-ideas-toggle-pages.md`.

## Quality bar
- Optimize zero-follower posts for **watch time + shares/view**.
- Use plain language with founder/operator stakes.
- Prefer specific workflows over generic categories.
- Make the hook visually filmable, not just text overlay.
- Supporting visuals should avoid generic robot imagery; use UI mockups, workflows, diagrams, props, product teardown visuals, or a deliberate mascot system.
- For Greg Isenberg/Hyperagent-style warm editorial product motion design — off-white canvas, green/red/mauve semantic palette, serif + sans typography, stylized UI mockups, agent mascots, workflow diagrams — load `editorial-ai-product-design-system`.
- For TRIBE v2 / social-signal model analysis, distinguish **real hosted/API inference** from heuristic critique; never report model scores unless the model actually ran. See `references/tribev2-video-analysis.md` for Replicate and Hugging Face pitfalls.

## Common mistakes
- Starting with brand/news recap instead of viewer tension.
- Writing only spoken hooks and forgetting visual/SFX hooks.
- Using template-sounding “AI just changed forever” language.
- Treating every AI update as hype instead of extracting a usable founder lesson.
- Saving new Instagram lessons only in memory. Update this skill, or create a narrower skill if the lesson is a distinct reusable system.

## Evolving this skill
When the user shares a new Instagram Reel/post and says “learn this”:
1. Use `social-link-summarization` or browser/web extraction to capture public metadata, caption, preview image, and any accessible transcript/visual pattern.
2. If Instagram blocks normal scraping or only shows a login shell, use the fallback in `references/instagram-reel-learning-workflow.md`: `yt-dlp` metadata, manual format URL download if needed, FFmpeg contact sheet, local `faster_whisper` transcript, then pattern extraction.
3. Do not trust a generic local-video analysis response that says it cannot access the video; verify with frames/contact sheet plus transcript.
4. If a Reel/video is downloaded locally for analysis, extract the reusable pattern, patch the relevant skill, then delete the downloaded MP4/images/metadata artifacts unless the user explicitly asks to keep them. Do not let temporary Instagram media accumulate on disk.
5. If it improves Reels/hooks/scripts, patch this skill with a concise new rule or source-library note.
6. If it is about carousels, update `instagram-carousel` instead.
7. If it is a separate domain system, create a new skill and cross-reference it here.
8. Keep persistent memory minimal: store only a pointer/preference if necessary, not the full lesson.
9. If the lesson is about Instagram algorithm, user psychology, engagement, hooks, editing, or OpenNolan production, also mirror the relevant social-media skill files into `~/projects/OpenNolan/skills/social-media/` as real repo files so the GitHub-synced local OpenNolan agent can use them. Do not rely on symlinks. See `references/opennolan-social-media-skill-mirror.md`.

## Extracting resource links from a Reel
When the user shares a Reel that lists tools/skills/repos/resources and asks for “all the links,” do not just summarize visible names. Use the link-list workflow in `references/instagram-reel-link-extraction.md`: capture metadata with `yt-dlp`, create contact sheets/full-size frames for OCR, search for companion posts/pages promised by the creator, parse install commands or repo slugs when available, verify repos with `git ls-remote`, then return a compact numbered table of names and canonical links. This is especially useful for fast slideshow Reels where many resources share one umbrella repo.

## Recalling previously shared Instagram resources
When the user asks what Instagram-shared projects/tools/repos they have already sent, use the recall workflow in `references/recalling-instagram-shared-resources.md`: search past sessions for direct `instagram.com/reel` user messages first, distinguish direct user shares from automated marketing research snippets, reuse prior extracted link tables when available, and label umbrella/list matches instead of overclaiming exact canonical repos. For “some” requests, return a compact high-confidence list rather than dumping every extracted item.
