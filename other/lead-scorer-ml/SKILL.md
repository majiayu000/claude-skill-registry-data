---
name: lead-scorer-ml
description: "Scoring ML hybride des prospects : LLM au démarrage, RandomForest quand assez de données. Utiliser pour évaluer la probabilité de conversion d'un prospect."
metadata: { "openclaw": { "emoji": "🎯", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# Lead Scorer ML — Scoring hybride des prospects

## Déclencheur
- `/scoreml 12345678901234` (SIRET)
- "analyse ML de cette entreprise"
- "quel est le score de ce prospect"
- "évalue la probabilité de conversion"

## Ce que fait ce skill
Scoring hybride en deux phases :

### Phase 1 — Démarrage (LLM-as-ML)
Quand il n'y a pas encore assez de données d'entraînement, le LLM génère un score structuré basé sur les features du prospect. Aucun modèle entraîné nécessaire.

### Phase 2 — Maturité (RandomForest)
Quand suffisamment de prédictions LLM se sont accumulées dans LanceDB (>100 exemples labelisés), un modèle RandomForest scikit-learn prend le relais pour des prédictions instantanées.

## Utilisation

### Scorer un prospect
```bash
source /opt/albert-ml/bin/activate
python3 scripts/score_lead.py --siret 12345678901234
```

### Scorer avec données manuelles
```bash
source /opt/albert-ml/bin/activate
python3 scripts/score_lead.py \
    --naf 6201Z \
    --employees 50 \
    --age 5 \
    --has-dpo true \
    --recruits-devsecops true \
    --cyber-score 3 \
    --bodacc-count 0 \
    --eligible-subsidies 2
```

### Entraîner le modèle RandomForest
```bash
source /opt/albert-ml/bin/activate
python3 scripts/train_model.py
```

## Arguments de score_lead.py
| Argument                | Description                              | Défaut   |
|------------------------|------------------------------------------|----------|
| `--siret`               | SIRET de l'entreprise (lookup LanceDB)  | —        |
| `--naf`                 | Code NAF                                | —        |
| `--employees`           | Nombre de salariés                      | —        |
| `--age`                 | Âge de l'entreprise en années           | —        |
| `--has-dpo`             | A un DPO (true/false)                   | `false`  |
| `--recruits-devsecops`  | Recrute en DevSecOps (true/false)       | `false`  |
| `--cyber-score`         | Score cyber (0-5)                       | `0`      |
| `--bodacc-count`        | Nombre d'annonces BODACC                | `0`      |
| `--eligible-subsidies`  | Nombre de subventions éligibles         | `0`      |
| `--force-llm`           | Forcer le mode LLM même si modèle ML   | `false`  |

## Features utilisées
| Feature              | Description                          | Poids indicatif |
|---------------------|--------------------------------------|-----------------|
| `naf_code`           | Secteur d'activité (encodé)         | Fort            |
| `employee_count`     | Taille de l'entreprise              | Moyen           |
| `age_years`          | Ancienneté                          | Faible          |
| `has_dpo`            | Présence d'un DPO                   | Fort            |
| `recruits_devsecops` | Recrute en DevSecOps                | Fort            |
| `cyber_score`        | Maturité cybersécurité              | Fort            |
| `bodacc_count`       | Signaux de défaillance              | Négatif         |
| `eligible_subsidies` | Subventions accessibles             | Fort            |

## Stockage
- Prédictions : LanceDB table `prospects` à `/home/node/.openclaw/data/prospects.lance`
- Modèle entraîné : `/home/node/.openclaw/data/models/lead_scorer.pkl`

## Sortie
```json
{
  "siret": "12345678901234",
  "score": 0.82,
  "label": "HOT",
  "method": "random_forest",
  "features": { ... },
  "explanation": "Score élevé : secteur IT, recrute en devsecops, 2 subventions éligibles"
}
```

Labels : `HOT` (>0.7), `WARM` (0.4-0.7), `COLD` (<0.4)
