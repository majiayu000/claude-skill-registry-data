---
name: design-review
description: Revisa una propuesta de UI/UX de Temp League contra el design brain, los tokens y las reglas de producto. Úsalo cuando alguien pida "revisa este diseño", "design review", validar una pantalla/componente, o antes de dar por terminada una propuesta visual.
---

# Design Review — Temp League

Revisa diseño (pantalla, componente o flujo) contra la fuente de verdad del proyecto.

## Pasos
1. Lee `design/00-design-brain.md`, `design/design-system/tokens.md`, `components.md` y los
   docs de producto relevantes en `/docs`.
2. Si existe `design/figma/` con proyecto, contrástalo también (Figma = verdad visual).
3. Evalúa la propuesta contra el checklist.
4. Entrega hallazgos priorizados (bloqueantes → menores) con la corrección concreta.

## Checklist
- **Consistencia de tokens:** ¿usa tokens de color/tipografía/espaciado o valores sueltos?
- **Alcance de producto:** ¿respeta features y reglas de `/docs` (gating, roles, bloqueos)?
- **Estados:** ¿cubre vacío, cargando, error, bloqueado, éxito?
- **Jerarquía:** ¿lo importante se ve primero? (app: próximo partido/mi equipo; admin:
  acción principal en 2-3 clics).
- **Plataforma:** app mobile-first / admin data-dense; áreas táctiles ≥44px.
- **Accesibilidad:** contraste suficiente en tema oscuro, texto legible.
- **Identidad:** se siente Temp League (esports/Gears), no plantilla genérica.

## Salida
Lista priorizada: `[bloqueante|mayor|menor] problema → corrección`. Sé específico y
accionable; no reescribas todo, señala lo que falla y cómo arreglarlo.
