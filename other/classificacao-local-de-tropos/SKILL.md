---
name: classificacao-local-de-tropos
description: Classifica tropos narrativos da ontologia PT-500 em capitulos usando BERTimbau local com janelas deslizantes e max-pooling.
---
# classificacao-local-de-tropos

## Descrição
A skill `classificacao-local-de-tropos` realiza a classificação multi-label local do manuscrito para identificar trechos candidatos à presença de tropos narrativos definidos na ontologia PT-500 (uma coleção de 500 tropos literários comuns, como *Chosen One*, *Mentor Death*, *Ancient Prophecy*). Ela opera de forma rápida localmente em janelas deslizantes de texto, fornecendo a triagem primária de clichês estruturais no romance.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor salva o capítulo em edição no editor de texto rico.
- Ocorre o upload ou a ingestão de um manuscrito literário novo na plataforma.
- O autor dispara uma requisição manual de "Mapeamento de DNA de Tropos" no painel de worldbuilding.

Quando NÃO usar:
- Para validar a consistência factual lógica de fatos de personagens (usar a skill `auditoria-global-consistencia-entidades`).
- Em notas de worldbuilding curtas ou brainstormings fragmentados que não possuam prosa literária fluida.

## Pré-requisitos
- Modelo classificador local: `BERTimbau-large` (2.4 GB) fine-tuned para as 500 categorias da ontologia PT-500.
- Biblioteca de tokenização de texto.
- Dispositivo local com capacidade de CPU/GPU suficiente para inferência em lotes (exige ~1.5 GB VRAM).

## Processo (passo a passo executável)
1. **Fatiamento Dinâmico em Janelas (Sliding Window):**
   - Receber o texto completo do capítulo.
   - Segmentar o texto em janelas deslizantes de tamanho estipulado em `WINDOW_TOKEN_SIZE` (padrão: `512` tokens) aplicando uma passada de deslocamento (stride) de `128` tokens para evitar a perda de tropos nas bordas dos blocos.
2. **Inferência Multi-Label Local:**
   - Para cada janela gerada na etapa 1, codificar os tokens e passar pelo classificador BERTimbau local.
   - O modelo emite um vetor de ativação sigmoide contendo probabilidades na faixa de $[0.0, 1.0]$ para cada um dos 500 tropos da PT-500.
3. **Agregação por Max-Pooling:**
   - Reunir os vetores de probabilidade de todas as janelas do capítulo.
   - Para cada uma das 500 categorias de tropos, selecionar o valor máximo obtido entre todas as janelas (Max-Pooling). Isso consolida a presença do tropo no capítulo como um todo.
4. **Filtragem de Candidatos:**
   - Descartar todos os tropos cujo score consolidado seja inferior a `0.30` (`TROPE_DETECTION_THRESHOLD = 0.30`).
   - Salvar a lista de tropos sobreviventes como "Candidatos Verificados de Nível 1" e passar para a etapa seguinte de validação global por LLM.

## Parâmetros e configuração
- `WINDOW_TOKEN_SIZE`: Tamanho do bloco de tokens para análise das janelas deslizantes. Padrão: `512`.
- `WINDOW_STRIDE_SIZE`: Deslocamento da janela deslizante na varredura. Padrão: `128`.
- `TROPE_DETECTION_THRESHOLD`: Limiar de probabilidade sigmoide mínimo para classificar o tropo como candidato. Padrão: `0.30`.

## Armadilhas e como evitá-las
- **Armadilha:** Desbalanceamento de Classes Raras: durante a fase de treinamento, a grande maioria dos tropos (como *Evil Twin* ou *Inception-style Dream*) apresenta pouquíssimos exemplos positivos na base literária, fazendo com que o classificador convencional convirja para responder sempre 0 (AUSENTE) nessas categorias para otimizar a perda.
  **Mitigação:** Durante a etapa de fine-tuning do modelo do pipeline, utilizar obrigatoriamente a função de perda Weighted Binary Cross Entropy (Weighted BCE) na camada final, atribuindo pesos inversamente proporcionais às frequências das classes no dataset literário. Isso equilibra a sensibilidade do classificador para tropos raros (Rodriguez Vidal et al., 2023).

## Critérios de validação (Definition of Done)
- [ ] O classificador de tropos atinge um Macro-F1 score mínimo de 0.51 no dataset de testes literários em português.
- [ ] A inferência do capítulo completo é concluída em tempo inferior a 1,5 segundo em ambiente de hardware padrão.

## Fundamentação científica
- Rodriguez Vidal, M. et al. (2023) - TropesInWild: A Dataset of Narrative Tropes in Novels - arXiv 2023
- García-Sánchez, M. et al. (2022) - AllTheRobotsEtAl: Tropes classification in Science Fiction - arXiv 2022
- García-Sánchez, M. et al. (2020) - Named Entity Recognition and Trope Classification in Literary Text - CLIN 2020

## Requisitos do projeto relacionados
- RF-172 (identificação de tropos)
- RF-173 (tropos recomendados)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: A classificação automática de tropos altamente sutis ou abstratos (ex: *Self-Fulfilling Prophecy*) apresenta taxas de falsos positivos moderadas na triagem primária.*
*Fallback para v1:* Implementar um mapeador lexical heurístico baseado em expressões regulares e glossário de termos chave na wiki do autor para marcar tropos óbvios, e desativar o modelo BERTimbau local se a inferência sofrer de alta latência em CPUs de baixo desempenho.

## Exemplos
**Entrada:**
```text
A anciã apontou o dedo trêmulo para Kael: 'Tu és o escolhido pela profecia da lua vermelha para carregar a espada sagrada e libertar o reino.'
```
**Saída esperada (Candidatos extraídos):**
```json
[
  {"trope": "Chosen One", "confidence": 0.88},
  {"trope": "Ancient Prophecy", "confidence": 0.91}
]
```
**Caso de falha conhecido:**
Classificar a menção casual de um livro de profecia em uma prateleira como o tropo ativo "Ancient Prophecy" no capítulo.
