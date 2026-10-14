---
name: state-management
description: "State management: own state minimally, avoid redundant/duplicate state, handle loading/error/empty/offline/optimistic UI."
---

# state-management

One owner per datum; everything else derives or syncs through a query layer.

## Activate when

- Placing state, choosing client/server/cached stores, or fixing stale/duplicate-state bugs.

## Do NOT activate for

- Component structure (see ui-architecture); backend caching (see backend/caching).

## Inspection

List every piece of state, its owner, its sync path, and its loading/error/empty/offline handling. Flag mirrors (server data copied into useState) and useEffect syncs between stores.

## Decision rules

- Server state → query library (cache, dedupe, retry, invalidation built in); never hand-rolled fetch + useState mirrors.
- Client UI state stays local until proven shared; cross-cutting client state → minimal store (Zustand/signals), not Redux-by-default.
- Derived data computes (selectors/memo), never stored; optimistic updates with rollback on failure; offline queue where the product promises it.

## Procedure

1. Assign each datum one owner; delete mirrors and effect-syncs.
2. Cover all async states per datum: loading skeleton, error with retry, empty with guidance, offline behavior.
3. Verify: no duplicated state (grep for parallel copies), state transitions tested, offline/error paths demonstrated.

## Failure modes

- Mirrored server state drifting; two stores synced by effect loops; global store for local concerns; optimistic UI without rollback; loading spinners with no error path.

## Escalation

Persistence choice (MMKV/AsyncStorage/secure store on mobile) → frameworks/react-native; server cache semantics → backend/caching.

## References

- Related: `../ui-architecture/`, `../component-design/`.
