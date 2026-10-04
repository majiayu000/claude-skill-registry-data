---
name: design-system-audit
description: Audita una vista o componente frente al design system en lo que un script no puede comprobar — estados de interacción, los cuatro estados de datos, primitivas nativas frente a componentes reinventados y jerarquía visual. Úsalo cuando la persona pida revisar el cumplimiento del design system o si un componente sigue las guías (p. ej. "¿esta tarjeta sigue nuestro sistema?", "audita la vista de ajustes").
---

Audita la UI indicada frente al design system de `design/`.

**Los colores no los revisas tú.** El job `Design system` del CI
(`.github/scripts/check-design-tokens.sh`) ya falla ante cualquier hex, `rgb()`,
utilidad de paleta (`bg-blue-500`) o valor arbitrario (`bg-[#0A7A9D]`) en las vistas.
Si crees ver un color crudo, es que el check no cubre esa ruta: dilo, y propón añadir
la carpeta al script en vez de convertirte en un linter humano.

Tu trabajo es lo que ningún script puede comprobar:

1. Lee `design/README.md` (el sistema) y `docs/conventions/ui.md` (cómo se organizan
   las vistas y dónde están los assets de marca).

2. **Primitiva nativa antes que componente reinventado.** Un diálogo hecho con `<div>`
   y `position: fixed` es un hallazgo aunque se vea bien: `<dialog>`, `<details>` y
   `popover` traen foco, teclado y Escape resueltos por el navegador. Si hay un
   componente custom donde había una primitiva, señálalo con el reemplazo concreto.

3. **Si el componente custom es inevitable**, señálalo y remite su accesibilidad
   (focus trap, Escape, `aria-*`, tabulación) a `/accessibility-audit` — esa lista
   vive allí, en un solo sitio, a propósito.

4. **Estados de interacción**: default, hover, active y disabled. (El foco visible y
   la navegación por teclado los audita `/accessibility-audit`.)

5. **Los cuatro estados de datos**, en toda vista que cargue algo: **loading**
   (skeleton con la forma del contenido, no un spinner genérico ni "Cargando…"),
   **empty** (icono + por qué está vacío + CTA que oriente), **error** (mensaje + acción
   de reintento) y **éxito**. El estado vacío es el que más define el producto y el que
   más se salta.

6. **Ambos temas**: claro y `data-theme="dark"` — que la vista use los tokens en los
   dos y ninguna pieza quede pegada a un solo tema. (La medición de contraste AA es
   de `/accessibility-audit`; `design/preview.html` la trae para los tokens base.)

7. **Jerarquía antes que decoración**: ¿se entiende qué es lo importante de la vista
   sin leer el texto? Espaciado y peso tipográfico antes que bordes y sombras.

Informa una lista: cada ítem **Pasa / Falla**, con `archivo:línea` y la corrección
concreta. Ejemplo: `Modal.tsx:12 — <div role="dialog"> sin focus trap; usa <dialog>`.

NO rediseñes ni reestilices por iniciativa propia: informas y propones. Para una
revisión de accesibilidad completa (contraste medido, lectores de pantalla), usa
`accessibility-audit`. `design/` siempre manda.
