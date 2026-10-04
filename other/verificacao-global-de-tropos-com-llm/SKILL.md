---
name: verificacao-global-de-tropos-com-llm
description: Valida candidatos a tropos usando LLM local com contexto global do enredo, distinguindo ocorrencias canonicas de subversoes criativas.
---
# verificacao-global-de-tropos-com-llm

## Descrição
A skill `verificacao-global-de-tropos-com-llm` realiza a validação de nível 2 de tropos narrativos pré-classificados. Ela submete as sugestões de tropos (candidatos) a um modelo de linguagem (LLM) local auxiliado por um prompt estruturado contendo a sinopse do enredo global. Isso permite diferenciar o tropo factual de clichês incidentais, além de catalogar subversões criativas (variantes lógicas do tropo).

## Quando usar
Gatilhos concretos e observáveis:
- O classificador de nível 1 (skill `classificacao-local-de-tropos`) gera a lista de candidatos a tropos e salva no banco de dados.
- O escritor solicita a checagem manual de "consistência e originalidade do enredo" na aba do romance.
- Ocorre a geração automática de relatórios de análise de clichês no encerramento da escrita de um capítulo.

Quando NÃO usar:
- Na triagem bruta inicial de texto (deve rodar obrigatoriamente após a filtragem rápida do classificador local).
- Em tempo de digitação instantâneo tecla-a-tecla (rodar em background ou sob demanda).

## Pré-requisitos
- Lista de tropos candidatos gerada no nível 1 com seus respectivos scores de confiança.
- Resumo global do romance compilado (saída $R_{L3}$ da skill `sumarizacao-hierarquica-recursiva`).
- Modelo de linguagem local instrutivo e leve (ex: Phi-3.5-mini-instruct) rodando localmente.

## Processo (passo a passo executável)
1. **Compilação de Prompt Contextual:**
   - Para cada tropo candidato retido (ex: *Mentor Death*):
     - Buscar no dicionário PT-500 a definição canônica e exemplos literários do tropo.
     - Extrair o snippet do capítulo onde o tropo foi pré-classificado.
     - Recuperar a sinopse do romance até o capítulo atual ($R_{L3}$).
     - Montar o prompt de inferência combinando essas quatro informações.
2. **Inferência por Classificação Ternária:**
   - Chamar o LLM local com o prompt montado.
   - Instruir o modelo a classificar a ocorrência em uma das três classes estritas:
     - `PRESENTE`: O tropo ocorre exatamente de forma canônica (clichê tradicional).
     - `AUSENTE`: Falso positivo (a frase cita elementos parecidos, mas a ação dramática não corresponde ao tropo).
     - `VARIANTE`: O autor introduziu o tropo de forma subvertida, irônica ou descontruída (ex: o mestre morre mas reencarna no parágrafo seguinte).
3. **Mapeamento de Subversões Criativas:**
   - Salvar o resultado no banco.
   - Se rotulado como `VARIANTE`, marcar o trecho na interface gráfica do escritor como uma "Subversão Criativa / Originalidade", fornecendo um feedback motivador e registrando na linha do tempo.
   - Se `PRESENTE`, catalogar a métrica na aba de densidade de clichês de gênero.

## Parâmetros e configuração
- `LLM_VALIDATION_TEMPERATURE`: Temperatura de geração do modelo de validação. Padrão: `0.00` (forçar comportamento determinístico).
- `MAX_CONTEXT_SYNOPSIS_WORDS`: Tamanho máximo em palavras da sinopse global incluída no prompt. Padrão: `400`.
- `TARGET_VALIDATION_LLM`: Identificador do modelo local. Padrão: `Phi-3.5-mini-instruct-Q4`.

## Armadilhas e como evitá-las
- **Armadilha:** Análise Sem Contexto de Enredo: classificar tropos profundos (ex: *Mentor Death*) alimentando o LLM apenas com a frase literal isolada da cena (ex: "Valdris deitou-se na cama e fechou os olhos para sempre"). Sem saber pela sinopse global que Valdris era o mestre e guia do protagonista Kael, a IA falhará sistematicamente na identificação, marcando-a como `AUSENTE` (TropeEval, 2025).
  **Mitigação:** Injetar obrigatoriamente a sinopse atualizada do enredo do livro no prompt de contexto da inferência. O modelo deve receber a árvore relacional de quem é quem (papel dos personagens no GTE) antes de validar a cena.

## Critérios de validação (Definition of Done)
- [ ] O pipeline híbrido (Nível 1 + Nível 2 LLM) atinge F1-score macro mínimo de 0.61 na ontologia de tropos, e F1-score de pelo menos 0.74 em tropos de alta frequência.
- [ ] O LLM local descarta falsos positivos causados por metáforas casuais em 100% dos testes unitários da suíte de regressão.

## Fundamentação científica
- TropeEval (2025) - Evaluating Trope Understanding in Large Language Models - arXiv 2025
- Surprising Turns (2025) - Detecting Narrative Subversion and Creative Tropes in Literature - arXiv 2025
- FlawedFictions (Ahuja, K. et al., 2025) - Finding Flawed Fictions: Plot Hole Detection - COLM 2025

## Requisitos do projeto relacionados
- RF-172 (identificação de tropos)
- RF-174 (brainstorm de arcos)

## Maturidade e riscos de adoção
**Nível:** Emergente.
*Risco: Pequenos LLMs locais podem demorar até 2 segundos por tropo validado e apresentar variações nas respostas devido a prompts instáveis.*
*Fallback para v1:* Validar tropos mais comuns (como mortes, traições ou casamentos) aplicando buscas diretas em banco relacional no estado do GTE (ex: checar se o mentor de Kael foi marcado como "Morto" no banco), dispensando a inferência de LLM na v1.

## Exemplos
**Entrada (Prompt compilado):**
- Tropo: *Mentor Death* (Mentor morre deixando o herói desamparado).
- Contexto global: "Valdris é o mestre ferreiro que treinou Kael".
- Snippet: "Kael chorou sobre o corpo inerte de Valdris no laboratório".
**Saída esperada (Classificação):**
```json
{
  "status": "PRESENTE",
  "trope": "Mentor Death",
  "confidence": 0.94,
  "justification": "O personagem Valdris, mestre do herói, faleceu na cena de acordo com o snippet."
}
```
**Caso de falha conhecido:**
Classificar a frase "Kael comprou um mentor de madeira para treinar esgrima" como o tropo ativo "Mentor Death" devido à palavra "mentor".
