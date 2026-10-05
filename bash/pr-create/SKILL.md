---
name: "pr-create"
description: "Crée la Pull Request GitHub avec titre et body générés depuis le contexte du ticket Jira et les changements effectués."
---

# PR Create Skill

## Required configuration

Variables d'environnement requises :
- `JIRA_DOMAIN`: Jira domain (e.g. `jira.dedalus.com`)
- `JIRA_API_TOKEN`: Jira Server Personal Access Token (PAT)

Prérequis : `gh` CLI installé et authentifié.

> Si `gh` n'est pas installé : `brew install gh` (macOS) ou `winget install GitHub.cli` (Windows), puis `gh auth login`.

## Available commands

### `/pr-create`

Génère et crée la Pull Request GitHub (draft) depuis la branche courante vers `develop`.

---

## Type detection rule

**The type is inferred from the ticket prefix (extracted from the branch name):**

| Ticket prefix | Type   | Commit prefix |
|---------------|--------|---------------|
| `HORME-`      | Story  | `feat`        |
| `ORBISBUG-`   | Defect | `fix`         |

---

## PR title format

> **⚠️ IMPORTANT: The title, body and all PR comments must be written in ENGLISH.**
> **⚠️ MANDATORY: The PR title MUST end with `/fixed`. Never omit it.**

```
<COMMIT_PREFIX>(<ISSUE_KEY>): <SUMMARY> /fixed
```

| Ticket type | Example |
|-------------|---------|
| Story       | `feat(HORME-1444): add SSO SAML support /fixed` |
| Defect      | `fix(ORBISBUG-302): fix crash on login /fixed` |

---

## Detailed behaviour

### Step 0 — Vérifications préalables

```bash
source ~/.bashrc

# Vérifier gh CLI
gh --version
```

Si `gh` n'est pas disponible :
```
❌ gh CLI non installé.
   → macOS  : brew install gh
   → Windows: winget install GitHub.cli
   Puis : gh auth login
```
**Stopper.**

Récupérer le contexte :
```bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TICKET=$(echo $BRANCH | grep -oE '(HORME|ORBISBUG)-[0-9]+')
```

Déterminer le type :
```bash
if [[ "$TICKET" == HORME-* ]]; then
  COMMIT_PREFIX="feat"
elif [[ "$TICKET" == ORBISBUG-* ]]; then
  COMMIT_PREFIX="fix"
else
  echo "❌ Unknown ticket prefix. Expected: HORME-XXXX or ORBISBUG-XXXX"
  exit 1
fi
```

### Step 1 — Lire le ticket Jira (pour le summary)

```bash
RESPONSE=$(curl -s -H "Authorization: Bearer ${JIRA_API_TOKEN}" \
  -H "Accept: application/json" \
  "https://${JIRA_DOMAIN}/rest/api/2/issue/${TICKET}?fields=summary,description,${JIRA_AC_FIELD:-customfield_10028}")

SUMMARY=$(echo "$RESPONSE" | jq -r '.fields.summary')
```

### Step 2 — Générer le titre de la PR

Format : `<COMMIT_PREFIX>(<ISSUE_KEY>): <SUMMARY> /fixed`

Le résumé court est tiré du `SUMMARY` du ticket Jira.
Si le résumé fait plus de 60 caractères, le tronquer proprement (ne pas couper un mot).

Exemples :
- `feat(HORME-1444): add SSO SAML support /fixed`
- `fix(ORBISBUG-302): fix crash on login /fixed`

### Step 3 — Générer le body de la PR

```markdown
## Jira Ticket

[<ISSUE_KEY>](https://${JIRA_DOMAIN}/browse/<ISSUE_KEY>)

## Acceptance Criteria

- [ ] AC1
- [ ] AC2
- [ ] AC3

## Description

<résumé du ticket Jira en 3-5 phrases : ce qui était demandé et pourquoi>

## Changes

<liste des fichiers créés ou modifiés avec une description de ce qui a changé>
- `src/app/...` — <description>
- `src/app/...` — <description>

## Tests

<résultat du /test-implement : specs lancées et leur statut>
- ✅ <spec-name.spec.ts> — <N> tests passants
- ⚠️ <fichier.ts> — aucune spec (à créer)
```

### Step 4 — Créer la PR

```bash
# Ensure WORKFLOWS label exists
gh label create "WORKFLOWS" --color "1D76DB" --description "PR managed by Jira workflow" 2>/dev/null || true

gh pr create \
  --title "${COMMIT_PREFIX}(${TICKET}): ${SUMMARY} /fixed" \
  --body "<body généré>" \
  --base develop \
  --draft \
  --label "WORKFLOWS"
```

### Step 5 — Afficher le résultat

```
✅ Workflow complete!

🌿 Branch  : <branche-courante>
📤 Push    : origin/<branche-courante>
🔗 PR      : <PR URL>
📋 PR title: <COMMIT_PREFIX>(<TICKET>): <SUMMARY> /fixed
🏷️  Labels  : WORKFLOWS
```

---

## Error handling

| Situation | Comportement |
|-----------|-------------|
| `gh` non installé | Afficher les instructions d'installation et stopper |
| `gh` non authentifié | Afficher `gh auth login` et stopper |
| Préfixe inconnu (ni `HORME-` ni `ORBISBUG-`) | "❌ Unknown prefix. Use HORME-XXXX or ORBISBUG-XXXX" |
| Ticket non trouvé sur Jira | "❌ Ticket <KEY> not found on ${JIRA_DOMAIN}" |
| `JIRA_API_TOKEN` manquant | "❌ Configure JIRA_API_TOKEN in ~/.bashrc" |
| PR déjà existante pour cette branche | Afficher l'URL existante et stopper |
| Branche non poussée | Proposer de lancer `/code-lint` d'abord |
| `develop` n'existe pas | Fallback vers `main` |
| Label `WORKFLOWS` n'existe pas | Le créer automatiquement |
