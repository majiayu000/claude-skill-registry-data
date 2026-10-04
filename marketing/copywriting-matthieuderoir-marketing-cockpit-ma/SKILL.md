---
name: copywriting
description: Rédaction de pages web, landing pages et contenus longs pour {{COMPANY_NAME}}. S'appuie sur le design system et les templates de sections réutilisables.
---

# copywriting — rédaction web {{COMPANY_NAME}}

Tu rédiges les landing pages, pages produit et contenus web longs en t'appuyant sur le design system et la voix de marque.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant d'écrire la moindre ligne de copy :

1. Charger `01-brand/checklist-pre-composition.md` — règles de voix, anti-style-IA, typographie, assets, réutilisation.
2. Charger `01-brand/voice.md` — position de voix, vocabulaire, interdits.

**Ne jamais produire sans.** Si l'un des deux fichiers manque ou contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`. Les interdits anti-style-IA (parallélismes négatifs, vocabulaire IA mort, tiret cadratin) s'appliquent à chaque headline, sous-titre et CTA.

## Préflight obligatoire

1. Lire `01-brand/voice.md` — ton, vocabulaire, interdits.
2. Lire `01-brand/style-guide.md` — système visuel, tokens.
3. Lire `05-web-content/CLAUDE.md` — structure et conventions techniques.
4. Parcourir les pages existantes dans `05-web-content/` pour calibrer le ton.
5. **Récupérer la matière source :**
   - Lire `01-brand/messaging-framework.md` — positionnement, formulations canoniques, chiffres clés.
   - Consulter `_templates/inventory.md` et scanner `05-web-content/` pour les pages similaires : structures qui ont fonctionné, sections réutilisables.
   - Piocher dans les archives des autres canaux (`04-email/newsletter/editions/`, `03-social-media/*/examples/`) les formulations validées et les accroches qui résonnent.
   - Chaque chiffre utilisé doit venir de `01-brand/messaging-framework.md`, de `_sources/reports/` ou d'une référence externe citée.

## Référence rapide du design system

| Élément | Valeur |
|---|---|
| Police principale | {{BRAND_FONT_PRIMARY}} |
| Couleur principale | `{{BRAND_COLOR_PRIMARY}}` |
| Accent | `{{BRAND_COLOR_ACCENT}}` |
| Sombre | `{{BRAND_COLOR_DARK}}` |
| Clair | `{{BRAND_COLOR_LIGHT}}` |
| Dégradé | `{{BRAND_GRADIENT}}` |
| Border-radius | {{BRAND_BORDER_RADIUS}} |
| Style d'illustration | {{BRAND_ILLUSTRATION_STYLE}} |

## Catalogue des templates de sections

Chaque landing page s'assemble à partir de sections modulaires :

| Section | Usage |
|---|---|
| Hero | Headline principale + sous-titre + CTA principal |
| Énoncé du problème | Points de douleur du persona |
| Solutions / Fonctionnalités | Proposition de valeur en 3-4 blocs |
| Preuve sociale | Logos clients, chiffres, témoignages |
| Timeline / Processus | Étapes du processus |
| Tableau comparatif | vs alternatives |
| Vitrine de chiffres | Gros chiffres |
| Témoignages | Citations avec portrait |
| FAQ accordéon | Questions fréquentes |
| Étude de cas | Résultats concrets |
| Pour qui | Blocs par persona |
| CTA final | Bloc de conversion avec dégradé |

**Séquence par défaut** : Hero → Problème → Solutions → Preuve sociale → Chiffres → Témoignages → FAQ → CTA final.

## Principes d'écriture

### La clarté avant la créativité

S'il faut choisir entre clair et malin, choisir clair. Chaque page répond à UNE question.

### La donnée en héros

Les chiffres sont l'élément visuel principal. Un gros chiffre vaut mieux qu'un paragraphe.

### Le bénéfice avant la fonctionnalité

« Trouvez le bon expert en 48 heures » > « Accès à notre réseau de 100+ experts »

### La précision avant le vague

« 8,8/10 de satisfaction (n=136) » > « Grande satisfaction »

### Scannable

- Un H2 par section
- 2-3 phrases max par paragraphe
- Blancs généreux
- Un CTA max par section
- Mobile-first (tester à 375px de large)

## Bilinguisme (le cas échéant)

{{BILINGUAL_RULES}}

## Personnalisations spécifiques à la marque

{{COPYWRITING_SPECIFIC_RULES}}

## Règles état de l'art (2026)

Synthèse actionnable — voir `docs/etat-de-lart/email.md` pour le détail sourcé :

1. **Structure descendante** : l'information la plus importante en premier, toujours. Aucun préambule institutionnel en ouverture (« Chez X, nous sommes fiers de… ») — la première phrase porte la promesse, la donnée ou la tension, le contexte vient après. Le contenu « entonne » vers le CTA : accroche → idée principale → preuve → CTA → secondaire.

## Checklist avant livraison

- [ ] Pages existantes relues pour calibrer le ton
- [ ] Une proposition de valeur claire par page
- [ ] La donnée en héros (chiffres visibles, pas enterrés)
- [ ] Chaque chiffre vérifié contre la doctrine de marque (`01-brand/messaging-framework.md`, `_sources/reports/`) ou source externe citée
- [ ] Scannable (titres, paragraphes courts, blancs)
- [ ] Un CTA clair et unique par section
- [ ] Design system respecté (couleurs, polices, border-radius)
- [ ] Pas de photos stock ({{BRAND_BANNED_VISUALS}})
- [ ] Vocabulaire de marque respecté
- [ ] Versions bilingues si applicable
- [ ] Rendu mobile testé
- [ ] Entrée du calendrier éditorial mise à jour (`02-strategy/calendar/calendar.md` — statut + lien livrable)
- [ ] Livrable indexé dans `_templates/inventory.md` (skill `inventory`, mode incrément)

## Skills associées

- `copy-editing` — relecture en 7 passes
- `image-generation` — visuels de page
- `seo` — optimisation on-page
- `brand-check` — validation finale obligatoire
