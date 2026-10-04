---
name: rastreamento-arco-emocional-continuo
description: Monitora a flutuacao emocional (valencia e arousal) de personagens ao longo da historia mapeando arquetipos dramaticos.
---
# rastreamento-arco-emocional-continuo

## Descrição
A skill `rastreamento-arco-emocional-continuo` monitora e plota a flutuação de sentimentos (valência e excitação/arousal) associada a um personagem ao longo do romance. Ela analisa a tonalidade emocional da prosa nos trechos de fala e ação do personagem, mapeando a curva resultante a arquétipos dramáticos tradicionais (curvas dramáticas clássicas) no painel de estatísticas do autor.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor conclui a redação de um capítulo (disparado pelo save do arquivo).
- O autor acessa o painel de visualização de "Arco Dramático do Personagem" no editor.
- O sistema analisa a curva de tensão para calibrar sugestões de enredo e ganchos dramáticos.

Quando NÃO usar:
- Em listagens de lore puras (wiki estática) que não correspondam à prosa corrida do manuscrito.
- Para análise gramatical ou ortográfica tradicional.

## Pré-requisitos
- Lema e dicionário NRC Emotion Lexicon adaptado e traduzido para o português.
- Classificador de sentimentos local (ex: BERTimbau-large fine-tuned em literatura) que retorne score contínuo no intervalo $[-1, 1]$.
- Banco de dados de menções de personagens resolvidas.

## Processo (passo a passo executável)
1. **Modelagem Dimensional de Emoção:**
   - Adotar a escala de duas dimensões de Russell:
     - **Valência ($V$):** Mede o tom de positivo ($+1.0$) a negativo ($-1.0$).
     - **Excitação/Arousal ($A$):** Mede a ativação de ativo/excitado ($+1.0$) a passivo/calmo ($-1.0$).
2. **Segmentação e Extração por Bloco Narrativo:**
   - Para o personagem selecionado, extrair todos os parágrafos em que ele é mencionado ou é o falante ativo de um capítulo.
   - Segmentar o trecho em blocos de sentenças.
   - Computar os scores contínuos de valência ($V_i$) e excitação ($A_i$) usando o classificador local e a busca de termos no NRC Lexicon.
3. **Filtro de Inversão por Ironia:**
   - Analisar a presença de modificadores gramaticais ou marcadores de ironia regex.
   - Caso identificados, multiplicar o score de valência $V_i$ por $-0.8$ para inverter a polaridade (ex: uma exclamação sarcástica "Que ótimo!" passa a ter peso de valência negativo).
4. **Cálculo da Curva Suavizada (Rolling Mean):**
   - Aplicar uma média móvel simples sobre a sequência temporal de sentenças do personagem com tamanho de janela parametrizado em `SMOOTHING_WINDOW_SIZE` (padrão: `7` sentenças; a literatura recomenda de 5 a 10 sentenças; adotamos 7 como valor padrão da engenharia).
5. **Classificação de Arquétipo Dramático:**
   - Comparar a curva suavizada contra os perfis geométricos de curvas clássicas de Vonnegut (ex: *Rags to Riches* - ascensão contínua, *Man in a Hole* - queda seguida de ascensão, *Icarus* - ascensão seguida de queda).
   - Retornar a classificação de arquétipo mais próxima com base na correlação de distância geométrica.

## Parâmetros e configuração
- `SMOOTHING_WINDOW_SIZE`: Tamanho da janela de média móvel para suavização da curva emocional. Padrão: `7` (sentenças).
- `AROUSEL_ACTIVATION_THRESHOLD`: Limiar mínimo de score de excitação para considerar a cena de "alta tensão". Padrão: `0.50`.
- `EMOTION_CLASSIFIER_MODEL`: Nome do modelo local de análise de sentimento. Padrão: `BERTimbau-sentiment-literary`.

## Armadilhas e como evitá-las
- **Armadilha:** Amortecimento por Janela Excessiva: se o tamanho da média móvel for muito longo, picos de emoção rápidos e cenas cruciais de choque (ex: revelação ou morte de um personagem que dura apenas 2 parágrafos) serão filtrados e a curva resultante parecerá plana e sem sentido dramático.
  **Mitigação:** Manter a janela `SMOOTHING_WINDOW_SIZE` configurável na interface e limitada ao limite máximo de 10 sentenças. Permitir ao escritor dar zoom em cenas específicas desativando a suavização temporariamente para ver os picos emocionais brutos.

## Critérios de validação (Definition of Done)
- [ ] A correlação de Pearson entre o arco emocional contínuo gerado pelo sistema e a anotação manual humana atinge no mínimo 0.72 em datasets literários padrão.
- [ ] A identificação do arquétipo dramático de Vonnegut corresponde ao planejado no outline do autor em 90% dos testes.

## Fundamentação científica
- Teodorescu, L. & Mohammad, S. (2023) - Evaluating Emotion Arcs Across Languages - arXiv 2023
- Continuous Sentiment (2025) - Continuous Sentiment Scores for Literary and Multilingual Contexts - arXiv 2025
- Mohammad, S. (2013) - From Once Upon a Time to Happily Ever After: Tracking Emotions in Novels - arXiv 2013
- Elkins, K. & Chun, J. (2018) - Can Sentiment Analysis Reveal Structure in a Plotless Novel? - arXiv 2018

## Requisitos do projeto relacionados
- RF-150 (arco de emoções)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: Textos literários com narradores não confiáveis, ironia profunda ou tom altamente neutro/metafórico podem gerar scores de valência instáveis.*
*Fallback para v1:* Implementar uma classificação simplificada baseada puramente em sentimentos discretos por cena (positivo, negativo, neutro) e omitir o cálculo bidimensional de excitação (arousal) e a inferência de arquétipos geométricos na v1 do painel do romance.

## Exemplos
**Entrada (Sentenças de Kael):**
```json
[
  {"text": "Kael celebrou com seus amigos a vitória na taverna.", "V": 0.8, "A": 0.6},
  {"text": "Mas no dia seguinte, Kael recebeu a notícia que seu vilarejo havia sido destruído.", "V": -0.9, "A": 0.7}
]
```
**Saída esperada (Valência e Arousal suavizados no tempo):**
```json
{
  "points": [
    {"time": 1, "valência": 0.8, "excitação": 0.6},
    {"time": 2, "valência": -0.9, "excitação": 0.7}
  ],
  "dramatic_archetype": "Icarus (Ascensão seguida de Queda rápida)"
}
```
**Caso de falha conhecido:**
Exibir uma curva emocional plana e constante ao longo de um capítulo inteiro que contém a morte dramática do antagonista devido a uma suavização excessiva da janela de média móvel.
