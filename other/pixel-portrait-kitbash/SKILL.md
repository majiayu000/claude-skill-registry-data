---
name: pixel-portrait-kitbash
description: Use when a character needs its own portrait and no final art exists - deriving a new pixel-art portrait from an existing one (recolour, mirror, glasses, grey hair, mourning), or when two characters share the same face in the game.
---

# Retratos derivados por código

El arte original nunca se toca: todo lo derivado va a archivos nuevos. Es un apaño honesto mientras llega el arte de verdad.

## Pasos

1. Añade el personaje a `Tools/make_derived_portraits.py`: base (`Assets/Images/Suspects/<base>.gif.png`), zonas y transformaciones. Salida: `Assets/Art/Derived/<clave>.png`. Prueba con `python Tools/make_derived_portraits.py --preview <carpeta del scratchpad>`.
2. Recolorea por **zona (rectángulo) y rango de tono/saturación/valor**, nunca solo por tono: la piel y las rayas del polo comparten color.
3. Regístralo en `Assets/Scripts/Art/DerivedPortraits.cs`: `"<Nombre>" → (ruta, claveBase, espejo)`. Hereda el encuadre de su base (`PortraitCrops` bust/face/figure, reflejado si va en espejo) y el mismo `ArtGrading.Kind.LegacyPortrait`.
4. En la ficha: `portraitKey = "<Nombre>"`. El `artId` se queda aunque cambie el nombre (Amparo sigue con `rosario`).
5. Tests: `PortraitAssignmentTests` (ningún personaje comparte retrato y cada derivado tiene archivo y encuadre).
6. Galería a tamaño de juego, historia por historia (ver la skill `before-after-gallery`). Mírala tú antes de enseñarla.
7. **Sé honesto en el informe** con lo que no se consigue y escribe el encargo en `ART-NEEDED.md` (ver la skill `art-brief`).

## Casos reales

- Había 7 retratos para 12 personajes. Compartían cara Daniel y Javier, Carmen y Lucía, Lucas y Álex, y las tres vecinas. Se derivaron 6.
- Límite reconocido: Javier sigue con la cara y el bigote de Daniel, y las vecinas con la misma cara y pose. Ropa, pelo y orientación los distinguen, pero no son personajes nuevos.
- La altura de la rueda se mide sobre la parte opaca de cada imagen (`PortraitCrops.Figure`, sin el humo del cigarro). Si cambia el arte, vuelve a medirla.
- El arte nuevo generado por código no pasa por el tratamiento del arte antiguo: con él, las intros salían casi negras.
