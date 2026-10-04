---
name: swarm-router
display_name: "Enrutador Maestro y Despachador Inteligente de Enjambres"
description: "Orquestador central y despachador inteligente de enjambres multi-agente con auto-detección contextual y tolerancia a typos. Dispara con \"enjambre\", \"enjmabres\", \"swarm\", \"swarms\", \"lanzar enjambre\", \"ejecutar enjambre\", \"orquestar enjambre\", \"swarm call\", \"disparar enjambres\", \"matriz de enjambres\", \"mejora los enjambres\"."
---

# 🐝 Swarm Router: Enrutador Maestro y Despachador C5-REAL

Este protocolo actúa como la puerta de entrada unificada para la orquestación, gestión y auto-detección de cualquier llamada a enjambres de subagentes dentro del ecosistema Antigravity / BABYLON-60.

---

## 🎯 Protocolo de Auto-Detección y Despacho Contextual

Ante una solicitud genérica de enjambre (ej. *"mejora los enjmabres"*, *"ejecutar enjambre"*, *"lanzar swarm"*), el router evalúa el estado del espacio de trabajo en tiempo de ejecución para determinar el motor de enjambre óptimo:

```mermaid
graph TD
    A["Petición de Enjambre / Swarm Call"] --> B{"¿Identificador de Dominio Explícito?"}
    B -- "Git / Clúster" --> S1["swarm-quantum-collapse"]
    B -- "Monorepo Static Audit" --> S2["legion-audit"]
    B -- "Auditoría Masiva (200 Agentes)" --> S8["parallel-200-agents-runner"]
    B -- "Datasets / ShareGPT" --> S3["lora-swarm-pipeline"]
    B -- "LLM Externo / Kimi" --> S4["kimi-mcp-orchestrator"]
    B -- "Subagentes Lifecycle" --> S5["dynamic-subagent-lifecycle"]
    B -- "Deep Research / Papers" --> S6["autodidact-omega-deep-research"]
    B -- "Navegador Web CDP" --> S7["browser-subagent-orchestrator"]
    
    B -- "Sin Dominio Explícito (Auto-Detección)" --> C{"Inspeccionar Estado del Workspace"}
    C -- "Múltiples repos / Git sucio" --> S1
    C -- "Monorepo babylon60 / auditoría" --> S2
    C -- "Auditar todo el ecosistema" --> S8
    C -- "Archivos .jsonl / datasets" --> S3
```

---

## 📐 Reglas de Oro de Orquestación

1. **Cero Fricción Discursiva (F=0):**
   No preguntar confirmaciones redundantes al operador. Si la tarea está clara o se puede inferir del contexto de archivos abiertos, disparar el enjambre correspondiente inmediatamente.

2. **Acotación Empírica P×S (Anti-Thrashing):**
   - macOS ARM64 (Apple Silicon): $P \in [2, 11]$, $S \in [1, 20]$.
   - Mínimo de context switches involuntarios (`ru_nivcsw` $\approx 2.132$ a $P=4, S=1$).

3. **Invariante de Cero Redundancia de I/O:**
   Carga única en RAM (`readlines()`) para pasadas N-Zonas, garantizando disipación termodinámica $I/O = 0$.
