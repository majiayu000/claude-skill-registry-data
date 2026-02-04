---
name: Git Risk Analysis
description: Analyze git history to enhance risk assessment for PR reviews. Use when analyzing file changes to detect code hotspots (high churn files), authorship patterns, historical failure correlation, and change complexity. Provides additional context beyond static code analysis to improve production risk scoring.
allowed-tools: [Bash]
---

# Git Risk Analysis Skill

## When to Use This Skill

- ✅ Analyzing file changes in Pull Request reviews
- ✅ Assessing risk of modifications to existing files
- ✅ Need historical context for code stability
- ✅ Enhancing risk scores with churn/hotspot data
- ✅ Identifying files with deployment failure history

## Git Metrics Analysis

**🚨 CRITICAL EXECUTION RULES:**
- **ALL git commands must run from project root** using `git -C workspace/{{REPO}}`
- **Do NOT use pipe operators** (`|`), compound operators (`&&`, `||`), or redirects (`>`, `2>`)
- **Do NOT use command substitution** (`$(...)`) for variable assignments
- **Do NOT use text processing tools** (`wc`, `tr`, `awk`, `sed`, `sort`)
- **Agent must count lines, deduplicate values, and parse output directly**
- **Use Read tool** to load metadata.json instead of `jq` command

### 1. Detect Code Hotspots (High Churn Rate)

**Purpose:** Identify files changed frequently (instability indicator)

**Task:** Count how many commits modified this file in the last 30 days **BEFORE the current PR**

**⚠️ CRITICAL: Temporal Filtering Required**

Use Read tool to load `output/pr-{{PR_NUMBER}}/metadata.json` and extract the `pr_timestamp` value.

Then run:
```bash
git -C workspace/{{REPO}} log main --since="30 days ago" --until="@{pr_timestamp}" --oneline -- <file>
```

Count the number of output lines in the agent to get the churn metric.

**Why:** Only analyze historical commits before the current PR to avoid temporal contamination (using future data to predict past risk).

**Interpretation:**
- **0-3 commits** = Stable file (LOW risk)
- **4-10 commits** = Moderate churn (baseline risk)
- **10-15 commits** = High churn → **+10 risk score**
- **15+ commits** = HOTSPOT → **+20 risk score, flag as CRITICAL**

**Rationale:** Research shows high churn correlates with poor implementation, missing abstractions, or inadequate tests. Hotspot files (20% of code) contain 80% of bugs.

---

### 2. Check Authorship Concentration

**Purpose:** Detect coordination risk from multiple contributors

**Task:** Identify how many unique authors have modified this file in the last 3 months **BEFORE the current PR**

**⚠️ CRITICAL: Temporal Filtering Required**

Use Read tool to load `output/pr-{{PR_NUMBER}}/metadata.json` and extract the `pr_timestamp` value.

Then run:
```bash
git -C workspace/{{REPO}} log main --since="3 months ago" --until="@{pr_timestamp}" --format="%ae" -- <file>
```

Deduplicate the output and count unique entries in the agent to get the authorship metric.

**Interpretation:**
- **1-2 authors** = Good ownership (LOW risk)
- **3-4 authors** = Coordination needed → **Note in findings**
- **5+ authors** = High coordination risk → **+10 risk score**

**Rationale:** Multiple authors increase merge conflicts, inconsistent patterns, and knowledge fragmentation. Coordination overhead grows exponentially with team size.

---

### 3. Find Historical Deployment Failures

**Purpose:** Identify files involved in production rollbacks/hotfixes

**Task:** Search git commit history **BEFORE the current PR** for messages containing keywords like "revert", "rollback", "hotfix", or "emergency" that affected this file

**⚠️ CRITICAL: Temporal Filtering Required**

Use Read tool to load `output/pr-{{PR_NUMBER}}/metadata.json` and extract the `pr_timestamp` value.

Then run:
```bash
git -C workspace/{{REPO}} log main --until="@{pr_timestamp}" --grep="revert\|rollback\|hotfix\|emergency" --oneline -- <file>
```

Count the number of output lines to determine if the file has rollback history.

**❌ DO NOT USE:** `git log --all` (includes future PR branches)

**Interpretation:**
- **0 matches** = No rollback history
- **1+ matches** = File has deployment failure history → **Upgrade severity to CRITICAL**
- **3+ matches** = Chronic production issues → **Recommend architectural review**

**Rationale:** Files with rollback history are statistically more likely to cause future production issues. Past failures predict future failures.

---

### 4. Measure Change Complexity

**Purpose:** Calculate lines changed (churn magnitude)

**Task:** Calculate the total number of lines added and deleted in this file over the last 30 days **BEFORE the current PR**

**⚠️ CRITICAL: Temporal Filtering Required**

Use Read tool to load `output/pr-{{PR_NUMBER}}/metadata.json` and extract the `pr_timestamp` value.

Then run:
```bash
git -C workspace/{{REPO}} log main --since="30 days ago" --until="@{pr_timestamp}" --numstat -- <file>
```

Parse the numstat output in the agent, sum the additions and deletions columns to calculate total lines changed.

**Interpretation:**
- **0-100 lines** = Small changes (LOW risk)
- **100-300 lines** = Moderate refactoring (baseline)
- **300-500 lines** = Large changes → **+5 risk score**
- **500+ lines** = Massive churn → **+15 risk score, recommend incremental approach**

**Rationale:** Large line changes increase bug probability. Smaller, incremental changes are safer for production.

---

### 5. Check Recent Bug Fix Rate

**Purpose:** Measure code quality via bug fix frequency

**Task:** Count commits in the last 60 days **BEFORE the current PR** that mention "fix", "bug", "issue", or "defect" in their messages for this file

**⚠️ CRITICAL: Temporal Filtering Required**

Use Read tool to load `output/pr-{{PR_NUMBER}}/metadata.json` and extract the `pr_timestamp` value.

Then run:
```bash
git -C workspace/{{REPO}} log main --since="60 days ago" --until="@{pr_timestamp}" --grep="fix\|bug\|issue\|defect" -i --oneline -- <file>
```

Count the number of output lines in the agent to get the bug fix rate.

**Interpretation:**
- **0-1 fixes** = Stable code quality
- **2-3 fixes** = Some quality concerns → **Note in findings**
- **4+ fixes** = Quality red flag → **+10 risk score, recommend tests**

**Rationale:** High bug fix rate indicates underlying quality issues. Files requiring frequent fixes often lack test coverage or have design flaws.

---

### 6. Detect Merge Conflict Frequency

**Purpose:** Identify files with complex merge history

**Task:** Count merge commits that affected this file in the last 2 months **BEFORE the current PR**

**⚠️ CRITICAL: Temporal Filtering Required**

Use Read tool to load `output/pr-{{PR_NUMBER}}/metadata.json` and extract the `pr_timestamp` value.

Then run:
```bash
git -C workspace/{{REPO}} log main --since="2 months ago" --until="@{pr_timestamp}" --merges --oneline -- <file>
```

Count the number of output lines in the agent to get the merge conflict frequency.

**Interpretation:**
- **0-2 merges** = Normal collaboration
- **3-5 merges** = Active development area
- **6+ merges** = High conflict risk → **+5 risk score**

**Rationale:** Frequent merges suggest parallel development streams, increasing conflict probability and integration issues.

---

## Integration with Risk Analysis

### Add Git Metrics to Findings

Include git context in your JSON output:

```json
{
  "file": "src/services/PaymentService.java",
  "line": 45,
  "severity": "CRITICAL",
  "git_metrics": {
    "commits_last_month": 18,
    "unique_authors_3mo": 7,
    "lines_changed_30d": 750,
    "bug_fixes_60d": 5,
    "rollback_history": true,
    "merge_conflicts_60d": 8
  },
  "risk_adjustment": "+35 (hotspot + rollback history + high bug rate)",
  "original_severity": "HIGH",
  "adjusted_severity": "CRITICAL",
  "recommendation": "This file is a production hotspot with rollback history. Consider: 1) Architectural review before adding complexity, 2) Increase test coverage (5 bugs in 60 days), 3) Limit concurrent modifications (7 authors)"
}
```

### Risk Score Adjustment Formula

```
Base Risk Score (from static analysis)
+ Churn Adjustment (0-20 points)
+ Authorship Adjustment (0-10 points)
+ Bug Fix Rate Adjustment (0-10 points)
+ Rollback History (upgrade to CRITICAL if present)
= Final Risk Score
```

---

## Best Practices

### ✅ Do:
- Run git commands from repository root
- Handle missing files gracefully (new files have no git history)
- Cache results to avoid redundant git calls
- Consider context (1 commit from 1 author in a 5-year-old file is stable!)
- **USE TEMPORAL FILTERING: Only analyze commits BEFORE current PR timestamp** ⚠️
- Load PR timestamp from metadata.json before running git queries
- Use `main --until="${PR_TIMESTAMP}"` for all git log commands

### ❌ Don't:
- Fail entire analysis if git commands error
- Run git commands on files outside the repository
- Make assumptions about git configuration
- **Use `--all` flag or search future branches** ⚠️
- Include commits from PR branches that haven't been merged yet
- Analyze data from future PRs (temporal contamination)

---

## Example Risk Assessment

**Scenario:** Analyzing PaymentService.java in PR #1234

After gathering git metrics, you might find:
- **Churn:** 15 commits in last month → HOTSPOT (+20 risk)
- **Authors:** 4 unique contributors → Coordination concern (+5 risk)
- **Rollbacks:** 2 rollback commits found → Deployment failure history (UPGRADE TO CRITICAL)
- **Bug fixes:** 5 bug fixes in last 60 days → Quality concern (+10 risk)

**Final Assessment:**
- Base severity: HIGH
- Git adjustments: +35 points
- Final: CRITICAL with strong evidence from git history

---

## Success Criteria

Git analysis enhances risk scoring when:

- ✅ Hotspot files get higher risk scores
- ✅ Files with rollback history flagged as CRITICAL
- ✅ Coordination risks identified for multi-author files
- ✅ Bug-prone files get test coverage recommendations
- ✅ Agent provides stability context in recommendations
- ✅ 20-30% more accurate risk predictions

---

## When NOT to Use

- ❌ New files (no git history exists)
- ❌ Non-git repositories
- ❌ Files outside repository boundaries
- ❌ When git commands timeout (very large repos)

In these cases, gracefully skip git analysis and rely on static code analysis only.
