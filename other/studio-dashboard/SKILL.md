---
name: studio-dashboard
description: "Retired: the Ponti Studio dashboard no longer exists."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ponti-studios, retired]
    related_skills: [studio-editorial, studio-imagegen]
---

# Retired — Ponti Studio dashboard

**This skill is a tombstone.** The SvelteKit dashboard (`apps/web`), the SQLite pipeline database
(`packages/database`) and the `@studio/contracts` schemas were deleted when Ponti Studio became
skills-only. There is no dev server, no route map, no `pnpm dev:web`. The last commit that carried
the app is tagged `web-app-final` in the `studio` repo.

Do not re-introduce app instructions here. If the work is "drive the pipeline", load
`studio-editorial` / `studio-imagegen` / `studio-workflows` (the `studio-videogen` procedure) / `studio-podcastgen`; if it is
"delete another surface", load `subsystem-removal`.

## What survives from it

These were learned on the dashboard but are not about it — they apply to any served UI, and they
are the reason this file is not empty:

- **Pin the runtime and prove which one booted.** A `node` resolved from `PATH` may not be the
  repo's pin; a native module compiled for another ABI fails every route that touches it while a
  route reading a JSON file still answers `200`. Read the version out of the startup log rather
  than trusting the shell.
- **One green route is not a working app.** Check two routes that read different stores before
  concluding a boot is healthy.
- **Relative hrefs resolve one level too high** on routes served without a trailing slash
  (`trailingSlash: 'never'`): `href="outputs?tab=essay"` becomes `/projects/outputs?…` → 404.
  Build links from the id, and request every `?tab=` value a user has never clicked.
- **`200` proves the route exists, not that the page is right.** Assert on counts, on painted
  values (`getComputedStyle`, not class attributes), and on hrefs extracted from the HTML.
- **Prove a write path with the cheapest real call**, not by mutating the user's data; prove an
  unreachable read branch by temporarily forcing the `load` value, then restoring it and
  re-verifying.
- **A gate that flips state must hand over to the next choice.** A button that only recolours a
  status pill reads as "nothing happened" even when the server did the work.
- **Derive status from data, never from page copy**, and never compare a derived count to a
  literal — a five-item list can never equal seven, so the step silently never completes.
- **A UI that claims provenance must persist it server-side.** Client-state-only pins forget their
  source on reload.
