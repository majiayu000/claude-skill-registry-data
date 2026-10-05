---
name: sync
description: 'Sync the Gmail filter set to match filters.js — dry run first, then apply. Owns the 🔍 and 💾 title prefixes across that pair, so other sessions can see a live write in flight. Use when asked to sync, apply the spec, push filters to Gmail, or reconcile the account with filters.js.'
---

# Sync (filters.js → the live Gmail filter set)

`src/sync.js` is a dry run by default; `--apply` performs the deletes and creates. This skill is the
two of them as one operation, and it exists because the stretch between them is the only thing in
this repo another session acts on. See `AGENTS.md` (Repo → Session titles).

`filter` and `archive` end by syncing — they invoke this skill rather than calling `sync.js`
directly, so the prefixes go on wherever a sync happens.

### 1. `🔍 ` before the dry run

Read the session's title (`mcp__ccd_session_mgmt__get_session` with `"self"`) and set it back with a
`🔍 ` prefix (`mcp__ccd_session_mgmt__set_session_title`), replacing any existing lifecycle prefix
rather than stacking. Do not report this.

Then:

```bash
node src/sync.js
```

Read the plan. Nothing is written yet.

### 2. Check the sidebar before applying

`--apply` takes a lock, but the dry run does not, so the plan just printed is stale the moment
another session applies. List sessions (`mcp__ccd_session_mgmt__list_sessions`) and look for another
`💾 `. If one is there, wait rather than applying — and re-run step 1 afterwards, because its plan was
computed against the account as it was.

Re-run step 1 too if anything else happened between the dry run and here.

### 3. `💾 ` across the apply

Swap the prefix to `💾 ` **before** the command, not after it returns — the warning is only useful
while the write is in flight. Do not report this.

```bash
node src/sync.js --apply
```

It prompts before a destructive run and refuses without a terminal to ask; `--yes` skips the prompt.
If it stops for that confirmation and the user has to click, the title stays `💾 ` while it waits — a
write in flight outranks a park, and handing back mid-apply is still mid-apply.

### 4. Whatever stage the branch reached

Once it returns, replace `💾 ` with what is true now: `📦 ` if the change is gated and shippable,
`⏳ ` if there is more to do, `🚙 ` if it waits on the user. Never leave `💾 ` on a session that has
stopped writing — another session reads it as a live write and waits on nothing. Do not report this.

If the apply failed, say so with its output and put the title back the same way. A partial apply is
possible: re-run step 1 to see what the account actually holds rather than assuming the plan applied
or did not.
