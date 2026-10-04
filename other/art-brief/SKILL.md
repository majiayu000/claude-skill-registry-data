---
name: art-brief
description: Use when writing an art request, illustrator brief or image-generation prompt for this game (portraits, emotional states, backgrounds, intro art, headers, icons), updating ART-NEEDED.md, or integrating generated images into Assets/Art.
---

# Encargos de arte

Todo encargo va en `ART-NEEDED.md`. Un test obliga a que cada hueco de arte del código esté documentado allí. Al soltar
el archivo en la ruta indicada, el catálogo se regenera solo. Modelo completo: `docs/art/javier/BRIEF.md`.

## Cada entrada lleva

| Campo | Valor |
|---|---|
| Ruta y nombre | Retratos: `Assets/Art/Portraits/<artId>_<estado>.png` (`artId` es el interno: Amparo = `rosario`) |
| Tamaño y formato | Retratos **768×1024 (3:4), PNG con fondo transparente**, cuerpo entero. Fondos 1080×1920. Cabeceras 1080×480. Iconos 128×128 transparentes, legibles a 48 px, trazo #E8E2D6 o #D9A441. |
| Estados | `tranquilo` como base más los **2 más frecuentes** según los datos del bot (~1500 respuestas). Javier, Maruxa y Álex necesitan "triste", no "enfadado". 3 por personaje: 36 imágenes, no 60. Primero los 12 `*_tranquilo`. |
| Consistencia | El mismo encuadre en todos los estados: la cara no salta al cambiar de estado. |
| Restricciones de composición | Arte de intro: la franja central (25-85 % de la altura) oscura y con poco detalle, porque el texto va encima. |
| Para qué personaje es urgente | Primero los que hoy comparten cara: Javier y Daniel, y las tres vecinas. |

## Reglas con caso real

| Regla | Caso real |
|---|---|
| **Referencias de estilo coherentes y medidas.** Antes de elegirlas, mide el píxel efectivo y la proporción cabeza/cuerpo. No mezcles estilos: hoy valen Marcos (`duenio_bar`, la principal) y Álex (`hermano`); Lucía (`madre`), solo para la paleta. | Daniel (`padre.gif.png`) tiene un píxel de 9 px y cabeza 1/3,6, frente a 5 px y 1/5,3 de Marcos y Álex. Mezclarlos pedía dos estilos a la vez. Daniel se rehará. |
| **El estilo se describe con lo medido, no a ojo:** contorno #000000 de un 1-2,4 % del alto, figura al 89-92 %, cabeza ≈1/5, sombra suave a la derecha de los pies (≈18 % de opacidad). Los originales no son pixel art estricto (decenas de miles de colores). | Primer encargo pedía "transparent background, no ground shadow", y los originales 02-04 sí llevan sombra. |
| **Se pide fondo blanco liso**, no transparente, y luego `python Tools/remove_white_bg.py entrada.png Assets/Art/Portraits/<artId>_<estado>.png`. | Los generadores ignoran la transparencia o pintan el patrón de cuadros. |
| **Se genera una vez (`tranquilo`) y se editan cara y hombros** para el resto, con un prompt de edición de "solo la expresión". Si `Tools/measure_portrait.py` da más de un 1 % de diferencia de encuadre, se rehace la edición; no se regenera. | Regenerar, aunque sea con la misma semilla, cambia la camisa, las manos o la postura. |
| **Importación: bilineal con mipmaps.** | A píxeles reales de móvil, Point sin mipmaps rompía las líneas finas en la rueda (figuras a ≈1/3). Ver `AnimationCapture.FiltroDeImportacion`. |
| **Ninguna expresión delata la culpa** si el personaje es culpable en una variante e inocente en otras: las imágenes son las mismas. | Javier: culpable en 3A, inocente en 3B y 3C. |
| Los personajes se inspiran en casos reales, pero ningún encargo usa nombres ni rasgos de personas reales ("real person likeness" en el negativo). | |

## Después de recibir el arte

1. Primero `remove_white_bg.py` y luego `measure_portrait.py`.
2. Pega los Rect medidos en `PortraitCrops.NewArtByArtId` (rama `feature/encuadre-arte-nuevo`).
3. Haz una galería a tamaño de juego (ver la skill `before-after-gallery`). Comprueba la altura en la rueda (ver la
   skill `pixel-portrait-kitbash`).
4. Anota lo que se deja sin hacer a propósito, y por qué.
