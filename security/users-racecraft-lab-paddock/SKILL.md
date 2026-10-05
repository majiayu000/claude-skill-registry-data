---
name: users
description: "Skill for the Users area of paddock. 45 symbols across 12 files."
---

# Users

45 symbols | 12 files | Cohesion: 78%

## When to Use

- Working with code in `src/`
- Understanding how getMcSessionCookieName, isRequestSecure, parseMcSessionCookieHeader work
- Modifying users-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/lib/auth.ts` | warnProxyAuthMisconfigOnce, safeCompare, getDefaultWorkspaceContext, getWorkspaceIdFromRequest, getTenantIdFromRequest (+15) |
| `src/lib/session-cookie.ts` | getMcSessionCookieName, isRequestSecure, parseMcSessionCookieHeader, envFlag, getMcSessionCookieOptions |
| `src/lib/security-events.ts` | normalizeSecurityEventType, calculateAgentTrustScore, logSecurityEvent, updateAgentTrustScore |
| `src/lib/password.ts` | hashPassword, verifyPasswordWithRehashCheck, verifyPassword |
| `src/app/api/auth/users/route.ts` | POST, PUT, DELETE |
| `src/app/api/setup/route.ts` | GET, POST |
| `src/app/api/auth/me/route.ts` | GET, PATCH |
| `src/app/api/auth/google/route.ts` | upsertAccessRequest, POST |
| `src/lib/google-auth.ts` | verifyGoogleIdToken |
| `src/lib/db.ts` | needsFirstTimeSetup |

## Entry Points

Start here when exploring this area:

- **`getMcSessionCookieName`** (Function) — `src/lib/session-cookie.ts:6`
- **`isRequestSecure`** (Function) — `src/lib/session-cookie.ts:10`
- **`parseMcSessionCookieHeader`** (Function) — `src/lib/session-cookie.ts:15`
- **`getMcSessionCookieOptions`** (Function) — `src/lib/session-cookie.ts:35`
- **`calculateAgentTrustScore`** (Function) — `src/lib/security-events.ts:62`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `getMcSessionCookieName` | Function | `src/lib/session-cookie.ts` | 6 |
| `isRequestSecure` | Function | `src/lib/session-cookie.ts` | 10 |
| `parseMcSessionCookieHeader` | Function | `src/lib/session-cookie.ts` | 15 |
| `getMcSessionCookieOptions` | Function | `src/lib/session-cookie.ts` | 35 |
| `calculateAgentTrustScore` | Function | `src/lib/security-events.ts` | 62 |
| `logSecurityEvent` | Function | `src/lib/security-events.ts` | 78 |
| `updateAgentTrustScore` | Function | `src/lib/security-events.ts` | 121 |
| `hashPassword` | Function | `src/lib/password.ts` | 11 |
| `verifyPasswordWithRehashCheck` | Function | `src/lib/password.ts` | 22 |
| `verifyPassword` | Function | `src/lib/password.ts` | 42 |
| `verifyGoogleIdToken` | Function | `src/lib/google-auth.ts` | 10 |
| `needsFirstTimeSetup` | Function | `src/lib/db.ts` | 353 |
| `safeCompare` | Function | `src/lib/auth.ts` | 42 |
| `getWorkspaceIdFromRequest` | Function | `src/lib/auth.ts` | 172 |
| `getTenantIdFromRequest` | Function | `src/lib/auth.ts` | 177 |
| `createSession` | Function | `src/lib/auth.ts` | 188 |
| `destroyAllUserSessions` | Function | `src/lib/auth.ts` | 274 |
| `authenticateUser` | Function | `src/lib/auth.ts` | 285 |
| `getUserById` | Function | `src/lib/auth.ts` | 333 |
| `createUser` | Function | `src/lib/auth.ts` | 356 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `PATCH → EnsureDirExists` | cross_community | 7 |
| `PATCH → CalculateAgentTrustScore` | cross_community | 7 |
| `PATCH → Generate` | cross_community | 7 |
| `POST → EnsureDirExists` | cross_community | 7 |
| `POST → CalculateAgentTrustScore` | cross_community | 7 |
| `POST → Generate` | cross_community | 7 |
| `GET → EnsureDirExists` | cross_community | 7 |
| `GET → CalculateAgentTrustScore` | cross_community | 7 |
| `GET → Generate` | cross_community | 7 |
| `POST → EnsureDirExists` | cross_community | 7 |

## Connected Areas

| Area | Connections |
|------|-------------|
| [id] | 27 calls |
| Cluster_289 | 4 calls |
| Cluster_191 | 1 calls |

## How to Explore

1. `gitnexus_context({name: "getMcSessionCookieName"})` — see callers and callees
2. `gitnexus_query({query: "users"})` — find related execution flows
3. Read key files listed above for implementation details
