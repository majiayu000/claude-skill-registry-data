---
name: create-agent-skill
version: 2.0.0
description: Meta-skill para crear una micro-skill nueva siguiendo el estandar Agent Skills (frontmatter validado, triggers, workflow). Usar cuando se necesita una skill nueva para una accion concreta y repetible. No usar para editar a mano una skill existente ni para un contrato de gobierno (los prompts de prompts/ gobiernan y la skill solo apunta).
triggers: [/create-skill, skill-create, /new]
author: agent
role: shared
stage: meta
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# create-agent-skill

Crea nuevas micro-skills portables siguiendo el estándar establecido.

## Overview

Cuando necesitas una nueva skill para una acción específica, usa esta skill para crearla correctamente.

## Workflow

### Paso 1: Definir Propósito

Determinar:
- **¿Qué acción realiza?** (una sola, concreta)
- **¿Quién la usa?** (Manager / Builder / Ambos)
- **¿Qué necesita saber el agente?** (contexto mínimo)

### Paso 2: Identificar Fuentes

Buscar en el sistema actual:
- Workflows relevantes
- Reglas del agente
- Protocolos existentes
- Código de referencia

**Principio:** Condensar, no copiar.

### Paso 3: Crear Estructura

```bash
# Nombre en kebab-case
mkdir -p skills/[nombre-skill]/references
```

**Convención de nombres** (verificada contra las 43 skills reales en disco; `man-`/`bui-` fue el
diseño original pero NUNCA se adopto — las 8 skills de Manager/Builder usan el nombre completo):
- `manager-[accion]` - Skills del Manager
- `builder-[accion]` - Skills del Builder
- `[accion]` - Skills compartidas / auditor / usuario (sin prefijo de rol)

**NO confundir con `contract_id`:** algunos `contract_id` historicos usan el prefijo corto
(`cid-man-review-v2`, `cid-bui-implement-v1`) porque se acunaron antes de fijar esta convencion.
Esos identificadores estan VIVOS y citados en skills activas (`builder-implement-from-plan`,
`builder-run-quality-gates`, `manager-review-implementation`) — no se renombran. El prefijo corto
solo esta prohibido para el NOMBRE DE CARPETA de una skill nueva.

### Paso 4: Escribir SKILL.md

Estructura obligatoria:
```markdown
---
name: nombre-skill
version: 1.0.0
description: Descripción clara de una línea
triggers: [/comando, alias1, alias2]
author: agent-system
role: shared            # user | shared | manager | builder | auditor
stage: support          # setup | plan | implement | quality | review | close | memory | support | meta
tags: [tag1, tag2, tag3]
writes_memory: false
quality_gate: false
---

# nombre-skill

Descripción breve (1-2 líneas).

## Overview

Cuándo y para qué usar esta skill.

## Workflow

### Paso 1: [Nombre del paso]
Instrucciones claras...

### Paso 2: [Nombre del paso]
...

## Output Format

Qué produce esta skill.

## References

- `references/ref1.md` - Descripción

## Constraints

- **NO** hacer X
- **SIEMPRE** hacer Y
```

**Límites:**
- SKILL.md: máximo 250 líneas
- References: máximo 80 líneas cada una

### Paso 5: Crear References

Extraer y condensar de las fuentes:
- Checklists
- Templates
- Ejemplos de código
- Formatos

### Paso 6: Validar

```bash
python skills/validate_all.py
```

Verificar:
- [ ] Frontmatter YAML válido
- [ ] Campos requeridos (ver `REQUIRED_FIELDS` en `skills/validate_all.py`, fuente de verdad —
  no copiar esta lista a mano en otro sitio): name, version, description, author, tags, role,
  stage, writes_memory, quality_gate
- [ ] `triggers` presente (recomendado para todas las skills activables por comando; no es
  requerido por `validate_all.py`, pero su ausencia impide el discovery por trigger)
- [ ] Cuerpo no supera 250 líneas
- [ ] References no superan 80 líneas
- [ ] Carpeta `references/` existe

### Paso 7: Documentar

Añadir a `skills/README.md`:
```markdown
| nombre-skill | Descripción | Manager/Builder | tags |
```

## Progressive Disclosure

Estructura de información:
1. **Frontmatter** - Metadatos esenciales
2. **Body** - Instrucciones paso a paso
3. **References** - Detalles de apoyo

## Output

Nueva skill en:
```
skills/[nombre-skill]/
├── SKILL.md           # Instrucciones principales
└── references/        # Documentación de apoyo
    ├── ref1.md
    └── ref2.md
```

## References

- `references/skill-anatomy.md` - Anatomía de un SKILL.md
- `references/frontmatter-template.md` - Template de frontmatter

## Constraints

- **UNA** acción por skill
- **MÁXIMO** 250 líneas en SKILL.md
- **MÁXIMO** 80 líneas por reference
- **SIEMPRE** validar con `validate_all.py`
- **USAR** nombre completo `manager-`/`builder-` según corresponda (NO el prefijo corto
  `man-`/`bui-`, que es el nombre de carpeta de una skill nueva — no confundir con un
  `contract_id` historico existente, que no se renombra)
