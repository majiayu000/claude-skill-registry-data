---
name: harness-quadrant-process
description: >
  Executa um fluxo direto de 5 passos (escopo, inspeção, classificação,
  pontuação/notas, entrega) para avaliar o harness de desenvolvimento de um
  repositório e entregar um documento objetivo com diagrama de quadrante
  guias×sensores, notas de eficácia/complexidade e contexto de mercado.
  OpenSpec, OpenSPDD e `spdd/` são opcionais — só entram no modo aprofundado,
  nunca como pré-requisito do fluxo padrão.
license: MIT
metadata:
  author: local
  version: "2.0"
---

# Skill — Harness Quadrant Process

Use este skill quando o usuário quiser avaliar ou evoluir o harness de
desenvolvimento de um ou mais repositórios e receber, ao final, um documento
consistente e comparável entre execuções.

## Objetivo

Entregar, ao fim do fluxo, um arquivo em `Docs/` com:
- Notas do harness (eficácia e complexidade, com evidências e confiança)
- Contexto de mercado (quando houver fonte verificável)
- Diagrama Mermaid `quadrantChart` (guias × sensores)
- Tabela de rastreabilidade (ponto -> arquivo-fonte -> justificativa)
- Backlog priorizado de lacunas de maior risco

## Fluxo padrão (5 passos)

Este é o único fluxo necessário para uma análise comum. Não pule passos. Se
um passo tiver ambiguidade material, pare e pergunte ao usuário antes de
seguir.

1. **Escopo** — identifique o repositório-alvo e confirme o destino do
   documento (`Docs/` no repositório-alvo). Se `Docs/` não existir, crie o
   diretório antes de gravar, ou informe o bloqueio explicitamente — nunca
   redirecione a saída silenciosamente para outro diretório.
2. **Inspeção** — explore de forma orientada a conceito, não varra o
   repositório inteiro:
   - Guias inferenciais: `AGENTS.md`, `CLAUDE.md`, `copilot-instructions`, skills e prompts.
   - Guias computacionais: manifests, configs de lint/type/editor.
   - Sensores computacionais: pre-commit/hooks/CI/fitness functions/guardrails.
   - Sensores inferenciais: code-review humano/segundo agente/skills de revisão.
3. **Classificação** — aplique os critérios de posicionamento (ver "Critérios
   do quadrante") e registre cada ponto só se houver fonte real. Sem fonte
   verificável, exclua o ponto ou marque-o explicitamente como não
   verificado — nunca o apresente como fato.
4. **Pontuação e notas** — calcule a nota de eficácia e a nota de
   complexidade (ver "Rubrica de notas"), preencha o bloco de notas do
   harness e, se houver fonte verificável, a tabela de contexto de mercado;
   sem fonte, declare a ausência de verificação (ver "Notas e contexto de
   mercado").
5. **Entrega** — gere ou atualize o documento em `Docs/` usando
   `references/quadrant-doc-template.md`, validando:
   - Sintaxe Mermaid de um único bloco `quadrantChart` por documento
     (atualizações incrementais editam o bloco existente, nunca duplicam)
   - Rastreabilidade: todo ponto cita um arquivo-fonte real
   - Toda lacuna do backlog está ligada a uma ação concreta

**Modo aprofundado (exceção opcional)**: se o usuário pedir governança
formal, recorrência entre múltiplos repositórios ou múltiplos revisores,
ofereça registrar o resultado também como change OpenSpec e/ou análise
SPDD (`spdd/analysis/`, `spdd/prompt/`). Isso nunca é obrigatório para uma
análise comum e nunca bloqueia o passo 1.

## Critérios do quadrante

- Eixo X: `Computacional --> Inferencial`
- Eixo Y: `Sensor feedback --> Guia feedforward`
- Quadrantes:
  - `quadrant-1 Guia Inferencial`
  - `quadrant-2 Guia Computacional`
  - `quadrant-3 Sensor Computacional`
  - `quadrant-4 Sensor Inferencial`

Regra de decisão (aplique nesta ordem):
1. **Computacional vs. Inferencial**: computacional = uma ferramenta avalia
   ou impõe o comportamento automaticamente, sem leitura humana (ex.:
   `SwiftLint`, CI, hooks); inferencial = depende de interpretação humana ou
   de um agente lendo texto (ex.: `AGENTS.md`, revisão humana).
2. **Guia vs. Sensor**: guia orienta antes ou durante a ação (feedforward,
   ex.: `AGENTS.md`, `harness.config.json`); sensor observa ou reprova depois
   da ação já realizada (feedback, ex.: CI, revisão de MR).

Exemplo por quadrante:
- Guia Inferencial: `AGENTS.md` — orienta o agente antes de agir, por leitura.
- Guia Computacional: `harness.config.json` — configura allowlist/guardrails de forma mecânica.
- Sensor Computacional: pipeline de CI — reprova automaticamente após o commit.
- Sensor Inferencial: revisão humana de MR — julgamento semântico após a ação.

As coordenadas `[x, y]` são qualitativas para priorização visual, mas cada
uma SHALL vir acompanhada de uma justificativa textual e do arquivo-fonte na
tabela de rastreabilidade — documente isso na seção de metodologia do
artefato final.

## Rubrica de notas

O documento final SHALL apresentar duas notas independentes, cada uma de
0 a 10:

**Nota de eficácia** — média das dimensões conhecidas (0–5 cada) x 2:
1. Clareza das guias
2. Automação
3. Cobertura de feedback
4. Rastreabilidade/evolução
5. Adoção/baixo atrito

Cada dimensão SHALL ter pontuação, arquivo-fonte de evidência e
justificativa. Se uma dimensão não puder ser avaliada com as fontes
disponíveis, marque-a como **desconhecida** e exclua-a do cálculo da média
(a média usa só as dimensões conhecidas) — nunca zere a dimensão nem eleve a
confiança declarada da nota.

**Nota de complexidade/tamanho** — independente da eficácia, usando a
evidência dos artefatos e gates identificados na classificação:
- 0–2 minimalista
- 3–4 leve
- 5–6 médio
- 7–8 pesado
- 9–10 extremo

## Notas e contexto de mercado

O documento final SHALL incluir um bloco de notas do harness com: data da
avaliação, escopo, nota de eficácia (com as 5 dimensões), nota de
complexidade, confiança, limitações e próximos passos.

O documento final SHALL incluir também uma tabela de contexto de mercado
(fonte, data/versão, prática observada, evidência, aplicabilidade, aderência
ao repositório) apenas quando houver fonte externa verificável fornecida
pelo usuário ou identificada no repositório. Sem fonte, declare
explicitamente que o contexto de mercado não foi verificado nesta avaliação
— nunca omita a seção nem apresente a nota interna como equivalente a uma
média estatística do mercado.

## Regras de qualidade

1. **Objetividade**: escrever curto, direto e orientado a ação.
2. **Rastreabilidade total**: nada no quadrante ou na rubrica pode ser
   "achismo" sem arquivo-fonte.
3. **Priorização prática**: lacunas ordenadas por risco, com próximo passo claro.
4. **Sem implementação prematura**: só gere/edite o documento em `Docs/` no
   passo 5, depois de escopo, inspeção, classificação e pontuação concluídos.
5. **Consistência cross-repo**: manter o mesmo formato de saída em qualquer projeto.
6. **Fluxo mais direto que sustente a rastreabilidade exigida**: use o modo
   padrão sempre que ele já atenda ao pedido; escale para o modo aprofundado
   só quando o próprio pedido do usuário exigir (ver "Modo aprofundado").

## Skill chaining recomendada

Nenhum destes é pré-requisito do fluxo padrão — use apenas quando o pedido
do usuário justificar:
- Para auditoria profunda do harness: usar `dev-harness-architect`.
- Para registrar o resultado como change formal (modo aprofundado): usar `openspec-propose`.
- Para converter regra recorrente em teste: usar `architecture-fitness-functions`.
- Para gate de fase em novos projetos: usar `install-dev-harness`.

## Definition of Done

Considere concluído apenas quando todos os itens abaixo forem verdadeiros:
1. Quadrante rastreável — todo ponto tem arquivo-fonte, quadrante e justificativa.
2. Notas calculadas — nota de eficácia e nota de complexidade preenchidas,
   com dimensões desconhecidas marcadas (não zeradas).
3. Contexto de mercado declarado — tabela preenchida com fonte real, ou
   declaração explícita de "não verificado".
4. Documento final em `Docs/` criado ou atualizado com um único `quadrantChart`.
5. Tabela de rastreabilidade e backlog de lacunas priorizado presentes.
6. Resumo final com próximos passos de melhoria do harness.
