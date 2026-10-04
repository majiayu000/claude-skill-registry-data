---
name: issue-investigate
description: GitHub issue を起点に、PR や永続的な repo 変更を成果物としない調査・設計・技術検証を実行し、構造化した結果を issue コメントへ記録して受け入れ条件確認後に close する。Ready なコメント完結型 issue の着手時に使用する。
version: 1.2.0
---

# Issue Investigate Skill

調査・設計・技術検証の結果を GitHub issue コメントへ記録して完了する orchestrator。repo の code / test / config / durable docs を成果物とする場合は `issue-implement` を使う。

## スコープ

- **含む**: Status・コメント・依存・親 issue の事前確認、調査・設計・技術検証、構造化した結果コメントの投稿、`acceptance-check`、明示された後続 issue の起票、成功後の対象 issue close。
- **含まない**:
  - repo の code / test / config / durable docs を成果物とする変更、commit、cross-review、PR、CI。
  - 調査結果を保存するための新規 Markdown ファイル追加。
  - ユーザー指示や元 issue の受け入れ条件にない後続 issue の自動起票。

## 依存

- **`issuekit:acceptance-check` skill**: 結果コメント投稿後、対象 issue の受け入れ条件を read-only で検査する。APM plain-skill mode では `acceptance-check` として呼び出す。
- **`issuekit:issue-create` skill**: 明示的に要求された後続 issue を起票する場合だけ使用する。APM plain-skill mode では `issue-create` として呼び出す。
- **`gh` CLI**: issue・コメント・親子関係の取得、コメント投稿、close に使用する。
- 調査対象に応じた read-only コマンドや検証ツール。repo を一時変更する検証は後述の安全条件を満たす場合だけ行う。

## 入力

- issue URL または issue 番号。

対象 issue の完了形が「issue コメント」であることを前提とする。受け入れ条件と `## スコープ外` を読み、repo の code / test / config / durable docs の変更も完了条件に含む、または完了形を判別できない場合は着手せず `issue-refine` を案内する。

## 実行手順

### 1. issue 本文・コメント・Status の確認

```bash
ISSUE_NUMBER=<issue 番号>
gh issue view "$ISSUE_NUMBER" --comments
gh issue view "$ISSUE_NUMBER" --json title,body,updatedAt,comments
```

- 本文先頭が `Status: Ready` であることを確認する。`Status: Draft` または表記不完全なら着手せず `issue-refine` を案内する。
- コメントを時系列で読み、本文との矛盾、未解決 blocker、方針保留、受け入れ条件の未反映変更がないことを確認する。`updatedAt` と時系列でも意図を確定できなければ着手しない。
- 受け入れ条件とスコープ外から完了形を判定する。調査結果のコメント記録が完了条件で、durable な repo 変更を要求しない場合だけ続行する。PR とコメントの両方に該当する、または判別不能なら自動着手せず `issue-refine` を案内する。

### 2. Depends on の確認

本文に `Depends on: #N, #M` があれば、各 issue の実際の state を取得する。

```bash
gh issue view <依存 issue 番号> --json state --jq '.state'
```

1 件でも open なら着手しない。依存状態を本文へ書き戻さない。

### 3. 親 issue の確認

本文の `親: #N` と GitHub sub-issue parent endpoint の両方を確認し、親があれば本文とコメントを読む。

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
gh api "repos/${REPO}/issues/${ISSUE_NUMBER}/parent" --jq '{number, title, state}'
gh issue view <親 issue 番号> --comments
```

parent endpoint の 404 は「親なし」として扱い、それ以外の取得失敗では着手しない。両経路で親が見つかった場合は和集合を取り、重複を除く。親の方針と対象 issue が矛盾し、時系列から解決できなければ着手しない。

### 4. 作業状態の記録と検証方法の決定

調査開始時に `git status --short` と必要に応じて `git diff` / `git diff --cached` を確認し、既存のユーザー変更を記録する。

- 原則として read-only な調査を優先する。
- 一時的な repo 変更が必要なら、開始時点が clean な専用 worktree / branch 等、調査由来の差分をユーザー変更と確実に区別できる環境でのみ行う。既存変更がある環境では一時変更を行わず、別の clean な作業環境をユーザーに用意してもらう。
- ユーザーの既存変更を `git reset`、`git checkout --`、`git clean`、手動上書き等で破棄しない。
- 一時変更は commit せず、PR も作らない。検証コマンドと観測結果を記録してから、調査で追加・変更した対象だけを元に戻す。開始時点の snapshot と照合できない変更には触れない。

### 5. 調査・設計・技術検証

issue の受け入れ条件と調査方針に沿って、必要なソース・公式文書・履歴・実行結果を確認する。バージョンや仕様など変わりうる情報は最新の一次情報を確認し、結果コメントに URL を残す。

途中で blocker が見つかっても、判明した事実と未検証範囲を整理する。blocker により受け入れ条件を満たせない場合は結果コメントを投稿しても完了扱いにせず、issue を close しない。

### 6. 明示された後続 issue の起票

元 issue の受け入れ条件またはユーザー指示に「後続 issue を起票する」と明記されている場合だけ、調査結果を踏まえて `issue-create` の手順で起票する。明記がなければ起票せず、step 7 の `### 後続候補` に提案を残すだけにする。

起票した後続 issue の URL は保持し、結果コメントの `### 後続候補` に記載する。起票に失敗した場合も判明済みの調査結果は step 7 でコメントするが、Blocker に失敗内容を記載し、受け入れ条件未達として close しない。

### 7. 結果コメントの投稿

以下の構造を保ち、該当事項がない見出しも `なし` と明記してコメントを投稿する。これにより `acceptance-check` がコメントの存在と必須項目を検査できる。

```md
## 調査結果

### 結論

<採用する結論、または現時点で結論不能である旨>

### 根拠

- <ソース、公式 URL、観測事実>

### 検証内容

- <実行した手順 / コマンドと結果>

### Blocker

- なし

### 却下案

- <案と却下理由、なければ「なし」>

### 後続候補

- <候補と理由。起票済みなら issue URL、未起票なら候補であることを明記。なければ「なし」>
```

```bash
RESULT_COMMENT_URL=$(gh issue comment "$ISSUE_NUMBER" --body-file - <<'EOF'
## 調査結果
...
EOF
)
[ -n "$RESULT_COMMENT_URL" ] || exit 1
```

投稿時に返された `RESULT_COMMENT_URL` を、この cycle で検査する結果コメントの一意な識別子として保持する。再投稿した場合は新しい URL へ置き換え、過去の結果コメントを今回の正本として扱わない。

### 8. 一時差分が残っていないことの確認

結果投稿前後に `git status --short` を再取得し、step 4 の開始時点と比較する。調査由来の差分が 1 件でも残っていれば完了扱いにせず、安全に所有権を特定できる差分だけを戻して再確認する。開始時点に存在したユーザー変更は同じ状態で保持する。

### 9. 受け入れ条件チェック

明示された後続 issue の起票、結果コメント投稿、一時差分の確認後に `issuekit:acceptance-check <N> --result-comment <RESULT_COMMENT_URL>`（APM plain-skill mode では `acceptance-check <N> --result-comment <RESULT_COMMENT_URL>`）を呼び出す。コメント完結型の条件は `gh issue view "$ISSUE_NUMBER" --json body,comments` から URL が一致する単一コメントだけを正本として検査し、過去コメントを合成して充足扱いにしない。

- `✗` があれば調査または結果コメントを補い、再検査する。
- `?` は呼び出し側で可能な確認を行う。判定できない項目が残れば close しない。
- すべての項目が `✓`、または根拠を伴って呼び出し側が充足と判定できた場合だけ次へ進む。

### 10. issue の close と完了報告

次の全条件を満たした後でのみ対象 issue を close する。

1. 構造化した結果コメントの投稿に成功した。
2. 調査由来の repo 差分が残っていない。
3. `acceptance-check` で未達・未判定項目がない。
4. 明示的に要求された後続 issue の起票に成功した。

```bash
gh issue close "$ISSUE_NUMBER"
```

結果コメント URL、受け入れ条件チェックのサマリー、close 結果、起票した後続 issue（ある場合）をユーザーへ返す。

## 失敗時の対応

- issue / コメント / 親 / 依存の取得に失敗した場合は着手せず、取得できなかった対象を報告する。
- コメント投稿に失敗した場合は close しない。結果をローカルの新規 Markdown として保存せず、再投稿可能な内容を会話内で保持してエラーを報告する。
- 一時変更を安全に元へ戻せない、またはユーザー変更との区別がつかない場合は操作を止め、差分を残したまま対象と理由を報告する。ユーザー変更を推測で破棄しない。
- `acceptance-check` に `✗` / 未解決の `?` がある、明示された後続 issue の起票に失敗した、結果コメント URL を保持できない、または `gh issue close` が失敗した場合は途中成功を明示し、close 済みと報告しない。

## やらないこと

- 調査結果を新規 Markdown として repo に追加しない。
- 調査中の一時変更を commit、push、PR 化しない。`cross-review` や CI も実行しない。
- 開始時点に存在したユーザー変更を破棄・上書き・整形しない。
- 結果コメント投稿前、受け入れ条件確認前、一時差分解消前、明示された後続 issue 起票前に対象 issue を close しない。
- 元 issue の受け入れ条件またはユーザー指示にない後続 issue を起票しない。
- repo 変更を含む issue や完了形が曖昧な issue を `issue-investigate` へ強行しない。`issue-refine` で完了形を明確にする。
