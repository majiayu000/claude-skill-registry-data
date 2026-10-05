---
name: check-logger
description: Verify and run BreakdownLogger debug output. Use when debugging test failures, running tests with LOG_KEY, or when user says 'ログ確認', 'デバッグ実行', 'LOG_KEY', 'LOG_LEVEL'.
---

テスト失敗の原因を特定するため、環境変数で BreakdownLogger 出力をフィルタ実行する。

## 環境変数

| 変数 | 値 | 用途 |
|------|---|------|
| `LOG_LEVEL` | `debug`, `info`, `warn`, `error` | 出力閾値 |
| `LOG_KEY` | カンマ区切り（例: `loader,validator`） | キーフィルタ |
| `LOG_LENGTH` | `S`=160, `L`=300, `W`=無制限 | 出力長（デフォルト80） |

## 実行コマンド

```bash
# 特定モジュール
LOG_LEVEL=debug LOG_KEY="loader" deno test tests/3.integrated/config_loading_integration_test.ts --allow-env --allow-write --allow-read
# 複数モジュール同時追跡
LOG_LEVEL=debug LOG_KEY="manager,loader" deno test --allow-env --allow-write --allow-read
# 全出力（フィルタなし、出力長無制限）
LOG_LEVEL=debug LOG_LENGTH=W deno test --allow-env --allow-write --allow-read
```

## シナリオ別 KEY

| 問題 | LOG_KEY | 確認すること |
|------|---------|-------------|
| 設定ファイルが読まれない | `loader` | ファイルパス・パース結果 |
| マージ結果が期待と違う | `manager` | マージ入力・優先順位・出力 |
| Public APIの戻り値が不正 | `config` | 生成された設定・アクセス結果 |
| バリデーションが通らない | `validator` | 適用ルール・拒否理由 |
| パスが解決できない | `path` | baseDir・resolved・存在チェック |
| キャッシュから古い値が返る | `cache` | hit/miss・無効化タイミング |
| エラーメッセージが不正 | `error` | エラーコード・i18n・伝播 |
| テスト環境が壊れている | `setup` | フィクスチャ・一時ディレクトリ |

## 検証チェックリスト

- [ ] LOG_KEY が対象モジュールに対応しているか（`/add-logger` の命名規則表を参照）
- [ ] `config` と `manager` が正しく使い分けられているか
- [ ] 関数呼び出し前後に `logger.debug()` があるか
- [ ] 期待値と実際の値の両方がログに含まれているか
- [ ] `LOG_LEVEL=debug LOG_KEY=<key>` で実行して出力を確認できるか

## 出力の読み方

タイムスタンプで処理順序、`[KEY]` でモジュール層、JSON data で具体値を読む。

```
[2025-02-17T10:30:00.000Z] [DEBUG] [manager] merge inputs {"appConfig":{"key":"app_value"}}
[2025-02-17T10:30:00.001Z] [DEBUG] [manager] merge result {"expected":"user_value","actual":"user_value"}
```
