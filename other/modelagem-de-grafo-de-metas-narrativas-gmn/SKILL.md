---
name: modelagem-de-grafo-de-metas-narrativas-gmn
description: Modela dependencias causais do enredo como DAG de metas narrativas com propagacao de inconsistencias e deteccao de ciclos.
---
# modelagem-de-grafo-de-metas-narrativas-gmn

## Descrição
A skill `modelagem-de-grafo-de-metas-narrativas-gmn` modela matematicamente a estrutura de dependências causais do enredo de romances como um Grafo Dirigido Acíclico (DAG) de Metas Narrativas (GMN). Ela mapeia as premissas e consequências lógicas das cenas do outline, propaga inconsistências automaticamente quando uma meta é removida ou alterada e impede que o autor conclua tarefas dependentes antes de suas predecessoras serem executadas.

## Quando usar
Gatilhos concretos e observárias:
- O autor cria, edita ou exclui uma cena ou meta no editor de outline do romance.
- Um novo arco de personagem ou linha de subtrama é adicionado ao planejamento.
- O sistema valida dependências antes de mover um cartão Kanban de "A Escrever" para "Escrevendo".

Quando NÃO usar:
- Para gerenciar dependências de tarefas técnicas de desenvolvimento de software (onde ferramentas dedicadas como Jira são mais adequadas).
- Em romances curtos de estrutura completamente linear sem sub-tramas entrelaçadas.

## Pré-requisitos
- Banco de dados relacional com tabelas `goals` (vértices) e `goal_dependencies` (arestas) para armazenar o DAG.
- Implementação do algoritmo de Kahn de detecção de ciclos.
- Motor de travessia de grafo que suporte propagação recursiva de estados em grafos direcionados.

## Processo (passo a passo executável)
1. **Definição da Estrutura do Grafo (GMN):**
   - Criar cada meta narrativa como um vértice $V$ do grafo com os atributos:
     - `id`, `titulo` (descrição da meta), `status` (`Pendente | Em andamento | Concluído | Inconsistente`), `capitulo_associado`.
   - Registrar cada relação de dependência causal entre duas metas como uma aresta direcionada $E = (A \rightarrow B)$, representando "meta $B$ só pode ser realizada após meta $A$".
2. **Validação de Aciclicidade (DAG Check):**
   - A cada nova aresta criada pelo autor no editor de outline:
     - Executar o algoritmo de Kahn (topological sort) sobre o grafo completo.
     - Se o algoritmo detectar um ciclo (ex: $A \rightarrow B \rightarrow A$), **bloquear** a inserção da aresta na UI com uma mensagem de erro explicativa e sugerir o redesenho.
3. **Propagação de Inconsistências:**
   - Quando uma meta $A$ mudar para o status `Inconsistente` (ex: foi editada de forma que quebra sua premissa lógica):
     - Executar BFS (Busca em Largura) ou DFS (Busca em Profundidade) a partir do nó $A$.
     - Aplicar a flag `Inconsistente` em cascata para todos os vértices descendentes $B \in Descendants(A)$.
4. **Validação de Pré-Condições (Conclusão de Metas):**
   - Bloquear a transição de status de uma meta $B$ para `Concluído` se:
     - Qualquer nó pai $P \in Parents(B)$ ainda possuir status `Pendente` ou `Inconsistente`.
   - Exibir uma mensagem bloqueante na UI listando as metas predecessoras ainda não concluídas.

## Parâmetros e configuração
- `MAX_GOAL_DEPTH`: Profundidade máxima permitida de aninhamento de dependências no DAG. Padrão: `10`.
- `PROPAGATION_ALGORITHM`: Algoritmo usado para propagação de flags de inconsistência. Padrão: `"BFS"`.
- `CYCLE_DETECTION_ALGORITHM`: Algoritmo usado para detecção de ciclos. Padrão: `"Kahn"`.

## Armadilhas e como evitá-las
- **Armadilha:** Paradoxos de Dependência Circular: o editor permite que o autor desenhe dependências mútuas entre duas metas (A depende de B e B depende de A simultaneamente). Isso gera um ciclo infinito nos algoritmos de validação e propagação, travando o sistema de gerenciamento de tarefas do romance.
  **Mitigação:** Executar a detecção de ciclo pelo algoritmo de Kahn imediatamente e sincronamente antes de registrar cada nova aresta no banco de dados. A inserção da dependência deve ser barrada na UI com mensagem clara antes de ser persistida, nunca depois (Narrative Task Graphs, 2026).

## Critérios de validação (Definition of Done)
- [ ] A verificação de aciclicidade e propagação de inconsistências em cascata em um DAG com 200 metas é concluída em menos de 5ms em CPU local.
- [ ] 100% das tentativas de criar dependências circulares entre metas do outline são bloqueadas antes de ser persistidas no banco de dados.

## Fundamentação científica
- Narrative Task Graphs (2026) - Task Dependency Graphs for Narrative Planning - CHI 2026
- Collaborative Plot Graphs (2024) - Collaborative Plot Graph Modeling for Long-form Narratives - arXiv 2024
- Graph-Based Outline Refinement (2026) - Graph-Based Outline Refinement and Consistency Checking - arXiv 2026

## Requisitos do projeto relacionados
- RF-194 (quadro de progresso)
- RF-195 (recomendar afazeres)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: A UI de desenho e visualização de dependências causais no outline pode ser cognitivamente complexa para romancistas sem experiência com ferramentas de planejamento em grafos.*
*Fallback para v1:* Oferecer somente relações lineares simples de dependência (uma meta por vez) via listas numeradas ordenadas no outline, sem visualização de grafo completo.

## Exemplos
**Inserção de dependência (caso válido):**
- Meta A: "Apresentar a personagem Helena (cap. 1)"
- Meta B: "Helena trai Kael (cap. 8)"
- Aresta $A \rightarrow B$ criada. Kahn não detecta ciclo. Inserção aprovada.
**Inserção de dependência (caso bloqueado — ciclo):**
- Aresta $B \rightarrow A$ solicitada (Helena trai → Apresentar Helena).
- Kahn detecta ciclo: $A \rightarrow B \rightarrow A$.
- Sistema bloqueia a inserção e exibe: "Dependência circular detectada: Meta B já depende de A. Impossível criar a dependência inversa."
**Caso de falha conhecido:**
Permitir que a meta "Resolver o mistério do assassinato" seja marcada como "Concluída" antes de a meta "Apresentar o suspeito principal" ter sido escrita.
