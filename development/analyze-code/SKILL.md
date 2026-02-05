---
name: analyze-code
description: Intelligence-first code analysis for bugs, architecture, performance, and security. Use proactively when investigating code issues, tracing dependencies, or understanding system behavior. MUST query project-intel.mjs before reading files.
parameters:
  mode:
    type: string
    enum: [auto, overview, feature, architecture]
    default: auto
    description: "Analysis mode: auto (detect from context), overview (general repository context → refs/overview.md), feature (specific feature/domain → refs/design.md), architecture (system structure analysis)"
  target:
    type: string
    optional: true
    description: "Target for analysis (e.g., feature name, component name). Required when mode=feature, optional otherwise."
---

# Code Analysis Skill

## Overview

This skill performs comprehensive code analysis using an **intel-first approach** - always querying project-intel.mjs before reading full files, achieving 80-95% token savings.

**Core principle:** Query intel → Verify with MCP → Report with evidence

**Announce at start:** "I'm using the analyze-code skill to investigate this issue."

---

## Quick Reference

| Phase | Key Activities | Token Budget | Output |
|-------|---------------|--------------|--------|
| **1. Scope** | Define objective, bounds, success criteria | ~200 tokens | analysis-spec.md |
| **2. Intel Queries** | Search, symbols, dependencies via project-intel.mjs | ~500 tokens | /tmp/intel_*.json |
| **3. MCP Verification** | Verify findings with authoritative sources | ~300 tokens | Evidence block |
| **4. Report** | Generate CoD^Σ trace report | ~1000 tokens | report.md |

**Total: ~2000 tokens vs 20000+ for direct file reading**

---

## Analysis Modes & Auto-Detection

This skill supports **three analysis modes** optimized for different use cases:

### Mode 1: Overview (General Repository Context)
**Purpose**: Create comprehensive repository map for reference (refs/overview.md)
**Use When**:
- First time exploring a codebase
- Need high-level architecture understanding
- Building project documentation
- User asks: "understand this codebase", "what's the architecture", "show me the structure"

**Output**: `refs/overview.md` with project stats, directory tree, component inventory, entry points

**Token Budget**: ~2K (vs 50K+ reading all files) = **96% savings**

### Mode 2: Feature (Specific Domain Context)
**Purpose**: Deep dive into specific feature/domain for development (refs/design.md)
**Use When**:
- Understanding how a specific feature works
- Planning feature modifications
- Need detailed feature documentation
- User asks: "how does [X] work", "analyze the booking feature", "explain authentication"

**Output**: `refs/design.md` with feature boundary, dependency graph, data flow, integration points

**Token Budget**: ~8K (vs 40K+ reading feature files) = **80% savings**

### Mode 3: Architecture (System Structure Analysis)
**Purpose**: Analyze system layers, boundaries, and architectural patterns
**Use When**:
- Evaluating architecture decisions
- Finding architectural violations
- Planning major refactoring
- User asks: "review architecture", "find circular dependencies", "show layers"

**Output**: `report.md` with layer analysis, boundary violations, pattern identification

**Token Budget**: ~5K (vs 30K+ reading system) = **83% savings**

### Auto-Detection Logic

When `mode=auto` (default), detect from user message context:

| User Message Pattern | Detected Mode | Example |
|---------------------|---------------|---------|
| "understand codebase", "show me structure", "what's here" | **overview** | "I'm new to this project, show me the structure" |
| "how does [X] work", "analyze [feature]", "[component] explanation" | **feature** (target=[X]) | "How does the booking system work?" |
| "review architecture", "find cycles", "analyze layers" | **architecture** | "Review the architecture for circular dependencies" |
| Ambiguous | **Ask user** | "What would you like me to analyze?" |

**Mode Selection CoD^Σ**:
```
UserMessage → ContextAnalysis
  ∣ contains("codebase", "structure", "overview") → mode=overview
  ∣ contains("how does", feature_name) → mode=feature, target=feature_name
  ∣ contains("architecture", "layers", "cycles") → mode=architecture
  ∣ else → AskUser("What would you like me to analyze? (overview/feature/architecture)")
```

---

## Workflow Files

**Mode-Specific Workflows** (Load based on detected mode):
- **@.claude/skills/analyze-code/workflows/overview-workflow.md** - Complete command chain for overview mode (stats → tree → list → search → summarize)
- **@.claude/skills/analyze-code/workflows/feature-workflow.md** - Complete command chain for feature mode (search → investigate → symbols → dependencies → importers)
- **@.claude/skills/analyze-code/workflows/architecture-workflow.md** - Complete command chain for architecture mode (map-imports → trace → metrics → analyze patterns)

**Reference Materials**:
- **@.claude/skills/analyze-code/references/decision-trees.md** - Mode selection tree + 3 analysis type decision trees
- **@.claude/skills/analyze-code/references/enforcement-rules.md** - 3 non-negotiable rules (no naked claims, intel before reading, MCP for authority)

---

## Templates You Will Use

**Mode-Specific Output Templates**:
- **@.claude/templates/analysis/overview.md** - Repository overview template (mode=overview → refs/overview.md)
- **@.claude/templates/analysis/design.md** - Feature design template (mode=feature → refs/design.md)
- **@.claude/templates/analysis/architecture.md** - Architecture analysis template (mode=architecture → report.md)

**General Templates**:
- **@.claude/templates/analysis-spec.md** - Scope definition (Phase 1, all modes)
- **@.claude/templates/report.md** - Standard analysis reports with CoD^Σ traces
- **@.claude/templates/mcp-query.md** - Optional MCP queries (Phase 3)

---

## Intelligence Tool Guide

- **@.claude/shared-imports/project-intel-mjs-guide.md** - Complete project-intel.mjs usage

---

## The Process (Overview)

**See:** Mode-specific workflow files in @.claude/skills/analyze-code/workflows/ for complete command chains

Copy this checklist to track progress:

```
Analysis Progress:
- [ ] Phase 1: Scope (analysis-spec.md created)
- [ ] Phase 2: Intel Queries (4 query types executed)
- [ ] Phase 3: MCP Verification (findings verified)
- [ ] Phase 4: Report (CoD^Σ trace complete)
```

### Phase 1: Define Scope

**Create analysis-spec.md** using template to define:

1. **Objective**: What question are we answering?
   - "Why does LoginForm re-render infinitely?"
   - "What causes 500 error on checkout?"
   - "Is there circular dependency in auth module?"

2. **Scope**: What's in/out of scope?
   - In-Scope: Specific components, files, functions
   - Out-of-Scope: Backend, database, third-party APIs

3. **Success Criteria**: How do we know when done?
   - "Root cause identified with file:line reference"
   - "Complete dependency graph generated"
   - "Performance bottleneck located"

**Enforcement Checklist:**
- [ ] Objective is clear and answerable
- [ ] In-scope/out-of-scope explicitly defined
- [ ] Success criteria are testable

---

### Phase 2: Execute Intel Queries

**CRITICAL:** Execute ALL intel queries BEFORE reading any files.

**4 Required Query Types:**

1. **Project Overview** (if first analysis in session):
   ```bash
   project-intel.mjs --overview --json > /tmp/analysis_overview.json
   ```
   Purpose: Understand project structure, entry points, file counts
   Tokens: ~50

2. **Search for Relevant Files**:
   ```bash
   project-intel.mjs --search "<pattern>" --type <filetype> --json > /tmp/analysis_search.json
   ```
   Purpose: Locate files related to objective
   Tokens: ~100

3. **Symbol Analysis** (for each relevant file):
   ```bash
   project-intel.mjs --symbols <filepath> --json > /tmp/analysis_symbols_<filename>.json
   ```
   Purpose: Understand functions/classes without reading full file
   Tokens: ~150 per file

4. **Dependency Tracing**:
   ```bash
   # What does this file import?
   project-intel.mjs --dependencies <filepath> --direction upstream --json > /tmp/analysis_deps_up.json

   # What imports this file?
   project-intel.mjs --dependencies <filepath> --direction downstream --json > /tmp/analysis_deps_down.json
   ```
   Purpose: Understand dependencies and impact
   Tokens: ~200 total

**Token Comparison:**
- Reading full LoginForm.tsx (1000 lines): ~3000 tokens
- Intel queries + targeted read (30 lines): ~300 tokens
- **Savings: 90%**

**Enforcement Checklist:**
- [ ] All 4 query types executed
- [ ] Intel results saved to /tmp/ for evidence
- [ ] No files read before intel queries complete

**See:** @.claude/skills/analyze-code/workflows/{mode}-workflow.md for complete query examples

---

### Phase 3: MCP Verification

Verify findings with authoritative sources:

**When to Use Each MCP:**

| MCP Tool | Use For | Example |
|----------|---------|---------|
| **Ref** | Library/framework behavior | React hooks, Next.js routing, TypeScript |
| **Supabase** | Database schema, RLS policies | Table structure, column types |
| **Shadcn** | Component design patterns | shadcn/ui component usage |
| **Chrome** | Runtime behavior validation | E2E testing, browser behavior |

**MCP Verification Pattern:**
```markdown
## Intel Finding
[What intelligence queries revealed]

## MCP Verification
**Tool:** [Which MCP tool]
**Query:** [Exact query executed]
**Result:** [What authoritative source says]

## Comparison
- **Intel shows:** [From project-intel.mjs]
- **Docs require:** [From MCP verification]
- **Conclusion:** [Agreement or discrepancy]
```

**Enforcement Checklist:**
- [ ] At least 1 MCP verification for non-trivial findings
- [ ] MCP results documented in Evidence section
- [ ] Discrepancies between intel and MCP flagged

**See:** @.claude/skills/analyze-code/workflows/{mode}-workflow.md for complete verification examples

---

### Phase 4: Generate Report

Create comprehensive report using **@.claude/templates/report.md**

**Required: CoD^Σ Trace**

Every report MUST include complete reasoning chain with symbolic operators:

```markdown
## CoD^Σ Trace

**Claim:** [Your conclusion with file:line reference]

**Trace:**
```
Step 1: → IntelQuery("search <pattern>")
  ↳ Source: project-intel.mjs --search "<pattern>" --type <type>
  ↳ Data: [What was found]
  ↳ Tokens: [Token count]

Step 2: ⇄ IntelQuery("analyze symbols")
  ↳ Source: project-intel.mjs --symbols <file>
  ↳ Data: [Functions/classes found with line numbers]
  ↳ Tokens: [Token count]

Step 3: → TargetedRead(lines X-Y)
  ↳ Source: Read <file> (lines X-Y only)
  ↳ Data: [Relevant code excerpt]
  ↳ Tokens: [Token count]

Step 4: ⊕ MCPVerify("<tool>")
  ↳ Tool: <MCP tool> - "<query>"
  ↳ Data: [What authoritative source says]
  ↳ Tokens: [Token count]

Step 5: ∘ Conclusion
  ↳ Logic: [Reasoning from data to conclusion]
  ↳ Root Cause: <file>:<line> - [What's wrong]
  ↳ Fix: [How to resolve]
```
**Total Tokens:** [Sum] (vs [baseline] for reading full files)
**Savings:** [Percentage]
```
```

**Report Sections:**

1. **Summary** (max 200 tokens): Key finding, root cause with file:line, recommended fix
2. **CoD^Σ Trace** (as shown above): Complete reasoning chain, token counts, savings
3. **Evidence**: All intel query results, MCP verification, targeted file excerpts
4. **Recommendations**: Specific fixes, implementation guidance, testing approach

**File Naming:** `YYYYMMDD-HHMM-report-<id>.md`

**Enforcement Checklist:**
- [ ] Report uses template structure
- [ ] CoD^Σ trace complete
- [ ] Every claim has file:line or MCP evidence
- [ ] Recommendations are specific
- [ ] Total report ≤ 1000 tokens when populated

**See:** @.claude/skills/analyze-code/workflows/{mode}-workflow.md for complete report examples

---

## Decision Trees for Different Analysis Types

**See:** @.claude/skills/analyze-code/references/decision-trees.md

**Summary:**

- **Tree 1: Bug Diagnosis** - Search error → Locate function → Trace dependencies → Find discrepancy → Verify with MCP → Report
- **Tree 2: Architecture Analysis** - Get overview → Identify entry points → Trace dependencies → Build graph → Analyze patterns → Report
- **Tree 3: Performance Analysis** - Search slow operations → Trace data flow → Identify bottlenecks → Measure impact → Verify best practices → Report

Choose based on user's request type. Can combine multiple trees for complex analyses.

---

## Enforcement Rules

**See:** @.claude/skills/analyze-code/references/enforcement-rules.md

**Summary:**

### Rule 1: No Naked Claims
Every claim MUST have file:line reference and evidence from intelligence queries or MCP verification.

### Rule 2: Intel Before Reading
Query project-intel.mjs BEFORE reading any files. Achieve 90-97% token savings.

### Rule 3: MCP for Authority
Verify library/framework behavior with authoritative MCP sources, not memory or assumptions.

**These rules are non-negotiable. Violations invalidate the analysis.**

---

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Skipping intel queries | 10-100x token waste | Enforce Phase 2 before any reads |
| Vague conclusions | Not actionable | Always include file:line references |
| No MCP verification | Incorrect assumptions | Verify library behavior with Ref MCP |
| Incomplete CoD^Σ trace | Can't verify reasoning | Document every reasoning step |

---

## Success Metrics

**Token Efficiency:**
- Intel-first: 500-2000 tokens per analysis
- Direct reading: 5000-20000 tokens
- **Target: 80%+ savings** ✓

**Accuracy:**
- Root cause identified: 95%+
- MCP verified: 100% for library issues

**Completeness:**
- All claims evidenced: 100%
- CoD^Σ trace complete: 100%

---

## When to Use This Skill

**Use analyze-code when:**
- User wants to **understand the codebase** (overview mode)
- User asks "**how does [feature] work**" (feature mode)
- User wants to **review architecture** (architecture mode)
- User needs **dependency analysis** or **impact assessment**
- User is **exploring unfamiliar code** or **building documentation**

**What This Skill Does NOT Do (Delegate Instead):**

❌ **Bug Diagnosis** → Use **debug-issues** skill instead
- Error messages, stack traces, "why is X broken?"
- Infinite loops, memory leaks, crashes
- Root cause analysis of failures

❌ **Performance Profiling** → Use **perf-analysis** skill (if available)
- Slow page loads, high CPU usage
- Memory profiling, bottleneck identification

❌ **Security Scanning** → Use **security-audit** skill (if available)
- Vulnerability detection, exposed secrets
- Security best practices validation

✅ **This Skill Creates**:
- `refs/overview.md` - Repository map for reference
- `refs/design.md` - Feature context for development
- `report.md` - Architecture analysis with patterns

**Scope Boundaries**:
- **analyze-code**: Structure understanding (what exists, how it's organized)
- **debug-issues**: Problem solving (why it's broken, how to fix)

---

## Prerequisites

Before using this skill:
- ✅ PROJECT_INDEX.json exists (run `/index` if missing)
- ✅ project-intel.mjs is executable
- ✅ Code to analyze exists in repository
- ⚠️ For external library analysis: MCP tools configured (Ref, Context7)

---

## Dependencies

**Depends On**:
- None (this skill is standalone and doesn't require other skills to run first)

**Integrates With**:
- **debug-issues skill**: Use after this skill if analysis reveals bugs
- **create-implementation-plan skill**: Use after this skill to plan fixes/enhancements

**Tool Dependencies**:
- project-intel.mjs (intelligence queries)
- MCP Ref tool (library documentation)
- MCP Context7 tool (external docs)

---

## Next Steps

After analysis completes, typical next steps:

**If bugs found**:
```
analyze-code → debug-issues skill → create-implementation-plan skill → implement-and-verify skill
```

**If performance issues found**:
```
analyze-code → create-implementation-plan skill (optimization) → implement-and-verify skill
```

**If architecture review**:
```
analyze-code → create-implementation-plan skill (refactoring) → implement-and-verify skill
```

**Commands to invoke**:
- `/bug` - If analysis reveals specific bugs
- `/plan` - To create implementation plan for fixes
- `/implement` - After plan exists, to execute changes

---

## Failure Modes

**Purpose**: Identify and fix the 5 most common intelligence-first analysis failures.

### Failure 1: PROJECT_INDEX.json Missing or Stale

**Symptom**:
- `project-intel.mjs --overview --json` returns "Error: PROJECT_INDEX.json not found"
- `project-intel.mjs --search "LoginForm" --json` returns empty results despite files existing

**Impact**: Intelligence queries fail or return empty results, forcing direct file reading (token waste)

**Solution**:
```bash
# Immediate fix: Generate PROJECT_INDEX.json
/index

# Verify generation
ls -la PROJECT_INDEX.json
project-intel.mjs --overview --json
```

**Prevention**:
- Hook auto-generates index on file changes (configure in .claude/settings.json)
- Run `/index` at session start if index missing
- Check index timestamp vs latest code changes

---

### Failure 2: Intelligence Queries Return No Results

**Symptom**:
- `project-intel.mjs --search "auth" --type tsx --json` returns empty despite auth files existing
- `project-intel.mjs --symbols src/components/LoginForm.tsx --json` returns "File not found in index"

**Impact**: Cannot locate relevant code, may incorrectly conclude code doesn't exist

**Root Causes**:
1. File excluded by .gitignore (node_modules/, .next/, dist/)
2. Wrong file type filter (searching --type tsx but file is .ts)
3. Typo in search pattern ("lgin" instead of "login")
4. File not yet indexed (new file created after index generation)

**Solution**:
```bash
# Step 1: Verify file exists
ls -la src/components/LoginForm.tsx
git check-ignore -v src/components/LoginForm.tsx

# Step 2: Regenerate index
/index

# Step 3: Verify index contents
project-intel.mjs --stats --json
project-intel.mjs --search "login" --json  # No type filter

# Step 4: Adjust search strategy
project-intel.mjs --search "Login" --json
project-intel.mjs --search "auth" --type ts --json
```

**Prevention**: Run `/index` after creating new files, use broader search terms initially

---

### Failure 3: MCP Tools Not Available

**Symptom**:
- "Tool call failed: mcp__Ref__ref_search_documentation"
- "Error: MCP server 'Ref' not configured"

**Impact**: Cannot verify library behavior, must rely on memory (less accurate)

**Solution**:
```bash
# Check MCP configuration
cat .mcp.json

# Configure Ref MCP (example)
{
  "mcpServers": {
    "ref": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-ref"]
    }
  }
}
```

**Workaround** (if MCP unavailable):
- Skip external library verification
- Note in report: "MCP verification unavailable"
- Focus analysis on internal code only
- Use web search as fallback

---

### Failure 4: Analysis Scope Too Broad

**Symptom**:
- Token limit exceeded
- Analysis incomplete
- Multiple unrelated issues found
- Report exceeds 1000 tokens

**Impact**: Cannot complete analysis, findings lack depth, token budget exhausted

**Root Causes**:
1. No scope defined (analyzing entire codebase)
2. Overly broad search (searching for "component" or "function")
3. Reading full files (not using targeted reads after intel queries)
4. Multiple unrelated issues (trying to solve everything at once)

**Solution**:

**Define Narrow Scope**:
```markdown
# analysis-spec.md
## Objective
Identify why LoginForm component re-renders infinitely

## In-Scope
- LoginForm.tsx only
- Related hooks (useEffect, useState)
- Direct dependencies only

## Out-of-Scope
- Other components
- Backend API
- Routing
```

**Use Targeted Searches**:
```bash
# ❌ Too broad
project-intel.mjs --search "component" --json

# ✅ Specific
project-intel.mjs --search "LoginForm" --type tsx --json
```

**Read Targeted Lines**:
```bash
# ❌ Full file
Read src/components/LoginForm.tsx

# ✅ Specific lines (after intel queries identify location)
sed -n '40,60p' src/components/LoginForm.tsx
```

**Prevention**: Define scope in analysis-spec.md before starting, use specific search terms, target single issue per analysis

---

### Failure 5: CoD^Σ Evidence Missing

**Symptom**:
- Report makes claims without file:line references
- No intelligence query results shown
- Missing reasoning steps
- Cannot verify findings

**Impact**: No audit trail, others can't reproduce analysis, recommendations lack credibility

**Root Causes**:
1. Skipped evidence collection (made claims without querying)
2. Intel queries not documented (ran queries but didn't save results)
3. MCP verification skipped (assumed behavior without checking)
4. CoD^Σ trace incomplete (missing reasoning steps)

**Solution**:

**Complete Intel Queries**:
```bash
# Save all intel query results
project-intel.mjs --search "LoginForm" --json > /tmp/search.json
project-intel.mjs --symbols src/LoginForm.tsx --json > /tmp/symbols.json
project-intel.mjs --dependencies src/LoginForm.tsx --json > /tmp/deps.json
```

**Document Every Step in CoD^Σ Trace**:
```markdown
## CoD^Σ Trace

**Claim:** LoginForm re-renders at src/LoginForm.tsx:45

**Trace:**
Step 1: → IntelQuery("search LoginForm")
  ↳ Source: project-intel.mjs --search "LoginForm" --type tsx
  ↳ Data: Found src/components/LoginForm.tsx
  ↳ Tokens: 100

Step 2: ⇄ IntelQuery("analyze symbols")
  ↳ Source: project-intel.mjs --symbols src/components/LoginForm.tsx
  ↳ Data: useEffect at line 45
  ↳ Tokens: 150

Step 3: → TargetedRead(lines 40-60)
  ↳ Source: sed -n '40,60p' src/components/LoginForm.tsx
  ↳ Data: useEffect(() => { setUser({...user}) }, [user])
  ↳ Tokens: 100

Step 4: ⊕ MCPVerify("React docs")
  ↳ Tool: Ref MCP - "React useEffect dependencies"
  ↳ Data: "Every value must be in dependency array"
  ↳ Tokens: 200

Step 5: ∘ Conclusion
  ↳ Logic: Effect depends on [user] and mutates user
  ↳ Root Cause: src/LoginForm.tsx:45 infinite loop
  ↳ Fix: Use functional setState

**Total Tokens:** 550
```

**Enforcement Checklist**:
- [ ] All intel queries documented with commands
- [ ] Intel results saved to /tmp/*.json
- [ ] CoD^Σ trace shows all 5 steps
- [ ] MCP verification included (if applicable)
- [ ] Targeted read excerpts included
- [ ] Every claim has file:line reference

**Report is incomplete until all checkboxes checked**

---

### Diagnostic Workflow for All Failures

When analysis fails:
```
Failure detected
    ↓
1. Check index (Failure 1)
   → PROJECT_INDEX.json exists and fresh?
    ↓
2. Check queries (Failure 2)
   → Intel queries return results?
    ↓
3. Check MCP (Failure 3)
   → MCP tools configured and working?
    ↓
4. Check scope (Failure 4)
   → Scope narrow and well-defined?
    ↓
5. Check evidence (Failure 5)
   → CoD^Σ trace complete with evidence?
```

**Quick Reference**:

| Failure | Symptom | Quick Fix |
|---------|---------|-----------|
| **1. Index Missing** | Intel queries fail | Run `/index` |
| **2. No Results** | Empty search results | Regenerate index, broaden search |
| **3. MCP Unavailable** | MCP tool errors | Configure .mcp.json, use workaround |
| **4. Scope Too Broad** | Token limit exceeded | Define narrow scope in analysis-spec.md |
| **5. Missing Evidence** | Claims lack proof | Save intel results, complete CoD^Σ trace |

**Remember**: Most analysis failures are preventable with proper scope definition and systematic intelligence queries

---

## Related Skills & Commands

**Direct Integration**:
- **debug-issues skill** - Use after this skill when bugs are identified
- **create-implementation-plan skill** - Use after analysis to plan changes
- **/analyze command** - User-facing command that invokes this skill
- **code-analyzer subagent** - Subagent that routes to this skill

**Workflow Context**:
- Position: Can be used at any time (analysis is standalone)
- Triggers: User mentions "analyze", "review", "understand", "architecture"
- Output: report.md or analysis-spec.md using templates

---

## Agent Integration

**Subagent Usage**:

When the code-analyzer subagent delegates work to this skill, it provides:
- Initial problem statement
- Suspected file locations (if known)
- Context from user conversation

This skill then:
1. Creates analysis-spec.md from provided context
2. Executes intelligence queries
3. Generates report with CoD^Σ trace
4. Returns findings to subagent

**Task Tool Example**:
```python
# From code-analyzer subagent
Task(
    subagent_type="code-analyzer",
    description="Analyze infinite render bug",
    prompt="""
    @.claude/skills/analyze-code/SKILL.md

    User reports: LoginForm component re-renders infinitely

    Use intelligence-first approach:
    1. Query project-intel.mjs for LoginForm location
    2. Analyze symbols to find hooks
    3. Verify React patterns with MCP Ref
    4. Generate report with CoD^Σ trace

    Output: Complete report.md with root cause and fix
    """
)
```

---

## Version

**Version:** 1.1.0
**Last Updated:** 2025-10-23
**Change Log**:
- v1.1.0 (2025-10-23): Refactored to progressive disclosure pattern (<500 lines)
- v1.0.0 (2025-10-19): Initial version

**Owner:** Claude Code Intelligence Toolkit
