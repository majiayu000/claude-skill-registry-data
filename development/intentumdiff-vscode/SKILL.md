---
name: intentumdiff-vscode
description: >-
  Architecture of the IntentumDiff VS Code extension (native-first). Use this whenever you work
  in `plugins/vscode/` — the diff surfaces, CodeLens/Peek/decorations, the review panel
  webview, intent explanation, content classes, the Semantic Changes tree, theme styling, or
  privacy/BYOK plumbing. It tells you which file owns what, the native-diff-not-Monaco rule,
  the theme-native and privacy invariants you must not break, and how to build/test/verify the
  extension (including the panel-render harness). Read intentumdiff-architecture first; hand off
  to intentumdiff-release-notes for notes/intent-"why" and intentumdiff-perceptual-asset-diff for
  images. Trigger on any extension UI work even if the user doesn't name a file.
---

# IntentumDiff — VS Code Extension (native-first)

The extension is TypeScript, compiled with `tsc` only (no bundler). It consumes the engine
over the LiveServer protocol (`intentumdiff live-server --stdio`, protocol v2) and renders
intent natively in the editor plus one review webview.

## Native-first diff (do not rebuild a diff editor)

The **native VS Code diff editor is the primary surface**:
- Open with `vscode.diff`: left = read-only `intentumdiff-base:` document
  (`git show <ref>:<path>` via a content provider), right = the **real working-tree file**
  (editable). Native `diffEditor.hideUnchangedRegions` handles collapse/expand.
- Editing the right pane re-runs the engine (debounced `scheduleDocument → diffDocument →
  handleDiff` in `extension.ts`) and refreshes intent live.
- **Do NOT** reintroduce Monaco, `createDiffEditor` webview embeds, the `media/monaco/`
  bundle, or the retired gap machinery (`gapStates`, `expandGap`/`collapseGap`, floating
  chevrons, per-side `setHiddenAreas`).

Intent is surfaced via **CodeLens + Peek + decorations**, not a bespoke editor.

## File map (what owns what, all under `plugins/vscode/src/`)

| Area | Files |
|---|---|
| Extension entry, live-diff wiring, commands, base content provider | `extension.ts`, `baseUri.ts`, `protocol.ts`, `gitStatus.ts` |
| CodeLens / Peek / hover / inlay (intent on the diff) | `intentCodeLens.ts` (pure logic), `intentCodeLensProvider.ts` (vscode provider) |
| Intent "what/why/risk" (deterministic) | `intentExplain.ts` |
| LLM explainer (BYOK / vscode-lm) | `intentLlmExplainer.ts`, `intentLlmPrompt.ts` |
| Release notes | `releaseNotes.ts` (see intentumdiff-release-notes) |
| Content class (code/docs/config/data/text) | `contentClass.ts` |
| Change → review entry mapping | `mapper.ts`, `reviewModel.ts` |
| Semantic Changes tree | `reviewTree.ts` |
| The one review webview (Intent / Release Notes / Evidence / Diagnostics + semantic diff + asset diff) | `reviewWebviewModel.ts` (model + HTML), `reviewWebview.ts` (controller) |

## The review webview (`reviewWebviewModel.ts`)

One webview, four tabs: **Intent**, **Release Notes**, **Evidence**, **Diagnostics**, plus an
editable semantic-diff view with per-hunk staging, and the **perceptual asset diff** for
images. Key model builders: `buildReviewPanelModel`, `renderPanelHtml`, `dashboardEntry`
(attaches an `IntentExplanation` per entry), `entryCard`, `assetModeViewer`.

Risk is *derived* (see `intentumdiff-engine`): `MEANINGFUL→Behavior`, `REFACTORING/MOVED→
Internal`, non-code content → `Content`, style/noise excluded, guardrails → critical.

## Content classes (`contentClass.ts`)

Non-code files must not get code framing. `contentClassForDiff(diff)` →
`code | docs | config | data | text` from language + `metadata.content_type.category` +
code-node detection. Drives: relabel `MEANINGFUL` → Docs/Config/Data/Content, risk `content`
(not "Behavior"), and suppresses code phrases ("New public API", function nouns) on prose/
config. A `.gitignore` line addition must read as a Content edit, never "Behavior".

## Ungrouped-change handling (ties into the engine's index-space contract)

A change owned by no `change_group` is a real ungrouped change, not evidence to bury.
`coveredChangeIndices(groups, count)` (in `intentCodeLens.ts`) unions in-range group indices;
`intentForLine`, `buildIntentLenses`, `releaseNotes.buildReleaseNotes`, and
`reviewModel.reviewEntriesForFile` all fall back per-change via `kindForChange`. In the tree,
`reviewEntriesForFile` **promotes** ungrouped changes to first-class Meaningful/Refactor/Moved
entries when a *modified* file has no shown intent groups (the ungrouped changes are the
story), and otherwise leaves them in the collapsed "Raw evidence" bucket. See
`intentumdiff-engine` → `references/index-space-contract.md`.

## Theme-native styling (hard rule)

Bind to the editor theme, never a bespoke palette:
- Chrome uses `--vscode-*` variables; change categories use the contributed
  `intentumdiff.semanticChanges.*` color IDs (+ `--vscode-diffEditor-*` for line backgrounds).
- **No hardcoded chrome hex literals. No bundled Google Fonts / JetBrains Mono `<link>`s** —
  use the editor's font vars. Must read in Dark+, Light+, and High-Contrast.
- **Codicons only** (`codicon codicon-*`); never ship custom chrome SVG for icons.
- **Guardrail reality (verify, don't assume):** `test/themeColors.test.ts` checks that the
  contributed `intentumdiff.semanticChanges.*` color IDs exist in `package.json` and that
  overview-ruler decorations use them — it does **not** scan the rendered panel/diagnostics HTML
  for chrome hex literals or custom SVG icons. That gap is real: `reviewWebviewModel.ts`
  `styles()` and `extension.ts` `renderDiagnosticsReportHtml` currently ship a bespoke dark
  palette (100+ hardcoded hex) + a custom `iconSvg` chrome icon set, and `color-scheme:dark`
  — a standing theme-native violation the test does not catch (tracked in `docs/BACKLOG.md`).
  When you touch these surfaces, migrate to `--vscode-*`/codicons and add the missing HTML hex
  scan to the test; don't trust the test's name to mean it's enforced.

## Privacy / BYOK (hard rule — see also `plugins/vscode/PRIVACY.md`)

- Never bundle an API key or run a paid proxy. The LLM explainer is opt-in
  (`intentumdiff.intent.explainer: "llm"`), BYOK or `vscode-lm`/Copilot.
- Keys live in VS Code **SecretStorage**, never settings.json. A cloud consent modal precedes
  any send.
- Default `codeSharing: "signatures"` sends a locally-derived fact sheet (symbol/type names +
  structural facts, no bodies/literals). `"facts"` sends counts/enums/flags only. `"full"`
  (verbatim source) is allowed **only to a local endpoint** (Ollama/LM Studio/vLLM).
- **Unit tests do no network.**

## Build, test, verify

```bash
cd plugins/vscode
npm run lint          # tsc --noEmit
npm run test          # node --test on compiled out/  (unit; no network)
```
Integration tests gate on `INTENTUMDIFF_SKIP_LIVE_DIFF=1`.

**Panel-render harness (fast visual check without launching VS Code):** compile, then run a
small node script that imports `out/src/reviewWebviewModel.js`, calls `buildReviewPanelModel`
+ `renderPanelHtml` on a synthetic `ReviewFile`, writes `panel.html`, and serve it with
`python -m http.server` for the Claude Preview MCP. Stub `acquireVsCodeApi` and strip the CSP
meta so it renders in a plain browser. Use this to verify layout/overflow/interaction (swipe,
blink, lasso, hotspots) before manual reload.

Pure-TypeScript changes need **no** maturin/Rust rebuild.
