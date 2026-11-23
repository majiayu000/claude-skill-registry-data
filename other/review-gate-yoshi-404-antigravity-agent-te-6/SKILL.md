---
name: review-gate
description: Protocolo de aprovação e rejeição usado por todos os supervisores.
---

# Skill: review-gate

Protocolo único de aprovação/rejeição usado por todos os supervisores.

## Princípios
- O revisor **não corrige** o artefato. Ele julga e devolve.
- O revisor lê apenas: briefing, critérios de aceite, artefato e handoff. **Não** lê o raciocínio interno do autor. Se o runtime não isola contextos, releia só esses arquivos antes de julgar.
- Critério é objetivo e vem do briefing. Gosto pessoal não rejeita; vira "ressalva".

## Passo a passo
1. Abra `work/_templates/review.md` e copie para `work/<ciclo>/reviews/<artefato>-r<N>.md`.
2. Percorra o checklist do seu papel (está no seu AGENT.md, seção "Definição de pronto").
3. Classifique cada achado: **bloqueante** (impede aprovar), **importante** (corrigir nesta rodada se barato) ou **menor** (vira ressalva).
4. Emita um veredito:
   - `APROVADO`: nenhum bloqueante.
   - `APROVADO COM RESSALVAS`: nenhum bloqueante; ressalvas vão para `work/<ciclo>/backlog.md`.
   - `REJEITADO`: ao menos um bloqueante.
5. Toda rejeição traz lista numerada com: **onde**, **qual o problema**, **por que importa**, **correção esperada**. Proibido "melhore isto" sem detalhar.

## Limites do loop
- Máximo de **2 rejeições** por artefato. Na 3ª, escale ao orquestrador, que decide: simplificar o escopo, trocar a abordagem ou perguntar ao humano.
- Na rodada N+1, só reavalie os pontos apontados em N e regressões. Não invente requisitos novos.

## Erros comuns
- Aprovar para "andar logo".
- Rejeitar por estilo.
- Reabrir ponto já aprovado.
- Pedir escopo novo disfarçado de correção.
