---
name: lwc-error-boundaries
description: "Isolate component errors so one failure does not blank an entire page using errorCallback and graceful fallbacks. NOT for server-side Apex exception design — use apex/exception-handling. Also covers: normalising error.body across UI API read, UI API write, Apex and network shapes; fallback UI; retry by remount; telemetry hand-off from the boundary."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - User Experience
triggers:
  - "lwc errorcallback"
  - "lwc component blank page"
  - "error boundary lwc"
  - "lwc graceful fallback"
  - "stop one broken LWC tile from blanking the whole dashboard page"
  - "normalise wire and Apex error shapes into one message list in LWC"
  - "read error.body when it is sometimes an array and sometimes an object"
  - "add a retry button that remounts a failed LWC child component"
  - "log LWC client errors to a custom object from errorCallback"
  - "write a Jest test that makes a child LWC throw into errorCallback"
  - "fallback UI renders but nothing is logged for the LWC failure"
  - "show an Apex AuraHandledException message in an LWC without leaking the class name"
tags:
  - error-handling
  - lwc
  - errorcallback
  - error-normalisation
  - fallback-ui
  - telemetry
inputs:
  - "parent component"
  - "child components that may error"
  - "which error producers the subtree uses — UI API wire, imperative Apex, network"
  - "where client errors are recorded today (custom object, external logger, or nowhere)"
outputs:
  - "wrapper boundary component + fallback UI"
  - "shared error-normalisation module reducing the four documented body shapes to one structure"
  - "Jest tests per normaliser branch plus a boundary test with a throwing child"
  - "static-check findings from scripts/check_lwc_error_boundaries.py"
dependencies: []
version: 1.2.0
author: Pranav Nagrecha
updated: 2026-09-05
---

# LWC Error Boundaries

`errorCallback(error, stack)` on any ancestor "captures errors in all the descendent
components in its tree" — errors "that occur in lifecycle hooks or during an event handler
declared in an HTML template" (`lwc_guide create-lifecycle-hooks-error L4158`). Wrapping
each widget in a reusable boundary keeps one failure from removing the whole page.

This skill covers the boundary *component*: where to place it, what its fallback may safely
depend on, how to reduce the four documented error shapes to one structure the fallback and
the telemetry record can both use, how to offer a retry that actually re-mounts the child,
and how to prove all of it with Jest. The hook's own contract and its position in the
lifecycle belong to `lwc/lifecycle-hooks`.

## Before Starting

Check for `salesforce-context.md` in the project root. If present, read it first —
particularly whether any of these components land on an Experience Cloud site, which
changes which toast module is legal (`references/gotchas.md`, Gotcha 10).

Gather if not available:

- Which subtrees are independently useful, and which would leave the page pointless if they
  vanished.
- Which error producers each subtree uses: UI API wire adapters, imperative Apex, plain
  `fetch`, or a mix. Each has a different `error.body` shape.
- Where client errors are recorded today, if anywhere.
- Whether users can meaningfully retry, or whether the failure is deterministic.

## Questions to Ask Before Configuring

Ask these before writing the wrapper. An assistant that skips them produces a grey box that
looks correct in review and reports nothing in production.

| Ask | Why it matters | What a good answer adds |
|---|---|---|
| "If this subtree disappears, can the user still do something useful on this page?" | The guide leaves placement to you — "You can wrap the entire app, or every individual component" (L4160) — but the throwing subtree is unmounted and removed from the DOM (L4162) | The boundary count and their exact positions in the markup |
| "Which of these components read from a UI API wire, and which call Apex imperatively?" | UI API **reads** return `error.body` as an array; UI API writes, Apex and network errors return an object (L6568–L6571) | Which normaliser branches are actually exercised, and which fixtures the Jest suite needs |
| "Does the failing operation have any chance of succeeding on a second attempt?" | A Retry button on a deterministic failure is a loop with a friendly label | Whether the fallback gets a Retry button, and what `maxRetries` should be |
| "Where do client-side errors go today — a custom object, an external logger, or nowhere?" | A silent boundary removes the user's only reason to report the problem while removing none of the problem | The telemetry target, the payload fields, and who reads it |
| "Is this component ever placed on an Experience Cloud page?" | `lightning/platformShowToastEvent` "isn't supported in environments like LWR sites for Experience Cloud or standalone apps" (L4773) | The toast module choice, and whether `lightningCommunity__Default` belongs in the `.js-meta.xml` |
| "Does the Apex behind this throw `AuraHandledException`, or does it throw uncaught?" | An uncaught Apex exception surfaces the Apex class name in `body.stackTrace` at the client (L7518); `AuraHandledException` omits it (L7521) | Whether the fallback may show the message at all, and a work item for `apex/exception-handling` |
| "Are any event handlers in this subtree attached in JavaScript rather than in the template?" | Errors from programmatically assigned handlers are not caught by `errorCallback` (L4167) | The list of handlers that need their own `try/catch`, since the boundary will never see them |

What a proper boundary adds over just implementing `errorCallback`: the failure stops at a
subtree the user can afford to lose, the message shown comes from the right level of the
error object regardless of which API produced it, the failure is recorded before the fallback
renders, and a recoverable failure gets one bounded retry instead of a page reload.

## Recommended Workflow

1. **Place the boundaries.** Mark each independently useful subtree in the parent template.
   Wrap each one — not the page — using the placement test from the Questions table above.
   Record the count; it is the number of `boundary-name` values you will see in telemetry.
2. **Deploy the normaliser first.** Copy the `errorUtils` module from
   `references/code-examples.md` (Bundle 1). It is the only place in the bundle set that
   knows `error.body` is an array for a UI API read and an object for everything else.
   Every branch in it carries its guide line; keep the citations when you copy it.
3. **Build the boundary.** Copy `errorBoundary` (Bundle 2): `errorCallback` → normalise →
   `hasError` → fallback with `lwc:if` / `lwc:else` → optional Retry → telemetry inside its
   own `try/catch`. Use `templates/lwc/component-skeleton/` for the bundle shell. Do not add
   a wire adapter or an imperative call to the boundary; it must have nothing of its own that
   can throw.
4. **Handle what the boundary cannot see, in the child.** Copy the `revenueTile` pattern
   (Bundle 3) for wire `error` branches, imperative `catch` blocks and programmatic handlers,
   routing all three into the same normaliser. Cross-check against
   `templates/lwc/patterns/imperativeApexPattern.js` and
   `templates/lwc/patterns/wireServicePattern.js`.
5. **Run the checker.**
   `python3 skills/lwc/lwc-error-boundaries/scripts/check_lwc_error_boundaries.py --manifest-dir force-app/main/default/lwc`
   Fix every ERROR (EB001 swallowed `errorCallback`, EB002 rethrow). Add `--strict` in CI to
   fail on the WARN rules too (EB003 unguarded `error.body.message`, EB004 console-only
   error branch, EB005 `platformShowToastEvent` on an Experience Builder target).
6. **Test both halves.** Port the Jest suites from `references/code-examples.md`: one case
   per normaliser branch with the fixture payloads from `references/examples.md`, and the
   boundary suite with a throwing child, the telemetry hand-off, the no-rethrow assertion
   and the retry re-mount.
7. **Verify in the org.** Work the seven-row verification table at the end of
   `references/code-examples.md` — deploy, force a failure, confirm one tile degrades, and
   confirm a telemetry row exists for it.

## The four error shapes, once

| Producer | `error.body` is | Guide line |
|---|---|---|
| UI API read (`getRecord`, related lists) | array of objects | `data-error L6568` |
| UI API write (`createRecord`, `updateRecord`) | object, often with object- and field-level errors | `data-error L6569` |
| Apex read and write | object | `data-error L6570` |
| Network, such as offline | object | `data-error L6571` |
| `errorCallback(error, stack)` | no `body` at all — a native `Error`, and `stack` is a string | `create-lifecycle-hooks-error L4164` |

The wrapper around the first four is a `FetchResponse`: `body`, `ok` (always false, status
400–599), `status`, `statusText` (`data-error L6545–L6551`). Before a wire fires, `data` and
`error` are both undefined — not an error state (`L6572`).

## Division of labour

| Failure | Where it surfaces |
|---|---|
| Throw in a descendant's lifecycle hook | Ancestor `errorCallback` (`L4158`) |
| Throw in a descendant's template-declared handler | Ancestor `errorCallback` (`L4158`) |
| Throw in a programmatically attached handler | Nowhere — local `try/catch` (`L4167`) |
| Rejected promise from imperative Apex | Nowhere — `.catch` / `try/await` (`L6513`, `L6524`) |
| Wire adapter failure | The wired property's `error` member (`L6542`) |
| Nothing catches it at all | The app shell's "A Component Error has occurred!" modal (`L7732`) |

## Adoption Signals

Dashboards with multiple independent widgets; record home pages with many components; any
page where a single tile calls Apex and a second tile is the reason users opened the page.

## Key Considerations

- The boundary owns no business logic, no wire adapter and no imperative call — anything it
  owns is a way for the error handler itself to fail.
- The fallback must not depend on data that may be the reason the boundary fired.
- `lwc:if` takes a property or a getter, never an expression: `lwc:if={!hasError}` is not
  supported (`reference-directives L19510`). Use `lwc:else`.
- Cap retries. A deterministic failure will happily re-mount forever.
- Keep `body.stackTrace` and the `stack` string in telemetry, never in the rendered message.

## Worked Examples (see `references/examples.md`)

- *Dashboard tile isolation* — six-tile sales dashboard, one boundary per tile
- *The failures the boundary does not catch* — wire error, promise rejection, programmatic handler
- *The four error payloads, as fixtures* — one JSON block the Jest suite asserts against

## Common Gotchas (see `references/gotchas.md`)

- **`error.body` is an array for UI API reads** — `error.body.message` returns `undefined`.
- **A legal app-level boundary still costs the whole app** — the unmount takes everything below it.
- **A fallback with dependencies** — fails inside the failure handler, with nothing above to catch it.
- **Toggling the retry flag twice in one block** — both writes land in the same microtask, so nothing happens.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- Reading `error.body.message` without an `Array.isArray` guard
- Rethrowing from `errorCallback` to "let something upstream handle it"
- Catching silently, so production failures are invisible
- A fallback that renders the raw error object, Apex class name and all

## Official Sources Used

Full list with the claim each supports in `references/well-architected.md` §
Official Sources Used.

- errorCallback() — https://developer.salesforce.com/docs/platform/lwc/guide/create-lifecycle-hooks-error.html
- Handle Errors in Lightning Data Service — https://developer.salesforce.com/docs/platform/lwc/guide/data-error.html
- Work with Errors — https://developer.salesforce.com/docs/platform/lwc/guide/data-error-types.html
- Handle Errors from Apex — https://developer.salesforce.com/docs/platform/lwc/guide/apex-error-handling.html
- Toast Notifications — https://developer.salesforce.com/docs/platform/lwc/guide/use-toast.html

## Reference Files

| File | Read it when |
|---|---|
| `references/code-examples.md` | You are writing the components: the `errorUtils` module, the `errorBoundary` bundle, the `revenueTile` bundle, `.js-meta.xml`, `package.xml`, deploy order, both Jest suites, and the verification table |
| `references/examples.md` | You want the worked scenarios and the four fixture payloads to test the normaliser against |
| `references/gotchas.md` | Something behaves unexpectedly — the array body, the silent retry, the invisible toast, the boundary that cannot query its child |
| `references/well-architected.md` | You are justifying boundary placement, normalisation or telemetry in a design review, and need the source list |
| `references/llm-anti-patterns.md` | You are reviewing generated boundary code, or about to generate some |

## Related Skills

- **lwc/lifecycle-hooks**: owns the `errorCallback` contract, hook ordering, and the minimal boundary example. Read it first; this skill assumes it.
- **lwc/wire-service-patterns**: the wire `{ data, error }` contract and refresh behaviour behind the wire branch here.
- **lwc/lwc-toast-and-notifications**: toast copy, variants, containers, and which module works in which container.
- **lwc/common-lwc-runtime-errors**: the catalogue of runtime error messages you will be normalising.
- **lwc/lwc-testing**: broader Jest patterns; this skill carries only the boundary and normaliser suites.
- **apex/exception-handling**: the server side — throwing `AuraHandledException` so the client never sees an Apex class name.
- **apex/debug-and-logging**: where the telemetry payload from `errorCallback` should land, and how to read it back.
