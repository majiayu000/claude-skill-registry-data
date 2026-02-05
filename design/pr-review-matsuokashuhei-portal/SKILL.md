---
name: pr-review
description: PRをレビューする。変更されたコードに対してmacOS/Swift/SwiftUI固有の問題を検出し、日本語でフィードバックを提供する。
allowed-tools: Read, Glob, Grep, Bash(git diff:*, git log:*, git show:*, git status, gh pr:*, gh api:*)
---

# PR Review

## 概要

PRの変更内容をmacOS/Swift/SwiftUI開発の観点からレビューするSkill。
変更されたファイルのみを対象に、コード品質、パフォーマンス、セキュリティの問題を検出する。

## 前提条件

- GitHub CLIがインストール・認証済み
- gitリポジトリ内で実行
- PRが作成済み、または変更がコミット済み

## レビュー実行手順

### 1. PR情報の取得

```bash
# 現在のブランチのPR情報を取得
gh pr view --json number,title,body,baseRefName,headRefName,files

# または指定したPR番号で取得
gh pr view <PR番号> --json number,title,body,baseRefName,headRefName,files
```

### 2. 変更ファイルの特定

```bash
# ベースブランチとの差分を取得
git diff main...HEAD --name-only

# 詳細な差分統計
git diff main...HEAD --stat

# 特定ファイルの差分（行番号付き）
git diff main...HEAD -- <filepath>
```

### 3. Review Scopeの解析

PR本文から以下を抽出:
- 「このPRでレビューしてほしいこと」
- 「このPRでレビュー不要なこと」

レビュー不要として明示された項目は指摘しない。

### 4. 変更コードのレビュー

各変更ファイルに対して以下の観点でレビュー:

#### メモリ管理
- クロージャ内の`self`キャプチャ（`[weak self]`の使用）
- delegate/datasourceの弱参照
- NotificationCenter、KVO、タイマーの解除

```swift
// NG: 循環参照
timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
    self.updateUI() // selfが強参照される
}

// OK: weakキャプチャ
timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
    self?.updateUI()
}
```

#### スレッド安全性
- UI更新がメインスレッドで実行されているか
- `@MainActor`の適切な使用
- 共有状態への同時アクセス保護

```swift
// NG: バックグラウンドスレッドからUI更新
URLSession.shared.dataTask(with: url) { data, _, _ in
    self.label.stringValue = "Done" // クラッシュの可能性
}

// OK: メインスレッドにディスパッチ
URLSession.shared.dataTask(with: url) { data, _, _ in
    DispatchQueue.main.async {
        self.label.stringValue = "Done"
    }
}
```

#### Accessibility
- `accessibilityLabel`の設定
- `accessibilityIdentifier`（テスト用）
- 適切な`accessibilityRole`

```swift
// NG: アクセシビリティ情報なし
Image(systemName: "gear")

// OK: 適切なアクセシビリティ情報
Image(systemName: "gear")
    .accessibilityLabel("Settings")
    .accessibilityHint("Opens application settings")
```

#### エラーハンドリング
- 強制アンラップ（`!`）の回避
- `try!`の使用回避
- 適切なエラー伝播

```swift
// NG: 強制アンラップ
let data = try! Data(contentsOf: url)

// OK: エラーハンドリング
do {
    let data = try Data(contentsOf: url)
    process(data)
} catch {
    handleError(error)
}
```

#### パフォーマンス
- 遅延初期化の活用
- ビュー再描画の最適化
- 非同期処理の適切な使用

```swift
// NG: 毎回計算
var body: some View {
    let results = expensiveCalculation() // ビューが更新されるたびに実行
    List(results) { ... }
}

// OK: 計算結果をキャッシュ
@State private var results: [Item] = []

var body: some View {
    List(results) { ... }
        .onAppear { results = expensiveCalculation() }
}
```

#### セキュリティ
- 機密情報のハードコード
- ユーザー入力のバリデーション

```swift
// NG: APIキーのハードコード
let apiKey = "sk-1234567890"

// OK: 環境変数または安全な保存先から取得
let apiKey = ProcessInfo.processInfo.environment["API_KEY"]
```

#### Swift/SwiftUI ベストプラクティス
- 命名規則の遵守
- プロトコル指向設計
- 適切な型アノテーション

#### AppKit統合
- NSViewRepresentableの正しい実装
- ライフサイクルメソッドの適切な使用

### 5. PR固有のチェック

#### メタデータ
- [ ] タイトルにIssue番号が含まれているか
- [ ] Summaryが変更内容を適切に説明しているか
- [ ] Test planが存在するか
- [ ] `Closes #XX`でIssueがリンクされているか

#### コミット品質
- [ ] コミットメッセージにIssue番号が含まれているか
- [ ] 論理的な単位でコミットが分割されているか

#### テスト
- [ ] 新機能/修正に対応するテストが追加されているか
- [ ] 既存テストが破壊されていないか

#### ドキュメント
- [ ] CLAUDE.mdの更新が必要か
- [ ] 新しいパブリックAPIにドキュメントコメントがあるか

## 出力フォーマット

```markdown
## PRレビュー結果: #<PR番号> <PRタイトル>

### メタデータチェック
| 項目 | 状態 | 詳細 |
|------|------|------|
| Issue番号 | OK/NG | #XX |
| Summary | OK/NG | - |
| Test plan | OK/NG | - |
| Closes | OK/NG | #XX |

### コードレビュー

#### Critical（修正必須）
- [ ] **[問題タイプ]**: 説明
  - 場所: `file.swift:123`
  - 変更: `+追加されたコード`
  - 問題: 具体的な説明
  - 改善案:
    ```swift
    // 修正後のコード
    ```

#### Warning（推奨修正）
- [ ] **[問題タイプ]**: 説明
  - 場所: `file.swift:456`
  - 改善案: 具体的な修正方法

#### Info（検討推奨）
- 観察点や改善の余地がある箇所

### スキップした項目
以下はReview scopeで「レビュー不要」として指定:
- Issue #XX で対応予定: 説明

### 良い点
- 適切に実装されている箇所の評価

### 推奨アクション
1. [ ] Critical項目を修正
2. [ ] Warning項目を検討
3. [ ] テストを追加/更新
```

## GitHubへのインラインコメント投稿

レビュー結果をGitHubのPRに直接インラインコメントとして投稿できる。

### 1. コミットSHAの取得

```bash
# PRのheadコミットSHAを取得
gh pr view <PR番号> --json headRefOid --jq '.headRefOid'
```

### 2. インラインコメントの投稿

```bash
gh api repos/{owner}/{repo}/pulls/{PR番号}/comments \
  -X POST \
  -f body="コメント内容" \
  -f commit_id="<コミットSHA>" \
  -f path="<ファイルパス>" \
  -F line=<行番号> \
  -f side="RIGHT"
```

#### パラメータ説明

| パラメータ | 説明 |
|-----------|------|
| `body` | コメント本文（Markdown対応） |
| `commit_id` | PRのheadコミットSHA |
| `path` | コメント対象のファイルパス（リポジトリルートからの相対パス） |
| `line` | コメント対象の行番号（diffの新しい側の行番号） |
| `side` | `RIGHT`（新しいコード）または`LEFT`（削除されたコード） |

### 3. コメントフォーマット

#### 問題指摘

```markdown
**[重要度] 問題の種類**

説明文。

**推奨修正**:
```swift
// 修正後のコード
```
```

重要度レベル:
- `[Critical]`: 修正必須（バグ、セキュリティ、クラッシュの可能性）
- `[Medium]`: 推奨修正（パフォーマンス、ベストプラクティス違反）
- `[Low]`: 軽微な改善提案
- `[Info]`: 情報提供のみ

#### 総評コメント

ファイルの先頭（line=1）に総評を投稿:

```markdown
**[Info] 総評**

全体的に良く設計されたPRです。

✓ **良い点**:
- 良い点1
- 良い点2

**推奨アクション**: 指摘事項を修正後、マージ可能

🤖 Reviewed by Claude Code
```

### 4. 複数コメントの投稿例

```bash
COMMIT_SHA=$(gh pr view 63 --json headRefOid --jq '.headRefOid')

# コメント1: Critical問題
gh api repos/matsuokashuhei/Portal/pulls/63/comments \
  -X POST \
  -f body="**[Critical] メモリリークの可能性**

クロージャ内で\`self\`を強参照しています。

**推奨修正**:
\`\`\`swift
timer = Timer.scheduledTimer { [weak self] _ in
    self?.updateUI()
}
\`\`\`" \
  -f commit_id="$COMMIT_SHA" \
  -f path="Portal/App/AppDelegate.swift" \
  -F line=50 \
  -f side="RIGHT"

# コメント2: 総評
gh api repos/matsuokashuhei/Portal/pulls/63/comments \
  -X POST \
  -f body="**[Info] 総評**

全体的に良い実装です。

🤖 Reviewed by Claude Code" \
  -f commit_id="$COMMIT_SHA" \
  -f path="Portal/Services/MenuCrawler.swift" \
  -F line=1 \
  -f side="RIGHT"
```

### 5. 既存コメントへの返信

```bash
gh api repos/{owner}/{repo}/pulls/{PR番号}/comments \
  -X POST \
  -f body="返信内容" \
  -F in_reply_to=<コメントID>
```

### 6. レビュー全体の投稿

インラインコメントと一緒にレビュー全体を投稿:

```bash
gh pr review <PR番号> --comment --body "レビュー完了しました。インラインコメントを確認してください。"
```

または承認/変更要求:

```bash
# 承認
gh pr review <PR番号> --approve --body "LGTM 🚀"

# 変更要求
gh pr review <PR番号> --request-changes --body "指摘事項を修正してください。"
```

## 使用例

```bash
# 現在のブランチのPRをレビュー
/pr-review

# PR番号を指定してレビュー
/pr-review 123

# 特定の観点に絞ってレビュー
/pr-review --focus memory,thread-safety

# レビュー後、GitHubにインラインコメントを投稿
/pr-review 123 --post-comments
```
