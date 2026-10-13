---
name: commit-and-push
description: Apply this repository's commit, push, and CI discipline. Use before every commit or push and while monitoring CI.
---

# Commit and push discipline

## The rule that matters most

**`dev` and `main` are release branches.** Every push to either one triggers CI
and cuts a release. Pushing without being asked pollutes the release history and
burns CI minutes.

- **Commit** freely, without asking. Local commits are free and reversible.
- **Never squash commits without explicit user authorization in the current
  conversation.** A request to merge, integrate, land, finish, or keep history
  linear does not authorize squashing. Preserve the atomic commits by default.
- **Push** to `dev` or `main` **only** when the user explicitly asks _in the
  current conversation_ — "push", "tu peux pusher", "merge".
- Approval does **not** carry over. Authorization given for one push covers that
  push only; the next one needs a new ask.
- Do **not** infer approval from: a green test suite, a finished fix, a request
  to "continue", or an earlier instruction to work autonomously. Autonomy covers
  the work, never the release.
- Leaving several commits stacked locally is the normal, expected end state. Say
  so plainly: "N commits waiting locally, nothing pushed."

Feature/fix branches that are not `dev` or `main` can be pushed freely.

## Commit format

Conventional Commits, English, imperative, lowercase, no trailing period, ≤ 72 chars.

```
<type>(<scope>): <short imperative description>

<body — explain WHY, not WHAT; wrap at 72>
```

Types: `feat` `fix` `perf` `refactor` `style` `docs` `test` `chore`.
Breaking change: `feat!:` plus an explanation in the body.

- **One commit per fix.** Do not batch unrelated fixes; each must be revertable alone.
- The body is for motivation and root cause — the diff already shows the what.

## Never credit a tool

**No `Co-Authored-By` trailers. Ever.** Not Claude, not Copilot, not
`github-actions[bot]`, not any LLM or tool. Remove them if present. The code is
ours, the credit is ours, the responsibility is ours.

## Linear history

`main` and `dev` must stay perfectly linear — no `Merge branch '…'` commits.
Rebase the topic branch when necessary, then use a fast-forward-only merge so
its atomic commits remain intact. Squashing is permitted only when the user
explicitly authorizes that exact squash in the current conversation.

## Before pushing (once authorized)

Run the full local gate first — see the `ship-fix` skill for the four commands.
A push that turns CI red costs far more than the two minutes the gate takes.

## Monitoring CI after a push

```bash
gh run list --branch dev --limit 1
gh run watch <run-id> > /tmp/ci.log 2>&1
gh run view <run-id> --json conclusion --jq .conclusion
```

**Do not pipe `gh run watch` into `tail` or `head`** and read the exit status —
`$?` becomes the pipe's last command, not `gh`'s, and a failing run reads as a
pass. This has caused a real misreport. Redirect to a file, then query
`--json conclusion` explicitly.

If CI fails: fix the cause and push the fix (the authorization to push covers
getting the branch green again — you are finishing the push the user asked for,
not starting a new one). Never weaken or delete a test to make CI pass.
