---
name: google-forms-builder
description: "Crée des formulaires Google Forms (COBACAM et autres): structure en markdown pour création manuelle, ou génération via Google Apps Script. Utiliser pour concevoir ou générer un formulaire, recensement, inscription, sondage, ou si Google Forms ou Apps Script est mentionné."
---

# Google Forms Builder

Crée des formulaires Google Forms, surtout pour la communauté COBACAM, selon deux modes: conception structurelle (manuel) ou génération programmatique (Apps Script).

## Choisir le mode

- **Manuel (structure markdown)**: formulaire simple (moins de 10 questions) ou ponctuel, utilisateur qui préfère l'interface Google Forms, pas d'automatisation. Produire un markdown complet: titre, description, champs avec types exacts, options, champs obligatoires, validations, paramètres recommandés (barre de progression, message de confirmation), sections. Gabarit de sortie: `references/modes-et-scripts.md`.
- **Apps Script FormApp**: formulaire complexe ou répétitif, automatisation souhaitée, utilisateur à l'aise avec le code. Base: `scripts/create_form_complete.gs`.
- **Apps Script API REST**: images dans les questions, choix mélangés, quiz sophistiqué, notifications Pub/Sub, mises à jour groupées. Base: `scripts/create_form_api.gs` (exige un projet GCP, voir `references/modes-et-scripts.md`).

## Références

- `references/question_types.md`: types de questions, syntaxe FormApp et API REST, validations, limites. Lire avant de générer du code.
- `references/best_practices.md`: conception de formulaires communautaires, structures COBACAM ("Types de formulaires récurrents"), logique conditionnelle, LPRPDE, checklist de publication. Lire avant de concevoir un formulaire COBACAM.
- `references/modes-et-scripts.md`: gabarit markdown, fonctions des scripts, configuration GCP et scopes, exemples, message WhatsApp d'accompagnement.

## Workflow

1. Demander les détails du formulaire, puis choisir le mode.
2. Manuel: consulter `best_practices.md`, écrire la structure, donner les instructions de création.
3. Apps Script: lire le script de base et `question_types.md`, adapter le code, fournir le code complet avec instructions d'utilisation.
4. COBACAM: identifier le type (recensement, appel à participation, sondage), appliquer la structure type, puis vérifier la checklist finale de `best_practices.md`.

## Règles COBACAM

COBACAM est une communauté camerounaise au Canada. Les formulaires sont:
- en français canadien, avec la typographie canadienne-française
- accompagnés d'une déclaration de confidentialité conforme à la LPRPDE et d'une case de consentement
- de ton professionnel mais chaleureux, adaptés à une diffusion par WhatsApp (message type dans `references/modes-et-scripts.md`)

## Notes

- Valider les champs courriel avec la validation appropriée.
- Un formulaire court est mieux rempli. Tester sur mobile avant publication.
- Lier une feuille de réponses Google Sheets pour l'analyse.
- Respecter les limites de Google Forms (`references/question_types.md`).
