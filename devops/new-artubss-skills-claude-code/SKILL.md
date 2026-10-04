---
name: railway-new
description: Criar projetos, serviços e bancos de dados no Railway com configuração adequada. Use quando o usuário disser "setup", "deploy to railway", "initialize", "create project", "create service", ou quiser fazer deploy do GitHub. Gerencia setup inicial E adição de serviços a projetos existentes. Para bancos de dados, use a skill railway-railway-database em vez disso.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Project, Service, Setup, Initialize, Deploy, Infrastructure, Scaffolding]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*), Bash(which:*), Bash(command:*), Bash(npm:*), Bash(npx:*)
---

# Novo Projeto / Serviço / Banco de Dados

Criar projetos, serviços e bancos de dados no Railway com configuração adequada.

## Quando Usar

- Usuário diz "deploy to railway" (adicionar serviço se vinculado, inicializar se não)
- Usuário diz "create a railway project", "init", "new project" (novo projeto explícito)
- Usuário diz "link to railway", "connect to railway"
- Usuário diz "create a service", "add a backend", "new api service"
- Usuário diz "create a vite app", "create a react website", "make a python api"
- Usuário diz "deploy from github.com/user/repo", "create service from this repo"
- Usuário diz "add postgres", "add a database", "add redis", "add mysql", "add mongo"
- Usuário diz "connect to postgres", "wire up the database", "connect my api to redis"
- Usuário diz "add postgres and connect to the server"
- Configurando código + serviço Railway juntos

## Pré-requisitos

Verificar CLI instalado:

```bash
command -v railway
```

Se não estiver instalado:

> Instale Railway CLI:
>
> ```
> npm install -g @railway/cli
> ```
>
> ou
>
> ```
> brew install railway
> ```

Verificar autenticação:

```bash
railway whoami --json
```

Se não autenticado:

> Execute `railway login` para autenticar.

## Fluxo de Decisão

```
railway status --json (no diretório atual)
     │
┌────┴────┐
Vinculado Não vinculado
  │            │
  │       Verificar pai: cd .. && railway status --json
  │            │
  │       ┌────┴────┐
  │    Pai         Não vinculado
  │    Vinculado   em nenhum lugar
  │       │            │
  │   Adicionar     railway list
  │   serviço          │
  │   Definir       ┌───┴───┐
  │   rootDir    Corresponde?  Sem correspondência
  │   Deploy           │        │
  │       │        Vincular   Inicializar novo
  └───────┴────────┴────────┘
           │
    Usuário quer serviço?
           │
     ┌─────┴─────┐
    Sim         Não
     │           │
Gerar código   Pronto
     │
railway add --service
     │
Configurar se necessário
     │
Pronto para deploy
```

## Verificar Estado Atual

```bash
railway status --json
```

- **Se vinculado**: Adicionar um serviço ao projeto existente (veja abaixo)
- **Se não vinculado**: Verificar se um diretório PAI está vinculado (veja abaixo)

### Quando Já Vinculado

**Comportamento padrão**: "deploy to railway" = adicionar um serviço ao projeto vinculado.

NÃO criar um novo projeto a menos que o usuário DIGA EXPLICITAMENTE:

- "new project", "create a project", "init a project"
- "separate project", "different project"

Nomes de aplicativos como "flappy-bird" ou "my-api" são nomes de SERVIÇOS, não de projetos.

```
Usuário: "create a vite app called foo and deploy to railway"
Projeto: Já vinculado a "my-project"

ERRADO: railway init -n foo
CORRETO: railway add --service foo
```

### Vinculação de Diretório Pai

Railway CLI percorre a árvore de diretórios para encontrar um projeto vinculado. Se você estiver em um subdiretório:

```bash
cd .. && railway status --json
```

**Se o pai estiver vinculado**, você não precisa inicializar/vincular o subdiretório. Em vez disso:

1. Criar serviço: `railway add --service <name>`
2. Definir `rootDirectory` para o caminho do subdiretório via skill de ambiente
3. Deploy a partir da raiz: `railway up`

**Se nenhum pai estiver vinculado**, prossiga com o fluxo de inicialização ou vinculação.

## Decisão Init vs Link

**Pule esta seção se já estiver vinculado** - apenas adicione um serviço em vez disso.

Use esta seção apenas quando NENHUM projeto estiver vinculado (diretamente ou via pai).

### Verificar Projetos do Usuário

A saída pode ser grande. Execute em um subaagent e extraia apenas:
- `id` e `name` do projeto
- `id` e `name` do workspace

```bash
railway list --json
```

### Lógica de Decisão

1. **Usuário diz explicitamente "new project"** → Use `railway init`
2. **Usuário nomeia um projeto existente** → Use `railway link`
3. **Nome do diretório corresponde a um projeto existente** → Pergunte: vincular existente ou criar novo?
4. **Nenhum projeto correspondente** → Use `railway init`
5. **Ambíguo** → Pergunte ao usuário

## Criar Novo Projeto

```bash
railway init -n <name>
```

Opções:

- `-n, --name` - Nome do projeto (auto-gerado se omitido em modo não-interativo)
- `-w, --workspace` - Nome ou ID do workspace (obrigatório se existirem múltiplos workspaces)

### Múltiplos Workspaces

Se o usuário tiver múltiplos workspaces, `railway init` exigirá a flag `--workspace`.

Obtenha IDs de workspace de:

```bash
railway whoami --json
```

O array `workspaces` contém `{ id, name }` para cada workspace.

**Inferindo workspace da entrada do usuário:**
Se o usuário disser "deploy into xxx workspace" ou "create project in my-team", combine o nome com o array de workspaces e use o ID correspondente:

```bash
# Usuário diz: "create a project in my personal workspace"
railway whoami --json | jq '.workspaces[] | select(.name | test("personal"; "i"))'
# Use o ID correspondente: railway init -n myapp --workspace <matched-id>
```

## Vincular Projeto Existente

```bash
railway link -p <project>
```

Opções:

- `-p, --project` - Nome ou ID do projeto
- `-e, --environment` - Ambiente (padrão: production)
- `-s, --service` - Serviço a vincular
- `-t, --team` - Team/workspace

## Criar Serviço

Após o projeto estar vinculado, crie um serviço:

```bash
railway add --service <name>
```

**Para fontes de repositório GitHub**: Criar um serviço vazio, então invocar a skill railway-environment para configurar a fonte via staged changes API. NÃO use `railway add --repo` - requer integração com app GitHub que frequentemente falha.

Fluxo:

1. `railway add --service my-api`
2. Invocar skill railway-environment para definir `source.repo` e `source.branch`
3. Aplicar mudanças para disparar o deploy

### Configurar Baseado no Tipo de Projeto

Consulte [railpack.md](../reference/railpack.md) para configuração de build.
Consulte [monorepo.md](../reference/monorepo.md) para padrões de monorepo.

**Site estático (Vite, CRA, Astro static):**

- Railpack auto-detecta diretórios de saída comuns (dist, build)
- Se diretório de saída não-padrão: invocar skill railway-environment para definir `RAILPACK_STATIC_FILE_ROOT`
- NÃO use CLI `railway variables` - sempre use a skill de ambiente

**Node.js SSR (Next.js, Nuxt, Express):**

- Verificar se existe script `start` em package.json
- Se start customizado necessário: invocar skill railway-environment para definir `startCommand`

**Python (FastAPI, Django, Flask):**

- Verificar se existe `requirements.txt` ou `pyproject.toml`
- Auto-detectado por Railpack, geralmente sem config necessária

**Go:**

- Verificar se existe `go.mod`
- Auto-detectado, sem config necessária

### Configuração de Monorepo

**Decisão crítica:** Diretório raiz vs comandos customizados.

**Monorepo isolado** (aplicativos não compartilham código):

- Definir Root Directory para o subdiretório do aplicativo (ex: `/frontend`)
- Apenas o código desse diretório está disponível durante o build

**Monorepo compartilhado** (workspaces TypeScript, pacotes compartilhados):

- NÃO definir diretório raiz
- Definir comandos de build/start customizados para filtrar o pacote:
  - pnpm: `pnpm --filter <package> build`
  - npm: `npm run build --workspace=packages/<package>`
  - yarn: `yarn workspace <package> build`
  - Turborepo: `turbo run build --filter=<package>`
- Definir watch paths para prevenir rebuilds desnecessários

Veja [monorepo.md](../reference/monorepo.md) para padrões detalhados.

## Orientação de Setup de Projeto

Analisar a base de código para garantir compatibilidade com Railway.

### Analisar Base de Código

Verificar arquivos de projeto existentes:

- `package.json` → Projeto Node.js
- `requirements.txt`, `pyproject.toml` → Projeto Python
- `go.mod` → Projeto Go
- `Cargo.toml` → Projeto Rust
- `index.html` → Site estático
- Nenhum → Guiar geração de scaffold

**Detecção de monorepo:**

- `pnpm-workspace.yaml` → pnpm workspace (monorepo compartilhado)
- `package.json` com campo `workspaces` → npm/yarn workspace (monorepo compartilhado)
- `turbo.json` → Turborepo (monorepo compartilhado)
- Múltiplos subdiretórios com `package.json` separados mas sem config de workspace → monorepo isolado

### Dicas de Scaffolding

Se não houver código, sugerir padrões mínimos de [railpack.md](../reference/railpack.md):

**Site estático:**

> Criar um arquivo `index.html` no diretório raiz.

**Vite React:**

```bash
npm create vite@latest . -- --template react
```

**Astro:**

```bash
npm create astro@latest
```

**Python FastAPI:**

> Criar `main.py` com aplicativo FastAPI e `requirements.txt` com dependências.

**Go:**

> Criar `main.go` com servidor HTTP ouvindo na variável de ambiente `PORT`.

## Bancos de Dados

Para adicionar bancos de dados (Postgres, Redis, MySQL, MongoDB), use a skill railway-railway-database.

A skill railway-railway-database gerencia:
- Criação de serviços de banco de dados
- Referências de variáveis de conexão
- Vinculação de serviços a bancos de dados

## Composabilidade

- **Após serviço criado**: Use skill railway-deploy para fazer push de código
- **Para config avançada**: Use skill railway-environment (buildCommand, startCommand)
- **Para domínios**: Use skill railway-domain
- **Para verificações de status**: Use skill railway-status
- **Para operações de serviço** (renomear, deletar, status): Use skill railway-service

## Tratamento de Erros

### CLI Não Instalado

```
Railway CLI não instalado. Instale com:
  npm install -g @railway/cli
ou
  brew install railway
```

### Não Autenticado

```
Não logado no Railway. Execute: railway login
```

### Nenhum Workspace

```
Nenhum workspace encontrado. Crie um em railway.com ou verifique autenticação.
```

### Nome de Projeto Já Existe

```
Nome de projeto já existe. Você pode:
- Vincular ao existente: railway link -p <name>
- Usar nome diferente: railway init -n <other-name>
```

### Nome de Serviço Já Existe

```
Nome de serviço já existe neste projeto. Use um nome diferente:
  railway add --service <other-name>
```

## Exemplos

### Criar Site Estático HTML

```
Usuário: "create a simple html site and deploy to railway"

1. Verificar status → não vinculado
2. railway init -n my-site
3. Guiar: criar index.html
4. railway add --service my-site
5. Nenhuma config necessária (index.html na raiz auto-detectado)
6. Usar skill deploy: railway up
7. Usar skill domain para URL pública
```

### Criar Serviço Vite React

```
Usuário: "create a vite react service"

1. Verificar status → vinculado (ou inicializar/vincular primeiro)
2. Scaffold: npm create vite@latest frontend -- --template react
3. railway add --service frontend
4. Nenhuma config necessária (saída Vite dist auto-detectada)
5. Usar skill deploy: railway up
```

### Adicionar API Python ao Projeto

```
Usuário: "add a python api to my project"

1. Verificar status → vinculado
2. Guiar: criar main.py com FastAPI, requirements.txt
3. railway add --service api
4. Nenhuma config necessária (FastAPI auto-detectado)
5. Usar skill deploy
```

### Vincular e Adicionar Serviço

```
Usuário: "connect to my backend project and add a worker service"

1. railway list --json → encontrar "backend"
2. railway link -p backend
3. railway add --service worker
4. Guiar setup baseado no tipo de worker
```

### Deploy para Railway (Ambíguo)

```
Usuário: "deploy to railway"

1. railway status → não vinculado
2. railway list → tem projetos
3. Diretório é "my-app", encontrou projeto "my-app"
4. Perguntar: "Encontrei projeto existente 'my-app'. Vincular a ele ou criar novo?"
5. Usuário: "link"
6. railway link -p my-app
7. Perguntar: "Criar um serviço para este código?"
```

### Adicionar Serviço a Monorepo Isolado

```
Usuário: "create a static site in the frontend directory"

1. Verificar: /frontend tem seu próprio package.json, nenhuma config de workspace
2. Este é monorepo isolado → usar diretório raiz
3. railway add --service frontend
4. Invocar skill de ambiente para definir rootDirectory: /frontend
5. Definir watch paths: /frontend/**
```

### Adicionar Serviço a Monorepo TypeScript

```
Usuário: "add a new api package to this turborepo"

1. Verificar: turbo.json existe, pnpm-workspace.yaml existe
2. Este é monorepo compartilhado → usar comandos customizados, NÃO diretório raiz
3. Guiar: criar packages/api com package.json
4. railway add --service api
5. Invocar skill de ambiente para definir buildCommand e startCommand (NÃO definir rootDirectory)
6. Definir watch paths: /packages/api/**, /packages/shared/**
```

### Deploy de Pacote Existente de Workspace pnpm

```
Usuário: "deploy the backend package to railway"

1. Verificar: pnpm-workspace.yaml existe → monorepo compartilhado
2. railway add --service backend
3. Invocar skill de ambiente para definir buildCommand e startCommand
4. Definir watch paths para backend + deps compartilhadas
```

### Deploy de Subdiretório de Projeto Vinculado

```
Usuário: "create a vite app in my-app directory and deploy to railway"
CWD: ~/projects/my-project/my-app (pai já vinculado a "my-project")

1. Verificar status em my-app → não vinculado
2. Verificar pai: cd .. && railway status → ESTÁ vinculado a "my-project"
3. NÃO inicializar/vincular o subdiretório
4. Scaffold: bun create vite my-app --template react-ts
5. cd my-app && bun install
6. railway add --service my-app
7. Invocar skill de ambiente para definir rootDirectory: /my-app
8. Deploy a partir da raiz: railway up
```