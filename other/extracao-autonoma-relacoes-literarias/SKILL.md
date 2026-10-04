---
name: extracao-autonoma-relacoes-literarias
description: Extrai automaticamente relacionamentos e fatos de manuscritos usando pipeline multiagente local para popular o grafo do universo.
---
# extracao-autonoma-relacoes-literarias

## Descrição
A skill `extracao-autonoma-relacoes-literarias` realiza a extração não-supervisionada de relacionamentos, eventos e fatos a partir dos rascunhos de manuscritos e notas de worldbuilding do autor. Ela utiliza um pipeline de extração conjunta de entidades e relações acoplado a uma orquestração multiagente local para povoar o Grafo do Universo Ficcional (GUF), prevenindo a multiplicação indesejada de nós redundantes.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor importa um arquivo de texto (.docx, .txt, .md) contendo notas de planejamento ou rascunhos de capítulos.
- O autor salva um capítulo concluído no editor.
- O usuário dispara uma ação de "Varredura Automática de Relacionamentos" no painel da wiki ou do grafo.

Quando NÃO usar:
- Para realizar buscas lexicais simples sem extração estruturada de arestas (relação sujeito-verbo-objeto).
- Durante o fluxo de digitação em tempo real (deve rodar de forma assíncrona sob demanda para evitar alta latência e consumo de CPU/GPU).

## Pré-requisitos
- Modelo de linguagem local (LLM local de tamanho intermediário, ex: Llama-3-8B quantizado, ou Qwen-2.5-7B) rodando via Triton ou llama.cpp.
- Pipeline de classificação conjunta de entidades e relações (Joint Entity-Relation Extraction).
- Acesso de leitura/escrita ao banco de dados relacional de grafos do romance.

## Processo (passo a passo executável)
1. **Pipeline de Extração Conjunta (Joint Extraction):**
   - Receber o texto bruto de entrada.
   - Executar a predição simultânea de nomes e arestas relacionais por meio do classificador conjunto, gerando triplas temporárias do tipo: `(entidade_1, relacao, entidade_2)`. Isso evita erros cumulativos (quando o NER erra a marcação da palavra e invalida o detector de relações).
2. **Orquestração Multiagente (Loop KnoBuilder):**
   - Instanciar e executar três agentes especializados baseados no LLM local:
     - **Agente A (Extrator de Lore):** Recebe o bloco de texto e gera as triplas e metadados contextuais (tipo de relação, local, tempo narrativo) em formato JSON bruto.
     - **Agente B (Auditor de Duplicidade):** Compara as entidades do JSON geradas pelo Agente A contra os nós já cadastrados no banco de dados local. Se "Arthur de Pendragon" for extraído, mas "Arthur" já existir, unificar as menções sob o mesmo identificador (canonical ID).
     - **Agente C (Integrador de Grafo):** Avalia se as novas triplas contradizem ou duplicam as arestas existentes. Atualiza as quádruplas temporais e salva no banco de dados do romance.
3. **Filtro de Subjetividade Contextual (CTiKG):**
   - Analisar orações subordinadas e verbos mentais (ex: achar, pensar, sonhar).
   - Se o texto indicar uma crença subjetiva (ex: "João acreditava que Lúcia era uma espia"), categorizar a aresta sob a classe `MentalRelation` em vez de criar uma aresta factual `EspiaDe(Lúcia, FactionX)`.

## Parâmetros e configuração
- `EXTRACTION_CONCURRENCY_AGENTS`: Número de agentes concorrentes rodando no loop de consistência. Padrão: `3`.
- `SUBJETIVE_VERB_LIST`: Lista de verbos que qualificam a aresta como mental/subjetiva. Padrão: `["pensar", "achar", "acreditar", "sonhar", "imaginar", "suspeitar"]`.
- `FUSION_CONFIDENCE_THRESHOLD`: Limiar mínimo de similaridade semântica para fusão automática de nós feita pelo Agente B. Padrão: `0.80`.

## Armadilhas e como evitá-las
- **Armadilha:** Propagação de Nós Duplicados: a extração automática gera dezenas de nós para o mesmo personagem sob apelidos ou variações gramaticais (ex: "Valerius", "Lorde Valerius", "Valerius da Masmorra" tratados como 3 personagens distintos).
  **Mitigação:** Bloquear a inserção direta de novas entidades no grafo central sem a aprovação do Agente B (Auditor). Caso a similaridade caia na zona cinzenta ($0.60$ a $0.80$), apresentar uma janela pop-up na UI perguntando ao autor: *"Valerius da Masmorra é o mesmo que Lorde Valerius?"* antes de atualizar o banco de dados.

## Critérios de validação (Definition of Done)
- [ ] O pipeline atinge F1-score mínimo de 85% na extração conjunta de triplas literárias sobre os dados do corpus de validação de worldbuilding.
- [ ] O loop de unificação do Agente B resolve duplicidades simples em 100% dos testes unitários de integração.

## Fundamentação científica
- KnoBuilder (2025) - LLM-Agent for Autonomous KG Construction - NeurIPS NORA 2025
- CTiKG (2026) - Context-aware Entity-Relation Extraction - arXiv 2026
- Chen, Y. et al. (2025) - Joint Entity-Relation Extraction for KG Construction - Applied Sciences 2025

## Requisitos do projeto relacionados
- RF-18 (auto-extrair)
- RF-107 (identificar entidades)
- RF-147 (sugerir fusão)
- RF-108 (atualizar entidades)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: O processamento multiagente síncrono local via LLM é pesado e pode demorar de 15 a 30 segundos por capítulo longo, consumindo até 6 GB de VRAM.*
*Fallback para v1:* Executar a extração de forma puramente linear em background (single-agent), permitindo ao autor revisar e aprovar cada relacionamento sugerido em uma fila de notificações, eliminando o loop de auto-refinamento concorrente.

## Exemplos
**Entrada:**
```json
{
  "text": "Arthur suspeitava que seu padastro Morgan havia roubado a chave do cofre da taverna em Dover."
}
```
**Saída esperada:**
```json
[
  {
    "subject": "Morgan",
    "predicate": "RelacaoParentesco",
    "object": "Arthur",
    "is_factual": true
  },
  {
    "subject": "Arthur",
    "predicate": "SuspeitaDeRoubo",
    "object": "Morgan",
    "is_factual": false,
    "target_item": "chave do cofre"
  }
]
```
**Caso de falha conhecido:**
Criar uma aresta factual de roubo `Roubou(Morgan, chave_do_cofre)` quando o texto expressa apenas uma suspeita subjetiva do personagem Arthur.
