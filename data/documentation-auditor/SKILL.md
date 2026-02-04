---
name: documentation-auditor
description: プロジェクト内のドキュメント（README.md、CHANGELOG.md、docs/ など）を監査し、コード変更に基づいて更新が必要な箇所を特定・提案します。作業完了後のドキュメント更新確認に使用。
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - Bash
---

# Documentation Auditor Skill

プロジェクト内のドキュメントを監査し、更新提案を行います。

## デフォルト監査対象

以下のドキュメントを自動検出して監査:

- `README.md`, `README.mdx` - プロジェクト説明
- `CHANGELOG.md`, `CHANGELOG.txt` - 変更履歴
- `docs/` ディレクトリ内の全 Markdown
- `.claude/CLAUDE.md` - Claude Code 設定
- `CONTRIBUTING.md` - コントリビューションガイド

## プロジェクト固有設定

`.claude/doc-audit.json` が存在する場合、その設定を優先:

```json
{
  "documents": ["path/to/doc.md"],
  "exclude": ["docs/generated/**"],
  "triggers": {
    "src/api/**": ["docs/api.md"],
    "src/components/**": ["docs/components.md"]
  }
}
```

## 監査プロセス

### 1. 変更検出

`git diff --name-only` で変更ファイルを特定

### 2. 関連ドキュメントの特定

- 変更ファイルのパスに基づいて関連ドキュメントを推定
- プロジェクト設定ファイルがあれば、その triggers を使用

### 3. 整合性チェック

- ドキュメントの内容と実際のコード/設定を比較
- 新機能がドキュメント化されているか
- 削除された機能がドキュメントから削除されているか
- API変更がドキュメントに反映されているか

### 4. 更新提案

- 自動更新可能: 変更内容を提示し、確認後に更新
- 判断が必要: 更新提案と理由を提示

## 出力形式

```markdown
## ドキュメント監査結果

### 更新が必要なドキュメント

1. **README.md**
   - 理由: 新しい CLI オプション --verbose が追加されました
   - 推奨: 「使用方法」セクションに追記

2. **docs/api.md**
   - 理由: /api/users エンドポイントのレスポンス形式が変更
   - 推奨: API リファレンスを更新

更新を実行しますか？
```

## 監査実行手順

1. `git status` と `git diff --name-only HEAD` で変更ファイルを確認
2. プロジェクト内のドキュメントファイルを Glob で検索
3. 変更内容とドキュメントの整合性を確認
4. 更新が必要な場合は具体的な提案を行う
5. ユーザーの承認後に更新を実行
