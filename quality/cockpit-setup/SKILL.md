---
name: cockpit-setup
description: "Logique partagée des commandes du wizard (/start-cockpit, /brand-discover, /tools-setup, /modules, /validate-setup, /health-check). Centralise les vérifications préalables, la mutation du registre d'outils, le lint des placeholders, les règles de sécurité, le gate de confidentialité et le schéma de .setup-completed."
---

# cockpit-setup — skill partagée du wizard

Chaque commande du wizard charge cette skill en premier et applique ses règles avant toute logique spécifique. C'est ce qui garde le wizard cohérent entre commandes et évite la duplication.

## Invariants (à ne jamais violer)

1. **Une étape par message.** Jamais plusieurs décisions groupées. Chaque étape : expliquer, demander, attendre la confirmation, puis avancer.
2. **Aucun défaut silencieux.** Une valeur manque ? On la demande. On ne suppose jamais.
3. **Aucune écriture avant validation.** Tout artefact généré (doctrine de marque, CLAUDE.md de rôle, métadonnées de setup) : présenter le brouillon, obtenir l'accord explicite, puis écrire.
4. **Aucun secret dans les messages ou les commits.** Les secrets vont SOIT dans `.env` (scripts et connecteurs Python, chargés via dotenv), SOIT dans le `.mcp.json` local non versionné (serveurs MCP) — les deux sont gitignorés, jamais dans un fichier tracké. Rappel technique : les `${VAR}` de `.mcp.json` ne sont **pas** développées depuis le `.env` du projet (voir `SECURITY.md`). Ne jamais renvoyer un secret à l'utilisateur — lui demander de vérifier `.env` / `.mcp.json` de son côté.
5. **Toute opération destructive exige confirmation.** Suppression de fichiers, déplacements vers `.setup-archive/`, opérations git forcées, `launchctl` : « oui » explicite requis.
6. **Langue du repo : français** (le `README.md` reste en anglais, vitrine publique). Le contenu produit ensuite par le cockpit suit la langue de marque choisie au setup.
7. **Gate de confidentialité obligatoire** avant tout connecteur touchant des données clients (CRM, emailing, GA4/GSC, transcriptions `00-intel/`, scraping de personnes). Le texte canonique du gate vit dans `.claude/commands/tools-setup.md` — l'afficher, recueillir le plan Claude utilisé, et appliquer les règles associées. `/modules` le ré-applique pour `veille`, `acquisition` et `reporting`.

## Vérifications préalables (à chaque entrée dans le wizard)

À exécuter dans l'ordre, silencieusement. En cas d'échec, remonter le problème avec une suggestion de remédiation.

1. **Modèle.** Session sur Sonnet 4.6 ou mieux. Sur Haiku, avertir que la phase wizard (découverte de marque, génération d'échantillons) gagne à tourner sur Sonnet ou Opus, et proposer de continuer quand même.
2. **État git.** `git status --porcelain`. Arbre sale : demander stash, commit, ou continuer.
3. **Dépendances Python.** `python3 -c "import yaml, dotenv, requests"`. Manquantes : suggérer `pip install pyyaml python-dotenv requests`.
4. **`.env` existe.** Sinon `cp .env.example .env` et prévenir. Ne jamais lire les valeurs — présence uniquement.
5. **`.mcp.json` est bien ignoré par git.** `git check-ignore -q .mcp.json` doit réussir et `git ls-files .mcp.json` être vide. Tracké ou non ignoré = alerte immédiate (risque de commit de tokens) : proposer `git rm --cached .mcp.json` + correction du `.gitignore`. S'il n'existe pas encore et qu'un serveur MCP doit être configuré : `cp .mcp.json.example .mcp.json`.
6. **État de `.setup-completed`.** Existe déjà ? Le wizard sert au premier setup — proposer de relancer des commandes individuelles (`/tools-setup`, `/brand-discover`, `/modules`) pour reconfigurer.

## Fichiers de référence — charger au besoin

| Fichier | Quand |
|---|---|
| `docs/placeholders.json` | Remplissage ou validation de templates |
| `docs/tools.json` | `/tools-setup`, pour savoir quels connecteurs sont prêts vs stubs |
| `docs/setup-completed.schema.json` | `/validate-setup`, pour produire un `.setup-completed` conforme |
| `SECURITY.md` | Affichage préalable, avant toute étape touchant secrets ou API externes |
| `_examples/` | Corpus de démarrage si l'utilisateur n'a rien à ingérer |

## Discipline des placeholders

Le template utilise des placeholders `{{MAJUSCULES_UNDERSCORE}}` (style Mustache). La liste canonique est `docs/placeholders.json`.

Avant la fin de toute commande :
- Lancer `python3 scripts/lint-placeholders.py --paths 00-intel 01-brand 02-strategy 03-social-media 04-email 05-web-content 06-graphic-design 07-events 08-video 09-seo 10-automatisations 11-reporting 12-acquisition .claude/skills`.
- Code de sortie non nul : la commande ne peut pas conclure. Afficher la liste des placeholders restants et leurs fichiers.
- Seul `/validate-setup` bloque durement sur des placeholders résiduels — les autres commandes avertissent et peuvent continuer si l'utilisateur accepte.

## Mutation du registre d'outils

Quand `/tools-setup` enregistre un choix d'outil :
1. Lire `docs/tools.json`.
2. Mettre à jour `.setup-completed` en mémoire (l'écriture réelle se fait dans `/validate-setup`).
3. Selon `connector_status` :
   - `ready` → rien à faire, le connecteur existe.
   - `stub` → prévenir : « Pas de connecteur intégré pour cet outil. Le wizard génère un stub TODO à `_integrations/connectors/<outil>.py` — à implémenter avant le premier push. »
   - `unsupported` → refuser et lister les alternatives supportées.
4. Régénérer tout `CLAUDE.md` de rôle référençant cette catégorie d'outil : lire `_templates/role-claudemd/<role>.md`, substituer, écrire dans `<role>/CLAUDE.md`. Toujours sauvegarder la version précédente dans `.setup-archive/role-claudemd-<ISO8601>/`.

## Anti-répétition — sans base vectorielle

L'anti-répétition du cockpit repose sur le **scan de fichiers + inventaires**, pas sur une base externe :
- lecture du calendrier éditorial (`02-strategy/calendar/calendar.md`) pour les sujets déjà planifiés ou publiés ;
- scan des archives par canal (`03-social-media/*/examples/`, `04-email/newsletter/editions/`, `09-seo/articles/`) ;
- fichiers d'inventaire tenus par les skills de production (voir la skill `social-content`).

Les commandes du wizard ne configurent aucune mémoire sémantique externe.

## Rappel sécurité

Au début de chaque commande du wizard, afficher une phrase sur les attentes de sécurité pertinentes et pointer `SECURITY.md`. Exemples :

- `/start-cockpit` : « Ce wizard vous demandera des URLs et des noms d'outils. Il ne vous demandera jamais de coller une clé API dans le chat — les clés vont dans `.env` uniquement. Règles complètes : `SECURITY.md`. »
- `/tools-setup` : « Pour chaque outil, je demande le nom des variables `.env` et confirmation qu'elles sont renseignées. Je ne lis pas les valeurs. »
- `/modules` : « L'activation d'un module vérifie ses prérequis par des tests non destructifs. Aucun secret n'est lu ni affiché. »

## Écriture de `.setup-completed`

Seul `/validate-setup` écrit ce fichier (exception : `/modules` peut mettre à jour la clé `modules` après le setup initial). Forme (conforme à `docs/setup-completed.schema.json`) :

```json
{
  "version": "2.0.0",
  "completed_at": "ISO 8601",
  "company": "string",
  "company_website": "URL",
  "language": "en | fr | es | de | pt",
  "bilingual": false,
  "tools": {
    "editorial_calendar": { "name": "calendar-file|notion|airtable|custom|none", "enabled": true },
    "email_marketing":    { "name": "mailerlite|mailchimp|resend|brevo|convertkit|custom|none", "enabled": true },
    "knowledge_base":     { "name": "outline|notion|confluence|gitbook|custom|none", "enabled": false },
    "events_platform":    { "name": "livestorm|zoom|riverside|google-meet|custom|none", "enabled": false },
    "crm":                { "name": "hubspot|pipedrive|odoo|notion|airtable|custom|none", "enabled": false },
    "web_analytics":      { "name": "ga4-gsc|plausible|fathom|custom|none", "enabled": false },
    "social_publishing":  { "name": "postiz|custom|none", "enabled": false },
    "scraping":           { "name": "apify|custom|none", "enabled": false },
    "client_space_ftp":   { "name": "ftp|none", "enabled": false }
  },
  "modules": {
    "video":               { "enabled": false, "checked_at": "ISO 8601" },
    "automatisations":     { "enabled": false, "checked_at": "ISO 8601" },
    "reporting":           { "enabled": false, "checked_at": "ISO 8601" },
    "acquisition":         { "enabled": false, "checked_at": "ISO 8601" },
    "veille":              { "enabled": false, "checked_at": "ISO 8601" },
    "publication-sociale": { "enabled": false, "checked_at": "ISO 8601" },
    "espace-client":       { "enabled": false, "checked_at": "ISO 8601" }
  },
  "features": {
    "image_generation": { "enabled": true, "model": "gemini-3-pro-image-preview" }
  },
  "wizard_log": [
    { "command": "/start-cockpit",  "at": "ISO 8601" },
    { "command": "/brand-discover", "at": "ISO 8601" },
    { "command": "/tools-setup",    "at": "ISO 8601", "privacy_gate": { "acknowledged": true, "claude_plan": "team" } },
    { "command": "/modules",        "at": "ISO 8601" },
    { "command": "/validate-setup", "at": "ISO 8601" }
  ]
}
```

## Politique de réentrée

Chaque commande est idempotente. Relancer `/tools-setup` ou `/modules` doit lire l'état courant, montrer ce qui est déjà configuré, et demander quoi changer — pas repartir de zéro.

## Ce que cette skill ne fait PAS

- Elle ne produit pas de contenu marketing (→ `social-content`, `email`, `copywriting`, etc.).
- Elle n'exécute pas brand-check (→ `brand-check`).
- Elle n'appelle pas d'API externe directement — les connecteurs de `_integrations/` s'en chargent.
- Elle ne stocke aucun secret. Présence uniquement.

Les commandes du wizard restent centrées sur l'orchestration et le consentement. Les skills de production restent centrées sur la production.
