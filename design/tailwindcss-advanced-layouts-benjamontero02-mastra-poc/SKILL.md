---
name: tailwindcss-advanced-layouts
description: Implementa layouts complejos con Tailwind CSS usando Grid, Flexbox y Container Queries. Usa cuando necesites holy grail layouts, grids responsivos, carousels con snap, sticky headers, o layouts con container queries.
allowed-tools: Read, Grep, Glob
---

# Layouts Avanzados con Tailwind CSS

Skill para crear layouts complejos y responsivos con las técnicas modernas de CSS.

## Cuándo usar esta skill

- Crear layouts de página completos (holy grail, dashboard, landing)
- Implementar grids automáticos con auto-fill/auto-fit
- Configurar container queries para componentes responsivos
- Crear carousels y secciones con scroll snap
- Manejar headers/sidebars sticky o fixed
- Resolver problemas de overflow en flex items

## Workflow

1. **Identificar el patrón**: ¿Es un layout 2D (Grid) o 1D (Flexbox)?
2. **Consultar referencias**: Ver [layout-patterns.md](references/layout-patterns.md) para ejemplos
3. **Implementar mobile-first**: Empezar con diseño móvil y agregar breakpoints
4. **Validar responsividad**: Probar todos los breakpoints (sm, md, lg, xl, 2xl)
5. **Testear edge cases**: `min-w-0` para truncate, overflow hidden para grids

## Decisiones rápidas

| Necesito... | Usar... |
|:------------|:--------|
| Layout 2D con filas y columnas | `grid` con template columns/rows |
| Navegación horizontal | `flex` con gap |
| Cards que se ajustan automáticamente | `grid-cols-[repeat(auto-fit,minmax(250px,1fr))]` |
| Componente responsivo al contenedor | `@container` con container queries |
| Header que sigue al scroll | `sticky top-0` |
| Carousel horizontal | `flex snap-x snap-mandatory overflow-x-auto` |

## Patrones críticos

### Prevenir overflow en Flex

```html
<div class="flex min-w-0">
  <div class="shrink-0">Icon</div>
  <div class="min-w-0 truncate">Texto largo</div>
</div>
```

### Grid auto-responsivo

```html
<div class="grid grid-cols-[repeat(auto-fit,minmax(min(100%,300px),1fr))] gap-4">
  <!-- Cards -->
</div>
```

### Sticky con offset

```html
<header class="sticky top-0 z-50 bg-white/80 backdrop-blur-sm">
  Nav
</header>
<section id="about" class="scroll-mt-20">
  <!-- Offset para el sticky header -->
</section>
```

## Recursos

- Patrones completos con ejemplos: [layout-patterns.md](references/layout-patterns.md)
