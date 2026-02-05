---
name: shared-layer
description: 共享层与通信机制模块。当需要定义消息类型、添加共享常量、设计 Extension-Webview 通信协议时使用。涵盖类型定义、消息格式、双向通信模式等。
---

# 共享层与通信机制

负责 Extension 与 Webview 之间的共享代码和通信协议设计。

## 目录结构

```
shared/
├─ types/
│   ├─ index.ts          # 类型导出
│   └─ message.ts        # 消息类型定义
└─ constants/
    └─ index.ts          # 共享常量
```

## Instructions

### 1. 定义新消息类型

在 `shared/types/message.ts` 添加：

```typescript
/**
 * 前后端通信消息类型
 */
export interface WebviewMessage<T = any> {
  type: string;
  payload?: T;
}

/**
 * 预定义的消息类型
 */
export const MessageTypes = {
  // 基础通信
  PING: 'ping',
  PONG: 'pong',
  
  // 通知类
  SHOW_INFO: 'showInfo',
  SHOW_ERROR: 'showError',
  
  // 业务类 - 在此添加新类型
  ANALYZE_PROJECT: 'analyzeProject',
  ANALYZE_RESULT: 'analyzeResult',
} as const;

export type MessageType = typeof MessageTypes[keyof typeof MessageTypes];

/**
 * 特定消息的 Payload 类型
 */
export interface AnalyzeProjectPayload {
  path: string;
  options?: {
    depth?: number;
    language?: 'chinese' | 'english';
  };
}

export interface AnalyzeResultPayload {
  success: boolean;
  data?: any;
  error?: string;
}
```

### 2. 通信模式

**请求-响应模式：**
```
Webview                    Extension
   |                          |
   |--- analyzeProject ------>|
   |                          |-- 处理 -->
   |<--- analyzeResult -------|
   |                          |
```

**实现示例：**

Extension 端 (`WebviewPanel.ts`)：
```typescript
private async _handleMessage(message: WebviewMessage) {
  switch (message.type) {
    case MessageTypes.ANALYZE_PROJECT:
      try {
        const result = await this.analyzeProject(message.payload);
        this._panel.webview.postMessage({
          type: MessageTypes.ANALYZE_RESULT,
          payload: { success: true, data: result }
        });
      } catch (error) {
        this._panel.webview.postMessage({
          type: MessageTypes.ANALYZE_RESULT,
          payload: { success: false, error: error.message }
        });
      }
      break;
  }
}
```

Webview 端 (`App.vue`)：
```typescript
import { vscode } from '@/api/vscode';
import { MessageTypes } from '@shared/types/message';

function analyzeProject(path: string) {
  vscode.postMessage({
    type: MessageTypes.ANALYZE_PROJECT,
    payload: { path }
  });
}

// 监听响应
window.addEventListener('message', (event) => {
  const message = event.data;
  if (message.type === MessageTypes.ANALYZE_RESULT) {
    if (message.payload.success) {
      // 处理成功结果
    } else {
      // 处理错误
    }
  }
});
```

### 3. 添加共享常量

在 `shared/constants/index.ts`：

```typescript
export const APP_CONSTANTS = {
  EXTENSION_NAME: 'ai-omni',
  WEBVIEW_ID: 'aiOmniWebview',
  
  // 配置键
  CONFIG_KEYS: {
    COMMENT_LANGUAGE: 'aiOmni.codeXray.commentLanguage',
    MAX_DEPTH: 'aiOmni.codeXray.maxDepth',
  },
  
  // 默认值
  DEFAULTS: {
    COMMENT_LANGUAGE: 'chinese',
    MAX_DEPTH: 10,
  },
} as const;
```

### 4. 类型安全的消息发送

创建类型安全的消息发送工具：

```typescript
// shared/utils/messaging.ts
import { WebviewMessage, MessageTypes } from '../types/message';

type MessagePayloads = {
  [MessageTypes.ANALYZE_PROJECT]: AnalyzeProjectPayload;
  [MessageTypes.ANALYZE_RESULT]: AnalyzeResultPayload;
  // 添加更多...
};

export function createMessage<T extends keyof MessagePayloads>(
  type: T,
  payload: MessagePayloads[T]
): WebviewMessage<MessagePayloads[T]> {
  return { type, payload };
}
```

## Best Practices

### 消息设计原则
- 每个消息类型有明确的用途
- Payload 使用 TypeScript 接口定义
- 请求-响应配对命名 (如 `xxx` / `xxxResult`)
- 错误响应包含 `success: false` 和 `error` 字段

### 类型共享原则
- 所有前后端共用的类型放在 `shared/types/`
- 使用 `as const` 确保常量类型推断
- 导出 index.ts 便于导入

### 避免的问题
- ❌ 在 Extension 或 Webview 中单独定义相同类型
- ❌ 使用魔法字符串作为消息类型
- ❌ Payload 缺少类型定义

## TypeScript 路径配置

确保两端都能正确导入 shared：

**Extension (tsconfig.json):**
```json
{
  "include": ["extension/**/*", "shared/**/*"]
}
```

**Webview (vite.config.ts):**
```typescript
resolve: {
  alias: {
    '@shared': path.resolve(__dirname, '../shared')
  }
}
```

**Webview (tsconfig.json):**
```json
{
  "compilerOptions": {
    "paths": {
      "@shared/*": ["../shared/*"]
    }
  },
  "include": ["src/**/*", "../shared/**/*"]
}
```
