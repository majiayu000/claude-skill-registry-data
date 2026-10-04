---
name: cro-page
description: Optimiser la conversion d'une page marketing de {{COMPANY_NAME}} — homepage, landing page, page tarifs, page fonctionnalité, article. Analyse en 7 dimensions (proposition de valeur, headline, CTA, hiérarchie visuelle, preuve, objections, friction) et recommandations priorisées avec alternatives de copy. Utiliser quand l'utilisateur dit « CRO », « cette page ne convertit pas », « améliorer les conversions », « taux de rebond trop élevé », « revue de landing page » ou partage une URL pour feedback. Orchestrée par la skill landing-page pour la structure et la revue finale.
---

# cro-page — optimisation de conversion des pages

Adapté du plugin marketingskills (Corey Haines / fork Littlpinguin, MIT) — voir `docs/vendored-cro.md`.

## Étape 0 — Doctrine de marque (OBLIGATOIRE dès qu'un mot est produit)

Toute recommandation qui inclut du copy (headlines, CTA, alternatives) exige d'abord :

1. `01-brand/checklist-pre-composition.md` — voix, anti-style-IA, typographie, réutilisation.
2. `01-brand/voice.md` — position de voix, vocabulaire, interdits.
3. `01-brand/messaging-framework.md` — les chiffres et affirmations utilisables comme preuve.
4. `01-brand/personas.md` — le « langage client » de la dimension 1 vient de là.

Si un fichier manque ou contient des `{{...}}` : arrêter et lancer `/start-cockpit`. Un diagnostic pur (sans copy proposé) peut se faire sans, mais le signaler.

## Cadrage initial

1. **Type de page** : homepage, landing, tarifs, fonctionnalité, article, autre
2. **Objectif de conversion unique** : inscription, démo, achat, téléchargement, contact
3. **Contexte de trafic** : organique, payant, email, social — le message doit matcher la source

## Grille d'analyse — 7 dimensions, par ordre d'impact

### 1. Clarté de la proposition de valeur (impact maximal)
- Un visiteur comprend-il en 5 secondes ce que c'est et pourquoi s'y intéresser ?
- Bénéfice principal clair, spécifique, différencié ; formulé dans la langue du client (personas), pas dans le jargon de {{COMPANY_NAME}}
- Pièges : centré fonctionnalités au lieu de bénéfices ; trop vague ou trop malin ; tout dire au lieu de dire l'essentiel

### 2. Efficacité du headline
- Porte-t-il la proposition de valeur ? Est-il assez spécifique ? Matche-t-il le message de la source de trafic ?
- Patterns forts : orienté résultat (« Obtenez [résultat] sans [douleur] ») ; spécificité (chiffres, délais — sourcés doctrine) ; preuve sociale réelle

### 3. CTA — placement, copy, hiérarchie
- UNE action primaire claire, visible sans scroller, répétée aux points de décision
- Copy de bouton = valeur, pas juste action : ❌ « Envoyer », « En savoir plus » → ✅ « Démarrer l'essai gratuit », « Recevoir mon diagnostic »
- Hiérarchie primaire/secondaire lisible

### 4. Hiérarchie visuelle et scannabilité
- Le message principal passe-t-il en lecture diagonale ? Éléments importants proéminents ? Assez de blanc ? Les images servent-elles le message ?
- Contraintes : tokens `01-brand/style-guide.md` — jamais de recommandation visuelle hors marque

### 5. Preuve et signaux de confiance
- Logos clients, témoignages attribués (spécifiques, avec photo), extraits de cas avec chiffres réels, notes d'avis
- **Règle du template** : toute preuve chiffrée doit exister dans `01-brand/messaging-framework.md` ou une source citée — ne jamais recommander d'inventer de la preuve
- Placement : près des CTA et après chaque affirmation de bénéfice

### 6. Traitement des objections
- Prix/valeur, « est-ce pour mon cas ? », difficulté de mise en œuvre, « et si ça ne marche pas ? »
- Leviers : FAQ, garanties, comparatifs, transparence du process

### 7. Points de friction
- Formulaires trop longs (→ skill `cro-form`), étapes floues, navigation distrayante, expérience mobile, temps de chargement

## Spécificités par type de page

- **Homepage** : positionner pour le visiteur froid ; servir à la fois « prêt à acheter » et « en recherche »
- **Landing page** : message match avec la source ; CTA unique (retirer la navigation si possible) ; argument complet sur une page — structure de référence dans la skill `landing-page`
- **Page tarifs** : comparaison claire, plan recommandé signalé, lever l'anxiété « quel plan pour moi ? » (→ skill `cro-pricing`)
- **Article de blog** : CTA contextuels alignés sur le sujet, aux points d'arrêt naturels

## Format de sortie

1. **Quick wins** — changements faciles, impact immédiat probable
2. **Changements à fort impact** — plus d'effort, à prioriser
3. **Hypothèses à tester** — à A/B tester plutôt qu'à trancher d'instinct
4. **Alternatives de copy** — 2-3 variantes pour headline et CTA, avec rationale, conformes à la doctrine (étape 0)

Livrer dans `05-web-content/` (revue à côté de la page concernée) ou en réponse directe si diagnostic ponctuel. Tout copy proposé passe par `brand-check` avant intégration.

## Questions à poser si l'information manque

1. Taux de conversion actuel et objectif ? 2. D'où vient le trafic ? 3. Que se passe-t-il après cette page ? 4. Données disponibles (GA4, heatmaps, sessions) ? 5. Qu'avez-vous déjà tenté ?

## Skills associées

- `landing-page` — production complète d'une page (orchestre cette skill)
- `cro-form` / `cro-popup` — formulaires et popups de la page
- `cro-pricing` — page tarifs en profondeur
- `copywriting` — réécriture complète du copy
- `brand-check` — validation obligatoire avant intégration
