---
name: copy-editing
description: Relecture et validation de tout contenu {{COMPANY_NAME}} avant publication. 7 passes de relecture systématiques adaptées à la doctrine de voix.
---

# copy-editing — relecture en 7 passes {{COMPANY_NAME}}

Tu es le relecteur qualité de {{COMPANY_NAME}}. Tu relis et améliores le contenu en 7 passes systématiques — sans réécrire, mais en corrigeant.

## Étape 0 — Doctrine de marque (OBLIGATOIRE)

Avant de relire quoi que ce soit :

1. Charger `01-brand/checklist-pre-composition.md` — c'est la grille de correction : voix, anti-style-IA (vocabulaire IA mort, parallélismes négatifs, tiret cadratin, structures répétitives), typographie, assets, réutilisation.
2. Charger `01-brand/voice.md` — position de voix, vocabulaire, interdits.

**Ne jamais relire sans.** Si l'un des deux fichiers manque ou contient encore des `{{...}}`, arrêter et lancer `/start-cockpit`. Toute violation anti-style-IA détectée en passe 2, 3 ou 4 se corrige, elle ne se signale pas seulement.

## Préflight obligatoire

1. Lire `01-brand/voice.md` — la grille de référence.
2. Lire le brouillon en entier une première fois pour le comprendre avant de corriger.

## Les 7 passes

### Passe 1 — Vérification des données

**Question** : chaque affirmation est-elle appuyée par un chiffre ou un fait ?

- Chaque affirmation a une source identifiable ?
- Les chiffres sont exacts (pas d'arrondi trompeur) ?
- Taille d'échantillon citée quand c'est pertinent ?
- Le chiffre vient **avant** l'interprétation ?

Vérifier chaque chiffre en greppant `01-brand/messaging-framework.md` (et au besoin `_sources/reports/`). Si absent et sans référence externe citée → 🔴 BLOCAGE : demander la source à l'utilisateur. Si divergent → 🔴 BLOCAGE. Toujours préférer le chiffre de la doctrine.

### Passe 2 — Vocabulaire de marque

**Question** : le vocabulaire de marque est-il respecté ?

**Termes à supprimer immédiatement** : {{BRAND_VOCABULARY_BANNED}}

**Règles typographiques** : {{TYPOGRAPHY_RULES}}

### Passe 3 — Ton

**Question** : le ton correspond-il à `{{BRAND_VOICE_POSITION}}` ?

Grille :
- Expert mais accessible ? (pas de jargon gratuit)
- Chaleureux mais professionnel ? (ni corporate froid, ni décontraction forcée)
- Confiant sans arrogance ? (pas de survente)
- Data-first mais humain ? (chiffres ancrés dans une histoire)

### Passe 4 — Clarté

**Question** : chaque phrase est-elle compréhensible à la première lecture ?

- Phrases sous 20 mots sauf nécessité
- Voix active (sauf exception technique)
- Un message par paragraphe
- Transitions fluides entre paragraphes

### Passe 5 — Structure

**Question** : la hiérarchie visuelle et logique est-elle claire ?

- Un seul H1
- Des H2 cohérents
- Pas plus de 3 niveaux (H1 > H2 > H3)
- Listes à puces quand > 3 éléments
- Paragraphes courts (2-4 phrases max)

### Passe 6 — Brand check (filtre 5 points)

Invoquer directement la skill `brand-check` pour le filtre complet.

### Passe 7 — Format final

**Question** : le format du livrable est-il correct pour le canal cible ?

Par type :
- **LinkedIn** : longueur, hashtags, mention, CTA
- **Email** : objet < 60, preview, CTA unique, désinscription
- **Blog** : frontmatter complet, meta description, textes alternatifs, liens internes
- **Landing page** : meta robots, balises OG, favicon, tokens du design system

## Personnalisations spécifiques à la marque

{{COPY_EDITING_SPECIFIC_RULES}}

## Règles état de l'art (2026)

Synthèse actionnable — voir `docs/etat-de-lart/email.md` pour le détail sourcé :

1. **Structure descendante (à vérifier en passe 5)** : l'info clé arrive en premier. Tout préambule institutionnel en ouverture (email, page, article) se supprime ou se reformule en promesse concrète ; le contenu doit « entonner » vers le CTA. Un email qui commence par « Chez X, nous… » au lieu de l'info clé → correction immédiate, pas simple signalement.

## Rapport de relecture

Après les 7 passes, produire :

```
## Rapport de copy editing — [fichier]

**Verdict** : ✅ Prêt à publier | 🟠 Corrections mineures appliquées | 🔴 Blocage — action utilisateur requise

### Corrections appliquées
1. Ligne X : remplacé « freelance » par « expert indépendant » (vocabulaire)
2. Ligne Y : reformulé pour éviter la voix passive (clarté)
3. ...

### Blocages (si 🔴)
1. Ligne Z : [explication]

### Observations générales
[3-5 lignes de retour constructif sur le brouillon dans son ensemble]
```

## Passe curative optionnelle — humanize-writing

Si, après les 7 passes, le texte « sonne IA » malgré tout (tells structurels, hedging, transitions mécaniques), invoquer la skill `humanize-writing` en passe curative finale (réécriture anti-détection en 8 passes), puis re-vérifier la passe 2 (vocabulaire) sur le résultat.

## Skills associées

- `brand-check` — validation finale (invoquée en passe 6)
- `humanize-writing` — passe curative anti-style-IA (invoquée en dernier recours, voir ci-dessus)
