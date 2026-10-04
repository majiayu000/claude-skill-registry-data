---
name: dynamic-subagent-lifecycle
display_name: "Supervisión del Ciclo de Vida de Subagentes Dinámicos"
description: "Gestión del ciclo de vida, mitigación de deadlocks y supervisión de subagentes dinámicos. Dispara con \"subagente dinámico\", \"ciclo de vida subagente\", \"dynamic subagent\", \"invoke_subagent\", \"supervisar subagente\"."
---

# Skill: Dynamic Subagent Lifecycle Protocol (C5-REAL / Ω)

Define las 4 reglas deterministas para la creación de **Dynamic Subagents** en el ecosistema Antigravity / BABYLON-60.

---

## 🎯 Disparadores Obligatorios de Creación

Crear un Dynamic Subagent vía `define_subagent` únicamente cuando se cumpla al menos uno de los siguientes criterios:

1. **Rol Hiper-Especializado (System Prompt Aislado):**
   - El subagente requiere directivas restrictivas o de dominio acotado (ej. *AST Walker 1-WL*, *SQLite BFT Auditor*, *Z3 Axiom Verifier*).
2. **Aislamiento de Herramientas (Least Privilege Boundary):**
   - Se requiere deshabilitar herramientas de escritura (`enable_write_tools=False`) o restringir llamadas a herramientas MCP (`enable_mcp_tools=False`).
3. **Optimización de Exergía de Contexto:**
   - La tarea debe ejecutarse en un entorno limpio para evitar la acumulación de entropía de una conversación larga.
4. **Enjambre Masivo de Micro-Agentes ($N \ge 5$):**
   - Orquestación paralela sobre múltiples repositorios o módulos aislados.

---

## ⚙️ Workflow de Ejecución 2-Step

```python
# Paso 1: Definir la especificación del subagente
define_subagent(
    name="bft_sqlite_auditor",
    description="Auditor determinista de colisiones e idempotencia en SQLite",
    system_prompt="Eres un auditor C5-REAL. Aplica INV_BFT_04 sobre committer functions...",
    enable_write_tools=True,
    enable_mcp_tools=False
)

# Paso 2: Invocar la instancia en el hypervisor
invoke_subagent(
    Subagents=[
        {
            "TypeName": "bft_sqlite_auditor",
            "Role": "Database BFT Auditor",
            "Prompt": "Audita todas las funciones de commit en babylon60/io_persist_ledger.py"
        }
    ]
)
```

---

## 📡 Patrón Agent Beeper (Zero-Friction Interruption)

Para la orquestación masiva de subagentes enjambre ($N \ge 100$), implementar siempre la primitiva de **Agent Beeper** (`AgentPager`):

1. **Suspensión de Anergía 0%**: Subagentes ingresan a un estado de letargo puro mediante `await pager.wait_for_beep(tenant_id)` en lugar de *polling* o `asyncio.sleep()`.
2. **Invariante de Desacoplamiento de Concurrencia**:
   - ❌ **Anti-Patrón (Deadlock)**: No colocar la espera de señal (`wait_for_beep`) dentro del bloque `async with semaphore:`. Esto causa inanición si $N > \text{limit}$.
   - ✅ **Patrón Correcto**:
     ```python
     # 1. Registro y espera del Beep FUERA del semáforo (0% CPU, N agentes escuchando)
     payload = await pager.wait_for_beep(tenant_id)

     # 2. Adquisición de semáforo para ejecución post-señal
     async with semaphore:
         await execute_agent_task(payload)
     ```
3. **Fan-Out Multicast $O(1)$**: Usar un `asyncio.Event` global compartido para señales de broadcast enjambre para lograr sincronización instantánea sin sobrecarga de memoria ($O(1)$ en lugar de $O(N)$ tareas).
