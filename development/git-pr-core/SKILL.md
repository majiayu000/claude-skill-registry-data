---
name: git-pr-core
description: >
  Skill interne fournissant les scripts communs pour la création de Pull Requests.
  Ne pas appeler directement - utilisé par git-pr et git-cd-pr.
allowed-tools: [Bash, Read, Write, AskUserQuestion]
model: claude-sonnet-4-5-20250929
---

# Git PR Core (Internal)

## Instructions à Exécuter

**IMPORTANT : Exécute ce workflow étape par étape :**


Ce skill fournit les scripts partagés pour la création de PR. Il ne doit pas être appelé directement.

## Scripts disponibles

| Script | Description | Usage |
|--------|-------------|-------|
| `check_scopes.sh` | Vérifie les scopes GitHub | `bash "$CORE_SCRIPTS/check_scopes.sh"` |
| `verify_pr_template.sh` | Vérifie le template PR | `bash "$CORE_SCRIPTS/verify_pr_template.sh" "$PR_TEMPLATE_PATH"` |
| `smart_qa.sh` | Lance la QA intelligente | `bash "$CORE_SCRIPTS/smart_qa.sh"` |
| `analyze_changes.sh` | Analyse les changements git | `bash "$CORE_SCRIPTS/analyze_changes.sh"` |
| `confirm_base_branch.py` | Confirme la branche de base | `python3 "$CORE_SCRIPTS/confirm_base_branch.py"` |
| `create_pr.sh` | Crée la PR (push + gh pr create) | `bash "$CORE_SCRIPTS/create_pr.sh" "$BRANCH_BASE" "$PR_TEMPLATE_PATH"` |
| `safe_push_pr.sh` | Push sécurisé avec création PR | `bash "$CORE_SCRIPTS/safe_push_pr.sh"` |
| `assign_milestone.py` | Assigne un milestone | `python3 "$CORE_SCRIPTS/assign_milestone.py" <pr_number> --milestone "<milestone_name>"` |
| `assign_project.py` | Assigne un projet GitHub | `python3 "$CORE_SCRIPTS/assign_project.py" <pr_number> --project "<project_name>"` |
| `auto_review.sh` | Lance la code review automatique | `bash "$CORE_SCRIPTS/auto_review.sh" <pr_number>` |
| `cleanup_branch.sh` | Nettoie la branche locale | `bash "$CORE_SCRIPTS/cleanup_branch.sh" [--delete]` |
| `final_report.sh` | Génère le rapport final | `bash "$CORE_SCRIPTS/final_report.sh"` |

## Usage par les skills enfants

```bash
CORE_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/git-pr-core/scripts"

# Exemples d'utilisation
bash "$CORE_SCRIPTS/check_scopes.sh"
bash "$CORE_SCRIPTS/create_pr.sh" "$BRANCH_BASE" "$PR_TEMPLATE_PATH"

# IMPORTANT : Pour assign_milestone.py et assign_project.py, utiliser --milestone et --project
# ❌ INCORRECT : python3 "$CORE_SCRIPTS/assign_milestone.py" 1234 "Continuous Delivery"
# ✅ CORRECT   : python3 "$CORE_SCRIPTS/assign_milestone.py" 1234 --milestone "Continuous Delivery"

PR_NUMBER=$(gh pr view --json number -q .number)
python3 "$CORE_SCRIPTS/assign_milestone.py" "$PR_NUMBER" --milestone "Continuous Delivery"
python3 "$CORE_SCRIPTS/assign_project.py" "$PR_NUMBER" --project "MyProject"
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
