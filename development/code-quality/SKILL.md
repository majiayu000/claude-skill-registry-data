---
name: code-quality
description: コードレビュー、コミットメッセージ生成、リファクタリング提案、テスト作成支援。静的解析、コーディング規約チェック、セキュリティスキャン。「レビュー」「コミット」「リファクタリング」「テスト」「コード品質」に関する質問で使用。
---

# コード品質・レビュー支援

## クイックスタート

### コミットメッセージ生成

```bash
# git diffからコミットメッセージを生成
git diff --staged | python scripts/generate_commit.py
```

### コードレビューチェックリスト

```
レビュー観点:
- [ ] 機能要件を満たしているか
- [ ] エラーハンドリングは適切か
- [ ] テストは十分か
- [ ] パフォーマンス問題はないか
- [ ] セキュリティ上の問題はないか
- [ ] 可読性・保守性は良いか
```

## レビュー観点

| 観点 | 確認内容 |
|------|----------|
| 正確性 | ロジックエラー、境界値、null処理 |
| セキュリティ | インジェクション、認証・認可、機密情報 |
| パフォーマンス | N+1、メモリリーク、不要な処理 |
| 可読性 | 命名、複雑度、コメント |
| 保守性 | 重複、結合度、テスタビリティ |

## 詳細ガイド

- **レビューガイド**: [reference/review.md](reference/review.md)
- **コミット規約**: [reference/commit.md](reference/commit.md)
- **リファクタリング**: [reference/refactoring.md](reference/refactoring.md)
- **テスト作成**: [reference/testing.md](reference/testing.md)

## ユーティリティスクリプト

```bash
# コミットメッセージ生成
python scripts/generate_commit.py

# 複雑度分析
python scripts/analyze_complexity.py src/

# セキュリティスキャン
python scripts/security_scan.py --path ./
```

## ワークフロー: コードレビュー

```
進捗チェックリスト:
- [ ] 1. 変更概要の把握（PR説明、コミット履歴）
- [ ] 2. 全体構造の確認
- [ ] 3. 詳細レビュー（ロジック、エラー処理）
- [ ] 4. テストの確認
- [ ] 5. セキュリティチェック
- [ ] 6. フィードバック作成
```
