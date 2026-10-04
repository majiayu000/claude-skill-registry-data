---
name: push-checkpoint
description: Run the every-10-pushes quality checkpoint — a scoped code review of everything since the last checkpoint, plus a test-and-lint debug pass. Use this skill whenever a hook reports that a push count hit a multiple of 10, whenever the user types /push-checkpoint, and whenever the user asks for a checkpoint, a periodic review, a "review the last batch of work" pass, or asks what has accumulated since the last review. Prefer this over an ad-hoc review whenever the request is about reviewing recent pushes as a batch.
---

# Push Checkpoint

A periodic quality gate. Every 10 successful pushes, review what accumulated and
confirm the project still builds clean — so problems surface on a cadence instead
of piling up until release.

This skill does **two things**: a scoped review, then a debug pass. Do both, in
order, and report once at the end.

## How this gets triggered

`.claude/hooks/push-counter.py` runs after every Bash call, counts successful
`git push` commands in `.claude/state/push-count`, and asks for this skill on
every 10th. The user can also run `/push-checkpoint` at any time.

Skills cannot fire themselves on an event — the hook is what makes the cadence
automatic. If the checkpoint never fires on its own, the hook is the thing to
debug, not this file.

## Step 0 — establish the range

Find the last checkpoint and scope all work to what came after it:

```bash
cat .claude/state/last-checkpoint 2>/dev/null || echo "(no previous checkpoint)"
git rev-parse HEAD
```

- If a SHA is recorded, the range is `<sha>..HEAD`.
- If not (first ever checkpoint), fall back to the last 10 commits: `HEAD~10..HEAD`,
  or the full history if the repo is shorter than that.

Confirm the range is non-empty before continuing:

```bash
git diff --stat <range>
```

If the range is empty, say so and stop — there is nothing to check, and the
counter should still be reset in step 3.

## Step 1 — review

Invoke the built-in `code-review` skill scoped to that range (pass the range as
its target). Review the batch, not all of history.

Report findings ranked most-severe first. Apply a fix yourself only when it is
small, local, and unambiguous — a clear bug, a typo, a missing guard. Anything
larger gets described, not silently changed: this is a checkpoint, not a
refactoring session.

## Step 2 — debug

There is no `/debug` skill; this is the debug step. Run the project's own checks
and triage anything that fails.

For this repository (Python):

```bash
python3 -m pytest -q
python3 -m ruff check .
```

If the project layout changes, run whatever the real checks are — prefer what
`pyproject.toml`, a `Makefile`, or CI config actually defines over the commands
above.

For each failure, find the **root cause** before proposing anything. Do not
paper over a red test:

- Never skip, disable, or `xfail` a test to get green.
- Never loosen an assertion to match wrong output.
- A failure that reproduces on the base branch too is pre-existing — say so, and
  keep it separate from failures this batch introduced.

Fix what is small and certain. Escalate the rest with a concrete proposal.

## Step 3 — record the checkpoint

Only after both steps are done:

```bash
git rev-parse HEAD > .claude/state/last-checkpoint
```

This is what keeps the next checkpoint scoped to the next batch. `.claude/state/`
is gitignored, so the counter and the checkpoint SHA stay local to each checkout.

## Step 4 — report

One consolidated summary:

- **Range** — the commit span reviewed, and how many commits it covered.
- **Review** — findings by severity; what you fixed vs. what needs a decision.
- **Debug** — test and lint results; root cause for each failure; pre-existing
  failures called out separately.
- **Verdict** — is the tree healthy, or is there something to act on now?

Be direct about a bad result. A checkpoint that always says "all clear" is
worthless — if tests fail, lead with that.
