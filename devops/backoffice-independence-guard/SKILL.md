---
name: backoffice-independence-guard
description: 'Garantit que le back-office HIVMeet ne modifie jamais le fonctionnement existant de l''application. À charger AVANT toute écriture liée au back-office et en fin de chaque phase.'
argument-hint: 'Indiquer la phase du back-office en cours.'
user-invocable: true
---

# Garde d'indépendance du back-office

## Règle n°1 (exigence explicite de l'utilisateur)
Le back-office est une application **séparée**. Aucune modification ne doit pouvoir
impacter le fonctionnement actuel de l'application mobile/API : son implémentation et
son comportement restent indépendants de la gestion (le back-office).

## Zones d'écriture autorisées (et seulement elles)
- `backoffice/**`
- `docs/backoffice/**`
- `.agents/skills/backoffice-*/**` et `.claude/skills/backoffice-*/**`
- `docker-compose.backoffice.yml` (nouveau fichier)
- Ajout de lignes (jamais de suppression) dans `.agents/skills/task-router/SKILL.md`
  et `.agents/skills/BACKEND_SKILLS_CATALOG.md` (gouvernance, sans effet runtime)

**Tout le reste est en lecture seule** : `hivmeet_backend/*` (settings, urls, test_runner…),
`requirements.txt`, `Dockerfile`, `docker-compose.yml`, `env.example`, et le code, l'admin
et les migrations de `authentication`, `profiles`, `matching`, `messaging`,
`subscriptions`, `resources`, `notifications`.

## Interdits
- `python manage.py migrate` **sans label** (appliquerait des migrations de la worktree
  non liées). Utiliser `migrate backoffice --settings=backoffice.conf.settings`.
- `makemigrations` hors de l'app `backoffice`.
- `git reset`, `git checkout -- <fichier>`, `git stash`, `git clean` : la worktree contient
  des modifications de l'utilisateur à préserver.
- Ajouter `backoffice` aux `INSTALLED_APPS`/URL de `hivmeet_backend`.
- Corriger un défaut de l'application existante : le consigner dans
  `docs/backoffice/RECOMMANDATIONS_HORS_PERIMETRE.md` et laisser l'utilisateur décider.
- Nouvelle dépendance pip.

## Procédure
1. **Avant toute écriture d'une phase** : `verify` doit afficher `INDEPENDENCE: PASS`.
   Sinon, comprendre l'écart avant d'écrire (voir ci-dessous).
2. **Fin de phase** : relancer `verify` (toujours avec `PYTHONDONTWRITEBYTECODE=1` pour les
   tests, des `.pyc` étant suivis par git).
3. **En cas d'écart** : identifier l'auteur. Annuler uniquement ses propres changements.
   Si l'utilisateur a lui-même modifié l'application, le signaler dans le HANDOFF, puis
   `rebase` **seulement avec son accord explicite**.

## Commandes
```
python .agents/skills/backoffice-independence-guard/scripts/check_independence.py verify
python .agents/skills/backoffice-independence-guard/scripts/check_independence.py report   # détail complet
python .agents/skills/backoffice-independence-guard/scripts/check_independence.py snapshot  # une seule fois (refuse d'écraser)
python .agents/skills/backoffice-independence-guard/scripts/check_independence.py rebase    # accord utilisateur requis
```
La baseline vit dans `docs/backoffice/independence-baseline.json` (SHA-256 de tous les
fichiers hors zones autorisées ; ignore `.git`, `__pycache__`, `.venv`, `media`,
`staticfiles*`, `private_uploads`, `celerybeat-schedule*`, logs, `.runtime`).

## Preuve d'indépendance à fournir en fin de phase
- `verify` : PASS.
- `python manage.py check` et `makemigrations --check --dry-run` avec les settings
  **principaux** inchangés (aucune migration nouvelle côté application).
- Aucun fichier de l'application dans la liste des fichiers modifiés par la phase.
