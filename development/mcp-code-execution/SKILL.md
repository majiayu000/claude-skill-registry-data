---
name: mcp-code-execution
description: MCP ツールを TypeScript コードとして実行し、トークン消費を最大 98.7% 削減します。Serena MCP ツール呼び出しが必要な場合、大規模データセット処理、コードベース全体への操作、バッチ処理、プライバシーに配慮したデータ処理が必要な場合に使用してください。
allowed-tools: Read, Write, Bash, Glob, Grep
---

# MCP コード実行

## 概要

MCP ツールを TypeScript コードとして実行し、トークン消費を劇的に削減します。必要なツールのみをインポートし、コード内でデータを処理してから、最終結果のみを返します。

**トークン削減**: マルチツールワークフローで最大 **98.7%**（150,000 トークン → 2,000 トークン）

## いつこのスキルを使うか

以下の条件のいずれかに該当する場合、このスキルを使用してください：

### 使用すべき場合
- ✓ **Serena MCP ツール**を連続使用する必要がある
- ✓ **100個以上のファイル**を処理する
- ✓ **大規模データのフィルタリング**（結果を絞り込んでから報告）
- ✓ **バッチ操作**（複数ファイルへのループ処理）
- ✓ **プライバシー保護**（機密データを LLM コンテキストに入れない）

### 使用すべきでない場合
- ✗ 1-2個のツールを1回だけ使う単純なタスク
- ✗ どのツールが必要かまだ分からない探索的作業
- ✗ 中間結果を確認する必要がある対話的デバッグ

## セットアップ

### プロジェクトルートの設定

このスキルの配置場所により、プロジェクトルートの設定方法が異なります。

#### Project Skills（`.claude/skills/` に配置）の場合

**プロジェクトルートは自動検出されます**。環境変数の設定は不要です。

```bash
# プロジェクト内のスキル
# .claude/skills/mcp-code-execution から自動的に ../../../../ でプロジェクトルートを検出
bun run src/your-script.ts
```

#### Personal Skills（`~/.claude/skills/` に配置）の場合

**環境変数 `SERENA_PROJECT_ROOT` が必須**です。未設定の場合、エラーが発生します。

**方法1: 環境変数で指定**
```bash
export SERENA_PROJECT_ROOT=/path/to/your/project
bun run src/your-script.ts
```

**方法2: .env ファイルで管理**（推奨）
```env
SERENA_PROJECT_ROOT=/path/to/your/project
```

プロジェクトルートに `.env` ファイルを配置すれば、Bun が自動的に読み込みます。

**異なるプロジェクトでの使用例**:
```bash
# test-parser プロジェクト
SERENA_PROJECT_ROOT=/Users/user/dev/test-parser bun run src/analyze-parser.ts

# testA プロジェクト
SERENA_PROJECT_ROOT=/Users/user/dev/testA bun run src/analyze-testA.ts
```

## ワークフロー（Claude が従うべき手順）

### ステップ1: タスクの評価

ユーザーのタスクが上記の「使用すべき場合」に該当するか判断してください。該当する場合のみ、このスキルを使用してください。

### ステップ2: ツール仕様の確認（必須・スキップ不可）

このステップを省略すると100%失敗します。以下のファイルを必ずReadツールで読んでください：

**チェックリスト:**
- [ ] TOOLS.mdを読んだ（Readツール使用）
- [ ] 使用する各ツールの型定義ファイル `servers/serena/[ツール名].ts` を読んだ（Readツール使用）
- [ ] パラメータ名が型定義と完全に一致している
- [ ] 戻り値の型が型定義と完全に一致している
- [ ] 型アサーション（`as`）を使用していない（型定義から自動推論される）

上記すべてにチェックが入るまでステップ3に進まないでください。

### ステップ3: TypeScript スクリプトの生成

`src/` ディレクトリに適切な名前の TypeScript ファイルを作成してください：

```typescript
import { /* 必要なツールのみ */ } from '../servers/serena/index.js';
import { closeClient } from './client.js';

async function main() {
  try {
    // ここにロジックを実装
    // - 必要なツールのみインポート
    // - コード内でデータをフィルタリング
    // - 最終結果のみ console.log()

  } catch (error) {
    if (error instanceof Error) {
      console.error('エラー:', error.message);
    }
  } finally {
    await closeClient();  // 必須
  }
}

main();
```

**重要**:
- 必要なツールのみをインポート（全20ツールではなく）
- **TOOLS.mdで確認した正確な型定義を使用**
- データ処理はコード内で実施（filter、map、reduce）
- 最終結果のみを `console.log()` で出力
- 必ず `await closeClient()` を呼び出す

### ステップ4: スクリプトの実行

```bash
bun run src/your-script.ts
```

### ステップ5: 結果の報告

スクリプトの出力から最終結果のみをユーザーに報告してください。中間データや処理の詳細は報告しないでください（プライバシー保護のため）。

**エラーが発生した場合**:
- 型エラー: TOOLS.mdと型定義を再確認
- 実行時エラー: パラメータの形式とツールの存在を確認

## 利用可能なツール

全20の Serena MCP ツールが利用可能です。詳細は [TOOLS.md](TOOLS.md) を参照してください。

**主要なツール**:
- `listDir`, `findFile`, `searchForPattern` - ファイル操作
- `getSymbolsOverview`, `findSymbol` - コード解析
- `replaceSymbolBody`, `renameSymbol` - コード編集

インポート例：
```typescript
import { listDir, findFile, getSymbolsOverview } from '../servers/serena/index.js';
```

## 基本的な使用例

### 例: エクスポートされたクラスを持つファイルを検索

```typescript
import { listDir, getSymbolsOverview } from '../servers/serena/index.js';
import { closeClient } from './client.js';

async function main() {
  try {
    const result = await listDir({ relative_path: 'src', recursive: true });
    const tsFiles = result.files.filter(f => f.endsWith('.ts'));

    const filesWithClasses = [];
    for (const file of tsFiles) {
      const symbols = await getSymbolsOverview({ relative_path: file });
      if (symbols.some(s => s.kind === 5)) {  // kind 5 = クラス
        filesWithClasses.push(file);
      }
    }

    console.log(`クラスを含むファイル: ${filesWithClasses.join(', ')}`);
  } catch (error) {
    if (error instanceof Error) {
      console.error('エラー:', error.message);
    }
  } finally {
    await closeClient();
  }
}

main();
```

**効果**: 1000ファイルの処理でも、最終結果のみが LLM に到達（トークン削減: 99%以上）

さらに詳しい例は [EXAMPLES.md](EXAMPLES.md) を参照してください。

## 必須事項

### 1. closeClient() を必ず呼び出す

```typescript
finally {
  await closeClient();  // スクリプトの最後に必ず
}
```

### 2. .js 拡張子を使用

```typescript
import { listDir } from '../servers/serena/index.js';  // ✓ 正しい
import { listDir } from '../servers/serena/index';     // ✗ 間違い
```

### 3. エラーハンドリング

```typescript
try {
  // ツール呼び出し
} catch (error) {
  console.error('エラー:', error.message);
} finally {
  await closeClient();
}
```

## 主な利点

| 利点 | 説明 |
|------|------|
| **トークン削減** | 最大 98.7% のトークン削減 |
| **オンデマンドロード** | 必要なツールのみインポート |
| **データフィルタリング** | LLM が見る前に処理 |
| **プライバシー保護** | 機密データがコード内に留まる |

## さらに詳しい情報

- **全ツールリスト**: [TOOLS.md](TOOLS.md)
- **詳細な使用例**: [EXAMPLES.md](EXAMPLES.md)
- **技術詳細**: [REFERENCE.md](REFERENCE.md)

## 参考

このスキルは Anthropic の推奨アプローチに基づいています:
[Code execution with MCP: building more efficient AI agents](https://www.anthropic.com/engineering/code-execution-with-mcp)
