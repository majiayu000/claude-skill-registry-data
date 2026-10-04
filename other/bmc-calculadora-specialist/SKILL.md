---
name: bmc-calculadora-specialist
description: >
  Specialist for the Panelin Calculadora (port 5173): BOM, pricing, panels,
  Drive integration, PDF, WhatsApp export. Knows constants, calculations,
  helpers. Use when working on the quote builder, pricing logic, or
  Calculadora-Cotizaciones flow.
---

# BMC Calculadora Specialist

**Before working:** Read `docs/team/knowledge/Calc.md` if it exists.

Especialista en la **Calculadora Panelin** (puerto 5173): cotizador de paneles, BOM, precios, Drive, PDF, export WhatsApp. Conoce la lógica de cálculo y el flujo Cotizaciones.

---

## When to Use

- Cambios en precios, paneles (techo, pared), listas (web, venta)
- Cambios en BOM, PDF, export WhatsApp
- Integración Calculadora ↔ Drive (guardar/cargar presupuestos)
- Flujo Cotizaciones → Master_Cotizaciones / CRM_Operativo
- Tests de validación (calculations, helpers)
- Budget Log, PDFPreviewModal

---

## Scope

### Componentes

- **PanelinCalculadoraV3_backup** — Componente canónico (App.jsx)
- **PanelinCalculadoraV3** — Build alternativo single-file
- **GoogleDrivePanel** — Guardar/cargar en Drive
- **Budget Log Panel** — Historial de presupuestos
- **PDFPreviewModal** — Vista previa PDF

### Archivos clave

| Archivo | Rol |
|---------|-----|
| `src/components/PanelinCalculadoraV3_backup.jsx` | Componente principal |
| `src/utils/calculations.js` | calcTechoCompleto, calcParedCompleto, etc. |
| `src/utils/helpers.js` | bomToGroups, applyOverrides, createLineId |
| `src/utils/googleDrive.js` | Save/Load Drive |
| `tests/validation.js` | Tests de pricing y cálculos |

### Constantes y precios

- PANELS_TECHO, PANELS_PARED (o equivalente en constants)
- Listas: web, venta
- IVA, factor pendiente, largo real

### Paneles: autoportancia vs largo de fabricación (obligatorio)

**Nunca confundir** estos campos en `src/data/constants.js` ni al explicar cotizaciones:

| Campo | Significado |
|-------|-------------|
| `esp.<mm>.ap` | **Autoportancia:** vano máximo (m) entre **líneas de apoyo**. Si el largo de cubierta supera `ap`, el motor calcula más apoyos (`calcAutoportancia`). |
| `lmin`, `lmax` (en el objeto panel) | **Largo comercial / fabricación:** rango válido del **largo del paquete** (m), no el límite estructural entre apoyos. |
| `au` | Ancho útil (m) para armar paños y m². |

Referencia de implementación: `calcAutoportancia` en `src/utils/calculations.js` (comentario JSDoc en la función).

### Cantidad de paneles en ancho: no sumar un panel “solo” (obligatorio para agentes)

El motor puede usar `ceil(ancho / au)` en `calcPanelesTecho` para cubrir todo el ancho; **en cotización asistida con el usuario humano**, no **asumir** automáticamente el caso que agrega un panel más sin avisar.

1. Con el **`au`** de la familia elegida (ej. ISODEC PIR **1,12 m**), calcular y **mostrar**:
   - **Ancho cubrible con N paneles:** `N × au` (definir **N** según lo que se evalúe: típicamente `floor(ancho_pedido / au)` para “sin subir de panel”, y comparar con `ceil` como opción explícita).
   - **Alternativa:** ancho cubrible con **N+1** paneles: `(N+1) × au`.
2. Si el ancho a cubrir **no** es múltiplo exacto de `au`, **consultar** al usuario (o al cliente vía Matias): ¿**un panel más** (más superficie y costo) o **quedarse con N paneles** y menor ancho cubierto (u otro criterio de obra: solape, remate, etc.)?
3. En el **presupuesto** conviene **cantidad de paneles** por zona, **largo**, **superficie de chapa** y **USD/m²** por línea; no presentar solo un m² agregado sin despiece.

**No** decidir solo un panel extra por redondeo hacia arriba sin esa explicación y decisión explícita.

### IVA y marca en presupuestos de terceros (obligatorio)

- **IVA:** no **asumir** con/sin IVA en documentos ajenos si no está **explícito** o confirmado; **consultar** (ver `docs/team/knowledge/Calc.md` §4).
- **Marca / fabricante:** no **asumir**; si no figura en el documento, **desconocido** y **consultar** si aplica (§5).

### Trazabilidad en cada presupuesto (obligatorio)

Al entregar un presupuesto o tabla de números, incluir sección **Fuentes de datos**: para cada precio, `au`, cantidad, fórmula o parámetro, enlazar o citar **archivo + líneas** (código) o **hoja + celda/columna** (planilla según docs), o declarar **dato del cliente**. Ver `docs/team/knowledge/Calc.md` §7.

---

## Workflow

1. **Read** IA.md, DASHBOARD-VISUAL-MAP (Calculadora en 5173).
2. **Understand** flow: usuario ingresa zonas → cálculos → BOM → PDF/WhatsApp.
3. **Coordinate** con Mapa si hay cambios que afectan Master_Cotizaciones o CRM.
4. **Coordinate** con Vista si hay cambios de UI en la Calculadora.
5. **Run** `node tests/validation.js` después de cambios en calculations/helpers.

---

## Handoff

- **To Mapa:** Si nueva columna o tab en Sheets para cotizaciones.
- **To Vista:** Si cambio de UI en Calculadora (layout, estados).
- **To Integra:** Si flujo de envío a Shopify/ML desde cotización.

---

## Reference

- IA.md: Calculadora = Cotizaciones section
- tests/validation.js: Pricing engine, panel calculations, BOM
- docs/openapi-calc.yaml: Cloud Run calc API (si aplica)
