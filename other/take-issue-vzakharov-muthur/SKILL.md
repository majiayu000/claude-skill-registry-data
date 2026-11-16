---
description: Take a GitHub issue onto the branch — export the thread and its attachments, commit them, and hand the number back to whoever called. Invoke as `/take-issue <number|url>`; its callers are `/task`, `/plan` and `/go`, each running it first when the prompt carries a `#<N>`.
---

End state of this skill: `docs/issue/<n>/` holds the thread and its attachments,
that export is committed on the branch, you have read it, and control is back
with the caller — which is where every decision about the work is made.

This skill decides nothing. It is the one place an issue gets pulled onto a
branch, so its contract to its callers is that the issue has been **taken**:
exported, committed, and there for a later session to re-read.

## Argument shape

The argument is an issue number or a full issue URL, optionally with prose
around it — `fix the sidebar scroll #847` is the same invocation as `847`. The
prose is the operator's own summary of the issue and is worth reading as a hint
at what they care about, but **the export outranks it**: where the two disagree,
the thread is what the work is against.

## Step 0 — Mode gate: native plan mode is not supported

If the session is in **native plan mode** — the launch banner or system prompt
says so, `ExitPlanMode` is the offered exit, or an edit is refused for that
reason — **stop before running anything below.** Tell the operator:

- this flow is plan-**file**-based (`@.claude/skills/plan/SKILL.md`), and native
  plan mode cannot write the two artifacts it depends on: the export under
  `docs/issue/<n>/` and the plan under `docs/plans/`. Both must be committed and
  pushed, because the operator reviews from a different machine than the one you
  run on;
- the plan-mode approval UI is unreliable in web sessions regardless
  (anthropics/claude-code#72704);
- so switch to **accept-edits** or **auto** and send any reply — the run picks
  up from there; no re-invocation needed.

Do not work around it, and do not fall back to a chat-only plan.

## Step 1 — Export the issue locally (then read the export)

**Look under `docs/issue/<n>/` before running anything: the export is normally
already there.** `.claude/hooks/prompt-issue-export.sh` runs this step's command
ahead of a session's first turn when that prompt _ends_ in `#<N>`, and names
what it wrote in that turn's context — so where the export exists, this step is
the reading below and nothing else. Run the command when it is absent: a number
that reached you any other way, a hook that reported a failure, or a tree that
adopted `/take-issue` without the hook.

**First command:** run the bundled exporter:

```bash
python3 scripts/export-github-item.py <issue-number|https://github.com/OWNER/REPO/issues/N> [--repo OWNER/REPO]
```

The script writes `docs/issue/<n>/issue.md` (body + comments + timeline) and
downloads any image / file attachments referenced in the thread to
`docs/issue/<n>/attachments/`.

Consult the issue only through the export — never `gh issue view`, the GitHub
MCP tools, or `WebFetch` in its place. `gh issue view` alone does **not** fetch
attachments: GitHub's `private-user-images.githubusercontent.com` URLs require
an authenticated request even when the issue is public, which is why the export
script exists. `WebFetch` on a github.com issue page often fails outright in
isolated environments. For a quick metadata check unrelated to the task at hand
— labels, assignees, linked PRs —
`gh issue view <n> --json title,body,labels,assignees,state,url` is still fine.

**Then read** `docs/issue/<n>/issue.md` end to end, and **open the files under**
`docs/issue/<n>/attachments/` when you need pixels (screenshots, mockups, design
references).

**Auth:** the script reads `$GH_TOKEN` (or `$GITHUB_TOKEN`) first, then falls
back to `gh auth token`. One of those must be available. **Deps:** stdlib Python
3.9+ only — no `pip install` needed.

**Repo:** if `--repo OWNER/REPO` is omitted and the argument isn't a full issue
URL, the script reads `origin` from the current git checkout. Pass `--repo`
explicitly when exporting an issue from a different repo than the one you're
working in.

If the export fails, **stop and report** — do not start solving the task from
the title alone. Tell the user what failed and how to proceed. The script exits
non-zero on every failure — auth, network, repo not found, or an attachment that
wouldn't download — so check the status, not just the last line. A partial
attachment failure still writes the Markdown and prints
`Downloaded 2/3 attachment(s)` plus each URL it missed: the thread is there, but
you'd be reading it with pixels missing.

### Attachments with no extension

The filename stem is the asset id, so an attachment's type is not readable off
its name — `file docs/issue/<n>/attachments/*` before deciding what to open. An
image you read directly. **A video** (e.g. `ISO Media, Apple QuickTime movie`)
you cannot play: load `@.claude/skills/take-issue/video-frames.md`, which
extracts frames you can read as images.

## Step 2 — Commit the export

```bash
git add docs/issue/<n> && git commit -m "docs: #<n> export the issue"
```

Commit it **now**, before any planning. The export is the source of truth for
what the issue says, so an agent resuming this branch — after a context wipe, a
handoff, or in a parallel session — re-reads the thread instead of re-exporting
it, and committing it up front means that holds even if the session dies
mid-plan. Never commit it on the trunk or a promotion branch.

`@.claude/skills/finalize/SKILL.md` deletes the whole `docs/issue/` tree in the
last commit before `gh pr ready`, so this add and that delete cancel out in the
squash. **You** must not delete it.

## Step 3 — Return to the caller

Hand back the export path (`docs/issue/<n>/issue.md`) and the number. **Whether
it is the number a PR closes is the caller's to decide**, and often it isn't
one: an issue taken for context — a related report, the thread a decision was
argued in, the parent of a carve — is read and closes nothing. Where the caller
carves, `@.claude/skills/plan/carving.md` settles which number the PR closes.

Then stop. Everything downstream belongs to the caller.
