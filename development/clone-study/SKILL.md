---
name: clone-study
description: "Studies and recreates the visual design of a high-end website (Awwwards, Site of the Day, premium SaaS) from a URL. Captures structure, design tokens, animations, and asset inventory, then orchestrates scaffold + design + polish + verify in a diff-driven loop until the recreation matches the original. Use this skill whenever the user wants to clone, study, recreate, replicate, copy, or rebuild a website's design from a URL — phrases like 'clone this site', 'recreate this website', 'rebuild this design', 'study how this site is built', 'copy this layout', 'I want my site to look like X', 'reverse engineer this design', 'pixel-match this'. Also use when the user shares a URL and asks 'how would you build this' or 'can we make something like this'. Output is a faithful study recreation, not a wholesale copy — assets are substituted, copy is rewritten, and a teardown doc explains the techniques learned."
---

# Clone Study Skill

Recreate the visual design and feel of a target website by capturing it systematically, extracting its design DNA, and rebuilding it through your existing scaffold/design/polish/verify pipeline.

This skill does not produce a byte-for-byte copy. It produces a faithful **study recreation**: same layout, same animations, same design tokens, same feel — but built from scratch with substituted assets and original copy. That distinction matters for two reasons. First, ethically and legally: copying someone's bundled JS, fonts, photography, and 3D models is not transformative use. Second, practically: minified production code is barely readable, so the only way to actually understand a site is to rebuild it from observation — which is exactly what makes this useful for video content and learning.

## When to invoke vs. delegate

You orchestrate the full loop. Within it you delegate to other skills already on the system:
- `scaffold` — bootstrap the React project once you've decided the stack
- `design` or `premium-design` — build sections from the recreation brief
- `polish` — tighten visual quality after initial build
- `verify` — screenshot the running build at each iteration
- `design-review` — final quality gate

Do not duplicate their work. Your job is capture, analysis, brief-writing, and the diff-driven iteration loop.

## Workflow at a glance

```
URL → capture → analyze → brief → scaffold → design → verify → diff → iterate → done
```

Each run produces a workspace at `~/clone-study/<site-slug>/` so the user can inspect intermediate artifacts (screenshots, network logs, briefs, diffs) — these are the most valuable parts for video content.

---

## Phase 1: Capture

The capture phase is the foundation. If you skip data here, you cannot recover it later — many premium sites have heavy scroll choreography, hover states, or time-based animations that are invisible in a single screenshot.

**Run `scripts/capture.py <url> <output-dir>`.** This Playwright script handles:
- Full-page screenshots at three viewports: 1920×1080 (desktop), 768×1024 (tablet), 390×844 (mobile)
- Scroll-state screenshots every 600px down the page (captures scroll-triggered reveals)
- A 30-second video recording of an automated scroll-through
- DOM snapshot after JS hydration (`document.documentElement.outerHTML`)
- All network requests with content-type, size, and URL
- Performance timeline (when paint events fire, when animations start)
- Console logs (often reveal framework warnings → fingerprints)
- Computed styles for all visible text and interactive elements
- Font face declarations actually loaded
- Detected scripts on `window` (`THREE`, `gsap`, `Lenis`, `Lottie`, etc.)

Read the script's docstring before invoking — flags let you tune the scroll cadence, viewport list, and total runtime. Default takes 60–90 seconds per site.

**Manual supplement:** after the script finishes, open the site in a regular browser and:
- Hover over interactive elements and note any cursor changes, magnetic effects, or color transitions
- Click through any nav menus or modals
- Note audio cues (some sites have subtle sound design)
- Save anything notable as `raw-capture/manual-notes.md`

These nuances rarely come through in headless capture but make a huge difference to "feel."

## Phase 2: Analyze

Now turn the raw capture into structured understanding. The output of this phase is `analysis.json` and a human-readable `analysis.md` summary.

### 2a. Framework and library fingerprinting

Read `references/framework-fingerprints.md` for the full detection table. Quick summary:
- Look for `__NEXT_DATA__`, `__nuxt`, `data-astro-`, `data-svelte-h` in the DOM snapshot
- Check window globals captured during capture (THREE, gsap, Lenis, motion, Lottie)
- Look at network bundles' filenames for fingerprints (`_next/static/`, `chunks/framework-`, `react-three-fiber`)
- CSS class patterns: Tailwind (utility-heavy), CSS Modules (hashed suffixes), styled-components (`sc-`)

Record what you found AND your confidence. "Probably Next 14 + GSAP + Lenis" is more useful than guessing.

### 2b. Design token extraction

**Run `scripts/extract_tokens.py <capture-dir>`.** This pulls:
- **Color palette** — clusters dominant colors from screenshots and computed `color`/`background-color` values. Outputs hex values grouped by role (background, surface, text-primary, text-muted, accent).
- **Typography scale** — every font-family + size + weight combination actually used, ranked by frequency. The top ~5 are the real type system.
- **Spacing scale** — pulls all margin/padding/gap values, finds the base unit (often 4px or 8px), and reports the scale.
- **Border radius scale**
- **Box shadows** (often the secret to premium feel — note them carefully)
- **Easing curves** from CSS transitions/animations

The token extractor outputs a Tailwind-config-shaped JSON so the design phase can drop it straight in.

### 2c. Narrative model — vertical-page vs scroll-pinned timeline

Decide this early. It determines the entire app architecture.

- **Vertical-page**: sections stack top-to-bottom, you scroll through them like a normal site. Animations entrance/exit per-section. This is what most "good" SaaS sites do (Linear, Vercel).
- **Scroll-pinned timeline**: the canvas + UI stay pinned to the viewport while a long scroll runway plays out as a *cinema timeline*. Scroll position drives camera waypoints, object transforms, and section opacity moments. Sections crossfade in/out at progress thresholds. This is what every Awwwards SOTD with a 3D centerpiece does (Oryzo, Lusion, Apple AirPods page).

**Signals that the original is a pinned timeline, not a vertical page:**
- The full-page screenshot from capture is mostly black or blank below the fold (canvas content doesn't paint into the static screenshot)
- Page height is much taller than its visible content would suggest (look for `height: 600vh` or `position: sticky` on inner wrappers in the DOM snapshot)
- Scroll-state screenshots show *the same canvas with different camera/object state* rather than different sections
- Network log shows a `.buf`, `.glb`, or splat camera-animation file (the timeline is data-driven)

**If pinned timeline**: read `references/scroll-pinned-timeline.md` before writing the brief. It contains the exact React architecture pattern, the bloom/material defaults that don't look "rough," and the half-day of debugging traps we already paid for.

### 2d. Animation and scroll behavior inventory

Read `references/animation-detection.md` for the full taxonomy. For each notable animation, record:
- **Trigger**: load / scroll-position / scroll-velocity / hover / click / time
- **Target**: which element, identified by a stable selector
- **Properties changing**: opacity, transform.translate, transform.scale, color, etc.
- **Duration and easing**: estimate from the captured video (frame-step it if needed)
- **Notes**: stagger? spring physics? scroll-pinned? parallax depth?

Watch the video recording at 0.25× speed in a player. This is slow but essential — premium sites get their feel from sub-100ms timing details that are invisible at full speed.

### 2e. Asset inventory

For each non-code asset in the network log, classify:
- **Type**: font, image, video, GLB/GLTF, texture, Lottie JSON, audio
- **Likely licensing**: bespoke (custom logo, brand photography, custom 3D), licensable (Adobe Fonts, stock photo), substitutable (use Google Fonts equivalent, Unsplash photo, free 3D)
- **Substitution plan**: what you'll use in the recreation

Read `references/asset-substitution.md` for the substitution playbook. Bespoke assets get replaced with closest-equivalent free alternatives. Never download and reship original brand assets.

### 2f. Section breakdown

Walk the full-page screenshot top to bottom. For each distinct section, record:
- Purpose (hero, feature, social proof, CTA, footer, etc.)
- Layout pattern (split, stacked, grid-N, hero-with-orbiting-cards, etc.)
- Animation behavior on entry
- Approximate viewport height it occupies

This becomes the section list for the design phase.

## Phase 3: Recreation brief

The brief is the bridge between analysis and build. Without it the design phase makes a thousand small decisions inconsistently. With it, the build is dramatically more faithful.

**Use the template at `references/recreation-brief-template.md`.** Save the filled brief as `recreation-brief.md` in the workspace root.

The brief must include:
1. **Narrative model** — vertical-page or scroll-pinned timeline (see 2c). This is the most consequential choice in the brief.
2. **Stack decision** — based on framework detection plus what scaffold supports. Defaults that work today:
   - Vite **^5** (not ^7 — Vite 7 needs Node 20.19+ and pulls in rolldown native bindings that fail under Node 20.18 with a cryptic `@rolldown/binding-darwin-*` error)
   - `@vitejs/plugin-react@^4`, Tailwind v4 via `@tailwindcss/vite`
   - For 3D: `three`, `@react-three/fiber`, `@react-three/drei`, `@react-three/postprocessing`
   - For premium "smooth feel": optionally `lenis`
3. **Design tokens** — paste the extracted Tailwind v4 `@theme` block ready to drop into `index.css`.
4. **Section list** — one numbered section per page region (or per *moment* if pinned timeline), with a thumbnail screenshot inline.
5. **Animation spec table** — every notable animation with trigger/target/timing. For pinned timelines, this is the **waypoint table** (see scroll-pinned-timeline reference).
6. **Asset substitution table** — original asset → replacement. If the original uses Gaussian splats and you don't have splat data, **SVG → ExtrudeGeometry is a strong substitute** for a brand-mark hero (see asset-substitution.md). User-owned SVG logos are a particularly clean swap.
7. **Copy direction** — original copy is off-limits. Provide a one-line tone description ("punchy fintech," "editorial agency," "playful indie") so the design phase generates appropriate replacement copy.
8. **Difficulty flags** — sections you're worried about (custom shaders, physics, precise scroll choreography). Flag them so the user knows what may need manual tuning.

## Phase 4: Build

Hand the brief to the build skills.

1. **Invoke `scaffold`** with the project name and one-liner. When scaffold asks its setup questions, paste the brief's stack decision and a one-sentence summary. **Immediately after scaffold finishes, pin Vite to ^5** (`npm install -D vite@^5 @vitejs/plugin-react@^4`) — see the Vite 7 / Node 20.19 trap in the stack-decision notes. Then `rm -rf node_modules package-lock.json && npm install` to be sure native bindings install cleanly.
2. **Register the dev server in `.claude/launch.json`** so the preview panel can manage it. One config per project, with `runtimeExecutable: "npm"`, `runtimeArgs: ["run", "dev", "--prefix", "<absolute path to build dir>"]`, and `port: 5173`. Then call `preview_start` rather than running `npm run dev` via Bash — the preview panel gives you live screenshot/eval/console access without managing processes.
3. **For pinned-timeline builds**: read `references/scroll-pinned-timeline.md` first. The architecture is non-obvious (sticky inner viewport inside a tall runway, opacity-driven stages, RAF-throttled scroll progress, mark position not camera offset). Most of the half-day of debugging the first build cost is encoded in that reference.
4. **Invoke `design` or `premium-design`** (premium for editorial/luxury aesthetics, otherwise `design`) with the brief as context. Build the sections in order. Pass the design tokens explicitly.
5. **After initial build, invoke `polish`** to fix any obvious issues.

Do not try to do steps 6 (verify) and 7 (diff) yourself — they have a dedicated loop.

## Phase 5: Visual diff loop

This is what closes the gap between "looks right-ish" and "looks like the original."

**Loop structure (max 5 iterations):**

1. **Capture current state** — for vertical-page builds, screenshot at the same three viewports used for the original capture. **For pinned-timeline builds, also screenshot at the timeline's key progress points** (typically 0.0, 0.28, 0.5, 0.72, 0.92 — the stage holds). Use `preview_eval` to scroll precisely:
   ```js
   (() => { const max = document.documentElement.scrollHeight - window.innerHeight;
            window.scrollTo(0, max * 0.28); return 'intro hold'; })()
   ```
   **Sleep ~1.5s between scroll and screenshot** — camera lerps and section fades need time to settle, and React's RAF-throttled progress hook adds a frame of latency. If you screenshot too fast you'll catch transient state and chase phantom bugs.
2. **Run `scripts/visual_diff.py <original-capture> <current-capture>`** — produces a side-by-side comparison image plus a structured diff report (per-section: spacing off, color off, typography off, animation missing, etc.).
3. **Review the diff report.** Categorize issues into: (a) easy fixes (token mismatch, spacing tweak), (b) medium (animation missing, layout structure wrong), (c) hard (custom shader, complex 3D, audio).
4. **Apply fixes.** Use the `design` skill for structural/animation issues, `polish` for spacing/color/typography. Do easy fixes first — they often unlock the medium ones (e.g., correct spacing reveals that the layout was actually right).
5. **Re-screenshot and re-diff.** Stop when: total diff score below threshold, OR no improvement for two iterations, OR you hit iteration 5.

After the loop, **always invoke `design-review`** as the final quality gate — it's already wired to run on UI work and will catch anything the diff loop missed.

## Phase 6: Teardown document

This is what makes the skill valuable for video content. Write a `teardown.md` in the workspace root covering:
- **Stack used** — what the original was vs. what you used
- **The interesting techniques** — for each notable section, a 2–3 sentence explanation of how it works (e.g., "The hero text reveal uses GSAP SplitText with a 30ms stagger and a clip-path mask that animates from bottom to top with a custom cubic-bezier easing")
- **What was hard to recreate and why** — be honest about the gaps
- **What you swapped** — assets, fonts, copy
- **Diff scorecard** — final per-section diff scores

This doc is the user's video script raw material. Write it like an engineer explaining the build to a peer.

## Output structure

When you finish, the workspace should look like:

```
~/clone-study/<site-slug>/
├── raw-capture/
│   ├── desktop-full.png, tablet-full.png, mobile-full.png
│   ├── scroll-states/  (screenshots at scroll positions)
│   ├── recording.webm
│   ├── dom-snapshot.html
│   ├── network-log.json
│   ├── computed-styles.json
│   ├── console-log.txt
│   └── manual-notes.md
├── analysis.json
├── analysis.md
├── recreation-brief.md
├── build/  (the scaffolded recreation project)
├── diff-iterations/
│   ├── iter-1/  (current screenshots + diff report)
│   ├── iter-2/
│   └── ...
└── teardown.md
```

## Boundaries — read carefully

- **Never download and reship the target's bespoke assets** (custom fonts, brand photography, original 3D models, proprietary Lottie animations). Substitute. The asset substitution doc is non-optional.
- **Never reuse the target's copy verbatim.** Generate replacement copy in the same tone. Original copy belongs to its author.
- **Do not republish the recreation as if it were the user's own commercial site** without making it clearly a study/parody/educational example. The intended use is video content, learning, and portfolio teardowns.
- **If the target site has visible source code that is open-source licensed** (rare but happens — check for a `LICENSE` link or a GitHub link in the footer), you can reference the actual code. Cite the license.
- **If the target requires login**, capture stops. Do not bypass auth.

These rules protect the user. They also produce better video content — "I rebuilt this from observation in 4 hours" is a vastly better story than "I downloaded their JS bundle."

## Tips for picking targets

The user may ask you to pick. Good clone-study targets:
- High visual interest, moderate technical complexity (Tier 1 SaaS like Linear/Vercel/Stripe)
- Notable signature animation worth understanding (a Lusion/Active Theory/Resn piece)
- Clear section structure (avoid one-page WebGL experiences without distinct regions — they're hard to compare via section diff)
- Public-facing marketing pages (no auth wall)

Avoid:
- Sites that are 95% one bespoke 3D scene (you can't faithfully recreate without the original assets and weeks of work)
- Sites with extensive video content (the video itself is the design)
- Sites known to be open-source clones of other sites (defeats the educational purpose)
