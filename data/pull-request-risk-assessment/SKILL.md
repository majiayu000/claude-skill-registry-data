---
name: pull-request-risk-assessment
description: "Evaluate pull request changes against Lime's Change Management risk assessment criteria. Use when asked to assess risk of a PR or branch."
---

# Pull Request Risk Assessment

Use this skill when the user asks you to:
- Assess the risk of a pull request or branch
- Evaluate changes against the Change Management policy
- Determine if special rollout/rollback plans are needed
- Classify a change as Low or High risk

## When to Use

- Before merging significant changes
- When reviewing infrastructure or shared solution changes
- When the user explicitly asks for a "risk assessment"
- As part of a comprehensive PR review (linked from pr-review-code skill)

## Risk Assessment Process

### 1. Understand the Changes

First, gather information about what's being changed:

```bash
# View commits on the branch
git log --oneline main..HEAD

# View changed files and stats
git diff main..HEAD --stat

# View the full diff
git diff main..HEAD
```

### 2. Classify the Change Type

Determine which category the change falls into:

1. **Infrastructure changes** - Docker, Consul, Logstash, Terraform, etc.
2. **Changes to solution-cloud-shared** - Shared deployment configuration
3. **Changes to isolated solutions** - Standard application code

### 3. Apply Risk Criteria

Evaluate the change against the risk criteria below and assign a risk level.

### 4. Provide Recommendation

Based on the risk level:
- **Low risk**: Standard deployment process is appropriate
- **High risk**: Document rollout plan, verification plan, and rollback plan

---

## Change Management Policy Reference

This document describes how the engineering department at Lime works with change management in Lime CRM Cloud. Every change must be linked to an issue in Github so that it can be tracked. We are utilizing templates to encourage useful issues and pull requests. This helps us ensure that we do change management in a good way.

We have 3 categories of changes, each having its own process:

1. Infrastructure changes
1. Changes to solution-cloud-shared
1. Changes to isolated solutions

### Risk assessment

An initial, qualitative, assessment of any risk to the business and/or information security caused by the implementation of the change is performed. A risk level is assigned based on the following criteria:

| Level | Criteria |
|-------|----------|
| Low   | Little or no risk to the business or information security |
| High  | Could affect a large number of customers or information security negatively to a large degree, a large degree of uncertainty of results, results not feasible to test or verify beforehand. See below for examples. |

Examples of _High_ risk changes include:
* Database migrations
* Changes to Docker Swarm, Consul, Logstash
* Large uncertainty / hard to test in staging/test environment

### Infrastructure changes

Issues describing a change to our infrastructure have a description with the following content to ensure that we treat potential risks in a good way:

```md
Description: ...
Risk (low/high)

If high:
    Rollout plan
    Verification plan
    Rollback plan

Perform outside business hours: Y/N
```

#### Example issue

```md
# Upgrade RabbitMQ to the latest version

## Description
RabbitMQ in production is version X and contains known security vulnerabilities. It should be updated to version Y within the next few weeks.

## Risk Level: High

This is a major version update. While tested in the staging environment with great success, load testing in the staging environment cannot easily be performed for this change.

## Perform outside business hours: Yes
The time estimated for rollout is 2 hrs

## Rollout:
1. [ ] Run terraform apply script.
2. [ ] Ensure that changes are propagated to all nodes in the cluster.

## Verification:
1. [ ] Check that the version number in the RabbitMQ admin interface has been updated to the new version for all nodes.
1. [ ] Ensure that Lime CRM services are operational and that messages are consumed.
1. [ ] Check that error logs are empty.

## Rollback plan:
1. [ ] Revert commit + PR.
1. [ ] Run terraform apply script.
1. [ ] Re-run verification steps and ensure that the correct (previous) version is reported.
```

#### Emergency changes

Example change:

* Directly updating a container image via Portainer
* Changing code in a running container to solve an urgent problem

Emergency changes have to be performed and verbally approved by at least 2 engineers.

Any emergency change must be documented in an issue, reviewed, and put into version control after the emergency.

### Solution changes

* We're using semantic release, which means that a new release automatically gets the correct version, based on the commit history.
* A new PR is automatically created in lime-crm, every time a new release is created for lime-webclient and/or lime-core. Merging this PR creates a new version of lime-crm.
* A new PR is automatically created in solution-cloud-shared, every time a new version of lime-crm is released.
* Deploying a new version means merging this PR and manually running the `lime-project deploy` script.

#### Deployment checklist for solution-cloud-shared (PR template)

PR:s generated in solution-cloud-shared has a deployment checklist, that you need to check before merging/releasing.

### Isolated solutions

Isolated solutions are automatically updated to a new version when a new lime-crm version is marked as `official`.

The decision to set a lime-CRM version as the official is made by a group of people:

* 1 Principal engineer
* 1 Product owner
* 1 person from the support department

Isolated solutions can also be manually updated. The process is described in greater detail [here](https://prime.lime.tech/products/limecrm/clouddeployment).

---

## Output Format

When providing a risk assessment, use this format:

```markdown
## Risk Assessment: [Feature/Change Name]

### Summary of Changes
- [Brief bullet points of what changed]
- [Number of files, lines added/removed]
- [Key components affected]

### Risk Level: **[Low/High]**

### Justification

| Criteria | Assessment |
|----------|------------|
| **Customer Impact** | [Assessment] |
| **Information Security** | [Assessment] |
| **Uncertainty / Testability** | [Assessment] |
| **Infrastructure Impact** | [Assessment] |
| **Rollback Complexity** | [Assessment] |

### Key Observations
1. [Observation 1]
2. [Observation 2]
3. ...

### Recommendation
[Standard deployment / Requires rollout+verification+rollback plans]

[If High risk, include suggested plans]
```

## Quick Reference Checklist

When assessing risk, ask yourself:

- [ ] Does this change database schema or migrations?
- [ ] Does this affect Docker, Consul, Logstash, or other infrastructure?
- [ ] Could this negatively affect a large number of customers?
- [ ] Is there significant uncertainty about the results?
- [ ] Is it difficult to test in staging/test environment?
- [ ] Are there security implications?
- [ ] Is there an easy rollback path?
- [ ] Is the change behind a feature flag/switch?

**If any of the first 6 are "yes" without mitigating factors, consider High risk.**
