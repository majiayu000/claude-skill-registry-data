---
name: deteccao-entidades-literarias-portugues
description: Detecta entidades nomeadas (personagens, locais, organizacoes) em textos ficcionais em portugues usando modelos NER fine-tuned em literatura.
---
# deteccao-entidades-literarias-portugues

## Descrição
A skill `deteccao-entidades-literarias-portugues` realiza a extração local e otimizada de entidades literárias básicas (como pessoas, locais e organizações) a partir de textos ficcionais em língua portuguesa. Ela utiliza modelos leves baseados na arquitetura BERTimbau ajustados especificamente no domínio literário, permitindo alta eficiência de uso em CPU ou GPUs com recursos limitados de memória VRAM, servindo de base para a catalogação do universo da obra sem recorrer a APIs externas proprietárias.

## Quando usar
Gatilhos concretos e observáveis:
- O usuário importa um manuscrito inédito ou um arquivo (.txt, .docx, .md) contendo texto de romance/ficção.
- O editor de texto rico atualiza ou salva um capítulo recém-redigido ou modificado.
- O sistema dispara uma ação para sugerir automaticamente novos itens ou preencher fichas de personagens e locais a partir do texto escrito.

Quando NÃO usar:
- Quando o texto a ser analisado for puramente jornalístico, técnico, jurídico ou científico, pois o modelo é especializado na linguagem artística de romances e ficção.
- Durante a digitação em tempo real tecla-a-tecla (deve rodar apenas em pausas ou de forma debounced/assíncrona para não causar lag).

## Pré-requisitos
- Modelo base: `BERTimbau-large` (2.4 GB de memória física) ou modelo otimizado calibrado sobre o corpus PPORTAL_ner.
- Biblioteca de tokenização: Hugging Face `tokenizers` ou `transformers`.
- Recurso de GPU de época: pesos adicionais do modelo `MariNER` caso o romance seja detectado/configurado como romance histórico/de época (início do século XX).
- Dados de entrada: string contendo texto corrido em português.

## Processo (passo a passo executável)
1. **Verificação de Época:** Verificar nos metadados do livro se a obra é classificada como romance histórico ou de época. Caso afirmativo, configurar o pipeline para carregar o modelo secundário de correção de vocabulário arcaico `MariNER`. Caso contrário, manter o modelo padrão ajustado no corpus `PPORTAL_ner`.
2. **Segmentação e Tokenização:** Segmentar o texto de entrada em blocos sequenciais respeitando limites de sentenças, limitando cada bloco a um tamanho máximo de 512 tokens utilizando o tokenizador do BERTimbau.
3. **Inferência NER:** Passar os blocos tokenizados pelo modelo NER selecionado (BERTimbau + PPORTAL_ner ou MariNER) para prever as tags sob o esquema IOB2.
4. **Filtragem e Limiar de Confiança:** Para cada entidade identificada, extrair a probabilidade de classificação da camada softmax. Descartar qualquer entidade cuja probabilidade de classificação seja menor que 70% (threshold configurável `CONFIDENCE_THRESHOLD = 0.70`).
5. **Conversão e Agrupamento:** Reconstruir os tokens parciais (subwords) em palavras completas (de-tokenização) e agrupar as entidades contíguas do mesmo tipo (`PESSOA`, `LOCAL`, `ORGANIZACAO`) em registros consolidados contendo: termo original, tipo, posição inicial (char_start) e posição final (char_end).
6. **Retorno:** Retornar a lista estruturada de entidades em formato JSON.

## Parâmetros e configuração
- `CONFIDENCE_THRESHOLD`: Limiar mínimo de probabilidade para aceitar a detectação. Padrão: `0.70`.
- `MAX_BLOCK_TOKENS`: Tamanho máximo do bloco de tokens enviado ao BERTimbau. Padrão: `512`.
- `MODEL_PATH`: Caminho ou identificador do Hugging Face para os pesos ajustados do PPORTAL_ner. Padrão: `PPORTAL_ner_bertimbau`.
- `HISTORICAL_MODEL_PATH`: Caminho ou identificador dos pesos do MariNER. Padrão: `MariNER_historical_pt`.

## Armadilhas e como evitá-las
- **Armadilha:** Erro de Domínio Noticioso: usar modelos NER treinados apenas em jornalismo (como SpaCy padrão) faz o sistema ignorar apelidos e confundir nomes ficcionais com palavras normais.
  **Mitigação:** Bloquear o uso de modelos base genéricos do SpaCy ou NLTK na v1. Forçar o pipeline a usar estritamente os pesos ajustados no corpus `PPORTAL_ner` ou `MariNER`.

## Critérios de validação (Definition of Done)
- [ ] O modelo NER atinge um F1-Score mínimo de 85% na extração da categoria `PESSOA` sobre o dataset de testes literários em português.
- [ ] O processamento do texto é executado com tempo médio inferior a 200ms por página de 500 palavras em ambiente de CPU local padrão.
- [ ] Teste de regressão: Processar um parágrafo contendo apelidos literários complexos (ex: "O Lobo da Estrada", "Chico das Conchas") e verificar se a saída identifica-os corretamente como entidade do tipo `PESSOA`.

## Fundamentação científica
- Silva, M. & Moro, S. (2024) - PPORTAL_ner: corpus português 25 obras literárias, 5 categorias de entidades - LREC-COLING 2024
- Sarcinelli, A. et al. (2025) - MariNER: Historical Brazilian Portuguese NER - BRACIS 2025
- Silva, M. & Moro, S. (2024) - Evaluating Pre-training Strategies for Literary NER in Portuguese - PROPOR 2024

## Requisitos do projeto relacionados
- RF-18 (reconhecimento de entidades)
- RF-15 (suporte multilíngue no NER)
- RF-107 (identificação automática)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A técnica baseia-se em modelos de classificação discriminativos estáticos do tipo BERT, cuja inferência local e comportamento de definição de tokens são altamente previsíveis, eficientes e consolidados na literatura.*

## Exemplos
**Entrada:**
```json
{
  "text": "Dona Bento sorriu ao ver Chico das Conchas entrar na estalagem em Ouro Preto.",
  "is_historical": false
}
```
**Saída esperada:**
```json
[
  {
    "text": "Dona Bento",
    "category": "PESSOA",
    "confidence": 0.94,
    "char_start": 0,
    "char_end": 10
  },
  {
    "text": "Chico das Conchas",
    "category": "PESSOA",
    "confidence": 0.89,
    "char_start": 25,
    "char_end": 42
  },
  {
    "text": "Ouro Preto",
    "category": "LOCAL",
    "confidence": 0.97,
    "char_start": 62,
    "char_end": 72
  }
]
```
**Caso de falha conhecido:**
O modelo usar uma biblioteca jornalística genérica e retornar `Chico` como `PESSOA`, `das` como `O` e `Conchas` como `ORGANIZACAO`, ou simplesmente ignorar "Dona Bento".
```json
// FALHA A SER EVITADA
[
  {
    "text": "Chico",
    "category": "PESSOA"
  },
  {
    "text": "Conchas",
    "category": "ORGANIZACAO"
  }
]
```
