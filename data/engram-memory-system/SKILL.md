---
name: engram-memory-system
description: "Trigger: When you need to save, consult, classify, or organize memory in Engram. Skill global de gestion de memoria — clasifica, organiza y decide el mejor sistema de almacenamiento para cada tipo de conocimiento en Engram."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Sistema de Memoria Engram

Carga esta skill cuando estes por guardar o consultar memoria en Engram.

## [REGLAS] REGLA DE ORO

**Guardá SIN PREGUNTAR.** No le preguntes al usuario "¿guardo esto?". Guardalo. Siempre.

Si no estás seguro del proyecto, pensalo 2 segundos. Si aún así no sabés, preguntá. Pero no preguntes "¿lo guardo?", preguntá "¿en qué proyecto?".

## AUTO-READ (OBLIGATORIO al iniciar sesión)

Antes de cualquier acción, ejecutá en paralelo:
1. `mem_context` → últimas sesiones, contexto fresco
2. `mem_search topic_key:preference/*` scope:personal → preferencias del user
3. `mem_search topic_key:skill/mini/*` → mini-skills del proyecto
4. `mem_search topic_key:pattern/*` → patrones del proyecto

Propósito: que cada sesión arranque sabiendo quién es el user, qué le gusta,
qué mini-skills están disponibles, y qué patrones aplican.

## Jerarquía de topic_key (carpetas virtuales)

```
topic_key = <area>/<subarea>
```

| Carpeta | Para qué | Ejemplo |
|---------|----------|---------|
| `architecture/infra` | Servidores, redes, Tailscale, VPNs | `architecture/infra` |
| `architecture/data` | Pipelines, ETL, DB schema | `architecture/data` |
| `architecture/frontend` | Componentes, estado, routing | `architecture/frontend` |
| `architecture/system` | Ecosistema, agentes, skills, SDD | `architecture/system` |
| `architecture/database` | SQL, esquemas, migraciones | `architecture/database` |
| `bugfix/python` | Errores en código Python | `bugfix/python` |
| `bugfix/infra` | Errores de infraestructura | `bugfix/infra` |
| `bugfix/config` | Errores de configuración | `bugfix/config` |
| `bugfix/tool` | Errores de herramientas/MCPs | `bugfix/tool` |
| `pattern/python` | Patrones de Python | `pattern/python` |
| `pattern/git` | Patrones de git y PRs | `pattern/git` |
| `pattern/workflow` | Patrones de flujo de trabajo | `pattern/workflow` |
| `pattern/architecture` | Patrones arquitectónicos | `pattern/architecture` |
| `skill/mini/<name>` | Mini-skills (micro-patrones reutilizables) | `skill/mini/commit-format` |
| `discovery/tool` | Descubrimientos sobre herramientas | `discovery/tool` |
| `discovery/workflow` | Descubrimientos sobre procesos | `discovery/workflow` |
| `discovery/ecosystem` | Descubrimientos sobre el ecosistema | `discovery/ecosystem` |
| `config/mcp` | Configuraciones de MCPs | `config/mcp` |
| `config/environment` | Variables de entorno, setup | `config/environment` |
| `config/tool` | Configuraciones de herramientas | `config/tool` |
| `config/system` | Config del ecosistema | `config/system` |
| `decision/architecture` | Decisiones arquitectónicas | `decision/architecture` |
| `decision/tool` | Decisiones sobre herramientas | `decision/tool` |
| `decision/workflow` | Decisiones sobre flujo | `decision/workflow` |
| `learning/language` | Aprendizaje de lenguajes | `learning/language` |
| `learning/tool` | Aprendizaje de herramientas | `learning/tool` |
| `learning/domain` | Aprendizaje de dominios | `learning/domain` |
| `preference/workflow` | Cómo le gusta trabajar al usuario | `preference/workflow` |
| `preference/tech-stack` | Tecnologías que prefiere | `preference/tech-stack` |
| `preference/communication` | Cómo le gusta que le hablen | `preference/communication` |
| `preference/general` | Otras preferencias | `preference/general` |

## Guardado automático (sin preguntar)

| Cuándo | type | topic_key | scope |
|--------|------|-----------|-------|
| Cambiaste configuración | `config` | `config/<area>` | project |
| Encontraste y fixeaste un bug | `bugfix` | `bugfix/<area>` | project |
| Tomaste una decisión con tradeoffs | `decision` | `decision/<area>` | project |
| Descubriste algo no obvio | `discovery` | `discovery/<area>` | project |
| Identificaste un patrón reusable | `pattern` | `pattern/<area>` | project |
| Aprendiste algo del usuario | `user_preference` | `preference/<area>` | **personal** |
| Definiste arquitectura | `architecture` | `architecture/<area>` | project |
| Terminaste una sesión | `session_summary` | — | project |
| Aprendizaje general | `learning` | `learning/<area>` | project |

## Perfil del usuario (crece solo)

Cuando descubras algo nuevo del usuario (cómo trabaja, qué prefiere, qué no le gusta):
1. Guardalo como `user_preference` con scope `personal`
2. Usá topic_key `preference/<area>` (ej: `preference/communication`, `preference/tech-stack`)
3. Si ya existe una entrada con ese topic_key, se actualiza sola (upsert)
4. **No preguntes** — guardalo y seguí

## Formato del contenido

```
**What**: [qué pasó, una línea]
**Why**: [por qué, qué problema resolvía]
**Where**: [archivos/componentes afectados, o la fuente del aprendizaje]
**Learned**: [gotchas, edge cases, decisiones no obvias — omitir si no aplica]
```

## Árbol de tipos

```
¿Qué tipo de información es?
│
├── architecture → decisiones de alto nivel sobre estructura
│   → topic_key: architecture/<area>
│   → scope: project
│
├── bugfix → bugs con causa raíz y solución
│   → topic_key: bugfix/<area>
│   → scope: project
│
├── pattern → patrones reutilizables, convenciones
│   → topic_key: pattern/<area>
│   → scope: project
│
├── config → configuraciones, setup, instalaciones
│   → topic_key: config/<area>
│   → scope: project
│
├── discovery → gotchas, edge cases, aprendizajes no obvios
│   → topic_key: discovery/<area>
│   → scope: project
│
├── decision → elecciones con tradeoffs documentados
│   → topic_key: decision/<area>
│   → scope: project
│
├── learning → aprendizajes generales
│   → topic_key: learning/<area>
│   → scope: project
│
├── user_preference → todo sobre el usuario
│   → topic_key: preference/<area>
│   → scope: personal (SIEMPRE)
│
└── session_summary → resumen al finalizar sesión
    → usar mem_session_summary, NO mem_save
    → scope: project
```

## Reglas de scope

| Scope | Cuándo usarlo |
|-------|--------------|
| `project` | Código, arquitectura, bugs, config, skills del proyecto actual |
| `personal` | TODO lo que sea del usuario: preferencias, forma de trabajar, gustos |

## LEND Workflow (modo auto-save)

### 1. DETECTAR
Antes de actuar, consultar Engram: mem_context para contexto reciente, mem_search para decisiones previas. Detectar si el evento actual merece guardado.

### 2. CLASIFICAR
Usar el árbol de tipos para elegir type, topic_key y scope. Si evoluciona en el tiempo → topic_key para upsert automático.

### 3. GUARDAR (sin preguntar — REGLA DE ORO)
mem_save con What/Why/Where/Learned. No preguntes "¿guardo esto?". Guardalo.

### 4. VERIFICAR + AUTO-EVOLUCIÓN
Confirmar que quedó guardado. Si hay conflictos con confianza > 0.7 → mem_judge automático. Si confianza < 0.7 → preguntar al user.

## Auto-evolución del sistema de memoria

El sistema de memoria NO es estático. Evoluciona solo:

### Detección de patrones
- Si un mismo topic_key se actualiza 3+ veces → considerar crear una skill dedicada
- Si un patrón de bugfix se repite → proponer test o guardia automática
- Si una preferencia del user aparece 2+ veces → consolidar en el perfil

### Mini-skills evolution
- Un `skill/mini/<name>` se usa 1-2 veces → sigue siendo mini
- Se usa 3+ veces → considerar skill formal en `skills/<name>/SKILL.md`
- Se vuelve crítico → agregarlo a `opencode.json` skills del agente correspondiente

### Crecimiento autónomo
- Cada 5 sesiones: el `growth-engine` revisa patrones en Engram y propone nuevas skills
- Si un discovery se vuelve recurrente → convertirlo en pattern
- Si un pattern se vuelve estándar → proponer skill formal
- Las mini-skills viejas (>5 sesiones sin uso) → archivar o eliminar

### Frescura de la memoria
- mem_context al iniciar sesión (siempre)
- mem_search antes de decisiones importantes
- Si una memoria tiene >10 sesiones de antigüedad y no se consultó → consolidar o archivar
- No borrar memorias viejas automáticamente — pero priorizar las frescas en context

## Cuando NO guardar

- Cada comando que ejecutaste (no es un log)
- Trivialidades (instalaciones de paquetes obvias)
- Info que ya esta en el codigo (para eso esta el repo)
- Lo mismo dos veces (usa topic_key para upsert)

## Cuando consultar (antes de actuar)

- Al empezar sesion: `mem_context` + `mem_search topic_key:preference/*` + `mem_search topic_key:skill/mini/*` + `mem_search topic_key:pattern/*`
- Antes de decisiones importantes: `mem_search "tema"`
- Cuando un error parece conocido: `mem_search type:bugfix`
- Cuando no recordas una preferencia: `mem_search scope:personal topic_key:preference/*`
- Antes de crear algo nuevo: ver si ya hay patrones similares o mini-skills aplicables
