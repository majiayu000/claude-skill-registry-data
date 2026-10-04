---
name: entity-linking-wikidata-local
description: Vincula entidades extraidas do manuscrito a entradas do Wikidata usando um indice SQLite local sem chamadas de API.
---
# entity-linking-wikidata-local

## Descrição
A skill `entity-linking-wikidata-local` conecta entidades geográficas e históricas mencionadas no texto do romance a identificadores universais do Wikidata (QIDs), enquanto constrói e mantém uma ontologia dinâmica em memória para os personagens e locais fictícios criados pelo próprio autor. Ela utiliza um motor de linkagem leve local baseado em grafos para resolver ambiguidades sem enviar manuscritos privados a APIs proprietárias na nuvem.

## Quando usar
Gatilhos concretos e observáveis:
- O autor insere notas de worldbuilding históricas ou geográficas e solicita referências ou verificação de fatos reais.
- O pipeline de PLN do editor extrai entidades do tipo `LOCAL` ou `PERSONAGEM_HISTORICO` e precisa associar dados de geolocalização ou biografia real.
- O usuário ativa o assistente de links de referências no painel lateral do editor.

Quando NÃO usar:
- Para realizar buscas lexicais simples em dicionários locais sem dependência de contexto de desambiguação.
- Quando o romance for puramente contemporâneo e não fizer referências a dados de contexto histórico real.

## Pré-requisitos
- Base de dados Wikidata local indexada (versão resumida ou subconjunto geográfico/histórico em formato SQLite/DuckDB).
- Embeddings locais carregados na RAM (ex: FastText ou BERTimbau) para representação vetorial de tópicos de contexto.
- Banco de dados local do romance contendo a lista de personagens fictícios ativos para filtragem primária.

## Processo (passo a passo executável)
1. **Filtro de Ficcionalidade:**
   - Comparar cada entidade extraída pelo NER com a tabela de personagens e locais do banco de dados local do romance.
   - Se houver match exato ou parcial de alta confiança com uma entidade já cadastrada como fictícia pelo autor, classificar o nó como `FICÇÃO` e pular a busca no Wikidata.
2. **Construção da Ontologia Local (On-the-fly):**
   - Para os nós marcados como `FICÇÃO`, verificar se já existem no Grafo do Universo Ficcional (GUF) local. Se não, instanciar um novo nó na ontologia local temporária mapeando suas relações descritas na frase.
3. **Candidatos Wikidata (Para Entidades Reais):**
   - Para as entidades não filtradas no passo 1, buscar no banco Wikidata local candidatos homônimos e seus respectivos QIDs, aliases e descrições curtas.
4. **Desambiguação Contextual (Princípio OpenTapioca):**
   - Extrair o vetor de tópicos $C_{text}$ do parágrafo adjacente (janela de 3 parágrafos) usando o modelo de embeddings.
   - Computar a similaridade de cosseno entre $C_{text}$ e a descrição/tópicos dos nós candidatos no grafo do Wikidata.
   - Atribuir o QID do candidato que apresentar a maior similaridade de cosseno (limiar configurável `SIMILARITY_THRESHOLD = 0.75`).
5. **Retorno:** Retornar os nós anotados com QID (factuais) ou ID Local (ficcionais).

## Parâmetros e configuração
- `SIMILARITY_THRESHOLD`: Limiar de similaridade de cosseno para resolução de ambiguidade de tópicos. Padrão: `0.75`.
- `MAX_CANDIDATES`: Número máximo de candidatos recuperados do banco local para desambiguação. Padrão: `5`.
- `WIKIDATA_DB_PATH`: Caminho do arquivo SQLite local contendo o dump compactado do Wikidata. Padrão: `./data/wikidata_mini.db`.

## Armadilhas e como evitá-las
- **Armadilha:** Sobre-associação a Bases Externas: o sistema tenta associar a todo custo nomes fictícios criados pelo autor a nós reais do Wikidata (ex: associar um protagonista fictício chamado "Júlio César" ao imperador romano).
  **Mitigação:** Se o candidato do Wikidata com maior score apresentar similaridade de contexto com o parágrafo menor que `0.60`, descartar a linkagem externa. Catalogar o nó estritamente na ontologia local de ficção.

## Critérios de validação (Definition of Done)
- [ ] Precision@5 de linkagem para entidades factuais (locais geográficos históricos reais) atinge no mínimo 80% sobre os datasets de teste (ex: Mahānāma adaptado).
- [ ] A latência de busca e desambiguação no grafo local é inferior a 500ms por entidade analisada.

## Fundamentação científica
- Delasalles, L. et al. (2020) - OpenTapioca: Lightweight Entity Linking for Wikidata - CEUR 2020
- Scharpf, P. et al. (2022) - Survey on English Entity Linking on Wikidata - Semantic Web Journal
- Sarkar, R. et al. (2025) - Mahānāma: Literary Entity Discovery and Linking - EMNLP 2025

## Requisitos do projeto relacionados
- RF-111 (Wikidata)
- RF-113 (busca contextual)
- RF-33 (links para referências)

## Maturidade e riscos de adoção
**Nível:** Emergente/Experimental.
*Risco: O dump local do Wikidata compactado em SQLite pode apresentar cobertura limitada de entidades históricas de nicho ou exigir armazenamento em disco elevado (ex: >2 GB).*
*Fallback para v1:* Desativar o motor de desambiguação por grafos dinâmicos. Implementar um dicionário estático contendo apenas cidades e países mais comuns e linkar termos não catalogados diretamente como entidades fictícias.

## Exemplos
**Entrada:**
```json
{
  "mention": "Paris",
  "context": "Dom Pedro II viajou para Paris para se encontrar com intelectuais franceses no século XIX.",
  "fictional_entities": []
}
```
**Saída esperada:**
```json
{
  "mention": "Paris",
  "canonical_name": "Paris",
  "qid": "Q90",
  "source": "Wikidata",
  "confidence": 0.94
}
```
**Caso de falha conhecido:**
Linkar a palavra "Paris" ao herói mitológico grego "Páris" (Q167646) em um contexto de viagem geográfica oitocentista.
