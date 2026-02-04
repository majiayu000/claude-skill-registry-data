---
name: write-gh-issues-prs
description: Write GitHub issues and PRs for this repo with the established conventions. Use when drafting issue or PR content or guidance.
---

## Writing GitHub Issues and PRs
- We use GitHub issues and PRs to coordinate work between agents and the project owner.
- Best practices with regards to content are explained in the templates: `.github/ISSUE_TEMPLATE/task.md`, `.github/PULL_REQUEST_TEMPLATE.md`.
- Use GitHub CLI with `--body-file` to avoid shell quoting pain.
- Agents start with zero context about the project before onboarding, and they will focus on onboarding and reference materials relevant to their task. We have to mention required readings explicitly in the github issues so that agents pick them up.
- Style:
  - Literal correctness, unambiguity, clarity are important. We don't have much interactiveness between author and worker agents, so misunderstandings must be avoided up front.
  - Calibrated confidence: predictions have relative strengths (probabilities, expected utility), and ideas are predictions about what subgoals, metrics, constraints, or even concrete steps will help the overall thesis project how much. We don't expunge the uncertainty and relative strength, but clearly communicate what we believe confidently is a must-have, and what is a speculative idea, or even just a first guess to try and throw out if unsuitable.
  - Most PRs are reviewed by the project owner only. We help the project owner by offering skimmable extra commentary and not leaving out insights we have that could cut down the time the project owner has to spend understanding, evaluating, or handing back the PR.
  - We use numbered/lettered lists to make references easier, since line numbers are not quite as stable.
- GitHub Identity: All agents share the GitHub identity of the project owner, thus various fields in PRs and issues lose their meaning (e.g. author, assignee). Instead we use footers and body text to clarify these aspects where relevant.
