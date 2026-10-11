---
name: client-watermark-server-wipe
description: "Use when clearing debug/staging cloud data, rebuilding a server store a sync client pushes into, after server-side data loss, or when sync says it worked but the cloud stays empty. Also when a user's synced records never re-upload after an in-app erase and sign-in."
---

# Wiping a server store a client syncs into

## The trap

A push-only sync client usually avoids re-uploading unchanged records by keeping
a **watermark** — a per-record fingerprint of what it believes the server already
holds. It lives on the **device**, not the server.

```
watermark[sessionId] == fingerprint(record)  ->  skip the upload
```

Wiping the server changes **no fingerprint**. So after the wipe every record
still "matches", the ordinary sync skips all of them, and the server stays empty
**permanently** — until some unrelated edit happens to change a fingerprint.

The wipe appears to succeed. The failure is silent and shows up as "sync says it
worked but the cloud is empty".

## Check this first: the existing erase feature probably has the same bug

Any shipped "delete my cloud data" / "erase my account data" action almost
certainly deletes server rows and forgets to clear the local watermark. Trace it:

1. Find the delete call (e.g. `deleteCloudData()`).
2. Find where the watermark is stored (`sync_state` table, prefs, a DAO).
3. If the delete path never clears it, the feature is broken: erase, sign back
   in, and the user's data never re-uploads.

That is a real privacy/data-integrity defect, not a hypothetical — report it even
if the task was only "wipe the debug data".

## The fix, in the code

Add three things, smallest first:

```kotlin
// DAO
@Query("DELETE FROM sync_state")
suspend fun clearAll()

// Repository
suspend fun clearPushWatermark() = syncStateDao.clearAll()

// Sync facade (it already holds Repository — no new wiring)
suspend fun forgetPushedState() = repo.clearPushWatermark()
```

Then:
- call `forgetPushedState()` on the **success** branch of the erase action;
- expose a user-facing **"Re-upload everything"** action = `forgetPushedState()`
  then `push()`. This is the only recovery from server-side data loss, so it
  earns a permanent place in the UI, not a debug flag.

## Run order — all three steps or it fails silently

1. Wipe the server.
2. **Clear the client watermark** (the new action).
3. Push, then verify the data actually reappeared server-side (count rows as the
   user, per `supabase-applied-state-from-device-jwt`).

Write step 2 into the wipe script's header comment. Whoever runs the SQL months
from now will not know the watermark exists.

## Writing the wipe script

- Put it **outside** the migrations directory (`supabase/reset_dev_data.sql`,
  not `supabase/migrations/`). A destructive truncate must never be runnable as
  part of a deploy.
- `truncate ... restart identity cascade` over the app tables, leaf-first for
  readability even though `cascade` makes order irrelevant.
- **Fake/test accounts are auth rows, not just profile rows.** Truncating the
  profile table alone leaves them able to sign in and re-create a profile.
  Delete from the auth table too.
- If the owner runs it in the hosted SQL editor, make the auth-table delete its own
  execution: one failing statement rolls back the whole run, truncate included
  (see `supabase-applied-state-from-device-jwt`).
- **Default to keeping the owner's own auth row.** Deleting it costs them their
  login, their claimed handle and any unique-name index entry; the profile row
  it points at is rebuilt by the re-upload anyway. Offer the full wipe as a
  commented-out alternative.
- End with a verification `select` unioning `count(*)` per table.

## Credentials reality check

Before promising a wipe, check what key you actually have:

- **anon key** (typical in `local.properties` / `BuildConfig`): RLS restricts it
  to the signed-in user's own rows. It **cannot** delete other users' data. You
  can write the script but not run it.
- **service-role key / DB connection string**: required for a full wipe.

If only the anon key is present, say so plainly and hand over the script rather
than implying the wipe was done.

## Ordering client and server changes

If the same job adds a new server column the client reads, give the client field
a **default** (`= 0`, `= null`):

```kotlin
@SerialName("held_seconds") val heldSeconds: Long = 0,
```

The client then decodes correctly against both the old and new schema, so the
migration can be applied at any time and in any order, and one missing field
never fails the whole page's decode.
