---
name: busca-hibrida-local-first
description: Motor de busca hibrido local combinando busca vetorial (SQLite-VSS) e lexical (BM25) com Reciprocal Rank Fusion para lore ficcional.
---
# busca-hibrida-local-first

## Descrição
A skill `busca-hibrida-local-first` implementa o motor local de busca híbrida no sistema de gerenciamento de conhecimento pessoal (PKM) do romance. Ela une as vantagens da busca vetorial densa (captura de intenção semântica e sinônimos) e da busca lexical esparsa (correspondência exata de termos próprios ficcionais, nomes e magias inventadas pelo autor), fundindo os rankings com Reciprocal Rank Fusion (RRF) em ambiente offline local.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor digita um termo de pesquisa na barra de busca semântica da wiki de worldbuilding.
- O autor dispara uma busca por palavras-chave ou conceitos no painel de notas rápidas ao lado do editor.
- O assistente de IA necessita buscar notas ou capítulos passados para responder a consultas de contextualização.

Quando NÃO usar:
- Em buscas de correspondência exata de arquivos por nome de sistema (onde uma consulta direta à tabela SQL resolve).
- Para processamento em lote remoto na nuvem sem requisição de latência instantânea (tempo real).

## Pré-requisitos
- Extensão `SQLite-VSS` (ou biblioteca vetorial equivalente rodando localmente no app desktop via WASM/Bindings).
- Modelo de embeddings local: `multilingual-e5-base` (dimensão 768) rodando localmente via llama.cpp/ONNX Runtime.
- Motor de indexação esparsa BM25 integrado localmente.

## Processo (passo a passo executável)
1. **Segmentação de Conteúdo (Semantic Chunking):**
   - Receber a nota ou capítulo do romance.
   - Dividir o texto em blocos (chunks) de tamanho fixo de `384` tokens (limiar de tokens do modelo E5), mantendo uma sobreposição (overlap) de 10% (`38` tokens) entre blocos adjacentes para evitar cortes de sentido dramático.
2. **Geração de Embeddings e Indexação Vetorial:**
   - Enviar cada chunk para o modelo `multilingual-e5-base` local e obter o vetor correspondente de 768 dimensões.
   - Salvar o vetor na tabela virtual da extensão `SQLite-VSS`.
   - Indexar a tabela usando topologia HNSW configurada com parâmetros de construção da árvore: `M = 16` e `ef_construction = 200`.
3. **Indexação Lexical BM25:**
   - Processar os mesmos chunks de texto com etapas de normalização em português (conversão para minúsculas, remoção de acentos e pontuação, e tokenização de termos).
   - Alimentar o índice invertido do motor BM25 local.
4. **Execução de Busca Híbrida e Fusão RRF:**
   - Ao receber a query de pesquisa do autor:
     - *Passo A:* Computar o embedding da query e recuperar os 20 melhores chunks pelo `SQLite-VSS` (distância de cosseno).
     - *Passo B:* Executar a consulta de palavras no motor BM25 local recuperando os 20 melhores chunks.
     - *Passo C:* Combinar os dois rankings aplicando a fórmula RRF:
       \[RRF\_Score(d) = \sum_{m \in \{VSS, BM25\}} \frac{1}{k + rank_m(d)}\]
       Onde a constante de ponderação $k$ é fixada em `60` (`RRF_CONSTANT_K = 60`).
     - *Passo D:* Ordenar a lista resultante de forma decrescente pelo $RRF\_Score$ e retornar os top resultados.

## Parâmetros e configuração
- `CHUNK_SIZE_TOKENS`: Tamanho de fatia de texto em tokens enviado ao modelo de embeddings. Padrão: `384`.
- `CHUNK_OVERLAP_PERCENT`: Percentual de sobreposição de tokens entre chunks vizinhos. Padrão: `10` (%).
- `RRF_CONSTANT_K`: Constante de ponderação para o cálculo do score de fusão de rank. Padrão: `60`.
- `HNSW_PARAM_M`: Número de conexões bidirecionais criadas para cada elemento no índice HNSW. Padrão: `16`.

## Armadilhas e como evitá-las
- **Armadilha:** Dependência Exclusiva de Vetores: buscas puramente vetoriais (embeddings) falham em recuperar termos inventados de fantasia (ex: "Valerianis", "Eldaria"), pois modelos pré-treinados não mapeiam correlações de cosseno para termos fora do vocabulário comum, retornando sinônimos errôneos.
  **Mitigação:** É mandatório usar a fusão híbrida concorrente com BM25. A busca lexical BM25 garante peso de atração máximo a termos exatos inéditos de worldbuilding, enquanto o VSS garante flexibilidade conceitual a termos gerais de prosa (Vector DB Survey, 2025).

## Critérios de validação (Definition of Done)
- [ ] O recall@10 de busca híbrida local atinge no mínimo 95% na recuperação de nomes próprios e termos próprios de lore inventados nos testes automatizados do romance.
- [ ] O tempo total de consulta e fusão dos rankings sobre uma base de 500k palavras de romance é inferior a 200ms em hardware local.

## Fundamentação científica
- SQLite-VSS Extension (asg017, 2023) - Vector Similarity Search for SQLite - GitHub
- MemX (2026) - Memory-enhanced Personal Knowledge Retrieval System - arXiv 2026
- Vector DB Survey (2025) - A Survey on Vector Databases: Technology, Application, and Challenges - arXiv 2025
- LLM-Vector DB Survey (2024) - Integrating LLMs with Vector Databases: A Survey - arXiv 2024

## Requisitos do projeto relacionados
- RF-24 (busca semântica)
- RF-28 (busca contextual)
- RF-126 (busca offline-first)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A busca híbrida fundindo BM25 e busca vetorial densa local em bancos leves como SQLite-VSS é amplamente testada, estável e madura para produção on-device.*

## Exemplos
**Entrada (Busca de lore):**
- Query: "Onde o cajado de Morgan foi quebrado?"
- Resultados VSS: ["Capítulo 5: O cajado se partiu na ponte de fogo", "Capítulo 1: Morgan treina Kael"]
- Resultados BM25: ["Capítulo 5: O cajado se partiu na ponte de fogo", "Wiki: Cajado de Morgan"]
**Saída esperada (Consolidado RRF):**
1. "Capítulo 5: O cajado se partiu na ponte de fogo" (Rank 1 em ambos - Maior Score RRF)
2. "Wiki: Cajado de Morgan"
3. "Capítulo 1: Morgan treina Kael"
**Caso de falha conhecido:**
Retornar "O cetro do rei se perdeu" como melhor resultado da busca de embeddings apenas porque "cajado" e "cetro" são semanticamente semelhantes no modelo E5, ignorando o termo exato "cajado de Morgan".
