---
name: route-models
description: >
  Assign each VDM-SL module to the lightest capable model tier (light / standard / heavy)
  based on objective complexity signals in the contract itself — operation counts,
  implicit definitions, state invariants, quantifiers, and proof-obligation counts —
  to cut token cost without weakening the verification safety net.
  Produces MODEL-ROUTING.md (human-readable, with rationale) and model-routing.json
  (machine-readable, consumed by generate-code / generate-tests / integrated-workflow).
  Triggered by: "route models", "assign models per module", "reduce token cost",
  "which modules can use a lighter model".
  Japanese triggers: 「モデルを割り振って」「モジュールごとに軽量モデルを」
  「トークン消費を抑えたい」「モデルルーティング」「安いモデルで済む部分を分けて」
metadata:
  version: "1.0.0"
---

# Model Routing — Contract-Driven Model Assignment per Module

## Overview

Multi-agent development spends most of its tokens on bulk phases: code generation,
test generation, and reconciliation. Not every module needs the strongest model for
those phases — a types-only module converts mechanically, while a module full of
implicit definitions needs real reasoning.

This skill reads the VDM-SL contract and assigns each module to the **lightest
capable model tier**, using only objective, countable signals from the spec.
The formal contract itself is what makes this safe: whichever model generates
the artifact, the same VDMJ checks and contract tests judge the result.

マルチエージェント開発でトークンを最も消費するのは、コード生成・テスト生成・照合
といった一括処理のフェーズです。型定義だけのモジュールは機械的に変換できる一方、
暗黙的定義だらけのモジュールには本物の推論が要ります。

このスキルは VDM-SL 契約を読み取り、仕様に含まれる客観的で数えられるシグナルだけを
根拠に、各モジュールを「能力が足りる範囲で最も軽いモデル層」へ割り振ります。これが安全
なのは形式契約があるからです — どのモデルが生成しても、同じ VDMJ チェックと契約
テストが結果を判定します。

## Trigger Conditions

Activate this skill when the user says any of:
- 「モデルを割り振って」「モジュールごとに軽量モデルを使いたい」
- 「トークン消費を抑えたい」「コストを下げたい（生成フェーズで）」
- "Route models", "assign models per module", "reduce token cost"
- Before a bulk generation phase over a multi-module spec, when the user wants to reduce cost

## Model Tiers

Tiers are abstract; the concrete model names depend on what the runtime offers.
In Claude Code, subagents accept a `model` parameter — map tiers as follows:

| Tier | Claude Code model | Suited for |
|------|-------------------|-----------|
| **light** | `haiku` | Mechanical conversion: types-only modules, boilerplate, simple pure functions |
| **standard** | `sonnet` | Typical modules: state + invariants, explicit operations |
| **heavy** | `inherit` (the session's main model) | Implicit-definition-heavy modules, cross-module protocol logic, high PO counts |

層は抽象名で扱い、実行環境が提供するモデルに対応付けます。`heavy` は「セッションの
メインモデルを継承」が既定です（メインより強いモデルを勝手に選ばない）。

## Execution Flow

### Step 1: Read the Specification

Read the `.vdmsl` file(s) specified by the user (search the workspace if unspecified).
Split into modules: VDM-SL `module ... end` sections, or treat a flat file as one module.

仕様ファイルを読み、`module ... end` 単位に分割する（フラットな仕様は 1 モジュール扱い）。

### Step 2: Collect Complexity Signals per Module

Count only **objective signals** — no vibes-based judgment. Per module:

| Signal | Why it matters |
|--------|----------------|
| Explicit functions/operations count | Volume of mechanical conversion work |
| **Implicit definitions** (pre/post only, no body) | Requires real implementation reasoning |
| State section with invariants | Cross-cutting consistency logic |
| Quantifiers (`forall` / `exists` / `exists1` / `iota`) | Logic that resists mechanical translation |
| Recursion (`measure` clauses, self-reference) | Termination-sensitive code |
| Cross-module `imports` / `exports` | Protocol logic between agents |
| PO count (if `verify-spec` results exist) | Verifier's own difficulty estimate |

If a PO report from `verify-spec` is available in the session or on disk, use it;
otherwise proceed with the static signals only (do not run VDMJ just for routing).

数えられるシグナルだけを使います。verify-spec の PO レポートがあれば併用し、
なければ静的シグナルのみで進めます（ルーティングのためだけに VDMJ は走らせない）。

### Step 3: Score and Assign Tiers

Apply the scoring rubric in `references/routing-rules.md` (weights and thresholds
are tunable defaults, not laws). Fast paths:

- **Types-only module** (types + invariants, zero functions and zero operations) → always **light**
- **Any implicit definition present** → never light (standard or heavy)

スコアリングの詳細は `references/routing-rules.md` を参照。型定義のみのモジュールは
常に light、暗黙的定義を1つでも含むモジュールは light にしない。

**Precondition — check the session's main model first**: `heavy` maps to `inherit`.
If the session's main model is itself the light tier's model (e.g. the session runs
on Haiku), routing has nothing to save — tell the user and skip. If it equals the
standard tier's model, collapse standard and heavy into one tier.

前提条件：セッションのメインモデルが light 層と同じなら削減の余地がないため、
その旨を伝えてスキップする。standard 層と同じなら standard と heavy を1つの層に
まとめて扱う。

### Step 4: Present the Routing Table for Confirmation

Show the proposed routing as a table and let the user override any row
(AskUserQuestion or direct edit). Never apply routing silently.

```
| Module      | Tier     | Score | Key signals                        |
|-------------|----------|-------|------------------------------------|
| Types       | light    | 1     | types-only (fast path)             |
| TaskStore   | standard | 6     | state+inv, 5 ops, 2 quantifiers    |
| Scheduler   | heavy    | 16    | 3 implicit defs, 14 POs, imports   |
```

提案テーブルを提示し、ユーザーが行単位で上書きできるようにする。無断適用はしない。

### Step 5: Write the Routing Artifacts

1. **`model-routing.json`** — machine-readable, placed next to the spec file.
   Schema in `references/routing-rules.md`. Consumed by `generate-code`,
   `generate-tests`, and `integrated-workflow`.
2. **`MODEL-ROUTING.md`** — human-readable: the table above, per-module rationale,
   and the share of modules routed below the main model (the honest cost metric —
   report percentages of routed work, not fabricated token counts).

成果物は 2つ。機械可読な `model-routing.json`（仕様ファイルの隣に配置）と、
根拠つきの `MODEL-ROUTING.md`。コスト効果は「メインモデルより軽い層に割り振れた
モジュールの割合」で正直に報告する（架空のトークン数は書かない）。

## How Consumers Use the Routing

When `model-routing.json` exists next to the spec, the bulk-phase skills process
each module in a **subagent with the assigned model** (Claude Code: the Task tool's
`model` parameter). If the runtime does not support per-subagent model selection,
present the routing table as a recommendation and proceed normally — the artifacts
are still useful for humans switching models manually.

`model-routing.json` が仕様の隣にあれば、一括フェーズのスキルはモジュールごとに
割り当てモデルのサブエージェントで処理します。サブエージェントのモデル指定が
使えない環境では、推奨表として提示して通常どおり進めます。

## Escalation Policy — The Safety Net

Routing must never weaken quality. The contract checks are the gate:

1. Artifacts generated under a routed model are verified as usual
   (VDMJ checks for specs, contract tests for code, and — for generated test
   suites — a clause-to-test coverage check derived from the contract; see
   `references/routing-rules.md` §4).
2. If verification fails **twice** for the same module under its assigned tier,
   **escalate one tier** (light → standard → heavy) and regenerate.
3. Record escalations in **both** stores: append to `escalation.history` in
   `model-routing.json`, and add the same row to the "Escalations" section of
   `MODEL-ROUTING.md`.
4. Never de-escalate silently; lowering a tier requires user confirmation.

ルーティングで品質を落としてはならない。割り当てモデルでの生成物が同一モジュールで
2回検証に失敗したら1層上げて再生成し、その事実を model-routing.json の
`escalation.history` と MODEL-ROUTING.md の両方に記録する。
層を下げる変更は必ずユーザー確認を取る。

## Honest Scope

- Routing reduces **cost and latency**, not correctness risk — because correctness
  is judged by VDMJ and contract tests, independent of the generating model.
  Without that verification step, this skill's safety argument does not hold.
- Scores are heuristics over the spec's surface; a low-scoring module can still be
  subtle. The escalation policy, not the score, is the real guarantee.

ルーティングが下げるのはコストとレイテンシであって、正しさのリスクではありません —
正しさは生成モデルと独立に VDMJ と契約テストが判定するからです。検証ステップを
省いた運用では、この安全性の議論は成り立ちません。スコアはあくまで表層のヒュー
リスティクスであり、本当の保証は段階的エスカレーションの側にあります。

## Detailed References

- `references/routing-rules.md` — scoring rubric, thresholds, JSON schema,
  escalation details, worked example
