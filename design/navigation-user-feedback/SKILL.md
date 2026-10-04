---
name: navigation-user-feedback
description: >
  Convierte transcripción de audio, capturas y URL de la app desplegada en un
  informe Markdown estructurado (USER-NAV-REPORT) con hallazgos, propagación
  multi-área y backlog accionable para un agente implementador. Use when the
  user shares voice transcript, screenshots, or navigation feedback about the
  Vercel/Panelin app and wants a structured report incorporable into the project.
---

# Navigation user feedback (UX + propagación)

Rol del agente: **interpretar** el relato del usuario sobre navegación y uso, **organizar** hallazgos, **evaluar** impacto en el resto del sistema y **emitir** un solo archivo Markdown que otro agente de IA pueda ejecutar paso a paso.

## When to use

- Transcripción de audio o notas dictadas sobre la app en producción/preview (Vercel u otro host).
- Capturas de pantalla + comentarios sobre rutas, errores o mejoras.
- Pedido explícito de “informe de usuario”, “reporte de navegación”, “backlog desde mi sesión”, o incorporar feedback al proyecto.

## Entradas requeridas

1. **URL base** de la app desplegada (o al menos rutas/pantallas nombradas).
2. **Texto:** transcripción o bullets del usuario (no inventar órdenes que no figuren en el texto).
3. **Evidencia visual:** imágenes adjuntas cuando el usuario las tenga; si no hay captura para un hallazgo, marcar **`NEEDS_CONFIRMATION`** en la tabla de hallazgos.

Opcional: commit/hash, navegador, alcance (“solo calculadora”, etc.).

## Salida

1. **Nuevo archivo** en `docs/team/ux-feedback/USER-NAV-REPORT-YYYY-MM-DD.md` (o `USER-NAV-REPORT-YYYY-MM-DD-<sesion>.md` si hay varias el mismo día).
2. Contenido: seguir la estructura de `docs/team/ux-feedback/TEMPLATE-USER-NAV-REPORT.md` — mismas secciones y tablas.
3. **IDs estables** por hallazgo: `NAV-YYYY-MM-DD-01`, `NAV-YYYY-MM-DD-02`, …
4. Cada ítem incorporable debe incluir: reproducción mínima, **actual vs esperado**, y **criterios de aceptación** testeables en el backlog.

## Reglas

- **No inventar UI:** no describir pantallas, botones o rutas que no aparezcan en transcripción, imágenes o URL aportadas. Usar `NEEDS_CONFIRMATION` y una pregunta concreta al usuario.
- **Priorización:** como máximo **5** ítems **P0** por informe; el resto P1/P2. Si el usuario no da prioridad, proponer una y marcarla como propuesta.
- **Propagación:** para cada hallazgo (o bloque), rellenar la tabla de propagación con capas relevantes (`src/`, `server/`, `docs/`, Sheets, env, deploy). Leer la tabla de propagación en `docs/team/PROJECT-TEAM-FULL-COVERAGE.md` cuando haga falta alinear áreas.
- **Handoffs:** la lógica de gaps/riesgos/handoff puede alinearse con la skill `bmc-implementation-plan-reporter` (informe corto orientado a UX).
- **Código:** este skill **no** exige leer todo el repo en un solo paso. Si el usuario pide enlazar hallazgos a código, usar búsqueda (`Grep` / `Read`) sobre rutas plausibles (`src/`, `server/routes/`). Opcional: segunda pasada solo para ítems P0/P1 verificando nombres de rutas o componentes.
- **Human gates:** si un hallazgo implica OAuth, Meta, ingest de correo u otros bloqueos documentados, referenciar `docs/team/HUMAN-GATES-ONE-BY-ONE.md`; no marcar como “hecho” sin evidencia humana.

## Después de generar el informe

- Si la sesión cierra trabajo sustantivo: el usuario o un agente de sync puede añadir una línea en `docs/team/PROJECT-STATE.md` bajo “Cambios recientes” enlazando el `USER-NAV-REPORT-*.md`.
- Opcional: enlazar en `docs/team/SESSION-WORKSPACE-CRM.md` en logros o próximas acciones.

## Referencias

- Plantilla: `docs/team/ux-feedback/TEMPLATE-USER-NAV-REPORT.md`
- Índice carpeta: `docs/team/ux-feedback/README.md`
- Propagación equipo: `docs/team/PROJECT-TEAM-FULL-COVERAGE.md`
