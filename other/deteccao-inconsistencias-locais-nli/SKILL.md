---
name: deteccao-inconsistencias-locais-nli
description: Detecta contradicoes logicas imediatas em paragrafos usando NLI local em tempo real enquanto o autor digita.
---
# deteccao-inconsistencias-locais-nli

## Descrição
A skill `deteccao-inconsistencias-locais-nli` detecta contradições lógicas imediatas e de negação no micro-contexto (sentença recém-digitada vs. parágrafo anterior) de forma extremamente rápida. Ela utiliza modelos compactos de Reconhecimento de Implicação Textual (NLI - Natural Language Inference) executados localmente para fornecer feedback visual instantâneo no editor enquanto o escritor está digitando.

## Quando usar
Gatilhos concretos e observáveis:
- O escritor conclui a redação de um parágrafo no editor de texto (gatilho disparado por tecla `Enter` ou `Space` após ponto final).
- Ocorre uma pausa na digitação ativa superior a 3 segundos (deteção de idle de teclado).
- O autor solicita explicitamente a checagem rápida do último bloco de texto digitado no painel do editor.

Quando NÃO usar:
- Para auditar a consistência lógica de eventos ao longo de múltiplos capítulos distantes (o processamento de NLI local deve ser restrito à janela imediata de contexto para evitar estouro de memória e latência).
- Em textos contendo descrições abstratas poéticas ou metáforas que não sigam lógica factual/declarativa direta.

## Pré-requisitos
- Modelo NLI compacto local: `RoBERTa-large-MNLI` destilado (ex: `distilroberta-base-nli` rodando via ONNX/WebAssembly ou CPU local).
- Limiar de tokenização: texto segmentado em sentenças limpas.
- Dados de entrada: a frase em digitação (Hipótese) e as últimas 500 a 1000 palavras anteriores (Premissa).

## Processo (passo a passo executável)
1. **Extração de Contexto (Premissa):** Capturar as últimas 500 a 1000 palavras (janela deslizante) anteriores à posição atual do cursor de digitação no editor. Rótulo: `Premissa`.
2. **Extração da Frase Ativa (Hipótese):** Capturar a frase ativa em digitação ou o parágrafo recém-concluído. Rótulo: `Hipótese`.
3. **Inferência NLI Local:**
   - Alimentar o par `(Premissa, Hipótese)` no modelo NLI local.
   - Extrair a distribuição de probabilidades softmax para as três classes lógicas: `entailment` (acarreta), `neutral` (neutro), e `contradiction` (contradiz).
4. **Validação de Negação Secundária:**
   - Se a classe `contradiction` apresentar score superior a 80% (`CONTRADICTION_THRESHOLD = 0.80`), acionar uma checagem local baseada em regras regex de antônimos e modificadores de negação (ex: verificar presença de palavras como "não", "nunca", "jamais" combinadas a verbos idênticos presentes na premissa).
5. **Gatilho de Sinalização:**
   - Se o score de contradição for mantido/confirmado pelo filtro secundário, marcar a linha correspondente no editor com um sublinhado ondulado vermelho.
   - Apresentar um balão suspenso explicativo com a premissa anterior conflitante e o score da probabilidade NLI.

## Parâmetros e configuração
- `CONTRADICTION_THRESHOLD`: Limiar mínimo da probabilidade NLI de contradição para acionar alertas. Padrão: `0.80`.
- `MAX_CONTEXT_WORDS`: Janela de contexto anterior para atuar como premissa. Padrão: `800` palavras.
- `DEBOUNCE_DELAY_MS`: Tempo de espera após parar a digitação para disparar a inferência de forma transparente. Padrão: `3000` (3 segundos).

## Armadilhas e como evitá-las
- **Armadilha:** Saturação de Atenção Global e Latência: tentar processar o livro completo em modelos locais de NLI causa estouro de memória RAM/VRAM e latências superiores a 10 segundos, quebrando a digitação em tempo real.
  **Mitigação:** Restringir estritamente a janela de premissa a no máximo `1000` palavras. Se uma busca global for necessária, delegar a auditoria em lote assíncrona ao fechamento de arquivos.

## Critérios de validação (Definition of Done)
- [ ] O modelo NLI local atinge acurácia e F1-score de pelo menos 82% em testes sintéticos de pares de frases contraditórias (ex: "Kael estava trancado na torre" vs. "Kael correu livremente pelo jardim").
- [ ] A latência de inferência combinada com a renderização visual do editor é inferior a 250ms em ambiente de CPU local.

## Fundamentação científica
- de Marneffe, M., Rafferty, A. & Manning, C. (2008) - Finding Contradictions in Text (taxonomia) - EMNLP 2008
- Anônimos (2025) - Straightforward Pipeline for Targeted Entailment and Contradiction Detection - arXiv 2025
- LiteReason (2025) - Lightweight Latent Reasoning for Narrative Tasks - arXiv 2025

## Requisitos do projeto relacionados
- RF-46 (reconhecer contradições)
- RF-73 (verificar antes de salvar)
- RF-75 (explicar contradição)

## Maturidade e riscos de adoção
**Nível:** Consolidada.
*A inferência discriminativa local de NLI em pares curtos de texto é previsível, com arquiteturas leves bem testadas em CPUs via ONNX Runtime.*

## Exemplos
**Entrada:**
```json
{
  "premissa": "A espada de Kael estava guardada no fundo do baú de ferro no sótão da estalagem.",
  "hipotese": "Kael desembainhou sua espada brilhante e golpeou o guarda na taverna."
}
```
**Saída esperada:**
```json
{
  "is_contradiction": true,
  "confidence": 0.89,
  "explanation": "Conflito físico detectado: A espada está guardada no baú no sótão, mas o personagem a utilizou imediatamente na taverna."
}
```
**Caso de falha conhecido:**
Marcar a frase como contradição se um personagem disser em diálogo "eu não tenho espada", interpretando como mentira lógica na premissa, quando é apenas uma fala do enredo.
