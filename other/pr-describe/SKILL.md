---
name: pr-describe
description: >-
  Writes or updates a pull request description: a diagram-based outline with screenshots
  when the feature has a plan folder, otherwise a summary, why, how to verify, and risks.
  Use whenever a PR is opened or updated.
user-invocable: true
argument-hint: [PR number | leave blank for the current branch]
---

# Describe a pull request

`git-workflow` never writes a PR body by hand — it always runs this skill instead, for every
PR. This skill decides, every time, which of its two styles fits: a diagram-based outline for a
feature-sized change, or a plain summary for everything else.

This skill only composes the description. Branch/push/PR-creation mechanics, force-push and
secret-scanning sanity rules, and the always-ask-before-touching-main rule all stay owned by
`git-workflow` — read that skill's "Pull requests" and "Sanity rules" sections and follow them
as-is; don't restate them here.

## Workflow

1. **Check for a plan folder.** Does `docs/plans/<feature-slug>/` exist for the current branch
   (the feature-* pipeline ran for this feature)? This decides which style you write in step 4 — a
   `quick-fix` or trunk-based commit won't have one, and that's expected, not an error.

2. **Gather context.**
   - Resolve `<base>` first, using `git-workflow`'s "Resolving the base branch" (branch
     prefix, remote existence check, and the stacked-PR check). A wrong base here means the
     diff below includes commits that were never really part of this PR.
   - Plan folder found: read `BRIEF.md`, `ARCHITECTURE.md`/`SPEC.md`, and `PLAN.md` for the
     "why." Then invoke `decision-review` (via the Skill tool) — always, not only if it
     happens to have already run — and use its ranked output as-is for step 4's "Special
     things to note." The PR is the one checkpoint a fully autonomous run is guaranteed to get
     a human look at, so this step never skips it: don't fall back to reading `DECISION-LOG.md`
     by hand and don't re-derive the list yourself.
   - No plan folder: read the branch's commit messages instead — there's no separate plan
     artifact to draw on, and `decision-review` needs a plan folder to run against.
   - Either way, read the full diff against the resolved base (`git diff <base>...HEAD`, or
     `gh pr diff <number>` if a PR already exists) — enough of it, and enough surrounding code,
     to explain behavior and ownership, not just line counts.

3. **Find or create the PR.**
   - `gh pr view --json url,number,title,state,baseRefName,headRefName` on the current branch.
   - No PR yet: carry on and write the description first. Step 5 opens the PR with it, using
     `git-workflow`'s "Pull requests" section for the push, title and base branch. Don't
     duplicate those rules here.

4. **Write the description**, in the style step 1 decided. Either way, a stacked PR (step 2)
   opens with `Stacked on #<parent-pr-number>.` ahead of everything else — the template's
   placeholder for it is omitted entirely when the PR isn't stacked.
   - **Plan folder found** — use `templates/pr-description.md`:
     - **Why the change** — exactly one sentence.
     - **What it looks like** — only when the PR adds or changes backoffice UI; omit the
       whole section otherwise. In this order:
       - **Where to find it**: the click path through the backoffice to each new or changed
         screen, from its `BUILD-LOG.md` entry ("Settings › Webhooks › any webhook ›
         Deliveries tab").
       - **Who can see it**: the section, user group or permission that decides access, read
         from the manifest `conditions` and the Management API authorization policy. "Anyone
         with access to the Settings section" beats quoting the condition alias.
       - **Screenshots** from the plan folder's `screenshots/`: the built screen for a new
         one; a two-column table with `<screen>-before.png` and `<screen>.png` for a changed
         one. No screenshots on disk means no screenshots in the PR. Never stand a mockup in
         for the built screen.
       - Image links in a PR body must be full URLs: a relative path renders as a broken
         image. Use `https://github.com/<owner>/<repo>/blob/<sha>/<path>?raw=true`, with
         `<owner>/<repo>` from `gh repo view --json nameWithOwner` and `<sha>` the pushed
         commit that contains the file (`git rev-parse HEAD` after pushing). Pinning to a
         commit keeps the image working after the branch is deleted.
     - **Special things to note** — led by whatever `decision-review` flagged in step 2. Carry
       its recommended action through as a visible prefix, don't smooth it into plain prose:
       `**Needs a decision:**` or `**Consider reverting:**` for those two verdicts, no prefix
       for a plain `Looks fine as documented` item. Every `Needs a decision`/`Consider
       reverting` item from `decision-review` gets a bullet, no exceptions. After those: a
       bullet each for migrations, compatibility constraints, or other deliberate omissions
       `decision-review` wouldn't have caught — no fixed count, but every one must be something
       the reviewer genuinely needs before approving, not a restatement of the diagram below or
       the diff itself. Write `- None.` if there's nothing at all — don't pad it out.
     - **Change outline** — the smallest set of diagrams that explains the implementation. See
       `references/diagram-conventions.md` for which shape fits which kind of change and how to
       draw it. Only include a view that actually changed; skip the rest. Order them the way a
       reader would want the story told (a data structure or contract usually comes before the
       code that uses it), not in a fixed sequence.
     - Prefer a `diff` block for a change to an existing shape; show the whole thing only when
       most of it is new or the diff notation would obscure ownership or order.
   - **No plan folder** — use `templates/pr-plain.md`: Summary, Why, How to verify, Risk /
     rollback. A diagram-heavy outline on a five-line fix is noise, not help.
   - Either way, write it following `plain-writing`: one person explaining a change to
     another, plain language, no jargon that isn't already in the codebase.

5. **Save and publish.**
   - Plan folder found: save the draft to `docs/plans/<feature-slug>/PR-DESCRIPTION.md` first —
     this skill owns that file, the same way `feature-build` owns `BUILD-LOG.md`. Then
     `gh pr edit <number> --body-file docs/plans/<feature-slug>/PR-DESCRIPTION.md`.
   - No plan folder: save the draft to a temporary file outside the repo, then
     `gh pr edit <number> --body-file <that file>`.
   - No PR yet (either case): open it with `gh pr create --body-file <the saved draft>`,
     following `git-workflow`'s "Pull requests" section, instead of `gh pr edit`. Always
     `--body-file`, never `--body`.
   - Confirm the update succeeded.

6. **Report back**, briefly: the PR URL, the saved description's path (if any), and a short
   list of changed files. Nothing else — the PR itself carries the full description.

## Sanity rules

Inherited from `git-workflow`, not restated: no force-push, no `--no-verify`, re-check the diff
for secrets before it goes anywhere, and stop to ask before running `git commit`/`git merge`
straight against the default branch or a `support/*` branch.
