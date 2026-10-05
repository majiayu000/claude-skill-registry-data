---
name: "code-lint"
description: "Formate avec Prettier, lint avec ESLint (auto-fix) les fichiers modifiés. Si tout est propre, propose un commit des corrections."
---

# Lint Check Skill

## Required configuration

Aucune variable d'environnement requise.

Prérequis :
- ESLint configuré dans le projet (`.eslintrc.json` ou `eslint.config.js`)
- Prettier configuré dans le projet (`.prettierrc`, `prettier.config.js`, ou config dans `package.json`)

## Available commands

### `/code-lint`

Formate avec Prettier, corrige automatiquement avec ESLint, puis propose un commit si tout est propre.

---

## Detailed behaviour

### Step 1 — Lister les fichiers modifiés à analyser

```bash
git diff main...HEAD --name-only | grep -E '\.(ts|html|scss)$'
```

Si aucun fichier `.ts`, `.html` ou `.scss` modifié, afficher :
```
ℹ️  Aucun fichier TypeScript, HTML ou SCSS modifié détecté.
```
Et stopper.

### Step 2 — Prettier : formater automatiquement

```bash
npx prettier --write <fichier1> <fichier2> ...
```

Afficher :
```
🎨 Prettier — <N> fichier(s) formaté(s)
```

> Prettier modifie les fichiers en place — les changements seront inclus dans le commit si `git add` n'a pas encore été fait. C'est intentionnel.

### Step 3 — ESLint : auto-fix puis vérification

#### 3a. Tenter de corriger automatiquement les erreurs fixables

```bash
npx eslint <fichier1> <fichier2> ... --fix
```

#### 3b. Vérifier qu'il ne reste plus rien

```bash
npx eslint <fichier1> <fichier2> ... --max-warnings=0
```

L'option `--max-warnings=0` traite les warnings comme des erreurs — zéro tolérance.

### Step 4 — Analyser les résultats

#### Si des erreurs subsistent après auto-fix

Afficher le rapport par fichier :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ ESLint — Erreurs non auto-corrigibles
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 <fichier1.ts>
  Ligne <N> : [<règle>] <message>
  Ligne <N> : [<règle>] <message>

📄 <fichier2.html>
  Ligne <N> : [<règle>] <message>

Total : <N> erreur(s), <N> warning(s)
```

Puis afficher :
```
⛔ Lint échoué. Corriger les erreurs manuellement avant de push.
   Ne pas passer à /pr-create sans avoir relancé /code-lint avec succès.
```

**Bloquer le push.**

#### Si tout est propre

Afficher :
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Prettier + ESLint — Aucune erreur
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fichiers vérifiés : <N>
```

### Step 5 — Proposer un commit (si lint OK)

Demander à l'utilisateur :
```
💾 Voulez-vous committer les corrections Prettier/ESLint ?
   Les fichiers modifiés seront ajoutés avec : git add <fichiers>
   Message de commit : chore: lint & format
   [o/n]
```

Si **oui** :
```bash
git add <fichiers modifiés>
git commit -m "chore: lint & format"
```
Afficher :
```
✅ Commit effectué.
   ➡️  Prochaine étape : /pr-create (qui effectuera le push)
```

Si **non** :
```
ℹ️  Aucun commit effectué. Les modifications restent en working tree.
```

> ⚠️ Aucun `git push` n'est jamais effectué par ce skill.

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| Prettier non installé | Afficher `⚠️ Prettier introuvable — étape de formatage ignorée.` et continuer avec ESLint |
| ESLint non installé | Afficher `❌ ESLint introuvable. Vérifier node_modules.` et stopper |
| Erreurs ESLint auto-corrigibles | Corrigées silencieusement par `--fix` |
| Erreurs ESLint non auto-corrigibles | Bloquer le push, lister par fichier et ligne |
| `git push` échoue | N/A — ce skill ne fait jamais de push |
| Aucun fichier `.ts`/`.html`/`.scss` modifié | Informer et stopper sans erreur |
