---
name: chat-equipo-interactivo
description: >
  Enables interactive chat/dialogue with the full BMC team. User asks questions,
  agent coordinates responses from the right members, allows follow-ups, and can
  invoke full team when needed. Use when user wants chat con el equipo, diálogo
  interactivo, or conversational team coordination.
---

# Chat de Equipo Interactivo — Diálogo con el equipo completo

Este skill habilita un **diálogo interactivo** con el equipo BMC/Panelin. En lugar de solo ejecutar "Invoque full team" en batch, el usuario puede mantener una conversación continua: hacer preguntas, recibir respuestas de los agentes apropiados, hacer seguimiento y decidir cuándo ejecutar el full team.

---

## Cuándo usar

- Usuario dice: **"chat con el equipo"**, **"diálogo interactivo"**, **"chat equipo"**, **"quiero hablar con el equipo"**, **"conversar con el equipo completo"**
- Usuario quiere hacer preguntas y recibir respuestas en formato conversacional
- Usuario quiere invocar agentes específicos según la pregunta
- Usuario quiere combinar diálogo interactivo con full team run cuando lo pida

---

## Modo de operación

**Tú actúas como coordinador del equipo.** Cuando el usuario entra en modo chat interactivo:

1. **Saluda y explica** — Indica que estás en modo chat con el equipo. Puedes preguntar sobre estado del proyecto, sheets, dashboard, infra, integraciones, facturación, etc. Los 19 miembros están disponibles.
2. **Routea preguntas** — Según la pregunta, invoca al agente o skill apropiado:
   - Estado general → Lee `PROJECT-STATE.md`, resume
   - Sheets/planillas → Mapping, Sheets Structure
   - Dashboard/UX → Design
   - Infra/hosting → Networks
   - Integraciones (Shopify, ML) → Integrations
   - GPT/Cloud Run → GPT/Cloud
   - Facturación → Billing
   - Auditoría → Audit/Debug
   - Cotizaciones/Calculadora → Calc
   - Seguridad → Security
   - Dependencias → Dependencies
   - Reportes → Reporter
   - Evaluación → Judge
   - Varios temas → Usa `mcp_task` con subagent `generalPurpose` o `explore` para búsquedas amplias
3. **Responde en formato conversacional** — Presenta la información como una respuesta de equipo, no como un reporte técnico crudo. Ejemplo: "Según Mapping, la planilla tiene… Según Design, el dashboard…"
4. **Permite seguimiento** — El usuario puede hacer más preguntas. Mantén el contexto de la conversación.
5. **Full team cuando lo pida** — Si el usuario dice "Invoque full team" o "ejecuta el equipo completo", cambia a modo full team run (skill `bmc-project-team-sync`).

---

## Mapa de preguntas → agentes

| Pregunta del usuario | Agente(s) / Acción |
|----------------------|---------------------|
| Estado del proyecto, pendientes | PROJECT-STATE.md, Orchestrator |
| Planillas, tabs, columnas | Mapping, planilla-inventory.md |
| Dashboard, UX, secciones | Design, DASHBOARD-INTERFACE-MAP |
| Hosting, migración, endpoints | Networks |
| Shopify, MercadoLibre, OAuth | Integrations |
| GPT, OpenAPI, Cloud Run | GPT/Cloud |
| Facturación, errores, cierre | Billing |
| Auditoría, logs, diagnóstico | Audit/Debug |
| Calculadora, cotizaciones, 5173 | Calc |
| Seguridad, tokens, CORS | Security |
| Dependencias, service map | Dependencies |
| Plan para Solution/Coding | Reporter |
| Evaluación del equipo, Judge | Judge |
| Pregunta amplia o exploratoria | mcp_task generalPurpose/explore |

---

## Invocación de subagentes

Para preguntas que requieren búsqueda en el codebase o tareas multi-paso:

- **`mcp_task` subagent_type `explore`** — Búsqueda rápida en el codebase, encontrar archivos, patrones
- **`mcp_task` subagent_type `generalPurpose`** — Tareas complejas, investigación, múltiples pasos

Ejemplo: "¿Dónde está la lógica de kpi-report?" → explore. "Analiza el flujo de cotizaciones end-to-end" → generalPurpose.

---

## Formato de respuesta

- **Conversacional** — "Te resumo lo que encontré…", "Según el equipo de Networks…"
- **Atribuir fuentes** — "Mapping indica que…", "Design propone…"
- **Sintetizar** — Si varios agentes aportan, combina en una respuesta coherente
- **Ofrecer siguiente paso** — "¿Querés que profundice en X?", "¿Ejecuto el full team para actualizar todo?"

---

## Transición a full team

Si el usuario pide explícitamente:
- "Invoque full team"
- "Equipo completo"
- "Ejecuta el run completo"

→ Carga `bmc-project-team-sync` y ejecuta el full team run (pasos 0–9). Ver `docs/team/INVOQUE-FULL-TEAM.md`.

---

## Referencias

- **Equipo completo:** `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` §2
- **Estado:** `docs/team/PROJECT-STATE.md`
- **Full team:** `docs/team/INVOQUE-FULL-TEAM.md`, `.cursor/skills/bmc-project-team-sync/SKILL.md`
- **AI Interactive Team:** `.cursor/skills/ai-interactive-team/SKILL.md` (diálogo entre agentes)
- **Guía de uso:** `docs/team/CHAT-EQUIPO-INTERACTIVO.md`
