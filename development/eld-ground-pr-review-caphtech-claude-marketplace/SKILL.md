---
name: eld-ground-pr-review
description: |
  PCE (Process-Context Engine) を活用したPRレビュースキル。Compile→Execute→Captureのフローでレビューを行い、知見を蓄積する。
  LDE（Law-Driven Engineering）との統合により、Law遵守・Grounding検証も実行。

  トリガー条件:
  - 「PRをレビューして」
  - 「PR #123 を確認して」
  - 「変更内容をチェックして」
  - gh pr view の結果を見た後
  - 「Law観点でレビューして」
---

# PCE PR Review Skill

PCEフローに基づく体系的なPRレビューを実行する。

## レビューフロー

### Step 1: Compile（投入物の編集）
```yaml
review_context:
  goal: PRの品質確認と改善提案

  references:
    - ADR（関連する設計決定）
    - 設計意図（README/設計メモ）
    - コーディング規約
    - 過去の類似PR
    - 既知のバグ/課題
    - テスト戦略
    - Law Catalog（LDE）
    - Grounding Map（LDE）

  constraints:
    - セキュリティ要件
    - 性能要件
    - 互換性要件

  expected_output:
    - 指摘の分類（Must/Should/Could）
    - 改善提案
    - 承認可否の判断
```

### Step 2: Execute（レビュー実行）

#### 確認観点
1. **機能性**: 要件を満たしているか
2. **設計**: アーキテクチャ決定と整合しているか
3. **コード品質**: 規約に準拠しているか
4. **テスト**: カバレッジは十分か
5. **セキュリティ**: 脆弱性はないか
6. **性能**: ボトルネックはないか
7. **Law遵守（LDE）**: 既存Lawに違反していないか
8. **接地完了（LDE）**: 新規LawにTest/Telemetryがあるか

#### 指摘の分類
| レベル | 意味 | 対応 |
|--------|------|------|
| Must | マージ前に必須 | ブロッカー |
| Should | 強く推奨 | 可能なら対応 |
| Could | あれば良い | 任意 |
| Note | 情報共有 | 対応不要 |

### Step 3: Capture（差分として記録）
```yaml
review_delta:
  adopted_patterns: 採用したパターン
  rejected_patterns: 却下したパターンと理由
  new_rules: 発見した新ルール
  next_review_points: 次回のチェック観点
  test_additions: 追加すべきテスト根拠
  law_candidates: 新Law候補（LDE）
  grounding_gaps: 接地不足のLaw（LDE）
```

### LDE統合チェック（Step 2.5）

LDEプロジェクトでは `/lde-grounding-check` と連携：

```yaml
lde_review:
  law_compliance:
    - law_id: LAW-xxx
      status: PASS | FAIL
      details: <違反箇所>

  grounding_status:
    - law_id: LAW-yyy
      test: ✅ | ❌
      runtime: ✅ | ❌
      telemetry: ✅ | ❌

  new_law_candidates:
    - statement: <発見した制約>
      type: Pre | Post | Invariant | Policy
      action: → /lde-law-card
```

## レビューテンプレート

```markdown
## PR Review: #[番号] [タイトル]

### Summary
[1-2文で変更内容を要約]

### Context（参照した情報）
- ADR: [関連ADR]
- 規約: [参照した規約]

### Findings

#### Must (マージ前に修正必須)
- [ ] [指摘1]

#### Should (強く推奨)
- [ ] [指摘2]

#### Could (あれば良い)
- [ ] [指摘3]

#### Note (情報共有)
- [メモ]

### Decision
- [ ] Approve
- [ ] Request Changes
- [ ] Comment

### Context Delta（記録すべき知見）
- [新しく発見したパターン/ルール]
```

## 使用例

```
User: PR #45 をレビューして

Claude:
## PR Review: #45 ユーザー検索API追加

### Summary
全文検索によるユーザー検索エンドポイントを追加

### Context
- ADR-003: 検索はElasticsearchを使用
- 規約: src/api/CLAUDE.md

### Findings

#### Must
- [ ] SQLインジェクション対策が不十分 (line 45)

#### Should
- [ ] 検索結果のページネーション追加
- [ ] レスポンス時間のログ出力

#### Note
- 既存のUserServiceを適切に活用している

### Decision
- [x] Request Changes

### Context Delta
- 検索APIのセキュリティチェックリストを追加 → pce-memory
```
