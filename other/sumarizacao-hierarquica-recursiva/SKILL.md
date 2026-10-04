---
name: sumarizacao-hierarquica-recursiva
description: Gera resumos de romances longos em multiplos niveis (cena, capitulo, obra) sem estourar janelas de contexto de modelos locais.
---
# sumarizacao-hierarquica-recursiva

## Descrição
A skill `sumarizacao-hierarquica-recursiva` realiza a condensação e geração de resumos de obras literárias de longa extensão (romances) de forma estruturada. Ela opera em múltiplos níveis de granularidade (cena, capítulo e livro completo), dividindo o texto de forma a respeitar as quebras naturais de cena do autor para evitar perda de coerência temporal e sem estourar as janelas de contexto limitadas de modelos de linguagem locais.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor encerra a redação de um capítulo ou cena (save de arquivo).
- O autor solicita explicitamente um resumo estruturado da obra ou de um conjunto de capítulos no painel do romance.
- Ocorre a importação em lote de um manuscrito longo inédito para catalogação no sistema.

Quando NÃO usar:
- Para responder a perguntas pontuais de lore (nesse caso, usar a skill `recuperacao-conhecimento-qfs-narrativo`).
- Em notas de worldbuilding ou brainstorm curtas.

## Pré-requisitos
- Modelo de linguagem local (SLM) otimizado para resumos de longa extensão (ex: Qwen-2.5-7B ou Llama-3-8B quantizado).
- Segmentador de texto que identifique quebras de capítulos (`# Capítulo N`) e marcadores de quebra de cena (ex: `***` ou quebras de parágrafo significativas).

## Processo (passo a passo executável)
1. **Montagem da Árvore de Segmentos Narrativos (ASN):**
   - Dividir o manuscrito de entrada hierarquicamente:
     - **Nível L1 (Folhas):** Cenas individuais (blocos lógicos de 200 a 1000 palavras delimitados por marcadores do autor).
     - **Nível L2 (Ramos):** Capítulos estruturais (conjunto de cenas L1 de um capítulo).
     - **Nível L3 (Raiz):** Romance completo (conjunto de resumos L2 de capítulos).
2. **Sumarização L1 (Local):**
   - Para cada bloco de cena L1, executar a inferência de resumo no SLM local usando o prompt de extração factual literária. O resultado gera um resumo conciso de cena $R_{L1}$ (limite: 150 palavras).
3. **Fusão Contextual L2 (Capítulo):**
   - Agrupar os resumos $R_{L1}$ de um mesmo capítulo.
   - Concatenar as saídas aplicando o método de Context-Aware Hierarchical Merging (CAHM) para preencher lacunas nas bordas das cenas.
   - Gerar o resumo do capítulo completo $R_{L2}$ (limite: 300 palavras).
4. **Sumarização L3 (Global):**
   - Reunir todos os resumos de capítulos $R_{L2}$.
   - Processar a fusão final no SLM local para produzir a sinopse global consolidada da obra $R_{L3}$ (limite: 500 palavras), focando na progressão dramática central (protagonista, conflito e clímax).

## Parâmetros e configuração
- `L1_MAX_WORDS`: Limite máximo de palavras para o resumo de cada cena individual. Padrão: `150`.
- `L2_MAX_WORDS`: Limite máximo de palavras para o resumo de cada capítulo. Padrão: `300`.
- `L3_MAX_WORDS`: Limite máximo de palavras para a sinopse global da obra. Padrão: `500`.
- `CHUNK_OVERLAP_SENTENCES`: Sentenças de sobreposição nas bordas dos blocos de cena para manter a coesão no CAHM. Padrão: `2`.

## Armadilhas e como evitá-las
- **Armadilha:** Chunking Fixo Arbitrário: cortar o romance em fatias cegas baseando-se em contagem bruta de tokens (ex: a cada 2000 tokens) quebra sentenças e diálogos importantes no meio, gerando resumos desconexos com falhas graves de enredo.
  **Mitigação:** Forçar o sistema a segmentar o texto baseando-se estritamente em elementos semânticos estruturais (marcadores de parágrafo, quebras de cena `***` e títulos de capítulos). Sentenças nunca devem ser cortadas ao meio.

## Critérios de validação (Definition of Done)
- [ ] O algoritmo atinge score médio de ROUGE-1 e ROUGE-L igual ou superior a 0.38 perante o dataset BookSum.
- [ ] O score de consistência lógica (BooookScore) dos resumos globais gerados é superior a 88% em testes automatizados contra o dataset de validação.

## Fundamentação científica
- DTCRS (2026) - Dynamic Tree Construction for Recursive Summarization - arXiv 2026
- CAHM (2025) - Context-Aware Hierarchical Merging for Long Document Summarization - arXiv 2025
- Kryściński, W. et al. (2021) - BookSum: Datasets for Long-form Narrative Summarization - arXiv 2021

## Requisitos do projeto relacionados
- RF-52 (resumo de textos longos)
- RF-181 (mesclar textos)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A sumarização recursiva por divisão de árvore (map-reduce adaptado) é a abordagem mais sólida e consolidada de engenharia de prompt para processar textos que excedem a janela física de atenção de LLMs locais.*

## Exemplos
**Entrada (Cena L1):**
```text
[Cena 1] Kael subiu os degraus de pedra fria com o coração palpitando. A porta do laboratório estava entreaberta. Ao entrar, deparou-se com o mago Érebo caído no chão, segurando um frasco quebrado. Érebo sussurrou: 'O traidor... está no conselho'. Kael tentou reanimá-lo, mas o mago deu seu último suspiro.
```
**Saída esperada (Resumo L1):**
```text
Kael encontra o mago Érebo gravemente ferido em seu laboratório. Antes de morrer, Érebo revela a Kael que há um traidor no conselho real.
```
**Caso de falha conhecido:**
Gerar um resumo que omita a informação crucial de morte de um personagem ou altere o culpado devido a um corte de chunk arbitrário no meio do diálogo.
