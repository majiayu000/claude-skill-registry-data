---
name: reverse-workflow
description: >
  Orchestrate the full reverse engineering pipeline: Extract provisional spec from existing code,
  refine through dialogue to uncover the true spec, then reconcile code with the confirmed spec.
  Optionally connects to the forward pipeline (verify → prove → generate → test).
  Triggered by: "reverse workflow", "extract and refine spec from code",
  "formalize existing code", "reverse engineer the specification",
  「リバースワークフローで」「既存コードから仕様を起こして」「コードの仕様を明確にしたい」
  「このプロジェクトを形式仕様で整理したい」「既存コードをリバースエンジニアリングして」
metadata:
  version: "1.4.0"
---

# Reverse Workflow — Spec Extraction, Refinement, & Code Reconciliation

## Overview

This skill orchestrates the full reverse engineering pipeline for formalizing existing code:
**Extract → Refine → Reconcile → (optionally) Verify → Prove → Generate → Test**

Each phase invokes an existing skill, with automated handoff, error recovery,
and a final session report summarizing all results.

この skill は既存コードを形式化するためのリバースエンジニアリング pipeline 全体をオーケストレートする。
各フェーズは既存スキルを呼び出し、フェーズ間の自動ハンドオフ、エラー回復、
最終セッションレポートの生成を行う。

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 1. EXTRACT  │────>│ 2. REFINE    │────>│ 3. RECONCILE │────>│ 4. VERIFY    │
│ 仮仕様抽出   │     │ 対話的磨き上げ │     │ コード照合     │     │ (既存スキル)  │
└─────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                          ▲  │                                      │
                          │  ▼                                      ▼
                     収束するまで                              既存フォワード
                     サイクルを回す                            パイプラインへ接続
                                                               (verify/prove/generate/test)
```

## Trigger Conditions

Activate this skill when the user says any of:
- 「リバースワークフローで」「既存のコードから仕様を起こして」
- "Run reverse workflow", "extract and refine spec from code"
- 「コードの仕様を明確にしたい」「このコードを形式的に整理したい」
- "Reverse engineer this code", "formalize the existing implementation"
- 「既存コードをVDM-SLで仕様化して」「コードベースをリバースエンジニアリングして」
- Explicitly requests extraction, refinement, and/or reconciliation in sequence

## Workflow Phases

```
┌──────────┐    ┌──────────┐    ┌────────────┐    ┌──────────┐    ┌──────────┐
│ 1.EXTRACT│───>│ 2.REFINE │───>│ 3.RECONCILE│───>│ 4.VERIFY │───>│ 5.PROVE  │
│ 抽出      │    │ 磨き上げ  │    │ 照合       │    │ 検証     │    │ 証明     │
└──────────┘    └──────────┘    └────────────┘    └──────────┘    └──────────┘
                      ▲ │
                      └─┘
                   収束ループ
                  (forward pipeline
                   に接続可能)
```

## Execution Flow

### Phase 0: Session Setup

1. Greet the user and explain the reverse workflow:
   > 「リバースワークフロー」では、既存のコードから形式仕様を起こし、
   > 対話を通じて真の仕様を明確にして、最後にコードと仕様を照合します。
   > 4～7つのフェーズを順番に実行します。途中でスキップや中断も可能です。

2. Emphasize the core principle:
   > **「コードから抽出した仕様は『仮の仕様』です。本当の仕様はあなたの頭の中にあります。」**

3. Gather session parameters:
   - **Project name**: What is this codebase called?
   - **Source code files/directories**: Which files or directories should we analyze?
   - **Source language**: TypeScript, Python, Java, Go, or auto-detect?
   - **Existing artifacts**: Are there tests, documentation, or comments explaining behavior?
   - **Target language for new code** (if reconcile phase generates): TypeScript, Python, or both?
   - **Connect to forward pipeline**: After reconciliation, should we verify/prove/generate?
   - **SMT verification**: Include Z3 automated proving? (requires Z3 installed)

4. Initialize session state (track mentally, no files needed):
   ```
   project_name: <name>
   source_paths: [<paths>]
   source_lang: ts | py | java | go | auto
   provisional_spec_path: <to be determined>
   confirmed_spec_path: <to be determined>
   target_lang: ts | py | both
   forward_pipeline: true | false
   smt_enabled: true | false
   phases_completed: []
   ```

セッションパラメータを収集し、内部状態を初期化する。

### Phase 1: Extract — Provisional Spec Extraction

**Invoke**: `extract-spec` skill

1. Follow the extract-spec SKILL.md flow
2. Analyze source code and extract structural information
3. Generate `.provisional.vdmsl` file with all items tagged `[PROVISIONAL]`
4. List all uncertainties and questions for the user

extract-specスキルの対話フローに従い、コード分析を実施する。

**Handoff criteria** → Phase 2:
- ✅ `.provisional.vdmsl` file generated
- ✅ Extraction report generated
- ✅ Questions list prepared
- ✅ User acknowledges provisional nature

**Error recovery**:
- If code is unparseable → Ask user to narrow scope to specific functions/classes
- If no types/functions found → Verify scope and ask user to point out key areas
- If user unsure about extraction → Proceed to Phase 2 to refine through dialogue

**Phase report**:
```
📋 Phase 1 Complete: Provisional Spec Extraction
- File: <project_name>.provisional.vdmsl
- Types extracted: <count>
- Functions/Operations: <count>
- State variables: <count>
- Questions for user: <count>
- Confidence level: <High|Medium|Low>
```

### Phase 2: Refine — Dialogue-Driven Refinement

**Invoke**: `refine-spec` skill

1. Follow the refine-spec SKILL.md flow (may loop multiple times)
2. Present extracted items and ask clarifying questions
3. For each item, determine:
   - **Confirmed**: Correct as extracted, user agrees
   - **Modified**: Correct concept but needs adjustment
   - **Removed**: Not part of the true spec
   - **Unresolved**: Too unclear to resolve now; mark and continue
4. Build Findings Report:
   - Bugs discovered in the code
   - Gaps between code and intended behavior
   - Refinements to the specification
   - Intentional design decisions (code is correct as-is)
   - Technical debt items
5. Generate confirmed `.vdmsl` (no `[PROVISIONAL]` tags)

refine-specスキルの対話フローに従い、仕様の明確化を実施する。

**Convergence cycles**: This phase may loop multiple times until:
- All `[PROVISIONAL]` items are classified (Confirmed/Modified/Removed/Unresolved)
- User feels confident about the specification
- No new questions emerge from previous round

収束するまで複数回ループする場合がある。

**Handoff criteria** → Phase 3:
- ✅ All `[PROVISIONAL]` items classified
- ✅ Findings Report generated (bugs, gaps, refinements, intentional, debt)
- ✅ Confirmed `.vdmsl` file generated (no `[PROVISIONAL]` tags)
- ✅ User approves confirmed specification

**Error recovery**:
- User very unsure about an item → Mark `[UNRESOLVED]` and continue with rest
- New questions surface during refinement → Document and address in next loop
- Conflicting evidence → Present all interpretations, let user choose

**Phase report**:
```
📋 Phase 2 Complete: Specification Refinement
- Confirmed items: <count>
- Modified items: <count>
- Removed items: <count>
- Unresolved items: <count> (marked [UNRESOLVED])
- Convergence rounds: <count>
- Findings Report:
  - Bugs: <count>
  - Spec gaps: <count>
  - Refinements: <count>
  - Intentional: <count>
  - Technical debt: <count>
```

### Phase 3: Reconcile — Code Alignment & Fix Generation

**Invoke**: `reconcile-code` skill

1. Read confirmed `.vdmsl` specification
2. Read source code
3. Compare specification against code:
   - Does code implement all specified operations?
   - Do pre/post-conditions match code behavior?
   - Are invariants enforced in the code?
   - Are there type mismatches?
4. Generate diff report:
   - Operations that don't match spec
   - Missing runtime checks
   - Potential bugs in code
5. Generate code fixes:
   - Add contract checks (pre/post/invariant)
   - Fix logic bugs if identified
   - Add missing operations (as stubs if needed)
6. Generate auto-generated tests based on confirmed spec
7. Validate fixes (run tests if runtime available)

reconcile-codeスキルの対話フローに従い、コード照合を実施する。

**Handoff criteria** → Phase 4 (Forward Pipeline):
- ✅ Diff report generated
- ✅ Code fixes generated (or identified for manual application)
- ✅ Auto-generated tests created
- ✅ User reviews and approves fixes

**Error recovery**:
- Fix conflicts with other code → Present alternatives or mark for manual review
- Tests fail → Diagnose and adjust fixes
- Missing functionality too complex → Generate stub with TODO and explanation

**Phase report**:
```
📋 Phase 3 Complete: Code Reconciliation
- Diff report: ✅ Generated
- Code fixes: <count> issues identified
  - Type mismatches: <count>
  - Missing contracts: <count>
  - Logic bugs: <count>
- Auto-generated tests: <count>
- Tests status: ✅ All passing  (or ⚠️ <N> failing)
```

### Phase 4: Verify — Forward Pipeline Entry (Optional)

**Invoke**: `verify-spec` skill (from integrated-workflow)

**Skip condition**: User chose `forward_pipeline: false` in Phase 0, or user says "stop here".
If skipped, proceed directly to Session Report.

1. Run VDMJ on the confirmed `.vdmsl` file (syntax check → type check → PO generation)
2. Explain each error or PO in natural language
3. Categorize POs by urgency (Critical, Standard, Info)

既存のverify-specスキルを使用して、確認済み仕様を検証する。

**Handoff criteria** → Phase 5:
- ✅ Syntax check: PASSED
- ✅ Type check: PASSED
- ✅ POs generated and explained

**Error recovery**:
- Syntax/type errors found → show errors with fix suggestions → return to Phase 2 for spec correction
- After fix → re-run Phase 4

**Phase report**:
```
📋 Phase 4 Complete: Specification Verification
- Syntax check: ✅ PASSED
- Type check: ✅ PASSED
- Proof Obligations: <total_count>
  - Critical: <count>
  - Standard: <count>
  - Info: <count>
```

### Phase 5: Prove — SMT Automated Proving (Optional)

**Invoke**: `smt-verify` skill (from integrated-workflow)

**Skip condition**: User chose `smt_enabled: false` in Phase 0, or Z3 is not available.
If skipped, proceed directly to Phase 6 or Session Report.

1. Convert each PO to SMT-LIB format
2. Run Z3 on each `.smt2` file
3. Report results per PO (unsat → proved, sat → counterexample, unknown → undetermined)

既存のsmt-verifyスキルを使用して、PO を Z3 で証明する。

**Handoff criteria** → Phase 6:
- ✅ All POs processed (proved, counterexample, or unknown)
- ⚠️ If counterexample found: warn user and offer to return to Phase 2 to fix spec

**Error recovery**:
- Counterexample found → explain the violation → offer to return to Phase 2 to fix the spec
- Z3 timeout → note as "unresolved" and continue

**Phase report**:
```
📋 Phase 5 Complete: SMT Automated Proving
- Total POs: <count>
  - ✅ Proved: <count>
  - ⚠️ Counterexample: <count>
  - ℹ️ Unknown/Timeout: <count>
```

### Phase 6: Generate & Test (Optional)

**Invoke**: `generate-code` skill (from integrated-workflow)

**Skip condition**: User chose not to generate new code in Phase 0.
If skipped, proceed directly to Session Report.

1. Generate code for the chosen target language(s) from the confirmed spec
2. Generate smoke tests
3. Run smoke tests
4. Report test results

既存のgenerate-codeスキルを使用して、確認済み仕様からコードを生成する。

**Completion criteria**:
- ✅ All types converted
- ✅ All functions/operations generated with contract checks
- ✅ Code compiles/parses without errors
- ✅ All valid-input tests pass
- ✅ All invalid-input tests correctly catch contract violations

**Phase report**:
```
📋 Phase 6 Complete: Code Generation & Testing
- Target: <language(s)>
- Files generated: <count>
- Types: <count>
- Functions: <count>
- Operations: <count>
- Smoke tests: <count>
- ✅ All tests passed
```

## Session Report

After all phases complete (or when the user stops), generate a comprehensive session report.
See `../integrated-workflow/references/session-report-template.md` for the full template.

全フェーズ完了後（またはユーザーが中断した時点で）、包括的なセッションレポートを生成する。

Summary format:
```
═══════════════════════════════════════════════════
  Reverse Workflow — Session Report
  Project: <project_name>
  Date: <date>
═══════════════════════════════════════════════════

Phase 1 — Extract:    ✅ <N> types, <M> operations extracted
Phase 2 — Refine:     ✅ <N> Findings (<bugs> bugs, <gaps> gaps)
                      Convergence: <rounds> rounds
Phase 3 — Reconcile:  ✅ <N> fixes, <M> tests generated
Phase 4 — Verify:     ✅ Syntax/Type OK, <N> POs  (or ⏭ Skipped)
Phase 5 — Prove:      ✅ <N>/<M> POs proved  (or ⏭ Skipped)
Phase 6 — Generate:   ✅ <lang> code generated (<N> files)  (or ⏭ Skipped)

Findings Summary:
  Bug:             <count>  →  Code fixes generated
  Spec Gap:        <count>  →  New code generated
  Spec Refinement: <count>  →  Conditions tightened
  Intentional:     <count>  →  Confirmed as-is
  Debt:            <count>  →  Recorded for future

Output files:
  - Provisional spec: <path>.provisional.vdmsl
  - Confirmed spec: <path>.vdmsl
  - Findings report: <path>-findings.md
  - Code fixes: <list of files>
  - Generated tests: <path>
  - Generated code: <path> (if Phase 6 run)

═══════════════════════════════════════════════════
```

## Workflow Control

Users can control the workflow at any point:

| Command | Action |
|---------|--------|
| 「次へ」/ "next" | Proceed to next phase |
| 「戻る」/ "back" | Return to previous phase |
| 「もう一周」/ "another round" | Re-run refine-spec cycle (Phase 2 only) |
| 「ここまで」/ "stop here" | Generate partial report, stop |
| 「フォワードに接続」/ "connect to forward" | Proceed to verify/prove/generate (if not already) |
| 「状態を見せて」/ "status" | Show current phase and progress |

ユーザーはいつでもワークフローを制御できる。

## Phase Selection — Partial Workflow

Users may enter the workflow at any phase:

- **From Phase 1**: Full reverse workflow (default)
- **From Phase 2**: User provides existing `.provisional.vdmsl` file
- **From Phase 3**: User provides existing `.vdmsl` file (confirmed)
- **From Phase 4**: User wants to verify/prove/generate only (forward pipeline entry)

Detect the entry point from the user's request and available files.

ユーザーは任意のフェーズからワークフローに参加できる。

## Integration with Other Skills

This skill acts as an **orchestrator** — it does not duplicate logic from other skills.
Instead, it:

1. Sets up context and parameters
2. Delegates to the appropriate skill for each phase
3. Handles transitions, error recovery, and reporting
4. Maintains session state across phases

このスキルはオーケストレーターとして機能し、各フェーズの詳細は個別スキルに委譲する。

Reference the individual skill SKILL.md files for phase-specific details:
- Phase 1: `skills/extract-spec/SKILL.md`
- Phase 2: `skills/refine-spec/SKILL.md`
- Phase 3: `skills/reconcile-code/SKILL.md`
- Phase 4–6: Reuse skills from `skills/integrated-workflow/`
- Background: `skills/formal-methods-guide/SKILL.md`
- Human doc export: `skills/export-human-spec/SKILL.md`
- MD spec import: `skills/import-natural-spec/SKILL.md`

After the reverse workflow completes, offer the user the option to generate a
human-readable specification document using `export-human-spec`.
If the user's starting point is a natural language MD file rather than source code,
recommend `import-natural-spec` instead of this reverse workflow.
