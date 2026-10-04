---
name: infrastructure
description: Gerencia infraestrutura, dependências e variáveis de ambiente. Use para "auditar", "atualizar pacotes", ou "sincronizar infra". Especialista em segurança e docs de variáveis (.env).
---

## Workflow Operacional

1. **Auditoria**: Executar scan de dependências nativo (ex: `npm audit`, `cargo audit`).
2. **Atualização**: Sugerir atualizações seguras (minor/patch) de pacotes defasados.
3. **Docs Sync**: Atualizar o `README.md` sempre que variáveis de ambiente novas forem adicionadas ou portas de rede (APIs) forem alteradas.
