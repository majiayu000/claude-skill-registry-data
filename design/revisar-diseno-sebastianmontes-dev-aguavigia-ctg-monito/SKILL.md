---
name: revisar-diseno
description: Revisa capturas o código de la interfaz de AguaVigía contra la identidad formal (ADR-070) y la lista de rasgos de diseño genérico o «hecho por IA», y devuelve hallazgos concretos con pantalla, elemento y corrección. Úsala antes de abrir un PR que toque frontend/, antes de pedir la aprobación visual de un prototipo, o cuando el usuario diga que algo «se ve genérico», «se ve hecho por IA» o «no se ve trabajado».
---

# Revisar el diseño

Una revisión de diseño que no mira las pantallas no es revisión. Necesitas capturas; si no las hay, genéralas
(1440 × 900, 1024 × 768, 768 × 1024 y 390 × 844, claro y oscuro, más una con movimiento reducido).

## Procedimiento

1. Lee `docs/diseno/identidad.md` §2–§6 y `DESIGN.md` §2 y §10.
2. Mira cada captura completa. Para cada una, recorre las cuatro listas de abajo.
3. Revisa el CSS cambiado: busca hexadecimales fuera de `tokens.css`, `font-family` fuera de los tokens,
   `transition`/`animation` sin su bloque `prefers-reduced-motion`, y `box-shadow` en elementos que no flotan.
4. Devuelve los hallazgos en una tabla: **gravedad** (bloquea / corrige / pule), **pantalla y tamaño**, **elemento**,
   **qué se ve**, **corrección**. Sin hallazgos, dilo y di qué revisaste.

## 1. ¿Se ve genérico?

- Marca y titulares sin Newsreader; Inter, Roboto, Space Grotesk u otra webfont en la interfaz; la serif fuera de
  la marca, el titular y el barrio (`ADR-071`); un gran titular editorial repetido en páginas que no lo necesitan.
- Turquesa, índigo o azul genérico como acción; degradados; gris puro; crema con terracota.
- Tarjetas con sombra y el mismo radio en todo; pastillas de colores en cada dato; barrita de color al costado.
- Todo centrado; secciones apiladas de igual peso; iconos decorativos o emojis.
- La vista de escritorio es la de celular estirada: una columna angosta en medio de una pantalla ancha.

## 2. ¿Se nota el oficio?

- Cifras y horas en `tabular-nums`, alineadas; rótulos en mayúsculas con tracking; titulares con `text-wrap: balance`.
- Jerarquía clara: una cosa grande por vista (el barrio, la cifra, el titular); el resto se subordina.
- Márgenes y separaciones de la escala de `identidad.md` §4; reglas de 1 px alineadas entre bloques vecinos.
- Estados de foco, vacío, carga y error diseñados; «Sin datos verificados» con trama, nunca verde.
- El tema oscuro está diseñado, no invertido: cardenillo y latón aclarados, contraste medido.

## 3. ¿El movimiento suma?

- Cada animación está en la tabla de `identidad.md` §5, con su duración y curva.
- Nada rebota, nada se repite salvo el punto «en vivo», nada retrasa la respuesta ni roba el foco.
- Con movimiento reducido, la pantalla se ve completa y final.

## 4. ¿Dice la verdad?

- Ningún dato que la API no devuelva (guía §5): sin rankings, periodos o conteos inventados.
- El color de estado va siempre con glifo y palabra; contraste AA en texto, 3:1 en bordes y glifos.
- Las fechas distinguen registro del estado, generación del listado y última consulta (guía §6.1).
