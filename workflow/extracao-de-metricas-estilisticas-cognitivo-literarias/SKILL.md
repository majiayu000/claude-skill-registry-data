---
name: extracao-de-metricas-estilisticas-cognitivo-literarias
description: Extrai assinatura matematica de estilo autoral (riqueza lexical, legibilidade Flesch-PT, ritmo) para medir desvio estilistico.
---
# extracao-de-metricas-estilisticas-cognitivo-literarias

## Descrição
A skill `extracao-de-metricas-estilisticas-cognitivo-literarias` computa uma assinatura matemática multidimensional de estilo de escrita (vetor de estilo) a partir de blocos de prosa em português. Ela captura a riqueza lexical, a legibilidade adaptada ao português e o ritmo cadencial da frase para permitir que o sistema meça a distância estilística entre o texto gerado pela IA e a voz autoral original do escritor.

## Quando usar
Gatilhos concretos e observáveis:
- O autor solicita análise de consistência de tom e estilo no painel de estatísticas de escrita.
- O pipeline de refinamento de prosa (skill `critico-e-refinador-de-prosa-literaria-local`) precisa de um vetor de referência de estilo do autor.
- Ocorre a importação de texto de outro escritor ou fonte para comparação estilística.

Quando NÃO usar:
- Para análise gramatical ou ortográfica simples (onde verificadores textuais padrão resolvem).
- Em textos poéticos de formas fixas (sonetos, haiku) onde a extensão de frase e sílabas é regida por regras métricas e não por opção de estilo em prosa.

## Pré-requisitos
- Biblioteca de processamento de língua portuguesa com suporte a lematização e contagem de sílabas (ex: spaCy com modelo `pt_core_news_lg`, ou NLTK/Pyphen adaptado para português).
- Corpus de calibração de estilo do autor (mínimo de 3 capítulos ou 5.000 palavras já escritas manualmente).

## Processo (passo a passo executável)
1. **Pré-processamento do Texto:**
   - Tokenizar o texto em sentenças e palavras.
   - Lematizar e filtrar, mantendo apenas as classes de conteúdo relevantes para estilo: substantivos, verbos, adjetivos e advérbios.
2. **Cálculo da Riqueza Lexical (Type-Token Ratio Adaptado — $m_1$):**
   - Contar o número de lemas únicos de conteúdo ($U$) e o total de palavras de conteúdo ($T$).
   - Calcular: $m_1 = \frac{U}{T}$. Valores mais altos indicam vocabulário mais diverso.
3. **Cálculo do Índice de Legibilidade (Flesch-PT — $m_2$):**
   - Computar a extensão média das frases em palavras ($ASL$) e o número médio de sílabas por palavra ($ASW$).
   - Aplicar a fórmula adaptada para o português:
     \[m_2 = 248.835 - (1.015 \times ASL) - (84.6 \times ASW)\]
4. **Cálculo do Ritmo Cadencial (Variabilidade de Frases — $m_3$):**
   - Calcular o desvio padrão $\sigma$ do número de palavras por frase dentro do bloco de texto analisado.
   - Mapear como $m_3 = \sigma_{frase}$.
5. **Compilação do Vetor de Estilo e Score de Distância:**
   - Montar o vetor atual: $\mathbf{v}_{atual} = [m_1, m_2, m_3]$.
   - Calcular a distância euclidiana do vetor atual em relação ao vetor de referência do autor:
     \[d_{estilo} = ||\mathbf{v}_{atual} - \mathbf{v}_{ref}||_2\]
   - Retornar o score $d_{estilo}$ como indicador de desvio estilístico (menor = mais próximo ao estilo do autor).

## Parâmetros e configuração
- `STYLE_DRIFT_THRESHOLD`: Distância euclidiana máxima do vetor de estilo considerada dentro da zona de estilo do autor. Padrão: `0.25`.
- `MIN_CORPUS_WORDS`: Mínimo de palavras do texto de referência para calibrar o vetor de estilo do autor. Padrão: `5000`.
- `FLESCH_PT_CONSTANT_BASE`: Constante base da fórmula de legibilidade adaptada para o português. Padrão: `248.835`.

## Armadilhas e como evitá-las
- **Armadilha:** Aplicar a Fórmula Flesch em Inglês em Textos em Português: a fórmula Flesch-Kincaid original foi calibrada para o inglês, onde as palavras têm em média menos sílabas e frases mais curtas. Aplicar essa fórmula em português gera scores sistematicamente inflados que não correspondem à percepção real de legibilidade do leitor lusófono.
  **Mitigação:** Usar obrigatoriamente a variante validada da fórmula com as constantes ajustadas para o português ($248.835 - 1.015 \times ASL - 84.6 \times ASW$), conforme publicado na literatura de NLP Cognitivo-Literário (COGNITIVE-LITERARY NLP, 2024).

## Critérios de validação (Definition of Done)
- [ ] O cálculo completo do vetor de estilo de uma página (500 palavras) de texto é concluído em menos de 150ms em CPU local.
- [ ] A correlação entre os scores de legibilidade Flesch-PT computados e as avaliações manuais de leitores nativos do português é superior a 0.75 no dataset de calibração.

## Fundamentação científica
- Cognitive-Literary NLP (2024) - Cognitive-Literary Metrics for Portuguese Narrative Analysis - arXiv 2024
- Tone Consistency in LLMs (2025) - Measuring Tone Consistency in LLM-Generated Literary Text - arXiv 2025
- Quality Estimation in Text (2024) - Quality Estimation for Creative Writing Systems - arXiv 2024

## Requisitos do projeto relacionados
- RF-180 (reescrever com estilo)
- RF-181 (mesclar estilo)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*As métricas de riqueza lexical (TTR) e legibilidade são técnicas estáveis de análise computacional de texto há décadas. A adaptação da constante para o português é o passo crítico.*

## Exemplos
**Entrada:**
```text
[Referência do Autor] "Kael caminhou devagar. Observou o horizonte com uma tristeza antiga."
[Trecho Gerado por IA] "O guerreiro Kael deslocou-se lentamente em direção à linha do horizonte, enquanto contemplava o pôr do sol com uma melancolia arcaica e profunda que residia em seu âmago há muitos anos."
```
**Saída esperada (Vetor e Score):**
```json
{
  "v_autor": {"m1": 0.62, "m2": 74.5, "m3": 2.1},
  "v_ia": {"m1": 0.48, "m2": 55.2, "m3": 1.2},
  "distancia_estilistica": 0.41,
  "alerta": "Desvio estilístico detectado. O trecho gerado é mais verboso e menos rítmico que o estilo do autor."
}
```
**Caso de falha conhecido:**
Calcular Flesch-PT com a constante original em inglês e retornar que um texto complexo de Machado de Assis tem legibilidade de "nível jardim de infância".
