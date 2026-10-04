---
name: pr-review
description: "Review a GitHub pull request: fetch PR diff, run all review agents, post summary."
argument-hint: "[pr-number-or-url]"
allowed-tools: Read Grep Glob Bash
model: gpt-5.3-codex
---

# /pr-review — PR Review

Review PR: **$ARGUMENTS**

1. **Fetch** — `gh pr view $ARGUMENTS --json title,body,baseRefName,headRefName,files` + `gh pr diff $ARGUMENTS`
2. **Merge readiness** — `gh pr view $ARGUMENTS --json mergeStateStatus,statusCheckRollup`. Stop if CI failing or conflicts.
3. **Review pipeline:**
   - General: `agents/code-reviewer.md`
   - Language: `agents/typescript-reviewer.md` or `agents/python-reviewer.md`
   - Security: `agents/security-reviewer.md`
   - Silent failures: `agents/silent-failure-hunter.md`
4. **Verdict** — Approve / Request Changes / Block with action items
