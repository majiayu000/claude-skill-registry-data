---
name: qa-explore
description: Git-log-scoped exploratory regression hunting — scope a pass from recent commit history, form concrete side-effect hypotheses per commit (not just re-testing stated intent), then drive the live app via curl or Playwright MCP to probe them. Open-ended exploration with no maintained fixture, bounded by time and commit count — NOT the fixed VERIFY.md anchor checks (/verify) or a PR-diff review (/review-pr).
when_to_use: "explore for regressions, what could recent commits have broken, hunt for regressions, exploratory QA pass, antirez-style regression hunt, manually poke the app after a batch of commits — NOT for the fixed behavior-anchor checklist (use /verify) or a VERIFY.md walkthrough (use /review)"
argument-hint: "[since <ref-or-date>]"
user_invocable: true
---
