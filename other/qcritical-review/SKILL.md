---
name: Qcritical-review
user_invocable: true
description: "Critical thinking verification for SIVS stages. Spawns adversarial sub-agents to stress-test specs, implementations, and merge readiness. Also hosts structured debate and evidence-backed risk proof modes. Use for 'review critically', 'stress test this', 'devil advocate', debates, risk proof, or auto-invoked by Qgenerate-spec, Qexecute -verify, Esupervision-orchestrator."
invocation_trigger: When critical verification is needed at any SIVS stage, or when the user wants adversarial review, structured debate, or code risk proof.
recommendedModel: opus
---

> **`.qe` reads → DB:** `.qe/` content is stored in the SQLite store (`qe_files`), so a path may have **no file on disk**. Read `.qe/` content with `node scripts/qe-cat.mjs <path>` (or `--ls`/`--exists`) and structured state with `node scripts/qe-query.mjs …` — do not assume the raw file exists. See `QE_CONVENTIONS.md`.

# Qcritical-review — Adversarial Verification

## Role
Stress-tests artifacts at each SIVS stage through adversarial sub-agents. Produces a structured PASS/WARN/FAIL verdict. Designed to be called standalone or auto-invoked by other SIVS skills. Debate and risk modes are additive compatibility modes; they do not replace the SIVS gate.

## Client Adapter Compatibility

- **Claude**: spawn reviewer agents via Agent tool and `subagent_type` as described below.
- **Codex native**: prefer native Codex subagents through the installed agent TOML. QE-installed TOML files carry `model` and `model_reasoning_effort` converted from each agent's `recommendedModel`.
- **Codex inline fallback**: only when native subagent delegation is unavailable, run reviewer roles as role-separated inline passes in the Lead session and mark the fallback explicitly.
- **Interaction**: ambiguous target selection and WARN/FAIL decisions use the interaction adapter. Claude uses `AskUserQuestion`; Codex interactive uses concise plain-text choices; Codex non-interactive applies the safe recommended default or stops on destructive ambiguity.
- **Command rendering**: user-visible examples use the active client's command prefix.

## CLI Interface

```text
{adapter.commandPrefix}Qcritical-review --stage spec                  # Review a spec document
{adapter.commandPrefix}Qcritical-review --stage verify                # Review an implementation
{adapter.commandPrefix}Qcritical-review --stage supervise             # Review merge readiness
{adapter.commandPrefix}Qcritical-review --mode cross-model            # Deprecated: uses isolated active-client reviewers
{adapter.commandPrefix}Qcritical-review --stage verify --mode cross-model   # Compatibility spelling
{adapter.commandPrefix}Qcritical-review --debate <topic>              # Structured multi-round debate
{adapter.commandPrefix}Qcritical-review --risk {UUID}                 # Evidence-backed code risk proof
{adapter.commandPrefix}Qcritical-review <file>                        # Auto-detect stage from file type
{adapter.commandPrefix}Qcritical-review                               # Auto-detect from recent SIVS context
```

## Review Modes

| Mode | Agents | When to Use |
|------|--------|-------------|
| `isolated-critical` (default) | 3 isolated active-client sub-agents | High-stakes critical review |
| `cross-model` (deprecated) | Resolves to `isolated-critical` | Compatibility only; never invokes another AI client |
| `--debate <topic>` | Debate agents/engines | Structured debate; see [./reference/debate-mode.md](./reference/debate-mode.md) |
| `--risk {UUID}` | Erisk-proof-auditor | Code Risk Gate proof; see [./reference/risk-mode.md](./reference/risk-mode.md) |

SIVS uses one active AI client. Reviewer independence comes from fresh isolated
contexts and non-overlapping adversarial roles; a review mode must not bridge to
another AI client.

## 9-Step Protocol

Each review session runs a structured sequence of up to 9 steps drawn from the OMC critic protocol. Not every SIVS stage runs all 9 steps.

| # | Step | Summary |
|---|------|---------|
| 1 | Pre-commitment Prediction | Before reading, commit to 3–5 predicted problem areas |
| 2 | Multi-perspective Review | Examine through SE / Junior / Ops lenses in parallel |
| 3 | Pre-Mortem | Generate 5–7 failure scenarios assuming exact execution |
| 4 | Ambiguity Scan | Identify steps with two valid but conflicting interpretations |
| 5 | Devil's Advocate | Argue the implementation is wrong; hunt for crashes and silent failures |
| 6 | Self-audit | Re-examine each CRITICAL/MAJOR finding for confidence and bias |
| 7 | Realist Check | Pressure-test severity against realistic worst-case and mitigations |
| 8 | Adversarial Escalation | Trigger max-adversarial mode on CRITICAL findings or 3+ MAJOR |
| 9 | Explicit Gap Analysis | Catalog what is missing — requirements, assumptions, omitted context |

Full definitions: [./reference/nine-step-protocol.md](./reference/nine-step-protocol.md)

## Stage Detection (when --stage is omitted)

| Stage | Detected From | 9-Step Mapping |
|-------|--------------|----------------|
| `spec` | `TASK_REQUEST*.md` or spec file | Steps 1, 2, 4, 9 |
| `verify` | Source code or diff | Steps 3, 5, 6 |
| `supervise` | PR or merge context | Steps 7, 8 |

Detection order:
1. If a file argument is given: match against the Stage column above.
2. If no argument: check `.qe/state/unified-state.json` for last SIVS stage.
3. If ambiguous: ask user via the interaction adapter.

## Execution Procedure

### Step 1: Gather Target Artifact

| Stage | What to Read |
|-------|-------------|
| `spec` | TASK_REQUEST file, VERIFY_CHECKLIST, any referenced design docs |
| `verify` | `git diff` of implementation, test results, checklist status |
| `supervise` | Full PR diff (`git diff main...HEAD`), CI status, review comments |

### Step 2: Spawn Adversarial Agents

Spawn **3 reviewer roles** via the agent adapter. Claude uses 3 sub-agents in parallel via the Agent tool. Codex should use native subagents first, relying on the installed TOML model routing; otherwise run role-separated inline passes and mark the fallback explicitly. Reviewers must NOT see each other's output when the client can enforce isolation.

#### Spec Stage Agents

Full mode definitions live in [./reference/thinking-modes.md](./reference/thinking-modes.md). These agents implement the mandatory Spec self-reference gate: [./reference/spec-gate-protocol.md](./reference/spec-gate-protocol.md).

| Agent | Mode | Role | Key Questions |
|-------|------|------|--------------|
| **Structural Reviewer** | Structural | Stress-test the spec's structure for completeness & internal consistency | "Does every goal map to an item and vice versa? Any contradictory requirements? Dangling dependencies? Subjective/unverifiable items? Whole sub-problems missing?" |
| **Critical Reviewer** | Critical | Devil's advocate on the spec's substance | "What false assumption is this built on? What error case / production scenario is absent? Where will this spec lead the implementer wrong?" |
| **Edge Case Finder** | Critical (boundary) | Identify boundary conditions | "What happens at zero? At max? With concurrent access? With malformed input? With network failure?" |

#### Verify Stage Agents

These agents implement the mandatory Verify gate: [./reference/verify-gate-protocol.md](./reference/verify-gate-protocol.md). The Verify lead and **Devil's Advocate** use high reasoning effort.

| Agent | Role | Key Questions |
|-------|------|--------------|
| **Devil's Advocate** | Argue the implementation is wrong | "Where does this break? What input crashes it? Which test is missing?" |
| **Security Auditor** | Find vulnerabilities | "Is there injection? Auth bypass? Data leak? OWASP Top 10 exposure?" |
| **Performance Skeptic** | Challenge efficiency | "What's the time complexity? Does it scale? Are there N+1 queries? Memory leaks?" |

For `type: code`, all Verify-stage agents also receive the TASK_REQUEST Risk Register and must explicitly challenge low-probability high-impact failures: data loss/corruption, permission escalation, concurrency/race behavior, rollback viability, and unverified assumptions. A HIGH/CRITICAL risk without a mitigation, test, defensive code path, or explicit defer rationale is a FAIL.

#### Supervise Stage Agents

These agents implement the mandatory Supervise gate: [./reference/supervise-gate-protocol.md](./reference/supervise-gate-protocol.md). **Merge Blocker** is the cross-model-upgrade target.

| Agent | Role | Key Questions |
|-------|------|--------------|
| **Merge Blocker** | Argue against merging | "What regression risk exists? Is test coverage sufficient? Are there unresolved TODOs?" |
| **Merge Advocate** | Argue for merging | "What's the cost of delay? Is the remaining risk acceptable? Does it meet the spec?" |
| **Impartial Judge** | Weigh both sides | "Which concerns are valid? Which are hypothetical? What's the actual risk level?" |

For `type: code`, the Supervise-stage review is the final **Code Risk Gate** owner. Merge Blocker must assume the worst credible production outcome and attempt to block merge on any unhandled HIGH/CRITICAL risk, missing rollback story, hidden residual risk, or unverified assumption. Merge Advocate may accept only risks that are explicitly mitigated, tested, or deferred with a named rationale. Impartial Judge must distinguish `verified`, `mitigated`, `deferred`, and `unknown`; `unknown` HIGH/CRITICAL risk is a FAIL.

Supervise-stage agents MUST read the `Qcritical-review --risk` report for `type: code` tasks. Missing `.qe/agent-results/risk-proof-{UUID}.md` is a FAIL unless the task is docs/analysis or no code changed. The report is the authoritative risk input; final-report wording is not accepted as evidence.

### Step 3: Each Agent Output Format

```markdown
## [Agent Role]

### Findings
1. [Finding with severity: CRITICAL / HIGH / MEDIUM / LOW]

### Evidence
- [Specific file:line or section reference for each finding]

### Verdict: [PASS | WARN | FAIL]
- FAIL: Found critical or high-severity issues that must be addressed
- WARN: Found medium issues worth discussing
- PASS: No significant concerns from this perspective
```

### Step 4: Aggregate Verdicts

Collect all 3 agent reports and produce a unified verdict. Before aggregation, collect each reviewer result via `wait_agent` or the active client equivalent, then close every completed reviewer handle with `close_agent` or the active client equivalent. The final report must state `open handles: 0` or include stale warning entries.

Condensed report schema:

```text
Critical Review Report
Stage: [spec | verify | supervise]
Target: [artifact]
Reviewer verdicts: [role + engine + PASS/WARN/FAIL + finding count]
Overall: PASS | WARN | FAIL
Action Items: [severity + concrete fix]
Subagent Lifecycle: open handles: 0; stale warnings: none
```

### Step 5: Verdict Rules

| Condition | Overall Verdict |
|-----------|----------------|
| Any agent returns FAIL | **FAIL** |
| 2+ agents return WARN | **WARN** |
| 1 agent returns WARN, rest PASS | **PASS** (with notes) |
| All agents return PASS | **PASS** |

### Step 6: Present to User

Display the full report, then ask:
- On **FAIL**: "Address the critical items before proceeding. Want me to fix them?"
- On **WARN**: "Review the warnings. Proceed anyway or address them first?"
- On **PASS**: "No critical issues found. Proceed to next stage."

## Agent Spawn Rules

1. All 3 agents run **in parallel** where supported.
2. Prompts include artifact content, role/questions, output format, and: "Be adversarial. Your job is to find problems, not confirm quality."
3. Agents must NOT be told what other agents are looking for.
4. The Lead waits, collects, and closes every reviewer handle; stale handles are warnings.

## Single-AI Reviewer Execution

All reviewers run as isolated subagents of the active client. The Verify and
Supervise leads use high reasoning effort, collect the independent reports, and
create the final verification/QA document. If native subagents are unavailable,
run isolated inline passes, record `mode=degraded-inline`, and cap the verdict at
WARN. Do not invoke a bridge or a second AI client.

#### Bootstrap clause (reviewing Qcritical-review itself)

When a change touches `Qcritical-review` or its `reference/*-gate-protocol.md` files, the gate cannot trust its own (possibly-changed) behavior to review that change — a self-reference within the self-reference defense. In that case the review MUST run against the **pre-change baseline** of these files plus an **explicit diff inspection** of the proposed change, rather than the in-tree (modified) version. This prevents a broken gate edit from approving itself.

## Integration Points

| Caller Skill | When | Stage / Mode |
|-------------|------|--------------|
| `Qgenerate-spec` | After spec generation | `spec` |
| `Qexecute -verify` | After verify loop passes | `verify` |
| `Qexecute -verify` | After Verify and before Supervise for code risk evidence | `--risk {UUID}` |
| `Esupervision-orchestrator` | Before final verdict | `supervise` |

Callers invoke stage review via: `{adapter.commandPrefix}Qcritical-review --stage <stage>`

## Attribution

9-Step Protocol adapted from oh-my-claudecode (MIT, © 2025 Yeachan Heo): https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/agents/critic.md
