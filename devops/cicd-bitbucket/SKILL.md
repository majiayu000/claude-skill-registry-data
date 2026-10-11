---
name: cicd-bitbucket
description: Bitbucket Pipelines — build, test, and deploy workflows.
---

# Bitbucket Pipelines

## File Location

```
bitbucket-pipelines.yml   ← root of repository
```

## Standard Pipeline

```yaml
image: node:20-alpine

definitions:
  caches:
    npm: ~/.npm
  services:
    postgres:
      image: postgres:16-alpine
      environment:
        POSTGRES_PASSWORD: postgres

pipelines:
  pull-requests:
    '**':
      - step:
          name: Lint & Test
          caches:
            - npm
          services:
            - postgres
          script:
            - npm ci
            - npm run lint
            - npm test
          after-script:
            - pipe: atlassian/junit-annotator:1.0.0

  branches:
    main:
      - step:
          name: Build & Push Image
          services:
            - docker
          script:
            - docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:$BITBUCKET_COMMIT .
            - docker login -u $DOCKER_USER -p $DOCKER_PASSWORD $DOCKER_REGISTRY
            - docker push $DOCKER_REGISTRY/$IMAGE_NAME:$BITBUCKET_COMMIT
      - step:
          name: Deploy
          deployment: production
          script:
            - pipe: atlassian/ssh-run:0.4.1
              variables:
                SSH_USER: $DEPLOY_USER
                SERVER: $DEPLOY_HOST
                SSH_KEY: $DEPLOY_KEY
                COMMAND: >
                  cd /opt/myapp &&
                  IMAGE_TAG=$BITBUCKET_COMMIT docker compose pull app &&
                  IMAGE_TAG=$BITBUCKET_COMMIT docker compose up -d &&
                  docker image prune -f
```

## Secrets & Variables

- Store credentials in **Repository Variables** (Settings → Repository variables)
- Use **Deployment variables** for environment-specific secrets (staging vs production)
- Never hardcode credentials in `bitbucket-pipelines.yml`
- Prefix sensitive variables to keep them organized: `DEPLOY_*`, `DOCKER_*`, `DB_*`

## Parallel Steps

```yaml
- parallel:
    - step:
        name: Unit Tests
        script:
          - npm run test:unit
    - step:
        name: Lint
        script:
          - npm run lint
    - step:
        name: Type Check
        script:
          - npm run typecheck
```

## Manual Trigger / Approval Gate

```yaml
- step:
    name: Deploy to Production
    trigger: manual
    deployment: production
    script:
      - echo "Deploying..."
```

## Best Practices

- Use `definitions.caches` for dependency caches — speeds up builds significantly
- Use `definitions.services` for databases/redis instead of setting up in scripts
- Use `deployment: staging` / `deployment: production` to track deploys in Bitbucket
- Add `fail-fast: false` to parallel steps if you want all to run even if one fails
- Use `after-script` for test report uploads — runs even on failure
