---
name: eld-record-collection
description: |
  PCE (Process-Context Engine) のContext Delta収集スキル。開発プロセス中に生まれた知見を体系的に収集・記録する。

  トリガー条件:
  - 意思決定を行った時（「なぜこの設計にしたか記録して」）
  - バグを解決した時（「このバグ修正の知見を残して」）
  - アーキテクチャ決定をした時（「ADRを作成して」）
  - パターン/アンチパターンを発見した時（「このパターンを記録して」）
  - セッション終了時（「今日の学びをまとめて」）
---

# PCE Collection Skill

Context Deltaを収集し、潜在的コンテキストプールを拡充する。

## 収集対象

### 1. 意思決定の痕跡
```yaml
decision:
  what: 何を決定したか
  why: なぜその選択をしたか
  alternatives: 検討した他の選択肢
  rejected_reasons: 却下した理由
  constraints: 効いた制約条件
  trade_offs: 受け入れたトレードオフ
```

### 2. エラー解決策
```yaml
error_resolution:
  symptom: 症状・エラーメッセージ
  root_cause: 根本原因
  solution: 解決策
  prevention: 再発防止策
  related_files: 関連ファイル
```

### 3. パターン発見
```yaml
pattern:
  name: パターン名
  context: 適用コンテキスト
  problem: 解決する問題
  solution: 解決方法
  consequences: 結果と影響
  examples: 実例
```

## 収集プロセス

1. **観察**: 作業中の重要な判断・発見を特定
2. **抽出**: 上記フォーマットで構造化
3. **検証**: 記録内容の正確性を確認
4. **保存**: pce-memoryまたは適切な場所に記録

## 出力先の選択

| 知見の種類 | 出力先 |
|-----------|--------|
| 即時参照が必要 | pce-memory (upsert) |
| アーキテクチャ決定 | docs/adr/ |
| プロジェクト共通 | ルートCLAUDE.md |
| ドメイン固有 | 該当フォルダのCLAUDE.md |

## 使用例

```
User: このAPIエンドポイントの設計判断を記録して

Claude:
収集した意思決定:
- what: REST APIではなくGraphQLを採用
- why: クライアント側でのデータ取得柔軟性
- alternatives: REST, gRPC
- rejected_reasons: RESTは過剰取得問題、gRPCはWeb対応コスト
- constraints: フロントエンドチームのGraphQL経験
- trade_offs: 学習コストを許容

→ pce-memory に記録完了
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
