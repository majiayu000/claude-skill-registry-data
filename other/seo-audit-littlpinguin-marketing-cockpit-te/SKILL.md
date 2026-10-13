---
name: seo-audit
description: Audit SEO du site {{COMPANY_NAME}} ou analyse approfondie d'une page unique — crawlabilité, indexation, Core Web Vitals, on-page, contenu E-E-A-T, schema, préparation IA. Produit un score de santé et un plan d'action priorisé dans 09-seo/audits/. Utiliser quand l'utilisateur dit « audit SEO », « pourquoi je ne ranke pas », « analyse cette page », « check SEO », « mon trafic a chuté », ou fournit une URL à diagnostiquer.
---

# seo-audit — audit de site & analyse de page

Skill d'**analyse**, pas de production. La production d'articles et de briefs reste dans la skill `seo`. Adapté du plugin claude-seo (AgriciDaniel, MIT) — voir `docs/vendored-seo.md`.

## Deux modes

| Mode | Déclencheur | Portée |
|---|---|---|
| **Audit de site** | « audit », « check complet », domaine fourni | Homepage + crawl interne (max 50 pages, respecter robots.txt) |
| **Analyse de page** | une URL précise fournie | La page seule, en profondeur |

## Workflow — audit de site

1. **Récupérer la homepage** (WebFetch ou `curl -sL`) + `robots.txt` + sitemap(s).
2. **Crawler** : suivre les liens internes (max 50 pages, 3 redirections max, respecter robots.txt). Sur les gros sites, échantillonner par gabarit (home, catégorie, article, page produit/service).
3. **Déléguer en parallèle** aux agents internes :
   - `seo-technical` — crawlabilité, indexation, canonicals, sécurité, CWV, rendu JS
   - `seo-content` — E-E-A-T, lisibilité, contenu mince, citabilité IA
   - `seo-google` — données terrain CrUX / GSC / GA4 (**seulement si** le couplage `/tools-setup` est actif)
   - skill `seo-geo` — crawlers IA, llms.txt, citabilité (si l'audit vise aussi la visibilité IA)
   - skill `seo-schema` — détection et validation des données structurées
4. **Agréger** en un score de santé SEO (0-100) :

| Catégorie | Poids |
|---|---|
| SEO technique | 25% |
| Qualité de contenu | 25% |
| On-page | 20% |
| Schema / données structurées | 10% |
| Performance (CWV) | 10% |
| Préparation recherche IA | 10% |

5. **Rapporter** dans `09-seo/audits/YYYY-MM-DD-audit-<domaine>.md` : résumé exécutif (score, top 5 problèmes critiques, top 5 quick wins), sections par catégorie, plan d'action priorisé.

## Workflow — analyse de page unique

Analyser directement (sans sous-agents, sauf besoin) :

### On-page
- Title : 50-60 caractères, mot-clé principal, unique
- Meta description : 150-160 caractères, incitative
- H1 unique aligné sur l'intention ; hiérarchie H2-H6 sans saut de niveau
- URL courte, descriptive, avec tirets, sans paramètres
- Maillage interne suffisant, ancres descriptives ; 1-2 liens externes d'autorité

### Contenu
- Volume vs type de page (home ≥ 500 mots, page service ≥ 800, article ≥ 1500 — planchers de couverture, pas des cibles)
- Densité de mot-clé naturelle (1-3%), variantes sémantiques
- Signaux E-E-A-T : bio auteur, dates de publication/mise à jour, sources citées

### Technique
- Canonical présent et correct ; meta robots ; Open Graph + Twitter Card ; hreflang si multilingue

### Images
- Alt descriptif ; poids (> 200 Ko = warning, > 500 Ko = critique) ; formats WebP/AVIF ; dimensions déclarées (CLS) ; `loading="lazy"` sous la ligne de flottaison

### CWV (indices depuis le HTML)
- Risques LCP (hero lourd, ressources bloquantes), INP (JS lourd sans async/defer), CLS (dimensions manquantes, contenu injecté)

## Priorités

- **Critique** : bloque l'indexation ou expose à une pénalité — corriger immédiatement
- **Haute** : impact significatif sur le ranking — sous 1 semaine
- **Moyenne** : opportunité d'optimisation — sous 1 mois
- **Basse** : backlog

## Format de sortie (page unique)

```
Score global : XX/100
On-page XX | Contenu XX | Technique XX | Schema XX | Images XX
```
Puis : problèmes par priorité → recommandations actionnables → snippets JSON-LD prêts à poser (via skill `seo-schema`).

## Gestion d'erreur

| Cas | Action |
|---|---|
| URL injoignable | Rapporter l'erreur, ne jamais inventer le contenu du site |
| robots.txt bloque le crawl | Analyser les pages accessibles, noter la limite dans le rapport |
| Contenu rendu en JS (body vide) | Analyser le HTML disponible, signaler que les résultats sont partiels |
| Rate limiting (429) | Ralentir, livrer un rapport partiel annoté |

## Extensions possibles (non vendorées)

Le plugin source couvre aussi : backlinks (APIs Moz/Bing), SEO local & Google Maps, e-commerce, hreflang avancé, drift/baselines, DataForSEO. Si le besoin apparaît, installer le plugin `claude-seo` complet ou re-vendorer — procédure dans `docs/vendored-seo.md`.
