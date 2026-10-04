---
name: c5-sre-postmortem-architect
display_name: "Arquitecto de Postmortems e Incidentes SRE"
description: "Redacción de informes postmortem sin culpa (blameless) siguiendo mejores prácticas SRE, análisis 5 Whys, líneas temporales de incidentes y cálculo MTTR. Dispara con \"incident review\", \"postmortem SRE\", \"análisis de incidentes\", \"5 whys\", \"postmortem report\"."
---

# Skill: C5 SRE Postmortem Architect

Este protocolo guía la redacción rigurosa e imparcial de postmortems de incidentes de producción bajo los principios de Site Reliability Engineering (SRE) sin asignación de culpa (blameless).

---

## 1. Pipeline de Análisis de Incidentes

1. **Recopilación y Línea Temporal (Timeline):**
   - Registro cronológico UTC de la detección, alertas, contención y resolución.
   - Cálculo de MTTR (Mean Time to Recovery) y MTTD (Mean Time to Detect).

2. **Análisis de Causa Raíz (5 Whys):**
   - Profundización deductiva en cascada desde el síntoma superficial hasta la falla estructural del sistema o del proceso.

3. **Planes de Acción y Prevención de Reincidencia:**
   - Asignación de tareas preventivas priorizadas (Preventative Action Items) con dueños y SLA de remediación.

---

## 2. Salida Estructurada

Informe técnico en Markdown con resumen ejecutivo de impacto (SLO/SLA afectado), línea temporal y grafo de causas raíz.
