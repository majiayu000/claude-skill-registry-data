---
name: comment-batch
description: Run /comment-file across a glob of files (e.g., one Comment Plan session at a time). Tracks progress with TaskCreate, runs /typecheck after each batch, and commits at the end. Use to execute one C-session of the Comment Plan.
---

# comment-batch

Drives one session of [[Sessions/Comment Plan C1-C20]]. Takes a glob, runs `/comment-file` on each file, verifies, and commits.

## Inputs

- **Session number** (e.g. `C4`) — used for the commit message and task labels
- **Glob or file list** — what to process (e.g. `apps/api/routes/{leads,customers,activities,contact-log,appointments}.ts`)
- **Mode** (default `update`) — passed through to `/comment-file`

## Steps

1. **Read** [[Sessions/Comment Plan C1-C20]] and confirm the session scope matches what the user asked for. If the glob doesn't match the plan, ask before proceeding.
2. **Read** [[Engineering/Comment Style]] once for this session.
3. **List the files** matching the glob. Show the user the count and ask to confirm before starting (commenting is reversible but noisy).
4. **Create TaskCreate items** — one per file. Mark the first `in_progress`.
5. **For each file**:
   a. Run `/comment-file` on it
   b. Mark the task `completed`
   c. Run `/typecheck` every 5 files (cheap insurance against accidentally breaking imports)
6. **After all files**:
   - Run `/typecheck` once more for the whole monorepo
   - Run `/coverage-report` and report the new coverage %
   - Read the diff (`git diff --stat`) and sanity-check the file count
7. **Tick the master plan** — edit `Aqarkom_Knowledge/Sessions/Comment Plan C1-C20.md`, change ⏳ → ✅ for this session row
8. **Commit** with `/commit-and-track` using a message like `docs: comment session C4 — CRM routes (5 files)`
9. **Report** to the user:
   - Files commented
   - Coverage % before/after
   - Next ⏳ session in the plan

## Verification

- [ ] User confirmed the file list before processing
- [ ] `/typecheck` clean at the end
- [ ] Master plan row ticked
- [ ] Single commit landed
- [ ] Coverage % reported

## Anti-patterns

- ❌ Don't run `comment-batch` across an entire app in one shot — that's why the C plan is broken into 20 sessions
- ❌ Don't commit per file — one commit per session keeps history readable
- ❌ Don't skip `/typecheck` between batches — broken imports surface late and waste time
- ❌ Don't continue past a typecheck error — fix or rollback the offending file first

## Notes

- Typical session is 5–15 files. If a session has 30+ files (like `components/admin/`), run two `/comment-batch` calls and commit twice.
- For Prisma schema (C2), don't use this skill — it's a single file with a different syntax (`///` triple-slash). Run `/comment-file` directly.
