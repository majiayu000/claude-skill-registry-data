---
name: triage-github-issues
description: Systematically triage incoming GitHub issues for the docent project
group: github
author: "@tnez"
version: 1.0.0
keywords: [github, issues, triage, maintenance]
---

# Runbook: Triage GitHub Issues

**Purpose:** Systematically triage incoming GitHub issues for the docent project
**Owner:** Maintainer Team (@tnez)
**Last Updated:** 2025-10-20
**Frequency:** Daily or when new issues arrive

## Overview

This runbook guides maintainers through triaging new GitHub issues, ensuring they are properly categorized, assigned priorities, checked for duplicates, and aligned with project goals. The workflow integrates with docent's documentation structure (PRDs, RFCs, ADRs) to make informed decisions about issue incorporation.

**What this runbook covers:**

- Finding untriaged issues
- Evaluating issue quality and completeness
- Checking for duplicates
- Aligning with project roadmap (PRDs)
- Determining next steps (RFC, ADR, implementation)
- Applying labels and milestones
- Expected duration: 5-10 minutes per issue

## Prerequisites

### Required Access

- [ ] Write access to `tnez/docent` repository
- [ ] GitHub CLI (`gh`) authenticated

### Required Tools

- `gh` CLI (GitHub CLI) - version 2.0 or higher
- `docent` CLI - installed locally
- Text editor for reviewing issues
- Web browser for detailed issue viewing

### Required Knowledge

- Familiarity with docent's PRDs (in `../prds/`)
- Understanding of RFC → ADR → Implementation workflow
- Knowledge of existing features and roadmap

### Pre-Flight Checklist

Before starting, ensure:

- [ ] You have reviewed recent PRDs and RFCs
- [ ] You understand current sprint/milestone priorities
- [ ] GitHub CLI is authenticated (`gh auth status`)
- [ ] You're in the docent project directory
- [ ] You have 15-30 minutes for triage session

## Procedure

### Step 1: Find Untriaged Issues

**Purpose:** Identify issues that haven't been reviewed yet

**Commands:**

```bash
# List issues without 'triaged' label (untriaged)
gh issue list --label "!triaged" --limit 20

# List issues with 'triage-needed' label (explicitly needs triage)
gh issue list --label "triage-needed" --limit 20

# List all open issues sorted by creation date (oldest first)
gh issue list --state open --json number,title,createdAt,labels \
  --jq 'sort_by(.createdAt) | .[] | "\(.number)\t\(.title)\t\(.labels | map(.name) | join(","))"'
```

**Validation:**

- Output shows list of issues needing triage
- Issue numbers, titles, and current labels displayed

**If step fails:**

- Verify you're in the docent repo directory
- Check GitHub CLI auth: `gh auth status`
- Check network connectivity

---

### Step 2: Review Issue Details

**Purpose:** Understand the issue content, context, and quality

**Commands:**

```bash
# View issue in terminal
gh issue view <ISSUE_NUMBER>

# View issue in browser for better formatting
gh issue view <ISSUE_NUMBER> --web

# Check if filed via docent tool (look for metadata in body)
gh issue view <ISSUE_NUMBER> --json body --jq '.body' | grep -i "docent version\|filed via docent"
```

**Quality Checklist:**

Evaluate the issue:

- [ ] **Clear title** - Descriptive and specific?
- [ ] **Type identified** - Bug, feature, question, or documentation?
- [ ] **Description provided** - Sufficient detail to understand?
- [ ] **Context included** - Version, OS, environment? (especially for bugs)
- [ ] **Reproduction steps** - For bugs, can it be reproduced?
- [ ] **Use case** - For features, is the motivation clear?

**Validation:**

- Issue is complete enough to act on
- Issue type is clear (bug/feature/question/docs)

**If issue is incomplete:**

```bash
# Request more information
gh issue comment <ISSUE_NUMBER> --body "Thanks for filing this issue! Could you provide additional details:

- [What specific information needed]
- [What specific information needed]

This will help us better understand and address your request."

# Apply 'needs-info' label
gh issue edit <ISSUE_NUMBER> --add-label "needs-info"
```

---

### Step 3: Check for Duplicates

**Purpose:** Avoid duplicate work by finding similar issues

**Commands:**

```bash
# Search for similar issues by keyword
gh issue list --search "<keywords from issue title>" --state all --limit 10

# Search closed issues too (may have been addressed)
gh issue list --search "<keywords>" --state closed --limit 5

# Use GitHub search via browser for more nuanced queries
gh issue view <ISSUE_NUMBER> --web
# Then use GitHub's search: is:issue [keywords]
```

**Evaluation:**

- Review similar issues found
- Check if exact duplicate exists
- Check if related issues provide context
- Check if issue was previously closed as wontfix

**If duplicate found:**

```bash
# Comment with link to original
gh issue comment <ISSUE_NUMBER> --body "Thanks for reporting this! This appears to be a duplicate of #<ORIGINAL_ISSUE>.

Closing as duplicate. Please follow the original issue for updates."

# Close as duplicate
gh issue close <ISSUE_NUMBER> --reason "not planned"
```

**If related but not duplicate:**

```bash
# Link the issues
gh issue comment <ISSUE_NUMBER> --body "Related to #<RELATED_ISSUE>"
```

---

### Step 4: Categorize and Label

**Purpose:** Apply appropriate labels for issue organization

**Standard Labels:**

- **Type:** `bug`, `enhancement`, `question`, `documentation`
- **Priority:** `priority-high`, `priority-medium`, `priority-low`
- **Status:** `triaged`, `needs-info`, `good-first-issue`, `help-wanted`
- **Component:** `mcp`, `cli`, `templates`, `docs`, `ci-cd`
- **Workflow:** `needs-rfc`, `needs-adr`, `ready-for-implementation`

**Commands:**

```bash
# Apply type label (choose one)
gh issue edit <ISSUE_NUMBER> --add-label "bug"
gh issue edit <ISSUE_NUMBER> --add-label "enhancement"
gh issue edit <ISSUE_NUMBER> --add-label "question"
gh issue edit <ISSUE_NUMBER> --add-label "documentation"

# Apply component label (can be multiple)
gh issue edit <ISSUE_NUMBER> --add-label "mcp"
gh issue edit <ISSUE_NUMBER> --add-label "cli"

# Apply priority based on impact and urgency
gh issue edit <ISSUE_NUMBER> --add-label "priority-high"    # Critical bugs, major features
gh issue edit <ISSUE_NUMBER> --add-label "priority-medium"  # Standard issues
gh issue edit <ISSUE_NUMBER> --add-label "priority-low"     # Nice-to-haves

# Mark as triaged
gh issue edit <ISSUE_NUMBER> --add-label "triaged"

# Remove 'triage-needed' if present
gh issue edit <ISSUE_NUMBER> --remove-label "triage-needed"
```

**Priority Guidelines:**

- **High:** Security issues, data loss bugs, breaking changes, blocker for releases
- **Medium:** Important features, non-critical bugs, user experience improvements
- **Low:** Minor improvements, documentation tweaks, edge cases

**Validation:**

- Issue has appropriate type label
- Issue has priority label
- Issue has 'triaged' label
- Component labels applied if relevant

---

### Step 5: Align with Project Direction

**Purpose:** Determine if issue aligns with docent's goals and roadmap

**Commands:**

```bash
# Review active PRDs
ls -l docs/prds/

# Search PRDs for related concepts
grep -r "<issue keywords>" docs/prds/

# Check for related RFCs
ls -l docs/rfcs/ | grep -i "<keywords>"

# Use docent analyze to understand current project focus
docent analyze
```

**Decision Matrix:**

| Issue Type | In PRD/Roadmap? | Action |
|------------|----------------|--------|
| **Enhancement** | ✅ Yes | Label `aligned-with-roadmap`, proceed to Step 6 |
| **Enhancement** | ❌ No | Evaluate strategic fit (see below) |
| **Bug** | N/A | Always proceed (fix regardless of roadmap) |
| **Question** | N/A | Answer and consider if docs need improvement |
| **Documentation** | N/A | Always consider (docs always welcomed) |

**Strategic Fit Evaluation (for features not in roadmap):**

Ask:

1. Does this align with docent's core mission? (Documentation intelligence for AI agents)
2. Would this benefit multiple users or one specific use case?
3. Is this a reasonable scope expansion or feature creep?
4. Does it conflict with existing architecture or decisions (check ADRs)?

**If aligned with mission:**

```bash
# Label as worthy of consideration
gh issue edit <ISSUE_NUMBER> --add-label "consider-for-roadmap"

# Comment on potential path forward
gh issue comment <ISSUE_NUMBER> --body "This is an interesting idea that could align with docent's mission.

Potential path forward:
- [ ] Create RFC to explore design
- [ ] Get community feedback
- [ ] Consider for next roadmap planning cycle

Would you be interested in drafting an RFC for this?"
```

**If not aligned:**

```bash
# Explain politely and close
gh issue comment <ISSUE_NUMBER> --body "Thank you for this suggestion! After reviewing, this doesn't align with docent's current focus on [core mission].

Some alternatives:
- [Alternative approach that does align]
- [External tool that might help]

Closing for now, but feel free to discuss further if you think we're missing something."

gh issue close <ISSUE_NUMBER> --reason "not planned"
```

---

### Step 6: Determine Next Steps

**Purpose:** Route issue to appropriate workflow stage

**Workflow Stages:**

1. **Needs RFC** - Complex features requiring design discussion
2. **Needs ADR** - Architectural decisions required
3. **Ready for Implementation** - Clear requirements, can be implemented
4. **Needs Discussion** - Requires community/team input before deciding

**Decision Tree:**

```
Is this a bug?
├─ Yes → Label 'ready-for-implementation', assign milestone
└─ No (it's a feature)
   │
   ├─ Is design straightforward?
   │  ├─ Yes → Label 'ready-for-implementation'
   │  └─ No → Does it need architectural decisions?
   │     ├─ Yes → Label 'needs-rfc', 'needs-adr'
   │     └─ No → Label 'needs-rfc'
   │
   └─ Is there controversy or uncertainty?
      ├─ Yes → Label 'needs-discussion'
      └─ No → Proceed with RFC/implementation path
```

**Commands:**

```bash
# For bugs - mark ready
gh issue edit <ISSUE_NUMBER> --add-label "ready-for-implementation"

# For features needing RFC
gh issue edit <ISSUE_NUMBER> --add-label "needs-rfc"

# For features needing architectural decisions
gh issue edit <ISSUE_NUMBER> --add-label "needs-adr"

# For uncertain/controversial items
gh issue edit <ISSUE_NUMBER> --add-label "needs-discussion"

# Assign to milestone (if ready)
gh issue edit <ISSUE_NUMBER> --milestone "v0.8.0"
```

**Comment with Next Steps:**

```bash
# For RFC path
gh issue comment <ISSUE_NUMBER> --body "Thanks for this suggestion! This would benefit from an RFC to explore the design.

Next steps:
1. Draft RFC following template in \`docs/rfcs/rfc-NNNN-template.md\`
2. Discuss design trade-offs and alternatives
3. Decide on approach
4. Create ADR if architectural changes needed
5. Implement

Would you like to draft the RFC, or should a maintainer take this on?"

# For ready implementation
gh issue comment <ISSUE_NUMBER> --body "This looks straightforward to implement. Marking as ready for implementation.

If you're interested in contributing, see our [contributing guide](.docent/guides/contributing.md)!"

# For discussion
gh issue comment <ISSUE_NUMBER> --body "This is an interesting idea that needs broader discussion. Adding to the agenda for the next maintainer sync.

Community members: please share your thoughts on this proposal!"
```

**Validation:**

- Issue has workflow label (needs-rfc, needs-adr, or ready-for-implementation)
- Next steps are clear in comments
- If ready, milestone assigned

---

### Step 7: Assign or Tag for Help

**Purpose:** Route work to appropriate people or signal availability for contributors

**Commands:**

```bash
# Assign to yourself if you'll work on it
gh issue edit <ISSUE_NUMBER> --add-assignee "@me"

# Tag as good first issue (simple, well-defined)
gh issue edit <ISSUE_NUMBER> --add-label "good-first-issue"

# Tag as help wanted (community contributions welcome)
gh issue edit <ISSUE_NUMBER> --add-label "help-wanted"

# Mention someone who might be interested
gh issue comment <ISSUE_NUMBER> --body "CC @username - this relates to the work you did on #<RELATED_ISSUE>"
```

**Good First Issue Criteria:**

- Well-defined scope (< 4 hours work)
- Clear requirements
- Doesn't require deep architectural knowledge
- Has examples or patterns to follow
- Low risk of breaking changes

**Validation:**

- Issue is assigned OR labeled for community contribution
- Labels reflect contributor suitability

---

## Validation

After completing triage for an issue, verify:

1. **Labels Applied:**

   ```bash
   gh issue view <ISSUE_NUMBER> --json labels --jq '.labels[].name'
   ```

   Should include:
   - Type label (bug/enhancement/question/documentation)
   - 'triaged' label
   - Priority label
   - Workflow label (needs-rfc/needs-adr/ready-for-implementation)

2. **Next Steps Clear:**
   - Comments explain what happens next
   - If RFC needed, template link provided
   - If ready for implementation, contributing guide linked

3. **Alignment Checked:**
   - Compared against PRDs/roadmap
   - Strategic fit evaluated
   - Not duplicate of existing issue

4. **Proper Categorization:**
   - Milestone assigned (if ready for upcoming release)
   - Assignee set (if someone taking it on)
   - Component labels applied

## Rollback

If you need to undo triage decisions:

### Remove Labels

```bash
# Remove incorrect labels
gh issue edit <ISSUE_NUMBER> --remove-label "label-name"
```

### Change Priority

```bash
# Remove old priority
gh issue edit <ISSUE_NUMBER> --remove-label "priority-low"

# Add new priority
gh issue edit <ISSUE_NUMBER> --add-label "priority-high"
```

### Reopen Closed Issue

```bash
# Reopen if closed incorrectly
gh issue reopen <ISSUE_NUMBER>

# Add comment explaining
gh issue comment <ISSUE_NUMBER> --body "Reopening - [reason for reopening]"
```

## Troubleshooting

### Common Issues

#### Issue 1: Can't Determine Issue Type

**Symptoms:**

- Vague title and description
- Could be bug or feature
- Unclear what user wants

**Resolution:**

```bash
gh issue comment <ISSUE_NUMBER> --body "Thanks for reporting this! To help us better understand, could you clarify:

- Is this a bug (something broken) or a feature request (something new)?
- If bug: What did you expect vs. what happened?
- If feature: What use case would this support?

This will help us properly categorize and prioritize."

gh issue edit <ISSUE_NUMBER> --add-label "needs-info"
```

---

#### Issue 2: Conflicts with Existing Architecture

**Symptoms:**

- Feature request contradicts ADR decision
- Requires significant architectural changes
- May break backward compatibility

**Resolution:**

```bash
gh issue comment <ISSUE_NUMBER> --body "This suggestion conflicts with [ADR-NNNN](.docent/adr/adr-NNNN.md) where we decided [decision].

The trade-offs were:
- [Trade-off 1]
- [Trade-off 2]

If you think we should revisit this decision:
1. Review the ADR rationale
2. Explain what's changed or what was overlooked
3. We can draft a new RFC to reconsider

Alternatively, [suggest workaround that aligns with architecture]"

gh issue edit <ISSUE_NUMBER> --add-label "needs-discussion"
```

---

#### Issue 3: Large Feature with Unclear Scope

**Symptoms:**

- Feature request is too broad
- Would require significant design work
- Multiple ways to implement

**Resolution:**

```bash
gh issue comment <ISSUE_NUMBER> --body "This is a substantial feature that needs careful design consideration.

Let's break this down:
1. What's the core problem you're trying to solve?
2. What's the minimal feature that would provide value?
3. What are nice-to-haves vs. must-haves?

Once we clarify scope, we can:
- Draft an RFC to explore design options
- Break into smaller, implementable issues
- Prioritize phases

Would you be willing to draft an RFC, or should we schedule a discussion?"

gh issue edit <ISSUE_NUMBER> --add-label "needs-rfc,needs-discussion"
```

---

### When to Escalate

Escalate to project lead (@tnez) if:

- Issue relates to security or privacy concerns
- Major architectural decision required (may affect ADRs)
- Controversial community feedback
- Unclear if issue aligns with project mission
- Legal or licensing questions

**Escalation Method:**

- Tag @tnez in issue comment
- Use "needs-discussion" label
- Bring to next maintainer sync

## Post-Procedure

After triaging a batch of issues:

- [ ] Update triage dashboard (if exists) or tracking document
- [ ] Note any patterns (common feature requests, recurring bugs)
- [ ] Consider creating meta-issues for themes (e.g., "Improve error messages")
- [ ] Update this runbook if new edge cases discovered
- [ ] Take break - triage is mentally taxing!

## Notes

**Important Notes:**

- **Be kind and welcoming** - Every issue represents someone taking time to engage
- **Thank reporters** - Even if closing, thank them for participation
- **Explain decisions** - Help people understand why issues are prioritized certain ways
- **Link liberally** - Point to PRDs, RFCs, ADRs, contributing guides
- **Encourage contribution** - If someone files an issue, they might implement it!

**Gotchas:**

- Don't assume context - What's obvious to maintainers may not be obvious to reporters
- Watch for drive-by feature requests - Politely redirect to use cases and motivation
- Balance responsiveness with thoughtfulness - Quick triage is good, but don't rush decisions
- Revisit periodically - Issue priorities change as project evolves

**Related Procedures:**

- [Contributing Guide](../guides/contributing.md) - For pointing contributors to guidelines
- [CI/CD Health Check](ci-cd-health-check.md) - When issues relate to builds

**Integration with RFC-0010:**

Issues filed via the `file-issue` tool will:

- Include rich context (version, OS, etc.) automatically
- Follow templates for better structure
- Have preliminary labels applied
- Still require triage using this runbook for prioritization and routing

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-10-20 | @tnez | Initial creation to support issue triage workflow |

---

**This runbook ensures consistent, thoughtful triage of docent issues, maintaining project quality while welcoming community contribution.**
