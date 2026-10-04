---
name: resolucao-correferencia-e-aliases-literarios
description: Resolve referencias pronominais e aliases de personagens em romance, unificando mencoes sob um ID canonico.
---
# resolucao-correferencia-e-aliases-literarios

## Descrição
A skill `resolucao-correferencia-e-aliases-literarios` resolve a coesão do elenco literário ao agrupar variações de nomes (aliases), epítetos (apelidos contextuais) e referências pronominais (ele, ela, seu, etc.) de volta à entidade canônica do personagem correspondente. Ela atua em nível de documento, realizando a desambiguação de menções indiretas em textos narrativos longos com base em redes locais de coocorrência e análise de papel sintático.

## Quando usar
Gatilhos concretos e observáveis:
- O sistema é solicitado a gerar ou atualizar a rede social de personagens de um capítulo ou livro completo.
- O autor vincula ou atualiza uma ficha de personagem no banco de dados, exigindo remapeamento de menções no texto.
- O pipeline de escrita atualiza o outline de uma cena e precisa mapear quais personagens participam ativamente da ação dramática.

Quando NÃO usar:
- Quando o texto analisado não contiver personagens ou entidades fictícias de tipo `PESSOA`.
- Para detecção isolada de nomes (deve rodar obrigatoriamente após a execução do motor NER).

## Pré-requisitos
- Saída estruturada (JSON) da skill `deteccao-entidades-literarias-portugues` contendo as entidades extraídas e suas posições (char_start, char_end).
- Analisador de dependências sintáticas (ex: parser UDPipe ou SpaCy adaptado para português) para extração de papéis de sujeito/objeto.
- Algoritmo de distância métrica de strings (ex: Jaro-Winkler).

## Processo (passo a passo executável)
1. **Filtro de Entidades:** Receber a lista de entidades detectadas pelo NER e isolar as do tipo `PESSOA` e os pronomes pessoais correspondentes.
2. **Resolução de Aliases Parciais:**
   - Para cada entidade candidata, comparar com as entidades canônicas do banco usando a métrica Jaro-Winkler (threshold configurável `STRING_SIMILARITY_THRESHOLD = 0.85`).
   - Se houver correspondência, associar a menção parcial (ex: "Sra. Silva") à entidade canônica correspondente ("Helena Silva").
3. **Resolução Pronomial (Janela Deslizante):**
   - Para cada pronome pessoal de terceira pessoa (ele, ela, eles, elas), definir uma janela deslizante contendo as últimas $N$ sentenças anteriores no texto (padrão `WINDOW_SENTENCES = 7`).
   - Mapear os candidatos do tipo `PESSOA` presentes nessa janela.
4. **Cálculo de Pontuação de Agência (Heurística Jahan et al., 2020):**
   - Utilizar a árvore de dependências para identificar o papel sintático de cada candidato na janela.
   - Atribuir peso $+2.0$ para sujeitos de verbos de elocução (falar, dizer, gritar), $+1.5$ para sujeitos de ações físicas e $+0.5$ para objetos diretos/indiretos.
5. **Agrupamento por Rede de Coocorrência (Heurística Taggus):**
   - Calcular a frequência de coocorrência espacial entre o pronome/alias e os candidatos no grafo local de parágrafos.
   - Vincular a referência ao candidato com maior pontuação combinada (soma da similaridade de string, pontuação de agência e frequência de coocorrência).
6. **Consolidação:** Atualizar a lista de entidades atribuindo a cada menção um `canonical_id`.

## Parâmetros e configuração
- `STRING_SIMILARITY_THRESHOLD`: Limiar mínimo de similaridade Jaro-Winkler para fusão de nomes. Padrão: `0.85`.
- `WINDOW_SENTENCES`: Janela de sentenças anteriores para busca de antecedentes pronominais. Padrão: `7` (recomendado pela literatura de 5 a 10 sentenças; adotamos 7 como valor médio configurável).
- `AGENCY_WEIGHT_SUBJECT`: Multiplicador para candidatos atuando como sujeitos gramaticais. Padrão: `1.5`.
- `AGENCY_WEIGHT_VERB_OF_SPEAKING`: Multiplicador para sujeitos de verbos de elocução. Padrão: `2.0`.

## Armadilhas e como evitá-las
- **Armadilha:** Perda de Referências Distantes: em romances, a resolução tradicional baseada puramente em distância física (janela de sentenças) falha quando um personagem é reintroduzido após longo hiato por pronomes.
  **Mitigação:** Se o score do candidato na janela local for ambíguo (diferença de pontuação entre os dois principais $< 0.15$), expandir a busca consultando o grafo de entidades da cena ativa (rede local de coocorrência do Taggus) e selecionar o personagem com maior peso de centralidade na cena.

## Critérios de validação (Definition of Done)
- [ ] O algoritmo atinge F1-Score mínimo de 75% no agrupamento de aliases sob o dataset de validação LitBank Coreference adaptado.
- [ ] Casos de ambiguidade nominal simples (ex: "Maria Silva" e "Sra. Silva" no mesmo capítulo) são agrupados no mesmo `canonical_id` em 100% dos testes de regressão.

## Fundamentação científica
- Vala, H. et al. (2015) - Mr. Bennet, his coachman... - EMNLP 2015
- Bamman, D., Lewke, O. & Mansoor, A. (2020) - Annotated Dataset of Coreference in English Literature - LREC 2020
- Jahan, M. et al. (2020) - Narratologically Grounded Character Identification - COLING 2020
- Canário, J. et al. (2025) - Taggus: pipeline redes sociais em ficção portuguesa - arXiv 2025

## Requisitos do projeto relacionados
- RF-109 (unificação de entidades)
- RF-146 (detecção de variações de nomes)
- RF-147 (aliases)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: O modelo pode incorrer em falsas conexões de pronomes em cenas com alta densidade de diálogos cruzados (múltiplos interlocutores do mesmo gênero).*
*Fallback para v1:* Usar correspondência exata de substrings para aliases e limitar a resolução de pronomes a regras heurísticas estritas baseadas puramente em distância gramatical imediata (mesma frase e frase anterior).

## Exemplos
**Entrada:**
```json
{
  "entities": [
    {"text": "Afonso da Maia", "category": "PESSOA", "char_start": 0, "char_end": 14},
    {"text": "ele", "category": "PRONOME", "char_start": 30, "char_end": 33}
  ],
  "text": "Afonso da Maia sentou-se na poltrona. Como ele estava velho!"
}
```
**Saída esperada:**
```json
[
  {"text": "Afonso da Maia", "category": "PESSOA", "canonical_id": "char_afonso_da_maia"},
  {"text": "ele", "category": "PRONOME", "canonical_id": "char_afonso_da_maia"}
]
```
**Caso de falha conhecido:**
Vincular o pronome "ele" a um personagem secundário mencionado em outra frase apenas porque este apareceu gramaticalmente mais perto, ignorando o sujeito principal ("Afonso da Maia").
