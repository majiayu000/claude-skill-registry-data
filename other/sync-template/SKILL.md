---
name: sync-template
description: Synchronise un repo client dérivé du marketing-cockpit-template avec les évolutions du template public (git fetch upstream + merge upstream/main). Diff résumé avant merge, alerte si des fichiers de marque (01-brand/, profile/) sont touchés, résolution guidée des conflits. À utiliser quand l'utilisateur veut « récupérer les nouveautés du template », « mettre à jour depuis upstream » ou « synchroniser le template ».
---

# sync-template — récupérer les évolutions du template dans un repo client

Cette skill s'exécute **dans un repo client** (fork/dérivé du template, déjà personnalisé pour {{COMPANY_NAME}}). Objectif : récupérer les améliorations de mécanique du template public **sans jamais écraser la personnalisation de marque**.

## Principe de séparation

| Catégorie | Exemples | Vient d'upstream ? |
|---|---|---|
| Mécanique | `.claude/skills/`, `.claude/commands/`, `.claude/hooks/`, `scripts/`, `_integrations/`, `docs/`, `_templates/` | ✅ Oui, c'est le but du sync |
| Marque & données client | `01-brand/`, `profile/`, `.setup-completed`, `.env`, contenus produits (`03-` à `09-`) | 🔴 **Jamais** — un commit upstream qui les touche est suspect |

## Préflight

1. Vérifier qu'on est bien dans un repo client : `.setup-completed` existe. Si absent → ce repo EST probablement le template, sync inutile ; s'arrêter.
2. `git status` — l'arbre de travail doit être propre. Sinon, demander de committer ou stasher d'abord.
3. Vérifier le remote : `git remote -v`. Si `upstream` manque, proposer :
   ```bash
   git remote add upstream <URL du template public>
   ```
   (demander l'URL à l'utilisateur, ne pas la deviner).
4. Noter la branche courante et le SHA de départ (`git rev-parse HEAD`) pour pouvoir revenir en arrière.

## Workflow

### Étape 1 — Fetch et diff résumé (AVANT tout merge)

```bash
git fetch upstream
git log --oneline HEAD..upstream/main        # commits à intégrer
git diff --stat HEAD...upstream/main         # fichiers touchés
```

Présenter à l'utilisateur un résumé lisible : nombre de commits, thèmes (nouvelles skills, fixes de scripts, docs...), liste des fichiers modifiés groupés par dossier.

### Étape 2 — Alerte fichiers de marque

Contrôler le diff entrant :

```bash
git diff --name-only HEAD...upstream/main | grep -E '^(01-brand/|profile/)' || true
```

Si des fichiers de `01-brand/` ou `profile/` apparaissent : **🔴 ALERTE bloquante**. Ces fichiers contiennent la marque du client et ne devraient jamais venir d'upstream (au pire, upstream modifie ses gabarits `_templates/brand/`, pas `01-brand/`). Expliquer le risque, et proposer :
- exclure ces chemins du merge (les restaurer depuis `HEAD` juste après le merge), **option par défaut** ;
- ou, si l'utilisateur confirme que c'est un changement de structure voulu, l'intégrer en re-personnalisant manuellement.

Ne jamais merger silencieusement un changement upstream sur ces dossiers.

### Étape 3 — Merge

Avec l'accord explicite de l'utilisateur :

```bash
git merge upstream/main
```

- **Merge propre** → passer à l'étape 5.
- **Conflits** → étape 4.

### Étape 4 — Résolution guidée des conflits

Pour chaque fichier en conflit (`git diff --name-only --diff-filter=U`), appliquer la grille :

| Fichier en conflit | Résolution recommandée |
|---|---|
| `01-brand/`, `profile/`, `.setup-completed` | **ours** (version client), toujours |
| `.claude/skills/`, `scripts/`, `_integrations/`, `docs/` | **theirs** (upstream) si le client ne l'a pas personnalisé ; sinon fusion manuelle en préservant les personnalisations |
| `CLAUDE.md` racine, `README.md` | Fusion manuelle : structure upstream + valeurs de marque client |
| Contenus `03-` à `09-` | **ours**, toujours (production client) |

Montrer chaque conflit à l'utilisateur avec la résolution proposée et sa justification ; appliquer après validation. Terminer par `git merge --continue` (jamais de `--force`, jamais de `reset --hard` sans confirmation explicite — cf. `SECURITY.md`).

### Étape 5 — Vérification après merge

1. `git diff --stat <SHA de départ>..HEAD` — récapituler ce qui a réellement changé.
2. Confirmer que `01-brand/` et `profile/` sont identiques à l'état de départ (`git diff <SHA de départ> HEAD -- 01-brand/ profile/` doit être vide, sauf choix explicite contraire).
3. Chercher des placeholders réintroduits par upstream : `grep -rn "{{" --include="*.md" .claude/ CLAUDE.md` — si des `{{...}}` apparaissent dans des fichiers censés être personnalisés, les re-remplir avec les valeurs de `.setup-completed` / `01-brand/`.
4. Si de nouvelles skills ou commandes sont arrivées, les lister à l'utilisateur avec une ligne de description.
5. Proposer un `/health-check` si le merge a touché `_integrations/`, hooks ou scripts.

## En cas de problème

Retour arrière propre (avec confirmation) : `git merge --abort` pendant le merge ; après coup, créer une branche de secours puis `git reset --keep <SHA de départ>`.

## Ce que cette skill ne fait PAS

- ❌ Remonter une amélioration client vers le template (→ `backport-to-template`, le sens inverse)
- ❌ `git push` automatique — l'utilisateur pousse lui-même après vérification
