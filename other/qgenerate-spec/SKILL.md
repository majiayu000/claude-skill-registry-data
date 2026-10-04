---
name: Qgenerate-spec
description: "Use when a routed goal or plan handoff needs TASK_REQUEST and VERIFY_CHECKLIST documents — router-owned internal PSE unit. Use Qgoal to enter; use Qplan for roadmap work."
user_invocable: false
recommendedModel: haiku
tier: core
---

> **`.qe` reads → DB:** `.qe/` content is stored in the SQLite store (`qe_files`), so a path may have **no file on disk**. Read `.qe/` content with `node scripts/qe-cat.mjs <path>` (or `--ls`/`--exists`) and structured state with `node scripts/qe-query.mjs …` — do not assume the raw file exists. See `QE_CONVENTIONS.md`.

# Project Spec Document Generation (Qplan Component)

> Internal PSE unit. Users start work with `{adapter.commandPrefix}Qgoal {목표}`; `user_invocable` is catalog/documentation metadata only. Runtime enforcement is the G010 PreToolUse gate.

## Role
You are a specialist document writer acting as a **sub-component of the `Qplan` ecosystem**. Your primary goal is to transform a high-level roadmap Phase into **Haiku-Ready Atomic Tasks**.

Before generating a spec internally, ensure the shared `QE.md` and active-client instruction pointer exist.
The supported public intake is `Qgoal` or `Qplan`; this stage is not directly invocable.

## Role Constraints (Absolute Rules)
- When this skill is invoked, focus exclusively on writing the 3 spec documents.
- Do not perform any actions outside of document writing, such as writing code, fixing bugs, or answering general questions.
- **User confirmation MUST go through the interaction adapter.** Claude MUST use `AskUserQuestion` and MUST NOT print options as plain text. Codex interactive may print concise plain-text choices because `AskUserQuestion` is not a Codex primitive. Codex non-interactive MUST select the deterministic recommended default and report it.

## Client Adapter Compatibility

Interaction rules:
- **Claude**: use `AskUserQuestion` for Step 3 and any other structured choice.
- **Codex interactive**: ask concise plain-text choices with the same option labels.
- **Codex non-interactive**: choose **Generate Only** unless the task is already chained or the user explicitly requested execution.

Command rendering rules:
- Render handoff commands through `adapter.commandPrefix`.
- Claude examples use `/Q...`, for example `/Qexecute {UUID}`.
- Codex examples use `$Q...`, for example `$Qexecute {UUID}`.

## Documents to Generate

| # | Filename | Path | Description |
|---|----------|------|-------------|
| 1 | Project instruction artifact | Project root | Shared QE context is `QE.md`; the Claude adapter points from `CLAUDE.md` and Codex from `AGENTS.md`. Must reference `QE_CONVENTIONS.md` for QE rules. Task history is in `.qe/TASK_LOG.md`. |
| 2 | `TASK_REQUEST_{UUID}.md` | `.qe/tasks/pending/` | Task request — what, how, checklist, notes |
| 3 | `VERIFY_CHECKLIST_{UUID}.md` | `.qe/checklists/pending/` | Verification checklist — validation criteria, additional notes |

- A single task shares the same UUID across both documents.
- Multiple tasks get separate TASK_REQUEST / VERIFY_CHECKLIST pairs.
- Newly generated documents always go in `pending/`.

## SIVS Single-AI Role Contract

The active client owns every SIVS stage; do not delegate Spec to another AI
client or bridge. The **main thread** creates TASK_REQUEST and
VERIFY_CHECKLIST, then runs the mandatory spec critical gate with isolated
subagent roles. If native subagents are unavailable, use role-separated inline
passes and record `mode=degraded-inline`.

`.qe/sivs-config.json` may set an active-client model or effort, but it cannot
route this stage to Claude or Codex. See `core/SIVS_SINGLE_AI_MODEL.md`.

## Workflow

### Step 1: Context Acquisition (Mandatory)
Before collecting user info, identify the strategic context:
1. **Resolve active plan** (slug-based Named Plan layout):
   - If the first CLI token matches `{slug}:` (where slug is `[a-z0-9][a-z0-9-]{0,63}`), use that as the plan slug and strip it from the argument string.
   - Else read `.qe/state/current-session.json` → extract `session_id` → read `.qe/planning/.sessions/{session_id}.json` → extract `activePlanSlug`.
   - Else read `.qe/planning/ACTIVE_PLAN` (single-line slug pointer).
   - Else (no slug resolvable): fall back to legacy flat `.qe/planning/ROADMAP.md` + `STATE.md` and proceed as before.
2. **Check Roadmap**: When a slug is resolved, read `.qe/planning/plans/{slug}/ROADMAP.md` and `plans/{slug}/STATE.md`. When falling back, read the flat files.
3. **Identify Phase**: If an active Phase exists in the resolved STATE.md, use its **Success Criteria** and **Requirement IDs** as the primary source of truth for the spec.
4. **Missing Roadmap**: If no plan is resolvable and no flat roadmap exists either, **STOP** and suggest running `{adapter.commandPrefix}Qplan` first to maintain the PSE Chain integrity.

### Steps 1.4–1.5: Context dump and clarification

Accept long or unstructured context without asking the user to reformat it. For
Small-or-larger ambiguous work, ask only the highest-impact missing questions;
Micro tasks and exact file/reproduction requests skip clarification. Record every
AI-chosen default under `## 가정 (AI 결정)` as `[ASSUMED]`. Full thresholds,
signals, and question dimensions:
[./reference/spec-workflow.md](./reference/spec-workflow.md).

### Step 2: Information Gathering
... (omitted) ...

Required information:
- **Project name**, **description** (one-paragraph summary)
- **Goals** (1-5 items), **Constraints** (tech stack, performance, security, etc.), **Decisions** (finalized)
- **Task list** — for each task: what, how, steps (checklist), expected output files (optional), notes, type (`code`|`analysis`|`docs`|`other`), validation criteria (checks), verification notes, and optional decision rationale (chosen approach, alternatives, consequences)
- **Code Risk Register** — for every `type: code` task, include a mandatory risk section that names worst-case failure, data loss/corruption risk, security/permission risk, concurrency/race risk, rollback strategy, and unverified assumptions. If a category is not applicable, write `N/A` with the reason; do not omit it.

### Step 2: Draft Documents
Write drafts using templates from `templates/` directory (`TASK_REQUEST_TEMPLATE.md`, `VERIFY_CHECKLIST_TEMPLATE.md`). For any generated project instruction artifact, reference `QE_CONVENTIONS.md` (project root) for QE rules (file naming, task status, completion criteria) and include a reference line pointing to it. Replace `{{placeholder}}` with actual content.
- **Frontmatter substitution (per `core/DOC_CONVENTIONS.md`)**: the title-following `qe-doc-frontmatter` block placeholders are filled deterministically — `{{kind}}` = the generator mapping value (`TASK_REQUEST` → `spec`, `VERIFY_CHECKLIST` → `verify`), `{{plan}}` = the active plan slug, `{{phase}}` = the requested/current phase name, `{{created}}` = today's date (`YYYY-MM-DD`), `{{status}}` = `pending` at creation. Keep the H1 title on line 1 so the completion hook still extracts it; the frontmatter block goes on the line immediately after.
- **Model Preference**: Use **Haiku** for drafting standardized templates to reduce latency.

### Steps 2.4–2.6: Premise and spec gates

Verify external CLI, manifest, hook, API, and npm claims before drafting. Mark
unresolved claims `[UNVERIFIED]` and remove disproved premises. Check structural
and executability criteria, then always run `Qcritical-review --stage spec` with
isolated roles. FAIL remains execution-blocking after at most two revisions;
WARN/PASS may proceed with notes. Full workflow:
[./reference/spec-workflow.md](./reference/spec-workflow.md).

This gate ALWAYS runs. Unlike Step 2.5, it has no skip conditions.

### Step 3: Review, Create, and Execute

Use the interaction adapter to choose Generate Only or Generate & Execute. A
gate-blocked spec may only be saved or revised. Recommend a wave for four or
more independent items. Non-interactive Codex defaults to Generate Only unless
execution was explicitly requested or chained. Create artifacts in pending/ and
chain execution internally; never ask the user to orchestrate internal PSE stages.
Detailed choices and output reporting:
[./reference/spec-workflow.md](./reference/spec-workflow.md).

## Autonomous Mode Support

When called from Qexecute -utopia (autonomous mode), Qgenerate-spec:
- Skips all interaction prompts — auto-selects the documented default
- Auto-proceeds through Steps 1-3 without user confirmation
- Sets `<!-- chained-from: Qgenerate-spec -->` on generated TASK_REQUEST files

See `Qexecute -utopia` for autonomous execution modes (`-utopia`, `-utopia -verify`).

## Document Writing Rules

### Language Matching (Required)
TASK_REQUEST and VERIFY_CHECKLIST must match the user's language.
- Korean user → Korean documents; English user → English documents; mixed/unclear → English
- **Scope:** TASK_REQUEST and VERIFY_CHECKLIST only. Internal framework files stay English. CLAUDE.md follows user language when specified.

### Project Instruction Artifact
- Single Source of Truth for client-specific project context; Claude adapter uses `CLAUDE.md`, Codex-capable projects may use `AGENTS.md` or an equivalent QE-managed instruction file.
- **Do NOT write task lists in the instruction artifact.** Task history lives in `.qe/TASK_LOG.md`. The instruction artifact only contains a reference pointer: `## Task Log` → see `.qe/TASK_LOG.md`

### TASK_REQUEST
- **What vs How**: Clearly separate the business goal from the technical implementation logic (from QE planning patterns).
- **Atomic Items**: Every checklist item must be **independent** and **verifiable**.
- **Dependency Mapping**: If an item depends on another, mark it: `- [ ] {desc} <!-- depends_on: [UUID/Item#] -->`.
- **Haiku-Ready**: Ensure items are small enough to be implemented without Sonnet-level reasoning.
- **Output files**: Always append `→ output: {file-path}` for direct accountability.
- **Assumed defaults**: Any decision the user delegated ("나머지는 알아서") and the AI resolved goes in an optional `## 가정 (AI 결정)` section, one `[ASSUMED]` line per decision with a one-phrase rationale. This keeps delegated choices reviewable instead of buried in the draft.
- **Role ownership**: In role-separated or tiered orchestration, identify the expected implementer-owned files or modules so the reviewer can later judge boundary violations.
- **Code Risk Register (mandatory for `type: code`)**: Add this section before the checklist and fill every field:
  ```markdown
  ## Risk Register
  - Worst-case failure:
  - Data loss / corruption risk:
  - Security / permission risk:
  - Concurrency / race risk:
  - Rollback strategy:
  - Unverified assumptions:
  ```
  The register is a hard SIVS contract. Empty fields, placeholder text, or omitted categories block execution until fixed.

### VERIFY_CHECKLIST
- Each criterion answerable as yes/no
- Task complete when all items checked
- Include note to update `.qe/TASK_LOG.md` task list to ✅
- **Auto-include by type:**
  - `type: code` → add: "No security vulnerabilities (OWASP Top 10) in changed code", "All existing tests pass", "Worst-case failure path is identified", "Data loss/corruption, security/permission, and concurrency/race risks are explicitly evaluated or marked N/A with reason", "Unverified assumptions and residual risks are reported in the final handoff", "High-risk findings are mitigated by tests, defensive code, or an explicit defer rationale"
  - `type: code` + auth/crypto/payment → add: "Authentication/encryption implementation is secure (Esecurity-officer or manual review)"
  - `type: docs` → add: "All links in documentation are valid", "Terminology and formatting are consistent"

## UUID Generation Rules
- 8-character hex (e.g., `a1b2c3d4`), generated randomly
- Same UUID shared between TASK_REQUEST and VERIFY_CHECKLIST for same task
- **Collision check**: Before using a UUID, verify no file matching `TASK_REQUEST_{UUID}.md` already exists in `.qe/tasks/pending/` or `.qe/tasks/completed/`. If it exists, generate a new random UUID and check again.
- Generate UUIDs via bash: `openssl rand -hex 4` (produces 8-char hex)

## Self-Evolving
- After completing tasks, if recurring patterns found, suggest template improvements
- On user approval, reflect patterns in future generation

## Contract Candidate Extraction (Optional)

Only `<!-- contract-candidates: auto -->` enables extraction. Write generated
contracts to `.qe/contracts/pending/`, preserve existing drafts, and require
explicit human approval before promotion. Full rules:
[./reference/document-contracts.md](./reference/document-contracts.md).

## Handoff
After generating spec files (on "Generate Only"), display using the standard handoff format from `QE_CONVENTIONS.md`:

```
Phase {X}: {PhaseName} — Spec complete

PSE: [x] Plan [x] Spec [>] Execute [ ] Verify

{TaskDescription — 다음 작업 내용 한 줄 요약}
Next: {adapter.commandPrefix}Qexecute {UUID}
```

Note: "Generate & Execute" auto-chains, so the handoff is only needed for "Generate Only".

**Fresh-context hint**: If the spec conversation was long (context dump + multi-round clarification), append one line recommending execution from a fresh session: "이 세션의 컨텍스트가 무겁습니다 — 새 세션에서 `{adapter.commandPrefix}Qexecute {UUID}` 실행을 권장합니다." The spec file already carries everything Qexecute needs; LLMs perform best with a lean context, so don't drag the spec-drafting conversation into execution.

## Output Format
- Wrap document content in markdown code blocks when displaying
- Pure markdown only, no JSON
