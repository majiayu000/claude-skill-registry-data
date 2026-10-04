---
name: outlit-sdk
description: Use when integrating Outlit tracking into web, server, native, or desktop apps; adding SDK event tracking, identity, consent, activation configuration, billing integrations, visitor tracking, customerId attribution, or troubleshooting @outlit/browser, @outlit/node, or the Rust outlit crate.
---

# Outlit SDK Integration

Decision-tree guide for adding product and website tracking to the Outlit customer context graph. Detect first, ask only when needed, keep changes small, and prefer official docs for framework-specific code.

## Branching Check

Before anything else, check whether Outlit is already installed:

1. Look for `@outlit/browser`, `@outlit/node`, `outlit` in `Cargo.toml`, `https://cdn.outlit.ai`, or existing `outlit.init(...)` / `new Outlit(...)` calls.
2. If not installed, go to [Phase 1: Quick Connect](#phase-1-quick-connect).
3. If installed, go to [Already Installed](#already-installed).

## Already Installed

Ask what they need help with, then run detection before changing code:

- Add event tracking -> [Decision 6: Event Tracking](#decision-6-event-tracking)
- Add/change auth identity -> [Decision 2: Identity](#decision-2-identity)
- Add consent management -> [Decision 1: Consent](#decision-1-consent)
- Add server/native tracking -> [Decision 7: Server and Native Tracking](#decision-7-server-and-native-tracking)
- Configure activation in Core -> [Decision 4: Activation](#decision-4-activation)
- Connect a billing integration -> [Decision 5: Billing](#decision-5-billing)
- Migrate from other analytics -> [Decision 3: Existing Analytics](#decision-3-existing-analytics)
- Debug/troubleshoot -> [Troubleshooting](#troubleshooting)

## Current API Guardrails

These points prevent the most common stale integrations:

- All current ingest SDKs use `publicKey` values that start with `pk_`. Do not use `privateKey`, `OUTLIT_PRIVATE_KEY`, `visitorId`, or `event` for `@outlit/node` examples.
- Node server events use `new Outlit({ publicKey })` and `track({ eventName, email | userId | fingerprint | customerId, properties })`.
- Browser events use `track(eventName, properties?)`; browser anonymous events are valid without identity because the SDK manages `visitorId`.
- Server `track()` requires at least one of `email`, `userId`, `fingerprint`, or `customerId`.
- Server `identify()` requires `email` or `userId`. `customerId` is optional account/workspace attribution, not a user identity by itself.
- Use `customerId` for your system-owned account/workspace/customer ID. The TypeScript SDK no longer uses `customerDomain`; do not add it.
- Browser `setUser()` can be called before tracking is enabled and will be applied after consent. Browser `identify()` requires tracking to already be enabled.
- Send ordinary `identify()` and `track()` events. Outlit Core derives activation from the configured activation event and derives engagement and inactivity from product activity.
- Billing status is account-level context supplied by verified billing integrations. Do not send SDK lifecycle or billing-status events as authoritative state.
- Event names should be `snake_case`.

## Phase 1: Quick Connect

Goal: get data flowing quickly so the user can see Outlit connection/activity without making product-strategy decisions.

### Step 1: Detect Framework and Package Manager

Check:

| Signal | How to detect |
|--------|---------------|
| Framework | `package.json` deps: `next`, `react`, `vue`, `nuxt`, `svelte`, `@sveltejs/kit`, `@angular/core`, `astro`, `express`, `fastify`, `electron`, `react-native`; `Cargo.toml` deps: `tauri`, `outlit` |
| Package manager | `bun.lockb`, `bun.lock`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json` |
| Current Outlit | `@outlit/browser`, `@outlit/node`, CDN script, Rust crate, `outlit.init`, `OutlitProvider`, `OutlitPlugin`, `new Outlit` |

### Step 2: Choose SDK

| App surface | Use |
|-------------|-----|
| Browser app: React, Next.js, Vue, Nuxt, SvelteKit, Angular, Astro, vanilla, script tag | `@outlit/browser` |
| Node backend: API routes, server actions, Express, Fastify, jobs, webhooks | `@outlit/node` |
| Native JS without browser storage: React Native, CLI, desktop main process | `@outlit/node` with a stable `fingerprint` |
| Rust backend, CLI, or Tauri backend | Rust crate `outlit` |
| Electron renderer or webview | `@outlit/browser`; use `@outlit/node` in main process only if tracking native/background events |

Install with the detected manager. Prefer `bun add` when the repo is a Bun workspace.

### Step 3: Add Public Key

Ask for the Outlit public key from **Outlit dashboard -> Settings -> Website Tracking** or onboarding.

Use the framework's public env convention:

| Framework | Env var |
|-----------|---------|
| Next.js | `NEXT_PUBLIC_OUTLIT_KEY` |
| Vite / Vue / React+Vite / Svelte | `VITE_OUTLIT_KEY` |
| SvelteKit | `PUBLIC_OUTLIT_KEY` |
| Nuxt | `NUXT_PUBLIC_OUTLIT_KEY` |
| Astro | `PUBLIC_OUTLIT_KEY` |
| Create React App | `REACT_APP_OUTLIT_KEY` |
| Angular | `environment.ts` or equivalent |
| Server/native | `OUTLIT_KEY` or `OUTLIT_PUBLIC_KEY` |

### Step 4: Minimal Setup

Fetch the framework doc from the [Doc URL Map](#doc-url-map) and implement only startup initialization:

- React/Next: prefer `OutlitProvider` from `@outlit/browser/react` in a client boundary.
- Vue/Nuxt: use `OutlitPlugin` from `@outlit/browser/vue`.
- Plain browser/script: use `@outlit/browser` or CDN script.
- Server/native: create one `Outlit` instance where the process can reuse it.

Do not add custom events, activation configuration, billing integrations, auth, or consent until basic tracking is working unless the user asked for a full integration immediately.

### Step 5: Verify Connection

Verify with one or more:

- DevTools Network has `https://app.outlit.ai/api/i/v1/<publicKey>/events` returning success.
- Browser console has no `[Outlit]` warnings.
- Server code calls `await outlit.flush()` or `await outlit.shutdown()` before process/serverless exit.
- Outlit onboarding/dashboard shows recent activity or connected tracking.

Then ask whether to continue with the full integration.

## Phase 2: Full Integration

Run detection and present what you found before changing behavior:

| Signal | How to detect |
|--------|---------------|
| Auth provider | `@clerk/*`, `next-auth`, `@auth/core`, `@supabase/*`, `@auth0/*`, `firebase`, custom session/auth files |
| Account model | `organization`, `workspace`, `team`, `account`, `tenant`, `customerId`, Stripe customer mapping |
| Billing provider | `stripe`, `@stripe/stripe-js`, `paddle`, `chargebee`, webhook routes |
| Existing analytics | `posthog-js`, `@posthog/node`, Amplitude, Mixpanel, Segment, analytics wrappers |
| Consent | Cookiebot, OneTrust, cookie banner components, CMP callbacks |
| Native/device | Tauri, Electron main process, React Native, CLI, mobile storage |
| Activation | first workspace/project/resource, first successful integration, invite sent, report generated, first meaningful feature success |
| Calendar embeds | Cal.com or Calendly embed code |

## Decision 1: Consent

| Detection | Recommendation |
|-----------|----------------|
| Existing CMP/cookie banner | Initialize with `autoTrack: false`; call `enableTracking()` from the CMP accept callback and `disableTracking()` on revoke/decline |
| EU/privacy signals but no CMP | Use `autoTrack: false` and tell the user they need a consent decision; do not build a CMP unless asked |
| No consent requirement found | Use default `autoTrack: true` |

Explain the tradeoff: `autoTrack: true` creates browser visitor storage immediately. `autoTrack: false` waits until `enableTracking()` is called.

If identity is known before consent, use the React `user` prop or `setUser()` so identity is queued and applied after tracking starts. Do not call browser `identify()` before tracking is enabled.

## Decision 2: Identity

Use the strongest identifiers available:

- `email`: primary person identifier.
- `userId`: the app/auth-provider user or contact ID.
- `customerId`: the app's account/workspace/customer/team ID.
- `customerTraits`: account/workspace metadata such as plan or seats.
- `traits`: user/contact metadata such as name or role.
- `fingerprint`: stable device/install ID for native or non-browser tracking.

Recommendations:

| Context | Pattern |
|---------|---------|
| React/Next | Pass `user={{ email, userId, customerId, traits, customerTraits }}` to `OutlitProvider` once auth resolves |
| Vue/Nuxt | Use `useOutlitUser(refOrComputedUser)` or plugin `setUser()` |
| SPA without framework helpers | Call `setUser({ email, userId, customerId })` after auth, and `clearUser()` on logout |
| Script tag | Call `window.outlit.setUser(...)` after auth, or `identify(...)` after tracking is enabled |
| Server Node | Call `identify({ email, userId, customerId })` for user/profile updates; call `track({ customerId, eventName })` for account-scoped events |
| Native/device | Track with a persistent `fingerprint`; later call `identify({ email, fingerprint })` or Rust `.fingerprint(...)` to link history |

Critical distinction: browser identify/setUser links anonymous visitor history. Server identify attributes server-side identity and can link fingerprints/customer IDs, but it does not link browser visitor cookies unless the browser also identifies.

## Decision 3: Existing Analytics

| Detection | Recommendation |
|-----------|----------------|
| Existing analytics wrapper | Add Outlit to the wrapper |
| Direct analytics calls scattered across files | Count them and ask whether to add Outlit alongside existing calls or introduce a wrapper |
| PostHog connected as data source | Do not duplicate every PostHog event by default; use SDK for missing product/website/customer identity gaps |
| No analytics | Add Outlit directly |

Keep event names `snake_case` and avoid reorganizing unrelated analytics code.

## Decision 4: Activation

Activation means a user reached the product's meaningful value moment. Outlit Core derives it from one configured ordinary product event; it is not automatically "completed onboarding" unless onboarding itself delivers value.

1. Scan for first-value actions: first project/resource created, first integration connected, first report/export generated, first invite, first successful core workflow.
2. Suggest the strongest candidate and ask for confirmation if ambiguous.
3. Reuse or add an ordinary `track()` event after the action is confirmed complete, usually after the backend succeeds.
4. Ensure the user is identified before that event when possible so Core can attribute it correctly.
5. Configure that exact event as the activation event in Outlit Core. Core derives engagement and inactivity from ongoing tracked activity.

## Decision 5: Billing

Billing is verified account-level context, separate from ordinary identity and product activity events.

| Detection | Recommendation |
|-----------|----------------|
| Stripe connected in Outlit | Verify the connection and customer mapping; let the integration supply billing status |
| Stripe in app but not connected | Recommend connecting Stripe in Outlit and verifying the customer mapping |
| Other/custom billing | Use a supported verified billing integration or source connector; do not turn webhook state into authoritative SDK events |
| No billing | Skip |

Use `identify()` and `track()` only for identity and ordinary product activity. Billing status must come from a verified billing integration rather than SDK lifecycle methods, billing enums, or custom status events.

## Decision 6: Event Tracking

Browser SDK defaults already capture:

- pageviews, including SPA navigation
- form submissions with sensitive fields removed
- auto-identify from email/name form fields
- engagement time and sessions
- Cal.com/Calendly booking events, without attendee email/name from client-side embeds

Add custom `track()` calls only for meaningful product actions that are not covered by automatic capture or connected integrations. Use properties for useful context, not PII or secrets.

Browser example:

```ts
outlit.track("project_created", { template: "blank" })
```

Server example:

```ts
outlit.track({
  customerId: "cust_123",
  eventName: "workspace_synced",
  properties: { provider: "github" },
})
```

Calendar embed limitation: Cal.com and Calendly client events do not expose attendee email/name. Use provider webhooks plus server `identify()` when booked-meeting identity matters.

Hash-routed SPAs, `file://` routes, and Electron-style hash paths are handled by the core path extractor; do not add custom path parsing unless the app has a special router.

## Decision 7: Server and Native Tracking

Use server/native tracking for backend-confirmed product activity, background jobs, native apps, CLIs, and device-based activity.

Node example:

```ts
import { Outlit } from "@outlit/node"

const outlit = new Outlit({ publicKey: process.env.OUTLIT_KEY! })

outlit.track({
  customerId: "cust_123",
  eventName: "workspace_synced",
  properties: { provider: "github" },
})

await outlit.flush()
```

Use `fingerprint` for native/desktop/mobile activity before login:

```ts
outlit.track({
  fingerprint: deviceId,
  eventName: "app_opened",
})

outlit.identify({
  email: user.email,
  fingerprint: deviceId,
  userId: user.id,
})
```

Serverless rule: `await outlit.flush()` before returning. Long-lived process rule: reuse one client and call `shutdown()` on graceful shutdown.

## Doc URL Map

Fetch docs as needed. Prefer docs over hardcoding long framework patterns, but apply the API guardrails above if examples conflict.

| Topic | URL |
|-------|-----|
| Quickstart | `https://docs.outlit.ai/tracking/quickstart` |
| How tracking works | `https://docs.outlit.ai/tracking/how-it-works` |
| Customer context graph | `https://docs.outlit.ai/concepts/customer-context-graph` |
| Website visitors | `https://docs.outlit.ai/concepts/website-visitors` |
| Identity resolution | `https://docs.outlit.ai/concepts/identity-resolution` |
| Customer journey | `https://docs.outlit.ai/concepts/customer-journey` |
| NPM/browser package | `https://docs.outlit.ai/tracking/browser/npm` |
| React | `https://docs.outlit.ai/tracking/browser/react` |
| Next.js | `https://docs.outlit.ai/tracking/browser/nextjs` |
| Vue 3 | `https://docs.outlit.ai/tracking/browser/vue` |
| Nuxt | `https://docs.outlit.ai/tracking/browser/nuxt` |
| SvelteKit | `https://docs.outlit.ai/tracking/browser/sveltekit` |
| Angular | `https://docs.outlit.ai/tracking/browser/angular` |
| Astro | `https://docs.outlit.ai/tracking/browser/astro` |
| Script tag | `https://docs.outlit.ai/tracking/browser/script` |
| Calendar embeds | `https://docs.outlit.ai/tracking/browser/calendar-embeds` |
| Node.js | `https://docs.outlit.ai/tracking/server/nodejs` |
| Rust / Tauri | `https://docs.outlit.ai/tracking/server/rust` |
| Ingest API | `https://docs.outlit.ai/api-reference/ingest` |
| Full docs index | `https://docs.outlit.ai/llms.txt` |

## Troubleshooting

### No browser events

1. Confirm the public env var prefix is correct and exposed to the client bundle.
2. Confirm provider/init runs once at app startup and wraps the app.
3. If `autoTrack: false`, call `enableTracking()` after consent.
4. Check Network for `/api/i/v1/<publicKey>/events`.
5. Check console warnings such as tracking not enabled, already initialized, or multiple instances.

### Events not linked to users

- Prefer `OutlitProvider user`, `useOutlitUser`, or `setUser()` for auth state.
- Send both `email` and `userId` when available.
- Include `customerId` for account/workspace-scoped products.
- Browser identity links visitor history; server identity does not replace browser identity.
- For native/device history, reuse the same persistent `fingerprint` before and after login.

### Server events missing

- Use `publicKey`, not `privateKey`.
- Use `eventName`, not `event`.
- Provide at least one of `email`, `userId`, `fingerprint`, or `customerId` to `track()`.
- `identify()` needs `email` or `userId`.
- Always `await outlit.flush()` before serverless handlers return.
- Non-retryable ingest errors stop automatic retries until restart; fix credentials/config instead of waiting.

### Activation missing or delayed

- Confirm the configured activation event name exactly matches the event sent with `track()`.
- Confirm identity is set before the event when possible and that the event reaches Outlit.
- Core derives activation from that configured event and engagement/inactivity from activity; do not send separate lifecycle state.

## Key Principles

- Minimal changes: instrument the existing app shape.
- Detect first, ask second.
- Use `customerId` for account/workspace context.
- Use `setUser`/provider user for auth lifecycle.
- Use `track()` for product activity; configure the activation event in Core and let Core derive lifecycle state.
- Let verified billing integrations supply billing status.
- Flush server/native queues before exit.
- Keep events `snake_case`.

## Installation

Install this skill through the Outlit CLI when possible:

```sh
outlit setup skills
```

Or with the Skills CLI:

```sh
npx -y skills add OutlitAI/skills --skill outlit-sdk -g
```
