---
name: portal-adk-agent
description: Build the Google ADK conversational agent for the Portal Centralizado de Datos Financieros with LlmAgent, manager-to-workers routing, four governed function tools that wrap FastAPI endpoints and propagate the user JWT, Gemini 3.5 Flash-Lite, and tool budget. Use when creating or modifying the agent, its tools, routing instructions, or session integration.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal ADK Agent Skill

## Rules — NON-NEGOTIABLE

- Agente con `LlmAgent` de Google ADK ✔C7: function tools Python **planas** con type hints y docstrings Google-style — ADK deriva el esquema automáticamente. NO Pydantic wrappers manuales por tool.
- Modelo: **Gemini 3.5 Flash-Lite** con `thinking_level: "medium"` por defecto; `"high"` SOLO a petición explícita del Analista.
- Arquitectura **manager → workers** (paper 01, Insight Agents): el manager rutea catálogo / datos / fuera-de-dominio (rechazo cortés en OOD, sin tool calls); workers de presentación de datos y de insights.
- Tools mínimas: `buscar_catalogo`, `consultar_metricas` (capa semántica), `solicitar_export`, `resumir_vista`. TODAS envuelven endpoints FastAPI internos y **propagan el JWT del usuario** (paper 03, Governed APIs) — el agente jamás ve datos que el usuario no puede ver. Ninguna ejecuta código libre (ni Polars ni SQL).
- Presupuesto: **máximo 5 tool calls por consulta**, declarado en la instruction del manager.
- Anti-alucinación: toda cifra de la respuesta proviene de un tool call; se cita la fuente del catálogo. Sin tool call no hay números.
- Sesiones con `Runner` + `SessionService`, alineadas a la sesión del portal (`user_id` = claim `sub`).
- Evaluación: las 9 familias del Anexo C respondidas correctamente sobre la semilla fija antes de cerrar la US.
- `structlog.get_logger()`, sin `print()`; jamás loguear el token ni el prompt crudo (solo `llm.prompt_hash`).

## Estructura del agente

```python
# ml/agent/agent.py
from google.adk.agents import LlmAgent
from ml.agent.tools import buscar_catalogo, consultar_metricas, solicitar_export, resumir_vista

MANAGER_INSTRUCTION = """
Eres el asistente del Portal Centralizado de Datos Financieros.
Enruta cada consulta a una de tres vias:
1. CATALOGO: definiciones, ubicacion de datos, reglas tribales -> buscar_catalogo.
2. DATOS: cifras, tendencias, cruces, resumenes -> consultar_metricas / resumir_vista.
3. FUERA DE DOMINIO: rechaza con cortesia sin llamar herramientas.
Reglas estrictas:
- Maximo 5 llamadas a herramientas por consulta.
- Toda cifra que menciones DEBE provenir de una herramienta; nunca inventes numeros.
- Cita siempre la fuente del catalogo (tabla y campo) junto a cada dato.
- Si el usuario carece de permisos (403), explica que rol se requiere.
- Responde en espanol neutro, sin emojis.
"""

presentation_worker = LlmAgent(
    model="gemini-3.5-flash-lite", name="presentation_worker",
    description="Formats retrieved data as tables and concise summaries with catalog citations.",
    instruction="Presenta los datos recibidos en tablas o listas breves, citando fuente del catalogo.")

insights_worker = LlmAgent(
    model="gemini-3.5-flash-lite", name="insights_worker",
    description="Produces analytical narratives (trends, risk summaries) from tool results only.",
    instruction="Genera narrativa analitica SOLO sobre resultados de herramientas ya obtenidos.")

def build_agent(thinking_level: str = "medium") -> LlmAgent:
    """Build the manager agent with governed tools and worker sub-agents.

    Args:
        thinking_level: Gemini thinking level; "high" only on explicit Analyst request.
    """
    return LlmAgent(
        model="gemini-3.5-flash-lite",
        name="portal_manager",
        instruction=MANAGER_INSTRUCTION,
        tools=[buscar_catalogo, consultar_metricas, solicitar_export, resumir_vista],
        sub_agents=[presentation_worker, insights_worker],
        generate_content_config={"thinking_config": {"thinking_level": thinking_level}},
    )
```

## Tool pattern — wrapper gobernado con propagación de Bearer

```python
# ml/agent/tools/consultar_metricas.py
import httpx
import structlog
from google.adk.tools import ToolContext

logger = structlog.get_logger()
INTERNAL_API = "http://backend:8000/api"

async def consultar_metricas(
    silo: str,
    metrica: str,
    dimensiones: list[str],
    filtros: dict[str, str],
    tool_context: ToolContext,
) -> dict:
    """Query a governed metric through the semantic layer.

    Args:
        silo: Data silo to query: "creditos", "liquidez" or "derivados".
        metrica: Metric name declared in the catalog (e.g., "saldo_total").
        dimensiones: Grouping dimensions (e.g., ["producto"]).
        filtros: Equality filters as {dimension: value}.
        tool_context: ADK context carrying session state (user JWT).

    Returns:
        Dict with rows, catalog source citation, and row_count.
    """
    token = tool_context.state["user_jwt"]  # inyectado por /api/chat al crear la sesion
    logger.info("tool_call_started", tool="consultar_metricas", silo=silo, metrica=metrica)
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{INTERNAL_API}/{silo}",
            json={"metric": metrica, "dimensions": dimensiones, "filters": filtros},
            headers={"Authorization": f"Bearer {token}"},  # paper 03: el agente hereda permisos
        )
    if resp.status_code == 403:
        return {"error": "permission_denied", "detail": "Requiere rol analista o superior."}
    resp.raise_for_status()
    return resp.json()
```

## Runner y sesiones

```python
# ml/agent/runtime.py
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(db_url=settings.DATABASE_URL)
runner = Runner(agent=build_agent(), app_name="portal", session_service=session_service)
# /api/chat crea la sesion con state={"user_jwt": token} y consume runner.run_async(...)
```

## Tabla de tools

| Tool | Endpoint envuelto | Scope minimo | Familias Anexo C |
|------|-------------------|--------------|------------------|
| `buscar_catalogo` | `/api/catalog/search` | autenticado | descubrimiento, definicion |
| `consultar_metricas` | `/api/{creditos\|liquidez\|derivados}` | operativo+ (agregaciones: analista+) | puntual, cruce, tendencia |
| `solicitar_export` | `/api/export` | analista+ | exportacion, permisos |
| `resumir_vista` | contexto Pinia serializado + `consultar_metricas` | directivo+ | resumen directivo |

## QA Checklist

- [ ] 4 tools planas con type hints + docstrings (esquema auto-derivado)
- [ ] Manager rutea OOD sin tool calls (rechazo cortes)
- [ ] JWT propagado en cada tool call; 403 explicado en conversacion
- [ ] Presupuesto de 5 tools en instruction y verificado en trazas (`llm.tool_calls.count`)
- [ ] Cifras solo de tool calls, con cita de fuente del catalogo
- [ ] 9 familias del Anexo C en verde sobre semilla fija (revision manual documentada)
