---
name: feature-discovery
description: "Aclara alcance, decisiones abiertas y supuestos antes de implementar features, flujos o refactors con ambigüedad relevante. Usa esta skill cuando falten definiciones que puedan cambiar UX, backend, contrato de datos, arquitectura o criterios de aceptación. Hace preguntas breves y de alto valor solo cuando sean necesarias."
---

## Propósito

Evitar que se implementen soluciones basadas en supuestos incorrectos cuando el prompt del usuario es ambiguo o carece de definiciones que pueden mejorar o cambiar la solución.

Es un sdd que se usa para aclarar alcance, decisiones abiertas y supuestos en features nuevas, flujos nuevos o refactors con incertidumbre funcional o técnica relevante.

## Cuándo usarla

Usala cuando una feature, componente, flujo existentes o nuevos, o refactor tenga incertidumbre relevante sobre:

- alcance funcional;
- comportamiento esperado;
- UX o interacción;
- persistencia o backend;
- permisos o roles;
- contrato de datos;
- criterios de aceptación;
- límites de lo que sí y no se debe tocar.

## Cuándo no usarla

No la uses cuando:

- el pedido ya está suficientemente definido;
- el cambio es directo y acotado;
- la duda es puramente técnica y puede resolverse leyendo contexto mínimo del repo sin cambiar alcance, UX, backend ni contrato;

## Presupuesto de preguntas

- Usá **1 a 3 preguntas** como estándar.
- Usá **hasta 6 preguntas como máximo** cuando falten decisiones importantes.
- Hacé **una sola ronda** de preguntas. No encadenes cuestionarios.

## Regla de calidad de preguntas

Preguntá solo lo que cambie alguno de estos puntos:

- alcance;
- UX;
- arquitectura;
- integración de datos;
- backend;
- contrato;
- validación;
- criterio de aceptación.

## Proceso

1. Leé el pedido.
2. Revisá solo el contexto mínimo del repo si ayuda a evitar preguntas innecesarias.
3. Detectá si hay ambigüedad en el prompt enviado por el usuario.
4. Si hay dudas o el prompt del usuario es ambiguo, usa el presupuesto de preguntas que corresponda.
5. Si el alcance queda claro y el trabajo es amplio usa `vertical-slice-planning` para la implementación.
