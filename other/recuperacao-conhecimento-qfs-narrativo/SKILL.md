---
name: recuperacao-conhecimento-qfs-narrativo
description: Responde perguntas do autor sobre o manuscrito usando RAG hibrido local com citacao de fontes (capitulos e notas).
---
# recuperacao-conhecimento-qfs-narrativo

## Descrição
A skill `recuperacao-conhecimento-qfs-narrativo` responde a perguntas específicas do autor sobre os acontecimentos do manuscrito e regras do universo da história (QFS - Query-Focused Summarization). Ela utiliza um pipeline local híbrido de recuperação de informações (vetorial + lexical) associado a técnicas de geração aumentada por recuperação (RAG) para consolidar e sumarizar respostas citando as fontes exatas (capítulos e notas) do projeto de escrita.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor insere uma dúvida ou pergunta em linguagem natural no painel lateral de consulta do editor (ex: "onde a espada de ferro foi guardada?", "qual a relação entre Kael e Helena?").
- O autor pesquisa termos na barra de busca semântica global da wiki do romance.
- O assistente de escrita precisa recuperar fatos consolidados sobre uma entidade para calibrar uma nova sugestão de texto.

Quando NÃO usar:
- Para gerar resumos globais de capítulos inteiros sem perguntas associadas.
- Em buscas lexicais simples de correspondência exata de palavras (onde a busca esparsa simples de banco de dados resolve sem LLM).

## Pré-requisitos
- Banco de dados vetorial de chunks locais (SQLite-VSS, DuckDB ou RAGdb local) contendo os textos segmentados do romance e da wiki.
- Motor de busca BM25 integrado para indexação lexical esparsa.
- Modelo de linguagem local (SLM) operando na máquina do usuário.

## Processo (passo a passo executável)
1. **Busca Híbrida de Contexto:**
   - Receber a pergunta (query) do autor.
   - Disparar em paralelo duas buscas locais nos textos do manuscrito e notas:
     - *Busca Vetorial:* Similaridade de cosseno usando embeddings locais da query.
     - *Busca Lexical:* Correspondência de palavras-chave usando o algoritmo BM25.
   - Fundir e ordenar os resultados usando RRF (Reciprocal Rank Fusion) com constante $k=60$ para recuperar os $N$ chunks de texto mais relevantes (padrão `TOP_CHUNKS = 5`).
2. **Geração da Resposta Sumarizada (QFS):**
   - Construir o prompt de inferência contendo a pergunta do autor e os textos dos chunks recuperados de forma estruturada.
   - Executar a geração no SLM local instruindo-o a responder de forma concisa e factual, proibindo o uso de informações externas à base do livro.
3. **Ancoragem de Citações (Grounding):**
   - Para cada afirmação feita na resposta, anexar obrigatoriamente a citação do arquivo/capítulo de origem da informação (ex: `[Capítulo 2, p. 12]`, `[Wiki: Helena Silva]`).
4. **Tratamento de Insuficiência de Dados:**
   - Se a pontuação de relevância dos chunks recuperados na etapa 1 for inferior ao threshold mínimo `RELEVANCE_THRESHOLD = 0.50`, abortar a geração e retornar a mensagem: *"Informação não encontrada no manuscrito ou na wiki do romance."*

## Parâmetros e configuração
- `TOP_CHUNKS`: Quantidade de trechos de texto recuperados na busca híbrida para alimentar o prompt. Padrão: `5`.
- `RELEVANCE_THRESHOLD`: Limiar de relevância de cosseno mínimo para aceitar os chunks recuperados. Padrão: `0.50`.
- `MAX_RESPONSE_WORDS`: Limite de extensão da resposta sumariada gerada. Padrão: `200` palavras.

## Armadilhas e como evitá-las
- **Armadilha:** Alucinação por Conhecimento Prévio de RAG: o LLM local responde à pergunta do autor introduzindo fatos históricos reais ou mitológicos externos que não constam no manuscrito, corrompendo a verdade do universo inventado.
  **Mitigação:** Incluir uma instrução de sistema estrita no prompt (System Prompt): *"Responda apenas com base nos fatos contidos nos trechos fornecidos. Se a resposta não estiver descrita neles, responda exatamente 'Não encontrei essa informação no manuscrito'. Nunca invente fatos."*

## Critérios de validação (Definition of Done)
- [ ] O sistema atinge uma precisão factual (grounding score) de no mínimo 92% perante as passagens recuperadas sob testes automatizados.
- [ ] Todas as frases da resposta gerada apontam corretamente a referência e citação do arquivo de origem (100% de cobertura de referências internas).

## Fundamentação científica
- QFS-KIT (2021) - Tackling Query-Focused Summarization as Knowledge-Intensive Task - arXiv 2021
- BeyondRD (2024) - Beyond Relevant Documents: Knowledge-Intensive QFS with LLMs - arXiv 2024
- OntoRAG (2025) - Enhancing QA through Automated Ontology Derivation (RAG) - arXiv 2025

## Requisitos do projeto relacionados
- RF-24 (busca semântica)
- RF-28 (busca contextual)
- RF-90 (wiki do universo)
- RF-106 (responder perguntas)
- RF-158 (responder citando)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A recuperação RAG híbrida local com restrição de prompt baseada em fontes locais é uma técnica estável, amplamente utilizada e de baixo risco operacional.*

## Exemplos
**Entrada:**
```json
{
  "query": "Quem entregou a espada mágica para Kael?",
  "chunks": [
    {"source": "Capítulo 3", "text": "O velho ferreiro Morgan entregou a espada mágica de prata para Kael antes de partir."},
    {"source": "Capítulo 1", "text": "Kael treinou esgrima na floresta com uma espada de madeira."}
  ]
}
```
**Saída esperada:**
```json
{
  "response": "A espada mágica de prata foi entregue a Kael pelo velho ferreiro Morgan [Capítulo 3].",
  "sources": ["Capítulo 3"]
}
```
**Caso de falha conhecido:**
Responder "A Dama do Lago entregou a Excalibur para Arthur" baseando-se em lendas reais, ignorando o texto do autor sobre Kael e Morgan.
