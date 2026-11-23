---
name: react-feature-architecture
description: Set up, complete, or extend a Vite + React frontend (JavaScript or TypeScript) using a Feature-Based (Hybrid) folder architecture with Tailwind CSS v4, shadcn/ui, Redux Toolkit + RTK Query (injectEndpoints, centralized response adapter, 401 → single-flight token refresh), cookie- or body-based refresh tokens, session restore on reload, react-router guards with safe redirects, lazy routes with retry + error boundary, react-hook-form + zod, sonner, and i18next (en/hi). Use when the user asks to scaffold a React frontend, restructure or adopt this architecture in an existing React project, add a feature/module/page to a project that follows it, set up login/auth with access + refresh tokens, or generate the project's CLAUDE.md for this architecture.
---

# React Feature-Based (Hybrid) Architecture

Build or extend a React app so that business code lives in self-contained `features/`, server state lives only in RTK Query, and auth (login, refresh, expiry, restore, redirects) works the same way in every project. Work **with the project as it is**: inspect first, propose, get approval, change only what was approved, and verify with real commands.

## References (read when the phase says so)

| File | Use it for |
|---|---|
| `references/inspection-guide.md` | Phase 1: what to detect, the component inventory, mode classification, conflict handling, the proposal format |
| `references/architecture.md` | Folder rules, mandatory vs recommended, import direction, naming, the "add a feature" example. **Read it before creating files.** |
| `references/code-templates.md` | JS starter templates for every infrastructure file |
| `references/typescript.md` | TS config differences, typed versions of the tricky files, conversion rules |
| `references/auth-and-security.md` | Auth flow, cookie vs body trade-offs, token storage, the backend contract with example responses, security rules, limitations |
| `references/testing.md` | Optional Vitest suites for auth/refresh/redirect/lazy-loading behavior |
| `references/quality-checklist.md` | Phase 5 self-check |
| `references/claude-md-template.md` | Phase 4: the project's `CLAUDE.md` |

The templates are **starter templates**. They were verified once in a fresh Vite app (see the status line at the top of `code-templates.md`), but they aren't proven in the target project until Phase 5 passes there.

## Phase 1: Inspect (read-only)

Follow `references/inspection-guide.md`:
- Locate the app root and source root.
- Detect the package manager, Node version, JS/TS, installed versions, and the scripts (build, lint, typecheck, test, plus which linter).
- Inspect the existing routing, store/API layer, auth, theme, i18n, Tailwind/shadcn setup, env usage, and tests.
- Build the 17-item architecture inventory, marking each item present, present-different, or missing.
- Classify the project: **Setup (scaffold / adopt / complete)**, **Extend**, or **Ambiguous**. A partial architecture is "Setup (complete)": add only what's missing. If it's ambiguous, ask; don't guess.

Don't modify anything in this phase.

## Phase 2: Propose, then STOP

Send the proposal in the inspection-guide format: what was detected, the mode and why, what gets reused, added, and modified, what gets installed (only what's missing, with the project's package manager), breaking or risky changes, and each conflict with a proposed resolution (keep, adapt, migrate, or remove).

**Wait for the user's approval.** Never overwrite, delete, or recreate existing infrastructure without it.

## Phase 3: Ask only what the project can't answer

Use AskUserQuestion for the decisions below, and only those that inspection didn't settle:
- **Refresh-token transport: httpOnly cookie or response body.** Always ask, never assume. In body mode, also ask about `localStorage` vs memory. Explain the trade-off (`auth-and-security.md` §4).
- **Access-token persistence across reloads.** The default is memory only, with restore through refresh. Persist only if the user explicitly wants it, after explaining the risk (§5).
- **JS or TS**, but only if the project is empty or mixed.
- **UI/styling or i18n**, but only if the project already uses something different (keep theirs, or migrate?).
- **Routing style**, but only if no router exists yet. The default is `BrowserRouter` + `<Routes>`. Keep an existing data router.
- **Backend contract** (base URL, paths, response shapes), if the user knows it. Otherwise use the placeholders and list them in the report.
- **Test tooling**, only if the project has none and you'd add Vitest.

If the backend has no refresh endpoint, stop and discuss it. The template design assumes one.

## Phase 4: Implement (approved changes only)

1. **Scaffold only if the project is empty.** Run `npm create vite@latest <dir> -- --template react` (or `react-ts`) with `--no-interactive`. Recent create-vite asks questions otherwise. Never scaffold on top of existing files.
2. **Install only missing deps**, with the project's package manager: `@reduxjs/toolkit react-redux react-router-dom react-hook-form zod @hookform/resolvers sonner i18next react-i18next date-fns lucide-react` and `-D tailwindcss @tailwindcss/vite`. Add `redux-persist` only if persistence was approved. Don't hand-install clsx/tailwind-merge; `shadcn init` installs whatever its `cn()` needs.
3. **Configure in this order:** Tailwind v4 plugin + `@import "tailwindcss"` → `@/*` alias in the bundler **and** jsconfig/tsconfig (`typescript.md` covers `baseUrl` on TS 7) → **`npx shadcn@latest init`**.
   - **Never hand-write `components.json`.** Without `init`, the CLI skips `lib/utils` and the theme CSS, and can miss dependencies.
   - Current CLIs (verified with 4.23) take `-t vite -b radix -p <preset>`. The presets are `nova`, `vega`, `maia`, `lyra`, `mira`, `luma`, `sera`, `rhea`; `-b radix -p vega` produced style `radix-vega`.
   - `-d` means the Next.js template, so don't use it for Vite.
   - Classic `new-york` is no longer a preset. Ask the user which preset they want. If they insist on `new-york`, it still installed correctly when set in `components.json` after `init` (CLI 4.23), but treat it as legacy.
   - Then run `npx shadcn@latest add button input label card form sonner`. If `form` isn't in the registry, use `field` + react-hook-form `Controller` and say so.
4. **Write the files** from `code-templates.md` (or `typescript.md`): config/constants → utils → api (responseAdapter → tokenRefresh → baseApi) → store → auth slice/api/AuthGate → routes → layout/loaders/theme/toaster → i18n/locales → main/App → the auth pages. Set `constants/auth` to the Phase 3 answers.
   - **Existing files:** edit them in a targeted way, and merge configs (`vite.config`, `.gitignore`, `main`) instead of replacing them.
   - **Existing equivalents:** reuse them (theme provider, i18n init, router, layout) and adapt the templates to them.
5. **Sonner and theme:** read the generated `components/ui/sonner.*` first.
   - If it spreads `{...props}` after its `theme` prop, mount `layout/AppToaster` (it passes `theme`) and don't edit the ui file.
   - Otherwise, make the smallest edit or ask, and report it.
   - Reuse an existing theme provider if there is one.
6. **Auth must be real.** No mocked success, no hard-coded users, and real network errors shown to the user.
7. **Write `CLAUDE.md`** from `claude-md-template.md`, filled with real values. If one already exists, merge into it.
8. Create `.env.example` (`VITE_API_BASE_URL=`) and make sure `.env` is gitignored.

## Phase 5: Verify (real commands, real output)

Run whatever the project has, using its package manager:
1. **Install:** a clean install.
2. **Build:** run `build`, and fix every error and unresolved import.
3. **Lint:** run `lint` with the project's linter (ESLint, oxlint, or Biome). Fix the errors. `only-export-components` warnings in `components/ui/*` are expected.
4. **Type check (TS):** `tsc -b` or `tsc --noEmit`.
5. **Tests:** run them if present or approved (`testing.md`).
6. **Smoke test (optional):** `vite preview`, then fetch `/` and `/login` and expect 200. Stop the server afterwards.
7. **Checklist:** go through `quality-checklist.md`, including the import-direction greps.

If a check can't run (no script, no network, a missing tool), say exactly why. Never claim something was tested, verified, or production-ready unless the relevant check passed in this project. Never claim browser-level behavior you didn't observe.

## Phase 6: Final report

Report:
- **Files created** and **files modified** (with a one-line reason each).
- **Dependencies added**, with versions.
- **Architecture decisions:** mode, transport, persistence, reused vs replaced pieces, and any approved deviations (including ui-file edits).
- **Verification:** each command with its real result (pass/fail plus key output lines), and checklist items marked verified or not verified.
- **Known limitations** (see `auth-and-security.md` §8).
- **Remaining manual configuration:** `VITE_API_BASE_URL`, the endpoint paths, the response shapes in the adapter, 401 semantics, the refresh contract, and CORS/cookie settings for cookie mode.

## Extend mode: adding a feature

Follow the project's `CLAUDE.md` first. If it conflicts with this skill, the project wins; mention the difference.
1. Create `src/features/<kebab-name>/` with only the subfolders it needs.
2. Write `<name>Api` via `baseApi.injectEndpoints`, with tags. Add any new tag types to `baseApi.tagTypes`. Use `transformResponse: unwrapData` when the backend wraps responses.
3. Add pages with loading, error, and empty states; feature-only components; and `schemas/<name>Schema` factories taking `t`.
4. Add a lazy route in `routes/AppRoutes` + a `ROUTES` constant (+ `PRIVATE_NAV` if it's in navigation), wrapped in `PrivateRoute` if it needs auth.
5. Add a slice only for client state, and register it in `app/store`.
6. Add the locale namespace in `en` + `hi`, registered in `i18n`.
7. When a second feature needs something, move it to `shared/` and update both imports.
8. Run build, lint, typecheck, and tests, and report the real results.

## Non-negotiables

- `import.meta.env` is read only in `config/env`.
- `api/` holds only `responseAdapter`, `tokenRefresh`, and `baseApi`, and never imports `features/` or `shared/`.
- Backend response shapes are known only to `api/responseAdapter`.
- Server data lives in RTK Query; slices hold client or session state only.
- One refresh path, single-flight, never for login, refresh, or logout. At most one retry per request.
- No tokens, passwords, or auth responses in logs. Refresh tokens never go into Redux or the RTK Query cache.
- Redirects are state-driven via the guards, and always go through `getSafeRedirect`.
- Every route page uses `lazyWithRetry`; the chunk-reload guard can never loop.
- Use the `@/` alias, follow the import-direction rules, and don't create duplicate files or second patterns without approval.
