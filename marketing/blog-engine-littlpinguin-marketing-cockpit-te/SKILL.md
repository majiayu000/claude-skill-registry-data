---
name: blog-engine
description: Moteur de production d'articles de blog pour {{COMPANY_NAME}} — workflow bout-en-bout (recherche → plan → rédaction → validation SEO → scoring qualité ≥ 90/100 → livraison), fact-checking avec fetch des sources citées, double optimisation Google (E-E-A-T) + citations IA (GEO/AEO), multilingue avec hreflang. Utiliser pour écrire, réécrire ou noter un article de blog. La stratégie et l'audit SEO restent dans la skill seo ; blog-engine = la production d'un article au standard publiable.
---

# blog-engine — production d'articles {{COMPANY_NAME}}

> Contenu vendorisé et condensé depuis **claude-blog** v1.9.1 d'AgriciDaniel (MIT) — voir `docs/vendored-content.md`. Le moteur d'origine compte 30 sub-skills ; cette skill en condense le workflow maître, le quality gate et le fact-checking.

Tu produis des articles de blog au standard publiable, doublement optimisés : classement Google (Core Update déc. 2025, E-E-A-T) et citations par les moteurs de réponse (ChatGPT, Perplexity, AI Overviews, Gemini). **Aucun article ne sort sans passer le quality gate (score ≥ 90/100) et le fact-checking.**

## Position dans le template

| Besoin | Qui s'en charge |
|---|---|
| Stratégie de contenu, clusters, briefs, audits SEO du site, priorisation GSC | Skill `seo` (+ plugin claude-seo pour l'analyse) |
| **Production d'un article** : recherche, rédaction, scoring, fact-check | **Cette skill** |
| Schema markup avancé, GEO/citabilité en audit | Plugin claude-seo (`seo-schema`, `seo-geo`) |
| Repurposing social de l'article | Skill `social-content` |

Workflow type : la skill `seo` fournit le brief (mot-clé, intention, angle, gaps concurrentiels) → `blog-engine` produit l'article dans `09-seo/` → le brand-check valide avant push.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant toute rédaction :

1. Charger `01-brand/checklist-pre-composition.md` — voix, anti-style-IA, typographie, réutilisation.
2. Charger `01-brand/voice.md` — position de voix, vocabulaire, interdits.

**Ne jamais produire sans.** Si un fichier manque ou contient des `{{...}}`, arrêter et lancer `/start-cockpit`. La doctrine 01-brand remplace les fichiers BRAND.md/VOICE.md du moteur d'origine : c'est elle qui fait autorité sur le ton, les interdits et le positionnement.

## Workflow bout-en-bout

1. **Parser** : sujet, plateforme cible (markdown par défaut), template de contenu (voir tableau).
2. **Rechercher** : statistiques et sources actuelles via WebSearch — sources Tier 1 (recherche primaire, données officielles), Tier 2 (grandes publications), Tier 3 (sources sectorielles réputées). **Jamais de Tier 4-5** (fermes de contenu, sites affiliés). Chaque donnée = le triplet de preuve : année dans la prose + citation inline (éditeur + titre) + URL.
3. **Structurer** : plan informé par la SERP (couvrir les gaps, pas copier les concurrents), hiérarchie H1 → H2 → H3 stricte.
4. **Rédiger** selon les 6 piliers (ci-dessous) et la doctrine 01-brand.
5. **Valider SEO** : title 50-60 caractères, meta description 150-160, mot-clé dans H1/intro/une H2, maillage interne (≥ 2-3 liens), alt text sur toutes les images, hiérarchie de titres sans saut.
6. **Scorer** (quality gate ci-dessous). Si < 90 : itérer, 3 fois maximum ; au 3ᵉ échec, livrer le diagnostic, pas le brouillon. **L'utilisateur n'est jamais le premier relecteur : les gates le sont.**
7. **Fact-checker** (protocole ci-dessous) avant la livraison finale.
8. **Livrer** dans `09-seo/` avec scorecard et notes d'amélioration, puis passer le brand-check.

## Les 6 piliers d'optimisation

| Pilier | Impact | Implémentation |
|---|---|---|
| Answer-first | Fort levier de citation IA | Chaque H2 s'ouvre sur un paragraphe de 40-60 mots, riche en données, qui répond directement |
| Données sourcées réelles | Confiance E-E-A-T | Sources Tier 1-3 uniquement, attribution inline, triplet de preuve |
| Médias visuels | Engagement + citations | Images avec alt text, graphiques variés (jamais deux fois le même type) |
| FAQ structurée | Signal de citation IA | Q/R avec réponses de 40-60 mots (+ schema FAQ si la plateforme le permet) |
| Structure extractible | Extractibilité IA | Blocs de 50-150 mots, titres-questions, hiérarchie H propre |
| Signaux de fraîcheur | 76 % des citations top | Date de mise à jour visible, `dateModified` en schema, refresh < 30 jours pour les pages clés |

## Templates de contenu (sélection auto selon l'intention)

| Template | Type | Volume |
|---|---|---|
| how-to-guide | Tutoriel pas à pas | 2 000-2 500 mots |
| listicle | Liste ordonnée | 1 500-2 000 |
| comparison | X vs Y avec matrice | 1 500-2 000 |
| case-study | Résultats réels chiffrés | 1 500-2 000 |
| pillar-page | Guide d'autorité complet | 3 000-4 000 |
| thought-leadership | Opinion avec angle contrarien | 1 500-2 500 |
| news-analysis | Analyse d'actualité | 800-1 200 |
| faq-knowledge | Base de connaissances / FAQ | 1 500-2 000 |

## Quality gate — scoring 100 points (seuil de livraison : ≥ 90)

| Catégorie | Poids | Ce qui est mesuré |
|---|---|---|
| Qualité du contenu | 30 pts | Profondeur, lisibilité (Flesch 60-70 ou équivalent FR), originalité, structure, absence de patterns IA |
| Optimisation SEO | 25 pts | Hiérarchie de titres, title, placement du mot-clé, maillage interne, meta description |
| Signaux E-E-A-T | 15 pts | Attribution d'auteur, citations de sources, indicateurs de confiance, marqueurs d'expérience |
| Éléments techniques | 15 pts | Schema, optimisation images, meta OG |
| Citabilité IA | 15 pts | Passages extractibles, format Q/R, clarté des entités |

Bandes : 90-100 publiable tel quel · 80-89 polish mineur (**ne suffit pas pour livrer ici**) · 70-79 retouches ciblées · 60-69 refonte lourde · < 60 repartir du plan.

### Règles dures (jamais transiger)

| Règle | Seuil | Action |
|---|---|---|
| Statistique fabriquée | Tolérance zéro | Chaque nombre a une source nommée |
| Longueur de paragraphe | Jamais > 150 mots | Couper ou élaguer |
| Hiérarchie de titres | Jamais de saut de niveau | H1 → H2 → H3 uniquement |
| Tier des sources | Tier 1-3 uniquement | Jamais de ferme de contenu ni de site affilié |
| Alt text | Obligatoire sur toute image | Descriptif, mot-clé naturel |
| Auto-promotion | Max 1 mention de marque | Contexte bio d'auteur uniquement |

## Fact-checking (obligatoire avant livraison)

1. **Extraire** toutes les affirmations chiffrées : nombre, pourcentage, montant, multiplicateur, source nommée — avec leur URL citée et leur emplacement.
2. **Vérifier** chaque affirmation citée : fetch de l'URL source (WebFetch), recherche de la valeur exacte, contrôle du contexte. Séquentiel, max 10 URLs par passe (le reste = SKIPPED, à vérifier en passe suivante).
3. **Scorer** : 1.0 VERIFIED (valeur exacte trouvée en contexte) · 0.7-0.9 PARAPHRASE (donnée proche, arrondi ou période différente) · 0.3-0.6 WEAK (page pertinente mais statistique invisible — dont paywall) · 0.0 NOT FOUND (la page ne contient pas la donnée ; 404 → tenter web.archive.org) · N/A UNVERIFIED (pas d'URL : proposer une requête de recherche).
4. **Corriger** : toute affirmation < 0.7 est remplacée, resourcée ou supprimée avant livraison. Un article ne part jamais avec un NOT FOUND.

Rapport : tableau claim / URL / score / statut / note, + actions recommandées.

## Multilingue et hreflang (si publication internationale)

- Traduire en préservant le format (frontmatter, liens, schema) et en réoptimisant le SEO par langue (mot-clé cible local, pas de traduction littérale du title).
- Localiser culturellement (exemples, devises, références réglementaires) — pas seulement traduire.
- Émettre les annotations **hreflang réciproques** : chaque version liste toutes les autres + `x-default` ; toute paire non réciproque est ignorée par Google.
- QA multilingue : complétude (toutes les sections traduites), parité des liens internes, fraîcheur alignée entre versions.

## Règles état de l'art (2026)

Voir `docs/etat-de-lart/contenu-aeo.md` pour le détail sourcé :

1. **Answer-first** : la réponse directe dans les 40-75 premiers mots sous chaque H2, en bloc déclaratif autonome — les pages structurées ainsi (titres propres, paragraphes courts, tableaux) sont citées 2 à 4× plus par les moteurs IA.
2. **Statistiques + sources nommées + citations d'experts** dans chaque section : jusqu'à ~+40 % de visibilité dans les réponses génératives (étude Princeton GEO).
3. **Format Q&R quand la requête s'y prête** (+25 % de citations), avec schema FAQPage/Article ; tableaux et listes pour toute comparaison.
4. **Bannir le ton promotionnel du contenu informatif** (−26 % de citations) — séparer strictement pages de vente et contenu citable.
5. **Couche éditoriale humaine obligatoire après tout draft assisté par IA** (données propriétaires, exemples vécus, voix de marque) : le contenu IA non supervisé est la cible explicite des spam updates Google 2025.

## Après livraison

- Mettre à jour l'entrée du calendrier éditorial (`02-strategy/calendar/calendar.md`) dans le même tour : statut + lien du livrable (`09-seo/articles/...`).
- Indexer l'article dans `_templates/inventory.md` (skill `inventory`, mode incrément) — mécanisme anti-répétition de référence du repo.

## Anti-patterns (jamais)

- Fabriquer une statistique (pénalisé depuis le Core Update déc. 2025)
- Enterrer la réponse en fin de paragraphe (les moteurs IA extraient les ouvertures de section)
- Bourrer les titres de mots-clés ; sauter la vérification des sources ; produire sans recherche préalable (le contenu-consensus généré est pénalisé)
- Style IA : les patterns listés dans `01-brand/checklist-pre-composition.md` (règle de trois, méta-commentaire, emphase gonflée) font échouer le score « Qualité du contenu »
