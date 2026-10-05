---
name: green
description: Run the repository's real CI gates locally and drive them to green — read the failing step, fix the cause, re-run only that job, repeat. Use before pushing, after a red hosted run, or whenever "make CI pass" is the ask. Never weakens a gate to make it pass.
when_to_use: "make CI pass, fix CI, run CI locally, is CI going to pass, pre-push check, 本地跑CI, 本地跑CI并修好失败, CI红了, 修CI"
argument-hint: '[job name or id — default: every job runnable on this machine]'
user_invocable: true
---
