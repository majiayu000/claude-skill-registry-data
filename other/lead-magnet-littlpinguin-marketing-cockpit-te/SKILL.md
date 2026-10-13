---
name: lead-magnet
description: Créer un lead magnet pour {{COMPANY_NAME}} — guide PDF charté, outil interactif (calculateur, diagnostic), quiz, template/checklist — avec le circuit de capture complet obligatoire (page de capture → formulaire → n8n → outil emailing → séquence de nurturing). Utiliser dès que l'utilisateur demande un lead magnet, un aimant à leads, un guide téléchargeable, un livre blanc, un calculateur, un quiz, un diagnostic, une checklist ou un template à offrir contre un email.
---

# lead-magnet — lead magnets {{COMPANY_NAME}}

Vous produisez des lead magnets qui génèrent des leads qualifiés, pas des fichiers.

**Principe fondateur : un lead magnet sans capture d'email est un PDF perdu.** Aucun lead magnet n'est livré sans son circuit complet : contenu → page de capture → formulaire → automatisation → séquence de nurturing → mesure. Si l'utilisateur demande « juste le PDF », produire le PDF mais signaler explicitement que le circuit n'est pas en place et proposer de le construire.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie, assets, réutilisation.
2. Charger `01-brand/voice.md` et `01-brand/personas.md` — le choix du type de lead magnet dépend du persona.
3. Charger `01-brand/style-guide.md` — tout livrable (PDF comme outil web) est charté.
4. Charger `01-brand/design-anti-generique.md` — un outil interactif visuellement générique décrédibilise la capture ; mêmes exigences qu'une landing page.
5. Lire `05-web-content/CLAUDE.md` — structure du dossier, conventions, règle de réutilisation.

**Ne jamais produire sans.** Si un fichier manque ou contient des `{{...}}`, arrêter et lancer `/start-cockpit`.

## Typologie et critères de choix

| Type | Format & production | Bon pour | Effort | Qualification du lead |
|---|---|---|---|---|
| **Guide PDF / livre blanc** | Skill `pdf` ou `docx` chartée si disponible ; sinon HTML charté (tokens 01-brand) exporté en PDF via impression navigateur | Audience haut de funnel, expertise à démontrer, sujet dense | Moyen-élevé | Faible (email seul) |
| **Outil interactif** (calculateur, simulateur, diagnostic) | HTML/JS vanilla single-file dans `outils-web/<slug>/` (méthode ci-dessous) | Audience qui veut un résultat personnalisé (ROI, score, estimation) ; forte valeur perçue, partage naturel | Élevé | Forte (les réponses qualifient) |
| **Quiz / auto-diagnostic** | Variante de l'outil interactif : questions → scoring → profil de résultat | Qualification + segmentation : chaque profil de résultat route vers une séquence de nurturing différente | Moyen | Très forte |
| **Template / checklist** | Page HTML chartée, PDF une page, ou fichier téléchargeable | Quick win immédiat, audience opérationnelle, production rapide | Faible | Faible |

**Critères de choix** (dans cet ordre) :

1. **Persona et niveau de conscience** (`01-brand/personas.md`) : découvre le problème → guide/checklist ; compare les solutions → calculateur/diagnostic ; prêt à agir → template + démo.
2. **Promesse en une phrase** : si la valeur ne se formule pas en une phrase (« Estimez X en 2 minutes », « Les 12 points à vérifier avant Y »), le lead magnet est mal choisi.
3. **Potentiel de qualification** : un quiz segmente, un PDF non. Si le nurturing doit être différencié, préférer l'interactif.
4. **Effort vs durée de vie** : un outil interactif coûte cher mais capte des leads pendant des années ; une checklist se produit en une session.

Présenter 2-3 options argumentées à l'utilisateur avant de produire ; {{COMPANY_MAIN_CONTACT}} tranche.

## Workflow commun

### 1. Brief

`05-web-content/briefs/<slug>.md` : promesse, persona visé, type retenu, sujet ancré dans `01-brand/messaging-framework.md`, séquence de nurturing prévue (existante ou à créer), métrique de succès (téléchargements/mois, taux de conversion page → lead).

### 2. Production du contenu (par type)

**Guide PDF / livre blanc** — `05-web-content/lead-magnets/guides-pdf/<slug>/`
1. Plan validé par l'utilisateur (5-15 pages ; un guide utile et court bat un pavé).
2. Rédaction via la skill `copywriting` (étape 0 doctrine incluse) ; chiffres vérifiés contre le messaging framework ou `_sources/reports/`.
3. Mise en forme chartée : skill `pdf` ou `docx` si disponible dans l'environnement ; sinon document HTML aux tokens 01-brand (custom properties, voir `05-web-content/sections-library.md`) avec CSS print, exporté en PDF via impression navigateur.
4. Couverture : assets de `01-brand/assets/` d'abord, sinon skill `image-generation`.
5. Dernière page : CTA vers l'étape suivante (démo, contact, autre contenu) — un PDF sans CTA est une impasse.

**Outil interactif / quiz** — `05-web-content/lead-magnets/outils-web/<slug>/`
1. Spécifier la logique (entrées, calcul ou scoring, restitution) et la faire valider AVANT de coder.
2. Build : `index.html` autonome, HTML/JS vanilla, tokens 01-brand, mobile-first, conventions techniques de `05-web-content/CLAUDE.md`. Design via `design-direction` / `design-system` avec les tokens injectés (la marque prime) ; fallback : sections-library + style-guide seuls.
3. **Capture intégrée à l'outil** : le résultat détaillé (score complet, rapport, recommandations) est délivré contre l'email — l'utilisateur voit un aperçu du résultat, l'email débloque le reste. Jamais de formulaire avant toute valeur : donner d'abord, capturer ensuite.
4. Pour un quiz : chaque profil de résultat porte un identifiant transmis à l'automatisation (segmentation du nurturing).

**Template / checklist**
1. Contenu via `copywriting`, format le plus actionnable (checklist cochable, tableau à remplir).
2. Livrable charté : page HTML dans `outils-web/` ou PDF une page dans `guides-pdf/`.

### 3. Page de capture

Invoquer la skill **`landing-page`** (brief allégé : hero avec promesse du lead magnet, aperçu/mockup, 3 bénéfices, preuve, formulaire). La page vit dans `05-web-content/landing-pages/<slug>/`.

### 4. Formulaire

Chemin nominal : skill interne **`cro-form`**. Fallback inline :

- Le minimum de champs : **email seul** par défaut ; prénom uniquement si le nurturing le personnalise ; toute question de qualification doit payer son coût en friction.
- Label explicite, bouton formulé en bénéfice (« Recevoir le guide », jamais « Envoyer »).
- Mention RGPD sous le formulaire : finalité, désinscription en un clic, lien politique de confidentialité. Case d'opt-in marketing distincte si la séquence dépasse la livraison du contenu ({{LEGAL_OPTIN_POLICY}}).
- Message de confirmation qui annonce la suite (« Le guide arrive par email dans 2 minutes »).

### 5. Automatisation — circuit de capture

**Le circuit complet, sans exception :**

```
Lead magnet → formulaire → n8n (module automatisations) → outil emailing → séquence de nurturing
```

- **Si le module `automatisations` est actif** (`.setup-completed.modules`) : concevoir le workflow n8n selon `10-automatisations/CLAUDE.md` (méthode conseil → plan → validation → exécution → REX). Pattern : webhook du formulaire → validation/normalisation de l'email → ajout au groupe/segment dans **{{EMAIL_MARKETING_TOOL}}** (tag = slug du lead magnet, + profil de résultat pour un quiz) → déclenchement de la séquence → envoi du livrable. Export sanitisé dans `10-automatisations/workflows/`.
- **Si le module est inactif** : brancher le formulaire directement sur le formulaire natif ou l'API de {{EMAIL_MARKETING_TOOL}} (tag identique), et signaler que n8n apporterait la validation, la segmentation fine et le suivi d'erreurs.
- Jamais de credentials dans le HTML ni dans les exports — `.env` et vault n8n uniquement (voir `SECURITY.md`).

### 6. Séquence de nurturing

Invoquer la skill **`email`** (catégorie lead nurturing, `04-email/lead-nurturing/sequences/`). Minimum vital :

1. **Email 0 (immédiat)** : livraison du lead magnet + rappel de la promesse.
2. **Emails 1-3 (J+2 à J+14)** : approfondissement du sujet, preuve, puis passage vers l'offre.

Pour un quiz : une branche par profil de résultat. La séquence est validée par brand-check comme tout contenu `04-email/`.

### 7. Brand-check (obligatoire)

`brand-check` sur chaque livrable : le lead magnet lui-même, la page de capture, les emails de la séquence.

### 8. Mesure — versée dans le reporting

Suivre, et verser dans `11-reporting/` si le module `reporting` est actif (sinon noter dans `05-web-content/deployed.md`) :

- **Téléchargements / complétions** (événement GA4 `generate_lead` de la page de capture — conventions de la skill `landing-page`)
- **Taux de conversion** visiteur → lead de la page de capture (cible indicative : 20-40 % sur trafic qualifié)
- **Qualité** : taux d'ouverture de la séquence, leads devenus opportunités ({{CRM_TOOL}} si configuré)

Mettre à jour `05-web-content/deployed.md` et le calendrier éditorial (`02-strategy/calendar/calendar.md`).

## Checklist pré-livraison

- [ ] Type choisi et argumenté selon persona + niveau de conscience, validé par {{COMPANY_MAIN_CONTACT}}
- [ ] Contenu produit via `copywriting`, chiffres vérifiés, livrable charté (tokens 01-brand)
- [ ] CTA de sortie présent dans le lead magnet lui-même
- [ ] Page de capture livrée via la skill `landing-page` (UTM + événement de conversion inclus)
- [ ] Formulaire minimal (`cro-form` ou règles inline), mention RGPD + opt-in
- [ ] Circuit complet branché : formulaire → n8n (ou direct) → {{EMAIL_MARKETING_TOOL}} → séquence
- [ ] Séquence de nurturing en place (skill `email`), email 0 livre le contenu
- [ ] `brand-check` passé sur les trois livrables (contenu, page, emails)
- [ ] Mesure configurée et `deployed.md` + calendrier à jour

## Skills associées

- `landing-page` — page de capture (structure CRO, design, tracking)
- `copywriting` / `copy-editing` — contenu
- `cro-form` / `cro-popup` — capture
- `design-direction` / `design-system` / `design-review` — design sous tokens 01-brand
- `email` — séquence de nurturing
- `image-generation` — couvertures et visuels
- `brand-check` — validation obligatoire
- `performance-report` — métriques (module `reporting`)
