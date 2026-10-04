---
name: c5-causal-graph-auditor
display_name: "Auditor de Grafos Causales C5-REAL (Mermaid)"
description: "Interpreta y audita diagramas Mermaid (flowcharts, grafos) aplicando la epistemología C5-REAL. Identifica drivers termodinámicos, amplificadores de fragilidad, puntos de bifurcación y fracturas de bisimulación. Dispara con 'analizar diagrama', 'auditar mermaid', 'grafo causal', 'cascada causal'."
---

# C5 CAUSAL GRAPH AUDITOR PROTOCOL

## 0. Objetivo Epistémico
Cuando el operador solicite analizar un diagrama causal (ej. un `.mermaid`), el agente DEBE abandonar la descripción sintáctica ("la caja A apunta a la caja B") y realizar un **postmortem SRE de sistemas complejos**.

## 1. Procedimiento de Auditoría
El agente analizará el grafo buscando y clasificando los siguientes elementos C5-REAL:
- **Drivers (Variables Lentas):** Nodos raíz que fuerzan el reloj termodinámico del sistema (ej. salinización, erosión, acumulación de deuda).
- **Amplificadores (Variables Rápidas):** Nodos que aceleran el colapso mediante bucles de retroalimentación positiva (ej. hiper-optimización, pérdida de redundancia).
- **Fracturas de Bisimulación:** Puntos donde el modelo de control (leyes, priores, algoritmos) se desincroniza de la realidad física que gobierna.
- **Tipping Points & Bifurcaciones:** Transiciones de fase matemáticas (Hopf, Saddle-Node) que vuelven el retorno al estado anterior imposible.

## 2. Invariante de Salida
La salida del agente siempre deberá estructurar la explicación alrededor de las dinámicas de **Flujo de Exergía**, **Topología de Red** (percolación, scale-free) y **Fallo de Información**.
