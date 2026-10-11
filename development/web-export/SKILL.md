---
name: "web-export"
description: "Builds a browser-playable Web export and ensures shipped text renders, bundling a redistributable font only if declared languages need one. Invoke when a finished local game must go to the Web."
---

# Web Export

**Standalone skill.** Takes a game that **already runs locally** and produces a Web build whose text displays correctly.

It owns exactly one concern: **making the game's own text renderable in a browser.** It runs that concern end to end, and stops.

> **A skipped run is a success.** For a Latin-only game this skill should do nothing at all and say so. Do not invent work to justify the invocation.

---

## Non-goals — do NOT do these here

- **No translation, no localization.** Adding or repairing a language is `/localize`. This skill never authors or invents text.
- **No source rewriting.** If displaying text requires editing gameplay or UI code, that is an architecture defect — report it. Never patch code as a side effect of an export; an export must produce a reviewable, code-unchanged diff.
- **No art, audio, gameplay, or balance work.** Out of scope even if obviously broken; report and move on.

---

## Constants

- **`LANG_SCOPE = declared`** — which languages the run inspects.
  - `declared` (default): only the languages the project actually declares as shipped.
  - `force`: run the font task regardless. Use when text is authored in a non-Latin script that the project never declared as a translation.
- **`SUBSET = off`** — font subsetting.
  - `off` (default): ship the font whole. Simple and safe; larger payload. **This is the recommended default — subsetting is fiddly and introduces a staleness failure mode.**
  - `on`: ship only the glyphs the text actually uses. See Phase 3 for the cost and the required mitigation.
- **`VERIFY = browser`** — post-export visual check via `control-browser`. This skill is not complete without a rendered check of the real build.

---

## Phase 0 — Decide whether there is anything to do

1. Read the project's **declared** release languages:
   - the localization/translation list in the project configuration (the set of translation resources, each carrying a locale code)
   - the configured fallback locale
   - any engine-specific localization setting
2. Classify each declared locale by the script it requires.
3. **Skip gate** — when every declared locale is Latin-script and no non-Latin locale is declared:

   > Report: `Declared languages are Latin-only → no bundled font required. Skipping.`
   > Exit. **Done.**

4. Otherwise continue to Phase 1.

A skipped run must still emit its one-line reason and the declared-language list to the report (Phase 6) so the decision is auditable.

### Why this skill exists at all

A **browser has no OS font fallback.** A script the engine's built-in font does not cover must therefore be *bundled* with the build. Desktop builds behave differently — most engines fall back to system fonts there — so **the same project can render correctly on desktop and show tofu boxes on the Web**. That asymmetry is the whole reason this is a separate, browser-specific concern.

### Known limitation of `LANG_SCOPE = declared`

If text is authored in a non-Latin script but the project never declares that language, the gate skips while the Web build still shows tofu. Re-run with `LANG_SCOPE = force`. This is an accepted trade-off (declaring a shipped language is the project's responsibility, and inspecting every string is not this skill's job) — but say so in the report when a forced run was needed.

---

## Phase 1 — Obtain a font that satisfies the requirements

**Choose the font yourself.** This skill deliberately names no font — the choice must fit the project's languages, art direction, and constraints. Judge candidates against all of these requirements:

| # | Requirement |
|---|---|
| R1 | **Redistribution in a compiled/embedded Web build is permitted by the license.** This is the hard gate — verify it, never assume it. |
| R2 | Commercial use is permitted. |
| R3 | The full license text is available and **must be vendored into the repository** next to the font. |
| R4 | Glyph coverage includes **every character required by every declared language**, plus the punctuation and symbols the UI actually uses. |
| R5 | Legible at the project's **smallest** UI text size — check small glyphs specifically, since CJK-style scripts degrade first at small sizes. |
| R6 | The family's weights are metrically consistent, so one family can serve the whole UI without mixing vendors. |
| R7 | **Not an OS-vendor font**, and not any font whose license restricts embedding or web distribution. |
| R8 | Provenance is recorded: where it came from, which version, under which license. |

**Acquisition order:** prefer a copy already present locally (project, font cache, or an openly-licensed font already installed on the machine); only reach the network if nothing local qualifies. If nothing satisfying R1–R7 can be obtained, **fail loudly** with the reason.

> **Never silently fall back to a system font.** A system font appears to work on the machine that ran the export and then renders as tofu on every player's browser. Failing loudly is strictly better than a build that looks fine locally.

---

## Phase 2 — Wire the font in (one place)

1. Assign the font as the **project-level default font** — a single global theme/stylesheet whose default font is this file. This is normally a one-line project setting.
2. **Do not edit gameplay or UI scripts.** If the font cannot be applied globally, stop and report the missing global styling layer as an architecture defect; do not sprinkle per-widget overrides during an export.
3. **Verify the assignment actually took effect.** A font configured but not wired is the most common silent failure in this skill. Confirm the global theme is the one the project loads.

---

## Phase 3 — Subsetting (only when `SUBSET = on`)

Skip this phase entirely when `SUBSET = off` (the default).

1. Extract the character set from the **shipped string tables** for all declared languages — not by grepping source files for characters, which misses runtime-assembled strings.
2. Add ASCII, digits, common punctuation (including full-width forms), and deliberate headroom for any character injected at runtime by formatting.
3. Generate the subset **with a script committed to the repository** so it can be regenerated. A one-off manual subset is a time bomb: the next content change silently reintroduces tofu.
4. Assert **0 missing glyphs** for the extracted character set.
5. Record the **character-set hash** in the report, so a future mismatch is detectable.

> **Staleness is the risk you are accepting by turning this on.** The mitigation is step 5 plus a report line telling future runs to regenerate when text changes. If that is more process than the project wants, leave `SUBSET = off`.

---

## Phase 4 — Export

1. Confirm the engine's **export templates** for the target version are installed.
2. Export headlessly to a build directory. **Output paths are relative to the project root** — a parent-relative path (`../build/web`) resolves outside the project and fails.
3. **Exclude test and evidence artifacts from the payload.** A default "export all resources" filter will happily pack your test scripts, probe scenes, and captured screenshots into the shipped archive — wasted payload, and test code shipped to players. Add explicit exclusions.
4. Prefer a **non-threading** Web template unless the project genuinely needs threads; it is far more broadly compatible.
5. Note the payload sizes produced (total, and the font's share — see Phase 6).

---

## Phase 5 — Verify in a real browser (mandatory)

This phase is what makes the run count. Static checks and headless runs cannot see the failure this skill exists to prevent.

1. Serve the build directory locally from **one** server on a probed free port.
   - **Serve a single page at a time.** A single-threaded static server can be saturated by concurrent requests for a multi-tens-of-MB engine payload; the result is a blank canvas that looks exactly like a broken build. Close other tabs before loading.
2. Drive it with the browser automation skill `control-browser`. **It is main-agent-only — do not delegate it to a subagent.**
3. Check, and capture a screenshot for each:
   - **Every declared language renders, with zero missing-glyph boxes.** This is the primary gate.
   - **The canvas fills or letterboxes as intended** at a window that is *not* the project's native aspect ratio.
   - **Audio unlocks after a user gesture** — browsers block autoplay until the user interacts; confirm the first sound actually plays, not merely that it loaded.
   - **The console reports no errors.**
4. Report honestly which level of verification was achieved. If no browser is available, the run is **incomplete**, not passed — say so plainly rather than substituting a headless check.

---

## Phase 6 — Report

Write `production/web-export/web-export-report.md`:

| Field | Content |
|---|---|
| Declared languages | the list read in Phase 0 |
| Outcome | `skipped (Latin-only)` / `acted` — plus whether `LANG_SCOPE = force` was needed |
| Font | name, source, version, license, and where the license text was vendored |
| Subsetting | on/off; if on, the character-set hash and missing-glyph count |
| Payload | total size, **and the font's absolute + percentage share** (report this even when subsetting is off, so the cost of the default is visible) |
| Verification | per-language screenshots, canvas-fit result, audio-unlock result, console result |
| Exclusions | what was filtered out of the export payload |
| Gaps | anything not verified, and anything that needs a human decision |

---

## Hard rules

- **Never bundle a font whose license forbids redistribution.** Verify the license; do not infer it from the font being "free to download". Getting this wrong is a legal defect that a local build will never reveal.
- **Never edit gameplay or UI source during an export.**
- **Never translate or author text.**
- **Never substitute a system font silently.**
- **Never claim the build verified without a browser render of the actual build.**
- **Always report the font's share of payload**, even when subsetting is off.

---

## Measured pitfalls (from real Web exports)

- **Headless is fine for exporting, but cannot produce screenshots** — a headless run uses a dummy renderer, so frame capture returns nothing. Visual verification needs a real window or a browser.
- **Export paths are relative to the project root**; a `../` path fails with "target folder does not exist".
- **An "export all resources" filter packs tests and evidence.** Add exclusions.
- **Desktop usually has system font fallback; browsers do not.** A desktop build rendering fine proves nothing about the Web build.
- **Screenshotting a WebGL canvas can tile/repeat** when the capture region is close to the viewport size. Keep the capture region clearly smaller than the viewport, and never read a tiled capture as a rendering bug.
- **Automation clicks may not reach the canvas** — synthetic pointer events dispatched into the page are often more reliable than high-level click APIs for a canvas-rendered game.

---

## Next steps after a successful export

- Hand the build directory plus the report to whoever is publishing it.
- If a language was added or text changed since the last export, re-run this skill — a stale font or subset is invisible until someone plays.
