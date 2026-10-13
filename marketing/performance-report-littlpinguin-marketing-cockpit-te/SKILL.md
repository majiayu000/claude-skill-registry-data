---
name: performance-report
description: Orchestre le rapport de performance mensuel de {{COMPANY_NAME}} — collecte GA4 + Search Console + analytics social (Postiz) + emailing, snapshot data.json, analyse par le sous-agent performance-analyst, régénération du dashboard 11-reporting et déploiement FTP sur l'espace client. À invoquer en début de mois pour le mois écoulé, ou à la demande (« rapport de perf », « bilan du mois »).
---

# performance-report — rapport de performance mensuel

Tu orchestres le bilan chiffré mensuel de {{COMPANY_NAME}}. Chaîne complète : **collecte multi-sources → snapshot → analyse → dashboard → déploiement**. Chaque mois est archivé et navigable ; le dashboard présente toujours le dernier mois avec accès à l'historique.

## Arborescence cible

```
02-strategy/performance/
├── 2026-06/
│   ├── data.json      # snapshot brut consolidé (source de vérité du mois)
│   └── analyse.md     # lecture des chiffres + recommandations (performance-analyst)
├── 2026-05/
│   └── ...
```

## Étape 1 — Collecte des connecteurs configurés

Lire `.setup-completed` pour savoir quels connecteurs sont actifs (`tools.web_analytics`, `tools.social_publishing`, `tools.email_marketing`, et la config de reporting si présente). Pour le mois M (par défaut : le mois calendaire écoulé) :

| Source | Données à collecter |
|---|---|
| **GA4** | Sessions, utilisateurs, pages vues, top pages, sources de trafic, conversions/événements clés |
| **Search Console** | Clics, impressions, CTR, position moyenne, top requêtes, top pages |
| **Postiz (analytics social)** | Posts publiés par canal, impressions, engagement, followers, top posts |
| **Emailing ({{EMAIL_MARKETING_TOOL}})** | Envois, taux d'ouverture, taux de clic, désabonnements, croissance de liste |

Règles de collecte :
- Utiliser les connecteurs de `_integrations/` (credentials via `.env`, jamais en clair).
- Un connecteur désactivé ou en erreur ne bloque pas le rapport : consigner `"status": "unavailable"` pour la source et continuer. Le rapport indique explicitement les sources manquantes.
- Collecter aussi le mois M-1 (ou le relire depuis `02-strategy/performance/<M-1>/data.json` s'il existe) pour permettre les comparaisons.

## Étape 2 — Snapshot `data.json`

Écrire `02-strategy/performance/YYYY-MM/data.json` :

```json
{
  "period": "2026-06",
  "generated_at": "2026-07-01T09:00:00Z",
  "sources": {
    "ga4":            { "status": "ok", "metrics": { "...": "..." } },
    "search_console": { "status": "ok", "metrics": { "...": "..." } },
    "postiz":         { "status": "ok", "channels": { "linkedin": { "...": "..." } } },
    "email":          { "status": "unavailable", "reason": "connector disabled" }
  },
  "previous_period_ref": "02-strategy/performance/2026-05/data.json"
}
```

Le snapshot est **brut et factuel** : pas d'interprétation dedans. C'est l'entrée unique de l'analyse et du dashboard (rejouable).

## Étape 3 — Analyse par le sous-agent

Dispatcher le sous-agent **`performance-analyst`** (voir `.claude/agents/performance-analyst.md`) avec :
- le chemin du `data.json` du mois,
- le chemin du `data.json` du mois précédent (s'il existe),
- le contexte : objectifs/KPIs ({{CONTENT_KPIS}}), tent-poles du mois (calendrier, `02-strategy/reports/`).

Il produit `02-strategy/performance/YYYY-MM/analyse.md` : tendances, anomalies, hypothèses causales, 3-5 recommandations concrètes et ajustements de stratégie. Relire sa sortie : si une recommandation contredit la doctrine de marque ou la stratégie en cours, l'annoter plutôt que la supprimer.

## Étape 4 — Régénérer le dashboard

Le dashboard HTML est généré par le **module `11-reporting`** (voir son `CLAUDE.md` pour les options). Ne pas réécrire sa logique ici : se contenter d'appeler son générateur en lui passant le dossier `02-strategy/performance/` — il produit la vue du dernier mois et la **navigation mois par mois via l'archive** (chaque `YYYY-MM/` devient une entrée de l'historique).

Vérifier après génération : le mois courant s'affiche, les mois archivés sont accessibles, les sources indisponibles sont signalées et non affichées à zéro.

## Étape 5 — Déploiement FTP (espace client)

1. Publier le dashboard régénéré sur l'espace client via le script de déploiement FTP du module `11-reporting` (credentials FTP dans `.env` : hôte, utilisateur, mot de passe, chemin distant — configurés au wizard).
2. **Dry-run d'abord** : afficher la liste des fichiers qui seront transférés et la destination, attendre la confirmation de l'utilisateur avant l'upload réel (règle `SECURITY.md` : pas d'action externe sans confirmation).
3. Après upload, donner l'URL de l'espace client et proposer une vérification visuelle.

## Étape 6 — Boucler

- Signaler le rapport dans `02-strategy/reports/YYYY-MM.md` (revue mensuelle de `content-strategy`) : lien vers `analyse.md` + les 3 recommandations principales.
- Si l'analyse recommande des ajustements éditoriaux, proposer de créer les entrées correspondantes dans le calendrier (statut `idée`), en citant le chiffre déclencheur.

## Règles état de l'art (2026)

Voir `docs/etat-de-lart/mesure-attribution.md` (et `email.md`, `contenu-aeo.md`, `social-linkedin.md`) pour le détail sourcé :

1. **Structure narrative fixe de l'analyse** : résumé exécutif en langage business (3-5 phrases) → 5-7 KPIs vs objectif (pas plus) → pourquoi ça a bougé → actions du mois prochain. Un rapport sans action item est raté ; un KPI en baisse porte toujours cause + plan, jamais le chiffre seul.
2. **Attribution assumée et documentée** : last non-direct click GA4 + attribution auto-déclarée (champ « Comment nous avez-vous connus ? »), avec une note fixe dans le rapport ; ligne « part non attribuable / dark social » à part entière (20-40 % du pipeline en B2B), jamais fondue dans « direct ».
3. **Lire GSC en 3 découpes** : requêtes marque vs non-marque, pages d'argent vs blog, delta impressions vs clics (un écart croissant = absorption par les AI Overviews, pas une perte de ranking).
4. **Canal « AI referrals » au snapshot mensuel** : sessions référées par chatgpt.com / perplexity.ai / gemini.google.com / claude.ai, qualifiées par la conversion, pas le volume.
5. **Hiérarchie des métriques par canal** : email = réponses > clics > ouvertures (open rate peu fiable post-Apple MPP) ; social = impressions, clics, saves, swipes — pas les likes ; recalibrer les attentes avec la déflation de portée LinkedIn documentée (−50 % de vues YoY).

## Ce que cette skill ne fait PAS

- ❌ Interpréter les chiffres elle-même (→ sous-agent `performance-analyst`)
- ❌ Générer le HTML du dashboard (→ module `11-reporting`, elle ne fait que l'appeler)
- ❌ Modifier la stratégie sans validation humaine — elle recommande, l'utilisateur décide
