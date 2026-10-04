---
name: modelagem-ontologica-worldbuilding
description: Estrutura elementos do universo ficcional (personagens, faccoes, locais, itens) em uma ontologia de grafos flexivel com quadruplas temporais.
---
# modelagem-ontologica-worldbuilding

## Descrição
A skill `modelagem-ontologica-worldbuilding` gerencia e estrutura os elementos do universo ficcional (personagens, facções, locais, itens) e suas regras lógicas internas em uma ontologia de grafo flexível. Ela acopla esses elementos estáticos às estruturas dramáticas da narrativa (obstáculos, temas, capítulos), utilizando uma representação temporal dinâmica (quádruplas) para manter o histórico de evolução do mundo ao longo da linha do tempo da obra.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor inicializa um novo projeto de livro no sistema.
- O autor cria ou atualiza uma ficha estruturada de personagem, local ou facção na wiki integrada.
- Ocorre a modelagem de regras mágicas, científicas ou leis físicas específicas de um mundo ficcional (fantasia/ficção científica).

Quando NÃO usar:
- Para anotação linguística simples de palavras do manuscrito.
- Quando o romance não possuir elementos recorrentes de worldbuilding ou complexidade relacional (ex: crônicas minimalistas baseadas em um único cenário contemporâneo).

## Pré-requisitos
- Banco de dados de grafos (ex: SQLite com extensão de grafos, Neo4j local ou representação relacional de arestas/vértices).
- Motor de controle de tempo narrativo (instantes lineares $t$).
- Schema do Fictional Universe Knowledge Graph (FUKG) carregado.

## Processo (passo a passo executável)
1. **Instanciação de Classes de Vértices:**
   - Criar e categorizar os nós no FUKG sob as classes primárias:
     - `Character` (atributos de perfil, espécie, gênero, status).
     - `Location` (tipo de relevo, hierarquia espacial ex: `DentroDe(Quarto, Castelo)`).
     - `Faction` (alinhamento, metas, integrantes).
     - `Item` (tipo, raridade, portador atual).
2. **Modelagem de Relações em Quádruplas:**
   - Toda aresta criada entre duas classes deve ser registrada no formato de quádrupla: `(sujeito, predicado, objeto, [t_inicial, t_final])`.
   - Relações permanentes herdam o intervalo `[0, infinity]`.
   - Relações dinâmicas (ex: casamento, alianças de facções, posse de itens) devem receber o marcador $t_{inicial}$ correspondente ao tempo narrativo da cena em que a relação iniciou.
3. **Mapeamento de Metadados Dramáticos (Plot Nodes):**
   - Conectar as entidades físicas a nós conceituais literários:
     - `Obstruction`: Objeto ou conflito que impede uma meta de personagem.
     - `Theme`: Ideias centrais mapeadas no romance (ex: vingança, amor, traição).
4. **Vinculação a Eventos de Capítulo:**
   - Para cada quádrupla inserida ou alterada, associar um identificador de metadado vinculando a transição de estado ao ID do `Capitulo` ou `Cena` correspondente onde o fato é descrito no manuscrito.

## Parâmetros e configuração
- `DEFAULT_RELATION_TIME`: Intervalo de tempo padrão atribuído a relações imutáveis. Padrão: `[0, "infinito"]`.
- `MAX_SUB_LOCATIONS_DEPTH`: Profundidade máxima permitida para a hierarquia de locais aninhados (ex: País -> Província -> Cidade -> Casa). Padrão: `5`.
- `GRAPH_SCHEMA_VERSION`: Versão da definição de classes do FUKG. Padrão: `"FUKG-v1.0"`.

## Armadilhas e como evitá-las
- **Armadilha:** Rigidez Ontológica do Mundo Real: tentar herdar esquemas genéricos do Wikidata ou DBpedia impede a definição de regras e relações de mundos de fantasia (ex: no Wikidata, a classe `Humano` é fixa; em mundos fantásticos, um personagem pode pertencer a classes como `Elfo` ou `Androide` com comportamentos biológicos específicos).
  **Mitigação:** Bloquear heranças diretas de schemas reais complexos. A modelagem no FUKG deve ser declarativa e flexível, permitindo ao autor criar novas classes e propriedades dinamicamente através do editor de ontologia.

## Critérios de validação (Definition of Done)
- [ ] 100% das fichas de lore preenchidas pelo autor na wiki possuem vértices correspondentes instanciados e mapeados no banco de grafos.
- [ ] Todas as arestas dinâmicas cadastradas possuem timestamps de início e fim lógicos associados no banco de dados.

## Fundamentação científica
- WLKG (2023) - The World Literature Knowledge Graph - ISWC 2023
- URW-KG (2024) - The URW-KG: Universal Resource of World Literature - Journal of Digital Humanities 2024
- Narrative World Model Consortium (2026) - Narrative World Model (NWM): Narratology-Grounded Writer Memory - arXiv 2026
- Story-Theme-Obstacle (2025) - Long Story Generation via Knowledge Graph and Literary Theory - arXiv 2025

## Requisitos do projeto relacionados
- RF-42 (classificar entidades)
- RF-44 (linha de conexão)
- RF-166 (biografias)
- RF-167 (fichas estruturadas)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A engenharia de ontologias e bancos de dados orientados a grafos RDF/TKG é amplamente consolidada na computação corporativa e acadêmica, apresentando padrões robustos de armazenamento e consulta.*

## Exemplos
**Entrada:**
```json
{
  "sujeito": "Kael",
  "classe_sujeito": "Character",
  "predicado": "MembroDe",
  "objeto": "Ordem dos Cavaleiros",
  "classe_objeto": "Faction",
  "cena_id": "cena_05_cap_1",
  "tempo_narrativo": 3
}
```
**Saída esperada:**
```json
{
  "quadrupla": ["Kael", "MembroDe", "Ordem dos Cavaleiros", [3, "infinito"]],
  "associated_event": "cena_05_cap_1",
  "status": "SAVED"
}
```
**Caso de falha conhecido:**
Permitir a criação de um link direto entre entidades sem associar o metadado temporal $t$, impossibilitando auditorias retroativas de consistência do enredo.
