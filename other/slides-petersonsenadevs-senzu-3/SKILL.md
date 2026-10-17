---
name: slides
description: "Crea presentaciones HTML estratégicas (pitch deck, ventas, demo) con Chart.js, design tokens, layouts responsive y fórmulas de copywriting. Disparadores: slides, deck, presentación, pitch. No para PPTX/Google Slides ni gráficos sueltos."
---

# slides (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (40 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep). Todo el contenido real está en `references/`.

## Cuándo usar / cuándo NO
- Usar: pitch deck (YC seed, ventas, demo de producto) en HTML autocontenido con narrativa y estructura de slides.
- Usar: slides con datos (Chart.js) y layouts predefinidos (título, dos columnas, grid de features, dashboard de métricas).
- Usar: redactar titulares y copy de slides con fórmulas (AIDA, PAS, etc.).
- NO usar: gráficos o dashboards fuera de una presentación → skill `dataviz`; paquete completo de marca con logo/CIP → `design`.
- NO usar: exportar a PPTX/Keynote (el upstream sólo produce HTML).

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar una presentación | `SKILL.upstream.md` L21-25 (§Subcommands) + `references/create.md` + `references/slide-strategies.md` L5-24 |
| Elegir estructura del deck | `references/slide-strategies.md` L25-74 (§Common Structures, §Duarte Sparkline) |
| Maquetar una slide | `references/layout-patterns.md` L5-23 (selección) y L24-98 (CSS) |
| Plantilla base y Chart.js | `references/html-template.md` L5-203 (base) y L204-238 (§Chart.js Integration) |
| Escribir el copy | `references/copywriting-formulas.md` |
| Depurar / rendimiento | `references/html-template.md` L239-295 (animaciones, fondos, variables CSS) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 14-19 | When to Use | Casos de uso |
| 21-25 | Subcommands | `create` → `references/create.md` |
| 27-34 | References (Knowledge Base) | Tabla tema → archivo |
| 36-40 | Routing | Resolución del subcomando desde `$ARGUMENTS` |

## Recursos
- `references/create.md` — prompt del subcomando `create` (4 líneas).
- `references/slide-strategies.md` — selección de estrategia, estructuras YC/ventas/demo, patrón Sparkline de Duarte, cómo casar estrategia y contexto.
- `references/layout-patterns.md` — layouts por caso de uso, estructuras CSS, variantes de card/métrica, tratamientos visuales y árbol de decisión.
- `references/html-template.md` — estructura HTML base, integración Chart.js, clases de animación, fondos, variables CSS.
- `references/copywriting-formulas.md` — fórmulas de titulares y cuerpo para slides.
- No hay `scripts/` ni `assets/`.

## Reglas duras
- Un mensaje por slide; elegir la estrategia (YC 10 slides, ventas 9, demo 6) antes de maquetar.
- Usar los design tokens del proyecto (variables CSS de `html-template.md`), no colores hardcodeados.
- Chart.js sólo cuando el dato aporta; cada gráfico con título y etiquetas legibles, sin más de una serie destacada.
- Layouts responsive con las estructuras de `layout-patterns.md`; animaciones sólo con las clases previstas y respetando `prefers-reduced-motion`.
- Copy con fórmula explícita (`copywriting-formulas.md`): titular corto + una idea de apoyo.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). La salida es un HTML estático independiente del framework; si el proyecto tiene `assets/design-tokens.css` (skill `brand`/`design-system`), enlázalo en lugar de redefinir variables.
