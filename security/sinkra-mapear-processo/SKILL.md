---
name: sinkra-mapear-processo
description: "Reconstruir e validar como um processo realmente funciona antes de propor melhorias: inventariar materiais e narrativa, extrair entidades, lifecycles, stages, transições, tasks, relações, exceções, evidências, gaps e conflitos, e publicar uma versão AS-IS rastreável. Usar para mapear, documentar, auditar ou entender operações e para separar realidade atual de desenho TO-BE."
---

# Sínkra — Mapear Processo

Produzir verdade operacional versionada. Não embelezar o AS-IS.

## Carregar

- Ler
  [runtime-and-persistence.md](../_shared/references/runtime-and-persistence.md).
- Ler [sinkra-core.md](../_shared/references/sinkra-core.md).
- Ler
  [evidence-and-authority.md](../_shared/references/evidence-and-authority.md).
- Usar
  [process-map.yaml](../_shared/templates/process-map.yaml) como contrato de
  saída.

## Escolher modo

| Modo | Usar quando |
|---|---|
| material | existem documentos, telas, logs ou skills recuperáveis |
| narrativa | o processo está principalmente na cabeça das pessoas |
| híbrido | materiais possuem gaps, divergências ou prática informal |
| investigação | ninguém sabe onde está a verdade |

Preferir híbrido para processo crítico com evidência dispersa e conhecimento
tácito.

## Orquestrar

1. [Delimitar e detectar estado](tasks/01-delimitar-e-detectar.md)
2. [Capturar realidade](tasks/02-capturar-realidade.md)
3. [Extrair modelo candidato](tasks/03-extrair-modelo.md)
4. [Validar status por status](tasks/04-validar-modelo.md)
5. [Publicar versão AS-IS](tasks/05-publicar-as-is.md)

Executar [as-is-gate.md](checklists/as-is-gate.md) antes de publicar.

## Invariantes

- Preservar narrativa bruta e fonte.
- Não criar entidade sem identidade e lifecycle.
- Não criar task sem verbo, executor, input e output.
- Não misturar stage da entidade com status da task.
- Registrar atalho, espera, loop, retorno, falha e exceção.
- Manter melhorias em `to_be_candidates`, fora do mapa AS-IS.
- Chamar
  [sinkra-elicitar-construcao](../sinkra-elicitar-construcao/SKILL.md) quando um
  conflito exigir decisão, sem alterar a história validada.

## Entregar

Mapa AS-IS, inventário de fontes, narrativa, evidência, gaps, conflitos,
exceções, responsável, data, versão e decisões necessárias.

Quando o pedido envolver nós, catálogo, Registry, deduplicação ou recombinação,
entregar o AS-IS validado para
[sinkra-extrair-nos](../sinkra-extrair-nos/SKILL.md). Não acionar essa composição
em mapeamentos comuns.
