---
name: work-log
description: Claude Codeで作業をする際に、docsディレクトリ内にmarkdown形式で作業ログを記録します。作業開始時、重要な変更時、作業完了時に自動的に使用されます。
---

# Work Log

Claude Codeでの作業内容をmarkdown形式で記録するSkillです。

## 目的

- 作業履歴の可視化
- チーム内での作業内容の共有
- 変更内容の追跡と振り返り
- ドキュメントとしての作業記録の蓄積

## Instructions

### 1. 作業開始時

新しいタスクや機能の開発を開始する際：

1. `docs/work-logs/`ディレクトリが存在するか確認
2. 存在しない場合は作成: `mkdir -p docs/work-logs`
3. 日付ベースのログファイルを作成: `docs/work-logs/YYYY-MM-DD-<task-name>.md`
4. 以下のテンプレートで作業ログを初期化:

```markdown
# [タスク名]

**作業日**: YYYY-MM-DD
**担当**: Claude Code
**ステータス**: 進行中

## 目的

[このタスクの目的や背景を記述]

## 作業内容

### [時刻] - 作業開始

- [作業内容1]
- [作業内容2]

## 変更ファイル

- `path/to/file1.ts` - [変更内容]
- `path/to/file2.tsx` - [変更内容]

## 課題・Todo

- [ ] [残タスク1]
- [ ] [残タスク2]

## 備考

[その他メモや注意事項]
```

### 2. 作業中の更新

重要な変更や進捗があった際：

1. 既存のログファイルをReadツールで読み込み
2. 「## 作業内容」セクションに新しいエントリを追加:

```markdown
### [HH:MM] - [作業内容の要約]

- 実施した作業の詳細
- 変更したファイルとその理由
- 発生した問題と解決方法
```

3. 「## 変更ファイル」セクションを更新
4. 必要に応じて「## 課題・Todo」を更新

### 3. 作業完了時

タスク完了時：

1. ステータスを「完了」に更新
2. 最終的な変更内容をサマリーとして追加:

```markdown
## 完了サマリー

### 実装内容

- [実装した機能1]
- [実装した機能2]

### 変更ファイル一覧

- `file1.ts`
- `file2.tsx`

### テスト結果

- [テスト実行結果]
- [カバレッジ情報（あれば）]

### 次のステップ

- [今後の改善点や残タスク]
```

## ファイル命名規則

```
docs/work-logs/YYYY-MM-DD-<task-name>.md
```

**例**:
- `docs/work-logs/2025-12-25-storybook-setup.md`
- `docs/work-logs/2025-12-25-add-dashboard-header.md`
- `docs/work-logs/2025-12-26-fix-auth-bug.md`

## 使用するツール

- **Write**: 新しいログファイルの作成
- **Read**: 既存ログファイルの読み込み
- **Edit**: ログファイルの更新
- **Glob**: 既存のログファイルの検索

## 自動起動の条件

以下の場合に自動的にこのSkillを使用します：

1. ユーザーが新しいタスクや機能の実装を依頼した時
2. 重要な変更（複数ファイルの編集、アーキテクチャ変更など）を行った時
3. タスクが完了した時
4. ユーザーが明示的に作業ログの記録を依頼した時

## IMPORTANT: 自動実行ポリシー

このSkillは以下の条件を満たした際、**ユーザーへの確認なし**に**即座に自動実行**してください：

### 1. 作業開始時（タスク開始直後）
- ✅ ユーザーが新しいタスク・機能の実装を依頼した直後
- ✅ 最初のツール（Read/Glob/Grep等）を実行する**前に**作業ログを作成
- ✅ 作業の目的と計画を記録
- ✅ **TodoWriteで「作業ログ更新」todoを自動追加**

### 2. 作業完了時（タスク完了直後）
- ✅ すべてのファイル編集が完了した時点
- ✅ ユーザーに「完了しました」と報告する**前に**作業ログを更新
- ✅ 完了サマリーを記録
- ✅ **TodoWriteで「作業ログ更新」todoをcompletedに更新**

### 3. 重要な変更時（複数ファイル編集時）
- ✅ 2つ以上のファイルを編集した場合
- ✅ アーキテクチャ変更を行った場合
- ✅ 新しいコンポーネント・関数を作成した場合

**禁止事項:**
- ❌ 「作業ログを記録しますか？」とユーザーに確認してはいけません
- ❌ ユーザーの明示的な指示を待ってはいけません
- ❌ 作業開始時は計画を立てた直後、作業完了時はすべての編集完了直後に即座に実行してください

**実行フロー例（TodoWrite統合版）:**
1. ユーザー: 「WorkoutChartのロジックをカスタムフックに切り出して」
2. あなた: **即座に**work-logスキルを実行（作業開始の記録）
3. あなた: **即座に**TodoWriteで「WorkoutChartリファクタリング」と「作業ログ更新」を追加
4. あなた: コードのリファクタリング実施
5. あなた: **即座に**TodoWriteで「作業ログ更新」をin_progressに変更
6. あなた: **即座に**work-logスキルを実行（完了サマリー追加）
7. あなた: **即座に**TodoWriteで「作業ログ更新」をcompletedに変更
8. あなた: 「リファクタリングが完了しました」とユーザーに報告

## TodoWriteとの統合

### タスク開始時の自動Todo追加

作業ログを作成した直後に、TodoWriteツールで以下のtodoを追加してください：

```typescript
{
  "todos": [
    {
      "content": "[実タスク内容]",  // 例: "WorkoutFormリファクタリング"
      "status": "in_progress",
      "activeForm": "[実タスク内容]中"  // 例: "WorkoutFormリファクタリング中"
    },
    {
      "content": "作業ログを完了時に更新",
      "status": "pending",
      "activeForm": "作業ログを更新中"
    }
  ]
}
```

### タスク完了時のTodo更新

作業ログを更新する前に、以下の手順でTodoWriteを使用してください：

1. 「作業ログを完了時に更新」todoを`in_progress`に変更
2. work-logスキルを実行（完了サマリー追加）
3. 「作業ログを完了時に更新」todoを`completed`に変更

**実装例:**

```typescript
// 1. タスク開始時
TodoWrite({
  todos: [
    { content: "WorkoutFormリファクタリング", status: "in_progress", activeForm: "WorkoutFormリファクタリング中" },
    { content: "作業ログを完了時に更新", status: "pending", activeForm: "作業ログを更新中" }
  ]
});

// 2. タスク完了時
TodoWrite({
  todos: [
    { content: "WorkoutFormリファクタリング", status: "completed", activeForm: "WorkoutFormリファクタリング中" },
    { content: "作業ログを完了時に更新", status: "in_progress", activeForm: "作業ログを更新中" }
  ]
});

// 3. work-logスキル実行後
TodoWrite({
  todos: [
    { content: "WorkoutFormリファクタリング", status: "completed", activeForm: "WorkoutFormリファクタリング中" },
    { content: "作業ログを完了時に更新", status: "completed", activeForm: "作業ログを更新中" }
  ]
});
```

### 利点

- **視覚的リマインダー**: ユーザーが進捗を視覚的に確認できる
- **忘れ防止**: 作業ログの更新を忘れることがなくなる
- **透明性**: 作業の各ステップがtodoリストで明確になる

## 注意事項

- **簡潔に**: 重要な情報のみを記録し、冗長な説明は避ける
- **事実ベース**: 実際に行った作業のみを記録
- **タイムスタンプ**: 各エントリに時刻を付与して時系列を明確に
- **リンク**: ファイルパスはmarkdownリンク形式で記述（例: `[file.ts](../src/file.ts)`）
- **ユーザー確認不要**: `docs/`ディレクトリ以下の作業ログファイルの作成・編集は、ユーザーへの確認なしに自動的に行ってよい。作業ログは記録目的のため、ユーザーの承認を待たずに即座に追記・更新すること。

## Examples

### Example 1: Storybook導入の作業ログ

```markdown
# Storybook v10 導入

**作業日**: 2025-12-25
**担当**: Claude Code
**ステータス**: 進行中

## 目的

プロジェクトにStorybook v10を導入し、UIコンポーネントの開発効率を向上させる。

## 作業内容

### 10:30 - 作業開始・計画立案

- プロジェクト構成の確認
- Storybook v10の導入計画を作成
- 既存のMaterial-UI設定を確認

### 11:00 - Storybookインストール

- `npx storybook@latest init`を実行
- 必要なパッケージのインストール完了
- `.storybook/`ディレクトリ作成

### 11:30 - 設定ファイルの作成

- `.storybook/main.ts`を作成
- Next.js 15 App Router対応設定を追加
- TypeScriptパスエイリアス設定

## 変更ファイル

- `.storybook/main.ts` - Storybook設定ファイル新規作成
- `.storybook/preview.tsx` - Material-UIテーマ統合
- `package.json` - 依存パッケージ追加

## 課題・Todo

- [x] Storybookインストール
- [x] 基本設定ファイル作成
- [ ] サンプルストーリー作成
- [ ] テーマ設定の統合

## 備考

- Material-UI v6とEmotion使用
- Next.js 15 App Router対応が必要
```

### Example 2: バグ修正の作業ログ

```markdown
# 認証バグ修正

**作業日**: 2025-12-25
**担当**: Claude Code
**ステータス**: 完了

## 目的

ログイン後にセッションが正しく保存されない問題を修正する。

## 作業内容

### 14:00 - 問題調査

- `src/lib/auth/auth.ts`を確認
- セッション設定の不備を発見
- NextAuth設定を確認

### 14:30 - 修正実装

- セッションコールバックを修正
- JWT設定を追加
- middleware.tsのリダイレクト処理を改善

### 15:00 - テスト実行

- 認証フローのテストを実行
- すべてのテストがパス

## 完了サマリー

### 実装内容

- セッションコールバックの修正
- JWT署名アルゴリズムの明示的指定
- middleware.tsのエッジケース対応

### 変更ファイル一覧

- [src/lib/auth/auth.ts](../src/lib/auth/auth.ts)
- [src/middleware.ts](../src/middleware.ts)

### テスト結果

- 全テストパス (12/12)
- 認証フローの手動テスト完了

### 次のステップ

- セッション有効期限の設定を見直し
- エラーハンドリングの改善
```

## Related Files

このSkillを効果的に使用するための関連ファイル：

- `docs/work-logs/README.md` - 作業ログの概要とインデックス
- `.gitignore` - 必要に応じてログファイルの除外設定
