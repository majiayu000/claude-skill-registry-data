---
description: Execute CD workflows on GitHub Actions to deploy backend/frontend
---

# Deploy (Continuous Deployment)

Execute backend (ECS Fargate) and frontend (AWS Amplify) CD workflows on GitHub Actions to deploy.

## Steps

### 1. Check current state

```bash
git branch --show-current
git log --oneline -5
```

### 2. Determine target environment

Auto-detection based on branch:

| Branch | Environment | Backend CD | Frontend CD |
|--------|-------------|-----------|-------------|
| `develop` | dev | Automatic on push | Manual only |
| `release/*` | stg | Automatic on push | Automatic on push |
| `main` | prod | Automatic on push | Manual only |

### 3. Select deployment target

Confirm with the user:
- **Target**: backend / frontend / both
- **Environment**: dev / stg / prod

### 4. Execute deployment

```bash
# Deploy via dev script
dev/deploy backend dev        # Deploy backend to dev
dev/deploy frontend stg       # Deploy frontend to stg
dev/deploy both dev           # Deploy both to dev
```

**Backend CD flow:**
1. Build Docker image
2. Push to Amazon ECR (tags: `latest` + `<commit-sha>`)
3. Update ECS task definition
4. Deploy ECS service (wait for service stability)
5. On failure, auto-rollback to previous task definition

**Frontend CD flow:**
1. Set up Amplify branch (create if not exists)
2. Trigger Amplify deploy job
3. Wait for deployment completion (up to 30 minutes)
4. Check status (SUCCEED / FAILED / CANCELLED)

### 6. Monitor deployment status

```bash
# Check backend deployment progress
gh run view <run-id> --log

# Check frontend deployment progress
gh run view <run-id> --log
```

### 7. Post-deployment verification

```bash
# Backend health check
curl -s https://api.<env>.legal-ai-reception.click/health

# Verify deployed image
gh run view <run-id> --json jobs --jq '.jobs[] | {name, conclusion}'
```

### 8. Handle deployment failure

```bash
# Check failure logs
gh run view <run-id> --log-failed

# Backend: ECS rollback is automatic
# Frontend: To rollback Amplify, a re-deploy of the previous version is needed
```

## Notes

- **Always obtain explicit user approval before prod deployment**
- Backend deployment failure triggers automatic rollback to the previous task definition
- Frontend Amplify deployment can take up to 30 minutes
- Manual `workflow_dispatch` requires `--ref` to specify the target branch
- Verify that all corresponding CI checks have passed before deploying

## Language

- **All user-facing output, reports, and summaries must be written in Japanese(すべてのユーザーへの出力は日本語にしてください)**
