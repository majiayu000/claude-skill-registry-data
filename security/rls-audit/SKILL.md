---
name: rls-audit
description: Really audits the RLS of a Supabase project — pg_policies per permissive anon policy + get_advisors, not just the relrowsecurity flag
---

> **Auto-Trigger:** Before declaring a Supabase schema "secure", when touching policies/RLS, or in a data-security audit
> **Keywords:** "rls", "secure supabase", "row level security", "anon leak", "pg_policies", "data leak", "advisors", "policy"
> **Priority:** HIGH
> **Tools:** Supabase MCP by capability — `execute_sql`, `get_advisors`, `list_tables` (the tool prefix varies by installation: it may be `mcp__supabase__*`, `mcp__claude_ai_Supabase__*`, etc. — NEVER hardcode the full prefix)

# rls-audit — real RLS (not the flag)

**Lesson:** `pg_class.relrowsecurity = true` does **NOT guarantee secure** — the real leak lives in **permissive `anon` policies** (`qual = true`). Auditing the flag only gives false comfort. This skill audits where the leak lives.

## Contract

**INPUT:** none (connects to the Supabase project already linked to the MCP).

**OUTPUT:** verdict per table — `(RLS on/off · anon policies · qual · sensitive?) → bug / by-design / to-fix`. Never "secure" by the flag alone.

**EXIT CODES** (from the MCP call):

| Exit | Meaning |
|---|---|
| 0 | query ran — the result (even "0 leaks") is trustworthy |
| `Unauthorized` error | Supabase MCP token missing/expired — do **NOT** declare "secure" or "0 leaks"; declare "not verified" |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `pg_policies` (via `execute_sql`) | Reads (read-only) | permissive anon/public policies |
| `get_advisors(type="security")` | Reads (read-only) | RLS-disabled, SECURITY DEFINER views |

## Process
1. **Advisors first:** `get_advisors(type="security")` — catches RLS-disabled, open policies, SECURITY DEFINER views, etc.
2. **Permissive anon policies (the blind spot):**
   ```sql
   select schemaname, tablename, policyname, roles, cmd, qual
   from pg_policies
   where 'anon' = any(roles) or roles = '{public}'
   order by tablename;
   ```
   Leak signal: `qual = true` (or null) in a `SELECT` policy for `anon`/`public` → **anyone reads the whole table**. Cross-check against sensitive data.
3. **Tables without RLS:** `select relname from pg_class where relkind='r' and not relrowsecurity and relnamespace='public'::regnamespace;` — RLS off = open door.
4. **Broad GRANTs:** look for `GRANT ALL ... TO anon/public` and permissive `ALTER DEFAULT PRIVILEGES`.
5. **Honest verdict:** list each table with (RLS on/off · anon policies · qual · sensitive?) → bug / by-design (e.g. an intentionally public `shared_state`) / to-fix. **Do not declare "secure" just because the flag is on.**

## When NOT to Activate
- Project without Supabase / without a connected Supabase MCP.
- Change that does not touch data/policies.

## Executed examples

```console
$ mcp__supabase__get_advisors(type="security")
{"error":{"name":"Error","message":"Unauthorized. Please provide a valid access token to the MCP server via the --access-token flag or SUPABASE_ACCESS_TOKEN."}}
```
<!-- executed: 2026-10-30 · exit=1 -->
(MCP token missing or invalid in this session — step 5 applies: do NOT declare "secure", declare "not verified, token missing".)

```console
$ mcp__supabase__list_tables(schemas=["public"], verbose=false)
{"error":{"name":"Error","message":"Unauthorized. Please provide a valid access token to the MCP server via the --access-token flag or SUPABASE_ACCESS_TOKEN."}}
```
<!-- executed: 2026-10-30 · exit=1 -->
(a 2nd identical error confirms it is the token — not a one-off failure of the 1st call.)

```console
$ python -c "
policies = [
    {'tablename': 'shared_state', 'roles': ['anon'], 'cmd': 'SELECT', 'qual': 'true'},
    {'tablename': 'billing_customers', 'roles': ['anon'], 'cmd': 'SELECT', 'qual': 'true'},
    {'tablename': 'audit_log', 'roles': ['authenticated'], 'cmd': 'SELECT', 'qual': 'user_id = auth.uid()'},
]
leaks = [p for p in policies if 'anon' in p['roles'] and p['cmd'] == 'SELECT' and p['qual'] in (None, 'true')]
for p in leaks:
    print('LEAK:', p['tablename'], '- qual=', p['qual'])
print(len(leaks), '/', len(policies), 'tabelas com leak anon-permissivo')
"
LEAK: shared_state - qual= true
LEAK: billing_customers - qual= true
2 / 3 tabelas com leak anon-permissivo
```
<!-- executed: 2026-10-30 · exit=0 -->
(the detection LOGIC of step 2 (qual=true in an anon SELECT policy = leak) validated locally — independent of the MCP being authenticated; `shared_state` may be by design, `billing_customers` is not.)

## Proof

```bash
python -c "policies=[{'roles':['anon'],'cmd':'SELECT','qual':'true'}]; assert any('anon' in p['roles'] and p['qual']=='true' for p in policies)"
```

## See also
`drift_check.py` (intent×reality).
