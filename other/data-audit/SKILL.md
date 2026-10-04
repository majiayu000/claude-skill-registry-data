---
name: data-audit
description: "Audit complet de qualite data sur les 9 dimensions ISO 8000-8. Utiliser pour verifier la fiabilite des donnees d'un projet, d'une table, ou d'un SIREN specifique."
user-invocable: true
context: fork
agent: Explore
allowed-tools: Read, Bash, Grep, Glob
---

# /data-audit — Audit Qualite Data

## Objectif
Evaluer systematiquement la qualite des donnees sur les 9 dimensions ISO 8000-8 et produire un rapport actionnable.

## Arguments
- `$ARGUMENTS` : projet, table, ou SIREN a auditer (optionnel, defaut = projet courant)

## Workflow

### Phase 1 — Decouverte
1. Identifier le schema de donnees (Prisma, Zod, interfaces TypeScript)
2. Lister les sources de donnees externes (crawlers, imports, APIs)
3. Identifier les tables/collections contenant des donnees

### Phase 2 — Evaluation des 9 dimensions
Pour chaque source/table identifiee :

**Dimension 1 — Validite**
- Grep les schemas Zod dans `src/core/entities/` et `src/api/validation.ts`
- Verifier que chaque champ a un type et un domaine de valeurs

**Dimension 2 — Exactitude**
- Verifier les formats cles : SIREN (9 digits), RNA (W+9), NAF (4 digits + lettre)
- Cross-ref : champs verifiables contre source officielle

**Dimension 3 — Fiabilite**
- Classifier chaque source (Tier A/B/C) depuis `src/config/sources.ts`
- Verifier le `confidence_score` par source

**Dimension 4 — Fraicheur**
- Verifier la presence de `source_updated_at` vs `ingested_at`
- Calculer l'age moyen des donnees par source

**Dimension 5 — Completude**
- Identifier les champs obligatoires
- Estimer le taux de null sur les champs critiques

**Dimension 6 — Coherence**
- Detecter les contradictions (deadline < date_ouverture, etc.)
- Verifier la coherence inter-tables (FK, memes SIREN = memes noms)

**Dimension 7 — Unicite**
- Verifier les doublons sur cles primaires (SIREN, RNA, externalId)

**Dimension 8 — Structure**
- Verifier encodage UTF-8, dates ISO, normalisation

**Dimension 9 — Tracabilite**
- Verifier la presence des champs DataProvenance
- Verifier `enrichmentSources` JSONB
- Verifier `lineage_run_id`

### Phase 3 — Rapport
Generer un rapport Markdown avec :
- Score global et par dimension
- Violations classees P0/P1/P2
- Recommandations concretes avec fichiers/lignes
- Comparaison avec les SLOs (Gold/Silver/Bronze)

## Reference
Voir [references/iso8000-dimensions.md](references/iso8000-dimensions.md) pour les definitions completes.
