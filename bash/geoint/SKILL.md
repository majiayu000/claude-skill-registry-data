---
name: geoint
description: "Intelligence géospatiale : géocodage d'adresses et création de cartes interactives. Utiliser pour cartographier des prospects, visualiser un marché géographiquement."
metadata: { "openclaw": { "emoji": "🗺️", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# GEOINT — Intelligence géospatiale

## Déclencheur
- `/carte ESN Toulouse`
- "cartographie les prospects du 31"
- "montre les entreprises sur une carte"
- "géolocalise les prospects en Occitanie"

## Ce que fait ce skill
1. Géocode des adresses françaises via l'API **BAN** (Base Adresse Nationale)
2. Génère une carte interactive **Folium** (Leaflet.js) avec marqueurs
3. Sauvegarde la carte en fichier HTML consultable dans un navigateur

## Utilisation

### Géocoder une adresse unique
```bash
source /opt/albert-ml/bin/activate
python3 scripts/geoint.py --address "10 rue de la Paix, Paris"
```

### Géocoder un fichier d'entités (JSON)
```bash
source /opt/albert-ml/bin/activate
python3 scripts/geoint.py --input /home/node/.openclaw/data/prospects.json --output /home/node/.openclaw/data/carte_prospects.html
```

Le fichier JSON d'entrée doit contenir une liste d'objets avec au minimum :
```json
[
  {"nom": "Acme Corp", "adresse": "10 rue de la Paix, 75002 Paris"},
  {"nom": "Tech SAS", "adresse": "5 place du Capitole, 31000 Toulouse"}
]
```

## Arguments
| Argument    | Description                          | Défaut                                         |
|------------|--------------------------------------|------------------------------------------------|
| `--address` | Adresse unique à géocoder           | —                                              |
| `--input`   | Fichier JSON avec liste d'entités   | —                                              |
| `--output`  | Chemin du fichier HTML de la carte   | `/home/node/.openclaw/data/carte.html`         |
| `--zoom`    | Niveau de zoom initial de la carte   | `6`                                            |

## Sortie
- Fichier HTML interactif avec marqueurs cliquables
- Résumé JSON : nombre d'entités géocodées, échecs, chemin de la carte

## API utilisée
- **BAN** (api-adresse.data.gouv.fr) — gratuite, sans clé API, données ouvertes françaises
- Aucune donnée personnelle transmise — uniquement des adresses professionnelles

## Limitations
- API BAN = adresses françaises uniquement
- Rate limit : ~50 requêtes/seconde (respecté par le script)
