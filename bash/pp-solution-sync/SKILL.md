---
name: pp-solution-sync
description: >-
  Exporte une solution Power Platform unmanaged avec PAC CLI (ou utilise un artefact local),
  synchronise sa représentation dans le projet, exécute les générateurs déclarés par le projet et
  prépare la validation Git. Utiliser pour actualiser une solution depuis un environnement ou
  Downloads.
---

# Synchroniser une solution Power Platform

Utiliser le script déterministe du skill pour l'export, l'analyse, la copie et les suppressions. Le projet décrit ses solutions et ses commandes dérivées dans `.pp-solution-sync.json`.

## Modes

- **PAC direct** : si l'utilisateur donne un nom de solution, exporter depuis l'environnement attendu par le manifeste.
- **Artefact local** : si l'utilisateur fournit un ZIP ou un dossier extrait, le passer avec `--artifact`. Ce mode remplace le parcours historique depuis `~/Downloads`.

Ne jamais exécuter `pac solution publish`, exporter managed par défaut, importer dans Dataverse ou changer le profil PAC. Le script omet `--managed` et passe explicitement l'URL d'environnement du manifeste.

## Préparer

1. Lire `.pp-solution-sync.json` et résoudre le nom unique, la cible, l'environnement et les mappings.
2. Vérifier `git status --short`. Le script refuse un worktree sale. N'utiliser `--allow-dirty` qu'après autorisation explicite et audit des fichiers déjà modifiés; ne jamais inclure ces changements dans un commit de synchronisation.
3. Lancer :

```sh
python3 <skill>/scripts/sync_solution.py prepare \
  --project-root <projet> \
  --solution <nom-unique>
```

Avec un artefact existant :

```sh
python3 <skill>/scripts/sync_solution.py prepare \
  --project-root <projet> \
  --solution <nom-unique> \
  --artifact <zip-ou-dossier>
```

Le script exporte dans un dossier temporaire, lit le ZIP sans imposer le format `.cdsproj`/SolutionPackager, vérifie `solution.xml`, extrait seulement les mappings déclarés et écrit un plan JSON.

## Confirmer et appliquer

Présenter les ajouts, modifications, suppressions et fichiers ignorés. Attendre une confirmation explicite avant :

```sh
python3 <skill>/scripts/sync_solution.py apply --plan <plan.json>
```

Le script vérifie que les fichiers cibles n'ont pas changé depuis le plan. En cas d'écart, arrêter et reconstruire le plan.

## Régénérer et valider

Après application, exécuter dans l'ordre chaque tableau `command` de `postSync`, puis de `validation`. Ne pas interpréter les chaînes avec un shell; passer les arguments tels qu'ils sont déclarés.

Présenter ensuite : environnement, nom unique, version locale précédente et version exportée, compte des ajouts/modifications/suppressions, commandes dérivées, validations et `git diff --stat`.

Si une commande échoue, conserver le dossier temporaire, diagnostiquer l'échec et ne pas déclarer la solution à jour.

## Validation humaine, commit et nettoyage

Attendre la validation de l'utilisateur avant le nettoyage. Le commit est optionnel et exige une demande ou une confirmation explicite; il ne contient que les changements attribuables à cette exécution.

Après validation :

```sh
python3 <skill>/scripts/sync_solution.py cleanup --plan <plan.json>
```

Ne jamais supprimer un ZIP ou dossier fourni par l'utilisateur. `cleanup` ne supprime que le dossier temporaire créé par le script et protégé par son fichier sentinelle.

## Manifeste de projet

Le manifeste versionné porte :

- `solutions.<nom>.target` : dossier local;
- `expectedEnvironmentUrl` : environnement autorisé pour l'export;
- `packageType` : actuellement `Unmanaged` uniquement;
- `mappings` : fichiers, dossiers ou fichiers aplatis gérés;
- `postSync` : générateurs propres au projet;
- `validation` : barrières finales.

Les mappings sont une liste d'autorisation. Une nouvelle catégorie de solution exige une mise à jour explicite du manifeste; ne jamais la copier implicitement.
