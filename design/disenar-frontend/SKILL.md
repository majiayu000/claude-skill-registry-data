---
name: disenar-frontend
description: Orienta cualquier trabajo sobre la interfaz de AguaVigía — pantallas, componentes, estilos, animaciones, prototipos o el muestrario — para que siga la identidad formal (ADR-070) y las reglas de datos de la guía, en vez de caer en un diseño genérico. Úsala SIEMPRE antes de crear o modificar algo en frontend/, antes de publicar un prototipo en un Artifact, o cuando el usuario pida «rediseñar», «mejorar el diseño», «hacer una pantalla» o «que se vea mejor».
---

# Diseñar en el frontend de AguaVigía

El modelo, sin contexto, produce la interfaz promedio: fuente del sistema, tarjetas redondeadas, un botón turquesa.
Eso ya pasó en este proyecto y el dueño lo rechazó. Esta skill fija el contexto antes de escribir una línea.

## 1. Lee, en este orden

1. `DESIGN.md` §1–§2, §5, §7–§10: principio, **los cuatro estados**, cómo se escribe, accesibilidad y checklist.
2. `docs/diseno/identidad.md` completo: paleta, tipografía, composición, **movimiento** y prohibiciones.
3. La fila de la pantalla en `docs/diseno/guia-frontend.md` §5 y §6: qué datos existen, estados y mensajes.
4. El contrato del recurso en `docs/api/` si la pantalla consume datos.

Si dos de estos se contradicen, **dilo al usuario**; no elijas en silencio. Mientras `identidad.md` diga «pendiente
de aprobación visual», `DESIGN.md` §3–§4 y `tokens.css` siguen vigentes en el código: no mezcles tokens de las dos
identidades en un mismo cambio y no migres a medias (la migración es un solo cambio: `identidad.md` §8).

## 2. Antes de escribir código, escribe el plan

Tres a seis líneas en la conversación, no en un archivo:
- **Qué responde la pantalla** en una frase, desde el lado del vecino.
- **Composición en escritorio (1440 px) y en celular (390 px)**: qué va a la izquierda, qué al centro, qué se
  desplaza. La vista web es una composición propia, no el celular estirado.
- **Tokens y tipografía** que usa (nombres de `identidad.md` §2–§3), sin valores nuevos.
- **Movimiento**: qué momento de `identidad.md` §5 aplica. Si no está en la tabla, no se anima.
- **Estados**: carga, vacío, error y `estado: null`, con los textos de la guía §6.2.

## 3. Reglas que no se negocian

- **Colores:** solo tokens. Nada de hexadecimales en componentes. Un solo color de acción (`--cardenillo`). Los
  colores de estado solo para estados del servicio, siempre con glifo y palabra.
- **Tipografía (`ADR-071`):** Newsreader solo en la marca, el titular de la página y el nombre del barrio; la pila
  del sistema en controles, texto y cifras. Cifras siempre `tabular-nums`. Nada espera a que cargue la serif.
- **Forma:** reglas de 1 px en vez de tarjetas; sombra solo en lo que flota; radios según `identidad.md` §4.
- **Movimiento:** solo lo de `identidad.md` §5, con sus duraciones y curvas; solo `transform`, `opacity`,
  `stroke-dashoffset` y colores; `prefers-reduced-motion` lo desactiva todo. Si una animación deja contenido
  invisible cuando el script falla, está mal.
- **Datos:** nada que la API no devuelva (guía §5). «Datos de ejemplo» se rotulan como tales en prototipos.
- **Prohibido:** la lista de `identidad.md` §6. Si lo que vas a hacer aparece ahí, detente y replantea.

## 4. Verifica antes de decir que terminaste

1. `npm run lint`, `npm run typecheck`, `npm test` y, si cambió la interfaz, `npm run test:e2e` en `frontend/`.
2. Capturas en 1440 × 900, 1024 × 768, 768 × 1024 y 390 × 844, en claro y oscuro, más una con movimiento reducido
   (Playwright o el MCP de Playwright). **Mira las capturas**; no las des por buenas sin verlas.
3. Pasa la skill `revisar-diseno` sobre esas capturas y corrige lo que encuentre.
4. Si cambió un token o una regla, cambia a la vez `DESIGN.md`/`identidad.md`, `tokens.css` y sus pruebas.

## 5. Registra

- Decisión visual nueva o cambio de una existente → `registrar-decision` (ADR) y actualización de `identidad.md`.
- Avance de fase → `docs/ingenieria/plan-frontend.md` y `docs/gestion/sprint-7.md` §2.
- Defecto visual encontrado → `registrar-bug`, aunque se corrija en el acto.
