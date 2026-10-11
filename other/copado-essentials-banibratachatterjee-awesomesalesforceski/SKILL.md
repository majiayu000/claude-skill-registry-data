---
name: copado-essentials
description: "Use when configuring or operating Copado Essentials deployment pipelines — including user story creation, branch management, promotion paths, conflict resolution, and choosing between Work Items and Pull Request deployment modes. Trigger keywords: copado essentials pipeline, user story deployment copado, copado branch management, copado conflict resolution, copado promotion path. NOT for native Salesforce CLI or SFDX workflows without Copado, NOT for Copado Enterprise (full ALM) features beyond Essentials tier, NOT for DevOps tool selection (use devops/salesforce-devops-tooling-selection)."
category: devops
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
  - Security
triggers:
  - "how do I set up a Copado Essentials pipeline for my Salesforce org"
  - "my Copado user story is not promoting to the next environment in the pipeline"
  - "how does Copado Essentials handle merge conflicts between feature branches"
  - "should I use Work Items or Pull Requests mode in Copado Essentials"
  - "how do I change the deployment order of user stories in Copado Essentials"
  - "Copado Essentials is creating the wrong branch name for my user story"
tags:
  - copado-essentials
  - user-stories
  - pipeline
  - branch-management
  - conflict-resolution
  - promotion-path
  - work-items
  - pull-requests
inputs:
  - "Copado Essentials version installed in the org (check via Setup > Installed Packages)"
  - "Deployment mode in use — Work Items (in-app) or Deployments with Pull Requests (Git-native)"
  - "Pipeline configuration — org list in stage order with assigned Git branches per environment"
  - "User story reference numbers and their linked feature branch names"
  - "Git hosting provider (GitHub, GitLab, Bitbucket, Azure DevOps)"
  - "Whether merge order override is needed for dependency-based promotion sequencing"
outputs:
  - "Pipeline configuration review with identified gaps or misconfigurations"
  - "Recommended deployment mode based on team Git literacy and approval requirements"
  - "Conflict resolution steps for blocked user story promotions"
  - "Branch naming pattern confirmation and validation (feature/{user-story-number})"
  - "Promotion path map showing environment order and required approvals"
  - "Merge order override guidance when default ascending reference order causes dependency failures"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-06
---

# Copado Essentials

Use this skill when configuring or troubleshooting Copado Essentials deployment pipelines in a Salesforce org. It activates when practitioners need to set up user stories, manage feature branches, configure promotion paths between environments, resolve merge conflicts, or choose between the two deployment modes — Work Items and Deployments with Pull Requests.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Installed package version:** Copado Essentials is a free managed package. Confirm it is installed via Setup > Installed Packages. Older versions have different UI paths and missing features; always note the version number before advising on navigation or troubleshooting steps.
- **Deployment mode:** Copado Essentials offers two mutually exclusive deployment modes per pipeline — Work Items (in-app approvals and conflict resolution) and Deployments with Pull Requests (Git-native PR-based promotion). The mode determines which actions are available in the UI and which operations must happen in Git. Confirm which mode is active before diagnosing promotion issues.
- **Pipeline topology:** Each pipeline stage maps to exactly one Salesforce org and one Git branch. A misconfigured branch-to-org mapping is the most common root cause of failed promotions. Confirm the branch name for each environment before troubleshooting.
- **User story reference numbering:** Copado Essentials names feature branches using the pattern `feature/{user-story-number}`. The user story reference field (not the record name or Id) drives the branch name. Confirm the reference field is populated before expecting branch creation to succeed.
- **Merge order:** By default, Copado promotes user stories in ascending User Story Reference number order. When stories have metadata dependencies that require a specific promotion sequence, the default order must be overridden using the merge order field.

---

## Core Concepts

### User Stories and Feature Branches

In Copado Essentials, a User Story is a custom object that represents a discrete unit of work — typically a feature or bug fix. Each user story is linked to a Git feature branch named `feature/{user-story-number}`, where `{user-story-number}` is the value in the user story reference field (not the record Id).

User Story Tasks are child records that represent individual metadata components committed to the feature branch. Copado tracks which components belong to which story, enabling targeted deployments rather than full-org comparisons. A user story with no task records will produce an empty or no-op deployment, which is a common source of confusion when promotions succeed but no changes appear in the target org.

The link between a user story and its Git branch is established when the developer clicks "Create Feature Branch" inside the user story record. This action calls the Copado managed package to create the branch in the connected Git repository. If a branch with the same name already exists, Copado links to the existing branch rather than creating a duplicate.

### Pipeline Stages and Branch-to-Org Mapping

A Copado Essentials pipeline is a sequence of environments (pipeline stages), each mapped to one Salesforce org credential and one Git branch representing that environment's current deployed state. The canonical mapping for a three-stage pipeline is:

- `feature/*` branches — developer sandboxes (ephemeral, not a pipeline stage themselves)
- `develop` or equivalent — Integration sandbox (first pipeline stage)
- `staging` or equivalent — UAT sandbox (second pipeline stage)
- `main` or `master` — Production (final pipeline stage)

When a user story is promoted from one stage to the next, Copado merges the feature branch into the target environment's branch and deploys the resulting metadata delta to the target org using the Salesforce Metadata API. The merge is performed in Git by Copado; the deployment uses standard Metadata API deploy operations.

Environment branches (`develop`, `staging`, `main`) must exist in the remote Git repository before the pipeline is configured. Copado creates `feature/*` branches on demand but does not create environment branches. This is a frequent setup mistake.

### Deployment Modes: Work Items vs. Pull Requests

Copado Essentials supports two deployment modes configured at the pipeline level:

**Work Items mode** orchestrates the entire promotion flow inside Salesforce. Approvals, conflict detection, and merge resolution happen within the Copado UI. No Git client access is required for the deployer role. This mode is appropriate for teams where pipeline operators do not have direct Git access or prefer Salesforce-native approval workflows and audit trails.

**Deployments with Pull Requests mode** creates a Git pull request for each promotion and waits for the PR to be merged before deploying to the target org. The PR must be approved and merged through the Git hosting provider's interface (GitHub, GitLab, etc.). This mode is appropriate for teams that enforce code review through Git-native PR policies, use branch protection rules, or need audit trails stored in their Git platform rather than in Salesforce.

The two modes are mutually exclusive per pipeline. A pipeline cannot mix Work Items and Pull Request promotions across stages. Switching modes after pipeline creation requires reconfiguring the pipeline and completing or cancelling all active user story promotions first.

### Merge Order and Dependency Management

When multiple user stories are ready for promotion simultaneously, Copado Essentials promotes them in ascending User Story Reference number order by default. This order is deterministic but not semantically aware — it does not know that User Story 1015 must be deployed before User Story 1008 because 1015 creates a custom field that 1008 references in a formula or validation rule.

When promotion order matters due to metadata dependencies, the default order must be overridden using the merge order integer field on the User Story record. Lower integers promote first. Setting merge order is the supported mechanism for controlling promotion sequence. Attempting to work around it by manually merging branches outside Copado risks desynchronizing pipeline state and causing subsequent automated promotions to behave unexpectedly.

---

## Common Patterns

### Pattern: Setting Up a Three-Stage Pipeline

**When to use:** New Copado Essentials installation where no pipeline has been configured. Team has a Developer Integration sandbox, a UAT sandbox, and a Production org.

**How it works:**
1. In Copado Essentials Setup, authenticate three Salesforce org credentials — one per environment.
2. In the remote Git repository, create three environment branches: `develop`, `staging`, and `main`. These must exist before pipeline configuration.
3. Create a new Pipeline record. Name it to reflect the project or release stream.
4. Add three Pipeline Stages in order: Developer Integration (branch: `develop`) → UAT (branch: `staging`) → Production (branch: `main`). Assign the matching org credential to each stage.
5. Choose deployment mode: Work Items for teams needing in-app approvals; Pull Requests for teams enforcing Git-based review and branch protection.
6. Create a test User Story with the reference field populated, assign it to the pipeline, click "Create Feature Branch," and promote it through one stage to validate the end-to-end connection.

**Why not the alternative:** Skipping branch pre-creation causes the pipeline to fail on first promotion with a Git error that is easily mistaken for an authentication or permissions issue. Environment branches are not created by Copado — they must exist in Git before the pipeline references them.

### Pattern: Resolving Merge Conflicts in Work Items Mode

**When to use:** A user story promotion fails with a conflict indicator in Copado Essentials Work Items mode, indicating two user stories modified the same metadata component.

**How it works:**
1. Open the blocked User Story record. The promotion status field reflects the conflict state.
2. In the Copado Conflicts tab on the user story, review the list of conflicting components and identify which other user story owns the competing change.
3. Decide the resolution strategy: accept the incoming change (from the story being promoted), keep the current environment branch state, or manually merge both sets of changes into the feature branch.
4. If manual merge is required, pull the feature branch locally, resolve conflicts using a diff tool (VS Code, IntelliJ, or a Git client), and push the resolved branch back to the remote repository.
5. Return to the Copado UI and re-trigger the promotion. Copado re-evaluates the conflict state after each new push to the feature branch.

**Why not the alternative:** Deleting and re-creating the user story to bypass a conflict does not resolve the underlying branch divergence. The new story will encounter the same conflict because the Git history has not changed. Conflicts must be resolved at the Git branch level or through the Copado conflict resolution UI — skipping this step propagates broken metadata forward in the pipeline.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Team has admins or release managers who do not have Git client access | Work Items deployment mode | All promotion actions occur inside Salesforce; no Git tooling required for operators |
| Team enforces PR reviews and uses branch protection rules in GitHub or GitLab | Deployments with Pull Requests mode | Copado creates PRs that must be approved and merged in Git; audit trail stays in the Git platform |
| Two user stories modify the same Apex class and must deploy in a specific order | Set merge order integers on both user stories | Merge order field overrides default ascending reference-number order |
| Feature branch was manually merged to environment branch outside Copado | Re-sync the user story branch reference in Copado before next promotion | Manual merges outside Copado desynchronize pipeline state; Copado must be reconciled before automating further |
| User story branch creation fails with no error message | Verify user story reference field is populated and contains no spaces or special characters | Branch name is derived from the reference field; invalid characters produce silent failures |
| Promotion completes successfully but no changes appear in target org | Verify User Story Task records list the correct metadata components | Copado deploys based on task-tracked components, not a full-org comparison; empty task list means empty deployment |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner configuring or troubleshooting Copado Essentials:

1. **Verify installation and connectivity** — Confirm Copado Essentials is installed (Setup > Installed Packages) and note the version. Confirm the Git repository connection is active by checking the Copado Setup page for authentication status. Verify all org credentials authenticate successfully.
2. **Map environments to branches** — Confirm that every pipeline stage has a unique Salesforce org credential and a unique Git branch. Verify the environment branches exist in the remote Git repository. Document the stage order from lowest fidelity (dev) to highest fidelity (production).
3. **Confirm deployment mode** — Identify whether the pipeline uses Work Items or Pull Requests mode. All subsequent troubleshooting and operator instructions depend on which mode is active.
4. **Audit user story records** — For any user story that is not promoting correctly: verify the reference field is populated, verify at least one User Story Task record exists and references the correct metadata component, and confirm the user story is assigned to the correct pipeline and pipeline stage.
5. **Check for conflicts and merge order** — Review the Copado Conflicts tab for blocked stories. If multiple stories are queued for promotion, confirm merge order integers are set when promotion sequence matters due to metadata dependencies.
6. **Trigger and monitor promotion** — Initiate the promotion from the user story record or pipeline view. Monitor the deployment status in the Copado Deployment record. Review Salesforce Metadata API deployment errors in the detail view if the deploy step fails after the merge succeeds.
7. **Validate and document** — After successful promotion, confirm the target org reflects the expected component changes. Document any merge order overrides or conflict resolutions applied so future promotions can reference the decision rationale.

---

## Review Checklist

Run through these before marking a Copado Essentials pipeline configuration complete:

- [ ] Copado Essentials managed package is installed and the Git repository connection is authenticated
- [ ] All pipeline stages have a unique org credential and a unique Git branch assignment
- [ ] All environment branches (`develop`, `staging`, `main`) exist in the remote Git repository before pipeline configuration
- [ ] Deployment mode (Work Items or Pull Requests) is chosen, documented, and tested
- [ ] A test user story has been created with a populated reference field, branched, and promoted through at least one pipeline stage end-to-end
- [ ] User Story Task records are confirmed to track actual metadata components (not empty tasks)
- [ ] Merge order override process is documented for any known inter-story metadata dependencies
- [ ] Conflict resolution procedure is documented and accessible to the team for the deployment mode in use

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Feature branch naming uses the reference field, not the record name** — The branch name `feature/{user-story-number}` is derived from the user story reference field, not the record name or Salesforce record Id. If that field is empty, incorrectly formatted, or contains spaces and special characters, branch creation either fails silently or produces an invalid Git branch name. Always confirm the reference field is populated and contains only alphanumeric characters, hyphens, or underscores before clicking "Create Feature Branch."

2. **Switching deployment modes breaks in-flight user stories** — Changing the pipeline from Work Items to Pull Requests mode (or vice versa) does not migrate active in-flight user stories to the new mode. They retain the previous mode's expectations and will behave unpredictably. Complete or cancel all active promotions before changing deployment mode on a live pipeline.

3. **Environment branches must be pre-created; Copado does not create them** — Copado Essentials creates `feature/*` branches on demand when a developer clicks "Create Feature Branch," but it never creates environment branches (`develop`, `staging`, `main`). If an environment branch is missing in the remote Git repository, the first promotion to that stage fails with a Git error that is frequently misdiagnosed as an org credential or permissions issue. Create all environment branches in Git before configuring the pipeline.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Pipeline configuration review | Assessment of stage order, branch assignments, org credential mapping, and deployment mode with identified gaps |
| Promotion path map | Tabular or visual representation of pipeline environments in order with branch names, deployment mode, and approval requirements |
| Conflict resolution log | Record of conflicting components, the user stories owning competing changes, and the resolution applied to each conflict |
| Merge order override record | Documentation of merge order integers assigned to user stories with dependency relationships and the rationale for the chosen sequence |

---

## Related Skills

- devops/salesforce-devops-tooling-selection — Use when choosing between Copado Essentials and other DevOps platforms before committing to this skill's configuration guidance
- devops/git-branching-for-salesforce — Use to design the branching strategy that Copado Essentials pipeline stages will enforce
- devops/source-tracking-and-conflict-resolution — Use when conflicts involve source-tracked orgs or when conflict resolution requires understanding Salesforce source tracking behavior
- devops/release-management — Use alongside this skill to define the release cadence and approval gates the Copado pipeline will automate
