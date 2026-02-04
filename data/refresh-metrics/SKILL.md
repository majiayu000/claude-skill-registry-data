---
name: refresh-metrics
description: Auto-update status metrics across governance documents - scans MCP issues/specs to calculate current counts and percentages, updates README files and NEXT_STEPS with accurate data
---

# Refresh Governance Metrics

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: refresh-metrics | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: refresh-metrics | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



You are updating status metrics across all governance documents to reflect the current state of issues, specifications, and implementation progress.

## Purpose

Governance documents contain metrics that become stale:
- Issue counts by status/priority
- Specification completion percentages
- Feature implementation status (✅ ⚠️ ❌)
- Top projects by issue count
- Phase progress indicators

This skill automatically scans MCP data and updates all metric sections.

## Refresh Process

### Phase 1: Gather Current Data

**1. Get Issue Statistics**

Use `issues_list` to get all issues:

```typescript
// Get all issues
const allIssues = await issues_list({})

// Get issues by status
const openIssues = await issues_list({ status: "open" })
const inProgressIssues = await issues_list({ status: "in_progress" })
const closedIssues = await issues_list({ status: "closed" })
const cancelledIssues = await issues_list({ status: "cancelled" })

// Get issues by priority
const criticalIssues = await issues_list({ priority: "critical" })
const highIssues = await issues_list({ priority: "high" })
const mediumIssues = await issues_list({ priority: "medium" })
const lowIssues = await issues_list({ priority: "low" })

// Get issues by type
const bugIssues = await issues_list({ labels: ["bug"] })
const featureIssues = await issues_list({ labels: ["feature"] })
const technicalDebtIssues = await issues_list({ labels: ["technical-debt"] })
```

**2. Get Specification Statistics**

```typescript
// Get all specifications
const allSpecs = await issues_list({ type: "specification" })

// Get specs by status
const openSpecs = await issues_list({ type: "specification", status: "open" })
const inProgressSpecs = await issues_list({ type: "specification", status: "in_progress" })
const closedSpecs = await issues_list({ type: "specification", status: "closed" })

// Get specs by roadmap phase (if using phase labels)
const phase1Specs = await issues_list({ type: "specification", labels: ["phase-1"] })
const phase2Specs = await issues_list({ type: "specification", labels: ["phase-2"] })
```

**3. Identify Top Projects**

```typescript
// Get all unique project values
const projectCounts = {}
allIssues.forEach(issue => {
  if (issue.project) {
    projectCounts[issue.project] = (projectCounts[issue.project] || 0) + 1
  }
})

// Sort by count
const topProjects = Object.entries(projectCounts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 5)
```

**4. Calculate Percentages**

```typescript
const totalIssues = allIssues.length
const openPct = Math.round((openIssues.length / totalIssues) * 100)
const inProgressPct = Math.round((inProgressIssues.length / totalIssues) * 100)
const closedPct = Math.round((closedIssues.length / totalIssues) * 100)

const totalSpecs = allSpecs.length
const completedSpecsPct = Math.round((closedSpecs.length / totalSpecs) * 100)
```

### Phase 2: Update Issues README

**File**: `.wrangler/issues/README.md`

**Find and update Status section:**

```markdown
**Status**: X issues open, Y issues in progress, Z issues closed
```

Replace with:

```markdown
**Status**: [openIssues.length] issues open, [inProgressIssues.length] issues in progress, [closedIssues.length] issues closed
```

**Find and update Metrics section:**

```markdown
## Metrics (Auto-Updated)

**Total Issues**: [totalIssues]
**By Status**:
- Open: [openIssues.length] ([openPct]%)
- In Progress: [inProgressIssues.length] ([inProgressPct]%)
- Closed: [closedIssues.length] ([closedPct]%)
- Cancelled: [cancelledIssues.length] ([cancelledPct]%)

**By Priority**:
- Critical: [criticalIssues.length]
- High: [highIssues.length]
- Medium: [mediumIssues.length]
- Low: [lowIssues.length]

**Top Projects**:
1. [topProjects[0][0]]: [topProjects[0][1]] issues
2. [topProjects[1][0]]: [topProjects[1][1]] issues
3. [topProjects[2][0]]: [topProjects[2][1]] issues
```

**Update Last Updated date:**

```markdown
**Last Updated**: [current YYYY-MM-DD]
```

### Phase 3: Update Specifications README

**File**: `.wrangler/specifications/README.md`

**Find and update Status section:**

```markdown
**Status**: X specifications active, Y specifications completed, Z specifications archived
```

Replace with:

```markdown
**Status**: [openSpecs.length + inProgressSpecs.length] specifications active, [closedSpecs.length] specifications completed, [cancelledSpecs.length] specifications archived
```

**Find and update Metrics section:**

```markdown
## Metrics (Auto-Updated)

**Total Specifications**: [totalSpecs]

**By Status**:
- Open (Design): [openSpecs.length] ([openSpecsPct]%)
- In Progress: [inProgressSpecs.length] ([inProgressSpecsPct]%)
- Closed (Complete): [closedSpecs.length] ([closedSpecsPct]%)
- Cancelled: [cancelledSpecs.length] ([cancelledSpecsPct]%)

**By Roadmap Phase**:
- Phase 1: [phase1Specs.length] specs
- Phase 2: [phase2Specs.length] specs
- Phase 3: [phase3Specs.length] specs

**Constitutional Compliance**:
- All specifications reviewed: [specsWithConstitutionalAlignment]/[totalSpecs] ([compliancePct]%)
- Principles coverage: [most referenced principles]
```

**Update Last Updated date:**

```markdown
**Last Updated**: [current YYYY-MM-DD]
```

### Phase 4: Update Roadmap Next Steps

**File**: `.wrangler/ROADMAP_NEXT_STEPS.md`

**This is the most complex update - requires analyzing feature implementation status**

**1. Read Current Next Steps File**

```bash
cat .wrangler/ROADMAP_NEXT_STEPS.md
```

**2. Scan for Feature Status Sections**

Identify features in three categories:
- ✅ Fully Implemented Features
- ⚠️ Partially Implemented Features
- ❌ Not Implemented Features

**3. For Each Feature, Determine Current Status**

**Heuristic for feature status**:

```typescript
function getFeatureStatus(featureName) {
  // Search for related specification
  const spec = await issues_search({ query: featureName, type: "specification" })

  if (spec && spec.status === "closed") {
    return "fully_implemented"
  }

  // Search for related issues
  const issues = await issues_search({ query: featureName })
  const openIssues = issues.filter(i => i.status === "open")
  const completedIssues = issues.filter(i => i.status === "closed")

  if (completedIssues.length > 0 && openIssues.length === 0) {
    return "fully_implemented"
  } else if (completedIssues.length > 0 && openIssues.length > 0) {
    return "partially_implemented"
  } else {
    return "not_implemented"
  }
}
```

**4. Calculate Overall Completion Percentage**

```typescript
// Count features in each category
const fullyImplemented = [count from ✅ section]
const partiallyImplemented = [count from ⚠️ section]
const notImplemented = [count from ❌ section]
const totalFeatures = fullyImplemented + partiallyImplemented + notImplemented

// Calculate weighted percentage
// Fully = 100%, Partially = 50%, Not = 0%
const overallPct = Math.round(
  ((fullyImplemented * 100) + (partiallyImplemented * 50)) / totalFeatures
)
```

**5. Update Executive Summary**

```markdown
### Current State
- ✅ [fullyImplemented]/[totalFeatures] features fully implemented ([fullyPct]%)
- ⚠️ [partiallyImplemented]/[totalFeatures] features partially implemented ([partiallyPct]%)
- ❌ [notImplemented]/[totalFeatures] features not implemented ([notPct]%)
- 📊 Overall: ~[overallPct]% complete
```

**6. Update Last Updated**

```markdown
**Last Updated By**: Claude Code (refresh-metrics skill)
**Next Review**: [current date + 30 days]
```

### Phase 5: Verify Constitutional Compliance

**Scan specifications for constitutional alignment sections:**

```bash
# Count specs with constitutional alignment
grep -l "Constitutional Alignment" .wrangler/specifications/*.md | wc -l
```

**Calculate compliance percentage:**

```typescript
const specsWithAlignment = [count from grep]
const compliancePct = Math.round((specsWithAlignment / totalSpecs) * 100)
```

**Update in Specifications README:**

```markdown
**Constitutional Compliance**:
- All specifications reviewed: [specsWithAlignment]/[totalSpecs] ([compliancePct]%)
```

**If <100%, add note:**

```markdown
⚠️ [totalSpecs - specsWithAlignment] specifications missing Constitutional Alignment section
```

### Phase 6: Extract Principle Coverage

**Scan specifications to see which principles are most referenced:**

```bash
# Count references to each principle
grep -h "Principle 1\|Principle 2\|Principle 3" .wrangler/specifications/*.md | sort | uniq -c | sort -rn
```

**Update Specifications README with most referenced principles:**

```markdown
**Principles coverage**: Most referenced: Principle 1 (X specs), Principle 3 (Y specs), Principle 5 (Z specs)
```

## Automated Calculations

### Issue Velocity (Optional Advanced Metric)

**Calculate weekly close rate:**

```typescript
// Get issues closed in last 7 days
const oneWeekAgo = new Date()
oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)

const recentlyClosedIssues = closedIssues.filter(issue => {
  const closedDate = new Date(issue.updatedAt)
  return closedDate >= oneWeekAgo
})

const weeklyVelocity = recentlyClosedIssues.length
```

**Add to Issues README Metrics section (optional):**

```markdown
**Velocity**:
- Issues closed (last 7 days): [weeklyVelocity]
- Average time to close: [calculate average if possible]
```

### Specification Completion Trend

**Calculate trend over time:**

```typescript
// Compare current completion % with last known %
// If increasing: 📈
// If decreasing: 📉
// If stable: ➡️
```

**Add trend indicator to Next Steps:**

```markdown
- 📊 Overall: ~[overallPct]% complete [📈/📉/➡️ vs last month]
```

## Update Report

After completing all updates, generate summary:

```markdown
# Metrics Refresh Complete

**Date**: [YYYY-MM-DD]
**Files Updated**: 3

---

## Summary of Changes

### Issues README (.wrangler/issues/README.md)

**Previous**:
- Total Issues: [old count]
- Open: [old count]
- Closed: [old count]

**Updated to**:
- Total Issues: [new count] ([+/- change])
- Open: [new count] ([+/- change])
- Closed: [new count] ([+/- change])

**Top Projects Updated**: [list]

### Specifications README (.wrangler/specifications/README.md)

**Previous**:
- Total Specs: [old count]
- Completed: [old count] ([old %])

**Updated to**:
- Total Specs: [new count] ([+/- change])
- Completed: [new count] ([new %])

**Constitutional Compliance**: [X]% ([+/- change])

### Next Steps (ROADMAP_NEXT_STEPS.md)

**Previous Overall Completion**: ~[old %]%

**Updated Overall Completion**: ~[new %]% ([+/- change])

**Features Moved**:
- ❌ → ⚠️: [list features that started implementation]
- ⚠️ → ✅: [list features that completed]

---

## Current Project Health

**Issue Backlog**: [open + in_progress count] active issues
**Specification Pipeline**: [open + in_progress specs count] active specs
**Implementation Progress**: ~[overall %]% complete

**Velocity** (if calculated):
- [weeklyVelocity] issues closed last 7 days

**Constitutional Compliance**: [compliancePct]% of specs have alignment sections

---

## Recommendations

[Based on metrics, provide recommendations:]

**If backlog growing**: Consider reducing scope or increasing velocity
**If completion % declining**: Review roadmap priorities
**If constitutional compliance <100%**: Update missing specs with alignment sections
**If no recent closes**: Check if issues are blocked

---

**Next Metrics Refresh**: [current date + 30 days]
```

## Edge Cases

### No Issues Exist Yet

**Situation**: Fresh project with no MCP issues

**Response**:
```markdown
**Status**: No issues tracked yet

**Metrics**: N/A - Use `issues_create` to begin tracking work
```

Keep README structure, just show zeros/N/A for metrics.

### Specifications Without Phase Labels

**Situation**: Specs don't have `phase-1`, `phase-2` labels

**Response**:
- Skip "By Roadmap Phase" section in metrics
- Add note: "⚠️ Specs not labeled with roadmap phases - consider adding phase labels"

### Next Steps File Uses Custom Structure

**Situation**: User modified Next Steps structure significantly

**Response**:
1. Detect standard sections (✅ ⚠️ ❌)
2. Update Executive Summary only
3. Leave custom sections untouched
4. Add note: "Custom Next Steps structure detected - manual review recommended"

### Conflicting Data

**Situation**: Spec says "closed" but has open issues

**Response**:
- Mark as partially implemented (⚠️)
- Add note: "Spec closed but [N] issues remain open"
- Suggest user review

## Success Criteria

Metrics refresh is complete when:

- [ ] Issues README metrics updated with current counts
- [ ] Issues README "Last Updated" date set to today
- [ ] Specifications README metrics updated
- [ ] Specifications README "Last Updated" date set to today
- [ ] Next Steps executive summary updated with current %
- [ ] Next Steps "Last Updated By" set to "Claude Code (refresh-metrics skill)"
- [ ] Constitutional compliance % calculated and updated
- [ ] Top projects list updated
- [ ] Update report generated and presented

## Automation Frequency

**Recommended schedule**:
- **Manual refresh**: When metrics seem stale (>30 days)
- **After major milestones**: Spec completion, phase transitions
- **Monthly**: Regular cadence for project health visibility
- **Before reviews**: Prior to stakeholder reviews or planning sessions

**Can be triggered by**:
- Direct invocation: "Refresh governance metrics"
- Housekeeping skill: As part of regular cleanup
- verify-governance skill: If metrics flagged as stale

## Related Skills

- **verify-governance** - Detects stale metrics and recommends this skill
- **housekeeping** - Can invoke this as part of regular maintenance
- **check-constitutional-alignment** - Uses compliance metrics calculated here

## Important Notes

**Read-only scanning**: This skill uses MCP `issues_list` and `issues_search` (read operations only) - never modifies issue data, only updates metric sections in markdown files.

**Preserve user content**: When updating README files, only replace metric sections - never delete user-added content.

**Percentage rounding**: Always round to nearest integer for readability.

**Trend indicators**: Only show trends if you have historical data to compare.

## Remember

Accurate metrics are essential for governance effectiveness. Stale data leads to poor decisions. Make refresh easy and automatic so it becomes routine maintenance, not a burden.
