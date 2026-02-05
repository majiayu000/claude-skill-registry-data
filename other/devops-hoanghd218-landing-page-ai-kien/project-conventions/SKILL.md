---
name: project-conventions
description: Polibaseのプロジェクト規約とベストプラクティスを説明します。Pre-commit hooks遵守、CI/CD運用、中間ファイル管理、知識蓄積層の活用など、開発時に守るべきルールとガイドラインをカバーします。
---

# Project Conventions（プロジェクト規約）

## 目的
Polibaseプロジェクトの開発規約、ベストプラクティス、守るべきルールを理解し、一貫性のある高品質な開発を実現します。

## いつアクティベートするか
このスキルは以下の場合に自動的にアクティベートされます：
- コミット作成時
- PR（Pull Request）作成時
- CI/CD失敗時
- ユーザーが「コミット」「pre-commit」「フック」「規約」「ルール」と言った時
- 中間ファイルやドキュメントを作成する時

## 重要な規約

### 1. Pre-commit Hooks遵守（最重要）

**絶対に `--no-verify` オプションを使用してpre-commit hooksを回避しないでください**

#### ルール
- Pre-commit hooksがfailした場合は、必ずエラーを修正してからコミットする
- `ruff`、`pyright`、`prettier`等のチェックが通らない場合は、コードを修正する
- 一時的な回避が必要な場合は、設定ファイル（`pyproject.toml`等）で適切に除外設定を追加する
- **`git commit --no-verify` は使用禁止**

#### 理由
- コード品質の一貫性を保つ
- チーム全体で同じ基準を維持
- バグやスタイル違反の早期発見
- CI/CDでの失敗を防ぐ

#### 例外処理
```bash
# ❌ 悪い例 - hooksを回避
git commit --no-verify -m "quick fix"

# ✅ 良い例 - 設定ファイルで除外
# pyproject.toml に追加
[tool.ruff]
exclude = ["legacy_code.py"]

# その後コミット
git add .
git commit -m "Add feature with proper exclusion"
```

### 2. CI/CDでのテストスキップ

テストやチェックを `continue-on-error: true` でスキップする場合は、**必ず対応するIssueを作成すること**

#### 必須事項
- スキップした理由を明確に記載
- 修正方法を具体的に記述
- 関連するPRやIssueをリンク
- 優先度を適切に設定（通常は高優先度）

#### Issueテンプレート
```markdown
## 問題
CI/CDで [テスト名] をスキップしています

## スキップ理由
[具体的な理由]

## 修正方法
1. [ステップ1]
2. [ステップ2]
3. [ステップ3]

## 関連
- PR: #123
- 関連Issue: #456

## 優先度
高
```

### 3. 中間ファイルの配置

**すべての一時ファイルや中間ファイルは `tmp/` ディレクトリに配置すること**

#### 対象ファイル
- Markdown形式の計画書、サマリー
- 一時的な分析結果
- 実験用スクリプト
- デバッグ用ログ
- 生成された一時データ

#### ルール
```bash
# ✅ 良い例
tmp/
├── planning/
│   └── 2025-01-15_feature_planning.md
├── analysis/
│   └── performance_analysis_2025-01-15.md
└── experiments/
    └── test_script.py

# ❌ 悪い例
project_root/
├── planning.md  # ルートに配置
├── analysis.txt # ルートに配置
└── test.py      # ルートに配置
```

#### 理由
- `tmp/` は `.gitignore` に含まれているため、誤コミットを防ぐ
- リポジトリを clean に保つ
- チーム全体で一貫性を維持

### 4. 知識蓄積層の活用（`_docs/`）

開発過程での思考や判断を適切に記録してください

#### いつ使うか
- **技術的な選択で迷った時** → `_docs/thinking/` に設計判断を記録
- **新機能を実装した時** → `_docs/features/` に実装の目的と完了条件を記録
- **ファイルやディレクトリを削除した時** → `_docs/deleted/` に削除理由と影響を記録

#### 記録のタイミング
判断した直後（記憶が鮮明なうちに）

#### 記録内容のポイント
- 短く簡潔に（長文は避ける）
- 箇条書きを活用
- 将来のClaude（または開発者）が理解できる言葉で書く
- 客観的な事実と主観的な判断を区別する

#### ファイル命名規則
`YYYY-MM-DD_簡潔な説明.md`

例: `2025-01-15_api_design_decision.md`

#### ディレクトリ構造
```
_docs/
├── thinking/       # 技術的判断の記録
├── features/       # 実装した機能の記録
└── deleted/        # 削除したファイル・ディレクトリの記録
```

#### テンプレート
各ディレクトリの `README.md` を参照

#### 注意
- この `_docs/` ディレクトリは `.gitignore` に含まれており、Gitリポジトリには含まれません
- チーム全体で共有すべき情報は `docs/` ディレクトリに記載してください

## クイックチェックリスト

### コミット前
- [ ] **Pre-commit hooksが通るか確認**
- [ ] **`--no-verify` を使用していないか**
- [ ] **コードフォーマットが適用されているか** (ruff, prettier)
- [ ] **型チェックが通るか** (pyright)
- [ ] **テストが通るか** (pytest)

### PR作成前
- [ ] **すべてのCI/CDチェックが通るか**
- [ ] **スキップしたテストにIssueを作成したか**
- [ ] **中間ファイルが `tmp/` に配置されているか**
- [ ] **重要な判断を `_docs/` に記録したか**

### 機能実装後
- [ ] **実装の目的を `_docs/features/` に記録したか**
- [ ] **重要な技術判断を `_docs/thinking/` に記録したか**
- [ ] **削除したコードの理由を `_docs/deleted/` に記録したか**

## 詳細リファレンス

詳細なガイドライン、例、トラブルシューティングは [reference.md](reference.md) を参照してください。

## 関連スキル

- [test-writer](../test-writer/): テスト作成ガイド
- [migration-helper](../migration-helper/): データベース移行ガイド
- [clean-architecture-checker](../clean-architecture-checker/): アーキテクチャガイド
