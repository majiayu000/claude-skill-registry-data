---
description: Update the plan, the log, and the decisions after a PR is merged
model: sonnet
---

# Goal

- Given the plan ids of merged PR(s), sync the project docs: tick the plan, add the
  log entry, and record the decisions
- Log facts only. Never invent a result

## Input

- `<PR_IDS>`: One or more plan ids, e.g., `PR_M10`
- `<PR_NUM>`: The GitHub PR number, optional
  - If missing, find the merged PR with `gh pr list --state merged --search
    "<PR_ID>"`
- `<DOCS_DIR>`: The project `docs/` dir, optional
  - If missing, use `docs/` in the current dir

# Workflow

## Check the PR Is Merged

- Read the PR with `gh pr view <PR_NUM>`
- If the PR is not merged, stop and tell the user. A PR is checked only when merged

## Update the Plan

- Tick `[x]` the PR in the roadmap and in its entry in `<DOCS_DIR>/04-plan.md`
- For a partly done PR, write its status in its entry. Do not tick it
- If the scope or order changed, edit the plan and log why in the progress log

## Update the Log

- Add the entry to `<DOCS_DIR>/07-progress.md`, after the older ones
  - Use a History row, or one section per PR when a row is too short
  - Follow `.claude/skills/project.rules.md` section "Write the Log" and the
    template `.claude/templates/project_progress.template.md`
- Take from the PR: the issue, the author, the UTC dates, the testing evidence,
  and the failing checks that the PR did not cause
- Update "Status", "Built", and "Next"
- Ask the user for any finding or number missing from the PR. Do not invent it

## Record the Decisions

- For each decision in the PR description's "Decisions" section, add an entry to
  `<DOCS_DIR>/03-decisions.md`
  - Follow `.claude/templates/project_decisions.template.md`
- Add a one-line pointer to the decision in the log entry
  - Make the pointer a link to the
    ```
    ### `D<N>` (<Decision title>)
    ```
    header in `03-decisions.md`, per `.claude/skills/project.rules.md` section
    "Link Requirements and Decisions"

## Sync the Other Docs

- Apply the event map in `.claude/skills/project.rules.md` section "Map Each Event
  to the Doc to Update"
- Update the design doc of each changed module
- Update `<DOCS_DIR>/README.md` if a doc was added, renamed, or removed
- Add new terms to `<DOCS_DIR>/10-glossary.md`, if the file exists

# Conventions

- Follow `.claude/skills/project.rules.md` for project docs
- Follow `.claude/skills/markdown.rules.md` and `.claude/skills/text.rules.md`

# Constraints

- Append to the history. Do not rewrite past rows
- Log facts, not plans
- Do not commit any change. The user commits the doc update in the PR that finishes
  the task

# Verification

- [ ] Only merged PRs are ticked
- [ ] The log entry has the PR link, the dates in UTC, and the testing evidence
- [ ] Every decision of the PR is in `03-decisions.md`
- [ ] `<DOCS_DIR>/README.md` lists every doc in the dir
- [ ] No past row of the history was changed
