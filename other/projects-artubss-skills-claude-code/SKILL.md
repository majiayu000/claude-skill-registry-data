---
name: railway-projects
description: Listar, alternar e configurar projetos do Railway. Use quando o usuário quiser listar todos os projetos, alternar entre projetos, renomear um projeto, ativar/desativar deploys de PR, tornar um projeto público/privado ou modificar configurações do projeto.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Projects, Workspace, Management, Settings, Infrastructure]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Gerenciamento de Projetos do Railway

Listar, alternar e configurar projetos do Railway.

## Quando Usar

- Usuário pergunta "mostre todos os meus projetos" ou "que projetos eu tenho"
- Usuário pergunta sobre projetos em diferentes workspaces
- Usuário pergunta "que workspaces eu tenho"
- Usuário quer alternar para um projeto diferente
- Usuário quer renomear um projeto
- Usuário quer ativar/desativar deploys de PR
- Usuário quer tornar um projeto público ou privado
- Usuário pergunta sobre configurações do projeto

## Listar Projetos

A saída de `railway list --json` pode ser muito grande. Execute em um subagent e retorne apenas campos essenciais:

- Projeto: `id`, `name`
- Workspace: `id`, `name`
- Services: `name` (opcional, se o usuário precisar de contexto de serviço)

```bash
railway list --json
```

Extraia e retorne um resumo simplificado, não o JSON completo.

## Listar Workspaces

```bash
railway whoami --json
```

Retorna informações do usuário incluindo todos os workspaces aos quais o usuário pertence.

## Alternar Projeto

Vincule um projeto diferente ao diretório atual:

```bash
railway link -p <project-id-or-name>
```

Ou interativamente:

```bash
railway link
```

Após alternar, use a skill railway-status para ver os detalhes do projeto.

## Atualizar Projeto

Modifique as configurações do projeto via GraphQL API.

### Obter ID do Projeto

```bash
railway status --json
```

Extraia `project.id` da resposta.

### Mutation de Atualização

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation updateProject($id: String!, $input: ProjectUpdateInput!) {
    projectUpdate(id: $id, input: $input) { name prDeploys isPublic botPrEnvironments }
  }' \
  '{"id": "PROJECT_ID", "input": {"name": "new-name"}}'
SCRIPT
```

### Campos de ProjectUpdateInput

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | String | Nome do projeto |
| `description` | String | Descrição do projeto |
| `isPublic` | Boolean | Tornar projeto público/privado |
| `prDeploys` | Boolean | Ativar/desativar deploys de PR |
| `botPrEnvironments` | Boolean | Ativar ambientes de PR do Dependabot/Renovate |

### Exemplos

**Renomear projeto:**
```bash
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh '<mutation>' '{"id": "uuid", "input": {"name": "new-name"}}'
```

**Ativar deploys de PR:**
```bash
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh '<mutation>' '{"id": "uuid", "input": {"prDeploys": true}}'
```

**Tornar projeto público:**
```bash
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh '<mutation>' '{"id": "uuid", "input": {"isPublic": true}}'
```

**Múltiplos campos:**
```bash
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh '<mutation>' '{"id": "uuid", "input": {"name": "new-name", "prDeploys": true}}'
```

## Composição

- **Visualizar detalhes do projeto**: Use a skill railway-status
- **Criar novo projeto**: Use a skill railway-new
- **Gerenciar ambientes**: Use a skill railway-environment

## Tratamento de Erros

### Não Autenticado
```
Not authenticated. Run `railway login` first.
```

### Nenhum Projeto
```
No projects found. Create one with `railway init`.
```

### Permissão Negada
```
You don't have permission to modify this project. Check your Railway role.
```

### Projeto Não Encontrado
```
Project "foo" not found. Run `railway list` to see available projects.
```