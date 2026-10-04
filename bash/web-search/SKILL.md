---
name: web-search
description: "Recherche sur le web via SearXNG auto-hébergé. Utiliser quand l'utilisateur demande de chercher des informations, actualités, ou données sur le web."
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# Web Search — Recherche web via SearXNG

## Déclencheur
- `/search NIS2 actualités France`
- "cherche sur le web X"
- "recherche les dernières nouvelles sur Y"

## Ce que fait ce skill
Interroge l'instance SearXNG auto-hébergée pour effectuer des recherches web.
Catégories disponibles : `general`, `news`, `it`, `science`, `social_media`.

## Utilisation

```bash
source /opt/albert-ml/bin/activate
python3 scripts/search.py --query "NIS2 réglementation France" --category news --lang fr --limit 10
```

## Arguments
| Argument     | Description                            | Défaut     |
|-------------|----------------------------------------|------------|
| `--query`    | Termes de recherche                    | (requis)   |
| `--category` | Catégorie SearXNG                      | `general`  |
| `--lang`     | Langue des résultats                   | `fr`       |
| `--limit`    | Nombre max de résultats                | `10`       |

## Sortie
Tableau JSON avec pour chaque résultat :
- `title` : titre de la page
- `url` : URL de la page
- `snippet` : extrait de texte
- `engine` : moteur source

## Notes
- L'URL SearXNG est configurée via la variable d'environnement `SEARXNG_URL` (défaut : `http://searxng:8080`)
- Aucune donnée personnelle n'est transmise à des tiers — instance auto-hébergée
- Respecte le RGPD : pas de tracking, pas de cookies tiers
