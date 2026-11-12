---
name: ak-show-off
description: "Create preference-aware self-contained HTML pages that showcase work."
when_to_use: "Invoke for demos, visual presentations or interactive showcases."
category: media
keywords: [HTML, showcase, demo, presentation]
argument-hint: "[markdown-or-prompt] [--no-antv|--no-diagram-design|--no-editorial-visuals]"
license: Proprietary
metadata:
  author: agentkit
  version: "1.0.3"
---

Activate `ak-frontend-design` to build the showcase page. Run its Decision Procedure (one-line Design Read) and Self-Review Gate, because a demo page converges on the same generic layout as product UI when they are skipped.

## REQUEST / MISSION:
$ARGUMENTS

## PURPOSE:
Showcase, social media posting, and optional output images for articles.

## PERSISTED PREFERENCES

`show-off` has user-level workflow preferences. Resolve them before invoking
`/ak-project-management`, because the resolved values decide which tasks the plan
registers. Defaults preserve legacy behavior:

```json
{
  "screenshots": true,
  "publishing": true,
  "languages": ["vi", "en"]
}
```

Resolve workflow preferences before choosing outputs:

```bash
PREF_SCRIPT="scripts/preferences.js"
node "$PREF_SCRIPT" get
```

The helper stores preferences at `$AGENTKIT_HOME/show-off/preferences.json`, or
`~/.agentkit/show-off/preferences.json` when `AGENTKIT_HOME` is unset.
`SHOW_OFF_PREFS_PATH` may override the path for tests or one-off advanced use.

Recognize workflow-control intent before registering optional outputs:
- Screenshot capture: phrases like "no screenshots", "skip screenshots", "turn off screenshots", or `--no-screenshots`.
- Publishing: phrases like "no publish", "skip publishing", "local only", "do not publish", or `--no-publish`.
- Language mode: phrases like "English only", "Vietnamese only", "disable dual language", "no bilingual", or `--languages en`.
- Reset: phrases like "reset show-off preferences" or "use defaults again".
- One-time override: if the user says "for this run only", apply it for this invocation but do not persist it.

If the user explicitly changes one of these settings and does not say it is only for this run, persist it immediately:

```bash
# Examples
node "$PREF_SCRIPT" set --no-screenshots
node "$PREF_SCRIPT" set --no-publish
node "$PREF_SCRIPT" set --languages en
node "$PREF_SCRIPT" set --screenshots on --publishing on --languages vi,en
node "$PREF_SCRIPT" reset
```

Use the resolved preferences for the current run. The latest explicit user instruction
wins over stored preferences. Do not ask the user to repeat a persisted opt-out.

## PREREQUISITE

After resolving preferences, inspect the mission and output scope. A small local showcase may proceed directly with a concise checklist and the existing asset path. For multi-artifact or publication work, reuse or create a plan through the installed project-management capability. That owner handles plan/task lifecycle.

Purpose:
- Create a dated plan directory under `plans/` (naming from hook injection: `{date}-{issue}-{slug}`).
- Register the resolved checklist below as trackable tasks:
  - Always: request-analysis, content, HTML, local open/review.
  - If `screenshots=true`: capture.
  - If `publishing=true`: publish content/static site.
- Set the active plan context so downstream skills (`frontend-design`, `agent-browser`, capture script) share the same plan folder and assets root.
- Record the invocation arguments and resolved preferences (`screenshots`, `publishing`, `languages`) in `plan.md`.

A missing live task surface does not block local HTML creation: keep the checklist in the plan or session. Resolve genuine missing content, target or permission decisions before dependent work.

## DETAILED INSTRUCTIONS
Follow these steps strictly in order, one by one:
- Read and analyze the request carefully, split into topics/sections (minimum 2, maximum 6, including hero section).
- Update the active checklist as meaningful work completes; use plan tracking only when a plan is needed.
- Search the internet for supporting evidence or fact-checking information in the request/mission.
- Write showcase content as markdown at `assets/showoff/<mission-name>/content.md` with all content organized by sections/topics.
  **NOTE:**
  - Check if one of these files existed:
    [
      `/Volumes/GOON/www/assets/writing-styles/`,
      `~/www/writing-styles/`,
      `~/.claude/writing-styles/`,
      `~/writing-styles/`
    ]
    -> Read it to use writing style (if none of them exists, just skip).
  - Attach citation URLs in references/footnotes at end of file.
- If `publishing=true`, use `agentwiki` CLI to publish this document (organize or create appropriate folder).
  If `publishing=false`, keep the document local and mark the publish task skipped.
- Follow the shared HTML composition contract in `../ak-preview/references/html-skill-composition.md`:
  1. Activate `ak-frontend-design` first for layout, typography, responsive shell, and design critique.
  2. Activate `ak-diagram` second (when installed) to compile typed JSON IR for system maps/flow diagrams.
  3. If `ak-diagram` is absent, produce a clean semantic inline SVG/CSS fallback with `<title>/<desc>`.
  - Include visual diagrams/illustrations
  - Include decorative elements (optional)
  - Micro-animation or subtle animation (optional)
  - Attach citation URLs in references/footnotes at bottom of page
- First section (hero section): always an impressive, eye-catching, glamorous design that hooks and entices into subsequent sections.
- Layout organized into multiple sections corresponding to request topics -> user scrolls smoothly top-to-bottom with parallax effects.
  Remember id/class names of each section for screenshot capture later.
- Content follows the resolved language preference:
  - `["vi", "en"]`: provide Vietnamese and English content with a clear language toggle or parallel bilingual treatment.
  - `["en"]`: English only. Do not add Vietnamese copy or a language toggle.
  - `["vi"]`: Vietnamese only. Do not add English copy or a language toggle.
- If `screenshots=false`, skip screenshot capture entirely. Do not run the local capture script or `rws`; mark the capture task skipped and report the local HTML path.
- If `screenshots=true`, capture each section as images (JPG/PNG) at `assets/showoff/<mission-name>/images/` with ratio-based prefix (`horizontal`, `vertical`, `square`).
  **NOTE:** The capture script now auto-waits for fonts, `<img>` completion, and CSS background-image loading before each shot. `--settle-delay` adds an extra cushion for animations / lazy reveals.
  Use the parallel capture script; it shoots the sections concurrently:
  ```bash
  node scripts/capture-sections.js \
    --url "file:///path/to/index.html" \
    --output-dir "assets/showoff/<mission-name>/images" \
    --sections "#hero,#section-2,#section-3" \
    --ratios "horizontal,vertical,square" \
    --settle-delay 1500
  ```
  **FALLBACK - `rws` CLI**: if `publishing=true` and the local script fails (puppeteer missing, headless Chrome unavailable, sandbox error, script exit non-zero) AND the `rws` command is on PATH AND `$RWEB_API_KEY` is set, fall back to the ReviewWeb screenshot API. The HTML must be publicly reachable (publish via `agentwiki` first, then use the public URL + `#section-id` anchors).

  Detection:
  ```bash
  command -v rws >/dev/null && [ -n "$RWEB_API_KEY" ] && echo "rws fallback available"
  ```

  Per (section, ratio) capture loop:
  ```bash
  # Viewports: horizontal=1920x1080, vertical=1080x1920, square=1080x1080
  rws screenshot \
    --url "https://public-host/mission/#hero" \
    --width 1920 --height 1080 \
    --delay 1500 \
    --format json \
    | jq -r '.imageUrl' \
    | xargs -I{} curl -sSL {} -o "assets/showoff/<mission-name>/images/horizontal-hero.png"
  ```

  Fallback rules:
  - Run per (section, ratio) combo; parallelise with `xargs -P` or shell `&`.
  - `--delay` passes the same settle-delay value used by the local script.
  - Skip `rws` fallback whenever `publishing=false`; the user explicitly chose a local-only flow.
  - Skip `rws` fallback if the HTML is only reachable via `file://` and cannot be published yet — in that case, surface the local script error to the user and stop.
  - Never pass `$RWEB_API_KEY` on the command line; rely on the env var resolution (`rws` reads it automatically).
  - On `rws` exit code 2 (auth error) or missing `$RWEB_API_KEY`, stop and report — do not silently skip capture.
- If `publishing=true`, use `agentwiki` CLI to publish/update this static site when complete.
  If `publishing=false`, do not publish and report the local artifact path instead.
- Use `open` CLI (or equivalent) to open the resulting HTML page.

## OUTPUT REQUIREMENTS
- Each section's components fit within the browser viewport
- Support responsive layout, especially good display for ratios 16:9, 9:16 and 1:1
- Font must support Vietnamese characters well when Vietnamese is enabled
- Theme toggle button: system (default), light & dark
- Ensure layout never breaks, section content never gets clipped on any side, displays well on all screen sizes
- Output images are sized to match their ratios when `screenshots=true`.
- Modularization & maintainable code

**Editorial visual layer (on by default, additive for non-hero panels):** read `ak config prefs resolve --json | jq '.prefs.visual'` (nested keys spell camelCase — `diagram_design` returns as `diagramDesign`). The hero section still delegates to `ak-frontend-design` unchanged. For non-hero KPI / ranked-list / quadrant panels, the AntV Infographic palette (`CandyCardLite`, `CompactCard`, `CompareBinaryHorizontal`, `CircularProgress`, `ChartPie`, `ChartBar`) is available when `.prefs.visual.antv.enabled` AND the artifact carries ≥3 such tiles. For architecture or process diagrams inside a section, `diagram-design` (Architecture, Process, Data flow) is available when `.prefs.visual.diagramDesign.enabled`. Kill switches: `--no-antv`, `--no-diagram-design`, `--no-editorial-visuals`. See the sibling `ak-preview` skill's `../ak-preview/references/html-antv-infographic.md` and `../ak-preview/references/html-diagram-design.md`.

## Handoff Gate (mandatory before delivering)

Before presenting the result, run the 5-dimension check in
`../ak-design/references/handoff-gate.md` (context fit, visual hierarchy,
craft/detail, usability/accessibility, implementation safety) against the
generated page(s). Fix a failing dimension now, or list it explicitly under
"Known limitations" in the handoff template — never ship a known failure
silently.

## PREFERENCE HELPER USAGE

The preference helper at `scripts/preferences.js` supports:

```bash
# Print resolved user preferences as JSON
node scripts/preferences.js get

# Persist workflow opt-outs
node scripts/preferences.js set --no-screenshots --no-publish --languages en

# Re-enable defaults
node scripts/preferences.js reset
```

Options for `set`:
- `--screenshots on|off`, `--no-screenshots`
- `--publishing on|off`, `--publish on|off`, `--no-publishing`, `--no-publish`
- `--languages en|vi|en,vi`, `--language en|vi`
- `--dual-language on|off`, `--no-dual-language`

## Capture options

Load `references/capture-options.md` only when screenshots are enabled.

## SECURITY POLICY
This skill handles HTML generation and screenshot capture only. 
Publishing uses the selected existing capability within the authorized target; this skill does not implement authentication, databases, or general server deployment.
Never include API keys or credentials in generated HTML files.
