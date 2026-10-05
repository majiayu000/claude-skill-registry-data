---
name: add-logger
description: Add BreakdownLogger to test code. Use when creating test files, adding debug logging to existing tests, or when user says 'ログ追加', 'logger追加', 'デバッグログ'.
---

テスト実行の追跡のため、BreakdownLogger をテストファイルに追加する（本番コード禁止）。

## Import と生成

```typescript
import { BreakdownLogger } from "@tettuan/breakdownlogger";
import { LogLevel, LogLength, type LogEntry } from "@tettuan/breakdownlogger";
const logger = new BreakdownLogger("loader"); // KEY=テスト対象モジュール
```

## API

| メソッド | 表示条件 |
|---------|---------|
| `debug(msg, data?)` | `LOG_LEVEL=debug` |
| `info(msg, data?)` | デフォルト以上 |
| `warn(msg, data?)` | `LOG_LEVEL=warn` 以上 |
| `error(msg, data?)` | 常時（stderr） |

## 型

| 型 | 値 |
|---|---|
| `LogLevel` | `DEBUG=0`, `INFO=1`, `WARN=2`, `ERROR=3` |
| `LogLength` | `DEFAULT`=80, `SHORT`=160, `LONG`=300, `WHOLE`=無制限 |
| `LogEntry` | `{ timestamp, level, key, message, data? }` |

## LOG_KEY 命名規則

問題の層を特定するため、src/ モジュール境界に1対1で KEY を対応させる。

| KEY | src/ モジュール | デバッグ対象 |
|-----|---------------|------------|
| `config` | `breakdown_config.ts` | Public API: 設定の生成・構造・アクセス |
| `manager` | `config_manager.ts` | 内部制御: 初期化・マージ戦略・リロード |
| `loader` | `loaders/` | ファイルI/O: 読み込み・パース・形式検出 |
| `validator` | `validators/` | 検証: スキーマ・制約・拒否理由 |
| `error` | `errors/`, `error_manager.ts` | エラー: 生成・i18n・伝播チェーン |
| `path` | `utils/path_resolver.ts`, `utils/valid_path.ts` | パス: 解決・探索・存在確認 |
| `cache` | `utils/config_cache.ts`, `utils/error_cache.ts` | キャッシュ: ヒット/ミス・TTL・無効化 |
| `setup` | テストのsetup/teardown | テスト環境: フィクスチャ・一時ディレクトリ |

`config` は BreakdownConfig クラス、`manager` は ConfigManager に使い、公開APIか内部制御かを切り分ける。

## 実装パターン

関数呼び出し前に入力値、呼び出し後に期待値と実際の値をログし、失敗原因を特定する。

```typescript
const logger = new BreakdownLogger("manager");

it("should merge user config over app defaults", () => {
  logger.debug("merge inputs", { appConfig, userConfig });
  const result = mergeConfigs(appConfig, userConfig);
  logger.debug("merge result", { expected: "user_value", actual: result.key });
  assertEquals(result.key, "user_value");
});
```
