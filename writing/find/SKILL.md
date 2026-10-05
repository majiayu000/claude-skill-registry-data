---
name: find
description: Find the local coding-agent session that wrote the uncommitted changes in a file, or in a pasted snippet of changed code or comment text, and give a one-line command that resumes it. Prefers the session that authored the change over a review session. Use when asked which session, chat, thread, or agent made an edit, or how to get back to the session behind a change.
metadata:
  website: "https://photostructure.com/coding/"
---

# Find the Session Behind a Change

> More on these workflows: [photostructure.com/coding](https://photostructure.com/coding/) (no dedicated `find` article yet)

Report which local agent session wrote a change that is still uncommitted, and
give the user a command that resumes it.

## Run the finder

Resolve the bundled [`scripts/find_session.py`](./scripts/find_session.py)
relative to this skill directory. Run it with the host's Python 3 launcher from
inside the repository that holds the change:

```text
python3 scripts/find_session.py <path-or-snippet>
```

- A path to a file with uncommitted changes attributes that file's whole diff
  against HEAD.
- Any other argument is a snippet of changed text. The finder locates it in the
  diff against HEAD, untracked files included, and attributes only the lines it
  spans. Indentation, line breaks, and leading comment markers are ignored, so
  a comment copied across wrapped lines still matches. Pass a multi-line
  snippet as one quoted argument.
- `--days N` searches transcripts modified in the last N days (default 14).
  `--limit N` caps the candidates shown (default 5).

On Windows, `py -3` is a common equivalent.

## How it attributes a change

The finder reads the transcripts that both supported agent CLIs keep under the
user's home directory; the script's docstring names the directories and the
environment variables that relocate them. It keeps only writes that succeeded,
and scores each session by how many of the target's changed lines its writes
added or removed. It counts:

- patches recorded by the file-editing tools;
- patch envelopes applied through a code-execution tool;
- shell commands that write the file and either name its absolute path or run
  inside its checkout, as weaker evidence, reported as "only through shell
  commands";
- writes to a path that no longer exists but has the target's file name and
  lies inside the same checkout, outside git-ignored directories, because the
  file was moved after them.

A session that only read, searched, or diffed the file never counts.

A session whose first prompt starts by running the coding `review` or
`review-staged` skill is a reviewer. A cross-model second opinion launches its
reviewer that way. Reviewers rank after every author, even one that wrote fewer
of the lines. Writes made by a subagent resume through its parent session.

Each candidate shows its last write to the file relative to the file's
modification time. A gap under a second or two means that session made the
most recent write. A formatter or a later session can move the modification
time without writing any of the attributed lines.

## Report

1. Lead with the top candidate: host, role, title, lines matched, and last
   write.
2. Put its resume command alone in a fenced code block, exactly as printed, so
   the user can copy one line.
3. Name another candidate only when it wrote a large share of the lines, and
   give its resume command the same way.
4. If the finder exits with an error, report its message. When no session
   matches, say so and offer a larger `--days`. Never name a session because it
   mentions the file; mentions are not writes.
