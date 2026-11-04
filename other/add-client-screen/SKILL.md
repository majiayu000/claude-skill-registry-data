---
name: add-client-screen
description: >-
  Add or change a screen in the Greenhouse universal client (apps/client: Expo web, iOS, Android,
  macOS shell): choose place vs sheet/inspector vs centered dialog (DIALOG_SIZES), build it from the
  DESIGN.md kit, wire routes under apps/client/app with .web/.ios/.android siblings, call the API
  through ApiResult helpers with identity-bound writes, add en+zh copy, cover it with React-free unit
  tests and tests/client-e2e, run the client checks. Covers core screens, Admin sections and official
  plugin glue. Use for: add a page / screen / dialog / Admin section / plugin native page, 加个页面,
  新增界面, 做个弹窗, 加个管理页, 加个后台页面, 客户端页面, 移动端页面. Red lines: never import
  @greenhouse/*, no raw hex or font sizes, objects open only through openObject.
---

# Add a client screen

Sources of truth: apps/client/DESIGN.md (layout, surfaces, kit, tokens) and apps/client/AGENTS.md (HTTP contract, data, platform rules). Read both first; they win on conflict.

## Before you start
- Missing endpoint: do add-api-route first; the client only calls what the station serves.
- Core screen or plugin page: core screens live in apps/client/app + src/<domain>/; plugin pages come from the station manifest (see Plugin surfaces).
- Reuse first: search src/ui, src/admin/kit.web.tsx and the domain folder; never build a parallel DOM app.

## Pick the surface
- Place: a rail area (Chat, Knowledge, Drive, Tables, Projects, Schedule; Admin for supers). A new core place needs a route under app/(drawer)/<place>/ and an entry in usePlaces() (src/shell/use-places.ts), the one source for rail, ⌘K and the desktop Go menu.
- Object: anything with an id opens through useOpenObject / useOpenHref (src/shell/open-object.ts): a sheet on phones, the inspector on wide screens, three deep at most. Never push a detail route by hand.
- New object kind: ref in src/shell/object-ref.ts, branch in open-object.ts, app/sheet/<kind>.tsx, Stack.Screen in both app/_layout.tsx and app/_layout.web.tsx.
- Centered dialog (web, not anchored): Overlay with a fixed size from DIALOG_SIZES (src/ui/overlay.web.tsx) and DialogBody inside.
- Sizes: sm 420 (confirm, prompt), md 560×600 (lists, short forms), lg 760×640 (documents, previews, long forms), xl 960×680 (settings window only). The box never resizes; the body scrolls.
- Centered route sheets on the web (src/ui/sheet-edge.web.tsx) use the same sizes (md by default); add the route to LARGE_SHEETS when it needs lg.
- Anchored menus and context menus: MenuPanel through NativeMenu (src/ui/menu*) or PlaceContext.
- Edits happen in a sheet or dialog: one title bar, scrolling body, Cancel + one primary action; Cmd/Ctrl+Enter submits; the page underneath never changes.
- The browser settings window (xl) holds personal settings only; apps go in the rail, administration in the Admin place.

## Routes and platform files
- Routes re-export screens: app/(drawer)/knowledge/index.tsx → src/knowledge/phone-screen.tsx, index.web.tsx → src/knowledge/place.web.tsx.
- Platform siblings are name.ios.tsx / .android.tsx / .web.tsx; the base file re-exports one (src/ui/dialogs.tsx re-exports dialogs.ios) so TypeScript and Expo Router resolve.
- Match the base file's extension (nav.ts → nav.web.ts); restart Metro after adding a platform file.
- Anything rendering @expo/ui/swift-ui needs a .android.tsx sibling; SwiftUI, Compose and native views never load in .web.tsx.
- Presentation is declared only in the app/_layout platform layouts with src/ui/nav presets; screens declare title and actions (useScreenActions / ScreenActions).
- Wide places portal secondary controls into PlaceSecondary (src/shell/place-secondary.web.tsx) and use Place, PlaceSidebar, PlaceRow, PlaceEmpty, PlaceContext (src/ui/place.web.tsx).

## Kit (DESIGN.md Components)
- Pages: Screen / SheetScreen (src/ui/screen.tsx); lists: Section, Row, Card, SectionHeader, SectionFooter (src/ui/list.tsx), rowPosition() for virtualized rows.
- States: EmptyState on phones, PlaceEmpty with icon + title (+ action) in wide places, Skeleton for a list's first load, LoadingState for small waits.
- Capsules: Chip for links, files and objects; Badge for status; Avatar for people, AssistantAvatar / AgentAvatar for agents; FileIcon for file kinds.
- Web controls: .gh-primary (one per surface), .gh-secondary-button, .gh-icon-button (needs aria-label), .gh-primary.gh-danger, .gh-form inside DialogBody.
- Native controls: NativeForm with FormNavRow, NativeButton; never Pressable plus Text, never JS-drawn headers, sheets or switches.
- Feedback: confirmAction, promptText, alertError (src/ui/dialogs); toast for success only; a failed load is EmptyState with retry.
- Icons: add to ICONS in src/ui/core.tsx, core.web.tsx and icon-map.ts, then run `python3 scripts/android-icons.py` in apps/client.
- Tokens: useTheme() in TS, var(--gh-*) in CSS (only variables the shell defines), typo / weight / space / radius from src/theme.ts, user colors through categoricalFor(), onAccent on the accent.

## Data and API
- Domain helpers live in src/api/<domain>.ts on get/post/patch/put/del (src/api/client.ts); they answer ApiResult<T> and never throw.
- Screen data: useResource (src/data/use-resource.ts) reloads on focus and drops answers from an old station or member.
- Every write and late answer is bound to the identity that started it: captureIdentity() (src/data/identity.ts); Admin sections use useWrite (src/admin/use-write.ts).
- 403 is a role/feature/capability gate (EmptyState, no retry); 404 is gone or not visible (src/data/access.ts).
- Optimistic writes roll back and say so with alertError.
- Never import @greenhouse/*: vendor shapes into src/shared (VENDORED files verbatim, checked by src/shared/vendor.parity.test.ts; greenhouse-types.ts is the hand-kept subset).
- Calling a new endpoint raises MOBILE_API (src/api/compat.ts) together with the server's MOBILE_API_LEVEL.
- Zustand selectors return stored values; derive filtered arrays with useMemo.

## Plugin surfaces vs core screens
- Declarative pages (entity-list, entity-detail, settings-form, embed) need no client code: the manifest drives /p/[plugin]/[page] and the Admin place.
- A native plugin page (manifest kind 'native' with screen + fallback_url) needs glue in src/plugins/<id>/index.ts exporting screen (NativeScreenEntry), listed in src/plugins/native-registry.ts.
- A plugin Admin section is a native page with parent: 'administration'; src/plugins/<id>/admin.web.tsx exports adminScreen (AdminScreenEntry), listed in src/plugins/admin-screens.web.ts.
- Core code (src/admin, src/shell) never names a plugin; the registries only aggregate entries.
- Nav labels stay short with a lucide icon name; map unknown names in pluginIcon() (src/plugins/icons.ts) instead of drawing a generic tile.

## Admin sections
- Core section: add it to CORE_SECTIONS (src/admin/sections.ts) and SECTIONS (src/admin/section-screen.web.tsx), implement src/admin/<id>.web.tsx.
- Build with src/admin/kit.web.tsx (AdminPage, Tabs, Card, Badge, Switch, FlagSwitch, Field, Callout, SectionState, AdminDialog with a fixed size); styles only in src/admin/admin.css.
- Lists are tables; a row opens its edit dialog; destructive actions confirm first; a secret shows once in a Callout with Copy.
- Pure rules go in a *-model.ts beside the section, with tests.

## Copy
- src/lib/i18n/en.ts is the key source; zh.ts is typed as Catalog and must match key for key.
- Admin copy lives in the admin block (plugin sections under admin.ext.<id>); manifest titles and labels are { en, zh } in the plugin manifest.
- Use the glossary in apps/client/AGENTS.md (首页, 知识库, 云盘, 项目, 定时任务, 表格, 通知, 工作站, 「我」); delete unused keys after checking dynamic uses.

## Tests
- Keep logic in React-free modules (src/data, *-model.ts) and test them as *.test.ts; root vitest runs them without a client install, so they never import react, react-native or expo-*, even transitively.
- A folder with tests carries a stub tsconfig.json (copy src/api/tsconfig.json).
- Design guard: src/theme/design-guard.test.ts fails on raw hex colors or raw fontSize outside src/ui, src/theme and src/shared (mark a chart color with a `data color` comment) and on undefined var(--gh-*).
- Browser: tests/client-e2e/*.e2e.ts (playwright.client.config.ts); stub the station with page.route as p2-fixture.ts and p3-fixture.ts do; auth.setup.ts signs in.
- The suite owns ports 18920/18921 and gh4_client on 55450; parallel worktrees set CLIENT_E2E_API_PORT, CLIENT_E2E_WEB_PORT, CLIENT_E2E_DATABASE.

## Checks
```bash
pnpm client:install                              # after dependency changes; never npx expo install
(cd apps/client && pnpm typecheck && pnpm lint)  # root typecheck/lint skip apps/client
pnpm test:unit apps/client                       # client units + design guard (also in pnpm test)
pnpm test:e2e:client                             # browser suite
pnpm app:build                                   # hosted export into public/app
```
- Look at it: `pnpm dev` (client web on :3100, API on :3000) or `pnpm run-dev up`; check 1440 and 390 widths, light and dark.
- Native UI is judged in a dev client (`pnpm client:ios`, `pnpm client:android`), never Expo Go.

## Red lines
- No @greenhouse/* import, no `npx expo install`, no @react-navigation/* dependency, no KeyboardAvoidingView.
- No raw hex, raw fontSize or undefined --gh-* variable outside the theme and kit.
- No hand-pushed detail routes; objects open through openObject.
- No resizing dialogs and no popups outside Overlay / MenuPanel.
- No plugin id in core client code.
- No en key without its zh twin.
