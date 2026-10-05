---
name: "pr-fix-build"
description: "Applique un fix automatique (format, tests) sur une branche distante via worktree, sans toucher à la branche locale. Commit et push le résultat."
---

# PR Fix Build Skill

## Required configuration

Prérequis :
- `git` et `gh` CLI installés et authentifiés
- `node_modules` présent à la racine du repo principal (pour Prettier/ESLint)

## Available commands

### `/pr-fix-build <branch> <fix>`

Paramètres :
- `<branch>` : nom de la branche distante (ex: `presc/bugfix/ORBISBUG-38544`)
- `<fix>` *(optionnel)* : type de fix à appliquer — `format` | `tests` (ou `test`)

Exemples :
```
/pr-fix-build presc/bugfix/ORBISBUG-38544
/pr-fix-build presc/bugfix/ORBISBUG-38544 format
/pr-fix-build presc/bugfix/ORBISBUG-38544 tests
```

---

## Detailed behaviour

### Step 1 — Valider les paramètres

Vérifier que `<branch>` est fourni. Sinon :
```
❌ Paramètre <branch> manquant.
   Usage : /pr-fix-build <branch> [format|tests]
```
**Stopper.**

Si `<fix>` n'est pas fourni, demander via `ask_user` :
> "Quel type de fix veux-tu appliquer sur `<branch>` ?"
> Choix : `format` | `tests`

Si `<fix>` est fourni mais n'est pas parmi `format`, `tests`, `test` :
```
❌ Fix inconnu : "<fix>"
   Valeurs acceptées : format | tests
```
**Stopper.**

> Si `<fix>` vaut `test`, le normaliser en `tests` avant de continuer.

### Step 2 — Initialiser le contexte

```bash
MAIN_REPO=$(git rev-parse --show-toplevel)
BRANCH="<branch>"
FIX="<fix>"
WORKTREE_DIR="/tmp/fix-remote-$(echo "$BRANCH" | tr '/' '-')"
```

### Step 3 — Fetcher et créer le worktree

```bash
git fetch origin "$BRANCH"

# Nettoyer si déjà existant
git worktree remove "$WORKTREE_DIR" --force 2>/dev/null || rm -rf "$WORKTREE_DIR"

git worktree add "$WORKTREE_DIR" "origin/${BRANCH}" --no-checkout
git -C "$WORKTREE_DIR" checkout "$BRANCH"
```

Si `git fetch` échoue (branche inexistante) :
```
❌ Branche introuvable sur origin : <branch>
   Vérifier le nom de la branche avec : git branch -r | grep <branch>
```
**Stopper** (après nettoyage worktree si créé).

### Step 4 — Identifier les fichiers modifiés

Détecter la branche de base :
```bash
BASE_BRANCH=$(git -C "$WORKTREE_DIR" show-branch -a 2>/dev/null \
  | grep '\*' | grep -v "$(git -C "$WORKTREE_DIR" rev-parse --abbrev-ref HEAD)" \
  | head -1 | sed 's/.*\[\(.*\)\].*/\1/' | sed 's/[\^~].*//')

# Fallback sur develop puis main
BASE_BRANCH=${BASE_BRANCH:-develop}
```

```bash
FILES_MODIFIED=$(git -C "$WORKTREE_DIR" diff "origin/${BASE_BRANCH}...${BRANCH}" \
  --name-only | grep -E '\.(ts|html|scss)$')
```

Si aucun fichier `.ts`/`.html`/`.scss` modifié **et** `fix` ≠ `tests` :
```
ℹ️  Aucun fichier TypeScript, HTML ou SCSS modifié sur <branch> par rapport à <BASE_BRANCH>.
   → Rien à fixer.
```
**Stopper** (après nettoyage worktree).

Récupérer aussi les fichiers de test modifiés (utile pour `fix` = `tests` ou `all`) :
```bash
FILES_SPEC=$(git -C "$WORKTREE_DIR" diff "origin/${BASE_BRANCH}...${BRANCH}" \
  --name-only | grep -E '\.spec\.ts$')
```

Afficher :
```
📋 Fichiers ciblés (<N>) :
   - src/app/foo/foo.component.ts
   - src/app/bar/bar.component.html
   ...
```

### Step 5 — Appliquer le(s) fix

#### 5a. Lint & Format — ESLint + Prettier (si `fix` = `format`)

> Dans ce projet, Prettier est intégré à ESLint via `plugin:prettier/recommended`. `ng lint --fix` corrige donc les deux en un seul passage. Il n'est **pas nécessaire** d'appeler `prettier --write` séparément.

```bash
ESLINT="$MAIN_REPO/node_modules/.bin/eslint"

if [ ! -f "$ESLINT" ]; then
  echo "❌ ESLint introuvable dans $MAIN_REPO/node_modules/.bin/"
  echo "   Lance 'npm install' dans le repo principal."
  git worktree remove "$WORKTREE_DIR" --force
  exit 1
fi

cd "$WORKTREE_DIR"
$ESLINT --fix $FILES_MODIFIED
```

Après auto-fix, vérifier qu'il ne reste aucune erreur :
```bash
$ESLINT --max-warnings=0 $FILES_MODIFIED
```

Si des erreurs non auto-fixables subsistent :
```
⚠️  ESLint/Prettier — <N> erreur(s) non auto-corrigible(s) :
   📄 src/app/foo/foo.component.ts
     Ligne 42 : [<règle>] <message>
```
Continuer quand même (commit ce qui a été fixé).

Afficher :
```
🔧 ESLint + Prettier — auto-fix appliqué
```

#### 5c. Tests unitaires (si `fix` = `tests` ou `all`)

##### 5c-i. Récupérer les logs Jenkins

Tenter de trouver la PR associée à la branche :
```bash
PR_NUMBER=$(gh pr list --repo "$REPO" --head "$BRANCH" --json number --jq '.[0].number' 2>/dev/null)
```

Si une PR est trouvée, récupérer l'URL Jenkins depuis le dernier commit status :
```bash
HEAD_SHA=$(gh pr view $PR_NUMBER --repo "$REPO" --json headRefOid --jq '.headRefOid')
JENKINS_STATUS=$(gh api "repos/${REPO}/commits/${HEAD_SHA}/statuses" \
  --jq '[.[] | select(.context | startswith("continuous-integration/jenkins/pr-merge"))] | sort_by(.updated_at) | last')
TARGET_URL=$(echo "$JENKINS_STATUS" | jq -r '.target_url')
```

Extraire les logs de tests depuis Jenkins :
```bash
CONSOLE_URL="${TARGET_URL/display\/redirect/consoleText}"
TEST_LOGS=$(curl -s "$CONSOLE_URL" | grep -E "(FAILED|ERROR|Tests run:|expected|but was|NullPointer|AssertionError)" \
  | grep -v "skipped due to earlier" | tail -60)
```

Si aucune PR ou logs inaccessibles, afficher :
```
⚠️  Impossible de récupérer les logs Jenkins automatiquement.
   → Fournir l'URL console Jenkins pour continuer.
```
Demander l'URL via `ask_user`.

##### 5c-ii. Analyser et afficher le diagnostic

Classifier chaque test en échec :

| Type | Détection |
|------|-----------|
| **Assertion simple** | `expected:` / `but was:` / `AssertionError` avec valeurs claires |
| **NullPointerException** | `NullPointerException` ou `Cannot read properties of undefined` |
| **Mock manquant** | `No provider for` / `is not a function` / `spy` non configuré |
| **Compilation** | `Cannot find symbol` / `is not assignable to type` |
| **Autre** | Tout le reste |

Afficher :
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 Tests en échec — <branch>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] 📄 src/app/foo/foo.component.spec.ts
    Type   : Assertion simple
    Message: Expected 'foo' to equal 'bar'
    Ligne  : ~42
    💡 Fixable automatiquement

[2] 📄 src/app/bar/bar.service.spec.ts
    Type   : Mock manquant
    Message: No provider for BarService
    💡 Fixable automatiquement

[3] 📄 src/app/baz/baz.component.spec.ts
    Type   : Logique métier complexe
    ⚠️  Fix manuel requis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

##### 5c-iii. Proposer et appliquer le fix IA

Si au moins un test est classifié "Fixable automatiquement", demander via `ask_user` :
> "Veux-tu que je tente de fixer les <N> test(s) automatiques ? (les cas complexes seront ignorés)"

Si l'utilisateur confirme :

Pour chaque test fixable, dans le worktree :
1. Lire le fichier spec concerné avec `view`
2. Lire le fichier source associé (même nom sans `.spec`) avec `view`
3. Analyser l'erreur et produire un fix **minimal et ciblé** :
   - **Assertion simple** → corriger la valeur attendue ou la logique testée
   - **NullPointerException** → ajouter le mock ou la valeur manquante
   - **Mock manquant** → ajouter le provider dans `TestBed` ou le spy manquant
4. Appliquer avec `edit`
5. Afficher :
   ```
   ✅ Fix [<N>/<total>] — <fichier>:<ligne> — <description courte>
   ```

Pour les cas complexes, afficher :
```
⏭️  Ignoré [<N>] — <fichier> — fix manuel requis
   → Voir les logs complets : <URL Jenkins>
```

#### 5d. Prettier final pass (systématique — toujours exécuté)

Peu importe le type de `fix`, exécuter un passage Prettier final sur **tous** les fichiers modifiés (sources + specs) pour garantir qu'aucune édition (tests, eslint, etc.) n'introduit d'erreur de formatage au build.

```bash
PRETTIER="$MAIN_REPO/node_modules/.bin/prettier"

# S'assurer que PRETTIER est défini (cas fix=tests ou fix=eslint sans step 5a)
if [ ! -f "$PRETTIER" ]; then
  echo "❌ Prettier introuvable dans $MAIN_REPO/node_modules/.bin/"
  echo "   Lance 'npm install' dans le repo principal."
  git worktree remove "$WORKTREE_DIR" --force
  exit 1
fi

ALL_FILES="$FILES_MODIFIED $FILES_SPEC"
cd "$WORKTREE_DIR"
$PRETTIER --config "$MAIN_REPO/.prettierrc" --write $ALL_FILES
```

Afficher :
```
🎨 Prettier final — formatage appliqué sur <N> fichier(s)
```

### Step 6 — Committer et pusher

```bash
git -C "$WORKTREE_DIR" add .

# Vérifier qu'il y a des changements
if git -C "$WORKTREE_DIR" diff --cached --quiet; then
  echo "ℹ️  Aucun changement détecté — les fichiers sont déjà propres."
else
  # Adapter le type de commit selon le fix
  if [ "$FIX" = "tests" ]; then
    COMMIT_TYPE="test"
  else
    COMMIT_TYPE="style"
  fi

  git -C "$WORKTREE_DIR" commit -m "${COMMIT_TYPE}: fix ${FIX} on ${BRANCH}

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

  git -C "$WORKTREE_DIR" push origin "$BRANCH"
fi
```

### Step 7 — Nettoyer le worktree

```bash
cd "$MAIN_REPO"
git worktree remove "$WORKTREE_DIR" --force
```

### Step 8 — Résumé final

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ pr-fix-build — Terminé
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Branche : <branch>
Fix      : <fix>
Fichiers : <N> fichier(s) traité(s)

  ✅ Commit pushé sur origin/<branch>
     🔁 Jenkins va relancer le build automatiquement.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Ou si aucun changement :
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️  pr-fix-build — Rien à corriger
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Branche : <branch>
Fix      : <fix>
→ Les fichiers sont déjà propres.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| Paramètre `<fix>` invalide | Afficher les valeurs acceptées (`format`, `tests`) et stopper |
| Branche inexistante sur origin | Afficher l'erreur et stopper |
| `node_modules` absent | Inviter à `npm install` dans le repo principal et stopper |
| Worktree déjà existant | Le supprimer silencieusement avant de recréer |
| Aucun fichier `.ts`/`.html`/`.scss` (hors mode `tests`) | Informer et stopper proprement |
| ESLint erreurs non-fixables | Afficher les erreurs, committer ce qui a été fixé quand même |
| Logs Jenkins inaccessibles | Demander l'URL console via `ask_user` |
| Aucune PR trouvée pour la branche | Avertir, demander l'URL Jenkins manuellement |
| Tests complexes non-fixables | Les signaler et les ignorer, ne pas bloquer le reste |
| Push rejeté (branche protégée) | Afficher l'erreur git et stopper |
| Échec à n'importe quelle étape | Toujours nettoyer le worktree avant de stopper |
