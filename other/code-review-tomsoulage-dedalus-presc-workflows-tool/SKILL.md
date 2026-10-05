---
name: "code-review"
description: "Review IA du diff Angular basée sur les règles front et les leçons apprises. Met à jour .copilot/lessons.md si une nouvelle erreur bloquante est trouvée."
---

# Code Review Skill

## Required configuration

Fichiers de référence :
- `.github/instructions/frontend/front-rules.instructions.md` — règles de code front
- `.copilot/lessons.md` — erreurs passées connues

## Available commands

### `/code-review`

Analyse le diff `main...HEAD` sur les fichiers Angular et produit une review structurée.

---

## Detailed behaviour

### Step 1 — Récupérer le diff

```bash
git diff main...HEAD -- 'src/**/*.ts' 'src/**/*.html' 'src/**/*.scss'
```

### Step 2 — Charger les fichiers de référence

- Lire `.github/instructions/frontend/front-rules.instructions.md`
- Lire `.copilot/lessons.md`

Si `.github/instructions/frontend/front-rules.instructions.md` est absent, afficher `⚠️ front-rules.instructions.md introuvable — review sans règles custom.`

### Step 3 — Analyser le diff

Passer en revue chaque fichier modifié sur les axes suivants :

#### 3a. Règles front (`front-rules.md`)

Pour chaque règle du fichier, vérifier qu'elle n'est pas violée dans le diff.
Signaler toute violation avec : fichier, numéro de ligne approximatif, règle concernée.

#### 3b. DRY

- Détecter du code logiquement dupliqué entre composants ou services
- Si détecté → suggérer extraction en service partagé, pipe, ou fonction utilitaire

#### 3c. Clean code

- Méthode > 20 lignes → suggérer découpage avec proposition de noms de sous-méthodes
- Nommage peu explicite : `data`, `res`, `tmp`, `obj`, `item`, `val` → proposer un nom plus descriptif
- Logique métier dans un composant → proposer de la déplacer dans un service

#### 3d. TypeScript

- `any` explicite ou implicite → proposer le type correct ou l'interface à créer
- `as` cast sans commentaire justificatif → signaler
- Propriétés de classe déclarées sans valeur initiale ni `!` → signaler

#### 3e. Angular

- Subscription sans `takeUntilDestroyed()` ni `async` pipe → signaler
- Appel HTTP direct dans un composant → signaler
- `ChangeDetectionStrategy.OnPush` absent sur un composant présentationnel → signaler
- `Subject` exposé publiquement sans `.asObservable()` → signaler

#### 3f. Leçons connues (`lessons.md`)

Vérifier que le diff ne reproduit pas une erreur déjà listée dans `lessons.md`.

### Step 4 — Niveaux de sévérité

Chaque problème est classé :

| Niveau | Signification |
|--------|--------------|
| `[BLOQUANT]` | Viole une règle de `front-rules.instructions.md` ou reproduit une leçon connue — **doit être corrigé avant /test-implement** |
| `[SUGGESTION]` | Amélioration recommandée mais non bloquante |
| `[INFO]` | Observation sans action requise |

### Step 5 — Mettre à jour `.copilot/lessons.md`

Si une erreur `[BLOQUANT]` **nouvelle** est identifiée (non présente dans `lessons.md`) :

1. Vérifier qu'une leçon similaire n'existe pas déjà — ne pas dupliquer
2. Ajouter **une seule ligne** à la liste, au format :

```markdown
- `<TICKET>` — <règle en une phrase courte, max 120 caractères>
```

**Exemples de bonnes entrées :**
```markdown
- `PROJ-118` — Toujours utiliser `takeUntilDestroyed()` dans les composants avec subscriptions HTTP.
- `PROJ-121` — Ne jamais retourner `any` depuis un service : créer une interface dans `models/`.
- `PROJ-130` — `ChangeDetectionStrategy.OnPush` obligatoire sur tout composant présentationnel.
```

**Règles de rédaction :**
- Une ligne = une règle actionnable
- Commencer par un verbe ou une contrainte directe
- Pas de contexte, pas d'explication — juste la règle

### Step 6 — Afficher le rapport de review

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Review — <TICKET>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Résumé :
  Fichiers analysés : <N>
  [BLOQUANT]        : <N>
  [SUGGESTION]      : <N>
  [INFO]            : <N>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 Problèmes [BLOQUANT]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<fichier>:<ligne> — <description>
  → Règle : <règle front-rules.instructions.md ou leçon>
  → Correction : <suggestion concrète>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 [SUGGESTION]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<fichier>:<ligne> — <description>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️  [INFO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<observations>
```

### Step 7 — Décision finale

- Si des `[BLOQUANT]` existent → afficher :
  ```
  ⛔ Des problèmes bloquants ont été trouvés.
     Corrige-les puis relance /code-review.
  ```
- Si aucun `[BLOQUANT]` → afficher :
  ```
  ✅ Aucun bloquant. Tu peux continuer avec /test-implement.
  ```

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| `git diff` vide | Afficher `⚠️ Aucun changement détecté par rapport à main.` |
| `front-rules.instructions.md` absent | Avertir et continuer sans règles custom |
| `lessons.md` absent | Créer le fichier vide avec `# Lessons` et continuer |
