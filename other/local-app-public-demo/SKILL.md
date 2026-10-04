---
name: local-app-public-demo
description: Turn a local app that writes to disk into a static, read-only public demo built from the same codebase, with machine paths and secrets removed and every write degraded to an honest message. Use when someone needs to show a local tool to a client or collaborator without them installing anything, when a server app cannot deploy as-is to static hosting, or when a demo build must be verified free of private data before going public.
---

# Local App to Public Demo

Someone wants to see what you built. Installing it is too much to ask, and the
app cannot deploy as-is because it writes to disk, shells out, or depends on a
local session.

The answer is not a rewrite and not a screen recording. It is a **static
snapshot**: the same frontend, served against frozen copies of its own API
responses, with writing turned off honestly.

This skill covers building that snapshot and, more importantly, verifying it is
safe to make public. Pair it with `github-safe-publisher` when the source code is
also going out.

## When to use

- Showing a local tool to a client, collaborator, or prospective employer.
- A server app that cannot run on static hosting as-is.
- Publishing a portfolio piece from something that normally runs on one machine.
- Verifying an existing demo build carries no private data.

## The core decision: one codebase, not a fork

Copy the app into a `demo/` folder and edit it there and the two drift within a
week. Instead:

- Ship a tiny config file in the real app, for example `demo-config.js`, holding
  a single flag set to false.
- The build copies the frontend verbatim and **overwrites only that one file**
  with the flag set to true.
- The frontend branches on the flag in exactly one place: its data layer.

Everything else stays identical, which means fixing a bug fixes it in both.

## Workflow

### 1. Inventory what the frontend reads

List every endpoint it fetches. That list is the contract. Anything missed
becomes a blank page in the demo with no error.

### 2. Freeze responses as static files

With the real app running, fetch each endpoint and write it as JSON at a path the
demo can reach. Map API routes to file paths with one small pure function, so the
mapping is testable and obvious.

### 3. Make writes refuse honestly

Route reads and writes through one data-layer object. In demo mode:

- Reads fetch the frozen JSON and return null on a miss.
- **Writes return a friendly refusal instead of calling the network.**

Write the refusal as a human sentence, and make it the value callers already
check. If callers do `if (result.error) show(result.error)`, then the friendly
sentence must be that error string, or a raw internal message reaches the screen.

Hide controls that cannot mean anything in a demo, like delete buttons.

### 4. Shrink the images

Original assets are usually far too heavy to host. Downscale to a sensible
maximum width and re-encode to a web format. An order-of-magnitude reduction is
normal, and re-encoding also drops embedded metadata as a side effect.

### 5. Strip everything private

This is the step that matters most. See `references/scrub-checklist.md`.

The category people forget: **absolute paths displayed in the interface.** A
local tool naturally shows a person where files live. Those strings are one
machine's folder layout, and they go public with the demo. Fix it properly by
having the server report its own base path and the frontend build paths from it,
rather than deleting the feature.

### 6. Label it

A visible banner saying what this is, who built it, and that it is read-only.
People who cannot tell whether a thing is live will assume it is broken.

### 7. Verify before deploying, and again after

Build, serve locally, and click every route. Then grep the built output, not the
source tree, for machine paths, usernames, key prefixes, and session folder
names. Confirm every private directory is absent.

After deploying, open the live URL from an unauthenticated session and confirm
it is actually reachable and images actually load.

## Rules

- One codebase with a flag, never a forked copy.
- Every write degrades to an honest message, never a silent no-op and never a
  raw error.
- Grep the built artifact, not the source. Source-tree greps miss generated
  files, and the artifact is what ships.
- Never republish third-party material that was gathered for private use, such as
  photos found by search. Your own assets are fine; other people's are not.
- If the hosting platform's access control is a paid feature, say so plainly
  rather than implying an unguessable URL is protection.
- Whatever gets added to the app later must be added to the snapshot too, or the
  demo breaks silently. Write that down where the next person will see it.

## Output

A `demo/` folder that serves as pure static files, a stated total size, a
verification report showing zero matches for each private pattern, and the live
URL confirmed reachable without authentication.
