---
name: react-development
description: >-
  Build, debug, refactor, and review React web apps, components, and hooks. Use for JSX/TSX behavior, state and effects,
  forms, data fetching, hydration bugs, or React render performance, including React work in Next.js, React Router, and
  Vite projects. Apply when the task or inspected code involves React; a React dependency alone does not make unrelated
  backend, tooling, or CSS-only work a match.
---

# React Development

Implement the requested React behavior within the project's architecture. For review requests, report concrete
correctness issues and supported performance findings; edit only when the request includes implementation or fixes.

## Establish the local contract

- For React Router route configuration, route modules, loaders, actions, fetchers, and navigation APIs, also use the
  react-router skill when available. It owns React Router API details; this skill owns general React behavior.
- Inspect the relevant components and callers, installed React and framework versions, routing and data APIs, and
  existing checks. Identify whether the affected code runs on the server, client, or both, and whether React Compiler is
  configured for it.
- Preserve the existing visual design, component APIs, styling system, and state and data libraries unless the task
  requires changing them. For new apps, follow the user's chosen stack and project conventions.
- Consult the relevant official React or framework documentation when changing an API contract or using unfamiliar
  behavior. Match the installed version. Use newer APIs when they solve the problem, without making a framework, React
  version, or compiler migration part of an unrelated task.

## Components and state

- Follow the [Rules of React](https://react.dev/reference/rules): keep rendering pure, treat props and state as
  immutable, and obey the calling rules for the hooks in use. Fix the cause of hook lint errors instead of suppressing
  them to make a change pass.
- Keep each piece of state with its consumers or their nearest shared owner. Reuse router state, server data caches, and
  store selectors where they already own the value. Avoid creating a second synchronized copy; an editable draft is a
  separate value with an explicit reset or save boundary.
- Derive values from current props and state during rendering when possible. Put work caused by a user action in its
  event handler. Use an Effect to synchronize with an external system, with dependencies that reflect the values it
  reads. See [Effect guidance](https://react.dev/learn/you-might-not-need-an-effect).
- Pair subscriptions, timers, and external resources with cleanup. Make setup and cleanup work across dependency changes
  and remounts; do not hide lifecycle problems with a ref that prevents an Effect from running again.
- Preserve component identity and stable keys when state should survive updates. Reset state deliberately when the
  underlying entity changes. Keep form inputs consistently controlled or uncontrolled and preserve entered values during
  pending submissions and recoverable errors.

## Data and rendering boundaries

- Use the established framework loaders, actions, server components, or query cache for data they own. Avoid adding a
  component fetch for data already supplied by that layer. If an Effect is the appropriate fetch mechanism, cancel
  obsolete work or ignore stale results so late responses cannot overwrite the current view.
- Handle loading, empty, error, and mutation states at the boundary that owns the operation. Keep pending feedback
  associated with the action and provide a usable retry path when recovery is possible.
- For server-rendered UI, keep the server output and initial client render consistent. Read browser-only state at an
  appropriate client lifecycle boundary. Investigate hydration mismatches instead of broadly suppressing warnings or
  disabling server rendering.
- In frameworks with server and client components, keep browser interactivity within the necessary client boundary and
  follow the framework's serialization rules for values passed across it.

## Performance

- Protect critical rendering paths: avoid unnecessary request waterfalls, duplicate fetches, cascading state updates,
  broad subscriptions, and expensive synchronous work that delays useful HTML, hydration, or user input.
- Profile the affected interaction before adding memoization, deferred rendering, or other optimizations. Identify
  whether the delay comes from network requests, React work, or browser layout and paint, and change the responsible
  layer. A rerender alone does not establish a performance problem.
- Check [React Compiler guidance](https://react.dev/learn/react-compiler) against the project's actual configuration
  before adding or removing manual memoization. Do not assume a React version means compilation is enabled. Keep
  correctness independent of memoization and document any identity requirement imposed by an integration.

## Verify the change

Run the relevant existing lint, type, and test checks. For a behavioral fix, reproduce the original failure and add a
focused regression test when it can protect that behavior. Check the affected browser interaction when tools are
available; include rapid input or navigation for async races, and reload or hydration for server-rendered changes. Check
keyboard use and focus when changing interactive controls. Use a production build or comparable profiling conditions to
support performance claims, and report what was measured and what remains unverified.
