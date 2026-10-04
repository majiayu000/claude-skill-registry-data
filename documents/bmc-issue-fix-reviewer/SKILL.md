---
name: bmc-issue-fix-reviewer
description: >
  Local alternative to Cursor Agent Review (Issue and Fix): reviews branch or
  uncommitted diffs against project rules, finds bugs/security/logic issues, and
  applies fixes. Runs gate:local after fixes. Use when Agent Review fails
  (insufficient funds), user says issue and fix, revisar y arreglar, or review
  and fix changes.
---

# BMC Issue & Fix Reviewer

Reemplazo local de **Cursor Agent Review → Issue and Fix**: revisa cambios, encuentra problemas reales y **corrige código** (no solo comenta).

**Orquestación:** para el flujo completo (Bugbot + fix + gates), usar la skill padre `.cursor/skills/issue-and-fix/SKILL.md` o `/issue-and-fix`.

---

## When to Use

- `Failed to run review: insufficient funds` en Agent Review de Cursor
- Usuario pide **fix-only**, **solo arreglar**, o agente `bmc-issue-fix-reviewer` directo
- Para flujo completo con Bugbot → usar `/issue-and-fix` (no esta skill sola)
- Antes de commit/PR cuando quieres revisión + corrección automática del diff

---

## Scope Modes

| Mode | Cuándo | Cómo obtener diff |
|------|--------|-------------------|
| `branch` (default) | Cambios de la rama vs base | `git diff` merge-base con `main` + staged + unstaged |
| `uncommitted` | Solo working tree | `git diff` + `git diff --cached` |
| `files` | Archivos explícitos | Leer archivos listados por el usuario |

Si el usuario no especifica → `branch`.

---

## Workflow

### 1. Context load (obligatorio)

Leer antes de revisar:

1. `AGENTS.md` — convenciones API, Sheets 503, no secrets
2. `CLAUDE.md` — hot spots si el diff toca calc/API/PDF
3. Reglas activas en `.cursor/rules/` (especialmente las que el diff viola)
4. `docs/team/PROJECT-STATE.md` solo si el cambio es grande o cross-module

### 2. Gather diff

```bash
cd /Users/matias/calculadora-bmc
git status --short
git branch --show-current
# branch mode:
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master
git diff <merge-base>...HEAD
git diff
git diff --cached
```

Si no hay diff ni untracked relevantes (ver scope) → informar en una línea y parar. En `branch`, no parar solo porque `git status` esté vacío.

### 3. Review (prioridad)

Revisar **solo líneas tocadas** (+ contexto mínimo para entender). Criterios (orden):

1. **Correctness** — bugs, edge cases, regresiones, error handling
2. **Security** — secrets, auth, injection, CORS, webhook HMAC
3. **Project rules** — Sheets `503` not `500`, ES modules, `config.*` not hardcoded IDs
4. **Maintainability** — legibilidad, patrones del archivo
5. **Tests** — falta de test cuando el fix es lógica crítica (solo si trivial agregar)

**No reportar** observaciones vagas ("verificar que…") sin bug concreto.

Severidades: `critical` | `high` | `medium` | `low`.

### 4. Fix (Issue and Fix)

Para cada hallazgo **actionable**:

1. Aplicar fix mínimo (StrReplace / edit focal)
2. Un problema por edit cuando sea posible
3. No refactors grandes ni features no pedidas
4. Preguntar antes de: borrar archivos, cambios destructivos, >20 archivos

Límites de seguridad:

- Max **5 iteraciones** review→fix→re-check
- Max **20 archivos** modificados
- Parar si no hay progreso entre iteraciones

### 5. Verify

Tras fixes en `src/` o `server/`:

```bash
npm run lint          # si tocó src/
npm test              # si tocó lógica/helpers
npm run test:api      # si tocó server/routes/
```

Preferir `npm run gate:local` si el cambio es amplio.

Si un gate falla → corregir y reintentar (dentro del límite de iteraciones).

### 6. Report

Entregar resumen en markdown:

```markdown
## Issue & Fix — [branch o uncommitted]

**Diff:** N archivos | **Findings:** N | **Fixed:** N | **Remaining:** N

| Severity | Location | Finding | Status |
|----------|----------|---------|--------|
| high | path:line | … | fixed / skipped / needs human |

### Gates
- lint: pass/fail
- test: pass/fail/skip

### Remaining / human gates
- …
```

No actualizar `PROJECT-STATE.md` salvo que el usuario pida documentar el cambio.

---

## Fix Strategies (BMC)

| Problema | Acción |
|----------|--------|
| Sheet error → 500 | Cambiar a `503` o `200` vacío según contrato |
| Secret/ID hardcoded | Mover a `config.js` / `process.env` |
| ESLint en `src/` | Fix o patrón del archivo |
| Missing import (ESM) | `import` correcto, no `require` |
| SVG inválido (`height="auto"`) | CSS/style, no atributo inválido |
| Test regression | Fix código o test según contrato |

---

## Trigger Terms

fix-only, solo arreglar, bmc issue fix, fix my changes, Bugbot fix (tras hallazgos).

Detalle de severidades: [reference.md](reference.md).
