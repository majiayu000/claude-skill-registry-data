---
name: verifica-tickets
description: Analisa tickets criados recentemente no projeto HYPERFLEET e verifica a qualidade de cada um. Use quando precisar verificar qualidade de tickets, higiene de backlog, ou validar tickets antes de sprint planning.
disable-model-invocation: true
argument-hint: [período, ex: -2d, -1w]
allowed-tools: Bash(date *), Bash(jira *), Skill(hyperfleet-jira:jira-story-pointer *)
---

# Verifica Tickets

Analisa tickets criados recentemente no projeto HYPERFLEET e verifica a qualidade de cada um.

## Argumentos

- `$ARGUMENTS`: Período de busca (opcional). Padrão: `-1d` (último dia). Exemplos: `-2d`, `-1w`

## Instruções

### 0. Determinar o período de busca

Se `$ARGUMENTS` foi fornecido, use-o diretamente.

Se `$ARGUMENTS` estiver vazio, determine o período padrão baseado no dia da semana:

```bash
date +%u
```

- Se hoje é **segunda (1)**: use `-3d` (cobre sexta, sábado e domingo)
- Se hoje é **domingo (7)**: use `-2d` (cobre sexta e sábado)
- Se hoje é **sábado (6)**: use `-1d` (cobre sexta)
- Nos demais dias: use `-1d`

### 1. Buscar tickets recentes

Execute o comando para buscar tickets criados no período que não estejam Closed ou Resolved:

```bash
jira issue list --project HYPERFLEET --jql "created >= <PERIODO> AND status NOT IN (Closed, Resolved)" --order-by created --reverse
```

Substitua `<PERIODO>` pelo valor de `$ARGUMENTS` ou pelo valor calculado no passo 0.

### 2. Para cada ticket encontrado, buscar detalhes

Para cada ticket, execute:

```bash
jira issue view <TICKET> --raw | jq '{
  key: .key,
  type: .fields.issuetype.name,
  created: .fields.created,
  summary: .fields.summary,
  summaryLength: (.fields.summary | length),
  description: .fields.description,
  descriptionLength: (.fields.description | length),
  priority: .fields.priority.name,
  status: .fields.status.name,
  assignee: (.fields.assignee.displayName // "Unassigned"),
  storyPoints: (.fields.customfield_10028 // null),
  components: [.fields.components[]?.name],
  activityType: (.fields.customfield_10464.value // "Uncategorized"),
  sprint: (.fields.customfield_10020 | if . and length > 0 then .[-1].name else null end),
  links: [.fields.issuelinks[]? | {
    direction: (if .outwardIssue then .type.outward else .type.inward end),
    key: (.outwardIssue.key // .inwardIssue.key),
    linkedSummary: (.outwardIssue.fields.summary // .inwardIssue.fields.summary),
    linkedStatus: (.outwardIssue.fields.status.name // .inwardIssue.fields.status.name)
  }]
}'
```

Note que `direction` já vem com o rótulo correto ("blocks" ou "is blocked by"), não apenas o nome genérico do tipo de link — isso é necessário para o passo 3.5.

### 3. Verificar duplicados

Para cada ticket, buscar possíveis duplicados baseado em palavras-chave do summary.

### 3.5. Verificar links e direção

Para cada ticket com links (`issuelinks`), aplique o critério **Links** definido em [criteria.md](criteria.md). Quando a direção precisar ser confirmada contra o conteúdo do ticket linkado (não apenas o summary), busque os detalhes completos do ticket linkado com o mesmo comando do passo 2.

### 4. Analisar cada ticket

Para cada ticket, aplique os critérios de análise definidos em [criteria.md](criteria.md). Não verifique epic — isso será feito pelo `/atribui-epics`.

### 5. Formato de saída

Use os templates definidos em [output-template.md](output-template.md) para:
- Análise individual de cada ticket
- Resumo executivo
- Flags para Tech Leads
- Sugestão de correções automáticas

## Regras

- Use o jira CLI para todas as operações
- Toda menção a um ticket em qualquer parte da saída (título da análise individual, Resumo Executivo, Flags para Tech Leads, observações sobre duplicados/dependências/links) deve usar o link completo em formato markdown `[HYPERFLEET-XXX](https://redhat.atlassian.net/browse/HYPERFLEET-XXX)` — nunca a chave nua (ex: `HYPERFLEET-XXX` sem link)
- Análise em português
- Seja objetivo nas recomendações
