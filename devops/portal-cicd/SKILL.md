---
name: portal-cicd
description: Build and maintain the CI/CD pipeline for the Portal Centralizado de Datos Financieros — GitHub Actions (ci.yml lint+test, deploy.yml build+migrate+deploy to Cloud Run), Docker Compose local, Makefile targets, and multi-stage Dockerfiles. Use when editing .github/workflows/, docker-compose.yml, Makefile, or Dockerfiles.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal CI/CD Skill

## Rules — NON-NEGOTIABLE

- Cada push dispara lint (ruff + eslint) y pruebas (pytest + Vue Test Utils) con caché de lockfiles Poetry/pnpm. Matriz back/front.
- Merge a `main` dispara: build Docker → push a Artifact Registry → `dbmate up` contra la BD del entorno → deploy Cloud Run. Las migraciones SIEMPRE antes del deploy.
- Secretos del pipeline en GitHub Environments, jamás en el repo ni en el workflow.
- Dependencias SOLO vía lockfiles commiteados (`poetry.lock`, `pnpm-lock.yaml`); pnpm fijado con `packageManager` (Corepack).
- Dockerfiles multi-stage: FastAPI via `poetry export` → imagen slim sin Poetry; Nuxt con capa `pnpm fetch` para caché.
- Sin emojis en nombres de jobs, steps ni logs de CI.

## ci.yml — lint + test en cada push

```yaml
# .github/workflows/ci.yml
name: ci
on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12", cache: "poetry" }
      - run: pipx install poetry && poetry install --with dev,test
        working-directory: backend
      - run: poetry run ruff check . && poetry run ruff format --check .
        working-directory: backend
      - run: poetry run pytest --cov=app --cov-fail-under=70
        working-directory: backend

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: "pnpm", cache-dependency-path: frontend/pnpm-lock.yaml }
      - run: pnpm install --frozen-lockfile && pnpm lint && pnpm test
        working-directory: frontend
```

## deploy.yml — merge a main

```yaml
# .github/workflows/deploy.yml
name: deploy
on:
  push: { branches: [main] }

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production        # secretos viven aqui
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with: { credentials_json: "${{ secrets.GCP_DEPLOY_SA_KEY }}" }
      - run: |
          gcloud auth configure-docker ${REGION}-docker.pkg.dev
          docker build -t "$BACKEND_IMAGE" backend/ && docker push "$BACKEND_IMAGE"
          docker build -t "$FRONTEND_IMAGE" frontend/ && docker push "$FRONTEND_IMAGE"
      - run: dbmate --url "${{ secrets.DATABASE_URL }}" up      # migrar ANTES de deploy
      - run: |
          gcloud run deploy portal-backend --image "$BACKEND_IMAGE" --region "$REGION"
          gcloud run deploy portal-frontend --image "$FRONTEND_IMAGE" --region "$REGION"
```

## Dockerfiles multi-stage

```dockerfile
# backend/Dockerfile — poetry export → slim
FROM python:3.12-slim AS builder
RUN pip install poetry poetry-plugin-export
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

FROM python:3.12-slim
COPY --from=builder requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

```dockerfile
# frontend/Dockerfile — pnpm fetch como capa de cache
FROM node:22-slim AS builder
RUN corepack enable
COPY pnpm-lock.yaml ./
RUN pnpm fetch                    # cache aunque cambie el codigo
COPY . .
RUN pnpm install --offline --frozen-lockfile && pnpm build

FROM node:22-slim
COPY --from=builder /.output /.output
CMD ["node", "/.output/server/index.mjs"]
```

## Makefile y Compose local

| Target | Acción |
|--------|--------|
| `make dev` | Docker Compose: FastAPI + Nuxt 4 + PostgreSQL, red bridge, volúmenes de código |
| `make test` | pytest backend/ml + vitest frontend |
| `make lint` | ruff + mypy + pnpm lint |
| `make check` | lint + secrets-scan — OBLIGATORIO antes de PR |
| `make data` | genera silos sintéticos con semilla fija |
| `make db-new SLUG=x` / `db-up` / `db-rollback` | wrappers de dbmate |

## QA Checklist

- [ ] Caché de lockfiles activa (setup-python `cache: poetry`, setup-node `cache: pnpm`)
- [ ] Cobertura gates en CI (≥70% backend)
- [ ] `dbmate up` como paso previo al deploy en deploy.yml
- [ ] Secretos solo en GitHub Environments
- [ ] Imágenes multi-stage (sin Poetry/devDeps en runtime)
- [ ] `make dev` reproducible en las 3 máquinas (gate vie 24-jul)
