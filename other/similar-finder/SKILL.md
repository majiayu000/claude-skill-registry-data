---
name: similar-finder
description: "Recherche d'entreprises similaires par embeddings vectoriels. Utiliser pour trouver des prospects qui ressemblent à un client idéal."
metadata: { "openclaw": { "emoji": "🔗", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# Similar Finder — Recherche de prospects similaires

## Déclencheur
- `/similaire 12345678901234` (SIRET du client idéal)
- "trouve des entreprises similaires à mon meilleur client"
- "quels prospects ressemblent à X"
- "lookalike de cette entreprise"

## Ce que fait ce skill
1. Encode le profil textuel d'une entreprise de référence en vecteur d'embedding
2. Recherche par similarité cosinus dans LanceDB
3. Retourne les 10 entreprises les plus proches

## Modèle utilisé
**paraphrase-multilingual-MiniLM-L12-v2** (~470 MB)
- Modèle multilingue optimisé pour le français
- Pré-téléchargé dans l'image Docker
- Embeddings de dimension 384

## Utilisation

### Chercher des similaires par SIRET
```bash
source /opt/albert-ml/bin/activate
python3 scripts/find_similar.py --siret 12345678901234 --top 10
```

### Chercher par description textuelle
```bash
source /opt/albert-ml/bin/activate
python3 scripts/find_similar.py \
    --description "ESN cybersécurité 50 employés Toulouse spécialisée NIS2 et SOC" \
    --top 10
```

### Ingérer une entreprise dans la base vectorielle
```bash
source /opt/albert-ml/bin/activate
python3 scripts/find_similar.py --ingest \
    --siret 12345678901234 \
    --description "Cabinet de conseil IT, 30 salariés, Paris, spécialiste cloud AWS et DevOps"
```

## Arguments
| Argument        | Description                              | Défaut |
|----------------|------------------------------------------|--------|
| `--siret`       | SIRET de l'entreprise de référence      | —      |
| `--description` | Description textuelle du profil cible   | —      |
| `--top`         | Nombre de résultats similaires          | `10`   |
| `--ingest`      | Mode ingestion (ajouter à la base)      | false  |
| `--threshold`   | Score de similarité minimum (0-1)       | `0.5`  |

## Stockage
- Table LanceDB : `company_embeddings` à `/home/node/.openclaw/data/companies.lance`
- Chaque enregistrement : SIRET, nom, description, vecteur 384D, métadonnées

## Sortie
```json
{
  "query": "ESN cybersécurité Toulouse...",
  "results": [
    {
      "siret": "98765432109876",
      "nom": "CyberSec SAS",
      "description": "...",
      "similarity": 0.89,
      "rank": 1
    }
  ],
  "total_in_db": 1500,
  "model": "paraphrase-multilingual-MiniLM-L12-v2"
}
```

## Comment enrichir la base
La base vectorielle s'enrichit automatiquement via les pipelines de données (skill `data-pipes`).
On peut aussi ingérer manuellement avec le flag `--ingest`.
Plus la base est riche, meilleurs sont les résultats de recherche.
