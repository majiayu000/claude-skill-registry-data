---
name: sinkra-forjar-skill
description: "Converter uma transição de processo validada em skill orquestradora portátil: priorizar reuso, depois adaptação e somente então criação, decompor tasks, calibrar liberdade, definir rotas, checklists, gates, persistência, handoffs e testes, e gerar um pacote SKILL.md compatível com CLIs baseados em Agent Skills. Usar quando entidade, stage de origem, stage de destino e contrato da transição já estiverem aprovados."
---

# Sínkra — Forjar Skill

Transformar uma transição validada em capacidade executável. Não usar esta
skill para descobrir o processo que ainda não foi mapeado.

## Carregar

- [runtime-and-persistence.md](../_shared/references/runtime-and-persistence.md)
- [sinkra-core.md](../_shared/references/sinkra-core.md)
- [orchestration-model.md](../_shared/references/orchestration-model.md)
- [contracts.md](../_shared/references/contracts.md)
- [skill-blueprint.yaml](../_shared/templates/skill-blueprint.yaml)

## Orquestrar

1. [Validar transição](tasks/01-validar-transicao.md)
2. [Aplicar reuse, adapt, create](tasks/02-reusar-adaptar-criar.md)
3. [Desenhar orquestração](tasks/03-desenhar-orquestracao.md)
4. [Autorizar artefatos](tasks/04-autorizar-artefatos.md)
5. [Validar e forward-testar](tasks/05-validar-e-testar.md)
6. [Registrar e entregar](tasks/06-registrar-e-entregar.md)

Executar [forge-gate.md](checklists/forge-gate.md) antes de promover a skill.

## Estrutura

```text
<skill-name>/
├─ SKILL.md
├─ tasks/
├─ checklists/
├─ references/
├─ scripts/       somente quando determinismo exigir
└─ agents/        metadados opcionais do host
```

Manter `SKILL.md` como orquestrador conciso. Colocar how-to atômico em `tasks/`
e conhecimento detalhado em `references/`.

## Regras

- Aplicar `reuse > adapt > create` e registrar a justificativa.
- Uma skill move uma entidade por uma transição delimitada.
- Registrar tasks não aplicáveis; não omitir silenciosamente.
- Colocar lógica calculável em Worker/script.
- Usar somente `name` e `description` no frontmatter comum.
- Evitar ferramenta, sintaxe de invocação ou path específico de um CLI no
  núcleo.
- Não criar full cycle antes de forward-testar as transições.

## Entregar

Pasta da skill, blueprint preenchido, resultado de validação, casos testados,
limitações, versão e handoff para o registry de capacidades.
