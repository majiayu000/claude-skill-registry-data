---
name: rapport-essai
description: "Transforme les notes d'essai de JP (une partie de Sur glace ou une run du Rogue, ses reproches tels quels) en rapport : chaque reproche ramené à sa cause dans le code, une correction, et le check qui la prouvera. À utiliser après une session de jeu."
argument-hint: "[glace | rogue] <les notes de JP, telles quelles>"
user-invocable: true
---

# Rapport d'essai

Les notes : `$ARGUMENTS`. Le premier mot dit le mode (`glace` ou `rogue`) ; sinon, devine-le des notes et dis-le.

## 1. Garder les mots de JP

Chaque reproche se cite tel quel, en italique, comme le journal le fait (JP : *ça feel zéro comme patiner*). Un reproche vague (« c'est laid ») se garde aussi : c'est à toi de le préciser en regardant le code et les images, pas à JP de le reformuler.

## 2. Lire le terrain

- Sur glace : `.claude/rules/sur-glace.md`, `docs/sur-glace.md` (ce qui est fait, partiel, à faire) et les entrées « Sur glace » de `docs/journal/2026-11.md` — un reproche qui revient après une correction le dit.
- Rogue : `.claude/rules/rogue.md`, `.claude/rules/interface.md` (« Le Rogue : des scènes, jamais des pages »), la dernière `docs/refonte-v*.md` (aujourd'hui `docs/refonte-v28.md` et ses extraits ; `docs/refonte-v28-4.md` dit ce qui est parti avec l'ancien Rogue), les maquettes `docs/maquettes/v28-ecrans.html`.

## 3. Ramener chaque reproche à sa cause

Pour chacun : le fichier, la fonction ou la constante qui le fait, et pourquoi (au Rogue : la règle dans `js/run.js` et son objet `RUN`, la scène dans `js/run-scenes.js`, le geste dans `js/run-jeu.js`, une pièce dans `js/pieces.js`). Lis le code ; ne devine pas. Si tu ne trouves pas la cause, dis-le et propose comment la trouver (une mesure, une image, une question à JP).

Range-les par domaine (Sur glace : le patin, la lame, le jeu physique, le gardien, les règles, l'IA, l'image, le son ; Rogue : le soir — la feuille, le match, le duel ; la semaine — la carte, les portes, l'échange ; l'acte — la cible, le rival, les arrêts ; la run — le banc, les cœurs, les séries ; l'économie — les jetons, le marché, le plafond ; les scènes).

## 4. Le rapport

```
## Essai — <mode>, <date>

| # | JP | La cause | La correction | La preuve | Qui |
|---|---|---|---|---|---|
| 1 | *<ses mots>* | <fichier · constante ou fonction> | <le réglage, en vraies unités> | <check existant, ou à écrire> | <agent> |

**Par où commencer** : <les deux ou trois qui paient le plus, et pourquoi>
**Ce qui revient** : <les reproches déjà « corrigés » au journal, s'il y en a>
**À trancher par JP** : <les choix de goût>
```

« Qui » nomme l'agent qui s'en charge : `glace-sensations`, `glace-ia`, `glace-graphiste`, `glace-son`, `glace-perf` ; `rogue-design`, `rogue-equilibre`, `rogue-economie`, `rogue-ux` (une scène, un parcours, ce qui ne répond pas), `rogue-recit` (une histoire, une voix). « La preuve », au Rogue : `check_run` (une règle de la run), `check_scene` (une scène), `essai_run` (un parcours au doigt), `mesure_run` (la difficulté), `check_pouvoirs` (une pièce de banc).

## 5. Ensuite

Ne corrige rien dans cette commande : le rapport sert à choisir. Si JP dit « go », les corrections partent une par une, chacune avec son check et son entrée courte au journal.
