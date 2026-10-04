---
name: seo-cluster
description: Clustering sémantique par recouvrement de SERP pour l'architecture de contenu de {{COMPANY_NAME}} — expansion de mots-clés, regroupement par résultats Google réellement partagés, architecture hub-and-spoke (page pilier + satellites), matrice de maillage interne. Alimente les briefs 09-seo/. Utiliser quand l'utilisateur dit « cluster », « topic cluster », « page pilier », « hub and spoke », « regrouper des mots-clés » ou « architecture de contenu ».
---

# seo-cluster — clustering sémantique par SERP

Skill d'analyse et de planification. La rédaction des contenus du cluster passe ensuite par la skill `seo` (workflow de production, doctrine `01-brand/`). Adapté du plugin claude-seo (AgriciDaniel, MIT ; méthodologie originale Lutfiya Miller) — voir `docs/vendored-seo.md`.

**Principe** : regrouper les mots-clés selon la façon dont **Google les classe réellement** (URLs partagées dans le top 10), pas selon leur similarité textuelle.

## Étape 1 — Expansion du mot-clé seed (30-50 variantes)

Via WebSearch :
1. **Recherches associées** et « autres questions posées » (PAA)
2. **Modificateurs longue traîne** : « meilleur », « comment », « vs », « pour débutants », « outils », « exemples », « guide », « modèle », « erreurs », « checklist »
3. **Questions** : qui/quoi/quand/où/pourquoi/comment
4. **Modificateurs commerciaux** : « prix », « avis », « alternative », « comparatif », « gratuit »

Dédupliquer (normaliser, retirer les doublons). Si < 30 variantes, relancer une passe avec les meilleures questions PAA comme seeds. Travailler dans la langue du marché cible ({{COMPANY_NAME}}).

## Étape 2 — Clustering par recouvrement de SERP

Pour chaque paire candidate (pré-grouper par intention supposée pour limiter les comparaisons) : chercher les deux mots-clés, compter les URLs partagées dans le top 10 organique (ignorer ads, featured snippets, PAA).

| Résultats partagés | Relation | Action |
|---|---|---|
| 7-10 | Même page | Fusionner en une seule page cible |
| 4-6 | Même cluster | Grouper sous le même satellite |
| 2-3 | Adjacents | Clusters voisins + liens croisés |
| 0-1 | Séparés | Clusters différents ou exclusion |

Optimisation : ne pas comparer les paires de variantes longue traîne d'une même tête (les supposer dans le même cluster) ; ne croiser que les mots-clés en frontière de groupe.

## Étape 3 — Classification d'intention

| Intention | Signaux | Inclure ? |
|---|---|---|
| Informationnelle | comment, pourquoi, guide, tutoriel | Oui |
| Commerciale | meilleur, avis, comparatif, vs, alternative | Oui |
| Transactionnelle | acheter, prix, tarif, essai, inscription | Oui |
| Navigationnelle | noms de marques/produits précis | **Non** (exclure) |

Intention mixte → classer par intention dominante ; cas limites → flagger pour arbitrage humain.

## Étape 4 — Architecture hub-and-spoke

1. **Pilier** : mot-clé au plus fort volume, intention la plus large, plus fort recouvrement avec les autres — 2500-4000 mots.
2. **Clusters** : 2-5 sous-thèmes par pilier ; **satellites** : 2-4 posts par cluster — 1200-1800 mots.
3. **Gabarit par intention** : guide complet / how-to / listicle / explainer (info) ; comparatif / avis / best-of (commercial) ; landing page (transactionnel — skill `landing-page`).
4. **Anti-cannibalisation** : aucun doublon de mot-clé principal ; recouvrement SERP ≥ 7 → fusionner.

## Étape 5 — Matrice de maillage interne

| Lien | Direction | Règle |
|---|---|---|
| Satellite → pilier | obligatoire | chaque satellite |
| Pilier → satellite | obligatoire | chaque satellite |
| Satellite ↔ satellite (même cluster) | 2-3 par post | — |
| Inter-clusters | 0-1 par post | — |

Règles : minimum 3 liens entrants par page ; aucune page orpheline (tout atteignable depuis le pilier en 2 clics) ; ancres = mot-clé cible ou variante proche (jamais « cliquez ici ») ; liens dans le corps du texte.

## Sorties (dans 09-seo/)

| Fichier | Contenu |
|---|---|
| `09-seo/keyword-research/<cluster>/YYYY-MM-cluster-plan.md` | Plan lisible : pilier, clusters, satellites, intentions, volumes estimés, matrice de liens |
| `09-seo/content-briefs/brief-<slug>.md` | Un brief par page au format de la skill `seo` (mot-clé principal + secondaires, intention, structure H2/H3, liens internes à inclure avec ancres, longueur cible, pages concurrentes à différencier) |

Mettre à jour le calendrier éditorial (`02-strategy/calendar/calendar.md`) avec les contenus planifiés (statut `idée`).

## Enchaînement production

Plan validé par l'utilisateur → skill `seo` produit pilier d'abord, puis satellites par volume décroissant. Après chaque publication, poser les liens retour vers les pages déjà en ligne. Suivi qualité : couverture (pages écrites/planifiées), densité de liens (≥ 3/page), orphelines (0), cannibalisation (0).

## Gestion d'erreur

| Cas | Résolution |
|---|---|
| Expansion < 15 variantes | Seconde passe avec les questions PAA |
| Données SERP indisponibles | Réessayer ; sinon clustering par intention seule, avec avertissement explicite |
| Cannibalisation détectée | Fusionner les pages ou réassigner les mots-clés |
