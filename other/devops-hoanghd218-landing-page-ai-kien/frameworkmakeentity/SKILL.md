---
name: framework:make:entity
description: Génère une entité Doctrine avec repository selon principes Elegant Objects
license: MIT
version: 1.0.0
---

# Framework Make Entity Skill

## Description
Génère une entité Doctrine complète avec son repository selon les principes Elegant Objects.

## Usage
```
Use skill framework:make:entity
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: product)
- **{namespace}** - Namespace du projet (défaut: App)
- **{properties}** - Liste des propriétés avec types (name:string, price:float)

## Dépendances
- Contracts présents (appelle `framework:make:contracts` si absent)

## Outputs
- `src/Entity/{EntityName}.php`
- `src/Repository/{EntityName}Repository.php`
- `src/Repository/{EntityName}RepositoryInterface.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Demander les propriétés (nom, type, nullable)
3. Vérifier si `src/Contracts/` existe, sinon appeler `framework:make:contracts`
4. Générer l'entité depuis le template `templates/Entity/`
5. Générer le repository et son interface
6. Afficher le résumé des fichiers créés

## Patterns appliqués

### Entité
- Classe `final`, constructeur privé, factory statique `create()`
- Traits : DatabaseTrait, NullTrait, DependencyInjectionTrait
- Interfaces : LoggableInterface, DatabaseEntityInterface, NullableInterface, DependencyInjectionAwareInterface, OutInterface, HasUrlsInterface, InvalideInterface

### Repository
- Classe `final`, extends ServiceEntityRepository
- Implémente interface du repository

## References

- [Usage](references/usage.md) - Exemples et détails de génération

## Notes
- ID Uuid ajouté automatiquement
- Propriétés privées avec getters (pas de setters)
- Méthode `toLog()` inclut toutes les propriétés
