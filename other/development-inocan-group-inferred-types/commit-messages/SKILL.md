---
name: commit-messages
description: Conventional Commits formatting guide for creating standardized commit messages. Use when Claude needs to create git commits, ensuring consistent message format with type prefixes (feat, fix, docs, chore). Automatically applied during git commit operations to maintain repository history standards.
---

# コミットメッセージ

明確で標準化されたgitコミットメッセージを作成するためのConventional Commitsフォーマットガイド。

## クイックリファレンス

以下のコミットタイプをプレフィックスとして使用:

- **feat**: 新機能や新しい機能の追加
- **fix**: バグ修正やエラーの修正
- **docs**: ドキュメントのみの変更
- **chore**: メンテナンス、依存関係、設定変更

## メッセージフォーマット

```
type(scope): subject

[optional body]

[optional footer]
```

**基本例:**
```
feat: ユーザー認証機能を追加
```

**スコープ付き:**
```
feat(auth): OAuth2サポートを追加
fix(ui): ボタンの配置を修正
```

**破壊的変更:**
```
feat!: 非推奨のAPIエンドポイントを削除
```

## サブジェクト行のガイドライン

- タイプのプレフィックスで始める（必須）
- スコープを括弧内に追加（任意）
- サブジェクトは50文字以下に保つ
- サブジェクトは小文字で書く
- 末尾にピリオドを付けない
- サブジェクトは日本語または英語で記述可能

**例:**
```
feat(api): ページネーション機能を実装
fix: メモリリークを解決
docs: READMEを更新
chore: 依存関係をアップグレード
feat(grpc): 双方向ストリーミングを追加
```

## タイプ選択ガイド

**feat** → 新しい機能の追加
- 新機能、エンドポイント、ページ
- ユーザー向けの新機能
- 開発者向けの新しいツールや機能

**fix** → 問題の修正
- バグ修正、エラーの修正
- 壊れた機能の修正
- 問題や不具合の解決

**docs** → ドキュメントのみ
- READMEの更新、コメント
- APIドキュメント、ガイド
- コードや設定の変更を含まない

**chore** → その他すべて
- 依存関係の更新、リファクタリング
- 設定変更、ツール設定
- ビルドシステム、CI/CDの更新
- 動作を変更しないコードのクリーンアップ

## 詳細リファレンス

以下を含む包括的なガイドライン:
- 各タイプの詳細な例
- 破壊的変更の表記方法
- 複数行メッセージのフォーマット
- 良い例と悪い例

詳細は [commit-types.md](references/commit-types.md) を参照
