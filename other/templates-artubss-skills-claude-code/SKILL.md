---
name: railway-templates
description: Procure e implante serviços do marketplace de templates do Railway. Use quando o usuário quiser adicionar um serviço de um template, encontrar templates para um caso de uso específico, ou implantar ferramentas como Ghost, Strapi, n8n, Minio, Uptime Kuma, etc. Para bancos de dados (Postgres, Redis, MySQL, MongoDB), prefira a skill railway-database.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Templates, Marketplace, Deployment, CMS, Automation, Infrastructure]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Railway Templates

Procure e implante serviços do marketplace de templates do Railway.

## Quando Usar

- Usuário pede para "adicionar Postgres", "adicionar Redis", "adicionar um banco de dados"
- Usuário pede para "adicionar Ghost", "adicionar Strapi", "adicionar n8n", ou qualquer outro serviço
- Usuário quer encontrar templates para um caso de uso (ex: "CMS", "storage", "monitoramento")
- Usuário pergunta "quais templates estão disponíveis?"
- Usuário quer implantar um serviço pré-configurado

## Códigos de Template Comuns

| Categoria | Template | Código |
|----------|----------|------|
| **Bancos de Dados** | PostgreSQL | `postgres` |
| | Redis | `redis` |
| | MySQL | `mysql` |
| | MongoDB | `mongodb` |
| **CMS** | Ghost | `ghost` |
| | Strapi | `strapi` |
| **Storage** | Minio | `minio` |
| **Automação** | n8n | `n8n` |
| **Monitoramento** | Uptime Kuma | `uptime-kuma` |

Para outros templates, use a consulta de busca abaixo.

## Pré-requisitos

Obtenha contexto do projeto:
```bash
railway status --json
```

Extraia:
- `id` - ID do projeto
- `environments.edges[0].node.id` - ID do ambiente

Obtenha ID do workspace:
```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query getWorkspace($projectId: String!) {
    project(id: $projectId) { workspaceId }
  }' \
  '{"projectId": "PROJECT_ID"}'
SCRIPT
```

## Procurar Templates

Liste templates disponíveis com filtros opcionais:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query templates($first: Int, $verified: Boolean) {
    templates(first: $first, verified: $verified) {
      edges {
        node {
          name
          code
          description
          category
        }
      }
    }
  }' \
  '{"first": 20, "verified": true}'
SCRIPT
```

### Argumentos

| Argumento | Tipo | Descrição |
|----------|------|-------------|
| `first` | Int | Número de resultados (máx. ~100) |
| `verified` | Boolean | Apenas templates verificados |
| `recommended` | Boolean | Apenas templates recomendados |

### Limite de Taxa

10 requisições por minuto. Não faça buscas em excesso.

## Obter Detalhes do Template

Busque um template específico por código:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query template($code: String!) {
    template(code: $code) {
      id
      name
      description
      serializedConfig
    }
  }' \
  '{"code": "postgres"}'
SCRIPT
```

Retorna:
- `id` - ID do template (necessário para implantação)
- `serializedConfig` - configuração do serviço (necessária para implantação)

## Implantar Template

### Passo 1: Buscar Template

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query template($code: String!) {
    template(code: $code) {
      id
      serializedConfig
    }
  }' \
  '{"code": "postgres"}'
SCRIPT
```

### Passo 2: Implantar no Projeto

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
      "templateId": "TEMPLATE_ID_FROM_STEP_1",
      "serializedConfig": SERIALIZED_CONFIG_FROM_STEP_1,
      "projectId": "PROJECT_ID",
      "environmentId": "ENVIRONMENT_ID",
      "workspaceId": "WORKSPACE_ID"
    }
  }'
SCRIPT
```

**Importante:** `serializedConfig` é o objeto JSON exato da consulta de template, não uma string.

## Composição

- **Conectar serviços**: Use a skill railway-environment para adicionar referências de variáveis
- **Ver serviço implantado**: Use a skill railway-service
- **Verificar logs**: Use a skill railway-deployment
- **Adicionar domínios**: Use a skill railway-domain