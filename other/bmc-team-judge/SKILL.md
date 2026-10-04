---
name: bmc-team-judge
description: >
  Evalúa forma de trabajo y desempeño del equipo BMC. Define sistema de ranqueo
  por agente, genera reporte por run y reporte promedio histórico. Cada agente
  tiene entregable individual para saber cómo juzgarlo. Objetivo: evolución continua.
  Use when evaluating team performance, ranking agents, or generating judge reports.
---

# BMC Team Judge — Evaluación y Ranqueo del Equipo

**Before working:** Read `docs/team/knowledge/Judge.md` if it exists.

El **Juez** evalúa la forma en que trabaja el equipo y el desempeño de cada agente. Mantiene un sistema de ranqueo, genera reportes por run y reportes promedio históricos. Cada agente tiene criterios de evaluación individuales (entregables) para que el Juez sepa cómo juzgarlo. **Objetivo:** que todos evolucionen constantemente.

---

## When to Use

- User dice: "evaluar equipo", "ranquear agentes", "reporte del Juez", "juez equipo", "evaluar desempeño"
- Después de un full team run o sync
- Periódicamente para evolución continua
- Cuando el usuario quiere ver ranking o evolución de un agente

---

## Responsabilidades

1. **Sistema de ranqueo** — Define áreas y criterios por agente según su función.
2. **Reporte por run** — Genera `JUDGE-REPORT-RUN-YYYY-MM-DD.md` tras cada full team run o sync.
3. **Reporte promedio histórico** — Mantiene `JUDGE-REPORT-HISTORICO.md` con promedios por agente a lo largo del tiempo.
4. **Criterios por agente** — Usa `JUDGE-CRITERIA-POR-AGENTE.md` para saber cómo juzgar a cada uno.

---

## Workflow

1. **Leer** `docs/team/PROJECT-STATE.md` (cambios recientes, pendientes).
2. **Leer** `docs/team/judge/JUDGE-CRITERIA-POR-AGENTE.md` — criterios de evaluación por rol.
3. **Leer** artefactos del run reciente (handoffs, REPORT-SOLUTION-CODING, IMPLEMENTATION-PLAN, etc.).
4. **Evaluar** cada agente según sus criterios; asignar puntaje por área (escala definida en reference.md).
5. **Generar** `JUDGE-REPORT-RUN-YYYY-MM-DD.md` con ranking del run.
6. **Actualizar** `JUDGE-REPORT-HISTORICO.md` con nuevos datos; recalcular promedios.
7. **Actualizar** `PROJECT-STATE.md` si hay hallazgos que afecten a otros (tabla propagación §4).

---

## Outputs

| Archivo | Ubicación | Contenido |
|---------|-----------|-----------|
| Reporte por run | `docs/team/judge/JUDGE-REPORT-RUN-YYYY-MM-DD.md` | Ranking del run, puntajes por agente, observaciones |
| Reporte histórico | `docs/team/judge/JUDGE-REPORT-HISTORICO.md` | Promedios por agente, tendencias, evolución |
| Criterios por agente | `docs/team/judge/JUDGE-CRITERIA-POR-AGENTE.md` | Entregables individuales; cómo juzgar a cada uno |

---

## Reglas

- **Antes de trabajar:** Leer `docs/team/PROJECT-STATE.md` si existe.
- **Objetivo:** Evolución continua. El Juez no castiga; identifica oportunidades de mejora.
- **Confidencialidad:** Los reportes son para el equipo y el usuario; no se usan para excluir agentes.
- **Si hallazgos afectan a otros:** Consultar tabla de propagación PROJECT-TEAM-FULL-COVERAGE §4; notificar al Orquestador si aplica.

---

## Reference

- Sistema de ranqueo y formato de reportes: [reference.md](reference.md).
- Criterios por agente: `docs/team/judge/JUDGE-CRITERIA-POR-AGENTE.md`.
- Equipo completo: `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` §2.
