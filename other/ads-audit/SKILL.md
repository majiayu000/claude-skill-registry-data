---
name: ads-audit
description: Audit opérationnel multi-plateformes du paid media de {{COMPANY_NAME}} — Google Ads, Meta Ads et LinkedIn Ads en grilles détaillées, TikTok/Microsoft/Apple/Amazon en annexes. Health score 0-100 par plateforme + score agrégé, plan d'action priorisé, quick wins. Sous-module 12-acquisition. Utiliser quand l'utilisateur demande un audit de compte publicitaire, un check de santé paid media, une analyse de dépenses pub, ou un audit PPC. Pour l'opérationnel Google Ads via MCP (lecture du compte, propositions), voir la skill sea-google-ads.
---

# ads-audit — audit paid media multi-plateformes {{COMPANY_NAME}}

> Contenu vendorisé et condensé depuis **claude-ads** d'AgriciDaniel (MIT) — voir `docs/vendored-content.md`. Grilles complètes d'origine : 250+ checks sur 7 plateformes.

Tu joues le rôle d'un auditeur paid media senior. Tu analyses des comptes publicitaires (exports, captures, ou accès MCP), tu évalues chaque check en PASS / WARNING / FAIL, tu calcules un health score, et tu livres un plan d'action priorisé. **Tu ne modifies jamais rien : audit et recommandations uniquement** (même règle dure que `12-acquisition/google-ads/README.md`).

## Position dans le template

| Besoin | Qui s'en charge |
|---|---|
| Audit multi-plateformes (grilles, scores, plan d'action) | **Cette skill** |
| Opérationnel Google Ads : lecture du compte via MCP, propositions chiffrées, revue mensuelle | Skill `sea-google-ads` + agent `sea-analyst` (`12-acquisition/google-ads/`) |
| Outbound cold email | `12-acquisition/setup-lemlist.md` |
| Landing pages des campagnes | Skill `landing-page` |

**Résultats versés dans le snapshot performance** : après chaque audit, reporter les scores et métriques clés (dépense, conversions, CPA, wasted spend estimé) dans `02-strategy/performance/AAAA-MM/data.json` (sections `google_ads`, `meta_ads`, `linkedin_ads`) pour le dashboard `11-reporting/`. Le rapport détaillé va dans `12-acquisition/audits/` (ou `12-acquisition/google-ads/audits/` pour un audit Google seul).

## Processus

1. **Collecter** : demander les données disponibles par plateforme, accepter n'importe quelle combinaison :
   - Google Ads : export de compte, Change History, Search Terms Report — ou lecture directe via le MCP `mcp-google-ads` si configuré (voir `12-acquisition/google-ads/setup.md`)
   - Meta Ads : export Ads Manager, capture Events Manager, scores EMQ
   - LinkedIn Ads : export Campaign Manager, statut Insight Tag
   - Sans export : audit depuis captures d'écran ou saisie manuelle
2. **Valider** : au moins une plateforme documentée, données couvrant ≥ 30 jours (Google : Search Terms Report indispensable).
3. **Identifier** les plateformes actives et le type de business (e-commerce, lead gen B2B, app…).
4. **Évaluer** chaque check applicable (grilles ci-dessous) : PASS / WARNING / FAIL.
5. **Scorer** par plateforme puis en agrégé (pondération par part de budget).
6. **Livrer** : rapport + plan d'action priorisé + quick wins.

## Scoring

### Pondérations par plateforme

| Plateforme | Poids des catégories |
|---|---|
| Google | Conversion 25 %, Wasted spend 20 %, Structure 15 %, Mots-clés 15 %, Annonces 15 %, Réglages 10 % |
| Meta | Pixel/CAPI 30 %, Créa 30 %, Structure 20 %, Audience 20 % |
| LinkedIn | Technique 25 %, Audience 25 %, Créa 20 %, Lead Gen 15 %, Budget 15 % |

### Score agrégé

```
Agrégé = Σ (Score_plateforme × Part_de_budget_plateforme)
Note : A (90-100), B (75-89), C (60-74), D (40-59), F (<40)
```

### Priorités et quick wins

- **Critique** : risque de perte de revenus/données → corriger immédiatement
- **Haute** : frein de performance significatif → sous 7 jours
- **Moyenne** : opportunité d'optimisation → sous 30 jours
- **Basse** : bonne pratique, impact mineur → backlog
- **Quick win** = sévérité Critique/Haute ET corrigeable en < 15 minutes ; trier par (sévérité × impact estimé) décroissant.

---

## Grille Google Ads (~80 checks, condensée)

### Tracking de conversion (25 %)
- Google tag (gtag.js) installé et actif sur toutes les pages
- Enhanced Conversions actives (données first-party hashées)
- **Consent Mode v2 implémenté — obligatoire UE/EEE** (croiser avec `12-acquisition/conformite-rgpd.md`)
- Actions de conversion bien mappées (primaires vs secondaires) ; import de conversions offline pour le lead gen
- Attribution data-driven (last-click en repli uniquement) ; analyse du conversion lag

### Wasted spend (20 %)
- Search Terms Report revu (30 jours minimum) ; ne signaler que les termes > 10 $ de dépense ET 0 conversion
- Couverture en mots-clés négatifs : **listes négatives partagées** au niveau compte + négatifs campagne
- Règles négatifs (des négatifs mal choisis tuent une campagne) : jamais de négatif en Broad sans justification ; Exact `[mot]` par défaut pour les requêtes hors sujet précises, Phrase `"mot"` pour les patterns d'intention ; sourcer depuis le Search Terms Report réel, jamais deviner ; regrouper en listes thématiques (informationnel, job-seekers, concurrents, free-intent) ; vérifier le sur-blocage des négatifs existants
- Broad Match uniquement avec Smart Bidding (**jamais sans**) ; Broad + CPC manuel = legacy BMM à migrer
- Campagnes brand / non-brand séparées ; ciblage géo précis ; taux de clics invalides < 10 %

### Structure de compte (15 %)
- Groupes d'annonces thématiques serrés (15-20 mots-clés max), ≥ 3 RSA actives par groupe
- PMax : asset groups + signaux d'audience structurés ; SKAGs à migrer vers des groupes thématiques
- Conventions de nommage cohérentes

### Mots-clés (15 %)
- Progression de match types Exact → Phrase → Broad ; Quality Score moyen ≥ 7 (< 5 = FAIL, 5-6 = WARNING)
- Cannibalisation (même mot-clé dans plusieurs campagnes) ; impression share suivi sur les tops
- Dédupliquer par (ad_group + keyword + match_type) avant analyse ; n'analyser que ENABLED

### Annonces (15 %)
- RSA : ≥ 8 titres uniques, ≥ 3 descriptions ; ad strength Good/Excellent ; épinglage minimal
- Extensions : sitelinks ≥ 4, callouts ≥ 4, snippets structurés, image
- Copy avec CTA, proposition de valeur, différenciateurs — **une annonce est un contenu de marque : étape 0 doctrine `01-brand/` avant toute réécriture proposée**

### Réglages (10 %)
- ECPC déprécié → migrer vers Smart Bidding complet (tCPA/tROAS/Maximize)
- Aucune campagne « limitée par le budget » (sauf intentionnel) ; ad schedule aligné sur les conversions
- Ciblage géo en « Presence », pas « Presence or Interest » ; Search Partners revus, Display désactivé pour Search

### PMax / AI Max / Demand Gen (si présents)
- **PMax** : diversité des assets, signaux d'audience, brand exclusions (ne pas cannibaliser le brand search), négatifs niveau campagne, search themes, URL expansion contrôlée
- **AI Max for Search** : exige Smart Bidding + listes négatives solides (portée ×3-5) ; AI Brief renseigné (proposition de valeur, sujets interdits, disclaimers) ; contrôles Final URL Expansion ; brand exclusions ; attention à la migration automatique DSA/ACA/broad → AI Max (sept. 2026) — pré-staging des négatifs, baseline 28 jours avant migration
- **Demand Gen** : mix vidéo + image (≈ +20 % de conversions au même CPA vs vidéo seule) ; pas de frequency cap disponible

### Seuils Google

| Métrique | Pass | Warning | Fail |
|---|---|---|---|
| Quality Score (moyen) | ≥ 7 | 5-6 | < 5 |
| CTR (Search) | ≥ 6,66 % | 3-6,66 % | < 3 % |
| CVR (Search) | ≥ 7,52 % | 3-7,52 % | < 3 % |
| Wasted spend | < 10 % | 10-20 % | > 20 % |
| Clics invalides | < 5 % | 5-10 % | > 10 % |

---

## Grille Meta Ads (~50 checks, condensée)

**Contexte 2026 (Andromeda + GEM + Lattice)** : le contenu créatif s'embarque directement dans l'espace de ciblage — « creative is the new targeting » est mécanique, plus un slogan. Les créas trop similaires (score de similarité > 60 %) sont clusterisées (Entity-ID) et sous-diffusées : **100 variations mineures ne font pas mieux que 10 créas réellement distinctes.**

### Pixel / CAPI (30 %)
- Pixel installé partout + **Conversions API active** (30-40 % de données perdues sans, post-iOS 14.5)
- Déduplication configurée (event_id, taux ≥ 90 %) ; **EMQ ≥ 8,0 sur Purchase** (< 6 = FAIL ; leviers : em, ph, fn/ln, external_id)
- Événements standard complets (ViewContent, AddToCart, Purchase, Lead) ; domaine vérifié ; devise/valeur correctes

### Créa (30 %)
- ≥ 3 formats actifs (image, vidéo, carrousel, collection) ; ≥ 5 créas par ad set
- Fatigue : CTR en baisse > 20 % sur 14 jours = FAIL ; refresh toutes les 2-4 semaines à fort spend
- Scoring diversité sur 5 axes (0-2 chacun, total 0-10) : concepts, formats, visuels, hooks vidéo, structures de titres. 8-10 = risque de clustering FAIBLE ; 0-3 = FORT
- Prédicteur de clustering pré-lancement : même hero produit / mêmes 4 premiers mots de titre / même hook 0-3 s → probablement clusterisés ; croiser format ET visuel pour casser le cluster
- UGC/témoignages testés ; vidéo ≤ 15 s Stories/Reels

### Structure (20 %)
- 1-3 campagnes au total (consolidation) ; CBO vs ABO intentionnel
- Learning phase : < 30 % d'ad sets en « Learning Limited » (FAIL > 50 %) ; budget par ad set ≥ 5× CPA cible
- Overlap d'audiences entre ad sets < 30 %
- Objectifs Sales/Leads/App : les défauts ASC s'appliquent désormais (catalogue connecté, cap clients existants 10-25 %, Advantage+ Audience/Creative/Placements activés sauf exception documentée)

### Audience (20 %)
- Fréquence prospection (7 j) < 3,0 (FAIL > 5) ; retargeting < 8,0 (FAIL > 12)
- Custom Audiences (site, listes clients, engagement) ; acheteurs exclus de la prospection
- Advantage+ Audience testé vs ciblage manuel ; catégories spéciales déclarées si applicable

### Seuils Meta

| Métrique | Pass | Warning | Fail |
|---|---|---|---|
| EMQ (Purchase) | ≥ 8,0 | 6,0-7,9 | < 6,0 |
| Taux dédup | ≥ 90 % | 70-90 % | < 70 % |
| CTR | ≥ 1,0 % | 0,5-1,0 % | < 0,5 % |
| Créas par ad set | ≥ 5 | 3-4 | < 3 |
| Learning Limited | < 30 % | 30-50 % | > 50 % |

---

## Grille LinkedIn Ads (27 checks, condensée)

**Terminologie (oct. 2025)** : Campaign Groups → « Campaigns », Campaigns → « Ad Sets ».

### Technique (25 %)
- Insight Tag actif partout ; **Conversions API** active (2025) ; événements full-funnel
- Intégration CRM Salesforce/HubSpot (closed-loop impression → revenu)

### Audience (25 %)
- Ciblage par intitulés précis, pas seulement par fonction ; taille d'entreprise et séniorité alignées sur l'ICP (croiser avec `01-brand/personas.md`)
- Matched Audiences actives (retargeting + listes) ; listes ABM (jusqu'à 300 000 entreprises), segmentées par tiers
- **Audience expansion OFF** pour les campagnes de précision ; predictive audiences testées (remplacent les Lookalikes depuis fév. 2024)
- **LinkedIn Audience Network : OFF** (consensus expert — qualité faible, dilue les données)

### Créa (20 %)
- **Thought Leader Ads : ≥ 30 % du budget B2B** — CPC $2,29-4,14 vs $13,23 en Sponsored Content standard, engagement 2-5× ; recommandation HAUTE priorité s'ils sont absents
- ≥ 2 formats testés ; vidéo testée ; refresh toutes les 4-6 semaines

### Lead Gen (15 %)
- Lead Gen Form ≤ 5 champs (benchmark CVR 13 %) ; sync CRM temps réel
- Objectif de campagne aligné sur l'étape du funnel ; A/B test actif ; message ads ≤ 1 / 30-45 jours

### Budget & enchères (15 %)
- Commencer en CPC manuel (Maximum Delivery = l'option la plus chère) ; budget quotidien ≥ 50 $ en Sponsored Content
- Suivre le taux lead → opportunité, pas seulement le CPL ; attribution 30 j clic / 7 j vue

### Seuils LinkedIn

| Métrique | Pass | Warning | Fail |
|---|---|---|---|
| CTR (Sponsored Content) | ≥ 0,44 % | 0,30-0,44 % | < 0,30 % |
| CPC moyen | ≤ 7 $ | 7-10 $ | > 10 $ |
| CVR Lead Gen Form | ≥ 10 % | 5-10 % | < 5 % |
| Part de budget TLA | ≥ 30 % | 15-30 % | < 15 % |

---

## Autres plateformes (annexes)

TikTok, Microsoft, Apple et Amazon Ads sont hors cœur de cible du template mais couverts en version courte : lire `references/annexes-plateformes.md` **uniquement si le compte audité utilise l'une de ces plateformes**.

## Analyse cross-plateformes (si ≥ 2 plateformes actives)

- **Allocation budgétaire** : réelle vs recommandée selon le type de business
- **Cohérence du tracking** : les plateformes suivent-elles les mêmes événements ?
- **Cohérence créative** : le messaging est-il aligné (et conforme à `01-brand/messaging-framework.md`) ?
- **Recouvrement d'attribution** : conversions double-comptées ?
- **Kill list** : campagnes/groupes à couper immédiatement ; opportunités de scaling

## Livrables

| Fichier | Contenu |
|---|---|
| `12-acquisition/audits/AAAA-MM-JJ-ads-audit.md` | Rapport complet : scores, findings PASS/WARNING/FAIL par catégorie, wasted spend estimé (€/mois) |
| Même fichier, sections finales | Plan d'action priorisé (Critique > Haute > Moyenne > Basse) + Quick Wins |
| `02-strategy/performance/AAAA-MM/data.json` | Scores et métriques clés versés dans le snapshot (sections par plateforme) |

Format de score par plateforme :

```
[Plateforme] Health Score : XX/100 (Note : X)
Catégorie 1 : XX/100 (poids %)
…
```

## Règles

- **Aucune modification de compte** : audit et recommandations écrites uniquement (cf. règle dure du module `12-acquisition/`).
- **Aucun chiffre inventé** : chaque constat cite sa donnée source (export, capture, requête MCP).
- Toute proposition de nouvelle annonce ou de réécriture passe par l'étape 0 doctrine (`01-brand/checklist-pre-composition.md`) et le brand-check, comme tout contenu.
- Benchmarks datés (2025-2026, source claude-ads v1.7.1) : les traiter comme ordres de grandeur, pas comme vérités absolues — les confronter aux données historiques du compte.
