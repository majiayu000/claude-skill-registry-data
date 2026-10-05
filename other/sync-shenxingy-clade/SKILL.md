---
name: sync
description: "End-of-session documentation sync — updates TODO.md and PROGRESS.md only (run /commit after to commit everything)"
---

# Clade for Codex

This workflow runs **directly in Codex**. Do not launch the `claude` CLI or
delegate the workflow to Clade's MCP bridge.

Codex compatibility rules:

- Plugin skills are namespaced. Invoke this workflow explicitly as
  `$clade:sync`; a bare `$name` does not select the installed Clade plugin.
- Read the nearest `AGENTS.md` files for repository instructions. If a project
  has only `CLAUDE.md`, treat it as legacy project guidance and read it too.
- Store new Clade working state under `.clade/` (or `~/.clade/` for personal
  state). Existing legacy Claude state may be read for migration, but do not
  create new vendor-specific state.
- A `/skill-name` reference means the corresponding Codex
  `$clade:skill-name` plugin skill, or the same workflow invoked naturally when
  explicit skill invocation is not available.
- Use Codex web, file, shell, image, and subagent capabilities when the source
  workflow names a vendor-specific tool. If a capability is unavailable, use
  the documented fallback instead of spawning another agent CLI.
- Paths such as `<plugin-root>/...` are relative to the installed Clade plugin
  containing this `SKILL.md`; resolve that root before invoking a helper.

## Canonical Clade workflow

You are the Sync skill. You automate the end-of-session documentation ritual.

This skill only updates documentation files (TODO.md, PROGRESS.md). It does NOT commit.
After /sync, the user runs `/commit` to commit all changes (code + docs) split by module.

---

## Step 1: Review recent work

Find what was done in this session:

1. Get the time window: Look for the last sync marker in PROGRESS.md, or default to the last 8 hours.
   ```bash
   git log --since="8 hours ago" --oneline
   ```
2. Get detailed changes:
   ```bash
   git log --since="8 hours ago" --stat
   ```
3. Read the commit messages to understand what was accomplished.
4. Also check for uncommitted changes via `git status --short`.

Build a mental model of: what features were added, what bugs were fixed, what was refactored.

---

## Step 2: Update TODO.md

1. Read `TODO.md`
2. For each unchecked `- [ ]` item, determine if the recent commits implemented it:
   - Match commit messages against TODO item descriptions
   - Use Grep to verify the implementation exists in code (e.g., if TODO says "add X route", grep for that route)
   - Only check off items you can verify — don't guess
3. Edit TODO.md to check off completed items: `- [ ]` → `- [x]`
4. If you discover new sub-tasks during verification, add them under the relevant step
5. Show what was checked off:
   ```
   TODO.md updated:
     ✓ Checked off: "Add project_repos table" (verified: schema exists)
     ✓ Checked off: "GitHub API client" (verified: lib/github-client.ts exists)
     ? Skipped: "OAuth integration" (no matching commits found)
   ```

---

## Step 3: Update PROGRESS.md

Add the session summary at the TOP of PROGRESS.md, immediately below the archive-pointer line — the log is newest-first and `archive-progress.py` keeps the newest entries that fit under the cap. Appending puts today's work first in line to be archived. Follow this format:

```markdown
### YYYY-MM-DD — [Brief session description]

**What was done:**
- [Feature/fix 1]: [one-line description of what and why]
- [Feature/fix 2]: [one-line description]

**What worked:**
- [Pattern or approach that was effective]

**What didn't work / lessons:**
- [Issue encountered and how it was resolved, or pitfall to avoid]

**Open items:**
- [Anything left unfinished that the next session should pick up]
```

Guidelines:
- Be concise — each bullet is one line
- Focus on lessons (what worked, what didn't) — this is the most valuable part
- Don't list every file changed — focus on the "why" and insights
- If nothing notable went wrong, skip "What didn't work"

---

## Step 3b: Prune old entries

If PROGRESS.md exceeds 100 lines, run the tool CI gates on rather than
archiving by hand:

```bash
python3 configs/scripts/archive-progress.py --apply
```

It keeps the newest entries that fit under the cap plus anything marked
`[ACTIVE]`, writes the rest to `docs/progress-archive/YYYY-MM.md`, reroots their
links, and refreshes the single archive pointer in the header. **Age is not the
criterion — the cap is.** This file used to say "older than 30 days", which
disagreed with the gate: a 40-day entry stays if it fits, and a 2-day entry
moves if it does not.

Report what it printed.

---


## Step 3c: Generate session scorecard

Run the session scorecard generator to log quality metrics:

```bash
bash ~/.clade/scripts/session-scorecard.sh
```

This appends a JSON entry to `~/.clade/corrections/scorecards.jsonl` with correction counts, commits, and a quality score. If the script doesn't exist, skip this step silently.

---

## Step 3d: Archive tier files

Check for 3-tier issue handling files from autonomous loop runs:

```bash
ls .clade/decisions.md .clade/skipped.md .clade/blockers.md 2>/dev/null
```

For each file that exists:
1. Append its contents to `.clade/{name}-archive.md` (create if needed)
2. Delete the original file
3. Report what was archived

If none exist, skip silently.

---

## Step 3e: README length check

A README is a landing page, not a reference manual: the cap is 300 lines.
Check every README at the repository root — `README.md` and its localized
siblings — and name the sections that should move into `docs/`.

```bash
# Each oversized README, then its `##` sections largest-first.
for f in README.md README.*.md; do
  [ -f "$f" ] || continue
  n=$(awk 'END {print NR}' "$f")
  [ "$n" -gt 300 ] || continue
  echo "OVER CAP: $f — $n lines (cap 300)"
  awk '/^## /{if (h != "") printf "  %5d  %s\n", NR - s, h; h = $0; s = NR}
       END {if (h != "") printf "  %5d  %s\n", NR - s + 1, h}' "$f" | sort -rn
done
```

Nothing printed: every README is inside the cap. Say nothing and move on.

The section sizes are a ranking hint, not a measurement — a `##` line inside a
fenced code block counts as a heading here. Read the file before trusting a
surprising number.

When a README is over the cap, name the move candidates. Four things stay in
the README however large it grows — install, the key-features table, the
command table, and the links into `docs/` — so the candidates are the largest
of what is left, and each candidate names the `docs/` file it would become.

Then record the flag so it outlives the session. Only when `TODO.md` exists,
and only when it is not already carrying this flag:

```bash
grep -Fq "over the 300-line landing-page cap" TODO.md
```

If that matches nothing, add one unchecked item per oversized README, in this
wording — the fixed phrase is what the grep above matches on the next run, so
keep it verbatim:

```
- [ ] README.md is over the 300-line landing-page cap (310 lines). Move
      "Skills" (64 lines) and "MCP Server" (32 lines) into docs/, leaving a
      link behind.
```

Do NOT move the sections yourself. This skill writes `TODO.md` and
`PROGRESS.md` only; splitting a README is a separate edit with its own review.

---

## Step 4: Print summary

Always end with a summary:

```
Sync complete:
  📋 TODO.md: 3 items checked off, 1 new sub-task added
  📝 PROGRESS.md: Session summary appended
  📏 README.md: 310 lines — over the 300 cap, flagged in TODO.md

  Run /commit to commit all changes. It checkpoints LOCALLY by default and
  publishes only with `--publish` or an existing delivery/repository
  authority — there is no `--no-push`, and there never was.
```

Drop the 📏 line when every README is inside the cap.

---

## General rules

- Be concise. This is a utility, not a conversation.
- Only check off TODO items you can verify — false positives are worse than false negatives.
- Don't modify TODO.md structure (don't reorder, don't delete items, don't change headers).
- PROGRESS.md entries should be useful to future-you, not a changelog.
- If there's nothing to sync (no recent commits, no changes), say so and exit.


---

## Completion Status

- ✅ **DONE** — task completed successfully
- ⚠ **DONE_WITH_CONCERNS** — completed but with caveats to note
- ❌ **BLOCKED** — cannot proceed; write details to `.clade/blockers.md`
- ❓ **NEEDS_CONTEXT** — missing information; use AskUserQuestion

**3-strike rule:** If the same approach fails 3 times, switch to BLOCKED — do not retry indefinitely.

## Additional skill reference

# Sync Skill

End-of-session documentation ritual. Reviews what was done and updates project docs — no commit. Run `/commit` after to commit everything (docs + code) split by module.

## What it does

1. Reviews recent git history to understand what was accomplished
2. Auto-updates TODO.md (checks off completed items)
3. Prepends a session summary to PROGRESS.md (newest-first; appending puts today's work first in line to be archived)
4. Flags a root README over the 300-line landing-page cap, naming the sections that should move to `docs/`

## Usage

```
/sync            # Update TODO.md + PROGRESS.md
/commit          # Commit all changes (code + docs) split by module — local only
/commit --publish  # Commit, then publish the owned branch
```

## Delivery completion

If this workflow changes files or external state:

- Inspect the real final state before responding, including `git status` for a
  repository task.
- Never report `DONE` while task-owned changes are uncommitted. Use or continue
  `$clade:delivery` and create a repository-compliant checkpoint or preserve
  the work when committing is unavailable.
- When the user request or trusted repository policy makes publication,
  deployment, or live verification part of the task, do not silently downgrade
  the result to local-only work.
- If a required delivery transition lacks authority, credentials, a destination,
  or reachable external state, report `BLOCKED` or `NEEDS_CONTEXT` rather than
  appending a "not committed/pushed/deployed" caveat after `DONE`.
