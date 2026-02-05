---
name: plan-parallel-dev
description: 複数開発者での並列開発計画書を作成するスキル。git worktree を活用したブランチ戦略、タスクの依存関係分析、クリティカルパス計算、開発者ロール割り当て、タイムライン作成を行う。「並列開発計画を作って」「複数人で同時開発したい」「worktree で分担したい」「開発を最大限並列化したい」などのリクエスト時に使用。また、「〇〇を並列で修正して」「worktree で△△をやって」「並列タスクを追加」などのリクエストで、オンデマンドの並列タスクを即座に開始できる。
---

# Parallel Development Planning

機能開発を複数開発者で最大限並列化するための実装計画書を作成する。
また、完成後のプロジェクトに対するオンデマンドの並列タスク（バグ修正・機能追加）もサポートする。

## 利用モード

このスキルには2つのモードがある:

### モード A: 初期並列開発（計画書作成モード）

プロジェクト初期化直後（`uv init` や `create-react-app` 直後など）で、これから複数機能を並列開発する場合に使用。

**トリガーフレーズ**:
- 「並列開発計画を作って」
- 「複数人で同時開発したい」
- 「worktree で分担したい」
- 「開発を最大限並列化したい」

**ワークフロー**: 9段階のワークフロー（後述）で計画書を作成し、複数タスクを一斉に開始。

### モード B: メンテナンス並列開発（クイックタスクモード）

すでに機能が実装されているプロジェクトへのバグ修正・機能追加で使用。計画書なしで即座に作業を開始。

**トリガーフレーズ**:
- 「〇〇を並列で修正して」
- 「〇〇を並列で対応して」
- 「worktree で△△をやって」
- 「並列タスクを追加: 〇〇」
- 「これを worktree でやって: 〇〇」

**ワークフロー**: 詳細は「Quick Task Workflow（クイックタスク）」セクション参照。

### モード選択の目安

| 状況 | 推奨モード |
|------|-----------|
| プロジェクト初期化直後、複数機能を並列開発 | A |
| 既存プロジェクトへの単発バグ修正 | B（単一タスク） |
| 既存プロジェクトへの中規模機能追加 | B（複数タスク + マージ担当を設ける） |

---

## Workflow（モード A: 初期並列開発）

```
1. 要件の把握
   └─→ 開発対象の機能一覧を収集
   └─→ 技術スタック確認 (BE/FE/インフラ等)

2. タスク分解
   └─→ 各機能を独立したタスクに分割
   └─→ 粒度: 以下のいずれか小さい方
       ├─→ 人間換算 0.5〜2日程度
       ├─→ 変更ファイル 20ファイル以内
       └─→ 単独テスト可能な機能単位
   └─→ ⚠️ UI仕様は人間の確認を取ってから確定（後述）

3. 依存関係分析
   └─→ タスク間のブロッキング関係を特定
   └─→ クリティカルパスを計算

4. 並列度の決定
   └─→ 必要な claude 数を算出
   └─→ 待機時間を最小化する割り当て

5. ブランチ戦略
   └─→ 統合ブランチの設計
   └─→ 機能ブランチの命名規則
   └─→ マージ順序の決定

6. タイムライン作成
   └─→ Gantt風の並列スケジュール

7. 計画書・指示書の作成
   └─→ 計画書の内容をユーザーに伝える（実行順序、並列度、各タスクの内容を表形式で提示）
   └─→ .parallel-dev/ にファイルを作成
       ├─→ PLAN.md (計画書)
       ├─→ README.md (全体概要・進捗管理)
       ├─→ merge-coordinator.md (マージ担当用)
       ├─→ tasks/*.md (各タスク用)
       ├─→ signals/ (完了通知用ディレクトリ)
       └─→ issues/ (問題報告用ディレクトリ)

8. 環境セットアップ
   └─→ 統合ブランチを作成してリモートにプッシュ
   └─→ 各タスク用の worktree を作成
   └─→ 各 worktree で依存関係インストール
   └─→ 各 worktree で .env コピー

9. マージ担当の Claude を tmux split-window で起動
   └─→ tmux split-window で新しいペインを作成し claude を起動
   └─→ マージ担当の初期指示を渡す
```

## Quick Task Workflow（モード B: クイックタスク）

既存プロジェクトに対するバグ修正や機能追加を、計画書なしで即座に開始するモード。

**特徴**:
- 計画書不要で即座に開始
- セッションファイル（`.parallel-dev/quick-session-{timestamp}.md`）で複数セッション並行可能
- main に直接マージ

→ **詳細は [references/quick-mode-guide.md](references/quick-mode-guide.md) を参照**

---

## Terminology（用語定義）

混乱を避けるため、以下の用語を統一する:

| 用語              | 説明                               | 例                                     |
| ----------------- | ---------------------------------- | -------------------------------------- |
| **タスク名**      | ブランチ名と同一。作業単位の識別子 | `skill-files-api`, `recommendation-ui` |
| **担当者/ロール** | 作業者の識別子。技術領域+番号      | `BE-1`, `FE-1`, `INFRA-1`              |
| **統合ブランチ**  | 全タスクをマージする先のブランチ   | `feature/multi-file-skills`            |

**重要**: 完了報告や状態管理では**タスク名（ブランチ名）**を使う。担当者名だけでは、複数タスクを担当している場合に特定できない。

## Task Decomposition Rules

タスク分割の原則:

1. **単一責任**: 1 タスク = 1 機能/1 コンポーネント
2. **適切な粒度**: 以下のいずれか小さい方
   - 人間換算 0.5〜2日程度
   - 変更ファイル 20ファイル以内
   - 単独テスト可能な機能単位
3. **明確な成果物**: 各タスクに API/コンポーネント/ファイル等の具体的成果物
4. **テスト可能**: 独立してテスト・レビュー可能な単位
5. **コンフリクト最小化**: 編集ファイルの重複を最小化し、共通ファイル（ルーティング、型定義等）の変更は1タスクに集約

ブランチ命名:

```
feature/recommendation-api  # 機能名ベース
feature/notification-api
feature/project-card-enhance
```

ロール（担当者）命名:

```
BE-1, BE-2, ...    # バックエンド担当
FE-1, FE-2, ...    # フロントエンド担当
INFRA-1, ...       # インフラ担当
```

## Dependency Analysis

依存関係の種類:

| 依存タイプ   | 記号 | 説明           |
| ------------ | ---- | -------------- |
| ブロッキング | `→`  | 完了必須       |
| 並行可能     | `//` | 独立して進行可 |
| 統合待ち     | `↓`  | マージ後に開始 |

クリティカルパス計算:

```
最長パス = max(各経路の合計工数)
最適人数 = ceil(総工数 / クリティカルパス)
```

依存関係マトリクスの作成:

```
         BE-01  BE-02  FE-01  FE-02
BE-01      -      //     ↓      //
BE-02     //       -     //      ↓
FE-01     待      //      -      //
FE-02     //      待     //       -
```

## Developer Role Assignment

ロール定義テンプレート:

| ロール | 担当ブランチ    | 必要スキル        |
| ------ | --------------- | ----------------- |
| BE-1   | feature/xxx-api | Python, FastAPI   |
| FE-1   | feature/xxx-ui  | React, TypeScript |

待機時間最小化の原則:

1. 依存元タスクの担当者に依存先も割り当て
2. 独立タスクで待機時間を埋める
3. レビュー・支援で空き時間を活用

## Branch Strategy with Worktree

git worktree を使った並列開発の基本:

```
main
└── feature/integration (統合ブランチ)
    ├── feature/xxx-api     → worktree/xxx-api/
    ├── feature/yyy-api     → worktree/yyy-api/
    └── feature/xxx-ui      → worktree/xxx-ui/
```

→ **詳細は [references/worktree-guide.md](references/worktree-guide.md) を参照**

## Agent Instruction Files

claude による並列開発では、各 claude への指示書を `.parallel-dev/` に配置する。

**ディレクトリ構成**:

| ディレクトリ/ファイル | 用途 |
|----------------------|------|
| `.parallel-dev/` | 並列開発管理（git管理） |
| `.parallel-dev/PLAN.md` | 計画書 |
| `.parallel-dev/merge-coordinator.md` | マージ担当用 |
| `.parallel-dev/tasks/*.md` | 各タスク用指示書 |
| `.parallel-dev-signals/` | 完了通知（.gitignore） |
| `.parallel-dev-issues/` | 問題報告（.gitignore） |

**テンプレート**:
- [references/templates/parallel-dev-readme.md](references/templates/parallel-dev-readme.md)
- [references/templates/merge-coordinator.md](references/templates/merge-coordinator.md)
- [references/templates/task-instruction.md](references/templates/task-instruction.md)

## Task Completion Flow

**役割分担**:
- **作業用 claude**: コード実装 → `.done` ファイル作成（コミットしない）
- **マージ担当**: コミット → テスト → マージ → プッシュ

**設計思想**: 作業用 claude はコードを書くことに集中。マージ順序の管理はマージ担当のみが把握。

→ **詳細は [references/worktree-guide.md](references/worktree-guide.md) を参照**

## Rules（全 claude 共通）

### 作業用 claude のルール

- **コミットしない**: コードを書くだけ。コミットはマージ担当が行う
- **プッシュしない**: リモートへのプッシュもマージ担当が行う
- **.done ファイルで完了報告**: 実装内容と変更ファイルを記載
- **UI 仕様は人間の承認必須**: issues/ に確認依頼を出し、承認を得てから実装

### マージ担当のルール

- **`tmux split-window` で作業用 claude を起動**（`new-window` や Task ツールは使用しない）
- **claude 起動時は必ず初期指示を引数で渡す**:
  ```bash
  tmux split-window -h "cd worktree/{task-name} && PROJECT_ROOT=$PROJECT_ROOT claude '../../.parallel-dev/tasks/{task-name}.md を読んで実装してください。完了したら .done ファイルを作成してください。'"
  tmux select-pane -T "{task-name}"
  ```
- **マージ成功後は作業用 claude を終了**: `tmux send-keys -t "{task-name}" C-c C-c`
- **`--no-ff` で常にマージ**
- **コンフリクト対応**: マージ担当が解決（作業用 claude に依頼しない）

### 依存関係ルール

- 依存タスクが**統合ブランチにマージされるまで**、依存元タスクは起動しない

→ **詳細は [references/worktree-guide.md](references/worktree-guide.md) を参照**

## Additional Guides（詳細ガイド）

- [references/worktree-guide.md](references/worktree-guide.md) - worktree 運用・作業フロー・ルール詳細
- [references/quick-mode-guide.md](references/quick-mode-guide.md) - クイックタスクモード運用
- [references/testing-guide.md](references/testing-guide.md) - テスト方針（本番同等テスト、E2E目視チェック）
- [references/ui-approval-guide.md](references/ui-approval-guide.md) - UI仕様の人間確認フロー
- [references/advanced-features.md](references/advanced-features.md) - Phase分離、タイムライン可視化、計画書テンプレート

## Utility Scripts（ユーティリティスクリプト）

| スクリプト | 用途 |
|-----------|------|
| [setup-quick-task.sh](references/scripts/setup-quick-task.sh) | クイックタスクのセットアップ |
| [watch-signals.sh](references/scripts/watch-signals.sh) | .done/.issues 監視 |
| [status.sh](references/scripts/status.sh) | 全タスク状態一覧 |
| [cleanup-worktrees.sh](references/scripts/cleanup-worktrees.sh) | 完了タスクのクリーンアップ |
