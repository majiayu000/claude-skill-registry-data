---
name: doc-declutter
description: >
  ドキュメントの肥大化を棚卸しするスキル。完了済み handoff の抽出→削除・古い行の trim・重複 doc の統廃合を、
  外部実体（PR merged / published:true / deploy / ファイル実在）を検証してから安全に行う。親が機械 surfacer
  と git/grep で完了シグナルを確定し、doc-curator（Evaluator）に KEEP/TRIM/DELETE/CONSOLIDATE を
  判定させ、承認後に削除・trim・参照更新・memory 同期まで適用する。doc-sync（コード起点の prose 陳腐化）とは別。
  Use when user asks to [ドキュメント棚卸し, handoff 整理, doc 肥大化, 完了 handoff を削除, doc declutter, /doc-declutter].
user-invocable: true
argument-hint: "[handoffs|reference|all] (既定: handoffs)"
domain: ops
---

ドキュメントの**ライフサイクル（肥大化・完了・重複）**を棚卸しする半自動オーケストレーションスキル。
親（あなた）が**外部実体の検証**と適用を担い、**処分の判定だけ**を Evaluator サブエージェント **`doc-curator`** に委ねる。

> **3 層の役割分担（混同しない）**
> - `scripts/check-doc-lifecycle.mjs` … 棚卸し候補の機械 surfacer（鮮度・orphan・PR/commit 言及。**非ブロッキング**）
> - **本スキル + `doc-curator`** … 候補の処分判定（KEEP/TRIM/DELETE/CONSOLIDATE・LLM・棚卸し時に手動）
> - `scripts/check-doc-refs.mjs` … 削除後の壊れ参照ゼロ検証（機械・pre-commit。**`docs/handoffs/**` は参照先チェック対象外**＝point-in-time 記録）
>
> **doc-sync との違い**: `/doc-sync` は**コード変更**で doc が旧仕様化していないか（prose 陳腐化）。本スキルは **doc 自体の処分**（完了・重複・肥大）。トリガーが違う。

## いつ回すか（発火規律）

- **回す**: `docs/handoffs/**` が蓄積した（週次 PDCA の `/weekly-review` Agent H が抽出候補を surface したとき）／reference・project に重複や完了済み記述が溜まったと感じたとき。
- **回さない**: 純コンテンツ（`content/site/**` MDX・`content/note,sns/**` 素材）。これらは肥大化管理の対象外。

## 鉄則（安全則）

> **handoff の既定処分は extract→削除（2026-07-11 改定・archive 廃止）**: handoff は溜めない。生きたタスクは `.claude/todo/backlog.md` へ、手順・runbook は `.claude/knowledge/reference/` の該当 SSOT へ、個人知見は memory へ抽出し、本体は**残作業の有無に関わらず** `git rm`（**記録は git 履歴が持つ**＝復元可能）。**残作業がある＝KEEP ではない**（タスクは backlog が持つ）。KEEP は「当該セッションで今まさに編集中・未だ backlog 未抽出」のごく直近に限る。真実源 → `.claude/knowledge/reference/information-architecture.md`「handoff のライフサイクル」。reference/project doc は従来どおり完了判定で KEEP/TRIM/DELETE。

1. **自己申告で完了と決めない**。doc が「完了」と書いていても、**外部実体を git/grep で検証**してから処分する（PR が merged か・成果物が `published:true`／noteUrl 付きか・参照 commit が develop/main に入っているか・ファイルが実在するか）。**検証できない残作業・外部尻尾がある handoff は、残作業を backlog に「未確認」として抽出してから削除**（情報を落とさない）。判断に迷う場合は KEEP でユーザーへ。
2. **抽出が先・削除が後**。タスク／手順／知見の抽出漏れがないことを確認してから `git rm`。削除は git 履歴から復元可能だが、抽出漏れは気づけない。
3. **参照の扱い**: `docs/handoffs/**` への出典引用は削除後も正当（`check-doc-refs` 対象外）＝張り替え不要。**reference/project doc を削除する場合**は全参照を SSOT へ同一 commit で張り替える（こちらは check-doc-refs 対象）。
4. **`git add` はしない。`git commit -- <pathspec>` で対象だけ**コミット（並行セッションの未 staged 変更を巻き込まない／CLAUDE.md §3・§10）。
5. **memory も同期**。`~/.claude/.../memory/` がその doc を参照していたら、本体 `.md` と `MEMORY.md` の索引行を実態へ更新（memory は repo 外＝commit 不要）。
6. **EOL 保持**。`docs/**` の handoff/reference は LF。trim 後に CRLF 混入していないか確認（混在は pre-commit reject）。

## 手順（親が実行）

### 1. 候補を機械で surface する

```bash
node scripts/check-doc-lifecycle.mjs            # 既定 handoffs・age>=14d or orphan
node scripts/check-doc-lifecycle.mjs --days 21  # 鮮度閾値を変える
```

orphan（参照元 0）・stale-age・言及 PR/commit が出る。**これは候補リストであって判定ではない**。

### 2. 各候補の「外部実体シグナル」を確定する（親が Bash/git/grep）

候補ごとに、doc の主張を**実体で裏取り**する。代表的な確認:

```bash
# 言及 PR の merged 状態（network 可能な環境で）
gh pr view <N> --json number,state,mergedAt 2>/dev/null

# 言及 commit が develop/main に入っているか（squash で SHA が変わる点に注意 → 成果物の実在で確認）
git merge-base --is-ancestor <sha> origin/develop && echo in-develop

# 成果物の実体（例: note 公開状態）
grep -nE '^(published|noteUrl|noteStatus):' <関連 article/SoT>

# この doc を参照しているファイル（reference/project doc 削除時の張り替え対象）
grep -rl '<doc-basename>' docs .claude --include='*.md' | grep -v '<self>'

# memory 参照
grep -rl '<doc-basename>' ~/.claude/projects/*/memory/ 2>/dev/null
```

「完了」を裏付けられないシグナル（note 投稿・deploy・cloud 生成など外部尻尾）は**未確認として明記**する。

### 3. doc-curator に判定させる

`doc-curator`（`model: sonnet`）を spawn し、**テキストで**渡す:
- **候補 doc パス一覧**（手順 1）
- **各候補の検証済みシグナル**（手順 2：完了 / 参照 / 重複 / 鮮度 / 凍結）

候補が **12 件超**なら**複数エージェントに分割**（1 エージェント 5〜8 件）。エージェントは候補を `Read` し、`verdict（KEEP/TRIM/DELETE/CONSOLIDATE）+ 根拠引用 + confidence + 後追い（どこへ何を抽出すべきか）` を返す。

> エージェントは Bash 不可。git/grep の確定は**必ず親が済ませて**から渡す（[[feedback_agent_bash]]）。

### 4. 提示 → 承認 → 適用

verdict を一覧提示し、ユーザー承認後に親が適用:

- **TRIM**: 完了行を Edit で除去。完了の事実は「注」で 1 行残す（誤読防止）。EOL 保持。
- **DELETE**（handoff の既定）: **生きたタスクを `.claude/todo/backlog.md` へ・手順を reference へ・知見を memory へ抽出**してから `git rm <doc>`。handoff への出典引用は張り替え不要（対象外）。reference/project doc の場合は全参照を SSOT へ張り替え。
- **CONSOLIDATE**: 内容を統合先へ移し、重複側を DELETE。参照は統合先へ。

```bash
# 例（抽出＋削除を 1 commit に・pathspec で対象だけ）
# （backlog / reference / memory へ抽出を Edit で反映してから）
git rm docs/handoffs/<doc>.md
git commit -m "docs(handoff): <doc> を抽出→削除（…完了検証済・記録は git 履歴）" -- \
  docs/handoffs/<doc>.md .claude/todo/backlog.md <抽出先ファイル...>
```

### 5. 適用後の検証

```bash
npm run check-doc-refs        # 壊れ参照ゼロ（reference/project 削除時の張り替え漏れ）
npm run check-doc-coupling    # 台帳もれゼロ（スキル/エージェントを動かした場合）
git show --stat HEAD          # 巻き込み確認（対象ファイルだけか）
git status --short            # 並行セッションの変更が手つかずか
```

文字化け（U+FFFD）混入・CRLF 混在もチェック。完了後、何を削除/trim し・何を未確認で残したかを 1 行で報告（CLAUDE.md §12）。

## 例

- **handoff 棚卸し**: `/doc-declutter` → surfacer が orphan 4 本提示 → 各 PR の merged と成果物 published:true を確認 → doc-curator が「3 本 DELETE（うち1本は残タスクを backlog へ抽出）・1 本 KEEP（open 残・編集中）」と判定 → 承認 → 抽出＋削除を pathspec commit。
- **reference 重複**: `/doc-declutter reference` → 同じ手順を ADR と reference が二重に持つ → CONSOLIDATE（ADR を SSOT に、reference 側を DELETE・参照を張り替え）。

## トラブルシューティング

- **check-doc-refs が落ちる**: 削除した reference/project doc への参照が残っている。`grep -rl '<basename>' docs .claude` で残存を洗い、SSOT へ全部張り替える（handoffs への参照は対象外なので落ちない）。
- **pre-commit が無関係ファイルで止まる**: `git add -A` していないか確認。必ず `git commit -- <pathspec>`。
- **「完了」と書いてあるのに実体は未完**: 外部尻尾（note 投稿・deploy）は repo に痕跡が出ない。`verify-note-magazines` 等で実体確認し、未確認なら残作業を backlog へ「未確認」として抽出してから削除（or KEEP でユーザーへ）。

## 連携

- Evaluator: `doc-curator`（処分判定）
- 機械 surfacer: `scripts/check-doc-lifecycle.mjs`（`npm run check-doc-lifecycle`）
- 削除後の検証: `scripts/check-doc-refs.mjs` / `scripts/check-doc-coupling.mjs`（pre-commit）
- 抽出もれガード: `scripts/check-handoff-extraction.mjs`（pre-commit）＝handoff 直下 `*.md` を前送りマーカー付きで削除するのに backlog を同梱していない／`_archive/` へ追加すると止める。本スキルの「抽出が先・削除が後」を機械で担保する最終網（回避 `SKIP_HANDOFF_EXTRACT=1`）
- 別系統: `/doc-sync`（コード変更起点の prose 陳腐化）
- ルール真実源: CLAUDE.md §8 / `.claude/knowledge/reference/information-architecture.md`「SSOT と参照規律」「handoff のライフサイクル」
