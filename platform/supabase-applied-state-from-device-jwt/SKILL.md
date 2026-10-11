---
name: supabase-applied-state-from-device-jwt
description: "Use when a Supabase wipe or migration 'ran' but data persists or a feature still fails, the hosted SQL editor said success but nothing changed, or before claiming a server-side change landed. Also when an anon-key count of 0 is offered as proof of a wipe, or a PostgREST probe returns PGRST205, PGRST204, PGRST202 or 42703."
---

# Supabase applied-state, proven from the device's own JWT

The question this answers: **did that migration / wipe / upload actually land, and
if not, why not?**

Three tempting sources of truth are all wrong:

- **The app's UI.** It may render an in-memory cached read, and a killed process is
  not enough if the cache is rebuilt from a stale server.
- **An anon-key count.** Under RLS the `anon` role usually sees zero rows *whether
  or not the wipe ran*. `Content-Range: */0` from anon proves nothing.
- **"I ran it."** Owners run the wrong file, a stale copy from an editor tab, or a
  script that errored and rolled back while still looking successful.

The device already holds a token for the real, authenticated role. Use it.

## Why a run that "succeeded" changed nothing

A script like this reports success in the Supabase SQL editor and deletes nothing:

```sql
begin;
truncate table a, b, c restart identity cascade;
commit;

begin;
delete from auth.users;   -- elevated privilege, other auth.* tables reference it; can fail
commit;
```

The hosted editor wraps **the entire submission** in its own transaction, so your
inner `begin;`/`commit;` are nested no-ops. When the last statement errors, the
editor rolls back **everything**, including the truncate that "already committed",
and the owner sees a run that looked fine. Splitting into two `begin/commit` blocks
does **not** fix this; only two **separate executions** (separate paste + run) do.

**Rule:** a destructive script is one statement, or one run per
independently-committable step. Never rely on inner transaction blocks in a hosted
editor, and end every operational script with a verification `SELECT` the owner
must read.

DDL from the *same session* (e.g. a `create table`) may have taken effect while DML
did not; that is not contradictory if the DDL was in a different run.

## 1. Get the credentials

```bash
URL=$(grep -m1 "^supabase.url" local.properties | cut -d= -f2- | tr -d ' \r')
KEY=$(grep -m1 "^supabase.key" local.properties | cut -d= -f2- | tr -d ' \r')
```

## 2. Pull the session JWT out of the app

supabase-kt stores it in the default SharedPreferences under a key shaped like
`sb-<project-ref>-supabase-co-session`, XML-escaped JSON. Requires a debuggable
build (`run-as` fails otherwise).

```bash
ADB="$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe"; export ANDROID_SERIAL=<serial>
"$ADB" shell run-as <pkg> cat shared_prefs/<pkg>_preferences.xml > .tmp/prefs.xml
```

```python
import re, html, json, base64, time
s = open('.tmp/prefs.xml', encoding='utf-8').read()
raw = html.unescape(re.search(r'name="sb-[^"]*-session">(.*?)</string>', s, re.S).group(1))
tok = json.loads(raw)["access_token"]
open('.tmp/tok.txt', 'w').write(tok)          # then in bash: TOK=$(cat .tmp/tok.txt)
p = tok.split('.')[1]; p += '=' * (-len(p) % 4)
c = json.loads(base64.urlsafe_b64decode(p))
print("sub", c["sub"], "email", c.get("email"), "exp", time.ctime(c["exp"]), "now", time.ctime())
```

**Check `exp` first.** An expired token yields misleading 401s that read like a
permissions problem.

## 3. Count rows as that user

`Prefer: count=exact` with `Range: 0-0` returns the count in a header without
downloading rows.

```bash
for t in profiles sessions session_sets; do
  printf "%-16s " "$t"
  curl -s -I "$URL/rest/v1/$t?select=*" \
    -H "apikey: $KEY" -H "Authorization: Bearer $TOK" \
    -H "Prefer: count=exact" -H "Range: 0-0" | grep -i content-range
done
```

`Content-Range: 0-4/5` = five rows exist. That settles a wipe argument outright, and
only a count does: **a deleted `auth.users` row does not invalidate its JWT.**
Supabase access tokens are stateless and signed; a token for a deleted user keeps
working until `exp`, so "I can still read data" is NOT evidence the account
survived.

## 4. Map each probe to the missing migration

Probe one distinctive object per migration (a table, a column, a view, an RPC) and
read the code. Selecting a column that only a newer migration adds is the cheapest
possible migration-applied probe.

| probe result | meaning |
|---|---|
| `200` (e.g. on `?select=<pk>&limit=1`) | the object exists, even if the table is empty |
| HTTP 404 / `PGRST205` | table missing |
| `PGRST204`, or `400` on `?select=<col>` | column missing |
| `42703` (`column X.Y does not exist`) | column missing; names the exact unapplied migration |
| `42P01` | table missing, when the statement reached Postgres |
| `PGRST202` (404 on `/rest/v1/rpc/<fn>`) | function missing, or the argument names you sent do not match its signature (see `supabase-function-revoke-anon-trap`) |

## Client-side consequences worth checking

- If the client maps only the table/column codes to "migration not applied" and
  lets a missing **function** fall through to a generic "try again", an unapplied
  migration makes the user retry forever. Add `PGRST202` to that branch.
- An RPC whose name lives in a `const` will not be found by a naive grep for the
  literal function name. Grep for the constant before concluding a client "never
  adopted" a server function.
- **Defaulted DTO fields hide a missing migration.** A kotlinx `@SerialName` field
  with a default decodes fine against an un-migrated view — correct for resilience,
  but it means the client cannot tell you the migration is missing. Probe the column
  over REST instead.

## Clean up

The extracted JWT is a live credential and the responses may contain the owner's
data. Delete the scratch files as soon as the checks are done:

```bash
rm -f .tmp/tok.txt .tmp/prefs.xml .tmp/*.json
```

## Boundary

Standing up a backend, applying migrations, and pooler/IPv6 discovery belong to
`supabase-backend-from-windows`. Writing a wipe script, and the push watermark that
stops a client re-uploading after a server wipe, belong to
`client-watermark-server-wipe`. This skill proves what is actually on the server and
why a run did not land.
