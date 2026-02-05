---
name: create-claude-rules
description: Claude Rulesファイルを.claude/rules/ディレクトリに作成・管理する。プロジェクト固有のルール、コーディング規約、ワークフロー設定を追加したい場合に使用。
allowed-tools: Read, Write, Glob, Bash(mkdir:*)
---

# Claude Rules 作成

## 概要

`.claude/rules/` ディレクトリにClaude Rulesファイルを作成・管理するSkill。
Claude Rulesはプロジェクト固有の指示をClaudeに与えるためのMarkdownファイル。

## ディレクトリ構造

```
.claude/
├── CLAUDE.md           # メインプロジェクト指示
├── settings.local.json # ローカル設定
└── rules/
    ├── code-style.md   # コードスタイル
    ├── testing.md      # テスト規約
    └── github.md       # GitHub操作ルール
```

## ルールファイルの作成手順

1. `.claude/rules/` ディレクトリが存在するか確認（なければ作成）
2. ルールの目的に応じたファイル名を決定（kebab-case）
3. Markdownファイルを作成

## ファイル命名規則

- kebab-case を使用: `code-style.md`, `api-design.md`
- 内容を表す具体的な名前にする
- 拡張子は `.md`

## ルールファイルの書式

### 基本形式

```markdown
# ルールのタイトル

## 目的
このルールが適用される状況を説明。

## ガイドライン
- 具体的な指示1
- 具体的な指示2

## 例
具体的なコード例やパターン。
```

### パス固有ルール（特定のファイルにのみ適用）

```markdown
---
paths: src/**/*.swift
---

# Swiftコードスタイル

## ガイドライン
- SwiftLintに従う
- ...
```

## ルールの種類例

| ファイル名 | 用途 |
|-----------|------|
| `code-style.md` | コーディング規約 |
| `testing.md` | テスト方針 |
| `git-workflow.md` | Gitワークフロー |
| `api-design.md` | API設計規約 |
| `security.md` | セキュリティ要件 |
| `github-issues.md` | GitHub Issue管理 |

## ベストプラクティス

- 1ファイル1トピックに集中する
- 具体的な例を含める
- Do's / Don'ts を明確にする
- チームで共有するためgitにコミットする
