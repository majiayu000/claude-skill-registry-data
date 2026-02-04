---
name: eld-sense-scope
description: |
  PCE (Process-Context Engine) のスコープ管理スキル。入れ子プロセス間のコンテキスト継承を設計し、親子間のハンドオフを最適化する。

  トリガー条件:
  - タスクを子タスクに分解する時
  - サブエージェントに作業を委譲する時（Task tool使用時）
  - 並列タスクを起動する時
  - 「このタスクを分割して」
  - 「サブタスクのコンテキストを設計して」
---

# PCE Scope Skill

入れ子プロセス（親→子→孫）間のコンテキスト継承範囲を設計する。

## スコープ設計の原則

### 親→子へ渡すもの（最小コンテキスト）
```yaml
to_child:
  goal: 子タスクの目的（親目的との関係）
  constraints: 子に適用される制約のみ
  references: 必要な参照のみ（フルパス）
  boundary: 子の責務範囲の明確な境界
```

### 子→親へ戻すもの（要約+差分）
```yaml
from_child:
  summary: 成果の要約（3行以内）
  artifacts: 生成した成果物リスト
  decisions: 子が行った重要な決定
  issues: 発見した問題・懸念
  delta: 潜在プールへ追加すべき知見
```

## スコープ破綻の防止

| 問題 | 症状 | 対策 |
|------|------|------|
| 過剰継承 | 子がノイズで混乱 | 最小コンテキストに絞る |
| 過少継承 | 子が前提を誤認 | 必須参照を明示 |
| 境界曖昧 | 責務が重複・漏れ | boundary明確化 |
| 差分欠落 | 親が子の学びを失う | deltaを必須化 |

## 継承設計テンプレート

```markdown
## Task: [親タスク名]

### Subtask 1: [子タスク名]
**Goal**: [子の目的]
**Boundary**: [責務の境界]
**Inherit**:
  - [継承する参照1]
  - [継承する参照2]
**Return**:
  - summary
  - artifacts
  - delta
```

## 使用例

```
User: API実装タスクを3人で分担したい

Claude:
## 親タスク: REST API実装

### Subtask 1: 認証エンドポイント
**Goal**: /auth/* の実装
**Boundary**: 認証のみ、認可は含まない
**Inherit**:
  - docs/adr/ADR-003.md
  - src/models/user.ts
**Return**: 実装ファイル + 認可境界の懸念

### Subtask 2: ユーザー管理エンドポイント
**Goal**: /users/* のCRUD
**Boundary**: ユーザーのみ、権限管理は含まない

### Subtask 3: API共通基盤
**Goal**: エラーハンドリング、バリデーション
**Boundary**: 横断的関心事のみ
```

---

## 品質優先原則（Superpowers統合）

### 核心原則

1. **Epistemic Humility**: 推測を事実として扱わない。`unknown`と言う勇気を持つ
2. **Evidence First**: 結論ではなく因果と証拠を中心にする
3. **Minimal Change**: 最小単位で変更し、即時検証する
4. **Grounded Laws**: Lawは検証可能・観測可能でなければならない
5. **Source of Truth**: 真実は常に現在のコード。要約はインデックス

### 「速さより質」の実践

- 要件の曖昧さによる手戻りを根本から排除
- テストなし実装を許さない
- 観測不能な変更を防ぐ

### 完了の定義

- [ ] Evidence Ladder目標レベル達成
- [ ] Issue Contractの物差し満足
- [ ] Law/Termが接地している（Grounding Map確認）
- [ ] Link Mapに孤立がない
- [ ] ロールバック可能な状態

### 停止条件

以下が発生したら即座に停止し、追加計測またはスコープ縮小：

- 予測と現実の継続的乖離（想定外テスト失敗3回以上）
- 観測不能な変更の増加（物差しで検証できない変更）
- ロールバック線の崩壊（戻せない変更の発生）
