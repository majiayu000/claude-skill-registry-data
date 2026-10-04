---
name: epistemic-redundancy-audit
description: Protocolo de detección termodinámica de entropía documental y colapso de redundancias. Identifica archivos clónicos (Similitud Jaccard) y secciones solapadas (encabezados duplicados) en un corpus Markdown, forzando la consolidación bajo invariantes C5-REAL (Cero Anergía).
---

# Auditoría de Redundancia Epistémica (Epistemic Redundancy Audit)

**Contexto:** El axioma de Cero Anergía prohíbe la fragmentación de la verdad. Múltiples fuentes para una misma definición, o archivos documentales clónicos, inyectan fricción termodinámica en el repositorio.

## 1. Disparadores (Triggers)
- "busca redundancias"
- "auditoría documental"
- "document redundancy"
- "entropía documental"
- "limpiar docs"
- "epistemic redundancy audit"

## 2. Metodología de Ejecución

Cuando el usuario requiera auditar redundancias en un directorio de documentación, procede estrictamente en este orden:

1. **Detección de Duplicados a Nivel de Archivo (Jaccard / Hashing):**
   - No confíes en el repositorio base sin medir. Ejecuta un script en Python (vía `run_command`) que recorra los archivos `.md` del directorio objetivo.
   - Calcula la similitud Jaccard de los tokens/palabras entre pares de archivos. 
   - Reporta cualquier par con un índice de similitud Jaccard superior a 0.8 como un "Clon Estructural" o "Duplicado de Alta Fricción".

2. **Detección de Duplicados a Nivel de Estructura (Encabezados):**
   - Ejecuta un script en Python que lea todos los archivos objetivo y extraiga todos los encabezados Markdown (`#`, `##`, `###`).
   - Cuenta la frecuencia de cada encabezado. 
   - Reporta cualquier encabezado que aparezca múltiples veces en el mismo archivo (o en el corpus, si el contexto lo requiere) como "Entropía Intra-Documental".

3. **Propuesta de Colapso (Consolidación):**
   - No borres ni edites directamente sin presentar la evidencia.
   - Presenta la topología redundante al Operador (ej. "Encontrados 4 certificados exactos, 2 mapeos de artículos duplicados").
   - Propón una purga o consolidación usando herramientas como `replace_file_content` o borrado de archivos (`rm`), garantizando preservar una única "Fuente de Verdad" (Single Source of Truth).
