---
name: networkx
description: Kit de ferramentas abrangente para criar, analisar e visualizar redes e grafos complexos em Python. Use ao trabalhar com estruturas de dados de rede/grafo, analisar relacionamentos entre entidades, calcular algoritmos de grafo (caminhos mais curtos, centralidade, clustering), detectar comunidades, gerar redes sintéticas ou visualizar topologias de rede. Aplicável a redes sociais, redes biológicas, sistemas de transporte, redes de citações e qualquer domínio envolvendo relacionamentos entre pares.
---

# NetworkX

## Visão Geral

NetworkX é um pacote Python para criar, manipular e analisar redes e grafos complexos. Use essa skill ao trabalhar com estruturas de dados de rede ou grafo, incluindo redes sociais, redes biológicas, sistemas de transporte, redes de citações, grafos de conhecimento ou qualquer sistema envolvendo relacionamentos entre entidades.

## Quando Usar Essa Skill

Invoque essa skill quando as tarefas envolvem:

- **Criar grafos**: Construir estruturas de rede a partir de dados, adicionar nós e arestas com atributos
- **Análise de grafos**: Calcular medidas de centralidade, encontrar caminhos mais curtos, detectar comunidades, medir clustering
- **Algoritmos de grafo**: Executar algoritmos padrão como Dijkstra, PageRank, árvores geradoras mínimas, fluxo máximo
- **Geração de redes**: Criar redes sintéticas (aleatórias, scale-free, small-world) para testes ou simulação
- **Entrada/saída de grafo**: Ler ou escrever em vários formatos (listas de arestas, GraphML, JSON, CSV, matrizes de adjacência)
- **Visualização**: Desenhar e personalizar visualizações de rede com matplotlib ou bibliotecas interativas
- **Comparação de redes**: Verificar isomorfismo, calcular métricas de grafo, analisar propriedades estruturais

## Capacidades Principais

### 1. Criação e Manipulação de Grafos

NetworkX suporta quatro tipos principais de grafo:
- **Graph**: Grafos não-direcionados com arestas simples
- **DiGraph**: Grafos direcionados com conexões unidirecionais
- **MultiGraph**: Grafos não-direcionados permitindo múltiplas arestas entre nós
- **MultiDiGraph**: Grafos direcionados com múltiplas arestas

Crie grafos por:
```python
import networkx as nx

# Criar grafo vazio
G = nx.Graph()

# Adicionar nós (pode ser qualquer tipo hashable)
G.add_node(1)
G.add_nodes_from([2, 3, 4])
G.add_node("protein_A", type='enzyme', weight=1.5)

# Adicionar arestas
G.add_edge(1, 2)
G.add_edges_from([(1, 3), (2, 4)])
G.add_edge(1, 4, weight=0.8, relation='interacts')
```

**Referência**: Veja `references/graph-basics.md` para orientação abrangente sobre criação, modificação, exame e gerenciamento de estruturas de grafo, incluindo trabalho com atributos e subgrafos.

### 2. Algoritmos de Grafo

NetworkX oferece algoritmos extensivos para análise de rede:

**Caminhos Mais Curtos**:
```python
# Encontrar caminho mais curto
path = nx.shortest_path(G, source=1, target=5)
length = nx.shortest_path_length(G, source=1, target=5, weight='weight')
```

**Medidas de Centralidade**:
```python
# Centralidade de grau
degree_cent = nx.degree_centrality(G)

# Centralidade de intermediação
betweenness = nx.betweenness_centrality(G)

# PageRank
pagerank = nx.pagerank(G)
```

**Detecção de Comunidades**:
```python
from networkx.algorithms import community

# Detectar comunidades
communities = community.greedy_modularity_communities(G)
```

**Conectividade**:
```python
# Verificar conectividade
is_connected = nx.is_connected(G)

# Encontrar componentes conectados
components = list(nx.connected_components(G))
```

**Referência**: Veja `references/algorithms.md` para documentação detalhada sobre todos os algoritmos disponíveis, incluindo caminhos mais curtos, medidas de centralidade, clustering, detecção de comunidades, fluxos, matching, algoritmos de árvore e traversal de grafo.

### 3. Geradores de Grafos

Crie redes sintéticas para testes, simulação ou modelagem:

**Grafos Clássicos**:
```python
# Grafo completo
G = nx.complete_graph(n=10)

# Grafo de ciclo
G = nx.cycle_graph(n=20)

# Grafos conhecidos
G = nx.karate_club_graph()
G = nx.petersen_graph()
```

**Redes Aleatórias**:
```python
# Grafo aleatório Erdős-Rényi
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)

# Rede scale-free Barabási-Albert
G = nx.barabasi_albert_graph(n=100, m=3, seed=42)

# Rede small-world Watts-Strogatz
G = nx.watts_strogatz_graph(n=100, k=6, p=0.1, seed=42)
```

**Redes Estruturadas**:
```python
# Grafo de grade
G = nx.grid_2d_graph(m=5, n=7)

# Árvore aleatória
G = nx.random_tree(n=100, seed=42)
```

**Referência**: Veja `references/generators.md` para cobertura abrangente de todos os geradores de grafo, incluindo clássicos, aleatórios, lattices, bipartidos e modelos de rede especializados com parâmetros detalhados e casos de uso.

### 4. Leitura e Escrita de Grafos

NetworkX suporta numerosos formatos de arquivo e fontes de dados:

**Formatos de Arquivo**:
```python
# Lista de arestas
G = nx.read_edgelist('graph.edgelist')
nx.write_edgelist(G, 'graph.edgelist')

# GraphML (preserva atributos)
G = nx.read_graphml('graph.graphml')
nx.write_graphml(G, 'graph.graphml')

# GML
G = nx.read_gml('graph.gml')
nx.write_gml(G, 'graph.gml')

# JSON
data = nx.node_link_data(G)
G = nx.node_link_graph(data)
```

**Integração com Pandas**:
```python
import pandas as pd

# A partir de DataFrame
df = pd.DataFrame({'source': [1, 2, 3], 'target': [2, 3, 4], 'weight': [0.5, 1.0, 0.75]})
G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight')

# Para DataFrame
df = nx.to_pandas_edgelist(G)
```

**Formatos de Matriz**:
```python
import numpy as np

# Matriz de adjacência
A = nx.to_numpy_array(G)
G = nx.from_numpy_array(A)

# Matriz esparsa
A = nx.to_scipy_sparse_array(G)
G = nx.from_scipy_sparse_array(A)
```

**Referência**: Veja `references/io.md` para documentação completa sobre todos os formatos de E/S, incluindo CSV, bancos de dados SQL, Cytoscape, DOT, e orientação sobre seleção de formato para diferentes casos de uso.

### 5. Visualização

Crie visualizações de rede claras e informativas:

**Visualização Básica**:
```python
import matplotlib.pyplot as plt

# Desenho simples
nx.draw(G, with_labels=True)
plt.show()

# Com layout
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', node_size=500)
plt.show()
```

**Personalização**:
```python
# Colorir por grau
node_colors = [G.degree(n) for n in G.nodes()]
nx.draw(G, node_color=node_colors, cmap=plt.cm.viridis)

# Tamanho por centralidade
centrality = nx.betweenness_centrality(G)
node_sizes = [3000 * centrality[n] for n in G.nodes()]
nx.draw(G, node_size=node_sizes)

# Pesos de aresta
edge_widths = [3 * G[u][v].get('weight', 1) for u, v in G.edges()]
nx.draw(G, width=edge_widths)
```

**Algoritmos de Layout**:
```python
# Layout spring (force-directed)
pos = nx.spring_layout(G, seed=42)

# Layout circular
pos = nx.circular_layout(G)

# Layout Kamada-Kawai
pos = nx.kamada_kawai_layout(G)

# Layout espectral
pos = nx.spectral_layout(G)
```

**Qualidade para Publicação**:
```python
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos=pos, node_color='lightblue', node_size=500,
        edge_color='gray', with_labels=True, font_size=10)
plt.title('Network Visualization', fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig('network.png', dpi=300, bbox_inches='tight')
plt.savefig('network.pdf', bbox_inches='tight')  # Formato vetorial
```

**Referência**: Veja `references/visualization.md` para documentação extensa sobre técnicas de visualização, incluindo algoritmos de layout, opções de personalização, visualizações interativas com Plotly e PyVis, redes 3D e criação de figuras com qualidade para publicação.

## Trabalhando com NetworkX

### Instalação

Certifique-se de que NetworkX está instalado:
```python
# Verificar se está instalado
import networkx as nx
print(nx.__version__)

# Instalar se necessário (via bash)
# uv pip install networkx
# uv pip install networkx[default]  # Com dependências opcionais
```

### Padrão de Workflow Comum

A maioria das tarefas NetworkX segue este padrão:

1. **Criar ou Carregar Grafo**:
   ```python
   # Do zero
   G = nx.Graph()
   G.add_edges_from([(1, 2), (2, 3), (3, 4)])

   # Ou carregar de arquivo/dados
   G = nx.read_edgelist('data.txt')
   ```

2. **Examinar Estrutura**:
   ```python
   print(f"Nós: {G.number_of_nodes()}")
   print(f"Arestas: {G.number_of_edges()}")
   print(f"Densidade: {nx.density(G)}")
   print(f"Conectado: {nx.is_connected(G)}")
   ```

3. **Analisar**:
   ```python
   # Calcular métricas
   degree_cent = nx.degree_centrality(G)
   avg_clustering = nx.average_clustering(G)

   # Encontrar caminhos
   path = nx.shortest_path(G, source=1, target=4)

   # Detectar comunidades
   communities = community.greedy_modularity_communities(G)
   ```

4. **Visualizar**:
   ```python
   pos = nx.spring_layout(G, seed=42)
   nx.draw(G, pos=pos, with_labels=True)
   plt.show()
   ```

5. **Exportar Resultados**:
   ```python
   # Salvar grafo
   nx.write_graphml(G, 'analyzed_network.graphml')

   # Salvar métricas
   df = pd.DataFrame({
       'node': list(degree_cent.keys()),
       'centrality': list(degree_cent.values())
   })
   df.to_csv('centrality_results.csv', index=False)
   ```

### Considerações Importantes

**Precisão de Ponto Flutuante**: Quando grafos contêm números de ponto flutuante, todos os resultados são inerentemente aproximados devido a limitações de precisão. Isso pode afetar os resultados dos algoritmos, particularmente em computações de mínimo/máximo.

**Memória e Performance**: Cada vez que um script é executado, dados do grafo devem ser carregados na memória. Para redes grandes:
- Use estruturas de dados apropriadas (matrizes esparsas para grafos grandes e esparsos)
- Considere carregar apenas subgrafos necessários
- Use formatos de arquivo eficientes (pickle para objetos Python, formatos comprimidos)
- Aproveite algoritmos aproximados para redes muito grandes (ex: parâmetro `k` em cálculos de centralidade)

**Tipos de Nó e Aresta**:
- Nós podem ser qualquer objeto Python hashable (números, strings, tuplas, objetos customizados)
- Use identificadores significativos para clareza
- Ao remover nós, todas as arestas incidentes são removidas automaticamente

**Seeds Aleatórias**: Sempre defina seeds aleatórias para reprodutibilidade em geração de grafos aleatórios e layouts force-directed:
```python
G = nx.erdos_renyi_graph(n=100, p=0.1, seed=42)
pos = nx.spring_layout(G, seed=42)
```

## Referência Rápida

### Operações Básicas
```python
# Criar
G = nx.Graph()
G.add_edge(1, 2)

# Consultar
G.number_of_nodes()
G.number_of_edges()
G.degree(1)
list(G.neighbors(1))

# Verificar
G.has_node(1)
G.has_edge(1, 2)
nx.is_connected(G)

# Modificar
G.remove_node(1)
G.remove_edge(1, 2)
G.clear()
```

### Algoritmos Essenciais
```python
# Caminhos
nx.shortest_path(G, source, target)
nx.all_pairs_shortest_path(G)

# Centralidade
nx.degree_centrality(G)
nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.pagerank(G)

# Clustering
nx.clustering(G)
nx.average_clustering(G)

# Componentes
nx.connected_components(G)
nx.strongly_connected_components(G)  # Direcionado

# Comunidade
community.greedy_modularity_communities(G)
```

### Referência Rápida de E/S
```python
# Ler
nx.read_edgelist('file.txt')
nx.read_graphml('file.graphml')
nx.read_gml('file.gml')

# Escrever
nx.write_edgelist(G, 'file.txt')
nx.write_graphml(G, 'file.graphml')
nx.write_gml(G, 'file.gml')

# Pandas
nx.from_pandas_edgelist(df, 'source', 'target')
nx.to_pandas_edgelist(G)
```

## Recursos

Essa skill inclui documentação de referência abrangente:

### references/graph-basics.md
Guia detalhado sobre tipos de grafo, criação e modificação de grafos, adição de nós e arestas, gerenciamento de atributos, exame de estrutura e trabalho com subgrafos.

### references/algorithms.md
Cobertura completa de algoritmos NetworkX, incluindo caminhos mais curtos, medidas de centralidade, conectividade, clustering, detecção de comunidades, algoritmos de fluxo, algoritmos de árvore, matching, coloração, isomorfismo e traversal de grafo.

### references/generators.md
Documentação abrangente sobre geradores de grafo, incluindo grafos clássicos, modelos aleatórios (Erdős-Rényi, Barabási-Albert, Watts-Strogatz), lattices, árvores, modelos de redes sociais e geradores especializados.

### references/io.md
Guia completo para ler e escrever grafos em vários formatos: listas de arestas, listas de adjacência, GraphML, GML, JSON, CSV, DataFrames Pandas, arrays NumPy, matrizes esparsas SciPy, integração com bancos de dados e diretrizes de seleção de formato.

### references/visualization.md
Documentação extensa sobre técnicas de visualização, incluindo algoritmos de layout, personalização da aparência de nós e arestas, rótulos, visualizações interativas com Plotly e PyVis, redes 3D, layouts bipartidos e criação de figuras com qualidade para publicação.

## Recursos Adicionais

- **Documentação Oficial**: https://networkx.org/documentation/latest/
- **Tutorial**: https://networkx.org/documentation/latest/tutorial.html
- **Galeria**: https://networkx.org/documentation/latest/auto_examples/index.html
- **GitHub**: https://github.com/networkx/networkx