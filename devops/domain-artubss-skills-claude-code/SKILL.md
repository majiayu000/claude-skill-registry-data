---
name: railway-domain
description: Adicionar, visualizar ou remover domínios para serviços Railway. Use quando o usuário quer adicionar um domínio, gerar um domínio railway, verificar domínios atuais, obter a URL de um serviço ou remover um domínio.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Domain, DNS, URL, Custom Domain, Infrastructure]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Gerenciamento de Domínios Railway

Adicione, visualize ou remova domínios para serviços Railway.

## Quando Usar

- Usuário pede para "adicionar um domínio", "gerar um domínio", "obter uma URL"
- Usuário quer adicionar um domínio customizado
- Usuário pergunta "qual é a URL do meu serviço"
- Usuário quer remover um domínio

## Adicionar Domínio Railway

Gere um domínio fornecido pelo Railway (máx. 1 por serviço):

```bash
railway domain --json
```

Para um serviço específico:
```bash
railway domain --json --service backend
```

### Resposta
Retorna a URL do domínio gerado. O serviço deve ter um deployment.

## Adicionar Domínio Customizado

```bash
railway domain example.com --json
```

### Resposta
Retorna os registros DNS necessários:
```json
{
  "domain": "example.com",
  "dnsRecords": [
    { "type": "CNAME", "host": "@", "value": "..." }
  ]
}
```

Informe ao usuário para adicionar esses registros ao seu provedor de DNS.

## Ler Domínios Atuais

Use a skill railway-environment para ver domínios configurados, ou consulte diretamente:

```graphql
query domains($envId: String!) {
  environment(id: $envId) {
    config(decryptVariables: false)
  }
}
```

Os domínios estão em `config.services.<serviceId>.networking`:
- `serviceDomains` - Domínios fornecidos pelo Railway
- `customDomains` - Domínios fornecidos pelo usuário

## Remover Domínio

Use a skill railway-environment para remover domínios:

### Remover domínio customizado
```json
{
  "services": {
    "<serviceId>": {
      "networking": {
        "customDomains": { "<domainId>": null }
      }
    }
  }
}
```

### Remover domínio railway
```json
{
  "services": {
    "<serviceId>": {
      "networking": {
        "serviceDomains": { "<domainId>": null }
      }
    }
  }
}
```

Em seguida, use a skill railway-environment para aplicar e fazer commit da alteração.

## Opções CLI

| Flag | Descrição |
|------|-------------|
| `[DOMAIN]` | Domínio customizado a adicionar (omita para domínio railway) |
| `-p, --port <PORT>` | Porta para conectar |
| `-s, --service <NAME>` | Serviço de destino (padrão: vinculado) |
| `--json` | Saída em JSON |

## Composição

- **Ler domínios**: Use a skill railway-environment
- **Remover domínios**: Use a skill railway-environment
- **Aplicar remoção**: Use a skill railway-environment
- **Verificar serviço**: Use a skill railway-service

## Tratamento de Erros

### Nenhum Serviço Vinculado
```
No service linked. Use --service flag or run `railway service` to select one.
```

### Domínio Já Existe
```
Service already has a railway-provided domain. Maximum 1 per service.
```

### Nenhum Deployment
```
Service has no deployment. Deploy first with `railway up`.
```

### Domínio Inválido
```
Invalid domain format. Use a valid domain like "example.com" or "api.example.com".
```