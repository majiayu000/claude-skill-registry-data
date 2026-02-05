---
name: cc-hooks-ts
description: TypeScriptで型安全なClaude Code Hooksを作成するためのガイド。cc-hooks-tsライブラリを使用してフックを実装する際に使用する。(1) Claude Code用の新しいhookを作成する時、(2) 既存のhookをTypeScriptで書き直す時、(3) PreToolUse/PostToolUse/SessionStart等のイベントフックを実装する時、(4) plugin.jsonにhooksを設定する時
---

# cc-hooks-ts を使用した Claude Code Hooks 作成ガイド

## インストール

```bash
bun add cc-hooks-ts
```

## 基本的なフック構造

```typescript
#!/usr/bin/env bun
import { defineHook, runHook } from "cc-hooks-ts";

const hook = defineHook({
  trigger: {
    // トリガーするイベントを指定
    PostToolUse: {
      Write: true,
      Edit: true,
    },
  },
  // オプション: 条件付き実行
  shouldRun: () => {
    return process.platform === "darwin"; // macOSのみ
  },
  run: (context) => {
    // フックのロジック

    // 成功レスポンス（何もしない）
    return context.success({});

    // または、追加コンテキストを返す
    return context.json({
      event: "PostToolUse",
      output: {
        hookSpecificOutput: {
          hookEventName: "PostToolUse",
          additionalContext: "Claude へのメッセージ",
        },
        suppressOutput: true,
      },
    });

    // または、エラーでブロック
    return context.blockingError("操作をブロックしました");
  },
});

if (import.meta.main) {
  await runHook(hook);
}
```

## サポートされているイベント

| イベント | 説明 | ユースケース |
|---------|------|-------------|
| `SessionStart` | セッション開始時 | 環境チェック、初期設定 |
| `PreToolUse` | ツール使用前 | 操作のブロック、入力検証 |
| `PostToolUse` | ツール使用後 | ログ記録、追加処理 |
| `PostToolUseFailure` | ツール失敗時 | エラーハンドリング |
| `Notification` | 通知イベント | アラート処理 |

## ツール固有のフック

特定のツールに対してのみフックをトリガーする場合:

```typescript
const hook = defineHook({
  trigger: {
    PreToolUse: {
      Read: true,  // Read ツールのみ
    },
  },
  run: (context) => {
    const filePath = context.input.tool_input.file_path;

    // .env ファイルへのアクセスをブロック
    if (filePath.endsWith(".env")) {
      return context.blockingError("環境ファイルへのアクセスは許可されていません");
    }

    return context.success({});
  },
});
```

## 主要 API

### context オブジェクト

| メソッド | 説明 |
|---------|------|
| `context.success({})` | 成功レスポンス（処理を続行） |
| `context.blockingError(message)` | エラーでブロック |
| `context.json(response)` | 構造化レスポンス（追加コンテキスト付き） |

### context.input の構造

```typescript
interface HookInput {
  event: string;           // イベント名
  tool_name?: string;      // ツール名（ToolUse系イベント）
  tool_input?: Record<string, any>;  // ツールの入力パラメータ
  tool_output?: string;    // ツールの出力（PostToolUse）
}
```

## plugin.json での設定

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bun run -i --silent ${CLAUDE_PLUGIN_ROOT}/path/to/hook.ts"
          }
        ]
      }
    ]
  }
}
```

**重要**:
- `bun run -i --silent` を使用すること
- `${CLAUDE_PLUGIN_ROOT}` でプラグインルートを参照

## 実装例

### 例1: ファイル書き込み時に知見ファイルを提案

```typescript
#!/usr/bin/env bun
import { existsSync } from "node:fs";
import { basename } from "node:path";
import { defineHook, runHook } from "cc-hooks-ts";

const hook = defineHook({
  trigger: {
    PostToolUse: {
      Write: true,
      Edit: true,
    },
  },
  run: (context) => {
    const filePath = context.input.tool_input.file_path;
    const knowledgePath = `${filePath}.knowledge.md`;

    if (existsSync(knowledgePath)) {
      return context.json({
        event: "PostToolUse",
        output: {
          hookSpecificOutput: {
            hookEventName: "PostToolUse",
            additionalContext: `${knowledgePath} に知見を追記してください`,
          },
          suppressOutput: true,
        },
      });
    }

    return context.success({});
  },
});

if (import.meta.main) {
  await runHook(hook);
}
```

### 例2: 特定ディレクトリへの書き込みをブロック

```typescript
#!/usr/bin/env bun
import { defineHook, runHook } from "cc-hooks-ts";

const PROTECTED_DIRS = ["/etc", "/usr", "/System"];

const hook = defineHook({
  trigger: {
    PreToolUse: {
      Write: true,
    },
  },
  run: (context) => {
    const filePath = context.input.tool_input.file_path;

    for (const dir of PROTECTED_DIRS) {
      if (filePath.startsWith(dir)) {
        return context.blockingError(
          `${dir} への書き込みは許可されていません`
        );
      }
    }

    return context.success({});
  },
});

if (import.meta.main) {
  await runHook(hook);
}
```

### 例3: セッション開始時の環境チェック

```typescript
#!/usr/bin/env bun
import { existsSync } from "node:fs";
import { defineHook, runHook } from "cc-hooks-ts";

const hook = defineHook({
  trigger: {
    SessionStart: true,
  },
  run: (context) => {
    const requiredFiles = [".env", "package.json"];
    const missing = requiredFiles.filter(f => !existsSync(f));

    if (missing.length > 0) {
      console.error(`警告: 以下のファイルが見つかりません: ${missing.join(", ")}`);
    }

    return context.success({});
  },
});

if (import.meta.main) {
  await runHook(hook);
}
```

## カスタムツール型の拡張

MCP で定義されたカスタムツールに型を追加する場合:

```typescript
import { defineHook } from "cc-hooks-ts";

declare module "cc-hooks-ts" {
  interface ToolSchema {
    my_custom_tool: {
      input: { query: string };
      output: { result: string };
    };
  }
}

const hook = defineHook({
  trigger: {
    PostToolUse: {
      my_custom_tool: true,
    },
  },
  run: (context) => {
    // context.input.tool_input は { query: string } として型付けされる
    return context.success({});
  },
});
```

## ベストプラクティス

1. **エラーハンドリング**: try-catch で予期しないエラーをキャッチ
2. **クールダウン**: 頻繁なトリガーを避けるためクールダウン機構を実装
3. **ログ出力**: `console.error()` でユーザーに情報を表示（`console.log` は避ける）
4. **冪等性**: 同じ入力に対して同じ結果を返すように設計
5. **軽量化**: フック処理は高速に完了するよう設計

## 参考リンク

- [cc-hooks-ts GitHub](https://github.com/sushichan044/cc-hooks-ts)
- [Claude Code Hooks 公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code/hooks)
