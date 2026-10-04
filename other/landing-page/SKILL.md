---
name: landing-page
description: Créer une landing page de conversion pour {{COMPANY_NAME}}, du brief à la livraison HTML statique dans 05-web-content/landing-pages/. Orchestre la structure CRO (skill cro-page), le copy (skill copywriting), le design (skills design-direction / design-system sous contrainte des tokens 01-brand), le tracking UTM + GA4 et la QA responsive/vitesse. Utiliser dès que l'utilisateur demande une landing page, une page de vente, une page de capture, une page d'inscription à un événement ou une page de campagne.
---

# landing-page — landing pages de conversion {{COMPANY_NAME}}

Vous produisez des landing pages au meilleur niveau du marché : structure CRO éprouvée, copy ancré dans le messaging framework, design premium sous contrainte stricte de la marque, tracking mesurable dès le premier jour.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant toute production :

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie, assets, réutilisation.
2. Charger `01-brand/voice.md` — position de voix, vocabulaire, interdits.
3. Charger `01-brand/style-guide.md` — tokens (couleurs, police, radius, gradient) : ils seront injectés à l'étape design.
4. Lire `05-web-content/CLAUDE.md` — structure du dossier, conventions techniques, règle de réutilisation.
5. Charger `01-brand/design-anti-generique.md` — doctrine design anti-générique : marqueurs du look IA interdits par défaut, workflow deux passes (plan de tokens → auto-critique), checklist de pré-livraison mesurable.

**Ne jamais produire sans.** Si un de ces fichiers manque ou contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`.

## Skills internes orchestrées

Le chemin nominal passe par les skills internes du template (`.claude/skills/`). Si l'une manque (template partiellement synchronisé), appliquer le fallback inline documenté à l'étape correspondante — ne jamais bloquer.

| Skill interne | Rôle dans le workflow | Fallback inline |
|---|---|---|
| `cro-page` | Valider/challenger la structure et faire la revue CRO finale | Structure de référence documentée à l'étape 2 |
| `design-direction` | Direction artistique : compositions, hiérarchie, typographie appliquée | Style-guide + `05-web-content/sections-library.md` seuls |
| `design-system` | Système de composants, tokens, états d'interaction | idem |
| `design-review` | QA visuelle finale | Checklist QA de l'étape 7 |
| `cro-form` | Optimiser le formulaire de capture s'il y en a un | Règles formulaire de la skill `lead-magnet` |
| `cro-popup` | Popup/exit-intent si explicitement demandé | Pas de popup — CTA inline uniquement |

## Workflow

### 1. Brief

Créer (ou compléter) `05-web-content/briefs/<slug>.md` avec, au minimum :

- **Objectif de conversion** : UNE action mesurable (inscription, demande de démo, téléchargement, achat). Une page = un objectif = un CTA primaire.
- **Cible** : persona (référence `01-brand/personas.md`) + niveau de conscience (découvre le problème / compare les solutions / prêt à agir).
- **Offre** : ce que le visiteur obtient, formulé en bénéfice ; prix ou contrepartie (email, formulaire).
- **Source de trafic prévue** : d'où viennent les visiteurs (post LinkedIn, newsletter, ads, QR event) — le message de la page doit prolonger le message de la source (*message match*).
- **Preuves disponibles** : chiffres du messaging framework, témoignages, logos, études de cas.
- **Métrique de succès** : taux de conversion visé, volume attendu.

{{COMPANY_MAIN_CONTACT}} valide le brief avant rédaction.

### 2. Structure CRO

**Chemin nominal** : invoquer la skill interne **`cro-page`** avec le brief pour construire et challenger la structure, puis continuer.

**Fallback** (si `cro-page` manque) : appliquer la structure de référence (l'ordre s'adapte au niveau de conscience de la cible) :

1. **Hero** — proposition de valeur en une phrase (bénéfice + spécificité), sous-titre qui précise pour qui / comment, CTA primaire visible sans scroller. Test des 5 secondes : un inconnu doit pouvoir dire ce que la page propose, pour qui, et quoi faire.
2. **Preuve immédiate** — logos clients, chiffre-clé ou note ; crédibilise avant même d'argumenter.
3. **Problème** — les frustrations du persona, dans ses mots (personas.md).
4. **Solution / bénéfices** — 3-4 blocs, bénéfice avant fonctionnalité, chaque bloc ancré dans un chiffre du messaging framework.
5. **Preuve détaillée** — stats, témoignages avec nom et contexte, étude de cas concrète.
6. **Traitement des objections** — FAQ, garanties, réponses aux freins identifiés dans personas.md.
7. **CTA final** — reformulation de la proposition de valeur + CTA identique au hero (même action, même libellé).

Règles transverses : un seul objectif de conversion ; le CTA primaire répété à chaque écran de scroll ; aucune navigation sortante (pas de menu complet — logo + CTA suffisent) ; message match avec la source de trafic ; les sections viennent de `05-web-content/sections-library.md` (règle « réutiliser avant de créer »).

### 3. Copy

Invoquer la skill **`copywriting`** avec le brief et la structure validée. Elle applique sa propre étape 0 doctrine, ancre chaque section dans `01-brand/messaging-framework.md` et respecte les interdits anti-style-IA. Passer ensuite la skill `copy-editing` si la page est à fort enjeu.

### 4. Design — tokens d'abord, skill ensuite

Ordre impératif :

1. **Charger les tokens** de `01-brand/style-guide.md` : `{{BRAND_FONT_PRIMARY}}`, `{{BRAND_COLOR_PRIMARY}}`, `{{BRAND_COLOR_ACCENT}}`, `{{BRAND_COLOR_DARK}}`, `{{BRAND_COLOR_LIGHT}}`, `{{BRAND_GRADIENT}}`, `{{BRAND_BORDER_RADIUS}}`, style d'illustration, interdits visuels.
2. **Invoquer les skills design internes** — `design-direction` (compositions, hiérarchie visuelle, typographie appliquée) puis `design-system` (composants, états d'interaction) — **en injectant les tokens dans la demande** et en précisant explicitement : « la charte de marque fournie prime sur tout style générique ; ne pas proposer de palette ni de typographie alternatives ». Les skills design décident des compositions, hiérarchies visuelles, rythmes, interactions — jamais des couleurs ni des polices.
3. **Fallback** (si ces skills manquent) : décliner les structures HTML de `05-web-content/sections-library.md` avec les tokens, en soignant hiérarchie typographique et espacements généreux.

Visuels : assets existants de `01-brand/assets/` d'abord, sinon skill `image-generation` (sortie copiée dans `assets/` de la page).

### 5. Build

- `05-web-content/landing-pages/<slug>/index.html` — single-file, CSS + JS inline, tokens en custom properties `:root` (bloc de référence dans `sections-library.md`).
- Header/footer depuis `05-web-content/templates/` s'ils existent (une landing page de campagne peut légitimement s'en passer).
- Mobile-first, HTML sémantique, alt text, contrastes AA, navigation clavier, `lang="{{BRAND_LANGUAGE}}"`.
- SEO/meta : `<title>`, meta description, Open Graph, favicon, `<meta name="robots">` (`noindex` par défaut pour une page de campagne, à confirmer au brief).

### 6. Tracking — UTM + conversion

**Conventions UTM** (pour toutes les URL diffusées vers la page — kebab-case, minuscules) :

| Paramètre | Contenu | Exemples |
|---|---|---|
| `utm_source` | Plateforme d'origine | `linkedin`, `newsletter`, `google`, `partenaire-x` |
| `utm_medium` | Type de canal | `social`, `email`, `cpc`, `qr`, `referral` |
| `utm_campaign` | Slug de campagne + année | `{{CAMPAIGN_SLUG}}-2026` |
| `utm_content` | Variante/emplacement | `post-1`, `cta-hero`, `cta-final` |

Générer le tableau des URL trackées dans le brief et le reporter dans `deployed.md`.

**Événement de conversion** :

- Si `web_analytics` est activé dans `.setup-completed` (GA4) : intégrer le snippet gtag avec `{{GA4_MEASUREMENT_ID}}` et déclencher :
  - `generate_lead` à la soumission du formulaire (avec `lead_source` = slug de la page) ;
  - `cta_click` au clic sur le CTA primaire (paramètre `cta_position`: `hero` | `final`).
  - Marquer `generate_lead` comme conversion clé dans GA4 (action manuelle côté interface — le signaler à l'utilisateur).
- Sinon : poser des attributs `data-track="generate_lead"` / `data-track="cta_click"` sur les éléments concernés, pour brancher l'analytics plus tard sans retoucher le HTML.

Jamais de clé ou d'ID en dur non documenté : l'ID de mesure vit dans `.env` / la config, référencé en placeholder dans le template.

### 7. QA responsive + vitesse

- **Responsive** : vérifier le rendu à 375, 600, 900 et 1280 px (outil de preview navigateur si disponible, sinon revue attentive des media queries). Aucun débordement horizontal ; CTA atteignable au pouce sur mobile ; hero lisible sans zoom.
- **Vitesse** : HTML+CSS+JS inline < 200 Ko ; images en WebP, compressées, dimensionnées à l'usage, `loading="lazy"` hors hero ; fonts en `font-display: swap` avec `preconnect` ; pas de JS bloquant ; cible LCP < 2,5 s.
- **Accessibilité** : contrastes AA sur les CTA, labels de formulaire explicites, focus visibles.

**Revues finales** : soumettre la page finie à `design-review` (QA visuelle : espacements, hiérarchie, cohérence des composants) puis à `cro-page` (revue CRO : frictions, clarté du CTA) et appliquer les corrections pertinentes. Si ces skills manquent, la checklist ci-dessus tient lieu de revue.

### 8. Brand-check (obligatoire)

Invoquer `brand-check` — copy ET conformité visuelle (couleurs, police, espacements contre le style guide). Aucune livraison sans verdict positif.

### 9. Livraison et enregistrement

1. Livrer `05-web-content/landing-pages/<slug>/index.html` (+ `assets/`).
2. Mettre à jour `05-web-content/deployed.md` : URL prévue/réelle, date, responsable, UTM, métrique de succès.
3. Mettre à jour le calendrier éditorial (`02-strategy/calendar/calendar.md`).
4. Déploiement : suivre `05-web-content/CLAUDE.md` § Publication (dry-run obligatoire).
5. Si module `reporting` actif : signaler la page à suivre (conversions `generate_lead`) dans `11-reporting/`.

## Checklist pré-livraison

- [ ] Brief validé par {{COMPANY_MAIN_CONTACT}} (objectif, cible, offre, source de trafic)
- [ ] Un seul objectif de conversion, CTA identique du hero au final
- [ ] Sections issues de `sections-library.md` (ou nouvelles sections reversées à la bibliothèque)
- [ ] Copy via skill `copywriting`, chiffres vérifiés contre le messaging framework
- [ ] Tokens 01-brand injectés AVANT toute skill design ; aucune couleur/police hors charte
- [ ] Test des 5 secondes concluant sur le hero
- [ ] UTM documentés + événement de conversion en place (GA4 ou `data-track`)
- [ ] QA responsive 375/600/900/1280 + budget vitesse respecté
- [ ] `brand-check` passé (copy + visuel)
- [ ] `deployed.md` et calendrier éditorial à jour

## Skills associées

- `copywriting` / `copy-editing` — texte
- `cro-page` / `cro-form` / `cro-popup` — structure et revues CRO
- `design-direction` / `design-system` / `design-review` — design sous tokens 01-brand
- `lead-magnet` — si la page capture un email contre un contenu (workflow complet côté lead magnet)
- `image-generation` — visuels
- `brand-check` — validation finale obligatoire
- `performance-report` — suivi des conversions (module `reporting`)
