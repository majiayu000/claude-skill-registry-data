---
name: prompt-app-builder
description: Build or update commercial-studio embedded prompt mini apps from a user-provided preset prompt. Use when the user gives a reusable image prompt/template, asks to package it as an app/小应用/内置提示词/模板化生图入口, or wants future preset prompts converted into high-quality project-native prompt apps in apps/public-web.
---

# Prompt App Builder

## Purpose

Turn a user-provided preset prompt into a project-native mini app under `apps/public-web/src/features/prompt-apps/`. Keep the full prompt hidden, expose only the variable fields users need, and submit through the existing public image job API. Treat `prompt-apps.ts` as the catalog surface, not as the long-prompt storage layer.

## First Decisions

Extract these from the user's prompt before editing code:

- **App name**: short Chinese title, e.g. `科普百科图`.
- **Slug**: lowercase kebab-case route segment, e.g. `encyclopedia-card`.
- **Primary variable**: usually the placeholder inside `{...}`, e.g. `{狸花猫}` means required field `topic`.
- **Optional fields**: usually `note`/备注 unless the prompt clearly needs more fields.
- **Mode**:
  - Use `generate` by default.
  - Use `edit` with uploaded `source_asset_id` only when the user explicitly wants generation based on a supplied image.
- **Count**: default `requested_count: 1` unless the user explicitly asks for multiple outputs.

If the prompt contains unsafe sexualization, minors, non-consensual, violent, or deceptive content, do not encode it directly. Offer a safe non-sexual template variant and continue only with acceptable wording.

## Project Files

Use the existing prompt app structure:

- Catalog and light prompt exports: `apps/public-web/src/features/prompt-apps/prompt-apps.ts`
- Long prompt builders: `apps/public-web/src/features/prompt-apps/<slug>-prompt.ts`
- Shared generate-only scaffold when multiple apps share the same shape: `apps/public-web/src/features/prompt-apps/prompt-image-generate-app.tsx`
- Shared result panel when the same output UI is reused across apps: `apps/public-web/src/features/prompt-apps/prompt-app-result-panel.tsx`
- App center: `apps/public-web/src/features/prompt-apps/prompt-apps-home.tsx`
- Shared CSS: `apps/public-web/src/features/prompt-apps/prompt-apps.module.css`
- App cover assets: `apps/public-web/public/app-covers/<slug>.*`
- Existing result panel: `apps/public-web/src/features/prompt-apps/character-poster-result-panel.tsx`
- Existing example page: `apps/public-web/src/features/prompt-apps/character-poster-app.tsx`
- Existing route pattern: `apps/public-web/src/app/apps/<slug>/page.tsx`
- Public API: `apps/public-web/src/lib/public-api.ts`
- Image upload pattern when needed: `apps/public-web/src/features/home/generation-prompt-image-upload.tsx`

Do not change backend APIs unless the requested app cannot be represented by the existing `/image/jobs` and `/image/uploads` flow. Do not fake uploads, generated results, or fallback success.

## Implementation Workflow

1. **Explore context**
   - Read `AGENTS.md` and `apps/public-web/AGENTS.md`.
   - Read the existing prompt app files listed above.
   - Check `git status --short` and preserve unrelated changes.

2. **Write a short design and plan**
   - Save a design doc to `docs/plans/YYYY-MM-DD-prompt-apps-<slug>-design.md`.
   - Save an implementation plan to `docs/plans/YYYY-MM-DD-prompt-apps-<slug>.md`.
   - Keep docs concise: goals, non-goals, route, fields, data flow, tests.

3. **Use TDD**
   - Add or update tests first.
   - Run the narrow test and confirm it fails for the expected missing behavior.
   - Implement the smallest code change.
   - Re-run the narrow test and confirm it passes.

4. **Catalog and prompt builder**
   - Add an item to `PROMPT_APPS`:
     - `id: "<slug>"`
     - `title`
     - concise `description`
     - `href: "/apps/<slug>"`
     - `statusLabel: "内置提示词"`
     - `access: "public-image-job-api"`
   - Add a typed prompt input, e.g. `<Name>PromptInput`.
   - Add `build<Name>Prompt(input)`.
   - Export the builder from `prompt-apps.ts` so tests and callers keep one public surface.
   - Keep long fixed prose out of React pages and out of the catalog file; place it in the dedicated prompt builder file.
   - Convert `{placeholder}` to a required form field line:
     - `【主题】= {${topic}}（${note}）`
     - Omit the parenthesized note when empty.
   - When adding a second app with the same `topic / note / modelCode` shape, reuse or extract a shared scaffold instead of copying model loading, submit, polling, and error handling again.
   - If the preset prompt is long or likely to grow past a single screen, keep it in `apps/public-web/src/features/prompt-apps/<slug>-prompt.ts` and import it from the catalog file.
   - Add a matching cover asset under `apps/public-web/public/app-covers/`; default to a 3:4 portrait cover unless the app is explicitly landscape.

5. **State helper**
   - Create `apps/public-web/src/features/prompt-apps/<slug>-app-state.ts`.
   - Export:
     - `canSubmit<Name>()`
     - `build<Name>ImageRequest()`
     - `<Name>State`
     - `get<Name>ErrorMessage()`
   - Use explicit request shape:
     - `prompt`
     - `model_code`
     - `requested_count`
     - `mode: "generate"` or `mode: "edit"`
     - `source_asset_id` only for image-reference apps.

6. **React page**
   - Create `apps/public-web/src/features/prompt-apps/<slug>-app.tsx`.
   - Create `apps/public-web/src/app/apps/<slug>/page.tsx`.
   - Reuse the existing quiet workspace design:
     - `<AppShell activeHref="/apps" headerTitle="<title>" leadingAction={<PromptAppBackLink />} workspaceMode>`
     - `styles.posterWorkspace`
     - `styles.posterPanel`
     - `PosterResultPanel` or a shared prompt-app result panel when the output UI is identical
     - same model loading, empty, and error labels.
   - Required fields should disable submit until valid.
   - Keep page components thin: they should wire config, state, and copy, not host the full prompt text.
   - For upload/reference-image apps, reuse `publicApi.uploadImageAsset(file)` and store `{ assetId, assetUrl, mimeType }`; do not continue silently after upload failure.

7. **Styling**
   - Reuse `prompt-apps.module.css`.
   - Add only shared, necessary classes.
   - Keep cards/panels at 8px border radius where this feature uses framed controls.
   - Keep text compact and readable on mobile; do not introduce a new visual language.

8. **Tests**
   - Update `apps/public-web/tests/prompt-apps.test.mjs` for metadata and prompt builder.
   - Add `apps/public-web/tests/<slug>-app-state.test.mjs`.
   - Add `apps/public-web/tests/<slug>-page.test.mjs`.
   - For hidden prompts, assert the React page source does not contain long fixed prompt phrases.
   - Assert the long prose lives in the builder module, not the page module.
   - Assert catalog cover metadata and cover asset existence; for PNG check dimensions, for SVG check the file exists and declares a stable viewport.
   - For image-reference apps, assert request mode/source asset behavior.

9. **Verification**
   - Run the narrow tests during TDD.
   - Run:
     - `pnpm --filter public-web test`
     - `pnpm --filter public-web typecheck`
     - `pnpm --filter public-web lint`
   - Check fixed public port:
     - `lsof -nP -iTCP:7700 -sTCP:LISTEN`
   - If 7700 is already running, smoke check:
     - `curl -sS -o /tmp/<slug>.html -w "%{http_code}\n" http://127.0.0.1:7700/apps/<slug>`
     - `curl -sS -o /tmp/apps.html -w "%{http_code}\n" http://127.0.0.1:7700/apps`
     - Inspect the saved HTML with targeted `rg` or `grep -q`; do not dump the whole page to the terminal.
   - If 7700 is not running, start only with `pnpm dev:public`; do not switch ports silently.
   - Run `wc -l` on touched feature and test files before finalizing; split files that approach the project line limit instead of adding one more copy-pasted page.

## Quality Rules

- Keep user-facing replies in Chinese unless asked otherwise.
- Do not expose the full prompt template in the UI.
- Do not add mock success paths, silent fallbacks, caps, or fake generated data.
- Surface backend and upload failures as explicit errors.
- Keep functions under 50 lines and files under 300 lines; split helpers when needed.
- Prefer generic names for shared prompt-app components once they are reused by more than one app.
- Treat `apps/public-web/src/features/prompt-apps/prompt-apps.ts` as a registry and type surface, not a dumping ground for long narrative prompts.
- Avoid broad refactors. Touch only prompt-app feature files, tests, route files, and the plan docs needed for the app.
