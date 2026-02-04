---
name: confidence-check
description: |
  5-check quantitative validation ensuring 90% confidence before implementation. Prevents
  wrong-direction work through systematic verification: duplicate check (25%), architecture
  compliance (25%), official docs (20%), working OSS (15%), root cause (15%). Thresholds:
  ≥90% proceed, ≥70% clarify, <70% STOP. Proven 25-250x token ROI from SuperClaude.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"

mcp-requirements:
  recommended:
    - name: serena
      purpose: Save confidence assessments for cross-wave validation
      fallback: local-storage
      trigger: complexity >= 0.50
    - name: tavily
      purpose: Search for official docs and working OSS references
      fallback: manual-search
      trigger: docs_verified = false OR oss_referenced = false
    - name: github
      purpose: Search GitHub for working OSS implementations
      fallback: manual-search
      trigger: oss_referenced = false

required-sub-skills:
  - spec-analysis

optional-sub-skills:
  - mcp-discovery

allowed-tools: [Read, Grep, Glob, Bash, Serena, Tavily, GitHub]
---

# Confidence Check

## Overview

**Purpose**: Shannon's quantitative 5-check validation algorithm prevents wrong-direction work by ensuring ≥90% confidence before implementation. Each check contributes weighted points (total 100%) across duplicate verification, architecture compliance, official documentation, working OSS references, and root cause identification.

**Critical Role**: This skill prevents the most expensive failure mode in software development - building the right thing wrong, or building the wrong thing right. Proven 25-250x token ROI in SuperClaude production use.

---

## Inputs

**Required:**
- `specification` (string): Implementation request or feature description from user
- `context` (object): Optional context from spec-analysis skill (8D complexity scores, phase plan)

**Optional:**
- `skip_checks` (array): List of checks to skip (e.g., ["oss", "root_cause"] for simple tasks)
- `confidence_threshold` (float): Override default 0.90 threshold (e.g., 0.85 for fast iterations)

---

## Anti-Rationalization (Critical - Read First)

**WARNING**: Agents systematically rationalize skipping confidence checks. Below are the 6 most dangerous rationalizations detected in production, with mandatory counters.

### Rationalization 1: "User seems confident, proceed"
**Example**: User says "I'm 75% sure this is right" → Agent responds "Let's proceed..."

**COUNTER**:
- ❌ **NEVER** accept user's confidence level without running 5-check algorithm
- ✅ User intuition is ONE data point (cognitive), not the total score
- ✅ Run all 5 checks objectively: duplicate (25%), architecture (25%), docs (20%), OSS (15%), root cause (15%)
- ✅ If calculated score <90%, STOP regardless of user's stated confidence
- ✅ Example: User "75% confident" + passed all 5 checks = 100% confidence → PROCEED
- ✅ Example: User "95% confident" + failed duplicate check (0/25) = 75% → STOP

**Rule**: Algorithm score overrides stated confidence. Always calculate objectively.

### Rationalization 2: "Simple task, skip validation"
**Example**: "Just add a button" → Agent proceeds without checking existing buttons

**COUNTER**:
- ❌ **NEVER** skip checks because task "seems simple"
- ✅ "Simple" tasks often duplicate existing code (25% penalty)
- ✅ "Simple" tasks often violate architecture patterns (25% penalty)
- ✅ Even trivial changes get validated (takes 30 seconds, prevents hours of rework)
- ✅ Example: "Add login button" → Check: Is LoginButton.tsx already defined? YES → 0/25 duplicate check → 75% confidence → CLARIFY

**Rule**: No task too simple to validate. 30-second check prevents 2-hour rework.

### Rationalization 3: "I know the API, skip docs"
**Example**: Agent uses Redis API from memory without checking current documentation

**COUNTER**:
- ❌ **NEVER** skip official docs based on "knowing" the API
- ✅ APIs change (Redis 3.x → 4.x syntax breaking changes)
- ✅ Memory is fallible (confusing similar APIs)
- ✅ Documentation takes 2 minutes to verify (debugging wrong API takes hours)
- ✅ Use Tavily MCP or direct doc access: redis.io, React docs, Express docs
- ✅ **Zero points (0/20)** if docs not consulted

**Rule**: Always verify official docs. Knowledge cutoff and API changes require fresh verification.

### Rationalization 4: "I can design this, skip OSS research"
**Example**: "I'll design a real-time sync protocol" without checking Yjs, Automerge, ShareDB

**COUNTER**:
- ❌ **NEVER** design from scratch when proven OSS exists
- ✅ Working OSS = battle-tested, production-proven, community-validated
- ✅ Custom designs often miss edge cases (race conditions, conflicts, network partitions)
- ✅ 15-30 minutes researching OSS saves weeks of debugging custom code
- ✅ Use GitHub MCP: search "real-time collaborative editing", filter by stars, check recent commits
- ✅ **Zero points (0/15)** if no OSS referenced

**Rule**: Learn from production code. OSS research is mandatory for complex features.

### Rationalization 5: "Obvious problem, skip root cause"
**Example**: "API slow → Add caching" without profiling actual bottleneck

**COUNTER**:
- ❌ **NEVER** implement solution before diagnosing root cause
- ✅ "Obvious" problems often have non-obvious causes
- ✅ Example: "API slow" → Root cause: N+1 database queries, not lack of caching
- ✅ Example: "Memory leak" → Root cause: Event listener not cleaned up, not memory allocation
- ✅ Diagnose FIRST (logs, profiler, metrics), implement SECOND
- ✅ **Zero points (0/15)** if no diagnostic evidence provided

**Rule**: Diagnosis before prescription. No solutions without identified root cause.

### Rationalization 6: "85% is close enough to 90%"
**Example**: Score 85% → Agent thinks "Close enough, let's proceed"

**COUNTER**:
- ❌ **NEVER** round up or "close enough" confidence scores
- ✅ Thresholds are precise: ≥90% proceed, ≥70% clarify, <70% STOP
- ✅ 85% = CLARIFY band → Request missing information to reach 90%
- ✅ Example: 85% = missing OSS reference (0/15) → "Please provide working OSS example before proceeding"
- ✅ 5% gap often reveals critical missing validation
- ✅ **Iron Law**: Thresholds are exact, not approximate

**Rule**: 90% means 90.0%. Not 89.9%, not 85%, not "close enough". Exact threshold enforcement.

### Rationalization 7: "Authority override"
**Example**: Senior engineer says "Trust me, I've done this 100 times, skip the checks"

**COUNTER**:
- ❌ **NEVER** accept authority as substitute for validation
- ✅ Algorithm is objective, applies to all experience levels
- ✅ "Trust" is not a substitute for verification
- ✅ Even senior engineers miss duplicates, architecture violations, outdated API knowledge
- ✅ Stated confidence (95%) doesn't override calculated confidence (might be 60%)
- ✅ Run 5-check algorithm regardless of who requests bypass

**Rule**: No authority exceptions. Algorithm applies universally, from junior to principal.

### Rationalization 8: "Urgent/emergency bypass"
**Example**: "Production down! No time for confidence checks, implement OAuth2 now!"

**COUNTER**:
- ❌ **NEVER** skip root cause check in emergencies
- ✅ Wrong fix in emergency wastes MORE time than 2-minute diagnosis
- ✅ Emergency waivers allowed: docs (20), OSS (15) can skip with assumed PASS
- ✅ Emergency MANDATORY: duplicate (25), architecture (25), root cause (15)
- ✅ Example: "Login broken" → Check: Is auth down or database connection down?
- ✅ 2 minutes root cause diagnosis saves 2 hours implementing wrong fix

**Rule**: Emergencies require faster checks, not skipped checks. Root cause MANDATORY.

### Rationalization 9: "Within margin of error"
**Example**: "88% is close to 90%, within margin of error, let's proceed"

**COUNTER**:
- ❌ **NEVER** round confidence scores
- ✅ Thresholds are exact: `if (score >= 0.90)` not `if (score > 0.88)`
- ✅ "Close enough" often reveals critical missing validation
- ✅ 2% gap = incomplete docs (2 points) OR missing OSS (15 points) - not trivial
- ✅ Example: 88% means incomplete OSS research - prevents reinventing wheel
- ✅ Request missing points explicitly, don't proceed "close enough"

**Rule**: Thresholds are exact. 89.9% = CLARIFY, not PROCEED. No rounding.

### Rationalization 10: "Found some OSS, counts as research"
**Example**: Found 50-star unmaintained repo, claims 15/15 OSS check passed

**COUNTER**:
- ❌ **NEVER** accept low-quality OSS as validation
- ✅ Quality criteria: >1000 stars OR active maintenance (<3 months) OR production-used
- ✅ Partial credit allowed: 8/15 for lower quality (<1000 stars but active)
- ✅ Zero credit: <100 stars AND unmaintained (>1 year no commits)
- ✅ Example: 50-star 2-year-old repo = 0/15 (find production-quality instead)
- ✅ Purpose: Learn from PROVEN implementations, not hobby projects

**Rule**: OSS quality matters. Production-grade (15/15), active lower-quality (8/15), or fail (0/15).

### Rationalization 11: "New feature bypasses root cause check"
**Example**: "'Add caching' is a new feature, so root cause check = N/A → 15/15"

**COUNTER**:
- ❌ **NEVER** claim "new feature" to skip root cause on fixes/improvements
- ✅ Keywords requiring root cause: "slow", "fix", "improve", "broken", "error", "leak", "crash", "optimize"
- ✅ "Add caching" to fix slow page = FIX → Need diagnostic evidence (profiler, metrics)
- ✅ "Build authentication system" from scratch = NEW FEATURE → Root cause N/A
- ✅ Example: "Page slow, add caching" = FIX → MANDATORY root cause check
- ✅ Example: "Build user authentication" = NEW → Root cause check N/A

**Rule**: Root cause MANDATORY for any fix/improvement. Keyword detection enforced.

### Rationalization 12: "User provided docs, skip verification"
**Example**: User provides syntax snippet, agent accepts without verifying against official docs

**COUNTER**:
- ❌ **NEVER** accept user-provided syntax without official doc verification
- ✅ User syntax may be outdated (Redis 3.x vs 4.x breaking changes)
- ✅ User syntax may be from different library (mixing APIs)
- ✅ User syntax may be pseudo-code, not actual API
- ✅ ALWAYS verify against official docs regardless of user input quality
- ✅ Example: User says "redis.connect()" → Verify: Official Redis 4.x is "createClient() + await connect()"

**Rule**: Official docs verification MANDATORY. User input verified, not trusted blindly.

### Detection Signal
**If you're tempted to**:
- Accept <90% confidence as "good enough"
- Skip checks for "simple" tasks
- Use memory instead of docs
- Design custom instead of researching OSS
- Implement solution before diagnosing problem
- Round 85% up to 90%

**Then you are rationalizing.** Stop. Run the 5-check algorithm. Report the score objectively.

---

## When to Use

Use confidence-check skill when:
- About to begin implementation of ANY feature, fix, or change
- User provides specification, requirements, or work description
- Complexity score ≥0.30 (Moderate or higher) from spec-analysis
- Starting new wave in wave-based execution
- User says "I think...", "Maybe...", "Probably..." (uncertainty signals)
- Before writing code that modifies existing system architecture

DO NOT use when:
- Pure research or investigation tasks (no implementation)
- Documentation-only changes (README, comments)
- Test writing based on existing implementation (tests validate, not implement)
- Responding to clarification questions (dialogue, not implementation)

---

## Core Competencies

### 1. Quantitative 5-Check Algorithm
Objective scoring across five validation dimensions, each contributing weighted points to total confidence score (0.00-1.00):

1. **No Duplicate Implementations (25%)**: Verify no existing code duplicates proposed implementation
2. **Architecture Compliance (25%)**: Confirm approach aligns with system architecture patterns
3. **Official Docs Verified (20%)**: Validate using current official documentation
4. **Working OSS Referenced (15%)**: Learn from production-proven open source implementations
5. **Root Cause Identified (15%)**: For fixes, verify diagnostic evidence of actual problem

### 2. Threshold-Based Decision System
- **≥90% confidence**: PROCEED to implementation
- **70-89% confidence**: CLARIFY - request missing information before proceeding
- **<70% confidence**: STOP - too many unknowns, requires deeper analysis

### 3. Integration with Shannon 8D Scoring
Confidence check score informs spec-analysis dimensions:
- Low confidence (<70%) increases Uncertainty dimension (10% weight)
- Missing architecture compliance increases Cognitive dimension (15% weight)
- No OSS reference increases Technical dimension (15% weight)

---

## Workflow

### Step 1: Initialize Confidence Assessment

**Input**: Implementation request from user

**Processing**:
1. Parse request to identify: feature name, scope, affected components
2. Initialize score: `confidence_score = 0.00`
3. Initialize checklist:
   ```javascript
   {
     duplicate_check: { passed: null, points: 0, max: 25 },
     architecture_check: { passed: null, points: 0, max: 25 },
     docs_check: { passed: null, points: 0, max: 20 },
     oss_check: { passed: null, points: 0, max: 15 },
     root_cause_check: { passed: null, points: 0, max: 15 }
   }
   ```

**Output**: Initialized assessment structure

**Duration**: Instant

---

### Step 2: Check #1 - No Duplicate Implementations (25%)

**Purpose**: Prevent reimplementing existing functionality

**Processing**:
1. **Search codebase** for similar implementations:
   - Use Grep to search for function names, component names, class names
   - Example: User wants "LoginButton" → Search: `grep -r "LoginButton" src/`
   - Example: User wants "authenticateUser" → Search: `grep -r "authenticateUser|authenticate.*user" src/`

2. **Check package.json** for existing libraries:
   - Example: User wants "JWT auth" → Check: `grep -i "jsonwebtoken|jwt" package.json`
   - If library installed, verify it's not already used

3. **Review existing architecture**:
   - Use Read to check key files (routes, controllers, services)
   - Example: Authentication → Check: `src/middleware/auth.js`, `src/routes/auth.js`

4. **Scoring**:
   - ✅ **PASS (25/25)**: No duplicate found, or duplicate intentional (different purpose documented)
   - ⚠️  **PARTIAL (15/25)**: Similar code exists but in deprecated/unused module
   - ❌ **FAIL (0/25)**: Active duplicate found, will create redundant implementation

**Output**:
- `duplicate_check.passed`: true | false
- `duplicate_check.points`: 0 | 15 | 25
- `duplicate_check.evidence`: File paths, code snippets showing existing implementation (if found)

**Duration**: 1-3 minutes

**Example**:
```
User: "Build authentication middleware"
Search: grep -r "auth.*middleware" src/
Found: src/middleware/authenticate.js (active, exports authenticateUser)
Result: FAIL (0/25) - Duplicate implementation exists
Evidence: "src/middleware/authenticate.js already implements JWT authentication"
```

---

### Step 3: Check #2 - Architecture Compliance (25%)

**Purpose**: Ensure proposed approach aligns with system architecture patterns

**Processing**:
1. **Identify architecture patterns**:
   - Frontend: Component structure (atomic, pages, layouts), state management (Redux, Context, Zustand)
   - Backend: MVC vs microservices, layered architecture (routes → controllers → services → models)
   - Database: ORM patterns (Prisma, TypeORM), repository pattern, query builders

2. **Locate architecture documentation**:
   - Check for: `ARCHITECTURE.md`, `CONTRIBUTING.md`, `docs/architecture/`
   - If missing, infer from codebase structure:
     - Read: `src/` directory structure
     - Read: Key files (index, app, main) to understand initialization patterns

3. **Verify proposed approach matches patterns**:
   - Example: Frontend component → Check: Does project use `/components/atoms/` structure?
   - Example: API endpoint → Check: Does project use `/routes/ → /controllers/ → /services/` layers?
   - Example: Database query → Check: Does project use raw SQL or ORM?

4. **Scoring**:
   - ✅ **PASS (25/25)**: Approach matches established patterns, or creates documented new pattern
   - ⚠️  **PARTIAL (15/25)**: Approach deviates slightly but acceptable (e.g., new pattern for new domain)
   - ❌ **FAIL (0/25)**: Approach violates architecture (e.g., business logic in routes, direct DB access in components)

**Output**:
- `architecture_check.passed`: true | false
- `architecture_check.points`: 0 | 15 | 25
- `architecture_check.rationale`: Explanation of alignment or violation

**Duration**: 2-4 minutes

**Example**:
```
User: "Add getUserById() in routes/users.js"
Architecture: Project uses MVC (routes → controllers → services → models)
Proposed: Adding business logic (getUserById) directly in routes
Result: FAIL (0/25) - Violates MVC pattern
Rationale: "getUserById should be in services/userService.js, routes should only handle HTTP"
```

---

### Step 4: Check #3 - Official Docs Verified (20%)

**Purpose**: Ensure implementation uses current, official API syntax and patterns

**Processing**:
1. **Identify required documentation**:
   - Extract technologies from user request
   - Example: "Redis caching" → Docs: redis.io
   - Example: "React hooks" → Docs: react.dev/reference/react
   - Example: "Express middleware" → Docs: expressjs.com/en/guide/writing-middleware.html

2. **Access official documentation**:
   - **If Tavily MCP available**: Use for quick doc lookup
     ```javascript
     tavily_search("Redis client.connect() API current syntax")
     ```
   - **If Context7 MCP available**: Use for framework-specific docs
     ```javascript
     get_library_docs("/redis/redis", topic: "client connection")
     ```
   - **Manual fallback**: Report doc URLs for user verification

3. **Verify current API syntax**:
   - Check version-specific changes (e.g., Redis 3.x vs 4.x breaking changes)
   - Confirm proposed usage matches official examples
   - Identify deprecated patterns (e.g., `componentWillMount` in React)

4. **Scoring**:
   - ✅ **PASS (20/20)**: Current official docs verified, syntax confirmed correct
   - ⚠️  **PARTIAL (10/20)**: Docs consulted but using slightly outdated version (still functional)
   - ❌ **FAIL (0/20)**: No docs consulted, using memory/intuition, or wrong syntax

**Output**:
- `docs_check.passed`: true | false
- `docs_check.points`: 0 | 10 | 20
- `docs_check.source`: URL or doc reference consulted
- `docs_check.verification`: Specific API syntax confirmed

**Duration**: 2-5 minutes (depending on MCP availability)

**Example**:
```
User: "Use Redis client.connect()"
Action: Search redis.io documentation
Found: Redis 4.x requires: await client.connect() (async)
      Redis 3.x used: client.connect(callback)
Verification: Project uses Redis 4.x (package.json: "redis": "^4.6.0")
Result: PASS (20/20) - Correct async syntax for Redis 4.x
Source: https://redis.io/docs/latest/develop/connect/clients/nodejs/
```

---

### Step 5: Check #4 - Working OSS Referenced (15%)

**Purpose**: Learn from production-proven implementations, avoid reinventing solved problems

**Processing**:
1. **Identify OSS research need**:
   - Complex features: Real-time sync, authentication, payment processing
   - Novel patterns: CRDT algorithms, optimistic UI updates, distributed systems
   - Domain-specific: E-commerce checkout, video streaming, collaborative editing

2. **Search for working implementations**:
   - **If GitHub MCP available**:
     ```javascript
     github_search_repos("real-time collaborative editing", language: "javascript")
     // Filter: stars > 1000, recently updated
     ```
   - **If Tavily MCP available**:
     ```javascript
     tavily_search("production WebSocket real-time sync implementation")
     ```
   - **Manual fallback**: Report search terms for user to research

3. **Evaluate OSS quality**:
   - Check: GitHub stars (>1000 preferred), recent commits (active maintenance)
   - Check: Production use (companies using it, "used by" section)
   - Check: Code quality (tests, documentation, TypeScript support)

4. **Extract learnings**:
   - Study: Architecture decisions, error handling patterns, edge case handling
   - Identify: Design patterns applicable to current implementation
   - Document: Key takeaways from OSS approach

5. **Scoring**:
   - ✅ **PASS (15/15)**: Production-quality OSS found (>1000 stars, active), learnings documented
   - ⚠️  **PARTIAL (8/15)**: OSS found but lower quality (<1000 stars, or inactive)
   - ❌ **FAIL (0/15)**: No OSS researched, designing from scratch
   - ⚠️  **N/A (skip)**: Trivial implementation where OSS research not applicable (e.g., simple utility function)

**Output**:
- `oss_check.passed`: true | false | null (N/A)
- `oss_check.points`: 0 | 8 | 15
- `oss_check.examples`: List of OSS repositories with URLs and star counts
- `oss_check.learnings`: Key design patterns extracted from OSS

**Duration**: 5-10 minutes (research intensive)

**Example**:
```
User: "Build real-time collaborative editing"
Action: Search GitHub for "collaborative editing CRDT"
Found:
  1. Yjs (github.com/yjs/yjs) - 13.2k stars, active, used by Google, Microsoft
  2. Automerge (github.com/automerge/automerge) - 3.5k stars, active, research-backed
  3. ShareDB (github.com/share/sharedb) - 6.1k stars, active, Operational Transforms
Learnings:
  - Yjs uses CRDT (Conflict-free Replicated Data Types) for automatic conflict resolution
  - WebSocket for real-time sync, with offline support and eventual consistency
  - State vector compression reduces bandwidth (only send deltas)
Result: PASS (15/15) - Production OSS researched, design patterns identified
Examples: ["yjs/yjs (13.2k stars)", "automerge/automerge (3.5k stars)"]
```

---

### Step 6: Check #5 - Root Cause Identified (15%)

**Purpose**: For fixes/improvements, verify diagnostic evidence of actual problem before implementing solution

**Processing**:
1. **Determine if root cause check applies**:
   - **Applies to**: Bug fixes, performance improvements, error handling, optimization
   - **Does NOT apply to**: New features, greenfield implementations, documentation

2. **If applicable, gather diagnostic evidence**:
   - **For bugs**: Error logs, stack traces, reproduction steps
   - **For performance**: Profiler output, metrics, query times, network traces
   - **For errors**: Log entries showing failure conditions, frequency, patterns

3. **Verify evidence identifies root cause** (not symptoms):
   - ❌ Symptom: "API is slow"
   - ✅ Root cause: "Database query takes 2.4s due to missing index on users.email"

   - ❌ Symptom: "Memory leak"
   - ✅ Root cause: "EventEmitter listeners not removed in componentWillUnmount, accumulating 1000+ listeners"

   - ❌ Symptom: "App crashes"
   - ✅ Root cause: "Uncaught promise rejection in async fetchData() when API returns 404"

4. **Validate proposed solution addresses root cause**:
   - Example: Root cause = missing index → Solution = add index ✅
   - Example: Root cause = N+1 queries → Solution = add caching ❌ (should fix query)

5. **Scoring**:
   - ✅ **PASS (15/15)**: Diagnostic evidence provided, root cause identified, solution matches cause
   - ⚠️  **PARTIAL (8/15)**: Evidence provided but root cause unclear (symptom identified, cause assumed)
   - ❌ **FAIL (0/15)**: No diagnostic evidence, solution-first approach
   - ⚠️  **N/A (skip)**: New feature (not a fix), root cause check doesn't apply

**Output**:
- `root_cause_check.passed`: true | false | null (N/A)
- `root_cause_check.points`: 0 | 8 | 15
- `root_cause_check.evidence`: Diagnostic data (logs, profiler, metrics)
- `root_cause_check.cause`: Identified root cause
- `root_cause_check.solution_alignment`: Does solution address cause?

**Duration**: 3-8 minutes (depending on diagnostic complexity)

**Example**:
```
User: "API is slow, add caching"
Action: Request diagnostic evidence
User provides: "Logs show /api/users taking 3.2s average"
Investigation:
  - Check: Database query logs
  - Found: SELECT * FROM users WHERE email = ? (no index on email column)
  - Profiler: 95% of time spent in database query
Root Cause: Missing database index on users.email column (N+1 query problem)
Proposed Solution: "Add caching"
Alignment: MISMATCH - Caching treats symptom, doesn't fix root cause
Better Solution: "Add index on users.email column"
Result: FAIL (0/15) - Solution doesn't address root cause
Evidence: "Database profiler shows 3.1s query time on unindexed email column"
Cause: "Missing index on users.email"
Solution Alignment: "Proposed caching, should add database index instead"
```

---

### Step 7: Calculate Total Confidence Score

**Input**: All 5 check results

**Processing**:
1. **Sum points from all checks**:
   ```javascript
   total_points = duplicate_check.points +
                  architecture_check.points +
                  docs_check.points +
                  oss_check.points +
                  root_cause_check.points
   ```

2. **Calculate confidence score** (0.00-1.00):
   ```javascript
   confidence_score = total_points / 100.0
   ```

3. **Determine threshold band**:
   ```javascript
   if (confidence_score >= 0.90) {
     decision = "PROCEED"
     action = "Begin implementation"
   } else if (confidence_score >= 0.70) {
     decision = "CLARIFY"
     action = "Request missing information before proceeding"
   } else {
     decision = "STOP"
     action = "Too many unknowns, requires deeper analysis or spec revision"
   }
   ```

4. **Identify missing checks** (if <90%):
   ```javascript
   missing_checks = checks.filter(c => c.points < c.max)
   // Example: [{name: "docs", missing: 20}, {name: "oss", missing: 15}]
   ```

**Output**:
- `confidence_score`: 0.00-1.00 (e.g., 0.85)
- `decision`: "PROCEED" | "CLARIFY" | "STOP"
- `action`: Recommended next step
- `missing_checks`: List of incomplete checks with missing points

**Duration**: Instant (calculation)

**Example**:
```
Results:
  duplicate_check: 25/25 ✅
  architecture_check: 25/25 ✅
  docs_check: 20/20 ✅
  oss_check: 0/15 ❌ (no OSS researched)
  root_cause_check: 15/15 ✅ (N/A, new feature)

Total: 85/100
Confidence: 0.85 (85%)
Decision: CLARIFY
Action: "Request OSS examples before proceeding"
Missing: ["OSS reference (0/15)"]
```

---

### Step 8: Report Confidence Assessment

**Input**: Complete assessment with decision

**Processing**:
1. **Format assessment report**:
   ```markdown
   # Confidence Check: [Feature Name]

   **Total Confidence**: X.XX (XX%)
   **Decision**: PROCEED | CLARIFY | STOP

   ## 5-Check Results

   | Check | Points | Status | Evidence |
   |-------|--------|--------|----------|
   | Duplicate | XX/25 | ✅/❌ | [Details] |
   | Architecture | XX/25 | ✅/❌ | [Details] |
   | Docs | XX/20 | ✅/❌ | [Details] |
   | OSS | XX/15 | ✅/❌ | [Details] |
   | Root Cause | XX/15 | ✅/❌ | [Details] |

   ## Decision: [PROCEED/CLARIFY/STOP]

   [Action description]

   ## Next Steps
   [Specific actions based on decision]
   ```

2. **Save to Serena MCP** (if available and complexity >=0.50):
   ```javascript
   serena_write_memory(`confidence_check_${feature_name}_${timestamp}`, {
     feature: feature_name,
     confidence_score: 0.85,
     decision: "CLARIFY",
     checks: [...],
     missing_checks: [...]
   })
   ```

3. **Integrate with spec-analysis**:
   - If confidence <70%, increase Uncertainty dimension in 8D scoring
   - Report confidence score to wave-orchestration for risk assessment

**Output**: Formatted markdown report with decision and next steps

**Duration**: 1 minute

---

### Step 9: Execute Decision

**Input**: Decision (PROCEED | CLARIFY | STOP)

**Processing**:

**If PROCEED (≥90%)**:
1. Document confidence assessment in implementation PR/commit
2. Proceed to implementation
3. No additional gating required

**If CLARIFY (70-89%)**:
1. Identify specific missing information:
   - Example: "Need OSS reference for real-time sync (missing 15 points)"
   - Example: "Need official Redis docs verification (missing 20 points)"
2. Request clarification from user:
   - "Before proceeding, please provide: [specific requests]"
   - "This will increase confidence from 85% to 100%"
3. Wait for clarification before implementation
4. Re-run confidence check with new information

**If STOP (<70%)**:
1. Report critical gaps:
   - Example: "Missing architecture alignment (0/25) AND OSS reference (0/15) = 60% confidence"
2. Recommend alternatives:
   - "Suggest running /shannon:spec for deeper analysis"
   - "Consider spike/research task before implementation"
   - "Revise specification to address unknowns"
3. DO NOT proceed to implementation
4. Escalate to user for direction

**Output**: Executed decision with user feedback or implementation start

**Duration**: Depends on decision path

---

## Integration with Shannon 8D Scoring

Confidence score informs spec-analysis dimensions:

```javascript
// In spec-analysis workflow
const confidence_result = run_confidence_check(feature_request)

// Update Uncertainty dimension (10% weight in 8D)
if (confidence_result.score < 0.70) {
  uncertainty_score += 0.30  // Major unknowns
} else if (confidence_result.score < 0.90) {
  uncertainty_score += 0.15  // Minor clarifications needed
}

// Update Cognitive dimension (15% weight) if architecture unclear
if (confidence_result.architecture_check.points < 15) {
  cognitive_score += 0.20  // Need deeper architectural thinking
}

// Update Technical dimension (15% weight) if no OSS reference
if (confidence_result.oss_check.points === 0) {
  technical_score += 0.15  // Increased technical risk without proven patterns
}

// Recalculate total complexity with confidence-adjusted dimensions
total_complexity = calculate_8d_weighted_total()
```

**Result**: Confidence check directly impacts project complexity assessment and resource planning.

---

## Outputs

Structured confidence assessment:

```json
{
  "feature": "authentication_middleware",
  "timestamp": "2025-11-04T10:30:00Z",
  "confidence_score": 0.85,
  "decision": "CLARIFY",
  "checks": [
    {
      "name": "duplicate",
      "points": 25,
      "max": 25,
      "passed": true,
      "evidence": "No existing auth middleware found in src/"
    },
    {
      "name": "architecture",
      "points": 25,
      "max": 25,
      "passed": true,
      "rationale": "Follows MVC pattern: middleware/ directory exists"
    },
    {
      "name": "docs",
      "points": 20,
      "max": 20,
      "passed": true,
      "source": "https://expressjs.com/en/guide/writing-middleware.html",
      "verification": "Confirmed Express 4.x middleware syntax"
    },
    {
      "name": "oss",
      "points": 0,
      "max": 15,
      "passed": false,
      "examples": [],
      "reason": "No OSS authentication middleware researched"
    },
    {
      "name": "root_cause",
      "points": 15,
      "max": 15,
      "passed": null,
      "note": "N/A - new feature, not a fix"
    }
  ],
  "missing_checks": [
    {
      "name": "oss",
      "missing_points": 15,
      "recommendation": "Research Passport.js or express-jwt OSS implementations"
    }
  ],
  "action": "Request OSS examples before proceeding (need 90% confidence)",
  "next_steps": [
    "User: Provide working OSS reference for authentication middleware",
    "User: Consider using Passport.js (13k stars) or express-jwt (6k stars)",
    "Agent: Re-run confidence check after OSS research"
  ]
}
```

---

## Success Criteria

This skill succeeds if:

1. ✅ All 5 checks executed (duplicate, architecture, docs, OSS, root cause)
2. ✅ Confidence score calculated correctly (0.00-1.00, sum of weighted checks)
3. ✅ Decision matches threshold: ≥90% PROCEED, 70-89% CLARIFY, <70% STOP
4. ✅ Missing checks identified when score <90%
5. ✅ Evidence documented for each check (file paths, doc URLs, OSS repos)
6. ✅ Decision executed (implementation started, clarification requested, or stopped)
7. ✅ Assessment saved to Serena MCP (if available and complexity >=0.50)
8. ✅ Confidence score integrated with spec-analysis (Uncertainty dimension updated)

Validation:
```python
def validate_confidence_check(result):
    assert 0.0 <= result['confidence_score'] <= 1.0
    assert result['confidence_score'] == sum(c['points'] for c in result['checks']) / 100.0

    # Verify decision thresholds
    if result['confidence_score'] >= 0.90:
        assert result['decision'] == 'PROCEED'
    elif result['confidence_score'] >= 0.70:
        assert result['decision'] == 'CLARIFY'
    else:
        assert result['decision'] == 'STOP'

    # Verify all checks present
    assert len(result['checks']) == 5
    check_names = [c['name'] for c in result['checks']]
    assert set(check_names) == {'duplicate', 'architecture', 'docs', 'oss', 'root_cause'}

    # Verify missing checks identified if <90%
    if result['confidence_score'] < 0.90:
        assert len(result['missing_checks']) > 0
```

---

## Common Pitfalls

### Pitfall 1: Accepting Stated Confidence Without Calculation

**Wrong:**
```
User: "I'm 80% sure this is right"
Agent: "Let's proceed with 80% confidence"
```

**Right:**
```
User: "I'm 80% sure this is right"
Agent: "Running 5-check validation..."
Result:
  - duplicate: 25/25
  - architecture: 0/25 (violates MVC pattern)
  - docs: 20/20
  - oss: 15/15
  - root_cause: N/A
Total: 60/100 (60% confidence)
Decision: STOP (below 70% threshold)
```

**Why**: User's stated confidence is subjective. Algorithm score is objective and often reveals hidden gaps.

---

### Pitfall 2: Skipping Checks for "Simple" Tasks

**Wrong:**
```
User: "Just add a login button"
Agent: "Simple task, proceeding..."
[Creates LoginButton.tsx, duplicating existing LoginButton.jsx]
```

**Right:**
```
User: "Just add a login button"
Agent: "Running confidence check..."
Check 1 (Duplicate): Searching for existing login buttons...
Found: src/components/LoginButton.jsx (active)
Result: FAIL (0/25) - Duplicate exists
Decision: STOP (25% confidence)
Recommendation: "Use existing LoginButton.jsx instead of creating new component"
```

**Why**: "Simple" tasks often duplicate existing code. 30-second check prevents 2-hour rework.

---

### Pitfall 3: Using Memory Instead of Official Docs

**Wrong:**
```
User: "Use Redis caching"
Agent: "I'll use client.connect(callback)..."
[Uses Redis 3.x syntax in Redis 4.x project → Error]
```

**Right:**
```
User: "Use Redis caching"
Agent: "Checking official Redis documentation..."
Version in package.json: "redis": "^4.6.0"
Redis 4.x docs: client.connect() is async (no callback)
Correct syntax: await client.connect()
Result: docs check PASS (20/20)
```

**Why**: APIs change (Redis 3.x → 4.x breaking changes). Always verify current docs.

---

### Pitfall 4: Designing From Scratch Instead of OSS Research

**Wrong:**
```
User: "Build real-time collaborative editing"
Agent: "I'll design a custom sync protocol..."
[Spends 2 weeks, hits race conditions, conflict resolution issues]
```

**Right:**
```
User: "Build real-time collaborative editing"
Agent: "Researching production OSS implementations..."
Found: Yjs (13.2k stars, used by Google/Microsoft)
Learnings: CRDT for conflict-free sync, state vector compression, offline support
Decision: Use Yjs patterns, adapt to our use case
Result: oss check PASS (15/15)
[Saves 2 weeks by learning from production-proven code]
```

**Why**: OSS has solved hard problems (race conditions, edge cases). Learn from battle-tested code.

---

### Pitfall 5: Solution-First Instead of Diagnosis-First

**Wrong:**
```
User: "API is slow, add caching"
Agent: "Adding Redis caching..."
[Implements caching, API still slow - root cause was missing database index]
```

**Right:**
```
User: "API is slow, add caching"
Agent: "Requesting diagnostic evidence for root cause check..."
User: [provides profiler data]
Analysis: 95% time in database query (missing index on users.email)
Root Cause: Missing database index
Proposed Solution: "Add caching"
Alignment: MISMATCH
Correct Solution: "Add database index on users.email"
Result: root_cause check adjusted (proposes correct solution)
```

**Why**: Diagnosis before prescription. Caching treats symptom; index fixes cause.

---

### Pitfall 6: "Close Enough" to 90%

**Wrong:**
```
Confidence: 85%
Agent: "85% is close to 90%, proceeding..."
```

**Right:**
```
Confidence: 85%
Decision: CLARIFY (70-89% band)
Action: "Missing OSS reference (0/15). Please provide working example to reach 90%."
[Wait for clarification before proceeding]
```

**Why**: Thresholds are exact, not approximate. 85% = CLARIFY, not PROCEED.

---

## Examples

### Example 1: PROCEED Scenario (100% Confidence)

**Input:**
```
User: "Add error logging to API endpoints using Winston library"
```

**Process:**
1. **Duplicate Check (25/25)**:
   - Search: `grep -r "winston" src/`
   - Found: package.json has "winston": "^3.8.0" but no middleware configured
   - Result: ✅ PASS - Winston installed but not configured for endpoints

2. **Architecture Check (25/25)**:
   - Read: src/middleware/ (exists, contains other middleware)
   - Pattern: Express middleware in src/middleware/, registered in src/app.js
   - Proposed: Create src/middleware/logger.js
   - Result: ✅ PASS - Follows established middleware pattern

3. **Docs Check (20/20)**:
   - Source: https://github.com/winstonjs/winston#usage
   - Verified: Current Winston 3.x syntax (createLogger, transports)
   - Result: ✅ PASS - Official docs consulted, syntax verified

4. **OSS Check (15/15)**:
   - Found: Express + Winston examples on GitHub (express-winston, 800 stars)
   - Learnings: Use express-winston for automatic request/response logging
   - Result: ✅ PASS - Production OSS patterns identified

5. **Root Cause Check (15/15)**:
   - Note: N/A (new feature, not a fix)
   - Result: ✅ SKIP (not applicable)

**Output:**
```json
{
  "feature": "winston_error_logging",
  "confidence_score": 1.00,
  "decision": "PROCEED",
  "checks": [
    {"name": "duplicate", "points": 25, "passed": true},
    {"name": "architecture", "points": 25, "passed": true},
    {"name": "docs", "points": 20, "passed": true},
    {"name": "oss", "points": 15, "passed": true},
    {"name": "root_cause", "points": 15, "passed": null}
  ],
  "action": "Proceed to implementation with 100% confidence",
  "next_steps": [
    "Create src/middleware/logger.js using Winston",
    "Register middleware in src/app.js",
    "Test error logging on sample endpoint"
  ]
}
```

**Decision**: PROCEED ✅ (100% confidence)

---

### Example 2: CLARIFY Scenario (85% Confidence)

**Input:**
```
User: "Implement WebSocket real-time notifications"
```

**Process:**
1. **Duplicate Check (25/25)**:
   - Search: `grep -r "websocket\|socket\.io" src/`
   - Found: No existing WebSocket implementation
   - Result: ✅ PASS

2. **Architecture Check (25/25)**:
   - Read: src/server.js (Express HTTP server)
   - Pattern: HTTP server uses Express, can upgrade to WebSocket
   - Proposed: Add Socket.io to existing HTTP server
   - Result: ✅ PASS - Compatible with architecture

3. **Docs Check (20/20)**:
   - Source: https://socket.io/docs/v4/server-initialization/
   - Verified: Socket.io 4.x syntax (server initialization, emit patterns)
   - Result: ✅ PASS

4. **OSS Check (0/15)**:
   - Action: Searched GitHub for "socket.io real-time notifications"
   - Found: Multiple examples but none reviewed for production patterns
   - Result: ❌ FAIL - No OSS researched

5. **Root Cause Check (15/15)**:
   - Note: N/A (new feature)
   - Result: ✅ SKIP

**Output:**
```json
{
  "feature": "websocket_notifications",
  "confidence_score": 0.85,
  "decision": "CLARIFY",
  "checks": [
    {"name": "duplicate", "points": 25, "passed": true},
    {"name": "architecture", "points": 25, "passed": true},
    {"name": "docs", "points": 20, "passed": true},
    {"name": "oss", "points": 0, "passed": false, "reason": "No OSS researched"},
    {"name": "root_cause", "points": 15, "passed": null}
  ],
  "missing_checks": [
    {
      "name": "oss",
      "missing_points": 15,
      "recommendation": "Research Socket.io notification patterns from production apps"
    }
  ],
  "action": "Request OSS examples before proceeding",
  "next_steps": [
    "User: Provide working Socket.io notification example from GitHub",
    "Suggested repos: socket.io-chat, slack-clone, discord-clone",
    "Agent: Review OSS patterns (room management, broadcast strategies, reconnection logic)",
    "Agent: Re-run confidence check after OSS research"
  ]
}
```

**Decision**: CLARIFY ⚠️ (85% confidence - need OSS research to reach 90%)

---

### Example 3: STOP Scenario (50% Confidence)

**Input:**
```
User: "Fix the memory leak in the dashboard"
```

**Process:**
1. **Duplicate Check (25/25)**:
   - Search: No duplicate fix implementations
   - Result: ✅ PASS

2. **Architecture Check (0/25)**:
   - Issue: User didn't specify which component has leak
   - Dashboard has 15+ components (DashboardPage, Sidebar, Charts, Tables, Modals)
   - Cannot determine architecture compliance without knowing affected component
   - Result: ❌ FAIL - Insufficient specification

3. **Docs Check (0/20)**:
   - Issue: "Memory leak" is symptom, not specific API issue
   - No specific docs to verify without knowing leak source
   - Result: ❌ FAIL - Cannot verify docs without root cause

4. **OSS Check (0/15)**:
   - Issue: Cannot research OSS fixes without knowing leak type
   - (Event listeners? Component unmount? Timers? Closures?)
   - Result: ❌ FAIL - Cannot research without specifics

5. **Root Cause Check (0/15)**:
   - Issue: No diagnostic evidence provided
   - Need: Heap snapshot, profiler data, reproduction steps
   - Result: ❌ FAIL - No root cause identified

**Output:**
```json
{
  "feature": "memory_leak_fix",
  "confidence_score": 0.25,
  "decision": "STOP",
  "checks": [
    {"name": "duplicate", "points": 25, "passed": true},
    {"name": "architecture", "points": 0, "passed": false, "reason": "Component not specified"},
    {"name": "docs", "points": 0, "passed": false, "reason": "Cannot verify without root cause"},
    {"name": "oss", "points": 0, "passed": false, "reason": "Cannot research without specifics"},
    {"name": "root_cause", "points": 0, "passed": false, "reason": "No diagnostic evidence"}
  ],
  "missing_checks": [
    {"name": "architecture", "missing_points": 25},
    {"name": "docs", "missing_points": 20},
    {"name": "oss", "missing_points": 15},
    {"name": "root_cause", "missing_points": 15}
  ],
  "action": "STOP - Too many unknowns (25% confidence)",
  "next_steps": [
    "User: Provide diagnostic evidence:",
    "  1. Which component has memory leak? (Chrome DevTools Memory profiler)",
    "  2. Heap snapshot showing leak growth over time",
    "  3. Reproduction steps (actions that trigger leak)",
    "  4. Browser console warnings/errors",
    "Alternative: Run /shannon:spec for deeper analysis phase",
    "Agent: Re-run confidence check after diagnostic evidence provided"
  ]
}
```

**Decision**: STOP 🛑 (25% confidence - critical gaps, requires investigation)

---

## Validation

How to verify confidence-check executed correctly:

1. **Check All 5 Checks Executed**:
   - ✅ duplicate_check: { passed: true|false, points: 0-25 }
   - ✅ architecture_check: { passed: true|false, points: 0-25 }
   - ✅ docs_check: { passed: true|false, points: 0-20 }
   - ✅ oss_check: { passed: true|false|null, points: 0-15 }
   - ✅ root_cause_check: { passed: true|false|null, points: 0-15 }

2. **Check Score Calculation**:
   - ✅ confidence_score = sum(check.points) / 100.0
   - ✅ Score in range [0.00, 1.00]
   - ✅ Example: 25+25+20+0+15 = 85 → 0.85 ✅

3. **Check Decision Threshold**:
   - ✅ ≥0.90 → "PROCEED"
   - ✅ 0.70-0.89 → "CLARIFY"
   - ✅ <0.70 → "STOP"

4. **Check Missing Checks Identified** (if <90%):
   - ✅ missing_checks array not empty
   - ✅ Each entry: { name, missing_points, recommendation }

5. **Check Evidence Documented**:
   - ✅ duplicate_check: File paths or "no duplicate found"
   - ✅ architecture_check: Pattern description or violation
   - ✅ docs_check: Doc URL and verification note
   - ✅ oss_check: Repository URLs with star counts (if applicable)
   - ✅ root_cause_check: Diagnostic evidence (if applicable)

6. **Run Validation Script** (if available):
   ```bash
   python3 shannon-plugin/tests/test_confidence_check.py
   # Expected: ✅ All validation checks passed
   ```

---

## Progressive Disclosure

**In SKILL.md** (this file): ~1100 lines
- Overview, when to use, anti-rationalization
- 5-check algorithm with detailed steps
- Workflow with processing logic
- Integration with Shannon 8D scoring
- 3 examples (PROCEED, CLARIFY, STOP)
- Success criteria, pitfalls, validation

**In references/** (for advanced usage):
- `references/CONFIDENCE_ALGORITHM.md`: Mathematical formulas, edge cases
- `references/OSS_RESEARCH_GUIDE.md`: How to evaluate OSS quality, extract learnings
- `references/ROOT_CAUSE_PATTERNS.md`: Common root cause patterns by domain

**Claude loads references/ when**:
- Score calculation unclear (consult CONFIDENCE_ALGORITHM.md)
- OSS research guidance needed (consult OSS_RESEARCH_GUIDE.md)
- Root cause identification unclear (consult ROOT_CAUSE_PATTERNS.md)

---

## References

- Spec Analysis: shannon-plugin/skills/spec-analysis/SKILL.md
- Wave Orchestration: shannon-plugin/skills/wave-orchestration/SKILL.md
- Context Management: shannon-plugin/core/CONTEXT_MANAGEMENT.md
- MCP Discovery: shannon-plugin/skills/mcp-discovery/SKILL.md
- Testing Philosophy (NO MOCKS): shannon-plugin/core/TESTING_PHILOSOPHY.md

---

## Metadata

**Version**: 4.0.0
**Last Updated**: 2025-11-04
**Author**: Shannon Framework Team (Adapted from SuperClaude)
**License**: MIT
**Status**: Core (QUANTITATIVE skill, mandatory before implementation)
**Proven ROI**: 25-250x token savings in SuperClaude production use
