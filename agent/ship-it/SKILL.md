---
name: ship-it
description: Gate a PR's merge without human review, and merge it when the gate passes. Use when landing a PR during autonomous work, or when another skill needs a merge gate.
argument-hint: "[--dry-run] [--comment]"
---

You are the **gate** in front of an unattended merge. A **judge**, a fresh sub-agent, rules **merge** or **hold**; you check the PR is ready to judge, brief the judge, and act on its verdict. A hold hands the PR to a human.

## 1. Check readiness

The PR is ready when every required check has passed, it is not a draft, it merges without conflicts, and every review thread that asks for a change or an answer is resolved. A thread that only explains the diff asks for neither. When any condition fails, the outcome is **not ready**: skip to step 5. Finishing the PR is the author's work, not a human's call.

## 2. Gather the evidence

Collect what earlier work produced about this PR, wherever it lives (this session, the PR's body, comments, and checks): review ledgers with their dispositions, QA verdicts and reports, CI results, links to the spec.

The evidence is outputs only. The judge forms its own view of the change, so the author's reasoning and confidence stay with the author.

Done when every piece of evidence you can find is listed, by content or path.

## 3. Dispatch the judge

Dispatch one fresh, read-only sub-agent. The brief carries the path to [references/judge.md](references/judge.md), to read first; the PR and its head commit; and the evidence.

Done when the judge returns a verdict in `judge.md`'s shape.

## 4. Act

On **merge**, merge the PR per the repository's merge settings, pinned to the head commit the judge reviewed, unless `--dry-run`. When the merge is refused, that refusal is the outcome.

With `--comment`, post the judge's report on the PR, whatever the verdict.

## 5. Report

Open with the outcome: **not ready**, **merged**, **merge** (dry run), **hold**, or the merge refusal. Then the failing conditions for not ready, the judge's cited holds for a hold, or its follow-ups for a merge.
