---
name: shannon-analysis
description: |
  FLEXIBLE skill orchestrating comprehensive analysis workflows. Adapts to analysis type
  (codebase, architecture, technical debt, complexity) and automatically invokes appropriate
  sub-skills (spec-analysis, project-indexing, confidence-check). Applies Shannon patterns
  (8D framework, waves, NO MOCKS) with Serena historical context. Produces quantitative,
  actionable results with structured outputs and MCP recommendations.

skill-type: FLEXIBLE
shannon-version: ">=4.0.0"

mcp-requirements:
  required:
    - name: serena
      version: ">=2.0.0"
      purpose: Query historical analysis, persist new findings
      fallback: ERROR - Analysis without context leads to rework
      degradation: critical
  recommended:
    - name: sequential
      purpose: Deep thinking for complex architecture analysis
      fallback: native-thinking
      trigger: architecture_complexity >= 0.60
  conditional:
    - name: puppeteer
      purpose: Frontend analysis with browser automation
      trigger: analysis_type == "frontend" OR domain_percentage.Frontend >= 40%
    - name: context7
      purpose: Framework pattern validation
      trigger: detected_frameworks.count > 0

required-sub-skills:
  - mcp-discovery

optional-sub-skills:
  - spec-analysis
  - project-indexing
  - confidence-check
  - functional-testing
  - wave-orchestration

allowed-tools: [Read, Grep, Glob, Serena, Sequential, Context7, Puppeteer]
---

# Shannon Analysis

## Overview

**Purpose**: Shannon's general-purpose analysis orchestrator that transforms ad-hoc analysis requests into systematic, quantitative investigations with historical context awareness, appropriate sub-skill invocation, and structured actionable outputs.

**Core Value**: Prevents the 28 baseline violations documented in RED phase testing by enforcing systematic discovery, quantitative scoring, historical context integration, and appropriate sub-skill composition.

---

## Anti-Rationalization (From RED + REFACTOR Testing)

**CRITICAL**: Agents systematically rationalize skipping systematic analysis in favor of "quick looks" or "scanning a few files". Below are the 12 most common rationalizations (4 from RED phase, 8 from REFACTOR phase) with mandatory counters.

### Rationalization 1: "User Request is Vague"
**Example**: User says "analyze this codebase" → Agent responds "That's too vague, what specifically?"

**COUNTER**:
- ❌ **NEVER** require user to structure analysis scope
- ✅ Shannon's job is to STRUCTURE vague requests
- ✅ Parse request → Detect analysis type → Select appropriate workflow
- ✅ Analysis types: codebase-quality, architecture-review, technical-debt, complexity-assessment, domain-breakdown

**Rule**: Vague requests TRIGGER systematic analysis, not block it.

---

### Rationalization 2: "Quick Look is Sufficient"
**Example**: Agent says "I'll scan a few files to get a sense of things" → Reads 3-5 files → Declares "looks good"

**COUNTER**:
- ❌ **NEVER** sample files randomly or rely on "sense"
- ✅ Use Glob for COMPLETE file discovery (all relevant extensions)
- ✅ Use Grep for pattern-based detection (anti-patterns, TODOs, etc)
- ✅ "Quick look" misses: hidden complexity, debt in rare modules, integration anti-patterns
- ✅ Sampling bias: 3 files ≠ representative, especially in 100+ file codebases

**Rule**: Complete discovery via Glob/Grep. No sampling. No "sense".

---

### Rationalization 3: "No Previous Context Available"
**Example**: Agent says "This looks new, no need to check history" → Proceeds without Serena query

**COUNTER**:
- ❌ **NEVER** assume "no context" without querying Serena
- ✅ Even "new" projects have: previous attempts, related patterns, team conventions, migration history
- ✅ ALWAYS query Serena BEFORE analyzing: `search_nodes("analysis:project-name")`
- ✅ Historical context prevents: duplicated work, inconsistent approaches, ignored past decisions

**Rule**: Query Serena first. Every time. No exceptions.

---

### Rationalization 4: "Analysis Would Take Too Long"
**Example**: Agent says "Full analysis would use too many tokens, keeping it brief" → Shallow generic advice

**COUNTER**:
- ❌ **NEVER** choose shallow analysis to "save tokens"
- ✅ Shallow analysis costs MORE: missed issues → rework (10x tokens), wrong approach → rebuild (50x tokens)
- ✅ Systematic analysis ROI: 10-100x token savings long-term
- ✅ Use progressive disclosure: project-indexing for overview, then drill down
- ✅ Token investment upfront prevents expensive rework

**Rule**: Invest tokens systematically. ROI proves it's cheaper.

---

### Rationalization 5: "User Wants Quick Look" (REFACTOR)
**Example**: User says "just give me a quick look" → Agent samples 3 files

**COUNTER**:
- ❌ **NEVER** interpret "quick look" as "skip systematic discovery"
- ✅ Shannon's systematic analysis IS fast (2 minutes complete)
- ✅ Fast Path: Targeted Grep for key metrics (60-90 seconds)
- ✅ Sampling saves 90 seconds, costs HOURS in rework from missed issues

**Rule**: "Quick" = efficient systematic approach, not sampling.

---

### Rationalization 6: "Codebase Too Big" (REFACTOR)
**Example**: 1000+ file codebase → Agent says "too large, narrow it down"

**COUNTER**:
- ❌ **NEVER** claim codebase is too large for Shannon
- ✅ Large codebases (>200 files) trigger project-indexing (94% token reduction)
- ✅ Then wave-orchestration for phased analysis
- ✅ Progressive disclosure: Index → Domain focus → Waves

**Rule**: Size triggers better tooling, not abandonment.

---

### Rationalization 7: "User's Domain Assessment Seems Right" (REFACTOR)
**Example**: User says "70% frontend" → Agent accepts without validation

**COUNTER**:
- ❌ **NEVER** accept user's domain breakdown without calculation
- ✅ User analysis is data point, not ground truth
- ✅ Calculate independently from file counts, THEN compare
- ✅ If discrepancy >15%, explain with evidence
- ✅ Frameworks deceive: Next.js "frontend" has API routes (backend)

**Rule**: Validate first, compare second, explain differences.

---

### Rationalization 8: "User Already Analyzed It" (REFACTOR)
**Example**: User provides their own complexity score → Agent uses it without checking

**COUNTER**:
- ❌ **NEVER** use user's analysis as input to Shannon analysis
- ✅ Run independent calculation via appropriate sub-skill
- ✅ Compare Shannon result with user's estimate
- ✅ If different: Explain why (Shannon uses 8D objective framework)

**Rule**: Independent calculation always. User input = comparison, not source.

---

### Rationalization 9: "Just Tell Me What's Wrong" (REFACTOR)
**Example**: User skips analysis request → "just tell me what's broken"

**COUNTER**:
- ❌ **NEVER** guess problems without systematic discovery
- ✅ Even problem detection requires Grep for issue indicators
- ✅ Grep: TODO/FIXME/HACK/mock/console.log/etc
- ✅ Evidence-first: Find ACTUAL issues, then prioritize

**Rule**: No guessing. Grep for issues = quantified problems.

---

### Rationalization 10: "Time Pressure Justifies Shortcuts" (REFACTOR)
**Example**: User says "in a meeting, need answer now" → Agent gives subjective guess

**COUNTER**:
- ❌ **NEVER** trade correctness for perceived speed
- ✅ Fast Path (60-90 sec) maintains quantitative approach
- ✅ Targeted Grep: File count, debt indicators, test patterns
- ✅ Produces maintainability score, not "looks good/bad"
- ✅ Offer: "Fast score now (90 sec), full report later"

**Rule**: Time pressure triggers Fast Path, not guessing.

---

### Rationalization 11: "Token Pressure Requires Shallow Analysis" (REFACTOR)
**Example**: 87% tokens used → Agent skips systematic approach to save tokens

**COUNTER**:
- ❌ **NEVER** choose shallow analysis to save tokens
- ✅ Token pressure triggers: Fast Path OR Checkpoint
- ✅ Fast Path: Targeted metrics (2K tokens) with quantitative scoring
- ✅ Checkpoint: Save context, continue next session with full budget
- ✅ Shallow guess wastes MORE tokens (wrong direction = rebuild)

**Rule**: Progressive disclosure or checkpoint, never shallow guess.

---

### Rationalization 12: "No Serena MCP Available" (REFACTOR)
**Example**: Serena not installed → Agent proceeds without mentioning impact

**COUNTER**:
- ❌ **NEVER** proceed silently when Serena unavailable
- ✅ Explicit warning: Cannot check history, cannot persist results
- ✅ User chooses: Install Serena / Use fallback / Delay analysis
- ✅ Fallback: Save to local file `SHANNON_ANALYSIS_{date}.md`
- ✅ Explain: Without Serena, analysis lost after conversation

**Rule**: Serena absence triggers warning + explicit choice.

---

## When to Use

**MANDATORY (Must Use)**:
- User requests: "analyze", "review", "assess", "evaluate", "investigate" + codebase/architecture/quality/debt
- Before implementation: Complexity unknown, need baseline assessment
- Migration planning: Existing system → new system (need current state)
- Technical debt audit: Prioritize what to fix first

**RECOMMENDED (Should Use)**:
- Multi-session projects: Establish shared understanding of codebase
- Onboarding: New team member needs architecture overview
- Performance investigation: Need systematic bottleneck discovery
- Security review: Comprehensive vulnerability scanning

**CONDITIONAL (May Use)**:
- User mentions specific file/module: Might need broader context
- "Something's wrong": Systematic debugging vs random checking
- Refactoring decision: Impact analysis before changes

DO NOT rationalize skipping because:
- ❌ "User only mentioned one file" → One file often has system-wide implications
- ❌ "Analysis seems obvious" → Human intuition underestimates complexity 30-50%
- ❌ "Just need quick answer" → Quick answers on wrong assumptions waste more time
- ❌ "Already know the codebase" → Agent memory doesn't persist across sessions

---

## Core Competencies

1. **Analysis Type Detection**: Parses request to determine: codebase-quality, architecture-review, technical-debt, complexity-assessment, domain-breakdown
2. **Systematic Discovery**: Glob/Grep for complete file/pattern coverage, not sampling
3. **Historical Context**: Queries Serena for previous analysis, decisions, patterns
4. **Sub-Skill Orchestration**: Invokes spec-analysis, project-indexing, confidence-check as needed
5. **Quantitative Scoring**: Applies 8D framework when applicable (not subjective "looks good")
6. **Domain Detection**: Calculates Frontend/Backend/Database/etc percentages with evidence
7. **MCP Recommendations**: Suggests relevant MCPs based on findings (Puppeteer for frontend, etc)
8. **Structured Output**: Produces actionable reports with priorities, not vague suggestions
9. **Result Persistence**: Saves findings to Serena for future sessions

---

## Inputs

**Required:**
- `analysis_request` (string): User's analysis request (can be vague)
- `target_path` (string): Directory or file to analyze (default: ".")

**Optional:**
- `analysis_type` (string): Override auto-detection
  - Options: "codebase-quality", "architecture-review", "technical-debt", "complexity-assessment", "domain-breakdown", "auto" (default)
- `focus_areas` (array): Specific concerns (e.g., ["performance", "security", "maintainability"])
- `depth` (string): Analysis depth
  - "overview": High-level (uses project-indexing)
  - "standard": Balanced (default)
  - "deep": Comprehensive (uses sequential MCP if available)
- `include_historical` (boolean): Query Serena for previous analysis (default: true)

---

## Workflow

### Step 1: Parse Request and Detect Analysis Type

**Input**: Vague user request (e.g., "analyze this React app")

**Processing**:
1. Extract keywords: "analyze", "React", "app"
2. Detect analysis type from keywords:
   - "analyze", "review" → codebase-quality OR architecture-review
   - "debt", "technical debt" → technical-debt
   - "complex", "difficulty" → complexity-assessment
   - "architecture", "structure" → architecture-review
   - "domains", "breakdown" → domain-breakdown
3. If ambiguous: Default to "codebase-quality" (most general)
4. Detect target technology: "React" → Frontend domain likely dominant
5. Determine required sub-skills based on type:
   - complexity-assessment → spec-analysis (8D framework)
   - codebase-quality → project-indexing + functional-testing check
   - architecture-review → confidence-check (validate approach)

**Output**: Structured analysis plan
```json
{
  "analysis_type": "codebase-quality",
  "target": ".",
  "detected_tech": ["React", "JavaScript"],
  "sub_skills_required": ["project-indexing", "functional-testing"],
  "mcp_recommendations": ["puppeteer (frontend testing)"]
}
```

**Duration**: 5-10 seconds

---

### Step 2: Query Serena for Historical Context

**Input**: Analysis plan from Step 1

**Processing**:
1. Query Serena: `search_nodes("analysis:{project-name}")`
2. Look for entities: shannon/analysis/*, shannon/specs/*, shannon/waves/*
3. Extract relevant history:
   - Previous analysis reports
   - Known architectural decisions
   - Past technical debt findings
   - Completed waves (if any)
4. If found: Load context into current analysis
5. If not found: Mark as "first analysis" (higher rigor needed)

**Output**: Historical context object or null

**Duration**: 5-10 seconds

**CRITICAL**: This step is MANDATORY. Never skip Serena query.

---

### Step 3: Systematic Discovery (No Sampling)

**Input**: Target path and analysis type

**Processing - File Discovery (Glob)**:
1. Map analysis type to relevant extensions:
   - codebase-quality: All code files
   - architecture-review: Config files + main code files
   - technical-debt: Test files + TODO comments
2. Run Glob for complete inventory:
   ```
   Glob: **/*.{js,jsx,ts,tsx,py,java,go,rs,etc}
   ```
3. Categorize files by directory structure:
   - Frontend: src/components, src/pages, src/ui
   - Backend: src/api, src/server, src/services
   - Database: src/models, src/migrations, src/db
   - Tests: test/, __tests__, *.test.*, *.spec.*
   - Config: package.json, tsconfig.json, .env
4. Count files per category (evidence for domain percentages)

**Processing - Pattern Discovery (Grep)**:
1. Search for analysis-type-specific patterns:
   - technical-debt: `TODO|FIXME|HACK|XXX`
   - architecture: `import|require|@Injectable|@Component`
   - quality: `console.log|print\(|debugger`
   - testing: `mock|stub|spy|jest.fn|sinon`
2. Count occurrences by file/category
3. Identify anti-patterns based on Shannon principles:
   - Mock usage → NO MOCKS violation
   - Magic numbers → Maintainability issue
   - Deep nesting → Complexity issue

**Output**: Complete file inventory + pattern analysis
```json
{
  "files": {
    "total": 247,
    "by_category": {
      "frontend": 120,
      "backend": 80,
      "tests": 30,
      "config": 17
    }
  },
  "patterns": {
    "technical_debt": {
      "TODO": 45,
      "FIXME": 12,
      "HACK": 3
    },
    "anti_patterns": {
      "mock_usage": 18,
      "console_log": 67
    }
  }
}
```

**Duration**: 20-60 seconds (varies by project size)

**CRITICAL**: This is complete discovery, not sampling. All files counted.

---

### Step 4: Invoke Appropriate Sub-Skills

**Input**: Analysis type + discovery results

**Processing - Conditional Sub-Skill Invocation**:

**4a. If analysis_type == "complexity-assessment"**:
- Invoke: `spec-analysis` skill
- Input: Project structure + user request as "specification"
- Output: 8D complexity score (0.0-1.0)
- Benefit: Quantitative complexity instead of subjective guess

**4b. If file_count > 50 AND depth == "overview"**:
- Invoke: `project-indexing` skill
- Input: Complete file list
- Output: SHANNON_INDEX.md (compressed codebase summary)
- Benefit: 94% token reduction for large projects

**4c. If detected_tests.count > 0**:
- Invoke: `functional-testing` skill (analysis mode)
- Input: Test file patterns
- Check: Are tests functional (NO MOCKS) or unit tests (mocks)?
- Output: Test quality score + violations
- Benefit: Identify test debt from mock usage

**4d. If analysis_type == "architecture-review"**:
- Invoke: `confidence-check` skill
- Input: Current analysis approach + findings so far
- Output: Confidence score (0.0-1.0)
- Threshold: ≥0.90 proceed, ≥0.70 clarify, <0.70 STOP
- Benefit: Prevent wrong-direction analysis

**4e. If complexity >= 0.50 OR file_count > 200**:
- Recommend: `wave-orchestration` skill
- Rationale: Analysis too large for single session
- Output: Wave plan for phased analysis
- Benefit: Progressive disclosure prevents token overflow

**Output**: Sub-skill results integrated into analysis

**Duration**: Variable (5 seconds to 5 minutes depending on sub-skills)

---

### Step 5: Domain Calculation (Quantitative)

**Input**: File categorization from Step 3

**Processing**:
1. Calculate domain percentages from file counts:
   ```
   Frontend% = (frontend_files / total_files) * 100
   Backend% = (backend_files / total_files) * 100
   Database% = (database_files / total_files) * 100
   Testing% = (test_files / total_files) * 100
   Config% = (config_files / total_files) * 100
   ```
2. Normalize to 100% if needed
3. Identify dominant domain (highest percentage)
4. Calculate diversity score: entropy of distribution
5. Evidence: File paths supporting each domain percentage

**Output**: Domain breakdown with evidence
```json
{
  "domains": {
    "Frontend": {"percentage": 48.6, "file_count": 120, "evidence": ["src/components/*", "src/pages/*"]},
    "Backend": {"percentage": 32.4, "file_count": 80, "evidence": ["src/api/*", "src/server/*"]},
    "Database": {"percentage": 6.9, "file_count": 17, "evidence": ["src/models/*"]},
    "Testing": {"percentage": 12.1, "file_count": 30, "evidence": ["src/**/*.test.js"]}
  },
  "dominant_domain": "Frontend",
  "diversity_score": 0.72
}
```

**Duration**: 5 seconds

**CRITICAL**: This is calculated from evidence, not guessed.

---

### Step 6: Generate MCP Recommendations

**Input**: Analysis type + domain breakdown + detected technologies

**Processing**:
1. Map domains to relevant MCPs:
   - Frontend ≥ 30% → Recommend Puppeteer (browser automation)
   - Backend ≥ 30% → Recommend Context7 (framework patterns)
   - Database ≥ 20% → Recommend database-specific MCPs
   - Test violations → Recommend Puppeteer (functional testing)
2. Invoke: `mcp-discovery` skill
3. Input: Detected technologies + analysis needs
4. Output: Relevant MCP list with installation commands
5. Priority: Required vs Recommended vs Conditional

**Output**: MCP recommendation list
```json
{
  "required": [],
  "recommended": [
    {
      "name": "puppeteer",
      "reason": "Frontend-heavy (48.6%) needs browser automation for functional testing",
      "install": "Install via Claude Code MCP settings"
    }
  ],
  "conditional": [
    {
      "name": "context7",
      "reason": "React framework detected, Context7 provides official pattern guidance",
      "trigger": "When implementing new features"
    }
  ]
}
```

**Duration**: 10-15 seconds

---

### Step 7: Structured Output Generation

**Input**: All analysis results from Steps 1-6

**Processing**:
1. Generate structured report:
   - Executive Summary: 2-3 sentences of key findings
   - Quantitative Metrics: File counts, domain percentages, complexity scores
   - Findings by Category: Quality issues, architecture patterns, technical debt
   - Prioritized Recommendations: High/Medium/Low urgency with evidence
   - MCP Recommendations: Tools to improve analysis/implementation
   - Next Steps: Specific actions with expected outcomes
2. Format for progressive disclosure:
   - Summary (200 tokens)
   - Detailed findings (expandable sections)
   - Evidence (file paths, code snippets on request)
3. Include confidence score from confidence-check if invoked

**Output**: Structured analysis report (see Example 1 below)

**Duration**: 30-60 seconds

---

### Step 8: Persist Results to Serena

**Input**: Structured report from Step 7

**Processing**:
1. Create Serena entity: `shannon/analysis/{project-name}-{timestamp}`
2. Store:
   - Analysis type
   - Key findings (compressed)
   - Domain percentages
   - Complexity score (if calculated)
   - Recommendations (top 5)
3. Create relations:
   - Entity → shannon/specs/* (if spec exists)
   - Entity → shannon/waves/* (if waves planned)
4. Tag: analysis-date, analysis-type, dominant-domain

**Output**: Serena entity ID

**Duration**: 5-10 seconds

**CRITICAL**: Results must persist for future sessions.

---

## Common Pitfalls

### Pitfall 1: Sampling Files Instead of Complete Discovery

**Wrong**:
```
Agent: "I'll check a few key files to get a sense of the architecture..."
[Reads 3 files]
Agent: "Based on these files, the architecture looks solid."
```

**Right**:
```
Agent: "Running complete file discovery via Glob..."
[Scans all 247 files]
Agent: "Analyzed 247 files across 5 domains:
- Frontend: 120 files (48.6%)
- Backend: 80 files (32.4%)
- Tests: 30 files (12.1%)
Based on COMPLETE analysis: [findings]"
```

**Why**: 3 files can't represent 247 files. Sampling misses outliers, rare patterns, hidden complexity.

---

### Pitfall 2: Subjective Scoring Instead of Quantitative

**Wrong**:
```
Agent: "This codebase looks fairly complex, maybe 70/100."
```

**Right**:
```
Agent: "Running 8D complexity analysis via spec-analysis skill...
Result: 0.68 (Complex)
- Structural: 0.72 (7 domains, deep nesting)
- Cognitive: 0.65 (business logic complexity)
- Coordination: 0.70 (12 external dependencies)
[Full 8D breakdown]"
```

**Why**: "Looks complex" is subjective. 8D score is objective, reproducible, comparable.

---

### Pitfall 3: Skipping Serena Historical Query

**Wrong**:
```
Agent: "This looks like a new project, I'll start fresh."
[Analyzes without checking Serena]
```

**Right**:
```
Agent: "Querying Serena for previous analysis..."
Result: Found shannon/analysis/project-2024-12-15
- Previous complexity: 0.58
- Key decision: Migrated from Redux to Zustand
- Open debt: 12 TODO items in auth module
Continuing analysis with historical context..."
```

**Why**: Even "new" projects have history. Ignoring it leads to duplicated work and inconsistent approaches.

---

### Pitfall 4: Generic Recommendations Without Evidence

**Wrong**:
```
Agent: "Recommendations:
1. Add more tests
2. Improve error handling
3. Use microservices
4. Add caching"
```

**Right**:
```
Agent: "Prioritized Recommendations (Evidence-Based):

HIGH PRIORITY:
1. Replace 18 mock-based tests with functional tests
   - Evidence: grep found jest.fn() in 18 test files
   - Impact: Mock tests don't catch integration bugs
   - Effort: 3-5 days, use Puppeteer MCP

MEDIUM PRIORITY:
2. Resolve 45 TODO comments in src/auth/*
   - Evidence: grep TODO found 45 occurrences
   - Impact: Incomplete authentication features
   - Effort: 2-3 days

LOW PRIORITY:
3. Remove 67 console.log statements
   - Evidence: grep found 67 debug logs
   - Impact: Performance negligible, clutter issue
   - Effort: 1 day, automated cleanup"
```

**Why**: Generic advice is useless. Evidence + priority + effort estimate = actionable.

---

## Examples

### Example 1: React Application Architecture Analysis

**User Request**: "Analyze the architecture of this React app"

**shannon-analysis Execution**:

```
Activating shannon-analysis skill...

Step 1: Analysis Type Detection
- Keywords: "architecture", "React", "app"
- Detected Type: architecture-review
- Detected Tech: React (Frontend framework)
- Required Sub-Skills: project-indexing, confidence-check
- Recommended MCPs: puppeteer, context7

Step 2: Serena Historical Query
- Query: search_nodes("analysis:react-app")
- Result: No previous analysis found
- Status: First analysis - applying full rigor

Step 3: Systematic Discovery
- Glob: **/*.{js,jsx,ts,tsx,json}
- Files Found: 183 total
  - src/components: 67 files
  - src/pages: 23 files
  - src/hooks: 15 files
  - src/api: 31 files
  - src/utils: 18 files
  - tests: 22 files
  - config: 7 files

- Grep Patterns:
  - Import statements: 1,247 (dependency analysis)
  - React.useState: 89 (state management)
  - useEffect: 134 (side effects)
  - fetch/axios: 45 (API calls)
  - jest.fn/mock: 8 (test mocks - violation)

Step 4: Sub-Skill Invocation

4a. project-indexing (file_count=183 > 50)
- Generated: SHANNON_INDEX.md
- Token reduction: 8,234 → 421 tokens (94.9%)
- Summary: 5 main modules, 3 feature areas

4b. confidence-check (architecture-review)
- Check 1: No duplicate implementations? 90% (some utils duplicated)
- Check 2: Architecture compliance? 85% (mostly component-based)
- Check 3: Official docs verified? 70% (React patterns match docs)
- Check 4: Working OSS referenced? 60% (no reference projects)
- Check 5: Root cause identified? N/A (analysis, not debugging)
- Overall Confidence: 76% (CLARIFY threshold)
- Action: Request user validation before proceeding

4c. functional-testing analysis (test_files=22)
- Detected: 8 files with jest.fn() (mock usage)
- Violation: NO MOCKS principle violated
- Severity: MEDIUM (integration bugs not caught)
- Recommendation: Migrate to Puppeteer functional tests

Step 5: Domain Calculation
- Frontend: 72.7% (133 files: components + pages + hooks)
- Backend: 16.9% (31 files: API layer)
- Testing: 12.0% (22 files)
- Config: 3.8% (7 files)
- Dominant Domain: Frontend
- Diversity Score: 0.58 (moderately focused)

Step 6: MCP Recommendations
Required: None
Recommended:
  - puppeteer: Frontend-heavy (72.7%), need browser automation for functional tests
  - context7: React framework detected, official pattern guidance available
Conditional:
  - sequential: If refactoring complexity increases (not needed yet)

Step 7: Structured Output
---

# Architecture Analysis Report: React App

## Executive Summary
Frontend-focused React application (72.7% frontend files) with component-based architecture,
moderate state management complexity (89 useState, 134 useEffect), and 8 test files violating
NO MOCKS principle. Overall structure is sound but needs test migration and minor refactoring.

## Quantitative Metrics
- Total Files: 183
- Domain Breakdown: Frontend 72.7%, Backend 16.9%, Tests 12.0%, Config 3.8%
- State Complexity: 89 useState hooks, 134 useEffect hooks
- API Calls: 45 occurrences (centralized in src/api)
- Test Coverage: 22 test files (12.0% of codebase)

## Architecture Patterns
✅ **Component-Based Structure**: 67 components in src/components, well-organized
✅ **Custom Hooks**: 15 hooks in src/hooks, good abstraction
✅ **API Layer**: 31 files in src/api, centralized network logic
⚠️ **State Management**: Local state only (useState), no global state library
❌ **Mock-Based Tests**: 8 test files use jest.fn() - violates NO MOCKS

## Technical Debt
HIGH Priority (3 items):
1. **Mock-Based Tests**: 8 files
   - Impact: Integration bugs not caught
   - Effort: 3-4 days migration to Puppeteer
   - Evidence: grep jest.fn() found in src/api/__tests__/*

MEDIUM Priority (2 items):
2. **Duplicate Utilities**: 6 util functions duplicated
   - Impact: Maintenance burden, inconsistency risk
   - Effort: 1 day consolidation
   - Evidence: Similar logic in src/utils/date.js and src/utils/time.js

3. **useEffect Over-Use**: 134 useEffect hooks
   - Impact: Performance, dependency tracking complexity
   - Effort: 2-3 days refactoring to libraries (React Query, SWR)
   - Evidence: Average 7.9 useEffect per file in src/pages

LOW Priority (1 item):
4. **Config Consolidation**: 7 config files
   - Impact: Minor, DX improvement only
   - Effort: 4 hours
   - Evidence: .env, .env.local, .env.production, config.js, constants.js

## Recommendations (Prioritized)

### 1. Migrate Tests to Functional Testing (HIGH)
**Effort**: 3-4 days
**Impact**: Catch integration bugs mocks miss
**Action**:
1. Install Puppeteer MCP
2. Replace src/api/__tests__/* mock tests with real browser tests
3. Test against real backend (or staging backend)
4. Remove jest.fn() entirely

**Evidence**: 8 test files with mock usage
**Expected Outcome**: Real coverage, fewer production bugs

### 2. Introduce Global State Management (MEDIUM)
**Effort**: 2-3 days
**Impact**: Reduce prop drilling, simplify state logic
**Action**:
1. Evaluate: Zustand (lightweight) vs Redux Toolkit (complex apps)
2. Migrate auth state first (highest prop drilling)
3. Gradually migrate feature state

**Evidence**: No global state detected, 89 useState hooks
**Expected Outcome**: Cleaner components, easier state debugging

### 3. Consolidate Duplicate Utilities (MEDIUM)
**Effort**: 1 day
**Impact**: DRY principle, maintainability
**Action**:
1. Identify duplicates: src/utils/date.js vs src/utils/time.js
2. Merge into single module
3. Update imports across codebase

**Evidence**: Similar date formatting logic in 2 files
**Expected Outcome**: Single source of truth for utilities

## MCP Recommendations
- **puppeteer** (Recommended): Browser automation for functional tests replacing mocks
- **context7** (Recommended): React pattern validation and best practices

## Confidence Score
**76%** (CLARIFY threshold)
- Architecture patterns look solid, but...
- Request user validation:
  1. Is local state (useState) sufficient, or needed global state?
  2. Are API tests currently catching integration bugs?
  3. Priority: tests vs state management?

## Next Steps
1. User: Clarify state management approach and test priority
2. If approved: Install Puppeteer MCP
3. Create wave plan for test migration (Phase 1) and state refactor (Phase 2)
4. Execute with checkpoints

---

Step 8: Persist to Serena
- Entity Created: shannon/analysis/react-app-20250104
- Stored: Key findings, domain percentages, recommendations
- Tagged: architecture-review, frontend-dominant, test-debt
```

**Duration**: ~2 minutes (complete analysis)

**Outcome**: User receives quantitative, evidence-based architecture report with prioritized actions.

---

### Example 2: Technical Debt Assessment

**User Request**: "What's our technical debt?"

**shannon-analysis Execution**:

```
Activating shannon-analysis skill...

Step 1: Analysis Type Detection
- Keywords: "technical debt"
- Detected Type: technical-debt
- Required Sub-Skills: None
- Recommended Sub-Skills: functional-testing (if tests found)

Step 2: Serena Historical Query
- Query: search_nodes("analysis:project")
- Result: Found previous analysis from 2024-12-01
- Previous Debt: 23 TODO items, 5 FIXME, 2 HACK
- Status: Tracking debt evolution

Step 3: Systematic Discovery
- Grep Patterns (Technical Debt Indicators):
  - TODO: 34 occurrences (↑11 since 2024-12-01)
  - FIXME: 8 occurrences (↑3)
  - HACK: 3 occurrences (↑1)
  - console.log: 89 (debug statements)
  - deprecated API: 12 (outdated dependencies)
  - mock: 15 test files (NO MOCKS violation)

- File Categorization:
  - 156 total files
  - 15 test files with mocks
  - 23 files with TODO
  - 8 files with FIXME
  - 3 files with HACK

Step 4: Sub-Skill Invocation
- functional-testing analysis:
  - 15 test files use mocks
  - Violation severity: HIGH (more than 10% of tests)

Step 5: Domain Calculation
- (Same as Example 1, based on file categories)

Step 6: Technical Debt Scoring
- Debt Categories:
  1. Test Debt: 15 mock-based tests (HIGH - blocks production confidence)
  2. Code Debt: 34 TODO items (MEDIUM - incomplete features)
  3. Design Debt: 8 FIXME items (MEDIUM - known issues)
  4. Quick Fixes: 3 HACK items (HIGH - brittle code)
  5. Debug Debt: 89 console.log (LOW - clutter only)
  6. Dependency Debt: 12 deprecated APIs (MEDIUM - future breakage)

- Debt Trend (vs 2024-12-01):
  - TODO: ↑11 (48% increase) - WORSENING
  - FIXME: ↑3 (60% increase) - WORSENING
  - HACK: ↑1 (50% increase) - WORSENING
  - Overall: DEBT ACCUMULATING (action needed)

Step 7: Structured Output

---

# Technical Debt Assessment Report

## Executive Summary
Technical debt has INCREASED 52% since December 2024. Primary concerns: 15 mock-based tests
(NO MOCKS violations), 34 TODO items (growing), and 3 HACK workarounds. Immediate action
required on test debt before it blocks releases.

## Debt by Category (Prioritized)

### 🔴 CRITICAL (Fix Immediately)
**1. Mock-Based Tests** (15 files)
- Impact: ⚠️ Integration bugs not caught, production incidents likely
- Evidence: grep 'jest.fn|sinon|mock' found 15 test files
- Trend: Stable (was 15, still 15)
- Effort: 4-5 days
- Action: Migrate to Puppeteer functional tests
- ROI: Prevent 80% of integration bugs (historical Shannon data)

**2. HACK Workarounds** (3 occurrences)
- Impact: ⚠️ Brittle code, high failure risk
- Evidence:
  - src/api/auth.js:45 - "HACK: bypassing validation"
  - src/utils/date.js:89 - "HACK: timezone workaround"
  - src/components/Form.jsx:120 - "HACK: force re-render"
- Trend: ↑1 since December (WORSENING)
- Effort: 2-3 days (depends on complexity)
- Action: Root cause analysis, proper fixes

### 🟡 HIGH (Fix Soon)
**3. TODO Items** (34 occurrences)
- Impact: ⚠️ Incomplete features, user confusion
- Evidence: grep TODO found 34 comments
- Distribution:
  - src/auth: 12 TODOs (authentication incomplete)
  - src/api: 8 TODOs (error handling gaps)
  - src/components: 14 TODOs (UI polish needed)
- Trend: ↑11 since December (+48%) - WORSENING
- Effort: Variable (1-5 days depending on item)
- Action: Prioritize auth TODOs (security-critical)

**4. Deprecated API Usage** (12 occurrences)
- Impact: ⚠️ Future breakage when dependencies updated
- Evidence:
  - React 17 lifecycle methods: 5 components
  - Deprecated npm packages: 4 (lodash, moment.js)
  - Old API endpoints: 3 backend calls
- Trend: New detection (not tracked before)
- Effort: 3-4 days migration
- Action: Update to React 18 patterns, modern libraries

### 🟢 MEDIUM (Fix When Convenient)
**5. FIXME Items** (8 occurrences)
- Impact: Known issues, workarounds in place
- Evidence: grep FIXME found 8 comments
- Examples:
  - "FIXME: performance issue with large lists"
  - "FIXME: error handling not robust"
- Trend: ↑3 since December (WORSENING)
- Effort: 2-3 days
- Action: Address during next refactor sprint

### 🔵 LOW (Nice to Have)
**6. Debug Statements** (89 occurrences)
- Impact: ℹ️ Code clutter, minor performance impact
- Evidence: grep console.log found 89 statements
- Trend: Not tracked previously
- Effort: 1 day (automated cleanup with linter)
- Action: Add ESLint rule to prevent future additions

## Debt Trend Analysis

**Overall Trend**: 📈 WORSENING (52% increase in 5 weeks)

December 2024:
- TODO: 23
- FIXME: 5
- HACK: 2
- Mock tests: 15
- Total: 45 debt items

January 2025 (Today):
- TODO: 34 (+48%)
- FIXME: 8 (+60%)
- HACK: 3 (+50%)
- Mock tests: 15 (stable)
- Total: 60 debt items (+33%)

**Velocity**: +3 debt items per week
**Projection**: 90 items by March 2025 if no action

## Prioritized Action Plan

### Phase 1: Critical Debt (Week 1-2)
**Goal**: Remove production risk

1. **Replace Mock Tests** (5 days)
   - Install Puppeteer MCP
   - Convert 15 test files to functional tests
   - Remove all jest.fn() usage
   - Expected: 80% fewer integration bugs

2. **Fix HACK Workarounds** (3 days)
   - Root cause analysis for each HACK
   - Implement proper solutions
   - Remove brittle code
   - Expected: Eliminate 3 high-risk points

**Phase 1 Outcome**: Production stability restored

### Phase 2: High-Priority Debt (Week 3-4)
**Goal**: Complete incomplete features

3. **Resolve Auth TODOs** (3 days)
   - Complete 12 authentication TODOs
   - Security-critical features
   - Expected: Auth module complete

4. **Migrate Deprecated APIs** (4 days)
   - Update to React 18
   - Replace deprecated packages
   - Expected: Future-proof codebase

**Phase 2 Outcome**: Feature completeness + modern stack

### Phase 3: Medium/Low Debt (Week 5+)
**Goal**: Code quality improvements

5. **Address FIXME Items** (3 days)
6. **Clean Debug Statements** (1 day)

**Phase 3 Outcome**: Clean, maintainable codebase

## Effort Summary
- Critical: 8 days
- High: 7 days
- Medium/Low: 4 days
- **Total**: 19 days (4 work weeks)

## MCP Recommendations
- **puppeteer** (Required): Migrate mock tests to functional tests

## Confidence Score
**92%** (PROCEED threshold)
- Debt patterns are clear from grep evidence
- Historical Serena data shows trends
- Action plan is evidence-based
- High confidence in recommendations

## Next Steps
1. User: Approve Phase 1 plan (critical debt)
2. Install Puppeteer MCP
3. Create wave plan for 3 phases
4. Execute with checkpoints after each phase

---

Step 8: Persist to Serena
- Entity Updated: shannon/analysis/project (existing)
- Stored: New debt counts, trend data, action plan
- Relations: Linked to previous analysis (2024-12-01)
- Tagged: technical-debt, trend-worsening, action-required
```

**Duration**: ~90 seconds

**Outcome**: User receives quantitative debt assessment with clear priorities and actionable plan.

---

## Outputs

Structured analysis object:

```json
{
  "analysis_type": "codebase-quality" | "architecture-review" | "technical-debt" | "complexity-assessment" | "domain-breakdown",
  "project_summary": {
    "total_files": 247,
    "domains": {
      "Frontend": {"percentage": 48.6, "file_count": 120},
      "Backend": {"percentage": 32.4, "file_count": 80},
      "Database": {"percentage": 6.9, "file_count": 17},
      "Testing": {"percentage": 12.1, "file_count": 30}
    },
    "dominant_domain": "Frontend"
  },
  "quantitative_metrics": {
    "complexity_score": 0.68,
    "technical_debt_count": 60,
    "test_quality_score": 0.45,
    "maintainability_score": 0.72
  },
  "findings": {
    "critical": [
      {"issue": "Mock-based tests", "count": 15, "impact": "HIGH"}
    ],
    "high": [
      {"issue": "TODO items", "count": 34, "trend": "+48%"}
    ],
    "medium": [],
    "low": []
  },
  "recommendations": {
    "prioritized": [
      {
        "priority": "HIGH",
        "action": "Replace 15 mock tests with functional tests",
        "effort": "3-5 days",
        "impact": "80% fewer integration bugs",
        "evidence": "grep jest.fn() found 15 files"
      }
    ]
  },
  "mcp_recommendations": {
    "required": [],
    "recommended": ["puppeteer"],
    "conditional": ["context7"]
  },
  "confidence_score": 0.92,
  "historical_context": {
    "previous_analysis": "shannon/analysis/project-2024-12-01",
    "trend": "WORSENING",
    "delta": "+33% technical debt"
  }
}
```

---

## Success Criteria

This skill succeeds if:

1. ✅ All analysis requests trigger systematic Glob/Grep discovery (no sampling)
2. ✅ Every analysis queries Serena for historical context first
3. ✅ Domain percentages calculated from file counts (not guessed)
4. ✅ Appropriate sub-skills invoked (spec-analysis, project-indexing, confidence-check)
5. ✅ Results are quantitative with evidence (not subjective "looks good")
6. ✅ Recommendations prioritized by impact + effort
7. ✅ MCP recommendations provided based on findings
8. ✅ All results persisted to Serena for future sessions

**Failure Modes**:
- Agent says "I'll check a few files" → VIOLATION (should use Glob for all files)
- Agent says "Looks complex" → VIOLATION (should invoke spec-analysis for 8D score)
- Agent starts without Serena query → VIOLATION (must check history first)
- Agent provides generic advice → VIOLATION (must include evidence + priorities)

**Validation Code**:
```python
def validate_shannon_analysis(result):
    """Verify analysis followed Shannon protocols"""

    # Check: Systematic discovery (not sampling)
    assert result.get("discovery_method") in ["glob", "grep"], \
        "VIOLATION: Used sampling instead of systematic discovery"
    assert result.get("files_analyzed") == result.get("total_files"), \
        "VIOLATION: Incomplete analysis (sampling detected)"

    # Check: Serena historical query performed
    assert result.get("historical_context_checked") == True, \
        "VIOLATION: Skipped Serena historical query"

    # Check: Quantitative domain percentages
    domains = result.get("project_summary", {}).get("domains", {})
    assert all(isinstance(d.get("percentage"), (int, float)) for d in domains.values()), \
        "VIOLATION: Domain percentages not calculated (subjective assessment used)"

    # Check: Evidence-based recommendations
    recommendations = result.get("recommendations", {}).get("prioritized", [])
    for rec in recommendations:
        assert "evidence" in rec, \
            f"VIOLATION: Recommendation lacks evidence: {rec.get('action')}"
        assert "effort" in rec, \
            f"VIOLATION: Recommendation lacks effort estimate: {rec.get('action')}"

    # Check: Confidence score present (from confidence-check)
    confidence = result.get("confidence_score")
    assert confidence is not None and 0.0 <= confidence <= 1.0, \
        "VIOLATION: Missing or invalid confidence score"

    # Check: Results persisted to Serena
    assert result.get("serena_entity_id") is not None, \
        "VIOLATION: Results not persisted to Serena"

    return True
```

---

## Validation

This skill is working correctly if validation function passes. The skill enforces:
- Systematic discovery (no sampling)
- Historical context integration
- Quantitative metrics (not subjective)
- Evidence-based recommendations
- Serena persistence

---

## References

- **RED Baseline Testing**: `shannon-plugin/skills/shannon-analysis/RED_BASELINE_TEST.md` (28 violations documented)
- **8D Framework**: `shannon-plugin/core/SPEC_ANALYSIS.md`
- **NO MOCKS Philosophy**: `shannon-plugin/core/TESTING_PHILOSOPHY.md`
- **Project Indexing**: `shannon-plugin/skills/project-indexing/SKILL.md`
- **Confidence Check**: `shannon-plugin/skills/confidence-check/SKILL.md` (validation before proceeding)

---

**Skill Status**: General-purpose analysis orchestrator
**Enforcement Level**: High - prevents 28 baseline violations
**Flexibility**: Adapts to analysis type, invokes appropriate sub-skills
