---
name: image-gen
description: "Generar imágenes IA coherentes con la web: producto flotando, heros, fondos, 3D, mockups. PRIMERO la generación nativa del host (app de ChatGPT/Codex, Antigravity); scripts/generate.mjs por API solo si no hay. Paleta y estilo del design system."
---

# image-gen (Senzu)

Genera imágenes **acordes a la web** (nunca genéricas): la paleta, el mood y el estilo salen de
`senzu/design-system/<slug>/MASTER.md` (o BRAND.md) y entran en el prompt. Recetas por tipo de imagen en
`references/prompt-recipes.md`; qué herramienta según tu agente en `references/tools-by-agent.md`.

## 1. REGLA 0 — ¿tu entorno ya genera imágenes? Úsalo directo, sin script
Comprueba PRIMERO si el host tiene generación nativa; si la tiene, dale el prompt de la receta tal cual
y sáltate el script (más rápido, sin claves, sin procesado extra):

| Entorno | Cómo genera |
|---|---|
| **App de ChatGPT/Codex** (Windows/Mac: agente + chat + imágenes) | **NATIVO**: genera la imagen directamente con el prompt de la receta. NO busques la API ni el script |
| **Antigravity** | **NATIVO**: Nano Banana Pro (Gemini 3 Pro Image) integrado en el IDE; prompt de la receta directo |
| Codex CLI / Claude Code / Cursor / Windsurf (sin generación nativa) | `node <skills-dir>/image-gen/scripts/generate.mjs "<prompt>"` — `--provider openai` (default, `OPENAI_API_KEY`) \| `gemini` \| `fal` |

Nativo o script, el resto de la skill aplica IGUAL: receta + tokens del design system + post-proceso.
Sin generación nativa ni clave → dile al usuario cuál exportar (`OPENAI_API_KEY`/`GEMINI_API_KEY`/`FAL_KEY`)
y NO improvises imágenes de stock como si fueran generadas.

## 2. Flujo obligatorio
1. **Brief de imagen** (1 línea cada uno): para qué sección es, tipo (producto flotante, hero bg, mockup,
   3D, textura, ilustración), qué debe transmitir, y dónde va (tamaño/aspect del hueco REAL en el layout).
2. **Tokens → palabras**: convierte la paleta del design system a lenguaje de prompt
   ("deep green #046a53 and mint accents, dark charcoal background") + el mood del MASTER.md
   ("clean, industrial, trustworthy"). La imagen debe parecer del MISMO sitio que el resto.
3. **Receta**: abre SOLO la sección del tipo en `references/prompt-recipes.md` y rellena su plantilla.
4. **Genera** (2-3 variantes): `node scripts/generate.mjs "<prompt>" --size 1536x1024 --n 2 --out hero.png`.
5. **Post-proceso**: recorte/limpieza, **WebP/AVIF comprimida** (squoosh/sharp), dimensiones exactas del
   hueco, `alt` descriptivo. Fondos transparentes: `--background transparent` (openai) o remove.bg.
6. **Verifica coherencia**: ponla EN la página junto al resto (no la juzgues suelta) y pasa `ui-verify`.

## 3. Qué modelo para qué (si puedes elegir proveedor)
| Necesitas | Usa |
|---|---|
| Seguir instrucciones finas de estilo/paleta, editar una imagen existente | gpt-image (openai) — el default del script |
| Fotorrealismo puro (producto, "fotos reales") | FLUX (`--provider fal`) o Imagen/Nano Banana |
| Texto legible DENTRO de la imagen (banners con claim) | Ideogram (via fal) o Nano Banana Pro |
| Iconos, ilustración vectorial, sistema de marca | Recraft V3 (via API propia/fal) — estilo consistente |
| Mockups de UI para enseñar al cliente | Antigravity + Nano Banana Pro (los hace nativamente) |

## 4. Reglas duras
1. **Nada de imágenes IA fingiendo ser reales del cliente**: sus obras, su equipo o su local se fotografían,
   no se generan. Una imagen IA de "equipo trabajando" se usa como recurso genérico y se anota en el devlog.
2. Personas generadas: sin caras de personas reales/famosas; cuidado con manos y texto (revisa siempre).
3. Sin logos ni marcas de terceros dentro de la imagen; el logo del cliente se compone después, en HTML/SVG.
4. Coherencia de serie: misma receta + mismos descriptores de luz/paleta para todas las imágenes de la web;
   guarda los prompts usados en `senzu/design-system/<slug>/prompts.md` para reutilizarlos.
5. Toda imagen pasa por compresión y lleva dimensiones + `alt`; el hero además `fetchpriority="high"`.
6. Coste: gpt-image ~0,02-0,19 $/imagen según calidad — genera 2-3 variantes, no 20.

## 5. Recursos
- `scripts/generate.mjs` — generador multi-proveedor (openai por defecto; gemini, fal). `--help` para opciones.
- `references/prompt-recipes.md` — recetas por tipo con plantillas (producto flotante, hero, 3D, mockup…).
- `references/tools-by-agent.md` — detalle por agente, modelos, precios y post-proceso.
