---
name: pr-post-comments
description: >
  Turn review findings or review replies into tagged, human-sounding PR comments
  and post them paced, one at a time, through a bundled driver. Applies the
  [r|o|f|c] tag scheme, dedupes against bot reviewers, lints every body against
  a fixed set of voice rules, drafts for approval, then posts with a delay sized
  to how long each comment would take to write. Use after pr-review or any PR review, when
  the user says "post the comments", "post the review", "paced comments",
  "/pr-post-comments", and as the posting step of pr-verify-review and
  pr-address-review. Works on any GitHub repo with gh auth.
---

# Post PR Comments

Findings already exist. This skill is only about getting them onto the PR:
correctly tagged, in a human voice, deduped, and paced.

The driver lives next to this file:

```bash
POST=~/.claude/skills/pr-post-comments/scripts/post_pr_comments.py  # adjust if installed elsewhere
```

## Hard rules

1. **Every inline comment carries a tag.** `[r]` `[o]` `[f]` `[c]`, first
   characters of the body. The tag is how the author knows whether they must act.
   Thread replies take no tag.
2. **Draft first. Post only on an explicit go.** Show the full set as a table plus
   bodies, wait for the user to say go. "Create the comments" is not "post the
   comments" - ask.
3. **Never post a comment the bots already made.** Fetch existing comments first.
4. **Never approve, request-changes, or merge.** This skill posts comments.
5. **Only the driver posts.** No `gh api ... -X POST`, no `gh pr comment`, no loop,
   no bulk review. Anything else skips the pacing and the lint.

## Step 1 - Read what is already on the PR

Bot reviewers get there first. Re-raising their findings makes the review look
automated and wastes the author's time.

```bash
gh api "repos/<owner>/<repo>/pulls/<PR>/comments?per_page=100" \
  --jq '.[] | "\(.id)\t\(.user.login)\t\(.path):\(.line)\t\(.body[0:120])"'
```

Drop any finding a bot (Copilot, code-quality, CodeQL) already made at the same
location. Keep a finding that *corrects* a bot, but write it as a reply on their
thread, not a fresh comment. Include your own comments from earlier rounds - do
not re-raise a resolved thread.

## Step 2 - Tag every finding

| Tag | Means | Test |
|---|---|---|
| `[r]` | must change before merge | would you block on it? |
| `[o]` | author may take or skip | you'd accept either answer |
| `[f]` | follow-up PR or ticket | real, but not this PR's job |
| `[c]` | question, no action | you want to understand, not change |

Post every finding in one round; the tags already say what blocks. Split rounds
only when the PR misses its own acceptance criteria (post the `[r]` set and stop)
or a `[r]` redesign would make the line-level comments pointless.

## Step 3 - Voice

If the user has a personal voice skill installed (for example `voice-of-er`),
load it and run every body through it. Either way, these rules apply, and the
driver's `--check` enforces the mechanical ones:

- Lead with the finding. No "I noticed that", no "It appears that".
- Contractions. Fragments where a fragment is how you'd say it.
- Uneven paragraphs. Never three sentences of the same length in a row.
- Name the file, the function, the number. "`execute_tool` builds deps with db,
  storage, mission_id... no sandbox" beats "the dependency dict is incomplete".
- Refer to the code, never the author. Never "you wrote", "your function".
- No process narration. Nobody needs "I checked the base branch and found".
- Length follows the finding. A one-line gap gets one line.

Enforced by `--check` (code spans exempt): no em or en dashes; no sentence opening
with So / Okay / Well / Yeah; none of furthermore, moreover, additionally,
consequently, utilize, facilitate, robust, seamless, synergy, deep dive, circle
back, touch base, nuanced, that said, it's important to note, in terms of,
"I checked / verified".

## Step 4 - Derive line numbers

Anchors are **new-file** line numbers, right side of the diff. Verify against the
real file rather than counting diff output by hand:

```bash
git show <head-sha>:<path> | rg -n "<the symbol you are anchoring to>"
```

A comment on the wrong line is worse than no comment - it sends the author hunting.

## Step 5 - Build the comments file

A JSON list in the scratchpad, one object per comment, in posting order. Build it
with python or `jq -n --arg` so quoting, backticks and newlines survive:

```json
[{"path": "app/a.py", "line": 28, "body": "[r] ..."},
 {"path": "app/a.py", "start_line": 40, "line": 44, "body": "[o] ..."},
 {"in_reply_to": 3992873113, "body": "..."},
 {"body": "PR-level note"}]
```

`in_reply_to` is the `databaseId` of the thread's first comment. Inline entries
need the head SHA as `--commit`. Dry-run first:

```bash
SHA=$(gh api repos/<owner>/<repo>/pulls/<PR> --jq '.head.sha')
python3 "$POST" <owner>/<repo> <PR> comments.json --commit "$SHA" --check
```

One failing body stops the whole batch, so fix it and re-check.

## Step 6 - Post paced

The same command without `--check`, as a background Bash task
(`run_in_background: true`).

A flat interval is its own tell. Nobody spends the same minute on a two-line nit
and on a four-paragraph architecture finding, so the driver waits before each
comment as long as writing it would take: 15-35 s of reading plus a second per
six characters, swung +/-25%, capped near 260 s. A 120-char `[o]` waits 30-60 s,
a 400-char finding 65-120 s. Nine mixed comments come out around 12-16 minutes.

The clock counts from the last post of any run (`~/.claude/state`, override with
`PR_COMMENTS_STATE_DIR`), and a lock there keeps two runs from interleaving.

## Step 7 - Verify and report

Read the log, confirm one `html_url` per entry, report what landed and what did
not. If the run was killed midway, say exactly which numbers posted.

Stop a run: `pkill -f post_pr_comments.py`, confirm with `pgrep -f post_pr_comments.py`.

Fix a body after posting:

```bash
gh api repos/<owner>/<repo>/pulls/comments/<comment_id> -X PATCH -f body='...'
```

A 404 there means the comment is gone, or `gh` is logged in as an account without
access. Check `gh api user --jq .login` before assuming anything else.

## Boundaries

- Comments only. No approve, no request-changes, no merge, no push.
- Do not invent findings to round out a set.
- A `[c]` about the PR as a whole belongs in a PR-level comment, not inline.
- Max 3 code snippets across a round. Past that, describe the change in prose.
