---
name: design-direction
description: Direction artistique distinctive pour les livrables web de {{COMPANY_NAME}} — choix esthétiques délibérés (typographie, palette, layout, signature visuelle) qui ne ressemblent pas à un template ni à du « design généré par IA ». Utiliser au moment de concevoir l'apparence d'une nouvelle page (landing, page événement, page campagne), quand un livrable « fait template » ou « fait IA », ou en amont de design-system pour poser une intention. Vendorisée depuis frontend-design d'Anthropic (Apache-2.0) — voir docs/vendored-design.md.
---

# design-direction — une identité visuelle qu'on ne peut confondre avec aucune autre

Abordez chaque brief comme le lead designer d'un petit studio réputé pour donner à chaque client une identité visuelle impossible à confondre avec celle d'un autre. Le client a déjà rejeté des propositions qui « faisaient template » : il paie pour un point de vue. Faites des choix délibérés et assumés de palette, typographie et layout, spécifiques à ce brief — et prenez un vrai risque esthétique que vous savez justifier.

## Étape 0 — Charger les design tokens de la marque (OBLIGATOIRE)

**Charger `01-brand/style-guide.md` — la marque PRIME sur tout style générique de cette skill.**

1. Lire `01-brand/style-guide.md` (couleurs, police, radius, gradient, style d'illustration, interdits visuels) et `01-brand/voice.md` (la voix nourrit la direction).
2. La direction artistique s'exerce **dans l'espace laissé libre par la marque** : la marque fixe les matériaux (couleurs, police), vous composez l'architecture (hiérarchie, rythme, layout, signature, motion). Un choix « distinctif » qui contourne un token de marque est une faute, pas de l'audace.
3. Si la marque possède déjà une signature visuelle (gradient, motif, style d'illustration), c'est le premier candidat pour l'élément signature de la page — l'amplifier avant d'inventer.
4. Lire `01-brand/design-anti-generique.md` — doctrine design anti-générique : marqueurs du look IA interdits par défaut et pratiques pro, applicables dans l'espace laissé libre par la marque.

Si `01-brand/style-guide.md` est manquant ou contient des `{{...}}` : s'arrêter et proposer `/start-cockpit`.

## Ancrer le design dans le sujet

Si le brief ne précise pas le produit ou le sujet, le fixer vous-même avant de dessiner : nommer un sujet concret, son audience, et l'unique mission de la page — et l'énoncer. L'univers propre du sujet — ses matériaux, ses instruments, ses artefacts, son vocabulaire — est la source des choix distinctifs. Construire avec le vrai contenu du brief, jamais avec du lorem ipsum mental.

## Principes de design

**Le héros est une thèse.** Ouvrir avec la chose la plus caractéristique de l'univers du sujet, sous la forme qui lui convient : un titre, une image, une animation, une démo, un moment interactif. Le « gros chiffre + petit label + stats de soutien + accent en gradient » est la réponse template — ne l'utiliser que si c'est réellement la meilleure option.

**La typographie porte la personnalité de la page.** Sous contrainte de `{{BRAND_FONT_PRIMARY}}` : travailler l'échelle, les graisses, les chasses et l'espacement pour que le traitement typographique soit mémorable en lui-même, pas un simple véhicule neutre du contenu. Si la marque autorise une police display complémentaire, la choisir pour ce brief précis (voir `design-system/references/typographie.md`), pas par habitude.

**La structure est de l'information.** Les dispositifs structurels — numérotation, eyebrows, filets, labels — doivent encoder quelque chose de vrai sur le contenu, pas le décorer. Les marqueurs numérotés (01 / 02 / 03) ne se justifient que si le contenu est réellement une séquence. Questionner chaque dispositif avant de l'adopter.

**Le mouvement est un choix, pas un réflexe.** Se demander où l'animation sert le sujet : séquence d'arrivée, révélation au scroll, micro-interactions, atmosphère. Un moment orchestré marque plus que des effets dispersés. Parfois, moins c'est mieux : l'animation excessive contribue précisément à l'impression « généré par IA ».

**La complexité doit égaler la vision.** Une direction maximaliste exige une exécution élaborée ; une direction minimale exige une précision extrême d'espacement, de typo et de détail. L'élégance, c'est d'exécuter la vision choisie au niveau qu'elle demande.

**Le texte fait partie du design.** Si le brief ne fournit pas de contenu réel, le copy que vous écrivez peut rendre une page aussi template que son design. Aller chercher `01-brand/messaging-framework.md` et la skill `copywriting` — jamais de texte de remplissage générique.

## Anti-défauts : les trois looks « IA » à ne pas produire par réflexe

Le design généré par IA se concentre aujourd'hui autour de trois looks :

1. fond crème chaud (proche `#F4F1EA`) + serif display à fort contraste + accent terracotta ;
2. fond quasi-noir + un seul accent vert acide ou vermillon ;
3. layout « broadsheet » : filets hairline, radius zéro, colonnes denses façon journal.

Les trois sont légitimes pour certains briefs, mais ce sont des **défauts**, pas des choix : ils apparaissent quel que soit le sujet. Là où le brief (ou la marque) fixe une direction, la suivre exactement — les mots du brief gagnent toujours, y compris s'ils demandent un de ces looks. Là où un axe reste libre, ne pas dépenser cette liberté sur un de ces défauts.

## Processus : brainstormer, explorer, planifier, critiquer, construire, re-critiquer

Travailler en deux passes.

**Passe 1 — plan de design compact** à partir du brief :
- **Couleur** : la palette effective (tokens de marque + dérivés), 4-6 valeurs nommées, avec le rôle de chacune.
- **Typo** : les rôles (display avec caractère utilisé avec retenue, corps complémentaire, utilitaire pour légendes/données si besoin) sous contrainte de la marque.
- **Layout** : un concept, décrit en une phrase + wireframe ASCII pour comparer 2-3 options.
- **Signature** : l'élément unique par lequel cette page sera mémorisée, incarnation du brief — de préférence dérivé de la signature de marque existante.

**Passe 2 — critique du plan avant d'écrire le code** : si une partie du plan ressemble au défaut générique que vous produiriez pour n'importe quelle page similaire (dérouler mentalement un brief voisin : arrivez-vous au même endroit ?), réviser cette partie et dire ce qui a changé et pourquoi. Ne coder qu'après avoir confirmé l'unicité relative du plan — puis le suivre exactement, chaque décision de couleur et de type découlant du plan.

À l'écriture du code : attention aux spécificités CSS qui s'annulent (sélecteur de type `.section` vs sélecteur d'élément `.cta`), surtout sur les paddings/margins entre sections.

Mener l'essentiel de cette itération en réflexion interne ; ne montrer à l'utilisateur que des pistes à haut niveau de confiance.

## Retenue et auto-critique

Dépenser l'audace à un seul endroit. Laisser l'élément signature être la chose mémorable, garder tout le reste calme et discipliné, couper toute décoration qui ne sert pas le brief. Ne pas prendre de risque est aussi un risque. Construire sur un socle de qualité sans l'annoncer : responsive jusqu'au mobile, focus clavier visibles, `prefers-reduced-motion` respecté. Se critiquer en construisant — prendre des captures d'écran si l'environnement le permet (une image vaut mille tokens). Et le conseil de Chanel : avant de sortir, un regard au miroir, et retirer un accessoire.

Consigner en fin de projet ce qui a été tenté (signature, palette dérivée, concept de layout) dans le dossier du livrable — les designers humains ont de la mémoire et cherchent à ne pas se répéter ; ces notes servent l'anti-répétition des prochaines pages.

## Écrire dans le design

Les mots n'apparaissent dans un design que pour une raison : rendre la page plus facile à comprendre, donc à utiliser. Le copy est un matériau de design, pas une décoration.

- Écrire du point de vue de l'utilisateur : nommer les choses par ce que les gens contrôlent et reconnaissent, jamais par la mécanique interne.
- Voix active par défaut : un bouton dit exactement ce qui se passe (« Enregistrer les modifications », pas « Soumettre ») ; une action garde le même nom sur tout le parcours (« Publier » → toast « Publié »).
- Erreurs et états vides sont des moments de direction, pas d'ambiance : expliquer ce qui s'est passé et comment corriger, sans excuse ni vague.
- Registre conversationnel et réglé : verbes simples, pas de remplissage, ton aligné sur `01-brand/voice.md`. Chaque élément fait exactement un travail.

## Enchaînement avec les autres skills

| Moment | Skill |
|---|---|
| Formaliser les tokens issus de la direction retenue | `design-system` |
| Écrire le copy réel de la page | `copywriting` |
| QA finale (marque, a11y, responsive, perf) | `design-review` |
| Validation éditoriale avant livraison | `brand-check` |

---

*Source : adapté de la skill [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) d'Anthropic (plugin officiel Claude Code), licence Apache-2.0. Adaptations : traduction française, ajout de l'étape 0 de chargement des tokens 01-brand (la marque prime), ancrage dans le workflow du template (copywriting, design-system, design-review, brand-check), notes anti-répétition dans le dossier livrable. Registre : `docs/vendored-design.md`.*
