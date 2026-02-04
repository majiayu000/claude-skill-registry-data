---
name: framework:make:collection
description: Génère classe Collection typée avec traits Atournayre
license: MIT
version: 1.0.0
---

# Framework Make Collection Skill

## Description
Génère une classe Collection typée pour gérer des ensembles d'entités avec les traits et interfaces Atournayre.

## Usage
```
Use skill framework:make:collection
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Entité dans `src/Entity/{EntityName}.php`
- Framework `atournayre/framework`

## Outputs
- `src/Collection/{EntityName}Collection.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Générer la classe Collection depuis le template `templates/Collection/`
4. Afficher le fichier créé

## Patterns appliqués

- Classe `final`
- Interfaces : AsListInterface, ToArrayInterface, CountInterface, CountByInterface, AtLeastOneElementInterface, HasSeveralElementsInterface, HasNoElementInterface, HasOneElementInterface, HasXElementsInterface, LoggableInterface
- Traits : Collection, Collection\ToArray, Collection\Countable
- Méthode statique `asList(array $collection)`

## References

- [Usage](references/usage.md) - Exemples d'utilisation et méthodes métier

## Notes
- Respect du principe YAGNI : pas de méthodes génériques anticipées
- Seules les méthodes explicitement demandées doivent être ajoutées
- Les traits fournissent déjà les fonctionnalités de base
