---
name: lend-ai-engram
description: >
  Gestión de memoria del ecosistema — guarda, consulta y organiza
  información en Engram para mantener contexto permanente entre sesiones.
  Trigger: Al guardar o consultar memoria en Engram. AUTO-SAVE sin preguntar.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
---

# Skill: lend-ai-engram

Memoria del ecosistema. Si no está en engram, no pasó.

## Regla de ORO

**Guardá SIN PREGUNTAR.** No preguntes "¿guardo esto?". Guardalo. Siempre.
Usá topic_key para que se actualice solo si ya existe.

## EFICIENCIA DE CONTEXTO — NO QUEMES TOKENS EN CALLS

Cada tool call cuesta tokens de ida + vuelta. Optimizá:

### Lectura paralela siempre
- Si necesitás leer 3+ archivos → hacé todo en UNA respuesta con calls paralelos
- No leas de a un archivo por vez

### Delegá exploración compleja
- Si necesitás {globs + greps + reads} para entender algo → usá un solo `task("explore", ...)` que devuelva resumen
- No hagas 8 calls secuenciales cuando un sub-agente puede hacer todo y devolverte el resultado

### Consolidá saves
- No guardes 3+ cosas en Engram en la misma interacción. Juntalas y hacé `mem_save` al final de la tarea
- Si son varias cosas, priorizá: 1 save principal + session_summary al cerrar
- Los saves individuales por cada micro-decisión queman contexto al pedo

### Pensá antes de llamar
- ¿Ya tengo esta info en contexto? → no llamar
- ¿Puedo inferirlo? → no llamar
- ¿Delegar a un sub-agente reduce calls? → delegar
- Regla: si vas a hacer >3 calls para explorar → task("explore")

## AUTO-READ AL INICIAR SESIÓN (obligatorio — paso 0 del flujo)

Antes de cualquier acción, ejecutá en paralelo:
1. `mem_context` → contexto de sesiones recientes
2. `mem_search topic_key:preference/*` → preferencias del usuario
3. `mem_search topic_key:skill/mini/*` → mini-skills aprendidas
4. `mem_search topic_key:pattern/*` → patrones del proyecto

Si no hay preferencias aún → crealas durante la sesión.
Si hay mini-skills → aplicarlas cuando corresponda.

## Triggers de auto-save (sin preguntar)

| Cuándo | type | topic_key | scope |
|--------|------|-----------|-------|
| Cambiaste configuración | `config` | `config/<area>` | project |
| Encontraste y fixeaste un bug | `bugfix` | `bugfix/<area>` | project |
| Tomaste una decisión con tradeoffs | `decision` | `decision/<area>` | project |
| Descubriste algo no obvio | `discovery` | `discovery/<area>` | project |
| Identificaste un patrón reusable | `pattern` | `pattern/<area>` | project |
| Creaste un micro-patrón reusable | `pattern` | `skill/mini/<name>` | project |
| El user dijo algo sobre cómo trabaja | `user_preference` | `preference/<area>` | personal |
| Definiste arquitectura | `architecture` | `architecture/<area>` | project |
| Terminaste una sesión | `session_summary` | — | project |
| Aprendizaje general | `learning` | `learning/<area>` | project |
| El user expresó una preferencia/estilo | `user_preference` | `preference/<area>` | personal |

## Mini-Skills (micro-patrones reutilizables)

Cuando descubras un patrón pequeño que se repite (un atajo, una convención, un approach):

1. Guardalo como `type: pattern`, `topic_key: skill/mini/<nombre>`
2. Formato del contenido:
   ```
   **Qué**: [el micro-patrón en 1 línea]
   **Cuándo**: [trigger — cuándo aplicar este patrón]
   **Cómo**: [instrucción rápida]
   **Ejemplo**: [si aplica]
   ```
3. En la próxima sesión, `mem_search topic_key:skill/mini/*` lo carga automáticamente
4. Si un mini-skill se usa 3+ veces → considerar convertirla en skill formal

## Workflow LEND (modo auto-save, sin menú)

1. DETECTAR
   ├── ¿Pasó algo relevante? (ver triggers arriba)
   ├── ¿Es project o personal?
   └── ¿Tiene topic_key para upsert?

2. GUARDAR (sin preguntar — directo)
   ├── Formato: **What**, **Why**, **Where**, **Learned**
   ├── Tipo: decision, bugfix, pattern, architecture, config, discovery, learning, user_preference
   ├── topic_key: siempre que evolucione en el tiempo
   └── scope: project para código/arquitectura, personal para preferencias del user

3. AL FINAL DE SESIÓN (no preguntar)
   ├── mem_session_summary con Goal/Accomplished/Next Steps/Relevant Files
   └── Guardar preferencias aprendidas durante la sesión

4. VERIFICACIÓN RÁPIDA
   ├── ¿Quedó guardado? sí → seguí
   └── ¿Hay conflicto? → mem_judge automático si confianza > 0.7, si no → preguntar
