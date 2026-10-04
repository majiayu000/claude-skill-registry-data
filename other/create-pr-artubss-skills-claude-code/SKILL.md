---
name: create-pr
description: Criar pull requests seguindo as convenções do Sentry. Use ao abrir PRs, escrever descrições de PR ou preparar mudanças para revisão. Segue as diretrizes de revisão de código do Sentry.
---

# Criar Pull Request

Criar pull requests seguindo as práticas de engenharia do Sentry.

**Requer**: GitHub CLI (`gh`) autenticada e disponível.

## Processo

### Passo 1: Verificar Estado da Branch

```bash
# Verificar branch atual e status
git status
git log main..HEAD --oneline
```

Garanta que:
- Todas as mudanças estão commitadas
- A branch está atualizada com o remoto
- As mudanças estão rebased em main, se necessário

### Passo 2: Analisar Mudanças

Revise o que será incluído no PR:

```bash
# Ver todos os commits que entrarão no PR
git log main..HEAD

# Ver o diff completo
git diff main...HEAD
```

Compreenda o escopo e a finalidade de todas as mudanças antes de escrever a descrição.

### Passo 3: Escrever a Descrição do PR

Siga esta estrutura:

```markdown
<descrição breve do que o PR faz>

<por que essas mudanças estão sendo feitas - a motivação>

<abordagens alternativas consideradas, se houver>

<qualquer contexto adicional que os revisores precisem>
```

**NÃO inclua:**
- Seções "Plano de testes"
- Listas de checkboxes com passos de testes
- Resumos redundantes do diff

**Inclua:**
- Explicação clara do quê e por quê
- Links para issues ou tickets relevantes
- Contexto que não é óbvio no código
- Notas sobre áreas específicas que precisam de revisão cuidadosa

### Passo 4: Criar o PR

```bash
gh pr create --title "<tipo>(<escopo>): <descrição>" --body "$(cat <<'EOF'
<corpo da descrição aqui>
EOF
)"
```

**Formato do título** segue convenções de commit:
- `feat(escopo): Adicionar nova funcionalidade`
- `fix(escopo): Corrigir o bug`
- `ref: Refatorar algo`

### Passo 5: Adicionar Revisores (se conhecido)

```bash
# Solicitar revisão de pessoas específicas
gh pr edit --add-reviewer usuario1,usuario2

# Ou solicitar de um time
gh pr edit --add-reviewer @getsentry/nome-do-time
```

Limite a 1-3 revisores para manter clara a propriedade.

## Exemplos de Descrição de PR

### PR de Funcionalidade

```markdown
Adicionar respostas em thread do Slack para notificações de alerta

Quando um alerta é atualizado ou resolvido, agora postamos uma resposta
na thread original do Slack em vez de criar uma nova mensagem. Isso mantém
as notificações relacionadas agrupadas e reduz o ruído no canal.

Anteriormente consideramos postar edições na mensagem original, mas as
threads preservam melhor a linha do tempo dos eventos e funcionam quando
a mensagem original é mais antiga que a janela de edição do Slack.

Refs SENTRY-1234
```

### PR de Correção de Bug

```markdown
Tratar resposta nula no endpoint da API de usuário

O endpoint de usuário poderia retornar nulo para contas soft-deleted,
causando crashes no dashboard ao acessar propriedades do usuário. Isso
adiciona uma verificação de nulo e retorna uma resposta 404 apropriada.

Encontrado ao investigar SENTRY-5678.

Fixes SENTRY-5678
```

### PR de Refatoração

```markdown
Extrair lógica de validação para módulo compartilhado

Move código de validação duplicado dos endpoints de alertas, issues e
projects para uma classe validadora compartilhada. Sem mudança de comportamento.

Isso prepara para adicionar novas regras de validação em SENTRY-9999 sem
duplicar lógica entre endpoints.
```

## Referências de Issues

Referencie issues no corpo do PR:

| Sintaxe | Efeito |
|--------|--------|
| `Fixes #1234` | Fecha issue do GitHub ao fazer merge |
| `Fixes SENTRY-1234` | Fecha issue do Sentry |
| `Refs GH-1234` | Vincula sem fechar |
| `Refs LINEAR-ABC-123` | Vincula issue do Linear |

## Diretrizes

- **Um PR por funcionalidade/correção** - Não agrupe mudanças não relacionadas
- **Mantenha PRs revisáveis** - PRs menores recebem revisões mais rápidas e melhores
- **Explique o por quê** - Código mostra o quê; descrição explica por quê
- **Marque WIP cedo** - Use draft PRs para feedback antecipado

## Referências

- [Diretrizes de Revisão de Código do Sentry](https://develop.sentry.dev/engineering-practices/code-review/)
- [Mensagens de Commit do Sentry](https://develop.sentry.dev/engineering-practices/commit-messages/)