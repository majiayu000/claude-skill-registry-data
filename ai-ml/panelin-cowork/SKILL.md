---
name: panelin-cowork
description: >
  Panelin Co-Work Live + Admin cotizaciones + surfaces (Admin / Gmail OCR / CRM).
  Use when working on Co-Work, wolfboard, wa_lead_to_admin, ACTION_JSON vs tools,
  email draft from chat, infoNotes/provider_reset, or reviewing operator chat transcripts
  that mix Admin sheet, Gmail, and calculator.
---

# Panelin Co-Work — surfaces, honesty, tools

Canonical skill for **operator Co-Work** sessions (JPEG screen share + Sheets/Wolfboard tools). Complements [`bmc-panelin-chat`](../../../.claude/agents/bmc-panelin-chat.md) and [`panelin-gym`](../panelin-gym/SKILL.md).

Session reports: [`docs/team/reports/PANELIN-SESSION-ANALYSIS-2026-07-20.md`](../../../docs/team/reports/PANELIN-SESSION-ANALYSIS-2026-07-20.md) (Wave 1–3), Wave 4 in PROJECT-STATE.

## Surfaces map (do not mix)

| Surface | What Panelin can do | Tools |
|---------|---------------------|--------|
| **Admin / Wolfboard** | List/create/update rows | `wolfboard_*`, `wa_lead_to_admin`, `sheets_*` |
| **CRM / quote registry** | Search clients, list quotes by month | `buscar_cliente_crm`, `listar_cotizaciones_recientes` (`desde`/`hasta`), `sheets_find` |
| **Gmail / mail (PMCA)** | Omni list/read/classify + draft + **HITL send**; OCR = HINT | `email_listar_hilos`, `email_leer_hilo`, `email_clasificar_mensaje`, `email_panelsim_resumen`, `email_borrador_saliente`, `email_enviar` |
| **Calculator UI** | Apply state + quote | Tool `aplicar_estado_calc` (not ACTION_JSON type) |

**Never:** tip in Gemini sidebar, control WhatsApp Web / Gmail DOM, claim “no CRM access” when tools exist, use `wolfboard_quote_batch` for “cargar al Admin”.

## Honesty (Wave 1+)

- Co-Work = **JPEG read-only**. Vision ≠ Sheets truth — verify with `sheets_*` / wolfboard.
- Learning = Training KB / Good-Correct — not “Google training”.
- Babeta: desarrollo **16 cm**, largo pieza ~**3 m**.

## ACTION_JSON vs tools

- **Tool** `aplicar_estado_calc` → server emits allow-listed actions via `emitAction`.
- **ACTION_JSON** types only: `setScenario`, `setLP`, `setTecho`, `setTechoZonas`, `setPared`, `setCamara`, `setFlete`, `setProyecto`, `setWizardStep`, `advanceWizard`, `buildQuote`.
- If the model emits `ACTION_JSON:{"type":"aplicar_estado_calc",...}` the server **remaps** via `buildAplicarActions` and **never leaks** raw JSON to the bubble. Unknown types are dropped.

`tipoAguas`: `una_agua` | `dos_aguas`. Operator default `aguasTecho: 1` → `una_agua` (`normalizeTipoAguas`).

## Writes + confirmation

All mutating tools need explicit operator intent (`userIntentClassifier` / `user_confirmed`):
- Create lead: `wa_lead_to_admin`
- Batch AI replies: `wolfboard_quote_batch` only when asked for mass AI responses
- CRM save / WA Cloud send / sync: existing guards

## Email

- Draft: `email_borrador_saliente` → `POST /api/email/draft-outbound` (no send).
- Inbox summary: `email_panelsim_resumen`.
- Deep IMAP cockpit: skill [`panelsim-email-inbox`](../panelsim-email-inbox/SKILL.md).

## SSE / history hygiene

- `info` → `infoNotes` (not message content); routine notes filtered in UI (`isRoutineInfoNote`).
- `provider_reset` clears bubble + infoNotes on failover.
- `stripHistoryNoise` before API history; cap 60 messages with actionable 400.
- Summarizer `KEEP_RECENT = 6`.

## Operator defaults (`operatorContext.defaults`)

- `listaPrecios: "venta"`, `aguasTecho: 1`, `crmFaltaInfoPrefix: "Falta información de:"`

## Anti-patterns (from operator sessions)

1. “Cargalas al Admin” → quote_batch (wrong) — use `wa_lead_to_admin` / interpret + create.
2. “Pendientes Gmail” → listing Admin only — clarify surface; use OCR + `email_panelsim_resumen`.
3. “Julio este año” → ask client name — use `listar_cotizaciones_recientes` with date bounds.
4. Leaking `ACTION_JSON:aplicar_estado_calc` — fixed server-side; prefer tool call.
5. Promising send email / type in Gemini — refuse honestly.

## Key files

- `server/lib/chatPrompts.js` — coworkVisionBlock, toolsBlock
- `server/lib/agentTools.js` — tools + `buildAplicarActions` / `normalizeTipoAguas`
- `server/routes/agentChat.js` — ACTION_JSON remap, `provider_reset`, TOOLS_REQUIRING_AUTH
- `src/hooks/useChat.js` — stripHistoryNoise, infoNotes filter
- `server/lib/coworkFrames.js` — formatOperatorContextBlock
- `docs/team/SDD-PANELIN-COWORK.md`
