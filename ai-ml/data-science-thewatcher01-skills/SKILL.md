---
name: data-science
description: |
  Agent data scientist spécialisé dans l'exploitation du datalake SubventionAI (2.8M entités, 168K versements, scoring ML, embeddings bge-m3 1024d). Stack: Python, PostgreSQL+pgvector, scikit-learn, XGBoost, LightGBM, spaCy, pandas. Use when: feature engineering, model training/evaluation, scoring batch, analyse statistique sectorielle, corrélation, clustering, prédiction, classification, anomaly detection, NLP sur objets sociaux, requêtes SQL analytiques, optimisation hyperparamètres. Triggers: data science, ML, modèle, scoring, feature engineering, prédiction, classification, clustering, analyse sectorielle, fundability, anomalie, NLP, embeddings, train, evaluate, cross-validation, AUC, F1, SHAP, Optuna.
---

# Data Science Agent — Datalake SubventionAI

## Données disponibles

Consulter `references/schema.md` pour le schéma complet.

| Table | Rows | Clé |
|-------|------|-----|
| dl_entities | 2.8M | SIREN, NAF, géo, scores, industryData JSONB |
| dl_subventions_versees | 168K | Historique versements réels 2010-2026 |
| dl_subventions | 2413 | Programmes actifs |
| dl_subvention_anomalies | 3.1K | Anomalies détectées |
| dl_bodacc_annonces | - | Annonces légales |
| dl_marches_publics | - | Marchés publics |

Connexion : `PGPASSWORD=datalake_dev psql -h 127.0.0.1 -p 5434 -U datalake -d datalake`

## Workflow ML

1. **Extraction** : SQL paramétré, export CSV pour batch compute
2. **Feature engineering** : pandas + NumPy dans `scripts/ml/`
3. **Training** : scikit-learn/XGBoost/LightGBM, cross-validation 5-fold
4. **Evaluation** : AUC-ROC, F1, precision/recall, SHAP feature importance
5. **Tuning** : Optuna (TPE sampler, 100 trials)
6. **Scoring batch** : export → compute local → reimport PG (séparer compute et I/O)
7. **Persistance** : colonnes dédiées dans dl_entities

## Scoring existant

| Score | Colonne | Modèle |
|-------|---------|--------|
| Fundability | fundabilityScore | Batch SQL 6 critères |
| Digital maturity | digitalMaturityScore | 7 facteurs rule-based |
| CNIL risk | cnilRiskScore | XGBoost AUC 0.90 |
| Hot lead | hotLeadScore | Composite 6 dimensions |

## Règles critiques

- SQL toujours paramétré ($1, $2) — jamais d'interpolation
- Données factuelles uniquement — jamais de chiffres approximatifs
- Performance first : batch SQL, COPY pour imports, pas de N+1
- Scripts dans `scripts/ml/` avec docstring et `if __name__ == "__main__":`
- Modèles évalués avec cross-validation avant déploiement
- Embeddings : bge-m3 1024d, colonne `vector(1024)` pgvector, index HNSW

## Patterns courants

Consulter `references/patterns.md` pour templates SQL et Python.
