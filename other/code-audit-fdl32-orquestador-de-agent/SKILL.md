---
name: code-audit
version: 2.1.0
description: Auditoria sistematica de codigo Python que detecta dead code, deuda tecnica y archivos inactivos con vulture, deadcode, ruff y git log. Usar cuando se quiere un censo de codigo muerto o deuda antes de limpiar o refactorizar. No usar para auditar la suite de tests (ver test-audit) ni para revisar el cambio de un ticket (ver manager-review-implementation).
triggers: [/code-audit, code-quality, /deadcode]
author: agent
role: auditor
stage: review
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# code-audit

Skill para ejecutar auditoría completa del codebase identificando código muerto, deuda técnica y patrones problemáticos.

## Overview

La auditoría realiza análisis estático multi-herramienta combinando:
- **vulture**: Detección de símbolos no utilizados (confidence >= 80)
- **deadcode**: Análisis de flujo para código realmente muerto
- **ruff**: Deuda técnica (complejidad ciclomática C90, código antiguo ERA, simplificaciones SIM)
- **git log**: Antigüedad de archivos (commit count para categorizar abandono)

## Workflow

### Paso 0: Verificar Pre-condiciones

Confirmar que las herramientas están disponibles:

```powershell
# PowerShell (Windows)
python -m vulture --version
deadcode --version
python -m ruff --version
```

```bash
# Bash/POSIX
python -m vulture --version
deadcode --version
ruff --version
```

Si faltan, instalar con: `uv sync`

Herramientas requeridas declaradas en `pyproject.toml`: `vulture>=2.0`, `deadcode>=2.0`.

### Paso 1: Ejecutar Vulture (simbolos no usados)

```powershell
# PowerShell
python -m vulture . --min-confidence 80 --exclude ".venv,venv,__pycache__,.git,agent_system,.agent"
```

```bash
# Bash
python -m vulture . --min-confidence 80 --exclude ".venv,venv,__pycache__,.git,agent_system,.agent"
```

**Salida esperada:** Lista de `path/file.py:NN: unused X 'name' (NN% confidence)`

Si la salida es grande, filtrar a un subdirectorio: `python -m vulture bus/ scripts/ --min-confidence 80`

> **Nota Windows:** La captura de salida de vulture puede tener encoding issues en Windows.
> Si ocurre, redirigir: `python -m vulture . --min-confidence 80 2>&1 | Out-File audit_vulture.txt -Encoding utf8`

### Paso 2: Ejecutar Deadcode (codigo realmente muerto)

```powershell
# PowerShell
deadcode . --exclude ".venv,venv,__pycache__,.git,agent_system,.agent"
```

```bash
# Bash
deadcode . --exclude ".venv,venv,__pycache__,.git,agent_system,.agent"
```

**Salida esperada:** Lista de `path/file.py:NN:N: DC01 X 'name' is never used`

Errores parciales (librerías externas sin AST) son tolerables — continuar.

### Paso 3: Ejecutar Ruff (deuda técnica)

```powershell
# PowerShell / Bash (mismo comando)
python -m ruff check . --select C90,ERA,SIM --output-format concise
```

**Salida esperada:** Lista de `path/file.py:NN:N: C901 'func' is too complex`

Reglas activas:
- **C90**: Complejidad ciclomática alta
- **ERA**: Código comentado (candidato a eliminar)
- **SIM**: Simplificaciones disponibles

### Paso 4: Revisar Antigüedad (git log)

```bash
# Ver archivos con menor actividad reciente (bash/git)
git log --oneline --name-only --since="6 months ago" | grep "\.py$" | sort | uniq -c | sort -n | head -20
```

```powershell
# PowerShell equivalente
$since = (Get-Date).AddMonths(-6).ToString("yyyy-MM-dd")
git log --oneline --name-only --after=$since |
    Where-Object { $_ -match "\.py$" } |
    Group-Object | Sort-Object Count | Select-Object -First 20 Count, Name
```

Archivos con 0-2 cambios en 6 meses son candidatos a ABANDONED/DEAD.

### Paso 5: Categorizar y Documentar Hallazgos

Para cada hallazgo cruzar vulture/deadcode con git log:

| Categoria | Criterio | Accion |
|-----------|----------|--------|
| **DEAD** | 0 commits + 0 usos | Eliminar inmediatamente |
| **ABANDONED** | <5 commits + 0 usos | Revisar manualmente antes de eliminar |
| **LEGACY** | >=5 commits + 0 usos | Revisar con equipo (puede ser API publica) |
| **SMELL** | Hallazgo ruff (C90/ERA/SIM) | Deuda tecnica, agendar refactor |

Documentar decisiones en `execution_log.md`:

```markdown
### Code Audit Results — [FECHA]

**Hallazgos:**
- Vulture: N items (confidence >= 80)
- Deadcode: N items
- Ruff C90/ERA/SIM: N items

**Decisiones:**
- DEAD: X eliminados
- ABANDONED: Y revisados, Z eliminados
- LEGACY: W confirmados como API interna
- SMELL: V documentados en PROJECT.md para refactor gradual
```

## Constraints

### Umbrales

| Herramienta | Parametro | Valor | Razon |
|-------------|-----------|-------|-------|
| vulture | `--min-confidence` | 80 | Evitar false positives en parametros opcionales |
| deadcode | `--exclude` | `.venv,venv,__pycache__,.git,agent_system,.agent` | Ignorar deps y frameworks |
| ruff | `--select` | `C90,ERA,SIM` | Complejidad, codigo antiguo, simplificaciones |
| git | `--since` | 6 months | Ventana de actividad para clasificar abandono |

### Limitaciones Conocidas

- **Windows encoding**: Vulture puede tener problemas con caracteres no-ASCII; redirigir a archivo con `-Encoding utf8` si ocurre.
- **Librerias externas**: Deadcode puede no analizar codigo de terceros — tolerable.
- **No-git repos**: Los pasos de git son opcionales si no es repo git.

### Reglas de Uso

- **NUNCA** eliminar codigo LEGACY sin revision manual (puede ser API publica).
- **SIEMPRE** documentar decisiones en `execution_log.md`.
- Los hallazgos son sugerencias del agente, no acciones automaticas.

## References

- `references/audit-report-template.md` — Plantilla para decisiones por hallazgo
- `references/audit-tools-guide.md` — Umbrales y configuracion de cada herramienta

---

**Version:** 2.1.0
**Autor:** agent-system
**Ultima actualizacion:** 2026-06-11 (WT-2026-253a: reescrito sobre CLIs directas)
