---
name: recomendador-hibrido-literario
description: Motor de recomendacao de enredo, nomes e referencias literarias com busca paralela vetorial, grafo e notas fundidas com RRF.
---
# recomendador-hibrido-literario

## Descrição
A skill `recomendador-hibrido-literario` projeta o motor de recomendações de enredo, nomes de personagens, tropos e referências bibliográficas do romance. Ela executa buscas paralelas em bases relacionais, vetoriais e de grafos baseando-se no vetor de contexto (CAC), aplicando fusão RRF (Reciprocal Rank Fusion) ponderada e filtragem de consistência contra a ontologia local da história.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor clica em "Sugerir Gancho Dramático" ou "Sugerir Nome de Personagem" na interface do editor.
- O autor solicita referências estilísticas de outras obras semelhantes ao parágrafo atual.
- Ocorre a geração de ideias de brainstorming na barra lateral baseado no contexto recente de escrita.

Quando NÃO usar:
- Para realizar autocompletes ortográficos ou gramaticais simples (usar corretores locais).
- Quando o autor desativar a IA de apoio à escrita nas configurações de foco.

## Pré-requisitos
- Vetor de contexto (CAC) ativo e atualizado pela skill `vetorizacao-e-contexto-de-escrita`.
- Banco de dados de referências literárias indexado (ex: dump do LitSearch/DraftRec).
- Grafo do Universo Ficcional (GUF) local instanciado.

## Processo (passo a passo executável)
1. **Disparo de Tri-Busca Paralela:**
   - Ao receber a requisição de recomendação, disparar em paralelo três canais de busca locais usando o vetor CAC como consulta:
     - *Canal A (Vetorial Externo):* Similaridade de cosseno contra a base de dados de obras e romances de referência.
     - *Canal B (Grafo Local):* Travessia de nós e arestas adjacentes no Grafo do Universo Ficcional (GUF) do romance para mapear personagens livres ou locais não-utilizados.
     - *Canal C (Vetorial Local):* Busca semântica nas notas de worldbuilding e brainstorm do próprio autor.
2. **Interseção e Filtro de Conflitos Lógicos:**
   - Para as recomendações recuperadas pelo *Canal A* (obras externas), submeter a lista a uma checagem de colisão nominal contra o GUF local.
   - Se uma obra sugerir a introdução de um personagem com nome idêntico ou muito semelhante a um nó existente no GUF, mas com perfil diferente, renomear o personagem sugerido usando a base de sugestão de nomes locais para evitar confusão no enredo.
3. **Fusão RRF Ponderada Assimétrica:**
   - Unificar os rankings dos três canais usando a fórmula RRF.
   - Ajustar os pesos de relevância ($w$) dos canais de acordo com a categoria de busca:
     - Se o autor pediu *ganchos de enredo* $\rightarrow$ Aumentar peso do Canal B (Grafo) e Canal C (Notas).
     - Se o autor pediu *referências de estilo* $\rightarrow$ Aumentar peso do Canal A (Obras Externas).
4. **Exibição na Interface:**
   - Retornar os Top 5 resultados mais relevantes estruturados em formato JSON para exibição na UI.

## Parâmetros e configuração
- `RRF_PLOT_WEIGHT_GRAPH`: Peso atribuído ao canal de grafos para sugestões de trama. Padrão: `0.60`.
- `RRF_PLOT_WEIGHT_EXTERNAL`: Peso do canal de referências externas para ganchos de trama. Padrão: `0.10`.
- `MAX_RECOMMENDATION_ITEMS`: Quantidade máxima de itens exibidos na lista de recomendação. Padrão: `5`.

## Armadilhas e como evitá-las
- **Armadilha:** Recomendação Inconsistente de Enredo: sugerir rumos de enredo baseados em bases de dados externas de forma crua, introduzindo nomes de deuses, organizações ou regras físicas que colidem diretamente com a lore definida pelo autor nas notas da wiki.
  **Mitigação:** Toda recomendação conceitual importada de bases de dados externas deve passar por uma checagem de restrição contra o grafo de mundo (GUF) do autor. O sistema deve substituir entidades de lore externas por variáveis correspondentes do próprio universo do autor (ex: substituir "Ordem dos Templários" sugerido externamente por "Ordem dos Cavaleiros" do autor) antes de apresentar o card na UI (CreativeRAG, 2025).

## Critérios de validação (Definition of Done)
- [ ] A precisão (Precision@5) das sugestões ativas de nomes e ganchos aceitas/salvas pelo autor é de pelo menos 80% nos testes de usabilidade.
- [ ] A latência total de consulta, filtragem de consistência e retorno das sugestões é inferior a 500ms na máquina do usuário.

## Fundamentação científica
- CreativeRAG (2025) - CreativeRAG: Conserving World Consistency in Fictional Recommendations - arXiv 2025
- LitSearch (2024) - LitSearch: A Recommender System for Literary Reference and Analogies - arXiv 2024
- DraftRec (2024) - DraftRec: Sequential Context Recommendations for Creative Writers - arXiv 2024
- GraphStory (2026) - Collaborative Story Writing through Event-Based Narrative Editing - arXiv 2026

## Requisitos do projeto relacionados
- RF-175 (sugestões contextuais)
- RF-176 (sugerir ganchos)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: Fundir bases de dados em formatos estruturados diferentes usando RRF pode resultar em perda de precisão conceitual se os pesos assimétricos não forem calibrados finamente por gênero literário.*
*Fallback para v1:* Restringir as sugestões contextuais estritamente às notas e outlines criados pelo próprio autor (RAG local simplificado), desativando o canal de busca em obras externas na v1 do recomendador.

## Exemplos
**Entrada (Requisição):**
- Tipo: "Sugerir Nome de Personagem"
- CAC: Contém "Cena medieval, Kael no porto, precisa de um marinheiro".
- Conflitos no GUF: Já existe um personagem chamado "Afonso".
**Saída esperada (Sugestões ordenadas):**
```json
[
  {"name": "Martim", "origin": "Notas locais (marinheiro citado no cap 1)"},
  {"name": "Nuno", "origin": "Base de nomes históricos portugueses (sugerido)"},
  {"name": "Vasco", "origin": "Base de nomes históricos portugueses (sugerido)"}
]
```
**Caso de falha conhecido:**
Sugerir o nome "Afonso" para o marinheiro sendo que "Afonso da Maia" já é o rei na lore ativa do livro, provocando confusão lógica no enredo do autor.
