---
name: daily-summary
version: 1.0.1
description: Use when preparing daily standups or status reports - automates PR summary generation with categorization, metrics, and velocity analysis; eliminates manual report compilation and ensures consistent format
triggers:
  - daily standup
  - PR summary
  - status report
  - progress tracking
  - gh pr list
---

# Daily Summary Skill

This skill automates the generation of comprehensive daily Pull Request (PR) summaries for team standups, status reports, and progress tracking. It produces structured markdown reports with metrics, categorization, contributor activity analysis, and velocity tracking.

## When to Use This Skill

Use this skill when you need:

- Daily standup preparation with current PR status
- End-of-day progress reporting for stakeholders
- Project status updates with metrics
- PR activity analysis and trends
- Weekly or monthly sprint retrospectives
- Contributor focus and productivity analysis

## When NOT to Use This Skill

Skip this skill when:

- **Real-time PR monitoring** - Use GitHub notifications or `gh pr status` instead
- **Individual PR details** - Use `gh pr view <number>` for single PR inspection
- **Non-GitHub repositories** - This skill requires GitHub-hosted projects
- **Missing `gh` CLI** - Installation of GitHub CLI is mandatory (see Dependencies)
- **Ad-hoc queries** - Use direct `gh` commands for one-off questions
- **Live collaboration** - Use GitHub web interface for interactive review sessions

## What This Skill Provides

Automated generation of structured markdown reports including:

- **Key Metrics** - PRs created/merged/open, active contributors
- **Categorized PR Lists** - Performance, Bug Fixes, Features, UI/UX, Documentation
- **Contributor Activity** - Breakdown by developer with focus areas
- **Highlights and Themes** - Grouped work patterns
- **Impact Summary** - Code quality, UX improvements, developer experience
- **Velocity Metrics** - Average time to merge, review turnaround
- **Action Items** - PRs ready for review, blockers, backlog items

## Dependencies

### Required Tools

- **GitHub CLI (`gh`)** - Required for fetching PR data
  ```bash
  # Install: https://cli.github.com/
  # Verify: gh --version
  ```

### Optional Tools

- **jq** - JSON processing for advanced filtering (recommended but not required)

### Bundled Resources

This skill includes:

- `assets/daily-pr-summary-template.md` - Output format specification
- `references/agent-instructions.md` - Agent framework methodology context
- `references/agent-definitions.md` - Terminology and behavioral principles

## The Seven Steps (MANDATORY)

### Step 1: Data Collection (REQUIRED)

Fetch PR data using GitHub CLI:

```bash
# Basic PR list command
gh pr list \
  --repo [owner]/[repo] \
  --state all \
  --limit 100 \
  --json number,title,state,createdAt,mergedAt,closedAt,author,url,additions,deletions,labels
```

The JSON output provides all necessary data for analysis and categorization.

**GATE: Verify JSON response contains expected fields before proceeding.**

### Step 2: Date Filtering (REQUIRED)

Filter PRs for the target date or date range:

```bash
# For single-day summary
TARGET_DATE="2025-11-13"

# Filter PRs created on target date
jq --arg date "$TARGET_DATE" \
  '[.[] | select(.createdAt | startswith($date))]'

# Filter PRs merged on target date
jq --arg date "$TARGET_DATE" \
  '[.[] | select(.mergedAt | startswith($date))]'

# For date range (sprint retrospective)
jq '[.[] | select(
  (.createdAt >= "2025-10-28") and (.createdAt <= "2025-11-13")
)]'
```

**GATE: Confirm filtered PR count > 0 and matches expected activity level. If zero PRs, verify date format and repository activity.**

### Step 3: Categorization (MANDATORY)

Apply keyword-based categorization to PR titles and labels:

**Categories:**

- **Performance & Optimization** - Keywords: `perf`, `optimize`, `memory`, `performance`, `speed`, `cache`
- **Bug Fixes** - Keywords: `fix`, `bug`, `resolve`, `issue`, `patch`
- **Features** - Keywords: `feat`, `feature`, `add`, `implement`, `new`
- **UI/UX** - Keywords: `ui`, `ux`, `design`, `animation`, `responsive`, `layout`
- **Documentation** - Keywords: `docs`, `documentation`, `readme`, `comments`, `adr`
- **Refactoring** - Keywords: `refactor`, `cleanup`, `restructure`, `simplify`
- **Testing** - Keywords: `test`, `spec`, `coverage`, `qa`

**Example Categorization Logic:**

```bash
if [[ "$title" =~ (perf|optimize|memory|performance) ]]; then
  category="Performance & Optimization"
elif [[ "$title" =~ (fix|bug|resolve|issue) ]]; then
  category="Bug Fixes"
elif [[ "$title" =~ (feat|feature|add|implement) ]]; then
  category="Features"
# ... continue for other categories
fi
```

**GATE: Every PR must be categorized. "Uncategorized" should be < 10% of total PRs. If > 10%, review keyword rules.**

### Step 4: Priority Assignment (MANDATORY)

Assign priority based on keywords in title or labels:

- 🔴 **HIGH PRIORITY** - Keywords: `breaking`, `critical`, `blocker`, `security`, `urgent`
- 🟡 **MEDIUM PRIORITY** - Keywords: `feature`, `enhancement`, `bug` (non-critical)
- 🟢 **LOW PRIORITY** - Keywords: `docs`, `chore`, `style`, `minor`

**GATE: All PRs must have priority assigned. Default to MEDIUM if no keywords match.**

### Step 5: Contributor Analysis (REQUIRED)

Group PRs by author and track focus areas:

```bash
# Count PRs by author
jq 'group_by(.author.login) |
    map({author: .[0].author.login, count: length, prs: map(.number)})'

# Identify focus areas by analyzing categories of each author's PRs
```

**Track:**

- PRs created count
- PRs merged count
- Focus areas (primary categories)
- Human vs. bot contributors

**GATE: Contributor count must match unique authors in filtered data. Verify no duplicate attribution.**

### Step 6: Velocity Calculation (REQUIRED)

Calculate time-based metrics:

```bash
# Average time to merge (in hours)
jq '[.[] | select(.mergedAt != null) |
    (((.mergedAt | fromdate) - (.createdAt | fromdate)) / 3600)] |
    add / length'

# Active development windows (peak activity hours)
jq '[.[] | .createdAt | fromdate | strftime("%H")] |
    group_by(.) | map({hour: .[0], count: length}) | sort_by(.count) | reverse'
```

**GATE: Velocity metrics must be calculated for all merged PRs. If no merged PRs, state "N/A - no merges in period" in report.**

### Step 7: Report Generation (MANDATORY)

Fill in the template (`assets/daily-pr-summary-template.md`):

1. Load template content
2. Replace `[count]` placeholders with calculated values
3. Fill in PR lists with categorized entries
4. Add contributor breakdown
5. Insert velocity metrics
6. List action items (open PRs needing review)

**GATE: All template sections must be filled. No `[placeholder]` text should remain in final output.**

## Red Flags - STOP

Immediately halt and fix if you observe:

- 🚨 **Fetching PR data without date filtering** - You'll pull thousands of irrelevant PRs. Filter immediately after fetch.
- 🚨 **Skipping categorization** - Everything marked "Uncategorized" means keyword rules weren't applied. Go back to Step 3.
- 🚨 **Not validating contributor counts** - Duplicate authors or missing bot detection corrupts analysis. Verify unique authors.
- 🚨 **Missing velocity calculations** - Average merge time and turnaround are core metrics. Don't skip Step 6.
- 🚨 **Template sections left unfilled** - `[count]`, `[author]`, `[category]` placeholders in output = incomplete execution.
- 🚨 **Running multiple times for same date** - Cache results! Re-running wastes API quota and produces identical output.
- 🚨 **Zero PRs in filtered results** - Verify date format (YYYY-MM-DD), repository name, and that activity occurred on target date.

## Verification Checklist

Before delivering the report, confirm:

- [ ] Report generated without errors
- [ ] All PRs from target date included (verify count matches API response)
- [ ] Categorization accuracy ≥ 90% (manual spot-check recommended)
- [ ] Metrics calculations correct (sanity checks on outliers)
- [ ] Output follows template format exactly
- [ ] Executable commands included for verification
- [ ] Data collection timestamp included in report
- [ ] No `[placeholder]` text remains in final output
- [ ] Contributor count matches unique authors in data
- [ ] Velocity metrics calculated (or explicitly marked N/A)

## Usage Examples

### Example 1: Daily Standup Summary

**Context:** Monday morning standup, need summary of Friday's work

**Command:**

```bash
gh pr list --repo owner/repo \
  --state all --limit 100 \
  --json number,title,state,createdAt,mergedAt,author,url | \
  jq '[.[] | select(
    (.createdAt | startswith("2025-11-08")) or
    (.mergedAt | startswith("2025-11-08"))
  )]'
```

**Output:** `daily-summary-2025-11-08.md` with Friday's PRs categorized and analyzed

### Example 2: Sprint Retrospective

**Context:** End of 2-week sprint, need cumulative summary

**Command:**

```bash
gh pr list --repo owner/repo \
  --state all --limit 200 \
  --json number,title,state,createdAt,mergedAt,author,url | \
  jq '[.[] | select(
    (.createdAt >= "2025-10-28") and (.createdAt <= "2025-11-08")
  )]'
```

**Output:** `sprint-46-retrospective.md` with aggregated metrics across 2 weeks

### Example 3: Contributor Focus Report

**Context:** Manager needs to understand individual contributions

**Command:**

```bash
gh pr list --repo owner/repo \
  --author username \
  --state all --limit 50 \
  --json number,title,state,createdAt,mergedAt,url | \
  jq '[.[] | select(
    (.createdAt >= (now - 604800 | strftime("%Y-%m-%d")))
  )]'
```

**Output:** Contributor-focused report with activity patterns and specialization

## Integration with Agent Framework

This skill was developed within the olympics-fotb agent framework, which uses:

- **Eight-Phase Methodology** - Structured approach from introspection to reality check
- **Confidence Scale (0-10)** - Quantifies certainty before and after execution
- **Role-Based Execution** - Used primarily by `reporting-agent` and `pm-agent` roles
- **Complexity Ratings** - Tracks low/medium/high complexity, not time estimates

For context on the framework, see the bundled `references/` files.

---

## After Using This Skill

**REQUIRED NEXT STEPS:**

1. **Share the report** - Distribute to stakeholders via Slack, email, or wiki
2. **Archive data** - Save PR JSON response for historical analysis
3. **Update tracking** - Mark standup/status report as complete in project tracker

**OPTIONAL NEXT STEPS:**

- **Trend Analysis** - Compare with previous reports to identify velocity changes
- **Action Items Follow-up** - Create GitHub issues for blockers identified in report
- **Team Metrics** - Track PR merge times, review latency trends over time

---

## Skill Maturity

**Current Confidence Level:** 8/10

- ✅ Template format proven
- ✅ Data collection commands tested
- ✅ Categorization rules documented and validated manually
- ⏳ Automation not yet in production (reduces confidence by 1)
- ⏳ Cross-project validation pending (prevents 10/10)

**Path to 9/10:** Successful automation in production for 2+ weeks with ≥90% accuracy

**Path to 10/10:** Canonicalized after 3+ months of reliable use across multiple projects

## Related Resources

### Templates
- `assets/daily-pr-summary-template.md` - Output format specification

### Framework Documentation
- `references/agent-instructions.md` - Eight-Phase methodology and confidence scale
- `references/agent-definitions.md` - Canonical vocabulary and behavioral principles

### External Resources
- GitHub CLI Documentation: https://cli.github.com/manual/gh_pr_list
- jq Manual: https://stedolan.github.io/jq/manual/

## Changelog

**v1.0.1** (2025-11-14)
- Added `version` and `triggers` to frontmatter for skill discovery
- Enhanced description to follow superpowers style (when/what/why format)
- Added "When NOT to Use This Skill" section with anti-patterns
- Renamed "Implementation Guide" → "The Seven Steps (MANDATORY)"
- Added REQUIRED/MANDATORY language to step headers
- Added gate functions between steps for validation checkpoints
- Added "Red Flags - STOP" section with common failure modes
- Renamed "Validation Criteria" → "Verification Checklist" with checkbox format
- Strengthened process-oriented language throughout
- Added cache warning to prevent redundant executions

**v1.0** (2025-11-13)
- Converted to standard Claude Code SKILL.md format
- Added bundled references for agent framework context
- Included template in assets/ directory
- Adapted for use outside olympics-fotb repository
- Maintained all original implementation details and examples

**v1.0 (olympics-fotb)** (2025-11-11)
- Initial skill definition in olympics-fotb repository
- Data collection commands documented
- Categorization rules established
- Examples provided for common use cases
