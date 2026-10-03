---
name: run-quality-gates
description: Ejecuta la suite completa de pruebas (tipos, pruebas unitarias y E2E con Playwright) y reporta el estado general del proyecto.
---

### Instrucciones para el Agente:
1. Ejecuta la verificación de tipos de TypeScript:
   `pnpm typecheck`
2. Ejecuta la suite de pruebas unitarias con Vitest:
   `pnpm test:unit`
3. Ejecuta las pruebas E2E con Playwright utilizando el servidor MCP de Playwright o el comando CLI:
   `pnpm test:e2e`
4. Si alguna prueba falla, analiza el stack trace, aplica la corrección mínima necesaria y reejecuta hasta obtener un estado 100% verde (Exit code 0).