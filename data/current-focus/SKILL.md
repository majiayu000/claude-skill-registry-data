---
name: current-focus
description: Sync Linear cycle data with CURRENT-FOCUS.md, analyze chat context for gaps, prioritize work based on dependencies and test failures, and provide actionable recommendations. This skill should be used when the user requests "show current focus", "update current focus", or discusses project status and upcoming work.
---

# Current Focus Skill

Update CURRENT-FOCUS.md by combining Linear cycle data, git history, test results, and chat context analysis. Prioritize work and identify gaps.

## Trigger Keywords

- "show current focus" → Read and display existing CURRENT-FOCUS.md
- "update current focus" → Execute full workflow below
- "current focus" → If recently updated (<1 hour), show; else update

## Project Constants

```
Team ID: d1aae15e-d5b9-418d-a951-adcf8c7e39a8
Project Dir: /Users/shayon/DevProjects/mcp-for-lifeos
Document: docs/CURRENT-FOCUS.md
Line Limit: 75 lines (STRICT)
```

## Workflow: Update Current Focus

### Phase 1: Analyze Chat Context

Scan the current conversation for relevant context.

**Step 1:** Scan last 20-30 messages for:

- Linear issue mentions (MCP-XXX pattern)
- File modifications (Write/Edit tool usage)
- Git operations (commits, PRs mentioned)
- Test failures or results discussed
- Work mentioned as needed but not in Linear

**Step 2:** Scan entire session for patterns:

- Uncompleted work mentioned
- Blocking issues preventing progress
- Test failures needing fixes
- Architecture changes requiring follow-up

**Step 3:** Categorize findings:

- **Active work**: Issues being discussed/worked on
- **Gaps**: Work needed but not in current cycle
- **Blockers**: Dependencies preventing progress

**Step 4:** Display context summary to user:

```
📊 Chat Context Analysis

Active Work Detected:
- {Issue mentions from conversation}

Gaps Detected:
- {Work mentioned but not in Linear}

Blockers:
- {Dependencies or issues blocking progress}
```

If no significant context found, say: "No active work detected in chat context."

### Phase 2: Collect Linear Cycle Data

**Step 1:** Call `mcp__linear-server__list_cycles` with:

- `teamId`: "d1aae15e-d5b9-418d-a951-adcf8c7e39a8"
- `type`: "current"

**Step 2:** From the response, extract:

- `cycleId` = `response[0].id` (e.g., "c82d7f64-689c-42e5-8dea-17ccc8572317")
- `cycleName` = `response[0].title`
- `cycleStart` = `response[0].startsAt`
- `cycleEnd` = `response[0].endsAt`
- `completedCount` = last value in `response[0].completedIssueCountHistory`
- `totalCount` = last value in `response[0].issueCountHistory`

**Step 3:** CHECKPOINT - Display to user:

```
✓ Current Cycle: {cycleName}
  ID: {cycleId}
  Dates: {cycleStart} → {cycleEnd}
  Progress: {completedCount}/{totalCount} issues
```

**Step 4:** If `cycleId` is empty or null, STOP and show error:

```
❌ Error: No current cycle found
Check Linear MCP server connection in Claude Code settings
```

**Step 5:** Call `mcp__linear-server__list_issues` SIX TIMES with these exact parameters:

**Query 1 - In Progress:**

```
team: "d1aae15e-d5b9-418d-a951-adcf8c7e39a8"
cycle: {cycleId}  ← USE THE ID FROM STEP 2
state: "In Progress"
limit: 25
```

**Query 2 - In Review:**

```
team: "d1aae15e-d5b9-418d-a951-adcf8c7e39a8"
cycle: {cycleId}  ← USE THE ID FROM STEP 2
state: "In Review"
limit: 25
```

**Query 3 - Todo:**

```
team: "d1aae15e-d5b9-418d-a951-adcf8c7e39a8"
cycle: {cycleId}  ← USE THE ID FROM STEP 2
state: "Todo"
limit: 20
```

**Query 4 - Backlog:**

```
team: "d1aae15e-d5b9-418d-a951-adcf8c7e39a8"
cycle: {cycleId}  ← USE THE ID FROM STEP 2
state: "Backlog"
limit: 20
```

**Query 5 - Deferred:**

```
team: "d1aae15e-d5b9-418d-a951-adcf8c7e39a8"
cycle: {cycleId}  ← USE THE ID FROM STEP 2
state: "Deferred"
limit: 10
```

**Query 6 - Done (last 3 days):**

```
team: "d1aae15e-d5b9-418d-a951-adcf8c7e39a8"
cycle: {cycleId}  ← USE THE ID FROM STEP 2
state: "Done"
updatedAt: "-P3D"
limit: 20
```

**Step 6:** Count results from each query:

- activeCount = Query 1 length
- reviewCount = Query 2 length
- todoCount = Query 3 length
- backlogCount = Query 4 length
- deferredCount = Query 5 length
- doneCount = Query 6 length
- totalIncomplete = activeCount + reviewCount + todoCount + backlogCount + deferredCount

**Step 7:** CHECKPOINT - Display to user:

```
=== Linear Data Collection ===
Cycle: {cycleName} ({cycleId})
Dates: {cycleStart} → {cycleEnd}
Progress: {completedCount}/{totalCount} issues

Issues in Current Cycle ONLY:
- In Progress: {activeCount}
- In Review: {reviewCount}
- Todo: {todoCount}
- Backlog: {backlogCount}
- Deferred: {deferredCount}
- Done (last 3d): {doneCount}

Total Incomplete: {totalIncomplete}
Total Issues: {totalIncomplete + doneCount}
```

**Step 8:** If total issues = 0, warn user:

```
⚠️ Warning: No issues found in current cycle
This may indicate:
- Cycle filter not applied correctly
- All work complete
- Wrong team ID
```

### Phase 3: Collect Git and Test Data

**Step 1:** Run bash command to get git history:

```bash
cd /Users/shayon/DevProjects/mcp-for-lifeos && git log --since="3 days ago" --no-merges --pretty=format:'%h %s' | head -20
```

Count lines and extract Linear issue references (MCP-XXX pattern).

**Step 2:** Run bash command to get merge commits:

```bash
cd /Users/shayon/DevProjects/mcp-for-lifeos && git log --since="3 days ago" --merges --pretty=format:'%h %s' | head -10
```

Extract PR numbers (#XXX pattern).

**Step 3:** Run test suite:

```bash
cd /Users/shayon/DevProjects/mcp-for-lifeos && npm test 2>&1
```

**Step 4:** Parse test output for:

- Passing count (look for "XXX passed")
- Total count (look for "XXX total")
- Skipped count (look for "XXX skipped")
- Test suites (look for "Test Suites: XXX passed")
- Duration (look for "Time: XXX")

**Step 5:** Display test summary to user:

```
=== Test Status ===
Passing: {passing}/{total} ({passRate}%)
Skipped: {skipped}
Duration: {duration}s
```

### Phase 4: Prioritize Work

**Step 1:** Combine all incomplete issues:

- In Progress issues
- In Review issues
- Todo issues
- Backlog issues
- Deferred issues (flag as blocked)

**Step 2:** For each issue, analyze:

- **Blocking dependencies**: Does description mention "BLOCKED BY" or "REQUIRES"?
- **Test failures**: Are there failing tests related to this issue?
- **Cycle deadline**: Days until cycle ends

**Step 3:** Sort issues by priority:

**URGENT (highest priority):**

- Issues with test failures
- Issues blocking other work
- Issues with cycle ending in <2 days

**HIGH PRIORITY:**

- Issues with dependencies completed
- Issues with cycle ending in 2-5 days

**NORMAL PRIORITY:**

- Issues with no blockers
- Issues with cycle ending in >5 days

**DEFERRED (lowest priority):**

- Issues in "Deferred" state
- Issues with incomplete dependencies

**Step 4:** Display prioritization to user:

```
🎯 Recommended Work Order

URGENT (Next):
1. {Issue ID} - {Title}
   Reason: {Why this is urgent}

HIGH PRIORITY:
2. {Issue ID} - {Title}
   Reason: {Why this matters}

(Show top 3 issues maximum)
```

### Phase 5: Gap Analysis

**Step 1:** Compare chat context (Phase 1) against Linear issues (Phase 2).

**Step 2:** Identify gaps:

- Work mentioned in chat but no Linear issue exists
- Follow-up tasks implied by recent changes
- Test failures without corresponding issues

**Step 3:** If gaps found, prompt user:

```
⚠️ Gaps Detected: Work Outside Current Cycle

Gaps Identified:
1. {Gap description}
2. {Gap description}

Actions:
[A] Search Linear for existing issues
[B] Create new issue(s) for these gaps
[C] Ignore for now

Your choice (A/B/C):
```

**Step 4:** Execute user's choice:

- **A**: Call `mcp__linear-server__list_issues` with `query` parameter to search
- **B**: Present issue templates for approval, then create via `mcp__linear-server__create_issue`
- **C**: Note gaps in document under "⚠️ Future Work" section

If no gaps, skip this phase entirely.

### Phase 6: Generate Document

**Step 1:** Read existing document to preserve Project Health:

```bash
awk '/## 📊 Project Health/,EOF' /Users/shayon/DevProjects/mcp-for-lifeos/docs/CURRENT-FOCUS.md
```

Save this to a variable.

**Step 2:** Build document sections in memory:

**VERBOSITY RULES (STRICT - to meet 75-line limit):**

- **Recommended Work**: Top 3 issues, 1-line reason each
- **Planned Work**: Issue ID + title ONLY (NO descriptions, NO context, NO labels)
- **Recent Completions**: Max 5 issues, Issue ID + 1 sentence ONLY (NO metrics, NO grouping)
- **Test Status**: Pass/fail + duration ONLY (NO "Recent Fixes" unless critical failure)
- **Gaps Section**: ONLY include if gaps detected (omit if none)

**Step 3:** Write document using bash heredoc (NOT Edit tool):

```bash
cat > /Users/shayon/DevProjects/mcp-for-lifeos/docs/CURRENT-FOCUS.md << 'EOF'
# Current Development Focus

**Last Updated:** {current timestamp in EST}
**Cycle:** {cycleName} ({cycleStart} - {cycleEnd})
**Progress:** {completedCount}/{totalCount} issues

## 🎯 Recommended Work Order

{Top 3 prioritized issues from Phase 4 - max 10 lines}

## 📋 Planned (This Cycle)

{Issue ID}: {Title}
{Issue ID}: {Title}
(ID + title only, NO descriptions)

## ✅ Recent Completions (Last 3 Days)

{Issue ID}: {Title} - {1-sentence summary}
(Max 5 issues, NO verbose descriptions)

## ✅ Test Status

**Latest Run ({date}):**
- {passing}/{total} passing ({skipped} skipped)
- {testSuites} suites, {duration}s

{If gaps detected, include this section:}
## ⚠️ Future Work

{Gap items from Phase 5}

{Preserved Project Health section}
EOF
```

**Step 4:** Verify encoding:

```bash
file /Users/shayon/DevProjects/mcp-for-lifeos/docs/CURRENT-FOCUS.md
```

Must show "UTF-8". If not, STOP and error.

**Step 5:** Count emojis:

```bash
grep -o "[🎯📋✅⚠️📊]" /Users/shayon/DevProjects/mcp-for-lifeos/docs/CURRENT-FOCUS.md | wc -l
```

Must be ≥4. If not, warn about encoding failure.

**Step 6:** Run markdown linting (REQUIRED):

Use the `/md-lint` slash command:

```bash
/md-lint docs/CURRENT-FOCUS.md --fix
```

The command will:

- Auto-fix supported violations
- Apply manual fixes if violations remain
- Use project + user-level markdown rules
- Display final results

Wait for /md-lint to complete before proceeding.

**Step 7:** Check final line count:

```bash
wc -l /Users/shayon/DevProjects/mcp-for-lifeos/docs/CURRENT-FOCUS.md
```

**Step 8:** CHECKPOINT - Display to user:

```
📄 Document Generated: {lineCount} lines

{If lineCount > 75:}
⚠️ Warning: Exceeds 75-line target by {lineCount - 75} lines
Verbosity reduction needed - consider:
- Fewer Recent Completions (currently showing {count})
- Remove descriptions from Planned Work
- Omit Gaps section if not critical
```

### Phase 7: Present Results

**Step 1:** Display summary:

```
✅ CURRENT-FOCUS.md Updated

📊 Summary:
- Cycle: {cycleName} ({completedCount}/{totalCount})
- Incomplete Issues: {totalIncomplete}
- Recent Completions: {doneCount}
- Gaps Detected: {gapCount}

🎯 Next Recommended Issue:
{Top issue from prioritization}
Reason: {Why this is next}

📄 Document: docs/CURRENT-FOCUS.md ({lineCount} lines, UTF-8 ✓)
```

**Step 2:** Prompt user for immediate action:

```
Ready to start {next issue ID}? (y/n)
```

**Step 3:** If user says yes, call `mcp__linear-server__get_issue` with the issue ID and display:

- Full description
- Acceptance criteria
- Dependencies
- Suggested branch name: `feature/{issue-id-lowercase}-{brief-slug}`

## Workflow: Show Current Focus

**Step 1:** Read existing document:

```bash
cat /Users/shayon/DevProjects/mcp-for-lifeos/docs/CURRENT-FOCUS.md
```

**Step 2:** Display content to user with formatting preserved.

**Step 3:** Show last updated timestamp and suggest:

```
Last updated: {timestamp}

To refresh with latest data: "update current focus"
```

## Critical Validation Checkpoints

Execute these validations at each phase:

**After Phase 2, Step 2:**

```
CHECKPOINT: Verify cycleId extracted
If cycleId is null/empty → STOP, show error
```

**After Phase 2, Step 5:**

```
CHECKPOINT: Verify cycle filter applied
Show user: "Querying {state} issues FROM CYCLE {cycleId}"
```

**After Phase 2, Step 7:**

```
CHECKPOINT: Validate issue counts
If totalIssues = 0 → Warn user about possible query error
If totalIssues > 30 → Warn user about possible missing cycle filter
```

**After Phase 6, Step 6:**

```
CHECKPOINT: Linting complete
/md-lint command handles auto-fix + manual fixes
Verify "0 error(s)" in output before proceeding
```

**After Phase 6, Step 7:**

```
CHECKPOINT: Line count validation
If > 75 lines → Show warning with reduction suggestions
If > 85 lines → MANDATORY reduction required
```

## Reference Materials

Consult `references/output-format.md` for:

- Section templates
- Verbosity reduction strategies for meeting 75-line limit
- Emoji usage patterns
- Data mapping (which Linear states go where)

## Error Recovery

**If Linear MCP fails:**

1. Show user the error
2. Ask: "Retry query or skip Linear data?"
3. If skip, generate document with git/test data only

**If test suite fails:**

1. Show failure details
2. Flag test failures in Recommended Work Order
3. Continue with document generation

**If linting fails:**

1. /md-lint command automatically handles manual fixes
2. Review /md-lint output for final status
3. If still failing after /md-lint, investigate markdown syntax errors

**If exceeds 75 lines:**

1. Identify verbose sections (check Recent Completions first)
2. Reduce to 5 issues maximum in Recent Completions
3. Remove ALL descriptions from Planned Work
4. Regenerate and re-lint

## Project Context

**MCP for LifeOS Team:**

- Team ID: d1aae15e-d5b9-418d-a951-adcf8c7e39a8
- Cycle-based development (weekly cycles)
- Direct master branch workflow (no CI/CD)
- Test suite: ~805/808 passing (99.6% typical)

**Document Purpose:**

- Focus on FUTURE work (what's next)
- Minimal PAST work (what's done)
- Actionable priorities
- Updated after each PR merge
