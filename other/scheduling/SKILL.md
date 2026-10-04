---
name: scheduling
description: "The cross-repo scheduling system (sch_* tables, matrx-scheduler). Use when touching features/scheduling/**, /schedules or /administration/scheduling, migrations/sch_*.sql, a scheduled agent, cron, trigger, lease, or claim, or debugging ghost tasks, missed fires, double-runs, or stuck claims."
---

# Scheduling

Cross-repo scheduling spine. Three live systems share four Supabase tables
(`sch_task`, `sch_agent_task`, `sch_trigger`, `sch_run`):

- **matrx-frontend** — control plane (this repo). Users create/observe.
- **aidream + matrx-scheduler** — server-side executor.
- **matrx-extend (Chrome extension)** — browser-context executor for
  context-match triggers.

Spec: [`docs/SCHEDULING.md`](../../../docs/SCHEDULING.md). FEATURE doc:
[`features/scheduling/FEATURE.md`](../../../features/scheduling/FEATURE.md).

---

## 30-second mental model

```
sch_task           kind='agent' (today). Spine: title, surfaces[], next_due_at.
  ↳ sch_agent_task   1:1 extension: agent_id, prompt, variables, conversation_id.
sch_trigger        when it fires (one-shot, interval, cron, heartbeat, context-match, …). v1 = one trigger per task.
sch_run            each execution attempt. Lease via claim_token + claim_expires_at.
```

RLS: owner-or-`is_super_admin()` on all four tables. Service_role is
NEVER used for user-initiated writes; admin pages use the regular browser
client and rely on RLS for cross-user reads.

Atomicity: a **partial unique index** `sch_run_unique_active_per_task`
forces at most one active run per task. Concurrent claimers lose the race
to the index, not the application.

DB invariants: `sch_task.next_due_at = MIN(sch_trigger.next_due_at)` is
maintained by trigger `sch_trigger_cascade_next_due_at`. Don't UPDATE
`sch_task.next_due_at` directly — write to `sch_trigger` and let the
cascade flow.

---

## When to use this skill

- Adding or modifying a `sch_*` migration.
- Changing the trigger taxonomy or adding a new trigger type.
- Building / fixing FE pages under `/schedules` or
  `/administration/scheduling`.
- Editing the Python `matrx-scheduler` package or its router on aidream.
- Wiring a new executor surface (e.g. a desktop app scanner).
- Debugging "ghost tasks" (queued runs not getting picked up), missed
  fires, double-runs, stuck claims.

## Where each thing lives

| Layer | Files |
|---|---|
| DB migrations | `migrations/sch_*.sql` |
| FE types | `features/scheduling/types.ts` |
| FE Supabase façade (reads) | `features/scheduling/service/queries.ts` — joined task reads + `taskDetailToAgendaTask` reshape + residual `updateAgentTaskFields` write (the one `sch_agent_task` field-patch HTTP doesn't cover yet). ONLY place that `.from('sch_*')`. |
| FE HTTP client (writes + compute) | `features/scheduling/service/schedulerClient.ts` — typed wrapper over aidream's `/scheduler/*` (16 endpoints): tasks/triggers/runs CRUD, cron validate, preview-fires, compute-next-due-at, scanner status. Primary path for all user-facing writes. |
| FE TS twin of next_due | `lib/scheduler-client/next-due.ts` — used by `CronForm` and cron-tester for live-typing previews; also exported to non-HTTP clients (Chrome extension, edge functions). |
| FE Redux slices | `features/scheduling/redux/{tasks,runs}/` |
| FE hooks | `features/scheduling/hooks/` — useScheduledTasks (+ list realtime), useTaskDetail, useTaskRuns, useRunStream |
| FE list / detail / form | `features/scheduling/components/{list,detail,form}/` |
| User routes | `app/(authenticated)/schedules/` |
| Admin routes | `app/(authenticated)/(admin-auth)/administration/scheduling/` |
| Admin service | `lib/services/scheduling-admin-service.ts` (browser client + `is_platform_admin()` RLS) |
| Python package | `aidream/packages/matrx-scheduler/matrx_scheduler/` |
| Python router | `aidream/aidream/api/routers/scheduling.py` |
| Per-request supabase client | `aidream/aidream/services/scheduling/per_request_client.py` |
| matrx-ai bridge | `aidream/aidream/services/scheduling/agent_runner_adapter.py` |
| Capture emitter | `aidream/aidream/services/scheduling/capture_emitter.py` |

## Non-negotiable rules

1. **NEVER call `.from('sch_*')` outside `features/scheduling/service/queries.ts` or `lib/services/scheduling-admin-service.ts`.** The select shape needs to stay consistent; row→AgendaTask flattening lives in one place. New user-facing writes go through `service/schedulerClient.ts` — don't add parallel Supabase writes to `queries.ts`.
2. **NEVER use the aidream service_role supabase singleton in scheduling routes.** Use `make_user_supabase_client(jwt)` so RLS binds to the caller.
3. **NEVER insert into `sch_run` directly from the FE.** Use the `sch_enqueue_manual_run(p_task_id)` RPC — it stamps `user_id` from the task row, sets `status='queued'`, and refuses to spoof other fields.
4. **NEVER UPDATE `sch_task.next_due_at` from application code.** Write to `sch_trigger.next_due_at`; the DB trigger cascades.
5. **NEVER bypass the RLS gate by tightening `is_super_admin()` to `is_platform_admin()` (or vice-versa).** The two tiers exist deliberately — scheduling uses `is_super_admin()` to match the route layout's `requireSuperAdmin` gate.

## Common tasks

### Add a new trigger type (e.g. `event`)

1. Add to the `TriggerType` discriminated union in
   `features/scheduling/types.ts` and the Python `models.py`.
2. Add the case to `computeNextDueAt` in `lib/scheduler-client/next-due.ts`
   (TS twin used by previews) AND `compute_next_due_at` in the Python
   `next_due` module (authoritative for writes).
3. Add a subform component in
   `features/scheduling/components/form/triggers/` and wire it in
   `ScheduleForm.tsx`.
4. Add validation in `features/scheduling/utils/validation.ts`.
5. Add a Jest + pytest case for the new type.
6. Update the DB CHECK on `sch_trigger.type` if you're adding a brand-new
   value — the existing 8 values already cover everything in the spec.

### Add a new executor surface (e.g. `desktop`)

1. Add the value to:
   - the FE `SURFACE_VALUES` constant
   - the `sch_task_surfaces_chk` CHECK constraint (migration)
   - the `SURFACE_META` map for the picker tooltip
2. In the new surface's code (e.g. Tauri desktop app), call
   `matrx_scheduler.configure(surface="desktop", ...)` and
   `start_scanner()`. Each surface has its own scanner; the partial
   unique index ensures no double-runs across surfaces.

### Debug a "ghost task" (queued run that never executes)

1. Confirm the row's `surface` value — manual fires set it to `NULL`
   so any surface can claim; if it's hardcoded to a value no executor is
   running on, it'll sit forever.
2. Check `sch_task.surfaces` — does it contain `'any'` or a value that
   matches an online scanner?
3. Check the scanner status: GET `/scheduler/status` (admin only), or
   the FE admin page at `/administration/scheduling/scanner-health`.
4. Confirm `AIDREAM_SCHEDULER=1` is set on the host process you expect to
   execute the run.

### Debug a "stuck claimed" run

1. Visit `/administration/scheduling/orphan-leases`.
2. The scanner sweeps any `status IN (claimed,running) AND
   claim_expires_at < now()` to `failed` on every tick — if a row sits
   in claimed for >60s after expiry, something's broken upstream.
3. Manual remediation: use the page's "Mark failed" button (RPC-less,
   direct UPDATE — gated by RLS owner-or-super-admin).

## Verification

After changes, always:

- Python: `uv run pytest packages/matrx-scheduler/tests` (25 tests, must all pass).
- TypeScript: `pnpm exec jest features/scheduling/utils/__tests__/`
  (triggerHumanize + validation).
- Type check: `pnpm tsc --noEmit` clean across the feature.
- Smoke: create a schedule via the form, confirm it lands in all 3
  tables (use Supabase MCP `execute_sql` to inspect).
- For Python execution changes: enable `AIDREAM_SCHEDULER=1`, create an
  interval task on `surfaces=['server']`, watch logs for "scheduler.run
  requested" and the resulting `sch_run` row transition.

## Related skills

- `protected-resources` — scheduling is NOT a protected resource (no
  audit log, no SECURITY DEFINER mutation gate), but if scheduling ever
  grows admin-level operations that warrant audit, follow that pattern.
- `connect-matrx-extend` — relevant when adding `context-match` UX or
  cross-repo run-pickup support.
- `window-panels` — for future "Quick Schedule" overlay (v1.5).
