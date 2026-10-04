---
name: iterate-pr
description: Itere em uma PR até que o CI passe. Use quando precisar corrigir falhas de CI, endereçar feedback de revisão, ou continuamente enviar correções até que todas as verificações fiquem verdes. Automatiza o ciclo de feedback-correção-push-aguardar.
---

# Iterar em PR Até o CI Passar

Itere continuamente no branch atual até que todas as verificações de CI passem e o feedback de revisão seja endereçado.

**Requer**: GitHub CLI (`gh`) autenticado e disponível.

## Processo

### Passo 1: Identificar a PR

```bash
gh pr view --json number,url,headRefName,baseRefName
```

Se não existir PR para o branch atual, pare e informe o usuário.

### Passo 2: Verificar Status de CI Primeiro

Sempre verifique o status de CI/GitHub Actions antes de analisar feedback de revisão:

```bash
gh pr checks --json name,state,bucket,link,workflow
```

O campo `bucket` categoriza o state em: `pass`, `fail`, `pending`, `skipping` ou `cancel`.

**Importante:** Se qualquer uma dessas verificações ainda estiver `pending`, aguarde antes de prosseguir:
- `sentry` / `sentry-io`
- `codecov`
- `cursor` / `bugbot` / `seer`
- Qualquer linter ou verificação de análise de código

Esses bots podem postar comentários de feedback adicionais após suas verificações serem concluídas. Aguardar evita trabalho duplicado.

### Passo 3: Coletar Feedback de Revisão

Quando as verificações de CI tiverem sido concluídas (ou pelo menos as verificações relacionadas a bots), colete feedback humano e de bot:

**Comentários de Revisão e Status:**
```bash
gh pr view --json reviews,comments,reviewDecision
```

**Comentários de Revisão Inline:**
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

**Comentários de Conversa da PR (inclui comentários de bot):**
```bash
gh api repos/{owner}/{repo}/issues/{pr_number}/comments
```

Procure por comentários de bot de: Sentry, Codecov, Cursor, Bugbot, Seer e outras ferramentas automatizadas.

### Passo 4: Investigar Falhas

Para cada falha de CI, obtenha os logs reais:

```bash
# Listar execuções recentes para este branch
gh run list --branch $(git branch --show-current) --limit 5 --json databaseId,name,status,conclusion

# Ver logs com falha para uma execução específica
gh run view <run-id> --log-failed
```

NÃO assuma o que falhou baseado apenas no nome da verificação. Sempre leia os logs reais.

### Passo 5: Validar Feedback

Para cada feedback (falha de CI ou comentário de revisão):

1. **Leia o código relevante** - Entenda o contexto antes de fazer mudanças
2. **Verifique se o problema é real** - Nem todo feedback é correto; revisores e bots podem se enganar
3. **Verifique se já foi endereçado** - O problema pode ter sido corrigido em um commit subsequente
4. **Ignore feedback inválido** - Se a preocupação não for legítima, siga adiante

### Passo 6: Endereçar Questões Válidas

Faça mudanças de código mínimas e direcionadas. Corrija apenas o que está realmente quebrado.

### Passo 7: Commit e Push

```bash
git add -A
git commit -m "fix: <mensagem descritiva do que foi corrigido>"
git push
```

### Passo 8: Aguardar CI

Use a funcionalidade de watch integrada:

```bash
gh pr checks --watch --interval 30
```

Isso aguarda até que todas as verificações sejam concluídas. Código de saída 0 significa que todas passaram, código de saída 1 significa falhas.

Alternativamente, faça polling manual se precisar de mais controle:

```bash
gh pr checks --json name,state,bucket | jq '.[] | select(.bucket != "pass")'
```

### Passo 9: Repetir

Retorne ao Passo 2 se:
- Qualquer verificação de CI falhar
- Novo feedback de revisão aparecer

Continue até que todas as verificações fiquem verdes e nenhum feedback não endereçado permaneça.

## Condições de Saída

**Sucesso:**
- Todas as verificações de CI estão verdes (`bucket: pass`)
- Nenhum feedback de revisão humana não endereçado

**Pedir Ajuda:**
- Mesma falha persiste após 3 tentativas (provável teste flaky ou problema mais profundo)
- Feedback de revisão requer esclarecimento ou decisão do usuário
- Falha de CI não relacionada a mudanças do branch (problema de infraestrutura)

**Parar Imediatamente:**
- Nenhuma PR existe para o branch atual
- Branch está desincronizado e precisa rebase (informe o usuário)

## Dicas

- Use `gh pr checks --required` para focar apenas em verificações obrigatórias
- Use `gh run view <run-id> --verbose` para ver todas as etapas de job, não apenas falhas
- Se uma verificação for de um serviço externo, o campo `link` no JSON de verificações fornece a URL para investigar