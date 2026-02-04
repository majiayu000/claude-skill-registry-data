---
name: hextra-icon-validator
description: Use this skill when working with Hextra icons to validate icon names against the available icon list. This skill should be invoked whenever you're about to use icon names in Hugo shortcodes, partials, or layouts to ensure they exist in the Hextra theme.
---

# Hextra Icon Validator

This skill validates Hextra icon names to prevent errors from using non-existent icons.

## When to Use

Invoke this skill automatically when:
- Using `{{</* icon "name" */>}}` shortcode
- Using `{{ partial "utils/icon.html" (dict "name" "icon-name") }}` partial
- Adding or editing content that includes icon references
- Reviewing code that uses Hextra icons

## Validation Process

1. **Read the icon list**: Load available icons from `project-docs/hextra-icons.md`
2. **Extract icon names**: Parse the icon list to get all valid icon names
3. **Validate**: Check if the requested icon name exists in the list
4. **Report**:
   - If valid: Confirm the icon exists
   - If invalid: Report error with:
     - The invalid icon name
     - List of similar icon names (using fuzzy matching)
     - Link to full icon list

## Validation Logic

```javascript
// Load icon list from project-docs/hextra-icons.md
// Extract lines that start with "- " (icon list items)
// Create array of valid icon names
// Check if requested icon is in the array
// If not found, suggest similar icons using Levenshtein distance
```

## Example Output

### Valid Icon
```
✓ Icon "github" is valid and available in Hextra theme.
```

### Invalid Icon
```
✗ Icon "githubs" is not available in Hextra theme.

Did you mean one of these?
- github
- gitlab
- gitea

See full icon list: project-docs/hextra-icons.md
```

## Helper Script

This skill uses `icon-search.js` helper script for efficient icon lookup and fuzzy matching.

## Usage by Claude Code

When this skill reports an invalid icon:
1. Claude Code (main) will review the suggested alternatives
2. Choose the most appropriate valid icon based on context
3. Update the code with the correct icon name
4. Optionally explain the change to the user

## 🔧 Auto-fix機能（将来実装予定）

将来的に以下の自動修正機能を提供する予定です:

### 機能概要

スキル実行時に `--fix` フラグを付けると、以下の処理を自動実行:

1. **無効なアイコンを検出**: コンテンツファイルをスキャンし、存在しないアイコン名を特定
2. **最適な代替案を選択**: Levenshtein距離アルゴリズムで最も近い有効なアイコンを自動選択
3. **ファイルを修正**: 無効なアイコン名を有効なものに自動置換（ユーザー確認後）
4. **変更内容をレポート**: 修正されたファイルと変更内容の詳細を出力

### 使用例（将来）

```bash
# 単一ファイルの検証と修正
node .claude/skills/hextra-icon-validator/icon-search.js --fix content/docs/page.md

# ディレクトリ全体を検証と修正
node .claude/skills/hextra-icon-validator/icon-search.js --fix content/**/*.md

# ドライラン（変更を適用せずにプレビュー）
node .claude/skills/hextra-icon-validator/icon-search.js --fix --dry-run content/
```

### 期待される出力例

```
🔍 Scanning files for invalid icons...

Found 3 invalid icons:

1. content/docs/getting-started.md:15
   ❌ Invalid: "githubs"
   ✅ Suggested: "github"

2. content/docs/deployment.md:23
   ❌ Invalid: "rocket-launch"
   ✅ Suggested: "rocket"

3. content/blog/post.md:8
   ❌ Invalid: "email"
   ✅ Suggested: "mail"

Apply these changes? (y/n): y

✅ Fixed 3 icons in 3 files
```

### 安全性の考慮事項

- **確認プロンプト**: デフォルトでユーザー確認を求める
- **バックアップ**: 修正前にファイルのバックアップを作成（`.bak`ファイル）
- **ドライランモード**: `--dry-run` で実際の変更を行わずにプレビュー可能
- **ログ記録**: すべての変更を `icon-fix.log` に記録

### 実装状況

現在この機能は**ドキュメント化のみ**です。実装は将来のバージョンで予定されています。

現時点では、スキルは**検証のみ**を行い、ファイルの修正はClaude Code（メイン会話）が手動で行います。

## Important Notes

- This skill ONLY validates - it does NOT modify files
- File modifications are handled by Claude Code main conversation
- Always check icon names before committing changes
- The skill can validate multiple icons at once if needed
- Auto-fix feature is documented for future implementation
