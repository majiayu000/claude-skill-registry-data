---
name: sector-analyst
description: "Analyse sectorielle et tendances à partir des données accumulées : croissance par NAF, signaux d'embauche, subventions, défaillances. Utiliser pour analyser un marché ou un secteur."
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# Sector Analyst — Analyse sectorielle et tendances

## Déclencheur
- `/secteur IT Occitanie`
- "analyse du secteur cybersécurité en France"
- "tendances du marché IT à Toulouse"
- "quels secteurs recrutent le plus en DevSecOps"

## Ce que fait ce skill
Analyse les données accumulées dans LanceDB pour produire un rapport sectoriel :

1. **Distribution NAF** — répartition des entreprises par code NAF dans le périmètre
2. **Signaux d'embauche** — heatmap des recrutements par département
3. **Subventions disponibles** — taux d'éligibilité par secteur
4. **Signaux de défaillance** — patterns BODACC (liquidations, redressements)
5. **Score d'opportunité** — scoring global du secteur pour la prospection

## Utilisation

```bash
source /opt/albert-ml/bin/activate
python3 scripts/analyze_sector.py --sector IT --region Occitanie
```

### Analyse par code NAF
```bash
source /opt/albert-ml/bin/activate
python3 scripts/analyze_sector.py --naf 6201Z
```

### Analyse d'un département
```bash
source /opt/albert-ml/bin/activate
python3 scripts/analyze_sector.py --dept 31
```

## Arguments
| Argument    | Description                          | Défaut    |
|------------|--------------------------------------|-----------|
| `--sector`  | Secteur macro (IT, CYBER, CONSEIL)  | —         |
| `--naf`     | Code NAF spécifique                  | —         |
| `--region`  | Région française                     | —         |
| `--dept`    | Numéro de département                | —         |
| `--format`  | Format de sortie (json, report)      | `json`    |

## Secteurs macro supportés
| Code      | Description                    | Codes NAF inclus           |
|-----------|-------------------------------|----------------------------|
| `IT`      | Services informatiques        | 6201Z-6209Z, 6311Z-6312Z  |
| `CYBER`   | Cybersécurité                 | 6201Z, 6202A (filtré)     |
| `CONSEIL` | Conseil en management         | 7022Z, 7021Z              |
| `LEGAL`   | Juridique                     | 6910Z                     |
| `FINANCE` | Comptabilité et finance       | 6920Z, 6430Z              |
| `TRAINING`| Formation professionnelle     | 8559A, 8559B              |

## Stockage
- Données source : LanceDB tables `prospects` et `signals` à `/home/node/.openclaw/data/`

## Sortie JSON
```json
{
  "sector": "IT",
  "region": "Occitanie",
  "total_companies": 342,
  "naf_distribution": {"6201Z": 120, "6202A": 85, ...},
  "hiring_heatmap": {"31": 45, "34": 22, ...},
  "subsidy_rate": 0.38,
  "bodacc_alerts": 12,
  "opportunity_score": 0.78,
  "top_departments": ["31", "34", "30"],
  "trend": "croissance",
  "recommendation": "Secteur IT en Occitanie : forte demande, 38% éligibles subventions, concentré sur Toulouse"
}
```

## Sortie rapport (--format report)
Génère un rapport textuel structuré directement utilisable pour la prospection commerciale, avec :
- Résumé exécutif
- Chiffres clés
- Cartographie des opportunités
- Recommandations d'action
