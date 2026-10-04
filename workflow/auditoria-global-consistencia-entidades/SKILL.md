---
name: auditoria-global-consistencia-entidades
description: Audita a continuidade fisica e logica de personagens, locais e objetos ao longo de multiplos capitulos usando grafos temporais.
---
# auditoria-global-consistencia-entidades

## Descrição
A skill `auditoria-global-consistencia-entidades` rastreia a continuidade física e lógica de personagens, locais e objetos (status vital de personagens, inventário de itens e localização espacial) ao longo de múltiplos capítulos do romance por meio de representações matemáticas em Grafos Temporais de Entidades (GTE). Ela analisa as transições de estado para evitar "buracos de roteiro" (plot holes) lógicos que violam as leis do próprio universo da história.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor conclui a redação de um capítulo inteiro (gatilho de save de capítulo ou mudança de status para "Concluído" no outline).
- O usuário solicita uma auditoria geral de inconsistências lógicas no painel de ferramentas da wiki do romance.
- Ocorre o encerramento da sessão ativa do aplicativo (salvamento geral do projeto no banco central).

Quando NÃO usar:
- Para checagens rápidas de digitação em tempo real na interface (deve rodar de forma assíncrona em background ou sob demanda devido ao custo computacional de varredura global).
- Em rascunhos de brainstorm livres e desorganizados onde o autor ainda não definiu a ordem cronológica dos capítulos.

## Pré-requisitos
- Pipeline NLP para extração estruturada de eventos baseados em triplas RDF ou JSON-LD.
- Motor de Grafos SQLite ou banco relacional local capaz de gerenciar vértices e arestas com indexação temporal $T$.
- Fichas de entidades da wiki já inicializadas no banco de dados.

## Processo (passo a passo executável)
1. **Extração de Relações de Eventos:**
   - Submeter o texto do capítulo concluído a um pipeline NLP (ou LLM local de classificação em lote) para extrair triplas de eventos contendo: `(sujeito, acao, objeto, local, instante_temporal_t)`.
2. **Modelagem no Grafo Temporal de Entidades (GTE):**
   - Inserir ou atualizar os nós de entidades (personagens, objetos, locais) no banco de dados de grafos local.
   - Conectar os nós com arestas direcionadas anotadas com a ordem cronológica $T$ do enredo (tempo narrativo, não tempo de escrita).
3. **Auditoria de Conservação Física (Execução de Regras Lógicas):**
   - **Regra de Localização:** Para cada evento em que o personagem $P$ participa no local $X$ em $T_n$, verificar no grafo se o local de $P$ em $T_{n-1}$ era diferente de $X$. Se sim, verificar a existência de uma aresta de viagem ou transição associada a $P$ entre $T_{n-1}$ e $T_n$. Caso contrário, marcar como conflito de teletransporte.
   - **Regra de Posse de Inventário:** Se o evento indica que o personagem $P$ utiliza ou entrega o objeto $O$ em $T_n$, validar se o nó de $O$ está conectado a $P$ por uma aresta de posse ativa em $T_{n-1}$. Se a posse pertencer a outro personagem, acusar conflito de posse.
   - **Regra de Status Vital:** Verificar se existem arestas de ação ativa (falar, caminhar, lutar) partindo de um personagem $P$ em $T_m$ cujo status vital foi registrado como "Morto" em $T_k$ (onde $k < m$).
4. **Propagação e Sinalização de Inconsistência:**
   - Ao detectar um conflito físico nas regras acima, propagar recursivamente a flag `Inconsistente` para todas as metas e cenas descendentes causalmente ligadas no grafo de eventos.
   - Salvar o relatório de conflito no banco e destacar visualmente os pontos de falha na timeline e na wiki do autor.

## Parâmetros e configuração
- `MAX_AUDIT_CHAPTERS`: Número máximo de capítulos processados de forma síncrona em background. Padrão: `100`.
- `STRICT_LOCATION_CHECK`: Se ativo, exige arestas explícitas de viagem para qualquer mudança de local geográfico entre cenas. Padrão: `true`.
- `VITAL_CHECK_ACTIONS`: Lista de verbos de ação ativa que disparam quebra de status vital. Padrão: `["falar", "dizer", "correr", "atacar", "olhar"]`.

## Armadilhas e como evitá-las
- **Armadilha:** Alucinação por RAG Puro: confiar apenas em buscas de similaridade vetorial em bancos RAG para validar consistência física faz o sistema ignorar conflitos binários booleanos (ex: o RAG acha o fato do personagem estar morto "semelhante" a ele estar vivo, falhando em acusar o erro).
  **Mitigação:** Não usar LLM direto para verificar a consistência. O pipeline deve extrair os estados fisicamente e rodar regras booleanas imperativas codificadas em SQL/Código de Grafos sobre a base relacional (SCORE, 2025).

## Critérios de validação (Definition of Done)
- [ ] O algoritmo de auditoria atinge métricas de Precision e Recall superiores a 85% na identificação de buracos de roteiro (plot holes) no benchmark padrão FlawedFictions.
- [ ] O tempo total de travessia do grafo e execução das checagens lógicas é menor que 2 segundos para um manuscrito contendo 100 capítulos e 50 entidades ativas.

## Fundamentação científica
- NarrativeTrack Consortium (2026) - NarrativeTrack: Entity-Centric Reasoning for Narrative Understanding - arXiv 2026
- SCORE (2025) - Story Coherence and Retrieval Enhancement for AI Narratives - arXiv 2025
- Duan, Q. et al. (2026) - TRACE: Tracking, Retrieving, Auditing for Coherent Epics - CHI EA 2026
- Semnani, S. et al. (2025) - Detecting Corpus-Level Knowledge Inconsistencies (CLAIRE, WIKICOLLIDE) - EMNLP 2025

## Requisitos do projeto relacionados
- RF-47 (contradições entre capítulos)
- RF-72 (dependência entre entidades)
- RF-151 (consistência de idade)
- RF-169 (inventário de itens)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: O pipeline de extração automática de eventos via NLP local pode gerar triplas com ruídos ou erros de parsing em prosas muito figurativas.*
*Fallback para v1:* O GTE deve ser alimentado primariamente por ações explícitas do autor ao mover cartões de cena e atualizar inventários na UI do Kanban, reduzindo a dependência de extração automática via NLP no rascunho bruto.

## Exemplos
**Entrada:**
```json
{
  "eventos_historico": [
    {"sujeito": "Lorde Valerius", "acao": "morrer", "objeto": null, "local": "Masmorra", "tempo": 10},
    {"sujeito": "Lorde Valerius", "acao": "falar", "objeto": "carta", "local": "Salão Real", "tempo": 12}
  ]
}
```
**Saída esperada:**
```json
{
  "has_plot_hole": true,
  "conflicts": [
    {
      "entity": "Lorde Valerius",
      "type": "VITAL_STATUS_VIOLATION",
      "description": "O personagem Lorde Valerius executou a ação 'falar' no tempo 12, após seu falecimento registrado no tempo 10.",
      "scenes": [10, 12]
    }
  ]
}
```
**Caso de falha conhecido:**
Ignorar a inconsistência se a ação de falar for uma lembrança ou flashback (deve-se modelar metadados de "tempo" e "tipo de cena" para evitar falsos positivos em memórias/sonhos).
