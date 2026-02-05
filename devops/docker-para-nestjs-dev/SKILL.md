---
name: "Docker para NestJS (Dev)"
description: "Cria e configura um ambiente de desenvolvimento Docker para NestJS com hot-reload, Dev Containers, e zero dependências no host."
version: "4.0.0"
---

# Skill: Docker para Desenvolvimento NestJS

## 1. Objetivo

Analisar e configurar um ambiente de desenvolvimento local para NestJS usando Docker, garantindo que o ecossistema funcione **sem dependências no host** (como Node.js ou `node_modules` locais). Opcionalmente, configurar suporte para VS Code Dev Containers.

## 2. Quando usar

Use esta skill quando o usuário pedir para:
- Configurar Docker para um projeto NestJS do zero.
- Corrigir um ambiente Docker existente que depende de `npm install` local.
- Criar um ambiente de desenvolvimento que "só precise do Docker".
- Resolver problemas de hot-reload, volumes, ou permissões (EACCES) em Docker com NestJS.
- Configurar VS Code para desenvolver dentro do container (Dev Containers).

**NÃO use para:** Ambientes de produção ou deploy.

## 3. Fluxo de Execução

### Passo 1: Analisar e Corrigir Configuração Existente
- **Verifique os `Dockerfile`s:** Procure por `volumes` que montam `node_modules` do host (ex: `- ./node_modules:/app/node_modules`). **Isto é um erro e deve ser removido.**
- **Verifique scripts de inicialização:** Confirme que `npm install` ou `npm ci` é executado **dentro** do contêiner, seja no `command` do `docker-compose.yml` ou em um script de entrypoint.
- **Verifique a documentação do projeto:** Procure por instruções que peçam para rodar `npm install` no host antes de subir o Docker. Se encontrar, informe que o objetivo é remover essa dependência.

### Passo 2: Criar o `.dockerignore`
Se não existir, crie um arquivo `.dockerignore` na raiz para minimizar o contexto de build.

```
# Git
.git
.github
.gitignore

# Node
node_modules
npm-debug.log*
dist
build

# Docker
Dockerfile*
docker-compose*.yml

# Outros
.DS_Store
.env
*.md
.devcontainer
```

### Passo 3: Criar/Ajustar o `Dockerfile`
Garanta que o `Dockerfile` da API NestJS segue este padrão.

**IMPORTANTE:** Em desenvolvimento, **NÃO** use `USER node`. Execute como `root` para evitar problemas de permissão com volumes.

```dockerfile
FROM node:22-alpine

RUN npm install -g @nestjs/cli
WORKDIR /home/node/app

# Mantém o container ativo para `docker-compose exec` e hot-reload
CMD ["tail", "-f", "/dev/null"]
```

### Passo 4: Criar/Ajustar o `docker-compose.yml`
Crie ou modifique o `docker-compose.yml` principal.

**PRINCÍPIOS-CHAVE:**
1.  **NÃO montar `node_modules` do host.**
2.  **Usar volume anônimo para `node_modules`**: Essencial para performance e para evitar erros `ENOTEMPTY`.
3.  **`healthcheck` no banco de dados**: Garante que a API só inicie quando o banco estiver pronto.
4.  **`command` com `npm install`**: Garante que as dependências sejam instaladas no contêiner.

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: nestjs-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-meudb}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U postgres']
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: nestjs-api
    command: sh -c "npm install && npm run start:dev"
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      NODE_ENV: development
      DATABASE_URL: "postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-postgres}@postgres:5432/${POSTGRES_DB:-meudb}?schema=public"
    ports:
      - '3001:3001'
      - '9229:9229'
    volumes:
      - .:/home/node/app:cached
      - /home/node/app/node_modules

volumes:
  postgres_data:
    driver: local
```

### Passo 5: Criar o script de inicialização `scripts/init.sh`
Crie o arquivo `scripts/init.sh` (se ainda não existir) e torne-o executável (`chmod +x scripts/init.sh`). Este script pode orquestrar tarefas mais complexas como migrations e seeds. Use o arquivo já existente na skill.

### Passo 6: (Opcional) Configurar para VS Code Dev Containers
Se o usuário utiliza VS Code, crie a seguinte estrutura de arquivos:

**1. Crie `.devcontainer/devcontainer.json`:**
```json
{
  "name": "NestJS Dev Container",
  "dockerComposeFile": [
    "../docker-compose.yml"
  ],
  "service": "api",
  "workspaceFolder": "/home/node/app",
  "features": {
    "ghcr.io/devcontainers/features/common-utils:2": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "firsttris.vscode-jest-runner"
      ]
    }
  },
  "postCreateCommand": "echo 'Container is ready!'"
}
```

**2. Informe o usuário sobre o uso:**
- "Para usar, instale a extensão 'Dev Containers' da Microsoft no VS Code."
- "Abra o projeto e clique no pop-up 'Reopen in Container' ou abra a paleta de comandos (Cmd+Shift+P) e selecione 'Dev Containers: Reopen in Container'."
- "Isso reabrirá o VS Code diretamente dentro do contêiner `api`, com terminal e ferramentas já configuradas."

### Passo 7: Adicionar scripts ao `package.json`
Adicione comandos ao `package.json` para facilitar o gerenciamento.
```json
"scripts": {
  "dev:init": "bash scripts/init.sh",
  "dev": "docker-compose up -d",
  "dev:stop": "docker-compose down",
  "dev:logs": "docker-compose logs -f api"
}
```

### Passo 8: Checklist de Validação Final
Ao final, verifique os seguintes pontos:
- [ ] O `Dockerfile` **não** contém `USER node`.
- [ ] O `docker-compose.yml` **não** monta o `node_modules` do host.
- [ ] O serviço da `api` tem um volume anônimo para `node_modules`.
- [ ] O comando de start executa `npm install` e `npm run start:dev` (ou similar com watch).
- [ ] O ambiente sobe com `docker-compose up --build` sem precisar de `npm install` no host.
- [ ] A edição de um arquivo `.ts` dispara o hot-reload nos logs do contêiner.
- [ ] (Se aplicável) O projeto abre corretamente no Dev Container.
