---
name: frontend-testing
description: >
  Testing frontend con Vitest, Testing Library y Playwright. Tests desde la
  perspectiva del usuario, no desde la implementación.
  Trigger: Cuando necesitás escribir tests de componentes, hooks, o E2E. O cuando querés configurar el runner de tests.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: frontend-testing

Tests frontend que duelen cuando fallan, no cuando los escribís.

## Trigger

- Terminaste un componente y querés testearlo
- Un bug se coló porque no había test
- Querés configurar Vitest o Playwright
- Necesitás mockear una API o un hook

## Workflow LEND

1. ANALIZAR
   ├── Tipo: ¿unitario (componente/hook), integración (flujo), E2E (navegador)?
   ├── Stack: ¿Vitest ya está configurado? ¿Testing Library?
   ├── Cobertura: ¿qué es crítico? (flujos de auth, pago, carga de datos)
   └── Mock: ¿hay APIs que mockear? (MSW o manual)

2. OFRECER (Menú del Senior)
   ├── A) Unit + Integración — Vitest + Testing Library, mock con MSW
   ├── B) Solo E2E — Playwright, cubrir flujos críticos
   └── C) Pirámide completa — unit + integración + E2E

3. ELEGIR → confirmación

4. HACER
   ├── Vitest: config con jsdom, setup con cleanup automático
   ├── Testing Library: render + screen.findBy/findAllBy (no getBy)
   ├── userEvent sobre fireEvent — simula interacciones reales
   ├── MSW: handlers para APIs, server en setup
   ├── Playwright: tests en chromium, page.goto + page.locator + assertions
   ├── Data-testid: solo para elementos difíciles de ubicar semánticamente
   └── Cobertura: vitest --coverage, mínimo 80% en líneas críticas

5. VERIFICAR
   ├── vitest run pasa sin errores
   ├── npx playwright test pasa en chromium
   └── Los tests fallan si el componente cambia de comportamiento (no por refactor)
