---
name: framework:make:urls
description: Génère classe Urls + Message CQRS + Handler
license: MIT
version: 1.0.0
---

# Framework Make Urls Skill

## Description
Génère une classe Urls pour la génération d'URLs d'une entité avec pattern CQRS (Message + Handler).

## Usage
```
Use skill framework:make:urls
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Entité dans `src/Entity/{EntityName}.php`
- Repository dans `src/Repository/{EntityName}Repository.php`
- Interface repository dans `src/Repository/{EntityName}RepositoryInterface.php`

## Outputs
- `src/Urls/{EntityName}Urls.php`
- `src/MessageHandler/{EntityName}UrlsMessage.php`
- `src/MessageHandler/{EntityName}UrlsMessageHandler.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité et le repository existent
3. Générer les 3 classes depuis les templates `templates/`
4. Afficher les fichiers créés

## Patterns appliqués

### Classe Urls
- `final readonly`, constructeur privé, factory `new()`
- Propriétés : UrlGeneratorInterface + entité

### Message CQRS
- Extends AbstractQueryEvent, Implements QueryInterface
- `final`, constructeur privé, factory `new()`

### MessageHandler
- `final readonly`, attribut #[AsMessageHandler]
- Injection : repository + UrlGeneratorInterface

## References

- [Usage](references/usage.md) - Architecture CQRS et exemples d'enrichissement

## Notes
- Pattern CQRS : séparation query (Message) / handler
- Classe Urls enrichissable avec méthodes spécifiques (show, edit, delete)
- Immutabilité (readonly)
