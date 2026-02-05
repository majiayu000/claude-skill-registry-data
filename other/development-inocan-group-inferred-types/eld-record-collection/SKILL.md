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
