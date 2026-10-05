---
name: skmtc-graphql
version: 0.1.1
description: |
  The GraphQL pipeline for SKMTC generators — authoring generators
  whose input schema is GraphQL SDL rather than OpenAPI. Covers
  `toGqlOperationEntry`, `GqlOperation`, `synthesizeArgsObject`
  (mutation args -> object schema), the GQL enrichment routing
  (`[id][rootKind][fieldName][variant]` — two nested subject keys
  where OAS has path+method), the
  `to<Lang>GqlOperationProjectionBase` companion factories,
  and the `GeneratorKey` shape `id|rootKind|fieldName|variant`.

  Use this skill ALONGSIDE `skmtc-generator` whenever the schema
  source is GraphQL SDL or the task mentions "GraphQL", "SDL",
  "GqlOperation", "toGqlOperationEntry", or GraphQL query/mutation
  generators. Engine rules (producers, register/insert, the axioms)
  stay in `skmtc-generator`; this skill carries only what differs
  for GraphQL.
metadata:
  internal: true
---

# SKMTC GraphQL pipeline

Everything in the `skmtc-generator` skill applies unchanged — same
axioms, same producers, same register/insert machinery, same
`ContentSettings`. GraphQL differs in exactly four places: the entry
factory, the operation object, enrichment resolution, and how
mutation arguments become a schema. This skill is those differences.

## 1. The entry factory

### Scaffold C variant: GraphQL entry (`toGqlOperationEntry`)

```ts fragment
import { toGqlOperationEntry, synthesizeArgsObject } from '@skmtc/core'

export const MyGqlEntry = toGqlOperationEntry<EnrichmentSchema>({
  id: denoJson.name,

  // ⬇ Mutations only, gated on a synthesizable args object.
  isSupported({ operation }) {
    return operation.rootKind === 'mutation' &&
      synthesizeArgsObject(operation) !== undefined
  },

  transform({ context, operation, variant }) {
    if (operation.rootKind !== 'mutation') return
    context.insertOperation({ projection: MyGen, operation, variant })
  },

  toEnrichmentSchema
})
```

GQL-specific notes:

1. **Enrichments arrive parsed on `settings.enrichments`**, exactly
   as for OAS operations and models — read them there; never index
   the raw umbrella by hand. The subject keys are
   `[id][rootKind][fieldName][variant]`.
2. **Mutation args come via `synthesizeArgsObject(operation)`** — GQL
   has no `requestBody`; this turns the field's arguments into an
   object schema for `insertNormalizedModel`.

Background: [`concepts/the-graphql-pipeline.md`](../../concepts/the-graphql-pipeline.md).


## 2. The four GraphQL differences

1. **Entries come from `toGqlOperationEntry`**; `transform` receives
   `operation: GqlOperation` (fields: `rootKind` —
   `'query' | 'mutation'` — and `fieldName`; `operation.identifier`
   is `<rootKind>_<fieldName>`). The companion projection-base
   factory is the lang package's
   `to<Lang>GqlOperationProjectionBase`.
2. **Enrichments arrive parsed on `settings.enrichments`, same as
   OAS** — the base's `static toEnrichments` parses the umbrella with
   `subjectSegments: [operation.rootKind, operation.fieldName,
   variant]` (`toGqlOperationProjectionBase.ts`). Only the subject
   keys differ: two nested segments (`rootKind`, `fieldName`) where
   OAS has path+method. `operation.identifier`
   (`<rootKind>_<fieldName>`) is a file-naming/cache key, never an
   enrichment key.
3. **Mutation args come via `synthesizeArgsObject(operation)`** — GQL
   has no `requestBody`; this turns the field's arguments into an
   object schema suitable for `insertNormalizedModel`.
4. **Routing keys**: enrichment routing is
   `enrichments.<id>.<rootKind>.<fieldName>.<variant>`; the
   `GeneratorKey` is `id|rootKind|fieldName|variant`. Compose with
   `this.insertOperation(Peer, op, { variant?, options })` exactly as
   for OAS — `options` only when the peer declares them.

## 3. Boundary with other skills

- **skmtc-generator** — everything engine-side; load it first.
- **skmtc-lang-typescript / skmtc-lang-kotlin** — the target-language
  layer, exactly as for OAS generators.
- Deep dive: `concepts/the-graphql-pipeline.md`; the
  operation-reference protocol's GraphQL example is in
  `concepts/cross-generator-coordination.md`.
