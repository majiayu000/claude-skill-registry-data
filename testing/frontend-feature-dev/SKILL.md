---
name: frontend-feature-dev
description: >
  Scaffold de una feature Angular nueva (componente standalone OnPush, servicio Signals,
  ruta lazy, tests Jest y Playwright+axe-core) ajustada a ADR-0001 y ADR-0012. Usar al
  crear cualquier pantalla, sección o feature nueva del frontend de Runcriticon.
disable-model-invocation: false
---

# frontend-feature-dev — Runcriticon

Scaffolding guiado de una feature Angular que cumple por construcción las sub-decisiones de ADR-0001 (D3-D12) y ADR-0012 (D1-D22): standalone, OnPush, Signals sin NgRx, cliente OpenAPI generado, lazy loading, lenguaje ubicuo en español, WCAG 2.1 AA en pantallas críticas y bundle budget vigilado.

## Cuándo usar esta skill

- Al crear una feature, pantalla o sección nueva del frontend.
- Al añadir una ruta nueva bajo `src/app/features/`.
- Cuando el usuario pida "crear un componente Angular" sin especificar la estructura.

## Argumentos

```
/frontend-feature-dev {nombreFeature}
```

`{nombreFeature}` en **español del glosario** y en camelCase o kebab-case (ej. `grupos`, `planSemanal`, `vistaHoy`, `gestion-alumnos`).

Si no se pasa el argumento, preguntar el nombre antes de continuar.

## Verificación previa

Antes de generar nada:

1. Comprobar que `frontend/src/app/features/{nombreFeature}/` no existe ya.
2. Si existe, parar y avisar al usuario.

## Preguntas al usuario

Lanzar **una sola tanda** con estas cuatro preguntas:

```
AskUserQuestion (4 preguntas):
1. ¿A qué área pertenece esta feature?
   - identidad  (login, activación, perfil)
   - club        (gestión de club y taxonomía de grupos)
   - salud       (reportes, marcas, vista de salud)
   - planificacion (editor de plan semanal, vista hoy)
   - otra        (indicar cuál)

2. ¿Requiere autenticación?
   - Sí → añadir authGuard en la ruta
   - No → ruta pública

3. ¿Es una pantalla crítica de accesibilidad?
   (login, dashboard alumno, editor plan, reportar sesión, vista salud club, gestión alumnos)
   - Sí → generar test Playwright + axe-core
   - No

4. ¿Consume datos del backend?
   - Sí → ¿qué recurso/endpoint OpenAPI? (ej. /grupos, /plan/{id})
   - No → sin servicio HTTP
```

## Artefactos a generar

| Fichero | Condición |
|---------|-----------|
| `frontend/src/app/features/{feature}/{feature}.component.ts` | Siempre |
| `frontend/src/app/features/{feature}/{feature}.component.html` | Siempre |
| `frontend/src/app/features/{feature}/{feature}.component.scss` | Siempre |
| `frontend/src/app/features/{feature}/{feature}.component.spec.ts` | Siempre |
| `frontend/src/app/features/{feature}/{feature}.routes.ts` | Siempre |
| `frontend/src/app/features/{feature}/{feature}.service.ts` | Si consume API o tiene estado compartido |
| `frontend/e2e/{feature}.spec.ts` | Solo si pantalla crítica a11y |
| `frontend/src/app/app.routes.ts` | **Actualizar**: añadir lazy import |

## Plantillas literales

### Componente — `{Feature}Component`

```typescript
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
// Importar componentes helm (src/app/ui/) según la pantalla
// ej: import { HlmButton } from '@spartan-ng/helm/button';

@Component({
  selector: 'rc-{feature}',
  standalone: true,
  imports: [],
  templateUrl: './{feature}.component.html',
  styleUrl: './{feature}.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class {Feature}Component {
  // Si hay servicio: private readonly {feature}Service = inject({Feature}Service);
}
```

### Servicio — `{Feature}Service` (solo si consume API o tiene estado)

```typescript
import { Injectable, signal, computed } from '@angular/core';
// Si consume API: import { {RecursoService} } from '../core/api/generated';

@Injectable({ providedIn: 'root' })
export class {Feature}Service {
  readonly #estado = signal<{Feature}Estado | null>(null);
  readonly estado = this.#estado.asReadonly();

  // Si hay llamada HTTP:
  // private readonly api = inject({RecursoService});
  //
  // cargar(): void {
  //   this.api.get{Recurso}().subscribe(datos => this.#estado.set(datos));
  // }
}
```

### Ruta lazy — `{feature}.routes.ts`

```typescript
import { Routes } from '@angular/router';
import { authGuard } from '../../core/auth.guard'; // eliminar si ruta pública

export const {FEATURE}_ROUTES: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./{feature}.component').then(m => m.{Feature}Component),
    canActivate: [authGuard], // eliminar si ruta pública
  },
];
```

### Entrada en `app.routes.ts`

```typescript
{
  path: '{ruta-feature}',
  loadChildren: () =>
    import('./features/{feature}/{feature}.routes').then(m => m.{FEATURE}_ROUTES),
},
```

### Test Jest — `{feature}.component.spec.ts`

```typescript
import { TestBed } from '@angular/core/testing';
import { {Feature}Component } from './{feature}.component';

describe('{Feature}Component', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [{Feature}Component],
    }).compileComponents();
  });

  it('debería crear el componente', () => {
    const fixture = TestBed.createComponent({Feature}Component);
    expect(fixture.componentInstance).toBeTruthy();
  });
});
```

### Test Playwright + axe-core — `e2e/{feature}.spec.ts` (solo pantallas críticas)

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('{Feature} — accesibilidad', () => {
  test('no debe tener violaciones WCAG 2.1 AA', async ({ page }) => {
    await page.goto('/{ruta-feature}');
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
  });

  test('flujo completo accesible solo con teclado', async ({ page }) => {
    await page.goto('/{ruta-feature}');
    // Navegar con Tab y verificar que se puede completar el flujo principal
  });
});
```

## Qué queda manual (no se genera)

- Lógica de negocio real en el servicio.
- Bindings en el template HTML (tablas, formularios, etc.).
- Imports de componentes helm/brain específicos de la pantalla.
- Integración con otros servicios o features.
- Textos marcados con `i18n` / `$localize`.
- Skeleton screens y loading states.

## Antipatrones a evitar

| Antipatrón | Regla |
|------------|-------|
| `any` en TypeScript | `@typescript-eslint/no-explicit-any: error` lo rechaza |
| `HttpClient` inyectado directamente | Usar siempre el cliente generado desde OpenAPI en `core/api/generated/` |
| Leer/guardar tokens en JS | La sesión es cookie `httpOnly`; el navegador la envía solo |
| Nombres en inglés para conceptos de dominio | Consultar `docs/glosario.md` |
| `changeDetection: ChangeDetectionStrategy.Default` | Siempre OnPush |
| `standalone: false` | Angular 19, siempre standalone |
| NgRx en el MVP | Solo Signals + servicios; promotor explícito en ADR-0012 D16 |
| Superar bundle budget | Initial 300 KB (error 350 KB); lazy route 100 KB (error 120 KB) |
| `::ng-deep` sin justificación | Penetra el ámbito del componente, fuente de bugs |
| Añadir Angular Material o segunda librería de componentes/estilos | Un solo paradigma: spartan + Tailwind v4 — ADR-0012 D5 |

## ADRs referenciados

- **ADR-0001** D3 (Angular), D4 (TypeScript strict), D5 (standalone), D6 (Signals), D10 (contract-first OpenAPI), D11 (mismo origen, cookie first-party)
- **ADR-0012** D1 (spartan.ng brain + helm), D3 (tokens CSS estilo shadcn), D4 (utilidades Tailwind en template), D6 (WCAG AA pantallas críticas), D7 (axe-core), D8 (teclado), D9 ($localize), D10 (estructura por features), D12 (cliente OpenAPI generado), D13 (CSRF interceptor), D14 (interceptor errores), D15 (interceptor 401), D16 (Signals sin NgRx), D17 (/me/permissions), D18 (route guards), D21 (Jest + Playwright), D22 (bundle budget)

## Referencias

- [referencias/arquitectura.md](referencias/arquitectura.md) — estructura de carpetas, lazy loading, bundle budgets, NFRs
- [referencias/convenciones.md](referencias/convenciones.md) — naming, español ubicuo, ESLint, Prettier
- [referencias/componentes.md](referencias/componentes.md) — spartan/helm, standalone, OnPush, Signals, template control flow
- [referencias/testing.md](referencias/testing.md) — Jest, Playwright, axe-core, cobertura mínima
- [referencias/api-client.md](referencias/api-client.md) — cliente OpenAPI, auth cookie, interceptores, permisos UI
