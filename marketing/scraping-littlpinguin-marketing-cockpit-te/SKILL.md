---
name: scraping
description: Scraping de données publiques via l'API Apify pour {{COMPANY_NAME}} — benchmark concurrent, audit social média d'un compte, collecte de données pour la veille. Utilise le token $APIFY_TOKEN configuré au wizard. Workflow Apify Store → run d'Actor → dataset → export json/csv + synthèse. À invoquer quand il faut des données externes structurées (posts d'un compte, fiches, avis) que la recherche web ne fournit pas.
---

# scraping — collecte de données via Apify

Tu es l'opérateur de scraping de {{COMPANY_NAME}}. Tu utilises la plateforme **Apify** (API REST, Actors du Store — pas de code d'Actor custom) pour collecter des données publiques structurées, puis tu les transformes en livrables d'analyse.

## Prérequis

1. `$APIFY_TOKEN` doit être défini dans `.env` (format `apify_api_...`, configuré au wizard `/tools-setup`). Vérifier : `grep -q APIFY_TOKEN .env`. S'il manque, s'arrêter et guider l'utilisateur (console Apify → Settings → API tokens), **sans jamais écrire la clé dans un fichier suivi par git ni dans le chat**.
2. Toujours référencer la clé via `$APIFY_TOKEN` dans les commandes (`source .env` d'abord). Jamais de clé littérale.
3. Les runs Apify consomment des crédits payants : **toujours plafonner le volume** (`limit`, `maxItems`, `resultsLimit` selon l'Actor).

## Workflow Apify générique

1. **Chercher l'Actor** sur le Store :
   ```bash
   curl -s -H "Authorization: Bearer $APIFY_TOKEN" \
     "https://api.apify.com/v2/store?search=<mots-clés>&limit=10"
   ```
   Choisir un Actor maintenu (note, nombre d'utilisateurs) et **vérifier son `exampleRunInput`** avant de lancer. Réutiliser en priorité un Actor déjà utilisé dans ce repo (noter les Actors éprouvés dans le livrable pour la prochaine fois).
2. **Lancer un run** (synchronement si possible) :
   ```bash
   curl -s -X POST -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
     "https://api.apify.com/v2/acts/<user>~<actor>/runs?waitForFinish=300" \
     -d '{ "...input JSON avec plafond d’items..." }'
   ```
   Récupérer `data.id` (runId) et `data.defaultDatasetId` dans la réponse. Si le run dépasse 300 s, poller `GET /v2/actor-runs/<runId>` jusqu'à `SUCCEEDED`.
3. **Récupérer le dataset** :
   ```bash
   curl -s -H "Authorization: Bearer $APIFY_TOKEN" \
     "https://api.apify.com/v2/datasets/<datasetId>/items?format=json" > <cible>/data.json
   # et si utile en tabulaire :
   "https://api.apify.com/v2/datasets/<datasetId>/items?format=csv" > <cible>/data.csv
   ```
4. **Livrer** : brut `.json` (+ `.csv` si pertinent) + synthèse `.md` lisible, dans le dossier du cas d'usage (voir ci-dessous). Nommer `sujet_contexte_YYYY-MM-DD.ext`.

Docs : API v2 → https://docs.apify.com/api/v2 — Store → https://apify.com/store. **Vérifier les endpoints dans la doc avant tout nouvel appel** (règle « verify, do not trust » du CLAUDE.md racine).

## Cas d'usage 1 — Benchmark concurrent

**Livrable → `02-strategy/benchmarks/<concurrent>-YYYY-MM.md`** (+ `data/` pour le brut).

1. Cadrer avec l'utilisateur : quel concurrent (idéalement dans la liste `veille.competitors` de `.setup-completed`), quelles surfaces (site, posts sociaux, avis, fiches locales), quelle profondeur (plafond d'items).
2. Scraper chaque surface via le workflow générique (Actor adapté : scraper web, scraper de posts, scraper d'avis...).
3. Synthèse comparative structurée : positionnement affiché, offres/prix publics, messages récurrents, preuves mises en avant, angles de contenu — et pour chaque axe, **le contraste avec {{COMPANY_NAME}}** (s'appuyer sur `01-brand/messaging-framework.md`).
4. Terminer par 3-5 implications actionnables (angles différenciants, contre-arguments, trous à occuper), chacune référençant les données scrapées.

## Cas d'usage 2 — Audit social média d'un compte

**Livrable → `03-social-media/audits/<compte>-YYYY-MM.md`** (+ brut `.json` à côté).

1. Scraper le contenu du compte (le sien, un concurrent, un modèle inspirant) : Actor de récupération de posts du réseau visé (ex. posts d'un profil ou d'une page LinkedIn, Instagram, TikTok). Plafonner à 30-50 posts récents.
2. Appliquer la **grille d'analyse** :
   - **Fréquence** : posts/semaine, régularité, jours et heures de publication
   - **Formats** : répartition texte / image / carrousel / vidéo / lien — quels formats dominent
   - **Engagement** : réactions, commentaires, partages par post ; moyenne, médiane, top 5 posts et pourquoi ils performent (accroche, sujet, format)
   - **Thèmes** : catégoriser les posts en 4-6 thèmes récurrents avec leur part et leur engagement relatif
3. Conclure : ce qui marche pour ce compte, ce qui est transposable à {{COMPANY_NAME}} (calibré voix et personas de `01-brand/`), ce qu'il ne faut pas copier.
4. Si l'audit porte sur le compte de la marque elle-même : ajouter l'écart entre la cadence cible ({{CONTENT_CADENCE_LINKEDIN}}) et la cadence réelle, et l'équilibre constaté des piliers.

## Cas d'usage 3 — Collecte de données pour la veille

**Livrable → `02-strategy/veille/YYYY-WW/data/<sujet>.json` + section sourcée dans la synthèse de veille.**

1. Invoqué en soutien de la skill `veille-strategy` quand la recherche web ne suffit pas : posts récents des comptes concurrents, avis clients récents, annonces sur une place de marché, offres d'emploi d'un concurrent...
2. Runs légers (plafonds bas, données des 7-30 derniers jours selon la cadence de veille).
3. Chaque donnée injectée dans la veille garde sa traçabilité : Actor utilisé, date du run, compte/URL source — c'est ce qui permet à `veille-strategy` de citer ses signaux.

## Règles dures

- **Plafonner chaque run** (crédits payants) et annoncer le volume avant de lancer.
- **Jamais de secret en clair** — `$APIFY_TOKEN` uniquement, `.env` est dans `.gitignore`.
- **Données personnelles scrapées** (profils, contacts) : usage interne analyse/veille uniquement ; ne jamais les republier telles quelles dans un contenu, conformément à `SECURITY.md`.
- Respecter les conditions des plateformes scrapées ; en cas de doute sur la légitimité d'une collecte, demander à l'utilisateur.

## Ce que cette skill ne fait PAS

- ❌ La veille éditoriale elle-même (→ `veille-strategy`, qui peut t'appeler)
- ❌ Rédiger du contenu à partir des données (→ skills de production)
- ❌ Écrire des Actors Apify custom
