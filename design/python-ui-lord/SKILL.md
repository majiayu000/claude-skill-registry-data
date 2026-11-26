---
name: python-ui-lord
description: Lord skill for Python UI design mastery — PySide6/Qt6 desktop apps, Textual 8 TUI, Flet 1.0 cross-platform, Reflex 0.9 / NiceGUI 3 / FastAPI+htmx web apps, design tokens, states, a11y, and packaging.
triggers:
  - python ui lord
  - python gui
  - python desktop app
  - desktop ui
  - pyside
  - pyside6
  - pyqt
  - pyqt6
  - qt app
  - qt designer
  - textual app
  - tui app
  - terminal ui
  - flet app
  - reflex app
  - nicegui
  - customtkinter
  - tkinter ui
  - kivy app
  - python web ui
  - python dashboard
  - pywebview
  - برنامج سطح المكتب
  - تطبيق ديسكتوب
  - واجهة رسومية
  - بايثون واجهة
personas:
  - UX
  - DEV
  - ARCH
  - DEVX
tech_stack:
  - pyside-6
  - textual-8
  - flet-1
  - reflex
  - nicegui-3
  - python-3-14
  - tailwind-4-3
lord: true

---

# Python UI Lord

[SKILL] python-ui-lord
[OBJ] Design and ship #1-quality Python UIs across desktop, terminal, and web — correct framework selection, token-driven theming, complete state coverage, a11y, and production packaging. No slop, no wrong tool.

[RULES]
1. [REQ] Framework Selection — Choose by deliverable, not habit. Matrix: professional native desktop/long-lived product → PySide6 6.10+; terminal/SSH/dev-ops tools → Textual 8; one Python codebase → desktop+web+mobile → Flet 1.0; production multi-user web app in pure Python → Reflex 0.9; fast custom web UI for tools/IoT/robotics → NiceGUI 3; server-rendered control → FastAPI+Jinja+htmx+Tailwind; batteries/admin → Django 6; data-science prototypes only → Streamlit/Dash/Gradio.
2. [REQ] Licensing — Default PySide6 (LGPL, closed-source OK via dynamic wheels). PyQt6 is GPL/commercial — only with a purchased license or a GPL-compatible project.
3. [REQ] Deprecation Watch — Never start new serious apps on customtkinter (dormant upstream, last release 5.2.2/2023) or Tkinter for anything beyond trivial scripts. Migrate path: PySide6 (native) or Flet (cross-platform).
4. [REQ] Research-First — Before styling, pull real product references via the `design-research` skill (mobbin/refero MCP). ONE dominant design direction per app — never average references. No invented gradients.
5. [REQ] Context7 Gate — Query Context7 MCP for the chosen framework BEFORE writing implementation code; APIs drift (Flet 1.0 rewrote the event loop, NiceGUI 3 refactored scenes). Live docs > memory.
6. [REQ] Tokens-First — Define the theme BEFORE the first widget: colors, spacing scale (4/8px base), type scale, radii, shadows. QSS template dict (Qt), .tcss theme (Textual), `page.theme` (Flet), `rx.theme` (Reflex), `ui.colors`+Tailwind classes (NiceGUI), CSS custom properties (htmx path). Hardcoded hex in a widget = defect.
7. [REQ] One Icon Set — Pick one family per app (Lucide, Material Symbols, Iconsax) at one stroke weight; `qtawesome`/`flet.Icons`/`rx.icon` mappings — never mix families.
8. [REQ] State Coverage — Every screen ships four states: empty (guidance + CTA, never bare "no data"), loading (skeleton/spinner, never blank), error (message + retry), success. Missing states = slop.
9. [REQ] Feedback Latency — Every interaction gets visible feedback ≤100ms: hover, pressed, disabled, busy. Long ops show determinate progress or stream partial results.
10. [REQ] Motion Discipline — 200–300ms transitions, ease-out on entry; animate transform/opacity only; honor reduced-motion/accessibility flags; never animate layout-blocking properties.
11. [REQ] A11y — accessibleName/aria on all controls; full keyboard navigation + shortcuts (QShortcut/BINDINGS/accesskey); contrast ≥4.5:1 text, ≥3:1 UI boundaries; never color-only state; visible focus indicator.
12. [REQ] Dark + Light — Ship both themes and verify each screen in both. Dark uses near-black surfaces (#0a0a0a–#1a1a2e range) with elevation tinting, never pure black.
13. [REQ] Density & Grid — Align everything to the spacing scale; consistent paddings per surface tier (toolbar < content < footer); text columns ≤75 chars; resize windows/terminals to min target and re-verify.
14. [REQ] RTL/Arabic — `Qt.LayoutDirection.RightToLeft`/Textual `text-align`/CSS `dir="rtl"`; logical properties; mirror nav/icons; Arabic font stack (IBM Plex Sans Arabic/Noto Sans Arabic, 1.5–1.7 line-height); test with real strings (+30% expansion).
15. [REQ] PySide6 Threading — NEVER touch QWidget/UI objects from a worker thread; QThreadPool+QRunnable with signals, or QThread+slots; heavy work yields progress via signals; use `@Slot` decorator.
16. [REQ] PySide6 Model/View — Data screens use QAbstractItemModel+QTableView/QSortFilterProxyModel (sorting/filtering for free); NEVER hand-populate QTableWidget for >100 rows — delegate+QListView/QML for cards.
17. [REQ] PySide6 Theming — Keep the palette in ONE Python dict; generate QSS from a template (QSS has no variables); Fusion style base + QSS overrides; `QPalette` for platform-native fallbacks.
18. [REQ] PySide6 Product Shell — Standard chrome: menubar/toolbar/statusbar/QSystemTrayIcon; QSettings for geometry+splitters+theme; single-instance guard (QLocalServer/QLockFile); native QFileDialog; DPI-aware (Qt6 auto-scaling).
19. [REQ] PySide6 Forms — Qt Designer `.ui` for complex static forms → `pyside6-uic`; prefer code for dynamic UIs; NEVER hand-edit generated `ui_*.py`.
20. [REQ] Textual Architecture — App → Screen(s) → composed Widgets; styles in `.tcss` files (not inline); reactive attrs + `watch_`/`compute_` for state; messages via `@on`/message handlers, not direct calls.
21. [REQ] Textual Async — NEVER block the message pump: `@work(thread=True)` for CPU, `run_worker`/async for IO; `LoadingIndicator`/progress widgets during waits.
22. [REQ] Textual Tooling — `textual console` + devtools for live inspection; BINDINGS for every action; CommandPalette for discoverability; `App.run_test()` + `pytest-textual-snapshot` for CI tests; same app can serve to browsers via textual-web for remote access.
23. [REQ] Flet 1.0 Model — Controls tree per `page`; single event loop runs handlers (1.0 breaking change from 0.28 — don't mix old patterns); `yield`/page.update() semantics per docs; `expand`/`spacing`/`alignment` for responsive layout; `View`s + `page.route` for navigation.
24. [REQ] Flet Theming & Targets — `page.theme=ft.Theme(color_scheme_seed=...)` + `page.dark_theme`; `page.theme_mode`; `flet build` targets windows/macos/linux/web/apk/aab/ipa/ios-simulator; persistent services (Audio/Geolocator/Clipboard) survive reloads.
25. [REQ] Reflex Architecture — `rx.State` subclasses hold ALL mutable state; event handlers mutate via `self`; components subscribe to vars and re-render selectively; NEVER put business logic in components — backend functions/services behind events.
26. [REQ] Reflex Long Tasks — `@rx.event(background=True)` for streaming progress/AI output (WebSocket push); yield intermediate state updates; NEVER block an event handler on long IO.
27. [REQ] Reflex Structure — Package layout: `pages/`, `components/`, `state/`, `backend/`; `rxconfig.py` for app/db/tailwind config; `rx.theme` tokens + `class_name` Tailwind escape; `reflex run --env prod` behind granian for production.
28. [REQ] NiceGUI Discipline — `ui.*` tree with slots; `ui.dark_mode()` binding; `ui.timer`/background async for live data; `app.storage.user|client` for persistence; `ui.run(native=True)` (pywebview) for a desktop window; escape to Quasar props via `.props()`/`.classes()` sparingly.
29. [REQ] htmx Path — FastAPI/Django + Jinja partials: endpoints return HTML fragments; `hx-target`/`hx-swap` precise swaps; CSRF on forms; Tailwind standalone CLI + `@theme` tokens; follow `web-design-guidelines` skill for the full 110-rule checklist.
30. [REQ] App Shell Contract — Title, icon, sane min/default window size, version string accessible; settings persist across restarts; proper shutdown (thread cleanup, port release, tray removal).
31. [REQ] Data Screens — Sorting + filtering + search on every table; pagination or virtualized list >1k rows; column resize/reorder persistence via settings.
32. [REQ] Dialogs & Feedback — Modal for destructive actions only; toast/snackbar for confirmations; validation inline at blur/submit with field-level errors; preserve user input on failure.
33. [REQ] Packaging — Desktop: Nuitka preferred (smaller/faster) or PyInstaller; bundle Qt platforms plugin; native icon + version metadata; test artifact on a CLEAN machine/VM before delivery.
34. [REQ] Testing — Smoke test "app boots to main screen" always; pytest-qt for Qt, `run_test()`/snapshot for Textual, TestClient/Playwright for web paths; states (empty/loading/error) get dedicated tests.
35. [PROHIBIT] Never update UI from non-UI threads/processes — signals/events/messages only.
36. [PROHIBIT] Never block the event loop or message pump — workers, async, or threads for all IO/CPU.
37. [PROHIBIT] Never put business logic, SQL, or HTTP calls inside widgets/components — service layer behind the UI.
38. [PROHIBIT] Never ship Streamlit/Dash as a production multi-user app — it's the prototype tier; production = Reflex/NiceGUI/FastAPI.
39. [PROHIBIT] Never hardcode colors, spacing, or fonts outside the theme token system — no slop (generic gradients, placeholder text, default-styled widgets, mixed radii).
40. [PROHIBIT] Never skip empty/loading/error states, keyboard nav, or the dark-mode pass.
41. [PROHIBIT] Never assume versions/APIs — Flet 1.0 broke 0.28 handler semantics; NiceGUI 3 refactored `ui.scene`; verify via Context7 + lockfile ([VER-01]).
42. [REQ] Desktop Security — secrets in OS keyring (`keyring` → Credential Manager/Keychain/libsecret), NEVER QSettings/.ini/plaintext; local UI servers (NiceGUI/Flet/webview modes) bind 127.0.0.1 + per-session auth token — open localhost API = any-process takeover; auto-updaters require signed packages + signature verification (unsigned updater = RCE); custom URL schemes/deep links validate every param (remote input); `js_api`/webview bridges expose Python methods — public API surface, validate + minimize; clipboard/drag-drop/file-drop content is untrusted.
43. [CMD] Context7 IDs — `/encode/httpx` family for API calls inside apps; framework IDs: textual `/textualize/textual`, reflex `/reflex-dev/reflex`, nicegui `/zauberzeug/nicegui`, flet `/flet-dev/flet`, pyside6 (Qt for Python docs via `/qt/qtforpython` when indexed — else official doc.qt.io).
44. [REQ] Delegation — Delegate pure HTML/CSS/token questions to `web-design-guidelines` + `ui-design-lord`; research references via `design-research`; API contracts via `api-architect`; backend reflexes via `backend-design`; security reviews via `web-security-checklist` + `tech-stack/appsec-hardening.md`.

[WORKFLOWS]
1. New PySide6 desktop app — pick MVVM shape → define token dict + QSS template → shell window (menu/toolbar/status/tray) → screens with 4 states → Model/View for data → QThreadPool workers → QSettings persistence → a11y + RTL pass → smoke test → Nuitka/PyInstaller package → clean-VM verify.
2. New Textual TUI — App + theme .tcss → screen map + BINDINGS → widgets with reactive state → workers for IO/CPU → CommandPalette → textual console devtools pass → `run_test()` + snapshot tests → optional textual-web serving.
3. New Reflex web app — `rxconfig.py` → `rx.theme` tokens → `rx.State` event model → components/pages split → background events for long tasks → dark/light verify → `reflex run --env prod` → deploy (self-host/Reflex Cloud).
4. FastAPI + htmx page — Jinja base (CSS custom props tokens + Tailwind) → partial endpoints → precise hx-swaps → CSRF + a11y per web-design-guidelines → pytest TestClient + Playwright smoke.
