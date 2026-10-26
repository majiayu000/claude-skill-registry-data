---
name: frontend-conventions
description: Where dashboard code lives and how it is decomposed. Use when creating, moving or splitting anything under frontend/src/ or backend/src/api/, deciding which directory a new component or router belongs in, adding a control that can move money, or naming a new Panel/Dialog/Tab/View. Covers the API boundary, file suffixes, per-domain shape, size budgets, colour tokens, the one polling rule, and money-safety in the UI. Pairs with docs/system/rules/30-architecture.md (layers) and docs/system/rules/40-testing.md (tests).
user-invocable: true
allowed-tools: Read, Grep, Glob
---

# Frontend conventions

The canonical rule set for **where** dashboard code lives and **how** a screen
is decomposed.

This app's dashboard is **React + TypeScript**, compiled by Vite into
`frontend/dist` and served as static files by the FastAPI process in
`backend/src/api/`. It replaced a NiceGUI dashboard on 2026-09-18 — see
[the decision record](../../../docs/system/domains/frontend/010-the-react-decision.md).
If you find a NiceGUI idiom in your head (`with ui.card():`, `ui.timer`,
`app.storage.user`), it is from the previous app and does not apply.

These rules apply to `frontend/src/**` and `backend/src/api/**`. They do not
apply to `backend/src/services/` or `backend/src/db/`.

**Related docs — read rather than duplicate:**

| Topic | Owner |
|---|---|
| Layers and which import is legal | [docs/system/rules/30-architecture.md](../../../docs/system/rules/30-architecture.md) |
| What can cost money | [docs/system/rules/20-trading-safety.md](../../../docs/system/rules/20-trading-safety.md) |
| Test protocol | [docs/system/rules/40-testing.md](../../../docs/system/rules/40-testing.md) |
| What is ported and what is not | [docs/todo/frontend/react-port/](../../../docs/todo/frontend/react-port/README.md) |

---

## 0. Stop conditions (read first, every time)

If any of these is true, **stop and fix it before writing more code.**

- **You are about to import `backend.src.services` or `backend.src.db` from
  `backend/src/api/`.** Stop. Two contracts enforce that at zero, with
  `server.py` as the one named exemption. A router asks a controller a named
  question.
- **You are about to put logic in a router** — a loop, a merge, a formatting
  step, a fallback, a lot-size clamp. Stop. A route handler is one controller
  call plus a response model. `history_controller` acquiring three-source
  ledger merges is the recorded example of how logic pools in the wrong layer.
- **You are about to take a Dialog/Panel/Tab file past 250 LOC.** Extract a
  controller hook into `hooks/` or a sub-component into `internal/` first.
  400 is a hard stop.
- **You are about to call `fetch` in a component.** Stop. Everything goes
  through `frontend/src/api/client.ts` — it is the one place a 401 becomes
  "go to the login screen" and the one place a refusal is told apart from a
  failure.
- **You are about to write `setInterval`.** Stop. `usePoll` is the only
  polling primitive. A new "what is the latest X" need is an extra field on an
  existing consolidated response, assembled server-side, not a new interval.
- **You are about to format money, a price or a timestamp inline.** Stop. Use
  `components/shared/format.ts`. MT5 stamps are UTC+3 encoded as an epoch and
  `formatBrokerTime` already knows that; re-deriving it puts every trade three
  hours into the future.
- **You are about to add a control that opens, closes, resizes or re-prices a
  position.** Stop and read [`/safe-change`](../safe-change/SKILL.md). A button
  that can lose money is not a UI change.
- **You are about to remap green, red, amber or blue.** Stop. green = profit,
  red = loss, yellow/amber = warning and the accent, blue = remote/VPS,
  gray = neutral.
- **You are about to disable a control without giving a reason.** Stop. Pass
  `disabledReason` — a greyed-out Execute button with no explanation is
  indistinguishable from a broken one.

---

## 1. The layer rule (the one that is enforced)

```
browser (frontend/src) → backend/src/api → controllers → services → db
```

```python
# ✅ DO — backend/src/api/routers/trading.py
from backend.src.controllers import trading_controller as trading_ctl

@router.get("/risk")
async def risk_settings() -> dict:
    return await trading_ctl.get_risk_settings_async()

# ❌ DON'T — counted by the contract, and it puts a service call on the
# server's event loop for every browser that asks
from backend.src.services.risk import settings as _risk
```

**If the controller doesn't expose what you need**, in order of preference:
the service already has the function → add a flat forwarder to the controller;
the service doesn't → add the named function to the *service*, then forward;
neither fits → you are probably asking the wrong question.

Controllers have a hard 200-line ceiling, enforced at zero. Routers inherit it.
A router that would exceed it means the *service* should expose one coarser
function.

**`server.py` is the only module that may hold the engine handle.** Everything
else receives it through `deps.engine`. That is the same single exemption
`frontend/app/__init__.py` carried, for the same reason.

---

## 2. Where things live

```
frontend/src/
  api/client.ts             the one HTTP client; types.ts beside it
  hooks/usePoll.ts          the one polling primitive
  contexts/                 AuthContext and anything else genuinely app-wide
  lib/                      cn(), asArray() — no domain knowledge at all
  pages/<Name>Page.tsx      top-level routed pages (login)
  components/
    shared/                 DialogShell, PanelShell, Button, StatCard,
                            EmptyState, NotPortedPanel, format.ts
    <domain>/               shell/, chart/, trading/, …
      <Domain>Panel.tsx     thin top-level: composition + minimal state
      <Feature>Dialog.tsx   thin top-level
      hooks/use<X>Controller.ts   state, fetching, side effects
      internal/             sub-components used only inside this domain
backend/src/api/
  server.py                 composition root — routers first, bundle last
  auth.py errors.py deps.py
  routers/<domain>.py       one per domain, named for the controller
  schemas/<domain>.py       Pydantic models; they name fields, never compute one
```

**Placement, in order:**

1. Used by one section of one domain → it lives in that domain's `internal/`.
2. Used by two domains → `components/shared/`, **on the second caller, not in
   anticipation of one.**
3. Generic with no domain knowledge → `components/shared/` or `lib/`. If the
   file names a trade, a signal, a strategy, a channel or an engine, it does
   not belong there.

**A domain folder is named after a business concept, and it matches the
backend's vocabulary** — the backend `trading/` service and the frontend
`trading/` components describe the same thing. Navigating between them should
be mechanical.

**Do not create a near-empty directory.** No `hooks/` or `internal/` until the
wrapper crosses 150 LOC or there is a second sub-component.

**Do not re-export a domain component through `shared/` to make it look
generic.** Import it from the domain that owns it.

---

## 3. File suffix vocabulary

Every component file ends in one of these. **No synonyms** — no `Modal`,
`Popup`, `Overlay`, `Drawer`, `Sheet` or `Widget`.

| Suffix | Use for | Shell |
|---|---|---|
| `*Dialog.tsx` | Modal opened on demand | `DialogShell` |
| `*Panel.tsx` | Persistent panel owning a screen surface | `PanelShell` |
| `*Tab.tsx` | One tab's content | none |
| `*View.tsx` | Read-only detail rendering | none |
| `*Form.tsx` | Multi-field input with a submit | none |
| `*Card.tsx` | Reusable bordered display unit | none |
| `*Section.tsx` | Grouping inside a Panel/Tab | none |
| `*Page.tsx` | Top-level routed page (`src/pages/`) | none |

Components are `PascalCase.tsx`; helpers beside them are `snake_case.ts` or
`camelCase.ts` matching what is already there. Tests live in
`__tests__/<Name>.test.tsx` next to their subject.

---

## 4. Size budgets

| Tier | LOC | Action |
|---|---|---|
| Thin wrapper | <150 | Default for a Dialog/Panel top-level file. |
| Acceptable | 150–250 | Fine if the logic is self-contained. |
| Refactor warning | 250–400 | Extract before adding more. |
| Hard stop | >400 | Cannot land. |
| Routers / controllers | >200 | Fails the gate, enforced at zero. |

**The thin-wrapper pattern.** A top-level Dialog or Panel reads as
composition, not implementation — which is where you check "does the confirm
step actually gate the order?":

```tsx
export function PlaceOrderDialog(props: PlaceOrderDialogProps) {
  const c = usePlaceOrderDialogController(props.onPlaced);
  return (
    <DialogShell title="Market order" footer={<OrderActions c={c} />}>
      {c.step === "form" ? <OrderForm controller={c} /> : <OrderConfirm c={c} />}
    </DialogShell>
  );
}
```

---

## 5. Reuse before you build

| Need | Use |
|---|---|
| Any HTTP call | `api.get/post/put` from `api/client.ts` |
| Anything that refreshes | `usePoll(key, fetcher, intervalMs)` |
| Money, price, lots, percent | `formatMoney`, `formatSignedMoney`, `formatPrice`, `formatLots`, `formatPercent` |
| An MT5 broker timestamp | `formatBrokerTime` — **do not roll your own** |
| Colour a P&L number | `pnlColour(value)` |
| A modal | `DialogShell` |
| A panel | `PanelShell` |
| A label + number | `StatCard` |
| An empty panel | `EmptyState` — and say what to do next |
| A list from an untyped response | `asArray<T>(data)` |
| A button that might be disabled | `Button` with `disabledReason` |

**The variant test.** Showing a variant of something already on screen? It gets
an extra pill or line on the **existing** component, never a parallel one.

---

## 6. Colour and theme

Colours are CSS tokens in `frontend/src/index.css`, used through Tailwind
(`text-profit`, `bg-surface-2`, `border-line`). **Semantic colours carry
meaning and are never remapped:**

| Token | Means |
|---|---|
| `profit` (green) | profit, connected, running, success |
| `loss` (red) | loss, disconnected, stopped, danger |
| `warning` / `accent` (amber, gold) | warning, attention, the app's brand accent |
| `remote` (blue) | informational, the remote/VPS node |
| `ink-*` / `surface-*` / `line` (gray) | neutral, disabled, absent data |

Only the neutral scale is meant to be re-skinned by a theme. That is exactly
what `theme.py`'s four presets did, and why they left every accent alone.

**Do:** use `.num` for any number a user might compare against another number.
Give a control a `title` when its label cannot be self-explanatory in three
words.

**Don't:** hard-code a hex colour in a component (a new colour is a token
change); add a light-mode style (there is no light mode — see QUESTIONS Q3);
introduce a surface step that is not defined in `index.css`.

---

## 7. Live data

**One poll, many subscribers.** `usePoll` runs one interval per key, dedups
in-flight requests and pauses while the tab is hidden. The NiceGUI app had
~20 `ui.timer()` calls and an unattended browser tab on the VPS was directly
implicated in event-loop stalls; this is the rule that stops that returning.

**Do:**
- Pick the interval from how fast the data actually changes. 5s for
  account/positions is the established cadence; a tick is 3s; a static config
  panel needs no poll at all.
- Put a consolidated payload behind one key when the fields are always read
  together — `/api/system/header` is the worked example.
- Show staleness. `updatedAt` exists so a number that stopped updating does not
  read as a number that stopped moving.

**Don't:**
- Add a second poll for data an existing one already fetches.
- Push an unbounded payload. History at `days=3650` is what forced the old
  WebSocket buffer to 10MB; paginate instead.
- Assume the tab is visible.

---

## 8. Money in the UI

**This app places real orders on a live MT5 account with real money. The
frontend is where the button is.**

**Do:**
- Route every order action through a controller. No exceptions.
- Require an explicit confirmation for anything that opens, closes or resizes a
  position, and **state the instrument, direction and size** — not "Are you
  sure?".
- Show the disabled reason: *trading paused*, *bridge disconnected*, *stood
  down as Remote*, *out of hours*. `Button`'s `disabledReason` makes this hard
  to forget.
- Make demo vs live unmistakable, and render a third "unknown" state when the
  bridge has not answered. Never show an unanswered bridge as DEMO.
- Surface a rejection verbatim. `ApiError.isRefusal` is how you tell the
  backend's considered "no" from a crash.

**Don't:**
- Let a component decide whether an order is allowed. The backend decides; the
  page renders the answer. Two risk checks produce two answers that drift.
- Add a confirmation that defaults to yes, or a destructive action on a single
  click.
- Show a stale P&L without saying it is stale.
- Write a test that places, closes or modifies a real **or demo** order. The
  sentinel engine in `tests/api/conftest.py` is the pattern; a test file that
  could reach a broker says so in its docstring and proves it cannot.

---

## 9. Adding a new tab or section

1. **Does it belong in an existing tab?** A new sub-tab on `trading` beats a
   new top-level tab nobody finds.
2. **Name it after what the user calls it**, not after the service behind it.
   (`test_panel.py` was the Bounce engine — a standing example of what that
   costs.)
3. **Write the router first**, one forwarding handler per controller question,
   with its tests and a negative control.
4. **Start as a single component** at `components/<domain>/<Name>Panel.tsx`.
   Create `hooks/` and `internal/` when the wrapper crosses 150 LOC.
5. **Open the nearest sibling domain and match it.** A panel that does not look
   like its siblings is a bug even when every line is correct.
6. **Register it** in `components/shell/tabs.ts` and clear its `notPorted`
   entry in the same change.

---

## 10. Known state (parking lot)

Current as of 2026-09-18.

- **Two of ten tabs are ported**: Chart and Trading. The other eight render
  `NotPortedPanel`, which names task 080. Do not quietly hide a tab instead.
- **32 backend modules are orphaned by the port**, recorded in
  `orphan_module_allowlist.json` with class `awaiting-react-port`. They are the
  controllers and services only an unported tab imported. Delete an entry when
  its tab lands.
- **The licence screens are still NiceGUI** (`config/licence/guard.py`), which
  is why `nicegui` is still a dependency and `no-nicegui-in-the-backend` still
  sits at 2. Task 090.
- **The Trading tab's money controls have not had a demo session.** Green tests
  are not sign-off for a money path.
- **The three engine panels** (breakout, reversal, test) are structurally
  near-identical and deliberately not collapsed. Porting them is not permission
  to merge them: they look alike and behave differently.
- **`frontend/dist` is committed.** Rebuild it in the same commit as any
  `frontend/src` change, or the dashboard ships the previous version.

---

## What this skill is NOT

- Not a styling guide. Colour *semantics* are here (§6); visual design is not
  specified anywhere and changing it is its own spec.
- Not a licence to refactor while passing. Restructuring and behaviour changes
  travel in separate commits, always.
