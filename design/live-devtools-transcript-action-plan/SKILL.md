---
name: live-devtools-transcript-action-plan
description: Convierte transcripción de navegación (voz/texto) en beats U-xx, cruza con evidencia MCP chrome-devtools (E-xx), y produce plan de acción + parches; repetible para Calculadora BMC local o prod.
metadata:
  filePattern: docs/team/ux-feedback/LIVE-DEVTOOLS*.md
---

# Transcripción + DevTools → plan de acción (repetible)

## Cuándo usarla

- El usuario **pegó o dictó** comentarios mientras usaba la app (local o prod).
- Querés **orden cronológico**, cruce con **consola/red/snapshot MCP**, y un **plan de implementación** con criterios de aceptación.
- Invocación sugerida: **“transcripción + DevTools plan”** o **“organizá mi narrativa con MCP”**.

## Entradas que el usuario puede dar

1. **Transcripción cruda** (ES/EN mezclado está bien).
2. **URL base:** default prod `https://calculadora-bmc.vercel.app` o local `http://localhost:5173/`.
3. **Imágenes / assets** opcionales (guardar en `public/images/` y referenciar por ruta estable).

## Salida obligatoria

1. **Tabla narrativa** `U-01…` con columnas: orden, **ACTION** (hecho), **EXPECT** (intención), notas de audio (p. ej. “paralim” → término UI corregido).
2. **Tabla evidencia** `E-01…`: tool MCP (`list_console_messages`, `list_network_requests`, `take_snapshot`, etc.) + hallazgo **sin inventar** (solo output real).
3. **Cruce** `User ID → Evidence IDs` + columna “¿coincide?”.
4. **Plan de acción** por fases: investigación → cambio de datos (`quoteVisorMedia`, `roofPanelCatalogMapUrls`, UI `QuoteVisualVisor`, tarjetas familia en `PanelinCalculadoraV3_backup`) → verificación (MCP otra pasada + `npm run lint` / `npm test`).
5. **Informe** en `docs/team/ux-feedback/LIVE-DEVTOOLS-NARRATIVE-REPORT-YYYY-MM-DD-<slug>.md`.
6. Si hubo trabajo sustantivo: línea en `docs/team/PROJECT-STATE.md` → **Cambios recientes**.

## Protocolo del agente

1. Normalizar transcripción a **beats ordenados**; corregir homófonos (“paralim” → pretil/Panelin según contexto; “sabas” → aguas).
2. Ejecutar MCP **chrome-devtools** en la URL acordada: navegar, **consola** (error > warn > issue), **red** (4xx/5xx), **snapshot** en pasos clave si el usuario no detalló IDs de DOM.
3. Mapear beats a **archivos probables** del repo (sin adivinar precios ni IDs de Sheets): buscar strings (`rg`) en `src/components/QuoteVisualVisor.jsx`, `src/data/quoteVisorMedia.js`, `src/data/roofPanelCatalogMapUrls.js`, `PanelinCalculadoraV3_backup.jsx`.
4. **Implementar** solo lo acordado por la transcripción + plan; assets en `public/images/`; URLs Shopify solo si el usuario pidió explícitamente CDN.
5. Cerrar con **checklist de verificación** y próxima corrida MCP (mismo flujo usuario).

## Anti-patrones

- No afirmar que MCP vio algo si no hubo tool output en el hilo.
- No mezclar hallazgos de **prod** y **local** en la misma tabla sin etiquetar entorno.
- No reemplazar imágenes de catálogo sin dejar **fallback** documentado si Shopify sync las sobrescribe (nota en informe).

## Referencias repo

- Skill narrativa MCP: `.cursor/skills/live-devtools-narrative-mcp/SKILL.md`
- Plantilla informe: `docs/team/ux-feedback/TEMPLATE-LIVE-DEVTOOLS-NARRATIVE-REPORT.md`
- Ejemplo informe transcript: `docs/team/ux-feedback/LIVE-DEVTOOLS-NARRATIVE-REPORT-2026-04-05-transcript-roof-visor-media.md`
