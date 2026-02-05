---
name: obsidian-analysis-pipeline
description: "Orquesta analisis semantico del vault (conceptos, grafo, embeddings y busqueda) con procesamiento por lotes y manejo de errores."
---
# Obsidian Analysis Pipeline

## Cuando usar
- Necesito indexar semanticamente el vault.
- Quiero extraer conceptos, construir grafo o ejecutar busqueda semantica.
- Quiero procesar en lotes con reanudacion.

## Fases principales
1. **Procesamiento progresivo**
   - Divido en lotes (100 archivos por defecto) y priorizo archivos recientes.
   - Guardo estado en `analisis/estado-procesamiento.json` para reanudar.
2. **Embeddings**
   - Genero embeddings (modelo consistente) y guardo en `analisis/embeddings.json`.
   - Si ya existe, proceso solo archivos con hash cambiado.
3. **Conceptos**
   - Extraigo terminos relevantes, frecuencias y co-ocurrencias en `analisis/conceptos.json`.
4. **Grafo**
   - Construyo nodos y aristas a partir de wikilinks y similitud semantica.
   - Guardo en `analisis/grafo-relaciones.json`.
5. **Busqueda semantica**
   - Calculo similitud coseno contra embeddings y retorno top K con extractos.

## Manejo de errores
- Registro en `analisis/errores.log` con nivel y archivo afectado.
- Reintento con backoff y continuo; no detengo el pipeline por un archivo.
- Creo backup antes de sobrescribir archivos JSON.

## Actualizacion incremental
- Si hay archivos nuevos o modificados, proceso solo esos.
- Elimino entradas de archivos borrados.

## Entrega
- Resumen del estado (archivos procesados, fallidos, tiempo estimado).
- Archivos JSON generados/actualizados y validacion basica.

