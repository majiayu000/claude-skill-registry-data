---
name: design-de-quadro-kanban-para-escrita-criativa
description: Adapta interfaces Kanban ageis para a ergonomia cognitiva de romancistas, minimizando interrupcao do flow criativo.
---
# design-de-quadro-kanban-para-escrita-criativa

## Descrição
A skill `design-de-quadro-kanban-para-escrita-criativa` especifica os padrões de interface do quadro Kanban de planejamento e progresso de escrita de romances. Ela adapta os princípios ágeis de gestão de tarefas (Scrum/Kanban) para a ergonomia cognitiva de romancistas, priorizando a minimização da carga cognitiva, a não-interrupção do estado de flow criativo e a visibilidade clara do progresso narrativo sem criar ansiedade de produtividade.

## Quando usar
Gatilhos concretos e observáveis:
- A equipe de design implementa ou atualiza o painel de planejamento e produtividade do aplicativo.
- O autor acessa o modo de planejamento de enredo na aba de "Outline" ou "Kanban" do editor.
- Ocorre a exibição de status de metas inconsistentes oriundas do sistema de auditoria GMN.

Quando NÃO usar:
- Para gerenciar sprints de desenvolvimento de software ou backlog técnico de engenharia.
- Em interfaces puramente de edição de texto sem planejamento estruturado de enredo.

## Pré-requisitos
- Componente Kanban com suporte a drag-and-drop e estados persistentes no banco de dados.
- Integração com o GMN (Grafo de Metas Narrativas) para receber flags de inconsistência.
- Integração com o tracker de progresso semântico para receber atualizações automáticas de conclusão de tarefas.

## Processo (passo a passo executável)
1. **Layout do Quadro (4 Colunas Canônicas):**
   - Estruturar o Kanban em quatro colunas com semântica literária clara:
     - **Backlog:** Ideias, tropos, ganchos e cenas ainda não comprometidas com o outline.
     - **A Escrever:** Cenas e capítulos com dependências satisfeitas e prontos para redação.
     - **Escrevendo:** A cena ou capítulo atualmente em edição ativa (máximo 1 cartão por vez para manter o foco).
     - **Escrito:** Cenas e capítulos com o texto redigido e validado.
2. **Filtros de Visualização por Personagem e Locação:**
   - Adicionar filtros de exibição que destacam apenas os cartões de tarefa relevantes para:
     - O personagem selecionado no filtro ativo (ex: ver todas as metas de "Helena").
     - A locação narrativa ativa (ex: ver todas as cenas que ocorrem na "Biblioteca Real").
3. **Sinalização Visual por Badges Discretos:**
   - Exibir badges de status nos cartões Kanban usando um sistema de cores de baixa intrusão:
     - **Cinza:** Meta pendente, sem inconsistências.
     - **Verde:** Meta concluída automaticamente via análise semântica ou manualmente.
     - **Laranja:** Meta em andamento (escritor está digitando a cena).
     - **Vermelho discreto (borda):** Meta com dependência inconsistente (herdada do GMN propagation).
   - Nunca usar animações piscantes, sons de alerta ou pop-ups modais para badges de inconsistência.
4. **Ações de Resolução de Desvios:**
   - Ao clicar em um cartão com borda vermelha, exibir discretamente no painel expandido do cartão as duas opções de resolução:
     - **Opção A:** "Reescrever o trecho conflitante" (ativa o refinador StyleGuard-PT sobre o parágrafo associado).
     - **Opção B:** "Remodelar dependências" (abre o editor do GMN para reorganizar as arestas causais).

## Parâmetros e configuração
- `MAX_IN_PROGRESS_CARDS`: Número máximo de cartões simultaneamente na coluna "Escrevendo". Padrão: `1` (WIP limit de foco).
- `BADGE_ANIMATION_ENABLED`: Controla se badges de status utilizam animações CSS piscantes. Padrão: `false` (sempre sem animação).
- `SIDEBAR_NOTIFICATION_DELAY_MS`: Tempo mínimo de delay antes de exibir uma notificação lateral de inconsistência durante escrita ativa. Padrão: `5000` (5 segundos após parada da digitação).

## Armadilhas e como evitá-las
- **Armadilha:** Interrupção do Estado de Flow: exibir modais de alerta ou pop-ups sobrepondo o editor quando o sistema detecta uma inconsistência de dependência enquanto o romancista está digitando ativamente, quebrando o estado mental de flow criativo do autor.
  **Mitigação:** Toda sinalização de inconsistência do GMN deve ser inserida silenciosamente como um badge de borda vermelho no cartão Kanban da sidebar, que é visível durante pausa de digitação, nunca sobre o texto em edição ativa. As opções de resolução devem aparecer apenas quando o autor abrir proativamente o cartão inconsistente (Cognitive Load in AI Writing, 2025).

## Critérios de validação (Definition of Done)
- [ ] O score de usabilidade da interface Kanban de escrita criativa, medido pela escala de usabilidade SUS (System Usability Scale), é de pelo menos 80 em testes com usuários romancistas.
- [ ] Nenhum modal ou pop-up modal é exibido durante sessões de digitação ativa no editor de texto.

## Fundamentação científica
- Cognitive Writing Process (2024) - Modeling the Cognitive Writing Process for Tool Design - arXiv 2024
- StoryPlanner (2024) - StoryPlanner: An Agile Planner for Novel Writing - ACM CHI 2024
- Cognitive Load in AI Writing (2025) - Managing Cognitive Load in AI-Assisted Creative Writing Interfaces - arXiv 2025
- Creative Task Planning (2026) - Creative Task Planning in Hybrid Scrum/Kanban Environments - arXiv 2026

## Requisitos do projeto relacionados
- RF-196 (cronograma de escrita)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*O padrão Kanban de 4 colunas com WIP limit é um mecanismo consolidado de gestão visual de trabalho criativo, adaptado amplamente em contextos de escrita profissional.*

## Exemplos
**Estado do Kanban (Exemplo visual textual):**
```
| BACKLOG         | A ESCREVER          | ESCREVENDO       | ESCRITO           |
|-----------------|---------------------|------------------|-------------------|
| [Gancho Ato 3]  | [Cap 5 - Porto]     | [Cap 4 - Prisão] | [Cap 1 - Prólogo] |
| [Subplot Morgan]| [Cena Helena traição| (Borda Laranja)  | ✅ (Verde)        |
|                 |  (Borda Vermelha ⚠) |                  | [Cap 2 - Kael]   |
|                 |  deps. inconsist.]  |                  | ✅ (Verde)        |
```
**Ação em cartão inconsistente:**
Helena traição → Borda vermelha → Autor clica → Painel expande → Opções:
1. Reescrever trecho conflitante (ativa StyleGuard)
2. Remodelar dependências no GMN

**Caso de falha conhecido:**
Exibir um modal de alerta vermelho "INCONSISTÊNCIA DETECTADA!" enquanto o escritor está no meio de uma frase importante, forçando o fechamento do pop-up antes de continuar.
