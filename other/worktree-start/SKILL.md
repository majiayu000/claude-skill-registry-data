---
name: worktree-start
description: "Claude Code 専用。起動済みの対話 session から、タスク説明または issue URL / 番号で命名した git worktree へ `EnterWorktree` で切り替える。既存 linked worktree では作成だけを no-op にする。Ready issue は完了形を判定し、PR なら `issue-implement`、コメント完結型なら `issue-investigate` へ連鎖し、要確認なら `issue-refine` を案内する。"
version: 3.1.0
---

# Worktree Start Skill

Claude Code の `EnterWorktree` ツールを使い、起動済み対話 session の cwd を専用 git worktree に切り替えてタスクを開始する skill。`issue-implement` は PR 完結、`issue-investigate` はコメント完結の orchestrator であり、本 skill は **issue 起点・タスク起点どちらでも入れる entry point** として完了形に応じた経路へつなぐ。

## スコープ

- **含む**: タスク説明 / issue URL / issue 番号からのブランチ名生成、`EnterWorktree` による cwd 切り替え、既存 worktree 内での no-op 判定、issue 入力時の Status・コメント・完了形の確認、着手可能な Ready issue の適切な orchestrator への引き継ぎ。
- **含まない**:
  - **外部タブ管理ツール (ターミナルマルチプレクサ等) との連携**: 並列タブの起動はユーザー操作のまま。
  - **Codex CLI / 他 agent 用の fallback 実装**: `EnterWorktree` は Claude Code 固有で、他 runtime には対応 primitive が存在しない。
  - **既存 worktree 間の移動**: 現行 `EnterWorktree` は `.claude/worktrees/` 配下の別 worktree へ path 指定で切り替えられるが、本 skill はタスクの二重割り当てを防ぐため、すでに linked worktree 内なら no-op とする。
  - **作成済み worktree のクリーンアップ**: `ExitWorktree` / `git worktree remove` 等は呼ばない。
  - **Draft / フォーマット不完全 / 完了形が要確認な issue の着手連鎖**: worktree 作成のみ行い `issue-refine` を案内する。

## 利用タイミング

- ユーザーが「worktree でタスクを始めたい」「並列タブで別タスクを切り出したい」のような起動指示を与えたとき。
- ユーザーが **issue URL** (`https://github.com/<owner>/<repo>/issues/<N>`) または **issue 番号** をセッション冒頭に貼り、新規 worktree で着手したいとき。
- すでにターミナルエミュレータで素の `claude` が起動しており、これから worktree に入りたい状況。
- `issuekit:issue-implement` skill (APM plain-skill mode では `issue-implement`) の冒頭ステップから呼ばれたとき。この場合は **Status / Depends on / 親 issue の確認は上流で完了済み**であり、本 skill 側では入力を「タスク説明モード」(後述 step 2) として扱って worktree 切り替え機能のみを提供する。詳細は後述「上流 skill (`issue-implement`) からの呼び出し」を参照。

## Runtime ごとの位置づけ

本 skill 自体は **Claude Code の対話 session 専用** で、Codex CLI / Codex App / Cursor / Gemini など他の agent runtime では利用できない。ただし worktree 隔離は各 runtime がそれぞれ所有する機能であり、次の境界を混同しない。

| Runtime / 機能 | 隔離方法 | 本 skill の役割 |
| --- | --- | --- |
| Claude Code CLI 対話 session | 起動時は `claude --worktree <name>`、起動後は `EnterWorktree` | 起動後の `EnterWorktree` 呼び出しだけを担当する。 |
| Claude Code subagent | frontmatter の `isolation: worktree`、または spawn 時の `isolation: "worktree"` | 作成しない。subagent runtime に委ねる。 |
| Claude Code Agent view | background session が書き込み前に自動で専用 worktree へ移る | 作成しない。移行後の linked worktree では no-op。 |
| Claude Desktop Code session | 新規 session ごとに自動 worktree | 作成しない。Desktop runtime に委ねる。 |
| Codex CLI | `issue-dispatch` が `codex exec --approve-for-me --worktree` で native managed worktree の worker を起動 | 本 skill は fallback を実行しない。単一 issue の `issue-implement` は default branch 上で `issuekit:issue-dispatch`（APM plain-skill mode では `issue-dispatch`）へ引き継ぐ。 |
| Codex App | App の managed worktree / Handoff | App 所有。skill から作成・操作しない。 |

Claude Code の現在の worktree 仕様は [公式 worktree ドキュメント](https://code.claude.com/docs/en/worktrees)、Agent view は [公式 Agent view ドキュメント](https://code.claude.com/docs/en/agent-view) を参照する。

## 上流 skill (`issue-implement`) からの呼び出し

本 skill は単独 entry point として呼ばれるほか、`issuekit:issue-implement` skill の冒頭ステップ (issue-implement の step 4) から呼ばれることがある。後者の場合、上流が以下を **既に確認済み**であることを前提に動作する:

- 対象 issue の `Status: Ready` と、コメント上に未解決 blocker / 本文矛盾 / 方針保留 / 受け入れ条件の未反映変更がないこと
- `Depends on:` がすべて close 済み
- 親 issue の文脈取り込み

そのため `issue-implement` から呼ばれた際は、本 skill 側で再度 `gh issue view` による Status / Depends on / 親 issue の検証は行わない（**Status チェックは上流に委譲**）。具体的には、上流から渡されるのは **issue 番号ではなく事前生成済みのブランチ名 slug** (`<title-slug>-<issue 番号>` 形式) のみであり、本 skill はそれを step 2 の「タスク説明モード」と同じ経路で扱う。issue 番号を伴う入力経路 (Status・完了形判定 → 対応 orchestrator への連鎖) には入らないため、`issue-implement → worktree-start → issue-implement` の再帰連鎖は発生しない。

万一上流が誤って issue 番号を渡してしまった場合、step 2 で完了形を再判定して対応 orchestrator を余分に呼ぶことになる。PR 経路で `issue-implement` が再度本 skill を呼び出しても、step 1 の no-op 判定で循環は止まる。とはいえ無駄な再呼び出しと誤ルーティングを避けるため、上流からは必ずブランチ名 slug のみを渡す運用にすること (詳細は `issue-implement` の "やらないこと" 節を参照)。

## 依存

- **`EnterWorktree` が利用できる Claude Code**: tool が無い場合は `claude --version` で確認し、最新版へ更新して session を再起動するか、`claude --worktree <name>` で新しい session を開始するよう案内する。
- **`git`**: worktree 作成のために必要（`EnterWorktree` の内部で利用される）。
- **git リポジトリ内であること**: 起動 cwd が git working tree でない場合、`EnterWorktree` は失敗する。

## 入力

ユーザーから受け取るのは以下のいずれか:

- **タスク説明** (issue 不要): 「Slack 連携の OAuth フローを実装したい」「dependabot PR をまとめてレビューする」など。
- **issue URL**: `https://github.com/<owner>/<repo>/issues/<N>` 形式。
- **issue 番号**: `#42` / `42` 単体。

issue URL / 番号が渡された場合は、本 skill 側で `gh issue view --comments` を呼び出して title (ブランチ名生成用)、Status と完了形 (連鎖判定用)、コメントの補足文脈を取得する。**Status と完了形は `issue-create` の定義に従う**。

## 実行手順

### 1. 既存 worktree のチェック (issuekit 固有の no-op 判定)

**現在の session が linked worktree 内なら新しい worktree は作らない**。これは `EnterWorktree` primitive の一般的制約ではなく、「すでにタスク用 worktree にいる session を別 worktree へ動かさず、二重作成もしない」という issuekit 固有の安全方針である。現行 Claude Code は `EnterWorktree` に既存の `.claude/worktrees/` 配下 path を渡して別 worktree へ切り替えることもできるが、本 skill はその機能を使わない。

その後の制御は入力ごとに分ける:

- **上流 `issue-implement` からの slug / タスク説明**: worktree 切り替えだけを skip して呼び出し元へ戻る。上流はその worktree で実装を続ける。
- **直接渡されたタスク説明**: worktree 切り替えだけを skip し、この worktree で次に何をするか確認して終了する。
- **直接渡された issue URL / 番号**: runtime / session 情報、現在 branch / path、または呼び出し文脈から、この worktree が対象 issue に専用割り当てされていると確認できる場合だけ step 2 の Status / コメント / 完了形確認へ進む。step 3 / 4 の作成は skip し、Ready なら step 5 で対応 orchestrator へ引き継ぐ。別 issue 用、または割り当てを確認できない場合は連鎖せず停止し、対象 issue 用の別 worktree で再開するよう案内する。

判定は以下のいずれかで行う:

- `git rev-parse --git-common-dir` と `git rev-parse --git-dir` を比較し、異なれば worktree 内。
- もしくは `git worktree list` の現在 path がメイン working tree と異なるかを確認。

`EnterWorktree` を投機的に呼ばず skill 側で先に判定し、ユーザーには「すでに専用 worktree 内のため、作成は skip してこの worktree を使います」と返す。

### 2. 入力タイプ、Status、完了形の判定

ユーザー入力を以下に分類する:

- **タスク説明 (issue なし)**: そのまま step 3 のブランチ名生成へ進む。issue 連鎖は行わない (step 5 はスキップ)。`issue-implement` 上流から呼ばれた場合 (= 事前生成済みブランチ名 slug が渡される) もこの経路で扱い、Status 判定や `gh issue view` は走らせない。
- **issue URL / 番号**: URL から番号を抽出し、`gh issue view <N> --comments` で本文、title、コメントを取得する。すでに linked worktree 内なら step 3 / 4 の作成だけを skip する。本文先頭の `Status:` を確認し、コメントに本文未反映の補足や矛盾がないかも確認して以下に分岐する。本文とコメントが矛盾する場合は、`updatedAt` やコメント時系列を踏まえて最新の意図を推定し、判断できないものだけを要確認として扱う:
  - **`Status: Ready` かつコメントに未解決事項がない**: 受け入れ条件と `## スコープ外` を `issue-create` の「成果物と完了形」に照らす。repo 変更が完了条件なら **PR**、結果コメントだけなら **issue コメント**、両方または判別不能なら **要確認** とする。
  - **`Status: Ready` だがコメントに未解決 blocker / 本文との矛盾 / 方針保留 / 受け入れ条件の未反映変更がある**: 完了形にかかわらず着手連鎖を行わない。既存 linked worktree でなければ worktree を作成して切り替え、既存なら保持したうえで、ユーザー確認または `issue-refine` を案内する。
  - **`Status: Draft`**: 着手連鎖を行わない。既存 linked worktree でなければ worktree を作成して切り替え、既存なら保持したうえで、`issuekit:issue-refine`（APM plain-skill mode では `issue-refine`）を案内する。
  - **`Status:` 表記なし / フォーマット不完全**: 同様に連鎖せず、`issue-refine` を案内する。

### 3. ブランチ名の決定

- **タスク説明から**: Claude Code 自身が短い slug を生成する。形式は英小文字 + 数字 + ハイフン (`kebab-case`) で 3〜5 単語程度。タスク説明の核となる名詞・動詞を抽出して要約する。
  - 例: 「Slack 連携の OAuth フロー実装」 → `slack-oauth-flow`
  - 例: 「dependabot PR の取りまとめレビュー」 → `dependabot-roundup-review`
- **issue 入力から**: issue title から同形式の slug を生成し、末尾に `-<issue 番号>` を付与する。issue とブランチを後から照合できるようにする狙い。
  - 例: issue #42「Slack 連携の OAuth フロー」 → `slack-oauth-flow-42`
- **ユーザー明示指定**: 「ブランチ名は `xxx` にして」と渡された場合は LLM 命名を行わずそのまま採用する。
- Claude Code の既定では `.claude/worktrees/<name>/` に `worktree-<name>` branch が作られる。この命名をそのまま許容する。既存名を指定すると既存 worktree が開かれる場合があるため、呼び出し前に `git worktree list` を確認する。runtime / session 文脈から現在の worker 専用と確認できる場合だけ再利用し、排他的な割り当てを確認できない場合は共有せず、衝突しない別名をユーザーへ求める。

### 4. `EnterWorktree` の呼び出し

step 1 で既存 linked worktree と判定済みなら本 step は skip し、現在の worktree を保持する。それ以外では、確定したブランチ名を `name` 引数に渡して `EnterWorktree` を呼ぶ。

```
EnterWorktree({ name: "slack-oauth-flow-42" })
```

成功すれば現在のセッションの cwd が新規 worktree (`worktree-slack-oauth-flow-42` 系のブランチ + 対応ディレクトリ) に切り替わる。以降のツール呼び出しは新 worktree 上で動作する。

切り替え後は `git rev-parse --git-common-dir` と `git rev-parse --git-dir` が異なることを確認する。worktree は fresh checkout なので、依存関係の install、build cache、環境初期化が必要なら実装前に行う。gitignored な `.env` 等が必要なら repository root の `.worktreeinclude` に `.gitignore` 構文で列挙する。tracked file は対象にせず、secret を含む場合はコピー先も同じ権限境界にあることを確認する。

### 5. (issue Ready 時のみ) 完了形に応じた引き継ぎ

step 2 で **issue URL / 番号 + `Status: Ready` + コメント上の未解決事項なし** だった場合、完了形に応じて分岐する。

- **PR**: `issuekit:issue-implement <N>`（APM plain-skill mode では `issue-implement <N>`）へ引き継ぐ。
- **issue コメント**: `issuekit:issue-investigate <N>`（APM plain-skill mode では `issue-investigate <N>`）へ引き継ぐ。
- **要確認**: 自動連鎖せず `issuekit:issue-refine <N>`（APM plain-skill mode では `issue-refine <N>`）を案内する。

- PR または issue コメントと判定できた Ready issue は、引き継ぎ前にユーザー確認を挟まない。Ready は受け入れ条件が確定したシグナルであり、完了形が要確認なら `issue-refine` へ戻す。
- 連鎖後の Status / Depends on / 親 issue 再確認と各 cycle の完了処理は呼び出し先 orchestrator の責務。本 skill は worktree 切り替えと引き継ぎだけを行う。

それ以外 (タスク説明 / Draft / 表記なし / 完了形が要確認) は着手 orchestrator へ引き継がず、step 6 の完了報告のみで終わる。

### 6. 完了報告

ユーザーには以下を返す:

- 使用する worktree のパス (新規作成時は新 cwd) と branch 名。既存 linked worktree を再利用した場合は、その path と branch / detached HEAD 状態を返す。
- **issue Ready で連鎖した場合**: 判定した完了形と、`issue-implement <N>` または `issue-investigate <N>` を起動済みであること。
- **issue Ready だが完了形が要確認の場合**: 自動連鎖せず、`issue-refine` で完了形を整理する案内。新規作成または再利用した worktree は保持する。
- **issue Ready だがコメント上の要確認点があり連鎖しなかった場合**: 要確認点を列挙し、ユーザー確認または `issue-refine` で整理してから再度呼ぶ案内。新規作成または再利用した worktree は保持する。
- **issue Draft / 表記なしの場合**: `issue-refine` で整理してから再度呼ぶ案内。新規作成または再利用した worktree は保持する。
- **タスク説明の場合**: 「次は何をしますか?」の確認 (そのまま実装に入る、別 skill を呼ぶ、など)。

## Resume / cleanup の扱い

- worktree 内の session を `--resume` / `--continue` すると Claude Code はその worktree に戻る。元 worktree が無い場合は起動ディレクトリで再開する。`--fork-session` は起動ディレクトリから fork し、元 session の worktree は保持する。
- 対話 session 終了時、clean な unnamed worktree は自動削除され、named session や変更・新規 commit がある worktree は keep / remove の確認対象になる。`-p` の非対話実行には終了確認がないため自動 cleanup されず、必要なら `git worktree remove <path>` を使う。
- subagent / Agent view の runtime 管理 worktree は別の cleanup 規則を持つ。未変更なら自動削除され得るが、変更・未追跡 file・未 push commit がある場合は保持される。ユーザー変更を破棄する `--force` cleanup は自動実行しない。
- worktree ごとに repository files、dependencies、build cache が増えるため disk 使用量を確認し、不要になった worktree は作業を保存したうえで整理する。

## 失敗時の対応

- **`EnterWorktree` ツールが見つからない**: `claude --version` を確認し、`npm install -g @anthropic-ai/claude-code` で最新版へ更新して session を再起動するか、`claude --worktree <name>` で新しい session を開始するよう案内する。
- **切り替え後も linked worktree と確認できない**: 実装を開始せず停止し、`git worktree list` と Claude Code のエラーを確認する。既存 worktree ならその path で `claude` を開始し直す方法も案内する。
- **git リポジトリ外で呼ばれた**: `git rev-parse --is-inside-work-tree` で先に検知し、git repo 内で再実行するようユーザーへ案内する。
- **ブランチ名衝突**: `EnterWorktree` 側のエラー出力をそのままユーザーに見せ、別のブランチ名を提示してもらう（自動でサフィックス付与等は行わない。意図しない命名を避けるため）。
- **既存名が別 session / worker に使用されている、または排他的な割り当てを確認できない**: その worktree を開かず停止し、衝突しない別名をユーザーへ求める。同じ worktree を複数の書き込み session で共有しない。
- **現在の linked worktree が別 issue / task 用、または対象への割り当てを確認できない**: 直接渡された issue の orchestrator へ連鎖せず停止し、対象 issue 用の別 worktree で再開するよう案内する。

## やらないこと

- **既に worktree 内にいる session の別 worktree への移動**: primitive が可能でも、上記 step 1 で worktree 作成だけを issuekit 固有の no-op とする。直接 issue 入力は、現在の worktree が対象 issue 専用と確認できる場合に限り、Status・完了形確認と対応 orchestrator への連鎖を続ける。
- **外部タブ / ペインの自動起動**: 並列タブの起動はユーザー操作のまま。skill から外部のターミナルマルチプレクサ等を直接操作しない。
- **Draft / フォーマット不完全 / 完了形が要確認な issue の着手連鎖**: worktree 作成までで止め、`issue-refine` を案内する。Status と完了形は `issue-create` の定義に従う。
- **タスク説明 (issue なし) 入力時の着手 orchestrator 連鎖**: issue 番号が文字列として登場しても、URL / 番号として明示入力されていなければ `gh issue view` を呼ばずタスク説明として扱う。連鎖は行わない。
- **Codex CLI / 他 agent 用の fallback 実装**: 本 skill は Claude Code 専用。「Runtime ごとの位置づけ」セクション参照。
- **Codex App の managed worktree / Handoff の作成・操作**: App 所有の UI / lifecycle を skill の機能として扱わない。
- **`EnterWorktree` の `path` パラメータでクリーン命名を試みる**: `worktree-` prefix 強制を許容する方針 (issue #13 スコープ外)。
- **作成済み worktree のクリーンアップ**: `ExitWorktree` / `git worktree remove` 等は呼ばない。worktree のライフサイクル管理はユーザー責務。
