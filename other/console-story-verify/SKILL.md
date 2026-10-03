---
name: console-story-verify
description: Verify console and ui-web UI work in Storybook before merging — how to run or statically build Storybook, find the right story, take a screenshot, and avoid another agent's stale dev server. Use whenever UI in packages/ui-web or apps/console changed and someone needs to SEE it, or when a task says "verify visually", "screenshot", "check the story", or "Storybook-first".
---

# Storybook-first verification

**Standing owner directive: visual work is verified in Storybook before it merges.** A live deploy
is confirmation, not discovery. A passing unit test is not a screenshot.

Every console screen is Keycloak-gated, so the browser cannot reach it locally without a session.
Storybook renders the same `packages/ui-web` sections against fixtures with no auth at all — that is
why it is the verification surface. `apps/lci`'s screens are in the same Storybook (its stories live
in `apps/lci/src`; `.storybook/main.ts` globs both trees).

## Find the story first

Sidebar folders and the rules for adding a story: `packages/ui-web/STORYBOOK.md`.

| What changed                               | Story title                       | File                                                            |
| ------------------------------------------ | --------------------------------- | --------------------------------------------------------------- |
| A `dashboards.yaml` panel                  | `Dashboard/FromSpec`              | `packages/ui-web/src/pages-stories/spec-page.tsx`               |
| A whole admin/settings screen              | `Pages/<Area>/<Screen>`           | `packages/ui-web/src/pages-stories/<screen>.stories.tsx`        |
| One primitive                              | `Primitives/<Group>/<Name>`       | `packages/ui-web/src/components/<name>/component.stories.tsx`   |
| One section                                | `Sections/<Area>/<Name>`          | `packages/ui-web/src/sections/<name>/component.stories.tsx`     |
| A chart mark                               | `Charts/<Name>`                   | `packages/ui-web/src/components/<name>/component.stories.tsx`   |
| German rendering                           | `Pages/Platform/I18nGerman`       | `packages/ui-web/src/pages-stories/i18n-german.stories.tsx`     |
| The shell itself (rail, footer, switchers) | `Pages/Platform/ShellPersistence` | `shell-fixtures.tsx` and `shell-persistence.stories.tsx`        |
| An LCI screen                              | `Pages/LCI/<Screen>`              | `apps/lci/src/containers/<screen>.stories.tsx`                  |
| An LCI component                           | `LCI/<Name>`                      | same directory as the component                                 |
| Loading / empty / error state              | —                                 | The same story file — every screen story carries those variants |

Every console and LCI screen has a page story; if you cannot find one for the screen you changed,
look again before concluding it has none (`ls packages/ui-web/src/pages-stories/`,
`ls apps/lci/src/containers/*.stories.tsx`).

`Dashboard/FromSpec` reads the **real** `apps/console/dashboards.yaml` and the **real**
`apps/console/locales/en/dashboards.json`. There is no fixture to update, and a panel showing a raw
i18n key means the locale files are incomplete.

**LCI stories run against bundler stubs, not a Next server.** `next/link`, `next/navigation`, the
Server Action modules and `lib/server/session` are aliased in `.storybook/main.ts` — so navigation
and writes are inert in a story. That is deliberate: a story certifies that a control exists and is
enabled/disabled correctly for the given permissions; what the action does to the control plane is
`apps/lci`'s own vitest suites' job.

## Method A — dev server (interactive, fastest to iterate)

```sh
pnpm --filter @lightbridge/ui-web storybook   # serves on :6007
```

**Before you start it, check port 6007 is not already serving somebody else's tree.** Parallel
agents in sibling worktrees run this constantly, and a stale server will happily render the OLD
component while you conclude your change did nothing.

```sh
lsof -nP -iTCP:6007 -sTCP:LISTEN          # is anything there?
curl -s localhost:6007/index.json | head  # whose stories are they?
```

If it is not yours: **do not kill it.** Start yours on another port
(`pnpm --filter @lightbridge/ui-web exec storybook dev -p 6017`) and use that.

## Method B — static build (deterministic, and what CI runs)

Preferred when you only need a screenshot, and the only method that also proves the story builds:

```sh
pnpm --filter @lightbridge/ui-web build-storybook   # -> packages/ui-web/storybook-static
npx --yes http-server packages/ui-web/storybook-static -p 6100 --silent &
```

Then open one story directly, no manager chrome, no navigation:

```
http://localhost:6100/iframe.html?id=<story-id>&viewMode=story
```

Story ids come from `packages/ui-web/storybook-static/index.json` — grep it rather than guessing
(`Dashboard/FromSpec` → `dashboard-fromspec--<variant>`; `Pages/LCI/Overview` →
`pages-lci-overview--<variant>`). Ids are derived from the title, so the 2026-09-03 folder
reorganisation changed every one of them — never reuse an id from an older document.

Screenshot it with the browser tooling available in your harness. Both themes matter: the console is
**dark by default (`black`) with a first-class light theme (`wireframe`)**. Check both, and check a
narrow viewport if you touched layout.

Stop the server when done.

## What to actually look at

- The **empty, loading and error** states, not just the happy path. Empty states are inline status
  lines, never centred placards.
- **Both themes.** A hardcoded colour shows up only in one.
- **Values on hover, never a legend list** under a chart.
- The **expanded** panel dialog if you touched a panel: it renders at a different DATA density
  (more ticks, 25 rows instead of 10), not as a scaled-up screenshot.
- German (`i18n-german.stories.tsx`) if you touched copy — German strings are longer and break
  tight layouts.

## The verification bar

Claim "verified" only with all of these, and paste the real output:

```sh
pnpm --filter @lightbridge/ui-web test          # includes the story-taxonomy guard
pnpm --filter @lightbridge/ui-web typecheck
pnpm --filter @lightbridge/ui-web build-storybook
```

If you touched an LCI story, `pnpm --filter lci test` and `pnpm --filter lci typecheck` too — those
story files are inside `apps/lci`'s tsconfig.

plus **a screenshot path in the PR body's `## Screenshots / Evidence` section**. "Looks right" with
no image is not evidence.

If the change is in `apps/console` too:

```sh
pnpm --filter console test
pnpm --filter console typecheck
pnpm --filter console build:web
```

## Pitfalls

- **A stale dev server from another agent is the single most common false result.** Check before you
  trust what you see. Symptom: your edit "has no effect".
- **`build-storybook` is the gate CI runs**, and it fails on a broken story even when the dev server
  rendered fine (different bundler path).
- **Storybook is not GitHub Pages here.** Pages is disabled on this repo; `storybook-pages.yml`
  skips its deploy job by design. Do not link a Pages URL as evidence — it will not exist.
- **`pnpm --filter console build` is not a script.** It is `build:web`.
- **Do not add a story that duplicates fixture data the YAML already carries.** For dashboards, the
  fixture path IS the YAML.
- **A duplicate `title:` silently merges two stories into one sidebar entry** — no warning, and
  `build-storybook` still passes while one of them stops being reachable.
  `packages/ui-web/src/story-taxonomy.test.ts` (and `node scripts/storybook-taxonomy.mjs --check`)
  is the gate for that; do not work around it by renaming to something outside the taxonomy.
