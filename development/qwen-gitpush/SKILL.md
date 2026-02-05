---
name: qwen_gitpush
description: Analyze uncommitted git changes and decide if/when to commit based on WSP 15 MPS
version: 1.0.0
author: 0102_infrastructure_team
agents: [qwen, gemma]
dependencies: [git_push_dae, pattern_memory]
domain: autonomous_operations
intent_type: DECISION
promotion_state: prototype
---

# Qwen GitPush Analyzer Skill

**Skill Type**: Micro Chain-of-Thought (WSP 96)
**Intent**: DECISION (autonomous git commit analysis)
**Agents**: Qwen 1.5B (strategic), Gemma 270M (validation)
**Promotion State**: prototype
**Version**: 1.0.0
**Created**: 2025-10-23
**Last Updated**: 2025-10-23

---

## Skill Purpose

Analyze uncommitted git changes and decide if/when to commit based on WSP 15 Module Prioritization Scoring (MPS). Generate semantic commit messages that reflect actual changes.

**Trigger Source**: HoloDAE periodic system check (5-10 min interval)

**Success Criteria**:
- Pattern fidelity >90% (Gemma validation)
- Commit messages accurately reflect changes
- MPS scoring prevents premature/excessive commits
- No manual intervention required

---

## Micro Chain-of-Thought Steps

### Step 1: Analyze Git Diff (Qwen Strategic Analysis)

**Input Context Required**:
```python
{
    "git_diff": str,  # Full git diff output
    "files_changed": List[str],  # File paths
    "lines_added": int,
    "lines_deleted": int,
    "branch": str,
    "last_commit_time": float  # Timestamp
}
```

**Qwen Instructions**:
```
You are analyzing git changes to understand what was modified.

1. Read the git diff carefully
2. Identify the TYPE of changes:
   - New features (added functionality)
   - Bug fixes (corrected behavior)
   - Refactoring (improved structure, no behavior change)
   - Documentation (README, ModLog, WSP updates)
   - Configuration (settings, env, dependencies)
   - Tests (new/updated test coverage)

3. Identify CRITICAL files (high importance):
   - main.py, __init__.py (entry points)
   - WSP_framework/src/*.md (protocol definitions)
   - modules/*/src/*.py (core functionality)
   - requirements.txt, .env (dependencies/config)

4. Summarize changes in 1-2 sentences
   Focus on WHY the changes were made, not just WHAT changed

Output format:
{
    "change_type": "feature|bugfix|refactor|docs|config|tests",
    "summary": "Brief description of changes",
    "critical_files": ["file1", "file2"],
    "confidence": 0.85
}
```

**Gemma Validation Pattern**:
- [ ] Did Qwen identify change_type?
- [ ] Is summary present and non-empty?
- [ ] Are critical_files listed (if any)?
- [ ] Is confidence score between 0.0-1.0?

**Expected Reasoning Time**: 200-500ms (Qwen 1.5B)

---

### Step 2: Calculate WSP 15 MPS Score (Custom Scoring)

**WSP 15 Criteria for Git Commits**:

1. **Complexity (C)**: How big/complex is the change?
   - 1: Single file, <50 lines
   - 2: 2-5 files, 50-200 lines
   - 3: 6-15 files, 200-500 lines
   - 4: 16-50 files, 500-1000 lines
   - 5: >50 files or >1000 lines

2. **Importance (I)**: Impact on system?
   - 1: Optional (docs, comments, formatting)
   - 2: Low (test updates, non-critical modules)
   - 3: Medium (feature additions, module updates)
   - 4: High (bug fixes, critical modules)
   - 5: Critical (main.py, WSP protocols, breaking changes)

3. **Deferability (D)**: Can it wait?
   - 1: Must commit immediately (blocking others)
   - 2: Should commit soon (<1 hour)
   - 3: Can wait (few hours)
   - 4: Batchable (can combine with next commit)
   - 5: Low priority (end of day/week)

4. **Impact (P)**: User/developer impact?
   - 1: Internal only (no user-facing change)
   - 2: Low (minor UX improvement)
   - 3: Medium (new feature, visible change)
   - 4: High (workflow improvement, bug fix)
   - 5: Transformative (major feature, architecture change)

**MPS Formula**: `MPS = C + I + D + P`

**Priority Mapping**:
- 18-20: P0 (Critical - commit immediately)
- 14-17: P1 (High - commit within 1 hour)
- 10-13: P2 (Medium - can batch if >10 files OR >2 hours)
- 6-9: P3 (Low - batch with next commit)
- 4-5: P4 (Backlog - defer until end of day)

**Qwen Instructions**:
```
Calculate WSP 15 MPS score for the git changes:

1. Complexity: Count files and lines changed
   <50 lines = 1, 50-200 = 2, 200-500 = 3, 500-1000 = 4, >1000 = 5

2. Importance: Check for critical files
   Docs/formatting = 1, Tests = 2, Features = 3, Bugfixes = 4, Core systems = 5

3. Deferability: Check time since last commit
   <10min = 1 (too frequent), 10min-1hr = 2, 1-3hr = 3, 3-6hr = 4, >6hr = 5

4. Impact: Assess user/developer visibility
   Internal = 1, Minor UX = 2, New feature = 3, Major feature = 4, Transformative = 5

Output format:
{
    "complexity": 3,
    "importance": 4,
    "deferability": 3,
    "impact": 4,
    "mps_score": 14,
    "priority": "P1",
    "reasoning": "14 files changed with bug fixes in critical modules"
}
```

**Gemma Validation Pattern**:
- [ ] All 4 scores (C, I, D, P) present and 1-5?
- [ ] MPS = C + I + D + P (correct sum)?
- [ ] Priority matches MPS range?
- [ ] Reasoning explains the scoring?

**Expected Reasoning Time**: 100-200ms (arithmetic + scoring)

---

### Step 3: Generate Semantic Commit Message (Qwen Generation)

**Commit Message Format** (Conventional Commits style):
```
<type>(<scope>): <subject>

<body>

WSP: <relevant_wsps>
MPS: <priority> (<score>)
```

**Qwen Instructions**:
```
Generate a semantic commit message based on the analysis:

1. Type: Use the change_type from Step 1
   - feat: New feature
   - fix: Bug fix
   - refactor: Code improvement (no behavior change)
   - docs: Documentation only
   - chore: Config/dependencies
   - test: Test coverage

2. Scope: Primary module affected
   - Examples: gitpush, holodae, youtube, wre_core

3. Subject: 50 chars max, imperative mood
   - Good: "Add WSP 15 scoring to git commit analysis"
   - Bad: "Added scoring" or "Adding scoring logic"

4. Body: 1-3 sentences explaining WHY
   - What problem does this solve?
   - What changes were made?
   - Reference relevant WSP protocols

5. Footer: Include MPS and WSPs
   - WSP: 15, 96 (if relevant)
   - MPS: P1 (14)

Output format:
{
    "commit_message": "Full formatted message",
    "confidence": 0.90
}
```

**Example Output**:
```
feat(gitpush): Add autonomous commit decision via WSP 15 MPS

Implements micro chain-of-thought skill for git commit analysis.
Qwen analyzes diff, calculates MPS score (complexity + importance +
deferability + impact), and decides push timing. Gemma validates
pattern fidelity at each step.

WSP: 15 (MPS scoring), 96 (Skills Wardrobe)
MPS: P1 (14) - High priority, commit within 1 hour
```

**Gemma Validation Pattern**:
- [ ] Message follows format (type, scope, subject)?
- [ ] Subject is <50 chars and imperative?
- [ ] Body explains WHY (not just WHAT)?
- [ ] Footer includes WSP and MPS?
- [ ] Message matches git diff content?

**Expected Reasoning Time**: 300-500ms (text generation)

---

### Step 4: Decide Push Action (Threshold Logic)

**Decision Matrix**:

| MPS Score | Priority | Immediate | Condition | Action |
|-----------|----------|-----------|-----------|--------|
| 18-20 | P0 | YES | Critical | `push_now` |
| 14-17 | P1 | YES | If >10 files OR >1hr | `push_now` or `defer_1hr` |
| 10-13 | P2 | NO | If >10 files OR >2hr | `push_now` or `defer_2hr` |
| 6-9 | P3 | NO | Batch | `defer_next_commit` |
| 4-5 | P4 | NO | Low priority | `defer_eod` |

**Qwen Instructions**:
```
Decide if we should commit/push now or defer:

1. Check MPS priority (from Step 2)

2. Apply decision logic:
   - P0: Always push immediately
   - P1: Push if >10 files OR >1 hour since last commit
   - P2: Push if >10 files OR >2 hours since last commit
   - P3: Defer until next commit (batch)
   - P4: Defer until end of day

3. Consider libido threshold:
   - If already committed 5+ times this session → Defer
   - If 0 commits in 6+ hours → Push even if P2/P3

Output format:
{
    "action": "push_now|defer_1hr|defer_2hr|defer_next_commit|defer_eod",
    "reason": "MPS P1 + 14 files changed + 90min since last commit",
    "confidence": 0.85
}
```

**Gemma Validation Pattern**:
- [ ] Action is one of the valid options?
- [ ] Reason references MPS score?
- [ ] Reason mentions time/file conditions?
- [ ] Confidence is 0.0-1.0?

**Expected Reasoning Time**: 50-100ms (threshold checks)

---

## Libido Thresholds (Gemma Monitoring)

**Pattern Frequency Limits**:
- `min_frequency`: 1 per session (at least check once)
- `max_frequency`: 5 per session (don't spam commits)
- `cooldown_period`: 600s (10 min between checks)

**Libido Signals**:
- `CONTINUE`: Frequency OK, proceed with skill
- `THROTTLE`: Hit max frequency (5x this session), skip execution
- `ESCALATE`: Below min frequency AND >6hr since last commit, force check

**Gemma Monitoring Code**:
```python
def check_libido(skill_name: str, context: dict) -> LibidoSignal:
    history = get_pattern_history(skill_name)
    count_this_session = len([p for p in history if p.session == current_session])

    if count_this_session >= 5:  # max_frequency
        return LibidoSignal.THROTTLE

    if count_this_session == 0 and time_since_last_commit() > 21600:  # 6 hours
        return LibidoSignal.ESCALATE

    if time_since_last_execution(skill_name) < 600:  # cooldown
        return LibidoSignal.THROTTLE

    return LibidoSignal.CONTINUE
```

---

## Integration with GitPushDAE

**Skill Output → DAE Execution**:
```python
# WRE Core routes skill result to GitPushDAE
skill_result = await wre.trigger_skill(trigger)

if skill_result.action == "push_now":
    # Pass to GitPushDAE with pre-generated message
    gitpush_dae.execute_from_skill(
        commit_message=skill_result.commit_message,
        mps_score=skill_result.mps_score,
        skip_analysis=True  # Qwen already analyzed
    )
```

**GitPushDAE receives**:
- Pre-analyzed commit decision
- Semantic commit message (Qwen generated)
- MPS score for logging
- No need to re-run decision logic

---

## Pattern Fidelity Scoring

**Gemma Validation at Each Step**:

| Step | Check | Weight | Pass Criteria |
|------|-------|--------|---------------|
| 1 | Analysis format valid | 25% | All required fields present |
| 2 | MPS calculation correct | 25% | Sum matches, priority mapped |
| 3 | Commit message format | 30% | Follows conventional commits |
| 4 | Decision logic applied | 20% | Action matches MPS threshold |

**Overall Fidelity** = Weighted average of all checks

**Target**: >90% fidelity for production promotion

**Evolution Trigger**: If fidelity <90% for 5 consecutive executions → Generate skill variation

---

## Benchmark Test Cases

**Test 1: Simple Bug Fix (P1)**
```yaml
Input:
  files: ["modules/gitpush/src/dae.py"]
  lines: +15, -8
  changes: "Fix OAuth import error"
Expected:
  mps: 12-14 (P1)
  action: push_now (if >1hr)
  message: "fix(gitpush): Resolve OAuth import error"
```

**Test 2: Large Refactor (P2)**
```yaml
Input:
  files: 25 files across modules
  lines: +450, -320
  changes: "Extract DAE launchers to modules"
Expected:
  mps: 13 (P2)
  action: push_now (>10 files)
  message: "refactor(modules): Extract 8 DAE launchers per WSP 62"
```

**Test 3: Doc Update (P3)**
```yaml
Input:
  files: ["README.md", "ModLog.md"]
  lines: +30, -5
  changes: "Update documentation"
Expected:
  mps: 8 (P3)
  action: defer_next_commit
  message: "docs: Update README and ModLog with refactoring notes"
```

**Test 4: WSP Protocol Update (P0)**
```yaml
Input:
  files: ["WSP_framework/src/WSP_96.md"]
  lines: +100, -20
  changes: "Add micro chain-of-thought paradigm"
Expected:
  mps: 18 (P0)
  action: push_now (critical)
  message: "docs(wsp): Add micro chain-of-thought to WSP 96"
```

---

## Learning & Evolution

**Initial Performance** (Week 1):
- Pattern fidelity: 65%
- Common failures: MPS scoring inconsistent, commit messages too generic

**Evolution Cycle**:
1. Qwen reflects on failures
2. Generates 3 variations with different prompts
3. A/B tests all 4 versions (original + 3 variations)
4. Promotes best performer (highest fidelity)

**Target Performance** (Week 4):
- Pattern fidelity: >92%
- Libido: 2-3 executions per session (optimal)
- Commit quality: Semantic, accurate, no manual edits needed

---

## Changelog

### v1.0.0 (2025-10-23)
- Initial skill creation
- WSP 15 MPS custom scoring for git commits
- Micro chain-of-thought (4 steps: analyze, score, generate, decide)
- Gemma validation at each step
- Libido thresholds: min=1, max=5, cooldown=10min
- Promotion state: prototype (0102 testing phase)

---

**Skill Status**: PROTOTYPE - Ready for 0102 validation
**Next Steps**:
1. Test with HoloIndex: `python holo_index.py --test-skill qwen_gitpush`
2. Validate pattern fidelity with real git changes
3. Tune libido thresholds based on first week's data
4. Promote to staged once fidelity >85%
