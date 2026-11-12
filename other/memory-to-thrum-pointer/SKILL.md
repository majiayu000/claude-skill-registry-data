---
name: memory-to-thrum-pointer
description: "Use when MEMORY.md is near or over its read limit, or when adding a new memory entry. Moves an entry's full text into a thrum memory record and shrinks its index line to a trigger plus the thrum memory ID, with a byte-for-byte check."
---

# Memory to thrum pointer

## Why

An index line that restates a rule goes wrong when it is shortened, because shortening drops the scope that makes the
rule true. An index line written as a TRIGGER cannot contradict the rule, because it does not state the rule. It only
tells you when to read the full text.

So each entry has three parts:

- **Full text:** the topic file's body, copied unchanged into a thrum memory record (`--full`). This is the source to
  read before acting.
- **Trigger:** one line saying WHEN it applies, never WHAT it says. It goes in the record's `--oneline` field and in the
  index.
- **Topic file:** kept as the local copy. Never delete it.

Index line format, under ~140 characters:

```text
- 🔴 <trigger: when this applies> → `thrum-mem-<ID>`
```

The topic file carries `thrum_memory: <ID>` in its frontmatter; find it with `grep -l 'thrum_memory: <ID>' <memory dir>/*.md`.

Keep the 🔴 only on entries that already have it.

## Writing the trigger

Name the situation or action that should make you read the rule, for example "before choosing a model for any role" or
"when the email bridge decides which inbound mail it processes". Do not put the rule's answer in the trigger: no
"always", "never", "X not Y" or numbers. If the answer leaks in, it will drift from the full text.

Test it by asking: if I were about to take the wrong action, would this line make me stop and read? If not, name the
action more concretely.

## Steps for one entry

Use the helper for steps 1 to 5. Run it from any directory with `THRUM_REPO=<repo>` set to the thrum repo root (the
helper runs thrum from there). It extracts the body, creates or reuses the record, checks it byte for byte, writes
`thrum_memory` into the frontmatter, and prints the ID. It exits non-zero on any problem, and then you leave that index
line alone.

```bash
bash <skill-dir>/resources/to-thrum.sh <topic-file.md> "<trigger>" [agent_rule|lesson]
```

Then do step 6 by hand. The manual steps below are what the helper does.

1. Read the topic file. Its body (everything after the frontmatter) is the full text.
2. Check whether a thrum memory already holds that text. Search with `thrum memory search` on a distinctive phrase. If
   the topic file names a `thrum-mem-` ID, `thrum memory show <ID> --format body --zoom full` and compare.
3. If there is none, create one. Write the body to a scratch file first, then pass it with `@file`, so the shell never
   rewrites it:

   ```bash
   thrum memory create --kind agent_rule --scope agent \
     --title "<topic file name>" --oneline "<trigger>" \
     --full @"$SCRATCH/body.md" --tag claude-memory --json
   ```

   Use `--kind lesson` for a habit or lesson rather than a rule.
4. Verify byte for byte before touching the index:

   ```bash
   thrum memory show <ID> --format body --zoom full > "$SCRATCH/back.md"
   cmp "$SCRATCH/body.md" "$SCRATCH/back.md"
   ```

   If they differ only by a trailing newline, that is acceptable; note it. Any other difference: stop and do not change
   that index line.
5. Add `thrum_memory: <ID>` to the topic file's frontmatter `metadata`.
6. Replace that entry's text in MEMORY.md with the trigger-format line. Change only that one entry. Entries packed on
   one line with `·` are separate entries: move only the one you are converting and leave its neighbours as they are.

## Rules

- Never delete a topic file, a thrum memory or an index entry. This skill only adds records and shortens lines.
- Never merge two entries into one line or one record.
- Never reword the full text. It is copied exactly.
- Do not convert the FORMAT CONTRACT header or the hook warning at the top of MEMORY.md. They must stay in full in the
  index, because they guard against editing the index wrongly.
- thrum memories are local to this machine. Do not convert an entry another box has to read.
- After a batch, reload MEMORY.md and check its size is below 24.4KB, then re-read three converted entries' full text
  through the ID to confirm they come back.

## Using converted entries

When a trigger matches what you are about to do, read the full rule before acting. The trigger is not the rule. The
exact command, run from the thrum repo (thrum finds its daemon from the current directory, and the memory folder is not
a repo):

```bash
cd <repo> && thrum memory show <ID> --format body --zoom full
```

If thrum is unreachable, find the topic file by its ID (grep above) and read it: it holds the same text.

The index header carries this command once, near the top. Do not repeat it on each index line; one copy at the top is
always in view and costs a fraction of the space.

## Other runtimes (survey 2026-10-21, agents' own reports, mostly not measured)

The pattern works on every runtime. What changes is where the index lives and where the skill is installed. In every
case, spell out the read command with `cd <repo> &&`: no runtime resolves an ID by itself, and shells may be fresh
subshells.

| Runtime | Where the trigger index goes (always loaded) | Skill location | Limits |
|---|---|---|---|
| Claude Code | `~/.claude/projects/<slug>/memory/MEMORY.md` | `~/.claude/skills/` | 24.4KB index read limit |
| Codex | AGENTS.md chain | `~/.agents/skills/` | ~32KiB `project_doc_max_bytes`; MEMORY.md not read |
| OpenCode | AGENTS.md / CLAUDE.md (loaded in full) | `~/.config/opencode/skills/` or `.claude/skills/` | skill description always loaded: keep it short |
| Muse | its own MEMORY.md (native read_memory) | already sees `~/.claude/skills/` | no cutoff at 40KB (measured 2026-10-21, 401 lines); higher untested. Prefers its own topic files; use thrum IDs only for rules shared with other runtimes |
| Cursor | `.cursor/rules/<name>.mdc` with `alwaysApply: true` | `.cursor/skills/` | always-apply text loads in full, so this saves the most |
| Copilot | AGENTS.md or the Copilot plugin | `~/.copilot/installed-plugins/` | ~41KB output cap on prime |
| AGY | AGENTS.md / GEMINI.md / `.agents/rules/` | `.agents/skills/` | 24KB per file, 20k-token rules budget; tool is `run_command` |

Each box needs its own installed copy in its runtime's skill location, and thrum memory IDs are local to each box's daemon.

## Licensing

`thrum memory create` needs the memory.substrate entitlement. The helper checks it through the daemon: a
`thrum memory edit` on a probe ID returns "not found" only when the entitlement is granted, because the gate runs before
the lookup and nothing is written. The check does not look at the license tier, so any tier that the server grants the
feature to proceeds. Without the entitlement the helper prints "needs Thrum Pro (free for eligible public
repositories)", exits 7, and changes nothing: no record and no index change.

## Improving this skill

If a trigger fails to stop a wrong action, or a step here is unclear, fix this file in the same turn and note what changed.
