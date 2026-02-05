---
name: creating-adrs
description: >
  MADR形式での構造化ADR作成。トリガー: ADR, Architecture Decision,
  決定記録, 技術選定, アーキテクチャ決定, design decision, 技術的決定, 設計判断,
  deprecation, 非推奨化, process change, プロセス変更
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# ADRクリエーター

## 目的

構造化された6フェーズプロセスを通じてMADR形式でArchitecture Decision Recordを作成。

## 6フェーズプロセス概要

| フェーズ | 目的 | 主要アクション |
| --- | --- | --- |
| 1. 事前チェック | 重複を防止 | 既存ADRをチェック、命名を検証、ディレクトリを確認 |
| 2. テンプレート | 構造を選択 | 決定タイプに基づいて4つのテンプレートから選択 |
| 3. 参照 | 証拠を収集 | プロジェクトドキュメント、Issue、PR、外部リソースを収集 |
| 4. 検証 | 品質保証 | 必須セクションを検証、完全性をチェック |
| 5. インデックス | ドキュメント更新 | ADRリストを自動生成、関連ADRをクロスリンク |
| 6. リカバリー | エラー処理 | パスを自動修正、フォールバックテンプレート |

## テンプレート選択

| テンプレート | ユースケース | 必須セクション |
| --- | --- | --- |
| technology-selection | ライブラリ、フレームワーク選択 | オプション（最低3つ）、Pros/Cons |
| architecture-pattern | 構造、設計ポリシー | コンテキスト、結果 |
| process-change | ワークフロー、ルール変更 | Before/After比較 |
| deprecation | 技術の廃止 | 移行計画、タイムライン |

## 実行フロー

### フェーズ詳細

| フェーズ | 主要アクション |
| --- | --- |
| 1. 事前チェック | `ls docs/adr/*.md`、重複チェック、次の番号を取得 |
| 2. テンプレート | キーワードをテンプレートタイプにマッチ |
| 3. 参照 | プロジェクトドキュメント、Issue、外部リソースを収集 |
| 4. 検証 | 必須セクションをチェック（Title、Status、Context、Decision、Consequences） |
| 5. インデックス | `docs/adr/README.md`を自動生成 |
| 6. リカバリー | 欠落ディレクトリ、重複、欠落セクションを処理 |

## スキル vs ルールの判断

| 観点 | /rulify | /adr:skill |
| --- | --- | --- |
| 目的 | 制約を強制 | パターンを提案 |
| 適用 | 常時アクティブ | キーワードでトリガー |
| 出力先 | docs/rules/ | .claude/skills/ |

**ルールを使用**: セキュリティ要件、絶対的制約
**スキルを使用**: 実装パターン、コンテキスト依存のガイダンス

## ベストプラクティス

| プラクティス | する | しない |
| --- | --- | --- |
| トリガー | 具体的な用語: "React Query", "useQuery" | 汎用的: "code", "implement" |
| 例 | プロジェクト固有のコード | 汎用サンプル |
| チェックリスト | 実行可能な項目 | 曖昧なガイダンス |
| 更新 | ADR変更時に再生成 | 古いスキルを保持 |

## ディレクトリ構造

```text
docs/adr/
├── README.md          # 自動生成インデックス
├── 0001-*.md         # 連番
└── 0002-*.md

.claude/skills/
├── adr-0001-*/       # 生成されたスキル
│   └── SKILL.md
└── adr-0002-*/
    └── SKILL.md
```

## 参照

- [MADR公式](https://adr.github.io/madr/)
- [@~/.claude/commands/adr.md](~/.claude/commands/adr.md) - /adrコマンド
- [@~/.claude/commands/adr/skill.md](~/.claude/commands/adr/skill.md) - /adr:skillクイックリファレンス
