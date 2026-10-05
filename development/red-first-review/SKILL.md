---
name: red-first-review
description: "Review someone else's pull request by measuring which of its own guards its own test suite actually catches. Use when reviewing a PR, auditing test coverage of a fix, checking whether a regression test is real, or when asked “is this change actually tested?“, “review this PR“, “does this test do anything“, “mutation test this“."
version: 1.0.0
---

# Red-first review

A test that has never been shown failing is a claim, not a check. This skill turns
that claim into a measurement: break the thing the test is supposed to protect,
and see whether anything goes red.

Applied to someone else's pull request it answers one question a human reviewer
cannot answer by reading: **which of the guards this PR adds would survive being
deleted?** Those are the ones the author will regress next month without noticing.

## When to use it

- reviewing a PR that adds a guard, a validation, a sanitiser, a redaction, a
  permission check — anything that says "no" on some paths
- someone claims a fix is covered by tests, and you want that claim measured
- you wrote a regression test yourself and want to prove it fails without the fix
- auditing a test file that has never failed in CI

Not for: pure refactors with no behavioural claim, docs, dependency bumps.

## The procedure

### 0. Read the whole files, not the diff

The diff shows what changed. The bug is usually in what did not. Open every
touched source file end to end, and specifically look for **sibling call sites**:
if the PR guards `delete`, does `rename` reach the same object? If it guards one
endpoint, how many endpoints are there?

Write down the full list of places the PR's own reasoning applies to. That list,
not the diff, is what you are about to measure.

### 1. Get the suite green before you touch anything

Check out the PR branch, install, run the tests it claims to affect.

A red baseline makes everything after it unattributable. If the suite is already
failing, narrow the command until it is green, **and check the same failures on
the base branch by name** — pre-existing failures reported as PR damage is the
fastest way to lose a maintainer's trust.

### 2. Prove your test command reaches the code

Break the file under review on purpose (append `raise RuntimeError("canary")`)
and re-run. If the suite stays green, that command never imports the file, and
every "covered" verdict you are about to produce is an artefact of some other
test. `mutmatrix.py` does this automatically and refuses to continue.

### 3. Neutralise each guard in turn, one at a time

```bash
python3 mutmatrix.py \
  --repo . \
  --test "pytest tests/unit -q -p no:randomly" \
  --file src/pkg/api.py \
  --call-identity redact_secrets
```

`--call-identity NAME` makes one mutant per call site of `NAME`, rewriting
`NAME(x)` to `x`. For guards that are branches rather than calls, spell the edit
out:

```bash
python3 mutmatrix.py --repo . --test "pytest tests/unit -q" --sep '@@' \
  --mutant 'root guard@@src/pkg/store.py@@if full_path == self.root.resolve():@@if False:'
```

Read the exit code, not just the table: `0` no survivors · `1` survivors found ·
`3` undecidable (baseline, canary, or a mutant that did not compile) · `4` the
tool broke. **Only `0` and `1` are results.**

Disable random test ordering (`-p no:randomly`) so runs are comparable.

### 4. Write the finding, one per survivor

A survivor is not "missing coverage" in the abstract. It is a specific sentence:
*reverting this one line leaves the whole suite green.* Say which line, and say
what the mutant table showed.

Then supply the test. Not a description of a test — the code, using the
project's existing fixtures and naming, so it can be pasted in.

### 5. Prove the new test is red for the right reason

Re-run the same command with your test added. The proof has three parts and you
report all three:

1. the row for that mutant flips from `SURVIVED` to `killed`
2. **every other row stays exactly as it was** — a test that kills every mutant
   is not specific, it is just noisy
3. the test passes on the PR as it stands

Without part 2 you have written a test that fails whenever anything changes.

### 6. Say what you did not check

Name the paths you never exercised — the UI, a live provider, an endpoint you
skipped. A review that implies total coverage is a review the maintainer has to
re-verify from scratch. Publish the hypotheses that came out clean too: it tells
them which doors are already closed.

### 7. Post it as a review object, not a comment

```bash
gh pr review <N> -R <owner/repo> --comment --body-file review.md
```

`gh pr comment` writes to the issue thread. It does not create a review object,
so it appears in no contribution graph and no `reviewed-by:` filter, while still
looking exactly like noise to spam heuristics. Reviews get `gh pr review`.
Do not use `--approve` or `--request-changes` on a repo you do not maintain.

If an AI agent produced the review, say so in the first line, and say whether a
human read it before it posted.

## Judgement rules

- **A syntactically broken mutant is not a covered site.** Every test fails on a
  `SyntaxError`, which looks identical to perfect coverage. `mutmatrix` compiles
  each mutant first and reports `INVALID`; if you mutate by hand, check it parses.
- **Never mutate a file you have not backed up**, and never leave a mutant behind.
  `mutmatrix` keeps a backup directory and refuses to start if a previous run
  left one.
- **Bytecode caching will lie to you.** CPython validates a `.pyc` by source size
  and mtime *in whole seconds*; two mutants of the same length in the same second
  run identical bytecode. Measured here: a killed site scored as SURVIVED.
  `mutmatrix` bumps mtime on every write.
- **Rank the findings and say which one matters.** Three findings with no order
  is a list. "Finding 1 is the one worth acting on" is a review.
- **Do not report a known issue as a discovery.** Search the repo's open PRs and
  issues for the adjacent problem first, and cite it if it exists.

## What ships with this skill

- `mutmatrix.py` — the engine. Standard library only, Python 3.8+, no install.
- `_test_mutmatrix.py` — its self-test, including `--red M1..M4`, which runs the
  suite against deliberately broken copies of the engine to prove the tests
  themselves can fail. A test suite that has never been shown red does not get to
  certify anyone else's.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
