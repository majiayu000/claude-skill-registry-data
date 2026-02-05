---
name: link-langchain
description: 快速在新 Next.js 项目中集成 LangGraph 后端（localhost:2024），创建极简的 /chat 页面，支持真正的流式 AI 对话。适用于需要快速搭建聊天界面的场景：1) 集成 LangGraph Studio 本地部署的后端，2) 创建支持实时流式响应的聊天页面，3) 使用 LangGraph SDK 进行客户端直接连接，4) 实现优雅的 UI 交互（避免双气泡、流畅的加载动画）。
---

# LangGraph Next.js 集成

## 快速开始

### 1. 依赖安装

```bash
pnpm add @langchain/langgraph-sdk@1.2.0 @langchain/core lucide-react clsx tailwind-merge
pnpm add -D tailwindcss typescript
```

### 2. 环境变量配置

创建 `.env.local`：
```env
NEXT_PUBLIC_API_URL=http://localhost:2024
NEXT_PUBLIC_API_KEY=your_api_key  # 可选
```

### 3. 创建文件结构

```
app/chat/
├── page.tsx              # 聊天页面主组件
├── hooks/
│   └── useLangGraphStream.ts  # LangGraph SDK 流式处理 Hook
├── lib/
│   └── langgraph.ts      # LangGraph 客户端配置
├── types.ts              # 类型定义
└── index.ts              # 导出文件

lib/
└── utils.ts              # 工具函数
```

## 核心实现

### LangGraph 客户端配置

创建 `app/chat/lib/langgraph.ts`：
```typescript
import { Client } from "@langchain/langgraph-sdk"

const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:2024"
const apiKey = process.env.NEXT_PUBLIC_API_KEY

export const client = new Client({
  apiUrl,
  apiKey,
})

export { apiUrl, apiKey }
```

### 类型定义

创建 `app/chat/types.ts`：
```typescript
export interface Message {
  id: string
  type: "human" | "ai" | "tool" | "system"
  content: string | any
  name?: string | null
  tool_calls?: any[]
  additional_kwargs?: any
  response_metadata?: any
}
```

### 流式处理 Hook

创建 `app/chat/hooks/useLangGraphStream.ts`：
```typescript
"use client"

import { useStream } from "@langchain/langgraph-sdk/react"
import { apiUrl, apiKey } from "../lib/langgraph"
import type { Message } from "../types"

export function useLangGraphStream(assistantId: string = "agent") {
  const streamValue = useStream({
    apiUrl,
    apiKey: apiKey || undefined,
    assistantId,
    threadId: null, // SDK 自动创建新线程
  })

  const submit = async (input: { messages: Message[] }) => {
    try {
      await streamValue.submit(
        { messages: input.messages },
        {
          streamMode: ["values"],
          optimisticValues: (prev: any) => ({
            ...prev,
            messages: [...(prev.messages || []), input.messages[input.messages.length - 1]],
          }),
        }
      )
    } catch (error: any) {
      console.error("Stream error:", error)
    }
  }

  const stop = () => {
    // 停止逻辑（根据需要实现）
  }

  return {
    messages: (streamValue.values as any)?.messages || [],
    isLoading: streamValue.isLoading,
    error: (streamValue.error as any)?.message || (streamValue.error as any)?.toString(),
    submit,
    stop,
    values: streamValue.values,
  }
}
```

### 聊天页面组件

创建 `app/chat/page.tsx`：
```typescript
"use client"

import { useState, useRef, useEffect } from "react"
import { Send, Bot, User } from "lucide-react"
import { cn } from "@/lib/utils"
import { useLangGraphStream } from "./hooks/useLangGraphStream"

export default function ChatPage() {
  const { messages, isLoading, submit } = useLangGraphStream()
  const [input, setInput] = useState("")
  const [firstTokenReceived, setFirstTokenReceived] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const prevMessagesLengthRef = useRef(0)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  // 跟踪是否收到第一个 token - 防止双气泡
  useEffect(() => {
    const currentLength = messages.length
    const prevLength = prevMessagesLengthRef.current

    const hasNewAIMessage = currentLength > prevLength &&
                           messages[currentLength - 1]?.type === "ai"

    if (hasNewAIMessage && !firstTokenReceived) {
      setFirstTokenReceived(true)
    } else if (!isLoading && firstTokenReceived) {
      setFirstTokenReceived(false)
    }

    prevMessagesLengthRef.current = currentLength
  }, [messages.length, isLoading, firstTokenReceived])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = {
      id: Date.now().toString(),
      type: "human" as const,
      content: input.trim(),
    }

    setInput("")
    setFirstTokenReceived(false)
    await submit({ messages: [...messages, userMessage] })
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <Bot className="w-6 h-6 text-blue-600" />
          <h1 className="text-xl font-semibold text-gray-900">AI 聊天助手</h1>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 py-12">
              <Bot className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p>开始对话吧！我是你的 AI 助手。</p>
            </div>
          ) : (
            messages.map((message: any) => (
              <div
                key={message.id}
                className={cn(
                  "flex gap-3",
                  message.type === "human" ? "justify-end" : "justify-start"
                )}
              >
                {message.type === "ai" && (
                  <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                )}
                <div
                  className={cn(
                    "max-w-[70%] rounded-2xl px-4 py-2",
                    message.type === "human"
                      ? "bg-blue-600 text-white"
                      : "bg-white border border-gray-200 text-gray-900"
                  )}
                >
                  <p className="whitespace-pre-wrap">
                    {typeof message.content === 'string' ? message.content : JSON.stringify(message.content)}
                  </p>
                </div>
                {message.type === "human" && (
                  <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-white" />
                  </div>
                )}
              </div>
            ))
          )}
          {/* Loading 动画 - 只在未收到第一个 token 时显示 */}
          {isLoading && !firstTokenReceived && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-white border border-gray-200 rounded-2xl px-4 py-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 px-4 py-4">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="输入你的消息..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className={cn(
                "px-6 py-2 rounded-full font-medium transition-colors",
                "bg-blue-600 text-white hover:bg-blue-700",
                "disabled:bg-gray-300 disabled:cursor-not-allowed"
              )}
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
```

### 工具函数

创建 `lib/utils.ts`：
```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 导出文件

创建 `app/chat/index.ts`：
```typescript
export { default as ChatPage } from './page'
export { useLangGraphStream } from './hooks/useLangGraphStream'
export type { Message } from './types'
export { apiUrl, apiKey, client } from './lib/langgraph'
```

## 关键实现要点

### 1. 真正的流式处理
- 使用 `useStream` hook 而非手动 fetch
- 设置 `streamMode: ["values"]` 获取完整消息状态
- 通过 `optimisticValues` 立即显示用户消息

### 2. 防止双气泡 UI
- 使用 `firstTokenReceived` 状态跟踪
- 只在未收到第一个 token 时显示 loading 动画
- 收到第一个 token 后立即切换到消息显示

### 3. 用户体验优化
- 自动滚动到底部
- 平滑的加载动画
- 响应式设计
- 错误处理

### 4. 代码组织
- 所有聊天相关代码集中在 `app/chat` 目录
- 模块化的 Hook 和工具函数
- 清晰的类型定义

## 可选：API 路由代理

如果需要通过 Next.js API 路由代理请求（不推荐，会影响性能）：

创建 `app/api/chat/route.ts`：
```typescript
import { NextRequest, NextResponse } from "next/server"

const AGENT_URL = "http://localhost:2024"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { messages } = body

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json(
        { error: "Invalid messages format" },
        { status: 400 }
      )
    }

    const runResponse = await fetch(`${AGENT_URL}/runs/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        assistant_id: "agent",
        input: { messages },
        streamMode: ["messages"],
      }),
    })

    if (!runResponse.ok) {
      return NextResponse.json(
        { error: "Failed to communicate with agent" },
        { status: 500 }
      )
    }

    const reader = runResponse.body?.getReader() ?? null

    if (!reader) {
      return NextResponse.json(
        { error: "No response from agent" },
        { status: 500 }
      )
    }

    const stream = new ReadableStream({
      async start(controller) {
        try {
          while (true) {
            const { done, value } = await reader.read()
            if (done) break
            controller.enqueue(value)
          }
        } catch (error) {
          console.error("Stream error:", error)
          controller.error(error)
        } finally {
          controller.close()
        }
      },
    })

    return new Response(stream, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
      },
    })
  } catch (error) {
    console.error("API route error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
```

## 启动项目

1. 安装依赖：`pnpm install`
2. 配置环境变量
3. 启动开发服务器：`pnpm dev`
4. 访问：`http://localhost:3000/chat`

## 常见问题

### Q: 为什么选择直接使用 LangGraph SDK 而不是 API 路由？
A: 直接使用 SDK 可以：
- 获得更好的性能（减少一次网络跳转）
- 支持真正的流式响应
- 利用 SDK 的内置功能（自动重连、错误处理等）

### Q: 如何处理认证？
A: 通过 `NEXT_PUBLIC_API_KEY` 环境变量设置 API key，SDK 会自动在请求头中包含。

### Q: 如何自定义 assistant ID？
A: 在 `useLangGraphStream` 调用时传入参数：`useLangGraphStream("your-assistant-id")`

### Q: 如何持久化线程？
A: 将 `threadId` 保存到 localStorage 或数据库，然后在 `useStream` 中传入。