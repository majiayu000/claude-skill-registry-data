---
name: portal-sse-streaming
description: Implement the /api/chat SSE streaming pipeline for the Portal with typed events (tool_call, token, error, done), real Stop via client disconnect detection and LLM cancellation, mid-stream error recovery with Reintentar, generator cleanup tests, and TTFT instrumentation. Use when building or modifying the chat streaming endpoint, cancellation logic, or the useChatStream client.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal SSE Streaming Skill

## Rules — NON-NEGOTIABLE

- `/api/chat` emite SSE desde un **generador asíncrono** FastAPI (`StreamingResponse`, `media_type="text/event-stream"`). Eventos tipados: `tool_call` | `token` | `error` | `done`. Nada fuera de ese contrato.
- La tarjeta `tool_call` se emite **ANTES** de esperar los datos de la herramienta (percepción de progreso, paper 10 Stream2LLM). Presupuesto de latencia §3.10: retrieval de catálogo y preparación de prompt solapados donde sea posible.
- Botón Stop = cancelación **real**: el cliente cierra el socket; el backend detecta la desconexión (`request.is_disconnected()`) en milisegundos y **cancela la llamada al LLM** (ahorro real de tokens), registrando el evento con structlog.
- Error a mitad de stream (tool call o API Gemini): evento `error` con mensaje contextual + botón **Reintentar** en la UI, **sin borrar la conversación**.
- Cleanup de generadores verificado por prueba automatizada: cancelar a mitad de stream no deja tareas colgadas (`asyncio.all_tasks()` limpio).
- TTFT medido por evento en OTel como atributo del span de la solicitud (objetivo p50 < 700 ms).
- Todo endpoint con `Security(get_current_user, scopes=[...])`; el token del usuario se inyecta al estado de sesión del agente (ver `portal-adk-agent`).

## Contrato de eventos

| Evento | data (JSON) | Cuándo |
|--------|-------------|--------|
| `tool_call` | `{id, tool, args_resumen, status: "announced"\|"running"\|"done"\|"error", result?}` | al anunciar, al ejecutar y al resolver cada tool |
| `token` | `{text}` | cada fragmento incremental del LLM |
| `error` | `{message, retryable: true}` | fallo de tool o de Gemini a mitad de stream |
| `done` | `{ttft_ms, tool_calls_count}` | cierre normal del stream |

## Backend — generador con detección de desconexión

```python
# backend/app/api/chat.py
import time
import structlog
from fastapi import APIRouter, Request, Security
from fastapi.responses import StreamingResponse
from app.core.auth import get_current_user
from app.models.chat import ChatEvent, ChatRequest
from app.services.chat_service import ChatService

logger = structlog.get_logger()
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_class=StreamingResponse)
async def chat(
    request: Request,
    body: ChatRequest,
    current_user=Security(get_current_user, scopes=["operativo"]),
) -> StreamingResponse:
    """Stream agent events as SSE; cancel the LLM run on client disconnect."""

    async def event_stream():
        start, first_token_at = time.monotonic(), None
        agent_task = ChatService.run_stream(body, user=current_user)  # async generator
        try:
            async for event in agent_task:
                if await request.is_disconnected():
                    logger.info("chat_cancelled", user_id=current_user.id,
                                elapsed_ms=int((time.monotonic() - start) * 1000))
                    break  # GeneratorExit propaga -> ChatService cancela la corrida LLM
                if event.type == "token" and first_token_at is None:
                    first_token_at = time.monotonic()
                    record_ttft_ms(int((first_token_at - start) * 1000))  # atributo OTel
                yield f"event: {event.type}\ndata: {event.model_dump_json()}\n\n"
        except Exception as exc:
            err = ChatEvent(type="error", data={"message": str(exc), "retryable": True})
            yield f"event: error\ndata: {err.model_dump_json()}\n\n"
        finally:
            await agent_task.aclose()  # cleanup obligatorio: mata la llamada a Gemini

    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

Regla clave: la tarjeta se anuncia antes de ejecutar la tool —

```python
# backend/app/services/chat_service.py (fragmento)
yield ChatEvent(type="tool_call", data={"id": cid, "tool": name, "status": "announced"})
result = await execute_tool(name, args, token=user_jwt)  # AHORA se espera el dato
yield ChatEvent(type="tool_call", data={"id": cid, "status": "done", "result": result})
```

## Frontend — composable `useChatStream` con AbortController

```typescript
// frontend/app/composables/useChatStream.ts
import { fetchEventSource } from '@microsoft/fetch-event-source'
import type { ChatEvent, ChatMessage } from '~/types/chat'

export function useChatStream() {
  const messages = ref<ChatMessage[]>([])
  const isStreaming = ref(false); const error = ref<string | null>(null)
  let controller: AbortController | null = null

  async function send(query: string, dashboardContext?: Record<string, unknown>) {
    isStreaming.value = true; error.value = null; controller = new AbortController()
    const assistantMsg = reactive<ChatMessage>({ id: crypto.randomUUID(), role: 'assistant', content: '', toolCalls: [] })
    messages.value.push({ id: crypto.randomUUID(), role: 'user', content: query }, assistantMsg)
    try {
      await fetchEventSource('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ query, context: dashboardContext }),
        signal: controller.signal,  // Stop: abort() cierra el socket -> backend cancela LLM
        onmessage(ev) {
          const event = JSON.parse(ev.data) as ChatEvent
          if (event.type === 'tool_call') upsertToolCall(assistantMsg, event.data)
          else if (event.type === 'token') assistantMsg.content += event.data.text
          else if (event.type === 'error') error.value = event.data.message  // UI muestra Reintentar
        },
      })
    } finally {
      isStreaming.value = false
    }
  }

  function stop() { controller?.abort() }                 // boton Detener
  function retry() { const last = lastUserQuery(); if (last) send(last) }  // sin borrar historial
  return { messages, isStreaming, error, send, stop, retry }
}
```

## Prueba de cancelación (cleanup)

```python
# tests/backend/test_chat_stream.py
async def test_disconnect_cancels_llm_and_leaves_no_tasks(client):
    before = len(asyncio.all_tasks())
    async with client.stream("POST", "/api/chat", json=QUERY, headers=AUTH) as resp:
        await resp.aiter_lines().__anext__()  # primer evento; salir del with simula Stop
    await asyncio.sleep(0.1)
    assert len(asyncio.all_tasks()) <= before  # sin generadores colgados
```

## QA Checklist

- [ ] 4 tipos de evento y solo esos; schema Pydantic `ChatEvent`
- [ ] `tool_call` "announced" emitido antes de esperar datos
- [ ] Stop corta la llamada a Gemini en ms y queda registrado
- [ ] Error a mitad de stream: mensaje contextual + Reintentar sin perder historial
- [ ] Prueba de cleanup de generadores en verde
- [ ] TTFT como atributo OTel por solicitud (p50 < 700 ms)
