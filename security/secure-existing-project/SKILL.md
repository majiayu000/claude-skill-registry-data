---
name: secure-existing-project
version: 2.1.0
description: Aplica la arquitectura de seguridad privada/publica a un proyecto Python existente con credenciales expuestas (fallback por convencion, no la solucion final). Usar cuando un proyecto ya existente guarda secretos en el arbol. No usar para un proyecto nuevo (ver scaffold-python-project) ni cuando keyring o SOPS resuelven el caso.
triggers: [/secure, /security-audit, /harden]
author: agent
role: shared
stage: support
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# secure-existing-project

Migra un proyecto Python existente a la arquitectura de seguridad privada/publica.

## Overview

Convierte un proyecto con credenciales expuestas a uno seguro con separación privada/publica.

> **Nota de arquitectura:** la separación `privada/`/`publica/` de este skill es un
> **fallback operativo por convención** (útil cuando el proyecto aún no tiene
> alternativa mejor), no la solución de seguridad final. Según el contexto del
> proyecto, prefiere: **keyring / OS DPAPI** para apps locales mono-usuario, **SOPS +
> age** para secretos compartidos o versionados cifrados, y **OAuth2 / OIDC / tokens
> efímeros** para sistemas productivos o backends. Este workflow documenta el
> fallback `privada/`; no sustituye esas opciones cuando son viables.

## Workflow

### Paso 1: Auditar Proyecto Actual

Buscar secrets hardcodeados:
```bash
grep -r "API_KEY\|SECRET\|PASSWORD\|TOKEN" src/ --include="*.py"
find . -name "*.env" -o -name "config.json" -o -name "credentials*"
```

**Lista de hallazgos:**
- Archivos con credenciales en repo
- Variables hardcodeadas
- Configuraciones sensibles

### Paso 2: Crear Estructura Segura

```
proyecto/
├── privada/              # ⛔ NUNCA commitear
│   ├── .env
│   ├── config.json
│   └── credentials.json
│
└── publica/
    └── repo/             # ✅ Workspace agentes
        ├── src/
        ├── tests/
        └── .env.example
```

### Paso 3: Migrar Secrets (👤 Usuario)

Instruir al usuario:
```markdown
## Acción Requerida (Usuario)

Mover archivos sensibles a `privada/`:

1. Copiar `.env` → `privada/.env`
2. Copiar `config.json` → `privada/config.json`
3. Eliminar originales de `publica/repo/`
4. Crear versiones `.example` sin valores reales
```

### Paso 4: Implementar Configuración

Crear `src/config.py`:
```python
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
PRIVATE_DIR = ROOT_DIR.parent.parent / "privada"

DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "output"
LOGS_DIR = ROOT_DIR / "logs"
```

Crear `src/settings.py` con búsqueda en cascada (ver reference).

### Paso 5: Actualizar .gitignore

```gitignore
# Seguridad
privada/
.env
.env.*
config.json
credentials.json
*.key
*.pem

# Python
__pycache__/
.venv/
```

### Paso 6: Verificar

```bash
# Verificar que privada/ no está trackeada
git status | grep privada  # No debe mostrar nada

# Verificar que .env.example existe
ls -la publica/repo/.env.example
```

### Paso 7 (opcional): Evaluar alternativa de la jerarquía escalonada

Antes de dar la migración por completa, evalúa si `privada/` es la opción correcta a
largo plazo o solo el fallback inmediato:

- **¿El proyecto es local y mono-usuario?** Considera migrar a `keyring` (Python) u
  OS DPAPI (Windows) en vez de `.env` en disco.
- **¿Los secretos deben compartirse entre desarrolladores o versionarse cifrados?**
  Considera SOPS + age.
- **¿El proyecto corre en un backend o entorno productivo?** Considera OAuth2 / OIDC
  / tokens efímeros en vez de credenciales estáticas.

Si ninguna alternativa es viable todavía, `privada/` con `.gitignore` + hook
`guard_paths` sigue siendo el fallback operativo válido -- pero queda registrado
como decisión temporal, no como arquitectura final.

## Output

- Estructura `privada/` creada
- `config.py` y `settings.py` implementados
- `.gitignore` actualizado
- Archivos `.example` creados
- Instrucciones al usuario para migración

## References

- `references/security-checklist.md` - Checklist de auditoría
- `references/cascade-config-pattern.md` - Código de config/settings

## Constraints

- **NO** mover archivos de `privada/` automáticamente (usuario lo hace)
- **NO** dejar secrets en código después de la migración
- **SIEMPRE** crear archivos `.example`
- **`privada/` es fallback, no solución final**: si el proyecto tiene mejor
  alternativa disponible (keyring/DPAPI, SOPS+age, OAuth2/OIDC), documentarla como
  siguiente paso en vez de asumir que la separación `privada/`/`publica/` cierra el
  tema de seguridad.
