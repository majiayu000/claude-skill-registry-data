---
name: seo-geo
description: Optimiser la visibilité de {{COMPANY_NAME}} dans les moteurs de réponse IA — Google AI Overviews, ChatGPT, Perplexity, Claude, Bing Copilot. Analyse d'accès des crawlers IA, llms.txt, citabilité des passages, signaux de mention de marque. Utiliser quand l'utilisateur dit « GEO », « AEO », « AI Overviews », « être cité par ChatGPT/Perplexity », « visibilité IA », « llms.txt » ou « citations LLM ».
---

# seo-geo — Generative Engine Optimization

Skill d'analyse GEO/AEO. La réécriture des passages pour citabilité se fait ensuite via la skill `seo` (production) avec la doctrine `01-brand/`. Adapté du plugin claude-seo (AgriciDaniel, MIT) — voir `docs/vendored-seo.md`. Les statistiques ci-dessous datent de début 2026 : re-vérifier à chaque re-sync.

## Insight central : mentions de marque > backlinks

Les mentions de marque corrèlent ~3x plus fortement avec la visibilité IA que les backlinks (étude Ahrefs déc. 2025, 75 000 marques). Signaux les plus corrélés : mentions YouTube (~0.74), Reddit, présence Wikipédia, LinkedIn. Le Domain Rating classique corrèle faiblement (~0.27).

Seuls ~11% des domaines sont cités à la fois par ChatGPT et par Google AI Overviews pour une même requête → l'optimisation par plateforme compte.

## Grille d'analyse (5 critères)

### 1. Citabilité des passages (25%)
- **Longueur optimale d'un passage citable : 134-167 mots**, auto-suffisant (extractible sans contexte)
- Réponse directe dans les 40-60 premiers mots de la section
- Faits et chiffres précis, attribués à une source
- Définitions au pattern « X est… » / « X désigne… »
- Données uniques introuvables ailleurs
- ❌ affirmations vagues, opinions non étayées, conclusions enterrées

### 2. Lisibilité structurelle (20%)
- Hiérarchie H1→H2→H3 propre ; **titres formulés en questions** (matchent les requêtes)
- Paragraphes courts (2-4 phrases) ; tableaux pour le comparatif ; listes pour le séquentiel
- 92% des citations AI Overviews viennent du top 10 Google, mais 47% de pages sous la position 5 : la sélection obéit à une logique propre

### 3. Contenu multi-modal (15%)
Texte + images pertinentes, vidéo, infographies, outils interactifs → taux de sélection nettement supérieur.

### 4. Signaux d'autorité et de marque (20%)
- Byline auteur avec titres/credentials ; dates de publication ET de mise à jour
- Citations de sources primaires ; citations d'experts attribuées
- Présence d'entité : Wikipédia/Wikidata, Reddit, YouTube, LinkedIn ; `sameAs` croisés dans le schema

### 5. Accessibilité technique (20%)
- **Les crawlers IA n'exécutent pas le JavaScript** → le contenu clé doit être dans le HTML servi (SSR)
- Accès des crawlers IA dans robots.txt ; présence et qualité de `/llms.txt`

## Crawlers IA à vérifier dans robots.txt

| Crawler | Propriétaire | Rôle |
|---|---|---|
| GPTBot / OAI-SearchBot / ChatGPT-User | OpenAI | Recherche & navigation ChatGPT |
| ClaudeBot | Anthropic | Fonctions web de Claude |
| PerplexityBot | Perplexity | Recherche Perplexity |
| Google-Extended | Google | Entraînement Gemini (distinct de Googlebot) |
| CCBot | Common Crawl | Données d'entraînement (souvent bloqué) |

**Recommandation par défaut** : autoriser GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot (visibilité) ; le blocage des crawlers d'entraînement purs (CCBot…) est un choix éditorial de {{COMPANY_NAME}} à trancher avec l'utilisateur.

## llms.txt

Fichier à la racine (`/llms.txt`) donnant aux IA un plan structuré du site :

```
# {{COMPANY_NAME}}
> [Description en une phrase]

## Pages clés
- [Titre](url) : description
## Faits clés
- [Chiffres vérifiables issus de 01-brand/messaging-framework.md]
```

Si absent : fournir un gabarit prêt à poser, alimenté par la doctrine (jamais de chiffres inventés).

## Optimisation par plateforme

| Plateforme | Sources de citation dominantes | Focus |
|---|---|---|
| Google AI Overviews | pages du top 10 (92%) | SEO classique + passages citables |
| ChatGPT | Wikipédia (~48%), Reddit | présence d'entité, sources d'autorité |
| Perplexity | Reddit (~47%), Wikipédia | validation communautaire, discussions |
| Bing Copilot | index Bing | SEO Bing, IndexNow |

## Sortie

Rapport `09-seo/audits/YYYY-MM-DD-geo-<domaine>.md` :
1. Score de préparation GEO (XX/100) + détail par critère
2. Statut des crawlers IA (autorisés/bloqués) et de llms.txt
3. Analyse de présence de marque (Wikipédia, Reddit, YouTube, LinkedIn)
4. Passages à retravailler (avec proposition de découpage 134-167 mots)
5. Top 5 des changements à plus fort impact

## Quick wins (ordre d'exécution typique)

1. Définition « Qu'est-ce que [sujet] ? » dans les 60 premiers mots
2. Blocs-réponses auto-suffisants de 134-167 mots
3. H2/H3 en forme de question
4. Chiffres sourcés (doctrine `01-brand/messaging-framework.md` ou source externe citée)
5. Dates de publication/mise à jour visibles + schema Person pour les auteurs (skill `seo-schema`)
6. Autoriser les crawlers IA clés + créer `/llms.txt`

Effort supérieur (à planifier avec `content-strategy`) : recherche originale/enquêtes propriétaires, présence Wikipédia, chaîne YouTube, outils/calculateurs uniques (voir skill `lead-magnet`).
