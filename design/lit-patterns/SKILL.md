---
name: ha:lit-patterns
description: "Build ha-frontend Lit components: async data via @lit/task, WebSocket subscriptions for real-time (hass.connection / src/data collections), reactive property change handling, ha-form editors/dialogs/file uploads, repeat()/virtualizer for lists, navigate() routing. Use when handling interactions, debugging reactive property changes, or wiring entity/collection subscriptions."
effort: medium
user-invocable: false
paths:
  - "src/components/**/*.ts"
  - "src/panels/**/*.ts"
  - "src/dialogs/**/*.ts"
  - "src/data/**/*.ts"
  - "**/*-card.ts"
  - "**/*-card-editor.ts"
---

# ha-frontend Lit Patterns Reference

> **Integration (Python) side**: config-flow forms are voluptuous schemas + selectors — use the `config-flow` skill; data fetching/entities live in a coordinator + typed `runtime_data` — use the `coordinator-patterns` and `entity-platforms` skills. Do not hand-roll ad-hoc field checks. This reference covers the **ha-frontend (Lit)** side only: `ha-*` components, card/panel/dialog authoring, and the `hass` object.

Reference for building with Lit 2+ (LitElement 3.0) in the `home-assistant/frontend` codebase. Provenance: `frontend-lit-docs.md` (official docs snapshot 2026-07-12) + 4,268 maintainer review rows (`review-patterns-frontend.md`, 2024-07..2026-07). Every rule carries a law ID (F/FS series from `docs/iron-laws.md` + `docs/strong-defaults.md`) and ≥1 PR citation.

> **CAVEAT (hass narrowing)**: The docs show a monolithic `hass` property passed everywhere. 2026 reviews push the opposite direction — narrow to slices (`HomeAssistant["states"]`, `localize`) or Lit context (`@consumeLocalize`, registries context). Docs lag; reviews lead. See **FS10** below. Prefer narrowed params in new code.

## MANDATORY: Impeccable Skill for UI Work

Before writing or modifying ANY UI code (components, templates, styling, layout):

1. Check the available-skills list for the `impeccable` skill.
2. **If present**: you MUST invoke it (Skill tool) BEFORE implementing. It owns design quality — this reference covers Lit mechanics only, not visual/UX craft.
3. **If absent**: STOP and prompt the user to install it (e.g. `impeccable` from the Anthropic skills marketplace via `/plugin`) before proceeding. Continue without it only if the user explicitly declines.

This is not optional — skipping it on UI work is a skill failure.

## Iron Laws — Never Violate These

1. **NO UNCONDITIONAL DATA LOADS IN `connectedCallback`** — `connectedCallback` can run more than once (detach/reattach). Default: `@lit/task`'s `Task` with an `args` gate, or subscribe with symmetric teardown in `disconnectedCallback`. **FS4** — "should not do this in `connectedCallback` as it could happen more than once" (bramkragten, [PR 21933](https://github.com/home-assistant/frontend/pull/21933#discussion_r1756987452))
2. **ALWAYS USE `repeat()` (OR THE VIRTUALIZER) FOR LISTS** — Plain `.map()` in `html` re-renders the whole list on every update. `repeat()` with a key function = minimal DOM diff; `@lit-labs/virtualizer` = O(viewport) memory for huge lists. **FS1/FS15** (render efficiency + memory) — see the `lit-render-audit` skill
3. **SUBSCRIBE IN `connectedCallback`/`SubscribeMixin`, TEAR DOWN SYMMETRICALLY** — Guard `hass.connection.subscribe*` / collection subscriptions so `disconnectedCallback` cleanup runs before a reconnect resubscribes. Dialogs are the exception: **never `SubscribeMixin` in a dialog** (dialogs are never removed). **FS4/FS5** — "We can not use `SubscribeMixin` on a dialog, as dialogs are never removed" (bramkragten, [PR 27284](https://github.com/home-assistant/frontend/pull/27284#discussion_r2415720777))
4. **EXTRACT VALUES BEFORE TASK CLOSURES / MEMO ARGS** — `Task`'s task function is a closure; pass reactive inputs explicitly via `args` instead of reading `this.foo` inside the body. Same for `memoizeOne`: pass every input (including `localize`) as an argument. **FS2** — "`Object.values` generates a new object each time and defeats the memoization" (MindFreeze, [PR 29636](https://github.com/home-assistant/frontend/pull/29636#discussion_r3481369292))
5. **GATE DERIVED WORK ON THE RELEVANT CHANGE** — Route/param changes re-trigger the `Task` via `args`; `willUpdate`/`updated` work is gated on `changedProps.has(...)` or `shouldUpdate`. Never run per-`hass`-update work for unrelated state. **FS1** — "This fires on every `hass` change which is way to often" (MindFreeze, [PR 28672](https://github.com/home-assistant/frontend/pull/28672#discussion_r2882169715))
6. **NARROW THE `hass` OBJECT — DON'T PASS THE WHOLE THING INTO HELPERS** — Take slices (`HomeAssistant["states"]`, `localize`) or Lit context; extract plain data before calling a helper. **FS10** — "we would like to avoid to pass the hass object around everywhere" (wendevlin, [PR 29788](https://github.com/home-assistant/frontend/pull/29788#discussion_r2847369136))
7. **CHECK CONFIG/VALIDATION ERRORS BEFORE UI DEBUGGING** — Silent card-editor save = check the `ha-form` schema / config validation first, not CSS/JS. Broken stored config never validating is a hard stop (**FS12**) — "that PR breaks that behavior and should not be merged" (piitaya, [PR 52596](https://github.com/home-assistant/frontend/pull/52596#discussion_r3426639565))
8. **EVERY CONFIG FIELD IS IN THE `ha-form` SCHEMA** — A card/flow field the user must set has an entry in the `.schema` array with the right selector; nothing is silently omitted or left as a bare string. **PS15** (config-flow craft, selectors) — "Use text selectors, not bare strings." (emontnemery, [PR 158228](https://github.com/home-assistant/core/pull/158228#discussion_r2931027722))
9. **NEVER LAZILY INITIALIZE LIFECYCLE-CRITICAL STATE** — Don't guard assignment of derived state with `??=` or "set once" checks; re-derive on the relevant `changedProps` so stale `hass`/locale never survives. **FS4** — reassign symmetrically, `connectedCallback` runs every time
10. **HANDLE ERRORS VISIBLY** — A bare `catch` that swallows an error leaves the UI stuck. Wrap async UI actions in try/catch, surface with `ha-alert`/toast, reset busy flags in `finally`. **FS11** — "I think we should try catch this and show an error when it fails." (wendevlin, [PR 24277](https://github.com/home-assistant/frontend/pull/24277#discussion_r1995335112))

## Always-On Frontend Laws

These apply to every template you touch — the judge blocks (F-series) or flags (FS-series) on them:

| Law | Rule | Citation |
|-----|------|----------|
| **F1** | Every user-facing string goes through `hass.localize` with a key in `src/translations/en.json` | wendevlin, [PR 22594](https://github.com/home-assistant/frontend/pull/22594#discussion_r1822479687) |
| **F2** | Never create objects/arrays/schemas/functions inside `render()` — hoist to module consts or memoize | piitaya, [PR 51401](https://github.com/home-assistant/frontend/pull/51401#discussion_r3056252654) |
| **F3** | Use the in-house `ha-*` component — never raw `<button>`/`<input>`, `mwc-*`, or ad-hoc widgets | piitaya, [PR 26091](https://github.com/home-assistant/frontend/pull/26091#discussion_r2189252259) |
| **F4** | Style with theme tokens (`--primary-color`, `--ha-space-*`, `--ha-border-radius-*`, `--ha-font-size-*`) — never hardcoded colors/spacing | piitaya, [PR 24843](https://github.com/home-assistant/frontend/pull/24843#discussion_r2021223353) |
| **F5** | Copy arrays/objects before modifying (spread, not push/assign) so Lit sees the change | balloob, [PR 23531](https://github.com/home-assistant/frontend/pull/23531#discussion_r1911774763) |
| **F6** | Import every custom element the template uses — don't rely on incidental registration | wendevlin, [PR 25425](https://github.com/home-assistant/frontend/pull/25425#discussion_r2086792155) |
| **F7** | Return Lit `nothing` (imported from `lit`) for empty render branches — not `""`/`undefined` | wendevlin, [PR 22579](https://github.com/home-assistant/frontend/pull/22579#discussion_r1820405033) |
| **F8** | Respect the browser floor: no CSS nesting (iOS 12), no `structuredClone` (use `deep-clone-simple`), no `substr` | wendevlin, [PR 24301](https://github.com/home-assistant/frontend/pull/24301#discussion_r1961328774) |
| **F9** | Compose translator-safe strings: whole sentences with placeholders/ICU select — never concatenate fragments | silamon, [PR 29104](https://github.com/home-assistant/frontend/pull/29104#discussion_r2734954889) |
| **F10** | All formatting/sorting is locale-aware: `format*`/`Intl` with `hass.locale`, `stringCompare` for sorting | MindFreeze, [PR 30193](https://github.com/home-assistant/frontend/pull/30193#discussion_r2958140694) |
| **FS6** | Communicate upward via `fireEvent` DOM events declared in `HASSDomEvents`; dialogs take callbacks | bramkragten, [PR 26011](https://github.com/home-assistant/frontend/pull/26011#discussion_r2182635995) |
| **FS7** | RTL: logical properties (`margin-inline-start`, `start`/`end`), `--scale-direction` for transforms | wendevlin, [PR 51990](https://github.com/home-assistant/frontend/pull/51990#discussion_r3225872214) |
| **FS9** | Mobile safe areas: `var(--safe-area-inset-*)` in bottom-anchored/fullscreen layouts; `100dvh` over `100vh` | wendevlin, [PR 30081](https://github.com/home-assistant/frontend/pull/30081#discussion_r2912494081) |
| **FS13** | Layering: domain/WS logic in `src/data/<domain>.ts`, generic helpers in `src/common`; `components` never import from `panels`; dialogs lazy-load | MindFreeze, [PR 29759](https://github.com/home-assistant/frontend/pull/29759#discussion_r2946731922) |

## Memory Impact

| Pattern | 3K items | 10K entities × 10K rows |
|---------|----------|----------------------|
| `.map()` in `html` | ~5.1 MB | ~10+ GB (browser memory, per open tab) |
| `repeat()` / virtualizer | ~1.1 MB | Minimal (viewport-bounded) |

**Decision**: Lists with >100 items → Use `repeat()` with a key; >1000 rows → reach for `@lit-labs/virtualizer`. Unbounded caches must be capped or use `WeakMap` (**FS15** — "there is no cap on it. It can run out of memory", balloob, [PR 52657](https://github.com/home-assistant/frontend/pull/52657#discussion_r3414893248)).

## Quick Patterns

### Async Tasks (CRITICAL)

```ts
import { Task } from "@lit/task";
import { LitElement, html, nothing } from "lit";
import { customElement, property } from "lit/decorators";
import type { HomeAssistant } from "../types";
import { fetchDeviceConfig } from "../data/my_domain";

@customElement("my-device-panel")
export class MyDevicePanel extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;

  @property() public deviceId = "";

  private _deviceTask = new Task(this, {
    task: async ([hass, deviceId], { signal }) =>
      fetchDeviceConfig(hass, deviceId, signal),
    args: () => [this.hass, this.deviceId] as const,
  });

  protected render() {
    return this._deviceTask.render({
      pending: () => html`<ha-spinner></ha-spinner>`,
      complete: (device) => html`<h1>${device.name}</h1>`,
      error: () =>
        html`<ha-alert alert-type="error"
          >${this.hass.localize("ui.panel.my_domain.load_error")}</ha-alert
        >`,
    });
  }
}
```

### `repeat()` for Lists

```ts
import { repeat } from "lit/directives/repeat";

protected render() {
  return html`
    <ha-md-list>
      ${repeat(
        this._items,
        (item) => item.id,
        (item) => html`<ha-md-list-item>${item.name}</ha-md-list-item>`
      )}
    </ha-md-list>
  `;
}

// Insert/update/delete — copy the backing array (F5), let repeat() diff by key
this._items = [newItem, ...this._items];
this._items = this._items.map((i) => (i.id === updated.id ? updated : i));
this._items = this._items.filter((i) => i.id !== deletedId);
```

### WebSocket / Entity Subscription with Cleanup Guard

```ts
import { LitElement, html } from "lit";
import { customElement, property, state } from "lit/decorators";
import type { UnsubscribeFunc } from "home-assistant-js-websocket";
import type { HomeAssistant } from "../types";
import { subscribeMyDomain, type MyItem } from "../data/my_domain";

@customElement("my-live-panel")
export class MyLivePanel extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;

  @state() private _items: MyItem[] = [];

  private _unsub?: UnsubscribeFunc;

  public connectedCallback() {
    super.connectedCallback();
    if (!this._unsub && this.hass) {
      this._unsub = subscribeMyDomain(this.hass.connection, (items) => {
        this._items = items;
      });
    }
  }

  public disconnectedCallback() {
    super.disconnectedCallback();
    this._unsub?.();
    this._unsub = undefined;
  }
}
```

Prefer `SubscribeMixin`'s `hassSubscribe()` for panels/cards where the subscription is stable. **Never** use `SubscribeMixin` in a dialog (**FS5**).

### Gating Derived Work on the Relevant Change

```ts
import { memoizeOne } from "memoize-one";

// Pass every input (incl. localize) as an argument — FS2
private _computeRows = memoizeOne(
  (states: HomeAssistant["states"], localize: LocalizeFunc) => /* … */
);

protected willUpdate(changedProps: PropertyValues) {
  // Gate on the relevant change — FS1
  if (changedProps.has("deviceId")) {
    this._resetSelection();
  }
}
```

### Cache-Backed Startup Paint

> **Framework internals (audience: framework-development)** — this pattern is for `home-assistant/frontend` framework work, not card authoring.

Startup-visible state (theme, language) keeps a `localStorage` cache so the first paint doesn't flash the default; the backend value overwrites the cache as soon as the WebSocket delivers it. Do **not** add anything to the startup hot path that isn't strictly required — balloob holds veto here (**FI-1**, extends **FS13**): "Putting extra imports in the hot path of the frontpage needs to be carefully considered." ([PR 28036](https://github.com/home-assistant/frontend/pull/28036#discussion_r2649287585)). See `references/async-streams.md`.

## Navigation Decision Tree

```
Same route, different query params? → replace URL + let willUpdate re-derive
Different route, client-side?       → navigate(path) (src/common/navigate)
Full page load / different origin?  → location.href = url (full reload)
```

`navigate()` pushes onto the history stack; every push must be popped on all exit paths (see `references/pubsub-navigation.md`).

## Component Decision Tree

```
Does the component need BOTH internal state AND event handling?
│
├── YES → Does it encapsulate PANEL/DIALOG logic (not just presentation)?
│   ├── YES → Stateful LitElement with @state ✅
│   └── NO → Presentational component driven by @property, fires events up
│
└── NO → Presentational component (props in, ha-* events out) ✅
```

**Official guidance**: props-down / events-up. `@state()` for internal reactive fields (anything async-assigned or rendered); `@property` only for the public API (**FS3** — "this shouldn't be a property. make it a boolean `@state`", wendevlin, [PR 27020](https://github.com/home-assistant/frontend/pull/27020#discussion_r2381811816)).

## Common Anti-patterns

| Wrong | Right |
|-------|-------|
| Loading data unconditionally in `connectedCallback` | Use `@lit/task`, or subscribe + guard + tear down |
| `.map()` in `html` for lists | `repeat()` with a stable key, or `<lit-virtualizer>` |
| Subscribing without a cleanup guard | Guard in `connectedCallback`, tear down in `disconnectedCallback` |
| `SubscribeMixin` in a dialog | Subscribe elsewhere; dialogs take callbacks (FS5) |
| Passing the whole `hass` to a helper | Narrow to the slice/`localize` you need (FS10) |
| Object/array/schema built in `render()` | Module constant or `memoizeOne` (F2) |
| Literal English text in a template | `hass.localize("ui.…")` with an en.json key (F1) |
| Raw `<button>`/`mwc-button` | `ha-button` / the matching `ha-*` element (F3) |
| Mutating `@state`/`hass` data with `push`/index-assign | Spread into a new array/object (F5) |
| `return ""`/`undefined` from a render branch | `return nothing` (F7) |

## Framework internals (audience: framework-development)

> These sections apply only to `home-assistant/frontend` **framework** work (`src/entrypoints`, `src/state`, `src/mixins`, `src/common`, `src/util`, build/translation pipeline). They are **NOT** for authoring cards, panels, or custom components. Keep them distinct from the authoring laws above. Source: `docs/framework-dev-laws.md` (FI-series) + `review-patterns-frontend-internals.md`.

- **FI-1 — Protect the startup hot path** (IRON, extends FS13): no new static imports reachable from `src/entrypoints/core.ts`/`app.ts` or the frontpage render path; dialogs, editors, and heavy libs (echarts modules) load via dynamic `import()`. balloob has reverted a merged PR himself over this. "Putting extra imports in the hot path of the frontpage needs to be carefully considered." (balloob, [PR 28036](https://github.com/home-assistant/frontend/pull/28036#discussion_r2649287585))
- **FI-2 — Symmetric lifecycle across mixins/state/util** (STRONG, extends FS4): every listener/observer/manager/timer a mixin or the state layer registers is attached only while needed and removed in `disconnectedCallback`; every `history.pushState` is popped on all exit paths; app-global registration needs explicit justification. "we need to call this on disconnected too!" (wendevlin, [PR 52165](https://github.com/home-assistant/frontend/pull/52165#discussion_r3303487164))
- **FI-3 — Design-token completeness** (STRONG, extends F4/FS9): use `--ha-space-*` (source: `src/resources/theme/core.globals.ts`), `--ha-animation-base-duration` (350ms / 0 under reduced motion — no manual reduced-motion guards on top), and `var(--safe-area-inset-*, 0px)` with the **mandatory `0px` fallback** inside the `calc()` in framework chrome (sidebar, dialogs, subpages, `src/resources/styles.ts`). "please use `ha-space-` tokens" (wendevlin, [PR 28080](https://github.com/home-assistant/frontend/pull/28080#discussion_r2556296836))
- **FI-4 — Lokalise key lifecycle** (STRONG, extends F9): a meaning/param change ⇒ a NEW key (Lokalise keeps serving the old one as unverified); wording-only iteration reuses the key; retired keys are deleted in Lokalise by maintainers — contributors just remove them from `en.json`. Backend-owned strings arrive via the core Lokalise project (`hass.loadBackendTranslation`), never duplicated into `en.json`. "When the translation has been changed in context … introduce a new translation" (silamon, [PR 22021](https://github.com/home-assistant/frontend/pull/22021#discussion_r1774621446))
- **FI-5 — Web Awesome era** (IRON candidate): new dialogs are `ha-wa-dialog`; `ha-wa-*` wrappers **extend** the upstream Web Awesome class (full API reachable), import from `@home-assistant/webawesome/dist/...`, and expose only `--ha-*` semantic variables (mapped onto the `--wa-*` internals — never expose `--wa-*`/`--mdc-*`). Only place written down: the frontend repo [`AGENTS.md`](https://github.com/home-assistant/frontend/blob/dev/AGENTS.md) decision table. "webawesome has a skeleton component. Use this please." (wendevlin, [PR 29451](https://github.com/home-assistant/frontend/pull/29451#discussion_r2781814022))
- **FI-6 — `src/common`/`src/util` Vitest coverage** (STRONG, extends FS15): new/changed common/util logic ships with Vitest tests in the mirrored `test/` path asserting *observable* behavior (length checks, edge inputs); inline-reimplementation tests are removed. wendevlin will not approve without them. "I would call the file `search-highlight` and I would like you to create unit tests" (wendevlin, [PR 29401](https://github.com/home-assistant/frontend/pull/29401#discussion_r2786371884))

## Verification

`yarn lint` (ESLint + Prettier + `tsc` + lit-analyzer), `yarn lint:types`, `yarn test` (Vitest). Keep `yarn lint:types` green — maintainers paste type errors verbatim as review comments.

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/async-streams.md` — `@lit/task`, `repeat()`, virtualizer, cache-backed startup paint
- `${CLAUDE_SKILL_DIR}/references/forms-uploads.md` — `ha-form` editors, config validation, `ha-file-upload`
- `${CLAUDE_SKILL_DIR}/references/components.md` — presentational vs stateful components, reactive controllers, `fireEvent`
- `${CLAUDE_SKILL_DIR}/references/pubsub-navigation.md` — entity/collection subscriptions, `navigate()` routing
- `${CLAUDE_SKILL_DIR}/references/js-interop.md` — third-party non-Lit libraries (echarts, leaflet), cleanup, lazy-load
- `${CLAUDE_SKILL_DIR}/references/channels-presence.md` — `hass.connection` subscriptions, `src/data` collection conventions, presence-style live state
