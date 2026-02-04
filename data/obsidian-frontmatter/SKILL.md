---
name: obsidian-frontmatter
description: "Aplicar reglas consistentes de YAML frontmatter en Obsidian: un bloque, claves estÃ¡ndar, fechas YYYY-MM-DD, tags en lista, comillas cuando proceda."
---

# Obsidian Frontmatter (YAML)

## CuÃ¡ndo usar
- AÃ±adir o corregir frontmatter
- Normalizar propiedades para Dataview
- Evitar errores YAML (comillas, duplicados, tipos)

## Reglas mÃ­nimas
1. **Un Ãºnico bloque** YAML al inicio (`---` ... `---`) con una lÃ­nea en blanco despuÃ©s.
2. Claves **en minÃºscula** y consistentes.
3. Fechas: `YYYY-MM-DD` (o datetime ISO si la nota ya usa hora).
4. `tags` siempre como lista:
   ```yaml
   tags:
     - area
     - tipo
   ```
5. Valores con `:`, `#`, enlaces `[[...]]` o nÃºmeros â€œsospechososâ€: **entre comillas**.

## Procedimiento
1. Lee el archivo completo para no duplicar propiedades existentes.
2. Identifica el set de propiedades usado en el vault (no inventes si hay estÃ¡ndar previo).
3. Aplica cambios mÃ­nimos:
   - evita renombrar claves si rompe Dataview sin confirmaciÃ³n
4. Valida YAML:
   - sin tabs
   - indentaciÃ³n consistente (2 espacios)
   - sin duplicados de clave

## Salida
- Reporta quÃ© claves se aÃ±adieron/cambiaron.
- Si detectas incertidumbre sobre el estÃ¡ndar del vault, detente y pregunta.


