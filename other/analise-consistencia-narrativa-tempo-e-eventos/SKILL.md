---
name: analise-consistencia-narrativa-tempo-e-eventos
description: Gerencia e valida a consistencia causal de tramas ramificadas e linhas do tempo alternativas usando grafos de eventos.
---
# analise-consistencia-narrativa-tempo-e-eventos

## Descrição
A skill `analise-consistencia-narrativa-tempo-e-eventos` gerencia e valida a consistência causal e temporal de tramas ramificadas, linhas do tempo alternativas e versões paralelas do universo da história (branches). Ela executa o raciocínio temporal nas ramificações lógicas do enredo para identificar incompatibilidades de datas, idades e sequências de eventos antes de mesclar ou visualizar alterações no outline.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor cria um novo universo alternativo ou "branch" temporário de enredo a partir de uma cena.
- O autor mescla (merge) ou compara duas ramificações de outline (versão A vs. versão B).
- Ocorre a importação de uma nova timeline de brainstorm que colide com a linha do tempo principal (main).

Quando NÃO usar:
- Em romances de linha temporal puramente linear com história de caminho único (sem branches lógicos).
- Para validação ortográfica ou estilística do texto.

## Pré-requisitos
- Estrutura de Grafo de Eventos Narrativos (GraphStory) implementada no banco local, tolerando bifurcação de nós (branches).
- Representação temporal NoT (Narrative-of-Thought) para sequenciamento lógico de fatos temporais.
- Módulo de visualização de mapas e timelines ativo.

## Processo (passo a passo executável)
1. **Mapeamento de Bifurcações (Branches):**
   - Tratar a bifurcação de enredo criando uma ramificação de vértices herdeira do nó de origem (Parent Node). A ramificação mantém herança de estado até o ponto de divisão.
2. **Cadeia de Raciocínio Temporal (NoT):**
   - Para o branch selecionado, reconstruir a sequência cronológica dos fatos do enredo extraindo a cadeia causal lógica passo a passo.
3. **Cálculo de Colisão e Comparação de Versões:**
   - Ao disparar o comando de mesclagem ou comparação de duas linhas temporais (ex: Branch A e Branch B), varrer as entidades associadas.
   - **Checagem de Idade/Tempo absoluto:** Se o tempo absoluto acumulado de eventos no Branch A resultar em uma idade para o personagem $P$ diferente de sua idade calculada no Branch B para o mesmo ponto de convergência, disparar erro de colisão de timeline.
   - **Incompatibilidade Causal:** Identificar se uma meta concluída no Branch A (ex: "Destruir o anel") entra em colisão com a premissa de um evento no Branch B ("Usar o anel").
4. **Sinalização Visual e Mapeamento Geográfico:**
   - Projetar as inconsistências detectadas em layouts visuais da timeline. O sistema deve pintar de vermelho as arestas com conflitos de colisão cronológica no mapa de enredo.

## Parâmetros e configuração
- `MAX_ACTIVE_BRANCHES`: Limite máximo de branches de enredo ativos simultaneamente na visualização para evitar sobrecarga cognitiva. Padrão: `3`.
- `TEMPORAL_RESOLUTION_UNIT`: Unidade de tempo básica para cálculo cronológico. Padrão: `"dia"` (valores: `"hora"`, `"dia"`, `"ano"`).
- `NOT_REASONING_STEPS`: Número de passos causais analisados em profundidade no Narrative-of-Thought. Padrão: `10`.

## Armadilhas e como evitá-las
- **Armadilha:** Sobrecarga Cognitiva de Ramificação: a proliferação desordenada de ramificações e linhas temporais alternativas pode confundir o autor e estourar a memória RAM na renderização gráfica global.
  **Mitigação:** O sistema deve limitar a visualização ativa na tela a no máximo `3` branches simultâneos. As ramificações inativas devem ser colapsadas no grafo principal e ter seu processamento de consistência pausado até serem explicitamente focadas pelo escritor.

## Critérios de validação (Definition of Done)
- [ ] O algoritmo identifica corretamente 100% das colisões temporais induzidas de forma intencional em testes de integração (ex: personagem no mesmo local em instantes conflitantes de diferentes branches mesclados).
- [ ] O recall na identificação de incompatibilidades e furos de enredo lógicos em tramas paralelas é superior a 80%.

## Fundamentação científica
- GraphStory (2026) - Collaborative Story Writing through Event-Based Narrative Editing - arXiv 2026
- TemporalStory (2023) - Enhancing Consistency in Story Visualization using Spatial-Temporal Attention - arXiv 2023
- Zhang, Y. et al. (2024) - Narrative-of-Thought (NoT): Improving Temporal Reasoning - arXiv 2024

## Requisitos do projeto relacionados
- RF-77 (universos alternativos)
- RF-80 (ramificações temporárias)
- RF-79 (comparar linhas do tempo)
- RF-55 (linha do tempo)

## Maturidade e riscos de adoção
**Nível:** Experimental.
*Risco: O gerenciamento matemático de merges e conflitos temporais de grafos complexos é altamente propenso a bugs de estado e inconsistência de dados.*
*Fallback para v1:* Tratar branches e universos alternativos como arquivos de projetos independentes (clones do banco). Desativar a mesclagem automatizada e a herança dinâmica de estados lógicos entre branches na v1, forçando o autor a gerenciar as versões manualmente.

## Exemplos
**Entrada:**
```json
{
  "branch_main": [
    {"evento": "Arthur coroa-se rei", "ano": 1120}
  ],
  "branch_alternativo": [
    {"evento": "Arthur é assassinado em combate", "ano": 1118},
    {"evento": "Arthur assina tratado de paz", "ano": 1120}
  ]
}
```
**Saída esperada:**
```json
{
  "can_merge": false,
  "conflict_detected": true,
  "description": "Colisão Causal: O evento 'Arthur assina tratado de paz' no ano 1120 é logicamente incompatível com 'Arthur é assassinado em combate' ocorrido em 1118 no mesmo branch."
}
```
**Caso de falha conhecido:**
Permitir a fusão de um branch onde o protagonista morre com a linha temporal principal sem alertar o autor, gerando furos na sequência do romance.
