---
name: phpstan-resolver
description: >
  Résout automatiquement les erreurs PHPStan en analysant et corrigeant
  les problèmes de types. Boucle jusqu'à zéro erreur ou stagnation.
allowed-tools: [Task, Bash, Read, Edit, Grep, Glob, TodoWrite]
model: claude-opus-4-1-20250805
---

# PHPStan Error Resolver Skill

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

## References

- [Scripts de workflow](references/workflow-scripts.md) - Scripts bash détaillés et TodoWrite

## Error Handling

- PHPStan non trouvé → ARRÊT
- Config absente → ARRÊT
- Stagnation → ARRÊT avec rapport
- Max itérations → ARRÊT avec rapport
