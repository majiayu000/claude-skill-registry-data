---
name: nickstire-shared-main-push
description: Use before any `git push` from the nickstire app while a sibling Claude session is also working on the same repo (statenour, voice, worker). Codifies the all-or-nothing shared-main protocol so you don't surprise the other session or get blocked by a state you don't own.
triggers: git push, shared main, sibling session, concurrent sessions, push protocol, nickstire push, all-or-nothing, blocked push
---

# nickstire-shared-main-push

`main` is shared between concurrent Claude sessions (nickstire, statenour,
voice, worker — all under `apps/*/`). On push, git is all-or-nothing: a
push from this session carries the OTHER sessions' committed work too.
The pre-push hook builds **both affected apps** — so the other app's
state can block this session's push, and vice-versa.

## The 5 rules (in order)

1. **`git fetch origin` FIRST, every time.** Always. Without this you
   don't know what the other session pushed since you last looked.

2. **Inspect what would ride along.** Before `git push`:
   ```bash
   git log origin/main..HEAD --oneline
   ```
   That's every commit your push will publish. If any aren't yours,
   note them — you're publishing the other session's work. Decide
   whether that's appropriate (almost always yes; they committed, they
   intended to ship).

3. **Pre-push hook builds the working tree, not the committed state.**
   `turbo run build --filter=...[$UPSTREAM]` runs on disk. If the OTHER
   session has uncommitted broken code in `apps/statenour/`, your push
   gets blocked by their working-tree build failure. This is the gate
   working as designed. Surface it to the operator with a self-contained
   prompt for that session (don't fix their code yourself unless they
   explicitly delegate).

4. **NEVER `--no-verify`.** The hook is the only thing keeping a broken
   prerender / broken build from reaching Railway. The hook message
   itself suggests `--no-verify` as a last-resort — ignore that
   suggestion unless the operator explicitly authorizes it for a
   specific commit.

5. **NEVER rewrite shared history.** No `git rebase -i` on commits the
   other session has based work on. No force-push (`-f`, `--force`,
   `--force-with-lease`) on main. Even if your own commit has a
   slightly-overstated commit message, leave it — it's local-only-
   reversible only until pushed, and once pushed, history surgery
   disrupts every other session that pulled it.

## When the push is blocked by the other session

If `git push` fails with the pre-push hook citing the OTHER app's build:

1. Identify what broke. Read the hook output for the failing target
   (e.g., `@statenour/web:build`).
2. Don't touch the broken code. The other session owns it.
3. Generate a self-contained prompt for the other session — the
   operator can paste it. Include: the error, file paths, the
   minimum-viable fix direction, and a "don't `--no-verify`" warning.
4. Wait. The other session fixes it and pushes (carrying your commit
   along), OR they tell you to retry.
5. After they fix and push, your local `git log origin/main..HEAD`
   should show in-sync (your commit went out with theirs).

## PR mechanics under concurrent sessions

1. **ALWAYS capture the PR number from the `gh pr create` output** —
   `$num = ($prUrl -split '/')[-1]` — and merge THAT. Never merge a
   guessed or remembered number: sibling sessions interleave the PR
   sequence, and on 2026-08-07 a session merged "#1411" by assumption —
   it was the sibling's already-merged PR (harmless only by luck).
2. **`gh pr merge` can fail AFTER the remote merge succeeded.** With
   `--delete-branch`, gh tries to check out `main` locally; if `main` is
   checked out in another worktree it exits 1 with
   `fatal: 'main' is already used by worktree ...` — but the squash-merge
   already landed. Before ANY retry:
   ```bash
   gh pr view <n> --json state,mergeCommit
   ```
   `MERGED` means done — just `git fetch origin main` and ff-sync.
3. **Merging to main CANCELS every open PR's in-flight checks.** Each
   merge recomputes the other PRs' `refs/pull/N/merge`, and GitHub kills
   whatever was running on the old ref. statenour's `node`/`e2e` jobs
   need ~9-11 minutes, so under parallel sessions a long check rarely
   survives to completion — and the kill presents as
   `The runner has received a shutdown signal` / `Force killed Turborepo
   tasks`, which reads as flaky infrastructure, not as merge ordering.
   Proven 2026-08-26 on #1886: killed at 4m30s minutes after one merge,
   killed again at 4m45s minutes after another, passed at 11m18s once
   main was deliberately held still (same day, #1897/#1898 failed one
   e2e lane 67s apart with identical signatures; both reruns passed).
   The rules: **hold merges while a sibling PR's long check is in
   flight**; sequence your own merge → next PR's push so each gets one
   clean CI cycle; and read a shutdown-signal kill minutes after a main
   merge as THIS before blaming infra — rerun it, don't debug it.
   Recurred 2026-09-15: merging #2340 killed #2338's and #2339's `node`
   jobs 3-7 min later; the root `AGENTS.md` merge recipe now starts with
   `gh pr list --state open` for exactly this reason. **The same
   signature with NO merge in the window** (also witnessed that day, and
   a 50-min job timeout after a run measured 232 MB free) is runner
   resource death during `@statenour/web#build` + `#check` in parallel —
   rerun once; if it recurs, the lever is `--concurrency=1` in
   `.github/workflows/test.yml`, never a code hunt.

4. **The reviewed SHA must equal the head you merge.** (a) Mark the PR
   ready-for-review when you OPEN it, not when you merge: `chatgpt-codex-connector`
   fires on draft-to-ready (about 4 min) while the sweep takes about 13, so
   un-drafting at merge time landed the review after the squash on 3 of 3
   merges (#2359, #2362, #2364, 2026-09-16, under 15 s each). (b) After ANY push
   that moves the head, comment `@codex review`: the reviewer does not fire on
   pushes (verified on #2370). Before merging, compare the reviewed commit in
   the review summary with the PR head; if they differ, nothing looked at it.

## A red gate whose own log says "unmodified tree" is main's condition, not yours

Minutes after a merge, every sibling PR (including a docs-only one) can show
the SAME gate red — witnessed with `knip orphan gate` immediately after
#2220 merged: the gate's own control step printed "reports failure on an
unmodified tree" and named three exports from #2220's files, none in the new
diffs. Without reading that control-step message, three unrelated PRs read
as three new regressions. Confirm the listed orphans are outside your diff
(a docs-only PR showing the identical red is the cleanest proof), disclose it
on the PR, spawn the fix as its own task, and do not absorb it into your own
change.

## Local Windows path note

The repo lives at `C:\Users\nourd\NOURCITY\` (in bash:
`/c/Users/nourd/NOURCITY/`). The `nickstire-repo-staging` path that
appears in older memory entries is a Windows junction that doesn't
always resolve under bash — use the real path.

## Real-session example

In 2026-05-22, a statenour session pushed `d7849454` ("tRPC migration —
scattered components slice") that introduced a Next.js prerender break
on `/brain/health` and `/system/features` (tRPC hooks called at build-
time export, no Context). This blocked nickstire's verified
`511755ce` (admin bug fixes). Recovery: surfaced a self-contained
prompt to the statenour session; they shipped `29e48302` (command-
palette prerender) and subsequent fixes; their next `git push` carried
nickstire's commit out cleanly. Total elapsed: ~20 min.
