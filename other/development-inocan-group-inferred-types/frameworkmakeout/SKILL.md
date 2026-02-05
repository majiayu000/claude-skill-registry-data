---
name: framework:make:out
description: Génère classe Out (DTO immuable pour output)
license: MIT
version: 1.0.0
---

# Framework Make Out Skill

## Description
Génère une classe Out (DTO readonly) pour représenter les données de sortie d'une entité.

## Usage
```
Use skill framework:make:out
```

## Variables requises
- **{EntityName}** - Nom de l'entité en PascalCase (ex: Product)
- **{entityName}** - Nom de l'entité en camelCase (ex: product)
- **{namespace}** - Namespace du projet (défaut: App)

## Dépendances
- Entité dans `src/Entity/{EntityName}.php`

## Outputs
- `src/Out/{EntityName}Out.php`

## Workflow

1. Demander le nom de l'entité (EntityName)
2. Vérifier que l'entité existe dans `src/Entity/{EntityName}.php`
   - Si non : arrêter et demander de créer l'entité d'abord
3. Générer la classe Out depuis le template `templates/Out/`
4. Afficher le fichier créé

## Patterns appliqués

- Classe `final readonly`
- Constructeur privé
- Factory statique `new()` pour instanciation
- Propriété privée de type entité

## References

- [Usage](references/usage.md) - Exemples et usage dans l'entité

## Notes
- Couche anti-corruption entre domaine et extérieur
- Peut être enrichie avec méthodes pour propriétés calculées
- Respecte le principe d'immutabilité
