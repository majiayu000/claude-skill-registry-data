---
name: data-contract
description: "Genere ou valide un contrat de qualite data (Data Quality Contract) pour une source de donnees. Utiliser quand on ajoute une nouvelle source, modifie un schema, ou verifie la conformite des contrats existants."
user-invocable: true
context: fork
agent: Explore
allowed-tools: Read, Bash, Grep, Glob
---

# /data-contract — Gestion des Contrats Data

## Objectif
Creer ou valider un Data Quality Contract (DQC) pour une source de donnees, definissant les SLOs, le schema attendu, et les regles de validation.

## Arguments
- `$ARGUMENTS` : nom de la source (ex: "sirene", "rna", "bodacc") ou "validate" pour verifier tous les contrats

## Workflow — Mode creation

### Phase 1 — Analyse de la source
1. Identifier la source dans `src/config/sources.ts`
2. Lire le crawler/importeur correspondant
3. Analyser le schema des donnees ingerees (Prisma + Zod)
4. Determiner la licence et les obligations legales

### Phase 2 — Generation du contrat
Generer un fichier YAML au format ODCS v3 :

```yaml
# data-contracts/[source-name]-dqc-v1.0.yml
contract:
  name: "[source-name]-dqc"
  version: "1.0"
  description: "Data Quality Contract pour [source]"
  owner: "datalake-souverain"

source:
  name: "[source-name]"
  api_url: "[url]"
  license: "[etalab-2.0|ODbL-1.0]"
  attribution: "[organisation]"
  cadence: "[daily|weekly|monthly]"
  rate_limit: "[N/min]"
  personal_data: [true|false]

schema:
  type: "object"
  properties:
    siren: { type: "string", pattern: "^\\d{9}$" }
    # ... champs specifiques

quality:
  tier: "[Gold|Silver|Bronze]"
  slos:
    validity: { min: 99.5 }
    completeness: { min: 97, critical_fields: ["siren", "legalName"] }
    uniqueness: { min: 99.5, key: "siren" }
    freshness: { max_age_days: 7 }
    traceability: { min: 100 }

validation:
  zod_schema: "src/core/entities/[schema].ts"
  test_file: "tests/dqc/[source-name].test.ts"
```

### Phase 3 — Validation
- Verifier que le schema Zod couvre tous les champs du contrat
- Verifier que le crawler respecte le rate limit declare
- Verifier que les SLOs sont coherents avec le tier

## Workflow — Mode validation

1. Lister tous les contrats dans `src/config/data-contracts/`
2. Pour chaque contrat :
   - Verifier que le crawler existe et est actif
   - Verifier la coherence schema Prisma ↔ Zod ↔ contrat
   - Signaler les contrats obsoletes ou incomplets
3. Generer un rapport de conformite
