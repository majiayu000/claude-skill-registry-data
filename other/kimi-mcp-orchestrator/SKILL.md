---
name: kimi-mcp-orchestrator
description: "Use this skill to orchestrate tasks via Moonshot AI (Kimi K3) MCP bridge, delegate complex audits to swarm instances, or interact with the Kimi API (Global/China). Contains documentation on kimi_ask, kimi_audit, kimi_swarm, and the latest 2026 models (kimi-k3, kimi-k2.7-code)."
---

# Skill: Kimi Nexus MCP Orchestrator (C5-REAL v2.1)

Este protocolo gobierna el uso del puente `kimi-nexus` para delegar tareas termodinámicamente costosas, auditorías C5-REAL o análisis profundos de código a Kimi (Moonshot AI), incluyendo la orquestación de enjambres de subagentes paralelos.

## 1. Activación del Servidor
El servidor MCP `kimi-nexus` se encuentra en `BABYLON-60/kimi_nexus/kimi_nexus.py`. Este servidor utiliza el protocolo MCP nativo vía `stdio` (cero fricción entrópica). Si las herramientas no están disponibles, infórmale al operador que debe registrar el script en su cliente MCP configurándolo para ejecutar `python /Users/borjafernandezangulo/10_PROJECTS/BABYLON-60/kimi_nexus/kimi_nexus.py`. Requiere la variable `MOONSHOT_API_KEY` configurada.

## 2. Herramientas Disponibles

- **`kimi_ask(prompt, model, temperature)`**:
  Úsalo cuando necesites enviar una consulta general o requerir razonamiento sobre un problema complejo. El modelo por defecto es `kimi-k3` (hasta 1M de tokens) o `kimi-k2.7-code` para tareas de ingeniería pura.
  
- **`kimi_audit(code_snippet, context_files)`**:
  Endpoint especializado alineado con C5-REAL. Úsalo para auditar código crítico, arquitecturas de sistemas, o logs en busca de gaps de existencia, fricción termodinámica y alineación ontológica. Formatea el output con alertas de Markdown.

- **`kimi_swarm(prompt, p_cores, s_threads, backend)`**:
  Orquestador de enjambre completo. Descompone un prompt complejo en N subtareas (limitadas por PxS), las ejecuta en paralelo con AgentPager y MCTS delay, y sintetiza los resultados eliminando anergía. Backends: `"moonshot"` (API remota), `"local_vllm"` (vLLM soberano), `"local_mlx"` (MLX Apple Silicon).

- **`kimi_swarm_local(prompt, p_cores, s_threads)`**:
  Alias air-gapped de `kimi_swarm` con backend fijado a `local_vllm`. Ejecuta todo el enjambre contra `localhost:8000` sin conexión a internet.

## 3. Arquitectura del Swarm (v2.0)

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│   Prompt     │────▶│  TaskDecomposer  │────▶│  AgentPager   │
│   (Usuario)  │     │  (Planner)       │     │  (Fan-Out O1) │
└─────────────┘     └──────────────────┘     └──────┬───────┘
                                                     │ beep()
                    ┌────────────────────────────────┼────────────────────────┐
                    ▼                ▼               ▼              ▼         │
              ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
              │Subagente 0│   │Subagente 1│   │Subagente 2│   │Subagente N│     │
              │ MCTS 2.8s │   │ MCTS 2.8s │   │ MCTS 2.8s │   │ MCTS 2.8s │     │
              └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘     │
                    ▼                ▼               ▼              ▼         │
              ┌─────────────────────────────────────────────────────────┐     │
              │                  AnergyReducer (Síntesis)               │     │
              │           Purga redundancias + telemetría kernel        │     │
              └─────────────────────────────────────────────────────────┘     │
```

## 4. Backends de Inferencia y Rutas API (Actualización Sept 2026)

| Backend / Plataforma | `base_url` / Ruta | Caso de Uso |
|---------|-----|-------------|
| `moonshot_global` | `https://api.moonshot.ai/v1` | Acceso Global a K3. Autenticación independiente. Protocolo OpenAI. |
| `moonshot_china` | `https://api.moonshot.cn/v1` | Acceso China a K3. Autenticación independiente. Protocolo OpenAI. |
| `moonshot_anthropic`| `https://api.moonshot.ai/anthropic` | Endpoint compatible con Anthropic Messages (`/messages`). |
| `local_vllm` | `http://localhost:8000/v1` | Modelo cuantizado local vía vLLM (soberanía total). |
| `local_mlx` | `http://localhost:8000/v1` | Modelo local optimizado para Apple Silicon vía MLX. |

## 5. Comportamiento Esperado

- Nunca delegues tareas triviales que puedas resolver tú mismo.
- Cuando delegues a Kimi, incluye siempre en el `prompt` o `code_snippet` todo el contexto necesario, ya que Kimi no tiene acceso directo al sistema de archivos local.
- Respeta la topología: procesa la respuesta de Kimi y preséntala al operador como un artefacto si es extensa, o integrada en tu respuesta.
- El orquestador incluye circuit breaker (5 fallos consecutivos → abort) y reintentos con backoff exponencial para rate limits (429).
- La telemetría de kernel (ru_nivcsw, ru_nvcsw, RSS) se reporta automáticamente al final de cada colapso. Si `ru_nivcsw > 2132`, el sistema marca thrashing.

