---
name: cro-form
description: Optimiser un formulaire de {{COMPANY_NAME}} — capture de lead, contact, demande de démo, inscription événement, devis. Maximise le taux de complétion en ne gardant que les champs qui servent vraiment, avec labels, messages d'erreur et bouton optimisés. Utiliser quand l'utilisateur dit « personne ne remplit le formulaire », « trop de champs », « optimiser le formulaire », « abandon de formulaire » ou « taux de complétion ». Orchestrée par les skills landing-page et lead-magnet.
---

# cro-form — optimisation de formulaires

Adapté du plugin marketingskills (Corey Haines / fork Littlpinguin, MIT) — voir `docs/vendored-cro.md`.

## Étape 0 — Doctrine de marque (OBLIGATOIRE dès qu'un mot est produit)

Labels, microcopy, messages d'erreur et copy de bouton sont du contenu de marque :

1. `01-brand/checklist-pre-composition.md` et `01-brand/voice.md` — ton, vocabulaire, interdits (un message d'erreur aussi a une voix).
2. `01-brand/personas.md` — le niveau de formalité et le vocabulaire des labels.

Si un fichier manque ou contient des `{{...}}` : arrêter et lancer `/start-cockpit`.

## Cadrage initial

1. **Type** : capture de lead (contenu gated, newsletter), contact, démo, inscription événement, devis, candidature
2. **État actuel** : nombre de champs, taux de complétion, répartition mobile/desktop, où les gens abandonnent
3. **Contexte** : que deviennent les soumissions ? quels champs sont réellement exploités ensuite (nurturing, CRM) ? contraintes RGPD ?

## Principes

### 1. Chaque champ a un coût
3 champs = référence ; 4-6 champs ≈ -10 à -25% de complétion ; 7+ ≈ -25 à -50%. Pour chaque champ : est-il indispensable **avant** de pouvoir aider la personne ? peut-on l'obtenir autrement (enrichissement, domaine de l'email) ? peut-on le demander plus tard (profilage progressif) ?

### 2. La valeur doit dépasser l'effort
Proposition de valeur claire au-dessus du formulaire ; ce qu'on obtient est évident ; effort perçu réduit (peu de champs, labels courts, « 30 secondes »).

### 3. Réduire la charge cognitive
Une question par champ ; labels clairs et conversationnels ; ordre logique (facile d'abord — nom, email — sensible en dernier — téléphone, budget) ; valeurs par défaut intelligentes.

## Règles champ par champ

| Champ | Règles |
|---|---|
| Email | champ unique, validation inline, détection de typo (gmial.com ?), clavier mobile adapté |
| Nom | un seul champ « Nom » sauf si la personnalisation exige prénom/nom séparés |
| Téléphone | optionnel si possible ; si requis, expliquer pourquoi |
| Entreprise | envisager l'inférence depuis le domaine email ou l'enrichissement post-soumission |
| Message libre | optionnel, extensible au focus |
| Select | < 5 options → boutons radio ; beaucoup d'options → recherche ; toujours une option « Autre » |

## Layout

- **Une colonne** (complétion supérieure, mobile-friendly) ; deux colonnes uniquement pour des champs courts liés
- **Labels toujours visibles** — jamais le placeholder seul (il disparaît à la saisie) ; placeholder = exemple, pas label
- Bouton immédiatement après le dernier champ, contrasté (tokens `01-brand/style-guide.md`), cibles tactiles ≥ 44 px
- **Multi-étapes si > 5-6 champs** : indicateur de progression, facile d'abord, retour possible, données conservées

## Erreurs

- Validation inline au passage au champ suivant (pas agressive pendant la frappe)
- Message spécifique + comment corriger, près du champ, dans la voix de la marque : ✅ « Cet email semble incomplet — il manque le @ » ❌ « Entrée invalide »
- À la soumission : focus sur le premier champ en erreur, **jamais** vider la saisie

## Bouton

Copy = **[action] + [ce qu'on obtient]** : « Recevoir le guide », « Réserver ma démo », « Obtenir mon estimation » — jamais « Envoyer »/« Soumettre ». États : chargement (bouton désactivé + indicateur), succès (confirmation + prochaine étape), erreur claire.

## Confiance

Près du formulaire : mention de confidentialité (« Jamais partagé, désindexation en un clic »), délai de réponse attendu, témoignage si pertinent. RGPD : consentement explicite, cases jamais pré-cochées, lien politique de confidentialité.

## Mesure

Suivre (GA4 / outil configuré via `/tools-setup`) : taux de démarrage (vues → premier focus), taux de complétion (démarré → soumis), abandon par champ, erreurs par champ, mobile vs desktop.

## Format de sortie

1. **Audit** : par problème — constat, impact estimé, correctif, priorité
2. **Formulaire recommandé** : champs requis justifiés un à un, champs optionnels, ordre, labels + placeholders + messages d'erreur + copy du bouton (conformes doctrine), notes de layout
3. **Hypothèses A/B** : ex. email seul vs email + nom ; avec/sans téléphone ; monopage vs multi-étapes

Le circuit complet formulaire → n8n → outil emailing → nurturing est défini dans la skill `lead-magnet`.

## Skills associées

- `lead-magnet` — circuit de capture complet
- `cro-page` / `cro-popup` — la page ou le popup qui contient le formulaire
- `landing-page` — production de la page
- `brand-check` — validation du microcopy avant intégration
