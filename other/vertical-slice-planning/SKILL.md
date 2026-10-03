---
name: vertical-slice-planning
description: "Divide trabajos ya comprendidos en slices funcionales, pequeños y verificables. Usa esta skill cuando una implementación, refactor o flujo involucre varias piezas, múltiples pasos o convenga ordenarlo en entregas incrementales para reducir riesgo y retrabajo."
---

# Vertical Slice Planning

## Propósito

Ordenar trabajos cuyo alcance ya está entendido y conviene implementar por entregas funcionales, revisables y verificables.

## Cuándo usarla

Usala cuando:

- la feature ya está definida;
- el refactor tiene alcance claro;
- el trabajo cruza varias piezas;
- hay varias etapas naturales de implementación;
- implementar todo de una aumentaría riesgo o retrabajo.

## Cuándo no usarla

No la uses cuando:

- el pedido todavía es ambiguo: primero aplicá `feature-discovery`;
- el cambio es pequeño o autocontenido;
- dividirlo no mejora claridad ni validación.

## Principios

- Cada slice debe entregar valor observable.
- Evitá separar por capas puras como “todo backend primero” o “toda UI después”, salvo que el contexto lo exija.
- Preferí slices que puedan revisarse y validarse por sí mismos.
- Marcá dependencias entre slices cuando existan.
- Si un slice queda bloqueado por backend, dejalo explícito y, si corresponde, coordiná con `frontend-data-integration`.

## Formato sugerido

```md
### Plan por slices

1. Slice 1 — [nombre]
   - Objetivo:
   - Cambios incluidos:
   - Validación:

2. Slice 2 — [nombre]
   - Objetivo:
   - Cambios incluidos:
   - Validación:
```

## Cierre

- Confirmá que los slices cubren el pedido.
- Confirmá que el orden reduce riesgo.
- Evitá planes más largos que la implementación misma.
