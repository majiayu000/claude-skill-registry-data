---
name: streaming-patterns
description: "Implement SSE, WebSockets, LLM token streaming, and real-time broadcasting in FastAPI."
context: fork
globs: []
alwaysApply: false
---

# Streaming Patterns

Server-sent events, WebSocket connections, LLM token streaming, real-time broadcasting, and streaming error handling in FastAPI.

---

## Server-Sent Events (SSE)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def event_generator():
    for i in range(5):
        yield f"data: Message {i}\n\n"
        await asyncio.sleep(1)

@app.get("/stream")
async def stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

### Frontend SSE Client
```javascript
const eventSource = new EventSource('/stream')
eventSource.onmessage = (e) => console.log(e.data)
eventSource.onerror = () => eventSource.close()
```

---

## WebSocket

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Echo: {data}")
```

### Frontend WebSocket Client
```javascript
const ws = new WebSocket('ws://localhost:8000/ws')
ws.onmessage = (e) => console.log(e.data)
ws.send('Hello')
```

---

## LLM Token Streaming

```python
async def stream_llm(prompt: str):
    async for chunk in llm.astream(prompt):
        yield f"data: {chunk.content}\n\n"

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        stream_llm(request.prompt),
        media_type="text/event-stream"
    )
```

---

## Redis Pub/Sub Broadcasting

```python
import redis.asyncio as redis

redis_client = redis.Redis()

async def broadcast(channel: str, message: str):
    await redis_client.publish(channel, message)

async def subscribe(channel: str):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    async for message in pubsub.listen():
        yield f"data: {message['data'].decode()}\n\n"
```

---

## Backpressure & Throughput

```python
from asyncio import Queue

class BackpressureQueue:
    def __init__(self, maxsize: int = 100):
        self.queue = Queue(maxsize=maxsize)

    async def put(self, item):
        if self.queue.full():
            await self.queue.get()  # Drop oldest
        await self.queue.put(item)

    async def get(self):
        return await self.queue.get()
```

---

## Streaming Error Handling

```python
async def safe_stream():
    try:
        async for chunk in generator():
            yield f"data: {chunk}\n\n"
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"
    finally:
        yield "data: [DONE]\n\n"
```

---

## Monitoring

- Track tokens/second for LLM streams
- Monitor active WebSocket connections
- Log SSE disconnects for debugging
- Set connection timeouts (default: 30s)

---

## Best Practices

- Always handle disconnects gracefully
- Set appropriate timeouts
- Use backpressure queues for high-throughput
- Send `[DONE]` signal when stream ends
- Log stream errors for observability
