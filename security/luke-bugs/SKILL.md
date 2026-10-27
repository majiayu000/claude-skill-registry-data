---
name: luke-bugs
description: >
  Runtime correctness scan for the Luke codebase. Finds race conditions, async
  bugs, N+1 queries, memory leaks, null crashes, error propagation failures,
  stale closures, React logic bugs and check-then-act races across a permission
  boundary. Escalates security-impacting defects to /luke-security rather than
  running its own exploit hunt.
  Use when asked to find bugs, do a bug assessment, or check for runtime issues.
  Scoping: default = diff vs merge-base. /luke-bugs apps/api | --since <ref> | --full
argument-hint: '[--full|--since <ref>|<path> [--since <ref>]]'
context: fork
agent: Explore
background: false
disallowed-tools: Edit, Write, NotebookEdit
---

# Luke Deep Bug Scan

Read-only. Do NOT modify any file.
Find real runtime and logic bugs — not style issues, not architectural drift
(that's /luke-audit's job). Every finding must be a plausible runtime failure,
data corruption, or security issue with a realistic failure scenario.

**Read `.claude/skills/luke-shared/audit-protocol.md` first** and apply it in
full: diff scoping (§1), baseline suppression (§2), the mandatory "Promotion
to rule" section (§3), `lessons.md` as a check input (§4), and the
constraint/heuristic classification (§8).

Most of the patterns below are **investigation triggers**, not constraints: they
say where to read, not what is broken. A finding still requires the failure
scenario. Ownership boundaries: `.claude/skills/luke-shared/governance-map.md`.

Then read:

- `packages/db/prisma/*.prisma` — understand models and relations (multi-file schema, split by domain; `schema.prisma` itself holds only `generator`/`datasource`)
- `packages/core/src/auth/permissions.ts` — permission model
- `apps/api/src/lib/` — middleware: requirePermission, auditLog, context
- `lessons.md` — regressions already paid for: the part routed to this skill, per protocol §4

**Invocation arguments:** $ARGUMENTS

Resolve the invocation arguments above per `audit-protocol.md` §1 **before**
running any git scope derivation. The whole bound value is the scope selector
here — this skill takes no mode. If it is empty, use the protocol default —
diff vs merge-base, not the whole monorepo. If it carries an explicit selector,
that selector wins and the default is never derived.

## A reproducible bug becomes a test

For every CRITICAL or HIGH finding, include in the fix the test that would
cover it (description, target file, key assertion). A bug fixed without a
test is a bug that can come back: it's the same control hierarchy from §3 of
the protocol, applied to behavior instead of syntax. If the project already
has a suitable suite, name the file; otherwise say where it should be created.

---

## Check Areas

Three areas, one single pass. See the fan-out note in `../luke-shared/audit-protocol.md` §6.

### 1 — Race Conditions, Async & Database

**Race conditions & atomicity:**

- Check-then-act where nothing keeps the checked condition true until the write commits (`findUnique/findFirst` followed by `create/update/upsert`): the criteria — constraint, conditional write, lock; a `$transaction` alone may not hold — are `CLAUDE.md` Development Patterns rule 3
- `pauseNavScheduler()` / `resumeNavScheduler()` not called symmetrically — if exception thrown between pause and resume, scheduler stays paused forever
- RBAC cache: a write to RBAC AppConfig keys that bypasses `saveConfig`/`saveConfigs`/`deleteConfig`
  without `invalidateRbacCache()` after its transaction commits
- `prisma.$transaction([...])` array syntax where operations depend on each other (should use callback syntax)

**Async/await bugs:**

- `someAsync()` called without `await` and without `.catch()` — silent fire-and-forget <!-- skill-check-ignore -->
- `Promise.all([...])` where one failure is not rethrown or logged
- `Promise.allSettled` results iterated without checking `status === 'rejected'`
- `array.forEach(async item => { await ... })` — forEach doesn't await async callbacks. Should be `await Promise.all(array.map(...))` or `for...of`. Effectively a **constraint** and syntactic: propose it for promotion (§3) rather than reporting occurrences forever
- tRPC procedures calling NAV/SMTP/LDAP without try/catch — unhandled exception → 500 with no useful message
- `setTimeout`/`setInterval` results not stored and not cleared on cleanup

**Prisma & database:**

- N+1 queries: loops containing `prisma.*.findUnique/findFirst` — should use `findMany` with `where: { id: { in: ids } }` or `include`. **Investigation trigger**: the finding is the query count against a realistic row count, not the shape
- `findMany` without `select` on tables with sensitive fields (passwords, encrypted values). **Heuristic**: a defect only when the extra fields can cross a trust boundary or reach a log — otherwise it is a `select` worth tightening, not a bug
- Hard deletes `prisma.*.delete(` outside migration scripts (should be soft delete `isActive: false`)
- `findMany` without `take`/`skip`/cursor on tables that grow unboundedly (audit logs, sync history, collection rows)
- `findUnique` result used without null check before accessing properties

**Catch blocks:**

- Empty or silent catch: `} catch (err) { }` or `} catch { return null }` without at minimum `logger.error()` or `debugError()`
- Error logged but not rethrown when caller needs to know it failed
- `new TRPCError({ code: 'INTERNAL_SERVER_ERROR' })` without `cause:` — root cause disappears from logs

---

### 2 — Memory Leaks, Null Crashes & Error Propagation

**Memory leaks & resource cleanup:**

- `useEffect` in `apps/web/src/` with subscriptions, event listeners, intervals, or WebSocket connections opened without a cleanup return function
- `window.addEventListener` / `document.addEventListener` without corresponding `removeEventListener` in cleanup
- mssql `ConnectionPool` opened in test/preview functions without try/finally that closes the pool in all code paths
- Module-level variables that accumulate data without bounds (in-memory caches without TTL or max size)
- Prisma client instantiated at module level in Next.js pages (should be singleton via `globalThis`)

**Null/undefined crashes:**

- `value!.property` non-null assertion without preceding null check
- `array[0]` or `array[index]` without bounds check — especially in tRPC result processing
- `JSON.parse(someString)` outside try/catch — malformed input crashes process. Especially dangerous in AppConfig value parsing and LDAP roleMapping
- Optional chaining `a?.b?.c` where null result is passed to a function expecting a value — silent wrong behavior

**Error propagation:**

- Sync operation failures (NAV sync errors) caught in orchestrator but not stored anywhere queryable — user has no way to know sync failed
- `logAudit()` failures: if audit log write throws, does it crash the mutation or silently continue? Should never block primary operation but must log to fallback
- tRPC error handlers that catch specific error but throw generic one — original error disappears

---

### 3 — React, Frontend Logic & Permission-Boundary Races

**React logic bugs (apps/web/src only):**

- Stale closures: `useEffect`, `useCallback`, `useMemo` with dependency arrays missing variables referenced inside the callback
- Direct state mutation: `items.push(newItem)` or `state.property = value` — React won't re-render
- tRPC query hooks used without handling `isLoading`, `isError` states — UI crashes on error with no feedback
- `useMutation` with `onMutate` optimistic update missing `onError` rollback — failed mutation leaves UI in incorrect state permanently
- Lists rendered with index as key when items can be reordered/filtered — causes React to reuse wrong component instances
- Mutations that modify data without calling `utils.entity.invalidate()` — sibling components show stale data

**Check-then-act across a permission boundary:**

- `requirePermission` check + sensitive DB write in the same procedure, with
  nothing keeping the check true until the write commits (rule 3's criterion,
  not "is it in a transaction") — the permission can be revoked between the check
  and the write. Report it when a stale check has an effect beyond that moment; a
  point-in-time eligibility check stated as such in the code (e.g.
  `merchandisingPlan.assignUser`) is not a finding. Same TOCTOU shape as the race
  conditions in area 1, and it stays here: the defect is the condition not held,
  not an attacker primitive.

**No systematic security hunt here.** IDOR, leaked internals in error
responses, missing auth rate limiting and secrets reaching client code used to
be enumerated in this section and are all systematic checks in
`/luke-security`. Two skills maintaining the same hunt drift into two
definitions of the same vulnerability, so the duplicate list is gone — not the
coverage.

A runtime bug that hands an attacker a primitive is still reported here, with
an explicit handoff:

```
Security escalation: YES
Reason: <why this runtime defect creates an attacker primitive>
Suggested follow-up: /luke-security <same scope>
```

Report the bug on its own merits — scenario, impact, fix — and let
`/luke-security` decide exploitability. Do not withhold a finding because it
looks security-adjacent, and do not grow an attack-scenario checklist here to
compensate.

---

## Report Format

```
## Luke Bug Scan Report
Scanned: <path or 'full monorepo'>
Date: <today>

### Summary
| Category                        | CRITICAL | HIGH | MEDIUM |
|---------------------------------|----------|------|--------|
| Race Conditions, Async & DB     |    N     |  N   |   N    |
| Memory, Null & Error Propagation|    N     |  N   |   N    |
| React, Frontend & Boundary Races|    N     |  N   |   N    |

### Severity Guide
- CRITICAL: data corruption, auth bypass, potential data loss
- HIGH: runtime crash in production, silent failure corrupting state
- MEDIUM: degraded behavior, missing error feedback, perf issue at scale

### Findings

#### [CATEGORY]

**[SEVERITY]** — <title>
File: `path/to/file.ts:line`
Scenario: <exact sequence of events that causes the bug>
Impact: <what goes wrong>
Fix:
\`\`\`typescript
// proposed fix
\`\`\`
Regression test: <target file + key assertion>

### Promotion to rule
<mandatory section — see §3 of the shared protocol>
```

### Rules

- Report ONLY plausible bugs with a realistic failure scenario
- If you can't describe the exact scenario, don't report it
- No style issues, no architectural drift — that's /luke-audit
- Max 25 findings — cut MEDIUM first if over limit
- If category is clean: `✅ No findings`
