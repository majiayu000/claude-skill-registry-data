---
name: obsidian-rag-ops
description: "Ejecuta flujos RAG en Obsidian para responder, resumir, reorganizar o crear notas nuevas con citas trazables."
---
# Obsidian RAG Ops

## Cuando usar
- Tengo que responder o resumir contenido del vault.
- Debo reorganizar una nota sin perder trazabilidad.
- Quiero crear una nota nueva basada en fuentes existentes.

## Guardrails
- Aplico lectura real con `obsidian-reading-guardrails`.
- Escribo en primera persona y sin inventar datos.
- Siempre incluyo **Fuentes internas** con wikilinks.

## Flujo base
1. **Localizar fuentes**
   - Busco notas candidatas por titulo, tags y palabras clave.
2. **Leer fuentes**
   - Leo completo y sigo enlaces de primer nivel.
3. **Sintetizar**
   - Respondo o resumo con estructura clara y fiel al contenido.
4. **Citar**
   - Cito por seccion o bloque con `[[ruta#Seccion|Alias]]` o `[[ruta#^ancla|Alias]]`.

## Variantes
- **Responder**: respuesta directa, sin introducir informacion no leida.
- **Resumir**: sintetizo ideas clave, con encabezados claros.
- **Reorganizar**: propongo cambios en forma de diff; no aplico sin solicitud explicita.
- **Nueva nota**:
  - Creo un esqueleto en la ruta indicada.
  - Añado frontmatter minimo si aplica.
  - Incluyo "Creado el: YYYY-MM-DD HH:mm" y fuentes internas.

## Entrega
- Resumen de acciones y rutas leidas.
- Bloque de **Fuentes internas** verificables.

