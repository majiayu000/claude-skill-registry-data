---
name: revue-design
description: "Juge un devis du Rogue (une refonte docs/refonte-v*.md, un écran, un système, une histoire) avant qu'on le code : complet, cohérent avec les règles fermes, faisable, et prouvable. Fait relire par les agents du terrain en adversaires, rend un verdict. Ne change rien sans accord."
argument-hint: "<chemin du devis, ou le sujet : carte | portes | banc | marché | histoires | duel | run>"
user-invocable: true
---

# Revue de design — un devis jugé avant le code

Le devis : `$ARGUMENTS`. Un chemin se lit ; un sujet se cherche dans la dernière `docs/refonte-v*.md` (aujourd'hui `docs/refonte-v28.md`, la run en carte, et ses extraits `docs/refonte-v28-<n>.md`).

Adapté de la commande `/design-review` de Claude-Code-Game-Studios (Donchitos, licence MIT : https://github.com/Donchitos/Claude-Code-Game-Studios), ramené au gabarit de ce dépôt (`docs/gabarits/devis.md`).

## 1. Les neuf parties

Un devis complet a ses neuf parties (le gabarit les nomme) : **ce que JP a dit** (ses mots, en italique), **ce que le joueur ressent** (le fantasme, le pic visé), **les règles du jeu** (assez précises pour qu'un autre les code sans deviner), **les chiffres** (chaque formule avec ses variables, leur plage et un exemple fait), **les cas limites** (le banc plein, personne qui tienne sous le plafond, le joueur parti, la vieille partie, les séries), **ce qu'il touche** (les fichiers, les règles fermes de `.claude/rules/`, les clés de sauvegarde qui ne bougent pas), **ce qui part** (chaque fonction, classe, bloc ou fichier remplacé, nommé en `code`, et ce qui reste avec sa raison), **les réglages** (les constantes, leur plage sûre) et **les critères d'acceptation**. Une partie manquante se nomme ; elle ne se devine pas. Un devis qui répond à un gros changement de JP (*refonte*, *de zéro*, *au complet*, *pas juste la peinture* ; CLAUDE.md, « Un gros changement ») avec « Ce qui part » vide ou sans nom en `code` est **À REFAIRE** : c'est le devis d'une retouche.

## 2. Les critères se prouvent

Chaque critère est vérifiable par un script nommé, existant ou à écrire : « une pièce se lit 30 à 50 % des soirs — `check_pouvoirs` », « la feuille du soir ne défile pas à 390 × 844 — `check_scene` », « une semaine gagnée : neuf touchers au plus — `essai_run` », « le malin gagne la Coupe 4 à 12 fois sur 64 — `mesure_run` ». Les phrases « plus le fun », « bien balancé », « plus clair » sont refusées telles quelles : traduis-les en un chiffre et une mesure, ou marque-les « à juger par JP à l'essai ».

## 3. Les règles fermes et les décisions

Pour chaque règle de `.claude/rules/rogue.md`, `interface.md` et `vocabulaire.md` que le devis touche : la nommer, lire sa décision dans `docs/decisions.md` (Grep), et dire si le devis la défait (alors JP tranche) ou la respecte. Cherche aussi ce qui a déjà été essayé et retiré (« essayé », « retiré », « parti ») sur le même sujet.

## 4. Les relecteurs en adversaires

Selon le terrain, fais relire en parallèle (l'outil Agent, un message, plusieurs appels), chacun avec le devis et la consigne de **chercher ce qui casse**, pas de l'approuver :

| Le devis touche | Les relecteurs |
|---|---|
| une scène, un parcours, une mise en scène | `rogue-ux`, `rogue-design` |
| une histoire, une voix, une réplique | `rogue-recit`, `rogue-equilibre` |
| une pièce de banc, un coach, le duel, l'élite | `rogue-equilibre`, `rogue-design` |
| les jetons, le marché, le plafond, les médailles | `rogue-economie`, `rogue-design` |
| la carte, les portes, la courbe d'une run | `rogue-design`, `rogue-economie`, `rogue-equilibre` |

## 5. Le verdict

```
## Revue — <devis>, <date>

**Verdict** : APPROUVÉ | À REPRENDRE | À REFAIRE
| Partie | État | Ce qui manque |
|---|---|---|
| … | ✓ / à préciser / absent | … |

**Ce qui casse** (des relecteurs, triés du plus grave) : …
**Les règles fermes touchées** : <règle> — respectée / défaite (décision : …)
**Les critères sans preuve** : …
**Ce qui part** : <n> noms, ou vide (alors une retouche, pas une refonte) — `check_refonte`
**À trancher par JP** : une ligne chacun
```

Tu ne modifies rien. Si JP dit « go », les corrections du devis partent dans le devis lui-même, puis le code, tranche par tranche.
