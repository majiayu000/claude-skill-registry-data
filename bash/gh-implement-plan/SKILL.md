---
name: gh-implement-plan
description: Implement a GitHub plan issue step by step with checkpoints. Use when the user asks to "implement the plan", "start working on the plan", or "execute the plan".
argument-hint: "[owner/repo#number]"
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

Implement the plan from GitHub issue $ARGUMENTS (issue URL or `owner/repo#number`). If no argument is given, use the issue referenced earlier in this conversation. If no issue can be determined, ask the user.

1. **Prepare branch**: If on main/master, fetch the latest and create a feature branch with a descriptive name derived from the plan issue title. If already on a feature branch, continue on it.
2. **Read the issue** and identify all steps (checkboxes). Steps may be in a separate **Steps** comment (new format) or in the issue body (old format). Check both. Before starting implementation, think about the design: What abstractions are needed? Where should the boundaries be? Is there a simpler approach than what's described? Flag any design concerns to the user before coding.
3. **Present the steps** to the user and confirm which step to start with. If a durable-memory CLI is configured, sync it here so recall in step 4 works off a fresh mirror.
4. **For each step**, in order:
   a. If a durable-memory CLI is configured, query it with the step's distinctive terms before implementing. See the memory tool's own integration doc for mechanics.
   b. Implement the change.
   c. Stage and commit the changes with a descriptive commit message. Do not reference the issue.
   d. Check off the step (`- [x]`) on the issue. Update wherever the steps are found (Steps comment or body).
5. **After all steps are complete**, present a summary of what was done for each step (files changed, key decisions). Tell the user to review the commits and push when ready.

Rules:
- Never commit directly to main/master -- always work on a feature branch.
- Never push to remote -- only stage and commit locally.
- If a step is unclear or seems wrong, stop and ask the user for clarification instead of guessing.
- If a step fails or produces unexpected results, stop and explain what happened before continuing.
