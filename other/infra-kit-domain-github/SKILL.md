---
name: infra-kit.domain.github
description: Create, review, standardize, or troubleshoot GitHub repository and CI/CD assets (CODEOWNERS, templates, branch protection guidance, and GitHub Actions workflows).
---

# GitHub (Repo + Actions)

Use this skill when the user is working on GitHub repository hygiene and delivery automation, including:

- repository governance and collaboration files such as `.github/CODEOWNERS`, pull request templates, issue templates, `CONTRIBUTING.md`, labels strategy
- merge safety guidance (branch protection, rulesets, required checks)
- GitHub Actions workflows under `.github/workflows/*.yml` (permissions, fork safety, maintainability)

## Outcomes

- Scaffold repository governance files that keep contribution flow consistent
- Review GitHub repo configuration for unclear ownership, missing templates, and weak merge controls
- Standardize pull request and issue hygiene with lightweight defaults
- Reduce duplicated contributor instructions and review rules across repo docs and templates
- Explain how GitHub collaboration features fit together across templates, reviews, and protected branches
- Review and harden GitHub Actions workflows for minimal permissions, fork safety, and maintainability

## Where This Fits In The Flow

- Use after `infra-kit.workflow` when the ticket is about repo hygiene: CODEOWNERS, templates, labels, protections.
- Use to make ownership and merge safety explicit so infra changes are reviewable and shippable.

## Workflow

1. Inspect repository collaboration files first:
    - `.github/`
    - `CODEOWNERS`
    - `CONTRIBUTING.md`
    - pull request and issue templates
    - `.github/workflows/`
    - release or merge automation config
    - use `gh pr diff` / `gh pr checkout <number>` to fetch the latest PR context when reviewing remote changes
2. Identify the operating model:
   - single maintainer
   - team-owned repository
   - platform/shared service repo
   - open-source contributor flow
3. Keep ownership and review routing explicit before adding automation.
4. Prefer the smallest set of governance files that solve the real workflow problem.
5. When branch protection or rulesets are part of the ask, describe the GitHub settings alongside any repo files that support them.
6. Look for duplicated contribution guidance spread across README sections, templates, and contributor docs.
7. Centralize shared instructions in the most durable place, usually `CONTRIBUTING.md`, and keep templates focused on request-specific context.
8. After editing, verify that file locations match GitHub's expected discovery paths.
9. During code reviews, if a pull request lacks an associated ticket or clearly described impact, leave an informational comment flagging the gap and avoid issuing Approve or Request Changes—final review state stays with a human maintainer.

### Actions Review Pass

When the change touches `.github/workflows/` (or the ticket is CI/CD-related), also check:

1. Trigger trust boundaries (push vs PR vs fork vs `pull_request_target`).
2. Top-level and job-level `permissions` (start minimal; escalate only when required).
3. Secret exposure paths (especially fork PR execution).
4. Supply-chain posture for actions (`uses:` pinning policy).
5. Maintainability (duplication -> reusable workflow or composite action).

## Hallucination Guardrails

- Ground every governance recommendation in concrete repo evidence: cite the exact path and, when possible, the lines you inspected so it is clear you are not describing imagined templates.
- When a required artifact (CODEOWNERS, templates, CONTRIBUTING, release config) is missing, say so explicitly and either scaffold it or ask for requirements—never assume it already exists.
- Call out GitHub UI settings (branch protection, rulesets, repo-level approvals) as manual follow-up instead of implying they changed inside the codebase.
- If stakeholder processes or ticket flows are unclear, document the assumption and request clarification instead of inventing Jira policies or approval chains.

## Output Standards

- Keep every review structured with explicit **Good News** and **Bad News** callouts so maintainers get balanced signal on strengths and gaps.
- Avoid referencing Jira or requesting Jira-specific evidence; keep discussion anchored to the GitHub context and repository docs.
- Cite at least one GitHub or industry best practice (for example, protected branches, CODEOWNERS, CONTRIBUTING docs) when explaining why a change matters.
- Deliver feedback through review comments only—do not mark the review as Approve or Request Changes so that a human maintainer owns the merge decision.

## Authoring Rules

- Use `CODEOWNERS` when review ownership matters, and keep patterns simple enough that maintainers can reason about them.
- Prefer pull request templates that collect decision-making context, testing notes, and rollout risk, not boilerplate filler.
- Use issue templates or forms only when triage quality is suffering; avoid over-structuring low-volume repos.
- Keep security-sensitive ownership explicit for areas like CI, release, infrastructure, and policy files.
- Keep `CONTRIBUTING.md` actionable:
  - setup
  - validation commands
  - branch or PR expectations
  - release process when relevant
- Keep shared instructions in one place instead of duplicating long checklists across PR templates, issue templates, and README sections.
- Prefer referencing `CONTRIBUTING.md` from templates when the full procedure is already documented there.
- Prefer protected branches and rulesets for merge controls instead of relying on convention alone.
- Prefer requiring reviews, required status checks, and linear or merge-queue style controls for higher-risk repositories when the team uses them.
- Keep automation-friendly labels and release notes conventions explicit if the repo uses them.
- Reuse `examples/` when the user wants a clean baseline for ownership or pull request hygiene.

## Review Priorities

When reviewing GitHub repository collaboration setup, check in this order:

1. Missing or wrong review ownership in `CODEOWNERS`
2. Merge safety gaps:
   - no required reviews
   - no required status checks
   - no protection on release branches
3. Missing security coverage for sensitive paths:
   - CI and release files without clear owners
   - infra or policy directories without designated reviewers
4. Missing pull request guidance for testing, risk, and rollback notes
5. Missing contribution instructions for local validation and branching flow
6. DRY violations:
   - duplicate contributor instructions across README and `CONTRIBUTING.md`
   - duplicate template text that will drift over time
7. Overly complicated templates or ownership patterns that people will ignore

## Best-Practice Notes

- GitHub documents that pull request templates and issue templates standardize the information contributors provide.
- GitHub documents that `CODEOWNERS`, protected branches, and rulesets help ensure the right reviewers and checks are applied before merge.
- Keep security-critical ownership and merge controls tighter than the repo default when some paths carry higher deployment or policy risk.
- Prefer one canonical contributor workflow document and have templates reinforce it instead of re-explaining the same process everywhere.
- Keep file placement aligned with GitHub discovery rules, such as `.github/PULL_REQUEST_TEMPLATE.md` or `.github/ISSUE_TEMPLATE/`.

## Delivery Standard

Always leave the user with:

- the collaboration pattern you chose and why it fits
- the files changed or recommended
- any GitHub UI settings that still need to be enabled manually
- unresolved risks around ownership gaps, weak branch protection, duplicated guidance, or template sprawl
