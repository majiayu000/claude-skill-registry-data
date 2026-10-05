---
name: doc-sync
description: >
  コード/スクリプト/スキル/設定の変更 diff を起点に、関連ドキュメント（docs/** ・CLAUDE.md ・.claude/**）が
  旧仕様化していないかを監査する。親が diff から「ドキュメント化された面」の変更を抽出し、参照している候補 doc を
  grep で特定し、doc-sync-auditor（Evaluator）に突合させて findings を提示、承認後に適用する。
  機械検知（check-doc-refs / check-doc-coupling）が拾えない意味的な陳腐化を埋める半自動ガード。
  Use when user asks to [ドキュメント同期, doc同期, 仕様ズレ確認, ドキュメント更新もれ, /doc-sync].
user-invocable: true
argument-hint: "[<git-range>] (既定: 作業ツリー+staged vs HEAD)"
domain: ops
---

コード変更に対しドキュメントの**意味的な陳腐化（semantic staleness）**を監査する半自動オーケストレーションスキル。
親（あなた）が決定論的な抽出と grep を担い、判定だけを Evaluator サブエージェント **`doc-sync-auditor`** に委ねる。

> **3 層の役割分担（混同しない）**
> - `scripts/check-doc-refs.mjs` … 壊れたパス参照（機械・pre-commit）
> - `scripts/check-doc-coupling.mjs` … スキル/エージェント台帳の更新もれ（機械・pre-commit）
> - **本スキル + `doc-sync-auditor`** … prose・表・コマンド・件数・閾値の**意味的ズレ**（LLM 判定・節目に手動）

## いつ回すか（発火規律）

**回す**: `src/**` `scripts/**` `.claude/skills/**` `.claude/agents/**` `package.json` `src/config/**` `src/styles/**` 等「**ドキュメント化された面**」を変更したタスクの**完了時 / コミット前**。
**回さない**: 純コンテンツ編集（`content/site/**` の MDX 記事、`content/note/**` `content/sns/**` の素材、画像）。これらは reference doc を陳腐化させないのでトークンの無駄。

## 手順（親が実行）

### 1. diff スコープを決める

```bash
# 既定: 作業ツリー + staged を HEAD と比較
git diff HEAD --name-status
# ブランチ作業中の累積を見るなら base と比較
git diff origin/develop...HEAD --name-status   # 引数で <git-range> 指定時はそれを使う
```

### 2. 「ドキュメント化された面」の変更だけ抽出

変更ファイルを次に絞る（純コンテンツは除外）:
`src/** scripts/** .claude/skills/** .claude/agents/** package.json src/config/** src/styles/**`

さらに、doc に響く**シンボル**を変更内容から拾う:
- **削除/リネーム/移動されたファイルの basename とパス**（例 `upload-images-r2`、`06_競合調査/`）
- **追加/削除された npm script 名**（`package.json` の diff）
- **削除/改名された export・config キー・デザイントークン・コンポーネント名**（`src/**` の diff）
- **変わった既定値・閾値・列挙の選択肢**

### 3. 候補 doc を grep で特定

抽出したパス/シンボルを doc 全体から逆引きする:

```bash
# 例: 変更された symbol/path を OR で grep
grep -rl -E 'upload-images-r2|06_競合調査|<その他symbol>' docs CLAUDE.md .claude --include='*.md' 2>/dev/null | sort -u
```

ヒットした doc が**候補 doc 一覧**。0 件なら陳腐化の心配は薄い（終了してよい）。

### 4. doc-sync-auditor に突合させる

`doc-sync-auditor`（`model: sonnet`）を spawn し、**テキストで**渡す:
- **変更サマリ**: 該当 diff の hunk または箇条書き要約（何が消えた/変わった/増えた）
- **候補 doc パス一覧**（手順 3 の結果）

候補が **12 件超**なら**複数エージェントに分割**（1 エージェントあたり候補 5〜8 件目安）して並列実行。エージェントは候補 doc を `Read` し、`file:line + 引用 + 矛盾根拠 + 修正案 + severity` で findings を返す。

> エージェントは Bash 不可。grep と diff 抽出は**必ず親が済ませて**から渡す（[[feedback_agent_bash]]）。

### 5. 提示 → 承認 → 適用

- findings を `must-fix / should-fix / maybe` で整理してユーザーに提示。
- **適用は親が行う**（auditor は検出専用＝Generator/Evaluator 分離）。`must-fix` を中心に、doc の該当箇所を Edit。
- 派手な改稿はしない。**事実の同期に必要な最小差分**だけ（CLAUDE.md §3 外科的変更）。

### 6. 適用後の検証

```bash
npm run check-doc-refs        # 参照破損ゼロ
npm run check-doc-coupling    # 台帳更新もれゼロ（staged 前提）
```

文字化け（U+FFFD）混入もチェック。完了後、何を直し・何を `maybe` で保留したかを 1 行で報告（CLAUDE.md §12 失敗/不確実を隠さない）。

## トークン目安

候補 doc を**読むのは auditor（sonnet）だけ**＝親は grep 結果（軽量）を渡すだけ。1 回あたり概ね **20k〜60k トークン**（候補 doc 数と diff 規模次第）。毎編集ではなく**節目に 1 回**回すこと。候補 0 件なら spawn せず即終了。

## 改善メモ（使いながら育てる）

- 誤検知が多い面・拾い漏れる面が分かったら、手順 2 の抽出範囲・手順 3 の grep パターン・auditor の判定基準を更新する。
- 将来、頻出する決定論パターン（例: 「`npm run` 表に消えた script が残存」）は本スキルから `scripts/` の機械チェックへ昇格させ、auditor の負荷を減らす。

## 連携

- Evaluator: `doc-sync-auditor`（判定）
- 機械ガード: `scripts/check-doc-refs.mjs` / `scripts/check-doc-coupling.mjs`（pre-commit）
- ルール真実源: CLAUDE.md §8 / `.claude/knowledge/reference/information-architecture.md`「SSOT と参照規律」
