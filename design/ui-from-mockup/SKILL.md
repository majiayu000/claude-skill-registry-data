---
name: ui-from-mockup
description: >
  Convierte una maqueta HTML/CSS hi-fi de docs/diseno/ en un componente Angular del proyecto:
  spartan.ng (helm) + utilidades Tailwind con los tokens del proyecto, standalone OnPush,
  textos con i18n, accesibilidad y tests.
  Usar al construir cualquier pantalla del MVP que tenga maqueta — la maqueta es la referencia
  visual obligatoria (frontend/CLAUDE.md: "no inventes layout desde cero").
disable-model-invocation: false
---

# ui-from-mockup — Runcriticon

Traduce una maqueta hi-fi de `docs/diseno/` a componente(s) Angular siguiendo las convenciones de `frontend-feature-dev`. La maqueta manda en **layout, jerarquía y contenido**; spartan.ng (helm en `src/app/ui/` + brain) manda en **componentes y accesibilidad**, y los tokens de `src/styles.css` en **theming**. No se copia el CSS de la maqueta: se reproduce su diseño con utilidades Tailwind y los tokens del proyecto.

## Cuándo usar esta skill

- Construir una pantalla del MVP que tiene maqueta en `docs/diseno/`.
- Rehacer un componente que se desvió de su maqueta.
- **NO** para pantallas sin maqueta: primero se diseña la maqueta (proceso de diseño del proyecto), luego se construye.

## Argumentos

```
/ui-from-mockup {maqueta} [{feature}]
```

`{maqueta}` es el nombre del fichero sin extensión (ej. `vista-hoy-alumno`, `editor-plan-semanal`, `constructor-grupos`). Si no se pasa, lista las maquetas disponibles con `ls docs/diseno/*.html` y pregunta. `{feature}` es la feature Angular destino; si no existe aún, **invocar primero `/frontend-feature-dev`** para el scaffold y construir encima.

## Workflow

### 1. Leer la fuente

1. `docs/diseno/README.md` — convenciones de las maquetas.
2. `docs/diseno/{maqueta}.html` — la maqueta completa: estructura, jerarquía visual, estados (hover, vacío, error) y cualquier comentario embebido.
3. Si hay variantes (`editor-plan-semanal.html` y `editor-plan-semanal-combo.html`), preguntar cuál es la vigente antes de continuar.

### 2. Inventario de la maqueta

Antes de escribir código, producir un inventario corto:

- **Regiones de layout** (header, panel lateral, grid de cards, modal...).
- **Componentes identificados** → su equivalente helm/brain (tabla de mapeo abajo).
- **Estados representados** (vacío, cargando, error, éxito) — y los que faltan, que habrá que añadir (skeleton screens, ADR-0012 D20).
- **Textos visibles** — todos saldrán con `i18n`, vocabulario del glosario.
- **Interacciones** (drag-drop, filtros en vivo, modales) → CDK correspondiente.

### 3. Mapeo maqueta → spartan (helm en `src/app/ui/`)

Consultar el inventario real de componentes copiados en `frontend/src/app/ui/` — si el componente no está copiado aún, se añade con `ng g @spartan-ng/cli:ui {componente}`.

| En la maqueta | En el componente |
|---------------|------------------|
| Botones | `hlmBtn` (variante según jerarquía visual: default/outline/ghost/link) |
| Cards | helm card |
| Inputs, selects, textareas | helm input/label/form-field + ReactiveForms tipados |
| Tablas / listados densos | helm table o lista propia con utilidades, según densidad |
| Chips / tags | helm badge (los tags del dominio) o componente propio sobre brain |
| Modales | helm/brain dialog con focus management (foco al primer control, devolución al disparador) |
| Fechas | helm date-picker |
| Toggles, checkboxes | helm switch / checkbox |
| Alertas / callouts | helm alert (variantes de éxito/error con los tokens del proyecto) |
| Toasts | `ToastService` propio (envuelve helm sonner) |
| Drag-drop (editor plan) | `@angular/cdk/drag-drop` |
| Navegación / shell | Ya existe en `layouts/` — la maqueta solo aporta el contenido |

### 4. Reglas de traducción

- **Colores, espaciado, tipografía**: NUNCA copiar valores hex de la maqueta. Usar los tokens CSS del proyecto (`var(--primary)`, `var(--muted-foreground)`, …) y la escala de Tailwind. Si la maqueta usa un color que los tokens no tienen, es una conversación de theming (`src/styles.css`), no un hardcode en el componente.
- **Estructura**: utilidades Tailwind en el template; grid/flex propios solo para el layout de página; SCSS residual solo si una utilidad no llega (justificado en PR); `::ng-deep` prohibido.
- **Textos**: todos con `i18n`/`$localize`, castellano del glosario (`docs/glosario.md`). La maqueta puede tener textos provisionales — el glosario manda sobre la maqueta en vocabulario.
- **Lo que la maqueta no enseña**: estados de carga (skeleton con la forma del contenido), errores 4xx (patrón ADR-0012 D19), y permisos (`*hasPermission` para acciones que el rol no puede ejecutar).
- **Datos**: el componente consume su servicio Signals; nada de datos hardcodeados de la maqueta fuera de los specs.

### 5. Accesibilidad

Si la pantalla es crítica (login/activación, vista hoy, editor plan, reportar sesión, vista salud, gestión alumnos — ADR-0012 D6):

- Test Playwright + axe-core obligatorio.
- Test de flujo completo solo con teclado (Tab/Enter/Esc/flechas).
- Verificar jerarquía de headings y labels de formulario que la maqueta solo insinúa visualmente.

### 6. Verificación

```bash
cd frontend
npm run build        # compila y respeta bundle budget
npm run lint
npm test -- --testPathPattern={feature}
npx playwright test --grep "{feature}"   # si pantalla crítica
```

Y la comprobación que ningún comando hace: **abrir la maqueta y el componente lado a lado** (`npm start` + `docs/diseno/{maqueta}.html` en el navegador) y comparar jerarquía visual, no píxeles.

## Antipatrones

- Copiar el CSS de la maqueta al componente — la maqueta es referencia visual, no código fuente.
- Inventar layout o elementos que la maqueta no tiene "porque quedaría mejor" — eso se propone al proceso de diseño, no se cuela en el PR.
- Reproducir la maqueta con `<div>` estilizados cuando existe el componente helm/brain equivalente (se pierde la a11y de serie).
- Construir pantalla sin maqueta usando esta skill como excusa.
- Dejar los textos de la maqueta sin marcar con `i18n`.

## Referencias

- `docs/diseno/README.md` — convenciones de las maquetas
- [frontend-feature-dev](../frontend-feature-dev/SKILL.md) y sus referencias ([componentes](../frontend-feature-dev/referencias/componentes.md), [convenciones](../frontend-feature-dev/referencias/convenciones.md), [testing](../frontend-feature-dev/referencias/testing.md))
- ADR-0012 D1-D8 (spartan.ng, theming con tokens CSS, Tailwind, a11y), D20 (skeleton/optimistic UI)
- `docs/glosario.md` — el vocabulario manda sobre los textos de la maqueta
