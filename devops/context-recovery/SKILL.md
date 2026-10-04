---
name: context-recovery
description: Use esta skill ao iniciar uma nova sessão ou quando o contexto da conversa for perdido. Reconstrói o entendimento completo do projeto lendo os documentos certos na ordem certa, antes de qualquer ação.
---

# Skill: Context Recovery

Use esta skill **sempre que**:
- Uma nova conversa começar neste projeto
- O contexto da sessão anterior foi perdido ou comprimido
- O usuário pedir para "retomar de onde parou"
- Você precisar entender o estado atual antes de propor ou implementar algo

---

## Objetivo

Reconstruir o contexto completo do projeto em menos de 2 minutos, sem pedir ao usuário que explique tudo novamente.

---

## Passos

### 1. Ler os documentos de contexto

Leia nesta ordem — cada arquivo responde uma pergunta diferente:

| Arquivo | Pergunta respondida |
|---------|-------------------|
| `docs/STATUS_LABORATORIO.md` | **Leia primeiro.** O que já foi feito, o que falta, próximos passos concretos, problemas conhecidos do ambiente |
| `docs/PROJECT_CONTEXT.md` | O que foi construído, como funciona, credenciais, comandos |
| `docs/ARCHITECTURE.md` | Como os componentes se relacionam, fluxos, segurança |
| `CLAUDE.md` | Regras do projeto que você deve seguir |
| `DOCS.md` | Descrição técnica de cada arquivo |

Se a tarefa da sessão for sobre CI/CD, containers ou colaboração em equipe, `docs/STATUS_LABORATORIO.md` já aponta para os documentos certos (`DEVOPS_GUIA.md`, `ROTEIRO_CICD_CLAUDE_CODE.md`, `COLABORACAO_EQUIPE.md`, `EXERCICIO_MULTIPLOS_DEVS.md`, `BACKLOG_KANBAN.md`, `SETUP_NOVA_MAQUINA.md`) — não é preciso ler todos de uma vez, apenas saber que existem.

### 2. Verificar o estado atual do repositório

```bash
git status
git log --oneline -10
```

- `git status` revela arquivos modificados não commitados — indica trabalho em andamento.
- `git log` mostra o histórico recente e o que foi entregue.

### 3. Verificar estrutura de arquivos atual

```bash
# Listar arquivos src/ e src/public/
```

Use Glob em `src/` e `src/public/` para confirmar quais arquivos existem de fato — documentação pode estar desatualizada.

### 4. Verificar dependências instaladas

```bash
cat package.json
```

Confirma pacotes disponíveis antes de sugerir código que os usa.

### 5. Montar o resumo de contexto

Após ler os documentos e verificar o estado, produza um resumo estruturado para o usuário com:

```
## Contexto recuperado

**Projeto:** <nome e objetivo em 1 linha>
**Stack:** <tecnologias principais>
**Estado atual:** <o que está funcionando, o que está pendente>
**Últimas alterações:** <baseado no git log>
**Pronto para:** <que tipo de tarefa posso executar agora>
```

---

## Regras

- Não faça perguntas ao usuário antes de ler os documentos — a resposta provavelmente já está lá.
- Não assuma que a documentação está 100% atualizada — verifique o estado real dos arquivos com Glob/Read.
- Se houver conflito entre documentação e código real, confie no código e sinalize o conflito.
- Não inicie nenhuma implementação antes de concluir todos os passos desta skill.
- Se algum documento não existir, sinalize e continue com o que estiver disponível.

---

## Quando NÃO usar

- Em continuações da mesma conversa com contexto ainda ativo.
- Para tarefas simples e isoladas que não dependem do estado do projeto (ex: "explique o que é scrypt").
