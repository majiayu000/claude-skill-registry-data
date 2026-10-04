---
name: rag-baseado-em-grafos-pessoais-locais
description: Motor GraphRAG local que responde perguntas complexas de lore usando travessia do grafo do universo ficcional com SLM local.
---
# rag-baseado-em-grafos-pessoais-locais

## Descrição
A skill `rag-baseado-em-grafos-pessoais-locais` implementa o motor local de GraphRAG no sistema de apoio à escrita. Ela combina a busca semântica em documentos com a travessia estruturada do Grafo do Universo Ficcional (GUF) para responder de forma factual a perguntas complexas do autor sobre as interações de seu universo (parentescos, lealdades, eventos cronológicos), injetando o contexto relacional exato em prompts para pequenos modelos de linguagem locais (SLMs) sem estourar suas janelas de contexto.

## Quando usar
Gatilhos concretos e observáveis:
- O autor submete uma dúvida complexa de lore no painel lateral de chat do editor (ex: "quem são os aliados de Kael na Ordem dos Cavaleiros?").
- O escritor solicita um relatório de relacionamentos na wiki de um personagem.
- O assistente de escrita de cenas precisa recuperar a árvore genealógica ou o histórico de interações de duas entidades concorrentes para uma cena de diálogo.

Quando NÃO usar:
- Para buscas simples de termos no texto (usar a skill `busca-hibrida-local-first`).
- Para resumir capítulos completos sequencialmente de forma geral.

## Pré-requisitos
- Banco de dados relacional de grafos local (`sqlite-graph`) contendo os nós de entidades e arestas tipadas de relacionamento.
- Pequeno Modelo de Linguagem local (SLM) otimizado para inferência de instruções (ex: Gemma-2B-IT ou Qwen-2.5-3B) via llama.cpp.
- Dicionário de sinônimos/embeddings para mapear as entidades citadas na pergunta (Entity Lookup).

## Processo (passo a passo executável)
1. **Identificação de Nós Principais (Entity Lookup):**
   - Receber a query do autor.
   - Identificar no texto da pergunta quais entidades cadastradas da wiki são citadas (ex: "Kael", "Ordem dos Cavaleiros").
2. **Travessia Limitada do Grafo (Multi-hop Retrieval):**
   - No banco `sqlite-graph`, buscar os IDs dos nós correspondentes às entidades encontradas na etapa 1.
   - Executar a travessia de arestas adjacentes coletando nós e arestas associadas limitando a profundidade a no máximo $N$ passos configurado em `MAX_HOP_DEPTH` (padrão: `2` hops).
   - Extrair a sub-rede gerada: vértices (ex: "Érebo (Inimigo de Kael)", "Mentor (Mestre de Kael)") e suas arestas explicativas.
3. **Compilação do Prompt Relacional (Graph Prompting):**
   - Recuperar o texto descritivo curto das fichas da wiki correspondentes a cada nó da sub-rede extraída no passo 2.
   - Construir o contexto do prompt listando de forma legível e estruturada os fatos do grafo:
     `Fatos relacionais confirmados do universo:`
     `- Kael é Inimigo de Feiticeiro Érebo (Causa: Érebo assassinou o Mentor de Kael).`
     `- Helena é Aliada de Kael.`
4. **Inferência Factual no SLM Local:**
   - Enviar a pergunta e o contexto estruturado do grafo ao modelo local (Gemma-2B-IT ou Qwen-2.5-3B).
   - Instruir o modelo a se basear estritamente na sub-rede fornecida para responder à pergunta.
5. **Rastreamento de Proveniência:**
   - Adicionar ao final da resposta gerada as referências e citações dos arquivos de notas da wiki correspondentes aos nós utilizados.

## Parâmetros e configuração
- `MAX_HOP_DEPTH`: Profundidade máxima de travessia do grafo relacional a partir do nó de busca. Padrão: `2` (hops).
- `SLM_TEMPERATURE`: Temperatura de geração do modelo de linguagem (valores baixos previnem alucinações). Padrão: `0.20`.
- `MAX_CONTEXT_NODES`: Número máximo de nós adjacentes incluídos no prompt para evitar estouro da janela de contexto. Padrão: `15`.

## Armadilhas e como evitá-las
- **Armadilha:** Context-Overflow de Modelos Pequenos: realizar travessias profundas no grafo (+3 hops) puxa dezenas de nós, arestas e arquivos de texto de descrição. Isso satura rapidamente a janela de atenção de 2K a 4K de tokens de SLMs locais de 2B/3B parâmetros, fazendo o modelo ignorar a pergunta ou sofrer alucinações.
  **Mitigação:** Limitar a expansão de travessia estritamente ao treshold `MAX_HOP_DEPTH = 2` hops. Filtrar e ordenar os nós adjacentes por relevância temporal e peso de relacionamento, mantendo apenas os top `15` nós mais importantes no contexto (RUVA, 2026).

## Critérios de validação (Definition of Done)
- [ ] O GraphRAG atinge acurácia igual ou superior a 90% nas respostas baseadas em conexões indiretas de entidades (ex: descobrir parentesco distante ou relações indiretas de facções).
- [ ] O tempo total de consulta ao banco de grafos e inferência da resposta no SLM local é inferior a 1,5 segundo em CPU local.

## Fundamentação científica
- GraphRAG (Microsoft Research, 2024) - From Local to Global: A Graph RAG Approach - arXiv 2024
- EpisTwin (2026) - Episodic Twins: Enhancing Memory Consolidation in RAG Systems - arXiv 2026
- RUVA (2026) - Reducing Context Overflow in Small Language Models for Narrative Retrieval - arXiv 2026
- OntoRAG (2025) - Enhancing QA through Automated Ontology Derivation (RAG) - arXiv 2025

## Requisitos do projeto relacionados
- RF-106 (responder perguntas)
- RF-158 (responder citando)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: Pequenos modelos de 2B a 3B rodando localmente possuem capacidade de raciocínio lógico menor do que LLMs gigantes de nuvem, podendo cometer falhas na interpretação de arestas de grafos complexos.*
*Fallback para v1:* Se o SLM local falhar nas checagens unitárias, desativar a travessia de grafos no RAG. Utilizar a busca vetorial simples (RAG padrão), injetando diretamente as 5 notas da wiki mais similares e omitindo a representação estruturada de conexões indiretas na v1 do sistema.

## Exemplos
**Entrada (Pergunta):**
- Query: "Qual a relação entre Lorde Valerius e o reino de Solaria?"
- Sub-rede extraída (2 hops): `[Lorde Valerius] --(MembroDe)--> [Ordem dos Cavaleiros] --(Defende)--> [Reino de Solaria]`
**Saída esperada:**
```json
{
  "response": "Lorde Valerius é membro da Ordem dos Cavaleiros, guilda que tem o dever de defender o Reino de Solaria [Wiki: Lorde Valerius, Wiki: Ordem dos Cavaleiros].",
  "nodes_traversed": ["Lorde Valerius", "Ordem dos Cavaleiros", "Reino de Solaria"]
}
```
**Caso de falha conhecido:**
Responder que Lorde Valerius governa Solaria (alucinação) devido a uma fusão errônea de termos de contexto.
