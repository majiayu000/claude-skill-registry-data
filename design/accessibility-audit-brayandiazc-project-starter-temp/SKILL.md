---
name: accessibility-audit
description: Revisa los cambios de UI en cuanto a accesibilidad — contraste de color, navegación por teclado, gestión del foco, uso de ARIA y texto alternativo. Úsalo cuando la persona pida una revisión de a11y/accesibilidad, verificar el cumplimiento de WCAG, el soporte de teclado, la compatibilidad con lectores de pantalla o el manejo del foco (p. ej. "¿es accesible este modal?", "audita la a11y del formulario").
---

Audita la UI indicada en cuanto a accesibilidad. Reparto con `design-system-audit`:
aquella cubre tokens, primitivas, estados de datos y jerarquía; **todo lo de
contraste, teclado, foco y ARIA vive aquí**, en una sola lista — si la otra skill te
remitió un componente custom, esta es la lista que le aplica.

1. Si `docs/conventions/` contiene guías de accesibilidad o de sistema de diseño, léelas para conocer el estándar objetivo del proyecto (p. ej. WCAG 2.1 AA) y cualquier regla específica.
2. Localiza el código fuente de la UI dentro del alcance y revísalo frente a estas comprobaciones:
   - Contraste — el texto y la UI significativa cumplen la relación de contraste para su tamaño/rol.
   - Teclado — todos los elementos interactivos son alcanzables y operables por teclado; sin trampas de teclado; orden de tabulación lógico.
   - Foco — indicadores de foco visibles; el foco se mueve/restaura correctamente en modales, menús y cambios de ruta.
   - Semántica y ARIA — se prefieren elementos nativos (`button`, `a`, `label`); roles/atributos ARIA usados correctamente y solo cuando se necesitan; los campos de formulario tienen labels asociadas.
   - Imágenes y medios — texto `alt` en imágenes significativas, `alt` vacío en las decorativas; subtítulos donde corresponda.
   - Movimiento y responsividad — respeta reduced-motion; usable con zoom/en tamaños pequeños.
3. Informa una lista de verificación: cada ítem como Pasa / Falla / Requiere-revisión-manual, con archivo:línea y una corrección concreta.

Ejemplo de hallazgo: `El botón solo de ícono en Nav.tsx:22 no tiene nombre accesible — añade aria-label.`

NO afirmes la conformidad total con WCAG solo a partir de una revisión estática — señala los ítems que requieren pruebas manuales o con tecnología de asistencia.
