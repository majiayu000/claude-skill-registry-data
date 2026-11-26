---
name: supabase-edge-scaffold
description: Scaffold of a Supabase Edge Function with correct CORS + service-role + error handling, instead of copying boilerplate by hand
---

> **Auto-Trigger:** When creating a new Supabase Edge Function / Supabase serverless endpoint
> **Keywords:** "edge function", "supabase function", "new edge", "/edge-new", "deno deploy supabase", "supabase serverless function"
> **Priority:** MEDIUM
> **Tools:** Write, Read, MCP Supabase by capability - `deploy_edge_function`, `list_edge_functions` (the tool prefix varies per installation, e.g. `mcp__claude_ai_Supabase__deploy_edge_function` or `mcp__supabase__deploy_edge_function` - never hardcode the full prefix)

# supabase-edge-scaffold - an edge function born right

Every new edge function repeats the same boilerplate (CORS, OPTIONS preflight, service-role via env, JSON error). This skill generates the correct skeleton.

## Contract

**INPUT:** kebab-case name of the function + (optional) specific logic to insert in the body.

**OUTPUT:** `supabase/functions/<name>/index.ts` with CORS + OPTIONS preflight + service-role via env + JSON error.

**EXIT CODES** (`deno check` smoke test over the generated file):

| Exit | Meaning |
|---|---|
| 0 | TypeScript type-checks clean (1st time downloads deps from jsr.io/npm; subsequent runs = local cache, offline) |
| ≠0 | syntax/type error in the generated skeleton - do not commit like this |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `supabase/functions/<name>/index.ts` | Writes | the skeleton |
| `Deno.env` (at runtime, not here) | - | service-role NEVER hardcoded/committed |

## Process
1. **Name + purpose** of the function (kebab-case).
2. **Generate `supabase/functions/<name>/index.ts`** with this skeleton:
   ```ts
   import { createClient } from "jsr:@supabase/supabase-js@2";

   const CORS = {
     "Access-Control-Allow-Origin": "*",
     "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
     "Access-Control-Allow-Methods": "POST, OPTIONS",
   };

   Deno.serve(async (req) => {
     if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
     try {
       // service-role: NEVER hardcode - comes from the function's environment
       const supabase = createClient(
         Deno.env.get("SUPABASE_URL")!,
         Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
       );
       const body = req.method === "POST" ? await req.json().catch(() => ({})) : {};
       // ... logic ...
       return new Response(JSON.stringify({ ok: true }), {
         headers: { ...CORS, "Content-Type": "application/json" },
       });
     } catch (e) {
       return new Response(JSON.stringify({ ok: false, error: String(e) }), {
         status: 500, headers: { ...CORS, "Content-Type": "application/json" },
       });
     }
   });
   ```
3. **Guardrails:** service-role only via `Deno.env` (never in code/commit - `no-secrets`); error always JSON+CORS (does not leak the stack); validate input before touching the DB.
4. **Deploy** when ready: `deploy_edge_function` (MCP) or `supabase functions deploy <name>`. **Deploy = human gate** (no auto-deploy without an ok).

## When NOT to Activate
- Project without Supabase.
- Editing an existing function (use Edit directly).

## Executed examples

```console
$ deno check supabase/functions/example/index.ts
Download https://jsr.io/@supabase/supabase-js/meta.json
[... resolves deps the 1st time ...]
Check supabase/functions/example/index.ts
```
<!-- executed: 2026-10-30 · exit=0 -->
(the EXACT skeleton of this skill type-checks clean - it is not pseudocode.)

```console
$ time deno check supabase/functions/example/index.ts
real 0m0.018s
```
<!-- executed: 2026-10-30 · exit=0 -->
(2nd call = local cache, 0.018s - from here on `deno check` is offline and works as a quick Proof.)

```console
$ grep -c "Access-Control-Allow-Origin\|OPTIONS\|Deno.env.get\|catch (e)" supabase/functions/example/index.ts
6
```
<!-- executed: 2026-10-30 · exit=0 -->
(6 matching lines confirm the 4 guardrails of step 3 are present in the generated file: CORS, preflight, env - never hardcoded, and error handling; `OPTIONS` and `Deno.env.get` each match 2 lines.)

```console
$ deno check broken.ts
Check broken.ts
TS2345 [ERROR]: Argument of type 'string | undefined' is not assignable to parameter of type 'string'.
  Type 'undefined' is not assignable to type 'string'.
      Deno.env.get("SUPABASE_URL"),
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    at file:///private/tmp/example/broken.ts:14:7

error: Type checking failed.
```
<!-- executed: 2026-10-30 · exit=1 -->
(real reproduction: removing the `!` non-null assertion from the original skeleton's `Deno.env.get(...)!` BREAKS the type-check - that is exactly why step 2 requires the `!`.)

## Proof

```bash
deno --version
```
(quick, offline precondition: without `deno` on the PATH, the smoke-test step's `deno check` does not run. After generating a real scaffold, replace it with `deno check supabase/functions/<name>/index.ts`.)

## See also
`rls-audit` (data security), `secret_scan_on_write` (do not commit the service-role).
