---
name: affiliate-apply
description: >
  もしも / afb で提携申請を実行する（dry-run 既定・--commit gate）。
  **提携申請は規約同意を伴う不可逆操作**なので、--commit を付けるかどうかは毎回ユーザーの
  明示許可を取る（前回の許可を次回に流用しない）。
  サイト帰属 assert（既定は stats47 側・不一致は例外で停止）、申請フォームのサイト select 検証、
  「一括提携申請へ」の除外、Red Line 案件の拒否を機械で強制する。
  A8 の申請は /scout-asp が担当（こちらは扱わない）。
  Use when user says "提携申請", "アフィリを申請", "もしもで申請", "affiliate-apply".
disable-model-invocation: true
argument-hint: "--asp <moshimo|afb> --id <id[,id]> [--commit]"
domain: affiliate
---

> [!warning] これは不可逆操作
> 提携申請は広告主の規約に同意する行為。**ユーザーの明示許可なしに `--commit` を付けない。**
> dry-run の結果を提示し、何をどの ASP でどのサイト名義で申請するかを確認してから実行する。

## 機械で強制される安全弁

どれも過去に実害・未遂があったもの。**緩めない。**

| 安全弁 | 何を防ぐか |
|---|---|
| サイト帰属 assert（例外で停止） | **既定の stats47 側で提携してしまう**。3 ASP 共通の罠 |
| 申請フォームの site select を read-back | URL に `shop_site_id` を付けるだけでは足りない（もしも） |
| ラベル exact 一致 ＋「一括」除外 | **「一括提携申請へ」を押して画面上の全案件を一度に申請**する |
| 候補が複数ヒットしたら中止 | どのボタンを押したか曖昧なまま進む |
| `redLine: true` はゲートの手前で拒否 | 廃止した講座/教材アフィリを申請する |

## 手順

1. **候補を出す**。カタログ（`data/affiliate/catalog.json`）と走査結果から、
   単価・確定率・EPC・読者セグメント適合を並べる
   - セグメント不一致を除外する（例: **建築転職は建築士系で土木読者とは別**。2026-07-27 判断）
   - Red Line（講座・教材・添削・書籍）を除外する
2. **dry-run**

   ```bash
   npm run affiliate:apply -- --asp moshimo --id 6154
   ```

   ブラウザが開いたらユーザーにログインを依頼する。出力で以下を確認:
   - サイト帰属（SID / 一致理由）
   - サイト select が doboku-note になったか
   - 「提携申請する」が一意に取れたか
3. **結果をユーザーに提示して許可を得る**
4. **実行**

   ```bash
   npm run affiliate:apply -- --asp moshimo --id 6154 --commit
   ```

5. **実機で確認**。申請直後の画面表記は申請中/提携中を区別できないので信用しない

   ```bash
   npm run affiliate:status -- --asp moshimo
   ```

6. カタログを commit する

## 提携できた ≠ 配置する

配置枠は 3 つでカニバリ回避の手キュレーション。提携が通ってもリンクを置くかは**人が判断**する。
カタログの `placement` は既定 `none` のままにして、配置候補と根拠を提示するところで止める。

## 関連

- 運用 SSOT: `.claude/knowledge/reference/affiliate-operations.md`
- 状態照合: `/affiliate-status`
- A8 の申請: `/scout-asp`（A8 は別系統・こちらでは扱わない）
