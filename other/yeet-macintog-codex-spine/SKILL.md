---
name: yeet
description: Publish a validated PR revision while continuing review, or complete a validated registered Git task when a selected private task reaches terminal delivery or the operator explicitly says yeet. Default pull-request completion delivers a tested ready PR and retires owned local state; integrate only for the user-selected outcome. Do not use for ordinary commits, tests, deployments, read-only or no-diff work, or selecting integration refs outside the user-selected outcome.
---

# Yeet

Use two lifecycle modes. Publication during a review loop retains the task;
terminal delivery finishes the user-selected PR or integration outcome. Neither
mode selects new work, another host, deployment, or historical cleanup.

## Publish and continue

When the selected task includes an active review/correction loop, publish its
validated revision with `codex-git-safe yeet --publish-only --apply --json --brief`
and the ordinary authored inputs. This mode keeps the same registered writer,
checkout and branch. The working coordinator may execute this nonterminal mode
directly; do not create a delivery worker or retire/recreate the task for each
revision. Use the repository Git lane and exact intake/validation requirements.

`--publish-only` cannot combine with integration, terminal review-only, retired
task selectors, or shared checkpoint writes. Resume interrupted publication with
that same mode. Once `published_open` is proved, further corrections publish to
the same PR against its last recorded live head. A retry of an unchanged published
head reuses its proof without another push or PR write. Record current validation
and reviewer feedback at the exact head; `review_acceptance: not_recorded` and the
legacy internal `ready_for_integration` phase do not claim independent approval.

This is successful publication, not task completion. After the review loop is
finished, use terminal delivery below. `--review-only` still retires local state
while holding integration; selected integration still needs its own authority.
The operator chooses the desired outcome, not the CLI mode.

## Finish the selected outcome

When the work is finished, read [Terminal delivery](references/terminal-delivery.md)
and follow its resumable transaction, designated-worker, exact-proof, and owned
retirement requirements. The parent retains selection and final acceptance.
Reuse an available designated worker serially within the currently selected batch,
with a fresh exact brief and independent receipt for each transaction.

Bare `yeet` finishes a ready PR under the normal PR workflow. Selected integration
adds keeper and hosted-closure proof. Preserve explicit merge holds, unrelated
reviews, and unowned objects. Report published, accepted, merged, and retained
cleanup as distinct facts; a successful query alone proves no completion.

For the historical naming comparison, see
[Same name, different contract](references/name-and-scope.md).
