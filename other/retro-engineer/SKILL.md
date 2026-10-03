---
name: retro-engineer
description: Engineering retrospective skill for continuous improvement. Use when the user wants to run a weekly or sprint retro, review shipping velocity, analyse test health trends, identify growth opportunities, get per-person breakdowns, or run a cross-project retrospective across all their AI tools and repos.
---

# Retro Engineer Skill

## Overview

This skill guides you through a thorough, structured engineering retrospective. It operates in two distinct modes:

1. **Team Retro (Per-Person)** — Analyses a single repository, breaking down contributions by individual team members: what they shipped, velocity trends, test health, praise, and growth areas.
2. **Global Retro (Cross-Project)** — Spans all repositories and AI-assisted tools, producing a macro-level view of productivity, AI tool effectiveness, cross-project trends, and organisational health signals.

When in doubt about which mode to run, ask the user:

> Which retro mode would you like?
> - A) Team Retro — per-person breakdown for this repo/sprint
> - B) Global Retro — cross-project, all AI tools, all repos

---

## Step 0: Environment & Context Detection

Before starting any retro, gather environment context:

```bash
# Determine current repo
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "non-git")
REPO_SLUG=$(basename "$REPO_ROOT" 2>/dev/null || echo "global")
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
TODAY=$(date +%Y-%m-%d)
WEEK=$(date +%Y-W%V)

echo "REPO: $REPO_SLUG"
echo "BRANCH: $CURRENT_BRANCH"
echo "DATE: $TODAY"
echo "WEEK: $WEEK"
```

Identify the retro time window. Default is the last 7 days (weekly retro). If the user specifies a sprint length (e.g. 2 weeks, 4 weeks), use that window.

```bash
# Default: last 7 days
SINCE="7 days ago"
# For a 2-week sprint: SINCE="14 days ago"
# Always confirm with user if unclear
```

---

## Mode A: Team Retro (Per-Person Breakdown)

### Step A1: Collect Commit History

```bash
# Full commit log for the retro window with author details
git log \
  --since="$SINCE" \
  --format="%H|%an|%ae|%ad|%s" \
  --date=short \
  | sort > /tmp/retro_commits.txt

# Count commits per author
git shortlog \
  --since="$SINCE" \
  -sne \
  | sort -rn > /tmp/retro_authors.txt

cat /tmp/retro_authors.txt
```

### Step A2: Collect PR & Branch Activity

```bash
# List recently merged branches (GitHub CLI if available)
if command -v gh &>/dev/null; then
  gh pr list \
    --state merged \
    --json number,title,author,mergedAt,additions,deletions,changedFiles \
    --limit 50 \
    2>/dev/null | tee /tmp/retro_prs.json
else
  # Fallback: list merged remote branches by date
  git branch -r --merged main \
    --sort=-committerdate \
    | head -30
fi
```

### Step A3: Per-Person Contribution Breakdown

For each unique author found in `/tmp/retro_authors.txt`, produce:

```
### 👤 [Author Name]

**Commits:** N  
**Files changed:** N  
**Lines added:** +N | **Lines removed:** -N  
**PRs merged:** N  
**Avg PR size:** N lines  

**Features shipped:**
- [List inferred from commit messages with feat: prefix]

**Bugs fixed:**
- [List inferred from commit messages with fix: prefix]

**Refactors / chores:**
- [List inferred from chore:, refactor:, test:, docs: prefixes]

**🌟 Praise (What went well):**
- [Highlight strong contributions, consistent commit quality, test coverage additions, documentation]

**📈 Growth Area:**
- [One respectful, actionable suggestion per person — e.g. commit message clarity, PR size, test coverage gaps]
```

To gather per-author file/line stats:

```bash
AUTHOR="[name]"
git log \
  --since="$SINCE" \
  --author="$AUTHOR" \
  --format="%H" \
  | xargs -I{} git diff-tree --no-commit-id -r --stat {} \
  | tail -1
```

### Step A4: Shipping Streak Tracking

Shipping streaks celebrate consistency. A "shipping day" is any calendar day with at least one merged PR or production-meaningful commit (feat/fix).

```bash
# Generate list of shipping days
git log \
  --since="$SINCE" \
  --format="%ad" \
  --date=short \
  | sort -u > /tmp/shipping_days.txt

# Count streak (consecutive days)
python3 - <<'EOF'
from datetime import date, timedelta

with open("/tmp/shipping_days.txt") as f:
    days = sorted(set(line.strip() for line in f if line.strip()))

if not days:
    print("No shipping days found.")
else:
    from datetime import datetime
    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in days]
    dates.sort(reverse=True)

    streak = 1
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            streak += 1
        else:
            break

    print(f"🔥 Current shipping streak: {streak} consecutive day(s)")
    print(f"📦 Total shipping days this period: {len(dates)}")
    print(f"Last shipped: {dates[0]}")
EOF
```

Render the shipping streak prominently in the retro report. If the streak is ≥ 5 days, call it out as an achievement worth celebrating.

### Step A5: Test Health Trend Analysis

```bash
# Discover test files changed
git log \
  --since="$SINCE" \
  --name-only \
  --format="" \
  | grep -E "(test|spec|__tests__|_test\.|\.test\.|\.spec\.)" \
  | sort | uniq -c | sort -rn \
  | head -20

# Count test files added vs deleted
TESTS_ADDED=$(git log --since="$SINCE" --diff-filter=A --name-only --format="" \
  | grep -cE "(test|spec|__tests__|_test\.|\.test\.|\.spec\.)" 2>/dev/null || echo 0)

TESTS_DELETED=$(git log --since="$SINCE" --diff-filter=D --name-only --format="" \
  | grep -cE "(test|spec|__tests__|_test\.|\.test\.|\.spec\.)" 2>/dev/null || echo 0)

echo "Test files added: $TESTS_ADDED"
echo "Test files deleted: $TESTS_DELETED"
```

Calculate a simple **Test Health Signal**:

| Signal | Meaning |
|--------|---------|
| Tests added > tests deleted | ✅ Health improving |
| Tests added == tests deleted | ⚠️ Neutral — no regression, no progress |
| Tests deleted > tests added | 🔴 Regression risk — investigate |
| Zero tests changed | ⚠️ No test activity — consider coverage goals |

If CI configuration is present (`.github/workflows`, `Jenkinsfile`, `.circleci`), note which pipelines ran and whether they passed:

```bash
# Check for CI config files
find . -maxdepth 3 \
  -name "*.yml" -o -name "*.yaml" -o -name "Jenkinsfile" \
  | grep -E "(github|ci|circleci|gitlab|jenkins)" \
  | head -10
```

### Step A6: Velocity Metrics

Compile the full velocity table for the retro period:

```
## 📊 Velocity Metrics — [WEEK] — [REPO_SLUG]

| Metric                     | This Period | Prior Period | Δ      |
|----------------------------|-------------|--------------|--------|
| Features shipped (feat:)   | N           | N            | ±N     |
| Bugs fixed (fix:)          | N           | N            | ±N     |
| PRs merged                 | N           | N            | ±N     |
| Commits total              | N           | N            | ±N     |
| Test files added           | N           | N            | ±N     |
| Lines added                | +N          | +N           | ±N     |
| Lines removed              | -N          | -N           | ±N     |
| Active contributors        | N           | N            | ±N     |
| Avg PR cycle time (hrs)    | N           | N            | ±N     |
| Shipping days              | N/7         | N/7          | ±N     |
```

To gather "prior period" data for comparison:

```bash
PRIOR_SINCE="14 days ago"
PRIOR_UNTIL="7 days ago"

git log \
  --after="$PRIOR_SINCE" \
  --before="$PRIOR_UNTIL" \
  --oneline \
  | wc -l
```

---

## Mode B: Global Retro (Cross-Project & AI Tool Analysis)

### Step B1: Discover All Active Repos

```bash
# Common repo locations — expand as needed
find ~/code ~/projects ~/workspace ~/src ~/dev \
  -maxdepth 3 \
  -name ".git" \
  -type d \
  2>/dev/null \
  | sed 's|/.git||' \
  | sort > /tmp/retro_all_repos.txt

echo "Repos found:"
cat /tmp/retro_all_repos.txt
```

For each repo found, run a condensed version of Steps A1–A6 and aggregate results.

### Step B2: Cross-Project Shipping Summary

```
## 🌐 Global Shipping Summary — [WEEK]

| Repo              | Commits | Features | Fixes | PRs | Active Contributors |
|-------------------|---------|----------|-------|-----|---------------------|
| repo-alpha        | N       | N        | N     | N   | N                   |
| repo-beta         | N       | N        | N     | N   | N                   |
| ...               | ...     | ...      | ...   | ... | ...                 |
| **TOTAL**         | N       | N        | N     | N   | N (unique)          |
```

Highlight the **top shipping repo** and the **repo with the most test activity**.

### Step B3: AI Tool Usage Breakdown

Scan for AI tool footprints across all repos:

```bash
# Check for AI-related config and history files
find ~ -maxdepth 4 \( \
  -name ".claude" -o \
  -name "CLAUDE.md" -o \
  -name ".cursor" -o \
  -name ".copilot" -o \
  -name ".gstack" -o \
  -name ".aider*" -o \
  -name "*.prompt.md" \
  \) -type f -o -type d \
  2>/dev/null \
  | head -40
```

Produce an AI tool usage breakdown table:

```
## 🤖 AI Tool Activity — [WEEK]

| AI Tool          | Sessions / Files Detected | Repos Active In | Notable Usage                   |
|------------------|--------------------------|-----------------|--------------------------------|
| Claude / Beacon  | N                        | N repos         | [e.g. architecture, debugging] |
| GitHub Copilot   | N                        | N repos         | [e.g. autocomplete, PR review] |
| Cursor           | N                        | N repos         | [e.g. multi-file edits]        |
| Aider            | N                        | N repos         | [e.g. commit automation]       |
| Other            | -                        | -               | -                              |
```

Flag any repos with **zero AI tool activity** — these may benefit from onboarding.

### Step B4: Cross-Project Trends & Signals

Analyse and report on:

1. **Language diversity** — what languages are being written across all repos this period?
2. **Hotspot files** — files changed in 3+ repos (shared libraries, config templates)?
3. **Bus factor risk** — any repo where a single author made 100% of commits?
4. **Doc debt signal** — repos with commits but no `docs:` or README changes?
5. **Security signal** — any `fix:` commits mentioning auth, token, secret, cve, vuln?

```bash
# Bus factor check per repo
for repo in $(cat /tmp/retro_all_repos.txt); do
  cd "$repo" 2>/dev/null || continue
  TOTAL=$(git log --since="$SINCE" --oneline | wc -l | tr -d ' ')
  TOP_AUTHOR=$(git shortlog --since="$SINCE" -sn | head -1)
  TOP_COUNT=$(echo "$TOP_AUTHOR" | awk '{print $1}')
  if [ "$TOTAL" -gt 0 ] && [ "$TOP_COUNT" -eq "$TOTAL" ]; then
    echo "⚠️  Bus factor risk: $(basename $repo) — single author ($TOP_COUNT commits)"
  fi
done
```

---

## Retro Report Format

Every retro (Team or Global) MUST produce a structured report in this format:

---

```markdown
# Engineering Retrospective — [REPO or GLOBAL] — [DATE]

**Period:** [START] → [END]  
**Mode:** [Team / Global]  
**Generated:** [TIMESTAMP]

---

## 🔥 Shipping Streak

[Streak badge and details]

---

## 📊 Velocity Metrics

[Velocity table from Step A6 / B2]

---

## 🧪 Test Health

[Test health signal + trend table]

---

## 👥 Per-Person Breakdown

[For Team mode: one section per author with praise + growth area]
[For Global mode: top contributors across all repos]

---

## ✅ What Went Well

1. [Achievement or win — be specific, name the person or team]
2. [...]
3. [...]

## 🔧 What to Improve

1. [Concrete, actionable issue — avoid blame, focus on process or system]
2. [...]
3. [...]

## 🚀 What to Try Next

1. [Experiment, new practice, or tool to trial in the next sprint]
2. [...]
3. [...]

---

## 🤖 AI Tool Usage

[AI tool breakdown table — Global mode only, or if AI tools detected]

---

## 📋 Action Items

| # | Action Item                          | Owner         | Due Date   | Priority |
|---|--------------------------------------|---------------|------------|----------|
| 1 | [Specific action]                    | [Name/@handle]| [YYYY-MM-DD] | High   |
| 2 | [...]                                | [...]         | [...]      | Medium   |
| 3 | [...]                                | [...]         | [...]      | Low      |

---

## ✔️ Definition of Done — This Sprint

- [ ] All planned features are merged to main
- [ ] All P0/P1 bugs are resolved or have owners
- [ ] CI/CD pipeline is passing (no red builds at sprint close)
- [ ] Test coverage has not decreased from prior sprint baseline
- [ ] All PRs have at least one approver
- [ ] Release notes / changelog updated (if applicable)
- [ ] No open security-flagged `fix:` commits unreviewed
- [ ] Retro action items from prior sprint reviewed (done / carried / dropped)
- [ ] Documentation updated for any public API changes
- [ ] Bus factor risk addressed (pair programming, docs, or handoff scheduled)

---

## 📅 Next Retro

**Recommended cadence:** [Weekly for fast-moving teams | Bi-weekly for mature sprints | Monthly for maintenance repos]  
**Next retro date:** [DATE + 7 or DATE + 14]  
**Owner / facilitator:** [Name]
```

---

## Retro Cadence Recommendations

Use the following table to recommend the right retro cadence based on observed team velocity:

| Team Signal                              | Recommended Cadence |
|------------------------------------------|---------------------|
| >20 commits/week, active CI, 3+ contributors | Weekly |
| 10–20 commits/week, 2 contributors       | Bi-weekly |
| <10 commits/week, solo or maintenance    | Monthly |
| Post-incident or major release           | Immediate / ad-hoc retro |
| New team or onboarding sprint            | Weekly (first 4 weeks minimum) |

Always state the recommendation and reasoning in the retro report. Do not just pick weekly by default without checking the data.

---

## Action Item Standards

Every action item MUST follow this format when written:

```
| [#] | [Verb] + [specific outcome] — e.g. "Add E2E tests for checkout flow" | @[owner] | [YYYY-MM-DD] | [High/Medium/Low] |
```

Rules for action items:
- **Never write vague items** like "improve tests" or "fix CI". Be specific.
- **Every item must have an owner** — a named person or GitHub handle.
- **Due date is mandatory** — default to end of next sprint if not specified.
- **Maximum 5 action items per retro** — prioritise ruthlessly.
- **Start each retro by reviewing prior action items** before generating new ones.

To surface prior action items, check for a prior retro file:

```bash
ls -lt ~/.gstack/projects/"$REPO_SLUG"/retros/*.md 2>/dev/null | head -5
# or
find . -name "retro-*.md" -newer /tmp/dummy | head -5
```

---

## Shipping Streak — Extended Logic

A shipping streak is a series of consecutive calendar days (Mon–Fri, excluding weekends unless the team ships on weekends) where the team merged at least one production-meaningful unit of work.

**What counts as shipping:**
- A merged PR with label `feat`, `fix`, or `perf`
- A commit with a `feat:` or `fix:` prefix on the default branch
- A tagged release or version bump

**What does NOT count:**
- `chore:`, `docs:`, `test:` only days
- WIP or draft PRs
- Commits with `[skip ci]` or `[wip]`

Streaks are per-repo in Team mode and global-aggregate in Global mode.

Display streak with a visual indicator:

```
🔥🔥🔥 3-day streak
🔥🔥🔥🔥🔥 5-day streak — MILESTONE! Keep it up.
🔥×10 10-day streak — LEGENDARY.
```

If the streak was broken, note when it broke and why (if inferable from commit history).

---

## Test Health Trend — Extended Analysis

Beyond counting test files, perform a deeper health scan:

```bash
# Look for test coverage reports
find . -name "coverage.xml" -o -name "lcov.info" \
  -o -name "coverage-summary.json" \
  -o -name ".nyc_output" \
  2>/dev/null | head -10

# Check if coverage decreased in this period
# (compare coverage badge or report if available)
```

Also scan for **anti-patterns** that indicate degrading test health:

```bash
# Tests that only skip
grep -r "\.skip\|xit\|xdescribe\|pytest.mark.skip" \
  --include="*.test.*" --include="*.spec.*" \
  -l . 2>/dev/null | head -10

# TODO in tests (unfinished tests)
grep -rn "TODO\|FIXME\|HACK" \
  --include="*.test.*" --include="*.spec.*" \
  . 2>/dev/null | wc -l
```

Report these as **Test Debt Signals** in the retro.

---

## Global Retro — AI Tool Effectiveness Score

For each AI tool detected, score its effectiveness (qualitative, based on evidence):

```
## 🤖 AI Tool Effectiveness — [WEEK]

| Tool         | Evidence of Use                            | Output Quality Signal          | Score (1–5) |
|--------------|--------------------------------------------|---------------------------------|-------------|
| AI agent   | SKILL.md files, session logs detected       | Commits with AI-attributed msgs | [score]     |
| Copilot      | .copilot config, PR review comments         | Test coverage trend             | [score]     |
| Cursor       | .cursor directory, multi-file diff patterns | Refactor commit frequency       | [score]     |
| Aider        | aider.chat.md files, commit message patterns| Commit quality, conventional msg| [score]     |
```

Scoring rubric:
- **5** — Clear productivity lift: more features, better test coverage, faster PRs
- **4** — Positive signal: consistent use, clean outputs, no regressions introduced
- **3** — Mixed signal: used but inconsistently, some regressions or noise commits
- **2** — Low signal: rarely used or outputs required heavy manual correction
- **1** — Negative signal: AI-generated code introduced bugs or tech debt

---

## Definition of Done — Full Checklist (Detailed)

This is the master DoD checklist. Include it in every retro. Check off items that are met; flag unchecked items as risks.

### Code Quality
- [ ] All code merged to default branch passes linting (ESLint, Pylint, Clippy, etc.)
- [ ] No new `FIXME` or `TODO` items introduced without a linked issue
- [ ] All functions/methods have docstrings or JSDoc (for public APIs)
- [ ] No dead code introduced (unused imports, unreachable branches)
- [ ] MISRA / CERT / coding standard violations resolved (if automotive/embedded context)

### Testing
- [ ] Unit tests written for all new functions (coverage ≥ prior baseline)
- [ ] Integration tests updated for changed API surfaces
- [ ] No test files have new `.skip` or `xit` entries without a tracking issue
- [ ] All tests pass locally and in CI
- [ ] Performance-sensitive code has benchmark tests

### CI/CD & Build
- [ ] CI pipeline green on default branch
- [ ] No secrets or credentials committed (secret scanning passed)
- [ ] Docker images build successfully (if applicable)
- [ ] Build artifacts are reproducible
- [ ] Deployment to staging succeeded (if applicable)

### Review & Process
- [ ] All PRs have at least 1 approving review
- [ ] No PR is older than the sprint window still open (or explicitly deferred)
- [ ] Commit messages follow Conventional Commits format
- [ ] Sprint board / backlog is up to date (done items closed, new items estimated)

### Documentation
- [ ] README updated for any new setup steps or environment variables
- [ ] CHANGELOG or release notes updated
- [ ] API documentation regenerated (if OpenAPI / Swagger / Javadoc driven)
- [ ] Architecture decision records (ADRs) written for significant design choices

### Security (Automotive & General)
- [ ] No new CVEs in updated dependencies (npm audit / pip audit / cargo audit)
- [ ] Authentication and authorisation logic reviewed
- [ ] Input validation present for all external data entry points
- [ ] Cryptographic operations use approved algorithms (no MD5, no hardcoded keys)
- [ ] (Automotive) UDS/CAN message handling validates all input lengths and ranges

### Handoff & Knowledge
- [ ] Bus factor risk addressed for any solo-authored critical component
- [ ] Onboarding docs updated if new tooling was added
- [ ] Prior sprint's retro action items reviewed and closed/carried/dropped

---

## Retro Facilitation Tips

When running this retro interactively with a team, follow these facilitation guidelines:

1. **Timebox each section** — What Went Well (10 min), What to Improve (15 min), What to Try Next (10 min), Action Items (10 min). Total: ~45 min.
2. **Start with data** — present the velocity metrics and test health before opinions. Let the data drive the conversation.
3. **No blame culture** — frame every "What to Improve" item as a system or process issue, not a person issue.
4. **Rotate facilitator** — each sprint, a different team member runs the retro. Log who facilitated in the retro file.
5. **Action items over discussion** — if a topic generates more than 5 minutes of discussion without converging, turn it into an action item and move on.
6. **Read prior action items first** — open every retro by reviewing the previous retro's action items. Mark each: ✅ Done, 🔄 Carry, ❌ Drop.
7. **Celebrate the streak** — always open with the shipping streak. Positive energy sets the tone.

---

## Saving the Retro Report

After generating the report, save it to a consistent location:

```bash
RETRO_DIR=~/.gstack/projects/"$REPO_SLUG"/retros
mkdir -p "$RETRO_DIR"
RETRO_FILE="$RETRO_DIR/retro-$TODAY.md"

# Write the report
cat > "$RETRO_FILE" << 'REPORT'
[generated report content]
REPORT

echo "✅ Retro saved to: $RETRO_FILE"

# Also write a local copy in the repo for team visibility (optional)
if [ -d "./.retros" ] || [ -f "./RETRO.md" ]; then
  cp "$RETRO_FILE" "./.retros/retro-$TODAY.md" 2>/dev/null || true
fi
```

Also update the repo timeline:

```bash
echo "{\"event\":\"retro\",\"date\":\"$TODAY\",\"week\":\"$WEEK\",\"mode\":\"$RETRO_MODE\"}" \
  >> ~/.gstack/projects/"$REPO_SLUG"/timeline.jsonl
```

---

## Summary Output Format

Always close the retro with a compact summary suitable for posting in Slack, Teams, or a standup channel:

```
📋 Retro Summary — [REPO] — [WEEK]

🔥 Shipping streak: N days
📦 Features shipped: N | 🐛 Bugs fixed: N | 🔀 PRs merged: N
🧪 Test health: [✅ Improving / ⚠️ Neutral / 🔴 Regressing]
👥 Active contributors: N

✅ Top win: [one sentence]
🔧 Top improvement: [one sentence]
🚀 Experiment next: [one sentence]

📋 Action items: N new | N carried from prior retro
📅 Next retro: [DATE]
```

This summary should be generated automatically at the end of every retro run.
