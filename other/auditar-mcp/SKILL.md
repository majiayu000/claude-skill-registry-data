---
name: auditar-mcp
description: Audita y verifica la conexión activa de los servidores MCP (sqlite, playwright, git, filesystem, fetch) y gh CLI.
---

# Skill: Auditoría de Servidores MCP

Ejecuta una verificación técnica de los servidores MCP configurados en `opencode.json` antes de finalizar la fase actual:

1. **Servidor SQLite (`mcp-server-sqlite`, `SQLITE_DB_PATH=data/music_catalog.db`):**
   - Ejecuta una consulta `SELECT` de prueba vía MCP sobre `music_catalog.db`.
   - Confirma la existencia y estructura de las tablas (`tracks`, `artists`, `users`).

2. **Servidor Playwright:**
   - Verifica la disponibilidad del navegador sin cabeza para pruebas E2E.

3. **GitHub (vía `gh` CLI, NO MCP — `github` MCP deshabilitado):**
   - Comprueba el estado de la autenticación (`gh auth status`) y la sincronización con el repositorio remoto.

4. **Registro:**
   - Imprime en la consola el estado de respuesta de cada herramienta MCP probada y reporta cualquier fallo de integración.

> Nota: `github` MCP está deshabilitado en `opencode.json` (consume demasiado contexto). GitHub se opera con `gh` CLI.
