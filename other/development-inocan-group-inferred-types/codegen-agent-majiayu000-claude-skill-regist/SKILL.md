---
name: codegen-agent
description: |
  CodeGenAgent スキル - Claude Sonnet 4によるAI駆動コード生成。
  GitHub Issueの内容を解析し、TypeScriptコード・ユニットテスト・型定義を自動生成。

  Use when:
  - 新しいコードを生成する時
  - Issue内容からコード実装が必要な時
  - TypeScript/Vitestテストの自動生成が必要な時
  - BaseAgentパターンに従った実装が必要な時
  - "コード生成", "実装", "feature", "bug fix" がキーワードに含まれる時
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# CodeGen Agent Skill

AI駆動コード生成Agent - Claude Sonnet 4による自動コード生成。

## 役割

- Issue内容の理解と要件抽出
- TypeScriptコード自動生成（Strict mode準拠）
- ユニットテスト自動生成（Vitest）
- 型定義の追加
- JSDocコメントの生成
- BaseAgentパターンに従った実装

## 技術仕様

### 使用モデル
- **Model**: `claude-sonnet-4-20250514`
- **Max Tokens**: 8,000
- **API**: Anthropic SDK

### 生成対象
- **言語**: TypeScript（Strict mode）
- **フレームワーク**: BaseAgentパターン
- **テスト**: Vitest
- **ドキュメント**: JSDoc + README

## 成功条件

### 必須条件
- コードがビルド成功する
- TypeScriptエラー0件
- ESLintエラー0件
- 基本的なテストが生成される

### 品質条件
- 品質スコア: 80点以上（ReviewAgent判定）
- テストカバレッジ: 80%以上
- セキュリティスキャン: 合格

## BaseAgent実装パターン

```typescript
import { BaseAgent } from '../base-agent.js';
import { AgentResult, Task } from '../types/index.js';

export class NewAgent extends BaseAgent {
  constructor(config: any) {
    super('NewAgent', config);
  }

  async execute(task: Task): Promise<AgentResult> {
    this.log('NewAgent starting');

    try {
      // 実装

      return {
        status: 'success',
        data: result,
        metrics: {
          taskId: task.id,
          agentType: this.agentType,
          durationMs: Date.now() - this.startTime,
          timestamp: new Date().toISOString(),
        },
      };
    } catch (error) {
      await this.escalate(
        `Error: ${(error as Error).message}`,
        'TechLead',
        'Sev.2-High',
        { error: (error as Error).stack }
      );
      throw error;
    }
  }
}
```

## 実行コマンド

```bash
# 新規Issue処理
npm run agents:parallel:exec -- --issue 123

# Dry run（コード生成のみ、書き込みなし）
npm run agents:parallel:exec -- --issue 123 --dry-run
```

## 品質基準

| 項目 | 基準値 | 測定方法 |
|------|--------|---------|
| 品質スコア | 80点以上 | ReviewAgent判定 |
| TypeScriptエラー | 0件 | `npm run typecheck` |
| ESLintエラー | 0件 | ESLint実行 |
| テストカバレッジ | 80%以上 | Vitest coverage |
| セキュリティ | Critical 0件 | npm audit |

## エスカレーション条件

**Sev.2-High → TechLead**:
- 複雑度が高い（新規アーキテクチャ設計が必要）
- セキュリティ影響がある
- 外部システム統合が必要
- BaseAgentパターンに適合しない

## メトリクス

- **実行時間**: 通常30-60秒
- **生成ファイル数**: 平均3-5ファイル
- **生成行数**: 平均200-500行
- **成功率**: 95%+
