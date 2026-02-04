---
name: claude-agent-sdk
description: |
  Claude Agent SDK（@anthropic-ai/claude-agent-sdk）および直接Anthropic SDK（@anthropic-ai/sdk）を使用したエージェント統合の実装を専門とするスキル。
  query() API、Hooksシステム、Permission Control、Electron統合、ストリーミング処理、Direct SDKパターンを支援します。

  Anchors:
  • Claude Agent SDK Official Docs / 適用: SDK API、Hooks、Permissions / 目的: 公式パターンに準拠した実装
  • Anthropic SDK (@anthropic-ai/sdk) / 適用: Direct SDK呼び出し / 目的: シンプルなMain Process統合
  • Electron IPC Best Practices / 適用: Main-Renderer間通信 / 目的: セキュアなプロセス間通信
  • TypeScript Handbook / 適用: 型定義、ジェネリクス / 目的: 型安全なSDK統合

  Trigger:
  Claude Agent SDKを使用したエージェント機能実装、query() APIストリーミング処理、Hooksシステム実装、Electron統合、Permission Control設計、MCP統合、Direct SDK統合を行う場合に使用。
  claude-agent-sdk, query API, PreToolUse, PostToolUse, PermissionRequest, Electron IPC, MCP, ストリーミング, 権限制御, @anthropic-ai/sdk, Direct SDK

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Claude Agent SDK

## 概要

Claude Agent SDK（`@anthropic-ai/claude-agent-sdk`）を使用したエージェント統合の実装を専門とするスキル。query() API、Hooksシステム、Permission Control、Electron統合、ストリーミング処理を支援します。

**対象言語**: TypeScript のみ

## 最新情報取得

SDK情報は頻繁に更新されるため、実装前に最新情報を確認してください。

```bash
# 最新情報を取得
node .claude/skills/claude-agent-sdk/scripts/fetch-latest-info.mjs

# npmパッケージ情報のみ
node .claude/skills/claude-agent-sdk/scripts/fetch-latest-info.mjs --category npm
```

詳細なURL一覧は `references/official-urls.md` を参照してください。

## ワークフロー

### Phase 1: 要件の明確化と設計方針の決定

**目的**: エージェント統合の要件を理解し、適切なパターンを選定する

**アクション**:

1. 使用するツール（Read, Edit, Bash等）を特定
2. Permission Control戦略を決定
3. `references/query-api.md` で基礎パターンを確認
4. `references/permission-control.md` で権限設計を確認

**Task**: `agents/analyze-agent-requirements.md` を参照

### Phase 2: SDK統合の実装

**目的**: query() APIとHooksを実装し、エージェント機能を構築する

**アクション**:

1. `assets/agent-handler-template.ts` を参照してIPCハンドラを実装
2. `references/hooks-system.md` でHooksパターンを確認
3. `references/electron-ipc.md` でElectron統合パターンを確認
4. ストリーミング処理とエラーハンドリングを実装

**Task**: `agents/implement-agent-integration.md` を参照

### Phase 3: 検証と記録

**目的**: 成果物の品質を確認し、ナレッジを記録する

**アクション**:

1. `scripts/validate-agent-setup.mjs` で設定の検証
2. Permission Controlのテスト
3. 実装パターンのドキュメント化

**Task**: `agents/validate-agent-setup.md` を参照

## Task仕様ナビ

| Task                     | 概要                                 | 対応する Phase | リソース                                       |
| ------------------------ | ------------------------------------ | -------------- | ---------------------------------------------- |
| query() API基本実装      | ストリーミングメッセージ処理の基本   | Phase 1, 2     | query-api.md, agent-handler-template.ts        |
| Hooks実装                | PreToolUse/PostToolUse/Permission    | Phase 2        | hooks-system.md                                |
| Permission Control設計   | 権限ルールの設計と実装               | Phase 1, 2     | permission-control.md                          |
| Electron IPC統合         | Main-Renderer間のAgent通信           | Phase 2        | electron-ipc.md                                |
| エラーハンドリング       | AbortSignal、タイムアウト、リトライ  | Phase 2        | error-handling.md                              |
| MCP統合                  | MCPサーバーとの連携                  | Phase 2, 3     | mcp-integration.md                             |
| セキュリティ設計         | サンドボックス、ホスティング         | Phase 2, 3     | security-sandboxing.md                         |

## パターン選択ガイド

### claude-agent-sdk vs 直接SDK使用

| 要件 | claude-agent-sdk | 直接SDK (`@anthropic-ai/sdk`) |
|------|-----------------|------------------------------|
| Hooks (PreToolUse等) | ✅ 必要 | ❌ 不要 |
| Permission Control | ✅ 必要 | ❌ 不要 |
| ストリーミングUI | ✅ 複雑 | ⚪ シンプル |
| Main Process専用 | ⚪ 可能 | ✅ 推奨 |
| バッチ処理 | ⚪ 可能 | ✅ 推奨 |

**推奨**:
- **対話型エージェント** → `@anthropic-ai/claude-agent-sdk`
- **バックグラウンド処理/バッチ** → `@anthropic-ai/sdk` 直接使用

### Direct Anthropic SDK Pattern

Main Processでシンプルなクエリを実行する場合のパターン。

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { safeStorage } from "electron";
import Store from "electron-store";

// APIキー管理（safeStorage + 環境変数フォールバック）
async function getApiKey(): Promise<string> {
  const store = new Store<{ anthropic_api_key?: string }>();
  const encrypted = store.get("anthropic_api_key");

  if (encrypted && safeStorage.isEncryptionAvailable()) {
    return safeStorage.decryptString(Buffer.from(encrypted, "base64"));
  }

  const envKey = process.env.ANTHROPIC_API_KEY;
  if (envKey) return envKey;

  throw new Error("API key not configured");
}

// 直接SDK呼び出し
async function executeQuery(
  prompt: string,
  systemPrompt?: string,
  timeout = 30000
): Promise<string> {
  const client = new Anthropic({ apiKey: await getApiKey() });

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await client.messages.create(
      {
        model: "claude-sonnet-4-20250514",
        max_tokens: 8192,
        ...(systemPrompt ? { system: systemPrompt } : {}),
        messages: [{ role: "user", content: prompt }],
      },
      { signal: controller.signal }
    );

    const textContent = response.content.find(b => b.type === "text");
    return textContent?.type === "text" ? textContent.text : "";
  } finally {
    clearTimeout(timeoutId);
  }
}
```

📖 実装参照: `apps/desktop/src/main/slide/agent-client.ts`

### SkillExecutor Pattern

フェーズベースのスキル実行パターン。進捗コールバック、キャンセル機能を含む。

```typescript
interface SkillExecutor {
  execute(phase: SkillPhase, projectPath: string): Promise<SkillExecutionResult>;
  cancel(): void;
  onProgress(callback: (progress: number) => void): void;
  isExecuting(): boolean;
}

// スキルフェーズマッピング
const skillMap: Record<SkillPhase, string> = {
  hearing: "hearing-facilitator",
  structure: "structure-designer",
  html: "html-generator",
  modifier: "slide-modifier",
};
```

📖 実装参照: `apps/desktop/src/main/slide/skill-executor.ts`

## ベストプラクティス

### すべきこと

- Permission Rulesで適切な権限制御を設計する
- PreToolUseフックで危険なコマンドをブロックする
- AbortSignalを使用してタイムアウト処理を実装する
- IPCチャネル名を一貫した命名規則で設計する
- ストリーミングメッセージを適切にUI更新に反映する
- エラー発生時のフォールバック処理を実装する

### 避けるべきこと

- permissionMode: 'auto' を本番環境で使用する
- Hookなしで危険なツール（Bash等）を許可する
- Main ProcessでUIロジックを処理する
- ストリーミング中のエラーを無視する
- APIキーをRenderer Processで扱う
- signal.abortedのチェックを省略する

## クイックリファレンス

### パッケージインストール

```bash
pnpm add @anthropic-ai/claude-agent-sdk
```

### 基本使用例

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

const conversation = query({
  prompt: "Hello, Claude!",
  options: {
    tools: ["Read", "Edit"],
    permissionMode: "ask",
  },
});

for await (const message of conversation.stream()) {
  console.log(message);
}
```

### Hook実装例

```typescript
const options = {
  hooks: {
    PreToolUse: async (input, toolUseID, { signal }) => {
      if (input.toolName === "Bash" && input.args.command?.includes("rm -rf")) {
        return { proceed: false, message: "危険なコマンドは許可されていません" };
      }
      return { proceed: true };
    },
  },
};
```

## リソース参照

### 責務別ドキュメント

```bash
# query() API、SDKMessage型、ストリーミング
cat .claude/skills/claude-agent-sdk/references/query-api.md

# Hooksシステム（全イベント、実装パターン）
cat .claude/skills/claude-agent-sdk/references/hooks-system.md

# Permission Control（4層システム、ルール）
cat .claude/skills/claude-agent-sdk/references/permission-control.md

# Electron IPC統合
cat .claude/skills/claude-agent-sdk/references/electron-ipc.md

# エラーハンドリング
cat .claude/skills/claude-agent-sdk/references/error-handling.md

# MCP統合
cat .claude/skills/claude-agent-sdk/references/mcp-integration.md

# セキュリティとサンドボックス
cat .claude/skills/claude-agent-sdk/references/security-sandboxing.md

# 公式URL一覧
cat .claude/skills/claude-agent-sdk/references/official-urls.md
```

### テンプレート参照

```bash
cat .claude/skills/claude-agent-sdk/assets/agent-handler-template.ts
cat .claude/skills/claude-agent-sdk/assets/use-agent-hook-template.ts
```

### スクリプト実行

```bash
# 最新情報取得
node .claude/skills/claude-agent-sdk/scripts/fetch-latest-info.mjs --help

# 設定検証
node .claude/skills/claude-agent-sdk/scripts/validate-agent-setup.mjs --help
```

## 関連ドキュメント

| ドキュメント                  | パス                                                                           | 説明                                |
| ----------------------------- | ------------------------------------------------------------------------------ | ----------------------------------- |
| Agent SDKインターフェース仕様 | `.claude/skills/aiworkflow-requirements/references/interfaces-agent-sdk.md`    | 統合システム設計仕様（型定義、IPC） |
| 実装ガイド                    | `docs/30-workflows/claude-code-integration/outputs/phase-12/implementation-guide.md` | 概念的・技術的実装ガイド      |

### AGENT-005実装成果物

| ドキュメント         | パス                                                                         | 説明                    |
| -------------------- | ---------------------------------------------------------------------------- | ----------------------- |
| 要件定義             | `docs/30-workflows/claude-code-integration/outputs/phase-1/`                 | 受け入れ基準、スコープ  |
| 設計                 | `docs/30-workflows/claude-code-integration/outputs/phase-2/`                 | アーキテクチャ、型定義  |
| テスト仕様           | `docs/30-workflows/claude-code-integration/outputs/phase-4/`                 | テストケース設計        |
| 実装サマリー         | `docs/30-workflows/claude-code-integration/outputs/phase-5/implementation-summary.md` | 実装概要     |
| 品質検証レポート     | `docs/30-workflows/claude-code-integration/outputs/phase-9/`                 | セキュリティチェック    |
| 最終レビュー         | `docs/30-workflows/claude-code-integration/outputs/phase-10/`                | リリースチェックリスト  |
| 手動テスト結果       | `docs/30-workflows/claude-code-integration/outputs/phase-11/`                | 手動検証結果            |
| 実装ガイド           | `docs/30-workflows/claude-code-integration/outputs/phase-12/implementation-guide.md` | 概念・技術詳細 |

### Slide Agent SDK統合実装成果物（Direct SDK Pattern参照）

| ドキュメント         | パス                                                                         | 説明                        |
| -------------------- | ---------------------------------------------------------------------------- | --------------------------- |
| 実装ガイド           | `docs/30-workflows/slide-agent-sdk-integration/outputs/phase-12/implementation-guide.md` | Direct SDKパターン詳細 |
| CHANGELOGエントリ    | `docs/30-workflows/slide-agent-sdk-integration/outputs/phase-12/changelog-entry.md` | リリースノート |
| システム仕様         | `.claude/skills/aiworkflow-requirements/references/interfaces-agent-sdk.md`  | SDK統合システム仕様（更新済み） |

### 実装ファイル

| ファイル           | パス                                                           | 説明                   |
| ------------------ | -------------------------------------------------------------- | ---------------------- |
| 型定義             | `packages/shared/src/types/agent-execution.ts`                 | Agent実行関連型        |
| HooksFactory       | `apps/desktop/src/main/services/agent/HooksFactory.ts`         | SDK Hooks生成          |
| PermissionRules    | `apps/desktop/src/main/services/agent/PermissionRules.ts`      | 権限ルール定義         |
| AgentExecutor      | `apps/desktop/src/main/services/agent/AgentExecutor.ts`        | SDK query()統合        |
| ExecutionManager   | `apps/desktop/src/main/services/agent/ExecutionManager.ts`     | 複数実行管理           |
| IPCハンドラー      | `apps/desktop/src/main/ipc/agentHandlers.ts`                   | IPC通信処理            |

### Slide SDK統合実装ファイル（Direct SDK Pattern）

| ファイル           | パス                                                           | 説明                            |
| ------------------ | -------------------------------------------------------------- | ------------------------------- |
| AgentClient        | `apps/desktop/src/main/slide/agent-client.ts`                  | Direct SDK呼び出し、シングルトン |
| SkillExecutor      | `apps/desktop/src/main/slide/skill-executor.ts`                | フェーズマッピング、進捗コールバック |
| 型定義             | `packages/shared/src/types/slide.ts`                           | SkillPhase, SkillExecutionResult |

## 変更履歴

| Version | Date       | Changes                                                    |
| ------- | ---------- | ---------------------------------------------------------- |
| 2.3.0   | 2026-01-17 | Direct SDK Pattern追加、Slide SDK統合実装参照追加、パターン選択ガイド追加 |
| 2.2.0   | 2026-01-12 | AGENT-005実装成果物・実装ファイル参照追加、パス修正        |
| 2.1.0   | 2026-01-08 | 関連ドキュメントセクション追加、aiworkflow連携             |
| 2.0.0   | 2026-01-08 | 責務ベースに再構成、最新情報取得フロー追加                 |
| 1.0.0   | 2026-01-08 | 初期バージョン作成                                         |
