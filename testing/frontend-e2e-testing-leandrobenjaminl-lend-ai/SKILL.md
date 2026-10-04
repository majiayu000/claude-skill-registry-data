---
name: frontend-e2e-testing
description: "Trigger: When user asks about E2E testing, Playwright, Cypress, or end-to-end test automation. Testing End-to-End de aplicaciones frontend. Pruebas de flujos completos multi-pagina con navegador real."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# E2E Testing

## Descripcion
Testing End-to-End de aplicaciones frontend. Pruebas de flujos completos multi-pagina con navegador real.

## Tecnologías
- **Playwright**: Multi-browser (Chromium, Firefox, WebKit), mobile emulation, network intercept
- **Cypress**: Developer-friendly, time travel debugging, menos browsers

## Por qué Playwright sobre Cypress
- Soporta 3 browsers (Chrome, Firefox, Safari)
- Mobile emulation real (no solo viewport)
- Network intercept más potente
- Más rápido en CI
- Mismo equipo que Puppeteer (Google → Microsoft)

## Patrones clave

### Test E2E básico
```ts
import { test, expect } from '@playwright/test';

test('user can login and see dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page.locator('h1')).toHaveText('Dashboard');
});
```

### Mock de API
```ts
await page.route('**/api/users', async (route) => {
  await route.fulfill({ json: [{ id: 1, name: 'Test' }] });
});
```

## LEND Workflow

### 1. ANALIZAR
Identificar flujos criticos que requieren E2E. Elegir herramienta (Playwright multi-browser vs Cypress developer-friendly). Revisar tests existentes.

### 2. OFRECER/DELEGAR
Decidir enfoque: E2E completo vs integracion. Determinar browsers objetivo y datos de prueba.

### 3. HACER
Escribir tests con data-testid, mocks de API, y parallel execution. Estructurar en flujos de usuario completos.

### 4. VERIFICAR
Correr en CI contra entorno controlado. Validar que flujos criticos pasan. Guardar patrones en Engram.

## Consideraciones
- E2E tests son lentos — solo para flujos criticos
- Usa data-testid en lugar de clases CSS fragiles
- Corre en CI contra un entorno controlado
- Parallel execution para acelerar
