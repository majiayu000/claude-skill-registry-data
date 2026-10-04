---
name: graph-intel
description: "Intelligence relationnelle via graphe KùzuDB : filiales, dirigeants, contacts croisés. Utiliser pour comprendre le réseau d'une entreprise ou d'un groupe."
metadata: { "openclaw": { "emoji": "🕸️", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# Graph Intel — Intelligence relationnelle

## Déclencheur
- `/graph 123456789 relations`
- "montre le réseau de cette entreprise"
- "quelles sont les filiales de ce groupe"
- "qui dirige cette entreprise et ses liens"

## Ce que fait ce skill
Exploite une base de données graphe **KùzuDB** pour modéliser et interroger les relations entre :
- **Entreprises** : liens de groupe, filiales, participations
- **Dirigeants** : mandats croisés, réseaux d'influence
- **Contacts** : personnes identifiées dans chaque entreprise

## Schéma du graphe
```
Dirigeant --[DIRIGE]--> Entreprise
Entreprise --[FILIALE_DE]--> Entreprise
Entreprise --[A_CONTACT]--> Contact
```

## Utilisation

### Ingérer des données dans le graphe
```bash
source /opt/albert-ml/bin/activate
python3 scripts/graph_ingest.py --file /home/node/.openclaw/data/entreprises.json
```

### Requêter le graphe
```bash
source /opt/albert-ml/bin/activate
python3 scripts/graph_query.py --siren 123456789 --query-type full_network
```

## Arguments de graph_query.py
| Argument        | Description                          | Défaut         |
|----------------|--------------------------------------|----------------|
| `--siren`       | SIREN de l'entreprise                | (requis)       |
| `--query-type`  | Type de requête                      | `full_network` |

### Types de requêtes disponibles
| Type            | Description                                           |
|----------------|-------------------------------------------------------|
| `subsidiaries`  | Filiales directes et indirectes du groupe             |
| `directors`     | Dirigeants et leurs mandats croisés                   |
| `contacts`      | Contacts identifiés dans l'entreprise                 |
| `full_network`  | Vue complète : filiales + dirigeants + contacts       |
| `no_dpo`        | Entreprises du groupe sans DPO identifié              |

## Arguments de graph_ingest.py
| Argument    | Description                                    | Défaut   |
|------------|------------------------------------------------|----------|
| `--file`    | Fichier JSON avec données à ingérer           | (requis) |
| `--reset`   | Réinitialiser la base avant ingestion          | false    |

### Format du fichier d'ingestion
```json
{
  "entreprises": [
    {"siren": "123456789", "nom": "Groupe Alpha", "naf": "7022Z", "effectif": 200, "dept": "31"}
  ],
  "dirigeants": [
    {"id": "dir_001", "nom": "Jean Dupont"}
  ],
  "contacts": [
    {"id": "ct_001", "nom": "Marie Martin", "email": "m.martin@alpha.fr", "role": "RSSI"}
  ],
  "relations": {
    "dirige": [{"dirigeant_id": "dir_001", "siren": "123456789"}],
    "filiale_de": [{"siren_filiale": "987654321", "siren_parent": "123456789"}],
    "a_contact": [{"siren": "123456789", "contact_id": "ct_001"}]
  }
}
```

## Stockage
- Base KùzuDB : `/home/node/.openclaw/data/prospects.kuzu`

## Sortie
```json
{
  "siren": "123456789",
  "query_type": "full_network",
  "entreprise": {"nom": "Groupe Alpha", "naf": "7022Z"},
  "filiales": [...],
  "dirigeants": [...],
  "contacts": [...],
  "stats": {"total_filiales": 5, "total_contacts": 12}
}
```

## Cas d'usage prospection
1. **Identifier les groupes** : une filiale convertie = porte d'entrée pour tout le groupe
2. **Mandats croisés** : un dirigeant convaincu dans une entreprise = accès à ses autres mandats
3. **Entreprises sans DPO** : cibles prioritaires pour les services RGPD
4. **Taille du réseau** : groupes avec beaucoup de filiales = contrats cadre potentiels
