---
name: supabase-backend-from-windows
description: "Use when adding a Supabase cloud backend to a mobile/desktop app from a Windows box with no supabase CLI or psql, applying Supabase SQL migrations, or when psql fails with could not translate host name for db.<ref>.supabase.co. Also for pooler errors like tenant/user not found, proving RLS blocks the anon key, wiring supabase-kt into Android, or Google sign-in failing with an invalid nonce."
---

# Supabase backend from a Windows box

Covers going from "here is my project URL and key" to a verified, RLS-protected
schema plus an Android client — without installing the Supabase CLI or psql.

## 1. Connecting when there is no psql

New Supabase projects resolve `db.<ref>.supabase.co` **AAAA-only**. Docker
Desktop on Windows usually has no IPv6 route, so:

```
psql: could not translate host name "db.<ref>.supabase.co" to address
```

Confirm before theorising:

```bash
nslookup -type=AAAA db.<ref>.supabase.co   # has an address
nslookup -type=A    db.<ref>.supabase.co   # none -> IPv6-only
```

Use the IPv4 **session pooler** instead. Host is region-specific and the region
is guessable from the IPv6 prefix (`2406:da1c…` = ap-southeast-2), but verify by
resolution, and note the generation prefix matters — `aws-1-…` may exist in DNS
yet reject the tenant (`FATAL: (ENOTFOUND) tenant/user … not found`) while
`aws-0-…` works. Try both:

```bash
for h in aws-0-<region>.pooler.supabase.com aws-1-<region>.pooler.supabase.com; do
  docker run --rm -i -e PGPASSWORD="$PGPW" postgres:17-alpine \
    psql "postgresql://postgres.<ref>@$h:5432/postgres?sslmode=require" \
    -tAc "select current_user;"
done
```

Username is `postgres.<project-ref>`, NOT `postgres`.

## 2. Applying migrations

Keep SQL in the repo (`supabase/migrations/NNNN_name.sql`); pass the password
only via env, never in a committed string or a command line that gets logged.

```bash
docker run --rm -i -e PGPASSWORD="$PGPW" -v "<abs-repo>/supabase/migrations:/mig:ro" \
  postgres:17-alpine psql "postgresql://postgres.<ref>@<pooler>:5432/postgres?sslmode=require" \
  -v ON_ERROR_STOP=1 -f /mig/0001_init.sql
```

`ON_ERROR_STOP=1` matters — without it psql happily applies half a schema.

Tell the user to rotate the DB password afterwards if it crossed a chat or any
shared channel.

## 3. Verifying RLS for real

Create every view over a protected table `with (security_invoker = true)`. Proving
the view actually hides rows (the `reloptions` check, and why it is not enough) is
`postgres-view-privacy-mutation-proof`.

**An empty table makes any anon test pass.** Insert a real row, check as `anon`,
roll back:

```sql
begin;
insert into auth.users (instance_id, id, aud, role, email, encrypted_password, created_at, updated_at)
values ('00000000-0000-0000-0000-000000000000', gen_random_uuid(), 'authenticated',
        'authenticated', 'proof@example.test', '', now(), now());
insert into profiles (id, display_name) select id, 'ProofUser' from auth.users where email='proof@example.test';
select 'owner', count(*) from leaderboard;
set local role anon;
select 'anon', count(*) from leaderboard;   -- must be 0
rollback;
```

That proves anon is refused, not that the board works: a view that shows nobody
anything passes it too. For views, add the friend/self rows from
`postgres-view-privacy-mutation-proof`.

Also exercise the public key over HTTP — reads should return `[]` and writes
should fail `42501`:

```bash
curl -s "$URL/rest/v1/<table>?select=*" -H "apikey: $PUBLISHABLE_KEY"
curl -s -X POST "$URL/rest/v1/<table>" -H "apikey: $PUBLISHABLE_KEY" \
  -H "Content-Type: application/json" -d '{...}'
```

## 4. Schema conventions that avoid pain

- Store the client's local row id (`local_id`) and make `(user_id, local_id)`
  unique, so re-syncing upserts instead of duplicating.
- Case-insensitive unique handles: `create unique index … on profiles (lower(display_name))`.
- Friendship as one row per pair with a `no_self_friendship` check; expose
  `is_friend(a,b)` and `can_view(owner)` as `security definer stable` SQL
  functions and write policies in terms of `can_view`. `revoke ... from public`
  alone leaves such functions callable with the anon key; see
  `supabase-function-revoke-anon-trap` before relying on a revoke.
- Decide explicitly what must never sync (e.g. body measurements) and give it
  **no table** — absence is a stronger guarantee than a policy.

## 5. Android client wiring

Verify versions from Maven metadata rather than recall:
`https://repo1.maven.org/maven2/io/github/jan-tennert/supabase/postgrest-kt/maven-metadata.xml`,
ktor from Maven Central, `androidx.credentials` and `googleid` from
`https://dl.google.com/dl/android/maven2/...` (googleid is NOT on Maven Central).

- supabase-kt needs the **kotlin serialization plugin** and a ktor engine
  (`ktor-client-okhttp`); use the supabase BOM and omit versions on modules.
- Put URL/keys in gitignored `local.properties`, surface via
  `buildConfigField` + `buildFeatures { buildConfig = true }`. Blank values must
  disable the feature, not crash. The publishable/anon key is safe in an APK —
  RLS is the protection.

## 6. Google sign-in

Free, and no billing account is required: OAuth consent screen + client IDs are
not billable Cloud resources. Consent screen can stay in **Testing** with the
user added as a test user.

Needed: a **Web** OAuth client (its client id is the `serverClientId` AND what
Supabase's Google provider validates) plus an **Android** client bound to the
package name and signing SHA-1.

Get the debug SHA-1 without fighting shell quoting — write a `.cmd` wrapper and
run it, or use `gradle signingReport`:

```cmd
@echo off
set KT="C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe"
%KT% -list -v -keystore "%USERPROFILE%\.android\debug.keystore" -storepass android
```

**The nonce trap:** generate a raw nonce, pass its **SHA-256 hash** to
`GetGoogleIdOption.setNonce(...)`, and the **raw** value to
`auth.signInWith(IDToken) { nonce = rawNonce }`. Reversed, it fails with an
opaque invalid-nonce error.

A Google sign-in does NOT create your `profiles` row — derive a display name
from the account/email local-part, sanitise to the length constraint, and handle
`23505` by suffixing and retrying once.
