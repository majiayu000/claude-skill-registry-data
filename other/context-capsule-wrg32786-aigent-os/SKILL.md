---
name: context-capsule
description: Write a resume-ready capsule of the current session (objective, what it is waiting on, the next concrete action) so a /clear or an auto-compact can pick up exactly where this left off. Write it before compaction; nothing writes one for you at that point. Use for a checkpoint before risky work, before /clear, or when a thread ships.
---

# context-capsule

**The whole job: reconcile, write the capsule, confirm it, then stop.**

A capsule is a small markdown file with YAML frontmatter. A fresh session reads three fields from it and continues. It is state for the next session, not a transcript of this one.

## Steps

1. **Reconcile from live state.** Look at what is actually true now: `git status`, `git log -n 5`, the files you changed, any task list. Budget: 2 to 4 reads. Record what happened, not what was said. A capsule that restates the conversation instead of the repo state is the failure this skill exists to prevent.
2. **Write it with the helper**, which stamps the date, validates the fields and writes into the configured capsule directory:

   ```
   node "${CLAUDE_PLUGIN_ROOT}/scripts/capsule-lib.mjs" write \
     --objective "<what this work is for, one sentence>" \
     --waiting-on "<concrete items, owners, gates a fresh session must know>" \
     --next-action "<the one next step, specific enough to act on cold>" \
     --slug "<short-topic>" \
     --dir '${user_config.capsuleDir}'
   ```

   Run it from the project directory (do not `cd` elsewhere) and keep the `--dir` line exactly as written, single quotes included (they stop the shell expanding the placeholder when the option is unset). A configured path that itself contains a single quote is not supported. It carries the configured capsule directory. If the directory option is not set, that value is empty or still reads `${user_config.capsuleDir}` literally; then drop the `--dir` line and the helper uses the project default.

   Optional: `--body-file <path>` with your own body sections (see Format).
3. **Confirm.** The helper prints the path it wrote. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/capsule-lib.mjs" validate <that path>` and expect `VALID`. If it prints `INVALID`, fix the fields and write again.
4. **Stop.** Tell the user the capsule path in one line. If they asked for `/refresh`, tell them to run `/clear` next.

## Field rules

- `objective`, `waiting_on`, `next_valid_action` are required and must be non-empty. `waiting_on` is the resume contract: write it so a fresh session can act from it alone.
- `next_valid_action` must be a real action, not "resume the session" or "re-read the state". The helper refuses ceremony text.
- Do not paste secrets, tokens or credentials into a capsule. It is a plain file in the project.

## Format

Frontmatter fields: `id`, `parent_capsule_id`, `status: active`, `objective`, `waiting_on`, `resume_trigger`, `expires`, `trigger`, `next_valid_action`, `success_criteria`, `tags`, `created_at` (ISO-8601 with offset), `resolved_at`. Body sections: `Done (don't redo)`, `Historical-Errors -> Resolutions`, `Historical-Rejected-Approaches`, `Files-Read / Files-Modified`, `Operating-Facts`, `Pending-Gates`, `Claimed-Rows`. The format is compatible with the full aigent-os install.

## Lifecycle

`active` then `resumed` (set automatically by the SessionStart hook when a `/clear` loads it) then done. Never edit `status` by hand. Capsules older than 14 days (plugin option `maxAgeDays`, or the `CONTEXT_CAPSULE_MAX_AGE_DAYS` env var, to change) are refused at resume with a message, not loaded.

## When not to capsule

Mid-thought (finish the thought first), or a trivial session a fresh start can rebuild from the repo.
