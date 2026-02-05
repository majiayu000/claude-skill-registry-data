---
name: subagent-patterns
description: SubAgent組み合わせパターン・選択ロジック提供。14種類のAgent定義・選択原則・Phase特性別組み合わせパターン・SubAgent責務境界判定・並列実行判断ロジック。Step開始時のSubAgent選択に使用。
allowed-tools: Read, Grep
---

# SubAgent Patterns Skill

## 概要

このSkillは、Phase・Step特性に応じた最適なSubAgent組み合わせを選択するためのパターン・判断基準・責務境界を提供します。ADR_013 SubAgentプール方式に基づく14種類のAgentの効果的な活用方法を定義します。

## 使用タイミング

Claudeは以下の状況でこのSkillを自律的に使用すべきです：

1. **Step開始時**（最重要）
   - step-start Command実行時
   - SubAgent組み合わせ選択時
   - 並列実行可能性判断時

2. **SubAgent選択迷い時**
   - 複数のAgentが候補になる時
   - 責務境界が不明確な時
   - 並列実行判断が必要な時

3. **エラー修正時**
   - Fix-Mode活用時のSubAgent選択
   - 責務に応じたAgent委託判断

4. **Phase計画時**
   - Phase開始時のSubAgent構成検討
   - Step間のAgent引継ぎ計画

## SubAgentプール（14種類）

### 調査分析系（4Agent）

**詳細**: [`patterns/research-agents-selection.md`](./patterns/research-agents-selection.md)

1. **tech-research**: 技術調査・最新情報収集・ベストプラクティス調査
2. **spec-analysis**: 仕様分析・要件抽出・仕様準拠マトリックス作成
3. **design-review**: 設計整合性確認・Clean Architecture準拠確認
4. **dependency-analysis**: 依存関係特定・実装順序決定・制約リスク分析

---

### 実装系（5Agent）

**詳細**: [`patterns/implementation-agents-selection.md`](./patterns/implementation-agents-selection.md)

1. **fsharp-domain**: F#ドメインモデル・ビジネスロジック実装
2. **fsharp-application**: F#アプリケーションサービス・ユースケース実装
3. **contracts-bridge**: F#↔C#型変換・TypeConverter実装（境界重要）
4. **csharp-infrastructure**: Repository・Entity Framework・外部サービス連携
5. **csharp-web-ui**: Blazor Server・Razor・フロントエンドUI実装

---

### 品質保証系（5Agent）

**詳細**: [`patterns/qa-agents-selection.md`](./patterns/qa-agents-selection.md)

1. **unit-test**: TDD実践・単体テスト設計実装・Red-Green-Refactorサイクル
2. **integration-test**: WebApplicationFactory統合テスト・データベース統合テスト（`Infrastructure.Integration.Tests`専任）
3. **e2e-test**: Playwright E2Eテスト実装・UIインタラクション・エンドツーエンドシナリオテスト（`E2E.Tests`専任・playwright-e2e-patterns Skill活用・Playwright MCP 21ツール）
   - **Playwright Test Agents統合**: MainAgentオーケストレーション型（パターンA/B）
   - **パターンA**: MainAgent → playwright-test-generator → e2e-test → playwright-test-healer（該当時）
   - **パターンB**: MainAgent → e2e-test（既存テストメンテナンス）
4. **code-review**: コード品質・保守性・Clean Architecture準拠・パフォーマンス・セキュリティレビュー
5. **spec-compliance**: 仕様準拠監査・受け入れ基準確認・仕様準拠マトリックス検証

---

## SubAgent責務境界判定

**詳細**: [`rules/agent-responsibility-boundary.md`](./rules/agent-responsibility-boundary.md)

### 実装系Agent責務境界（重要）

#### fsharp-domain
**✅ 実行範囲**:
- `src/UbiquitousLanguageManager.Domain/` 配下のみ
- ValueObjects.fs, Entities.fs, DomainServices.fs 実装
- F#ドメインモデル・ビジネスロジック実装

**❌ 禁止範囲**:
- `tests/` 配下のファイル読み込み・参照
- テスト実装・TDD実践（unit-testの責務）
- Contracts層・Infrastructure層・Web層への言及

#### fsharp-application
**✅ 実行範囲**:
- `src/UbiquitousLanguageManager.Application/` 配下のみ
- UseCase・ApplicationService実装

**❌ 禁止範囲**:
- `tests/` 配下のファイル読み込み・参照
- Domain層・Infrastructure層の実装修正

#### contracts-bridge
**✅ 実行範囲**:
- `src/UbiquitousLanguageManager.Contracts/` 配下のみ
- DTO・TypeConverter・F#↔C#境界実装

**❌ 禁止範囲**:
- Domain層・Application層の実装修正
- テストプロジェクトへの参照

#### csharp-infrastructure
**✅ 実行範囲**:
- `src/UbiquitousLanguageManager.Infrastructure/` 配下のみ
- Repository・Entity Framework・外部サービス連携

**❌ 禁止範囲**:
- Domain層・Application層の実装修正

#### csharp-web-ui
**✅ 実行範囲**:
- `src/UbiquitousLanguageManager.Web/` 配下のみ
- Blazor Server・Razor・フロントエンドUI

**❌ 禁止範囲**:
- 他層の実装修正

### 品質保証系Agent責務境界

#### unit-test
**✅ 実行範囲**:
- `tests/` 配下のすべてのテストプロジェクト
- TDD実践・Red-Green-Refactorサイクル
- テスト実装・既存テスト修正

**❌ 禁止範囲**:
- `src/` 配下の実装コード修正（テスト対象の修正禁止）

#### integration-test
**✅ 実行範囲**:
- `tests/Infrastructure.Integration.Tests/` 専任
- WebApplicationFactory統合テスト・データベース統合テスト
- Testcontainers.PostgreSql使用テスト

**❌ 禁止範囲**:
- `src/` 配下の実装コード修正
- `tests/E2E.Tests/` 配下の実装（e2e-test Agentの責務）

#### e2e-test
**✅ 実行範囲**:
- `tests/E2E.Tests/` 専任
- Playwright E2Eテスト実装・実行・検証
- UIインタラクション・エンドツーエンドシナリオテスト
- playwright-e2e-patterns Skill活用（data-testid/MCP/SignalR）
- Playwright MCP 21ツール直接使用
- **重要**: Playwright Test Agents統合はMainAgentが調整（本Agentは実行・検証担当）

**❌ 禁止範囲**:
- `src/` 配下の実装コード修正（テスト対象の修正禁止）
- `tests/Infrastructure.Integration.Tests/` 配下の実装（integration-test Agentの責務）
- Playwright Test Agentsの直接呼び出し（SubAgent間呼び出し不可・MainAgent責務）

#### code-review
**✅ 実行範囲**:
- 全プロジェクトの読み込み・品質評価
- Clean Architecture準拠・コード品質確認

**❌ 禁止範囲**:
- 実装コードの直接修正（改善提案のみ）

#### spec-compliance
**✅ 実行範囲**:
- 仕様書・実装コードの照合確認
- 仕様準拠マトリックス検証

**❌ 禁止範囲**:
- 実装コードの直接修正（準拠度評価のみ）

---

## Phase特性別組み合わせパターン

**詳細**: [`patterns/phase-specific-combinations.md`](./patterns/phase-specific-combinations.md)

### Pattern A: 新機能実装Phase

**特徴**: 新規ドメインモデル・ユースケース実装

**推奨組み合わせ**:
```
Step1: spec-analysis (仕様分析)
Step2: design-review (設計確認)
Step3: fsharp-domain + unit-test (並列)
Step4: fsharp-application + unit-test (並列)
Step5: contracts-bridge (F#↔C#境界)
Step6: csharp-infrastructure + integration-test (並列)
Step7: csharp-web-ui + integration-test (並列)
Step8: code-review + spec-compliance (並列)
```

### Pattern B: 技術基盤整備Phase

**特徴**: アーキテクチャ改善・技術負債解決

**推奨組み合わせ**:
```
Step1: tech-research + dependency-analysis (並列)
Step2: design-review (設計確認)
Step3: 該当層Agent + unit-test (並列)
Step4: integration-test (統合テスト)
Step5: code-review (品質確認)
```

### Pattern C: テスト強化Phase

**特徴**: テストカバレッジ向上・E2Eテスト実装

**推奨組み合わせ**:
```
Step1: spec-analysis (テスト要件分析)
Step2: unit-test (単体テスト拡充)
Step3: integration-test (統合テスト拡充)
Step4: e2e-test (E2Eテスト実装・playwright-e2e-patterns Skill活用)
Step5: code-review (テスト品質確認)
```

---

## 並列実行判断ロジック

### 並列実行可能な組み合わせ

**実装系 + テスト系**:
```
✅ fsharp-domain + unit-test (並列可能)
✅ fsharp-application + unit-test (並列可能)
✅ csharp-infrastructure + integration-test (並列可能)
✅ csharp-web-ui + integration-test (並列可能)
```

**理由**: テスト系Agentは `tests/` 配下、実装系Agentは `src/` 配下で責務が分離

**品質保証系同士**:
```
✅ code-review + spec-compliance (並列可能)
```

**理由**: 両方とも読み取り専用（実装修正なし）

### 並列実行不可能な組み合わせ

**実装系同士（同一ファイル操作可能性）**:
```
❌ fsharp-domain + fsharp-application (並列不可)
❌ contracts-bridge + csharp-infrastructure (並列不可)
```

**理由**: 同一ファイルへの同時書き込みリスク

**テスト系同士（同一テストプロジェクト操作可能性）**:
```
❌ unit-test + integration-test (並列不可・推奨しない)
```

**理由**: テストプロジェクト参照関係の競合リスク

---

## SubAgent選択チェックリスト

### Step開始時

- [ ] Step特性を判定した（調査分析・実装・テスト・品質保証）
- [ ] 必要なSubAgentをリスト化した
- [ ] 責務境界を確認した
- [ ] 並列実行可能性を判断した
- [ ] SubAgent実行計画を作成した

### SubAgent選択迷い時

- [ ] 責務境界を確認した（`rules/agent-responsibility-boundary.md`）
- [ ] 該当AgentのSubtypeがあるか確認した
- [ ] 並列実行判断ロジックを適用した

### エラー修正時（Fix-Mode）

- [ ] エラー内容で責務判定した
- [ ] 責務マッピングでSubAgent選定した
- [ ] Fix-Mode指示テンプレート使用した

---

## 参照元ADR・Rules

- **ADR_013**: SubAgentプール方式採用
- **ADR_018**: SubAgent指示改善とFix-Mode活用
- **SubAgent組み合わせパターン.md**: Step特性別推奨パターン
- **SubAgent実行ガイドライン.md**: SubAgent起動・実行手順

---

## 関連Skills

- **fsharp-csharp-bridge Skill**: F#↔C#境界の型変換パターン
- **clean-architecture-guardian Skill**: Clean Architecture準拠性チェック
- **tdd-red-green-refactor Skill**: unit-test Agent活用パターン
- **playwright-e2e-patterns Skill**: e2e-test Agent専用・3つのE2Eテストパターン（data-testid/MCP/SignalR）・93.3%効率化実証済み

---

**作成日**: 2025-11-01
**Phase B-F2 Step2**: Agent Skills Phase 2展開
**Phase B-F2 Step3**: E2E専用SubAgent新設（13種類→14種類）
**参照**: SubAgent組み合わせパターン.md、ADR_013, ADR_018, **ADR_024**
**最終更新**: 2025-11-02
