---
name: walkthrough-gif
description: >
  Generate browser walkthrough recordings as GIF and MP4 from a natural language description.
  Use this skill whenever the user wants to record a browser walkthrough, create a product demo,
  document a UI flow, generate onboarding visuals, or produce a "how to" screen recording for any
  web app. Triggers include: "record a walkthrough of", "create a GIF showing how to", "make a
  demo of", "capture the flow for", "show how [feature] works in the browser", "document this UI
  flow", or any request combining a browser/web app with recording/capture/demo output.
  The skill generates a local Node.js/TypeScript project that the user runs on their machine
  using Stagehand + Playwright for AI-controlled browser automation, and gifski/ffmpeg for output.
  For quick one-off captures in the user's live browser session, prefer the claude-in-chrome
  gif_creator tool instead; use this skill when a re-runnable script, MP4, high-quality GIF,
  clean-profile recording, or CI repeatability is needed.
compatibility: "Node >=18, Playwright, Stagehand, ffmpeg, gifski (optional). Generates scripts for local execution — Claude Code only."
---

# Walkthrough GIF Skill

Generates a self-contained Node.js project that records a browser walkthrough and exports MP4 + GIF.

## When to use this skill vs. claude-in-chrome gif_creator

For a quick, one-off capture inside the user's live browser session (their profile, their open
tabs, already logged in), the `claude-in-chrome` `gif_creator` tool is far simpler — no project
scaffolding, no API keys. Reach for this skill when the user needs something gif_creator can't
give them: a **re-runnable/versionable script** (re-record after every UI change), **MP4 output**,
a **high-quality gifski GIF**, a **clean-profile recording** (no personal bookmarks/extensions in
frame), or **CI repeatability**.

## Architecture

```
Natural language description
        ↓
Claude generates TypeScript script
        ↓
Stagehand v3 (AI browser control) — Playwright attached over CDP
        ↓
Playwright recording context captures video (.webm)
        ↓
ffmpeg converts → .mp4
gifski converts frames → .gif
        ↓
Output: walkthrough.mp4 + walkthrough.gif + walkthrough.md
```

## Workflow

### Step 1: Gather Requirements

**Prerequisite — LLM API key:** Stagehand calls an LLM for every AI action. The user needs
`ANTHROPIC_API_KEY` (or the provider key matching the configured model, e.g. `OPENAI_API_KEY`)
available for `.env`. Confirm this upfront — without it the generated script cannot run.

Before generating any code, confirm:

1. **Target URL** — Where does the walkthrough start? (e.g., `https://app.example.com/login`)
2. **Flow description** — What steps should be demonstrated? (natural language is fine)
3. **Auth situation** — Is the page public, or does it need login? If login: will they hardcode creds in `.env`, use a pre-authenticated session/cookie export, or start from a logged-in state?
4. **Output format** — GIF only, MP4 only, or both? (default: both)
5. **Duration / pace** — Fast demo or deliberate step-by-step? (~1-2s pause between steps is default)
6. **Viewport** — Default is 1280×800. Narrower for mobile-style demos.

If the user gives a rich description upfront, infer what you can and ask only about gaps.

### Step 2: Generate the Project

Output a complete, runnable project at `./walkthrough-[name]/`:

```
walkthrough-[name]/
├── package.json
├── tsconfig.json
├── .env.example
├── src/
│   └── walkthrough.ts      ← main script
└── scripts/
    └── convert.sh          ← ffmpeg + gifski conversion
```

Read `references/stagehand-patterns.md` for the Stagehand API and step translation patterns.
Read `references/output-pipeline.md` for the ffmpeg/gifski conversion commands and GIF tuning.

### Step 3: Translate Steps

Convert the user's natural language into `stagehand.act()` calls (v3: `act()` lives on the
stagehand instance and takes a plain string, with options like `variables` and `page`). See
`references/stagehand-patterns.md` for patterns and gotchas.

Key translation rules:
- Each logical UI action = one `stagehand.act("...", { page })` call with a clear English instruction
- Typed input goes through `variables` (`%name%` placeholders) — never inline secrets in the instruction string
- Add `page.waitForTimeout(1500)` between major steps for pacing (visible to viewer)
- Add `page.waitForLoadState('networkidle')` after navigations
- Never hardcode selectors — Stagehand figures those out from natural language instructions
- For flows that have auth: use `.env` for credentials, never hardcode

### Step 4: Recording Strategy

Always use **Playwright video recording** as the primary capture method:
- Stagehand v3 has no built-in recording — connect Playwright to Stagehand's browser via
  `chromium.connectOverCDP({ wsEndpoint: stagehand.connectURL() })`, create a context with the
  `recordVideo` option, and drive that context's page (see `references/stagehand-patterns.md`)
- Record full session as `.webm` via that recording context
- Do NOT try to stitch individual screenshots into GIF directly — video → frames → GIF is higher quality
- After script completes, run `convert.sh` to produce MP4 and GIF

**Never make GIF the primary artifact.** MP4 is always produced first. GIF is derived from it. GIFs are large and low quality for anything over 15 seconds — warn the user and suggest keeping walkthroughs under 60s.

### Step 5: Click/Cursor Overlays (Optional but recommended)

Inject a click-highlight overlay via `page.addInitScript()` before the walkthrough starts. See `references/stagehand-patterns.md` → "Click Overlay" section for the snippet.

This adds a subtle ripple animation at each click point — makes walkthroughs dramatically more readable without post-processing.

### Step 6: Output

After generation, produce:
1. The project directory (all files)
2. A brief setup checklist in the conversation:

```
## Setup
npm install
npx playwright install chromium
cp .env.example .env  # fill in ANTHROPIC_API_KEY + any credentials

## Run
npx tsx src/walkthrough.ts

## Convert to GIF + MP4
bash scripts/convert.sh
```

Also tell the user what to expect: approximate duration, viewport size, output filenames.

**Offer to run it:** Claude Code can execute the whole pipeline itself — `npm install`,
`npx playwright install chromium`, run the walkthrough script, then `bash scripts/convert.sh` —
if the user agrees (they still need to provide the `.env` values). When running it yourself,
verify the output before declaring success: `ffprobe` the MP4 for a sane duration and check the
GIF/MP4 file sizes are non-trivial (`convert.sh` prints these in its verification tail).

---

## Warnings / Bail Conditions

Tell the user upfront if any of these apply:

| Condition | Guidance |
|---|---|
| Page requires login with MFA/SSO | Script can't handle this automatically — user must export cookies from a logged-in browser session |
| CAPTCHA on target page | Playwright will stall — use a demo/sandbox environment instead |
| Heavy animations / infinite scrollers | Recording will capture them, but GIF conversion will be large — suggest clipping |
| Flow is >90 seconds | Recommend MP4 only; GIF will be unusably large |
| Page content is randomized/dynamic | Stagehand handles visual targeting, but warn that reruns may look different |

---

## Output Naming Convention

```
walkthrough-[slug]/
  output/
    walkthrough.webm     ← raw Playwright recording
    walkthrough.mp4      ← converted (H.264, web-safe)
    walkthrough.gif      ← gifski output, max 800px wide
    walkthrough.md       ← step-by-step annotation (auto-generated)
```

The `.md` file lists each `act()` call as a numbered step with timestamps — useful for embedding as a caption alongside the GIF.

---

## Reference Files

- `references/stagehand-patterns.md` — Stagehand API, step translation, click overlay snippet, auth patterns
- `references/output-pipeline.md` — ffmpeg commands, gifski flags, GIF optimization, troubleshooting
