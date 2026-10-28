---
name: fix-github-issues
description: Verify, triage, fix, and close review-bot GitHub issues one finding at a time.
disable-model-invocation: true
argument-hint: "Optional issue numbers or a label (defaults to the project's review-bot label, else ai-review)"
allowed-tools: "Bash(gh issue view *) Bash(gh issue list *) Bash(gh issue comment *) Bash(gh issue close *) Bash(gh api repos/{owner}/{repo}/issues/*)"
---

# Fix GitHub Issues

Work the open issues that a review bot filed. Each issue is a **container of findings**:
some are legit, some stale, some wrong. Every finding earns its own verdict from the
code on the default branch, never from the issue's headline. An issue closes only when
no legit finding is left in it, and a fix counts only once it reaches the default branch.

**Project context.** Read `.agents/github-review.md` when the repo has one. Its
sections `## Review bots` (with the bot's issue label), `## Auto-dismiss`,
`## Never dismiss`, and `## Stack facts` (what the bots get wrong) hold this repo's
facts; a missing section means the default here. Then follow the repo's `AGENTS.md` /
`CLAUDE.md` rules for tests, lint, cache clears, and a dirty tree.

## 1. Build the working set

Find the default branch (written `<default>` below), run `git fetch origin`, and
verify everything against `origin/<default>`, not a local branch. List every open issue
with the bot label (or the ones the user named), newest first. The calls, and the
check that the list is not cut off at its limit, are in [`references/mechanics.md`](references/mechanics.md).

Walk order is newest to oldest, but let evidence reorder it. A newer diff that
introduced a defect an older issue already flagged makes the older finding LEGIT, and
you fix both in one commit chain. A newer commit that fixed an older finding makes that
finding STALE: cite the sha.

Completion criterion: every open issue in scope is listed, newest first, with fewer
issues than the limit.

## 2. Classify every finding

For each issue, read its body and every comment (note any "fixed in <sha>" or "false
positive" from earlier runs). Read the commits it reviewed. Then write one line per
finding:

```
Finding N: [STALE | AUTO-DISMISS | HALLUCINATION | LEGIT] — <one-line evidence>
```

- `Finding 1: STALE — fixed in bf707fde3, see app/Foo.php:42`
- `Finding 3: HALLUCINATION — rg 'BarPolicy::class' returns 0; symbol does not exist`
- `Finding 4: LEGIT — app/Auth.php:88 still uses < instead of <=, exploitable on token boundary`

Verification rules:

- For a "class, method, or permission missing" claim, `rg` the symbol where the finding
  says it is missing (that file, call site, or test). If it is there, the finding is
  HALLUCINATION. That it exists somewhere else does not refute a missing check.
- For an "X may break Y" claim, trace the real call sites. If nothing calls it, the
  finding is STALE or HALLUCINATION.
- A finding whose file:line does not exist at the reviewed commit, or does not hold the
  code it describes, is HALLUCINATION. A finding on a file the commit did not touch
  stands when the change reaches it (a changed caller that breaks an unchanged callee);
  only when nothing in the commit leads there is it HALLUCINATION.
- A documented design choice in the commit body that contradicts the finding is
  AUTO-DISMISS.
- A finding whose body retracts itself ("this technically works", "disregard") is
  AUTO-DISMISS.

**Delegate the legwork on a large set.** With more than 5 findings, hand the first pass
to read-only workers in batches of about 10. Each brief carries the batch (id, author,
reviewed commit, file:line, body), the ref `origin/<default>`, the line format above,
and the verification rules. In Claude Code with this plugin installed, dispatch
`subagent_type=leek-skills:finding-verifier` for each batch in parallel; it keeps the
bots' recurring false premises in project memory, under this repo's `.claude/`.
Elsewhere, use any read-only sub-agent on a cheaper model, or classify inline when the
harness has none. Then re-verify yourself every line that came back LEGIT or UNSURE.
You read that code for the fix anyway.

**Second pass.** Re-read every LEGIT against the project's auto-dismiss list and
downgrade any match. A category on the project's never-dismiss list stays LEGIT. Do this
before writing any code.

Completion criterion: every finding in the working set has a line, and the second pass is done.

## 3. Fix the legit ones

Work on a new branch `fix/issues-<run>` from `origin/<default>`, always in a worktree
([Branch or worktree](references/mechanics.md#branch-or-worktree)). The main checkout
stays on the branch the run found it on, including when that tree is clean.

Per LEGIT finding: make the minimal change, with no drive-by refactors. Add a test for
logic, auth, or data changes and run that test file green. A user message to stop the
tests ends test commands for the rest of the run: the last focused result stands, and
the commits continue. Commit each fix on its own (Conventional
Commits, explicit staging). Put `fixes #NNN` **only** on the commit that resolves the
issue's last legit finding, so the issue closes at the right moment.

Run that test file against the repo's configured test database when you can. A run that needs
its own database names and registers it by [Scratch databases](references/mechanics.md#scratch-databases).

A LEGIT finding you cannot fix (a secret rotation, infra, a human decision) keeps the
issue OPEN; step 5 names the blocker.

Completion criterion: every fixable LEGIT finding has a commit on `fix/issues-<run>`,
with a green test where it needs one, and every unfixable one is named.

## 4. Land the fixes

An issue closes only when its `fixes #NNN` commit reaches `<default>`, so a local
commit fixes nothing yet. Show the user the commits and the issues each one closes, say
where they will go, and land them without asking: push to `<default>` by default; open a
pull request instead when branch protection or the repo's rules forbid direct pushes. A
user instruction in the input or the conversation ("open a PR", "keep them local")
overrides both. The commands are in [Land](references/mechanics.md#land).

Once they are landed, the main checkout is still the branch recorded at the start
([The checkout stays](references/mechanics.md#the-checkout-stays)). The fix branch
stays in its worktree. Do the same check if the run stops early.

Completion criterion: the commits are on `<default>`, in an open pull request, or kept
local by the user's instruction, and `git branch --show-current` in the main checkout
is still the starting branch.

## 5. Post a disposition

Post one comment per issue in the working set, with one bullet per finding
(calls in [Disposition and close](references/mechanics.md#disposition-and-close)):

```
- Finding 1 (X): fixed in <sha>
- Finding 2 (Y): stale — superseded by <sha>
- Finding 3 (Z): auto-dismiss — <category>
- Finding 4 (W): hallucination — symbol does not exist at claimed location
```

- Fixed on `<default>`: the push closed it; post the comment after.
- Nothing legit: post the comment, then close the issue.
- Fix in an open pull request or kept local: the issue stays open; the comment says where
  the fix is.
- A LEGIT finding you cannot fix: the issue stays open; the comment names the blocker.

If you later find a misclassified finding, reopen the issue with a correction note.

Completion criterion: every issue has its comment, and `gh issue view N --json state`
agrees with it.

## 6. Clean up

Remove nothing before this step. Then remove without asking every worktree and database
you created whose fixes are on `<default>` (or nothing was fixed in it), and list each
removal in the report ([Clean up](references/mechanics.md#clean-up)). A worktree git
refuses to remove without `--force` holds unsaved work: keep it.

Ask once only about what is left that you created: a refused worktree, and one whose
fixes are in an open pull request or kept local (`AskUserQuestion` where available: a
`multiSelect: true` question with one option per item, nothing pre-ticked, at most 4 per
question and further questions for the rest; otherwise a plain question in chat: "Can I
delete these too?"). Remove only what the answer selects, never with `--force`. What
stays stays registered, for `repository-cleanup`. Skip the question when nothing is left.

Completion criterion: everything removable is removed, any question is answered, or you
created nothing. Report the tally:
fixed, stale, auto-dismiss, hallucination, and blocked. Name each fix not yet on
`<default>`, and each worktree or database kept. Mark the blocked count and each kept
item ⚠️; no other marks.
