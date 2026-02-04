---
name: data-gouv
description: Skill professionnel pour Claude Code permettant d'accéder, télécharger et analyser les données ouvertes françaises via data.gouv.fr. Inclut une librairie Python complète, des exemples de code, et une documentation détaillée des datasets les plus utilisés.
version: 2.1.0
author: Benoit Vinceneux
license: Licence Ouverte 2.0
tags: [opendata, france, data, api, python, datasets, statistics]
---

# Skill data.gouv.fr pour Claude Code

## ⚠️ Nature de ce skill

Ce skill est une **documentation + librairie Python**, **PAS un plugin avec des commandes interactives**.

**Ce que vous trouverez ici :**
- 📚 Documentation de l'API data.gouv.fr
- 🐍 Librairie Python réutilisable
- 📊 Datasets documentés avec exemples
- 💡 Code prêt à l'emploi

**Ce que vous ne trouverez PAS ici :**
- ❌ Commandes slash (`/data-gouv-search`, etc.)
- ❌ Agents interactifs
- ❌ Requêtes en langage naturel

**Pour des commandes interactives**, utilisez le [MCP officiel data.gouv.fr](https://github.com/datagouv/datagouv-mcp).

---

## Vue d'ensemble

Ce skill fournit un accès programmatique complet aux données ouvertes françaises hébergées sur [data.gouv.fr](https://www.data.gouv.fr/), le portail national des données publiques.

**Capacités principales :**
- 🔍 Recherche de datasets via l'API officielle
- 📥 Téléchargement automatique et mise en cache
- 🧹 Parsing intelligent des formats français (CSV avec `;`, dates DD/MM/YYYY, décimales `,`)
- 📊 Chargement direct dans pandas DataFrames
- 📚 Documentation complète des datasets fréquemment utilisés
- 🐍 Librairie Python réutilisable et professionnelle

## Nouvelles fonctionnalités v2.0.0

Cette version 2.0.0 ajoute le support du **MCP (Model Context Protocol) officiel de data.gouv.fr** en complément de notre librairie Python.

### Deux approches complémentaires

**1. Notre librairie Python** (recommandée pour 80% des cas)
- ✅ Simple : `pip install` et c'est tout
- ✅ Offline : Cache local
- ✅ Portable : Fonctionne partout
- ✅ Léger : Pas de Docker ni serveur

**2. MCP officiel data.gouv.fr** (pour 20% des cas avancés)
- ✅ Requêtes SQL complexes via Hydra
- ✅ Recherche dans toute la base
- ✅ Création de datasets
- ⚠️ Nécessite Docker + configuration

### Comment choisir ?

**Utilisez notre librairie Python si :**
- Vous voulez télécharger et analyser des datasets
- Vous travaillez offline ou avec cache
- Vous faites des scripts automatisés
- Vous préférez la simplicité

**Utilisez le MCP officiel si :**
- Vous avez besoin de requêtes SQL complexes
- Vous voulez créer/modifier des datasets
- Vous posez des questions en langage naturel sur les données

### Documentation

- **Guide de choix détaillé** : [GUIDE_CHOIX.md](GUIDE_CHOIX.md)
- **Documentation MCP officiel** : [mcp/MCP_OFFICIEL.md](mcp/MCP_OFFICIEL.md)
- **Repository MCP officiel** : https://github.com/datagouv/datagouv-mcp

## Installation

### Via le marketplace Claude Code (recommandé)

```bash
/plugin marketplace add benoitvx/data-gouv-skill
/plugin install data-gouv@data-gouv-skill
```

### Installation manuelle

```bash
# Installation globale (disponible dans tous les projets)
cd ~/.claude/skills
git clone https://github.com/benoitvx/data-gouv-skill.git

# OU installation par projet
cd /chemin/vers/votre/projet
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/benoitvx/data-gouv-skill.git
```

### Dépendances Python

```bash
pip install pandas requests openpyxl
```

## Utilisation rapide

Une fois installé, vous pouvez directement utiliser la librairie dans Claude Code :

```python
# Importer la librairie
from data-gouv.lib.datagouv import DataGouvAPI, quick_search

# Recherche rapide
datasets = quick_search("vaccination")
for ds in datasets:
    print(f"{ds['title']} - {ds['organization']['name']}")

# Utilisation complète de l'API
api = DataGouvAPI()

# Rechercher des datasets
results = api.search_datasets("qualité eau", page_size=10)

# Charger directement un CSV
df = api.load_csv("https://www.data.gouv.fr/fr/datasets/r/resource-id")

# Obtenir la dernière ressource d'un dataset
resource = api.get_latest_resource("dataset-id", format="csv")
```

## Structure du skill

```
data-gouv-skill/
├── .claude-plugin/
│   ├── plugin.json          # Métadonnées du plugin
│   └── marketplace.json     # Configuration marketplace
│
├── skills/data-gouv/
│   ├── SKILL.md            # Ce fichier (point d'entrée)
│   │
│   ├── lib/
│   │   └── datagouv.py     # Librairie Python principale
│   │
│   ├── datasets/           # Documentation des datasets
│   │   ├── iqvia-vaccination.md
│   │   ├── eau-potable.md
│   │   ├── calendrier-scolaire.md
│   │   └── ...
│   │
│   └── examples/           # Exemples de code
│       ├── basic_search.py
│       ├── vaccination_analysis.py
│       ├── water_quality.py
│       └── ...
│
├── scripts/
│   ├── sync-datasets.sh    # Synchroniser les métadonnées
│   └── update-metadata.py  # Mettre à jour la documentation
│
└── README.md               # Documentation GitHub
```

## Datasets documentés

Le skill inclut une documentation détaillée pour les datasets les plus utilisés :

### 1. IQVIA France - Vaccinations anti-grippales

**Organisation** : IQVIA France  
**Mise à jour** : Hebdomadaire (campagne de vaccination)  
**Format** : CSV, XLSX

Données de suivi des campagnes de vaccination contre la grippe saisonnière, avec détail par région, département, tranche d'âge et type de site de vaccination.

**Documentation** : [datasets/iqvia-vaccination.md](datasets/iqvia-vaccination.md)

**Exemple d'utilisation** :
```python
# Rechercher le dataset de la campagne actuelle
results = api.search_datasets("vaccination grippe 2025-2026", organization="iqvia-france")
dataset_id = results['data'][0]['id']

# Charger les données
resource = api.get_latest_resource(dataset_id, format='csv')
df = api.load_csv(resource['url'])

# Filtrer par région
df_na = df[df['code_region'] == '75']  # Nouvelle-Aquitaine
print(f"Total vaccinations: {df_na['nb_doses'].sum():,}")
```

### 2. Contrôle sanitaire de l'eau potable

**Organisation** : Ministère de la Santé  
**Mise à jour** : Mensuelle  
**Format** : CSV (fichiers volumineux)

Résultats complets des analyses de qualité de l'eau du robinet, commune par commune, avec tous les paramètres testés (microbiologie, chimie, physico-chimie).

**Documentation** : [datasets/eau-potable.md](datasets/eau-potable.md)

**Exemple d'utilisation** :
```python
# Charger le fichier de correspondance communes/UDI
dataset_id = "resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune"
dataset = api.get_dataset(dataset_id)

# Obtenir les données pour une commune
udi_com = api.load_csv(udi_com_resource_url)
udi_larochelle = udi_com[udi_com['codecommune'] == '17300']

# Analyser la conformité
results = api.load_csv(results_resource_url)
conformite = results['conforme'].value_counts()
taux = (conformite.get('O', 0) / len(results)) * 100
print(f"Taux de conformité: {taux:.1f}%")
```

### 3. Calendrier scolaire

**Organisation** : Ministère de l'Éducation Nationale  
**Mise à jour** : Annuelle  
**Format** : CSV, JSON

Calendrier officiel des vacances scolaires par zone académique (A, B, C) et pour l'ensemble du territoire.

**Zones académiques** :
- **Zone A** : Besançon, Bordeaux, Clermont-Ferrand, Dijon, Grenoble, Limoges, Lyon, Poitiers
- **Zone B** : Aix-Marseille, Amiens, Caen, Lille, Nancy-Metz, Nantes, Nice, Orléans-Tours, Reims, Rennes, Rouen, Strasbourg
- **Zone C** : Créteil, Montpellier, Paris, Toulouse, Versailles

### Autres datasets disponibles

- Population légale (INSEE)
- Code Officiel Géographique (COG)
- Qualité de l'air
- Production d'énergie renouvelable
- Transports publics (GTFS)
- Pharmacies et services de santé

## Librairie Python

### Classe principale : DataGouvAPI

```python
from data-gouv.lib.datagouv import DataGouvAPI

api = DataGouvAPI(cache_dir="/custom/cache/dir")  # optionnel
```

#### Méthodes disponibles

**search_datasets(query, organization=None, tag=None, page_size=20, page=1)**
- Rechercher des datasets dans le catalogue
- Retourne : `Dict[str, Any]` avec résultats et métadonnées

**get_dataset(dataset_id)**
- Obtenir les détails complets d'un dataset
- Retourne : `Dict[str, Any]` ou `None`

**get_latest_resource(dataset_id, format='csv', title_contains=None)**
- Obtenir la ressource la plus récente d'un format donné
- Retourne : `Dict[str, Any]` ou `None`

**download_resource(resource_url, cache=True)**
- Télécharger une ressource (avec cache automatique)
- Retourne : `bytes` ou `None`

**load_csv(resource_url, sep=None, encoding=None, decimal=',', cache=True)**
- Charger un CSV avec détection automatique des formats français
- Retourne : `pd.DataFrame` ou `None`

### Fonctions utilitaires

```python
from data-gouv.lib.datagouv import quick_search, load_dataset_csv

# Recherche rapide
datasets = quick_search("vaccination", limit=5)

# Chargement rapide d'un CSV
df = load_dataset_csv("dataset-id", resource_index=0)
```

## Exemples complets

### Analyse de vaccination par département

```python
from data-gouv.lib.datagouv import DataGouvAPI
import pandas as pd
import matplotlib.pyplot as plt

api = DataGouvAPI()

# Charger les données
results = api.search_datasets("vaccination grippe 2025-2026", organization="iqvia-france")
dataset_id = results['data'][0]['id']
resource = api.get_latest_resource(dataset_id, format='csv')
df = api.load_csv(resource['url'])

# Analyser par département en Nouvelle-Aquitaine
df_na = df[df['code_region'] == '75']
par_dept = df_na.groupby('libelle_departement')['nb_doses'].sum().sort_values()

# Visualiser
plt.figure(figsize=(12, 6))
par_dept.plot(kind='barh')
plt.title('Vaccinations anti-grippales par département (Nouvelle-Aquitaine)')
plt.xlabel('Nombre de doses')
plt.tight_layout()
plt.savefig('vaccinations_departement.png', dpi=150)
```

### Comparaison qualité de l'eau entre communes

```python
from data-gouv.lib.datagouv import DataGouvAPI

api = DataGouvAPI()

communes = {
    'La Rochelle': '17300',
    'Royan': '17306',
    'Saintes': '17415'
}

# Charger les données
dataset_id = "resultats-du-controle-sanitaire-de-leau-distribuee-commune-par-commune"
dataset = api.get_dataset(dataset_id)

# Analyser chaque commune
for nom, code in communes.items():
    # ... (voir datasets/eau-potable.md pour le code complet)
    print(f"{nom}: {taux_conformite:.1f}% de conformité")
```

## Bonnes pratiques

### 1. Utiliser le cache

Le cache est activé par défaut et économise de la bande passante :

```python
api = DataGouvAPI(cache_dir="~/.cache/datagouv")
df = api.load_csv(url, cache=True)  # cache=True par défaut
```

### 2. Gérer les fichiers volumineux

Pour les gros fichiers (>100 MB), charger par chunks :

```python
chunks = []
for chunk in pd.read_csv(url, chunksize=10000, sep=';', encoding='utf-8'):
    # Filtrer immédiatement
    chunk_filtered = chunk[chunk['region'] == 'Nouvelle-Aquitaine']
    chunks.append(chunk_filtered)

df = pd.concat(chunks, ignore_index=True)
```

### 3. Valider les données

Toujours vérifier la qualité des données chargées :

```python
df = api.load_csv(url)

if df is not None:
    print(f"✓ Chargé: {len(df)} lignes, {len(df.columns)} colonnes")
    print(f"✓ Colonnes: {df.columns.tolist()}")
    print(f"✓ Période: {df['date'].min()} à {df['date'].max()}")
else:
    print("✗ Erreur de chargement")
```

### 4. Gestion des erreurs

```python
try:
    df = api.load_csv(url)
    if df is None:
        raise ValueError("Failed to load CSV")

    # Traiter les données
    result = df.groupby('region')['value'].sum()

except Exception as e:
    print(f"Erreur: {e}")
    # Fallback ou alternative
```

## Formats de données français

### CSV
- **Séparateur** : `;` (détecté automatiquement)
- **Encodage** : `utf-8`, `latin-1`, ou `cp1252` (détecté automatiquement)
- **Décimales** : `,` au lieu de `.` (géré automatiquement)

### Dates
- **Format courant** : `DD/MM/YYYY`
- **Format ISO** : `YYYY-MM-DD`
- **Semaines ISO** : `YYYY-Www` (ex: 2025-W42)

### Codes géographiques
- **Commune** : Code INSEE 5 chiffres (ex: `17300`)
- **Département** : 2 ou 3 chiffres (ex: `17`, `2A`, `2B`)
- **Région** : 2 chiffres (ex: `75` pour Nouvelle-Aquitaine)

## Ressources et support

### Documentation officielle
- [data.gouv.fr](https://www.data.gouv.fr/)
- [API documentation](https://www.data.gouv.fr/fr/apidoc/)
- [Guide des producteurs](https://guides.data.gouv.fr/)

### Organisations principales
- **INSEE** : Statistiques, population, économie
- **Ministère de la Santé** : Santé publique, qualité de l'eau
- **IQVIA France** : Campagnes de vaccination
- **Santé Publique France** : Surveillance sanitaire
- **Ministère de l'Éducation** : Données scolaires
- **Ministère de la Transition Écologique** : Environnement, énergie

### Support du skill
- **Issues** : [GitHub Issues](https://github.com/benoitvx/data-gouv-skill/issues)
- **Contributions** : Pull requests bienvenues !
- **Licence** : Licence Ouverte 2.0 (compatible CC-BY)

## Contribution

Les contributions sont les bienvenues ! Pour ajouter un nouveau dataset documenté :

1. Créer un fichier `datasets/nom-dataset.md`
2. Suivre le modèle des datasets existants
3. Ajouter des exemples de code concrets
4. Soumettre une pull request

## Changelog

### v2.0.0 (2025-12-02)
- 🚀 Ajout support MCP officiel data.gouv.fr
- 📝 Guide de choix entre librairie Python et MCP
- 📚 Documentation complète du MCP officiel
- 🔗 Liens vers repository officiel
- ✨ Deux approches complémentaires pour tous les cas d'usage

### v1.0.0 (2025-12-02)
- 🎉 Version initiale
- ✅ Librairie Python complète
- ✅ Documentation IQVIA Vaccination
- ✅ Documentation Qualité de l'eau
- ✅ Exemples de code
- ✅ Cache automatique
- ✅ Support formats français

---

**Auteur** : Benoit Vinceneux
**Licence** : Licence Ouverte 2.0
**Version** : 2.0.0
**Dernière mise à jour** : 2025-12-02
