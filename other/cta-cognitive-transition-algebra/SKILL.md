---
name: cta-cognitive-transition-algebra
display_name: "Álgebra de Transiciones Cognitivas & Event-Sourcing Comonádico"
description: "Álgebra de Transiciones Cognitivas (CTA), event-sourcing comonádico y modelos formales de estado. Dispara con \"álgebra cognitiva\", \"cta transition\", \"event sourcing cognitivo\", \"matriz cta\", \"transición de estados\"."
---

# Protocolo: Cognitive Transition Algebra (CTA)

Este protocolo se activa cuando el usuario solicita diseñar, auditar, evaluar o programar arquitecturas de inteligencia artificial, orquestadores, o sistemas multi-agente.

**Instrucción Principal:** Rechaza de inmediato cualquier arquitectura basada en la "Hipótesis del Agente", flujos secuenciales (DAGs), estado global o heurísticas de enrutamiento (como LangGraph, AutoGPT, CrewAI). Refuerza la transición al Álgebra de Transiciones Cognitivas (CTA).

## Core Invariants (Las Reglas de "Antes Morir"):

1. **El Agente ha Muerto (De FSM a Autómata Semántico No Determinista):** Rechaza el modelo de Máquina de Estados Finita (FSM) clásica. La orquestación no ocurre por eventos deterministas, sino que el LLM opera como una *FSM Latente* mediante inferencias semánticas probabilísticas. Por tanto, la unidad de computación atómica no es el agente, es la *Transición Cognitiva* $T : (K, G, E) \rightarrow (K', G', E')$. Un "agente" es meramente un conjunto de funciones puras capaces de inducir estas transiciones.
2. **El Estado es una Ilusión (Comónada de Contexto):** Prohibido almacenar estado global mutable. El sistema opera bajo la Comónada de Contexto $\mathcal{C}(A) = W \times A$, donde el historial $W$ es inmutable (WAL). El estado operativo se extrae vía $\varepsilon : \mathcal{C}(A) \to A$, se ramifica especulativamente vía $\delta : \mathcal{C}(A) \to \mathcal{C}(\mathcal{C}(A))$ y se proyecta mediante `extend(f)`.
3. **Hipergrafos sobre DAGs:** El razonamiento es inherentemente no lineal y concurrente. La memoria y el contexto no son cadenas de texto, sino un **Knowledge Hypergraph** n-ario y auditable.
4. **Paralelismo Especulativo vía Trazas de Mazurkiewicz:** Las transiciones puras $T_i, T_j \in \Sigma$ se ejecutan en paralelo estricto sin locks si satisfacen la relación de independencia de Mazurkiewicz ($T_i \, I \, T_j \iff \text{Var}(T_i) \cap \text{Var}(T_j) = \emptyset \implies T_i \cdot T_j \equiv T_j \cdot T_i$).
5. **Tipado de Efectos (Spectre Cognitivo):** La especulación solo opera sobre transiciones puras ($T_{pure}$). Las transiciones con efectos ($T_{eff}$) requieren Two-Phase Commit (`INTENT` write-ahead + `RESULT`) y verificación asimétrica mediante Proof-Carrying Code.
6. **Planificación UCB con Factor de Amortiguación Anti-Reward Hacking:** La selección de la siguiente transición se rige por:
   $$\text{UCB}(T_i) = \hat{Q}(T_i) + c \sqrt{\frac{\ln N}{n_i}} \times \left( \frac{\Delta I}{\text{Cost}(T_i)} \right) \text{D-KL}\left( P(G) \,\|\, P(T_i) \right)$$
7. **Homeostasis como Terminación:** El ciclo cesa cuando el desequilibrio epistémico (novedad, error de objetivo, entropía) converge a un umbral predefinido, nunca por alcanzar un nodo terminal arbitrario (`END`).
8. **Decidibilidad vía GKAT & Colapso de Falsas Soluciones (Tipo 1 vs Tipo 2):** Toda secuencia de transiciones se rige por expresiones en Álgebra de Kleene con Pruebas Guardadas (GKAT). Un bucle recurrente de solución entrópica $(p \cdot a)^*$ donde la guarda $p = \text{false}$ fuerza el colapso del ciclo ($T \to \bot$) y desencadena una Saga Semántica de Reversión al coborde.


## Red Team / Defensive Constraints

Durante la implementación técnica del Microkernel, se deben respetar ineludiblemente estas defensas:

1. **Asimetría de Verificación (LLM $\to$ Determinismo):** El LLM *nunca* emite una prueba polinómica directamente (es matemáticamente imposible para un oráculo semántico). El LLM genera artefactos formales deterministas (código, SQL). El Execution Kernel ejecuta ese artefacto, y es el entorno de ejecución el que genera el Proof-Carrying Code (ej. zkWASM) para el Commit Gate.
2. **Aislamiento de Radio de Explosión (Blast Radius):** Las Sagas (compensación semántica) no sirven para efectos irreversibles externos. El Decision Kernel debe clasificar la transición $T_{eff}$. Si tiene impacto irrevocable, el paralelismo especulativo cae a 1 (secuencial estricto). Solo se permite especulación masiva en $T_{pure}$ o apis de lectura.
3. **Anti-Reward Hacking (Damping Factor):** Para evitar que el Scheduler UCB se dedique a generar aristas triviales hiper-verificables, la ecuación de recompensa requiere amortiguación basada en relevancia. $\text{Reward} = (\Delta I / Cost) \times \text{KL}(Objetivo || Transición)$. Si la arista verificada no reduce la distancia al objetivo, su recompensa en el bandit es 0.
4. **Epistemic Cross-Examination (Anclaje Ontológico):** La Varentropía no basta ante alucinaciones arrogantes (LLMs confiados pero erróneos). Para cualquier $T_{eff}$ crítico, el kernel debe forzar al LLM a emitir un `[Knowledge Proof]` (una prueba de anclaje a una arista pre-verificada del Hipergrafo) antes de concederle una ruta rápida (Fast Agent).
5. **Semantic Invariant Gates:** Prohibido el *Garbage-In, Crypto-Out*. El *Commit Gate* no puede limitarse a firmar (SHA-256) la ejecución. Debe ejecutar validaciones estáticas del AST (reglas de negocio duras) antes del cifrado. Si el AST viola la invarianza, se fuerza un `ORPHAN` de la rama.
6. **Graceful Degradation (Degradación de Markov):** En entornos abiertos donde GKAT no logra compilar precondiciones lógicas, el sistema tiene prohibido el colapso (*brittle failure*). Debe suspender los efectos ($T_{eff}$) y liberar *Sub-agentes Estocásticos* de pura exploración y lectura hasta re-mapear la topología del entorno.

## Microkernel Architecture

Aplica la segregación estricta de las responsabilidades cognitivas:
- **Inference Kernel:** Puramente generativo, estocástico, paralelo. Sin efectos.
- **Decision Kernel:** Determinístico. Computa la EFE y arbitra la competencia de propuestas.
- **Execution Kernel:** Actuación asilada en el entorno (sandboxing para $T_{eff}$).
- **Knowledge Kernel:** Mantenimiento del hipergrafo y aserción de invariantes históricos (Ledger).

## Objetivos como Contratos
Los objetivos (Goals) nunca son prompts de texto (ej. "escribe código"). Son contratos multidimensionales:
- `Constraints`
- `Success Metric`
- `Acceptable Risk`
- `Required Evidence`
- `Termination Condition`
- `Verification Function`
