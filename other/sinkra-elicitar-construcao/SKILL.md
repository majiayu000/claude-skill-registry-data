---
name: sinkra-elicitar-construcao
description: "Conduzir decisões e construções complexas com controle epistemológico: resolver contexto, reaproveitar decisões existentes, separar gaps reais, descobrir se o humano domina o tema, elicitar ou pesquisar, explicar uma decisão por turno, registrar e ratificar escolhas e transformá-las em contrato executável. Usar em desenvolvimento, processos, produtos, arquiteturas ou qualquer construção bloqueada por conhecimento, intenção ou trade-offs."
---

# Sínkra — Elicitar Construção

Governar a passagem de uma intenção ou problema para uma construção decidida,
contratada e persistida. Não tratar conversa fluida como estado do processo.

## Carregar

1. Ler
   [runtime-and-persistence.md](../_shared/references/runtime-and-persistence.md)
   para inicializar ou retomar o estado portátil.
2. Ler [mecanismo-do-video.md](references/mecanismo-do-video.md) no início.
3. Ler
   [evidence-and-authority.md](../_shared/references/evidence-and-authority.md)
   ao classificar domínio ou fontes.
4. Ler [contracts.md](../_shared/references/contracts.md) antes de registrar
   decisão, gate ou handoff.
5. Ler
   [orchestration-model.md](../_shared/references/orchestration-model.md) e
   [persistence-and-learning.md](../_shared/references/persistence-and-learning.md)
   antes de executar ou retomar uma construção.

## Inicializar

Reutilizar `sinkra-work/` no projeto atendido ou criá-lo a partir do
template em `skills/_shared/templates/sinkra-work/`. Não criar um segundo estado
paralelo.

Não substituir artefato existente sem ler seu estado, versão, decisões e
blockers.

## Escolher profundidade

| Pedido | Executar |
|---|---|
| decisão consultiva | tasks 1–5 e 8; devolver decisão sem construir |
| decisão + contrato | tasks 1–6 e 8; deixar execução contratada |
| implementação | tasks 1–8; task 7 somente após autorização |

Registrar tasks não aplicáveis. Não transformar uma pergunta consultiva em
projeto completo.

## Orquestrar

Executar as tasks em ordem:

1. [Resolver contexto](tasks/01-resolver-contexto.md)
2. [Classificar domínio](tasks/02-classificar-dominio.md)
3. [Elicitar ou pesquisar](tasks/03-elicitar-ou-pesquisar.md)
4. [Construir opções comparáveis](tasks/04-construir-opcoes.md)
5. [Validar compreensão e decidir](tasks/05-validar-compreensao-e-decidir.md)
6. [Contratar a construção](tasks/06-contratar-construcao.md)
7. [Executar e verificar](tasks/07-executar-e-verificar.md), somente no modo
   implementação e após o gate.
8. [Persistir e entregar](tasks/08-persistir-e-entregar.md)

Executar [preflight.md](checklists/preflight.md) após a task 1,
[decision-gate.md](checklists/decision-gate.md) após a task 5 e
[construction-gate.md](checklists/construction-gate.md) antes de encerrar.

## Triar antes de perguntar

- Capturar o resultado pretendido e qual execução precisa ser destravada.
- Aplicar `reuse > adapt > create` às decisões, regras e artefatos existentes.
- Classificar cada pendência como `resolvida`, `não bloqueante`, `pesquisa`,
  `decisão humana` ou `conflito`.
- Não reabrir decisão válida nem criar artefato por quota. “Sem novo ADR” não
  significa “sem governança”.
- Levar ao diálogo somente decisão humana irredutível ou conflito que pertença
  à autoridade presente.

A intenção em linguagem natural e a invocação explícita da skill ativam a mesma
cadeia. Conduzir a análise até o primeiro gate humano sem expor trabalho interno
desnecessário.

## Interagir

- Resolver o contexto elegível antes de pedir decisão; não devolver jargão para
  o humano decifrar.
- Mostrar uma decisão por turno, identificada como `D<n> de <total>`.
- Em cada turno apresentar: pergunta em linguagem comum, situação atual,
  exemplo prático, opções reais com consequências e recomendação justificada.
- Aceitar uma opção, combinação, alternativa nova ou adiamento. As opções
  propostas não formam menu fechado.
- Registrar a resposta antes de abrir a próxima decisão.
- Ao terminar o conjunto, resumir escolhas, mudanças, riscos e pendências e
  pedir `ratifico` ou `ajustar: ...`.
- Ajustar profundidade por novidade, centralidade, risco e domínio humano.
- Em modo de implementação, transformar definição ratificada em manifestação
  prática antes de pedir a próxima decisão que dependa dela.

## Rotear

- Se o humano dominar, elicitar regras, casos, restrições e critérios; não
  substituí-lo por pesquisa genérica.
- Se não dominar, pesquisar fontes adequadas e atuais antes de propor escolha.
- Se dominar parcialmente, dividir a decisão por dimensão e usar rota híbrida.
- Se uma resposta já estiver persistida, confirmar validade em vez de perguntar
  novamente.
- Se o usuário pediu somente decisão, parar após persistir a decisão e o
  handoff; não criar contrato de construção.
- Se pediu planejamento executável, parar após o contrato de construção.
- Se o usuário pediu execução, avançar somente após o gate de decisão.
- Se a execução possuir unidades independentes, propor uma Wave cobrindo toda a
  fronteira segura; não serializar trabalho apenas por conveniência.

## Bloquear

Bloquear quando entidade/objeto, decisão, autoridade, pesquisa obrigatória,
compreensão ou responsável pelo gate estiver ausente. Dizer exatamente:

- o que falta;
- por que impede o avanço;
- quem ou qual fonte pode resolver;
- qual task será retomada depois.

Não inventar opção para cumprir quantidade. Se não houver caminhos realmente
distintos, registrar o gap, pesquisar ou reformular a decisão.

## Encerrar

Entregar:

1. contexto e autoridade usados;
2. opções comparáveis apresentadas;
3. decisão e riscos aceitos;
4. ratificação do conjunto;
5. contrato da construção;
6. outputs e evidências, se houve execução;
7. próximo passo, owner e ponto de resume.
