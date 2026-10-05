---
name: affiliate-status
description: >
  A8 / もしも / afb の 3 ASP の提携状態を実機と突合し、カタログとのドリフトを報告する（read-only）。
  申請も設定変更もしない（申請は /affiliate-apply）。
  **3 ASP すべてで doboku-note と stats47 が同一口座に同居し既定は stats47 側**のため、
  サイト帰属 assert（不一致は例外で停止）を通してから読む。
  Use when user says "アフィリ提携状況", "提携状態を確認", "ASP 横断で確認", "affiliate-status".
  **取得できなかった ASP を「提携なし」と報告しないこと**（unknown として区別する）。
disable-model-invocation: true
argument-hint: "[--asp a8|moshimo|afb] [--write]"
domain: affiliate
---

> [!important] 「提携なし」と「確認できなかった」は別
> ログイン失敗・回線タイムアウト・サイト帰属 NG で取得できなかった ASP は
> **判定不能**として報告する。`status: none`（未提携と確認した）と `unknown`（調べていない）は
> カタログの語彙として分かれているので、埋めるときにこの区別を潰さない。

## 何をするか

`data/affiliate/catalog.json`（自社がどの案件をどの ASP で運用するか）を
各 ASP の提携中/申請中一覧と突合し、ドリフトを出す。

```bash
npm run affiliate:status
```

| オプション | 意味 |
|---|---|
| `-- --asp moshimo` | 1 ASP だけ照合（afb は毎回ログインが要るので分けたいとき） |
| `-- --write` | 実機の値でカタログを更新（既定は read-only で報告のみ） |

## 前提

- **ローカル実行のみ**（ログイン済みプロファイルが要る）。CI では動かない
- **ログインは人間**。スクリプトは待つだけで認証情報を扱わない
- **afb はセッションを別プロセスに持ち越せない**ため毎回ログインが要る。かつ headless 不可・
  1 ページ 1〜1.5 分かかることがある（`timeoutMs` 90 秒）

## 手順

1. `npm run affiliate:status` を実行し、ブラウザが開いたらユーザーにログインを依頼する
2. 出力の **SID / 口座 ID** を確認する。報告には必ずこれを添える
   （「どのサイトのデータか」を示さない報告は信用できない）
3. ドリフトが出たら、**カタログが古いのか実機が変わったのか**を判断する
   - 実機が正（申請が承認された等）→ `-- --write` で反映
   - カタログの意図が正（誤って stats47 で提携した等）→ 実機を直す提案をする
4. `npm run check-affiliate-wiring` で配線の穴（`placement=active` なのに mat が無い等）も見る
5. 変更したらカタログを commit する

## 出力の読み方

```
取得できなかった ASP（判定不能・「提携なし」ではない）:
  - afb: サイト帰属 NG: サイト ID 不一致: 期待 984453 / 実際 959426
ドリフト 1 件:
  - kensetsu-career-plus / moshimo: カタログ "applying" ↔ 実機 "approved"（id=5665）
```

サイト帰属 NG が出たら**それは成功の一種**（stats47 のデータを読む前に止まった）。
迂回せず、切替が効かない原因を調べる。

## 関連

- 運用 SSOT: `.claude/knowledge/reference/affiliate-operations.md`
- 申請: `/affiliate-apply`
- A8 の成果取込: `/a8-report` ／ A8 の案件開拓: `/scout-asp`（守備範囲が直交）
