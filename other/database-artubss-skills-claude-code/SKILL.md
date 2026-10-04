---
name: railway-database
description: Adicionar serviços oficiais de banco de dados Railway (Postgres, Redis, MySQL, MongoDB). Use quando o usuário quer adicionar um banco de dados, diz "adicionar postgres", "adicionar redis", "adicionar banco de dados", "conectar ao banco de dados" ou "configurar o banco de dados". Para outros templates (Ghost, Strapi, n8n), use a skill railway-templates.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Database, Postgres, Redis, MySQL, MongoDB, Infrastructure, Deployment, Template]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Railway Database

Adicione serviços oficiais de banco de dados Railway. Estes são templates mantidos com volumes pré-configurados, networking e variáveis de conexão.

Para templates que não são de banco de dados, consulte a skill `railway-templates`.

## Quando Usar

- Usuário pede para "adicionar um banco de dados", "adicionar Postgres", "adicionar Redis", etc.
- Usuário precisa de um banco de dados para sua aplicação
- Usuário pergunta sobre conectar a um banco de dados
- Usuário diz "adicionar postgres e conectar ao meu servidor"
- Usuário diz "configurar o banco de dados"

## Fluxo de Decisão

**SEMPRE verifique bancos de dados existentes ANTES de criar.**

```
Usuário menciona banco de dados
        │
  Verificar BDs existentes
  (consultar config de env por source.image)
        │
   ┌────┴────┐
Existe    Não existe
    │           │
    │      Criar banco de dados
    │      (CLI ou API)
    │           │
    │      Aguardar deploy
    │           │
    └─────┬─────┘
          │
    Usuário quer
    conectar serviço?
          │
    ┌─────┴─────┐
   Sim        Não
    │           │
Conectar vars  Pronto +
via env        sugerir
skill          conectar
```

## Verificar Bancos de Dados Existentes

Antes de criar um banco de dados, verifique se já existe um.

Para a estrutura completa do config de ambiente, veja [environment-config.md](../reference/environment-config.md).

```bash
railway status --json
```

Então consulte o config do ambiente e verifique `source.image` para cada serviço:

```graphql
query environmentConfig($environmentId: String!) {
  environment(id: $environmentId) {
    config(decryptVariables: false)
  }
}
```

O objeto `config.services` contém a configuração de cada serviço. Verifique `source.image` para:

- `ghcr.io/railway/postgres*` ou `postgres:*` → Postgres
- `ghcr.io/railway/redis*` ou `redis:*` → Redis
- `ghcr.io/railway/mysql*` ou `mysql:*` → MySQL
- `ghcr.io/railway/mongo*` ou `mongo:*` → MongoDB

## Bancos de Dados Disponíveis

| Banco de Dados | Código do Template |
|---|---|
| PostgreSQL | `postgres` |
| Redis | `redis` |
| MySQL | `mysql` |
| MongoDB | `mongodb` |

## Pré-requisitos

Obtenha contexto do projeto:
```bash
railway status --json
```

Extraia:
- `id` - ID do projeto
- `environments.edges[0].node.id` - ID do ambiente

Obtenha ID do workspace (não está na saída de status):
```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query getWorkspace($projectId: String!) {
    project(id: $projectId) { workspaceId }
  }' \
  '{"projectId": "PROJECT_ID"}'
SCRIPT
```

## Adicionar um Banco de Dados

### Passo 1: Buscar Template

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query template($code: String!) {
    template(code: $code) {
      id
      name
      serializedConfig
    }
  }' \
  '{"code": "postgres"}'
SCRIPT
```

Isso retorna o `id` e `serializedConfig` do template necessários para o deploy.

### Passo 2: Fazer Deploy do Template

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation deployTemplate($input: TemplateDeployV2Input!) {
    templateDeployV2(input: $input) {
      projectId
      workflowId
    }
  }' \
  '{
    "input": {
      "templateId": "TEMPLATE_ID",
      "serializedConfig": SERIALIZED_CONFIG,
      "projectId": "PROJECT_ID",
      "environmentId": "ENVIRONMENT_ID",
      "workspaceId": "WORKSPACE_ID"
    }
  }'
SCRIPT
```

**Importante:** `serializedConfig` é o objeto exato da consulta de template, não uma string.

## Conectar ao Banco de Dados

Após o deploy, outros serviços se conectam usando variáveis de referência.

Para a sintaxe de referência de variáveis completa e padrões de conexão, veja [variables.md](../reference/variables.md).

### Serviços Backend (Lado do Servidor)

Use a URL privada/interna para comunicação entre servidores:

| Banco de Dados | Referência de Variável |
|---|---|
| PostgreSQL | `${{Postgres.DATABASE_URL}}` |
| Redis | `${{Redis.REDIS_URL}}` |
| MySQL | `${{MySQL.MYSQL_URL}}` |
| MongoDB | `${{MongoDB.MONGO_URL}}` |

### Aplicações Frontend

**Importante:** Frontends rodam no navegador do usuário e não conseguem acessar a rede privada do Railway. Devem usar URLs públicas ou passar por uma API backend.

Para acesso direto ao banco de dados pelo frontend (não recomendado):
- Use as variáveis de URL pública (ex: `${{MongoDB.MONGO_PUBLIC_URL}}`)
- Requer TCP proxy habilitado

Padrão melhor: Frontend → API Backend → Banco de Dados

## Exemplo: Adicionar PostgreSQL

```bash
bash <<'SCRIPT'
# 1. Obter contexto
railway status --json
# Extrair project.id e environment.id

# 2. Obter ID do workspace
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query { project(id: "proj-id") { workspaceId } }' '{}'

# 3. Buscar template do Postgres
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query { template(code: "postgres") { id serializedConfig } }' '{}'

# 4. Fazer deploy do template
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation deploy($input: TemplateDeployV2Input!) {
    templateDeployV2(input: $input) { projectId workflowId }
  }' \
  '{"input": {"templateId": "...", "serializedConfig": {...}, "projectId": "...", "environmentId": "...", "workspaceId": "..."}}'
SCRIPT
```

### Então Conectar de Outro Serviço

Use a skill `railway-environment` para adicionar a referência de variável:

```json
{
  "services": {
    "<backend-service-id>": {
      "variables": {
        "DATABASE_URL": { "value": "${{Postgres.DATABASE_URL}}" }
      }
    }
  }
}
```

## Resposta

Deploy bem-sucedido retorna:
```json
{
  "data": {
    "templateDeployV2": {
      "projectId": "e63baedb-e308-49e9-8c06-c25336f861c7",
      "workflowId": "deployTemplate/project/e63baedb-e308-49e9-8c06-c25336f861c7/xxx"
    }
  }
}
```

## O que Será Criado

Cada template de banco de dados cria:
- Um serviço com a imagem do banco de dados
- Um volume para persistência de dados
- Variáveis de ambiente para strings de conexão
- TCP proxy para acesso externo (quando aplicável)

## Tratamento de Erros

| Erro | Causa | Solução |
|---|---|---|
| Template não encontrado | Código de template inválido | Use: `postgres`, `redis`, `mysql`, `mongodb` |
| Permissão negada | Usuário sem acesso | Precisa de função DEVELOPER ou superior |
| Projeto não encontrado | ID de projeto inválido | Execute `railway status --json` para obter ID correto |

## Fluxos de Exemplo

### "adicionar postgres e conectar ao servidor"

1. Verificar BDs existentes via consulta de config de env
2. Se postgres existe: Pular para passo 5
3. Se não existe: Fazer deploy do template postgres (buscar template → deploy)
4. Aguardar conclusão do deploy
5. Identificar serviço alvo (perguntar se múltiplos, ou usar serviço vinculado)
6. Usar skill `railway-environment` para preparar: `DATABASE_URL: { "value": "${{Postgres.DATABASE_URL}}" }`
7. Aplicar alterações

### "adicionar postgres"

1. Verificar BDs existentes via consulta de config de env
2. Se existe: "Postgres já existe neste projeto"
3. Se não existe: Fazer deploy do template postgres
4. Informar usuário: "Postgres criado. Conecte um serviço com: `DATABASE_URL=${{Postgres.DATABASE_URL}}`"

### "conectar o servidor ao redis"

1. Verificar BDs existentes via consulta de config de env
2. Se redis existe: Conectar REDIS_URL via skill environment → aplicar
3. Se sem redis: Perguntar "Nenhum Redis encontrado. Criar um?"
   - Fazer deploy do template redis
   - Conectar REDIS_URL → aplicar

## Composição

- **Conectar serviços**: Use a skill `railway-environment` para adicionar referências de variáveis
- **Visualizar serviço de banco de dados**: Use a skill `railway-service`
- **Verificar logs**: Use a skill `railway-deployment`