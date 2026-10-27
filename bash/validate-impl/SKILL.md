---
name: kiro-validate-impl
description: Validate feature-level integration after all tasks are implemented. Checks cross-task consistency, full test suite, and overall spec coverage.
allowed-tools: Read, Bash, Grep, Glob, Agent, Skill, AskUserQuestion
argument-hint: <feature-name> [task-numbers]
---

> **移植说明**｜本文件是 `kiro` skill 的阶段规范（源自 `kiro-validate-impl` skill），由 kiro 总控按需读取并就地执行。
> 文中出现的 `kiro-xxx` / `/kiro-xxx` skill 引用，一律按 `kiro/SKILL.md` 的「阶段解析规则」处理：
> 宿主已注册同名 skill → `Skill(kiro-xxx)`；否则读 `phases/xxx/SKILL.md` 就地执行。
> 相对路径（`rules/`、`templates/`）一律相对本文件所在目录 `phases/validate-impl/`。

# kiro-validate-impl Skill

## Role
Individual tasks have already been reviewed by the per-task reviewer during implementation. Your job is to catch problems that only become visible when looking across all tasks together.

Boundary terminology continuity:
- discovery identifies `Boundary Candidates`
- design fixes `Boundary Commitments`
- tasks constrain execution with `_Boundary:_`
- feature validation checks for cross-task `Boundary Violations`

## Core Mission
- **Success Criteria**:
  - All tasks marked `[x]` in tasks.md
  - Full test suite passes (not just per-task tests)
  - Cross-task integration works (data flows between components, interfaces match)
  - Requirements coverage is complete across all tasks (no gaps between tasks)
  - Design structure is reflected end-to-end (not just per-component)
  - No orphaned code, conflicting implementations, integration seams, or boundary spillover

## What This Skill Does NOT Do
Per-task checks are the reviewer's responsibility during `/kiro-impl`. This skill does **not** re-check:
- Individual task acceptance criteria
- Per-file reality checks (mock/stub detection)
- Single-task spec alignment

This skill's main question is: when the completed tasks are viewed together, do they still respect the designed boundary seams and dependency direction?

## Execution Steps

### Step 1: Detect Validation Target

**If no arguments provided**:
- Parse conversation history for `/kiro-impl` commands to detect recently implemented features and tasks
- Scan `.kiro/specs/` for features with completed tasks `[x]`
- Report detected implementations (e.g., "user-auth: 1.1, 1.2, 1.3")

**If feature provided** (feature specified, tasks empty):
- Use specified feature
- Detect all completed tasks `[x]` in `.kiro/specs/{feature}/tasks.md`

**If both feature and tasks provided** (explicit mode):
- Validate specified feature and tasks only (e.g., `user-auth 1.1,1.2`)

### Step 2: Gather Context

If steering/spec context is already available from conversation, skip redundant file reads.
Otherwise, for each detected feature:
- Read `.kiro/specs/<feature>/spec.json` for metadata
- Read `.kiro/specs/<feature>/requirements.md` for requirements
- Read `.kiro/specs/<feature>/design.md` for design structure
- Read `.kiro/specs/<feature>/tasks.md` for task list and Implementation Notes
- Core steering context: `product.md`, `tech.md`, `structure.md`
- Additional steering files only when directly relevant to the validated boundaries, runtime prerequisites, integrations, domain rules, security/performance constraints, or team conventions that affect the GO/NO-GO call

**Discover canonical validation commands**:
- Inspect repository-local sources of truth in this order: project scripts/manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, app manifests), task runners (`Makefile`, `justfile`), CI/workflow files, existing e2e/integration configs, then `README*`
- Derive a feature-level validation set for this repo: `TEST_COMMANDS`, `BUILD_COMMANDS`, and `SMOKE_COMMANDS`
- Prefer commands already used by repo automation over ad hoc shell pipelines
- For `SMOKE_COMMANDS`, choose the lightest trustworthy runtime-liveness check for the app shape (for example: root URL load, Electron launch, CLI `--help`, service health endpoint, mobile simulator/e2e harness if one already exists)
- If multiple candidates exist, prefer the command with the smallest setup cost that still exercises the real built artifact

### Step 3: Execute Integration Validation

#### Subagent Dispatch (parallel)

These validation dimensions are independent — dispatch them as **concurrent subagents in a single message** via the Agent tool, following `../../rules/parallel-dispatch.md`. Adjust the decomposition to feature scope: split, merge, or skip. Each returns a **structured findings summary** so the main context stays clean for GO/NO-GO synthesis.

**Typical validation dimensions** (adjust as appropriate):
- **Test execution** (`general-purpose`, runs commands): Run the complete test suite, report pass/fail with details
- **Requirements coverage** (`Explore`): Build requirements → implementation matrix, report gaps
- **Design alignment** (`Explore`): Verify architecture matches design.md, report drift and dependency violations
- **Cross-task integration** (`Explore`): Verify data flows, API contracts, shared state consistency — the dimension per-task review structurally cannot see, and therefore the highest-value one here
- **Runtime liveness** (`general-purpose`): Run the smoke command and report what actually happened at boot

Split further when the feature spans several subsystems — one subagent per subsystem for the coverage dimension beats one sweeping the whole repo.

**The GO/NO-GO call stays in the parent.** Subagents report findings; only the parent sees all dimensions at once and can weigh them. Never let a subagent return a GO verdict.

For simple features (few tasks, small scope), run checks in main context without subagent dispatch.

#### Mechanical Checks (run commands, use results)

These checks apply at the feature level. Use command output as the primary signal.

**A. Full Test Suite**
- Run the discovered canonical full-test command. Use the exit code.
- If tests fail → NO-GO. No judgment needed.
- If the canonical test command cannot be identified → `MANUAL_VERIFY_REQUIRED`

**B. Residual TBD/TODO/FIXME**
- Run: `grep -rn "TBD\|TODO\|FIXME\|HACK\|XXX" <files-in-feature-boundary>`
- If matches found that were introduced by this feature → flag as Warning

**C. Residual Hardcoded Secrets**
- Run: `grep -rn "password\s*=\|api_key\s*=\|secret\s*=\|token\s*=" <files-in-feature-boundary>` (case-insensitive)
- If matches found that aren't environment variable references → flag as Critical

**D. Runtime Liveness (Smoke Boot)**
- Run the discovered canonical smoke command that proves the built artifact actually starts and reaches its first usable state.
- Examples if relevant: open the root URL in a headless browser and require zero boot-time console errors; launch Electron and wait for the main process ready signal and first renderer load; run a CLI with `--help`; start a service and hit its health endpoint.
- If boot produces a runtime crash, unhandled exception, module-load failure, native ABI mismatch, or missing required env/config → NO-GO.
- If no trustworthy smoke command can be identified, or the required runtime environment is unavailable → `MANUAL_VERIFY_REQUIRED`

#### Judgment Checks (read code, compare to spec)

**E. Cross-Task Integration**
- Identify where tasks share interfaces, data models, or API contracts
- Verify that Task A's output format matches Task B's expected input
- Check for conflicting assumptions between tasks (naming conventions, error codes, data shapes)
- Verify shared state (database schemas, config, environment) is consistent across tasks
- Verify integration work happens at the intended seams rather than by leaking one boundary's behavior into another

**F. Requirements Coverage Gaps**
- Map every requirement section to at least one completed task
- Identify requirements that no single task fully covers (cross-cutting requirements)
- Identify requirements partially covered by multiple tasks but not fully by any
- Use the original section numbering from `requirements.md`; do NOT invent `REQ-*` aliases

**G. Design End-to-End Alignment**
- Verify the overall component graph matches design.md
- Check that integration patterns (event flow, API boundaries, dependency injection) work as designed
- Verify dependency direction follows design.md's architecture (no upward imports)
- Verify File Structure Plan matches the actual file layout
- Identify any architectural drift from the original design
- Use the original section numbering from `design.md`

**G.5 Boundary Audit**
- Compare completed work against the design's `Boundary Commitments`, `Out of Boundary`, `Allowed Dependencies`, and `Revalidation Triggers`
- Identify cross-task spillover where one area quietly absorbed another boundary's responsibility
- Identify downstream-specific workarounds embedded upstream "to make integration easier"
- Identify new hidden dependencies or shared ownership that were not declared in the design
- If a revalidation trigger fired, verify the affected adjacent specs or integration points were actually re-checked

**H. Blocked Tasks & Implementation Notes**
- Check for any tasks still marked `_Blocked:_` — report why and assess impact on feature completeness
- Review `## Implementation Notes` in tasks.md for cross-cutting insights that need attention

### Step 4: Generate Report

Before returning `GO`, apply the `kiro-verify-completion` protocol to the feature-level claim. Tests alone are insufficient: include full-suite, runtime liveness, coverage, integration, design-alignment, and blocked-task status in the evidence.

Classify concrete failures by ownership before writing remediation:
- `LOCAL` if the defect belongs to the feature being validated
- `UPSTREAM` if the root cause belongs to a dependency, foundation, shared platform, or earlier spec
- `UNCLEAR` if ownership cannot be established from the available evidence

If ownership is `UPSTREAM`, do not collapse the issue into local remediation for this feature. Name the owning upstream spec and explain which dependent specs should be revalidated after that upstream fix lands.

Provide summary in the language specified in spec.json:

```
## Validation Report
- DECISION: GO | NO-GO | MANUAL_VERIFY_REQUIRED
- MECHANICAL_RESULTS:
  - Tests: PASS | FAIL (command and exit code)
  - TBD/TODO grep: CLEAN | <count> matches
  - Secrets grep: CLEAN | <count> matches
  - Smoke boot: PASS | FAIL | MANUAL_REQUIRED
- INTEGRATION:
  - Cross-task contracts: <status>
  - Shared state consistency: <status>
  - Boundary audit: <status>
- COVERAGE:
  - Requirements mapped: <X/Y sections covered>
  - Coverage gaps: <list of uncovered requirement sections>
- DESIGN:
  - Architecture drift: <findings>
  - Dependency direction: <violations if any>
  - File Structure Plan vs actual: <match/mismatch>
- OWNERSHIP: LOCAL | UPSTREAM | UNCLEAR
- UPSTREAM_SPEC: <feature-name | N/A>
- BLOCKED_TASKS: <list and impact assessment>
- REMEDIATION: <if NO-GO: specific, actionable steps to fix each issue>
```

If NO-GO, REMEDIATION is mandatory — identify the exact issue and what needs to change. Vague feedback is not acceptable.

## Important Constraints
- **Strict Final Gate**: Return `GO` only when all integration checks passed; return `NO-GO` for concrete failures and `MANUAL_VERIFY_REQUIRED` when mandatory validation could not be completed
- **Boundary integrity over convenience**: Do not return `GO` if the feature only works by smearing responsibilities across boundaries, even when tests pass

## Safety & Fallback

### Error Scenarios
- **No Implementation Found**: If no `[x]` tasks found, report "No implementations detected"
- **Test Command Unknown**: Return `MANUAL_VERIFY_REQUIRED` and explain which validation command is missing; do not return `GO`
- **Missing Spec Files**: Stop with error if spec.json/requirements.md/design.md missing

### Next Steps Guidance

**If GO Decision**:
- Feature validated end-to-end and ready for deployment or next feature

**If NO-GO Decision**:
- Address issues listed in REMEDIATION
- Re-run `/kiro-impl {feature} [tasks]` for targeted fixes
- Re-validate with `/kiro-validate-impl {feature}`

**If MANUAL_VERIFY_REQUIRED**:
- Do not treat the feature as complete
- Provide the exact missing validation step or environment prerequisite
