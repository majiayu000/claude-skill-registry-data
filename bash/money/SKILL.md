---
name: money
description: |
  `money` / `moneycli` コマンドを使って家計スナップショット（資産・負債・純資産・月次収支・口座ステータス）を取得し、必要に応じて同期・日付指定・プロバイダー確認を行う。ユーザーが「money コマンドを実行して」「資産状況を見たい」「Money Forward のキャッシュを更新して」「過去日の家計を確認して」など依頼したときに使う。
---

# Money CLI Skill

`money` コマンドを実行して、指定日付の家計スナップショットを取得する。

## 実行場所

- 通常実行: `/home/yuiseki/Workspaces` で `money ...` を実行する。
- 開発フォールバック: `/home/yuiseki/Workspaces/repos/moneycli` で `npm run build` 後に `npm run start -- ...` を実行する。

## 基本手順

1. `money --help` でコマンド存在を確認する。
2. `money providers` で利用可能プロバイダーを確認する。
3. `money` または `money --date <yyyy-mm-dd>` でスナップショットを取得する。
4. キャッシュ更新が必要なときだけ `money sync --date <yyyy-mm-dd>` を実行する。

## 基本コマンド

```bash
money
money --date 2026-02-21
money providers
money sync --date 2026-02-21
money --json
```

## 開発フォールバック（repos/moneycli）

`money` バイナリが見つからない、または実装確認が必要な場合は以下を使う。

```bash
cd /home/yuiseki/Workspaces/repos/moneycli
npm run build
npm run start -- --help
npm run start -- --date 2026-02-21
```

## 主要オプション

- `--date <yyyy-mm-dd>`: 対象日付を指定する（未指定時は当日）。
- `--provider <name>`: 利用プロバイダーを指定する。
- `--json`: JSON 形式で出力する。
- `--cache-dir <path>`: キャッシュ保存先を上書きする。
- `sync` サブコマンド: 指定日付を強制取得してキャッシュ更新する。

## 環境変数

- `MONEYFORWARD_COOKIE_PATH`: Money Forward の cookie JSON ファイルパス。
- `MONEYCLI_CACHE_DIR`: キャッシュディレクトリ（デフォルト: `~/.cache/moneycli`）。
- `MONEYCLI_PROVIDER`: 既定プロバイダー名（デフォルト: `money_forward`）。
- `MONEYCLI_PROVIDER_MODULES`: 追加プロバイダーモジュールのカンマ区切りパス。

## キャッシュ動作

- 当日: キャッシュがあれば再利用し、必要時に取得する。
- 過去日: 既定ではキャッシュ読み取りのみ。キャッシュ未作成ならエラーになる。
- 保存先: `~/.cache/moneycli/YYYY/MM/DD/<provider>/data.json`

## トラブルシュート

- `money: command not found`:
  `repos/moneycli` で `npm run build` 後に `npm run start -- ...` を使う。常用するなら `npm install -g @yuiseki/moneycli` を使う。
- `No cache snapshot for <date>`:
  `money sync --date <date>` を実行してキャッシュを作成する。
- `Money Forward session appears to be invalid`:
  `.cookies/moneyforward.com.cookie.json` を更新するか、`MONEYFORWARD_COOKIE_PATH` を正しいファイルに設定する。

## 実行時の注意

- 金融情報を含むため、出力を外部共有するときはユーザー承認を取る。
- 自動処理では `--json` を優先して機械可読で扱う。
