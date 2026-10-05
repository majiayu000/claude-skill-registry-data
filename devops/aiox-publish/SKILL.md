---
name: aiox-publish
description: >
  Executa a publicação segura de alterações: gates pré-push, verificação de
  story fechada, QA aprovado e push via @devops. Usar quando o usuário solicitar
  publicação, push, deploy ou release.
---

# AIOX Publish — Publicação Segura

## Quando esta skill é acionada

- "publique as alterações"
- "faça o push"
- "deploy"
- "release"
- "mande para produção"
- Qualquer solicitação de publicação ou operação remota

## Pré-condições (todas verificadas antes do push)

1. Story fechada pelo @po (status Done)
2. QA veredito aceitável (PASS, CONCERNS ou WAIVED)
3. Lint passa (`ruff check scripts/`)
4. Typecheck passa (`mypy scripts/`)
5. Testes passam (`pytest`)
6. Build passa (se aplicável)
7. Nenhum débito HIGH introduzido sem registro
8. ChangeLog e File List atualizados

## Sequência

```
@qa (gate final) → @devops (push/PR/release)
```

### Fase 1: Gate final (@qa)

**Agente:** aiox-qa
- Verificar todas as pré-condições
- Executar `/quality-gate` + `/code-review`
- Emitir veredito final de publicação

### Fase 2: Push (@devops)

**Agente:** aiox-devops
- Único autorizado a executar `git push`
- Criar PR se aplicável
- Criar release/tag se aplicável
- Atualizar `touch .claude/.pre-push-passed`

## Bloqueios (hooks)

| Hook | O que bloqueia |
|------|---------------|
| `enforce-git-push-authority.cjs` | Push por agente que não é @devops |
| `pre-push-gate.cjs` | Push/commit sem validação recente |
| `no-story-no-edit.cjs` | Edição de código sem story ativa |
| `db-destructive-guard.cjs` | Operação DB destrutiva sem HIGH-RISK |

## Condições de interrupção

- Qualquer pré-condição falha → bloqueia push, informa gate faltante
- Push para branch protegida → requer autorização explícita
- `--force` ou `--force-with-lease` → bloqueado salvo procedimento autorizado
- Story não fechada → "Story deve ser fechada pelo @po antes do push"

## Operações permitidas apenas ao @devops

- `git push`
- `git push --force` (com autorização explícita)
- `gh pr create`
- `gh pr merge`
- `git tag`
- `gh release create`
- MCP add/remove/configure
- CI/CD pipeline management

## Referências

- Hooks: `.claude/settings.local.json`, `.claude/hooks/`
- Agent authority: `.claude/rules/agent-authority.md`
- Protocolo: `.claude/rules/aiox-project-operating-protocol.md`
