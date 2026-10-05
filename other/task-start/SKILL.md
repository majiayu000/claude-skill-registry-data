---
name: "task-start"
description: "Initialise le contexte de travail pour un ticket Jira : création de branche, puis appel à /task-analyze pour l'analyse approfondie"
---

# Task Start Skill

## Required configuration

Variables d'environnement requises (dans `~/.bashrc`) :
- `JIRA_DOMAIN`: domaine Jira (e.g. `jira.dedalus.com`)
- `JIRA_API_TOKEN`: Jira Server Personal Access Token (PAT)

> Toujours exécuter `source ~/.bashrc` avant toute action pour charger les variables.

## Available commands

### `/task-start <TICKET>`

Initialise le contexte de travail pour un ticket Jira donné.

---

## Detailed behaviour

### Step 0 — Validation des variables d'environnement

```bash
source ~/.bashrc
```

Vérifier que `JIRA_DOMAIN` et `JIRA_API_TOKEN` sont définis.

Si l'une est manquante, afficher :
```
❌ Variables d'environnement manquantes :
   - JIRA_DOMAIN    (ex: jira.dedalus.com)
   - JIRA_API_TOKEN (Jira Server PAT)
Définis-les dans ~/.bashrc puis relance source ~/.bashrc.
```
Et **stopper l'exécution**.

### Step 1 — Détection du type et récupération du summary

Détecter le type depuis le préfixe du ticket :

| Préfixe du ticket | Type    | Préfixe de branche       |
|-------------------|---------|--------------------------|
| `HORME-`          | Story   | `main/presc/feature/`    |
| `ORBISBUG-`       | Defect  | `main/presc/bugfix/`     |

Si le préfixe est inconnu → afficher `❌ Préfixe inconnu. Attendu : HORME-XXXX ou ORBISBUG-XXXX` et stopper.

Récupérer uniquement le summary du ticket :

```bash
source ~/.bashrc

curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" \
  -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/<TICKET>?fields=summary"
```

Extraire `SUMMARY` = `fields.summary`.

### Step 2 — Vérifier l'état du repo et créer la branche git

#### 2a. Vérifier que le working directory est propre

```bash
git status --porcelain
```

Si des fichiers modifiés ou non commités sont détectés, afficher :
```
⚠️  Des changements non commités ont été détectés :
   <liste des fichiers>

   Options :
   → Commite ou stash tes changements avant de continuer.
   → Ou réponds "force" pour créer la branche quand même.
```

**Stopper et attendre une réponse explicite.** Ne pas continuer automatiquement.

#### 2b. Déterminer le nom de la branche

Convention de nommage :
- **HORME-** (Story)  → `main/presc/feature/<TICKET>`
- **ORBISBUG-** (Defect) → `main/presc/bugfix/<TICKET>`

#### 2c. Vérifier si la branche existe déjà

```bash
# Vérifier en local
git branch --list "<branch_name>"

# Vérifier sur le remote
git ls-remote --heads origin "<branch_name>"
```

**Cas 1 — Branche inexistante (local et remote)** : créer et basculer.
```bash
git checkout -b <branch_name>
```
```
✅ Branche créée : <branch_name>
```

**Cas 2 — Branche existante en local uniquement** : basculer dessus sans recréer.
```bash
git checkout <branch_name>
```
```
ℹ️  Branche locale existante détectée. Bascule sur : <branch_name>
```

**Cas 3 — Branche existante sur le remote** : récupérer et basculer.
```bash
git fetch origin <branch_name>
git checkout -b <branch_name> origin/<branch_name>
```
```
ℹ️  Branche remote existante détectée. Récupérée depuis origin et bascule sur : <branch_name>
```

**Cas 4 — Branche existante en local ET remote avec divergence** : afficher un avertissement.
```
⚠️  La branche <branch_name> existe localement et sur le remote avec des divergences.
   → Réponds "local" pour garder la version locale
   → Réponds "remote" pour écraser avec la version remote
```
**Attendre une réponse explicite avant de continuer.**

### Step 3 — Appeler /task-analyze

Exécuter le skill `/task-analyze <TICKET>` pour effectuer l'analyse approfondie :
- Lecture complète du ticket (description, AC, liens, attachments)
- Fetch des linked issues et documentation Confluence
- Investigation du codebase
- Génération des hypothèses de fix / hints d'implémentation
- Sauvegarde de l'ANALYZE.md

### Step 4 — Demander validation humaine

Terminer par :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✋ Ce plan te convient-il ?
   → Réponds "ok" pour lancer /task-implement
   → Ou précise les ajustements à apporter
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ne pas continuer avant validation explicite.**

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| Variable d'env manquante | Afficher les variables requises et stopper |
| Préfixe de ticket inconnu | Afficher l'erreur et stopper |
| Ticket introuvable (404) | Afficher `❌ Ticket <TICKET> introuvable sur ${JIRA_DOMAIN}` et stopper |
| Working directory non propre | Lister les fichiers et attendre "force" ou correction |
| Branche déjà en local | Basculer sans recréer, afficher `ℹ️` |
| Branche déjà sur le remote | Fetch + checkout, afficher `ℹ️` |
| Divergence local/remote | Demander "local" ou "remote" et attendre réponse |
| `git checkout` échoue | Afficher l'erreur git et stopper |
| `/task-analyze` échoue | Afficher l'erreur et stopper |
