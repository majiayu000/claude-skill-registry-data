---
name: gerar-quiz-rag
description: "Gerador e executor de quiz sobre conhecimento RAG. Comandos: '/gerar-quiz-rag gerar' para gerar perguntas do banco RAG e salvar em JSON, '/gerar-quiz-rag iniciar' para executar quiz de 10 perguntas, '/gerar-quiz-rag status' para ver progresso. Claude consulta o banco SQLite RAG e gera perguntas diretamente."
---

# Quiz RAG - Skill do Claude Code

## ⚠️ IMPORTANTE: Nome Completo Qualificado

Ao invocar este skill via **Skill tool** (não via comando do usuário), você DEVE usar o **nome completo qualificado**:

```
✅ CORRETO: skill: "gerar-quiz-rag:gerar-quiz-rag"
❌ ERRADO:  skill: "gerar-quiz-rag"
```

**Por quê?**
- O nome curto `gerar-quiz-rag` pode causar erro: `Unknown skill: gerar-quiz-rag`
- O sistema requer o formato completo: `<namespace>:<skill-name>`
- Para este skill: `gerar-quiz-rag:gerar-quiz-rag`

**Quando usar:**
- Quando Claude invoca o skill programaticamente via Skill tool
- Quando há necessidade de desambiguação entre skills com nomes similares

**Comandos do usuário (continuam funcionando normalmente):**
- `/gerar-quiz-rag gerar 30` ✅
- `/gerar-quiz-rag iniciar` ✅
- `/gerar-quiz-rag status` ✅

---

## Visão Geral

Esta skill permite ao Claude:
1. **Gerar perguntas** consultando o banco de dados RAG (SQLite) e salvando em JSON
2. **Executar quizzes** de 10 perguntas com feedback imediato
3. **Gerenciar banco** de perguntas em formato JSON puro

**IMPORTANTE:** Claude gera as perguntas consultando o banco RAG SQLite diretamente.

## Comandos da Skill

### `/gerar-quiz-rag gerar [quantidade]`
Gera perguntas consultando o banco RAG e salva no JSON.

**MÉTODO PADRÃO: SUBAGENTS EM PARALELO** ⚡

**IMPORTANTE: SEMPRE usar subagents para máxima velocidade e qualidade!**

Exemplos:
- `/gerar-quiz-rag gerar` → 10 perguntas (1 subagent)
- `/gerar-quiz-rag gerar 50` → 50 perguntas (5 subagents paralelos)
- `/gerar-quiz-rag gerar 100` → 100 perguntas (10 subagents paralelos)
- `/gerar-quiz-rag gerar 200` → 200 perguntas (20 subagents paralelos) ⚡
- `/gerar-quiz-rag gerar completo` → Máximo possível (~250 perguntas, 25 subagents)

**Processo com Subagents (PADRÃO):**
1. **CRIAR PASTA** (se não existir): `mkdir -p temp-lotes/`
2. Calcular número de lotes: `quantidade / 10` (10 perguntas por lote)
3. Distribuir chunks entre lotes (59 chunks / N lotes)
4. Lançar N subagents EM PARALELO usando `Task` tool
5. Cada subagent:
   a. Consulta SQLite: `regulamento.db` chunks específicos
   b. Gera 10 perguntas REAIS do conteúdo
   c. ⚠️ **CRÍTICO**: Salva em `/Users/2a/.claude/skills/gerar-quiz-rag/temp-lotes/temp-lote-N.json`
      - ❌ NUNCA salvar na raiz da skill!
      - ✅ SEMPRE em temp-lotes/temp-lote-N.json
6. Aguardar todos os subagents concluírem (~1-2 minutos)
7. Executar `python3 coletar-e-merge-final.py` para merge automático
8. Resultado em `banco-perguntas.json` (validado, sem duplicatas)
9. Limpar `temp-lotes/` (opcional)

### `/gerar-quiz-rag iniciar [modo]`
Executa quiz de 10 perguntas.

**Modos:**
- `novo` - Gera 10 perguntas novas do banco RAG
- `aleatorio` - Sorteia 10 do banco JSON existente
- `teste` - Modo teste com respostas marcadas (⭐)

### `/gerar-quiz-rag status`
Mostra progresso atual do banco de perguntas.

## Banco de Perguntas (JSON Local)

As perguntas são armazenadas em arquivo JSON local na própria skill.

### Arquivo Principal
- **Localização**: `/Users/2a/.claude/skills/gerar-quiz-rag/banco-perguntas.json`
- **Formato**: JSON estruturado com metadata e array de perguntas
- **Gerenciado por**: Claude diretamente (lê e escreve via ferramentas Read/Write)

### Arquivos Temporários
- **Localização**: `/Users/2a/.claude/skills/gerar-quiz-rag/temp-lotes/`
- **Arquivos**: `temp-lote-1.json`, `temp-lote-2.json`, etc.
- **Uso**: Lotes individuais quando gerado com subagents paralelos
- **Limpeza**: Podem ser apagados após merge em `banco-perguntas.json`

### Schema do JSON (OBRIGATÓRIO)

**CAMPOS PERMITIDOS (apenas estes):**

```json
{
  "metadata": {
    "total_perguntas": 10,
    "ultima_atualizacao": "2026-01-04T20:00:00.000000",
    "fonte": "regulamento.db"
  },
  "perguntas": [
    {
      "numero": 1,
      "texto": "Qual a idade mínima para participar?",
      "alternativas": {
        "A": {
          "texto": "16 anos",
          "correta": false,
          "explicacao": "Incorreto. Idade mínima é 18 anos."
        },
        "B": {
          "texto": "18 anos",
          "correta": true,
          "explicacao": "Correto! Conforme regulamento."
        },
        "C": { "texto": "...", "correta": false, "explicacao": "..." },
        "D": { "texto": "...", "correta": false, "explicacao": "..." }
      },
      "dificuldade": "facil",
      "topico": "Elegibilidade",
      "fonte_chunk": "chunk_0"
    }
  ]
}
```

**⚠️ CAMPOS PROIBIDOS (NUNCA incluir):**
- ❌ `item_regulamento` (dentro de pergunta)
- ❌ `referencia_fonte` (dentro de pergunta)
- ❌ `secao` (dentro de pergunta)
- ❌ `regulamento_ref` (dentro de alternativas)

**✅ FORMATO CORRETO do `fonte_chunk`:**
- ✅ `"chunk_0"` - índice do chunk no banco RAG
- ✅ `"chunk_5"` - outro exemplo
- ❌ Não usar `regulamento_ref` aqui

## 🚀 Geração com Subagents (MÉTODO PADRÃO)

### Por Que Subagents?

✅ **10-15x mais rápido** que método sequencial
✅ **Máxima qualidade** - Perguntas reais e específicas
✅ **Paralelização** - Múltiplos agentes trabalhando ao mesmo tempo
✅ **Validação automática** - Merge detecta e remove duplicatas

### Template de Prompt para Cada Subagent:

```
Gere 10 perguntas de MÚLTIPLA ESCOLHA (A,B,C,D) do banco RAG.

**Banco**: /Users/2a/.claude/skills/gerar-quiz-rag/fonte-da-verdade-rag/regulamento.db
**Chunks**: X a Y
**Numeração**: N a N+9
**Arquivo**: /Users/2a/.claude/skills/gerar-quiz-rag/temp-lotes/temp-lote-Z.json

⚠️ CRÍTICO: Use caminho COMPLETO e ABSOLUTO para o arquivo!
   CORRETO: /Users/2a/.claude/skills/gerar-quiz-rag/temp-lotes/temp-lote-Z.json ✅
   ERRADO: temp-lote-Z.json (vai salvar na raiz!) ❌

FORMATO EXATO (array JSON):
[
  {
    "numero": N,
    "texto": "Pergunta específica baseada no chunk?",
    "alternativas": {
      "A": {"texto": "Opção", "correta": false, "explicacao": "Razão"},
      "B": {"texto": "Opção", "correta": true, "explicacao": "Razão"},
      "C": {"texto": "Opção", "correta": false, "explicacao": "Razão"},
      "D": {"texto": "Opção", "correta": false, "explicacao": "Razão"}
    },
    "dificuldade": "facil|media|dificil",
    "topico": "Tópico Específico",
    "fonte_chunk": "chunk_X"
  }
]

PASSOS:
1. sqlite3 regulamento.db "SELECT conteudo FROM chunks WHERE chunk_index BETWEEN X AND Y;"
2. Leia conteúdo REAL
3. Gere 10 perguntas ESPECÍFICAS
4. Salve array JSON em temp-lotes/
```

### Distribuição de Chunks (para 200 perguntas):

| Lote | Chunks | Perguntas | Arquivo |
|------|--------|-----------|---------|
| 1-20 | 0-58 (~3 chunks cada) | 10 cada | temp-lotes/temp-lote-N.json |

### Após Gerar os Lotes:

```bash
python3 coletar-e-merge-final.py
```

Resultado: `banco-perguntas.json` com todas as perguntas validadas e sem duplicatas!

---

## Instruções para o Claude

**⚠️ LEMBRETE:** Se você precisar invocar este skill via Skill tool, use o nome completo qualificado: `gerar-quiz-rag:gerar-quiz-rag` (não apenas `gerar-quiz-rag`).

### Quando `/gerar-quiz-rag gerar` for invocado:

**⚡ IMPORTANTE: SEMPRE USE SUBAGENTS EM PARALELO!**

**PASSO 0: Usar Subagents (OBRIGATÓRIO)**

1. **CRIAR PASTA**: `mkdir -p temp-lotes/`

2. **Calcular distribuição**:
   - Lotes: `quantidade_solicitada / 10`
   - Chunks por lote: 59 / num_lotes (normalmente 3 chunks/lote)

3. **Para CADA lote (1 a N)**, lançar subagent com este prompt COMPLETO:

```
Gere 10 perguntas de múltipla escolha do banco RAG.

BANCO: /Users/2a/.claude/skills/gerar-quiz-rag/fonte-da-verdade-rag/regulamento.db
CHUNKS: X, X+1, X+2
PERGUNTAS: N a N+9
SALVAR EM: /Users/2a/.claude/skills/gerar-quiz-rag/temp-lotes/temp-lote-Z.json

EXEMPLO DE 1 PERGUNTA (siga EXATAMENTE este formato):
{
  "numero": 1,
  "texto": "Qual idade mínima para pessoa física no Renda Extra conforme item 3.1?",
  "alternativas": {
    "A": {
      "texto": "16 anos",
      "correta": false,
      "explicacao": "Incorreto. Item 3.1 estabelece 18 anos."
    },
    "B": {
      "texto": "18 anos",
      "correta": true,
      "explicacao": "Correto! Item 3.1 define idade mínima de 18 anos."
    },
    "C": {
      "texto": "21 anos",
      "correta": false,
      "explicacao": "Incorreto. É 18 anos conforme item 3.1."
    },
    "D": {
      "texto": "25 anos",
      "correta": false,
      "explicacao": "Incorreto. Idade mínima é 18 anos."
    }
  },
  "dificuldade": "facil",
  "topico": "Elegibilidade",
  "fonte_chunk": "chunk_0"
}

REGRAS CRÍTICAS:
✅ Use "alternativas" (NÃO "opcoes", NÃO "options")
✅ Cada alternativa: {"texto": "...", "correta": boolean, "explicacao": "..."}
✅ Apenas 1 alternativa com correta: true
✅ Retorne array: [ {pergunta1}, {pergunta2}, ... ]
✅ NÃO envolva em {"perguntas": [...]}

PASSOS:
1. cd /Users/2a/.claude/skills/gerar-quiz-rag
2. Consulte chunks: sqlite3 fonte-da-verdade-rag/regulamento.db "SELECT conteudo FROM chunks WHERE chunk_index BETWEEN X AND X+2;"
3. Gere 10 perguntas REAIS
4. Write("temp-lotes/temp-lote-Z.json", array_json)
```

4. **Aguardar** todos terminarem (~2 min)

5. **Executar merge**: `python3 coletar-e-merge-final.py`
   - Move automaticamente JSONs soltos para temp-lotes/
   - Valida formato
   - Remove duplicatas
   - Gera banco-perguntas.json final

6. **Validar**: `jq '.metadata' banco-perguntas.json`

**NÃO USE MÉTODO MANUAL/SEQUENCIAL** (lento e ineficiente)

---

**PASSO 1 (Apenas para referência): Consultar banco RAG**
1. Subagents farão isso automaticamente com `sqlite3` em `regulamento.db`
2. Comando SQL para ler chunks:
   ```sql
   SELECT chunk_index, conteudo FROM chunks WHERE doc_id = 1 ORDER BY chunk_index;
   ```
3. Usar ferramenta `Read` para ler `/Users/2a/.claude/skills/gerar-quiz-rag/banco-perguntas.json` (se existir)
4. Analisar perguntas existentes para evitar duplicatas

**PASSO 1.5: Pré-processar texto dos chunks** 🧹 LIMPEZA OBRIGATÓRIA

**PROBLEMA:** Chunks do RAG contêm formatação com ruído (espaços duplos, caracteres especiais).

**SOLUÇÃO:** Antes de gerar perguntas, SEMPRE normalizar o texto:

```python
# Aplicar estas transformações NO TEXTO DOS CHUNKS:
1. Remover espaços múltiplos → espaço único
   "Renda  Extra" → "Renda Extra"

2. Normalizar aspas especiais → aspas normais
   "ˮ" → '"'

3. Remover espaços antes de pontuação
   " ." → "."
   " ," → ","

4. Normalizar quebras de linha
   Múltiplas → única

5. Remover caracteres de controle/unicode indesejados
```

**EXEMPLO de limpeza:**
```
ANTES (chunk bruto):
"O  Programa  Renda  Extra  (" Renda  Extra ˮ)  consiste  em..."

DEPOIS (chunk limpo):
"O Programa Renda Extra ("Renda Extra") consiste em..."
```

**IMPORTANTE:**
- Aplicar limpeza MENTALMENTE ao interpretar chunks
- Usar texto limpo para gerar perguntas
- Não modificar o banco de dados original
- Apenas processar em memória durante geração

**PASSO 2: Gerar perguntas novas** 🚨 LIMITE DE TOKENS

**REGRA CRÍTICA - Gerar em LOTES PEQUENOS:**

Se quantidade solicitada > 5:
```
❌ ERRADO: gerar_20_perguntas() de uma vez
✅ CORRETO:
   - gerar_5_perguntas() → salvar
   - gerar_5_perguntas() → salvar
   - gerar_5_perguntas() → salvar
   - gerar_5_perguntas() → salvar
```

**LIMITE MÁXIMO POR LOTE: 5 PERGUNTAS**

Processo para cada lote de 5:
1. Ler banco atual
2. Consultar conteúdo dos chunks via SQL
3. Gerar EXATAMENTE 5 perguntas completas baseadas nos chunks
4. Adicionar ao banco
5. Salvar imediatamente
6. Validar que salvou correto
7. Continuar próximo lote

**Motivo:** Evitar JSON truncado por limite de tokens

Requisitos por pergunta:
1. Baseado no conteúdo dos chunks do RAG
2. Estrutura JSON validada (ver schema acima)
3. Garantir que é DIFERENTE das já existentes
4. Variar tópicos e dificuldade
5. Referenciar o `fonte_chunk` de origem

**PASSO 3: Salvar no JSON** 🚨 ANTI-CORRUPÇÃO

**TÉCNICA OBRIGATÓRIA - Gerar por Partes:**
1. Ler banco existente (se houver)
2. Para cada nova pergunta:
   - Criar dict completo da pergunta
   - Adicionar ao array `perguntas`
3. Atualizar metadata (total_perguntas, ultima_atualizacao)
4. **VALIDAÇÃO CRÍTICA antes de Write:**
   ```
   CHECKLIST PRÉ-SAVE:
   [ ] Todas as perguntas têm 4 alternativas (A, B, C, D)?
   [ ] Todas alternativas têm texto, correta, explicacao?
   [ ] Nenhum campo está truncado (ex: "explicac", "tex", "corr")?
   [ ] fonte_chunk no formato "chunk_X"?
   [ ] SEM campos proibidos?
   [ ] JSON completo, sem "..." ou placeholders?
   ```
5. Usar ferramenta `Write` com JSON validado
6. **VERIFICAÇÃO PÓS-SAVE (OBRIGATÓRIA):**
   - Usar `Read` para ler arquivo salvo
   - Confirmar que JSON é válido e completo
   - Se corrompido: regerar
7. Mostrar resumo do que foi gerado

### Quando `/gerar-quiz-rag iniciar` for invocado:

**PASSO 1: Escolher perguntas**
- Se modo `novo`: Gerar 10 perguntas consultando RAG
- Se modo `aleatorio`: Ler JSON e sortear 10 existentes
- Se modo `teste`: Marcar resposta correta com ⭐

**PASSO 2: Executar quiz**
1. Apresentar 1 pergunta por vez
2. Aguardar resposta do usuário
3. Dar feedback imediato (correto/incorreto + explicação)
4. Avançar para próxima
5. Ao final, mostrar pontuação e análise

**Critérios para criação das perguntas:**

- Criar perguntas baseadas no conteúdo dos chunks do banco RAG
- Cada pergunta deve testar compreensão de pontos importantes
- Variar a dificuldade (fácil, média, difícil)
- Explorar diferentes tipos de informação do conteúdo
- **NÃO repetir perguntas que já estão no banco**
- **Referenciar o chunk de origem**: Cada pergunta deve indicar de qual chunk veio (ex: "chunk_0")

### Formato das Perguntas no Quiz

Cada pergunta deve seguir este formato:

```
**Pergunta X/10**

[Enunciado da pergunta]

A) [Alternativa A]
B) [Alternativa B]
C) [Alternativa C]
D) [Alternativa D]

Qual é a sua resposta? (A, B, C ou D)
```

Regras para as alternativas:
- Exatamente 4 alternativas (A, B, C, D)
- Apenas UMA alternativa correta
- Três alternativas incorretas mas plausíveis
- Randomizar a posição da resposta correta
- **[TESTE]** Em modo teste, destacar alternativa correta com ⭐

### Avaliação de Respostas

Após o usuário responder:

**Se CORRETA:**
```
✅ Correto! A resposta é [letra]: [texto da alternativa]

[Breve explicação do porquê está correto]

Pontuação atual: X/Y
```

**Se INCORRETA:**
```
❌ Incorreto. Você respondeu [letra], mas a resposta correta é [letra correta].

**Por que sua resposta está errada:**
[Explicação clara do erro]

**Resposta correta:**
[Texto da alternativa correta] - [Explicação]

Pontuação atual: X/Y
```

### Pontuação Final

Após a 10ª pergunta:

```
===========================================
           RESULTADO DO QUIZ
===========================================

Pontuação: X/10 (XX%)

[Avaliação baseada na pontuação:]
- 10/10: Excelente! Domínio completo.
- 8-9/10: Muito bom! Conhecimento sólido.
- 6-7/10: Bom. Alguns pontos precisam de revisão.
- 4-5/10: Regular. Recomenda-se revisar.
- 0-3/10: Precisa estudar mais.

DESEMPENHO POR TÓPICO:
===========================================
✓ Tópico A: 2/2 (100%)
✗ Tópico B: 1/2 (50%)
...

TÓPICOS PARA REVISÃO:
- [Lista de tópicos com desempenho < 70%]
===========================================
```

## Regras de Interação

1. **Uma pergunta por vez** - Nunca mostrar múltiplas perguntas de uma vez
2. **Aguardar resposta** - Não avançar até o usuário responder
3. **Aceitar formatos flexíveis** - Aceitar "A", "a", "1", "primeira" etc.
4. **Feedback imediato** - Sempre explicar o resultado após cada resposta
5. **Manter contexto** - Lembrar a pontuação ao longo do quiz
6. **Tom educativo** - Ser construtivo nas correções, não punitivo

## Comandos do Usuário

Durante o quiz:
- "pular" ou "próxima" - Conta como erro e avança
- "desistir" ou "parar" - Encerra e mostra pontuação parcial
- "repetir" - Repete a pergunta atual
- "pontuação" - Mostra pontuação atual

## Validação de Duplicatas (CRÍTICO)

**PARA GARANTIR QUIZ COMPLETO SEM DUPLICATAS:**

### Algoritmo de Detecção:

1. **Match Exato** (100% similiar):
   - Comparar texto da pergunta (ignorando case)
   - Se idêntico: ❌ DUPLICATA - gerar outro

2. **Similaridade de Texto** (>60% similar):
   - Extrair palavras-chave principais
   - Contar palavras em comum
   - Se palavras_em_comum / total_palavras > 60%: ❌ DUPLICATA

3. **Match de Padrão**:
   - Mesmos itens/seções mencionadas?
   - Mesma pergunta, apenas redação diferente?
   - Se sim: ❌ DUPLICATA

### Implementação:

**ANTES DE GERAR CADA PERGUNTA:**

```
Para cada pergunta nova:
  1. Extrair palavras-chave do texto
  2. Para cada pergunta existente no banco:
     a. Comparar texto (case-insensitive)
     b. Se 100% igual: DUPLICATA
     c. Contar palavras em comum
     d. Se similaridade > 60%: DUPLICATA
  3. Se não for duplicata:
     a. ACEITAR pergunta
     b. Adicionar ao banco
  4. Se for duplicata:
     a. GERAR nova pergunta diferente
     b. Voltar ao passo 1
     c. Máximo 3 tentativas
```

### Critérios de Duplicata (CONCRETOS):

- ✅ **ACEITAR**: "Qual é a idade mínima?" + "Qual idade mínima?" → Texto diferente, mesmo conceito ✓
- ❌ **REJEITAR**: "Qual é a idade mínima?" + "Qual é a idade mínima?" → Idêntico
- ❌ **REJEITAR**: "Qual é a idade mínima para participar?" + "Qual é a idade mínima para o programa?" → >60% similar

### Estratégia para 200+ Perguntas:

1. **Variar enfoques**:
   - "O Pagar.me pode fazer X?" (verdadeiro/falso)
   - "Qual é a consequência de X?" (resultado)
   - "O artigo Y menciona qual ponto?" (citação)
   - "Em qual situação Z se aplica?" (aplicação)

2. **Variar tópicos**:
   - Nunca gerar 2 perguntas sobre mesmo item consecutivamente
   - Alternar entre seções

3. **Monitorar duplicatas**:
   - A cada 50 perguntas: avisar se taxa de duplicatas > 10%
   - Se atingir 3 duplicatas seguidas: PARAR (banco completo)
   - Se quantidade solicitada > máximo estimado: ALERTAR usuário

## Início do Quiz

Ao iniciar, apresentar:

```
===========================================
        QUIZ DO CONHECIMENTO RAG
===========================================

Este quiz contém 10 perguntas de múltipla escolha
baseadas no conhecimento armazenado no banco RAG.

- Cada pergunta tem 4 alternativas (A, B, C, D)
- Apenas uma alternativa está correta
- Você receberá feedback após cada resposta

Preparado? Vamos começar!

---
```
