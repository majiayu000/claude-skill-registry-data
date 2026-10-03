---
name: crav1-draft-commit-message
description: >-
  Draft paste-ready GitKraken Summary and Description only. Does not create a
  git commit. Ask style.md vs this repo’s git log, this commit only or onward
  as a deletable rule. Use for GitKraken paste, or /crav1-draft-commit-message.
  To edit the wording and then copy or git commit, use /crav1-finalize-commit.
  When docs/specs/<slug>/work-item.md exists, append that work-item mention
  as the last description line.
disable-model-invocation: true
icon: git-commit
color: purple
---

# Draft commit message

You draft paste-ready **Summary** and **Description** (GitKraken fields). You do **not** create the commit unless the user also asked you to commit.

Command: `/crav1-draft-commit-message`. To **edit** the text and/or **create** the commit after they accept it, use `/crav1-finalize-commit` (it follows this skill, then a commit / copy / edit / rewrite / stop menu, **commit first**).

Bundled style: [references/style.md](references/style.md).  
Git-log style: this repo’s recent `git log` (subject + body).

Persistent rules (at most one should exist). If a file in the table exists, do not ask.

| File | Meaning | Template |
| --- | --- | --- |
| `.claude/rules/draft-commit-style.md` | Always `style.md` (Claude Code project) | `assets/draft-commit-style.mdc` |
| `.claude/rules/draft-commit-gitlog.md` | Always live `git log` (Claude Code project) | `assets/draft-commit-gitlog.mdc` |
| `~/.claude/rules/draft-commit-style.md` | Always `style.md` (Claude Code user) | `assets/draft-commit-style.mdc` |
| `~/.claude/rules/draft-commit-gitlog.md` | Always live `git log` (Claude Code user) | `assets/draft-commit-gitlog.mdc` |

On Claude Code, write the **project** path when this repo contains the kit (`.claude/` or `.cursor/` in git). Write the **user** path when the kit lives in `~/.claude/` and this repo did not ask for the kit in git, so the rule is not committed into a client repo.

Also treat these **legacy** names as the same persist (if you find them, use them; new writes use the names above):

- `.claude/rules/gitkraken-commit-style.md` or `~/.claude/rules/gitkraken-commit-style.md` → style.md onward
- `.claude/rules/gitkraken-commit-gitlog.md` or `~/.claude/rules/gitkraken-commit-gitlog.md` → git log onward

## Before drafting

1. Inspect what would be committed (staged first; if empty, unstaged). On Windows, `git` may not be on `PATH` — try `git`, then `C:\Program Files\Git\cmd\git.exe`.
2. Read `git log` (about 8–15 commits: subject + body) when git works.
3. Check which persist rule exists (new names first, then legacy).

### If a **style.md onward** rule exists

Do **not** ask. Draft using `references/style.md` (`style.md` wins over the log). After the blocks: delete that rule file to stop; mention the git-log rule if both files exist (ask which to keep).

### If a **git-log onward** rule exists (and no style.md rule)

Do **not** ask. Draft matching **live `git log`**. If the log is empty, say so and fall back to asking the menu. After the blocks: delete the git-log rule file to stop.

### If neither rule exists

**Do not draft yet.** Offer these options (questions tool when available). Explain impact:

| Id | Choice | What it does | Disk |
| --- | --- | --- | --- |
| `once` | `style.md`, this commit only | Use bundled `references/style.md` for **this** message. Ask again next time. | None |
| `onward` | `style.md`, this commit and onward | Same, **and** write the style persist rule. Remove any git-log persist rule. | Claude Code project: `.claude/rules/draft-commit-style.md`. Claude Code user (kit not in this repo’s git): `~/.claude/rules/draft-commit-style.md`. Content from `assets/draft-commit-style.mdc`. |
| `log-once` | Git log, this commit only | Match **this repo’s** recent messages for **this** message. Ask again next time. | None |
| `log-onward` | Git log, this commit and onward | Same, **and** write the git-log persist rule. Remove any style.md persist rule. | Claude Code project: `.claude/rules/draft-commit-gitlog.md`. Claude Code user (kit not in this repo’s git): `~/.claude/rules/draft-commit-gitlog.md`. Content from `assets/draft-commit-gitlog.mdc`. |

If `git log` is empty or unavailable, say that `log-once` / `log-onward` have no pattern to copy; they can still pick `style.md`.

If they already named an id (`once`, `onward`, `log-once`, `log-onward`), skip the menu.

After `onward` or `log-onward`: write the matching **new** rule name **before** showing the message, and delete the other persist files (including legacy names) so only one remains. Tell them they undo by **deleting that rule file**.

## Draft

4. Apply the chosen source (`style.md` **or** live log — not a blend that reintroduces Conventional Commits unless the log already uses it).
5. Draft **one** message for the intended set of files. Warn if `artifacts/`, `bin/`, `obj/`, or other build output is staged. Leave any work-item mention out of this draft.
6. Resolve an optional Azure Boards mention in [references/work-item-mention.md](references/work-item-mention.md). Subject and the drafted description stay as written. When a mention is resolved, append one blank line and that mention as the **last line** of the Description. When it is not, the Description ends where the draft ended.
7. Output only paste blocks (see below). A hint from the work-item reference, when it has one, is a single sentence **after** the blocks. Do not run `git commit` unless they asked.

## When the source is `style.md`

- **Summary:** one line, sentence case, no trailing period. Imperative or “Adds/Implement …”. Include `(T#)` when the change completes a `tasks.md` row. Not marketing (“Ship…”) and not `type(scope):`.
- **Description:** GitKraken Description field. `- ` bullets. Lead with why/what; name endpoints, tests, and spec task checkboxes when those are in the diff.

## When the source is git log

- Copy the **shape** of recent subjects and bodies (length, prefixes or lack of them, bullets vs paragraph).
- Do not force `style.md` rules if the log does something else (including Conventional Commits).
- Still scope the message to the files they will actually commit.
- Do not copy a trailing `#<id>` or `AB#<id>` line from older commits into the description. Step 6 appends the current slug’s mention once.

## Output

```markdown
**Summary**
```
<summary>
```

**Description**
```
- bullet
- bullet
```
```

When a work-item mention was resolved, the Description fence includes it as the last line, after a blank line:

```
- bullet
- bullet

AB#52
```

That line is `#<id>` or `AB#<id>` per the work-item reference (or the file’s full token). It is part of the Description they paste into GitKraken. Omit it when no mention was resolved.

If they should exclude paths, add one short sentence after the blocks. The work-item hint, if any, is another short sentence after the blocks, not inside them.
