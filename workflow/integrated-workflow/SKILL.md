---
name: integrated-workflow
description: >
  Orchestrate the full formal development pipeline end-to-end:
  Define (VDM-SL contract) → Verify (VDMJ) → Prove (Z3, optional) → Generate (TS/Python code)
  → Test (contract tests), with automated handoff between phases, error recovery,
  and a final session report. Each phase invokes an existing skill
  (define-contract, verify-spec, smt-verify, generate-code, generate-tests).
  Triggered by: "run the full workflow", "end-to-end development",
  "define and generate code for an agent", or when the user requests multiple phases in sequence.
  Japanese triggers: 「統合ワークフローで開発したい」「一気通貫で」「エンドツーエンドで」
  「定義から生成まで」「全フェーズ実行して」
metadata:
  version: "2.1.0"
---

# Integrated Workflow — End-to-End Formal Agent Development

## Overview

This skill orchestrates the full formal development pipeline for multi-agent systems:
**Define → Verify → Prove → Generate → Test** in a single guided session.

Each phase invokes an existing skill, with automated handoff, error recovery,
and a final session report summarizing all results.

各フェーズは既存のスキルを呼び出し、フェーズ間の自動ハンドオフ、エラー回復、
最終セッションレポートの生成を行います。

## Trigger Conditions

Activate this skill when the user says any of:
- 「統合ワークフローで開発したい」「一気通貫で」「エンドツーエンドで」
- "Run the full workflow", "end-to-end development"
- 「定義から生成まで」「全フェーズ実行して」
- "Define and generate code for an agent"
- Explicitly requests multiple phases in sequence

## Workflow Phases

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 1.DEFINE │───>│ 2.VERIFY │───>│ 3.PROVE  │───>│ 4.GENERATE│───>│ 5.TEST  │
│          │    │          │    │ (optional)│    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼
  .vdmsl         PO list        SMT results     TS/Python        Test
   file         + report        + proofs         code           report
```

## Execution Flow

### Phase 0: Session Setup

1. Greet the user and explain the integrated workflow briefly:
   > 「統合ワークフロー」では、エージェントの契約定義から実装コード生成まで、
   > 5つのフェーズを順番に実行します。途中でスキップや中断も可能です。

2. Gather session parameters:
   - **Agent name**: What agent are we defining?
   - **Starting point**: New definition, existing `.vdmsl` file, or natural language spec (MD)?
     - If existing `.vdmsl` file: skip to Phase 2 (Verify)
     - If natural language MD file: invoke `import-natural-spec` first to convert to VDM-SL
   - **Target language**: TypeScript, Python, or both?
   - **SMT verification**: Include Z3 automated proving? (requires Z3 installed)

3. Initialize session state (track mentally, no files needed):
   ```
   agent_name: <name>
   vdmsl_path: <to be determined>
   target_lang: ts | py | both
   smt_enabled: true | false
   phases_completed: []
   ```

セッションパラメータを収集し、内部状態を初期化する。

### Phase 1: Define — Contract Definition

**Invoke**: `define-contract` skill

1. Follow the define-contract SKILL.md flow (5-step dialogue)
2. Guide the user through natural language → VDM-SL conversion
3. Save the generated `.vdmsl` file to the workspace

define-contractスキルの対話フローに従い、自然言語→VDM-SL変換を実施する。

**Handoff criteria** → Phase 2:
- ✅ `.vdmsl` file generated and saved
- ✅ User confirms the specification looks correct

**Error recovery**:
- If user is unsure about VDM-SL concepts → invoke `formal-methods-guide` inline, then return
- If user wants to change the spec → iterate within Phase 1

**Phase report**:
```
📋 Phase 1 Complete: Contract Definition
- File: <agent_name>.vdmsl
- Types defined: <count>
- Functions: <count>
- Operations: <count>
- State variables: <count>
```

### Phase 2: Verify — Specification Verification

**Invoke**: `verify-spec` skill

1. Run VDMJ on the `.vdmsl` file (syntax check → type check → PO generation)
2. Explain each error or PO in natural language
3. Categorize POs by urgency:
   - **Critical**: pre/post-condition obligations, state invariant obligations
   - **Standard**: subtype obligations, non-empty set/seq obligations
   - **Info**: let-be-st, cases exhaustiveness

VDMJで構文チェック→型チェック→PO生成を実行し、各POを平易に解説する。

**Handoff criteria** → Phase 3:
- ✅ Syntax check: PASSED
- ✅ Type check: PASSED
- ✅ POs generated and explained

**Error recovery**:
- Syntax/type errors found → show errors with fix suggestions → return to Phase 1 for spec correction
- After fix → re-run Phase 2

**Phase report**:
```
📋 Phase 2 Complete: Specification Verification
- Syntax check: ✅ PASSED
- Type check: ✅ PASSED
- Proof Obligations: <total_count>
  - Critical: <count>
  - Standard: <count>
  - Info: <count>
```

### Phase 3: Prove — SMT Automated Proving (Optional)

**Invoke**: `smt-verify` skill

**Skip condition**: User chose `smt_enabled: false` in Phase 0, or Z3 is not available.
If skipped, proceed directly to Phase 4.

1. Convert each PO to SMT-LIB format following type/expression mapping rules
2. Run Z3 on each `.smt2` file
3. Report results per PO:
   - `unsat` → ✅ Proved (obligation is guaranteed to hold)
   - `sat` → ⚠️ Counterexample found (specification may have a flaw)
   - `unknown`/`timeout` → ℹ️ Could not determine (may need manual review)

各POをSMT-LIBに変換しZ3で検証。反例があれば仕様修正を提案する。

**Handoff criteria** → Phase 4:
- ✅ All POs processed (proved, counterexample, or unknown)
- ⚠️ If counterexample found: warn user and ask whether to proceed or fix spec first

**Error recovery**:
- Counterexample found → explain the violation → offer to return to Phase 1 to fix the spec
- Z3 timeout → note as "unresolved" and continue (does not block code generation)

**Phase report**:
```
📋 Phase 3 Complete: SMT Automated Proving
- Total POs: <count>
  - ✅ Proved: <count>
  - ⚠️ Counterexample: <count>
  - ℹ️ Unknown/Timeout: <count>
```

### Phase 3.5 (optional): DB Schema — Persistence Design

**Invoke**: `generate-db-schema` skill — only when the spec has persistent state
(a `state` definition the user wants stored in a database).

仕様に永続化すべき state がある場合、コード生成の前に generate-db-schema で
DDL・DEVIATIONS（乖離表）・TRACEABILITY（担保箇所対照表）を導出する。
生成されたスキーマの「アプリ層」補償項目は Phase 4 のデータアクセス層実装に、
「契約テスト」補償項目は Phase 5 のテスト生成に引き継ぐ。

### Phase 3.6 (optional): Route — Model Assignment per Module

**Invoke**: `route-models` skill — recommended for multi-module specs when the
user wants to reduce token cost in the bulk phases (4 and 5).

1. Score each module from the spec's objective signals; reuse the PO counts
   already produced in Phase 2 (Verify) — this is the ideal moment, because
   the verifier's difficulty estimate is fresh.
2. Present the routing table for user confirmation; write `model-routing.json`
   next to the spec and `MODEL-ROUTING.md` alongside it.
3. Phases 4 and 5 will then process each module in a subagent with its assigned
   model (see the routing hooks in `generate-code` / `generate-tests`).
   Verification gates are unchanged; failures escalate one tier per the
   escalation policy.

マルチモジュール仕様で一括フェーズのトークン消費を抑えたい場合、Phase 2 の
PO 件数が手元にあるこの時点で route-models を実行するのが最適。Phase 4・5 は
モジュールごとに割り当てモデルのサブエージェントで処理する。検証ゲートは不変で、
失敗時は1層ずつエスカレーションする。

Skip silently if the user does not ask for cost optimization (single-module
specs rarely benefit).

### Phase 4: Generate — Code Scaffold Generation

**Invoke**: `generate-code` skill

1. Read the verified `.vdmsl` specification
2. Generate code for the chosen target language(s):
   - **TypeScript**: interfaces, factory functions, contract utilities, operation classes
   - **Python**: dataclasses, NewType aliases, contract decorators, operation classes
3. Include runtime contract verification (pre/post/inv checks)
4. Generate as a structured module:
   ```
   generated/<agent_name>/
   ├── types.ts / types.py          # Type definitions
   ├── contracts.ts / contracts.py  # Validation functions
   ├── <agent_name>.ts / .py        # Operation implementations
   └── index.ts / __init__.py       # Module exports
   ```

検証済み仕様からターゲット言語のコードを生成。ランタイム契約検証を含む。

**Handoff criteria** → Phase 5:
- ✅ All types converted
- ✅ All functions/operations generated with contract checks
- ✅ Code compiles/parses without errors

**Error recovery**:
- Unsupported VDM-SL pattern → generate TODO stub with explanation
- Implicit definition → generate stub with `// TODO: implement` comment

**Phase report**:
```
📋 Phase 4 Complete: Code Generation
- Target: <language(s)>
- Files generated: <count>
- Types: <count>
- Functions: <count>
- Operations: <count>
- Runtime contracts: pre=<count>, post=<count>, inv=<count>
```

### Phase 5: Test — Smoke Test & Validation

1. Generate a smoke test file that exercises the generated code:
   - Construct valid instances of each type (using factory functions)
   - Call each function/operation with valid inputs → verify no contract violations
   - Call with invalid inputs → verify contract violations are caught
   - Test invariant enforcement on record types

2. Run the smoke test:
   - **TypeScript**: `npx tsx <test_file>.ts` (or `ts-node`)
   - **Python**: `python3 <test_file>.py`

3. Report test results

生成コードの動作検証としてスモークテストを生成・実行する。

**Completion criteria**:
- ✅ All valid-input tests pass
- ✅ All invalid-input tests correctly catch contract violations
- ✅ No unexpected errors

**Error recovery**:
- Test failure → diagnose issue → fix generated code → re-run
- Runtime error → check type mapping or contract logic

**Phase report**:
```
📋 Phase 5 Complete: Smoke Test
- Tests run: <count>
- ✅ Passed: <count>
- ❌ Failed: <count>
```

## Session Report

After all phases complete (or when the user stops), generate a comprehensive session report.
See `references/session-report-template.md` for the full template.

全フェーズ完了後（またはユーザーが中断した時点で）、包括的なセッションレポートを生成する。

Summary format:
```
═══════════════════════════════════════════════════
  Formal Agent Development — Session Report
  Agent: <agent_name>
  Date: <date>
═══════════════════════════════════════════════════

Phase 1 — Define:    ✅ <agent_name>.vdmsl (<N> types, <M> operations)
Phase 2 — Verify:    ✅ Syntax/Type OK, <N> POs generated
Phase 3 — Prove:     ✅ <N>/<M> POs proved  (or ⏭ Skipped)
Phase 4 — Generate:  ✅ <lang> code generated (<N> files)
Phase 5 — Test:      ✅ All <N> tests passed

Output files:
  - Specification: <path>.vdmsl
  - Generated code: generated/<agent_name>/
  - Test results: generated/<agent_name>/test_<agent_name>.<ext>

═══════════════════════════════════════════════════
```

## Workflow Control

Users can control the workflow at any point:

| Command | Action |
|---------|--------|
| 「次へ」/ "next" | Proceed to next phase |
| 「スキップ」/ "skip" | Skip current phase |
| 「戻る」/ "back" | Return to previous phase |
| 「やり直し」/ "redo" | Re-run current phase |
| 「ここまで」/ "stop here" | End workflow, generate partial report |
| 「状態を見せて」/ "status" | Show current phase and progress |

## Phase Selection — Partial Workflow

Users may enter the workflow at any phase:

- **From MD import**: User provides a natural language spec → `import-natural-spec` → Phase 1
- **From Phase 1**: Full workflow (default)
- **From Phase 2**: User provides existing `.vdmsl` file
- **From Phase 4**: User wants code generation only (verification already done)

Detect the entry point from the user's request and session state.

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
- Pre-phase (MD import): `skills/import-natural-spec/SKILL.md`
- Phase 1: `skills/define-contract/SKILL.md`
- Phase 2: `skills/verify-spec/SKILL.md`
- Phase 3: `skills/smt-verify/SKILL.md`
- Phase 3.5 (DB schema): `skills/generate-db-schema/SKILL.md`
- Phase 3.6 (model routing): `skills/route-models/SKILL.md`
- Phase 4–5: `skills/generate-code/SKILL.md`
- Post-phase (human doc export): `skills/export-human-spec/SKILL.md`
- Background: `skills/formal-methods-guide/SKILL.md`

After the workflow completes, offer the user the option to generate a human-readable
specification document using `export-human-spec`. This is especially valuable when
stakeholders who don't read VDM-SL need to review the spec.
