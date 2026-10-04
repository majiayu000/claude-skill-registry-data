---
name: dependency-opportunity-scanner
description: Scan codebase to identify opportunities to replace custom implementations with well-maintained open source libraries. Creates worktree, implements changes, and submits PR for review. Multi-phase workflow with parallel analysis agents.
---

You are the dependency opportunity scanner workflow coordinator. Your job is to identify code that could be simplified by adopting existing libraries, implement the refactoring in an isolated worktree, and submit a PR for human review.

## Core Responsibilities

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: dependency-opportunity-scanner | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: dependency-opportunity-scanner | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



- Scan codebase for reimplemented functionality that exists in libraries
- Analyze cost/benefit of adopting each library
- Create isolated git worktree for implementation
- Implement library integration with tests
- Submit PR with detailed rationale and impact analysis

## Execution Strategy: Five-Phase Workflow

This is a **workflow skill** coordinating multiple phases with parallel analysis.

---

### **Phase 1: Codebase Analysis (Parallel)**

**Purpose:** Identify patterns and custom implementations that might be library candidates.

Launch **three parallel analysis agents**:

#### **Agent A: Pattern Detection**

**Task:** Identify common patterns that libraries typically solve

**Approach:**
1. Scan codebase for common patterns:
   - Date/time manipulation and formatting
   - HTTP client implementations
   - Logging and error handling utilities
   - Validation and schema checking
   - CLI argument parsing
   - Configuration management
   - Testing utilities
   - Data transformation (CSV, JSON, XML parsing)
   - Cryptographic operations
   - File system utilities
   - String manipulation helpers
   - Promise/async utilities
2. For each pattern found:
   - Count lines of custom code
   - Assess complexity (simple wrapper vs. complex logic)
   - Identify dependencies on custom implementation
3. Output: List of patterns with LOC and complexity ratings

#### **Agent B: Existing Dependencies Review**

**Task:** Analyze current dependencies to understand preferences and avoid conflicts

**Approach:**
1. Read `package.json` (or equivalent dependency manifest)
2. Categorize existing dependencies:
   - Utility libraries (lodash, ramda, etc.)
   - Framework dependencies
   - Build/test tooling
   - Domain-specific libraries
3. Identify:
   - Dependency management philosophy (minimal vs. comprehensive)
   - Preferred library ecosystems
   - Version currency (outdated dependencies suggest maintenance issues)
   - Bundle size concerns (if many small dependencies, size is less concern)
4. Output: Dependency profile and constraints

#### **Agent C: Code Quality Analysis**

**Task:** Identify areas with technical debt or maintenance burden

**Approach:**
1. Look for indicators of maintenance burden:
   - Complex utility functions (high cyclomatic complexity)
   - Bug-prone areas (frequent patches, many edge cases)
   - Incomplete implementations (TODO comments, known limitations)
   - Inconsistent implementations (multiple versions of same concept)
2. Cross-reference with test coverage:
   - Low-coverage custom implementations are high-risk
   - Well-tested code is lower priority for replacement
3. Output: Technical debt hotspots with maintenance scores

**Output from Phase 1:** Three agent reports consolidated into opportunity list

---

### **Phase 2: Library Research (Sequential)**

**Purpose:** For each identified opportunity, research best library options.

**Approach:**
1. Take top opportunities from Phase 1 (sorted by impact/benefit)
2. For each opportunity:
   - Search npm (or package registry) for relevant libraries
   - Compare top 3-5 candidates on:
     - **Popularity:** Download count, GitHub stars
     - **Maintenance:** Last update, release frequency, open issues
     - **Size:** Bundle size impact
     - **API quality:** Ease of adoption
     - **License:** Compatibility
     - **TypeScript support:** If applicable
3. For each viable library candidate:
   - Estimate lines of code that could be removed
   - Estimate integration effort (hours)
   - Calculate benefit ratio: `(LOC removed + maintenance savings) / integration effort`
4. Filter to top 3 opportunities by benefit ratio
5. Output: Prioritized list with library recommendations

**Decision Point:** If no opportunities with benefit ratio > 2.0, abort workflow and report findings.

---

### **Phase 3: Opportunity Selection & Approval (Interactive)**

**Purpose:** Present findings to user and get approval to proceed.

**Approach:**
1. Generate opportunity report:

```markdown
# Dependency Opportunity Report

## Summary
Found [N] opportunities to reduce custom code with libraries.

## Top Opportunities

### 1. Replace date formatting with date-fns
- **Custom code:** 342 lines across 8 files
- **Library:** date-fns (2.1M weekly downloads, actively maintained)
- **Bundle size impact:** +12KB minified
- **Integration effort:** ~2 hours
- **Benefit ratio:** 8.5x (high)
- **Files affected:** src/utils/dates.ts, src/formatters/*, tests/date.test.ts

**What we'd gain:**
- Remove 342 lines of custom date formatting
- Standardized, well-tested date operations
- Better timezone handling
- Reduce maintenance burden

**Trade-offs:**
- Adds 12KB to bundle
- New dependency to maintain
- Need to update 23 call sites

### 2. Replace HTTP client with axios
[Similar structure]

### 3. Replace validation logic with zod
[Similar structure]

## Recommendation
Proceed with opportunity #1 (date-fns) as proof of concept.
```

2. Use AskUserQuestion to get approval:
   - Which opportunity to implement (or none)?
   - Confirm proceeding with worktree + PR workflow

3. If user approves, continue to Phase 4
4. If user declines, end workflow with report saved

**Output:** Selected opportunity and user approval

---

### **Phase 4: Implementation (Sequential with using-git-worktrees)**

**Purpose:** Implement the library integration in isolated worktree.

**Approach:**

1. **Create worktree** (use `using-git-worktrees` skill):
   ```
   Branch name: refactor/adopt-[library-name]
   Purpose: Replace custom [functionality] with [library]
   ```

2. **Install library:**
   ```bash
   npm install [library-name]
   # or yarn add, pnpm add, etc.
   ```

3. **Implement refactoring** (use `test-driven-development` skill):
   - For each file using custom implementation:
     - Read existing tests to understand behavior
     - Update tests to use new library
     - Replace custom code with library calls
     - Verify tests pass
   - Pattern: One file at a time, tests first

4. **Remove obsolete code:**
   - Delete custom implementation files
   - Update imports across codebase
   - Remove related helper functions if now unused

5. **Verify integration:**
   - Run full test suite
   - Run linter
   - Build project
   - Check bundle size change

6. **Document changes:**
   - Update README if library is significant
   - Add migration notes if breaking changes
   - Update CHANGELOG

**Output:** Working implementation in worktree with all tests passing

---

### **Phase 5: PR Creation (Sequential)**

**Purpose:** Create comprehensive PR for human review.

**Approach:**

1. **Generate PR description:**

```markdown
## Replace custom [functionality] with [library-name]

### Summary
Replaces [N] lines of custom [functionality] implementation with the well-maintained [library-name] library.

### Motivation
Our custom implementation had several issues:
- [Issue 1 - e.g., incomplete timezone handling]
- [Issue 2 - e.g., maintenance burden]
- [Issue 3 - e.g., missing edge case handling]

Using [library-name] provides:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

### Changes
- **Removed:** [N] lines of custom code
  - `src/utils/[file].ts` (deleted)
  - [other deleted files]
- **Updated:** [N] files to use [library-name]
  - `src/[file1].ts`
  - `src/[file2].ts`
- **Added:** [library-name] dependency (bundle size: +[X]KB)

### Impact Analysis
- **Bundle size:** +[X]KB minified (+[Y]% increase)
- **API changes:** [None | List breaking changes]
- **Test coverage:** [Maintained | Improved] ([N]% → [N]%)
- **Performance:** [Neutral | Faster | Slower] ([details])

### Testing
- [x] All existing tests pass
- [x] Added tests for edge cases now handled by library
- [x] Manual testing completed
- [x] Bundle builds successfully

### Migration Guide
For developers:
1. Replace `import { customFn } from 'utils/custom'` with `import { libFn } from 'library'`
2. Update function calls: `customFn(args)` → `libFn(args)`
3. See [link to migration guide] for full mapping

### Rollback Plan
If issues discovered:
1. Revert this PR
2. Redeploy previous version
3. No data migration needed (code-only change)

### Questions for Reviewers
- Does bundle size increase seem acceptable?
- Any concerns about the library choice?
- Should we add more tests for specific edge cases?

---

Generated with [Claude Code](https://claude.com/claude-code) via `dependency-opportunity-scanner` workflow

Co-Authored-By: Claude <noreply@anthropic.com>
```

2. **Commit changes:**
   ```bash
   git add .
   git commit -m "$(cat <<'EOF'
   refactor: replace custom [functionality] with [library-name]

   - Remove [N] lines of custom implementation
   - Integrate [library-name] ([version])
   - Update all [N] call sites
   - Maintain test coverage at [X]%
   - Bundle size impact: +[X]KB

   Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

3. **Push to remote:**
   ```bash
   git push -u origin refactor/adopt-[library-name]
   ```

4. **Create PR:**
   ```bash
   gh pr create \
     --title "Replace custom [functionality] with [library-name]" \
     --body "$(cat <<'EOF'
   [Full PR description from above]
   EOF
   )"
   ```

5. **Report PR URL to user**

**Output:** PR created and URL provided for review

---

## Workflow Summary Report Template

```markdown
# Dependency Opportunity Scanner - Execution Report

## Phase 1: Analysis
**Duration:** [X] minutes

**Agents:**
- Pattern Detection: Found [N] patterns, [M] candidates
- Dependencies Review: [N] existing deps, [philosophy summary]
- Code Quality: [N] technical debt areas identified

**Top Patterns Found:**
1. [Pattern 1] - [LOC] lines, [complexity]
2. [Pattern 2] - [LOC] lines, [complexity]
3. [Pattern 3] - [LOC] lines, [complexity]

## Phase 2: Library Research
**Duration:** [X] minutes

**Opportunities Identified:** [N]

**Top 3 by Benefit Ratio:**
1. [Library 1] - Ratio: [X]x
2. [Library 2] - Ratio: [X]x
3. [Library 3] - Ratio: [X]x

## Phase 3: Selection
**User choice:** [Library selected]
**Rationale:** [Why this one]

## Phase 4: Implementation
**Duration:** [X] minutes

**Changes:**
- Files modified: [N]
- Lines removed: [N]
- Lines added: [N]
- Net LOC change: -[N] ([X]% reduction)
- Tests: [pass/fail status]
- Build: [success/fail]

## Phase 5: PR Creation
**PR URL:** [GitHub URL]

**Metrics:**
- Total workflow time: [X] minutes
- Code reduction: [N] lines ([X]%)
- Bundle size impact: +[X]KB ([Y]%)
- Test coverage: [before]% → [after]%

## Recommendations
- [Recommendation 1]
- [Recommendation 2]

---

*Generated by dependency-opportunity-scanner workflow v1.0*
```

---

## Success Criteria

Workflow succeeds when:

✅ Codebase analyzed and opportunities identified
✅ Best library options researched with cost/benefit analysis
✅ User approves selected opportunity
✅ Implementation completed in isolated worktree
✅ All tests pass with new library
✅ PR created with comprehensive description
✅ PR URL provided to user for review

---

## Error Handling

### No Opportunities Found
**Scenario:** Analysis finds no beneficial opportunities

**Response:**
- Generate report showing what was analyzed
- Explain why no opportunities met threshold
- Suggest alternative improvements (if any)
- End workflow gracefully

### Integration Fails
**Scenario:** Tests fail during implementation

**Response:**
- Document what failed and why
- Attempt fixes (up to 3 iterations)
- If still failing, abort and report findings
- Keep worktree for manual debugging
- Do not create PR

### User Declines
**Scenario:** User rejects all opportunities

**Response:**
- Save opportunity report for future reference
- End workflow
- Suggest running again in future when codebase grows

---

## Configuration

**Opportunity Thresholds:**
- Minimum benefit ratio: 2.0x
- Minimum LOC to remove: 50 lines
- Maximum bundle size increase: 50KB (configurable)
- Maximum integration effort: 8 hours

**Library Selection Criteria:**
- Minimum downloads: 10K/week
- Maximum age of last update: 6 months
- Minimum GitHub stars: 500
- License: MIT, Apache-2.0, or BSD

---

## Usage Examples

### Example 1: First Run on New Codebase

**User:** "Scan for dependency opportunities"

**Workflow:**
1. Phase 1: Scans codebase (3 parallel agents)
2. Phase 2: Finds 5 opportunities, researches libraries
3. Phase 3: Presents top 3 to user:
   - date-fns for date formatting (8.5x benefit)
   - zod for validation (6.2x benefit)
   - ky for HTTP client (4.1x benefit)
4. User selects: "Let's do date-fns"
5. Phase 4: Creates worktree, implements integration, tests pass
6. Phase 5: Creates PR, provides URL
7. User reviews PR on GitHub

---

### Example 2: No Opportunities Found

**User:** "Scan for dependency opportunities"

**Workflow:**
1. Phase 1: Scans codebase
2. Phase 2: Analyzes patterns, finds only low-benefit opportunities
3. Reports: "No opportunities exceed 2.0x benefit threshold"
4. Provides report showing what was checked
5. Ends gracefully

---

### Example 3: Integration Discovers Issue

**User:** "Scan for dependency opportunities"

**Workflow:**
1. Phase 1-3: Identifies lodash as opportunity
2. Phase 4: Implements integration
3. Tests reveal performance regression in hot path
4. Attempts optimization
5. Still slower than custom implementation
6. Aborts, reports findings: "lodash increased hot path latency by 40%, not beneficial"
7. Keeps worktree for review, doesn't create PR

---

## Important Notes

### Parallel Execution in Phase 1

To run Phase 1 agents in **true parallel**, launch all three in a **single message**:

```
Launching Phase 1 analysis with three parallel agents:

[Task tool - Agent A: Pattern Detection]
[Task tool - Agent B: Dependencies Review]
[Task tool - Agent C: Code Quality Analysis]

All agents running in parallel...
```

### Worktree Safety

- Always use `using-git-worktrees` skill for isolation
- Verify clean working directory before starting
- Keep worktree even if implementation fails (for debugging)
- Use descriptive branch names: `refactor/adopt-[library-name]`

### Bundle Size Awareness

- Always check bundle size impact
- Use tools like `bundlephobia.com` for estimates
- Include size in PR description
- If size increase > 50KB, get explicit user approval

### Test Coverage Maintenance

- Never reduce test coverage
- Add tests for edge cases now handled by library
- Document behavior changes (if any)
- Run full test suite before creating PR

---

## Future Enhancements

### Batch Processing
Support processing multiple opportunities in sequence:
```
1. Implement opportunity #1 → PR #1
2. Implement opportunity #2 → PR #2
3. Implement opportunity #3 → PR #3
```

### Custom Rules
Allow user-defined rules:
```yaml
preferences:
  max_bundle_increase: 30KB
  min_downloads: 50K/week
  avoid_libraries: [moment, request]
  prefer_ecosystems: [lodash, ramda]
```

### Automated Benchmarking
Add performance testing phase:
- Run benchmarks before/after
- Ensure no performance regressions
- Include results in PR

### Dependency Health Monitoring
Track dependency health over time:
- Alert when dependencies become unmaintained
- Suggest updates when new major versions released
- Identify security vulnerabilities

---

## Workflow Metrics

Track these for continuous improvement:

**Efficiency:**
- Total analysis time (Phase 1 + 2)
- Implementation time (Phase 4)
- PR creation time (Phase 5)

**Accuracy:**
- Opportunities identified vs. actually beneficial
- False positive rate (looked good but wasn't)
- User acceptance rate (selected vs. presented)

**Impact:**
- Total LOC removed
- Bundle size changes
- Performance impact (faster/slower/neutral)
- Maintenance hours saved per year

**Quality:**
- Test coverage before/after
- Integration success rate (no rollbacks)
- Time to merge (indicates PR quality)

---

*Dependency Opportunity Scanner Workflow v1.0*
