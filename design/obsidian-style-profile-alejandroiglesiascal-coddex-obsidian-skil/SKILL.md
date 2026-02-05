---
name: obsidian-style-profile
description: "Analiza el estilo de escritura del usuario y genera un perfil con metricas y ejemplos citados."
---
# Obsidian Style Profile

## Cuando usar
- Necesito modelar el estilo de escritura del usuario.
- Quiero actualizar un perfil de estilo con evidencia.

## Procedimiento
1. **Seleccionar muestra**
   - Tomo una muestra representativa (por ejemplo 100 notas recientes con contenido sustancial).
2. **Lectura real**
   - Leo cada nota completa y sigo enlaces de primer nivel relevantes.
   - Registro lecturas en `cache/lecturas.json`.
3. **Extraer patrones**
   - Longitud de frases y parrafos.
   - Vocabulario frecuente y expresiones recurrentes.
   - Tono (formalidad, tecnicidad, directividad).
   - Formato (listas, tablas, codigo, emojis).
4. **Seleccionar ejemplos**
   - Elijo fragmentos representativos y los cito con wikilinks.
5. **Generar perfil**
   - Creo `memoria/estilo-escritura.md` con metricas, ejemplos y fuentes.

## Estructura minima sugerida
- Patrones linguisticos
- Vocabulario caracteristico
- Tono y voz
- Formato y estructura
- Ejemplos representativos
- Fuentes internas

## Restricciones
- No expongo datos sensibles en ejemplos.
- Si la muestra es insuficiente, lo declaro.

## Entrega
- Perfil actualizado y trazable con fuentes internas.

