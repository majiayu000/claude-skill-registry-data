---
name: polish-component
description: "Refina componentes frontend recién creados o refactorizados para mejorar su calidad interna. Usa esta skill cuando un componente tenga props públicas, constantes, handlers, mappings, estilos configurables o lógica que convenga ordenar antes de cerrar la implementación. Es un paso de cierre,cargala después de terminar la implementación de UI, no antes. Detecta handlers inline sin nombrar, classNames sin extraer, ARIA labels faltantes y props mal tipadas."
---

# Polish Component

## Propósito

Refinar la calidad interna de un componente ya creado o refactorizado sin rediseñar toda la feature.

## Cuándo usarla

Usala cuando un componente:

- es reusable o exportado;
- tiene props públicas relevantes;
- contiene constantes, mappings o helpers;
- concentra handlers o lógica derivada;
- expone estilos configurables;
- creció lo suficiente como para que valga la pena revisar su estructura interna.

## Cuándo no usarla

No la uses para:

- wrappers triviales;
- componentes puramente presentacionales de pocas líneas;
- ajustes visuales mínimos sin impacto estructural.

## Checklist de refinamiento

### 1. API de props

- Nombres claros.
- Responsabilidades entendibles.
- Evitá componentes ambiguos entre controlados y no controlados salvo que sea intencional.
- Evitá props genéricas que oculten decisiones importantes.

### 2. Constantes y mappings

- Si una constante o mapping es pequeño y local, puede quedar colocalizado.
- Si representa lógica reusable, crece demasiado o podría compartirse, evaluá extraerlo a:
  - `*.constants.ts`;
  - helper;
  - util del dominio.
- No extraigas archivos por reflejo.

### 3. Handlers y lógica interna

- Revisá si los handlers están bien nombrados y son legibles.
- Extraé lógica a hooks o helpers solo cuando:
  - se reutiliza;
  - dificulta leer el componente;
  - mezcla reglas de negocio con render.
- No agregues `useCallback`, `useMemo` o memoización sin motivo real o patrón del repo.

### 4. Organización del archivo

- Orden lógico:
  - tipos;
  - constantes;
  - helpers locales;
  - componente;
  - exports.
- Si el archivo queda sobrecargado, proponé una separación mínima y justificada.

### 5. Estilos configurables

- Si el componente reusable necesita adaptarse visualmente a varios contextos, revisá:
  - `className` raíz;
  - `classNames` por slots;
  - variantes del design system.
- Conservá defaults funcionales.

### 6. Accesibilidad e interacción

- Si hay interacción, revisá etiquetas, botones, feedback y estados disabled.
- No conviertas esta skill en una auditoría de accesibilidad completa, pero corregí problemas evidentes.

## Salida esperada

- Qué se pulió.
- Qué se mantuvo colocalizado y por qué.
- Qué se extrajo y por qué.
- Riesgos o deuda menor restante, si aplica.
