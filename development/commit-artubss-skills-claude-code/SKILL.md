---
name: commit
description: Crie mensagens de commit seguindo as convenções Sentry. Use ao fazer commit de alterações de código, escrever mensagens de commit ou formatar histórico git. Segue conventional commits com referências de issues específicas do Sentry.
---

# Mensagens de Commit Sentry

Siga estas convenções ao criar commits para projetos Sentry.

## Formato

```
<type>(<scope>): <subject>

<body>

<footer>
```

O header é obrigatório. Scope é opcional. Todas as linhas devem ter menos de 100 caracteres.

## Tipos de Commit

| Tipo | Propósito |
|------|-----------|
| `feat` | Novo recurso |
| `fix` | Correção de bug |
| `ref` | Refatoração (sem mudança de comportamento) |
| `perf` | Melhoria de performance |
| `docs` | Apenas documentação |
| `test` | Adição ou correção de testes |
| `build` | Sistema de build ou dependências |
| `ci` | Configuração de CI |
| `chore` | Tarefas de manutenção |
| `style` | Formatação de código (sem mudança de lógica) |
| `meta` | Metadados do repositório |
| `license` | Mudanças de licença |

## Regras da Linha de Assunto

- Use imperativo, tempo presente: "Add feature" e não "Added feature"
- Capitalize a primeira letra
- Sem ponto no final
- Máximo 70 caracteres

## Diretrizes do Body

- Explique **o que** e **por quê**, não como
- Use modo imperativo e tempo presente
- Inclua a motivação para a mudança
- Contraste com comportamento anterior quando relevante

## Footer: Referências de Issues

Referencie issues no footer usando estes padrões:

```
Fixes GH-1234
Fixes #1234
Fixes SENTRY-1234
Refs LINEAR-ABC-123
```

- `Fixes` fecha a issue quando merged
- `Refs` faz link sem fechar

## Exemplos

### Correção simples

```
fix(api): Handle null response in user endpoint

The user API could return null for deleted accounts, causing a crash
in the dashboard. Add null check before accessing user properties.

Fixes SENTRY-5678
```

### Recurso com scope

```
feat(alerts): Add Slack thread replies for alert updates

When an alert is updated or resolved, post a reply to the original
Slack thread instead of creating a new message. This keeps related
notifications grouped together.

Refs GH-1234
```

### Refatoração

```
ref: Extract common validation logic to shared module

Move duplicate validation code from three endpoints into a shared
validator class. No behavior change.
```

### Mudança com breaking change

```
feat(api)!: Remove deprecated v1 endpoints

Remove all v1 API endpoints that were deprecated in version 23.1.
Clients should migrate to v2 endpoints.

BREAKING CHANGE: v1 endpoints no longer available
Fixes SENTRY-9999
```

## Formato de Revert

```
revert: feat(api): Add new endpoint

This reverts commit abc123def456.

Reason: Caused performance regression in production.
```

## Princípios

- Cada commit deve ser uma única mudança estável
- Commits devem ser revisáveis independentemente
- O repositório deve estar em estado funcional após cada commit

## Referências

- [Sentry Commit Messages](https://develop.sentry.dev/engineering-practices/commit-messages/)