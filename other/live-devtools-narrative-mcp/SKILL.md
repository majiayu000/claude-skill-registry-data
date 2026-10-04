---
name: live-devtools-narrative-mcp
description: >
  Live DevTools narrative (Narrativa en vivo DevTools): sesión en Cursor donde el
  agente usa el MCP chrome-devtools para navegar la app (default
  calculadora-bmc.vercel.app), extrae consola/red/performance/DOM según aplique,
  y cruza en tiempo real con la narrativa del usuario (chat o transcripción
  pegada), organizada para lectura. Use when the user says Live DevTools
  narrative, Narrativa en vivo DevTools, or wants MCP browser evidence linked
  to their commentary on the Calculadora BMC Vercel app.
---

# Live DevTools narrative (MCP + voz/texto del usuario)

## Nombre canónico (invocación)

- **EN:** **Live DevTools narrative**
- **ES:** **Narrativa en vivo DevTools** (o **Narrativa MCP DevTools**)

Cuando el usuario use cualquiera de esas frases, **esta skill tiene prioridad** sobre un informe solo textual: implica que el agente debe **usar herramientas del MCP `chrome-devtools`** cuando estén disponibles en el cliente, no solo inferir desde texto.

## Rol del agente

1. **Navegar** la URL acordada (default producción Calculadora BMC: `https://calculadora-bmc.vercel.app`) con el MCP.
2. **Registrar evidencia** del navegador: al menos **consola** y **red** en cada “cierre de bloque”; **snapshot** o **screenshot** cuando ayude a anclar la UI al comentario del usuario.
3. **Organizar** lo que el usuario escriba o pegue (transcripción, dictado, bullets) en una **línea de tiempo legible** con IDs estables (`U-01`, `U-02`, …).
4. **Vincular** cada ítem del usuario con ítems de evidencia (`E-01`, `E-02`, …): tabla *expectativa vs observado*.
5. **Emitir** un informe Markdown en el repo siguiendo la plantilla (misma corrida o al cierre de sesión).

## Requisitos

- **MCP `chrome-devtools`** habilitado en Cursor (ver `.cursor/mcp.json` en el repo).
- **Node** y **Chrome** según requisitos del paquete `chrome-devtools-mcp`; **espacio en disco** suficiente para `npx` (si falla `ENOSPC`, no hay MCP — avisar y seguir solo con texto si el usuario lo pide).

**Límite:** el MCP **no escucha** audio; la narrativa debe entrar como **texto en el chat** o **transcripción pegada**.

## URL y alcance

| Parámetro | Default | Notas |
|-----------|---------|--------|
| Base URL | `https://calculadora-bmc.vercel.app` | El usuario puede fijar otra (preview, `localhost:5173`, subruta). |
| Ámbito | Web app Calculadora / Panelin | Si el flujo cruza API Cloud Run, anclar por **URL de request** en la pestaña red (lo que ve el cliente). |

## Formato recomendado para el usuario (mejor lectura y cruce)

Pedir o normalizar así:

```text
ACTION: [qué hacés o qué hizo el agente]
EXPECT: [qué esperás ver o qué debería pasar]
```

Transcripción larga: prefijar bloques con **`[mm:ss]`** o **`Paso N`** para que la tabla de cruce sea estable.

## Protocolo del agente (MCP)

Ejecutar en bucle según la conversación:

1. **`navigate_page`** (o equivalente) a la URL acordada; **`wait_for`** carga estable si hace falta.
2. Tras cambios de ruta o acciones importantes: **`list_console_messages`** (prioridad **error**, luego **warning**).
3. **`list_network_requests`**: prioridad **fallos** (4xx/5xx), luego **lentitud** si el usuario menciona espera.
4. Opcional: **`take_snapshot`** o **`take_screenshot`** para anclar UI a `U-xx`.
5. Si el usuario describe **lentitud**: **`performance_start_trace`** / **`performance_stop_trace`** o **`performance_analyze_insight`** cuando el MCP lo permita; relacionar hallazgos con los `EXPECT` del usuario.

**No inventar** mensajes de consola, URLs ni status HTTP: solo lo devuelto por las tools o pegado explícitamente por el usuario.

## Salida (artefactos)

1. **Informe principal:** `docs/team/ux-feedback/LIVE-DEVTOOLS-NARRATIVE-REPORT-YYYY-MM-DD-<slug>.md` usando la plantilla [`TEMPLATE-LIVE-DEVTOOLS-NARRATIVE-REPORT.md`](../../../docs/team/ux-feedback/TEMPLATE-LIVE-DEVTOOLS-NARRATIVE-REPORT.md).
2. **JSON opcional** (si el usuario pidió trazabilidad máquina-legible o hay muchos ítems): `docs/team/ux-feedback/LIVE-DEVTOOLS-NARRATIVE-EVIDENCE-YYYY-MM-DD-<slug>.json` — array de objetos `{ "id": "E-01", "tool": "...", "summary": "...", "linkedUserIds": ["U-01"] }` más `userBeats` espejo de la narrativa.

**IDs hallazgos mezcla UX + técnico:** `LDN-YYYY-MM-DD-01`, `LDN-YYYY-MM-DD-02`, …

## Relación con otras skills

| Situación | Usar |
|-----------|------|
| Sin MCP / solo transcripción + capturas + URL | `navigation-user-feedback` → `USER-NAV-REPORT-*.md` |
| Vídeo + método nombrado | `user-session-video-to-backlog` / **Video-User-interactive-dev** |
| Esta skill | **Live DevTools narrative** + MCP + narrativa en el mismo hilo |

## Después de la sesión

- Si el informe cierra trabajo sustantivo: añadir línea en `docs/team/PROJECT-STATE.md` bajo **Cambios recientes** con enlace al `LIVE-DEVTOOLS-NARRATIVE-REPORT-*.md`.
- **Human gates** (cm-0 / cm-1 / cm-2): si un hallazgo los implica, referenciar `docs/team/HUMAN-GATES-ONE-BY-ONE.md`; no marcar corregido sin evidencia.

## Referencias

- Plantilla: `docs/team/ux-feedback/TEMPLATE-LIVE-DEVTOOLS-NARRATIVE-REPORT.md`
- Índice: `docs/team/ux-feedback/README.md`
- MCP proyecto: `.cursor/mcp.json`
