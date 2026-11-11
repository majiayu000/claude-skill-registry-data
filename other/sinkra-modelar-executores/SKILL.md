---
name: sinkra-modelar-executores
description: "Modelar e supervisionar quem deve executar, revisar e responder por cada task de um processo: separar Humano, Worker e Agente, decompor trabalho misto, especificar contratos, desenhar handoffs, ondas paralelas, subagentes e gates sem criar personas soltas. Usar quando um processo validado precisar virar operação, automação, Worker, Agente, squad ou execução multiprocessos."
---

# Sínkra — Modelar Executores

Escolher executor depois de conhecer entidade, stage, task, input e output.

## Carregar

- [runtime-and-persistence.md](../_shared/references/runtime-and-persistence.md)
- [executor-model.md](../_shared/references/executor-model.md)
- [contracts.md](../_shared/references/contracts.md)
- [executor-registry.yaml](../_shared/templates/executor-registry.yaml)

## Orquestrar

1. [Classificar tasks](tasks/01-classificar-tasks.md)
2. [Contratar Workers](tasks/02-contratar-workers.md)
3. [Contratar Agentes e Humanos](tasks/03-contratar-agentes-e-humanos.md)
4. [Desenhar topologia e governança](tasks/04-desenhar-topologia.md)

Executar [executor-gate.md](checklists/executor-gate.md) antes de publicar o
registry.

## Regras

- Humano: intenção, assinatura, risco, exceção e responsabilidade.
- Worker: regra calculável, repetível, testável e escalável.
- Agente: interpretação contextual dentro de fontes, método e limites.
- Decompor task que exige naturezas incompatíveis.
- Separar executor, reviewer, accountable e dono do gate.
- Preencher a maior fronteira segura por especialização, hipóteses distintas,
  isolamento de contexto ou paralelismo real.
- Definir owner do fan-in e contrato comum de saída.
- Se o host oferecer sessões paralelas, manter o chat principal como supervisor,
  pedir uma aprovação por Wave, iniciar os executores prontos e acompanhar seus
  reports sem usar o humano como relay.

## Entregar

Registry de executores, assignments por task, contratos de Worker e Agente,
papéis humanos, handoffs, gates, gaps de capacidade e justificativas.
