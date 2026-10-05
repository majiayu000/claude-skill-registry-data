---
name: ci-troubleshooting
description: Use when user encounters CI errors, JSR connection issues, 'deno task ci' failures, or sandbox-related build problems. Provides solutions for common CI issues.
allowed-tools: [Bash, Read, Edit, Grep, Glob]
---

CI失敗時の原因特定と解決を行う。CI実行は `/local-ci`、リリースは `/release-procedure` を参照。

## CIパイプライン順序

deps → check → jsr-check → test → lint → fmt

## JSR接続エラー

sandbox制限でJSRに接続できない場合、`dangerouslyDisableSandbox: true` で実行する。

## Lintエラー

| ルール | 修正方法 |
|--------|---------|
| `no-console` | `// deno-lint-ignore no-console` を追加 |
| `prefer-ascii` | 日本語→英語に変更（テストフィクスチャは例外） |
| `no-await-in-loop` | ignore追加または `Promise.all` にリファクタ |
| `explicit-function-return-type` | 戻り値型を明記 |

ファイルレベル: `// deno-lint-ignore-file no-console prefer-ascii`（ファイル先頭）
行レベル: `// deno-lint-ignore <rule>`（対象行の直前）

## テスト失敗

タイミング問題（フレーキーテスト）は並列→逐次実行に変更し、十分なdelayを入れる。型エラーはインターフェース変更後のフィクスチャ更新漏れを確認する。

## フォーマットエラー

`deno fmt --check` で確認、`deno fmt` で修正する。

## 個別ステージ実行

```bash
deno check src/**/*.ts    # 型チェックのみ
deno lint                  # Lintのみ
deno test path/to/test.ts  # 単一テスト
```
