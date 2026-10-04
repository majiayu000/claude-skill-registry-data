---
name: railway-status
description: Verificar o status atual do projeto Railway para este diretório. Use quando o usuário perguntar "status railway", "está rodando", "o que está deployado", "status de deployment" ou sobre uptime. NÃO para queries de variáveis ou configuração - use a skill railway-environment para isso.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Status, Project, Environment, Deployment, Infrastructure]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*), Bash(which:*), Bash(command:*)
---

# Railway Status

Verificar o status atual do projeto Railway para este diretório.

## Quando Usar

- Usuário pergunta sobre status do Railway, projeto, serviços ou deployments
- Usuário menciona fazer deploy ou push para Railway
- Antes de qualquer operação no Railway (deploy, atualizar serviço, adicionar variáveis)
- Usuário pergunta sobre ambientes ou domínios

## Quando NÃO Usar

Use a skill railway-environment quando o usuário quiser:
- Configuração detalhada de serviço (tipo de builder, dockerfile path, build command, root directory)
- Config de deploy (start command, restart policy, healthchecks, predeploy command)
- Fonte do serviço (repo, branch, image)
- Comparar configs de serviço
- Query ou alterar variáveis de ambiente

## Verificar Status

Execute:
```bash
railway status --json
```

Primeiro, verifique se a CLI está instalada:
```bash
command -v railway
```

## Tratando Erros

### CLI Não Instalada
Se `command -v railway` falhar:

> Railway CLI não está instalado. Instale com:
> ```
> npm install -g @railway/cli
> ```
> ou
> ```
> brew install railway
> ```
> Depois autentique: `railway login`

### Não Autenticado
Se `railway whoami` falhar:

> Você não está logado no Railway. Execute:
> ```
> railway login
> ```

### Nenhum Projeto Vinculado
Se status retornar "No linked project":

> Nenhum projeto Railway vinculado a este diretório.
>
> Para vincular um projeto existente: `railway link`
> Para criar um novo projeto: `railway init`

## Apresentando o Status

Faça parse do JSON e apresente:
- **Projeto**: nome e workspace
- **Ambiente**: ambiente atual (production, staging, etc.)
- **Serviços**: lista com status de deployment
- **Deployments Ativos**: qualquer deployment em progresso (do campo `activeDeployments`)
- **Domínios**: qualquer domínio configurado

Exemplo de formato de saída:
```
Projeto: my-app (workspace: my-team)
Ambiente: production

Serviços:
- web: deployado (https://my-app.up.railway.app)
- api: deployando (build em progresso)
- postgres: rodando
```

O array `activeDeployments` em cada serviço mostra deployments atualmente em execução
com seu status (building, deploying, etc.).