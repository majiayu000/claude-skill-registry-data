---
name: delivery
description: Gerencia ciclo de releases, changelogs e deployments. Use para "finalizar tarefa", "fazer release", "deploy" ou "publicar versão".
---

## Workflow de Conclusão (Template Adaptativo)

1. **Build Check**: Identificar e executar o comando de build conforme a stack detectada no bootstrap (ex: `npm run build`, `go build`, `mvn package`, etc). Garanta que o projeto compila sem erros.
2. **Versionamento**: Realizar o *bump* semântico no manifesto principal (ex: `package.json`, `version.go`, `VERSION`, etc).
3. **Changelog**: Atualizar o `CHANGELOG.md` ou arquivo equivalente com as novas implementações.
4. **Git Sync**: Executar Git flow (commits convencionais) e realizar o deploy para o provedor configurado no bootstrap (ex: Firebase, AWS, Vercel, etc) utilizando os comandos dinâmicos da stack.
