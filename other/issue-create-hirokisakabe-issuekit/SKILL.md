---
name: issue-create
description: "Invoke for any request to create, file, open, or record a new GitHub issue. Trigger on:\n- Direct creation: 「issue 作って」「起票して」「issue 立て(といて)」「issue 化して」「issue 作れる?」\n- Record intent: 「issue に残したい/残しておいてほしい」「issue として残しておきたい」\n- Issue types: bug reports (with repro steps), feature requests, refactoring tasks, doc fixes, investigation / design tasks, code-review findings to track later\n\nDo NOT trigger for viewing, listing, searching, or implementing existing issues."
version: 2.2.0
---

# Issue Create Skill

GitHub issue を起票する際のフォーマットと手順。

## 基本方針

- 種別（feature / bug / task など）は持たない。共通セクションの組み合わせで表現する。
- ラベルやテンプレ整備はリポジトリ側に委ねる。本 Skill はあくまで本文構造を統一する。
- 起票は `gh issue create` を使用する。

## ステータス

issue 本文の **先頭** に必ず以下のいずれかを記載する。

- `Status: Ready` — 受け入れ条件確定、着手可
- `Status: Draft` — 受け入れ条件未確定、議論中（着手不可）

### Draft とする条件

Status の判定軸は **受け入れ条件の確定度** 一本である。言い換えると **「やったかどうか自分で判定できる受け入れ条件があるか」** で判断する。

受け入れ条件が以下のいずれかに該当する場合は `Status: Draft` とする。

- 「仮」「要検討」等を含み確定していない
- 検証不能なほど曖昧で、「やったかどうか自分で判定できない」状態

上記に該当しない場合は `Status: Ready` とする。

`Status: Draft` の場合は、本文に `## Ready にするための未決事項` セクションを必ず設ける。ここには Draft であるという状態説明ではなく、**何を決めれば受け入れ条件を確定できるか**を具体的な問いのチェックリストとして記載する。

```md
## Ready にするための未決事項

- [ ] 対応対象に Linux を含めるか
- [ ] エラー時の期待結果を A / B のどちらにするか
```

- 受け入れ条件の確定を妨げている事項だけを書く。実装方法の選択肢や、着手後に調査可能な技術的詳細は含めない。
- 未決事項が解消したら、その決定を `## 受け入れ条件` へ反映し、未決事項セクションを削除して `Status: Ready` に変更する。
- 未決事項が 1 件でも残っている間は `Status: Draft` を維持する。

実装方針の確定度は Status に絡めない。バグ issue では「方針 A を試して直らなかったら B」というプロセス自体が正しい進め方であり、方針の事前確定を強制すると実態とミスマッチする。受け入れ条件が確定していて `acceptance-check` skill で検証可能であれば、「方針 A を採用したのにバグが直っていないまま close される」事故は防げる。

そのため **実装方針が複数案あっても、優先順位付き（または順序付き）で列挙されていれば `Status: Ready`** でよい。

### 着手時の確認

着手依頼を受けた際、agent は **実装を始める前に必ずこのステータスを確認する**。`Status: Draft` の場合は実装に着手せず、ユーザーに受け入れ条件の確認を行うこと。

## 依存 issue (Depends on)

他 issue の完了を待つ必要がある場合、`Status:` 行の直下に `Depends on: #<番号>` を記載する。

- 形式: `Depends on: #123, #124`（複数あればカンマ区切り）
- 依存が無ければ **行ごと省略** する（空の `Depends on:` を残さない）。
- **依存 issue の状態（open / closed）は本文に書かない。** GitHub UI 側で close 済み issue は取り消し線で表示されるため、本文に状態を書くと二重管理になり古い情報が残るリスクがある。状態を判定したいときは `gh issue view <番号> --json state` で実体を確認する。
- `Status` との関係: `Status` は spec 自体の確定度（Ready / Draft）、`Depends on` は他 issue の完了待ちを表し、両者は独立した軸。「Ready だが Depends on あり」「Draft かつ Depends on あり」のような組み合わせもありうる。

## 成果物と完了形

受け入れ条件と `## スコープ外` には、issue の完了形を判定できる情報を明記する。

- repo の code / test / config / durable docs の変更が完了条件に含まれる → **PR**。`issue-implement` で着手する。
- 調査・設計・技術検証の結果を issue コメントへ記録することが完了条件で、durable な repo 変更を要求しない → **issue コメント**。`issue-investigate` で着手する。
- 両方に該当する、または受け入れ条件とスコープ外から判別できない → **要確認**。`Status` の判定とは分けて扱い、着手前に `issue-refine` で完了形を明確にする。

調査・設計 issue の成果物は、デフォルトで対象 issue の結果コメントとする。公開 API 仕様、architecture decision、継続的な運用手順など、issue close 後も継続参照される durable artifact が **受け入れ条件に明示的に必要**な場合だけ repo 文書を成果物に含める。issuekit は durable artifact の保存場所を一律に決めない。

コメント完結型の受け入れ条件には、最低限「構造化した調査結果を対象 issue のコメントへ投稿する」を含め、必要な見出し・検証内容や close 条件を具体化する。`## 調査メモ` は着手前の情報であり、完了成果物の結果コメントとは区別する。

## 本文フォーマット

### 共通セクション（必須）

```md
Status: Ready # または Draft
Depends on: #123, #124 # 依存がある場合のみ。無ければ行ごと省略

## 概要

<1〜3 行で何をするか>

## 背景 / モチベーション

- <なぜやるのか>

## 受け入れ条件

- [ ] <検証可能な完了条件>

## スコープ外

- <やらないこと>

## 参考

- <関連 issue / PR / URL>
```

### 追加セクション（必要時のみ）

- **Ready にするための未決事項** — `Status: Draft` の場合に追加

  受け入れ条件を確定するために必要な判断を、具体的な問いのチェックリストとして記載する。`Status: Ready` の場合はこのセクションを記載しない。

  ```md
  ## Ready にするための未決事項

  - [ ] <受け入れ条件を確定するために決めること>
  ```

- **実装方針** — 方針案を記載する場合に追加

  単一の方針が確定しているケースだけでなく、**解消候補を優先順位付き（または試行順）で列挙する書き方も許容する**。バグ issue で「上から順に試す」プロセスが想定される場合は、後者の形式が自然。

  単一方針が確定している場合:

  ```md
  ## 実装方針

  - <方針 / 採用案 / 検討した代替案>
  ```

  解消候補を優先順位付きで列挙する場合:

  ```md
  ## 実装方針

  以下を上から順に試す:

  1. <候補 1>
  2. <候補 2>
  3. <候補 3>
  ```

- **再現手順 / 期待 / 実際** — バグ報告の場合

  ```md
  ## 再現手順

  1.

  ## 期待する挙動

  ## 実際の挙動
  ```

  バグ issue では **受け入れ条件を再現手順・期待挙動とセットで検証可能な形** に書く。「バグが fix される」だけの曖昧な書き方ではなく、再現手順や期待挙動セクションを参照する形で記述する。例:

  ```md
  ## 受け入れ条件

  - [ ] <再現手順> を実行してもエラーが発生しない
  - [ ] <期待挙動> セクションに記載した動作になる
  ```

  これにより、複数の解消候補から方針を選んで実装した結果として実際にバグが直ったかを `acceptance-check` skill で検証でき、「方針を採用したのに直っていないまま close される」事故を防げる。

- **調査メモ** — 調査タスクの場合

  ```md
  ## 調査メモ

  - <現時点でわかっていること / 未確認事項>
  ```

## 親子 issue の扱い

- 子 issue を切るのは以下の **いずれか** に該当する場合に限る:
  - 実装が複数 PR にまたがる規模
  - 並行実装可能で価値がある
  - 各タスクが独立にレビューされるべき
- 1 PR に収まる規模なら、実装ステップは親 issue の受け入れ条件に並べる（子 issue 化しない）。
- **子 issue は「実装タスク」のみを対象とする。** 調査・バグは親子で分けない（1 つの issue に集約する）。
- 親子の紐づけは GitHub の **sub-issue 機能** を使う。親本文にチェックリストで子 issue を列挙しない。
- 子 issue の本文には必ず以下を含める。
  - 親 issue へのリンク（例: `親: #123`）
  - 「**実装前に親 issue を必ず読むこと**」の明記
- **注意:** 子 issue を agent に渡して実装依頼する際、親 issue を読まずに進めてしまうことがある。子 issue を扱う際は最初に親 issue を `gh issue view` で取得し、文脈を踏まえてから着手する。

子 issue 本文テンプレ例:

```md
Status: Ready
Depends on: #<依存 issue 番号> # 依存がある場合のみ。無ければ行ごと省略

親: #<親 issue 番号>

> **実装前に親 issue を必ず読むこと。**

## 概要

...
```

## 実行手順

1. ユーザーの要求から上記フォーマットに沿って本文を組み立てる。情報が不足している場合はユーザーに確認する。
2. ステータス（Ready / Draft）を判定する。「ステータス > Draft とする条件」に従い、いずれかに該当すれば Draft。
3. 親子関係がある場合は親 issue 番号を確認し、子 issue 本文に親リンクを入れる。
4. `gh issue create` で起票する。タイトルに記号が含まれても安全なよう、本文は `--body-file -` で標準入力から渡す。

   ```bash
   TITLE="<タイトル>"
   gh issue create --title "$TITLE" --body-file - <<'EOF'
   Status: Ready

   ## 概要
   ...
   EOF
   ```

5. 起票後、issue URL を保持する（まだユーザーに返さない）。
6. **親 issue がある場合は、必ず `gh api` で sub-issue として紐づける。** この手順を省略してはならない。

   ```bash
   # gh issue create の出力 URL から子 issue 番号を抽出
   CHILD_ISSUE_URL="<gh issue create が返した URL>"
   CHILD_ISSUE_NUMBER="${CHILD_ISSUE_URL##*/}"
   PARENT_ISSUE_NUMBER=<親 issue 番号>

   # リポジトリ名を取得
   REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

   # 子 issue の database ID (integer) を取得。
   # `gh issue view --json id` は GraphQL node ID (例: `I_kwDO...`) を返すが、
   # REST `POST .../sub_issues` の `sub_issue_id` は integer の database ID を要求する。
   CHILD_ID=$(gh api "repos/${REPO}/issues/${CHILD_ISSUE_NUMBER}" --jq '.id')

   # 親 issue に sub-issue として追加 (-F で integer として送る)
   gh api "repos/${REPO}/issues/${PARENT_ISSUE_NUMBER}/sub_issues" \
     -X POST \
     -F sub_issue_id="$CHILD_ID"
   ```

7. 紐づけ完了を確認してから、issue URL をユーザーに返す。

## やらないこと

- close キーワード（`close #123` など）を issue 本文・コメントに書かない。PR 側では、選定方法にかかわらず、対応する issue 全体を完了させる場合だけ使用する。
- 既存 issue のフォーマットを遡及的に書き換えない。
