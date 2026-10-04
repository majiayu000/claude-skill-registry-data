---
name: session-report
description: Use when writing a NIGHT-LOG.md diary entry, a docs/REPORT-*.md session report, or a closing summary of work for Cristian.
---

# NIGHT-LOG e informes

## Entrada de NIGHT-LOG (después de cada tarea, no al final)

```
- **HH:MM** <Qué> (<archivo o clase>). <Por qué y qué se midió, con la cifra y su fuente>. <Qué falló por el camino
  y cómo se arregló>. EditMode N/N, PlayMode N/N.
```

- Hora real en negrita. Va bajo `## Bloque N: …` de la sesión en curso (`# Sesión X (fecha)`).
- La causa concreta, no "arreglado un fallo". Ejemplo: "el destello usaba el sprite de viñeta en vez del radial; vuelto a capturar".
- Cómo se verificó: test (nombre), captura revisada a tamaño real, o medición.
- Las cifras de los tests son las de la última ejecución que viste, nunca de memoria.

## Informe `docs/REPORT-<SESIÓN>.md`

1. Una tabla por bloque: HECHO CUANDO, resultado y commits.
2. Una sección por bloque con las cifras y su fuente (`Logs/…`, semilla, N). Si hay antes y después, con la misma semilla.
3. **Lo que salió mal y corregí**: errores propios con su commit y su arreglo (`ff30092`, CR CR LF, el heredoc, el XML viejo).
4. Los A/B fallidos o no concluyentes se cuentan como datos, igual que los éxitos (`StrictTimeNudge`, el "Dice" de la libreta).
5. "Decisiones para Cristian": numeradas, conservadoras, cada una con cómo se deshace (ajuste del tema o método).
6. Pendiente y riesgos. La galería enlazada con la imagen (ver la skill `before-after-gallery`).

## Reglas con caso real

- Si una cifra posterior contradice a una publicada, corrígela **en todos los sitios** donde se citó: el 2 % de premisas pasó a 2-5 % en el informe, el README, GAME-DESIGN y COHERENCE.
- Mira la mediana y las pistas que bajaron, una por una, no solo la media.
- Nada de "debería funcionar". Si algo no se verificó, dilo.
