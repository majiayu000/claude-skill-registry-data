---
name: git-pr-core
description: >
  Skill interne fournissant les scripts communs pour la création de Pull Requests.
  Ne pas appeler directement - utilisé par git-pr et git-cd-pr.
allowed-tools: [Bash, Read, Write, TodoWrite, AskUserQuestion]
model: claude-sonnet-4-5-20250929
---

# Git PR Core (Internal)

Ce skill fournit les scripts partagés pour la création de PR. Il ne doit pas être appelé directement.

## Scripts disponibles

| Script | Description |
|--------|-------------|
| `check_scopes.sh` | Vérifie les scopes GitHub |
| `verify_pr_template.sh` | Vérifie le template PR |
| `smart_qa.sh` | Lance la QA intelligente |
| `analyze_changes.sh` | Analyse les changements git |
| `confirm_base_branch.py` | Confirme la branche de base |
| `create_pr.sh` | Crée la PR (push + gh pr create) |
| `safe_push_pr.sh` | Push sécurisé avec création PR |
| `assign_milestone.py` | Assigne un milestone |
| `assign_project.py` | Assigne un projet GitHub |
| `auto_review.sh` | Lance la code review automatique |
| `cleanup_branch.sh` | Nettoie la branche locale |
| `final_report.sh` | Génère le rapport final |

## Usage par les skills enfants

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/git-pr-core/scripts"

# Exemple d'utilisation
bash "$CORE_SCRIPTS/check_scopes.sh"
bash "$CORE_SCRIPTS/create_pr.sh" "$BRANCH_BASE" "$PR_TEMPLATE_PATH"
```

## Workflow standard

1. `check_scopes.sh` - Vérifier scopes GitHub
2. `verify_pr_template.sh` - Vérifier template PR
3. `smart_qa.sh` - Lancer QA
4. `analyze_changes.sh` - Analyser changements
5. `confirm_base_branch.py` - Confirmer branche base
6. `create_pr.sh` - Créer la PR
7. `assign_milestone.py` - Assigner milestone
8. `assign_project.py` - Assigner projet
9. `auto_review.sh` - Code review
10. `cleanup_branch.sh` - Nettoyage
