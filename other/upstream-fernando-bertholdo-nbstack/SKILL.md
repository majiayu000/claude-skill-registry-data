---
name: generate-session-prompt
version: 4.0.0
description: Gerar prompt para retomada de desenvolvimento em nova sessão. Use quando sessão >150k tokens, ao retomar trabalho após pausa, ao trocar de ferramenta, ou em mudança de contexto. Aceita argumento de detalhe (brief, standard, detailed). Funciona em qualquer projeto — modo opinionated quando há `.planning/` na raiz, modo genérico caso contrário.
---

# Generate Session Prompt

Gera prompt para continuidade de trabalho em nova sessão, adaptando nível de detalhe ao contexto.

## Quando Usar

- Sessão atual >150k tokens (performance degradada)
- Retomar trabalho após pausa (dias/semanas)
- Trocar de ferramenta (ex: Cursor → Claude Code)
- Mudança de contexto (ex: finalizou um trabalho secundário, vai retomar o principal)
- Handoff de tarefas complexas com conclusões a preservar

## Níveis de Detalhe

A skill aceita um argumento que define a profundidade do prompt gerado:

| Nível | Invocação | Tokens | Quando Usar |
|-------|-----------|--------|-------------|
| **brief** | `generate-session-prompt brief` | 200-500 | Continuação imediata, mesmo contexto, próximo dia |
| **standard** | `generate-session-prompt` (default) | 800-1500 | Retomada após pausa, troca de ferramenta, complexidade moderada |
| **detailed** | `generate-session-prompt detailed` | 1500-3000+ | Handoff complexo, múltiplas tarefas pendentes, conclusões/análises a preservar |

### Quando usar cada nível

**brief** — Quando o contexto da próxima sessão é simples:
- Mesmo trabalho, continuando de onde parou
- Poucas tarefas restantes, caminho claro
- Sem análises ou conclusões a transportar

**standard** (default) — Para a maioria dos casos:
- Retomada após dias/semanas
- Troca de ferramenta (Cursor → Claude Code)
- Trabalho com progresso parcial e próximos passos claros
- Algumas decisões ou conclusões a registrar

**detailed** — Quando o prompt precisa carregar contexto rico:
- Múltiplas tarefas pendentes com sub-itens e pontos de atenção
- Conclusões de análises (monitoramento, arquitetura, roadmap) que a próxima sessão deve executar
- Handoff de sessão longa com descobertas técnicas (ex: APIs, convenções, bugs)
- Transição entre fases ou reconciliação de roadmap
- Quando o usuário pede "contexto completo" ou "prompt detalhado"

### Seleção automática (quando o usuário não especifica nível)

Se o usuário não indicar nível explicitamente, **inferir** com base no contexto:

```
Sessão curta + mesmo trabalho + poucas tarefas         → brief
Caso geral / sem indicação clara                       → standard
Sessão com análises, conclusões ou múltiplas tarefas   → detailed
Usuário pediu "contexto completo" ou similar           → detailed
```

## Princípios

1. **Contexto proporcional** — O detalhe do prompt deve ser proporcional à complexidade do handoff
2. **Referências @** — Facilita navegação do agente (links diretos a arquivos)
3. **Conclusões inline** — Carregar conclusões/análises no prompt quando a próxima sessão precisa agir sobre elas (nível standard e detailed)
4. **Tipo-agnóstico** — Funciona para qualquer tipo de trabalho. Em projetos com framework opinionado (`.planning/` presente), reconhece os tipos do framework; caso contrário, opera com tipos genéricos
5. **Skills contextuais** — Indicar skills relevantes para a próxima sessão

## Detecção de Modo

**Antes de qualquer coleta**, verifique se o diretório `.planning/` existe na raiz do projeto atual:

- **Existe `.planning/`** → use **MODE:opinionated-initiative** (vocabulário milestone/detour/ajuste/avulso, leitura de Roadmap/CONTEXT, templates específicos do framework)
- **Não existe `.planning/`** → use **MODE:generic** (vocabulário feature/bugfix/refactor/spike/misc, leitura de README/git/sessão, templates universais)

A detecção determina **apenas** o procedimento de coleta de contexto e o conjunto de templates. Os princípios, níveis de detalhe, regras gerais e validação são idênticos nos dois modos.

## Procedimento de Geração

1. **Detectar modo** (ver seção acima)
2. **Coletar estado atual** — segue o bloco do modo detectado (ver abaixo)
3. **Determinar nível de detalhe** — argumento explícito, ou inferir
4. **Gerar prompt** seguindo a estrutura do nível escolhido + template do tipo de trabalho do modo ativo
5. **Validar** contra o checklist do nível

---

<!-- MODE:opinionated-initiative start -->
## MODE:opinionated-initiative — Coleta e Templates

Use quando `.planning/` existe na raiz. Vocabulário e estrutura assumem o framework `tech-product-template`.

### Coleta (Procedimento passo 2)

```bash
1. Identificar tipo de trabalho
   - Ler .planning/README.md para identificar tipo (milestone / detour)
   - Se milestone → localizar .planning/milestones/MX.X-nome/
   - Se detour → localizar .planning/detours/<nome>/
   - Se avulso (sem vínculo) → verificar .planning/scratch/

2. Coletar estado atual
   - Resolver path do CONTEXT.md:
     a. Milestone: .planning/milestones/MX.X-*/CONTEXT.md (glob)
     b. Detour: .planning/detours/<nome>/CONTEXT.md
     c. Fallback legado: _archive/<id>/CONTEXT.md
     d. Se nada → prosseguir sem CONTEXT.md (usar Roadmap.md)
   - Ler CONTEXT.md resolvido (contexto vivo, se existir)
   - Ler a issue da iniciativa no rastreador: descrição, checkboxes de DoR/DoD e
     comentários de topo (veredito, decisão respondida, nota) — o que só existe
     na thread não chega ao prompt por arquivo nenhum (medido em 18/09/2026)
   - Ler Roadmap.md (milestone/fase atual, DoR/DoD)
   - Ler plans em .claude/plans/ (se existir)
   - Verificar últimos commits (git log --oneline -5)
   - Verificar git status (mudanças pendentes)
   - Ler Projeto.md (regras de negócio, se relevante)
   - Coletar conclusões/análises da sessão atual (se houver)
```

### Templates por Tipo de Trabalho

#### Milestone (qualquer nível)

**Abertura:** `Vamos continuar a implementação do milestone [ID] ([NOME]).`
**Referências obrigatórias:** Roadmap.md (DoR/DoD), CONTEXT.md da initiative
**Contexto:** Progresso quantitativo (X/Y tarefas, N% DoD), próxima tarefa, bloqueios
**Skills:** validate-dor, validate-dod, pre-commit-check, validate-testing

#### Detour (qualquer nível)

**Abertura:** `Vamos continuar o detour [NOME] (relacionado a [MILESTONES]).`
**Referências obrigatórias:** .planning/detours/<nome>/CONTEXT.md, Roadmap.md (seção Desvios)
**Contexto:** Fases do detour, entregas já concluídas, impacto em milestones futuros
**Skills:** pre-commit-check, organize-commits, update-docs

#### Ajuste de Roadmap / Documentação (qualquer nível)

**Abertura:** `Vamos continuar os ajustes de roadmap e documentação de [PROJETO].`
**Referências obrigatórias:** Roadmap.md, Projeto.md, .planning/README.md
**Contexto:** O que motivou os ajustes, quais milestones são afetados, decisões a registrar
**Skills:** update-docs, validate-docs-links, audit-architecture

#### Troubleshooting (qualquer nível)

**Abertura:** `Vamos resolver o issue [DESCRIÇÃO] no contexto de [INICIATIVA].`
**Referências obrigatórias:** Arquivo com erro, log/evidência, CONTEXT.md da iniciativa
**Contexto:** Sintoma, esperado, tentativas anteriores, impacto
**Skills:** pre-commit-check, validate-testing

#### Trabalho Avulso / Sem Milestone (qualquer nível)

**Abertura:** `Vamos trabalhar em [DESCRIÇÃO] no projeto [PROJETO].`
**Referências:** .planning/scratch/<slug>-CONTEXT.md (se existir), arquivos relevantes
**Contexto:** Motivação, escopo, relação com roadmap (se houver)

### Exemplos de Formato (modo opinionated)

#### Brief (200-500 tokens)

```markdown
Vamos continuar o desenvolvimento de [PROJETO]
na [TIPO: milestone|detour|ajuste] [ID] ([NOME]).

**Referências principais:**
- @[arquivo1] (contexto sobre X)
- @[arquivo2] (tarefas e checklist)
- @[arquivo3] (se aplicável)

**Objetivo:** [Descrição concisa — 1 frase]

**Contexto atual:**
- [Progresso — N% ou X/Y tarefas]
- [Estado — o que foi feito]
- [Próximo — o que falta]

**Por favor:**
1. [Tarefa 1]
2. [Tarefa 2]
3. [Tarefa 3]
4. [Tarefa 4 — atualizar docs/tracking]
```

#### Standard (800-1500 tokens — default)

```markdown
Vamos continuar o desenvolvimento de [PROJETO]
na [TIPO] [ID] ([NOME]). [1 frase de contexto situacional]

**Referências principais:**
- @[arquivo1] (contexto — detalhe)
- @[arquivo2] (tarefas — detalhe)
- @[arquivo3] (plano/evidência — detalhe)
- ... (até 8 refs)

**Objetivo:** [Descrição — 1-2 frases]

**Contexto atual:**
- [Progresso quantitativo]
- [Estado das entregas]
- [Decisões pendentes ou recentes]
- [Bloqueios/dependências se houver]

**Conclusões da sessão anterior:** (se aplicável)
- [Conclusão 1 — resumo]
- [Conclusão 2 — resumo]
- [Impacto/próximos passos derivados]

**Por favor:**
1. [Tarefa 1 — com contexto mínimo]
2. [Tarefa 2 — com skill sugerida]
3. [Tarefa 3 — com critério de completude]
4. [Tarefa 4 — atualizar docs/tracking]
```

#### Detailed (1500-3000+ tokens)

```markdown
Vamos continuar o desenvolvimento de [PROJETO]
com foco em [DESCRIÇÃO DO FOCO]. [2-3 frases de contexto situacional]

**Referências principais:**
- @[arquivo1] (detalhe)
- @[arquivo2] (detalhe)
- ... (todas as referências relevantes, sem limite)

**Objetivo:** [Parágrafo descrevendo o objetivo principal e sub-objetivos]

---

### Contexto: [Frente/Iniciativa 1]

[Parágrafo descrevendo estado, progresso, entregas]
[Dados quantitativos: commits, testes, cobertura]
[Referências a evidências]

---

### TAREFA A — [Nome da tarefa]

**Conclusão da análise anterior:**
- [Ponto 1 — com justificativa]
- [Ponto 2 — com alternativas descartadas]
- [Ponto 3 — com recomendação]

**Ação sugerida:**
1. [Sub-ação 1 — detalhada]
2. [Sub-ação 2 — detalhada]
3. [Sub-ação 3 — detalhada]

---

### TAREFA B — [Nome da tarefa]

**Pontos de atenção identificados:**

**Ponto 1: [Título]**
- Estado real: [descrição]
- Ação: [o que fazer]

**Ponto 2: [Título]**
- Estado real: [descrição]
- Ação: [o que fazer]

(... quantos pontos forem necessários)

---

**Por favor:**
1. [Tarefa consolidada 1 — com referências]
2. [Tarefa consolidada 2 — com skills sugeridas]
3. [Tarefa consolidada 3 — com critérios de completude]
4. [Tarefa consolidada 4 — com referências a seções acima]
5. [Tarefa consolidada N — atualizar docs/tracking]
```

### Referências (modo opinionated)

- `.planning/README.md` — Hub: mapeamento milestone→initiative, tipos de trabalho
- `.planning/milestones/MX.X-nome/CONTEXT.md` — Contexto vivo de milestone
- `.planning/detours/<nome>/CONTEXT.md` — Contexto vivo de detour
- `.planning/scratch/` — Context dumps avulsos (sem milestone)
- `documents/core/Roadmap.md` — Milestones, desvios, DoR/DoD
- `documents/core/Projeto.md` — Regras de negócio e decisões
- `CLAUDE.md` — Regras operacionais

### Skills Relacionadas (modo opinionated)

- `fresh-context` — Gerar CONTEXT.md para handoff (complementar: context file vs. prompt)
- `validate-dor` — Validar DoR antes de iniciar milestone
- `validate-dod` — Validar DoD antes de fechar milestone
- `update-docs` — Atualizar documentação (Projeto/Roadmap)
- `pre-commit-check` — Qualidade antes de commit
<!-- MODE:opinionated-initiative end -->

---

<!-- MODE:generic start -->
## MODE:generic — Coleta e Templates

Use quando `.planning/` **não** existe na raiz. Vocabulário e estrutura são universais — funcionam em qualquer projeto, independente de framework.

### Coleta (Procedimento passo 2)

```bash
1. Identificar tipo de trabalho
   - Olhar a sessão atual: o que foi discutido, código tocado, problema sendo resolvido
   - Verificar branch atual (git branch --show-current)
     a. Padrões nominais ajudam: feat/* → feature; fix/* → bugfix;
        refactor/* → refactor; spike/* → spike
   - Se ambíguo, classificar como "misc" e seguir

2. Coletar estado do projeto
   - Ler README.md (visão geral, comandos, stack)
   - Ler manifest principal se existir (package.json, pyproject.toml, Cargo.toml,
     go.mod, etc. — para entender stack e scripts)
   - git log --oneline -10 (últimos commits — narrativa do trabalho recente)
   - git status (mudanças pendentes não commitadas)
   - git diff HEAD --stat (escopo das mudanças não commitadas, se houver)
   - Se o projeto tem rastreador de issues: a issue do trabalho corrente
     (descrição, checkboxes, comentários de topo) — decisão que vive só na
     thread não chega ao prompt por arquivo nenhum
   - Listar arquivos modificados nas últimas 48h:
     find . -type f -mtime -2 -not -path './.git/*' -not -path './node_modules/*' \
       -not -path './.next/*' -not -path './dist/*' -not -path './build/*' 2>/dev/null | head -20

3. Coletar contexto da sessão atual (CRÍTICO)
   - O que o usuário pediu, o que foi entregue, o que ficou pendente
   - Decisões tomadas e o porquê
   - Análises ou descobertas técnicas relevantes (APIs, bugs, convenções)
   - Bloqueios encontrados e como foram contornados (ou não)
```

### Templates por Tipo de Trabalho

#### Feature / Initiative (qualquer nível)

**Abertura:** `Vamos continuar a implementação de [FEATURE] em [PROJETO].`
**Referências obrigatórias:** README.md, arquivos principais da feature, branch atual
**Contexto:** O que está pronto, o que falta, próxima tarefa concreta
**Skills sugeridas:** organize-commits, pre-commit-check (se existirem)

#### Bug fix / Investigation (qualquer nível)

**Abertura:** `Vamos resolver [BUG/ISSUE] em [PROJETO].`
**Referências obrigatórias:** Arquivo onde o bug se manifesta, log/stack trace, teste reproduzindo (se houver)
**Contexto:** Sintoma, comportamento esperado, hipóteses já testadas, impacto
**Skills sugeridas:** systematic-debugging (se disponível)

#### Refactor / Cleanup / Docs (qualquer nível)

**Abertura:** `Vamos continuar o refactor/limpeza de [ÁREA] em [PROJETO].`
**Referências obrigatórias:** Arquivos sendo refatorados, testes correspondentes, docs afetadas
**Contexto:** Motivação (debt, performance, clareza), escopo definido, restrições, reversibilidade
**Skills sugeridas:** simplify, code-review

#### Spike / Exploração (qualquer nível)

**Abertura:** `Vamos continuar a exploração de [TEMA/QUESTÃO] em [PROJETO].`
**Referências obrigatórias:** Notas/scratch da exploração (se existirem), código de prova de conceito
**Contexto:** Pergunta sendo respondida, alternativas já avaliadas, critério de sucesso da exploração
**Skills sugeridas:** brainstorming (se disponível)

#### Misc / Trabalho Avulso (qualquer nível)

**Abertura:** `Vamos continuar o trabalho em [DESCRIÇÃO] em [PROJETO].`
**Referências:** Arquivos relevantes identificados na sessão
**Contexto:** O que motivou, o que foi feito, o que falta

### Exemplos de Formato (modo genérico)

#### Brief (200-500 tokens)

```markdown
Vamos continuar a [TIPO: implementação|correção|refactor|exploração]
de [DESCRIÇÃO] em [PROJETO].

**Referências principais:**
- @[arquivo1] (contexto sobre X)
- @[arquivo2] (código sendo tocado)
- @[arquivo3] (teste/evidência se aplicável)

**Objetivo:** [Descrição concisa — 1 frase]

**Contexto atual:**
- Branch: [nome] — [progresso resumido]
- [O que foi feito na sessão anterior — 1 bullet]
- [Próximo passo concreto — 1 bullet]

**Por favor:**
1. [Tarefa 1]
2. [Tarefa 2]
3. [Tarefa 3]
```

#### Standard (800-1500 tokens — default)

```markdown
Vamos continuar a [TIPO] de [DESCRIÇÃO] em [PROJETO].
[1 frase de contexto situacional — o que está acontecendo]

**Referências principais:**
- @[arquivo1] (contexto — detalhe)
- @[arquivo2] (código sendo tocado — detalhe)
- @[arquivo3] (teste/evidência — detalhe)
- ... (5-8 refs)

**Objetivo:** [Descrição — 1-2 frases]

**Contexto atual:**
- Branch: [nome]
- Últimos commits: [resumo de 1-3 commits relevantes]
- Mudanças pendentes: [arquivos com diff não commitado, se houver]
- [Estado do trabalho — bullet]
- [Decisões tomadas/pendentes — bullet]
- [Bloqueios se houver]

**Conclusões da sessão anterior:** (se aplicável)
- [Conclusão 1 — resumo]
- [Conclusão 2 — resumo]
- [Próximo passo derivado]

**Por favor:**
1. [Tarefa 1 — com contexto mínimo]
2. [Tarefa 2 — com critério de completude]
3. [Tarefa 3 — atualizar testes/docs se aplicável]
4. [Tarefa 4 — commit/PR conforme padrão do projeto]
```

#### Detailed (1500-3000+ tokens)

```markdown
Vamos continuar [TIPO] de [DESCRIÇÃO] em [PROJETO]
com foco em [FOCO]. [2-3 frases de contexto situacional]

**Referências principais:**
- @[arquivo1] (detalhe)
- @[arquivo2] (detalhe)
- ... (todas as referências relevantes, sem limite)

**Objetivo:** [Parágrafo descrevendo objetivo e sub-objetivos]

---

### Contexto do projeto

[Parágrafo: o que é o projeto, stack, convenções relevantes que a próxima sessão precisa saber]
[Branch atual, narrativa dos últimos commits, escopo do diff pendente]

---

### TAREFA A — [Nome da tarefa]

**Conclusão da análise anterior:**
- [Ponto 1 — com justificativa]
- [Ponto 2 — alternativas descartadas]
- [Ponto 3 — recomendação]

**Ação sugerida:**
1. [Sub-ação 1 — detalhada]
2. [Sub-ação 2 — detalhada]

---

### TAREFA B — [Nome da tarefa]

**Pontos de atenção identificados:**

**Ponto 1: [Título]**
- Estado real: [descrição]
- Ação: [o que fazer]

**Ponto 2: [Título]**
- Estado real: [descrição]
- Ação: [o que fazer]

---

**Por favor:**
1. [Tarefa consolidada 1 — com referências]
2. [Tarefa consolidada 2 — com critério de completude]
3. [Tarefa consolidada N — commit/PR conforme padrão]
```

### Skills Relacionadas (modo genérico)

- `simplify` — Refinar código para clareza após mudanças
- `commit-commands:commit` — Criar commits estruturados
- `code-review` — Revisar mudanças antes de PR
- `superpowers:systematic-debugging` — Debug metódico para bugs persistentes
- `superpowers:brainstorming` — Explorar opções antes de implementar
<!-- MODE:generic end -->

---

## Regras de Geração

### SEMPRE:

1. Adaptar detalhe ao nível solicitado/inferido
2. Usar referências @ (facilita navegação do agente)
3. Incluir métricas quando disponíveis (progresso %, coverage, commits)
4. Referenciar skills aplicáveis à próxima sessão (do conjunto do modo ativo)
5. Incluir conclusões/análises inline quando a próxima sessão precisa agir sobre elas
6. Identificar tipo de trabalho (usando os tipos do modo ativo)
7. Incluir validações e critérios de completude

### NUNCA:

1. Incluir histórico completo da sessão (resumir, não copiar)
2. Duplicar conteúdo extenso dos arquivos referenciados (resumir e apontar)
3. Usar descrições genéricas ("continue o trabalho")
4. Omitir referências aos arquivos principais
5. Forçar formato/vocabulário do modo errado (não usar "milestone" sem `.planning/`; não usar "feature" como abertura quando há milestone ativo)
6. Ignorar conclusões/análises relevantes da sessão atual em níveis standard/detailed
7. Misturar templates dos dois modos no mesmo prompt

## Estrutura por Nível (universal)

### Brief (200-500 tokens)

**Seções:**
- Linha de abertura (do template do tipo de trabalho do modo ativo)
- Referências (3-5)
- Objetivo (1 linha)
- Contexto atual (3-5 bullets)
- Tarefas (3-4 ações)

### Standard (800-1500 tokens — default)

**Seções:**
- Linha de abertura (do template do tipo + 1 frase de contexto)
- Referências (5-8)
- Objetivo (1-2 frases)
- Contexto/Progresso (5-8 bullets, organizados por tema)
- Decisões/Conclusões relevantes (se houver — 2-5 bullets)
- Tarefas (4-6 ações com sub-detalhes quando necessário)
- Skills sugeridas

### Detailed (1500-3000+ tokens)

**Seções:**
- Linha de abertura (do template do tipo)
- Referências (sem limite arbitrário — todas as relevantes)
- Objetivo + sub-objetivos
- Contexto expandido (situação, progresso, estado de cada frente)
- Seções por tarefa/frente pendente com:
  - Conclusões/análises da sessão (inline, não referenciadas)
  - Pontos de atenção identificados
  - Ações sugeridas com detalhes
- Tarefas consolidadas (lista final acionável)
- Skills e validações

## Validação por Nível

### Brief

- [ ] Tokens: 200-500
- [ ] Referências: 3-5
- [ ] Objetivo: 1 frase clara
- [ ] Contexto: 3-5 bullets
- [ ] Tarefas: 3-4 ações específicas
- [ ] Tipo de trabalho identificado (modo ativo)

### Standard

- [ ] Tokens: 800-1500
- [ ] Referências: 5-8
- [ ] Objetivo: 1-2 frases
- [ ] Contexto: 5-8 bullets organizados
- [ ] Conclusões: inline se houver (2-5 bullets)
- [ ] Tarefas: 4-6 ações com sub-detalhes
- [ ] Skills sugeridas (do modo ativo)
- [ ] Tipo de trabalho identificado

### Detailed

- [ ] Tokens: 1500-3000+
- [ ] Referências: todas as relevantes (sem limite)
- [ ] Objetivo: parágrafo com sub-objetivos
- [ ] Contexto: expandido por frente/iniciativa
- [ ] Conclusões/Análises: seções dedicadas por tarefa
- [ ] Pontos de atenção: listados com estado real + ação
- [ ] Tarefas: consolidadas com referências às seções
- [ ] Skills e validações sugeridas
- [ ] Tipo de trabalho identificado

## Fluxo de Uso

### Cenário 1: Continuação simples

```bash
generate-session-prompt brief
```

### Cenário 2: Retomada após pausa

```bash
generate-session-prompt
# Gera prompt standard (default)
```

### Cenário 3: Handoff complexo

```bash
generate-session-prompt detailed
# Prompt carrega conclusões, pontos de atenção, ações detalhadas
```

### Cenário 4: Troca de ferramenta

```bash
# Cursor → Claude Code (precisa contexto suficiente)
generate-session-prompt
# ou detailed se houver muito contexto a preservar
```

### Cenário 5: Projeto sem framework

```bash
# Projeto sem .planning/ — modo genérico ativado automaticamente
generate-session-prompt
# Lê README, git log, git status, contexto da sessão
```

## Troubleshooting

### Problema: Prompt muito genérico

**Causa:** Tipo de trabalho não identificado, ou modo errado, ou contexto da sessão pobre
**Solução:** Em modo opinionated, atualizar o CONTEXT.md da iniciativa antes; em modo genérico, garantir que a sessão tem decisões/análises explícitas

### Problema: Prompt detalhado quando queria conciso

**Causa:** Inferência automática optou por mais detalhe
**Solução:** Usar argumento explícito: `generate-session-prompt brief`

### Problema: Conclusões da sessão não aparecem no prompt

**Causa:** Nível brief não inclui conclusões; ou sessão não teve análises explícitas
**Solução:** Usar nível standard ou detailed

### Problema: Referências quebradas

**Causa:** Arquivos movidos ou renomeados
**Solução:** Em modo opinionated, executar `validate-docs-links`; em modo genérico, validar manualmente os caminhos

### Problema: Modo errado detectado

**Causa:** `.planning/` existe mas o trabalho é genérico (ou vice-versa)
**Solução:** Hoje a detecção é binária pela presença de `.planning/`. Se necessário, edite o prompt gerado para misturar — porém isso indica que o framework do projeto está mal-definido (considere mover o trabalho ad-hoc para `.planning/scratch/`)

---

## Changelog

### v4.0.0 (28/Abril/2026)

**Refactor para modo dual (opinionated + generic):**
- Adicionada detecção automática de modo via presença de `.planning/` na raiz
- Bloco `MODE:opinionated-initiative` preserva integralmente o comportamento v3.0.0
  (vocabulário milestone/detour/patch/ajuste/avulso, leitura de Roadmap/CONTEXT)
- Novo bloco `MODE:generic` para projetos sem framework opinionado: vocabulário
  feature/bugfix/refactor/spike/misc, coleta via README + git log + git status +
  contexto da sessão
- Princípios, níveis de detalhe, regras gerais e validação são universais
- Templates por tipo movidos para dentro dos blocos de modo
- Sentinelas `<!-- MODE:X start -->` / `<!-- MODE:X end -->` delimitam cada bloco
  para facilitar manutenção e syncs futuros
- Versão movida para o frontmatter
- **Compatibilidade:** projetos que usam o template (com `.planning/`) não veem
  diferença alguma — modo opinionated é selecionado automaticamente

**Motivação:** Permitir uso da skill em qualquer projeto, viabilizando empacotamento
como plugin no marketplace `4-successful-AI-life`. Sem este refactor, a skill
produziria output esquisito em projetos sem `.planning/`.

### v3.0.0 (19/Fevereiro/2026)

**Evolução para níveis de detalhe dinâmicos:**
- Três níveis: brief (200-500 tokens), standard (800-1500, default), detailed (1500-3000+)
- Substituição de "formato obrigatório" por guidelines flexíveis por nível
- Suporte a iniciativa-agnóstico (milestone, detour, patch, ajuste, avulso)
- Templates por tipo de trabalho (5 tipos vs. 4 milestone-only anteriores)
- Procedimento expandido para cobrir todos os tipos de .planning/
- Conclusões/análises inline nos níveis standard e detailed
- Remoção do hard cap de 250 tokens e limites fixos de referências/tarefas
- Inferência automática de nível quando não especificado
- Validação por nível (checklists separados)

**Autor:** Fernando Bertholdo
**Contexto:** Feedback de uso real — prompts curtos demais perdiam contexto de análises,
formato milestone-only não cobria detours e ajustes de roadmap

### v2.0.0 (27/Janeiro/2026)

- Criação dos templates por tipo (Planejamento, Implementação, Testes, Troubleshooting)
- Integração com skills (validate-dor, validate-dod, etc.)
- Limite de 250 tokens

### v1.0.0 (22/Janeiro/2026)

- Criação inicial
