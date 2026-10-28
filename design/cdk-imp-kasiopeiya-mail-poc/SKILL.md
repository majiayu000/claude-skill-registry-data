---
name: cdk-imp
description: AWS CDK実装専用コマンド。GitHub IssueからCDK実装・テスト・CDK合成まで自動実行する。CDKインフラの実装を依頼されたときに使用すること。
argument-hint: '<Issue番号>'
---

指定されたGitHub Issueを元に、設計書を参照してAWS CDKコード（`infra/` 配下）のみを実装し、テスト・合成まで実行してください。

Issue指定: <skill-args>

引数が空の場合は、ユーザーにIssue番号を確認してください。

---

## CDK実装の詳細手順

GitHub IssueからAWS CDK実装を実行する。
設計書を参照し、CDKルールを遵守したインフラコードを実装、テスト・合成まで実行する。

## スコープ制約

- **`infra/` 配下のみを対象とする**
- **`app/` は変更しない**（アプリ実装は `/tdd` の担当）
- **新規に Stack / Construct を書き起こす前に `samples/infra/` を Read する。** スタック分割・環境差分の出し方・Construct の粒度・テストの書き方の手本がある。`samples/` 自体は変更しない
- Issueのタスク一覧のうち、CDK/インフラに関するタスクのみを実装対象とする
- Lambdaハンドラー実装、UI実装、アプリケーションのテストコード等は対象外
- 対象外のタスクはスキップし、GitHub Issueのチェックリストも更新しないこと

## 実行プロセス

### Phase 1: Issue読み込みと実装仕様の抽出

#### ステップ 1-1: Issue番号の取得

タスクプロンプトの「Issue指定:」の値を確認する。値が含まれている場合はそれを使用し、空の場合のみAskUserQuestionでユーザーに確認する。

```
question: "CDK実装を行うIssueを指定してください。Issue番号（例: 1）を入力してください。"
header: "Issue指定"
options: [
  { label: "その他（手動入力）", description: "Issue番号を入力してください" }
]
multiSelect: false
```

**取得情報**:

- Issue番号

#### ステップ 1-2: GitHub IssueのJSON取得

Bash ツールで GitHub Issue の情報を取得:

```bash
gh issue view {番号} --json number,title,body,labels
```

**エラーハンドリング**:

Issue が見つからない場合:

```
=== Issue 読み込みエラー ===

Error: Issue #{番号} が見つかりませんでした。
gh issue list で利用可能なIssue一覧を確認してください。
```

→ AskUserQuestion で再入力を促す（最大3回まで）

body が空の場合:

```
=== Issue 読み込みエラー ===

Error: Issue #{番号} の本文が空です。
```

→ 処理を中止

#### ステップ 1-3: Issue内容の解析

取得したJSONから以下の情報を抽出:

**1. Issue番号とタイトル**

- Issue番号: `.number` フィールド
- タイトル: `.title` フィールド

**2. ラベル**

`.labels[].name` フィールドから抽出

- 抽出例: `[{name: "cdk"}, {name: "infra"}]` → `['cdk', 'infra']`

**3. スコープ/作業項目**

body内 `## スコープ / 作業項目` セクションの内容全体を抽出

**4. タスク一覧（CDKタスクのみ抽出）**

body内 `## タスク一覧` セクションのチェックリスト（`- [ ]` 形式）を抽出し、**CDK/インフラに関するタスクのみをフィルタリング**する。

**フィルタリングルール**:

- **対象**: 「CDK」「cdk」「インフラ」「スタック」「Construct」「デプロイ」「synth」「スナップショット」等のキーワードを含むタスク
- **対象外（スキップ）**: 「Lambda実装」「ハンドラー実装」「API実装」「フロントエンド」「画面」「テストコード作成」「TDD」「単体テスト」等、アプリケーションコードに関するタスク
- 上記キーワードに一致しないタスクは既定で対象外とする。取りこぼしがあれば、body内「対象ファイル」節に挙げた CDK ディレクトリ配下のファイルに明示的に言及しているタスクだけを対象に加える
- フィルタリング結果（対象タスク・スキップしたタスク）を明示的に表示する

**5. 対象ファイル**

body内 `## 📂 コンテキスト` または `### 対象ファイル` セクションから抽出

- `<CDKディレクトリ>/lib/{スタックファイル名}.ts`
- `<CDKディレクトリ>/lib/constructs/*.ts`（新規Constructの場合）

**出力例**:

```
=== Issue解析結果 ===

Issue: #1 CDK初期構築

ラベル: cdk, infra
対象ファイル: <CDKディレクトリ>/lib/{スタックファイル名}.ts

対象タスク（CDK/インフラ関連）:
- [ ] CDKコード実装
- [ ] スナップショットテスト更新
- [ ] cdk synth確認

スキップするタスク（アプリケーションコード関連）:
- [ ] Lambdaハンドラー実装 → 対象外
- [ ] フロントエンド実装 → 対象外

スコープ:
- CDKプロジェクト初期化
- スタック基本構成作成
```

#### ステップ 1-5: 実装仕様の整理と確認

抽出した情報をユーザーに提示し、開始確認:

```
question: "以下の内容でCDK実装を開始します。よろしいですか？"
header: "実装開始確認"
options: [
  { label: "はい、開始します", description: "CDK実装を開始します" },
  { label: "いいえ、中止します", description: "処理を中止します" }
]
```

### Phase 2: 設計書参照と実装方針確認

#### ステップ 2-1: 設計ハブから対象設計書を特定

設計ハブ `docs/design-hub.md` を Read し、リンクされている個別設計書の一覧と担当範囲を取得する。

**特定ロジック**:

1. インフラ設計書（何を組むか＝アーキテクチャ概要を記す文書）と IaC 設計書（どう作り・変えるか＝IaC 管理方針・スタック設計・命名規約を記す文書）は、**両方**を常に対象に含める
2. Issue のラベル・タイトル・スコープと、各設計書の概要を照合し、関連する設計書（Lambda関連の変更ならバックエンド設計、CloudFront/S3関連の変更ならフロントエンド配信設計、等）を追加で対象に含める
3. 設計ハブが未作成、または対応する設計書が見つからない場合は、AskUserQuestion でユーザーに確認する（推測で新規作成しない）

**結果例**:

```
対象設計書:
- {インフラ設計書}（常に対象）
- {IaC 設計書}（常に対象）
- {バックエンド設計書}（Lambda関数関連の場合）
```

#### ステップ 2-2: インフラ設計書・IaC 設計書の読み込み

ステップ2-1 で特定した2文書を Read ツールで読み込み、以下を抽出する:

- 設計判断サマリー（ADRへのリンクと決定内容）
- アーキテクチャ概要（全体構成図、コンポーネント）— インフラ設計書
- スタック構成・環境差分の出し方・命名規約 — IaC 設計書

#### ステップ 2-3: 関連設計書の読み込み（必要に応じて）

ステップ2-1 で対象に加えた関連設計書（バックエンド／フロントエンド等）があれば、その内容も Read ツールで読み込む。

#### ステップ 2-4: CDKルールの確認

```
file_path: .claude/rules/cdk.md
```

**確認事項**:

- L2 Construct優先
- IAM Role自動生成の活用

#### ステップ 2-5: 実装方針の整理と確認

設計書とCDKルールから抽出した情報を整理してユーザーに提示:

```
=== 実装方針サマリー ===

設計判断:
- Lambda Function URLs を使用（ADR-001）
- OAC + IAM認証（ADR-004）

CDKルール:
- L2 Construct優先
- IAM Role自動生成を活用

循環参照回避戦略:
- SSM Parameter Store の利用
- ワイルドカードリソース指定
- L1 Construct（Cfn）の活用
```

AskUserQuestion で実装方針を確認:

```
question: "上記の実装方針でCDKコードを実装します。よろしいですか？"
header: "実装方針確認"
options: [
  { label: "はい、この方針で実装します", description: "CDKコード実装に進みます" },
  { label: "いいえ、修正が必要です", description: "実装方針を見直します" }
]
```

### Phase 3: CDK実装

#### ステップ 3-1: 対象ファイルの特定

Issue内の「📂 コンテキスト」または「### 対象ファイル」セクションから対象ファイルを取得:

- 通常は `<CDKディレクトリ>/lib/{スタックファイル名}.ts`（メインスタック）
- 新規Constructの場合は新規ファイル作成も検討

#### ステップ 3-2: 既存CDKコードの読み込み

Read ツールで対象ファイルを読み込み:

```
file_path: <CDKディレクトリ>/lib/{スタックファイル名}.ts
```

**確認事項**:

- 既存の実装パターン
- 既存のConstructの構成

#### ステップ 3-3: CDKルールの遵守チェック

実装前に以下を確認:

**L2 Construct優先**:

- 可能な限りHigh-level APIを使用
- L1（Cfn）は循環参照回避時のみ使用

**IAM Role自動生成**:

- L2 ConstructのIAM Role自動生成機能を活用
- 明示的なRole定義は避ける

#### ステップ 3-4: CDKコードの実装

Edit または Write ツールで実装:

**実装ガイドライン**:

コメント・JSDoc は `docs/policy/code-comment-policy.md` に従う（実装コメントは WHY、doc comment は契約。コードが語る WHAT/HOW は書かない）。

1. **JSDocコメント**: 関数の役割・引数・戻り値・例外を契約として明記
2. **日本語コメント**: コードから読み取れない WHY（判断理由・制約・罠）を説明
3. **循環参照の回避**:
   - SSM Parameter Storeの活用（CloudFront URLなど）
   - ワイルドカードリソース指定（Secrets Managerなど）
   - L1 Construct（Cfn）の活用（後付け設定）

**実装例**:

```typescript
/**
 * S3バケットを作成
 * @param {string} bucketName - バケット名
 * @returns {s3.Bucket} - 作成されたS3バケット
 */
private createS3Bucket(bucketName: string): s3.Bucket {
  // 1. S3バケット作成（L2 Construct使用）
  const bucket = new s3.Bucket(this, 'FrontendBucket', {
    bucketName: bucketName,
    removalPolicy: RemovalPolicy.DESTROY,
    autoDeleteObjects: true,
  })

  // 2. バケットポリシー設定（OAC用）
  // 循環参照回避のため、CloudFront作成後にL1 Constructで設定

  return bucket
}
```

#### ステップ 3-5: 実装内容の確認

実装したコードをユーザーに提示:

```
=== CDK実装完了 ===

実装ファイル: <CDKディレクトリ>/lib/{スタックファイル名}.ts

変更内容:
- Lambda Function作成（NodejsFunction使用）
- Lambda Function URL設定
- CloudFront Origin設定
- IAMポリシー自動生成
```

AskUserQuestion で確認:

```
question: "実装内容を確認してください。このままテストに進みますか？"
header: "実装確認"
options: [
  { label: "はい、テストに進みます", description: "npm testを実行します" },
  { label: "いいえ、修正が必要です", description: "実装を見直します" }
]
```

**重要な考慮事項**:

- **TypeScriptコンパイルは単体では実施しない**。次の Phase のテスト実行で型エラーも検出されるため、`tsc` を別途走らせる意味がない

### Phase 4: テスト実行

#### ステップ 4-1: npm test の実行

Bash ツールでCDKテストを実行:

```bash
cd <CDKディレクトリ> && npm test
```

**成功判定**: 終了コード 0

#### ステップ 4-2: テスト結果の解析

**成功時**:

```
✅ Tests Passed

All CDK tests passed successfully.
```

**失敗時**:

テストエラーメッセージを解析:

1. **スナップショット不一致**の検出:
   - エラーメッセージに "snapshot" または "does not match" が含まれる
   - → ステップ 4-3 へ

2. **その他のエラー**:
   - 型エラー、構文エラー、ロジックエラー等
   - → ステップ 4-4 へ

#### ステップ 4-3: スナップショット更新の確認

スナップショット不一致が検出された場合:

```
⚠️ Snapshot Mismatch Detected

スナップショットテストが不一致です。以下のファイルで差分が検出されました:

<CDKディレクトリ>/test/__snapshots__/{テストファイル名}.snap

差分内容:
- CloudFormation テンプレートの変更
- リソース追加/削除

スナップショットを更新しますか？
```

AskUserQuestion でスナップショット更新の可否を確認:

```
question: "スナップショットを更新しますか？（実装内容が正しい場合は更新してください）"
header: "スナップショット更新"
options: [
  { label: "はい、更新します", description: "npm test -- -u を実行してスナップショットを更新" },
  { label: "いいえ、実装を修正します", description: "CDKコードを見直します" }
]
multiSelect: false
```

**「はい」選択時**:

```bash
cd <CDKディレクトリ> && npm test -- -u
```

スナップショット更新後、再度テスト実行:

```bash
cd <CDKディレクトリ> && npm test
```

**「いいえ」選択時**:

Phase 3に戻り、実装を修正

#### ステップ 4-4: エラーがあれば修正提案

テスト失敗（スナップショット以外）の場合:

```
🔴 Test Failed

以下のエラーが検出されました:

<CDKディレクトリ>/lib/{スタックファイル名}.ts:42:7
  Error: Property 'functionUrl' does not exist on type 'Function'.

原因:
Lambda Function URLはNodejsFunctionのプロパティとして直接アクセスできません。

修正方法:
1. FunctionUrl Constructを使用してURLを作成
2. または、addFunctionUrl() メソッドを使用

修正しますか？
```

AskUserQuestion で修正するか確認:

```
question: "上記のエラーを修正しますか？"
header: "エラー修正"
options: [
  { label: "はい、修正します", description: "エラーを修正してテストを再実行" },
  { label: "いいえ、中止します", description: "処理を中止します" }
]
```

「はい」選択時: Phase 3に戻り、実装を修正

**エラーハンドリング**:

- 最大3回まで修正を試行
- 3回失敗した場合は処理を中止し、ユーザーに手動修正を促す

### Phase 5: CDK合成と循環参照チェック

#### ステップ 5-1: cdk synth の実行

Bash ツールでCloudFormationテンプレート合成:

```bash
cd <CDKディレクトリ> && npx cdk synth
```

**成功判定**: 終了コード 0

#### ステップ 5-2: 合成結果の確認

**成功時**:

```
✅ CDK Synth Passed

CloudFormation テンプレートが正常に生成されました:

cdk.out/{アプリ名}.template.json
cdk.out/{アプリ名}.assets.json
cdk.out/manifest.json
cdk.out/tree.json
```

**失敗時**:

合成エラーメッセージを解析:

1. **循環参照エラー**の検出:
   - エラーメッセージに "Circular dependency" が含まれる
   - → ステップ 5-3 へ

2. **その他のエラー**:
   - 構文エラー、リソース設定エラー等
   - → ステップ 5-4 へ

#### ステップ 5-3: 循環参照エラーのチェック

循環参照エラーが検出された場合、循環しているリソースと原因を示し、[references/error-handling-and-constraints.md](references/error-handling-and-constraints.md) の「循環参照の回避」から該当パターンの回避方法を提示する。

AskUserQuestion で修正方法を確認:

```
question: "循環参照を回避するため、以下のいずれかの方法で修正します。どれを選択しますか？"
header: "循環参照回避"
options: [
  { label: "SSM Parameter Store を利用", description: "CloudFront URLをSSMに保存し、Lambda側で参照" },
  { label: "ワイルドカード指定", description: "IAMポリシーで '*' を使用" },
  { label: "L1 Construct 活用", description: "Cfn を使用して後付け設定" },
  { label: "手動で修正", description: "処理を中止して手動で修正" }
]
```

選択に応じて Phase 3 に戻り、実装を修正

#### ステップ 5-4: エラーがあれば修正提案

合成エラー（循環参照以外）の場合:

```
🔴 Synth Failed

以下のエラーが検出されました:

Error: Bucket name must be lowercase

原因:
S3バケット名に大文字が含まれています。

修正方法:
bucketName を小文字に変更してください。
```

AskUserQuestion で修正するか確認:

```
question: "上記のエラーを修正しますか？"
header: "エラー修正"
options: [
  { label: "はい、修正します", description: "エラーを修正してcdk synthを再実行" },
  { label: "いいえ、中止します", description: "処理を中止します" }
]
```

「はい」選択時: Phase 3に戻り、実装を修正

### Phase 6: 結果報告と Next Actions

#### ステップ 6-1: レポートの出力

[references/report-format.md](references/report-format.md) のフォーマットに従い、実装サマリー・テスト結果・Next Steps をまとめて出力する。

#### ステップ 6-2: GitHub Issueのタスクチェックリスト更新

Bash ツールで実装・テスト・CDK合成に関するタスクを完了マークに更新:

```bash
BODY=$(gh issue view {番号} --json body --jq '.body')
# CDK実装・テスト・synth完了に関連するタスクを完了マークに更新
UPDATED_BODY=$(echo "$BODY" | sed 's/- \[ \] \(.*実装.*\)/- [x] \1/g' \
  | sed 's/- \[ \] \(.*テスト.*\)/- [x] \1/g' \
  | sed 's/- \[ \] \(.*synth.*\)/- [x] \1/g')
gh issue edit {番号} --body "$UPDATED_BODY"
```

該当するタスクが見つからない場合はスキップ（エラーにしない）。

## 参照

- [references/report-format.md](references/report-format.md) — 完了レポートの出力フォーマット
- [references/error-handling-and-constraints.md](references/error-handling-and-constraints.md) — エラーハンドリング一覧・制約事項・循環参照の回避
