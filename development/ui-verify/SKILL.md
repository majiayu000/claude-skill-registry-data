---
name: ui-verify
description: "Verificación OBLIGATORIA de UI antes de dar una vista por hecha: script Playwright (scripts/verify-ui.mjs) o navegador Chrome MCP en 375/768/1440, MÓVIL PRIMERO, dark mode, consola y accesibilidad. También al pedir verificar el responsive."
---

# ui-verify (Senzu)

Cierra el ciclo de `ui-ux-pro-max`: su checklist exige comprobar 375/768/1440, dark mode y accesibilidad — esta skill
lo hace de verdad en vez de darlo por supuesto. Se usa al terminar una vista, en `/revisar-ui` y en el "Verificar" de
las tarjetas de UI del plan. **El móvil (375 px) se comprueba PRIMERO: es donde todo falla y donde menos se mira.**

## Vía 1 (preferida): script automático `scripts/verify-ui.mjs`
Con la app corriendo en local (comando `dev` de `config.json`/`stack.json`):
```bash
node <skills-dir>/ui-verify/scripts/verify-ui.mjs http://localhost:PUERTO/ruta
# requiere una vez por proyecto:  npm i -D playwright && npx playwright install chromium
```
Comprueba por viewport: **scroll horizontal (con los elementos culpables)**, errores de consola, meta viewport,
nº de h1, imágenes sin `alt`/dimensiones, tap targets < 44px (móvil), texto < 12px, campos sin label, y
**GEOMETRÍA en píxeles** (`scripts/geometria.mjs`): centrado real de lo que el contenedor centra, loaders y su
grupo centrados en su capa, loader y barra en el mismo eje, spinners que se desplazan al girar, dibujos de SVG
descentrados en su caja y hermanos «casi» alineados (1-8 px: un margin o un top sobrante), con la causa
probable. En **MÓVIL** (`scripts/movil.mjs`): contenido que solo sale con hover, campos < 16 px (zoom en
iPhone), fijos que tapan, fondos fijos, cursor propio, h1 que se come la pantalla, navegación que no cabe
o desaparece, y **el menú usado de verdad**: lo pulsa, mide el panel abierto (enlaces ≥ 44 px, dentro de
pantalla, no tapados), lo captura y prueba Escape; imprime los tamaños reales (h1, párrafo, cabecera, CTA).
Capturas en `senzu/ui-verify/`: `<ancho>.png`, `<ancho>-anotada.png` (cada aviso `[g1]`/`[m2]` recuadrado
sobre su elemento) y `375-menu.png`. Sale con código 1 si hay problemas: **corrígelos y vuelve a
ejecutarlo hasta 0**. Un desplazamiento INTENCIONADO (ajuste óptico): `data-geometria="ignorar"` en el
elemento y el porqué en el devlog. `--tolerancia <px>` (por defecto 1).
Después ABRE las capturas (Read), la ANOTADA primero: cada aviso se confirma o se descarta MIRÁNDOLO, y lo
que a ojo parezca torcido se mide antes de tocarlo. Revisa lo que el script no ve: jerarquía, espaciados,
dark mode. Cómo pensar la versión móvil: `ui-ux-pro-max/references/es/movil.md`.

## Vía 2: navegador Chrome MCP (referencia paso a paso: `references/browser-checks.md`)
1. Abre la URL en pestaña nueva y redimensiona a **375 primero**, luego 768 y 1440; captura full-page en cada uno.
2. **Dark mode**: alterna el tema y captura 375 y 1440.
3. **Consola y red**: errores/warnings y peticiones fallidas (4xx/5xx, assets 404).
4. **Accesibilidad**: inyecta axe-core; violaciones por impacto. A mano: un H1, foco visible tabulando, `Esc` cierra modales.
5. **Interacción mínima**: hover/focus en CTAs; formularios muestran error junto al campo; menú móvil abre/cierra.

## Fallback sin navegador ni Node
Pide al usuario abrir la URL y reporta contra el checklist: DevTools responsive en los 3 anchos (móvil primero),
toggle de dark, consola limpia, Tab por la página. Deja explícito en el devlog que la verificación fue manual.

## Construir bien antes de verificar (lectura por tarea)
| Tarea | Lee solo |
|---|---|
| Construir UI accesible (ARIA, teclado, formularios, modales) | `references/a11y-build.md` — lo que axe no ve |
| Core Web Vitals: LCP/CLS/INP, Lighthouse, presupuesto JS | `references/web-performance.md` (backend → `code-quality/references/performance.md`) |

## Crítica visual (OBLIGATORIA para el veredicto APTA)
Tras la pasada técnica, ABRE las capturas (Read) y evalúalas con `references/visual-critique.md`:
9 ejes 1-5 (jerarquía, aire, alineación, contraste percibido, consistencia, densidad móvil, fotos,
test de portada, olor a IA). Nota 1-2 en cualquiera = corregir antes de entregar. Antes de publicar la web:
`/lanzar` → `references/launch-checklist.md` (SEO, PageSpeed, medición, legales, dominio).

## Informe (va al devlog y a la tarjeta del plan)
Tabla ancho×tema con OK/incidencias + errores de consola + veredicto `APTA` / `APTA con menores` / `NO APTA`
(con acciones concretas). En móvil, di explícitamente: sin scroll horizontal, CTAs pulsables, texto legible, menú usable.

## Reglas duras
- Una UI no está "hecha" sin esta pasada documentada. Decir "debería verse bien" NO es verificar.
- Si el script devuelve problemas, se corrigen y se re-ejecuta: no se entrega con el verificador en rojo.
- No corrijas sobre la marcha lo ajeno a tu tarea: repórtalo (o tarjeta `X-Tn` si hay plan) y espera decisión.
- Capturas SIEMPRE en `senzu/ui-verify/` del proyecto, nunca en el scratchpad ni en carpetas temporales. Las del navegador (MCP) no se guardan en disco: si el usuario quiere conservarlas, usa el script.
- No navegues fuera de la URL objetivo ni envíes formularios con datos reales.
