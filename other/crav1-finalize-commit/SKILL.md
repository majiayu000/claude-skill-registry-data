---
name: crav1-finalize-commit
description: >-
  Finalize a commit: style.md vs git log first if needed, then draft GitKraken
  Summary and Description, then offer git commit first, then copy / edit /
  rewrite / stop. Wording is shown before those choices. Use when they want
  to change the message or actually create the commit, or /crav1-finalize-commit.
  Does not push. Does not commit until they pick commit. Paste-only:
  /crav1-draft-commit-message. Keeps a trailing work-item mention through the
  HEAD check and the Cursor attribution strip.
disable-model-invocation: true
icon: git-branch
color: green
---

# Finalize commit

You wrap **`crav1-draft-commit-message`**. First produce the same Summary and Description. Then keep those two fields in play until they pick **commit**, **copy**, or **stop**.

Command: `/crav1-finalize-commit`.

Order: (1) style menu if no persist rule, (2) generate and show Summary/Description, (3) then the choices with **`commit` first** (top of the questions tool), then copy / edit / rewrite / stop. Never put those choices before the wording exists.

Paste-only (no copy/edit/commit choices): tell them `/crav1-draft-commit-message` instead, or they can pick `copy` here.

## Draft (same as the other skill)

Follow skill **`crav1-draft-commit-message`** in full for the first draft (drop-in: `.claude/skills/crav1-draft-commit-message/SKILL.md`; plugin: sibling `skills/crav1-draft-commit-message/SKILL.md`):

- Style menu or persist rule (`once` / `onward` / `log-once` / `log-onward`)
- Inspect staged first, else unstaged
- Output the **Summary** and **Description** paste blocks
- Work-item mention, when [references/work-item-mention.md](../crav1-draft-commit-message/references/work-item-mention.md) resolves one (plugin: sibling `skills/crav1-draft-commit-message/references/work-item-mention.md`): one blank line, then that mention as the **last line** of the Description. Subject stays as drafted.

Do **not** run `git commit` in that step. Do **not** skip the paste blocks — they stay GitKraken-copyable on every turn. The mention is inside the Description fence, so a GitKraken paste includes it. A work-item hint stays after the fences.

Remember the intended file set (the paths the message describes). Warn if `agent-tools/` or build output is in that set.

## After every new wording (first draft, edit, or rewrite)

They choose **after** the message exists, not before.

**Do not** open copy/edit/commit choices in the same turn as the style.md vs git-log menu. If style is needed, that turn is style only: no draft, no finalize choices.

On the turn that produces wording:

1. Finish the draft (git inspect, style already chosen).
2. Write the **Summary** and **Description** paste blocks into the user-visible reply. This is required. Do not skip it.
3. **Then** offer the choices (questions tool when available). Put the **actual Summary and Description** in the question prompt so the choice UI still shows the generated text, for example:

   `Summary: <one line>`

   `Description:` (the body, including the trailing work-item line when the draft has one)

   `What next?`

   Options, **in this order**: `commit` / `copy` / `edit` / `rewrite` / `stop`. **`commit` is always the first/top option** in the questions tool and in any bullet list.

Never call the questions tool (or any blocking choice UI) **before** step 2. Never call it as the first action of a draft turn. Draft first, choices last. Do not `git commit` until they pick `commit`.

| Id | Choice | What it does |
| --- | --- | --- |
| `commit` | Create the git commit | Use the **current** Summary + Description. See below. **Always list this first.** |
| `copy` | Copy for GitKraken | Done. Same outcome as `/crav1-draft-commit-message`. They paste Summary/Description. No `git commit`. |
| `edit` | Change the text | They say what to change (summary, description, or both). Apply **only** those edits. Keep the same style source. Show the new blocks, **then** the same choices again (`commit` still first). |
| `rewrite` | New draft from the diff | Run the draft skill’s draft step again on the **same** file set and style source. Discard the previous wording. Show the new blocks, **then** the same choices again (`commit` still first). |
| `stop` | Abort | No commit. They can still copy the last blocks. |

If they named `copy`/`edit`/`commit` **before** any wording exists, ignore it, draft, show blocks, then offer choices.

Do not invent extra options (push, amend, commit subsets they did not name). If they ask to push after a successful commit, that is a **new** request — only then `git push`. If they want a pull request, that is `/crav1-open-pr` in a later turn. Do not open it here.

## When they pick `edit`

- If they paste a full new Summary and/or Description, use that text (cleanup only: no Conventional Commits unless the style source is git log that already uses them). Their pasted Description replaces the body, including its last line.
- If they give notes (“shorter summary”, “mention verify.md”), rewrite just those parts. Keep the trailing work-item mention as the last line of the Description unless the note changes or removes it.
- Ask which field if it is unclear.
- Then show the new paste blocks and **then** the same choices again (`commit` still first). Never commit in the same turn as `edit` unless they also said `commit` **after** seeing the new blocks.

## When they pick `commit`

1. Confirm git works (same PATH fallback as the draft skill).
2. **Files:** commit **staged** files if the index is non-empty. If the index is empty, ask whether to `git add` the intended file set from the draft. Do not add `agent-tools/`, `artifacts/`, `bin/`, `obj/`, or other build output.
3. **Message:** `git commit` with Summary as the subject (`-m`) and Description as the body (second `-m`, or a HEREDOC). The body is the Description paste, including a trailing work-item mention when the draft has one. Do not add `Co-authored-by`, `Made-with: Cursor`, or other trailers yourself. Do not drop the mention line.
4. Do **not** push.
5. Read `git log -1 --format=%B`. Compare to the drafted Summary + Description. The mention, when the draft has one, is the last line of that Description. A last line of `#<id>` or `AB#<id>` is the work-item mention, not Cursor attribution.
6. Show the new hash, subject, and `git status` short result.
7. If the body has extra **Cursor attribution** (`Co-authored-by: Cursor`, `cursoragent@cursor.com`, `Made-with: Cursor`) that was **not** in the draft: this is Cursor’s commit-attribution setting (or a cloud agent), **not** this skill and usually **not** a repo hook. Follow **Cursor attribution** below.
8. After the commit message is settled (including a one-time attribution strip), one optional line and nothing more: Next (optional): `/crav1-open-pr` when you want to push and open the PR. Do not run that skill in this turn.
9. If commit fails (hooks, empty index, identity), show the error. Keep the paste blocks, **then** offer the choices again (`commit` still first). Do not name `/crav1-open-pr` on a failed commit.

Do not `git commit --amend` for wording tweaks unless they asked. Amending **only** to restore the drafted message (strip attribution) is allowed as below.

## Cursor attribution

After a successful commit, if HEAD’s message is the draft **plus** a Cursor co-author/trailer:

1. Tell them in one short sentence: Cursor appended it; it was not part of the message they accepted.
2. **Strip it once** when all of these are true: this process created HEAD, HEAD is not pushed, they have not asked to keep the trailer.
   - `git commit --amend --no-verify` with **exactly** the drafted Summary + Description (same `-m` / HEREDOC as the original commit). No extra trailers. When the Description ends with the work-item mention, that line stays the last line of the amended message.
   - Read `git log -1 --format=%B` again. If the trailer is gone, show the clean hash/message, then the optional `/crav1-open-pr` line from the commit steps. Do not amend again.
   - If the trailer **came back**, Cursor wrapped `git commit` again. Do not loop amend. Offer `strip` (they should turn attribution off first) or `keep`.
3. How to stop it on **future local** commits: Cursor Settings → **Git & PRs → Attribution** (older: **Agent → Attribution**) → turn commit attribution off. CLI: `attribution.attributeCommitsToAgent` false in `~/.cursor/cli-config.json`. Enterprise admins can disable it org-wide. **Cloud / background agents** may still add co-author; the IDE toggle does not always apply there.
4. Do not install a `prepare-commit-msg` hook unless they ask.

If they say they **want** the Cursor trailer, leave it.

## Hard rules

- Never offer commit/copy/edit before Summary/Description exist. After they exist, show the blocks, then the choices with **`commit` first**. The question prompt includes that wording.
- No commit until `commit` (or an unambiguous “commit this message now”) **after** they have seen the current blocks.
- `copy` never runs `git commit`.
- After `commit`, if Cursor appended `Co-authored-by` / `Made-with` that was not in the draft, strip it once with amend when HEAD is ours and unpushed; do not fight a second inject—tell them to turn Attribution off. The amend keeps the drafted Description, including a trailing work-item mention.
- Do not install a hook to enforce the work-item line. Do not block the commit when `work-item.md` is missing.
- Do not change product files except the persist rules the draft skill already writes. Cursor: `.claude/rules/draft-commit-style.md` or `.claude/rules/draft-commit-gitlog.md`. Claude Code project: `.claude/rules/draft-commit-style.md` or `.claude/rules/draft-commit-gitlog.md`. Claude Code user: `~/.claude/rules/draft-commit-style.md` or `~/.claude/rules/draft-commit-gitlog.md`.
- Do not open a PR. After a successful commit, one optional line may name `/crav1-open-pr`. Do not invoke it.
