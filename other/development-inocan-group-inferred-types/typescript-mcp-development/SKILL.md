---
name: typescript-mcp-development
description: 'TypeScript SDKとzodバリデーション、Express統合を使用したMCPサーバー構築ガイド。TypeScript/Node.jsベースのMCPサーバーの作成、zodスキーマ定義、STDIOおよびHTTPトランスポート設定を行う際に使用。'
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# TypeScript MCP Server Development

このスキルは、TypeScript SDKとzodバリデーションを使用したModel Context Protocol (MCP) サーバーの構築を支援します。

## いつこのスキルを使用するか

以下の場合に本スキルを活用してください:

- TypeScript/Node.js でMCPサーバーを新規作成する
- zodスキーマによる型安全なツール・リソースを実装する
- STDIOまたはHTTPトランスポート(Express統合)を設定する
- MCP Inspector を使用したテストとデバッグを行う
- 既存のTypeScript MCPサーバーを最適化・リファクタリングする
- 動的リソース、補完機能、サンプリングを実装する

## 開発環境のセットアップ

### 1. プロジェクト初期化

```bash
# 新規プロジェクト作成
mkdir mcp-server-demo
cd mcp-server-demo
npm init -y

# TypeScript と MCP SDK のインストール
npm install @modelcontextprotocol/sdk zod
npm install --save-dev typescript @types/node tsx

# TypeScript設定
npx tsc --init
```

### 2. package.json の設定例

[プロジェクト設定ファイル](./templates/package.json)を参照してください。

### 3. tsconfig.json の推奨設定

[TypeScript設定ファイル](./templates/tsconfig.json)を参照してください。

## ツール実装パターン

### 基本的なツール

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "demo-server",
  version: "1.0.0",
});

// ツールの登録
server.registerTool({
  name: "calculate",
  title: "Calculate Numbers",
  description: "Perform basic arithmetic operations",
  inputSchema: {
    a: z.number().describe("First operand"),
    b: z.number().describe("Second operand"),
    operation: z.enum(["add", "subtract", "multiply", "divide"])
      .describe("Operation to perform"),
  },
}, async ({ a, b, operation }) => {
  let result: number;

  switch (operation) {
    case "add":
      result = a + b;
      break;
    case "subtract":
      result = a - b;
      break;
    case "multiply":
      result = a * b;
      break;
    case "divide":
      if (b === 0) throw new Error("Division by zero");
      result = a / b;
      break;
  }

  return {
    content: [{ type: "text", text: `Result: ${result}` }],
    structuredContent: { result, operation, a, b },
  };
});
```

### zodスキーマを使用した高度なバリデーション

```typescript
const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
  roles: z.array(z.enum(["admin", "user", "guest"])).default(["user"]),
});

server.registerTool({
  name: "create_user",
  title: "Create User",
  description: "Create a new user with validation",
  inputSchema: UserSchema.shape,
}, async (input) => {
  // zodが自動的にバリデーション
  const user = UserSchema.parse(input);

  return {
    content: [{ type: "text", text: `User created: ${user.name}` }],
    structuredContent: user,
  };
});
```

### エラーハンドリング

```typescript
server.registerTool({
  name: "risky_operation",
  title: "Risky Operation",
  description: "Operation that may fail",
  inputSchema: {
    input: z.string(),
  },
}, async ({ input }) => {
  try {
    const result = await performRiskyOperation(input);
    return {
      content: [{ type: "text", text: `Success: ${result}` }],
      isError: false,
    };
  } catch (error) {
    return {
      content: [{
        type: "text",
        text: `Error: ${error instanceof Error ? error.message : "Unknown error"}`
      }],
      isError: true,
    };
  }
});
```

## リソース実装パターン

### 静的リソース

```typescript
server.registerResource({
  name: "config",
  uri: "config://app",
  title: "Application Configuration",
  description: "Get application config",
}, async () => {
  return {
    contents: [{
      uri: "config://app",
      mimeType: "application/json",
      text: JSON.stringify({
        version: "1.0.0",
        environment: "production",
      }, null, 2),
    }],
  };
});
```

### 動的リソース（ResourceTemplate）

```typescript
import { ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";

server.registerResource({
  name: "user_profile",
  template: new ResourceTemplate("users://{userId}", { list: undefined }),
  title: "User Profile",
  description: "Get user profile by ID",
}, async ({ userId }) => {
  const user = await fetchUserProfile(userId);

  return {
    contents: [{
      uri: `users://${userId}`,
      mimeType: "application/json",
      text: JSON.stringify(user, null, 2),
    }],
  };
});
```

## プロンプト実装パターン

```typescript
server.registerPrompt({
  name: "code_review",
  title: "Code Review Prompt",
  description: "Generate a code review prompt",
  inputSchema: {
    code: z.string().describe("Code to review"),
    language: z.string().default("typescript").describe("Programming language"),
  },
}, async ({ code, language }) => {
  return {
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Please review the following ${language} code:\n\n\`\`\`${language}\n${code}\n\`\`\``,
        },
      },
    ],
  };
});
```

## トランスポート設定

### STDIOトランスポート

```typescript
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const transport = new StdioServerTransport();
await server.connect(transport);

// 注意: STDIOモードでは console.log() を使用しない
// console.error() のみ使用可能
```

### HTTPトランスポート（Express統合）

```typescript
import express from "express";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/http.js";

const app = express();

app.post("/mcp", async (req, res) => {
  const transport = new StreamableHTTPServerTransport({
    sessionId: req.headers["mcp-session-id"] as string,
    enableDnsRebindingProtection: true,
  });

  await server.connect(transport);
  await transport.handleRequest(req, res);

  res.on("close", () => transport.close());
});

app.listen(3000, () => {
  console.error("MCP server listening on port 3000");
});
```

## テストとデバッグ

### MCP Inspector を使用したテスト

```bash
# サーバーを起動してInspectorで検査
npx @modelcontextprotocol/inspector node dist/server.js

# または tsx を使用
npx @modelcontextprotocol/inspector tsx src/server.ts
```

### 単体テストの例

[テストサンプル](./examples/server.test.ts)を参照してください。

## セキュリティチェックリスト

- [ ] 入力バリデーション: すべてのパラメータをzodで検証
- [ ] 型安全性: TypeScriptの厳密な型チェックを有効化
- [ ] アクセス制御: ファイルシステム操作を許可ディレクトリに制限
- [ ] 環境変数: APIキーなどのシークレットをコードにハードコードしない
- [ ] エラーメッセージ: 内部実装の詳細を露出しない
- [ ] レート制限: 外部API呼び出しにタイムアウトを設定
- [ ] ログ: STDIO使用時はconsole.error()のみ使用
- [ ] CORS: HTTPサーバーで適切なCORS設定を実装

## 一般的な問題と解決策

### 問題1: STDIO サーバーでログが出力されない

**原因**: `console.log()` を使用すると、JSON-RPCメッセージが破損します。

**解決策**:
```typescript
// ❌ 悪い例
console.log("Debug message");

// ✅ 良い例
console.error("Debug message");
```

### 問題2: zodバリデーションエラー

**原因**: スキーマ定義とデータが一致していません。

**解決策**:
```typescript
const schema = z.object({
  count: z.number().int().positive(),
});

// エラーハンドリング
try {
  const validated = schema.parse(input);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error("Validation failed:", error.errors);
  }
}
```

### 問題3: ESモジュールのインポートエラー

**原因**: `.js` 拡張子が欠けています。

**解決策**:
```typescript
// ❌ 悪い例
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp";

// ✅ 良い例
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
```

## 高度な機能

### 補完機能の実装

```typescript
import { completable } from "@modelcontextprotocol/sdk/server/mcp.js";

server.registerTool({
  name: "search",
  title: "Search",
  description: "Search with autocomplete",
  inputSchema: {
    query: completable(z.string()),
  },
}, async ({ query }, { onComplete }) => {
  if (onComplete) {
    // 補完候補を返す
    const suggestions = await getSuggestions(query);
    return { completions: suggestions };
  }

  // 実際の検索を実行
  const results = await performSearch(query);
  return { content: [{ type: "text", text: JSON.stringify(results) }] };
});
```

### サンプリング（LLM呼び出し）

```typescript
server.registerTool({
  name: "summarize",
  title: "Summarize Text",
  description: "Summarize text using LLM",
  inputSchema: {
    text: z.string(),
  },
}, async ({ text }) => {
  const result = await server.server.createMessage({
    messages: [{
      role: "user",
      content: { type: "text", text: `Summarize: ${text}` },
    }],
    maxTokens: 100,
  });

  return {
    content: [{ type: "text", text: result.content.text }],
  };
});
```

## 参考リソース

- [TypeScript MCP SDK GitHub](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Zod Documentation](https://zod.dev/)
- [プロジェクトテンプレート](./templates/)
- [実装例](./examples/)

## 次のステップ

1. [プロジェクトテンプレート](./templates/basic-server.ts)からサーバーを作成
2. TypeScriptをビルド: `npm run build`
3. MCP Inspectorでツールをテスト
4. [セキュリティチェックリスト](#セキュリティチェックリスト)を確認
5. 本番環境デプロイ
