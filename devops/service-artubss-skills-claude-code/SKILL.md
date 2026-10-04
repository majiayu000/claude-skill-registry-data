---
name: railway-service
description: Verificar status do serviço, renomear serviços, alterar ícones de serviço, vincular serviços ou criar serviços com imagens Docker. Para criar serviços com código local, prefira a skill railway-new. Para fontes de repositório GitHub, use a skill railway-new para criar serviço vazio e depois railway-environment para configurar a fonte.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Service, Status, Docker, Container, Infrastructure, Management]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Gerenciamento de Serviços Railway

Verificar status, atualizar propriedades e criação avançada de serviços.

## Quando Usar

- Usuário pergunta sobre status do serviço, saúde ou deployments
- Usuário pergunta "meu serviço foi deployado?"
- Usuário quer renomear um serviço ou alterar ícone do serviço
- Usuário quer vincular um serviço diferente
- Usuário quer fazer deploy de uma imagem Docker como um novo serviço (avançado)

**Nota:** Para criar serviços com código local (caso comum), prefira a skill railway-new que lida com configuração de projeto, scaffolding e criação de serviço em conjunto.

**Para fontes de repositório GitHub:** Use a skill railway-new para criar serviço vazio, depois railway-environment para configurar source.repo via API de alterações em staging.

## Criar Serviço

Criar um novo serviço via API GraphQL. Não há comando CLI para isso.

### Obter Contexto

```bash
railway status --json
```

Extraia:
- `project.id` - para criar o serviço
- `environment.id` - para staging da configuração de instância

### Mutation de Criação de Serviço

```graphql
mutation serviceCreate($input: ServiceCreateInput!) {
  serviceCreate(input: $input) {
    id
    name
  }
}
```

### Campos de ServiceCreateInput

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `projectId` | String! | ID do projeto (obrigatório) |
| `name` | String | Nome do serviço (gerado automaticamente se omitido) |
| `source.image` | String | Imagem Docker (ex: `nginx:latest`) |
| `source.repo` | String | Repositório GitHub (ex: `usuario/repo`) |
| `branch` | String | Branch Git para fonte de repositório |
| `environmentId` | String | Se definido e é um fork, cria apenas nesse ambiente |

### Exemplo: Criar serviço vazio

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation createService($input: ServiceCreateInput!) {
    serviceCreate(input: $input) { id name }
  }' \
  '{"input": {"projectId": "PROJECT_ID"}}'
SCRIPT
```

### Exemplo: Criar serviço com imagem

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation createService($input: ServiceCreateInput!) {
    serviceCreate(input: $input) { id name }
  }' \
  '{"input": {"projectId": "PROJECT_ID", "name": "my-service", "source": {"image": "nginx:latest"}}}'
SCRIPT
```

### Conectando um Repositório GitHub

**NÃO use serviceCreate com source.repo** - use API de alterações em staging em vez disso.

Fluxo:
1. Criar serviço vazio: `serviceCreate(input: {projectId: "...", name: "my-service"})`
2. Use a skill railway-environment para configurar a fonte via API de alterações em staging
3. Aplique para disparar o deployment

### Após Criar: Configurar Instância

Use a skill railway-environment para configurar a instância do serviço:

```json
{
  "services": {
    "<serviceId>": {
      "isCreated": true,
      "source": { "image": "nginx:latest" },
      "variables": {
        "PORT": { "value": "8080" }
      }
    }
  }
}
```

**Crítico:** Sempre inclua `isCreated: true` para novas instâncias de serviço.

Depois use a skill railway-environment para aplicar e fazer deploy.

## Verificar Status do Serviço

```bash
railway service status --json
```

Retorna status de deployment atual para o serviço vinculado.

### Histórico de Deployment

```bash
railway deployment list --json --limit 5
```

### Status Atual

Mostre:
- **Serviço**: nome e status atual
- **Último Deployment**: status (SUCCESS, FAILED, DEPLOYING, CRASHED, etc.)
- **Deployado em**: quando o deployment atual entrou em produção
- **Deployments Recentes**: últimos 3-5 com status e timestamps

### Status de Deployment

| Status | Significado |
|--------|------------|
| SUCCESS | Deployado e em execução |
| FAILED | Falha na compilação ou deployment |
| DEPLOYING | Fazendo deployment atualmente |
| BUILDING | Compilação em andamento |
| CRASHED | Crash em tempo de execução |
| REMOVED | Deployment removido |

## Atualizar Serviço

Atualizar nome ou ícone do serviço via API GraphQL.

### Obter ID do Serviço

```bash
railway status --json
```

Extraia `service.id` da resposta.

### Atualizar Nome

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation updateService($id: String!, $input: ServiceUpdateInput!) {
    serviceUpdate(id: $id, input: $input) { id name }
  }' \
  '{"id": "SERVICE_ID", "input": {"name": "new-name"}}'
SCRIPT
```

### Atualizar Ícone

Ícones podem ser URLs de imagem ou GIFs animados.

| Tipo | Exemplo |
|------|---------|
| URL de imagem | `"icon": "https://example.com/logo.png"` |
| GIF animado | `"icon": "https://example.com/animated.gif"` |
| Devicons | `"icon": "https://devicons.railway.app/github"` |

**Railway Devicons:** Faça consulta em `https://devicons.railway.app/{query}` para ícones comuns de desenvolvedor (ex: `github`, `postgres`, `redis`, `nodejs`). Navegue por todos em https://devicons.railway.app

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation updateService($id: String!, $input: ServiceUpdateInput!) {
    serviceUpdate(id: $id, input: $input) { id icon }
  }' \
  '{"id": "SERVICE_ID", "input": {"icon": "https://devicons.railway.app/github"}}'
SCRIPT
```

### Campos de ServiceUpdateInput

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | String | Nome do serviço |
| `icon` | String | Emoji ou URL de imagem (incluindo GIFs animados) |

## Vincular Serviço

Trocar o serviço vinculado para o diretório atual:

```bash
railway service link
```

Ou especifique diretamente:

```bash
railway service link <service-name>
```

## Composição

- **Criar serviço com código local**: Use a skill railway-new (lida com scaffolding + criação)
- **Configurar serviço**: Use a skill railway-environment (variáveis, comandos, imagem, etc.)
- **Deletar serviço**: Use a skill railway-environment com `isDeleted: true`
- **Aplicar alterações**: Use a skill railway-environment
- **Visualizar logs**: Use a skill railway-deployment
- **Fazer deploy de código local**: Use a skill railway-deploy

## Tratamento de Erros

### Nenhum Serviço Vinculado
```
No service linked. Run `railway service link` to link a service.
```

### Sem Deployments
```
Service exists but has no deployments yet. Deploy with `railway up`.
```

### Serviço Não Encontrado
```
Service "foo" not found. Check available services with `railway status`.
```

### Projeto Não Encontrado
O usuário pode não estar em um projeto vinculado. Verifique `railway status`.

### Permissão Negada
O usuário precisa de pelo menos role DEVELOPER para criar serviços.

### Imagem Inválida
A imagem Docker deve estar acessível (pública ou com credenciais de registry).