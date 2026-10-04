---
name: onboard
description: 既存プロジェクトにTDD環境をセットアップする。フレームワーク検出、AGENTS.md + CLAUDE.md生成、docs/STATUS.md作成を行う。「TDDセットアップ」「onboard」「プロジェクト初期化」で起動。
allowed-tools: Read, Write, Bash, Grep, Glob
---

# TDD Onboard

## Progress Checklist

```
Onboard Progress:
- [ ] プロジェクト分析（フレームワーク/テストツール検出）
- [ ] プロジェクト状態判定（fresh/existing-no-tdd/dev-crew-installed）
- [ ] 検出結果をユーザーに確認
- [ ] docs/ 構造作成（cycles/, README.md, STATUS.md）
- [ ] CONSTITUTION.md 生成（型検出 + テンプレート）
- [ ] AGENTS.md 生成（cross-tool情報、最大5セクション）
- [ ] CLAUDE.md 生成（@AGENTS.md import + AI Behavior、既存あればマージ）
- [ ] 階層CLAUDE.md推奨（任意）
- [ ] .claude/ 構造生成（rules/, hooks/）
- [ ] Pre-commit Hook確認（推奨）
- [ ] 初期Cycle doc作成
- [ ] Generated Files Validation
- [ ] Next Steps 表示
```

## Workflow

### Step 1: プロジェクト分析

フレームワーク・ツール・**プロジェクト型**を検出。加えてプロジェクト状態を判定:
- `fresh` / `existing-no-tdd` / `dev-crew-installed`

状態判定ロジック、**symlink 検出**、検出コマンドは [reference.md](reference.md) 参照。

### Step 2: 検出結果確認

AskUserQuestion で確認:
- **プロジェクト目的**（fresh/existing-no-tdd）: 何を実現するプロジェクトか
- フレームワーク、パッケージマネージャ、プロジェクト状態、**プロジェクト型**

モード別確認項目は [reference.md](reference.md) 参照。

### Step 3: docs/ 構造作成

`mkdir -p docs/cycles` で作成。`docs/README.md` + `docs/STATUS.md` を生成。テンプレートは [reference.md](reference.md) 参照。

### Step 4: CONSTITUTION.md + AGENTS.md + CLAUDE.md 生成

CONSTITUTION.md（型検出結果に基づくテンプレート）→ AGENTS.md → CLAUDE.md の順で生成。

#### AGENTS.md (cross-tool、最大5セクション)

- `fresh` → テンプレートから生成
- `existing-no-tdd` / `dev-crew-installed` → 既存あればバックアップ後マージ
- Content: Overview, Quick Commands, TDD Workflow, Quality Standards, Project Structure(条件付き)

#### CLAUDE.md (Claude固有)

- 先頭に `@AGENTS.md` import を配置
- `fresh` → テンプレートから生成
- `existing-no-tdd` → AI Behavior Principlesをマージ（カスタム保持）
- `dev-crew-installed` → AI Behavior更新/リフレッシュ確認

テンプレートとマージ戦略は [reference.md](reference.md) を参照。
生成後に Deletion Test（各行を削除してもClaude が困らないなら削除）を実施。詳細は [reference.md](reference.md)。

### Step 5: 階層CLAUDE.md推奨（任意）

tests/, src/, docs/ に CLAUDE.md 配置を推奨（各30-50行）。
`@docs/xxx.md` 形式の import で外部ファイルを参照可能。詳細は [reference.md](reference.md)。

### Step 6: .claude/ 構造生成

不足分のみ作成、既存は更新確認。rules/: `rules/*.md` を全て `.claude/rules/` に identical mirror (drift は tests/test-rules-mirror.sh で検証)。hooks/: recommended。
Hook設定は `~/.claude/settings.json` へコピー+再起動を案内。詳細は [reference.md](reference.md)。

### Step 7: Pre-commit Hook確認（推奨）

hookなし → セットアップ推奨。詳細は [reference.md](reference.md) を参照。

### Step 8: 初期Cycle doc作成

`docs/cycles/YYYYMMDD_0000_project-setup.md` を作成。

### Step 9: Generated Files Validation

生成されたファイルの健全性チェック。FAILは警告のみ（修正は強制しない）。
詳細は [validation.md](validation.md) 参照。

### Step 10: 完了

セットアップ完了メッセージと**コミット案内**を表示。Codex連携の案内は [reference.md](reference.md#sync-skills-prompt) 参照。次: spec で開発開始。メンテナンス案内は [reference.md](reference.md) 参照。

## Reference: [reference.md](reference.md)
