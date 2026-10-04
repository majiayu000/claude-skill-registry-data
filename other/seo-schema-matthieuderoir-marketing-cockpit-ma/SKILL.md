---
name: seo-schema
description: Détecter, valider et générer des données structurées Schema.org (JSON-LD) pour {{COMPANY_NAME}} — Organization, Article, FAQ (si éligible), Event, Person, etc. Connaît les types actifs, restreints et dépréciés par Google. Utiliser quand l'utilisateur dit « schema », « données structurées », « rich results », « JSON-LD », « balisage » ou après publication d'un article/d'une page.
---

# seo-schema — données structurées

Skill d'analyse et de génération technique (pas de copy — pas de doctrine de marque requise, mais les données injectées doivent venir de sources réelles : site, `01-brand/messaging-framework.md`). Adapté du plugin claude-seo (AgriciDaniel, MIT) — voir `docs/vendored-seo.md`.

## Détection

1. Scanner la source de la page : JSON-LD `<script type="application/ld+json">` (format à privilégier — préférence déclarée de Google), Microdata (`itemscope`/`itemprop`), RDFa.
2. Valider : `@context` présent, `@type` valide, propriétés requises par type, URLs absolues, formats de date ISO, aucun texte placeholder résiduel.
3. Signaler les types dépréciés ou restreints (liste ci-dessous).

## Statut des types (état février 2026 — re-vérifier à chaque re-sync)

**ACTIFS (recommander librement)** : Organization, LocalBusiness, SoftwareApplication, WebApplication, Product, Offer, Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage, ContactPage, VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting.

**RESTREINTS** :
- **FAQPage** : rich results réservés aux sites gouvernementaux et de santé faisant autorité (restriction août 2023). Le balisage reste utile pour la compréhension machine (GEO), mais ne pas promettre de rich result.

**DÉPRÉCIÉS (ne jamais recommander)** :
- **HowTo** (rich results supprimés sept. 2023), **SpecialAnnouncement** (juil. 2025), **ClaimReview**, **VehicleListing**, **CourseInfo**, **EstimatedSalary**, **LearningVideo** (retirés 2025).

> **Rendu JavaScript** : du JSON-LD injecté en JS peut être traité avec retard. Pour un balisage sensible au temps (Event, Offer), l'inclure dans le HTML servi côté serveur.

## Génération

1. Identifier le type de page (article, événement, page entreprise, offre…).
2. Choisir le(s) type(s) de schema appropriés.
3. Générer un JSON-LD valide avec propriétés requises + recommandées.
4. **Uniquement des données véridiques et vérifiables.** Marquer clairement `[À COMPLÉTER]` ce qui manque — ne jamais inventer un téléphone, une adresse, une note.
5. Valider avant de livrer (parse JSON + propriétés requises).

## Gabarits usuels pour {{COMPANY_NAME}}

### Organization (page d'accueil / à propos)
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{{COMPANY_NAME}}",
  "url": "{{COMPANY_WEBSITE}}",
  "logo": "[URL logo]",
  "sameAs": ["[LinkedIn]", "[autres profils]"]
}
```

### Article / BlogPosting (articles 09-seo/)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Titre]",
  "author": { "@type": "Person", "name": "[Auteur]" },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "image": "[URL image]",
  "publisher": {
    "@type": "Organization",
    "name": "{{COMPANY_NAME}}",
    "logo": { "@type": "ImageObject", "url": "[URL logo]" }
  }
}
```

### Event (webinaires, événements 07-events/)
```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "[Nom]",
  "startDate": "[YYYY-MM-DDTHH:MM+01:00]",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": { "@type": "VirtualLocation", "url": "[URL]" },
  "organizer": { "@type": "Organization", "name": "{{COMPANY_NAME}}", "url": "{{COMPANY_WEBSITE}}" }
}
```

## Sortie

- Tableau de validation : `| Schema | Type | Statut ✅/⚠️/❌ | Problèmes |`
- Opportunités manquantes par page
- Snippets JSON-LD prêts à intégrer (fichier à côté du livrable concerné, ex. `09-seo/articles/…` ou `05-web-content/…`)

## Gestion d'erreur

| Cas | Action |
|---|---|
| Aucun balisage détecté | Le dire, puis recommander les types adaptés au contenu de la page |
| JSON-LD invalide | Pointer l'erreur de syntaxe précise et fournir la version corrigée |
| Type déprécié détecté | Signaler avec la date de retrait, proposer remplacement ou suppression |
