---
name: obsidian-dispatch
description: Router de intención para Obsidian en Codex CLI. Selecciona la skill más adecuada (o pide la mínima aclaración), aplica guardrails de lectura real y ejecuta el flujo correcto sin inflar AGENTS.md.
---

# Obsidian Dispatch (Router)

## Objetivo
Actuar como “controlador de tráfico” de la bóveda: interpretar la petición del usuario, **elegir la skill correcta** y conducir la ejecución con el mínimo de fricción y el máximo de seguridad (sin inventar).

## Reglas globales (no negociables)
1. **Cero alucinaciones**: si no puedes leer/verificar una fuente del vault necesaria para la respuesta, di **“no consta en la bóveda”** y ofrece el siguiente paso.
2. **Lectura real antes de concluir**: para decisiones o respuestas sustantivas, lee el/los archivos relevantes.
3. **Cambios con riesgo** (mover/renombrar/ediciones masivas): propone plan reversible y lista de archivos impactados.
4. **No tocar `_templates/`** sin permiso explícito.
5. Mantén la interacción **directa**: una única pregunta solo si desbloquea la acción.

## Cómo se usa
- Invocación recomendada: `$obsidian-dispatch` seguido de tu objetivo.
- Si el usuario no invoca skills explícitamente pero la intención es clara, puedes auto-aplicar este router mentalmente.

---

## 1) Clasificación de intención (elige UNA ruta)

### A. Búsqueda / localización
Señales: “encuentra”, “busca”, “dónde está”, “qué notas hablan de…”, “lista”.
→ Usa: `obsidian-vault-ops` (buscar + leer).

### B. Lectura / verificación / trazabilidad
Señales: “confirma”, “verifica en la nota”, “cita fuentes internas”, “¿dónde pone…?”.
→ Usa: `obsidian-vault-ops` (leer) + `obsidian-links` si hay enlaces dudosos.

### C. Frontmatter / Dataview
Señales: “YAML”, “frontmatter”, “propiedades”, “dataview”, “normaliza campos”.
→ Usa: `obsidian-frontmatter`.

### D. Estructura y limpieza Markdown
Señales: “reorganiza”, “limpia”, “estructura”, “formatea”, “hazlo legible”, “sin romper Dataview/Templater”.
→ Usa: `obsidian-markdown-structure`.

### E. Enlaces internos (wikilinks)
Señales: “enlaza”, “crea links”, “repara enlaces rotos”, “sección/ancla”.
→ Usa: `obsidian-links`.

### F. Mermaid / diagramas
Señales: “diagrama”, “Mermaid”, “flujo”, “arquitectura”, “secuencia”.
→ Usa: `obsidian-mermaid`.

### G. Canvas
Señales: “canvas”, “.canvas”, “nodos”, “edges”, “layout”.
→ Usa: `obsidian-canvas`.

### H. Tareas
Señales: “tareas”, “backlog”, “inbox”, “prioriza”, “semanal”, “daily”.
→ Usa: `obsidian-task-ops`.

### I. Procedimientos / SOP
Señales: “procedimiento”, “SOP”, “playbook”, “checklist”, “estándar”.
→ Usa: `obsidian-sop-authoring`.

---

## 2) Resolución de ambigüedad (solo si es necesario)
Si hay dos rutas posibles, haz **UNA** pregunta de desambiguación con opciones cerradas:

Ejemplos:
- “¿Quieres que **solo** lo resuma (sin tocar archivos) o que además **reestructure** la nota?”
- “¿El objetivo es **arreglar enlaces** o **normalizar YAML**?”

Si el usuario no responde, elige la opción **menos destructiva** (leer/responder, sin editar).

---

## 3) Ejecución estándar (plantilla)
1. **Reformular** el objetivo en 1 línea (para confirmar intención sin pedir permiso).
2. **Seleccionar** skill (según mapa).
3. **Operar** siguiendo la skill elegida:
   - Buscar → Leer → Actuar → Validar.
4. **Salida**:
   - Resumen de lo hecho
   - Archivos tocados (si aplica)
   - Fuentes internas cuando corresponda

---

## 4) Atajos (para funcionar “solo”)
Si el usuario da instrucciones muy claras, no pidas confirmación; ejecuta:
- “Normaliza frontmatter” → `obsidian-frontmatter`
- “Crea diagrama Mermaid” → `obsidian-mermaid`
- “Repara enlaces” → `obsidian-links`

---

## 5) Política de “no consta”
Di “no consta en la bóveda” únicamente cuando:
- el dato requerido depende de una fuente interna que no existe/no se puede leer,
- o cuando el usuario pide certezas sin aportar el archivo.

Siempre añade: “Puedo hacerlo si me indicas la nota (ruta/nombre) o pegas el contenido relevante.”

