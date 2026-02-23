---
name: multi-review
description: "This skill should be used when the user wants a comprehensive code review using multiple specialized reviewers in parallel. Invoked with /multi-review or when user asks for 'thorough review', 'full code review', or 'review from multiple perspectives'."
allowed-tools: Read, Bash, Glob, Grep, Write, AskUserQuestion, Task
---

# Multi-Review: Parallel Specialized Code Review

You are orchestrating a comprehensive code review using multiple specialized review agents in parallel.

## Workflow

### Step 1: Identify Changes

Determine what code to review:

```bash
# If in a PR/branch context
git diff main...HEAD --name-only

# Or for staged changes
git diff --cached --name-only

# Or recent changes
git diff HEAD~5 --name-only
```

List the changed files and their types (e.g., `.py`, `.ts`, `.go`).

### Step 1.5: Load Review Configuration

Check for a project-level review configuration:

```bash
# Prefer review.json, fall back to risk-tiers.json for backward compatibility
cat .claude/review.json 2>/dev/null || cat .claude/risk-tiers.json 2>/dev/null || echo "No review config found"
```

If found, parse the configuration:
- `tiers`: Maps risk levels (critical, high, medium, low) to file glob patterns
- `reviewers` (v2): Optional object with `exclude` and `include` arrays for reviewer control

**Backward compatibility:** If the config contains a v1 `frameworks` key, honor it as a gate for framework reviewers and log a deprecation note: "Deprecation: `frameworks` array in risk-tiers.json is deprecated. Framework reviewers now auto-detect. Migrate to review.json v2 schema."

**Risk tier resolution:** For each changed file, match against tier patterns (most specific match wins). If a file matches multiple tiers, use the highest tier. If no match, default to `medium`.

Determine the **overall PR risk tier** = the highest tier among all changed files.

If no review config exists, fall back to the keyword-based behavior in Step 2.

### Step 2: Analyze Change Types

Categorize the changes to select appropriate reviewers:

| Change Type | Indicators | Relevant Reviewers |
|------------|------------|-------------------|
| Auth/Security | login, auth, password, token, jwt, permission | security-sentinel |
| Performance | query, cache, loop, batch, async, database | performance-oracle |
| Architecture | new files, interface, refactor, module | architecture-strategist |
| Patterns | any code change | pattern-recognition-specialist |
| Complexity | any code change | code-simplicity-reviewer |
| Agent/Tool systems | agent definitions, skills, prompts, tool configs | agent-native-reviewer |
| Database migrations | db/migrate/*, schema changes, data backfills | data-integrity-guardian, data-migration-expert |
| Frontend/UI | .tsx, .jsx, .vue, .svelte, .html, .css, templates | (browser testing — see Step 9) |

### Step 2.5: Framework Auto-Detection

Map changed files to framework reviewers. A framework reviewer is activated when at least one changed file matches its patterns. No config required.

| File Patterns | Framework | Agent |
|--------------|-----------|-------|
| `*.tsx`, `*.jsx`, `next.config.*`, `middleware.ts` | `nextjs` | `nextjs-reviewer` |
| `*.css`, `tailwind.*`, `components/ui/**` | `tailwind` | `tailwind-reviewer` |
| `*.py`, `alembic/**` | `python-backend` | `python-backend-reviewer` |
| `routes/**`, `api/**`, `endpoints/**`, `controllers/**` | `api` | `api-security-reviewer` |

**Reviewer overrides (v2 config):**
- `reviewers.exclude`: Suppress auto-detected reviewers (e.g., `["tailwind-reviewer"]` to prevent false positives)
- `reviewers.include`: Force always-on reviewers regardless of changed files (e.g., `["security-sentinel"]`)

**Backward compatibility:** If a v1 config with a `frameworks` key is loaded, use it as a gate — only activate framework reviewers that are both listed in `frameworks` AND matched by changed files (preserves old behavior).

### Step 3: Select Reviewers

**Always include:**
- `code-simplicity-reviewer` (YAGNI, complexity)
- `pattern-recognition-specialist` (anti-patterns, conventions)

**Conditionally include (keyword-based):**
- `security-sentinel` — if auth, input handling, secrets, or user data
- `performance-oracle` — if database queries, loops, caching, or data operations
- `architecture-strategist` — if structural changes, new modules, or interface changes
- `agent-native-reviewer` — if agent definitions, skill files, system prompts, or tool configurations
- `data-integrity-guardian` — if database migrations, schema changes, or data model modifications
- `data-migration-expert` — if data backfills, ID mappings, enum conversions, or column renames

**Tier-based reviewer selection (when review config exists):**

Use the overall PR risk tier from Step 1.5 to adjust reviewer selection:

| Tier | Reviewers |
|------|-----------|
| **critical** | All conditional reviewers that match + ALL matched framework agents |
| **high** | `security-sentinel` + `performance-oracle` + matched framework agents |
| **medium** | `code-simplicity-reviewer` + `pattern-recognition-specialist` + matched framework agents |
| **low** | `code-simplicity-reviewer` + up to 1 matched framework agent |

Always include `code-simplicity-reviewer` and `pattern-recognition-specialist` regardless of tier.

**Select 3-7 reviewers** based on the change types identified.

### Step 3b: Conditional Migration Reviewers

**Run migration-specific agents when the PR matches ANY of these criteria:**

- Files matching `db/migrate/*`, `migrations/*`, or `alembic/versions/*`
- Modifications to columns that store IDs, enums, or mappings
- Data backfill scripts or management commands
- Changes to how data is read/written (e.g., FK to string column)
- PR title/body mentions: migration, backfill, data transformation, ID mapping

**What these agents check:**
- `data-integrity-guardian`: Transaction boundaries, reversibility, constraint safety, ACID compliance, regulatory considerations (GDPR/CCPA)
- `data-migration-expert`: Verifies hard-coded mappings match production reality (prevents swapped IDs), checks for orphaned associations, validates dual-write patterns, provides SQL verification queries

### Step 4: Read Agent Definitions

For each selected reviewer, read the agent definition:

```bash
cat ~/.claude/agents/review/<agent-name>.md
```

### Step 4.5: SAST Artifact Consumption (Hybrid Verification)

Before launching reviewers, check if CI/CD SAST results are available:

```bash
# Check for SARIF artifacts from the security-checks workflow
gh run download --name semgrep-sarif --dir /tmp/sarif 2>/dev/null
```

If SARIF results are found, parse them and include in the `security-sentinel` prompt:

> "The following SAST findings were reported by Semgrep. For each finding, verify it in context: **confirm** as a real vulnerability, **dismiss** as a false positive with explanation, or **escalate** with additional context that amplifies the severity. Do not simply repeat SAST output — add the reasoning that automated tools cannot."

Append the SARIF finding summaries (file, rule ID, message) to the security-sentinel agent's prompt. This creates the hybrid approach: deterministic tools catch patterns, the AI agent reasons about whether they are real vulnerabilities in this specific codebase.

If no SARIF artifacts exist (CI hasn't run, or the project doesn't use the security-checks workflow), skip this step silently.

### Step 5: Launch Parallel Reviews

Use the Task tool to spawn parallel review agents.

**Model selection:** Default to Sonnet for efficiency. When review config exists and the PR risk tier is **critical**, use Opus for `security-sentinel` and `architecture-strategist` (these benefit most from deeper reasoning on critical code). All other reviewers use Sonnet regardless of tier.

```
Launch these agents in parallel:

1. Task: code-simplicity-reviewer
   - Subagent type: general-purpose
   - Model: sonnet
   - Prompt: [agent definition] + [files to review]

2. Task: pattern-recognition-specialist
   - Subagent type: general-purpose
   - Model: sonnet
   - Prompt: [agent definition] + [files to review]

3. Task: security-sentinel (if critical tier)
   - Subagent type: general-purpose
   - Model: opus (critical tier) or sonnet (other tiers)
   - Prompt: [agent definition] + [files to review]

4. Task: [additional selected reviewer]
   ...
```

Each agent should return findings in this format:
```markdown
## [Agent Name] Findings

### Critical Issues
- [Issue with file:line] - Confidence: X%

### Important Issues
- [Issue with file:line] - Confidence: X%

### Suggestions
- [Issue with file:line] - Confidence: X%
```

### Step 6: Aggregate Findings

Combine results from all reviewers, sorted by severity:

```markdown
## Multi-Review Summary

### Reviewers
- [x] code-simplicity-reviewer
- [x] pattern-recognition-specialist
- [x] security-sentinel
- [ ] performance-oracle (not applicable)
- [ ] architecture-strategist (not applicable)

### Critical Issues (Confidence >= 80%)
| File:Line | Issue | Reviewer | Confidence |
|-----------|-------|----------|------------|
| ... | ... | ... | ...% |

### Important Issues (Confidence >= 80%)
| File:Line | Issue | Reviewer | Confidence |
|-----------|-------|----------|------------|
| ... | ... | ... | ...% |

### Suggestions (Confidence >= 80%)
| File:Line | Issue | Reviewer | Confidence |
|-----------|-------|----------|------------|
| ... | ... | ... | ...% |

### Low-Confidence Findings (< 80%)
[Collapsed/summarized - these may be false positives]
```

### Step 7: Filter Results

Only surface findings with **confidence >= 80%**. Lower confidence findings should be mentioned but not emphasized — they may be false positives.

**Security exception:** All `security-sentinel` and `api-security-reviewer` findings appear in the main severity tables regardless of confidence level — never collapse them into "Low-Confidence Findings." Tag each with a `[SEC]` prefix in the Issue column to distinguish them from other reviewer findings. Security issues at any confidence level warrant human review.

### Step 8: Offer Auto-Fix

> **Verification discipline** (from `/verify`): Before proposing any fix, read the actual code at the file:line the reviewer flagged. Reviewers hallucinate. Confirm the issue exists, then fix. If it doesn't exist, drop it — don't implement phantom fixes.

For Critical and Important issues with clear fixes:

```
Would you like me to auto-fix the high-confidence issues?

Auto-fixable:
1. [file:line] - [issue] - [proposed fix summary]
2. [file:line] - [issue] - [proposed fix summary]

Manual review recommended:
3. [file:line] - [issue] - [reason it needs human judgment]

Options:
1. Fix all auto-fixable issues
2. Fix specific issues (provide numbers)
3. Skip auto-fix, I'll handle manually
```

**Maximum 3 review cycles** — if auto-fix is applied, re-run only the affected reviewers (not all). Stop after 3 rounds regardless.

### Step 9: Frontend Browser Testing (Optional)

**When the PR includes frontend/UI changes**, offer browser-based testing using the Claude in Chrome MCP tools.

Detect frontend changes by checking for files matching:
- `*.tsx`, `*.jsx`, `*.vue`, `*.svelte`, `*.html`
- `*.css`, `*.scss`, `*.less`, `*.tailwind`
- `templates/**`, `views/**`, `components/**`, `pages/**`

If frontend changes are detected, use `AskUserQuestion`:

```
This PR includes frontend changes. Would you like me to test the UI in the browser?

1. **Yes — test affected pages** (I'll navigate to the changed routes and verify the UI)
2. **No — skip browser testing**
```

**If the user accepts:**

1. Use `mcp__claude-in-chrome__tabs_context_mcp` to get browser context
2. Create a new tab with `mcp__claude-in-chrome__tabs_create_mcp`
3. Navigate to the dev server URL for each affected route
4. Use `mcp__claude-in-chrome__read_page` to inspect the DOM and verify elements
5. Use `mcp__claude-in-chrome__computer` with `action: screenshot` to capture visual state
6. Check for console errors with `mcp__claude-in-chrome__read_console_messages`
7. Test interactive elements (forms, buttons, navigation) if applicable
8. Report findings:
   - Visual issues (layout breaks, missing elements, styling problems)
   - Console errors or warnings
   - Broken interactions
   - Accessibility concerns from the DOM structure

**Note:** Ask the user for the dev server URL if not obvious from the project config. Common defaults: `localhost:3000`, `localhost:5173`, `localhost:8000`.

## Agent Reference

### Always Included

#### code-simplicity-reviewer
**Focus**: YAGNI, complexity reduction, unnecessary code
**Path**: `agents/review/code-simplicity-reviewer.md`

#### pattern-recognition-specialist
**Focus**: Anti-patterns, code conventions, consistency
**Path**: `agents/review/pattern-recognition-specialist.md`

### Conditionally Included

#### security-sentinel
**Focus**: CWE-enriched OWASP review, business logic vulnerabilities (IDOR, auth bypass), absence detection, self-verification loop
**Include when**: Auth code, user input, API endpoints, secrets handling, new routes/handlers
**Path**: `agents/review/security-sentinel.md`

#### performance-oracle
**Focus**: N+1 queries, memory leaks, caching, async patterns
**Include when**: Database operations, loops over data, caching changes
**Path**: `agents/review/performance-oracle.md`

#### architecture-strategist
**Focus**: SOLID principles, design patterns, module structure
**Include when**: New files, interface changes, structural refactoring
**Path**: `agents/review/architecture-strategist.md`

#### agent-native-reviewer
**Focus**: Action/context parity, tool design, agent capability gaps
**Include when**: Agent definitions, skill files, system prompts, MCP configs
**Path**: `agents/review/agent-native-reviewer.md`

#### data-integrity-guardian
**Focus**: Migration safety, ACID compliance, transaction boundaries, GDPR/CCPA
**Include when**: Database migrations, schema changes, data model modifications
**Path**: `agents/review/data-integrity-guardian.md`

#### data-migration-expert
**Focus**: Mapping validation, rollback safety, production data verification
**Include when**: Data backfills, ID mappings, enum conversions, column renames
**Path**: `agents/review/data-migration-expert.md`

### Framework-Specific Reviewers (Auto-detected from changed files)

#### nextjs-reviewer
**Focus**: App Router conventions, Server vs Client Components, Server Actions security, metadata, routing
**Auto-detected when**: Changed files match `*.tsx`, `*.jsx`, `next.config.*`, `middleware.ts`
**Path**: `agents/review/nextjs-reviewer.md`

#### tailwind-reviewer
**Focus**: Tailwind/shadcn patterns, accessibility, responsive design, dark mode, WCAG 2.1 AA
**Auto-detected when**: Changed files match `*.css`, `tailwind.*`, `components/ui/**`
**Path**: `agents/review/tailwind-reviewer.md`

#### python-backend-reviewer
**Focus**: FastAPI, SQLAlchemy 2.0, Alembic, async Python, Pydantic v2, pytest
**Auto-detected when**: Changed files match `*.py`, `alembic/**`
**Path**: `agents/review/python-backend-reviewer.md`

#### api-security-reviewer
**Focus**: Rate limiting, pagination bounds, response data filtering, CORS, request size limits, security logging
**Auto-detected when**: Changed files match `routes/**`, `api/**`, `endpoints/**`, `controllers/**`
**Path**: `agents/review/api-security-reviewer.md`

## Important Notes

- Parallel execution is key — don't run reviewers sequentially
- Filter to >= 80% confidence to reduce noise
- Security findings should always be surfaced even at lower confidence
- Maximum 3 review cycles for auto-fix iterations
- Migration reviewers should always run together (integrity + migration expert)
- Browser testing is optional and requires user consent
- Framework reviewers auto-detect from changed files. Use `reviewers.exclude` in `review.json` to suppress false positives.
