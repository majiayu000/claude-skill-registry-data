---
name: commitLog
description: Write the day-log entry every log-cli commit needs, in the private devlog (LOG_DEVLOG_DIR, default ~/.logCli/devlog/<date>.md, indexed by log.md there), never in the repo. On commit, the commit-msg hook parses the staged code into an abstract syntax tree (AST), writes which declarations and tests were added, changed or removed into a template entry, and feeds that back to the agent. The agent writes What changed, Why and Checked in the commit message (one commit) or under the template (two).
---

# commitLog

The day log is the running record of the work, one entry per commit. It is
private: the repo is public, and day logs quote requests, people and infra
steps. It lives in `LOG_DEVLOG_DIR` (default `~/.logCli/devlog/`), one file per
day, `<date>.md` (the day in UTC, newest entry at the bottom), and `log.md` in
the same folder is the index of every day, newest first. lefthook's commit-msg
hook (`lefthook.yml`) runs `scripts/commitLog/commitLog.mjs --message <file>`, which uses
`scripts/commitLog/astSummary.mjs`:

- `.ts` / `.mjs` files are parsed with the TypeScript compiler API.
- `.py` files are parsed with Python's own `ast` module.
- For each file it compares the syntax tree before and after the change and
  lists what was added, changed or removed: top-level functions, classes,
  interfaces, types, enums, consts, re-exports, and test titles in
  `*.test.ts`. Formatting-only edits don't count as changes.

## Hard boundaries

1. **Every commit gets an entry.** No `--no-verify`, ever.
2. **Never edit the AST block.** The tool writes it. If it looks wrong, fix
   `scripts/commitLog/astSummary.mjs`, not the entry. The hook rejects a block that
   doesn't match the staged code, and rewrites it.
3. **Never edit old entries.** Only add.
4. **Write the three fields from the AST,** in plain words, naming the real
   behaviour, commands and results. No `<fill in>` left.
5. **Nothing from the day log goes in the repo.** Never copy an entry into a
   tracked file. The hook stages nothing.

## The routine

Commit once, with the three fields in the message:

```bash
GIT_CONFIG_COUNT=0 git add <files>
GIT_CONFIG_COUNT=0 git commit -F <message file>
# the message carries, after its subject and body:
#   What changed: <plain facts>
#   Why: <the reason>
#   Checked: <what was run, and what wasn't>
# the hook parses the staged code, writes the entry (AST block plus the three
# fields) to today's ~/.logCli/devlog/<date>.md, prints the AST, and the commit
# goes through
```

Without the three lines in the message, it is two tries, as before:

```bash
GIT_CONFIG_COUNT=0 git commit -m "..."
# 1st try: the hook prints the AST of the staged change, appends the entry
#          to today's ~/.logCli/devlog/<date>.md, updates the index log.md
#          there, remembers the entry as this checkout's pending one, and stops
# write What changed / Why / Checked under the AST block in that file
GIT_CONFIG_COUNT=0 git commit -m "..."
# 2nd try: the hook re-parses the staged code; if it matches the block and the
#          fields are written, the commit goes through
```

A pending template left by a stopped commit is filled from the message's three
lines when the next commit carries them, so it is never written twice.

The pending entry is kept per checkout in `<devlog>/.pending/`, and lefthook's
post-commit clears it once the commit lands, so a commit stopped by a later
hook keeps its written entry. If you change code after the entry was written,
the hook updates the AST block in place and stops once more. Re-read your What
changed line and commit again.

To see the AST for any commit: `node scripts/commitLog/astSummary.mjs <commit>`. With
no argument it shows the staged change.

## The entry

```markdown
## 2026-10-18 05:40Z · feat/branchName

AST (generated from the staged code by scripts/commitLog/astSummary.mjs, don't edit):
- `src/camofox/worker/helpers/fromCamofoxStatus.ts`: added function fromCamofoxStatus
- `src/cli/live/index.ts`: added const connectCommand · removed const loginCommand

What changed: <fill in>
Why: <fill in>
Checked: <fill in>
```

- **What changed**: the behaviour behind the AST lines. Example: "`log facebook connect`
  replaces `log login` for Facebook sessions", not "edited index.ts".
- **Why**: the request or bug behind it. Quote the owner's ask when there is one.
- **Checked**: the exact command and its result (`bun run check`: 62 pass),
  plus any real run. Say what you didn't check.

If the commit also adds a rule from the owner, `skills/captureRule/SKILL.md`
applies too.
