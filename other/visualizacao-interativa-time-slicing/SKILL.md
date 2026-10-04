---
name: visualizacao-interativa-time-slicing
description: Renderiza redes de personagens e locais com filtros temporais e agrupamento semantico para evitar saturacao visual no navegador.
---
# visualizacao-interativa-time-slicing

## Descrição
A skill `visualizacao-interativa-time-slicing` especifica a renderização gráfica e interação com o Grafo do Universo Ficcional (GUF) no navegador Web. Ela mitiga o emaranhado visual (efeito novelo/hairball) aplicando filtros temporais (time-slicing) baseados nas quádruplas relacionais e agrupamento semântico de nós (clustering), mantendo a legibilidade cognitiva da rede e alto desempenho da interface (taxa de quadros estável).

## Quando usar
Gatilhos concretos e observáveis:
- O escritor acessa a tela de visualização do grafo relacional de personagens ou locais do romance.
- O autor manipula o controle deslizante (slider) de linha do tempo na visualização gráfica.
- O usuário ativa filtros de visualização por facção, parentesco ou local na barra de ferramentas lateral do grafo.

Quando NÃO usar:
- Para renderizar visualizações estáticas lineares (ex: fluxogramas ou listas de texto tradicionais).
- Durante o processamento puro do banco de dados (deve atuar estritamente na camada de apresentação/UI).

## Pré-requisitos
- Motor de renderização WebGL/Canvas habilitado no navegador (ex: D3.js, Sigma.js ou Cytoscape.js).
- Banco de dados FUKG configurado com quádruplas relacionais contendo timestamps `[t_inicial, t_final]`.
- Módulo de agrupamento hierárquico estruturado (clustering).

## Processo (passo a passo executável)
1. **Fatiamento Temporal (Time-slicing Filter):**
   - Capturar o instante temporal ou intervalo narrativo $T_{active} = [t_a, t_b]$ selecionado pelo autor na interface (via slider linear).
   - Filtrar a base de dados de quádruplas mantendo apenas vértices e arestas que satisfaçam a condição:
     \[(t_inicial \le t_b) \land (t_final \ge t_a)\]
   - Ocultar da tela todos os nós e arestas que não pertençam ao intervalo ativo de tempo.
2. **Agrupamento Semântico (Hierarchical Clustering):**
   - Agrupar nós pertencentes a uma mesma categoria agregadora (ex: membros de uma mesma `Faction` ou sub-locais dentro de uma `Location`).
   - Renderizar o grupo como um único nó representativo consolidado (nó pai).
   - Adicionar o manipulador de eventos duplo clique: quando o usuário clicar no nó consolidado, expandi-lo revelando a rede interna de sub-nós com transição suave.
3. **Simulação de Forças Otimizada (Force-Directed Layout):**
   - Configurar o motor de física do layout (ex: `d3-force-layout`).
   - Definir parâmetros para minimizar cruzamentos de arestas:
     - Repulsão entre nós: `-150` pixels de raio.
     - Força de atração por aresta: `0.05` de multiplicador.
     - Centralização de gravidade: `0.1` de peso.
4. **Legenda e Código de Cores Relacional:**
   - Colorir as arestas baseando-se no tipo de predicado:
     - Verde sólido para alianças/amizade (`MembroDe`, `Aliado`).
     - Vermelho sólido para hostilidade/conflitos (`InimigoDe`).
     - Cinza tracejado para relações neutras ou segredos lógicos.

## Parâmetros e configuração
- `LAYOUT_STABILIZATION_ITERATIONS`: Número máximo de iterações do algoritmo de forças antes de congelar a renderização. Padrão: `150`.
- `MAX_VISIBLE_NODES_UNFILTERED`: Limite máximo de nós exibidos na tela sem forçar colapso/clustering automático. Padrão: `50`.
- `EDGE_STRETCH_FORCE`: Coeficiente de elasticidade das arestas na simulação física. Padrão: `0.05`.

## Armadilhas e como evitá-las
- **Armadilha:** Exibição Global Desfiltrada: renderizar o grafo relacional total de um romance de longo formato (mais de 200 personagens e locais) sem agrupamento causa travamento no navegador e poluição visual ilegível.
  **Mitigação:** Configurar a interface para abrir o grafo sempre colapsado (exibindo apenas nós consolidantes e os 5 personagens principais definidos). Forçar o agrupamento automático sempre que o número de nós ativos na tela superar o limite `MAX_VISIBLE_NODES_UNFILTERED = 50`.

## Critérios de validação (Definition of Done)
- [ ] A taxa de atualização de quadros da tela do grafo mantém-se igual ou superior a 60 FPS durante rotação, zoom ou arraste de nós (usando renderização via Canvas/WebGL).
- [ ] O tempo total de carregamento e estabilização física do layout de forças é inferior a 800ms para uma rede de 50 nós.

## Fundamentação científica
- GuidelineExplorer (2025) - nod-link diagram guidelines - IEEE TVCG 2025
- Graph Usability Group (2026) - Empirical Evaluation of Graph Visualizations - Computer Graphics Forum 2026
- Tiddi, I. et al. (2024) - From Nodes to Narratives: KGs for Creative Storytelling - SWC Workshops 2024

## Requisitos do projeto relacionados
- RF-57 (visualização de grafos)
- RF-96 (filtrar por personagem)
- RF-97 (filtrar por tipo)
- RF-98 (filtrar por período)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*Os algoritmos de layouts de forças force-directed e filtros WebGL/Canvas são amplamente suportados e otimizados em bibliotecas JS consolidadas de mercado.*

## Exemplos
**Entrada:**
```json
{
  "active_time": 5,
  "nodes": [
    {"id": "char_kael", "type": "Character"},
    {"id": "char_leandra", "type": "Character"}
  ],
  "edges": [
    {"source": "char_kael", "target": "char_leandra", "relation": "Aliado", "valid_time": [1, 10]},
    {"source": "char_kael", "target": "char_leandra", "relation": "Inimigo", "valid_time": [11, 20]}
  ]
}
```
**Saída esperada:**
Apenas renderizar uma aresta verde entre Kael e Leandra, pois o tempo ativo 5 situa-se no intervalo `[1, 10]` da relação de aliança.
```json
{
  "rendered_nodes": ["char_kael", "char_leandra"],
  "rendered_edges": [
    {"source": "char_kael", "target": "char_leandra", "color": "green", "style": "solid"}
  ]
}
```
**Caso de falha conhecido:**
Exibir simultaneamente a aresta de aliança (verde) e de hostilidade (vermelho) no mesmo ponto de tempo narrativo, gerando contradição visual de estado.
