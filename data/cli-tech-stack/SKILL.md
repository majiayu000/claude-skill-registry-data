---
description: CLIツール開発の技術スタック・規約定義
---

# CLI Tech Stack

CLIツール開発で使用する技術スタックと規約の定義。

## 技術スタック

全て必須。指定バージョン以上の最新版を使用すること。

| 項目 | 技術 | バージョン | 備考 |
|------|------|-----------|------|
| 言語 | TypeScript | - | - |
| 実行環境 | Bun | - | - |
| 型チェック | @typescript/native-preview (tsgo) | v7以上 | tsc禁止 |
| linter/formatter | @biomejs/biome | v2以上 | - |
| CLIフレームワーク | citty | v0.1.6以上 | - |
| 色付き出力 | chalk | v5.6.2以上 | - |
| プログレスバー | cli-progress | v3.12.0以上 | - |
| 未使用コード検出 | knip | - | - |

使用していない技術スタックがあった場合は重大な問題として通知する必要がある。

## TypeScript 規約

- `any`の使用禁止
- `interface`ではなく`type`を使用（既存ライブラリ型の拡張時のみ例外、コメント必須）
- barrel import/exportの禁止
- 無駄なオプション・デフォルト値を設定しない

## スクリプト規約

- Bunで実行可能なTypeScriptファイルとして作成
- シェバン設定で単体実行可能にする
- 引数を取る時は全てオプション形式にする。位置引数は使わない。
  - サブコマンドを指定する時は例外的に許可。

```bash
# OK
./hoge.ts

# NG
bun run hoge.ts

# 引数あり
# OK
./hoge.ts --fuga "fuga" --piyo

# NG
./hoge.ts "fuga" piyo
```

## コード品質

- 関数型スタイルを意識（map/filterを優先、array.pushを避ける）
- fail fast. 無駄に catch して console.error するなどをせず、素直にエラー終了させること。
- 暗黙のフォールバック禁止
- ダミーコード・NO-OP実装の禁止

### ダミーコード・NO-OPの例

```typescript
// NG: 何もしない関数
function doSomething() {
  // TODO: 後で実装
}

// NG: 常にtrueを返す検証
function validate(input: string): boolean {
  return true; // 実際の検証なし
}

// NG: エラーを握りつぶす
try {
  riskyOperation();
} catch {
  // 何もしない
}
```
