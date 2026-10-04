---
name: c5-interactive-gantt-planner
display_name: "Planificador Interactivo Gantt y Ruta Crítica"
description: "Generación de diagramas Gantt y mapas de historias HTML interactivos con análisis de Ruta Crítica (Critical Path Method - CPM) e identificación de holguras. Dispara con \"gantt planner\", \"gantt chart\", \"critical path\", \"ruta crítica\", \"mapa de historias\"."
---

# Skill: C5 Interactive Gantt & Critical Path Planner

Este protocolo construye diagramas de Gantt interactivos en HTML/SVG con cálculo explícito de la Ruta Crítica (CPM) y holguras de tareas.

---

## 1. Algoritmo CPM (Critical Path Method)

1. **Forward Pass (Early Start / Early Finish):**
   - $ES_i = \max_{p \in Predec(i)} (EF_p)$
   - $EF_i = ES_i + Duration_i$

2. **Backward Pass (Late Start / Late Finish):**
   - $LF_i = \min_{s \in Suces(i)} (LS_s)$
   - $LS_i = LF_i - Duration_i$

3. **Holgura (Float/Slack) y Ruta Crítica:**
   - $Float_i = LS_i - ES_i = LF_i - EF_i$
   - Tareas con $Float_i = 0$ conforman la **Ruta Crítica**.

---

## 2. Salida Entregable

Generación de archivo HTML autosuficiente (sin dependencias externas pesadas) que renderiza el diagrama Gantt interactivo con resaltado dinámico de la Ruta Crítica.
