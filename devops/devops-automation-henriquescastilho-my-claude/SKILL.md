---
name: devops-automation
description: Automacao de CI/CD, infraestrutura como codigo, containers, monitoramento. Usar automaticamente quando o contexto envolve pipelines, deploy, Docker, Kubernetes, GitHub Actions, ou infraestrutura.
---

# DevOps e Automacao -- Padrao DME

## Capacidades

- CI/CD: GitHub Actions (principal), GitLab CI
- Infraestrutura: Docker, Docker Compose
- Deploy: Railway, GCP Cloud Run, Vercel
- Monitoramento: logs estruturados, health checks
- Seguranca: scanning de dependencias, SAST basico

## Checklist de CI/CD local (GitHub Actions esgotado)

1. Lint + type-check antes de commit
2. Build local antes de push
3. Testes automatizados antes de merge
4. Security scan de dependencias

## Dockerfile padrao

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Regras DME

- Sempre multi-stage build pra imagens Docker
- Nunca rodar como root no container
- Health check endpoint obrigatorio (/health)
- Logs em JSON estruturado
- Secrets via env vars, nunca no Dockerfile
