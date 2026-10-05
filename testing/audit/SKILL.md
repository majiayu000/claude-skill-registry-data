---
name: ha:audit
description: Project health audit and health check — architecture, performance, tests, dependencies, code quality. Use when assessing overall project health, before releases, or after refactors.
effort: high
argument-hint: [--quick|--full|--focus=area|--since=commit]
---

# Project Health Audit

Comprehensive project-wide health assessment using 5 parallel specialist subagents.

## Usage

```
/ha:audit              # Full audit (default)
/ha:audit --quick      # 2-3 minute pulse check
/ha:audit --focus=quality      # Deep dive single area
/ha:audit --focus=performance
/ha:audit --since abc123   # Incremental audit since commit
/ha:audit --since HEAD~10  # Audit last 10 commits
```

## When to Use

- **Quarterly** health checks
- **Before major releases**
- **After large refactors**
- **New team member onboarding** (understand codebase health)

## Iron Laws

1. **Wait for ALL agents before synthesizing** — Partial results create misleading health scores because cross-category correlations get missed
2. **Scope agent prompts to specific directories** — Vague prompts like "analyze the codebase" produce generic findings that waste tokens and miss real issues
3. **Never compare scores across projects** — Scoring methodology depends on integration size and maturity; only track trends within the same project
4. **Quick mode before full mode** — Run `--quick` first to catch mypy/hassfest/pytest failures before spending tokens on 5 parallel agents

## Subagent Architecture

Spawn 5 specialists in parallel using Agent tool. Each call routes to a
declared-model plugin specialist (sonnet/haiku) so the work doesn't fall
through to `general-purpose` (Opus by default):

| Subagent | Focus | Output File | Routes to |
|----------|-------|-------------|-----------|
| Architecture Reviewer | Integration structure, quality-scale status, coupling | `arch-review.md` | `ha-patterns-analyst` (sonnet) |
| Performance Auditor | Event-loop discipline (P4), blocking I/O, executor batching | `perf-audit.md` | `blocking-io-auditor` (sonnet) |
| Test Health Auditor | Coverage, black-box tests (P13), flaky tests | `test-audit.md` | `testing-reviewer` (sonnet) |
| Dependency Auditor | Manifest `requirements` (P11), vulnerabilities, outdated | `deps-audit.md` | `general-purpose` (TODO: per-package `pypi-deps-triager` only) |
| Code Quality Auditor | ruff/mypy, dead code (P10), typing discipline | `code-quality.md` | `verification-runner` (sonnet) |

## Workflow

### Step 1: Create Task List and Spawn All 5 Auditors (Parallel)

**Create Claude Code tasks** for real-time progress visibility:

```
For each auditor:
  TaskCreate({subject: "{Area} audit", activeForm: "Auditing {area}..."})
  TaskUpdate({taskId, status: "in_progress"})
```

Then spawn all 5 agents with Agent tool (parallel). Route to declared-model
specialists where they exist, keep `general-purpose` only where no specialist
covers the audit category:

```
Agent(subagent_type: "ha-patterns-analyst",  prompt: "Architecture audit: analyze integration structure, module layout, coupling/cohesion, and quality-scale tier completeness. Write findings to .claude/audit/reports/arch-review.md", run_in_background: true)
Agent(subagent_type: "blocking-io-auditor",  prompt: "Performance audit: blocking I/O on the event loop (P4), unbatched executor jobs, @callback discipline (PS19), coordinator interval config (PS3/PS6). Write findings to .claude/audit/reports/perf-audit.md", run_in_background: true)
Agent(subagent_type: "testing-reviewer",     prompt: "Test health audit: coverage, config-flow 100% (P15), black-box compliance (P13), flakes. Write findings to .claude/audit/reports/test-audit.md", run_in_background: true)
Agent(subagent_type: "general-purpose",      prompt: "Dependency audit: manifest requirements transparency (P11), vulnerabilities (OSV PyPI), outdated pins. Write findings to .claude/audit/reports/deps-audit.md", run_in_background: true)
Agent(subagent_type: "verification-runner",  prompt: "Code quality audit: ruff + mypy + hassfest gates, dead/commented code (P10), typing discipline (P5/P6). Write findings to .claude/audit/reports/code-quality.md", run_in_background: true)
```

**Why specialist routing matters**: `general-purpose` subagents inherit the
parent session model (usually Opus). Plugin specialists declare their own
model in frontmatter (sonnet/haiku for most). Routing 4 of 5 audit tracks to
declared-model specialists materially cuts Opus subagent volume per audit run.

**Agent prompts must be FOCUSED.** Scope each prompt to the
relevant directories and patterns. Do NOT give vague prompts
like "analyze the codebase."

**Output efficiency**: Tell each agent: "Report ONLY issues found.
Do NOT list clean checks, passing categories, or 'What's Good'.
One summary line per clean area suffices."

### Step 2: Collect Results

Wait for ALL auditors to complete. Mark each auditor's task as
`completed` via `TaskUpdate` as it finishes. NEVER proceed while
any auditor is still running.

Read reports from `.claude/audit/reports/`.

**Rate-limit circuit breaker:** if 2+ auditors return empty results or
rate-limit/API errors, STOP spawning. Synthesize from the reports that
exist, mark missing categories as "not audited (rate limit)", and tell
the user to re-run `/ha:audit` after the limit resets. Never leave the
user typing "continue" against dead agents.

### Step 3: Compress Findings

After all 5 auditors complete, spawn context-supervisor:

```
Agent(subagent_type: "context-supervisor", prompt: """
Compress audit findings.
Input: .claude/audit/reports/
Output: .claude/audit/summaries/
Priority: Health scores per category, critical findings
only, cross-category correlations, deduplicate findings
found by 2+ agents.
""")
```

Read `.claude/audit/summaries/consolidated.md` for synthesis.

### Step 4: Calculate Health Score

Each category scores 0-100. See `${CLAUDE_SKILL_DIR}/references/scoring-methodology.md`.

### Step 5: Generate Report

Write to `.claude/audit/summaries/project-health-{date}.md`.

## Output Format

Report includes: Executive summary with health score (A-F, numeric/100),
per-category score table (Architecture, Performance, Tests, Dependencies, Code Quality),
critical issues, top recommendations, and action plan (Immediate/Short-term/Long-term).

## Quick Mode (`--quick`)

Only run essential checks (~2-3 minutes), in dev-loop order:

Run `ruff check homeassistant/components/<domain>/`, then `mypy homeassistant/components/<domain>/`, then `python3 -m script.hassfest --domain <domain>`, then `python3 -c "import homeassistant.components.<domain>"` (catches hard import cycles), then `pytest tests/components/<domain>/ --cov=homeassistant.components.<domain> 2>&1 | tail -20`.

Skip: Full dependency scan, blocking-I/O sweep, test quality metrics, architecture deep dive.

## Focus Mode (`--focus=area`)

Deep dive single area with full specialist resources:

| Focus | Subagent | Extra Checks |
|-------|----------|--------------|
| `architecture` | ha-patterns-analyst | Full import graph, coupling matrix, quality-scale audit, duplication scan — see `boundaries`, `call-tracing`, `techdebt`, and `quality-scale` skills |
| `performance` | blocking-io-auditor | Event-loop blocking sweep (P4), executor discipline, memory/singleton review — see `perf` and `blocking-io-check` skills |
| `tests` | testing-reviewer | Coverage by module, config-flow 100% (P15), black-box compliance (P13) — see `testing`/`verify` skills |
| `deps` | general-purpose | Manifest requirements transparency (P11), OSV/CVE scan, maintenance status (per-package `pypi-deps-triager` only) — see `deps-audit` skill |
| `quality` | verification-runner | ruff + mypy + hassfest, dead code (P10), typing discipline (P5/P6) — see `verify` and `python-idioms` skills |

## Incremental Mode (`--since <commit>`)

Analyze only changes since a specific commit. Useful for pre-merge checks:

Run `git diff --name-only <commit>...HEAD` to identify changed files, then run targeted audits on changed files only (skips full project scan).

Combines with other flags: `/ha:audit --since HEAD~5 --focus=quality`

## Relationship to Other Commands

| Command | Scope | Frequency |
|---------|-------|-----------|
| `/ha:review` | Changed files (diff) | Every PR |
| `/ha:audit` | Entire project | Quarterly |
| `/ha:boundaries` | Integration structure | On-demand |
| `/ha:verify` | Lint/type/test pass | Anytime |

## References

- `${CLAUDE_SKILL_DIR}/references/scoring-methodology.md` - How scores are calculated
- `${CLAUDE_SKILL_DIR}/references/architecture-checks.md` - Detailed architecture criteria
