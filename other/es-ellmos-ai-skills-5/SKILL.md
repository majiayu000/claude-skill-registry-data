---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: Orquestación multimodelo y estrategia de cambio de modelos. Selección de modelos basada en puntuación, delegación entre agentes (Gemini, Codex, Ollama), emparejamiento con advisor, disparadores de escalado, matriz de permisos y optimización de eficiencia de costos.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="model-strategy banner">

> **Español** — Versión oficial en español de `model-strategy`.


# Estrategia de cambio de modelo (Español)

> Orquestación multimodelo: selección de modelos basada en puntuación, delegación entre agentes, emparejamiento con advisor, disparadores de escalado y optimización de eficiencia de costos

---

## 1. Catálogo de modelos

### Claude (apto para subagentes mediante la herramienta Agent)

```
Level 4 (Reviewer):   Opus 4.8  — advisor, math review     [user only: /model, /advisor]
Level 3 (Strategist): Opus 4.6  — architecture, concepts   [subagent: model:"opus"]
Level 3 (Creative):   Fable 5   — creative texts, stories  [subagent: model:"fable"]
Level 2 (Workhorse):  Sonnet 4.6— implementation, debug    [subagent: model:"sonnet"]
Level 1 (Fast):       Haiku 4.5 — boilerplate, formatting  [subagent: model:"haiku"]
```

### Agentes externos (scripts complementarios / SSH)

```
Level 2-3: Gemini 3.5 pro  — research, scientific databases [agy-companion CLI]
Level 2:   Gemini 3.5 flash— fast research                  [agy-companion CLI]
Level 2-3: Codex 5.5 (GPT) — code review, code generation   [codex-companion CLI]
Level 2:   Codex 4.5 (GPT) — simpler code tasks             [codex-companion CLI]
```

### Modelos locales (sin consumo de tokens, 24/7)

```
Level 1-2: Ollama (Qwen 3.5:35b-a3b) — Haiku-to-Sonnet level [<ollama-host>:11434]
           Invocation: SSH + curl http://<ollama-host>:11434/v1/chat/completions
           Or: delegation via an agent-system control API (if available)
```

### Matriz de alcanzabilidad

| Modelo | Iniciable por LLM | Ruta de invocación | Restricciones |
|-------|---------------|-----------------|-------------|
| Sonnet 4.6 | Sí | `Agent(model:"sonnet")` | — |
| Opus 4.6 | Sí | `Agent(model:"opus")` | — |
| Haiku 4.5 | Sí | `Agent(model:"haiku")` | — |
| Fable 5 | Sí | `Agent(model:"fable")` | — |
| Opus 4.8 | Solo advisor | `advisor()` en la sesión | el usuario debe establecer `/advisor` |
| Gemini 3.5 | Sí (Bash) | `companion-for-agy "prompt"` | Solo Windows, solución alternativa para stdout |
| Codex 5.5/4.5 | Sí (Bash) | `node codex-companion.mjs task "prompt"` | requiere autenticación |
| Ollama | Sí (SSH/curl) | SSH + curl a la API del host de Ollama | VPN/Tailscale debe estar activa |
| Opus 4.8 como modelo principal | No | usuario: `/model opus 4.8` | solo acción del usuario |
| Fable 5 como modelo principal | No | usuario: `/model fable` | solo acción del usuario |

---

## 2. Cálculo de puntuación

```
Dimensions (0-10):
  CLARITY     : How unambiguous is the task?
  COMPLEXITY  : How many components?
  CREATIVITY  : New solutions needed?
  CONTEXT     : How much prior knowledge?
  CRITICALITY : How important is perfection?

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### Umbrales de puntuación

| Puntuación | Modelo | Ejemplos |
|-------|-------|----------|
| 0-8 | Ollama (host local) | generación de prompts, resúmenes, textos sencillos |
| 9-12 | Haiku | `__init__.py`, formateo, código repetitivo (boilerplate) |
| 13-22 | Sonnet | implementación, corrección de errores, código estándar |
| 13-22 | Gemini 3.5 | investigación, búsqueda bibliográfica, bases de datos científicas |
| 13-22 | Codex 5.5 | generación de código (Luau, Node.js), scripts de cálculo |
| 23-28 | Sonnet + revisión de advisor | código complejo con control de calidad |
| 23-35 | Fable 5 | textos creativos, marketing, narrativa (storytelling) |
| 29-40 | Opus 4.6 | arquitectura, estrategia, redacción de artículos |
| 35-50 | Opus 4.6 + advisor | demostraciones, decisiones de arquitectura, estadística |
| 40-50 | Opus 4.8 (recomendación al usuario) | demostraciones matemáticas, máximo rigor |

---

## 3. Delegación entre agentes

### ¿Qué agente externo para qué tarea?

| Tarea | Mejor agente | Razón |
|------|-----------|--------|
| Búsqueda de literatura científica | Gemini 3.5 pro | habilidades nativas de OpenAlex/arXiv/PubMed |
| Revisión de código (segunda opinión) | Codex 5.5 | perspectiva independiente |
| Generación de texto sencillo | Ollama (host local) | sin consumo de tokens, 24/7 |
| Textos creativos, marketing | Fable 5 | la mejor producción creativa |
| Demostraciones matemáticas | Opus 4.8 (advisor) | máxima profundidad analítica |

### Exclusiones (debilidades documentadas)

- **Gemini:** NO para revisiones matemáticas o trabajo de demostraciones (error de dirección documentado en una revisión de demostración, 07-06-2026)
- **Codex 4.5:** solo cuando 5.5 no esté disponible; de lo contrario, siempre 5.5

### Rutas de invocación

> Reemplace los marcadores de posición `<host>`, `<ollama-host>`, `<tailscale-ip>`, `<user>` y `~/.ssh/<key>` con su propia infraestructura.

**Gemini (via companion-for-agy):**
```
companion-for-agy --researcher --json --timeout 120000 "research prompt"
```

**Codex (via codex-companion):**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "code prompt"
```

**Ollama on a remote host (via SSH):**
```
ssh -i ~/.ssh/<key> <user>@<tailscale-ip> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**Delegation to an agent system with tools (example):**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. Emparejamiento con advisor

### Mecánica

`advisor()` es una **herramienta a nivel de sesión**: el modelo advisor lo establece el usuario mediante `/advisor`, no de forma programática. Esto genera los siguientes patrones de emparejamiento:

| Patrón | Cómo funciona | Cuándo usar |
|---------|--------------|-------------|
| **Advisor de sesión** | el usuario establece `/advisor opus 4.8`, el agente llama a `advisor()` | estándar para demostraciones/arquitectura |
| **Orquestador como revisor** | el modelo principal Opus revisa la salida del subagente Sonnet | el orquestador es más fuerte que el trabajador |
| **Contra-agente** | el agente A trabaja, el agente B revisa de forma adversarial | verificación independiente, 2 perspectivas |
| **Recomendación al usuario** | el agente recomienda: "realice esta tarea con opus 4.8 + advisor" | cuando la sesión actual sea demasiado débil |

### ¿Cuándo recomendar un advisor?

- Trabajo de demostración matemática (puntuación ≥ 35)
- Decisiones de arquitectura con consecuencias a largo plazo
- Metodología estadística / diseño de estudios
- Errores complejos tras 2 o más ciclos de depuración infructuosos

### ¿Cuándo NO usar un advisor?

- Código rutinario, contenido, formateo (puntuación < 23)
- Implementación de funciones sencillas
- Tareas bien definidas y no críticas

---

## 5. Disparadores de escalado

### Ollama -> Haiku
- Se requiere acceso a archivos
- Se requiere análisis de código

### Haiku -> Sonnet
- Más de 2 archivos afectados
- Se requiere decisión entre alternativas
- Ocurrió un error inesperado
- Se solicitó una operación de eliminación

### Sonnet -> Opus
- Se requiere decisión de arquitectura
- Se deben integrar 3 o más sistemas
- Requisitos contradictorios/poco claros
- Se requiere planificación estratégica

### Sonnet -> Gemini (lateral)
- Se requiere investigación científica
- Verificación de bibliografía

### Sonnet -> Codex (lateral)
- Revisión de código como segunda opinión
- Advisor sobrecargado (revisor de respaldo)

### Opus -> Opus + advisor
- Se requiere revisión de demostración
- Decisión de arquitectura crítica
- Metodología estadística

### Desescalado
- Concepto definido -> Sonnet asume la implementación
- Tarea trivial/repetitiva -> Haiku asume el control
- Solo texto, sin acceso a herramientas -> Ollama asume el control

---

## 6. Matriz de permisos

| Operación | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|-----------|--------|-------|--------|------|--------|-------|
| Leer archivos | - | Sí | Sí | Sí | Sí* | Sí* |
| Escribir archivos | - | Sí | Sí | Sí | Sí* | Sí* |
| Eliminar archivos | - | - | Sí** | Sí | - | - |
| Comandos del sistema | - | - | Sí** | Sí | Sí* | Sí* |
| Decisiones de arquitectura | - | - | - | Sí | - | - |
| Investigación web | - | - | Sí | Sí | Sí | - |
| Llamar a advisor() | - | - | Sí | Sí | - | - |

*mediante script complementario en su propio modo sandbox
**con confirmación del usuario

---

## 7. Eficiencia de costos

### Ahorro de tokens mediante enrutamiento

| Tipo de tarea | Sin enrutamiento | Con enrutamiento | Ahorro |
|-----------|-----------------|--------------|---------|
| Trivial | Tokens de Opus | Ollama (gratis) | 100% |
| Código repetitivo | Tokens de Opus | Tokens de Haiku | ~80% |
| Código estándar | Tokens de Opus | Tokens de Sonnet | ~50% |
| Investigación | Tokens de Claude | Tokens de Gemini | ~70% (presupuesto diferente) |
| Revisión de código | Tokens de advisor() | Tokens de Codex | ~60% (presupuesto diferente) |

---

## 8. Regla de oro

> "Opus piensa, Sonnet construye, Haiku ejecuta, Ollama ahorra. Gemini investiga, Codex revisa, Fable narra."

---

## Historial de cambios

### 2.0.0 (12-06-2026)
- Delegación entre agentes: Gemini, Codex, Ollama (host local) como destinos de enrutamiento
- Emparejamiento con advisor: 4 patrones (advisor de sesión, orquestador como revisor, contra-agente, recomendación al usuario)
- Matriz de alcanzabilidad: documentado ejecutable por LLM vs. solo usuario
- Se añadió Ollama (Qwen 3.5:35b-a3b, nivel Haiku a Sonnet) como nivel 1-2
- Escalado lateral: Sonnet -> Gemini (investigación), Sonnet -> Codex (revisión)
- Exclusiones documentadas (Gemini no apto para matemáticas)
- Umbrales de puntuación extendidos a todos los modelos

### 1.0.0 (15-03-2026)
- Portado desde BACH v3.8.0 (ing-strategie v2.0.0)

---

*Portado desde BACH v3.8.0 | Ampliado con delegación entre agentes + advisor v2.0.0*
