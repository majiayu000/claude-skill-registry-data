---
name: railway-deploy
description: Fazer deploy de código para Railway usando "railway up". Use quando o usuário quer enviar código, diz "railway up", "deploy", "ship" ou "push". Para configuração inicial ou criação de serviços, use a skill railway-new. Para imagens Docker, use a skill railway-environment.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Deploy, CI/CD, Push, Ship, Infrastructure, Deployment]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Railway Deploy

Fazer deploy de código do diretório atual para Railway usando `railway up`.

## Quando Usar

- Usuário pede para "fazer deploy", "enviar", "fazer push do código"
- Usuário diz "railway up" ou "fazer deploy para Railway"
- Usuário quer fazer deploy de mudanças de código local
- Usuário diz "fazer deploy e corrigir qualquer problema" (use modo --ci)

## Modos

### Modo Detach (padrão)
Inicia o deploy e retorna imediatamente. Use para a maioria dos deploys.

```bash
railway up --detach
```

### Modo CI
Transmite os logs de build até completar. Use quando o usuário quer acompanhar o build ou precisa debugar problemas.

```bash
railway up --ci
```

**Quando usar modo CI:**
- Usuário diz "fazer deploy e acompanhar", "fazer deploy e corrigir problemas"
- Usuário está debugando falhas de build
- Usuário quer ver a saída do build

## Fazer Deploy de Serviço Específico

O padrão é o serviço vinculado. Para fazer deploy em um serviço diferente:

```bash
railway up --detach --service backend
```

## Fazer Deploy em Projeto Não Vinculado

Fazer deploy em um projeto sem vincular primeiro:

```bash
railway up --project <project-id> --environment production --detach
```

Requer ambas as flags `--project` e `--environment`.

## Opções de CLI

| Flag | Descrição |
|------|-----------|
| `-d, --detach` | Não anexar aos logs (padrão) |
| `-c, --ci` | Transmitir logs de build, sair quando concluído |
| `-s, --service <NAME>` | Serviço alvo (padrão é o vinculado) |
| `-e, --environment <NAME>` | Ambiente alvo (padrão é o vinculado) |
| `-p, --project <ID>` | Projeto alvo (requer --environment) |
| `[PATH]` | Caminho para fazer deploy (padrão é o diretório atual) |

## Vinculação de Diretório

O Railway CLI percorre PARA CIMA a árvore de diretórios para encontrar um projeto vinculado. Se você estiver em um subdiretório de um projeto vinculado, não precisa vincular novamente.

Para deploys em subdiretório, prefira definir `rootDirectory` via a skill railway-environment e depois fazer deploy normalmente com `railway up`.

## Após o Deploy

### Modo detach
```
Deploying to <service>...
```
Use a skill railway-deployment para verificar o status do build (com a flag `--lines`).

### Modo CI
Os logs de build são transmitidos inline. Se o build falhar, o erro estará na saída.

**NÃO execute `railway logs --build` após modo CI** - os logs já foram transmitidos. Se precisar de mais contexto, use a skill railway-deployment com a flag `--lines` (nunca transmita).

## Composição

- **Verificar status após deploy**: Use a skill railway-service
- **Ver logs**: Use a skill railway-deployment
- **Corrigir problemas de configuração**: Use a skill railway-environment
- **Fazer redeploy após corrigir configuração**: Use a skill railway-environment

## Tratamento de Erros

### Nenhum Projeto Vinculado
```
No Railway project linked. Run `railway link` first.
```

### Nenhum Serviço Vinculado
```
No service linked. Use --service flag or run `railway service` to select one.
```

### Falha de Build (modo CI)
Os logs de build já foram transmitidos - analise-os diretamente da saída do `railway up --ci`.
NÃO execute `railway logs` após modo CI (transmite indefinidamente sem `--lines`).

Problemas comuns:
- Dependências ausentes → verifique package.json/requirements.txt
- Comando de build incorreto → use a skill railway-environment para corrigir
- Problemas com Dockerfile → verifique o caminho do dockerfile