---
name: extracao-redes-personagens-portugues
description: Extrai a rede social dinamica de interacoes entre personagens usando co-ocorrencia e dialogos diretos em portugues.
---
# extracao-redes-personagens-portugues

## Descrição
A skill `extracao-redes-personagens-portugues` extrai a rede social dinâmica de interações entre personagens em romances e textos de ficção escritos em português. Ela mapeia o grafo de coocorrência e conversação ativa no manuscrito, pesando a força dos laços relacionais e gerando snapshots cronológicos que representam a evolução dos grupos dramáticos ao longo dos capítulos.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor salva ou encerra a redação de um capítulo ou cena.
- Ocorre a importação global de um manuscrito novo de romance no sistema.
- O autor acessa a aba "Rede de Personagens" ou o grafo relacional do painel de worldbuilding.

Quando NÃO usar:
- Para mapeamento estático de relações sem base textual (onde o autor desenha o grafo manualmente).
- Quando a cena analisada possuir apenas um único personagem ativo (rede sem arestas).

## Pré-requisitos
- Mapeamento prévio de nomes e aliases de personagens gerado pelas skills `deteccao-entidades-literarias-portugues` e `resolucao-correferencia-e-aliases-literarios`.
- Parser ou regex para identificação de discursos diretos em português (travessão `—` ou aspas `"` iniciando falas).

## Processo (passo a passo executável)
1. **Catalogação de Menções de Personagens:**
   - Obter o texto segmentado em sentenças e a lista de entidades de tipo `PESSOA` já consolidadas com seus respectivos IDs canônicos.
2. **Cálculo de Arestas por Coocorrência (Janela Deslizante):**
   - Definir uma janela deslizante contendo o tamanho de palavras configurado em `WINDOW_WORDS_SIZE` (padrão: `150` palavras).
   - Varrer o texto movendo a janela palavra por palavra.
   - Sempre que dois personagens distintos aparecerem dentro da mesma janela, incrementar o peso da aresta de coocorrência passiva no banco em $0.1$.
3. **Cálculo de Arestas Conversacionais (Diálogos):**
   - Identificar parágrafos marcados como discurso direto (iniciados por travessão `—` ou aspas `"`).
   - Identificar quem é o falante (speaker) e quem é o interlocutor (listener) na cena ativa (via atribuição de diálogos do parser).
   - Para interações de diálogo direto confirmadas, atribuir peso duplicado ($+0.5$ por fala correspondente) à aresta relacional entre o falante e o interlocutor.
4. **Construção Dinâmica por Snapshots:**
   - Agrupar e exportar o acumulado de pesos das arestas relativas à sequência temporal de cada capítulo.
   - Salvar cada grafo gerado como um snapshot indexado por capítulo (`capitulo_n_network_data.json`) para permitir a visualização da evolução histórica da rede de personagens.

## Parâmetros e configuração
- `WINDOW_WORDS_SIZE`: Tamanho da janela móvel de palavras para detecção de coocorrência. Padrão: `150` palavras.
- `DIALOGUE_WEIGHT_MULTIPLIER`: Fator de peso adicional para interações conversacionais. Padrão: `2.0`.
- `MIN_EDGE_WEIGHT_THRESHOLD`: Peso mínimo acumulado necessário para exibir a aresta na rede final. Padrão: `1.0`.

## Armadilhas e como evitá-las
- **Armadilha:** Falsas Arestas Globais: criar conexões espúrias (falsos positivos de amizade/interação) entre personagens apenas porque eles aparecem listados no mesmo capítulo completo (ex: personagem A aparece na primeira página e B na última página de um capítulo de 30 páginas, sem nunca conversarem).
  **Mitigação:** Proibir o cálculo de coocorrência em nível global de capítulo. A força das arestas deve ser calculada estritamente com base na proximidade imediata no texto via janela deslizante (`WINDOW_WORDS_SIZE = 150` palavras) ou presença no mesmo parágrafo (City of Millions, 2025).

## Critérios de validação (Definition of Done)
- [ ] O algoritmo atinge um F1-score mínimo de 86% na identificação de interações válidas sobre o dataset de testes literários.
- [ ] O grafo gerado exporta corretamente os snapshots ordenados por capítulo, sem misturar os pesos de arestas passadas.

## Fundamentação científica
- Canário, J. et al. (2025) - Taggus: pipeline redes sociais em ficção portuguesa - arXiv 2025
- Renard (2024) - A Modular Pipeline for Extracting Character Networks - JOSS 2024
- DialogueRelation (2025) - Dialogue-Based Multi-Dimensional Relationship Extraction from Novels - arXiv 2025
- City of Millions (2025) - Mapping Literary Social Networks At Scale - arXiv 2025

## Requisitos do projeto relacionados
- RF-94 (rede social de personagens)
- RF-98 (filtrar por período)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A extração de grafos sociais baseados em coocorrência de termos e janelas deslizantes é uma metodologia madura, estável e amplamente documentada na literatura de humanidades digitais.*

## Exemplos
**Entrada:**
```text
— Olá, Helena — disse Afonso da Maia ao entrar na sala. Helena sorriu e serviu o chá.
```
**Saída esperada (Arestas calculadas):**
```json
[
  {
    "source": "char_afonso_da_maia",
    "target": "char_helena",
    "cooccurrence_weight": 0.1,
    "conversational_weight": 0.5,
    "total_weight": 0.6
  }
]
```
**Caso de falha conhecido:**
Criar uma aresta de interação de peso alto entre dois personagens que aparecem em cenas distantes do mesmo capítulo, poluindo a legibilidade da rede social de personagens.
