---
name: figma-pixel-verify
version: "1.11.0"
user-invocable: true
description: "Measure laid-out frames of a running UI against a Figma living artifact (inventory + spec + Verify section). Use when checking pixel alignment / 对照 Figma 验收 after implement, including light/dark or hover/variant states (switch theme and state, measure each row). Non-document UIs use a layout-probe; source-constant compare is not a pass. Fix and remeasure in the same run until overall PASS, without asking a person. Critical unmeasured rows fail overall. Report checker must exit 0; a layout probe mounts the shipping parent. An openable channel must cite a saved non-empty screenshot file; layout-probe may say not-openable. Triggers — 「检查像素对齐」「对照 Figma 验收」「设计保真检查」「是否对齐稿面」「figma 保真检查」「暗黑模式验收」「多主题保真检查」 / verify Figma fidelity, pixel check, dark mode fidelity check, multi-theme verify. Do NOT use as the primary implement workflow (use figma-pixel-implement) or for code→Figma."
---

# Figma Pixel Verify

Measure a **running** UI against a Figma **living artifact** (Inventory + Spec) and write pass/fail evidence into its **Verify** section (or a Spec source sibling). On a non-pass row, fix and remeasure in this run. Actual values come from a laid-out read. Do not overwrite Figma `expected`. Do not edit `figma-pixel-implement` skill prose.

## When to use

- After `figma-pixel-implement` (or any Figma implement pass that left a durable inventory + spec **path**)
- User asks to check pixel alignment / design fidelity / 对照稿面验收
- Standalone: user provides Figma URL + running preview URL/route; persist a minimal inventory + spec to the same path convention **before** measuring

## Inputs

1. **Living artifact** — File path from implement. Same columns as implement reference (`state`, `mode`, `basis`). After an implement run this session, do **not** silently rebuild a missing table and claim that handoff complete—FAIL and return to `figma-pixel-implement`.
2. **Runnable UI** — Document surfaces, preferred first: a component-workbench story from the living artifact’s Stories subsection (or a detected Storybook-style workbench) → a lightweight isolated harness (stub out host/engine dependencies) → the in-product preview route → a full app/browser launch (heaviest, last resort). Surfaces with no computed-style API use `layout-probe`: a command that mounts the control in the shipping parent (the container the screen uses), runs layout, and prints frames. A command that lays out the control with no parent is not a measurement.
3. **Running-UI screenshot** when the channel can open a UI (`storybook`, `isolated-harness`, `preview`, `full-app`): save a png, jpg, jpeg, or webp of that UI this run and cite its path. A `layout-probe` that cannot open a UI records `Screenshot: not-openable` and does not invent an image. The image is supporting evidence. It does not replace numeric checks.

## Workflow (ordered)

1. **Preflight** — Resolve the measurement channel per the ladder in [reference.md](reference.md). Document UIs: Stories-subsection story → detected component workbench → in-product preview → full app launch (last resort). Surfaces with no computed-style API, or with every document rung unavailable: `layout-probe` — a command this run executes that mounts the control inside the shipping parent (the same container the screen uses), runs one layout pass, and prints the control's width, height, and child frames. A command that lays out the control with no parent is not a measurement. Build the smallest probe the project toolchain can run when none exists, then run it. If no workbench exists, make one advisory adoption suggestion; if the workbench is broken, fall down the ladder and record it; declare the channel in the report (`storybook | isolated-harness | preview | full-app | layout-probe`). Confirm the chosen channel is reachable. Resolve `Spec source` (living-artifact path). The Inventory plus Spec **is** the list of rows to measure. If this run already implemented from Figma and the file is missing or critical rows are absent: Overall **FAIL**, return to `figma-pixel-implement` to complete the table—do not invent rows and claim handoff complete. If this is **standalone** (no implement this run): persist a minimal inventory + spec using implement’s path convention, then measure. Note theme scope (`mode`) and visual `state`s. When multiple themes are in scope, identify how the running UI switches themes (`data-theme`, toggle, system preference) before measuring. **Browser channel (quality gate):** On macOS, if the `ego-browser` skill (or its install script) is available and the CLI is already usable, or the install finishes in this turn without waiting on a person, use it before other document channels. If install still needs GUI onboarding, record that and continue with the next reachable JS-eval or layout-probe channel in this turn. Do **not** copy that product’s TaskSpace/CLI API into this skill. If the OS is not macOS, the skill/install path is absent, or install is blocked, continue with another channel and record which one was used. Missing `ego-browser` does **not** abort verify.
2. **Source reconciliation (gate)** — Before any measurement, mechanically derive the expected-item list from the Figma source (fetched node-tree data and/or the reference exports): every in-scope node's position, size, typography set, container properties, and sibling gaps becomes an expected item. Reconcile it against the Spec table — every expected item MUST be covered by a spec row or listed as `out-of-scope` with a reason; gaps MUST be added as new spec rows (they become rows to measure in this run) or explicitly marked `out-of-scope`. Write the reconciliation table (expected items / covered / added rows / out-of-scope) into the Verify report. Measurement MUST NOT begin before reconciliation completes. When an in-scope frame lacks its reference export, overall is FAIL and control returns to `figma-pixel-implement`.
3. **Vision** — When the model can inspect images, capture UI vs Figma screenshot; note gross mismatches (wrong component, missing block, theme drift, fragment-cut / stacking look). Vision is supporting evidence. When JS-eval or a layout probe can run, vision-only comparison does **not** produce Overall PASS. On an openable channel, keep the saved running-UI file and cite it. On a layout probe that cannot open a UI, record `not-openable`.
4. **Pixel differential sweep** — Compare each reference export against this run's implementation screenshot as a same-box side-by-side (and a per-pixel difference artifact when the toolchain allows); inspect region by region. Every observed difference becomes either a new measured row or a recorded residual — differences found outside the spec table are this sweep's legitimate product. Save the sweep artifacts (side-by-side and/or diff images) and cite their paths in the report; for an openable channel without sweep artifacts, overall is not PASS.
5. **Numeric measurement** — For each critical visual row, switch the running UI into that row’s `state` and `mode` (prefer a real pointer hover/click/theme control through the browser channel — a declarative story entry (test id, knob, auto-action) counts as reaching the state — then read **computed style** and/or **bounding box**). On `layout-probe`, actual is the printed frame from that command. A source literal written to match `expected` leaves the row unmeasured. Map selectors carefully; prefer stable test ids when present. Default-state readings do not satisfy a hover (or other state) row. Shipped-reference interactions: when the task text contains `figma.com` or `node-id=` and also `参考`, `match the existing`, or `same as`, read the named existing control's authored rules for hover, focus, focus-within, and open or expanded. Each property that differs from the resting rule becomes a spec row with that `state`. A resting-frame reading does not pass those rows. A probe that only checks text, visibility, or item count does not measure them. Per-mode rows under different themes are separate verdicts. Skip numeric PASS claims for `out-of-scope: behavior` lines — list them as behavior, not pixel PASS. For every multi-line text node in scope, measure beyond the box: line count, each line's ink start position (the rendered left edge of its first visible character), the break content, and any hanging indent or in-line offset — record them as rows; a box-only reading does not count as coverage for a multi-line node's alignment.
6. **Compare** — Apply tolerances in [reference.md](reference.md). Assign a **verdict** per row. Unmeasured critical visual rows (JS-eval was available but the row was skipped) are blocking, not a path to Overall PASS via residuals.
7. **Fix loop** — On a non-pass row, fix the running UI and remeasure in this run, then update actual/verdict columns. Continue until overall PASS or the measurement command cannot be executed. Safety cap: about **8** iterations; hitting the cap is overall FAIL with residuals listed. When the measured box matches a platform control’s intrinsic size and not the spec, the next iteration switches that control to `custom-layout` and assigns the spec frames in the layout pass. Do **not** change Spec `expected`. Do **not** patch `figma-pixel-implement` skill files. Do **not** pause for a person to judge pixels.
8. **Independent re-check** — Before writing overall PASS, obtain an independent re-check: a fresh-context agent run, a different model, or a blind re-source check that re-derives the expected-item list from the Figma source without consulting the author's Spec table. Record the method, the re-checker identity, and its artifact path as an `Independent check:` line in the report. When no independent channel is available, record the attempted methods and the unavailability reason — never claim a check that did not run.
9. **Report** — Write the Verify section of the living artifact (or the sibling report named in Spec source). Template: [reference.md](reference.md). Include coverage (measured vs inventory), the **channel declaration** (`Channel: storybook | isolated-harness | preview | full-app | layout-probe`), and, when the project declares a host engine older than the workbench browser, an optional note of that difference. The note does not withhold geometric PASS and does not create a human step. Rows that depend on that engine's syntax are measured with a runtime or parser at that floor, or they stay unmeasured and overall is not PASS. Component-test results may be cited as supporting evidence. For multi-theme scope, report per theme. That Verify section **is** the measured report hosts require. Overall is **PASS** only when every critical visual row in scope is PASS or `accepted-residual` and each actual cites a laid-out read from this turn, **and** the Source reconciliation table is present and complete, **and** the pixel-differential-sweep artifacts are cited, **and** the `Independent check:` line is present (or its recorded unavailability with attempted methods). Overall is **not PASS** if any critical row is unmeasured, `MISSING-style`, unaccepted `DRIFT`, `HARDCODED` when the spec required a token, the spec itself is incomplete, actual was copied from a source literal, or the running UI shows an **invented solid fill** against Spec transparent/`none`, a **fragment-cut** graphic against a single Assets export, a **generic wrapper** that does not match instance geometry, a **self-invented text-color alias** when Spec recorded a Figma variable, or a visible graphic still on a **remote design URL**. When the probe command cannot run, overall is **FAIL** and the report names that command. Before reporting PASS, run `scripts/check-figma-verify-report.mjs` in this skill directory on the living artifact. Exit 0 is required. The Verify section must include `Mounted in`, `Measurement command`, `Screenshot`, and a `### Measurement excerpt` code block whose text contains every passing row's actual numbers and colors. For `storybook`, `isolated-harness`, `preview`, and `full-app`, `Screenshot` is a path to a non-empty png, jpg, jpeg, or webp saved this run. For `layout-probe` that cannot open a UI, `Screenshot` is `not-openable`. The checker resolves a relative path from the report file's directory and rejects a missing or empty file. A screenshot file does not replace the numeric pass.

## Verdict taxonomy

| Verdict | Meaning |
|---------|---------|
| **PASS** | Within tolerance of expected, measured in the correct `state` / `mode` |
| **DRIFT** | Measurable but outside tolerance |
| **HARDCODED** | Value matches by luck or literal, not via project token/variable when the spec required a token — flag when token mapping was part of the contract |
| **VARIANT** | Matches a different documented variant (e.g. hover/dark) than the requested one |
| **MISSING-style** | Property not measurable (no node, no style, or channel unavailable) |
| **accepted-residual** | Explicit frozen deviation (owner + reason). Not PASS against the Figma expected |

## Tool intent (platform-agnostic)

| Intent | Agent may use |
|--------|----------------|
| Open/preview UI | Quality channel after the macOS install gate; otherwise another JS-eval / preview channel the Agent already has |
| Switch visual state | Real pointer hover/click/theme control, then read styles |
| Read laid-out frames | JS evaluate in page, DevTools-like APIs, or a layout-probe command that prints frames |
| Screenshots | Browser or Figma screenshot tools (vision inspects them when the model can see images) |
| Apply fixes | Native edit tools, then re-measure |

After a successful quality-channel install, use that channel for measurement. When install is impossible, another JS-eval path is valid. Do not copy a third-party browser API into this skill.

If **no** document channel exists, run a layout probe and read its printed frames. If that command cannot be executed, label numeric rows **MISSING-style**, name the missing command, and **do not** claim pixel PASS.

## Relationship

| Skill | Boundary |
|-------|----------|
| `figma-pixel-implement` | Produces code + durable Inventory/Spec; does not own final verdict |
| Agent-native Figma→code guidance / MCP fetch | Not a substitute for measurement |
| Host PDCA workflows | Strong-depend at install; invoke when Figma UI is in scope; missing Verify section (or Spec source sibling) fails that verification stage; spec-gap FAIL re-enters implement |
| `ego-browser` (external, macOS) | Quality measurement channel: install when the skill/install path exists; not a frontmatter dependency; degrade when not installable |

## Pitfalls

- Declaring PASS from screenshots alone when measurement was possible.
- Infinite tweak loops without re-measure.
- Treating ±1 CSS px geometry noise on high-DPR as failure without noting DPR.
- Silent skip of mask/currentColor issues — if implement violated asset rules, call that out as root cause of color DRIFT.
- Marking per-mode rows PASS after measuring only the default theme — each theme in scope is measured under its own theme.
- Marking hover rows PASS from default-state styles.
- Overall PASS while critical rows sit only in residuals as “not measured yet”.
- Treating a frozen 18px vs 16px as PASS instead of `accepted-residual`.
- Keeping the report only in chat when a living-artifact path exists.
- Overwriting Spec `expected` with measured actuals.
- After this-run implement: silently rebuilding a missing spec and claiming the handoff was complete.
- Marking PASS for an invented solid fill, stacked leaf-path icon, generic 16/24 shell, invented text-color alias, or remote design URL.
- Skipping a usable quality-channel CLI on macOS, then measuring only through a weaker document channel.
- Waiting on GUI onboarding while another channel or a layout probe can run in this turn.
- Treating a source literal that matches `expected` as a measured actual.
- Copying a third-party browser TaskSpace/CLI API into this skill.
- Aborting verify because `ego-browser` is unavailable on a host that cannot install it.
- Declaring Overall PASS from vision/screenshots alone when JS-eval was available.
- Reporting a verdict without declaring the measurement channel used.
- Treating a workbench/engine-floor note as a reason to withhold geometric PASS or to ask a person to finish those rows.
- Treating a layout command that never mounts the shipping parent as a measurement.
- Reporting PASS for an openable channel without a saved non-empty screenshot file.
- Inventing an image for a layout probe that cannot open a UI.
- Skipping source reconciliation — the measured set then equals whatever the author remembered to write down.
- Reporting PASS without differential-sweep artifacts on an openable channel.
- Treating same-context self-review as an independent re-check.
- Measuring a multi-line text node's box only and calling its alignment covered.
