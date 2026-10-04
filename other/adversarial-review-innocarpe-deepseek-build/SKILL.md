---
name: adversarial-review
description: >
  Run a bounded, evidence-based adversarial review of a DeepSeek Build change
  with the pinned GPT-6 Astra or Claude Opus 5.5 reviewer. Use before a merge
  when the user asks for an adversarial review or when this unit requires it.
---

# Adversarial review

Use this skill to find reachable defects in a concrete change. A review is not
complete because a command exited successfully: the runner also checks the
observed model, output quality, and review structure.

## Fixed reviewers and attempt budget

The runner supports exactly these pairs:

| Model | Effort |
|---|---|
| `gpt-6-astra` | `xhigh` |
| `claude-opus-5-5` | `xhigh` |

Each launch gets a fresh context. The default goal is to finish within two
attempts per model; the hard limit is three launches per model for the same
commit and diff. A timeout, interrupted process, provider error, malformed
response, wrong model, or weak answer consumes an attempt. Never retry
automatically, lower effort, or switch models when one fails. A new attempt
requires an explicit `run` command and must stay within the recorded limit.

Claude's JSON response can identify the model, but does not attest the effort
used. The runner records `--effort xhigh` as command-line evidence and states
that the response cannot verify effort; it does not present that as observed
metadata. Claude runs with `--restricted --safe-mode` and only `Read`, `Grep`,
and `Glob` tools enabled. This disables user/project/local customizations and
hooks while preserving read-only code inspection.

## Prepare the review prompt

Write a prompt file with all six headings below. Be concrete and include prior
review findings when there are any; use `None` when there are none.

```markdown
## Invariant
State the product or code invariant this change must preserve.

## Boundaries and mutations
Name boundary values, plausible mutations, and failure cases to challenge.

## Real-world path
Trace the user or runtime path that reaches this code in a real environment.

## CI evidence
List the relevant commands and CI evidence, including gaps or skipped checks.

## Prior findings
List earlier findings and their human disposition, or state that none exist.

## Closure question
Ask whether the pinned change is safe to merge and what evidence supports that verdict.
```

Run one model at a time:

```sh
scripts/adversarial-review.sh run --model gpt-6-astra \
  --repo . --base origin/main --prompt /path/to/review-prompt.md
scripts/adversarial-review.sh run --model claude-opus-5-5 \
  --repo . --base origin/main --prompt /path/to/review-prompt.md
```

The runner rejects a dirty checkout, an empty diff, missing prompt sections,
and a file manifest that does not match the generated full diff. It pins the
base, merge-base, target commit, changed paths, and diff hash before launching
the reviewer. It does not post comments or edit repository files.

## Read status and results

```sh
scripts/adversarial-review.sh status [review-id]
scripts/adversarial-review.sh list
scripts/adversarial-review.sh result <review-id> <model>
scripts/adversarial-review.sh result <review-id> <model> --raw
```

Each attempt stores its prompt, full diff, stdout, stderr, final body, timestamps,
exit code, requested and observed model, requested effort and its evidence, and
failure reason under `~/.deepseek-build/adversarial-reviews/`. A result counts
as `done` only when the command exits zero, the observed model matches, the
pinned checkout is still clean at completion, and the body passes the
review-quality checks. An unobservable model, effort mismatch,
JSON parse error, timeout, nonzero exit, short answer, or answer without the
required review sections is `failed`.

The minimum body length is 300 characters and it must contain a verdict,
findings, invariant/boundary analysis, CI/environment analysis, and a closure
answer. A finding must state priority, impact, location, reproduction, and a
minimal fix. An explicit `No findings` is acceptable only with the required
analysis and verdict.

This threshold includes a measured HQ failure from 2026-09-27:
`dsb-pr288-opus-xhigh-final-20260927` exited zero and reported
`claude-opus-5-5`, but its result was only 97 characters (188 bytes) saying it
would wait for a background Grok test. HQ correctly marked it failed. The
runner treats that kind of waiting message as a failed review and does not
call the model again automatically.

## Human disposition

Read each completed body and reproduce or reject every finding with evidence.
Apply only findings that are valid for the pinned change. Re-review only when
the fix creates a material new question, and always review the new commit/diff
as a new pinned target. Do not treat a model's verdict as merge authorization.
