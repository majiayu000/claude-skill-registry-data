---
name: analytics
description: PostHog product analytics pattern — how to add/change events, identity rules, surface configs. Use BEFORE touching analytics, adding events, or anything involving tracking/telemetry in web/.
---

# Analytics (PostHog)

The code is the source of truth — `web/src/analytics.ts` IS the event
taxonomy. If your PR changes an analytics pattern, update this file in the
same PR.

## NEVER track child identity

**This is the load-bearing rule of the whole feature. No exceptions.**

- No child names, no child profile UIDs, no PINs — not as distinct ids,
  not in event properties, not in group properties, not "just for
  debugging".
- No `identify()` on any child surface (`/join`, `/play`).
- Children appear ONLY as anonymous usage inside their family group:
  `attachChildToFamily(familyId)` — group key only, never the family name
  or any other property from the child side.
- Child surfaces run `persistence: 'memory'` — no analytics
  cookies/localStorage on a kid's device, ever. Don't "improve" retention
  of the anonymous id; it is throwaway by design.
- If a requested feature needs per-child analytics to work, **STOP and
  raise it with the repo owner instead of implementing.** Parents are the
  consenting users; children consented to nothing.

## The chokepoint rule

- `web/src/analytics.ts` is the ONLY file that may import `posthog-js`
  (and only via dynamic `import()`), and the ONLY file that may contain
  event-name strings.
- Every event is a typed helper on the exported `track` object
  (snake_case, past tense names). To add an event: add the helper with a
  one-line comment saying when it fires, then call it from the UI success
  point. Nothing else — the helper list is the taxonomy.
- Helpers are fire-and-forget: never throw, silently no-op before init or
  when analytics is off. Never `await` a track call in UI flow.

## Key-unset = fully off (invariant)

`MATHIZ_POSTHOG_API_KEY` unset → `/api/v1/config` omits
`posthogKey`/`posthogHost`, the `/relay` proxy is not mounted, and the SPA
never downloads the posthog-js chunk. Self-hosters and every test run with
zero analytics. Never add an analytics code path that executes without the
key.

## Same-origin relay (part of the pattern)

The browser never talks to `*.posthog.com` — ad-blocker domain lists would
drop the events. The server proxies `/relay/*` to the configured
`MATHIZ_POSTHOG_HOST` (`internal/saas/server/posthog_proxy.go`), and
`/api/v1/config` hands the SPA `posthogHost: "/relay"`. **Never point
`api_host` at a third-party domain**; the upstream host is server-side
config only. `ui_host` stays `https://us.posthog.com` (toolbar).

## Surface configs

| Surface | init call | Options on top of the shared set* | Identity |
|---|---|---|---|
| public (`/`, `/pricing`) | `ensureAnalyticsBooted('public')` | — | anonymous |
| parent (`/login`, `/dashboard/*`) | `ensureAnalyticsBooted('parent')` (App.tsx pageview effect) | — | `identifyParent` + `identifyFamilyGroup` after `/me`; `resetAnalytics()` on sign-out; manual `$pageview` per route |
| child (`/join`, `/play`) | `ensureAnalyticsBooted('child')` | `persistence:'memory'` | `attachChildToFamily` only; NO pageviews |

\* shared: `autocapture:false`, `capture_pageview:false`,
`disable_session_recording:true`, `respect_dnt:true`,
`person_profiles:'identified_only'`, `api_host:'/relay'`.

## Verification

```bash
CGO_ENABLED=0 go build ./... && go test ./internal/saas/server/
cd web && npx tsc --noEmit && npm run lint && npm run build && cd ..
git checkout internal/saas/webui/dist/.gitkeep
# posthog-js must be a separate lazy chunk, not in the main bundle:
grep -l "PostHog" internal/saas/webui/dist/assets/*.js   # NOT index-*.js
# no posthog imports outside the chokepoint (type/bootconfig field refs ok):
grep -rn "posthog" web/src --include=*.tsx --include=*.ts | grep -v analytics.ts
```
