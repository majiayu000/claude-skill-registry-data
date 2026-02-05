---
name: framework:make:contracts
description: Génère les interfaces de contrats pour une architecture Elegant Objects
license: MIT
version: 1.0.0
---

# Framework Make Contracts Skill

## Description
Génère l'ensemble des interfaces de contrats nécessaires pour une architecture respectant les principes Elegant Objects et DDD.

Ces interfaces servent de fondation pour toutes les autres skills du framework.

## Usage
```
Use skill framework:make:contracts
```

## Templates
- `OutInterface.php` - Interface pour objets de sortie (DTO)
- `InvalideInterface.php` - Interface pour exceptions métier
- `HasUrlsInterface.php` - Interface pour objets ayant des URLs
- `OutDataInterface.php` - Interface pour data classes de sortie
- `InvalideDataInterface.php` - Interface pour data classes d'invalidation
- `UrlsDataInterface.php` - Interface pour data classes d'URLs
- `Story/StoryInterface.php` - Interface pour stories de tests
- `Doctrine/DoctrineMigrationInterface.php` - Interface pour migrations Doctrine

## Variables requises
Aucune - Ces interfaces sont génériques et ne nécessitent pas de paramètres.

## Dépendances
Aucune - C'est la première skill à exécuter (Niveau 0 - Fondation).

## Outputs
- `src/Contracts/OutInterface.php`
- `src/Contracts/InvalideInterface.php`
- `src/Contracts/HasUrlsInterface.php`
- `src/Contracts/OutDataInterface.php`
- `src/Contracts/InvalideDataInterface.php`
- `src/Contracts/UrlsDataInterface.php`
- `src/Contracts/Story/StoryInterface.php`
- `src/Contracts/Doctrine/DoctrineMigrationInterface.php`

## Workflow

1. Vérifier si le répertoire `src/Contracts/` existe
2. Créer la structure de répertoires si nécessaire :
   - `src/Contracts/`
   - `src/Contracts/Story/`
   - `src/Contracts/Doctrine/`
3. Copier tous les templates d'interfaces depuis `framework/skills/make-contracts/templates/Contracts/` vers `src/Contracts/`
4. Afficher la liste des fichiers créés

## Notes
- Ces interfaces n'ont pas besoin d'être modifiées pour chaque projet
- Elles doivent être créées une seule fois par projet
- Toutes les autres skills du framework dépendent de ces interfaces
