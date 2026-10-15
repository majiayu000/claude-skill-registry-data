---
name: firestore-mastery
description: >-
  Firebase/Firestore guidance: project setup, security rules, data modeling, indexes, query performance, cost, auth, real-time listeners, migrations. Use for Firebase, Firestore, security rules, NoSQL schema design or Firebase Authentication.
---

# Firestore Mastery

Expert guidance for Cloud Firestore architecture, security, and operations.

## Core philosophy

Firestore is read-optimized. Design schemas to match UI queries, not entity relationships. Accept denormalization as the norm.

Key constraints:
- 1 MiB max document size
- 1 write/sec sustained per document (soft limit)
- No server-side JOINs
- Security rules are NOT filters
- Queries scale with result size, not dataset size

## Reference files

Load based on the task:

| Task | Reference file |
|------|----------------|
| Security rules, auth, RBAC | `references/security-rules.md` |
| Indexing, queries, transactions, costs | `references/performance-ops.md` |
| Schema design, relationships, patterns | `references/data-architecture.md` |
| Limits, error codes, decision trees | `references/quick-reference.md` |
| Code templates (CRUD, pagination, listeners, counters, transactions), starter rules, emulator tests, deploy commands | `references/code-templates.md` |

## Workflow by task type

### Project setup

1. Choose database mode: **Native** (default: mobile/web, real-time sync, offline) or **Datastore** (server-only, massive write throughput, no real-time).
2. Run `firebase init firestore`.
3. Start with locked rules (`allow read, write: if false;`), then add specific allowances. Starter rules: `references/code-templates.md`.

### Security rules

**Always load `references/security-rules.md`.** Core patterns: owner access (`request.auth.uid == userId`), RBAC through custom claims (preferred over database lookups), schema enforcement with `request.resource.data` type checks. Snippets: `references/code-templates.md`.

**Critical: rules are not filters.** Query constraints must match rule constraints.

### Schema design

**Always load `references/data-architecture.md`.** Decision flow for child data:
1. Owned exclusively by parent? Consider a subcollection.
2. Need cross-parent queries? Root collection or Collection Group.
3. Under 100 items and always loaded together? Embed as array/map.
4. Unbounded growth? Subcollection (never embed unbounded arrays).

### Performance

**Always load `references/performance-ops.md`.** Quick wins:
- Cursor pagination (`startAfter`), never `offset(n)`
- Exempt large or sequential fields from indexing
- `FieldValue.increment()` for counters
- Offline persistence to avoid re-billing on reconnects

### Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| PERMISSION_DENIED | Security rules | Check rules logic, verify auth token |
| FAILED_PRECONDITION | Missing index | Create index via console link in error |
| High latency on writes | Hotspotting | Check Key Visualizer, exempt sequential indexes |
| 429/RESOURCE_EXHAUSTED | Rate limit | Check quotas, implement backoff |
| Document too large | >1 MiB | Move data to subcollection |

## Anti-patterns (never do)

1. **Sequential IDs**: never use timestamps or auto-increment as doc IDs
2. **Unbounded arrays**: move to a subcollection past 50 items
3. **Test mode in production**: never deploy `allow read, write: if true`
4. **Auth-only access**: `if request.auth != null` alone is insufficient
5. **Missing unsubscribe**: always clean up `onSnapshot` listeners

## Testing and deployment

Test rules with the Emulator Suite (`firebase emulators:start --only firestore`) and `@firebase/rules-unit-testing` (`assertSucceeds`, `assertFails`). Deploy with `firebase deploy --only firestore:rules` or `firestore:indexes`. Rules propagate within minutes, with up to a 10-minute inconsistency window from edge caching. Snippets: `references/code-templates.md`.
