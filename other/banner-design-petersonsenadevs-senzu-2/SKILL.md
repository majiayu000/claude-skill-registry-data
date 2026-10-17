---
name: banner-design
description: "Diseña banners (cover, header, display ad, hero web, print) en HTML/CSS + visual IA y exporta PNG a medida exacta. Disparadores: banner, cabecera, portada social, Google Ads, hero. No para vídeo, webs completas ni imprenta."
---

# banner-design (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (196 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: portadas y cabeceras de redes (Facebook, X, LinkedIn, YouTube, Instagram) con medidas oficiales.
- Usar: display ads (300x250, 728x90), hero de web o banner de evento/print con varias direcciones de arte.
- Usar: generar 2-3 opciones de estilo (minimalista, gradiente, tipografía bold, neón, glassmorphism...) y exportarlas a PNG.
- NO usar: imágenes de post/story genéricas para redes → `design` (Social Photos); identidad de marca completa → `brand`.
- NO usar: edición de vídeo o diseño de sitios completos (fuera de alcance explícito del upstream).

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un banner desde cero | `SKILL.upstream.md` L28-50 (§Workflow, Step 1-2) + `references/banner-sizes-and-styles.md` |
| Diseñar y generar visuales con IA | `SKILL.upstream.md` L51-100 (§Step 3: Design & Generate Options) |
| Exportar a PNG y nombrar archivos | `SKILL.upstream.md` L102-136 (§Step 4: Export Banners to Images) |
| Elegir medida o estilo rápido | `SKILL.upstream.md` L148-179 (§Banner Size Quick Reference, §Art Direction Styles) |
| Revisar / depurar un banner | `SKILL.upstream.md` L181-188 (§Design Rules) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 15-22 | When to Activate | Lista de disparadores del skill |
| 24-26 | Prerequisites | En Windows usar `python` en vez de `python3` |
| 28-146 | Workflow | Flujo completo en 5 pasos |
| 30-38 | Step 1: Gather Requirements (AskUserQuestion) | Propósito, plataforma, contenido, marca, estilo, cantidad |
| 40-49 | Step 2: Research & Art Direction | Referencias en Pinterest y elección de 2-3 estilos |
| 51-100 | Step 3: Design & Generate Options | HTML/CSS + generación de imagen (Flash vs Pro, aspect ratios, prompts) |
| 102-136 | Step 4: Export Banners to Images | Screenshot con chrome-devtools, compresión, convención de rutas |
| 138-146 | Step 5: Present Options & Iterate | Cómo presentar las opciones e iterar |
| 148-162 | Banner Size Quick Reference | Tabla de medidas por plataforma |
| 164-179 | Art Direction Styles (Top 10) | Estilos y para qué sector sirven |
| 181-188 | Design Rules | Zonas seguras, CTA, tipografía, ratio de texto, print |
| 190-196 | Security | Límites de alcance del skill |

## Recursos
- `references/banner-sizes-and-styles.md` — tabla completa de medidas por plataforma y los 22 estilos de dirección de arte (118 líneas).
- `scripts/` — no hay; el upstream invoca scripts de otras skills (`ai-artist`, `ai-multimodal`, `chrome-devtools`, `brand/inject-brand-context.cjs`) que pueden no existir en este repo: comprueba antes de citarlos.
- `assets/` — no hay; la salida va a `assets/banners/{campaña}/{estilo}-{ancho}x{alto}.png`.

## Reglas duras
- Contenido crítico dentro del 70-80 % central del lienzo (zonas seguras); una sola CTA, abajo-derecha, mínimo 44 px de alto.
- Máximo 2 tipografías; cuerpo ≥ 16 px, titular ≥ 32 px; contraste 4.5:1.
- Texto por debajo del 20 % del área en anuncios (Meta penaliza).
- Print: 300 DPI, CMYK, sangrado 3-5 mm.
- El visual generado por IA no lleva texto ("no text, no letters"); el texto se superpone en HTML/CSS.
- Exportar a las dimensiones exactas de la plataforma; comprimir si supera 5 MB.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). El banner es HTML/CSS estático independiente del framework; si el proyecto tiene tokens de marca (`assets/design-tokens.css`) úsalos en lugar de colores ad hoc, y para la paleta/voz remite a `brand`.
