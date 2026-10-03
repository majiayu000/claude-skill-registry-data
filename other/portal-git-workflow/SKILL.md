---
name: portal-git-workflow
description: Manage branches (feature/E{epic}-US-XXX-{slug}), Conventional Commits with epic scope, PRs to develop, and User Story closure for the Portal Centralizado de Datos Financieros. Use when committing, creating branches, opening PRs, or closing a US.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Git Workflow Skill

## Rules — NON-NEGOTIABLE

- Rama por User Story: `feature/E{epic}-US-XXX-{slug}` — épicas válidas: `UX`, `E0`, `E1`, `E2`, `E3`, `E4`, `E5`.
- Conventional Commits con scope de épica: `feat(E2): ...`, `fix(E3): ...`, `docs(UX): ...`.
- Commits SIN trailer `Co-Authored-By` de asistentes IA — la autoría queda en el `Author:` real.
- Sin emojis en mensajes de commit ni descripciones de PR.
- PR siempre a `develop` con `make check` limpio ANTES de abrirlo. Merge a `main` = deploy automático a Cloud Run (skill `portal-cicd`) — solo cuando el equipo decide desplegar.
- Cerrar una US exige criterios de aceptación verificados y referencia a las US absorbidas que cubre.

## Branches

- `main` — protegido; merge aquí dispara build + `dbmate up` + deploy a Cloud Run.
- `develop` — integración continua; target de todos los PRs de features.
- `feature/E{epic}-US-XXX-{slug}` — una rama por US del plan.
- `hotfix/{slug}` — solo fixes urgentes sobre `main`; cherry-pick de vuelta a `develop`.

## Conventional Commits con scope de épica

```
feat(E0): add docker compose with backend, frontend and postgres services
feat(E2): implement semantic query compiler with catalog validation
fix(E3): cancel LLM call on SSE client disconnect
feat(E2): add user CRUD endpoints with admin scope
docs(UX): add journey maps evidence for A2 deliverable
test(E5): add TTFT measurement script with percentile report
chore(E0): pin pnpm version via packageManager field
ci(E0): add dbmate migration step before cloud run deploy
```

| Tipo | Cuándo |
|------|--------|
| feat | nueva funcionalidad de una US |
| fix | corrección de bug |
| docs | documentación y entregables (`docs(UX):` para A1–A5) |
| test | añadir/corregir pruebas |
| refactor | sin cambio de comportamiento |
| perf | mejora de rendimiento (ECharts, Polars) |
| chore | mantenimiento, dependencias |
| ci | pipelines y workflows |

## Flujo por User Story

```bash
# Inicio — partir SIEMPRE de develop actualizado
git checkout develop && git pull
# XXX = numero de la US segun context/planeacion_proyecto.md
git checkout -b feature/E2-US-XXX-jwt-rbac

# Trabajo iterativo: commits atomicos con scope de epica
git add backend/app/core/auth.py
git commit -m "feat(E2): add pwdlib password hashing with dummy-hash timing guard"

git add db/migrations/20260728000000_create_app_user.sql db/schema.sql
git commit -m "feat(E2): add app_user migration and seed with argon2 passwords"

# Pre-PR: gate obligatorio
make check && make test

# Push y PR a develop (NUNCA directo a main)
git push -u origin feature/E2-US-XXX-jwt-rbac
gh pr create --base develop --title "feat(E2): US-XXX JWT auth and RBAC" \
  --body "## US-XXX — Autenticacion JWT y RBAC

Criterios de aceptacion verificados:
- [x] OAuth2 password flow con PyJWT HS256 + pwdlib argon2id
- [x] Scopes por rol; 401/403 verificados por matriz de pruebas
- [x] Seed de 7 usuarios via migracion dbmate

Si absorbe US del backlog consolidado (plan §18), citarlas aqui."

# Tras aprobacion y CI verde
gh pr merge --squash
git checkout develop && git pull
git branch -d feature/E2-US-XXX-jwt-rbac
```

## Cierre de US

1. PR mergeado a `develop` con CI verde.
2. Criterios de aceptación de la US verificados uno a uno contra `context/planeacion_proyecto.md`.
3. Referenciar US absorbidas en el PR/cierre para trazabilidad con el backlog original (backlog consolidado, plan §18).
4. Si la US ejecutó una degradación acordada (§10.2: CRUD de usuarios reducido, ECharts a 500 K), documentarla en el cierre.
5. Marcar la US como completada en el tracking del equipo.

## Merge a main = deploy

```bash
# Solo cuando el equipo decide desplegar (fin de sprint o demo)
gh pr create --base main --head develop --title "release: sprint S2 increment"
# El merge dispara deploy.yml: build -> Artifact Registry -> dbmate up -> Cloud Run
# Post-merge: verificar smoke tests verdes en Actions (skill portal-testing)
```

## QA Checklist

- [ ] Rama sigue `feature/E{epic}-US-XXX-{slug}` con épica válida (UX, E0–E5)
- [ ] Commits con Conventional Commits + scope de épica
- [ ] Sin trailer `Co-Authored-By` de IA ni emojis
- [ ] `make check` limpio antes de abrir el PR
- [ ] PR target `develop` (main solo para releases/deploy)
- [ ] PR referencia la US y sus US absorbidas
- [ ] Criterios de aceptación verificados al cierre
- [ ] CI verde antes de merge; smoke tests verdes tras deploy a main
