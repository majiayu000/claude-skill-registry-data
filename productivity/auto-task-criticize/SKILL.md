---
description: Review a plan or GitHub issue for an `auto_task` before execution
model: haiku
---

# Goal

- The user passes a file `<FILE>` (e.g., `tasks.md`) or a GitHub issue number
  `<GITHUB_ISSUE_NUM>`
- Read the content carefully. Make sure the problem and the solution are clear
  and complete

# Workflow

## Read Context

- Read the plan (file or GitHub issue)
- Analyze the problem and the solution

## Create a Plan, If Needed

- Identify the repos the change affects. This decides whether a PR spans
  multiple repos
  - Update the `* Repo:` checklist in `.claude/templates/auto_task.template.md`,
    following `.claude/skills/auto_task.rules.md` section "Multi-Repo Issues,
    Branches, and PRs"
  - If more than one repo is checked, each `PR<NUM>` block in "Solution" must name
    its target repo. An unlabeled `PR<NUM>` in a multi-repo task is an unclear
    plan (see "Ask for Clarification Before Executing an Unclear Plan" in
    `.claude/skills/auto_task.rules.md`)
  - Do not add or edit a `## Companion PRs` section. Once PRs exist,
    `git_create_issue_and_branch.py` generates it, per
    `.claude/skills/auto_task.rules.md` "Multi-Repo Issues, Branches, and PRs"

- If the task is not perfectly clear, follow `.claude/skills/auto_task.rules.md`
  section "Ask for Clarification Before Executing an Unclear Plan"

## Output Results

- Follow `.claude/skills/auto_task.rules.md`
- Write the output as a file in the format `.claude/templates/auto_task.template.md`

# Conventions

- Follow `.claude/skills/coding.rules.md` when writing code
- Follow `.claude/skills/testing.rules.md` when writing testing code

# Verification

- [ ] The problem statement is clear and unambiguous
- [ ] The proposed solution is clear and unambiguous
- [ ] Any needed clarification was requested before the task moves to execution
