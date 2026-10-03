---
name: portal-observability
description: Instrument FastAPI with OpenTelemetry for the Portal Centralizado de Datos Financieros — request traces, db.retrieval/rag.retrieval/llm.call/llm.postprocess sub-spans, FinOps token attributes, SHA-256 prompt hashing, TTFT capture. Use when adding spans, wiring exporters (console dev / Cloud Trace), or building the tokens/cost dashboard.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Observability Skill

## Rules — NON-NEGOTIABLE

- Un trace representa cada solicitud HTTP de inicio a fin (instrumentación automática de FastAPI).
- Jerarquía de sub-spans por solicitud de chat: `rag.retrieval` → `llm.call` → `llm.postprocess`; extractores Polars siempre bajo `db.retrieval`.
- `llm.call` captura semántica FinOps: `llm.usage.prompt_tokens`, `llm.usage.completion_tokens`, `llm.usage.total_tokens`, `llm.model`, `llm.tool_calls.count`.
- PRIVACIDAD: el contenido crudo de prompt/respuesta JAMÁS va a trazas ni logs. Solo `llm.prompt_hash` (SHA-256), calculado en el PUNTO ÚNICO de salida a Gemini.
- TTFT registrado como atributo por solicitud streaming (fuente de la métrica p50 < 700 ms del plan).
- Exporter: consola en dev, Cloud Trace en cloud (selección por settings, no por comentar código).
- Propagación de contexto verificada en llamadas async (los spans hijos no deben quedar huérfanos en `asyncio.gather` / threadpool).

## Inicialización

```python
# backend/app/core/telemetry.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_telemetry(app, settings) -> None:
    provider = TracerProvider()
    if settings.env == "cloud":
        from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
        provider.add_span_processor(BatchSpanProcessor(CloudTraceSpanExporter()))
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer("portal")
```

## Span db.retrieval en extractores

```python
# ml/data/extractors.py
from app.core.telemetry import tracer

async def read_silo(silo: str) -> pl.DataFrame:
    with tracer.start_as_current_span("db.retrieval") as span:
        span.set_attribute("silo.name", silo)
        df = await asyncio.to_thread(_read_parquet, silo)  # no bloquear event loop
        span.set_attribute("db.row_count", df.height)
        return df
```

## llm.call — atributos FinOps + prompt hash

```python
# ml/agent/llm_gateway.py — PUNTO UNICO de salida a Gemini
import hashlib

def prompt_hash(prompt: str) -> str:
    """Return the SHA-256 hex digest; raw prompt content never leaves this function."""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

async def call_gemini(prompt: str, model: str, tool_calls_count: int) -> LlmResult:
    with tracer.start_as_current_span("llm.call") as span:
        span.set_attribute("llm.model", model)                    # gemini-3.5-flash-lite
        span.set_attribute("llm.prompt_hash", prompt_hash(prompt))
        first_token_at: float | None = None
        async for chunk in stream_gemini(prompt, model=model):
            if first_token_at is None:
                first_token_at = time.monotonic()
                span.set_attribute("llm.ttft_ms", (first_token_at - start) * 1000)
            yield chunk
        usage = chunk.usage_metadata
        span.set_attribute("llm.usage.prompt_tokens", usage.prompt_token_count)
        span.set_attribute("llm.usage.completion_tokens", usage.candidates_token_count)
        span.set_attribute("llm.usage.total_tokens", usage.total_token_count)
        span.set_attribute("llm.tool_calls.count", tool_calls_count)
```

Postproceso (formateo, citas del catálogo) bajo `llm.postprocess`; búsqueda híbrida del catálogo bajo `rag.retrieval`.

## Verificación de privacidad

```bash
# Ningun log/traza imprime contenido crudo — corre antes de cerrar la instrumentacion
grep -rEn "logger\.(info|debug|warning|error)\(.*\b(prompt|password|messages)\b" backend/ ml/ \
  && echo "FAIL: raw content in logs" || echo "OK"
```

## Tablero de consumo

Consumir los spans exportados y graficar: tokens/día, costo estimado/día (tokens × tarifa Flash-Lite), p50/p95 de `llm.call`. Cloud Monitoring o notebook breve — la fuente SIEMPRE son los atributos `llm.usage.*` (skill `portal-finops` los audita).

| Métrica | Fuente | Objetivo |
|---------|--------|----------|
| TTFT p50 | atributo `llm.ttft_ms` | < 700 ms |
| P90 consulta agente | duración del trace de chat | < 15 s |
| Tokens/día, costo/día | `llm.usage.total_tokens` | dentro de §23 |

## QA Checklist

- [ ] Trace por solicitud HTTP con instrumentación automática
- [ ] Sub-spans `db.retrieval` / `rag.retrieval` / `llm.call` / `llm.postprocess` anidados correctamente
- [ ] 100% de spans `llm.call` con `usage.*` y `prompt_hash` (criterio §22.3)
- [ ] Grep de privacidad limpio (cero prompts/contraseñas crudos)
- [ ] TTFT capturado en streaming
- [ ] Contexto propagado en async (spans no huérfanos)
- [ ] Exporter por settings: consola (dev) / Cloud Trace (cloud)
