---
name: grafo-de-lore-visualizacao-e-filtros
description: Renderiza, navega e filtra o grafo de entidades do universo ficcional (personagens, locais, eventos, objetos) com agrupamento semântico, zoom temporal e filtros por tipo/personagem/período. Ativar ao implementar ou atualizar o painel de visualização de grafos da wiki do projeto.
---

# grafo-de-lore-visualizacao-e-filtros

## Descrição
A skill `grafo-de-lore-visualizacao-e-filtros` especifica a implementação do painel de visualização interativa do Grafo de Universo Ficcional (GUF) no navegador. Ela define a biblioteca de renderização, a estratégia de layout, os filtros interativos por tipo de entidade, personagem e período temporal, e as otimizações para evitar saturação visual quando o grafo tem centenas de nós.

## Quando usar
Gatilhos concretos e observáveis:
- A equipe implementa ou atualiza o componente de grafo na aba "Wiki" ou "Universo" do editor.
- O usuário abre o painel de grafo com mais de 50 entidades cadastradas.
- Novos tipos de entidade (facções, itens mágicos, locais) são adicionados ao GUF.

Quando NÃO usar:
- Para a lógica de extração e persistência de entidades (ver skill `extracao-autonoma-relacoes-literarias`).
- Para análise temporal de consistência (ver skill `analise-consistencia-narrativa-tempo-e-eventos`).

## Pré-requisitos
- Biblioteca de visualização de grafos: **Cytoscape.js** (recomendada) ou **D3-force**.
- API de backend que retorna nós e arestas do GUF em formato JSON (campos: `id`, `label`, `type`, `chapter_first_appearance`, `connections`).
- Componente de sidebar de filtros implementado no framework frontend.

## Processo (passo a passo executável)
1. **Inicialização do Grafo (Cytoscape.js):**
   - Instanciar o Cytoscape com o container `div#guf-canvas`.
   - Carregar os dados do GUF via endpoint `/api/guf/nodes` com paginação por `chapter_range`.
   - Definir estilos visuais por `type` de entidade (ex: `personagem` = círculo azul, `local` = hexágono verde, `evento` = diamante laranja).

2. **Layout Inicial (Cola Force-Directed):**
   - Aplicar o layout `cose-bilkent` (Cola) para separação automática de clusters de entidades relacionadas.
   - Agrupar nós com 3 ou mais conexões em clusters colapsáveis para reduzir saturação visual.
   - Limitar o número de nós visíveis simultaneamente a `MAX_VISIBLE_NODES = 120`.

3. **Filtros Interativos (Sidebar):**
   - Implementar filtros cumulativos na sidebar:
     - **Por Tipo:** Checkboxes para cada tipo de entidade (personagem, local, evento, objeto, facção).
     - **Por Personagem:** Dropdown que ao selecionar um personagem destaca o subgrafo ego-centrado (o personagem + todos os nós conectados a ele em até 2 saltos).
     - **Por Período Temporal:** Slider de capítulos (ex: capítulos 1–5) que oculta entidades introduzidas fora do intervalo selecionado.
   - Aplicar filtros via `cy.elements().filter()` sem recarregar os dados do servidor.

4. **Interação com Nós:**
   - Ao clicar num nó, exibir um painel lateral com a ficha completa da entidade (nome, aliases, descrição, capítulo de introdução).
   - Ao passar o mouse sobre uma aresta, exibir tooltip com o tipo da relação (ex: "é aliado de", "é filho de", "habita").

5. **Time-Slicing Animado:**
   - Implementar botão "Animar linha do tempo" que itera progressivamente pelos capítulos, mostrando como o grafo evolui (entidades aparecendo e desaparecendo conforme o capítulo avança).

## Parâmetros e configuração
| Parâmetro | Descrição | Padrão |
|---|---|---|
| `MAX_VISIBLE_NODES` | Número máximo de nós visíveis simultaneamente antes de colapsar clusters | `120` |
| `EGO_GRAPH_HOPS` | Número de saltos para o subgrafo ego-centrado ao selecionar personagem | `2` |
| `LAYOUT_ALGORITHM` | Algoritmo de layout do grafo | `"cose-bilkent"` |
| `ANIMATION_INTERVAL_MS` | Intervalo entre frames na animação de linha do tempo | `800` |

## Armadilhas e como evitá-las
- **Armadilha:** Renderizar o grafo completo com todos os nós de uma vez sem paginação ou cluster colapso. Com 300+ nós em um layout force-directed, o navegador congela por 5–10 segundos e o resultado visual é ilegível.
  **Mitigação:** Implementar colapso automático de clusters com `MAX_VISIBLE_NODES` e carregar entidades de capítulos adicionais sob demanda (lazy loading por range de capítulos).

## Critérios de validação (Definition of Done)
- [ ] O painel de grafo com 200 entidades carrega e renderiza em menos de 2 segundos no Chrome.
- [ ] Os filtros por tipo, personagem e período funcionam sem recarregar dados do servidor.
- [ ] O usuário consegue navegar pelo grafo (zoom, pan, clique em nó) sem travamentos.

## Exemplos
**Filtro por personagem:**
Usuário seleciona "Helena" → sistema destaca Helena (nó central) + todos os personagens com quem ela interage + todos os locais onde ela aparece. Nós sem conexão com Helena ficam com opacidade 0.15.

**Time-slicing:**
Slider em Capítulo 3 → somente entidades introduzidas até o capítulo 3 são visíveis. Slider movido para Capítulo 7 → novas entidades aparecem com animação fade-in.
