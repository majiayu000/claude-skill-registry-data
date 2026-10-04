---
name: ui-screenshots
description: >-
  Capture screenshots and short clips of any web application's UI for visual review, documentation, or pull requests.
  Use for screenshot requests, before/after comparisons, recording UI interactions, and preparing or attaching visual
  evidence of a UI change. Adapt to the application's framework, authentication, tooling, and delivery destination.
metadata:
  owner: Matti
---

# UI screenshots and clips

Capture the actual running web UI with enough context to assess the requested surface or behaviour. Support standalone
screenshots, before/after comparisons, and motion clips. A reachable application and a browser capture tool are
sufficient; a repository, test runner, account, or hosting service is needed only when the task requires one.

## Establish the capture scope

- Identify the application URL, relevant pages, and interaction states from the request. For a code change, inspect the
  diff or implementation plan to find affected surfaces without assuming particular directories, file extensions, or
  component libraries.
- Determine whether the user wants a current-state capture, a comparison, or a clip. For comparisons, capture the
  baseline before editing when possible. For UI-change PRs, prefer before/after pairs for the affected surfaces. A
  standalone screenshot needs no baseline.
- Use the requested viewport, device, theme, and locale, or the project's established capture settings. Otherwise use
  the desktop defaults below. Record the settings and include relevant mobile breakpoints or alternate themes when the
  change affects them.
- Determine the delivery destination from the request and project conventions. Local files are a valid deliverable.
  Capturing screenshots does not itself require a ticket, PR, asset branch, or upload.

If assessing a change, decide whether it affects visible content or interaction. Backend changes can alter rendered UI,
and component changes can be visually inert. When there is no visual effect, explain that briefly in the requested
review or verification output instead of creating unrelated media.

## Discover the application's setup

For a local application, read its project instructions, startup scripts, browser-test configuration, and relevant
fixtures. Start only the services the chosen surface needs using the documented commands and available
process-management tools. Discover the actual URL and port, and wait for the application to be ready. For an existing
preview or deployed application, use its provided URL directly.

Prefer available browser automation or the project's existing capture tooling. If using Playwright, use the project's
installed version, test configuration, and supported browser installation command. Do not assume a package manager,
database, container runtime, server launcher, or browser version.

Choose authentication and data setup for the actual surface:

- Public pages need no session.
- For authenticated pages, prefer existing test fixtures, supported test-login helpers, or a dedicated test account. Use
  an existing browser session when authorized and appropriate for the requested capture. Keep credentials and saved
  authentication state out of screenshots and published artifacts.
- Seed only the data needed for the scenario. Reuse project helpers when available; do not assume a particular account,
  workspace, or domain model, and do not reset unrelated data.
- A component preview, documentation site, or local email preview is suitable when it renders the requested surface
  faithfully. Use the application itself when layout, routing, or integration matters.

Verify that the browser reached the intended UI rather than a login redirect, error page, or loading shell.

## Keep capture files inspectable

Use `.local/` in the application's project root for local capture work. If there is no local checkout, use `.local/` in
the current task workspace. Create it if it does not exist, then create a descriptive capture directory such as
`.local/ui-screenshots/<capture-id>/`. Keep each capture's screenshots, original recordings, converted clips, capture
scripts, reports, and a short record of its URL, revision, and settings together there for later inspection. Use a new
capture directory when needed to avoid overwriting earlier evidence.

In Git projects, verify that `.local/` is ignored. If it is not, add `/.local/` to the project's `.gitignore`,
preserving existing entries. Keep capture artifacts out of the application commit and preserve any existing staged work.

## Capture the requested states

### Preserve a trustworthy baseline

For a comparison, record which revision or deployment each capture represents. If implementation has already started,
inspect staged and unstaged changes before choosing a baseline. Prefer a separate worktree at the appropriate base
revision under `.local/ui-baselines/<capture-id>/`, or an existing baseline deployment, leaving the current work and
index intact. Create the parent directory when needed. Do not automatically stash, reset, or switch the active checkout.

Give an isolated baseline its own server port and build output. Check whether dependencies are consumed from source or
compiled artifacts, and follow the project's rebuild or cache-invalidation procedure between revisions. Confirm that
each server and browser actually loaded the intended code.

Use equivalent test data on both versions. If shared data or a schema change prevents a valid comparison, use isolated
fixtures or report the limitation. If a baseline cannot be recovered, deliver the available capture clearly labelled as
current-state or after-only evidence and explain what remains unverified.

### Make captures reproducible

- Match route, browser, viewport, scale factor, zoom, theme, locale, timezone, data, and interaction state across a
  pair. Different base URLs are fine when comparing separate deployments of the same route.
- When no request or project convention specifies otherwise, use a 1280 by 820 desktop viewport, scale factor 2, light
  theme, and `en-US` locale. Adapt these defaults when the target device, language, or theme requires it, and keep the
  chosen settings fixed across the pair.
- Wait for observable readiness: expected content, loaded fonts and images, and the required UI state. Avoid arbitrary
  sleeps for page readiness. Keep clocks, random data, and incidental animations stable where practical without hiding
  the behaviour under review.
- Drive the relevant states explicitly: keyboard focus, hover, validation errors, open menus or dialogs, scroll
  positions, and loading or empty states. A state described only in prose is not visual evidence.
- Prefer viewport captures for layout and overlays. Use full-page captures for page-length content or element captures
  for isolated details. Keep useful surrounding context.
- Use the same crop rectangle for a comparison. If using element captures, record any size change and include a shared
  viewport capture when element cropping would conceal movement or overflow.
- Check the functional claim as well as its appearance. A screenshot of hidden overflow does not prove that content
  remains accessible or that the container still scrolls.

When the project uses Playwright, adapt this example to its test discovery, authentication, and readiness signals.
`UI_CAPTURE_URL` is the page to capture; `UI_CAPTURE_PHASE` can be `before`, `after`, or `current`. Replace the `main`
locator if the application has a different ready-state signal, and add the interactions needed for the requested state.
Set the runner's output directory to `.local/ui-screenshots/<capture-id>/test-results/` so `testInfo.outputPath()`
writes inside the capture directory.

```ts
import { expect, test } from "@playwright/test"

test.use({
  viewport: { width: 1280, height: 820 },
  deviceScaleFactor: 2,
  colorScheme: "light",
  locale: "en-US",
})

test("capture UI", async ({ page }, testInfo) => {
  const url = process.env.UI_CAPTURE_URL
  const phase = process.env.UI_CAPTURE_PHASE ?? "current"
  if (!url) throw new Error("Set UI_CAPTURE_URL to the target page")
  if (!["before", "after", "current"].includes(phase)) {
    throw new Error("UI_CAPTURE_PHASE must be before, after, or current")
  }

  await page.goto(url)
  await expect(page.getByRole("main")).toBeVisible()
  await page.evaluate(() => document.fonts.ready)
  await page.screenshot({ path: testInfo.outputPath(`surface-${phase}.png`) })
})
```

Use the project's test command to run only the capture spec. Keep capture scripts in the `.local/` capture directory
when the runner supports it. If test discovery requires a temporary spec elsewhere, retain a copy under `.local/` and
remove the spec outside `.local/` after the run. Copy each phase's deliverables into an `artifacts/` subdirectory of the
capture directory before another run can clear test results. Name files by subject and state, such as
`menu-mobile-before.png` and `menu-mobile-after.png`.

For animation, scrolling, dragging, or intermediate flow states, read [references/clips.md](references/clips.md).

### Add onion-skin evidence for subtle changes

When spacing, alignment, borders, typography, or other small differences are hard to see in the before/after pair, also
create an onion-skin comparison image. Keep the original pair alongside it; the overlay is supplemental evidence.

- Blend the before and after images equally at identical pixel coordinates: 50% before plus 50% after. Use deterministic
  image compositing, such as a canvas or image-processing utility, so the comparison preserves the captured pixels
  rather than generating or retouching UI content.
- Require matching capture geometry, pixel dimensions, scale, and scroll position. Do not stretch, warp, or shift one
  image to make its elements align, since that can conceal the change being reviewed. If the captures do not match,
  recapture a common viewport or use the same explicit crop from both originals where that still shows the change.
- Save `<subject>-onion-skin.png` beside the originals in `.local/ui-screenshots/<capture-id>/artifacts/`. Record the
  source filenames, blend ratio, and any crop coordinates with the capture settings.
- Inspect the overlay at native resolution. If the relevant detail is still difficult to see, also include a close-up
  using the same crop coordinates for both sources, and identify the region in its caption.
- Label it clearly, for example, `Onion skin: 50% before / 50% after`, and explain what to inspect. Confirm that visible
  differences come from the UI change rather than mismatched data, fonts, or capture state. The blended colors are not
  the actual appearance of either version; use the originals to assess final colors and contrast.

If a comparable before image is unavailable, report that limitation instead of fabricating an overlay. Deliver any
generated overlay with the original pair, using the same local or authorized PR destination.

## Inspect and deliver

Open every final image and play every final clip. Check legibility, framing, state, and whether the artifact actually
shows the claimed change. Inspect the whole frame for private data, account details, secrets, autofill menus, or
unrelated notifications. Prefer synthetic data; recapture with safe data if the media contains information inappropriate
for its destination.

For local delivery, show or link the files and state the captured route and relevant settings. For a comparison, present
labelled before/after images together with descriptive alt text that identifies what the reviewer should inspect. Use
one pair per subject. For example, replace these local filenames with the actual file paths or verified hosted URLs
supported by the destination:

```markdown
| Before                                             | After                                                  |
| -------------------------------------------------- | ------------------------------------------------------ |
| ![Menu clipped by the panel edge](menu-before.png) | ![Menu fully visible beside the panel](menu-after.png) |
```

For a PR or review, follow that project's template and place evidence in its existing screenshots, testing, or coverage
section. If there is no prescribed section, use a concise visual-evidence section or the requested comment. Do not
assume a particular template or depend on another PR-writing skill. Screenshots support the project's normal checks;
they do not replace them.

When upload or posting is requested or already authorized, read [references/hosting.md](references/hosting.md). For
screenshots requested in a PR description, recommend the repository's `assets-pr-screenshots` orphan branch unless the
user or project specifies another destination. Upload the selected media and embed verified links in the requested PR
body as part of that task. Otherwise deliver local artifacts and prepare any requested draft without publishing them.

Keep the `.local/` capture directory and its useful inspection files after delivery. Remove only temporary copies
outside it, throwaway fixtures, sensitive session files, and redundant intermediate files created for this capture.
Preserve the delivered media, original recordings, capture scripts, reports, settings, user data, and staged work.
Report any remaining access, baseline, or rendering limitation instead of claiming complete verification.

## Done when

- The requested pages and states have inspected, readable screenshots or clips.
- Comparisons identify both versions and hold capture conditions constant, or disclose why a baseline or equivalent
  state was unavailable.
- Subtle differences include an inspected, labelled onion-skin overlay when comparable before/after captures are
  available, while retaining the original pair.
- The user has usable local artifacts or verified links at the authorized destination.
- Capture files remain available for inspection under `.local/ui-screenshots/<capture-id>/`.
- Any requested PR evidence follows its actual template, and cleanup preserves unrelated work.
