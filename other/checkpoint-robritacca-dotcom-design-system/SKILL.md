---
name: checkpoint
description: Save work in progress to a remote branch and keep working. Never touches main and never deploys; if invoked on main it moves the work to a new branch first. Use when asked to checkpoint, save progress, back this up, or push to the branch.
icon: save
displayDescription: "Saves work in progress to a remote branch as a safety net, then stays on that branch so work continues. It never touches main and never deploys: if invoked on main it moves the work to a new branch first, because pushing main publishes the site. A quick lint runs before the push and failures are flagged without blocking the backup."
invoke: ["checkpoint","save my progress","back this up","push to the branch"]
---

# checkpoint

Save the session's work-in-progress to a remote branch, then keep working on it. Nothing merges, nothing deploys, `main` is never touched. The end state: the work is safely on GitHub and the session stays on the branch.

## When invoked

Use this skill when asked to save unfinished work — phrases like "checkpoint", "save my progress", "back this up", "push to the branch". When the work is finished and should go live, that's `ship`; to save and *stop* working on it, that's `park`.

**If asked to "merge and push"**: that's the retired ambiguous skill name, and it now maps onto more than one verb. Confirm the intended end state before doing anything: `ship` (merge into `main`, push, deploy), `checkpoint` (push the branch, keep working), or `land` (combine several pieces of pending work into a local `main`, pushing nothing).

## Instructions

1. **Check the branch**: `git branch --show-current`.
   - **On a work branch**: commit and push there (steps 2–5).
   - **On `main`**: move the work to a branch first — there is no "push to main but don't deploy", because a push to `main` publishes robertritacca.com. Create a branch named for the work, not the date: `git checkout -b wip/<short-topic>` (e.g. `wip/nav-search`, `wip/chart-tokens`). Uncommitted changes ride along automatically. Never commit directly to `main` from this skill.

2. **Survey the tree**: run `git status --short` and classify every entry as in scope (this session's work) or out of scope (predates the session or wasn't part of the requested work). **Never run `git add -A`, `git add .`, or `git add` on a directory** — always add explicit file paths. Out-of-scope files stay out and are named in the report.

3. **Quick check, not the full verify**: run `npm run lint`; if the session touched `website/`, also run `npm --prefix website run lint` (root ESLint ignores the website workspace, so the root lint alone carries no signal about website work). This is a backup, not a release — the full `verify` (several minutes) is `ship`'s job. **A lint failure does not block the push**: the whole point is that the work is saved even mid-mess. But flag any failure loudly in the report so it isn't a surprise at ship time.

4. **Commit in the repo's conventional style** (`feat(scope):`, `fix(scope):`, `chore(scope):`, with a short why in the body) — checkpoint commits eventually reach `main` through a merge, so they are real history, not throwaways. One commit is fine if the work is one concern; split if it's clearly several.

5. **Push the branch**: `git push -u origin <branch>` (same-named remote branch). Pushing a branch publishes nothing — no deploy, no site change.

6. **Stay on the branch** and report:
   - The branch name and each commit (hash + subject)
   - Lint status, including any failure being flagged rather than fixed
   - Every file deliberately left out and why
   - The closing line: work is backed up, session continues on the branch; say `ship` when it should go live, `park` to set it aside

## Guardrails

- Never touch `main`: no commits to it, no merges into it, no pushes of it
- Never force-push, never rewrite pushed history
- Never commit `ga-analysis/output/`, `ga-analysis/service-account.json`, `.env*`, or anything credential-shaped — even if explicitly staged by mistake
- If there is nothing in scope to commit, say so and stop — don't invent a commit
- Never chain into `ship` automatically — going live is always a separate, explicit ask
