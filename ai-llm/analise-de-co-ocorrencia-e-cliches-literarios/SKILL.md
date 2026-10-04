---
name: analise-de-co-ocorrencia-e-cliches-literarios
description: Compara densidade de tropos do romance com benchmarks de genero e sugere rotas de subversao criativa preservando a agencia autoral.
---
# analise-de-co-ocorrencia-e-cliches-literarios

## Descrição
A skill `analise-de-co-ocorrencia-e-cliches-literarios` analisa a densidade de clichês estruturais no romance comparando o conjunto de tropos detectados com as estatísticas de gênero literário. Ela gera representações gráficas no radar de "DNA Narrativo" e sugere de forma proativa caminhos opcionais de subversão de roteiro, mantendo o controle sob a agência artística do escritor.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor abre o dashboard de planejamento ou visualiza o painel "Radar de DNA de Gênero" da obra.
- A quantidade de tropos validados no banco de dados do romance é alterada.
- O autor solicita brainstorm de novas ideias na sidebar do editor e precisa quebrar um bloqueio criativo de trama.

Quando NÃO usar:
- Para realizar buscas lexicais de termos ou formatações simples.
- Para impor restrições mecânicas rígidas que limitem as escolhas estéticas do romancista.

## Pré-requisitos
- Tabela de correspondência estatística de tropos por gênero literário indexada (ex: dados do Fantasy Tropes Analysis, 2025).
- Lista de tropos validados no romance.
- Acesso ao modelo de geração de ideias local (SLM) para sugestões de subversão.

## Processo (passo a passo executável)
1. **Compilação do Perfil de DNA de Gênero:**
   - Agrupar os tropos validados da obra em quatro supercategorias: `Character` (personagem), `Plot` (enredo), `Setting` (cenário) e `Theme` (tema).
   - Calcular a frequência relativa e plotar o gráfico de radar comparando os scores do livro com as distribuições médias do gênero selecionado do romance (ex: fantasia épica, ficção científica, suspense).
2. **Auditoria de Densidade de Clichê (Co-ocorrência):**
   - Varrer a rede de tropos do livro buscando subgrafos hiperconectados conhecidos por formar clichês tradicionais (ex: a presença conjunta de *Chosen One* + *Ancient Prophecy* + *Mentor Death* + *Kingdom under Threat*).
   - Se a correlação acumulada dos tropos no mesmo capítulo exceder o limiar de segurança `CLICHE_CORRELATION_LIMIT = 0.85`, acionar o sinalizador de alerta de clichê.
3. **Módulo de Sugestão de Subversão Proativa:**
   - Para os pacotes de clichê acionados na etapa 2, consultar a base de variantes de desconstrução.
   - Chamar o SLM local usando uma técnica de prompting de inversão de premissas (ex: *"O mestre morre no Ato I, mas na verdade ele apenas simulou o próprio assassinato por motivos políticos, passando a operar como um espião nas sombras"*).
   - Apresentar as rotas de subversão como sugestões opcionais de escrita na barra de ferramentas.

## Parâmetros e configuração
- `CLICHE_CORRELATION_LIMIT`: Coeficiente de correlação estatística acumulado necessário para acionar aviso de clichê. Padrão: `0.85`.
- `MAX_SUBVERSION_SUGGESTIONS`: Número máximo de ideias alternativas de roteiro sugeridas de cada vez. Padrão: `3`.
- `GENRE_RADAR_METRIC`: Tipo de normalização aplicada aos dados de gênero. Padrão: `"Z-score"`.

## Armadilhas e como evitá-las
- **Armadilha:** Bloqueio de Liberdade Autoral: o sistema de IA marcar tropos comuns como erros lógicos ou forçar o autor a alterá-los. Tropos e clichês de gênero são estruturas dramáticas válidas e adoradas por leitores. Castrar o autor gera frustração e alienação.
  **Mitigação:** Proibir qualquer mensagem punitiva ou alerta de "erro de escrita" associada a clichês. Tratar o dashboard de clichês de forma puramente analítica (ex: exibindo percentuais comparativos: *"Seu livro possui 15% mais tropos clássicos de fantasia do que a média"*). As sugestões de subversão devem ser descritas como *"Opções alternativas e caminhos criativos de quebra de expectativa"*, deixando a decisão estética final sempre sob controle humano (Genre-Specific Clichés, 2025).

## Critérios de validação (Definition of Done)
- [ ] A acurácia na classificação estatística de gênero baseada unicamente na rede de tropos extraída atinge no mínimo 90% perante os dados de benchmark.
- [ ] O radar de DNA é renderizado a 60 FPS estáveis na interface gráfica.

## Fundamentação científica
- Fantasy Tropes Analysis (2025) - A Distant Reading Approach to Fantasy Tropes - arXiv 2025
- Genre-Specific Clichés (2025) - Genre-Specific Clichés and Reader Expectation: A Survey - Journal of Literary studies 2025
- Narrative Patterns in SF (2024) - Narrative Patterns and Trope Co-occurrence in Science Fiction - arXiv 2024
- Moretti, F. (2013) - Distant Reading - Verso Books 2013

## Requisitos do projeto relacionados
- RF-173 (tropos recomendados)
- RF-174 (brainstorm de arcos)
- RF-149 (arco dramático)

## Maturidade e riscos de adoção
**Nível:** Consolidada/Emergente.
*A modelagem e visualização estatística de dados comparativos Z-score de tropos é estável; a sugestão dinâmica de desconstruções por IA é a camada emergente.*

## Exemplos
**Entrada (Lista de Tropos Validados no Capítulo):**
```json
{
  "genre": "Fantasia",
  "detected_tropes": ["Chosen One", "Ancient Prophecy", "Mentor Death"]
}
```
**Saída esperada (Avisos analíticos e sugestões):**
```json
{
  "cliché_density": "Alta correlação estrutural detectada (0.89).",
  "radar_comparison": {
    "Chosen One": "+25% acima da média do gênero",
    "Ancient Prophecy": "+18% acima da média do gênero"
  },
  "subversion_suggestions": [
    "O protagonista descobre que a profecia era falsa, forjada pelo vilão para manipulá-lo.",
    "O mentor simula sua morte para forçar o protagonista a agir por conta própria."
  ]
}
```
**Caso de falha conhecido:**
Exibir alertas vermelhos de erro impedindo o salvamento do capítulo alegando "presença excessiva de clichês", quebrando as regras de agência e privacidade criativa do autor.
