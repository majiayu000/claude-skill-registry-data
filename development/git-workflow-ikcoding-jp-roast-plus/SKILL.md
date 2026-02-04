---
name: git-workflow
description: Git操作の自動化とベストプラクティス。コミットメッセージ生成、バージョン更新、変更内容の要約に使用。commit、version、changelog、git操作時に使用。
---

# Git Workflow スキル

Git操作を効率化し、プロジェクトのコミット履歴を整理するためのスキルです。
コンベンショナルコミット形式に準拠した日本語コミットメッセージの生成を支援します。

---

## このスキルを使用するタイミング

- コミットメッセージを作成するとき
- バージョン番号を更新するとき
- 変更履歴（changelog）を生成するとき
- Git操作全般の支援が必要なとき

---

## 1. コンベンショナルコミット形式

### 1.1 基本構造

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 1.2 タイプ一覧

| タイプ | 説明 | 例 |
|--------|------|-----|
| `feat` | 新機能追加 | feat(auth): ログイン機能を追加 |
| `fix` | バグ修正 | fix(timer): タイマーが停止しない問題を修正 |
| `docs` | ドキュメント変更 | docs(readme): セットアップ手順を追加 |
| `style` | コードスタイル変更（動作に影響なし） | style: コードフォーマットを統一 |
| `refactor` | リファクタリング | refactor(utils): ヘルパー関数を整理 |
| `test` | テスト追加・修正 | test(api): ユーザーAPIのテストを追加 |
| `chore` | ビルド・設定変更 | chore(deps): 依存関係を更新 |
| `perf` | パフォーマンス改善 | perf(render): 描画速度を最適化 |
| `ci` | CI/CD設定変更 | ci(github): デプロイワークフローを追加 |

### 1.3 スコープ例

プロジェクトに応じて適切なスコープを使用：

- コンポーネント名: `header`, `sidebar`, `modal`
- 機能名: `auth`, `timer`, `settings`
- レイヤー名: `api`, `ui`, `db`

---

## 2. コミットメッセージ生成ワークフロー

### 2.1 変更内容の確認

```bash
# ステージングされた変更を確認
git diff --staged --stat

# 詳細な差分を確認
git diff --staged
```

### 2.2 コミットメッセージの決定

1. **変更の種類を特定**
   - 新機能？ → `feat`
   - バグ修正？ → `fix`
   - ドキュメント？ → `docs`

2. **スコープを特定**
   - どのコンポーネント/機能に影響？

3. **簡潔な説明を作成**
   - 50文字以内
   - 命令形で記述（「追加する」ではなく「追加」）
   - 日本語で記述

### 2.3 コミット実行

```bash
git commit -m "feat(timer): 抽出タイマー機能を追加"
```

---

## 3. バージョン更新

### 3.1 セマンティックバージョニング

`MAJOR.MINOR.PATCH` 形式：

- **MAJOR**: 後方互換性のない変更
- **MINOR**: 後方互換性のある新機能
- **PATCH**: 後方互換性のあるバグ修正

### 3.2 バージョン更新手順

#### Next.js (package.json)

```json
{
  "version": "0.5.16"
}
```

#### Flutter (pubspec.yaml)

```yaml
version: 1.3.1+42
```

形式: `MAJOR.MINOR.PATCH+BUILD_NUMBER`

---

## 4. 変更履歴（Changelog）生成

### 4.1 形式

```markdown
## [0.5.16] - 2026-01-15

### 追加
- 抽出タイマー機能を追加

### 修正
- タイマーが停止しない問題を修正

### 変更
- UIデザインを更新
```

### 4.2 カテゴリ

- **追加** (Added): 新機能
- **修正** (Fixed): バグ修正
- **変更** (Changed): 既存機能の変更
- **削除** (Removed): 機能削除
- **非推奨** (Deprecated): 将来削除予定
- **セキュリティ** (Security): 脆弱性対応

---

## 5. よく使うGitコマンド

### 5.1 基本操作

```bash
# 状態確認
git status

# 変更を全てステージング
git add .

# 特定ファイルをステージング
git add path/to/file

# コミット
git commit -m "type(scope): message"

# プッシュ
git push origin <branch>
```

### 5.2 ブランチ操作

```bash
# ブランチ作成＆切り替え
git checkout -b feature/new-feature

# ブランチ一覧
git branch -a

# ブランチ切り替え
git checkout main

# ブランチ削除
git branch -d feature/old-feature
```

### 5.3 履歴確認

```bash
# コミット履歴（簡潔）
git log --oneline -10

# コミット履歴（詳細）
git log -n 5

# ファイルの変更履歴
git log --oneline -- path/to/file
```

---

## AI アシスタント指示

このスキルが有効な場合：

1. **変更内容を確認**: `git status` と `git diff --staged` で変更を把握
2. **適切なタイプを選択**: 変更の性質に基づいてコミットタイプを決定
3. **日本語でメッセージ作成**: 50文字以内で簡潔に
4. **バージョン更新が必要か確認**: リリース時はバージョン番号を更新

**必ず守ること**:
- コミットメッセージは日本語で作成
- コンベンショナルコミット形式に準拠
- 1コミット = 1つの論理的な変更

**避けること**:
- 複数の無関係な変更を1コミットにまとめない
- 曖昧なメッセージ（「修正」「更新」のみ）は避ける
