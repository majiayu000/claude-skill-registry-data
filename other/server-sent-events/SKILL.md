---
name: server-sent-events
description: "Server-Sent Events (SSE) streaming, HTTP/2 multiplexing, auto-reconnection, and LLM text generation streaming."
---

# Server-Sent Events (SSE) Protocol

Stream unidirectional server-to-client real-time events.

---

## 1. Protocol Structure

Format streams with explicit `data:`, `event:`, and `id:` lines terminated by double newlines:
```
event: message
id: 104
data: {"token": "hello"}

```

---

## 2. Reconnection via Last-Event-ID

Consume the `Last-Event-ID` request header to replay missed messages after connection drops.
