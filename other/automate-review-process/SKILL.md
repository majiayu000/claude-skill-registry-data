---
name: automate-review-process
description: Design a risk-tiered review process for code, design, or approvals. Measures review latency, splits the work between checks, AI reviewers, and humans, and produces the policy plus starter config. Use when reviews are slow or inconsistent, or when adding an AI review gate.
---

# Automate the Review Process

Help an engineering team spend human review time only where judgment matters. Everything deterministic moves to checks, and everything else is routed by risk.

## Reasoning Framework

"Fully automated review" is the wrong goal. Review is a risk-control system, so design it like one: tiers of risk, gates matched to each tier, evidence that each gate ran, an escape hatch for emergencies, and metrics that show whether it works. Automate what a script can decide (format, lint, tests, secrets, size, forbidden files). Let an AI reviewer take the first pass on logic. Keep human approval for design intent, correctness in risky areas, and anything compliance requires.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| Review baseline | Markdown table from `scripts/pr_review_stats.py` | Eng lead, PM |
| Review process design | Markdown, from `references/review-policy-template.md` | Eng leads, team |
| Starter config | CODEOWNERS, PR template, branch-protection checklist | Repo admins |

## When to Use

- PRs wait days for review, or reviews are rubber stamps
- Review rules differ by reviewer and nobody knows the policy
- Adding an AI code reviewer and deciding what it may block or approve
- Design reviews or launch approvals that stall

## When NOT to Use

- Reviewing a specific PR: use your code-review tool (for example `/code-review` in Claude Code)
- Launch go/no-go for one release: use `launch-checklist`

## Inputs

1. **Scope**: code review, design review, approvals, or all three.
2. **Repos and access**: GitHub with `gh` authenticated gives a measured baseline; other hosts need the same numbers exported by hand.
3. **Team**: size, roles, time zones, who owns which areas.
4. **Pain**: slow, inconsistent, missed defects, reviewer burnout, or something else.
5. **Constraints**: compliance rules (for example two-person approval), regulated or sensitive code paths.
6. **Tools available**: CI, AI reviewers, merge queue.

## Steps

1. **Measure the baseline (script).**
   ```bash
   gh pr list --state merged --limit 200 \
     --json number,createdAt,mergedAt,additions,deletions,author,reviews > prs.json
   python3 scripts/pr_review_stats.py prs.json -o review-baseline.md
   python3 scripts/pr_review_stats.py prs.json --exclude-bots   # human-only view
   ```
   Before you conclude anything, ask how review actually happens. Reviews outside GitHub's review feature do not appear in these numbers: pre-PR AI gates, verdicts stamped in the PR body, pairing. In that case "merged unreviewed" is a measurement gap, not a finding.
2. **Map the flow.** Author → automated checks → reviewer assignment → rounds → approval → merge → deploy. Separate waiting time (queue) from rework time (rounds). Note the failure modes: oversized PRs, unclear ownership, nit rounds, late design feedback.
3. **Define risk tiers by path.** This is the core of the design.
   - **Tier 0**: docs, copy, tests only. Automated checks, optional async review.
   - **Tier 1**: standard product code. Checks, an AI first pass, one human reviewer.
   - **Tier 2**: auth, payments, data migrations, infra and permissions, secrets, public APIs. Checks, AI review, and a code-owner approval, with no auto-merge.

   Write tiers as an allowlist of low-risk paths. Any path the rules don't recognize falls into the stricter tier.
4. **Automate the deterministic layer.** Formatting, lint, type checks, tests, secret scanning, dependency review, a PR size warning (about 400 changed lines), forbidden-file checks, and PR template completeness. If a script can decide it, it is not a reviewer's job.
5. **Design the AI review gate** (if used):
   - Where it runs: locally before the PR opens (fast, cheap) or as a CI check (enforceable).
   - What blocks: findings at or above an agreed severity.
   - The record: every verdict is written somewhere verifiable (a check run or a stamp in the PR body). Nobody writes "AI reviewed" without that artifact.
   - A round cap (for example 3). After that, a human decides instead of grinding through more rounds.
   - A skip protocol for when the reviewer is down or out of quota. Only Tier 0 and Tier 1 changes may skip, and each skip records the reason and the substitute review.
   - Cost routing: a cheaper model or lower effort for Tier 0 surfaces, the strongest for Tier 2.
6. **Set human review rules.** A response-time SLA (for example first response within one business day), assignment (CODEOWNERS plus rotation), what humans review (intent, design, risk; not style), merge authority per tier, and an emergency path (hotfix now, review within 24 hours).
7. **Cover design reviews and approvals** if in scope. Apply the same tiering (new pattern or flow versus copy tweak) and use async written review with a decision deadline. Route launch approvals through `launch-checklist`.
8. **Plan the rollout.** Pilot on one repo or team for 2–4 weeks, rerun the script, and compare against the baseline. Target metrics: first-review p50/p90, merge p50, share of PRs over 400 lines, change-request rounds, and escaped defects per tier.
9. **Write the design** from `references/review-policy-template.md`. Keep the policy to about one page.

## Examples

- "Our PRs sit for two days." Measure, find that XL PRs dominate the p90, and propose a size budget, CODEOWNERS routing, and an AI first pass for Tier 1.
- "We want an AI reviewer to block merges." Define what it blocks on, where verdicts are recorded, the round cap, and the skip protocol, then pilot on Tier 0 and Tier 1 only.

## Guardrails

- Never remove a human approval that compliance or policy requires.
- No auto-merge for Tier 2 paths.
- Every rule states its reason. If a rule can't be explained, cut it.
- "Reviewed" means a verifiable artifact exists, for humans and AI alike.
- Measure before and after. Don't declare success on anecdotes.
- Keep private repo names, internal paths, and team names out of anything committed to this public repo.

## Related Skills

- `devex-survey`: developer sentiment on review turnaround
- `launch-checklist`: approval gates for releases
- `decision-brief`: get sign-off on the new policy
- `engineering-foundations`: review drills and habits
- `library/lenny-podcast/lenny-running-design-reviews/SKILL.md`: design review practice
