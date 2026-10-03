---
name: performance-analysis
description: "Diagnosticá problemas de performance frontend con evidencia antes de proponer cambios. Usá esta skill solo cuando el usuario pida analizar lentitud de navegación, renders excesivos, fetches duplicados, useEffects redundantes, componentes pesados o cuellos de botella visibles."
---

# Performance Analysis

## Propósito

Medir, interpretar y priorizar problemas de performance antes de refactorizar.

## Proceso

1. Definí qué se quiere medir:
   - navegación entre rutas;
   - render inicial;
   - render repetido;
   - fetch o waterfall;
   - interacción concreta.
2. Revisá el código y buscá síntomas:
   - `useEffect` redundantes;
   - estados duplicados;
   - fetches repetidos;
   - transformaciones costosas en render;
   - props inestables;
   - árboles de componentes demasiado pesados.
3. Instrumentá solo si suma evidencia:
   - logs temporales estratégicos;
   - marcas de tiempo;
   - mediciones simples comparables.
4. Separá:
   - evidencia observada;
   - hipótesis;
   - impacto probable.
5. Proponé mejoras priorizadas.
6. Si agregaste instrumentación temporal, indicá que debe retirarse o retirala cuando corresponda.

## Salida esperada

```md
### Informe de performance

- Síntoma:
- Evidencia:
- Posible causa:
- Prioridad:
- Mejora propuesta:
- Riesgo de la mejora:
```

## Regla principal

No sugieras optimizaciones por reflejo. Primero justificá el problema.
