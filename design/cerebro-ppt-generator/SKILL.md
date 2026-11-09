---
name: cerebro-ppt-generator
description: Habilidad para generar presentaciones interactivas en HTML del proyecto. HTML custom autocontenido con stage 1280x720, trama de marca y navegación nativa por teclado y botones.
license: Apache-2.0
metadata:
  author: equipo
  version: "4.0"
---

## Cuándo se usa
Úsalo cuando el usuario o analista funcional pida armar una presentación de flujos o reglas del negocio en HTML interactivo en `entregables/presentaciones/`.

## 🎯 Filosofía (UNA SOLA VÍA)
Las presentaciones son **HTML custom autocontenido**: un solo archivo `.html` con CSS y JS embebidos. Sin compiladores, sin dependencias externas (solo Google Fonts y el logo local). El `.html` ES el entregable final. **No hay nada que compilar.**

## 📋 Flujo de Trabajo (4 pasos obligatorios)
1. **Leer fuentes**: Consultar los conceptos en el OKF (`cerebro-digital/`) y los tokens/componentes en `cerebro-digital/diseno/diseno-sistema.md`.
2. **Copiar el template**: Partir de `template-ppt.html` de esta misma carpeta, que es la estructura canónica. No partir de cero ni inventar estilos nuevos.
3. **Completar y guardar en borrador**: Completar las slides con el contenido del negocio y guardar el `.html` en `borrador/presentaciones/` — **nunca directo en `entregables/presentaciones/`**. Verificar que el stage es 1280x720 (16:9) y que la navegación funciona (flechas + botones).
4. **Promover solo si lo piden**: Copiar el `.html` de `borrador/presentaciones/` a `entregables/presentaciones/` únicamente cuando el usuario lo pida explícitamente (ej: "metelo en funcional"). Nunca por iniciativa propia.

## 🎨 Estructura del HTML (canónica — ver template-ppt.html)
- **Variables CSS** en `:root`: `--azul-marca` (⚠ placeholder: toma el valor de `--brand-900` de `diseno/diseno-sistema.md`), `--azul-hover`, `--verde-exito` y `--rojo-error` (toman los tokens semánticos de `diseno-sistema.md`, nunca un hexadecimal a mano), `--grafito` (token de `diseno-sistema.md`), `--gris`, `--gris-claro`, `--blanco`, `--grad-oscuro`, `--f`.
- **`#stage`**: 1280x720px, centrado, `border-radius: 12px`, sombra profunda.
- **Slides `.s`** con tres variantes:
  - `.s--portada` — oscura con gradiente, h1 + h2 + footer `.docentes` (autor y {{PRODUCTO}}·{{ORGANIZACION}}).
  - `.s--claro` — fondo `var(--neutral-50)`, logo en `.head`.
  - `.s--oscuro` — cierre o sección oscura, sin logo.
- **Animación**: `.on` con `@keyframes in` (0.45s `cubic-bezier(.2,.7,.3,1)`).
- **Trama**: SVG de anillos concéntricos embebido en base64 con `stroke="currentColor"` (tamaño y color por variante: 600px azul al 4% en claras, 750px `var(--brand-300)` al 6% en oscuras).
- **Navegación**: botones `.nav-bar` (‹ ›) + teclado (ArrowRight/ArrowLeft/espacio) vía función `showSlide`.

## 📋 Reglas de Generación
1. **Logo de la organización** (`../disenos/logo.png`): SOLO en slides claras (`.s--claro`), dentro de `.head` con un `span` contextual. PROHIBIDO en portada (`.s--portada`) y cierre (`.s--oscuro`).
2. **Portada**: `.s--portada` con `.eyebrow`, `h1` (máx 18ch), `h2` de subtítulo y footer `.docentes` con autor/es y marca {{PRODUCTO}}·{{ORGANIZACION}}.
3. **Layout simétrico**: `.cards` (tarjetas `.card` / `.card.p` primarias) y `.ruta` (pasos `.paso` / `.paso.activo` con conectores) maquetados en fila con `flex-direction: row`.
4. **Contenido secundario**: usar `.body`/`.col` con listas `ul`/`li` (bullets azules), `.eyebrow` como kicker y `.lead` como párrafo introductorio.
5. **Trazabilidad**: referenciar la fuente del OKF al final de cada slide con `[[archivo]]`.
6. **Estilos nuevos**: agregar CSS solo si el diseño lo exige (ej: tablas, toasters); documentarlos para reutilización.
7. **Autocontenido**: el `.html` debe funcionar abriéndolo directo en el navegador. Verificar encoding UTF-8 sin BOM.

## 📂 Referencias
- `template-ppt.html` — Plantilla canónica. Siempre partir de este archivo.
- `cerebro-digital/diseno/diseno-sistema.md` — Tokens y componentes (toasters, pills, modales, data grids, sintaxis de filtro).
