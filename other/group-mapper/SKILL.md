---
name: group-mapper
description: "Cartographie la structure d'un groupe (maison mère, filiales, établissements) via l'API Recherche Entreprises. Utiliser quand l'utilisateur demande la structure d'un groupe, les filiales d'une entreprise, ou veut identifier l'arborescence capitalistique."
metadata: { "openclaw": { "emoji": "🏢" } }
user-invocable: true
---

# Group Mapper

## Objectif

Cartographier la **structure d'un groupe d'entreprises** (maison mère, filiales, établissements secondaires) pour identifier toutes les entités d'un même groupe. Cas d'usage principal : **"1 vente = 10 filiales"** — identifier le potentiel commercial total d'un groupe.

## Déclencheurs

- `/groupe 383474814` (SIREN)
- `/groupe Airbus`
- "montre la structure du groupe X"
- "quelles sont les filiales de Y ?"
- "qui est la maison mère de Z ?"
- "cartographie le groupe ACME"

## Données sources

| Source | Usage |
|--------|-------|
| API Recherche Entreprises (`sirene`) | Recherche par SIREN, identification des liens de groupe, liste des établissements |
| BODACC (optionnel) | Événements récents sur les entités du groupe |

## Logique

### 1. Identification de l'entité de départ

- Si SIREN fourni : recherche directe
- Si nom fourni : recherche textuelle, sélection du résultat le plus pertinent

### 2. Remontée vers la tête de groupe

L'API Recherche Entreprises expose le champ `groupe` ou des liens capitalistiques quand disponibles. Stratégie :

1. Identifier le SIREN de l'entité de départ
2. Chercher le SIREN de la maison mère (si renseigné dans les données INSEE)
3. Lister toutes les entités partageant le même identifiant de groupe

### 3. Descente vers les filiales et établissements

Pour chaque entité du groupe :
- Lister les **établissements** (siège + secondaires) via l'API sirene
- Identifier les **filiales** (entités juridiques distinctes liées au même groupe)
- Récupérer : SIREN/SIRET, raison sociale, NAF, effectif, localisation, statut (actif/fermé)

### 4. Construction de l'arborescence

Organiser les résultats en arbre hiérarchique.

## Format de sortie

```json
{
  "groupe": {
    "nom": "GROUPE ACME",
    "tete_de_groupe": {
      "siren": "383474814",
      "raison_sociale": "ACME HOLDING SA",
      "siege": "Paris (75)",
      "effectif_total_groupe": 1250
    }
  },
  "arborescence": [
    {
      "niveau": 0,
      "type": "maison_mere",
      "siren": "383474814",
      "raison_sociale": "ACME HOLDING SA",
      "naf": "7010Z",
      "effectif": 15,
      "siege": "Paris (75)",
      "statut": "actif",
      "etablissements": [
        { "siret": "38347481400012", "type": "siege", "adresse": "Paris 8e" }
      ]
    },
    {
      "niveau": 1,
      "type": "filiale",
      "siren": "383474822",
      "raison_sociale": "ACME CONSULTING SAS",
      "naf": "7022Z",
      "effectif": 85,
      "siege": "Toulouse (31)",
      "statut": "actif",
      "lien": "filiale 100%",
      "etablissements": [
        { "siret": "38347482200015", "type": "siege", "adresse": "Toulouse" },
        { "siret": "38347482200023", "type": "secondaire", "adresse": "Montpellier" }
      ]
    },
    {
      "niveau": 1,
      "type": "filiale",
      "siren": "383474830",
      "raison_sociale": "ACME DIGITAL SAS",
      "naf": "6201Z",
      "effectif": 200,
      "siege": "Lyon (69)",
      "statut": "actif",
      "lien": "filiale 100%",
      "etablissements": [
        { "siret": "38347483000018", "type": "siege", "adresse": "Lyon" },
        { "siret": "38347483000026", "type": "secondaire", "adresse": "Bordeaux" },
        { "siret": "38347483000034", "type": "secondaire", "adresse": "Nantes" }
      ]
    }
  ],
  "synthese": {
    "nombre_entites_juridiques": 3,
    "nombre_etablissements_total": 6,
    "effectif_cumule": 300,
    "regions_presence": ["Île-de-France", "Occitanie", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine", "Pays de la Loire"],
    "secteurs_naf": ["7010Z", "7022Z", "6201Z"]
  },
  "potentiel_commercial": {
    "approche": "La tête de groupe est à Paris mais les filiales opérationnelles sont en régions. Cibler ACME CONSULTING (Toulouse, 85 sal.) comme point d'entrée — même région, taille accessible. Si conversion, potentiel de déploiement sur ACME DIGITAL (200 sal.) et les 3 autres établissements.",
    "contacts_entrees_recommandees": [
      "ACME CONSULTING SAS — Toulouse — 85 salariés — Conseil management"
    ],
    "valeur_potentielle": "1 contrat initial pourrait couvrir 3 entités juridiques et 6 établissements"
  }
}
```

## Représentation arbre (texte)

En plus du JSON, produire une représentation textuelle lisible :

```
ACME HOLDING SA (383474814) — Paris — 15 sal.
├── ACME CONSULTING SAS (383474822) — Toulouse — 85 sal.
│   └── [Secondaire] Montpellier
├── ACME DIGITAL SAS (383474830) — Lyon — 200 sal.
│   ├── [Secondaire] Bordeaux
│   └── [Secondaire] Nantes
```

## Règles

- Ne montrer que les entités **actives** (sauf si demande explicite des entités fermées).
- Limiter la profondeur à 3 niveaux max.
- Si le groupe est très grand (> 50 entités), afficher les 20 plus grandes et indiquer le total.
- Les données de liens capitalistiques ne sont pas toujours disponibles dans les données INSEE — indiquer clairement quand l'arborescence est reconstituée par heuristique (même adresse de siège, même dirigeant, etc.) vs. données officielles.
- Toujours inclure le potentiel commercial (approche "1 vente = N filiales").
