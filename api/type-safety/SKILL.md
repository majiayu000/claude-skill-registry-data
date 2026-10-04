---
name: type-safety
description: "Doctrine for fixing TypeScript errors against generated types (database.types.ts, api-types.ts). Use when fixing tsc or type-check failures or a type-errors batch, writing supabase .rpc()/.from() calls or DB shape guards, errors mention Json/unknown/Database, or you are tempted to cast or suppress."
---

# Type Safety

## Source of Truth

Generated types are **always correct**. Code, local types, and stored data conform to them — never the reverse.

| Boundary | Generated source | Regen |
|---|---|---|
| Database (Supabase) | `types/database.types.ts` | `pnpm db-types` |
| Python API (aidream Pydantic → OpenAPI) | `@ai-matrx/agents/generated/api-types` — alias via `components["schemas"]["..."]` | `pnpm sync-types` (live) · local-ahead case below |

Never hand-mirror, re-declare, or widen a generated type. A hand-written "compatible" copy is a violation even if it currently matches — it drifts silently and shields call sites from schema changes. Full standards: [`TYPESCRIPT_STANDARDS.md`](../../../TYPESCRIPT_STANDARDS.md). Duplicate-type doctrine: [`PRINCIPLES.md`](../../../PRINCIPLES.md) §1.

### Live OpenAPI behind local aidream

`pnpm sync-types` (no flag) hits the **live** server. A route that exists in local `../aidream` but is not deployed yet is **absent** from `keyof paths` / `PathWith<"get">`. That is not an escalation and not a license to copy `openapi.json` or `api-types.ts` by hand.

**Do this — then stop:**

1. **Start** the AI Dream server from `../aidream`: `python run.py`. Wait until it prints `Local Link: http://localhost:8000`. If 8000 is already serving this checkout's aidream, reuse it — do not start a second.
2. From this repo: **`pnpm sync-types:local`**.
3. Stay until Step 3 prints **Type-check passed**. Remaining errors are real code/contract bugs — fix them per this skill and re-run until green.
4. **Kill** the server you started. Do not leave it running. Do not kill a server you did not start.

**Supabase query/RPC patterns** (`DbRpcRow` guard, the one sanctioned cast, Json field narrowing, `Tables<T>`): [`supabase-patterns.md`](./supabase-patterns.md) in this skill.

---

## Reality Check — What a Real Fix Actually Involves

A type error at a data boundary is a **signal that the code produces or accepts wrong data shapes**. The error is the diagnostic, not the problem. A real fix changes the code and the data — not the type annotations. Expect a real fix to involve most or all of:

1. **Actual code modifications** — nearly always. If your diff only touches type declarations, casts, or annotations, it is not a fix.
2. **Runtime validation at ingress** — data fetched from the DB or imported from external sources is validated against the generated schema, with explicit errors or warnings when it doesn't conform. `Json` → typed happens through **validation, never assertion**.
3. **A backfill** — if old rows in the DB carry the wrong shape, they get repaired, not papered over at read time.
4. **A codebase-wide audit** — every path that reads, writes, or constructs this data is found and corrected. Fixing one call site while others still produce bad data is not a fix.
5. **Cascading fixes** — expect the first correction to surface additional errors downstream. That is the fix working. Resolve them all so this is fixed ONCE and fixed correctly.

**Silencing the type error is the exact opposite of fixing it.** A cast tells the compiler to stop checking; the malformed data still reaches the DB or Python at runtime, now with zero warning. Data typed with a duplicate wrong type is more dangerous than data not typed at all.

## Trace to the terminal consumer

Before deciding what shape is "correct", find where the data **ends up** — the Python endpoint that parses it, the DB column that stores it, the component that renders it. Read that code (aidream Pydantic model, table schema, wire handler). The shape question is answered at the destination, not at the error site. If the current format cannot work 100% of the time at the destination, the format is the bug — not the annotation.

## The Required Sequence — errors go UP before they go down

1. **Expose everything to the truth.** Delete hand-written duplicate types and alias directly from the generated source (`components["schemas"]["..."]` / `Database["schema"]["Tables"][...]`). Errors erupt across the feature — that is the goal: every error is a location where code disagrees with the real contract.
2. **Fix the code, not the errors.** Correct construction sites, add ingress validation, repair converters, backfill bad rows.
3. **Errors resolve themselves.** When the code genuinely conforms, the errors disappear — zero casts, zero suppressions, zero shadow types remaining.

**Definition of done:** the feature compiles against the generated types with no assertions or suppressions in the data path, invalid DB data is caught and surfaced at read time, and no code path can construct a non-conforming value.

Worked example (CustomTool / OpenAPI alias): [`docs/type-drift-openapi-alias-example.md`](../../../docs/type-drift-openapi-alias-example.md).

---

## Forbidden "fixes"

If your solution contains any of these at a data boundary, you have hidden the bug, not fixed it (`TYPESCRIPT_STANDARDS.md` §3; growth gated by `pnpm check:hatches`):

- `as SomeType` / `as unknown as SomeType` / `as NonNullable<...>` / `as any` / `value!`
- `@ts-ignore` / `@ts-expect-error` / `@ts-nocheck`
- Widening a generated type (literal union → `string`), `Record<string, any>`, making a field optional/`any` to quiet the error
- Re-declaring a hand-written "compatible" version of a generated schema
- `?? {}` / `|| []` to paper over bad data — throw at the boundary instead

**The ONE sanctioned cast:** `as unknown as T` on a Supabase RPC row **only** when a compile-time `DbRpcRow` shape guard validates `T` against the generated row — see [`supabase-patterns.md`](./supabase-patterns.md). The guard proves the structural shape; it cannot check Json field interiors — those stay `JsonObject`/`unknown` and are narrowed by runtime guards or a Zod parse, never given concrete types via the cast.

**The "cast it harder" anti-fix:** when a strictness flag surfaces an error on a line that already has a loose `as X`, the wrong move is escalating to `as unknown as X`. The right move is almost always **deleting the cast** — it was masking a signature the type system satisfies honestly.

---

## Escalation is success, silencing is failure

A path missing from live `keyof paths` that **exists on local aidream** is the **Live OpenAPI behind local aidream** procedure above — not this brief.

Some errors cannot be fixed without a human decision: an architecture choice, a DB migration/backfill, a contract question only the Python **source** can answer, a product-behavior call. **Stopping and reporting these is the correct outcome** — it is worth more than any diff. Making the error disappear and claiming victory is the single worst thing you can do.

Escalate with a **decision brief**, not a shrug:

```
### ESCALATION: <file>:<line> — <error code>
**Data:** what value/shape is in question
**Produced by:** every construction/write site found (paths)
**Consumed by:** the terminal destination(s) — Python model / DB column / renderer (paths, incl. aidream)
**Conflict:** what the generated contract says vs what the code/data actually does
**Decision needed:** the specific question a human must answer (A vs B, with implications)
```

An escalation without "Consumed by" is incomplete — trace the destination first.

---

## Fix patterns (canonical)

- **Duplicate local type** → delete it; import/alias the generated type.
- **Property doesn't exist after schema change** → the DB renamed it; update the code (and audit every other reader/writer).
- **Signature disagrees with DB return** → align the signature; under `strictFunctionTypes`, prefer **widening the implementation's parameter** to the expected signature over narrowing the expected type.
- **`Json`/`unknown` field** → narrow the FIELD, never the row: `isJsonObject` & friends from `@/types/json` for open JSON; Zod parse at ingress for a known concrete shape (`TYPESCRIPT_STANDARDS.md` §4).
- **`X | null` vs `X | undefined`** (Supabase) → `p_arg: v || undefined` for optional RPC args (omits the arg); `?? undefined` per field or widen the domain type to `| null` for row→domain mappers. Never blanket-cast.
- **`possibly null/undefined` on query results** → guard first (`if (error) throw error; if (!data) return …`) so `data` narrows. This is the real-bug class strictNullChecks exists to catch — handle it, don't `!`.

---

## Operating modes

**Deep Fix (default).** You own the whole fix: the Required Sequence above, cross-feature audit, ingress validation, backfill. Live types missing a route that local aidream already serves → local-sync procedure, not an escalation. Escalate (decision brief) for: a DB migration/backfill needing approval, an architecture or product-behavior decision, a wire-contract question needing the Python **source** changed, or protected resources (`protected-resources` skill).

**Batch / wave mode** — assigned per-file task lists (strictness waves, post-release Stage 8 type-error armies, `type-errors/` fan-outs; see [`docs/upgrades/STRICTNESS-WAVE-HANDOFF.md`](../../../docs/upgrades/STRICTNESS-WAVE-HANDOFF.md)):
- Edit only the assigned file or named sibling cluster; work blind from the error list.
- **Never run `tsc` / `pnpm build` / full type-checks** — parallel agents stall everyone; the orchestrator verifies centrally.
- At most **six** agents at a time (provider rate limit).
- No forbidden hatches, ever — a batch fix that cheats is worse than no fix.
- An error needing cross-file/logic/data changes → **leave it in place and file a decision brief**; the brief feeds a Deep Fix, it is not a license to cast.
- **Commit locally as you finish each assigned file.** Exclusive paths only. An uncommitted type fix does not exist — it will not be in the next build. Report the commit SHA. Escalations with no code change do not invent a commit.

## Verification

- Solo sessions: `pnpm type-check` (raw `tsc`, ~60–70s) — but read the active-wave banner in `STRICTNESS-WAVE-HANDOFF.md` first; during an active wave it is red by design.
- `pnpm check:hatches` — the escape-hatch ratchet must not grow; `pnpm check:hatches <path>` lists offenders under a path.
- After DB/API changes: `pnpm sync-types` when the route is **already live**. Local aidream is ahead of live → the local-sync procedure above (`python run.py` → `pnpm sync-types:local` → green → kill). Per the `finalize-and-ship` skill.

## Reporting

```
### filename.ts
**Fixed:** [error] → [what changed and why]
**Commit:** [sha] (required on every fix; omit only when there is no code change)
**Escalated:** [error] → decision brief (format above)
```

## Key files

| File | Role |
|------|------|
| `types/database.types.ts` | Supabase-generated types — source of truth |
| `@ai-matrx/agents/generated/api-types` | OpenAPI-generated Python API types — source of truth |
| `types/supabase-rpc.ts` | `DbRpcRow<F>`, `JsonToUnknown<T>` |
| `types/json.ts` | `JsonObject`/`JsonValue` + `isJsonObject` guards |
| `TYPESCRIPT_STANDARDS.md` | The constitution — banned constructs, validation points |
| `scripts/check-type-hatches.ts` | Escape-hatch ratchet (`pnpm check:hatches`) |
