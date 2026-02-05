---
name: chatbot
description: |
  マルチターン対話管理 Skill。会話履歴管理、コンテキスト維持、Agent 連携、RAG 統合をサポート。
  チャットボット構築、対話型アシスタント、カスタマーサポートボットに使用。
version: 1.0.0
author: AgentFlow Team
triggers:
  - chat
  - チャット
  - 対話
  - conversation
  - 会話
  - assistant
  - アシスタント
  - bot
  - ボット
  - multi-turn
  - session
requirements:
  - openai>=1.0.0
tags:
  - conversation
  - dialogue
  - assistant
  - core-skill
examples:
  - "チャットボットを作成"
  - "対話セッションを管理"
  - "RAG 連携チャット"
  - "Agent 呼び出し対話"
---

# ChatBot Skill

## 概要

マルチターン対話を管理する統一 Skill。会話履歴、コンテキスト維持、Agent/RAG 連携をサポート。

## 機能

| 機能 | 説明 |
|------|------|
| **セッション管理** | 複数の対話セッションを管理 |
| **履歴管理** | 会話履歴の保存・取得・クリア |
| **コンテキスト維持** | トークン制限内でコンテキストを維持 |
| **RAG 統合** | 知識ベースからの情報取得 |
| **Agent 連携** | Coordinator/SubAgent との連携 |

## クイックスタート

### 基本的な使い方

```python
from agentflow.skills.chatbot import ChatBotSkill, ChatBotConfig

# 初期化（最小設定）
chatbot = ChatBotSkill()

# セッション作成
session = chatbot.create_session()

# 対話
response = await chatbot.chat(session.id, "こんにちは！")
print(response)  # "こんにちは！何かお手伝いできますか？"

response = await chatbot.chat(session.id, "天気について教えて")
print(response)  # "申し訳ありませんが、現在の天気情報は..."
```

### カスタム設定

```python
from agentflow.llm.llm_client import LLMConfig

# LLM 設定
llm_config = LLMConfig(
    model="gpt-4o",
    temperature=0.7,
    max_tokens=2000,
)

# ChatBot 設定
bot_config = ChatBotConfig(
    system_prompt="あなたは親切なカスタマーサポートです。",
    max_history=20,
    enable_rag=False,
)

chatbot = ChatBotSkill(llm_config=llm_config, config=bot_config)
```

### RAG 連携

```python
from agentflow.skills.rag import RAGSkill

# RAG Skill を先に初期化
rag = RAGSkill()
await rag.start()

# ドキュメント追加
await rag.add_document("製品マニュアルの内容...", topic="manual")
await rag.add_document("FAQ の内容...", topic="faq")

# RAG 連携 ChatBot
chatbot = ChatBotSkill(
    config=ChatBotConfig(enable_rag=True),
    rag_skill=rag,
)

session = chatbot.create_session()
response = await chatbot.chat(session.id, "製品の使い方を教えて")
# → RAG から関連情報を取得して回答
```

## セッション管理

### セッション作成

```python
# デフォルトセッション
session = chatbot.create_session()

# カスタム設定セッション
session = chatbot.create_session(
    system_prompt="あなたは技術サポートです。",
    metadata={"user_id": "user123", "department": "engineering"},
)

print(f"セッション ID: {session.id}")
```

### セッション取得

```python
# ID でセッション取得
session = chatbot.get_session("session_xxx")

# 全セッション一覧
sessions = chatbot.list_sessions()
for s in sessions:
    print(f"{s['id']}: {s['message_count']} messages")
```

### セッションクリア

```python
# 特定セッションをクリア
chatbot.clear_session("session_xxx")

# 全セッションをクリア
chatbot.clear_all_sessions()
```

## 会話履歴

### 履歴取得

```python
# セッションの履歴を取得
messages = chatbot.get_history(session.id)
for msg in messages:
    print(f"[{msg.role}] {msg.content}")
```

### 履歴のエクスポート

```python
# JSON 形式でエクスポート
history_json = chatbot.export_history(session.id, format="json")

# Markdown 形式でエクスポート
history_md = chatbot.export_history(session.id, format="markdown")
```

## Agent 連携

### Coordinator 連携

```python
from agentflow.patterns.coordinator import AgentCoordinator

# Coordinator を設定
coordinator = AgentCoordinator(agents=[Agent1(), Agent2()])

chatbot = ChatBotSkill(
    config=ChatBotConfig(enable_agent=True),
    coordinator=coordinator,
)

# Agent を呼び出す対話
response = await chatbot.chat(
    session.id, 
    "データを分析して",
    invoke_agent=True,  # Agent 呼び出しを有効化
)
```

## ストリーミング

```python
# ストリーミング応答
async for chunk in chatbot.chat_stream(session.id, "長い説明をして"):
    print(chunk, end="", flush=True)
print()  # 改行
```

## FastAPI 統合

```python
from fastapi import FastAPI, WebSocket
from agentflow.skills.chatbot import ChatBotSkill

app = FastAPI()
chatbot = ChatBotSkill()

@app.post("/api/chat")
async def chat(session_id: str, message: str):
    response = await chatbot.chat(session_id, message)
    return {"response": response}

@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        async for chunk in chatbot.chat_stream(session_id, message):
            await websocket.send_text(chunk)
```

## Agent 統合例

```python
from agentflow import agent, AgentClient

@agent
class CustomerSupportAgent:
    """カスタマーサポート Agent"""
    
    system_prompt = "あなたは親切なカスタマーサポートです。"
    
    def __init__(self):
        self.chatbot = ChatBotSkill()
    
    async def run(self, input_data: dict) -> dict:
        session_id = input_data.get("session_id") or self.chatbot.create_session().id
        message = input_data.get("message", "")
        
        response = await self.chatbot.chat(session_id, message)
        return {
            "session_id": session_id,
            "response": response,
        }
```

## 設定オプション

| オプション | デフォルト | 説明 |
|-----------|----------|------|
| `system_prompt` | "あなたは..." | システムプロンプト |
| `max_history` | 50 | 最大履歴メッセージ数 |
| `enable_rag` | False | RAG 統合を有効化 |
| `enable_agent` | False | Agent 連携を有効化 |
| `context_window` | 4000 | コンテキストウィンドウサイズ |

## ベストプラクティス

### 1. セッション管理

```python
# ユーザーごとにセッション管理
user_sessions: dict[str, str] = {}

def get_or_create_session(user_id: str) -> str:
    if user_id not in user_sessions:
        session = chatbot.create_session(metadata={"user_id": user_id})
        user_sessions[user_id] = session.id
    return user_sessions[user_id]
```

### 2. エラーハンドリング

```python
from agentflow.skills.chatbot import ChatBotError, SessionNotFoundError

try:
    response = await chatbot.chat(session_id, message)
except SessionNotFoundError:
    # セッションが見つからない場合は新規作成
    session = chatbot.create_session()
    response = await chatbot.chat(session.id, message)
except ChatBotError as e:
    logger.error(f"ChatBot エラー: {e}")
    response = "申し訳ありません、エラーが発生しました。"
```

### 3. メモリ管理

```python
# 定期的に古いセッションをクリア
import asyncio

async def cleanup_sessions():
    while True:
        await asyncio.sleep(3600)  # 1時間ごと
        chatbot.cleanup_old_sessions(max_age_hours=24)
```

