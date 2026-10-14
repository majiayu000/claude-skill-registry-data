---
name: ci-spend
type: Skill
title: "ci-spend — GitHub Actions cost discipline"
description: "The GitHub Actions cost rules ($100/week cap). Use when editing .github/workflows, adding a schedule or cron, dispatching a workflow, publishing a package version, hitting a billing block, or seeing a CI SPEND OFF TRACK line, ci-breaker issue or spend alert."
tags: [skill, ci, cost, github-actions]
timestamp: 2026-10-11
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/ci-spend/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# ci-spend

The law is [ci-spend.md](/policies/ci-spend.md); read it, it is short. How to apply it:

1. **Before touching a workflow**, write its `.github/ci-cost.json` entry first (trigger, runs/week, minutes, OS, $/week, benefit). Run `python3 scripts/check_workflow_runner_cost.py`. If $/week has no benefit you can name, do not add the workflow.
2. **Prefer** `paths:` filters, Linux runners, `timeout-minutes`, `concurrency` with cancel-in-progress, and a path or content-hash check before publishing.
3. **Dispatching a workflow**: pass `requested_by`; never loop a dispatch; if a run goes red, fix it before dispatching again.
4. **Billing or spending block**: stop. Do not move the job elsewhere. Tell Arman in plain English.
5. **Seen cost without benefit** (any shape in the policy): fix it if it is yours, else one plain sentence to Arman: what, roughly how much, no benefit.
6. **Check spend**: the one-liner in the policy, or the `github_actions_spend_watch` result.
