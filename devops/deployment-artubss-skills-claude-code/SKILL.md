---
name: railway-deployment
description: Gerenciar deployments do Railway - visualizar logs, reimplementar, reiniciar ou remover deployments. Use para ciclo de vida de deployment (remover, parar, reimplementar, reiniciar), visibilidade de deployment (listar, status, histórico) e troubleshooting (logs, erros, falhas, travamentos). NÃO é para deletar serviços - use a skill railway-environment com isDeleted para isso.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Deployment, Logs, Debug, Troubleshooting, Redeploy, Infrastructure]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Gerenciamento de Deployments do Railway

Gerenciar deployments existentes do Railway: listar, visualizar logs, reimplementar ou remover.

**Importante:** "Remover deployment" (`railway down`) interrompe o deployment atual mas mantém o serviço. Para deletar um serviço inteiramente, use a skill railway-environment com `isDeleted: true`.

## Quando Usar

- Usuário diz "remover deploy", "desativar serviço", "parar deployment", "railway down"
- Usuário quer "reimplementar", "reiniciar o serviço", "reiniciar deployment"
- Usuário pergunta "listar deployments", "mostrar histórico de deployment", "status do deployment"
- Usuário pergunta "ver logs", "mostrar logs", "verificar erros", "debugar problemas"

## Listar Deployments

```bash
railway deployment list --limit 10 --json
```

Mostra IDs de deployment, status e metadados. Use para encontrar IDs específicos de deployment para logs ou debugging.

### Especificar Serviço

```bash
railway deployment list --service backend --limit 10 --json
```

## Visualizar Logs

### Logs de Deploy

```bash
railway logs --lines 100 --json
```

Em modo não-interativo, streaming é desabilitado automaticamente e a CLI busca logs e sai.

### Logs de Build

```bash
railway logs --build --lines 100 --json
```

Para debugar falhas de build ou visualizar saída de build.

### Logs de Deployments Falhados/Em Progresso

Por padrão `railway logs` mostra o último deployment bem-sucedido. Use `--latest` para o atual:

```bash
railway logs --latest --lines 100 --json
```

### Filtrar Logs

```bash
# Apenas erros
railway logs --lines 50 --filter "@level:error" --json

# Busca de texto
railway logs --lines 50 --filter "connection refused" --json

# Combinado
railway logs --lines 50 --filter "@level:error AND timeout" --json
```

### Filtragem por Período

```bash
# Logs da última hora
railway logs --since 1h --lines 100 --json

# Logs entre 30 e 10 minutos atrás
railway logs --since 30m --until 10m --lines 100 --json

# Logs de timestamp específico
railway logs --since 2024-01-15T10:00:00Z --lines 100 --json
```

Formatos: relativo (`30s`, `5m`, `2h`, `1d`, `1w`) ou timestamps ISO 8601.

### Logs de Deployment Específico

Logs de deploy:
```bash
railway logs <deployment-id> --lines 100 --json
```

Logs de build:
```bash
railway logs --build <deployment-id> --lines 100 --json
```

Obtenha o ID de deployment com `railway deployment list`.

**Nota:** O ID de deployment é um argumento posicional, NÃO `--deployment <id>`. A flag `--deployment` é booleana que seleciona logs de deploy (vs `--build` para logs de build).

## Reimplementar

Reimplementar o deployment mais recente:

```bash
railway redeploy --service <name> -y
```

A flag `-y` pula confirmação. Útil quando:
- Config mudou via skill railway-environment
- Precisa reiniciar sem novo código
- Deploy anterior foi bem-sucedido mas serviço misbehaving

### Reiniciar Apenas Container

Reiniciar sem rebuildar (pega mudanças de recursos externos):

```bash
railway restart --service <name> -y
```

Use quando recursos externos (arquivos S3, config maps) mudaram mas código não.

## Remover Deployment

Desativa o deployment atual. O serviço permanece mas sem deployment rodando.

```bash
# Remover deployment para serviço vinculado
railway down -y

# Remover deployment para serviço específico
railway down --service web -y
railway down --service api -y
```

Isso é o que usuários querem dizer com "remover deploy", "desativar", ou "parar o deployment".

**Nota:** Isso NÃO deleta o serviço. Para deletar um serviço inteiramente, use a skill railway-environment com `isDeleted: true`.

## Opções de CLI

### deployment list

| Flag | Descrição |
|------|-----------|
| `-s, --service <NAME>` | Nome ou ID do serviço |
| `-e, --environment <NAME>` | Nome ou ID do ambiente |
| `--limit <N>` | Max deployments (padrão 20, máx 1000) |
| `--json` | Saída JSON |

### logs

| Flag | Descrição |
|------|-----------|
| `-s, --service <NAME>` | Nome ou ID do serviço |
| `-e, --environment <NAME>` | Nome ou ID do ambiente |
| `-d, --deployment` | Mostrar logs de deploy (padrão, flag booleana) |
| `-b, --build` | Mostrar logs de build (flag booleana) |
| `-n, --lines <N>` | Número de linhas (obrigatório) |
| `-f, --filter <QUERY>` | Filtrar usando query syntax |
| `--since <TIME>` | Hora de início (relativa ou ISO 8601) |
| `--until <TIME>` | Hora de fim (relativa ou ISO 8601) |
| `--latest` | Deployment mais recente (mesmo se falhado) |
| `--json` | Saída JSON |
| `[DEPLOYMENT_ID]` | Deployment específico (opcional) |

### redeploy

| Flag | Descrição |
|------|-----------|
| `-s, --service <NAME>` | Nome ou ID do serviço |
| `-y, --yes` | Pula confirmação |

### restart

| Flag | Descrição |
|------|-----------|
| `-s, --service <NAME>` | Nome ou ID do serviço |
| `-y, --yes` | Pula confirmação |

### down

| Flag | Descrição |
|------|-----------|
| `-s, --service <NAME>` | Nome ou ID do serviço |
| `-e, --environment <NAME>` | Nome ou ID do ambiente |
| `-y, --yes` | Pula confirmação |

## Apresentando Logs

Ao mostrar logs:
- Inclua timestamps
- Destaque erros e avisos
- Para falhas de build: mostre erro e sugira correções
- Para crashes em runtime: mostre stack trace com contexto
- Resuma padrões (ex: "15 erros de timeout nos últimos 100 logs")

## Composabilidade

- **Fazer push de novo código**: Use skill railway-deploy
- **Verificar status do serviço**: Use skill railway-status
- **Corrigir problemas de config**: Use skill railway-environment
- **Criar novo serviço**: Use skill railway-new

## Tratamento de Erros

### Nenhum Serviço Vinculado
```
No service linked. Run `railway service` to select one.
```

### Nenhum Deployment Encontrado
```
No deployments found. Deploy first with `railway up`.
```

### Nenhum Log Encontrado
Deployment pode ser muito antigo (limites de retenção de log) ou serviço não produziu saída.