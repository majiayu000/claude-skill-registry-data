---
name: review-agent-feedback
description: "Use when an existing GitHub pull request or GitLab merge request already carries review comments from an automated reviewer — Kody/Kodus, CodeRabbit, Copilot, Gemini Code Assist, PR Review, or any other bot — and the user wants those threads validated against the real code, answered in-thread, rated with 👍/👎, and resolved: '봇 리뷰 검증해줘', 'Kody 코멘트 답글', 'CodeRabbit 지적 맞는지 확인', '리뷰 스레드 정리/resolve', 'reply to the bot review', 'review feedback triage'. Not for writing a new review (pr-review), an uncommitted local diff (code-review), or human reviewer feedback inside an issueops cycle (issueops review-feedback)."
---

# Review Agent Feedback

**A bot's finding is a claim, not a fact — and a reply is not a resolution.** Every
automated review thread gets one verdict grounded in the code as it exists at the
PR/MR head, one in-thread reply that states that verdict with evidence, one reaction
the reviewer can learn from, and one resolution — then the thread is re-read and the
report says what the remote actually shows.

Works on GitHub (`gh`) and GitLab (`glab`), self-hosted included; provider is
auto-detected from `origin` or the URL. Canonical location:
`issueops/skills/review-agent-feedback` (home skill paths are symlinks installed
by `issueops update`). `agents/openai.yaml` exposes it as `$review-agent-feedback`
on Codex. Call the script as `<skill>/scripts/review_threads.py`, where `<skill>` is
this directory.

## Pipeline

```
1 List     review_threads.py list   → bot threads, normalised, with already_handled
2 Verify   you, per thread          → verdict + evidence (code, diff, tests, rules)
3 Plan     plan.json                → verdict / reply / reaction / resolve per thread
4 Apply    review_threads.py apply --dry-run, then apply → verified ledger
5 Report   ledger table             → what the remote shows, not what was sent
```

### 1. List

```bash
out=<repo>/.issueops/issues/<issue-number>/review/<provider>-<number>; mkdir -p "$out"   # no linked issue: <repo>/.issueops/tmp/review-agent-feedback/<number>
python3 <skill>/scripts/review_threads.py list --pr <number|!n|#n|URL> --repo-dir <repo> > "$out/threads.json"
```

`threads.json`, `plan.json`, and the ledger live under that `$out` — the per-issue
artifact folder's ignored `review/` area (same rule as `pr-review`); they are working files,
not commits. The issue number comes from the PR/MR body's issue link or the IssueOps record.

Read `threads.json`. It contains only bot-authored threads (`--all` adds humans);
each has `reviewer`, `mention`, `resolvable`, `resolved`, `path`, `line`,
`already_handled`. Skip threads whose `already_handled` equals the verdict you would
give now — they were finished by an earlier run. Threads with `resolvable: false`
(summary / status notes) are not part of the job unless the user names them. If
`state` is not open, say so before doing anything. If the list is empty after those
filters, report "처리할 봇 스레드 없음" with the counts and stop.

With a full URL, `--repo-dir` is only needed for the verify step (a clone at the
PR/MR head); provider, host, and project come from the URL. With a bare number the
`origin` remote of `--repo-dir` decides them.

For GitLab hosts whose token lives in a profile-scoped MCP server rather than the
CLI, reproduce the calls in `references/providers.md` through that `glab_api` tool —
the paths and fields are identical; the `gitlab-usecase` skill governs profile choice.

### 2. Verify (you)

For every thread, before writing a word of reply:

- Open the file at the PR/MR head (`git fetch` + checkout or `git show <head_sha>:<path>`),
  not the diff hunk alone; follow the symbol one hop upstream (where the value is
  produced/validated) and one hop downstream (where it is consumed).
- Decide whether the change under review introduced the issue or it is pre-existing
  (`git blame`/base branch), and whether a cited project rule really names it.
- Run the fastest relevant check when the claim is about behaviour (the test, a
  typecheck, a reproduction). Where the claim cannot be checked, the verdict is
  `hold`, not `valid`.
- Verdict: `valid` · `partial` · `invalid` · `out_of_scope` · `hold`
  (definitions and default reaction/resolve in `references/providers.md`).

### 3. Plan

Write `plan.json` (schema in the script docstring). Each reply is Korean prose in this
shape; the script prepends the reviewer's mention and appends the idempotency marker:

```md
**판정: 타당** (또는 부분 타당 / 타당하지 않음 / 범위 밖 / 보류)

근거: <파일:라인 · 호출 경로 · 명령 결과>. <봇의 전제 중 맞는 것/틀린 것>.

조치: <적용한 수정과 커밋 · 별도 이슈 · 현재 코드가 안전한 이유 · 보류 사유>
```

Identifiers, paths, and commands stay verbatim; never quote secret values. A reply
must contain the evidence that decided the verdict — "확인했습니다" alone is not a reply.

Before posting `plan.json`, invoke the `fluent-korean` skill and apply it to every
`reply`. These replies are published to a remote thread a human reads, so the polish
pass is a precondition for posting, not an option.

Rules for the plan:

- `hold` threads (waiting on a human, a follow-up promised in this PR/MR that is not
  pushed yet, or the user said leave it open) keep `resolve: false` and a
  `reason_open`; every other verdict resolves, whether accepted or rejected.
- Reaction rates the finding's usefulness for **this** change: 👍 correct and
  actionable here, 👎 false, misleading, over-severe, or not actionable here.
- The user's overrides ("resolve 하지 마", "반응 달지 마") go into `reaction`/`resolve`
  fields, not into skipped steps.

### 4. Apply

```bash
python3 <skill>/scripts/review_threads.py apply --pr <ref> --repo-dir <repo> --plan plan.json --dry-run   # preview reply bodies and planned actions
python3 <skill>/scripts/review_threads.py apply --pr <ref> --repo-dir <repo> --plan plan.json             # post, react, resolve, then re-read
```

The script replies to the original thread, adds the reaction on the reviewer's note,
resolves the thread, then re-fetches it and marks each row `ok`, `unverified`, or
`error`. It never duplicates a reply or reaction on re-run and refuses to resolve
`resolvable: false` threads. Single primitives (`reply`, `react`, `resolve`,
`unresolve`, `verify`) exist for partial redo.

### 5. Report

Present the ledger as a table — one row per thread: file:line · reviewer · verdict ·
reply id · reaction · resolved (and `reason_open` when not) · status. A row that is
`unverified` or `error` is reported as not done, with the observed state. Then, if any
verdict changed code, point at the commit; if any is `hold`, list what the human must
decide.

## Hard rules

- Verify before replying; a verdict without opened code is `hold`.
- Reply, react, resolve, read back — for every handled thread, in that order. Missing
  any one of the four means the thread is not handled. A `hold` thread is the one
  exception: reply and read back, reaction `none`, no resolve, `reason_open` in the report.
- Never resolve a thread you did not reply to, and never resolve a `hold`.
- Never post through a second path (web UI, another tool) to "fix" a failed row — re-run
  the script or the primitive so the ledger stays true.
- Never print tokens; the script masks known token shapes in output and errors.

| Rationalisation | Reality |
|---|---|
| "The bot is usually right, I'll accept it" | The 2026 `!5581` findings looked right and were blocked upstream by validation. Open the code. |
| "I replied, that's enough" | An open thread is open review debt; the MR still shows it as blocking. Resolve or say why not. |
| "It's out of scope, so I'll just resolve it silently" | The reviewer learns nothing and the author cannot see why. Reply with the scope reason, then resolve. |
| "The POST returned 201" | The ledger's `observed` block is the deliverable. Read back or report unverified. |
| "This reviewer doesn't learn from reactions" | The reaction is also the author's and the next reviewer's signal. Add it unless the user opts out. |
