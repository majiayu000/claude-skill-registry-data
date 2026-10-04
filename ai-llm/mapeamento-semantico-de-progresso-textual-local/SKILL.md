---
name: mapeamento-semantico-de-progresso-textual-local
description: Rastreia conclusao de metas narrativas pela analise semantica do texto digitado, atualizando o Kanban de forma silenciosa.
---
# mapeamento-semantico-de-progresso-textual-local

## Descrição
A skill `mapeamento-semantico-de-progresso-textual-local` rastreia automaticamente a conclusão de metas narrativas (cartões de tarefa Kanban) pela análise semântica local do texto livre digitado pelo autor no editor. Ela compara embeddings do parágrafo recém-digitado com os vetores das metas pendentes da cena ativa e usa um LLM local para confirmar a ação concreta, atualizando o status do Kanban de forma silenciosa sem interromper o fluxo de escrita.

## Quando usar
Gatilhos concretos e observáveis:
- O autor digita uma quebra de parágrafo no editor e o sistema processa o texto gerado em background.
- O escritor muda o cartão Kanban de "A Escrever" para "Escrevendo" manualmente na UI.
- O sistema de gestão de outline detecta que novas cenas foram adicionadas ao banco de dados.

Quando NÃO usar:
- Em textos de notas de brainstorming ou rascunhos marcados como `is_draft = true` (devem ser excluídos da análise).
- Durante processamentos em tempo real tecla-a-tecla (deve rodar exclusivamente em background debounced).

## Pré-requisitos
- Banco de dados vetorial local (SQLite-VSS) com os embeddings das metas ativas da cena.
- Modelo de embeddings local (`multilingual-e5-base`) carregado em memória.
- Pequeno modelo de linguagem local instruct-tuned (ex: Phi-3.5-mini) para classificação zero-shot.

## Processo (passo a passo executável)
1. **Indexação das Metas Ativas (GMN Embeddings):**
   - Para cada meta do GMN com status `Em andamento` na cena atual, computar e armazenar o embedding da descrição da meta no banco vetorial local.
2. **Vetorização do Parágrafo Digitado:**
   - Ao término da digitação de um parágrafo (identificado por quebra de parágrafo `\n\n` ou ponto seguido de quebra), capturar o texto do parágrafo.
   - Executar o embedding do parágrafo usando o modelo local em background.
3. **Filtragem por Similaridade de Cosseno:**
   - Comparar o vetor do parágrafo com os vetores de cada meta pendente da cena ativa.
   - Se a distância de cosseno entre o parágrafo e alguma meta superar o limiar `SEMANTIC_MATCH_THRESHOLD = 0.82`, eleger essa meta como candidata à conclusão.
4. **Validação por Classificação Zero-Shot (LLM Local):**
   - Para cada meta candidata identificada na etapa 3, construir um prompt de verificação:
     ```text
     Meta: "Kael apresenta a chave de ferro ao ferreiro."
     Parágrafo: "Kael retirou a pequena chave enferrujada do bolso e a estendeu para Mestre Morgan."
     Pergunta: Esta meta foi concretamente executada no parágrafo? Responda APENAS com SIM ou NÃO.
     ```
   - Executar a inferência no modelo local e verificar a resposta.
5. **Atualização Automática do Kanban:**
   - Se o LLM responder `SIM`:
     - Atualizar o status do cartão correspondente no banco de dados para `Concluído`.
     - Criar um hyperlink de citação associando o cartão à linha e parágrafo exatos no manuscrito.
     - Exibir um badge verde discreto no cartão Kanban na sidebar sem exibir pop-ups ou alertas.

## Parâmetros e configuração
- `SEMANTIC_MATCH_THRESHOLD`: Limiar de similaridade de cosseno para candidatura de meta à conclusão. Padrão: `0.82`.
- `KANBAN_UPDATE_DEBOUNCE_MS`: Tempo de debounce após quebra de parágrafo para disparar análise semântica. Padrão: `2000` (2 segundos).
- `MAX_GOALS_PER_SCENE`: Número máximo de metas ativas simultaneamente por cena. Padrão: `5`.

## Armadilhas e como evitá-las
- **Armadilha:** Falsos Positivos por Discussão Passiva: um personagem menciona verbalmente que pretende realizar uma ação futura ("Temos que encontrar a chave"), gerando alta similaridade semântica com a meta "Apresentar a chave", mas sem concretizar a ação na cena.
  **Mitigação:** A etapa de filtragem por cosseno é apenas triagem. A validação final via prompt zero-shot do LLM local é mandatória antes de marcar qualquer meta como concluída. O prompt deve perguntar explicitamente se a ação foi **concretamente executada** na cena, não apenas mencionada ou planejada (Narrative Goal Tracking, 2025).

## Critérios de validação (Definition of Done)
- [ ] A acurácia geral de detecção automática de conclusão de metas validadas (sem falsos positivos de discussão passiva) é de pelo menos 85% no dataset de validação de cenas literárias.
- [ ] A análise semântica e o update do Kanban não causam nenhum frame drop no editor durante digitação ativa.

## Fundamentação científica
- Plot Event Extraction (2025) - Plot Event Extraction for Narrative Progress Tracking - arXiv 2025
- Narrative Goal Tracking (2025) - Automatic Tracking of Narrative Goals from Text Using LLMs - arXiv 2025
- Event-Centric Story Generation (2024) - Event-Centric Story Generation and Progress Detection - arXiv 2024

## Requisitos do projeto relacionados
- RF-108 (atualizar wiki)
- RF-194 (quadro de progresso)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: O passo de validação por LLM local adiciona latência de 0.5 a 1 segundo por parágrafo, que pode ser percebida em máquinas com CPU lenta.*
*Fallback para v1:* Desativar a validação por LLM. Usar somente o threshold de cosseno para sugerir ao autor a marcação da tarefa como concluída, exibindo uma pergunta discreta na sidebar: "Você completou esta meta: [nome]? [Sim / Não]".

## Exemplos
**Entrada (Parágrafo e Meta ativa):**
- Meta ativa: "Kael apresenta a chave secreta ao ferreiro."
- Parágrafo: "Kael tirou a chave do bolso e a colocou nas mãos do velho ferreiro sem dizer uma palavra."
**Saída esperada (Atualização automática do Kanban):**
```json
{
  "goal_id": "goal_kael_chave_ferreiro",
  "status_updated_to": "Concluído",
  "source_paragraph_ref": "cap03_par14",
  "hyperlink_created": true
}
```
**Caso de falha conhecido:**
Marcar "Kael entrega a chave" como concluída quando o parágrafo diz apenas "Kael não encontrou a chave por nenhum lado".
