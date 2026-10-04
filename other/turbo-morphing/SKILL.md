---
name: turbo-morphing
description: Apply Turbo 8 page refreshes with morphing and broadcast refreshes correctly, and avoid the morphing footguns. Use when adding smooth page refreshes (turbo_refreshes_with / turbo-refresh-method morph), broadcasting live updates with broadcasts_refreshes, deciding between morph-refresh vs targeted Turbo Streams vs frames, or when morphing resets browser state (an open details or dialog element, popovers, scroll, focus, JS widgets) after a refresh. Provides a decision guide and a morph-readiness checker.
---

# Turbo 8 morphing & page refreshes

Turbo 8 added a second update model alongside targeted Turbo Streams: **page
refreshes with morphing**. Render the current page again (e.g. submit → redirect
back) and Turbo morphs only the changed DOM via idiomorph, preserving screen state.
It's the simpler "happy path" — but it has sharp edges. This skill helps you pick
the right tool and avoid the footguns.

Full background: [`references/morphing-guide.md`](references/morphing-guide.md). Real-world note:
`piazza-web/wip/analysis/08-turbo8-morphing-refreshes.md`.

## When to use

- Adding `turbo_refreshes_with method: :morph, scroll: :preserve`.
- Broadcasting live updates and considering `broadcasts_refreshes` vs targeted streams.
- Morphing resets UI state (a `<details>` reopens for everyone, a popover closes,
  scroll jumps, a JS-initialized widget breaks) after a refresh/broadcast.
- Reviewing a PR that enables morphing, especially in the global layout.

## Decision guide

| Need | Use |
|---|---|
| Submit-and-redirect-back with many small scattered changes | morph page refresh: `turbo_refreshes_with method: :morph` |
| Live multi-user updates, simplest server code, "good enough" fidelity | `broadcasts_refreshes` + `turbo_stream_from @record` |
| High-fidelity append/prepend (chat), surgical control | targeted streams (`broadcast_append_to`, etc.) |
| Reload one region during a full-page refresh / explicit `.reload()` | frame with `refresh="morph"` |
| Morph a single element instead of replacing it | `turbo_stream.replace id, ..., method: :morph` |

Mantra (37signals): morphing is an **implementation detail of a page refresh**, not
a new partial-update tool. Use targeted streams when you need precision.

## broadcasts_refreshes (the simplification)

```ruby
class Listing < ApplicationRecord
  broadcasts_refreshes      # after create/update/destroy → <turbo-stream action="refresh">
end
```
```erb
<%= turbo_stream_from @listing %>
<%= turbo_refreshes_with method: :morph, scroll: :preserve %>
```
Async via `Turbo::Streams::BroadcastJob` (needs a job backend), auto-**debounced**
(only the last of a burst), and self-refreshes are deduped via `X-Turbo-Request-Id`.

## Avoid the footguns (morphing resets browser-only state)

In order of preference:
1. `data-turbo-permanent` — exclude an element from morphing entirely.
2. `turbo:before-morph-element` / `turbo:before-morph-attribute` + a small Stimulus
   controller to veto a specific change (e.g. keep `<details open>` open).
3. **Best** — keep the state on the server (a user-pref record or a URL param like
   `?sidebar=1`) so the re-render already matches the browser; morph is then a no-op.

Don't enable `turbo_refreshes_with` in the global layout without auditing stateful
widgets first.

## Check a repo

```bash
scripts/lint_morphing.sh path/to/rails-app
```

Reports: whether morph is enabled (and if it's **global** — in the layout — which is
risky), stateful widgets (`<details open>`, `<dialog>`, scrollable/JS-controlled
elements) that morphing may reset *without* a `data-turbo-permanent` /
`before-morph` guard nearby, and `_later` broadcast usage that needs a job backend.
Heuristic grep scan that names its ceiling — guidance, not a parser.
