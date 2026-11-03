---
name: menuyukti-mobile
description: >-
  DEPRECATED / inactive Expo React Native app (apps/mobile-app). Kept in the repo but not an
  active product track — prefer the web customer PWA in apps/web. Use this skill only when
  maintaining legacy CRM enroll, device keys, React Navigation, or mobile BFF clients.
---

# Menuyukti: `apps/mobile-app` (deprecated)

**Status:** **Deprecated / inactive.** Customer focus is the **web PWA** (`apps/web` customer shell + Serwist). Keep this app in the monorepo for now; do not expand it as the primary customer path. Prefer [`menuyukti-web`](../menuyukti-web/SKILL.md) for new customer work.

**Expo** (React Native) CRM client (legacy): enroll via CRM token, then Home / Rewards / Profile. **Product data** goes through the **Next.js mobile BFF** (proxies private GraphQL). CRM enroll: `POST /api/mobile/crm/v1/enroll` on the web app.

For monorepo boundaries, see [`menuyukti-repo-orientation`](../menuyukti-repo-orientation/SKILL.md).

## Companion skills

When implementing in **`apps/mobile-app`**, follow these skills in addition to this doc.

### Feature work (default)

- [`expo-native-ui`](../expo-native-ui/SKILL.md) — Native-feeling screens, layout, colors, controls.
- [`expo-data-fetching`](../expo-data-fetching/SKILL.md) — Network/API calls, caching, errors.
- [`react-navigation`](../react-navigation/SKILL.md) — Stacks, tabs, headers, safe areas (this app uses React Navigation, **not** Expo Router).
- [`vercel-composition-patterns`](../vercel-composition-patterns/SKILL.md) — Compound components and context providers.

### Upgrades, shipping, and performance

- [`expo-upgrade`](../expo-upgrade/SKILL.md) — Expo SDK upgrades and dependency fixes.
- [`expo-dev-client`](../expo-dev-client/SKILL.md) — Dev clients when native modules need a custom build.
- [`expo-examples`](../expo-examples/SKILL.md) — Canonical Expo `with-*` integration patterns.
- [`eas-app-stores`](../eas-app-stores/SKILL.md) / [`eas-workflows`](../eas-workflows/SKILL.md) — Store release and EAS CI.
- [`react-native-best-practices`](../react-native-best-practices/SKILL.md) — FPS, TTI, lists, re-renders, bundle size.

**Do not** restructure this app to match Expo Router “new project” layouts. Prefer React Navigation skills over Expo Router unless migrating intentionally.

## Layout (high level)

| Concern              | Typical locations                                                                                                                                                                                                                                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Entry                | [`App.tsx`](../../../apps/mobile-app/App.tsx), [`index.ts`](../../../apps/mobile-app/index.ts)                                                                                                                                                                                                                                  |
| Navigation           | [`navigation/RootNavigator.tsx`](../../../apps/mobile-app/navigation/RootNavigator.tsx), [`MainTabs.tsx`](../../../apps/mobile-app/navigation/MainTabs.tsx)                                                                                                                                                                     |
| Screens              | [`screens/`](../../../apps/mobile-app/screens/) — `EnrollScreen`, `HomeScreen`, `RewardsScreen`, `ProfileScreen`                                                                                                                                                                                                                |
| UI primitives        | [`components/`](../../../apps/mobile-app/components/) — `Screen`, `Button`, `TextField`, cards                                                                                                                                                                                                                                  |
| Theme / brand        | [`theme/tokens.ts`](../../../apps/mobile-app/theme/tokens.ts), [`BrandContext.tsx`](../../../apps/mobile-app/theme/BrandContext.tsx), [`SessionContext.tsx`](../../../apps/mobile-app/theme/SessionContext.tsx)                                                                                                                 |
| CRM enroll + session | [`lib/enroll.ts`](../../../apps/mobile-app/lib/enroll.ts), [`lib/keys.ts`](../../../apps/mobile-app/lib/keys.ts), [`sessionStorage.ts`](../../../apps/mobile-app/lib/sessionStorage.ts), [`sessionCodec.ts`](../../../apps/mobile-app/lib/sessionCodec.ts), [`secureStorage.ts`](../../../apps/mobile-app/lib/secureStorage.ts) |
| CRM auth / API       | [`lib/crmAuth.ts`](../../../apps/mobile-app/lib/crmAuth.ts), [`crmClient.ts`](../../../apps/mobile-app/lib/crmClient.ts), [`accessToken.ts`](../../../apps/mobile-app/lib/accessToken.ts), [`tokenStorage.ts`](../../../apps/mobile-app/lib/tokenStorage.ts), [`signNonce.ts`](../../../apps/mobile-app/lib/signNonce.ts)       |
| Cashback             | [`lib/cashback.ts`](../../../apps/mobile-app/lib/cashback.ts) — authenticated CRM reads via `crmFetch`                                                                                                                                                                                                                          |
| Mock / demo data     | [`data/mockRestaurant.ts`](../../../apps/mobile-app/data/mockRestaurant.ts)                                                                                                                                                                                                                                                     |
| Expo config          | [`app.json`](../../../apps/mobile-app/app.json), [`package.json`](../../../apps/mobile-app/package.json)                                                                                                                                                                                                                        |

Commands: [`apps/mobile-app/package.json`](../../../apps/mobile-app/package.json) scripts (`pnpm --filter mobile-app …`).

## Boundaries

- **No database drivers** or migrations in the mobile app — call GraphQL / CRM HTTP only.
- Prefer **pnpm** (`pnpm --filter mobile-app …` from repo root, or scripts inside `apps/mobile-app`).
- Secrets: use `EXPO_PUBLIC_*` only for non-secret public config (e.g. `EXPO_PUBLIC_CRM_API_URL`). Device private keys stay in **SecureStore** (native) or localStorage (web demo) via `lib/keys.ts` — never log or ship private key material.
- CRM enroll backend lives in **`apps/graphql`** (`crm_auth/`, `/crm/v1/enroll`) — see [`menuyukti-graphql`](../menuyukti-graphql/SKILL.md).

## Session and navigation

1. **`SessionProvider`** hydrates `session` (`customerId`, `deviceId`, optional `appId`) and profile from SecureStore; exposes `isHydrated` so the navigator does not flash enroll.
2. **`RootNavigator`**: native stack with `Enroll` | `Main` (tabs), gated by hydrated session. Deep links use scheme `menuyukti` (`menuyukti://enroll?token=…&app=…`).
3. Enroll flow: parse token / deep link → `ensureDeviceKeypair()` → `enrollDevice()` → persist session → tabs.
4. **`resetSession`** clears SecureStore session, profile, and device key.

Brand theming uses **`BrandProvider`** + Warm Editorial tokens in `theme/tokens.ts` (aligned with web/UI brand colors). Override via `brand` prop for white-label builds.

## Networking

- Public BFF base: `EXPO_PUBLIC_CRM_API_URL` (default `http://localhost:3000`).
- Enroll: `POST /api/mobile/crm/v1/enroll` (`lib/enroll.ts`).
- Authenticated CRM: `crmFetch` (`lib/crmClient.ts`) → `/api/mobile/crm/v1/*` with device access token from `crmAuth` / `accessToken` (refresh token in SecureStore via `tokenStorage`).
- Example product read: cashback via `lib/cashback.ts` (`GET .../me/cashback`).
- Quality: `pnpm lint` (ESLint / `eslint-config-expo`), `pnpm check-types`, `pnpm test`, `pnpm check:expo` (`expo-doctor`), `pnpm format-check`.
- Keep new client code under `lib/` and follow [`expo-data-fetching`](../expo-data-fetching/SKILL.md).

## Related

| Topic            | Skill                                                                  |
| ---------------- | ---------------------------------------------------------------------- |
| CRM / enroll API | [`menuyukti-graphql`](../menuyukti-graphql/SKILL.md)                   |
| Monorepo map     | [`menuyukti-repo-orientation`](../menuyukti-repo-orientation/SKILL.md) |
| Web counterpart  | [`menuyukti-web`](../menuyukti-web/SKILL.md)                           |

## Canonical docs

- Expo docs matching the app’s SDK (see `apps/mobile-app/package.json` `expo` version)

## Progressive disclosure

Split long screen or API maps into `reference.md` in this folder if this file grows.
