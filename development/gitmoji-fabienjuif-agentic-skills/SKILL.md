---
name: gitmoji
description: Commit the current changes with a gitmoji-prefixed message (https://gitmoji.dev), picking the one gitmoji that matches the intent of the change and following the repo's own commit format. Use when the user says "/gitmoji", "gitmoji commit", "commit with a gitmoji", "commit this with an emoji", "which gitmoji for this", or asks to commit in a repo whose convention or history uses gitmoji. Commits only; never pushes.
effort: low
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git add *) Bash(git commit *)
---

# /gitmoji: commit with a gitmoji

One commit, one intent, one gitmoji. The emoji is picked from the **intent** of the change
(why it was made), not from the file types touched.

Speed matters here: the target is **one tool call** (the commit). Pick the gitmoji yourself,
inline; do not delegate it to a sub-agent (a spawn costs more than the pick).

## Context (injected at load, do not re-run these)

Working tree (`git status --short`):

```!
git status --short
```

Staged (`git diff --staged --stat`):

```!
git diff --staged --stat
```

Recent commits (`git log --oneline -15`):

```!
git log --oneline -15
```

## Process

### 1. Scope

- **Something is staged:** the user already chose the scope. Commit exactly that, add nothing.
- **Nothing is staged:** stage the files that belong to the change, by name. Leave unrelated or
  stray untracked files alone; ask if it's unclear whether one belongs.

Read the actual diff (`git diff --staged`, or `git diff` when nothing is staged) **only if**
this session doesn't already know what the changes are. If you made or reviewed them here,
skip it.

### 2. Match the repo's commit format

The repo's convention always wins over this skill's default:

1. A documented format already in context (`CLAUDE.md`, `AGENTS.md`). Don't go hunting for one.
2. Otherwise the recent commits above: shortcode (`:bug:`) vs rendered glyph, scope/theme
   prefix, casing, presence of a body.

Default when the repo says nothing: `:shortcode: <short, lowercase, imperative summary>`,
single line, subject under 60 chars, no body. Prefer the shortcode over the glyph.

### 3. Pick the gitmoji

Most commits are covered by this short list:

| Shortcode               | Use for                                  |
| ----------------------- | ---------------------------------------- |
| `:sparkles:`            | new feature                              |
| `:bug:`                 | bug fix                                  |
| `:memo:`                | documentation                            |
| `:recycle:`             | refactor (no behaviour change)           |
| `:white_check_mark:`    | add, update, or pass tests               |
| `:wrench:`              | configuration files                      |
| `:fire:`                | remove code or files                     |
| `:zap:`                 | performance                              |
| `:arrow_up:`            | upgrade dependencies                     |
| `:construction_worker:` | CI build system                          |
| `:truck:`               | move or rename files, paths, routes      |
| `:tada:`                | initial commit                           |

If none fits, **search** the full list rather than reading it: grep
`${CLAUDE_SKILL_DIR}/gitmojis.md` (the `gitmojis.md` next to this file) for a keyword of the
intent, e.g. `security`, `typo`, `revert`, `types`, `database`. Read the whole file only after
a couple of greps miss. It also carries the glyph for repos that use the rendered form.

Never invent a shortcode: it must exist in that file.

When the diff mixes intents:

- Staged by the user: keep it one commit, pick the dominant intent.
- Staged by you: split into one commit per intent when they separate cleanly by file;
  otherwise one commit with the dominant intent.

### 4. Commit

Stage (when needed) and commit in a **single** call:
`git add <files> && git commit -m "<message>"`. Do not push.

`git commit` already prints the short sha and subject, so don't follow up with `git log`.
Say nothing beyond that line (one per commit when split).
