---
name: jsgui3-ssr-activation-data-bridge
description: Understand and debug how jsgui3 SSR markup becomes activated client-side, including persisted fields (data-jsgui-fields) and ctrl_fields (data-jsgui-ctrl-fields), and where to patch/plugin.
---

# jsgui3 SSR → Activation Data Bridge

## Scope

- Explain the real runtime path from server-rendered HTML → client reconstruction (`pre_activate`) → event binding (`activate`).
- Use the built-in DOM-attribute “data bridge”:
  - `data-jsgui-fields` → persisted fields hydration (`_persisted_fields`)
  - `data-jsgui-ctrl-fields` → named child control wiring (`this.status`, `this.btn`, …)
- Identify high-leverage patch points (plugins / monkeypatch wrappers) for:
  - noisy console warnings
  - missing `context.map_Controls` registrations
  - text-node alignment issues (`&&& no corresponding control`)

Non-goals:
- Rewriting the bundler/publisher.
- Large refactors of upstream `jsgui3-*` packages without a minimal repro + regression guard.

## Inputs

- Which surface is failing?
  - “SSR renders but clicks don’t work”
  - “Persisted fields didn’t hydrate”
  - “ctrl_fields not bound”
  - “Missing context.map_Controls …” warnings
- The minimal repro (prefer an existing lab experiment).

## Procedure

1) Start from a lab repro (preferred)
- Use experiment 020 as the known-good baseline:
  - `node src/ui/lab/experiments/020-jsgui3-server-activation/check.js`

2) Confirm SSR emits the bridge attributes
- In SSR HTML, find:
  - `data-jsgui-id` (identity)
  - `data-jsgui-type` (constructor key; may be absent for exempt tags)
  - `data-jsgui-fields` (persisted fields payload)
  - `data-jsgui-ctrl-fields` (named child ids payload)

3) Understand activation sequence (client)
- Browser boot (from `jsgui3-client`) does:
  - create `Client_Page_Context`
  - update standard controls
  - `pre_activate(context)` (reconstruct controls from DOM)
  - `activate(context)` (call `ctrl.activate()` depth-first)

4) Persisted fields hydration (data-jsgui-fields)
- During control construction, `jsgui3-html` reads `data-jsgui-fields` from the DOM element and stores it as `_persisted_fields`.
- Controls typically consume `_persisted_fields` in `activate()` to restore state.

5) ctrl_fields hydration (data-jsgui-ctrl-fields)
- During `pre_activate_content_controls`, `jsgui3-html` parses `data-jsgui-ctrl-fields` (key→id) and binds:
  - `this[key] = context.map_controls[id]`
- This enables patterns like `this.btn.on('click', ...)` or `this.status.dom.el.textContent = ...`.

6) Interpret the common warnings
- `Missing context.map_Controls for type <X>`
  - Means SSR (or DOM) said the element is type `<X>`, but the client context doesn’t have a constructor registered at `context.map_Controls[X]`.
  - Client falls back to generic `Control`, so activation may still work (but you lose the intended class).

- `Missing context.map_Controls for type undefined`
  - Often corresponds to tags where `data-jsgui-type` is intentionally not emitted (notably `html/head/body` in upstream control-core).
  - This is usually log noise unless it breaks reconstruction.

- `&&& no corresponding control`
  - Emitted during pre-activation content linking when the DOM contains text nodes (often whitespace/newlines) that don’t correspond to a control entry in `content._arr`.
  - Often benign, but it is a good signal that DOM↔control-array alignment is fragile.

## Patch / plugin strategies

### Strategy A: Silence known-noise logs (safe)
- Wrap/monkeypatch the client-side `pre_activate` logger to skip warning output for exempt tag names (`HTML`, `HEAD`, `BODY`) when type is missing.

### Strategy B: Fill `context.map_Controls` for common tags (safe)
- Ensure common typed tags are registered (or mapped) so `style`, `main`, etc. don’t warn.
- Prefer adding registrations in a single place near client startup rather than scattered per-control.

### Strategy C: Make `pre_activate_content_controls` robust to whitespace text nodes (medium risk)
- Ignore text nodes where `nodeType === 3` and `nodeValue.trim() === ''` during the alignment walk.
- Keep a deterministic repro (experiment 020) and add a regression assertion on console output if/when you implement this.

## Validation

- Primary: `node src/ui/lab/experiments/020-jsgui3-server-activation/check.js`
- If you modify client-side controls/bundles: `npm run ui:client-build`

## References

- Experiment repro: `src/ui/lab/experiments/020-jsgui3-server-activation/`
- Guide: `docs/guides/JSGUI3_UI_ARCHITECTURE_GUIDE.md` (Client-Side Activation Flow)
- Upstream runtime (read-only reference in installed packages):
  - `node_modules/jsgui3-client/client.js`
  - `node_modules/jsgui3-html/html-core/html-core.js`
  - `node_modules/jsgui3-html/html-core/control-enh.js`
  - `node_modules/jsgui3-html/html-core/control-core.js`
