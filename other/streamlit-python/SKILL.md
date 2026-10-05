---
name: streamlit-python
description: Use for writing, reviewing, debugging, or testing Python Streamlit apps, especially rerun behavior, widget identity and callbacks, session_state, cache_data/cache_resource, forms, fragments, containers, multipage navigation, uploads/downloads, and Streamlit-hosted chart/table interaction. Do not use for standalone Plotly/Altair figure design, generic backend services, Dash apps, or deployment configuration without app code.
argument-hint: "[Streamlit app task, rerun/state/cache/form/fragment defect, or test]"
---

# Streamlit Python

Design for reruns. Each connected browser session executes the Python script
top-to-bottom; widget interaction normally triggers another run. State, cache,
forms, callbacks, and fragments alter what survives or which code reruns, not
the need for deterministic repeated execution.

## Boundary

Use this skill when a project imports Streamlit or explicitly requests a
Streamlit app. Do not route standalone Plotly/Altair figure semantics, a generic
API/backend, Dash callbacks, or hosting-only configuration here. Use the
relevant visualization/table skill for the object embedded in Streamlit, then
this skill for its rerun, state, and event integration.

## Know the execution objects

| Object | Runtime meaning | Responsibility |
|---|---|---|
| Script run | One top-to-bottom execution for one session | Recompute UI deterministically from current widget/session/cache inputs. |
| Widget | Frontend value plus identity | Use stable unique keys; distinguish current value from a momentary trigger. |
| Callback | Function executed before the ensuing full script run | Update state or perform narrow side effects; rendered callback output is not the main page. |
| `st.session_state` | Per-session values surviving reruns | Own UI/workflow state, not durable database state or cross-user cache. |
| `st.cache_data` | Memoized data-producing function keyed by code/arguments | Cache serializable data results with freshness/size policy. |
| `st.cache_resource` | Shared cached resource/singleton | Own expensive thread-safe resources shared across sessions; mutation is visible. |
| Form | Batch of widget values sent on submit | Prevent a full rerun for each intermediate edit. |
| Fragment | Function with a partial rerun scope | Isolate frequently updating/interactive region after correctness under full rerun. |
| Container/placeholder | Stable location in the current render tree | Control layout/update destination; not persistent state by itself. |

Read [the rerun and state model](references/execution-state.md) before fixing
“value resets,” duplicate side effects, callback ordering, or widget-key errors.

## Ordered workflow

1. Draw the rerun boundary: which lines execute on first load, every widget
   change, form submit, callback prefix, fragment rerun, and every session.
2. Classify every value as widget input, derived value, per-session workflow
   state, cached data, shared resource, durable external state, or transient
   event. Put it in exactly one owner.
3. Initialize session keys before reading them or instantiating widgets that use
   them. Give dynamic/repeated widgets stable unique keys based on durable IDs.
4. Keep ordinary rendering idempotent. Gate writes, messages, and costly calls
   behind explicit submit/button events or domain idempotency.
5. Use a form when edits should commit together. Use callbacks only for a
   short state transition that must precede the rerun.
6. Add caching after correctness. Choose data versus resource, include all
   semantic inputs, and set TTL/entry bounds from freshness and memory needs.
7. Add a fragment only when a measured region should rerun independently and
   its state/container effects are understood.
8. Test first load and a sequence of interactions, including two isolated
   sessions and cache invalidation where relevant.

## State and execution router

| Requirement | Use | Do not use |
|---|---|---|
| Current widget value | widget return or keyed widget state | Duplicate shadow variable unless a committed/draft distinction exists |
| Value survives reruns for one user | `st.session_state` | Module global |
| Durable/cross-device record | Database/file/service with explicit transaction | Session state |
| Pure-ish data result expensive to recompute | `st.cache_data` | Resource cache for mutable dataframes/results |
| Connection/model/client shared across sessions | `st.cache_resource` if thread-safe | Session state merely to avoid construction |
| Commit several inputs together | `st.form` + submit button | Callback on every field |
| One region reruns independently | `st.fragment` | Fragment before full-rerun semantics are correct |
| One-time side effect | Explicit trigger plus idempotency/receipt state | Bare top-level call |
| Clear app output in same run | placeholder/container `.empty()`/replacement | Deleting session state alone |
| User-specific secret | Secure auth/secret boundary and per-session reference | Cached data/resource argument or rendered state |

## Canonical state/form anchor

```python
import streamlit as st


if "filters" not in st.session_state:
    st.session_state.filters = {"region": "All", "minimum": 0}

with st.form("filters"):
    region = st.selectbox("Region", ["All", "North", "South"])
    minimum = st.number_input("Minimum", min_value=0)
    submitted = st.form_submit_button("Apply")

if submitted:
    st.session_state.filters = {"region": region, "minimum": minimum}

filters = st.session_state.filters
st.write(f"Applied: {filters['region']}, minimum {filters['minimum']}")
```

The form's draft widget values reach the backend together on submit. The
committed state is separate, so unrelated reruns do not silently apply drafts.

## Widget and side-effect invariants

- Widget identity must remain stable across reruns. Use explicit keys for loops,
  reusable components, pages, or same-label widgets.
- Do not write a widget-backed session key after that widget is instantiated in
  the same run; initialize first or transition it in a callback before rerun.
- Buttons are momentary triggers, not durable state. Store the resulting
  workflow state separately.
- A callback executes before the script reruns. Use it to update state, not to
  render the main result or perform an unguarded irreversible workflow.
- Uploaded files and session state are session-scoped, not durable storage.
- Module globals and cached resources may be shared between users. Protect
  mutable resources and never place per-user data there.

## Cache, forms, and fragments

`cache_data` keys by function code and arguments; omit an input only when it
truly cannot affect the result. Bound stale remote data with TTL and high-cardinality
caches with `max_entries`. `cache_resource` returns shared mutable objects;
ensure thread safety and keep user-specific state out. Read [cache and forms](references/cache-forms.md).

Fragments narrow reruns; forms delay backend updates. A fragment interacting
with external containers can accumulate elements across fragment reruns, and
shared state/resource access still needs safe ownership. Read [fragments and
testing](references/fragments-testing.md).

## Verification

Inspect the installed version of Streamlit before using drift-sensitive widget,
cache, fragment, navigation, chart-selection, or test APIs. Streamlit was absent
from this foundry during authoring; static checks do not prove an app session.

Completion requires: first run succeeds with initialized keys; each interaction
causes the intended full/form/fragment rerun; state is isolated per session;
side effects occur once; cache ownership/freshness is explicit; dynamic widget
keys are stable; empty/error/loading states render; and Streamlit's app-testing
or a real browser session verifies the interaction sequence.

## References

- [Rerun, widget, and session-state model](references/execution-state.md)
- [Caching and forms](references/cache-forms.md)
- [Fragments and interaction testing](references/fragments-testing.md)
