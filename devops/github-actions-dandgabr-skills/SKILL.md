---
name: program-github-actions
description: "Especialista na Plataforma GitHub, GitHub Actions e CI/CD. Cobre governança de repositórios, regras de proteção (Rulesets), CODEOWNERS, fluxos de Pull Request, automação com GitHub CLI (gh), segurança com GHAS (Dependabot, CodeQL, Secret Scanning), GitHub Packages (ghcr.io), GitHub Codespaces, e engenharia completa de workflows YAML (reusable workflows, composite actions, matrix strategies, concurrency, environments protegidos, autenticação OIDC e caching)."
---

# Plataforma GitHub, Governança & GitHub Actions CI/CD

Esta skill orienta a inteligência artificial a atuar como **Especialista Sênior na Plataforma GitHub e Engenharia de CI/CD com GitHub Actions**, abrangendo governança de repositórios, segurança avançada de código (GHAS), automação com o GitHub CLI (`gh`) e design de pipelines de integração e entrega contínuas resilientes.

---

## 🌿 1. Governança e Estrutura de Repositórios

### 1.1 Estratégias de Branching
- **GitHub Flow**: Branch `main` sempre estável e pronta para deploy; feature branches curtas com merge via Pull Request após validação de CI e aprovação de revisores.
- **Trunk-Based Development**: Commits diretos na `main` ou feature branches com ciclo de vida inferior a 24 horas, acompanhadas de *feature flags*.
- **GitFlow**: Estrutura com `main`, `develop`, `release/*`, `feature/*` e `hotfix/*` para ciclos formais de release com versionamento semântico.

### 1.2 Repository Rulesets e CODEOWNERS
- **Branch Protection & Rulesets**:
  - Exigência de Pull Request com no mínimo 1 aprovação obrigatória.
  - Bloqueio de merges quando status checks de CI estiverem falhando.
  - Exigência de commits assinados via chave GPG ou SSH.
  - Bloqueio estrito de force pushes (`git push --force`).
- **`.github/CODEOWNERS`**:
```ini
# Fallback global
* @org-core-team

# Infraestrutura e CI/CD
.github/workflows/ @org-devops-team
terraform/ @org-devops-team

# Backend e Segurança
src/backend/ @org-backend-leads
src/backend/auth/ @org-security-team
```

---

## ⚙️ 2. GitHub Actions: Anatomia de Workflows e Padrões

### 2.1 Workflow de CI/CD Seguro com Permissões Mínimas
```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
    paths-ignore: ['docs/**', '*.md']
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: write
  security-events: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Tests with Pytest
        run: pytest --cov=src --cov-report=xml

      - name: Run Snyk Code SAST
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### 2.2 Reusable Workflows (`workflow_call`)
```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy application
        run: ./deploy.sh --env ${{ inputs.environment }}
        env:
          KEY: ${{ secrets.DEPLOY_KEY }}
```

### 2.3 Autenticação OIDC com Provedores Cloud (AWS / GCP / Azure)
Elimine credenciais estáticas de longa duração em `secrets`:
```yaml
jobs:
  deploy-aws:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsDeployRole
          aws-region: us-east-1
```

---

## 🔒 3. GitHub Advanced Security (GHAS)

1. **Dependabot**:
   - `dependabot.yml` configurado para atualizações diárias de segurança e checagem de vulnerabilidades em dependências.
2. **CodeQL (SAST)**:
   - Análise estática profunda de código-fonte integrada à aba *Security > Code scanning*.
3. **Secret Scanning & Push Protection**:
   - Bloqueio imediato de commits contendo chaves de API, tokens privados ou credenciais no momento do push.

---

## 💻 4. Automação com GitHub CLI (`gh`)

```bash
# Autenticação e status
gh auth status
gh repo view --json name,description,defaultBranchRef

# Gerenciamento de Pull Requests
gh pr create --title "feat: novo endpoint de pagamentos" --body "Implementa RFC 10008" --reviewer "org-core-team"
gh pr review 123 --approve --body "LGTM!"
gh pr merge 123 --squash --delete-branch

# Disparo e inspeção de Workflows
gh workflow run ci.yml --ref main -f environment=staging
gh run list --workflow=ci.yml --limit 5
gh run watch
gh run view --log-failed
```

---

## 📦 5. GitHub Packages (ghcr.io) e Codespaces

- **GitHub Container Registry (`ghcr.io`)**: Autenticação nativa com `GITHUB_TOKEN`, publicação e versionamento de imagens OCI com tags de commit SHA e semver.
- **GitHub Codespaces**: Configuração com `.devcontainer/devcontainer.json` para ambientes de desenvolvimento reprodutíveis e pré-configurados em segundos.
