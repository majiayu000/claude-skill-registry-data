---
name: dl-schema
description: Schema complet PostgreSQL du datalake (20 tables dl_*, volumes, relations)
paths:
  - "prisma/**"
  - "src/adapters/db/**"
  - "src/core/entities/**"
---

# Database Schema — Datalake Souverain

PostgreSQL 16 on port 5434 (5432=calendrier-subvention, 5433=recolte).
Schema prefix: `dl_` tables:

| Table | Volume | Description |
|-------|--------|-------------|
| `dl_entities` | 2.84M | SIRENE+RNA+FINESS, enriched |
| `dl_marches_publics` | 2.88M | DECP Parquet |
| `dl_subventions_versees` | 218K | Historical subsidies |
| `dl_subventions` | 36K | Active programs |
| `dl_subvention_matches` | — | entity<>subvention matching |
| `dl_bodacc_annonces` | 10.5K | Legal announcements |
| `dl_job_queue` | — | Async ML/LLM jobs (hybrid compute) |
| `dl_worker_heartbeats` | — | Worker availability tracking |
| `dl_pipeline_prospects` | — | CRM pipeline (7 stages) |
| `dl_crawl_runs` + `dl_crawl_cursors` | — | Audit trail |
| `dl_dvf_transactions` | — | Transactions immobilieres DVF |
| `dl_erp_accessibilite` | — | ERP accessibilite (AccesLibre) |
| `dl_emploi_territorial` | — | Effectifs/DPAE/auto-entrepreneurs (FLORES+URSSAF) |
| `dl_organismes_formation` | — | Organismes Qualiopi |
| `dl_transparence_sante` | — | Liens pharma<>beneficiaires |
| `dl_cnil_controles` | — | Historique controles CNIL 2014-2023 |
| `dl_dpe_tertiaire` + `dl_dpe_entity_scores` | — | DPE batiments tertiaires |
| `dl_epci` | 1.5K | EPCI intercommunalites (BANATIC, SIREN-indexed) |
| `dl_kali_conventions` | 407 | Conventions collectives IDCC (referentiel KALI) |

Extensions: Apache AGE (graph), pgvector (vector 1024-dim), ltree (hierarchy).
