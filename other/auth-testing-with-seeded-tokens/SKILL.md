---
name: auth-testing-with-seeded-tokens
description: >-
  Use when writing browser tests for sign-in redirects, protected-route bounces or
  destination-preservation in a repository whose production-parity test image seeds every visitor
  with an auth token for Lighthouse and Playwright runs. Symptoms include an end-to-end spec that
  can never reach the logged-out state, a protected route that never redirects under test, and
  acceptance criteria wording that assumes an unauthenticated first visit.
---

# Auth Testing With Seeded Tokens

## Profile keys consumed

- `make.test_unit_client`
- `make.test_e2e`
- `make.test_visual`
- `make.start_prod`
- `make.lighthouse_desktop`
- `make.lighthouse_mobile`
- `capabilities.visual_testing`
- `capabilities.lighthouse`

Every suite runs through the profile's `make` target map. Skip a suite with a recorded
capability-absent note when its key maps to `null`, or when `capabilities.visual_testing` /
`capabilities.lighthouse` is `false` — never improvise a raw host command in its place.

## Overview

When the production-parity test image preloads an auth token so audits — the Lighthouse runs mapped
by `make.lighthouse_desktop` / `make.lighthouse_mobile`, gated on `capabilities.lighthouse` — can
reach protected routes without a real login, every browser visitor starts authenticated and the logged-out paths become
unreachable end to end. Split the coverage instead of weakening the seam: unit tests own the
absent-state logic, browser tests own the state transition.

## When to use

- An end-to-end or visual spec needs a logged-out visitor and the app is already authenticated.
- Testing a bounce-and-return flow: a protected route stores the attempted destination and sign-in
  returns the user to it.
- Writing acceptance criteria for auth controls whose wording assumes a first visit with no session.
- Reviewing a spec that clears storage to fake the logged-out state and now diverges from what the
  audited build actually does.
- Not for: repositories with no preloaded-token seam, and not for server-side authorization tests —
  the client guard is a UI affordance, never the authorization boundary.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — the seam is `src/config/env/preloaded-auth-token.ts`, read only by a build that set
  `ENABLE_PRELOADED_AUTH_TOKEN_SEED`, which is the `test-harness` Dockerfile stage that the
  production-parity compose file builds behind `make.start_prod`; the guard is pinned by the
  repository's preloaded-auth seed-gate target and the protected-route guard lives in the auth
  feature module under the source root.
- **Next.js app shape** (routed pages, no aggregate duplication gate): no — no preloaded-token seam
  or protected route.
- **Component-library shape** (Storybook-first, no bootable app, published package): no — component
  library, no auth routes.

```bash # profile-example
# With a profile whose make.start_prod maps to `start-prod`, the seed-gate target is a
# repository-specific sibling:
make check-auth-seed-gate
```

## Core pattern

The seam returns `null` unless the build opted in, so the guard and both reads must stay inside one
function body for the bundler to fold them away:

```ts
public read(currentWindow?: PreloadedAuthTokenWindow): string | null {
  if (
    process.env.NODE_ENV === 'production' &&
    process.env.ENABLE_PRELOADED_AUTH_TOKEN_SEED !== 'true'
  ) {
    return null;
  }
  // window global first, then the build-time token
}
```

Because the audited build always opts in, plan the test split before writing either suite:

- **Unit tests own the unauthenticated path.** Rendering the protected route with no token stores
  the attempted location; a subsequent sign-in navigates back to it. These tests control the token
  directly, so they can express the state the browser suite cannot reach. They run through the
  target mapped by `make.test_unit_client`.
- **Browser tests own the authenticated transition.** With the seeded session in place, assert the
  complementary property — signing in while already authenticated does not navigate away, and the
  protected route renders rather than bouncing. They run through the targets mapped by
  `make.test_e2e` and `make.test_visual`; skip the visual half with a recorded note when
  `capabilities.visual_testing` is `false`.

Together the two prove the whole flow: the unit suite proves the absent-state logic, the browser
suite proves the transition against the real build.

## Procedure

1. Confirm which build sets the opt-in flag; only the ephemeral test image should. A deployable
   build must contain neither the window key nor the token literal.
2. Write the unit tests for every branch that depends on the token being absent, and assert the
   stored destination explicitly rather than inferring it from a final URL.
3. Write the browser spec for the authenticated side only, and name it for what it asserts.
4. Record in the pull request body which acceptance criterion is covered by units instead of by the
   browser suite, and why — an untested-looking criterion with no explanation reads as a gap.

## Common mistakes

- Rewriting the unit test to dodge the logged-out scenario — that unit test is the only proof the
  absent-state logic works.
- Clearing browser storage inside the spec to fake a logged-out visitor — the audited build seeds
  the token again on the next load, so the spec becomes flaky rather than correct.
- Moving a token read out of the guarded method to "tidy" it — constant folding is scope-local, and
  the identifier then ships in every production bundle.
- Adding the opt-in flag to a dotenv file — the bundler merges dotenv keys into the process
  environment, so it silently re-enables the seed for local and deployable builds.
- Reading the passing browser suite as proof that route protection works — it is a client-side UI
  guard; the upstream API service rejecting an unauthenticated request is what protects the data.
