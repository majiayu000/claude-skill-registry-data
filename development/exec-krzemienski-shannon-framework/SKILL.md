---
name: exec
description: |
  Autonomous task execution with library discovery, 3-tier validation, and atomic git commits.
  Integrates with Shannon CLI Python modules for platform-specific execution. Invokes /shannon:wave
  for code generation, validates outputs functionally, commits only validated changes. Use when: user
  requests autonomous execution, wants library-first development, needs validated commits.

skill-type: PROTOCOL
shannon-version: ">=5.0.0"
complexity-triggers: [0.00-1.00]

mcp-requirements:
  required:
    - name: serena
      purpose: Cache library discoveries and execution state
  recommended:
    - name: sequential
      purpose: Multi-step planning for complex tasks

required-sub-skills:
  - wave-orchestration

optional-sub-skills:
  - spec-analysis
  - functional-testing

allowed-tools: [SlashCommand, Bash, Read, Write, Serena, Sequential]
---

# Exec Skill: Autonomous Task Execution

## Purpose

Execute tasks autonomously with automatic library discovery, 3-tier functional validation, and atomic git commits. Provides a complete autonomous execution workflow that:
1. Discovers existing libraries (don't reinvent wheels)
2. Validates changes functionally (not just compilation)
3. Commits atomically (only validated code enters git history)
4. Retries on failure (with rollback and research)

**Key Innovation**: Combines Shannon Framework's multi-agent orchestration (/shannon:wave) with Shannon CLI's validation and git automation for truly autonomous, validated execution.

---

## When to Use This Skill

### Primary Use Cases

**MANDATORY when user says**:
- "Execute this task autonomously"
- "Add [feature] with validation and commit"
- "Build [component] using existing libraries"
- "Implement [functionality] and ensure it works"

**RECOMMENDED when**:
- Task requires code generation AND validation
- Library discovery would save time
- Git automation desired
- Quality gates needed before commit

**DO NOT USE when**:
- Just analyzing (use spec-analysis instead)
- Just planning (use phase-planning instead)
- Just generating (use wave-orchestration directly)
- Manual validation preferred

---

## Workflow

### Phase 1: Context Preparation (30-60s)

**Action**: Invoke /shannon:prime for session setup

```
@skill context-preservation
  operation: prepare
  task_focused: true
```

**Purpose**:
- Discover available skills and tools
- Verify MCP connections (Serena required)
- Load project context
- Restore any previous session state

**Output**: Session ready, skills discovered, context loaded

### Phase 2: Library Discovery (5-30s)

**Action**: Call Shannon CLI library discoverer

```bash
# Execute CLI command to search registries
shannon discover-libs "[feature extracted from task]" --category [ui|auth|networking|data|forms] --json
```

**Purpose**:
- Search package registries (npm, PyPI, CocoaPods, Maven, crates.io)
- Rank by quality (stars, maintenance, downloads, license)
- Cache results in Serena MCP (7-day TTL)
- Return top 5 recommendations

**Output**: List of LibraryRecommendation objects with install commands and reasoning

**Example**:
```json
{
  "libraries": [
    {
      "name": "next-auth",
      "score": 95.0,
      "why_recommended": "15k+ stars, maintained 4 days ago, MIT license",
      "install_command": "npm install next-auth"
    }
  ]
}
```

**Integration with Phase 4**: Library recommendations inject into wave execution context

### Phase 3: Task Analysis (Optional, 10-30s)

**Action**: Invoke /shannon:analyze for complexity assessment

```
@skill spec-analysis
  specification: {task description with context}
  include_mcps: true
```

**Purpose**:
- Assess task complexity (0.00-1.00)
- Identify domains involved
- Recommend execution strategy
- Estimate timeline

**Output**: Complexity score, domain breakdown, MCP recommendations

**Usage Decision**:
- Skip for simple tasks (quick execution desired)
- Include for complex tasks (benefits from planning)

### Phase 4: Execution Planning (5-15s)

**Action**: Build execution plan with library context

**For Simple Tasks** (complexity <0.30):
```javascript
// Single-step execution
const plan = {
  steps: [{
    number: 1,
    description: task,
    libraries: discoveredLibraries.map(l => l.name),
    validation: {tier1: ["build"], tier2: ["test"], tier3: ["functional"]}
  }]
}
```

**For Complex Tasks** (complexity ≥0.30):
```javascript
// Use sequential-thinking MCP for multi-step planning
@mcp sequential-thinking
  task: Break down {task} into execution steps
  context: Recommended libraries: {libraries}
  format: [{step: "", files: [], validation: {}}]
```

**Output**: ExecutionPlan with steps, each having validation criteria

### Phase 5: Execution Loop (Per Step)

**FOR EACH step in plan**:

#### Step 5a: Execute via /shannon:wave (30-180s per step)

**Action**: Invoke wave with enhanced prompts

```
@skill wave-orchestration
  task: {step.description}
  enhanced_context: |
    RECOMMENDED LIBRARIES: {step.libraries}

    CRITICAL INSTRUCTIONS:
    - Use recommended libraries (don't build custom)
    - Make minimal focused changes
    - Follow project conventions
    - Include error handling

    [Full enhanced prompts from Shannon CLI]
```

**Purpose**:
- Wave analyzes step complexity
- Spawns appropriate number of agents
- Agents execute in parallel
- Files created/modified via Write/Edit tools

**Output**: Files modified/created

#### Step 5b: Parse Wave Results (Instant)

**Action**: Extract file changes from wave execution

```javascript
const filesChanged = parseWaveMessages(messages).filter(m =>
  m.type === 'ToolUseBlock' && ['Write', 'Edit'].includes(m.name)
).map(m => m.input.file_path)
```

**Output**: List of files that were modified

#### Step 5c: Validate Changes (10-120s)

**Action**: Call Shannon CLI validator

```bash
# Tier 1: Static validation
shannon validate --tier 1 --json

# If Tier 1 passes, Tier 2: Tests
shannon validate --tier 2 --json

# If Tier 2 passes, Tier 3: Functional
shannon validate --tier 3 --json
```

**Validation Tiers**:

**Tier 1 - Static** (~10s):
- Build: `npm run build` or `cargo build` or `xcodebuild`
- Type Check: `tsc --noEmit` (if TypeScript) or `mypy .` (if Python)
- Lint: `eslint` or `ruff check` or `swiftlint`

**Tier 2 - Tests** (~1-5min):
- Unit/Integration: `npm test`, `pytest tests/`, `xcodebuild test`
- Parse results for pass/fail count
- Verify: All tests pass (no regressions)

**Tier 3 - Functional** (~2-10min):
- **Node.js**: `npm run dev`, wait for server, `curl health endpoint`, verify 200 OK
- **Python**: `uvicorn main:app`, `curl endpoint`, verify response correct
- **iOS**: Boot simulator, run UI tests, verify element visible

**Output**: ValidationResult(tier1_passed, tier2_passed, tier3_passed, all_passed)

#### Step 5d: Decision Point

**IF validation.all_passed**:
```bash
# Commit validated changes
shannon git-commit \
  --step "{step.description}" \
  --files "{filesChanged.join(',')}" \
  --validation-json "{validation.toJSON()}"
```

**Creates commit**:
```
feat: {step description}

VALIDATION:
- Build: PASS
- Tests: 12/12 PASS
- Functional: Feature works in browser

Files: package.json, src/auth/login.tsx, ...
```

**Result**: Proceed to next step

**ELSE validation failed**:
```bash
# Rollback changes
shannon git-rollback

# Research solution (if research enabled)
@mcp firecrawl
  search: "{validation.failures[0]} solution"

# Replan step with research findings

# Retry (attempt 2 of 3)
```

**Result**: Rollback → Research → Retry (max 3 attempts)

**IF all attempts fail**:
- Document failure reason
- Return partial results
- Recommend manual intervention

### Phase 6: Execution Report

**Action**: Generate comprehensive report

```javascript
const report = {
  success: true,
  task: taskDescription,
  steps_completed: completedSteps.length,
  steps_total: plan.steps.length,
  commits_created: commits.map(c => c.hash),
  branch_name: branchName,
  duration_seconds: totalDuration,
  libraries_used: uniqueLibraries,
  validations: {
    passed: validationsPassed,
    failed: validationsFailed
  }
}
```

**Display**:
```
✅ AUTONOMOUS EXECUTION COMPLETE

Task: {taskDescription}
Branch: {branchName}
Commits: {commits.length}
Duration: {duration}s
Libraries: {libraries.join(', ')}

Ready for: git push origin {branchName}
```

**Save to Serena**:
```
@mcp serena
  write_memory: exec_result_{timestamp}
  content: {report.toJSON()}
```

---

## Integration Points

### Shannon Framework Skills Used

1. **/shannon:prime** - Phase 1 (context preparation)
2. **/shannon:analyze** - Phase 3 (optional complexity analysis)
3. **/shannon:wave** - Phase 5 (code generation per step)

### Shannon CLI Modules Used

1. **shannon discover-libs** - Phase 2 (library search)
2. **shannon validate** - Phase 5c (3-tier validation)
3. **shannon git-commit** - Phase 5d (atomic commits)
4. **shannon git-rollback** - Phase 5d (rollback on failure)

### MCPs Used

1. **Serena** - Required (cache libraries, save execution state)
2. **Sequential-thinking** - Optional (multi-step planning)
3. **Firecrawl** - Optional (research on failures)

---

## Success Criteria

**Technical**:
- [ ] All 6 phases execute without errors
- [ ] Library discovery returns relevant packages
- [ ] Validation runs all 3 tiers correctly
- [ ] Only validated code commits to git
- [ ] Failed validations trigger rollback
- [ ] Retry logic functions (max 3 attempts)

**Functional**:
- [ ] Generated code actually works (not just compiles)
- [ ] Libraries are used (not custom implementations)
- [ ] Git history is clean (only validated commits)
- [ ] Execution is truly autonomous (no manual intervention)

**User Experience**:
- [ ] Real-time progress visible
- [ ] Clear success/failure messages
- [ ] Helpful error reporting
- [ ] Results save to Serena for reference

---

## Common Pitfalls

### Pitfall 1: Skipping Library Discovery
**Symptom**: Task builds custom authentication instead of using next-auth
**Cause**: Phase 2 not executed or results not used
**Fix**: Always run library discovery, inject results into wave context

### Pitfall 2: Committing Unvalidated Code
**Symptom**: Commit created but code doesn't build
**Cause**: Skipped validation or ignored failures
**Fix**: Enforce all_passed check before commit

### Pitfall 3: Not Rolling Back on Failure
**Symptom**: Git history has broken commits
**Cause**: Validation failed but rollback not executed
**Fix**: Always rollback before retry

### Pitfall 4: Infinite Retry Loops
**Symptom**: Same validation error repeated indefinitely
**Cause**: No max iterations or no error detection
**Fix**: Enforce max_iterations=3, detect repeated failures

---

## Examples

### Example 1: Simple File Creation

**Input**:
```
@skill exec
  task: "create hello.py that prints hello world"
```

**Execution**:
- Phase 1: Context (skip for simple)
- Phase 2: Libraries (none needed)
- Phase 3: Analysis (skip for simple)
- Phase 4: Plan (single step)
- Phase 5: Wave creates hello.py → Validate → Commit
- Phase 6: Report success

**Duration**: ~20-30s
**Result**: 1 commit with hello.py

### Example 2: Authentication Feature

**Input**:
```
@skill exec
  task: "add authentication to Next.js app"
  interactive: true
```

**Execution**:
- Phase 1: Prime context
- Phase 2: Discover next-auth library (95/100 score)
- Phase 3: Analyze (complexity 0.42 - MODERATE)
- Phase 4: Plan:
  1. Install next-auth
  2. Configure NextAuth.js
  3. Create login page
  4. Add protected routes
  5. Test authentication
- Phase 5: Execute each step with wave → Validate → Commit (5 commits)
- Phase 6: Report (5 commits, authentication working)

**Duration**: ~5-8 minutes
**Result**: 5 commits, working authentication

### Example 3: Multi-Stack Feature

**Input**:
```
@skill exec
  task: "add user profile feature: FastAPI endpoint + React component"
```

**Execution**:
- Phase 2: Discover Pydantic (backend), shadcn/ui (frontend)
- Phase 4: Plan:
  1. Create Pydantic model
  2. Add FastAPI endpoint
  3. Create React ProfileCard component
  4. Connect frontend to API
- Phase 5: Each step executed, validated, committed
- Phase 6: Report (4 commits, full-stack feature working)

**Duration**: ~8-12 minutes
**Result**: 4 commits, working profile feature

---

## Related Skills

- **wave-orchestration**: Used in Phase 5 for code generation
- **spec-analysis**: Optional in Phase 3 for complexity assessment
- **context-preservation**: Automatic checkpoints between steps
- **functional-testing**: Philosophy enforced in Tier 3 validation

---

## Related Commands

- **/shannon:prime**: Invoked in Phase 1
- **/shannon:analyze**: Optional in Phase 3
- **/shannon:wave**: Invoked per step in Phase 5
- **shannon CLI commands**: discover-libs, validate, git-commit, git-rollback

---

## Version History

**v5.0.0** (2025-11-18):
- Initial release
- Integration with Shannon CLI V3.5.0 executor modules
- Support for Python, Node.js, React, iOS validation
- Multi-registry library discovery (npm, PyPI, CocoaPods, Maven, crates.io)
- 3-tier validation with auto-detected test infrastructure
- Atomic git commits with validation messages
- Retry logic with rollback (max 3 attempts)

---

## Requirements

**Shannon CLI**: Version 3.5.0 or higher (provides executor modules)
**MCPs**: Serena (required), Sequential (recommended)
**Tools**: Bash (for calling CLI commands), Read/Write (for file operations)

**Installation**:
```bash
# Ensure Shannon CLI installed
pip install shannon-cli>=3.5.0

# Verify exec modules available
shannon --version  # Should show 3.5.0+
```

---

**Status**: Production-ready for Shannon Framework V5.0.0
