---
name: sinkra-arquitetar-sistema
description: "Arquitetar projetos, processos e sistemas completos no método Sínkra: reconstruir AS-IS, modelar entidades, lifecycles, stages, transições e relações, resolver decisões, desenhar TO-BE, contratar Humanos, Workers e Agentes, forjar skills orquestradoras e publicar um sistema auditável. Usar quando o pedido envolver desenho operacional, arquitetura de processos, automação ou estrutura de agentes conectada ao sistema Sínkra."
---

# Sínkra — Arquitetar Sistema

Atuar como orquestradora de topo. Partir da entidade e da transição; usar
Agentes, Workers e Humanos somente como executores contratados pelas tasks.

## Carregar

Ler no início:

- [runtime-and-persistence.md](../_shared/references/runtime-and-persistence.md);
- [sinkra-core.md](../_shared/references/sinkra-core.md);
- [orchestration-model.md](../_shared/references/orchestration-model.md);
- [source-boundaries.md](../_shared/references/source-boundaries.md).

Carregar os contratos e templates compartilhados somente quando a task pedir.

## Inicializar

Resolver o estado existente em `sinkra-work/`. Se ainda não existir, copiar o
template em `skills/_shared/templates/sinkra-work/` para o projeto atendido.

Preservar versões anteriores. Não recomeçar um sistema já mapeado sem registrar
por que a versão foi substituída.

## Escolher profundidade

| Escopo pedido | Rota |
|---|---|
| somente AS-IS | tasks 1–2, gate e handoff |
| arquitetura sem implementação | tasks 1–5, gate e handoff |
| sistema completo | tasks 1–7 |

Não forjar skills ou executores quando o pedido termina no diagnóstico ou no
desenho. Registrar as etapas posteriores como não aplicáveis ou futuras.

## Orquestrar

1. [Inicializar sistema](tasks/01-inicializar-sistema.md)
2. [Reconstruir AS-IS](tasks/02-reconstruir-as-is.md)
3. [Resolver decisões e gaps](tasks/03-resolver-decisoes.md)
4. [Desenhar TO-BE](tasks/04-desenhar-to-be.md)
5. [Modelar executores](tasks/05-modelar-executores.md)
6. [Forjar skills de transição](tasks/06-forjar-transicoes.md)
7. [Auditar e publicar](tasks/07-auditar-e-publicar.md)

Executar [architecture-gate.md](checklists/architecture-gate.md) antes da task 6
e [release-gate.md](checklists/release-gate.md) antes de publicar.

## Compor skills

Carregar a skill irmã indicada e devolver seu output a esta orquestradora:

- AS-IS:
  [sinkra-mapear-processo](../sinkra-mapear-processo/SKILL.md);
- decisões:
  [sinkra-elicitar-construcao](../sinkra-elicitar-construcao/SKILL.md);
- executores:
  [sinkra-modelar-executores](../sinkra-modelar-executores/SKILL.md);
- transições:
  [sinkra-forjar-skill](../sinkra-forjar-skill/SKILL.md);
- integridade:
  [sinkra-auditar-sistema](../sinkra-auditar-sistema/SKILL.md).

Se o host não suportar invocação aninhada, ler e executar o `SKILL.md` irmão
diretamente. Não copiar seu conteúdo para esta skill.

## Restringir

- Não desenhar TO-BE antes do gate AS-IS.
- Não criar Agente a partir de dor, desejo ou persona.
- Não tratar documento oficial como prática observada sem validação.
- Não confundir nível, stage e status de task.
- Não automatizar Herança ou Spawn sem contrato de origem, atualização,
  idempotência e rollback.
- Não compor full cycle com transições ainda não testadas.

## Entregar

Publicar um bundle autocontido com versão AS-IS, decisões, arquitetura TO-BE,
registry de executores, skills de transição, gates, persistência, auditoria,
blockers e ordem de implantação.
