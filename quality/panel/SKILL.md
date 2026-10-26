---
name: panel
description: Orchestrate a rigorous multi-agent implementation, review, and verification panel inside Herdr. Use when the user requests Panel or a Herdr-managed panel review.
---

# Panel

Run independent reviewers in panes created for the current task, then return one
deduplicated set of evidence-backed findings.

1. Verify `HERDR_ENV=1`. When it is absent, tell the user to start the primary
   agent inside Herdr and stop; Panel does not bootstrap or attach to Herdr from
   an ordinary terminal.
2. Read [`../herdr/SKILL.md`](../herdr/SKILL.md) and follow its discovery,
   targeting, lifecycle, and safety rules. Use `/code-review` as the authority
   for standards and specification review.
3. Learn the installed CLI with `herdr --help` and `herdr agent`. Treat its
   reported agent kinds as authoritative. Honor agent kinds requested by the
   user; otherwise select from installed kinds appropriate to the task. Never
   assume one vendor or executable.
4. Inspect the calling pane, create the required sibling panes with
   `herdr pane split`, and preserve the current working directory and user
   focus. Panel creates its own panes; the user need not prepare a layout.
5. Start each reviewer with a unique role-based name through
   `herdr agent start <name> --kind <kind> --pane <pane-id>`. Supported kinds
   may include Claude, Codex, Copilot, OpenCode, and others reported by the
   installed Herdr version.
6. Give reviewers non-overlapping assignments. For implementation work, cover
   specification compliance, repository standards, and executable
   verification. Include the fixed comparison point, issue or specification,
   and repository instructions each reviewer needs.
7. Wait for each reviewer to settle, inspect blocked or timed-out panes before
   sending more input, and collect the complete results. A timeout does not
   prove a prompt was not delivered.
8. Validate findings against the diff and test evidence, remove duplicates and
   unsupported claims, and report actionable findings by severity. If no valid
   findings remain, say so and report the verification performed.

Panel coordinates local agents and commands only. Pushing, opening or merging a
change request, answering unfamiliar approval prompts, and deleting panes or
workspaces require the user's existing authorization.
