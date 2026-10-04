---
name: issue-and-fix
description: >
  Orchestrates local Agent Review Issue and Fix: Bugbot review (optional),
  bmc-issue-fix-reviewer fixes, optional security-review, expert-debug cleanup,
  and gate:local. Use when user says /issue-and-fix, issue and fix, revisar y
  arreglar, agent review local, or Cursor Agent Review insufficient funds.
---

# Issue and Fix — Orchestrator

Skill de **entrada** que llama en orden las capacidades de revisión y corrección del repo. Reemplaza el botón **Agent Review → Issue and Fix** de Cursor cuando falla por `insufficient funds`.

**Componentes que orquesta:**

| Paso | Función | Skill / subagent |
|------|---------|------------------|
| 1 | Revisión readonly (bugs) | `review-bugbot` → subagent `bugbot` |
| 2 | Revisar + **corregir** diff | `bmc-issue-fix-reviewer` |
| 3 | Seguridad (si aplica) | `review-security` → subagent `security-review` |
| 4 | Linter/tests residuales | `expert-debug-autonomous` |
| 5 | Gate local | `npm run gate:local` |

---

## When to Use

- `/issue-and-fix` o **issue and fix**
- **revisar y arreglar**, **review and fix**
- `Failed to run review: insufficient funds`
- Antes de commit/PR con corrección automática

---

## Modes

| Mode | Pasos | Cuándo |
|------|-------|--------|
| `full` (default) | 1 → 2 → 5 (+ 3 si auth, + 4 si gates fallan) | Flujo completo tipo Agent Review |
| `fix-only` | 2 → 5 (+ 4 si falla) | Ya revisaste; solo arreglar |
| `review-only` | 1 | Igual que `/review-bugbot` |
| `security` | 3 → 2 (solo critical/high) → 5 | Security **siempre** en paso 3; luego fix |

Si el usuario no especifica modo → `full`.

**Diff scope** (igual que issue-fix-reviewer):

- `branch` (default) → `branch changes`
- `uncommitted` → `uncommitted changes`
- `files` → pasar lista al paso 2 con `files` mode

---

## Step 0 — Repo y scope

1. `cd` al repo git activo (default: `/Users/matias/calculadora-bmc`).
2. Determinar si hay trabajo a revisar (no usar solo `git status` vacío como corte):
   - **`branch`:** `git merge-base HEAD main` (o `master`) + `git diff <base>...HEAD` + `git diff` + `git diff --cached`. Commits en la rama sin dirty tree **sí** cuentan.
   - **`uncommitted`:** `git diff`, `git diff --cached`, y paths `??` en `git status` (untracked).
   - Parar solo si no hay diff ni untracked relevantes.
3. Anotar: repo path absoluto, pipeline mode, diff scope.

---

## Step 1 — Bugbot (skip si `fix-only` o `security`)

Seguir **verbatim** `~/.cursor/skills-cursor/review-bugbot/SKILL.md` (skill Cursor; no está bajo el repo).

Resumen de invocación:

```text
Task:
  subagent_type: bugbot
  readonly: true
  run_in_background: false
  description: Bugbot

Prompt:
  Full Repository Path: <absolute path>
  Diff: branch changes | uncommitted changes
  [Custom Instructions: priorizar hallazgos en ...]  # solo si el usuario pidió foco
```

Guardar hallazgos (tabla Severity | Location | Finding) para el paso 2.

Si diff vacío → parar pipeline, informar usuario.

---

## Step 2 — Issue & Fix (corrección)

Ejecutar **completo** `.cursor/skills/bmc-issue-fix-reviewer/SKILL.md`:

1. Cargar `AGENTS.md`, `.cursor/rules/`, diff según scope.
2. Si hubo Bugbot en paso 1 → tratar sus hallazgos como **prioridad alta** (fix primero).
3. Revisar diff + aplicar fixes (max 5 iteraciones, 20 archivos).
4. `npm run lint` / `npm test` / `npm run test:api` según archivos tocados.

**No** lanzar otro subagente para este paso — el agente padre ejecuta la skill directamente (como `ceo-ai-agent`).

---

## Step 3 — Security (condicional)

En pipeline mode **`security`**, ejecutar **siempre** (sin depender de globs de path).

En mode **`full`**, ejecutar solo si el diff toca alguno de:

- `server/routes/auth*`, `server/middleware/requireAuth*`, `server/tokenStore*`
- `server/config.js`, `.env.example`, webhooks, `server/routes/shopify*`
- OAuth, CORS, HMAC, credenciales

Seguir `~/.cursor/skills-cursor/review-security/SKILL.md`:

```text
Task:
  subagent_type: security-review
  readonly: true
  description: Security Review

Prompt:
  Full Repository Path: <absolute path>
  Diff: branch changes | uncommitted changes
```

Si hay hallazgos **critical** o **high** → una pasada extra del paso 2 solo para esos ítems (max 1 iteración).

---

## Step 4 — Expert debug (condicional)

Ejecutar solo si tras paso 2/3:

- `npm run lint` o `npm test` sigue fallando, o
- `ReadLints` muestra errores en archivos modificados

Seguir `.cursor/skills/expert-debug-autonomous/SKILL.md` (max 5 iteraciones, 20 archivos).

---

## Step 5 — Gate local

Si se modificó `src/` o `server/`:

```bash
cd <repo>
npm run gate:local
```

Si falla → paso 4 una vez más; si sigue fallando → reportar remaining.

---

## Step 6 — Reporte combinado

```markdown
## Issue and Fix — [mode] / [scope]

| Phase | Result |
|-------|--------|
| Bugbot | N findings / skipped |
| Issue-Fix | N fixed, N remaining |
| Security | N findings / skipped |
| Expert debug | N fixed / skipped |
| gate:local | pass / fail |

### Findings (fixed)
| Severity | Location | Finding | Status |

### Remaining / human
- …
```

No commit/push salvo petición explícita. No actualizar `PROJECT-STATE.md` salvo petición.

---

## Errores frecuentes

| Error | Acción |
|-------|--------|
| `insufficient funds` (Agent Review Cursor) | Usar esta skill — no reintentar Agent Review |
| Subagent falla | Reintentar 1× con forma correcta; luego continuar pipeline sin ese paso |
| Diff vacío | Parar con mensaje claro |
| Checkout bloqueado | Preguntar stash; no stash sin confirmación |

---

## Trigger Terms

/issue-and-fix, issue and fix, revisar y arreglar, review and fix, agent review local, insufficient funds, orchestrate issue fix.

**Procedimiento humano (checklist pre-PR):** [`docs/team/PROCEDIMIENTO-PRE-PR-LOCAL.md`](../../docs/team/PROCEDIMIENTO-PRE-PR-LOCAL.md)

Detalle de pipeline: [reference.md](reference.md).
