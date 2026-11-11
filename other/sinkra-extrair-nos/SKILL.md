---
name: sinkra-extrair-nos
description: Extrair, revisar, promover, resolver e validar nós semânticos rastreáveis e recombináveis a partir de fontes ou modelos AS-IS. Usar quando o pedido envolver nós completos, granularidade, catálogo, Registry Sínkra, deduplicação, promoção seletiva, reutilização entre fluxos ou montagem de novas composições sem copiar o núcleo dos componentes.
---

# Sínkra — Extrair Nós

Transformar material contextual em componentes completos, versionados e recombináveis. Manter definição, composição, execução e evidência separadas.

## Carregar referências

Ler sempre:

- [contrato do grafo de nós](references/node-graph-contract.md);
- [núcleo do método Sínkra](../_shared/references/sinkra-core.md);
- [evidência e autoridade](../_shared/references/evidence-and-authority.md).

Ler [contratos operacionais](../_shared/references/contracts.md) ao trabalhar
com tasks, evidências ou promoção.

## Escolher o modo

| Pedido ou estado | Modo |
|---|---|
| Fonte bruta ainda não reconstruída | `candidate`, depois de `sinkra-mapear-processo` |
| Modelo AS-IS ou materiais já classificados | `candidate` |
| Candidatos existentes | `review` |
| Plano aprovado por humano | `promote` |
| Busca por ID, tipo, capacidade, alias ou texto | `resolve` |
| Integridade, hashes, versões ou referências | `validate` |

Usar `sinkra-work/node-graph/` no projeto atendido. Manter o Registry canônico
em `sinkra-work/registry/nodes/`. Não alterar a fonte.

## Candidate

1. Se a entrada for bruta, chamar `sinkra-mapear-processo` e aguardar um AS-IS rastreável.
2. Atravessar chunks e reunir o contrato semântico completo de cada candidato; não confundir chunk com nó.
3. Separar `definition`, `composition`, `runtime` e `evidence`.
4. Gerar IDs provisórios `CAND-<KIND>-<sequência>` e preservar locators de proveniência.
5. Gravar candidatos em `candidates/`, composições em `compositions/`, ocorrências em `runtime/` e relações em `relations.jsonl`.

Normalizar `cycle` como `lifecycle`, `full-cycle` ou `cycle-run`. Modelar verificação como capacidade de uma task. Classificar material como fonte, evidência, template, definição de artefato ou instância produzida.

## Review

1. Deduplicar por intenção e contrato, não apenas por nome.
2. Dividir mega-nós e unir fragmentos que não funcionam isoladamente.
3. Remover ordem, papel, condição contextual e parâmetros do núcleo; registrar isso no binding da composição.
4. Rejeitar mistura entre definição e runtime e registrar referências quebradas ou ausentes.
5. Gerar `promotion-plan.json` com `promote-new`, `promote-version`, `hold` ou `archive`.

Ideias, blockers e tasks vindos de WhatsApp ficam em `hold` por padrão. Não converter proposta em verdade observada.

## Promote

Promover somente itens nomeados em decisão humana aprovada. A identidade declarada serve para auditoria, não para autenticação criptográfica.

```text
<python> scripts/node_registry.py promote <promotion-plan.json> --registry <registry> --decision <decision.json> --by <humano> [--dry-run]
```

Exigir `--registry` e apontar para `sinkra-work/registry/nodes/`. Executar
`--dry-run` antes da escrita real.

Sem Python 3.11 ou superior, permitir apenas `candidate` e `review`. Bloquear
`promote` e `validate`, registrar a limitação e entregar um handoff executável
para uma máquina compatível.

Nunca promover implicitamente, apagar um objeto ou mover runtime histórico para o Registry de definições.

## Resolve

```text
<python> scripts/node_registry.py resolve --registry <registry> [--id <id-ou-ref> | --kind <kind> | --capability <capacidade> | --query <texto>]
```

Retornar referências exatas. Para ID sem versão, listar as versões disponíveis; nunca substituir silenciosamente uma versão fixada por `latest`.

## Validate

```text
<python> scripts/node_registry.py validate <bundle-ou-registry> [--registry <registry>]
```

Ao validar um bundle com referências canônicas, informar `--registry`; sem ele, a referência externa não pode ser comprovada e falha. Tratar como falha: contrato obrigatório ausente, referência quebrada, versão ausente, hash divergente, relação constitutiva faltante ou classe incompatível. Reportar órfãos e nós sem referência sem mudar seu estado.

## Cancelar sem destruir

- Cancelar composição: impedir novos runs, preservar versões e nós.
- Cancelar run: fechar tasks abertas como `cancelled` ou `not-applicable`, preservar evidências e manter a entidade no último stage válido.
- Tratar nó exclusivo de composição cancelada como `unreferenced` no relatório; não arquivar automaticamente.
- Exigir decisão separada para retirada, arquivamento ou nova versão.

## Encerrar

Entregar no máximo:

1. localização do bundle e modo executado;
2. contagem por classe, tipo e status;
3. falhas, duplicatas e itens em `hold`;
4. plano de promoção ou referências resolvidas;
5. próxima decisão humana, quando existir.
