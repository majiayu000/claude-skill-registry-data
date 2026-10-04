---
name: backport-to-template
description: Remonte une amélioration de mécanique développée dans un repo client vers le template public marketing-cockpit-template. Dé-brandification systématique (valeurs de marque → placeholders) puis checklist de sanitisation BLOQUANTE (noms clients, chiffres réels, URLs privées, emails, IDs, tokens) avant préparation de la branche et de la PR. À utiliser quand une skill, un script ou un workflow mis au point chez un client mérite d'entrer dans le template.
---

# backport-to-template — remonter une amélioration client vers le template public

Sens inverse de `sync-template` : une mécanique éprouvée chez un client (nouvelle skill, fix de script, amélioration de workflow) est **généralisée** puis proposée en PR sur le template public. Le template est public : **une seule donnée client qui fuite est une faute grave**. La sanitisation est donc bloquante, pas indicative.

## Étape 1 — Identifier la mécanique pure

1. Demander (ou identifier depuis la conversation) ce qui doit être remonté : commits précis, fichiers, ou diff.
2. Lister le contenu : `git log --oneline`, `git show --stat <sha>`, ou diff des fichiers concernés.
3. **Filtrer** : seule la mécanique remonte (logique de skill, script, hook, structure de dossier, doc générique). Est exclu d'office :
   - tout contenu produit (`03-` à `09-`),
   - tout fichier de `01-brand/`, `profile/`, `.setup-completed`, `.env*`,
   - toute config d'outil contenant des identifiants de ressources client (IDs Notion, audiences, boards).
4. Si un commit mélange mécanique et marque, ne reprendre que les hunks de mécanique (reconstruire le fichier cible à la main plutôt que cherry-pick aveugle).

## Étape 2 — Dé-brandification

Remplacer **toute valeur de marque** par le placeholder canonique. Référence : `docs/placeholders.json` du template (liste complète). Table des cas fréquents :

| Valeur trouvée dans le code client | Placeholder |
|---|---|
| Nom de l'entreprise | `{{COMPANY_NAME}}` / `{{COMPANY_SHORT_NAME}}` |
| Site web | `{{COMPANY_WEBSITE}}` |
| Positionnement, audience | `{{COMPANY_POSITIONING}}`, `{{COMPANY_AUDIENCE_SHORT}}` |
| Couleurs hex, police | `{{BRAND_COLOR_PRIMARY}}`, `{{BRAND_COLOR_ACCENT}}`, `{{BRAND_FONT_PRIMARY}}`... |
| Ton, vocabulaire | `{{BRAND_VOICE_POSITION}}`, `{{BRAND_VOCABULARY_BANNED}}`... |
| Personas nommés | `{{PERSONA_1_NAME}}`, `{{PERSONA_1_DETAILS}}` |
| Piliers, cadences | `{{PILLAR_1}}`, `{{CONTENT_CADENCE_LINKEDIN}}`... |
| Contact, interlocuteurs | `{{COMPANY_MAIN_CONTACT}}`, `{{SALES_CONTACT}}` |
| Exemples de posts/contenus réels | Réécrire des exemples **fictifs mais réalistes** (style `_examples/`) |

Si une valeur n'a pas de placeholder existant, en proposer un nouveau et **l'ajouter à `docs/placeholders.json` dans la même PR** — jamais de valeur en dur.

## Étape 3 — CHECKLIST DE SANITISATION (bloquante)

Exécuter chaque scan **sur le diff complet destiné à la PR** (fichiers ajoutés/modifiés). Adapter les motifs au contexte client (noms réels connus).

```bash
# 1. Noms de clients, de marques clientes, de personnes (compléter avec les noms réels du repo source)
grep -rniE "<nom-client>|<nom-produit>|<noms-fondateurs>" <fichiers du diff>

# 2. Tarifs et chiffres d'affaires réels (montants €/$, pourcentages business suspects)
grep -rnE "[0-9][0-9 .,]*(€|EUR|\\$|USD|k€)" <fichiers du diff>

# 3. URLs privées ou spécifiques client (domaines non génériques, staging, espaces clients)
grep -rnoE "https?://[a-zA-Z0-9./_-]+" <fichiers du diff> | grep -vE "apify\\.com|github\\.com|docs\\.|schema\\.org|example\\.com"

# 4. Emails
grep -rnE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-z]{2,}" <fichiers du diff>

# 5. IDs de ressources (Notion 32 hex, Google Drive/Sheets ~25-44 chars, Airtable app…, bases)
grep -rnE "[a-f0-9]{32}|[a-zA-Z0-9_-]{25,44}|app[a-zA-Z0-9]{14}" <fichiers du diff>

# 6. Tokens et secrets (JWT, clés API)
grep -rnE "eyJ[a-zA-Z0-9_-]{10,}|sk-[a-zA-Z0-9]|apify_api_|ghp_|gho_|xox[bap]-|AKIA[0-9A-Z]{16}|AIza[a-zA-Z0-9_-]{35}|-----BEGIN" <fichiers du diff>
```

**Règle de décision :**
- Le motif 5 génère des faux positifs (hash, slugs) : examiner chaque hit à la main.
- Tout hit **confirmé** (vraie donnée client, vraie clé, vraie URL privée) → 🔴 **REFUS de préparer la PR**. Corriger (placeholder, exemple fictif, suppression), puis **relancer la checklist complète depuis le scan 1**.
- La PR n'est préparée que quand les 6 scans sont vierges ou 100 % faux positifs justifiés un par un dans le message final.
- En cas de doute sur un hit : le traiter comme confirmé. Jamais de bénéfice du doute sur un repo public.

## Étape 4 — Branche et PR

1. Dans un clone/worktree local du **template** (pas du repo client), créer la branche :
   ```bash
   git checkout -b backport/<slug-court> origin/main
   ```
2. Appliquer les fichiers dé-brandifiés et sanitisés. Mettre à jour si nécessaire : `CLAUDE.md` racine (tableau des skills), `docs/placeholders.json`, `CHANGELOG.md`.
3. Relancer les scans de l'étape 3 sur `git diff origin/main...HEAD` (dernier filet avant publication).
4. Committer avec un message descriptif, puis préparer la PR vers `main` du template via `gh pr create`, en incluant dans le corps :
   - origine (« généralisé depuis un déploiement client », **sans nommer le client**),
   - ce que ça change pour le template,
   - la mention « Checklist de sanitisation exécutée : 6/6 scans propres ».
5. Le push et l'ouverture effective de la PR se font **après confirmation de l'utilisateur** (cf. `SECURITY.md`).

## Ce que cette skill ne fait PAS

- ❌ Descendre les évolutions du template vers un client (→ `sync-template`)
- ❌ Remonter du contenu, des exemples réels ou de la config de marque — mécanique uniquement
- ❌ Pousser ou merger sans validation humaine
