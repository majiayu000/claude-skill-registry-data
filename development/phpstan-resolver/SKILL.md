---
name: phpstan-resolver
description: >
  Résout automatiquement les erreurs PHPStan en analysant et corrigeant
  les problèmes de types. Boucle jusqu'à zéro erreur ou stagnation.
allowed-tools: [Task, Bash, Read, Edit, Grep, Glob]
model: claude-opus-4-1-20250805
---

# PHPStan Error Resolver Skill

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


## Usage
```
/qa:phpstan
```

## Configuration

```bash
PHPSTAN_BIN="./vendor/bin/phpstan"
PHPSTAN_CONFIG="phpstan.neon"  # ou phpstan.neon.dist
ERROR_BATCH_SIZE=5
MAX_ITERATIONS=10
```

## Workflow

### Initialisation

**Créer les tâches du workflow :**

Utiliser `TaskCreate` pour chaque phase :

```
TaskCreate #1: Vérifier environnement PHPStan
TaskCreate #2: Exécuter analyse initiale (--error-format=json)
TaskCreate #3: Grouper erreurs par fichier
TaskCreate #4: Boucle de résolution (max 10 itérations)
TaskCreate #5: Générer rapport final
```

**Important :**
- Utiliser `activeForm` (ex: "Vérifiant environnement PHPStan", "Résolvant erreurs")
- La tâche #4 peut prendre du temps (boucle jusqu'à 10 itérations)
- Chaque tâche doit être marquée `in_progress` puis `completed`

**Pattern d'exécution pour chaque étape :**
1. `TaskUpdate` → tâche en `in_progress`
2. Exécuter l'étape
3. `TaskUpdate` → tâche en `completed`

**Spécial pour la boucle de résolution (tâche #4) :**
- Marquer en `in_progress` au début de la boucle
- Ne marquer en `completed` qu'à la fin (0 erreur, stagnation, ou max itérations)
- Le statut reste `in_progress` pendant toutes les itérations

### Étapes

1. Vérifier environnement PHPStan
2. Exécuter analyse initiale (`--error-format=json`)
3. Grouper erreurs par fichier
4. Boucle de résolution :
   - Déléguer corrections à `@phpstan-error-resolver`
   - Re-exécuter PHPStan
   - Répéter jusqu'à 0 erreur ou stagnation
5. Générer rapport final

## Délégation

Utilise l'agent `@phpstan-error-resolver` pour les corrections :
- Batch de 5 erreurs par fichier par itération
- Maximum 10 itérations

## Rapport

```yaml
details:
  total_errors_initial: X
  total_errors_final: Y
  errors_fixed: Z
  success_rate: "X%"
  iterations: N
```

## Task Management

**Progression du workflow :**
- 5 tâches créées à l'initialisation
- La tâche #4 (boucle) reste `in_progress` pendant toutes les itérations
- Chaque tâche suit le pattern : `in_progress` → exécution → `completed`
- Utiliser `TaskList` pour voir la progression (notamment pour la boucle longue)
- Les tâches permettent à l'utilisateur de suivre la résolution progressive des erreurs

## References

- [Scripts de workflow](references/workflow-scripts.md) - Scripts bash détaillés

## Error Handling

- PHPStan non trouvé → ARRÊT
- Config absente → ARRÊT
- Stagnation → ARRÊT avec rapport
- Max itérations → ARRÊT avec rapport
