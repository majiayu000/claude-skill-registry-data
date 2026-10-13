---
name: seo
description: Production SEO pour {{COMPANY_NAME}} — briefs de contenu, articles longs, clusters thématiques, optimisation on-page et AEO (citations LLM), dans 09-seo/. L'analyse (audits techniques, SERP, mots-clés, GEO) est déléguée aux skills internes seo-audit / seo-schema / seo-geo / seo-cluster et aux agents seo-technical / seo-content / seo-google. Couplage Google Search Console / GA4 configuré via /tools-setup.
---

# seo — production blog & SEO {{COMPANY_NAME}}

Tu pilotes la stratégie de contenu long-format et sa production, optimisée pour les moteurs de recherche (Google) et les moteurs de réponse (ChatGPT, Claude, Perplexity, Gemini).

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant de rédiger un brief ou un article :

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie, assets, réutilisation.
2. Charger `01-brand/voice.md` — position de voix, vocabulaire, interdits.

**Ne jamais produire sans.** Si l'un des deux fichiers manque ou contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`. Les articles SEO sont le format le plus exposé au style IA (règle de trois, méta-commentaire, emphase gonflée) : le filtre anti-style-IA conditionne aussi la citabilité par les LLM.

## Division du travail — analyse vs production

**Cette skill produit. Elle n'audite pas.** L'analyse s'appuie sur les skills et agents **internes au template** (vendorés depuis claude-seo d'AgriciDaniel, MIT — voir `docs/vendored-seo.md`) :

| Besoin d'analyse | Déléguer à |
|---|---|
| Audit complet du site ou analyse d'une page unique | skill `seo-audit` |
| Technique : crawl, indexation, CWV, rendu JS | agent `seo-technical` (dispatché par `seo-audit`) |
| Qualité de contenu, E-E-A-T, contenu mince, citabilité IA | agent `seo-content` |
| Clustering sémantique, architecture hub-and-spoke | skill `seo-cluster` |
| Schema markup, données structurées | skill `seo-schema` |
| GEO / AI Overviews / citations LLM / llms.txt | skill `seo-geo` |
| Données terrain CrUX, GSC, GA4 | agent `seo-google` (si couplage `/tools-setup` actif) |

Workflow type : lancer l'analyse via ces skills/agents → récupérer les conclusions (mots-clés, intentions, gaps, structure recommandée) → **produire** ici (briefs, articles, clusters) dans `09-seo/`.

Besoins non couverts en interne (backlinks multi-sources, pages concurrentes, dérive/baselines, SEO local, e-commerce) : installer le plugin `claude-seo` complet en complément — les skills internes restent prioritaires (règle du CLAUDE.md racine).

## Données de performance — GSC / GA4

Le couplage **Google Search Console + GA4** se configure via `/tools-setup`. Une fois actif :

- Prioriser les sujets d'après les requêtes réelles (impressions sans clic = opportunité de brief).
- Alimenter le cycle de refresh (article > 6 mois avec positions en baisse → mise à jour prioritaire).
- Vérifier l'indexation des articles publiés.

Si le couplage n'est pas configuré, le signaler à l'utilisateur et travailler à partir des clusters et des personas.

## Préflight production (après l'étape 0)

1. Lire `09-seo/CLAUDE.md` — workflow complet, clusters, frontmatter.
2. Lire `01-brand/messaging-framework.md` — chiffres et affirmations utilisables.
3. **Anti-répétition** : scanner `09-seo/articles/` pour recouvrement de sujet, consulter `_templates/inventory.md`, et vérifier les positions déjà établies dans `01-brand/messaging-framework.md`.
4. **Règle critique** : chaque affirmation factuelle de l'article est adossée à un chiffre de la doctrine ou à une source externe citée. Les moteurs (classiques et LLM) pénalisent le contenu non sourcé.

## Clusters thématiques

{{SEO_CLUSTERS}}

## Workflow de production en 7 étapes

### 1. Recherche de mots-clés (via skills internes)

- Identifier le cluster cible (le construire au besoin via la skill `seo-cluster`).
- Déléguer la collecte (SERP top 10, recouvrements, questions des personas, intentions) à `seo-cluster` ; les données terrain (requêtes GSC réelles) à l'agent `seo-google` si le couplage est actif.
- Consigner dans `09-seo/keyword-research/<cluster>/YYYY-MM-<sujet>.md`.

### 2. Brief de contenu

Fichier `09-seo/content-briefs/brief-<slug>.md` avec :
- Mot-clé principal + secondaires (3-5)
- Intention de recherche (informationnelle / commerciale / transactionnelle)
- Structure proposée (H1, H2, H3)
- Sources à intégrer (doctrine, données externes, conclusions des skills/agents seo-*)
- CTA principal
- Persona cible
- Longueur cible (1500-2500 mots typique)

### 3. Rédaction

- Suivre le brief et la doctrine de voix (étape 0).
- Intégrer données et citations de l'étape 1.
- Fichier `09-seo/articles/YYYY-MM-DD-<slug>.md`, frontmatter complet (modèle ci-dessous).

### 4. On-page SEO

- Title tag : < 60 caractères, mot-clé en tête
- Meta description : < 155 caractères, CTA implicite
- Slug : court, minuscules, mot-clé
- H1 unique ; H2 avec variantes du mot-clé
- Maillage interne : minimum 3 liens vers d'autres pages `{{COMPANY_WEBSITE}}`
- Images : alt descriptif, noms de fichiers avec mot-clé
- Schema markup : Article, FAQ (si pertinent), Organization — génération et validation via la skill `seo-schema`

### 5. AEO (Answer Engine Optimization)

Pour être cité par ChatGPT, Perplexity, Claude, Gemini :
- Réponse factuelle en début de paragraphe
- Balisage sémantique clair (H2 = question, paragraphe = réponse)
- Sources citées avec liens
- Chiffres précis et sourcés
- Aucune formulation floue qu'un LLM ne peut pas reformater proprement
- Audit de citabilité : skill `seo-geo`

### 6. Brand-check (obligatoire)

Invoquer `brand-check` avant toute publication.

### 7. Publication

- Push vers {{BLOG_CMS}} — dry-run d'abord : `python3 scripts/dry-run-push.py --target {{BLOG_CMS}} --file <article>`.
- Ajouter images et meta tags dans le CMS.
- Configurer catégories et tags.
- Soumettre à Google Search Console (via le couplage `/tools-setup` si actif).
- Mettre à jour le statut dans le calendrier éditorial.

## Frontmatter d'article

```yaml
---
title: "Titre de l'article"
slug: slug-article
date: YYYY-MM-DD
author: {{COMPANY_NAME}}
category: [pilier]
tags: [tag1, tag2, tag3]
keyword_primary: "mot-clé principal"
keywords_secondary: ["kw2", "kw3", "kw4"]
meta_title: "..."
meta_description: "155 caractères max"
status: draft | review | published
language: en | fr
word_count: XXXX
cluster: "..."
---
```

## Règles SEO

### Contenu
- Data d'abord : ≥ 3 chiffres sourcés par article
- Pas de keyword stuffing — densité naturelle
- Maillage interne : ≥ 3 liens par article
- Liens externes : 1-2 sources d'autorité
- Refresh : revisiter tous les 6 mois (prioriser via GSC si couplé)

### Jamais
- Contenu IA générique sans valeur spécifique {{COMPANY_NAME}} (cf. filtre anti-style-IA de l'étape 0)
- Articles sous 800 mots
- Duplication inter-langues (adaptation culturelle, pas traduction mécanique)
- Link-building artificiel

## Règles état de l'art AEO/GEO (2026)

Voir `docs/etat-de-lart/contenu-aeo.md` pour le détail sourcé :

1. **Answer-first systématique** : sous chaque H2, ouvrir par un paragraphe autonome de 40-75 mots qui répond entièrement à la question du titre (sujet explicite, extractible sans contexte) — les pages structurées ainsi sont citées 2 à 4× plus par les moteurs IA.
2. **Chaque affirmation clé = chiffre daté + source nommée** (+ citation d'expert si possible) : levier GEO mesuré le plus fort (~+40 % de visibilité IA). Tableau comparatif obligatoire pour les intents comparatifs ; schema FAQPage/Article dans la checklist de livraison.
3. **Dé-prioriser l'informationnel générique** dans la sélection de mots-clés (CTR ÷2 à ÷4 par les AI Overviews) au profit du transactionnel, comparatif, local et marque — documenter l'arbitrage auprès de l'utilisateur.
4. **Ne jamais recommander llms.txt par défaut** : Google confirme l'absence d'implémentation et aucun moteur ne déclare l'utiliser. Le proposer uniquement sur demande explicite.
5. **Vérifier l'indexation Bing en plus de Google** : 87 % des citations ChatGPT correspondent au top organique Bing — prérequis de la citabilité.
6. **Alimenter les briefs avec la veille** : pages comparateur/alternatives déclenchées par les changements pricing concurrents, clusters sur les angles non couverts (voir `docs/etat-de-lart/veille-intelligence.md`).

## Personnalisation par marque

{{SEO_SPECIFIC_RULES}}

## Skills associées

- `seo-audit` / `seo-schema` / `seo-geo` / `seo-cluster` (internes) — audits et analyses (technique, contenu, clusters, schema, GEO) ; agents `seo-technical`, `seo-content`, `seo-google`
- `copywriting` — rédaction narrative
- `copy-editing` — relecture 7 passes orientée SEO
- `content-strategy` — planification globale
- `image-generation` — visuels d'article
- `brand-check` — validation finale obligatoire
