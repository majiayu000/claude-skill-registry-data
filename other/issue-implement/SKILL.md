---
name: issue-implement
description: 特定の GitHub issue への実装着手と PR 作成を依頼されたときに使う。issue 番号・URL・会話内で選んだ issue のいずれかを起点に、runtime と worktree の実装隔離を preflight で保証してから、実装・commit・lint・受け入れ条件チェック・cross-review・PR 作成・CI 確認まで一気通貫で自動進行する。コードを書いてプルリクを出す作業全般が対象で、issue 選定相談・タイトル編集・クローズ操作・PR レビュー単体には使わない。
version: 3.2.0
---

# Issue Implement Skill

GitHub issue を起点とした issue-driven 開発サイクルの中核 skill。issue 番号を受け取り、Status 確認から PR 作成・CI 確認までを定型的に実行する。

実装中の試行錯誤や中間段階を **commit 履歴として残す** 設計。commit を細かく区切ったうえで、最終状態に対して `acceptance-check`（受け入れ条件検査）→ `cross-review`（base...HEAD diff へのレビュー）→ PR 作成の順で回す。レビュー由来の修正も独立した commit として履歴に残るため、後から「なぜそう直したか」を追えるようになる。

## 依存

- **`issuekit:cross-review` skill**: 実装・commit 後、PR 作成前に、実装セッションから独立した reviewer session による second opinion を得る。APM plain-skill mode では `cross-review` として呼び出す。実装前に runtime と対応 CLI を事前確認し、未対応 runtime や CLI 未導入の場合は明確に失敗させる（該当 skill 側の失敗時対応に従う）。
- **`issuekit:acceptance-check` skill**: 実装・commit 後、cross-review より前に受け入れ条件の自動検査を実施する。APM plain-skill mode では `acceptance-check` として呼び出す。
- **`issuekit:worktree-start` skill**: Claude Code の対話 session が default branch 上にいる場合に、実装直前で `EnterWorktree` による専用 worktree への切り替えに使用する (後述 step 4)。APM plain-skill mode では `worktree-start` として呼び出す。他 runtime では呼ばない。
- **`issuekit:issue-dispatch` skill**: Codex CLI の default branch 上から単一 issue で本 skill が呼ばれた場合に、対象1件を専用 worktree の `issue-implement` worker へ引き継ぐ。APM plain-skill mode では `issue-dispatch`。linked worktree 内の worker は本 skill の preflight を通過して再 dispatch しない。
- **`issuekit:issue-create` skill**: Status と完了形の single source of truth。APM plain-skill mode では `issue-create`。本 skill では定義を複製せず参照する。
- **`gh` CLI**: GitHub 操作全般に使用する。

## スコープ

- **含む**: Status・PR 完了形の確認、Depends on の close 確認、親 issue の文脈取り込み、runtime / branch / worktree の実装隔離 preflight、Claude Code で可能な場合の worktree 切り替え、Codex CLI default branch からの単一 issue dispatch、実装と適宜 commit、lint/format/型チェック、受け入れ条件チェック、cross-review、PR 作成、CI 確認・修正。
- **含まない**:
  - default branch 名を hardcode した branch ガード。default branch 名はリポジトリにより異なる (main / master / develop / trunk 等) ため、`gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'` で動的に解決した値と現在ブランチを比較する。
  - Codex App の managed worktree / Handoff の作成・操作。これらは App が所有する機能であり、skill は App 管理 worktree を作成したふりをしない。
  - Codex CLI の起動済み session を別 cwd へ安全に移せるという仮定。default branch 上では親 session 自身を移動せず、対象1件を `issue-dispatch` に引き継ぎ、`codex exec --approve-for-me --worktree` で native managed worktree の専用 worker を起動する。
  - ユーザーが既に手動で feature ブランチに切り替えているケースの上書き。default branch 以外にいる場合は worktree 化を行わず既存ブランチを尊重する。
  - レビュー指摘の修正を `git commit --amend` / `rebase` / `fixup` で履歴整形すること。指摘対応は **追加 commit** で行い、試行錯誤やレビュー対応の経緯を履歴に残す。
  - issue コメントだけを成果物とする調査・設計・技術検証。`issue-investigate` の対象とする。

## 実行手順

### close intent の共通判定規則

PR description に `close #N` を付けるかは、`issue-dispatch` と同じ次の規則で判定する。

- `ISSUE_CLOSE_INTENT=true`: 実装対象に対応する GitHub issue があり、その issue 全体を完了させる PR を作る。番号 / URL の直接指定、提示済み候補への参照表現、広い選定条件からの dispatcher による機械選定のいずれも含む。
- `ISSUE_CLOSE_INTENT=false`: 対応する issue がない、または依頼が部分実装・親 epic の一部・単なる関連付けであり、その PR だけでは issue 全体を完了させない。
- PR 単体で issue 全体を完了するか曖昧なら `true` と推測せず、PR 作成前にユーザーへ確認する。

直接起動では取得済みの issue 契約と依頼された実装範囲から intent を判定し、`ISSUE_CLOSE_INTENT_REASON` に issue と実装範囲の対応関係を1行で記録する。dispatcher worker では prompt の `ISSUE_CLOSE_INTENT` と `ISSUE_CLOSE_INTENT_REASON` を必須入力としてそのまま使い、worker prompt 内の issue 番号から再判定しない。flag と reason が欠落・矛盾している場合は PR を作成せず dispatcher へ blocker を返す。

### 1. issue の取得と Status・完了形の確認

```bash
ISSUE_NUMBER=<issue 番号>
gh issue view "$ISSUE_NUMBER" --comments
gh issue view "$ISSUE_NUMBER" --json title,body,updatedAt,comments
```

- issue 本文だけでなく、コメントも必ず確認する。コメントには本文更新前の補足、後続議論で決まった方針変更、未反映の制約、追加の再現情報が残っていることがあるため、本文のみを唯一の文脈として扱わない。
- コメントに本文と矛盾する内容がある場合は、`updatedAt` やコメント時系列を踏まえて最新の意図を推定し、判断できなければ実装前にユーザーへ確認する。
- コメントに未解決 blocker、方針保留、受け入れ条件の未反映変更がある場合は、`Status: Ready` であっても着手を止める。ユーザーに確認するか、必要なら `issuekit:issue-refine` skill（APM plain-skill mode では `issue-refine`）で本文へ反映してから再開する。
- 本文先頭の `Status:` を確認する。Status の判定軸は **受け入れ条件の確定度** 一本（実装方針の確定度は問わない）であり、その意味を踏まえて分岐する。
  - **`Status: Ready`**: 受け入れ条件が「やったかどうか自分で判定できる」形になっている。コメント上の未解決 blocker / 本文矛盾 / 方針保留 / 受け入れ条件の未反映変更がなければ続行。
  - **`Status: Draft`**: 受け入れ条件が未確定（「仮」「要検討」を含む / 検証不能なほど曖昧）。着手しない。**worktree 化 (step 4) より前にここで early abort する**ため、worktree は作成されない。ユーザーに受け入れ条件の確認を促し、必要なら `issuekit:issue-refine` skill（APM plain-skill mode では `issue-refine`）で整理する。
  - **`Status:` 表記なし / フォーマット不完全**: 同様に worktree 化前に abort し、`issuekit:issue-refine` skill（APM plain-skill mode では `issue-refine`）での整理を案内する。

Status 確認後、受け入れ条件と `## スコープ外` を `issue-create` の「成果物と完了形」に照らし、worktree 化より前に分岐する。

- **PR**: repo の code / test / config / durable docs の変更が完了条件に含まれる。本 skill で続行する。
- **issue コメント**: durable な repo 変更を要求しないコメント完結型。実装・commit を開始せず、plugin mode では `issuekit:issue-investigate <N>`、APM plain-skill mode では `issue-investigate <N>` を案内して停止する。
- **要確認**: 両方に該当する、または判別不能。実装・commit を開始せず、`issuekit:issue-refine <N>`（APM plain-skill mode では `issue-refine <N>`）を案内して停止する。

### 2. Depends on (依存 issue) の確認

issue 本文に `Depends on:` 行がある場合、列挙された依存 issue がすべて close 済みかを確認する。

- 抽出: `gh issue view "$ISSUE_NUMBER"` の出力から `Depends on:` で始まる行をパースし、`#<数字>` を列挙する。
- 判定は **本文の状態表記ではなく `gh issue view <番号> --json state` の実体で行う**。本文に状態を書き写さない設計（`issuekit:issue-create` 側）と整合させ、表記漏れの影響を受けないため。

```bash
gh issue view <依存 issue 番号> --json state --jq '.state'
# → "OPEN" or "CLOSED"
```

- **1 件でも `OPEN` の場合**: 着手しない。どの依存 issue が未 close かをユーザーに報告し、判断（先に依存を片付ける / 強行する / 中止）を仰ぐ。
- **すべて `CLOSED` の場合**: 次のステップへ進む。
- **`Depends on:` 行が無い場合**: 何もせず次のステップへ進む。

### 3. 親 issue の確認

issue 本文に `親: #<番号>` の記載、または GitHub の sub-issue として親が存在する場合は、必ず親 issue をコメント込みで取得し、文脈を踏まえる。

```bash
# 親 issue が本文に記載されている場合
gh issue view <親 issue 番号> --comments

# sub-issue として登録されているかの確認 (任意)
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
gh api "repos/${REPO}/issues/${ISSUE_NUMBER}/parent" --jq '{number, title, state}' || true
```

### 4. 実装隔離 preflight (必須)

実装・ファイル書き込み・commit の **前** に runtime、現在 branch、worktree 状態、並列 worker かを分類する。default branch を直接変更しないことと、書き込みを伴う並列 worker が同じ working tree を共有しないことをここで保証する。後続 step 8 の `cross-review` に必要な CLI も同時に確認する。runtime は実行中 agent が明示的に把握している値を使い、`PATH` 上の CLI の存在順から推測しない。

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name') || { echo "default branch を取得できませんでした。" >&2; exit 1; }
[ -n "$DEFAULT_BRANCH" ] || { echo "default branch が空です。" >&2; exit 1; }
GIT_COMMON_DIR=$(git rev-parse --git-common-dir) || { echo "git common dir を取得できませんでした。" >&2; exit 1; }
GIT_DIR=$(git rev-parse --git-dir) || { echo "git dir を取得できませんでした。" >&2; exit 1; }
if CURRENT_BRANCH=$(git symbolic-ref --quiet --short HEAD); then
  : # branch checkout
elif [ "$GIT_COMMON_DIR" != "$GIT_DIR" ]; then
  CURRENT_BRANCH='' # Codex App 等の detached HEAD linked worktree は worktree 判定で扱う
else
  echo "main working tree が detached HEAD のため安全に分類できません。" >&2
  exit 1
fi
```

ここに到達した時点で、対象 issue は step 1 を通過した `Status: Ready` + 完了形 `PR` である。Draft / フォーマット不完全 / コメント上の未解決事項 / コメント完結型 / 要確認はすでに停止済みである。

分類後は次の表を **上から順に**評価する。ここでいう「専用 worktree」は `GIT_COMMON_DIR` と `GIT_DIR` が異なるだけでなく、runtime の session / worker 情報、branch / path、または呼び出し文脈から、その worker と対象 issue / task に排他的に割り当てられたと確認できる linked worktree を指す。現在の対象への割り当てを確認できない、または別 task 用なら停止し、別 worktree で再開する。dispatcher から起動された Codex CLI worker は prompt の対象 issue、専用 worker 宣言、expected branch を割り当て根拠として使う。

| 現在位置 / 呼び出し方 | 判定 |
| --- | --- |
| 並列 worker | **最優先。1 worker = 1 worktree を必須**とする。その worker 専用と確認できる linked worktree 内でなければ、branch 名にかかわらず実装・commit 前に停止する。同じ worktree を別 worker と共有しない。 |
| 単独 session ですでに専用 worktree 内 | detached HEAD を含め、二重作成せずその worktree で続行する。 |
| default branch 以外の既存 feature branch、かつ単独実装 | ユーザーの branch を上書きせず、そのまま続行する。`CURRENT_BRANCH` が空ならこの判定に入れない。 |
| default branch | runtime 別手順で専用 worktree へ移る。安全に移行できなければ停止する。 |

dispatcher から `codex exec --approve-for-me --worktree` で起動された Codex CLI worker は、上表で linked worktree と専用割り当てを確認した直後、最初の実装 write / commit より前に expected branch を確立する。`EXPECTED_BRANCH` は worker prompt から受け取り、空や不正なら停止する。

この worker では、`git fetch` / `git switch` / `git add` / `git commit` / `git push` と、その他の Git metadata を変更する操作を、通常の sandbox command として一度失敗させてから再試行してはならない。各操作は**最初の実行から、その exact command だけ**を対象に narrowly scoped escalation を要求し、Auto-review の判定を受ける。複数の Git mutation を shell operator、pipeline、subshell、wrapper script 等による複合 command にまとめず、1 command ずつ要求する。source file の編集、test、lint、inspection、acceptance-check と cross-review 用 diff の一時 file 生成は `workspace-write` 内に留め、Git metadata 以外へ escalation を広げない。cross-review の Codex reviewer process 起動だけは、nested sandbox failure を避けるため `cross-review` skill の規則どおり exact command 単位の scoped escalation を使い、子 reviewer 自体を `--ask-for-approval never` + `--sandbox read-only` に固定する。

Auto-review が unavailable / denied / timeout の場合、または承認後も Git metadata write が失敗した場合は、その場で worker を blocked とし、通常実行での再試行や権限拡大をしない。blocker には次を記録する。

- 失敗した exact Git command
- Auto-review の状態、または reviewer が返した rationale
- `git rev-parse --git-dir` と `git rev-parse --git-common-dir` の出力、および両者が同一か linked worktree として分離しているか

`danger-full-access`、`--dangerously-bypass-approvals-and-sandbox`、repository / 共有 checkout / Git metadata directory の writable root 追加、`--add-dir`、alternate Git directory、手動 `git worktree` fallback は適用しない。

```bash
git check-ref-format --branch "$EXPECTED_BRANCH" >/dev/null 2>&1 || { echo "expected branch が不正です。" >&2; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "branch 切り替え前の worktree が dirty です。" >&2; exit 1; }
if [ "$CURRENT_BRANCH" = "$EXPECTED_BRANCH" ] || git show-ref --verify --quiet "refs/heads/$EXPECTED_BRANCH"; then
  echo "expected branch が worker の確立前から存在し、今回の native worker 専用と確認できません。" >&2
  exit 1
fi
git fetch origin "$DEFAULT_BRANCH"
git switch -c "$EXPECTED_BRANCH" "origin/$DEFAULT_BRANCH"
[ "$(git symbolic-ref --quiet --short HEAD)" = "$EXPECTED_BRANCH" ] || exit 1
```

上の `git fetch` と `git switch` は、コードブロック全体をまとめて実行するのではなく、それぞれを完全に別の exact command として scoped escalation 付きで最初から実行する。いずれかが non-zero なら、その時点で上記 blocker 情報を記録して即座に blocked とする。read-only の `check-ref-format` / `status` / `show-ref` / branch 確認は sandbox 内で実行する。

native worker は dispatcher が不存在を確認した expected branch を `origin/$DEFAULT_BRANCH` から新規作成する。起動時点ですでに expected branch 上にいる場合や ref が存在する場合は、同名の残存 branch、競合 race、別 task の commit を取り込まないよう自動 switch / 再利用せず停止する。branch 作成失敗、別 worktree での使用、または `origin/$DEFAULT_BRANCH` の取得失敗も、別名の自動生成や branch の削除・上書きを行わず実装前の blocker とする。

default branch 上の runtime 別分岐:

- **Claude Code 対話 session**: `EnterWorktree` が利用できる場合だけ `issuekit:worktree-start` (APM plain-skill mode では `worktree-start`) を呼ぶ。issue title から作った `<title-slug>-<issue 番号>` を **タスク説明モード**で渡し、切り替え後に `GIT_COMMON_DIR != GIT_DIR` を再確認してから続行する。`EnterWorktree` が無い旧版や、切り替えに失敗した場合は停止し、`claude --worktree <title-slug>-<issue 番号>` で新しい session を開始して `issue-implement <issue 番号>` を再実行するよう案内する。
- **Codex CLI**: worktree 作成を skip して続行してはならない。起動済み親 session の cwd を skill が安全に移せるとは仮定せず、対象 issue 1件と、上記の共通規則で確定した `ISSUE_CLOSE_INTENT=true|false` および `ISSUE_CLOSE_INTENT_REASON=<根拠>` を `issuekit:issue-dispatch <issue番号>`（APM plain-skill mode では `issue-dispatch <issue番号>`）へ引き継ぐ。dispatcher はこの継承値を機械的な issue 番号の形式から再判定しない。dispatcher が `codex exec --approve-for-me --worktree` で native managed worktree の `issue-implement <issue番号>` worker を1つだけ起動し、expected branch を prompt へ渡して PR / CI まで待機・集約する。本 invocation は実装を開始せず、dispatcher の結果をそのまま完了報告する。native worker 起動に失敗した場合は独自 worktree へ fallback しない。

- **Codex App**: App の **Worktree** で開始済み、または **Handoff** で managed worktree へ移動済みなら続行する。Local の default branch 上なら実装前に停止し、App UI で Worktree chat を開始するか Handoff してから再実行するよう案内する。managed worktree / Handoff は runtime 所有であり、skill 自身は作成・操作しない。
- **Claude Code Agent view / Desktop**: Agent view の background session と Desktop の新規 Code session は runtime が自動隔離する。実際に linked worktree へ移ったことを確認して続行する。移行前の main checkout では書き込みを始めない。
- **未対応 runtime**: default branch 上では停止する。対応する reviewer-session launch 手順も無ければ、cross-review preflight の時点でも停止する。

`Status: Draft` / フォーマット不完全 / コメント上の blocker は step 1 で early abort 済みなので、この preflight に到達しない。`worktree-start → issue-implement` または `issue-dispatch → issue-implement` で入った場合は linked worktree 判定により二重作成・再 dispatch せず、その worktree で続行する。

### 5. 実装（必要に応じて適宜 commit）

issue 本文の「実装方針」「受け入れ条件」「スコープ外」と、step 1 / step 3 で確認したコメントの文脈に従い実装する。実装中に方針の揺らぎや不明点が出た場合は、勝手に拡張せずユーザーに確認する。

「実装方針」が **優先順位付き（または順序付き）の解消候補リスト** として書かれている場合は、上から順に試す。各候補の試行後に `acceptance-check` skill 相当の検証で受け入れ条件の充足を確認し、満たせない場合は次の候補へ進む。候補を恣意的に選ばず、最初から順に試すこと。すべて試しても受け入れ条件を満たせない場合は、勝手に新しい方針を追加せずユーザーに報告する。

実装完了の判定は **受け入れ条件のチェックリストをすべて満たしていること**。

#### commit 粒度のガイド

実装途中で「ここまでは固まった」という区切りがついたら、その時点で commit する。最終 PR 単位ではなく、**試行錯誤や中間段階を履歴に残す** ことを優先する。`acceptance-check` は最終状態に対して受け入れ条件を、`cross-review` は base...HEAD の最終 diff を対象に回るため、commit が何個に分かれていても判定結果は変わらない。

粒度の目安:

- **受け入れ条件 1 項目 ≒ 1 commit**: 受け入れ条件のチェック項目に対応する変更が一段落したら commit する。
- **リファクタや前処理は別 commit に分離**: 機能追加と無関係な整理（型の整え、import の並び替え、関連箇所のリネーム等）は同じ commit に混ぜず、独立した commit として切り出す。
- **試行錯誤の途中段階も残してよい**: 「方針 A を試した → やめて方針 B に切り替えた」のような経過は、後追いの価値があるなら commit として残す（ただし明らかに作業途中の壊れた状態は commit しない）。

commit メッセージは Conventional Commit-like prefix (`feat:` / `fix:` / `chore:` / `refactor:` / `docs:` 等) を使用し、scope を絞った具体的な記述にする。

Codex managed linked worktree worker で commit する際は、対象 path を限定した `git add <path...>` と `git commit -m <message>` を別々の exact command として、どちらも最初の実行から scoped escalation 付きで要求する。`git add .` のように対象を不必要に広げない。

### 6. lint / format / 型チェック

プロジェクトに設定されているフォーマッタ・リンタ・型チェックを実行し、すべてパスすることを確認する。これらが通らない場合は実装完了とみなさない。lint/format による自動修正が発生した場合は追加 commit として残す。

### 7. 受け入れ条件チェック (issuekit:acceptance-check skill)

実装と適宜 commit が一段落した時点で、受け入れ条件の充足を最終確認するステップ。`issuekit:acceptance-check` skill を呼び出し、issue 本文の `## 受け入れ条件` を抽出して各項目を自動検査する。APM plain-skill mode では `acceptance-check` を呼び出す。

**`acceptance-check` を `cross-review` より前に置く理由**: 受け入れ条件 ✗ の場合は実装に戻って修正することになり、追加変更が発生した時点で cross-review の対象 diff も変わる。先に cross-review を回すと、その指摘対応・受け入れ条件修正の双方で diff が動くたびに cross-review がやり直しになり無駄打ちが発生する。受け入れ条件を確定させてから cross-review を回すことで、レビュー対象 diff の安定性を確保する。

- **`✗` が 1 件でもある場合**: 受け入れ条件未達。step 5 の実装に戻って **追加 commit** で修正する（`git commit --amend` / `rebase` / `fixup` は使わない）。修正完了後にこの step 7 をやり直す。
- **`?` (要人間判定) のみの場合**: Claude 自身で動作確認方法を実行できる範囲は実行し、ブラウザ操作や主観評価など人間判定が必要なものは判断結果を添えて進む。判断が困難なものはユーザーに確認する。
- **すべて `✓` の場合**: 次の step 8 (cross-review) に進む。

`issuekit:acceptance-check` 自体は read-only であり、issue body や code を変更しない。failed 項目の修正は本 skill 側の責任。

### 8. cross-review (issuekit:cross-review skill)

受け入れ条件をすべて満たした最終形に対して、実装セッションから独立した reviewer session による cross-review を実施する。`issuekit:cross-review` skill を呼び出す。APM plain-skill mode では `cross-review` を呼び出す。

- **critical** の指摘がある場合: **追加 commit** で修正してから次に進む（`git commit --amend` / `rebase` / `fixup` は使わない）。修正後に受け入れ条件への影響が無いか軽く確認する（影響が疑わしい場合は step 7 をやり直す）。
- **warning** の指摘がある場合: 実装 agent 自身で対応要否を判断する。妥当な指摘は自律的に **追加 commit** で修正し、見送る場合は理由を添えて報告する（ユーザー確認は不要）。
- **info** のみの場合: 指摘を共有し、PR 作成に進む。

reviewer session は実行中 agent runtime に対応する CLI で起動する。Codex CLI で実装している場合は `codex --ask-for-approval never exec --sandbox read-only`、Claude Code で実装している場合は `claude -p` を使う。base branch は `gh repo view --json defaultBranchRef` から動的に解決される（`master` / `develop` / `trunk` でもそのまま動く）。default branch 解決が失敗した場合は同 skill が明示的に停止するので、エラー出力に従って原因を解消してから再実行する。

Codex managed worker では `cross-review` skill の規則に従い、diff を `workspace-write` 内の 0600 一時 file に生成し、reviewer process 起動だけを最初から1つの exact command として scoped escalation に要求する。sandbox 外で `git diff` や repository command を実行しない。Auto-review の拒否・timeout、または承認後の command failure は blocker とし、通常 sandbox での再試行、権限拡大、別 reviewer への暗黙 fallback を行わない。子 reviewer の `--ask-for-approval never` と `--sandbox read-only` は維持する。Claude Code の `claude -p --allowedTools "Read"` 経路は変更しない。

### 9. PR 作成

```bash
gh pr create --title "<title>" --body-file - <<'EOF'
<日本語の description>
EOF
```

- **PR description は日本語**で記載する（CLAUDE.md の常時適用ルール）。
- description の先頭に `close #<issue 番号>` を記載するのは `ISSUE_CLOSE_INTENT=true` の場合だけとする。対応 issue の完全実装は、直接の番号 / URL 指定、提示済み候補への参照、dispatcher の機械選定のいずれでも `true` とする。対応 issue がない場合や、部分実装・epic の一部・関連付けだけの PR は `false` とする。dispatcher worker は prompt の flag と reason をそのまま使い、機械的に渡された `issue-implement <N>` だけを close intent の根拠にしない。
- description には目的、影響パッケージパス、ローカル検証手順を含める。
- Codex managed linked-worktree worker では、PR 作成前の `git push -u origin "$EXPECTED_BRANCH"` も、最初の実行からその exact command だけの scoped escalation として要求する。Auto-review または Git metadata write が失敗した場合は PR を作成せず、step 4 の形式で blocked を報告する。それ以外の runtime / checkout では、現在 branch と対象 branch が一致し、default branch でないことを安全に確認したうえで従来どおり push する。

### 10. CI 確認

```bash
gh pr checks <PR 番号 or URL> --watch
```

- CI が成功するまで監視する。
- **失敗した場合**: ログを確認して修正し、追加 commit で対応する（`git commit --amend` / `rebase` / `fixup` は使わない）。
- **CI が開始されない場合**: ブランチのコンフリクトが原因の可能性が高い。`gh pr view` でコンフリクト状況を確認し、解消してから再度 CI を待つ。

### 11. 完了報告

PR URL と CI 結果（成功 / 修正後成功）をユーザーに返す。

## やらないこと

- default branch 名 (`main` / `master` / `develop` 等) を hardcode した branch ガード。step 4 の判定は `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'` の結果と動的に比較する。
- default branch 上で worktree 化を単に skip して実装へ進むこと。runtime が安全に切り替えられなければ、書き込み・commit 前に停止する。Codex CLI は単一 issue を `issue-dispatch` へ引き継ぐ。
- Codex CLI の起動済み親 session の cwd を変更すること、または Codex App の managed worktree / Handoff を skill が作成・操作すること。
- dispatcher worker が detached HEAD / expected branch 以外のまま実装 write や commit を始めること。linked worktree と専用割り当てを確認後、expected branch を確立できなければ停止する。
- Codex CLI dispatch で `git worktree add` や `codex exec -C <worktree-path>` の互換 fallback を使うこと。
- Codex managed linked worktree で Git metadata mutation をまず sandbox 内で通常実行して失敗させること、複数 command を1つの escalation にまとめること、または Auto-review の unavailable / denied / timeout 後に別方式で再試行すること。
- Git metadata write のために `danger-full-access`、`--dangerously-bypass-approvals-and-sandbox`、repository / 共有 checkout / Git metadata directory の writable root 追加、`--add-dir`、alternate Git directory を使うこと。
- 書き込みを伴う並列 worker が同じ worktree を共有すること。並列 worker は branch 名にかかわらず 1 worker = 1 worktree とする。
- 単独実装で、すでに default branch 以外の feature branch にいるユーザーへの worktree 強制切り替え。step 4 の分類で既存 branch を尊重する。
- step 4 で `worktree-start` を呼ぶ際に issue 番号を渡すこと。issue 番号を渡すと `worktree-start` 側の Status 判定経路に入り `issue-implement` への再帰連鎖が起きるため、タスク説明モードで slug (`<title>-<issue 番号>`) のみを渡す。
- issue 本文や PR への `close` キーワードの無条件な自動付与。`ISSUE_CLOSE_INTENT=true` の完全実装 PR にだけ付ける。
- 受け入れ条件を満たさない状態での PR 作成。
- コメント完結型または完了形が要確認な issue の実装・commit・PR 化。step 1 で停止し、`issue-investigate` または `issue-refine` を案内する。
- 実行中 agent runtime に対応する CLI が未導入な状態での cross-review 省略（該当する `issuekit:cross-review` / `cross-review` skill の失敗時対応に従い、明確に失敗させる）。
- **`acceptance-check` / `cross-review` / CI の指摘修正のために `git commit --amend` / `git rebase` / `git rebase -i` / `--fixup` / `git reset` 等で履歴を整形すること**。レビュー対応・修正対応はすべて **追加 commit** として残し、試行錯誤と修正経緯を後から追えるようにする。issuekit リポジトリは merge commit 運用（squash ではない）なので、commit 履歴は merge 後も価値を持つ。
