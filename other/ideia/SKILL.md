---
name: ideia
description: Analyze any input (GitHub repo, Instagram reel, YouTube video, article, link, idea description) and evaluate what can be extracted, adapted, or integrated into DME Technology projects or global config.
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Grep Glob WebFetch WebSearch
argument-hint: <link-ou-descricao>
---

# Analisador de Ideias — DME Technology

Você recebeu uma ideia, link, ou referência. Seu trabalho é analisar e recomendar o que fazer com isso.

## Input recebido

$ARGUMENTS

## Processo

### Passo 1 — Identificar o tipo de input

Detecte o que foi recebido:

| Tipo | Como detectar | Como processar |
|------|---------------|----------------|
| **GitHub repo** | URL contém github.com | Clonar info via `gh api`, ler README, analisar estrutura |
| **YouTube video** | URL contém youtube.com ou youtu.be | Buscar transcrição/resumo via WebSearch |
| **Instagram reel** | URL contém instagram.com | Buscar contexto via WebSearch sobre o conteúdo |
| **Artigo/Blog** | URL genérica | Fetch conteúdo via WebFetch |
| **Ideia em texto** | Sem URL | Analisar direto |
| **Arquivo local** | Path de arquivo | Ler o arquivo |

### Passo 2 — Extrair o valor

Responda:
1. **O que é isso?** (1 parágrafo)
2. **O que tem de útil?** (tecnologia, padrão, UI, ideia de negócio, ferramenta, workflow)
3. **Qualidade** (1-10): vale o tempo de integrar?

### Passo 3 — Recomendar ação

Classifique em UMA das categorias:

#### A) Integrar como Plugin/Skill/Agent (global)
Melhora o Claude Code pra TODOS os projetos.
- Exemplo: "Esse repo tem um agent de code review melhor que o nosso"
- Ação: explicar o que copiar/adaptar e onde colocar em `~/.claude/`

#### B) Usar em projeto específico
Serve pra um ou mais projetos da DME.
- Dizer QUAL projeto em `~/Desktop/dme/projects/` se beneficia
- Ação: explicar como integrar no projeto

#### C) Inspiração para projeto novo
É uma ideia que pode virar um produto/serviço da DME.
- Ação: sugerir criar pasta em `/projects/` e usar `/new-project`

#### D) Referência para aprendizado
Não é pra integrar, mas vale estudar.
- Ação: salvar na memória como referência

#### E) Não vale a pena
Baixa qualidade, já temos algo melhor, ou não se aplica.
- Ação: explicar por que e sugerir alternativa se existir

### Passo 4 — Output

```
═══════════════════════════════════════
  ANÁLISE DE IDEIA — DME Technology
═══════════════════════════════════════

Input: [tipo] — [título/descrição curta]
Qualidade: [N/10]
Categoria: [A/B/C/D/E] — [nome da categoria]

O que é:
[1 parágrafo]

O que tem de útil:
[bullets com o valor extraído]

Recomendação:
[ação concreta: o que fazer, onde colocar, qual projeto]

Próximo passo:
[comando exato ou ação que Henrique deve tomar]
═══════════════════════════════════════
```

### Passo 5 — Salvar na memória

Se a qualidade for >= 7, salvar via `memory_store` com tags relevantes para consulta futura.
Se for categoria A (global), já perguntar se quer que eu implemente agora.
