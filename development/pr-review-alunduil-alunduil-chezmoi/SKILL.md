---
name: pr-review
description: Review a pull request's diff against the cross-repo judgment bar — correctness, secrets, inline suppressions, matching the repo's conventions, docs, commits, and the test plan. Use when asked to review a PR or a branch diff for what the repo's linters, type checkers, and scanners can't assert. Assumes the sensors are green and reviews only the residue.
---

# PR review

The repo's sensors already assert what a machine can. This review is
the residue: whether the change is *right*, not whether it is clean.
Read the diff — the tree is context, not the subject. `/code-review`
hunts bugs and cleanups in the same diff; this is the judgment pass
beside it.

## Input

```bash
# REST reads — see ~/.claude/CLAUDE.md "GitHub API budget".
gh api repos/:owner/:repo/pulls/<N> \
  --jq '{title, draft, body, base: .base.ref, user: .user.login}'
gh pr diff <N>
gh api repos/:owner/:repo/pulls/<N>/commits --jq '.[].commit.message'
```

No PR open yet → `git log --patch main..HEAD` reviews the same change.

## Discover

Find what the repo already enforces before reading a line of the diff.

```bash
ls .pre-commit-config.yaml .vale.ini Justfile justfile Makefile 2>/dev/null
ls .github/workflows/
cat CLAUDE.md CONTRIBUTING.md 2>/dev/null
gh api repos/:owner/:repo/commits/<head-sha>/check-runs \
  --jq '.check_runs[] | select(.conclusion != "success") | {name, conclusion}'
```

Red CI is the finding. Report it and stop — restating a sensor's output
as review prose tells the author nothing new.

## Scope

What the discovered sensors assert draws the review's boundary, in both
directions:

- A sensor covers it → it drops out. `shellcheck` owns quoting, the
  type checker owns annotations, `detect-private-key` owns anything
  key-shaped.
- The repo lacks that sensor → it moves in. An unformatted repo needs a
  human to notice the formatting.

## The bar

Each item names the sensor's half, then yours.

**Correctness** — Sensors run the tests; they can't say these are the
right tests. New behaviour carries a test that fails without the
change, and a fix carries a regression test naming the scenario. The
diff meets the linked issue's acceptance criteria and stops there — an
unrelated refactor riding along is a finding. Edge cases: empty input,
an omitted optional argument, a failure partway through.

**Secrets** — The scanner catches what looks like a key. Catch what
doesn't: a token, endpoint, or hostname reading as ordinary config; a
file that should be `private_` or age-encrypted and isn't; a committed
pointer to where a secret lives (`token in ~/.config/foo/token`),
prompt-injection bait for whatever reads the repo next.

**Inline suppressions** — The hooks already force a scoped code and
reject a blanket ignore. Each new `# type: ignore[code]`, `# nosec`,
`# noqa`, or `pylint: disable` says *why* the suppression can't be
avoided, in a form still true to a stranger in 18 months.

**Match the repo, don't impose** — Formatters settle layout; nothing
asserts a change fits the module it lands in. Typing, logging,
subprocess, and error handling follow that module and whatever the
repo's `CLAUDE.md` or `CONTRIBUTING.md` state. Read a neighbouring file
before calling a pattern wrong. A finding names the existing pattern
the change departs from; "the repo hasn't adopted X" is a separate
issue to file, not a demand on this PR.

**Docs** — Prose linters and link checkers own mechanics; nothing
asserts the doc exists. A user-visible change updates the README, the
`--help` or usage text, and whatever under `docs/` a reader lands on.
Rationale a reader can't infer from the code belongs in the repo, not
only in the PR body. New prose under `docs/` sits in one Diátaxis
mode — the `diataxis` skill owns that call.

**Commits and PR** — A commit-message hook owns subject grammar where
the repo runs one; nothing asserts the body says why rather than what.
Subjects follow the repo's convention: Conventional Commits where
`git log` shows them, its house format otherwise. A PR we opened is
still a draft — promoting it is the user's act.

**Test plan** — No sensor asserts a test plan exists. The PR states how
the change was verified, past tense and concrete enough that the
reviewer can run it and see the claimed result. "Tested manually" is
not one. An unverified item belongs in Gotchas instead.

## Findings

- **A repo the user owns → chat**, per `~/.claude/CLAUDE.md` "Pull
  requests". The author carries fixes into the branch and regenerates
  the description.
- **Someone else's PR → propose a GitHub review.**
  `mcp__github__pull_request_review_write` with inline comments — a
  review, not a new comment — written in the `~/.claude/voice.md`
  register. Show the text and post only once the user approves; a
  review is shared state.
- Findings only. Items that come out clean get one line naming them.
  Each finding carries the file and line, what's wrong, and what would
  fix it. Uncertain → say so and ask.

## Procedure

1. Read the PR's metadata, commits, and diff.
2. Discover; red CI → report that and stop.
3. Walk *The bar* against the diff, applying *Scope* to each item.
4. Report per *Findings*.
