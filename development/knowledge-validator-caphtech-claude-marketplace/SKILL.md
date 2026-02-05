---
name: knowledge-validator
description: |
  pce-memory + shirushiを活用した知識検証・整合性チェックスキル。
  以下の場合に使用:
  (1) 資料・ドキュメント間の矛盾チェック
  (2) 指示・意思決定の追跡と検証
  (3) 作業途中のリアルタイム整合性チェック
  (4) 成果物と要件の照合検証
  (5) shirushi Doc-IDとコードのトレーサビリティ検証
  「チェックして」「整合性確認」「矛盾ない？」「検証して」「トレーサビリティ」等で起動。
---

# Knowledge Validator

pce-memory + shirushiを活用した5種類の検証ワークフロー。

## 前提条件

- pce-memoryがReady状態であること
- shirushiが設定済みであること（トレーサビリティ検証時）

## クイックスタート

### 1. 矛盾チェック
```
1. pce_memory_activate(scope=["project"], q="対象キーワード")
2. 関連Claimを取得
3. 各Claim間の論理的整合性を検証
4. 矛盾発見時はpce_memory_feedback(signal="outdated")
```

### 2. 意思決定チェック
```
1. pce_memory_activate(q="決定 ADR policy")
2. 決定間の依存関係を確認
3. 新決定と既存決定の競合を検出
```

### 3. リアルタイムチェック
```
1. 作業開始: pce_memory_observe(source_type="chat", content="開始状態")
2. マイルストーン: pce_memory_activate→期待値と比較
3. 逸脱検出時: 即時報告
```

### 4. 成果物チェック
```
1. pce_memory_activate(q="要件 仕様 spec")
2. 要件リストを抽出
3. 成果物と要件を1:1照合
4. カバレッジレポート生成
```

### 5. トレーサビリティチェック（shirushi統合）
```
1. shirushi lint で Doc-ID整合性確認
2. scripts/trace_doc_code.py でコード内参照を収集
3. Doc-ID ↔ Code 照合マトリクスを生成
4. pce-memoryにRelation登録
```

## shirushi Doc-ID形式

`.shirushi.yml`で定義されたID形式を使用。例:
```
DOC-REQ-0001-A
│   │   │    └─ チェックサム（mod26AZ）
│   │   └────── 連番（スコープ内）
│   └────────── 種別（REQ/SPEC/ADR等）
└────────────── コンポーネント
```

## コード内参照形式

```typescript
// @shirushi DOC-REQ-0001-A
export function authenticate() { ... }
```

## 検証レポート形式

```markdown
## 検証レポート

| 項目 | 状態 | 詳細 |
|------|------|------|
| 要件A | ✅ | 実装済み |
| 要件B | ⚠️ | 部分的実装 |
| 要件C | ❌ | 未実装 |

カバレッジ: X/Y (Z%)
```

## 詳細ワークフロー

- **矛盾チェック詳細**: [contradiction-check.md](references/contradiction-check.md)
- **意思決定追跡**: [decision-tracking.md](references/decision-tracking.md)
- **リアルタイム検証**: [realtime-validation.md](references/realtime-validation.md)
- **成果物検証**: [deliverable-check.md](references/deliverable-check.md)
- **トレーサビリティ**: [traceability.md](references/traceability.md)
