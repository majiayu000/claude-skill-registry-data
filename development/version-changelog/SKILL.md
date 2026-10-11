---
name: version-changelog
version: 2.0.0
description: Gestiona versiones semanticas y CHANGELOG.md siguiendo Keep a Changelog y SemVer 2.0 (bump, entrada y etiqueta git). Usar cuando se cierra una fase del work_plan o antes de publicar o entregar. No usar para el cierre completo del proyecto (ver project-finalize).
triggers: [/changelog, version, /release]
author: agent
role: shared
stage: close
cycle_phase: [F7-cierre-sesion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# version-changelog

Gestiona el ciclo de versiones de un proyecto: bumping semántico, entradas de changelog y etiquetas git. Sigue [SemVer 2.0](https://semver.org) y [Keep a Changelog](https://keepachangelog.com).

## Cuándo activar

El Manager activa esta skill:
- Al **cerrar una fase** del work_plan (antes de DONE)
- Cuando el Builder ha completado un conjunto de cambios revisados y aprobados
- Antes de cualquier **publicación o entrega** al usuario

## Conceptos clave

### Reglas SemVer

| Tipo | Cuándo | Ejemplo |
|------|--------|---------|
| **PATCH** (0.0.x) | Bug fix, corrección interna, mejora sin cambio de API | `1.2.3 → 1.2.4` |
| **MINOR** (0.x.0) | Nueva funcionalidad retrocompatible | `1.2.3 → 1.3.0` |
| **MAJOR** (x.0.0) | Cambio incompatible con versión anterior | `1.2.3 → 2.0.0` |
| **pre-release** | Trabajo en progreso | `1.3.0-alpha.1` |

### Secciones del CHANGELOG

```
Added      → nuevas funcionalidades
Changed    → cambios en funcionalidad existente
Deprecated → funcionalidades que serán eliminadas
Removed    → funcionalidades eliminadas
Fixed      → corrección de bugs
Security   → vulnerabilidades corregidas
```

## Workflow

### Paso 1: Leer versión actual

```bash
# Desde pyproject.toml
python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])"

# O desde __init__.py
grep -r "__version__" src/ | head -1
```

Si no existe versión → inicializar en `0.1.0`.

### Paso 2: Clasificar cambios del ciclo actual

Revisar los cambios implementados (via work_plan.md + execution_log.md) y clasificar:

```markdown
## Clasificación de cambios

**Tipo de bump sugerido:** MINOR  <- (PATCH / MINOR / MAJOR)
**Razón:** Se añadieron 2 nuevas funcionalidades sin romper API existente

**Added:**
- Skill `graphify` para exploración eficiente de codebase
- Skill `version-changelog` para gestión de versiones

**Fixed:**
- (ninguno)

**Changed:**
- (ninguno)
```

Presentar clasificación al Manager para **validación humana** antes de continuar.

### Paso 3: Calcular nueva versión

```python
# Ejemplo de lógica de bump
current = "1.2.3"
major, minor, patch = map(int, current.split("."))

bump_type = "minor"  # determinado en Paso 2

if bump_type == "major":
    new_version = f"{major+1}.0.0"
elif bump_type == "minor":
    new_version = f"{major}.{minor+1}.0"
else:  # patch
    new_version = f"{major}.{minor}.{patch+1}"

print(f"{current} → {new_version}")
```

### Paso 4: Actualizar CHANGELOG.md

Si no existe `CHANGELOG.md`, crearlo con la plantilla base (ver reference).

Añadir la nueva entrada **al inicio** del archivo, justo después del header:

```markdown
## [1.3.0] - 2026-04-13

### Added
- Skill `graphify` para construcción de grafos de conocimiento persistentes
- Skill `version-changelog` para gestión semántica de versiones

### Fixed
- Corrección en hook `guard_paths` con rutas con espacios
```

El bloque `[Unreleased]` se vacía y queda listo para el próximo ciclo:

```markdown
## [Unreleased]

### Added
### Changed
### Fixed
```

### Paso 5: Actualizar versión en el proyecto

**pyproject.toml:**
```toml
[project]
version = "1.3.0"
```

**src/__init__.py** (si existe):
```python
__version__ = "1.3.0"
```

Buscar y actualizar todos los lugares donde vive la versión:
```bash
grep -r "version" pyproject.toml src/__init__.py 2>/dev/null
```

### Paso 6: Actualizar PROJECT.md

Añadir entrada en el historial de PROJECT.md:

```markdown
# Historial de versiones

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.3.0 | 2026-04-13 | Skills graphify y version-changelog |
| 1.2.0 | 2026-03-15 | Sistema multi-agente v4 |
```

### Paso 7: Git tag (solo si el usuario aprueba)

```bash
git add CHANGELOG.md pyproject.toml src/__init__.py PROJECT.md
git commit -m "chore: bump version to 1.3.0

- Actualiza CHANGELOG con cambios del ciclo
- Versión en pyproject.toml y __init__.py"

git tag -a v1.3.0 -m "Release 1.3.0"
```

**IMPORTANTE**: El tag solo se crea si el Manager lo aprueba explícitamente. No crear tags automáticamente.

## Plantilla CHANGELOG.md

Ver `references/changelog-template.md`.

## Constraints

- **NUNCA** saltarse la validación humana del tipo de bump (Paso 2 → Manager aprueba)
- **NUNCA** crear git tags sin aprobación explícita del usuario
- **SIEMPRE** mantener el bloque `[Unreleased]` en CHANGELOG.md
- **SIEMPRE** usar formato ISO-8601 para fechas (`YYYY-MM-DD`)
- Las entradas del changelog deben ser **legibles por humanos**, no mensajes de commit
- Si el proyecto usa `__version__` en múltiples sitios, actualizarlos todos

## References

- `references/changelog-template.md` - Plantilla CHANGELOG.md inicial
- `references/semver-decision-guide.md` - Guía de decisión PATCH/MINOR/MAJOR
