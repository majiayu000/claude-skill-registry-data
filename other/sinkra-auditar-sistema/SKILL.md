---
name: sinkra-auditar-sistema
description: "Auditar um pack, processo ou sistema Sínkra sem alterá-lo por padrão: inventariar componentes, construir grafo de referências, verificar contratos, detectar órfãos, ciclos, drift, duplicação, conflitos, gaps de evidência e autoridade, priorizar impacto e produzir plano de remediação verificável. Usar antes de revisões, releases, remapeamentos ou otimizações e quando a doutrina parecer correta mas o sistema executável estiver inconsistente."
---

# Sínkra — Auditar Sistema

Inspecionar primeiro. Corrigir somente quando o usuário pedir implementação da
remediação.

## Carregar

- [runtime-and-persistence.md](../_shared/references/runtime-and-persistence.md)
- [sinkra-core.md](../_shared/references/sinkra-core.md)
- [contracts.md](../_shared/references/contracts.md)
- [source-boundaries.md](../_shared/references/source-boundaries.md)
- [audit-report.md](../_shared/templates/audit-report.md)

## Orquestrar

1. [Inventariar](tasks/01-inventariar.md)
2. [Construir grafo](tasks/02-construir-grafo.md)
3. [Verificar contratos e drift](tasks/03-verificar-contratos.md)
4. [Priorizar remediação](tasks/04-priorizar-remediacao.md)
5. [Publicar auditoria](tasks/05-publicar-auditoria.md)

Executar [audit-gate.md](checklists/audit-gate.md) antes de encerrar.

## Procurar

- referência quebrada ou fantasma;
- skill, task, gate ou executor órfão;
- ciclo sem condição de saída;
- nomes divergentes para o mesmo objeto;
- contratos duplicados com regras diferentes;
- stage confundido com status;
- output sem destino ou consumidor;
- gate sem owner ou executor que se autoaprova;
- decisão sem fonte ou inferência tratada como fato;
- estado que não permite resume;
- componentes não usados e full cycles prematuros.

## Priorizar

Ordenar por risco de perda, bloqueio de transição, corrupção de verdade,
segurança, alcance e custo de reparo. Não usar volume de arquivos como proxy de
qualidade.

## Entregar

Relatório com evidência e localização, severidade, impacto, remediação mínima,
dependências, decisões necessárias e ordem de reparo.
