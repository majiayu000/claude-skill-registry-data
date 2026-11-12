---
name: refonte
description: "Un gros changement demandé par JP (une refonte, « de zéro », « au complet », « pas juste la peinture ») mené pour qu'il en soit un : l'inventaire de ce qui existe, le devis avec ce qui part, le code réécrit plutôt que retouché, et check_refonte qui mesure que ce n'est pas une couche de peinture. À charger avant de lire le code."
argument-hint: "<le sujet : la carte | les portes | le banc | le marché | les histoires | le duel | la run | un module | …>"
user-invocable: true
---

# Refonte — un gros changement qui en est un

Le sujet : `$ARGUMENTS`.

JP (4 nov. 2026) : *ça fait une bonne vingtaine de fois qu'on retravaille le UI et retourne le même* ; *faut arrêter de juste changer la peinture*. La raison, mesurée (docs/decisions.md, « Un gros changement se mesure à ce qui part ») : devant « refais tout, de zéro », chaque session relisait l'existant, le retouchait fonction par fonction, et empilait du CSS dessus ; le diff minimal qui passait les juges. Un gros changement se juge à ce qui part et à ce qui est réécrit, jamais à ce qu'on ajoute par-dessus.

## 1. Ses mots, et la taille qu'il demande

Reprends les mots de JP en italique. S'il dit *refonte*, *de zéro*, *au complet*, *tout*, *pas juste la peinture*, la taille est décidée : on ne la négocie pas à la baisse en silence. Ce que tu peux faire, c'est lui dire en une ligne, AVANT de coder, ce que l'inventaire montre et ce que tu proposes, si tu crois qu'une refonte n'est pas la bonne réponse. Jamais une retouche livrée sous le nom d'une refonte.

## 2. L'inventaire de ce qui existe

Avant tout devis, la liste de ce qui fait le sujet aujourd'hui : les fichiers, les fonctions de rendu, les classes CSS, les blocs de l'écran, les constantes, en lignes (`wc -l`, Grep). C'est la matière qu'une refonte remplace ; sans la liste, on retouche ce qu'on a sous les yeux et on oublie le reste. Cherche aussi ce qui a déjà été essayé et retiré sur le sujet (docs/decisions.md : « essayé », « retiré », « parti », « écarté ») : on ne refait pas ce qui est mort.

## 3. Le devis, et ce qui part

Un devis sur le gabarit `docs/gabarits/devis.md`, jugé par `/revue-design` avant le code. Sa partie **« Ce qui part »** est la pièce maîtresse : chaque fonction, classe, bloc, fichier ou règle que la refonte remplace, nommé en `code`, avec ce qui le remplace. Le test du zéro : si le neuf peut s'écrire sans relire l'ancien ligne par ligne, c'est une refonte ; si chaque ligne du neuf répond à une ligne de l'ancien, c'est une retouche. « Ce qui reste » se nomme aussi, avec sa raison (les cartes du jeu restent telles quelles : JP, deux fois).

Pour un écran : des maquettes d'abord, à 390 × 844, en deux ou trois directions franchement différentes, et JP tranche sur les maquettes (c'est ainsi que le Rogue a enfin changé : la run en carte de la V28, sur `docs/maquettes/v28-ecrans.html`) ; le code reproduit la maquette choisie, il ne « s'en inspire » pas. Pour un système : les règles du jeu réécrites au complet dans le devis, pas un diff des règles d'avant.

## 4. Le code : réécrit, pas retouché

- Un module refait se repart d'un fichier neuf (ou vidé), avec les composants partagés qui existent (`js/util.js`, les cartes de `js/cartes.js` ; dans le Rogue, le HUD et les briques de `js/run-scenes.js`) ; l'ancien se supprime, il ne se commente pas.
- Pas de `body.mode-rogue` ni de classe « v2 » posée sur l'ancien composant : la surface se change à la source (interface.md). Dans le Rogue, le neuf ne s'appuie pas sur l'ancien : aucun module `js/run*.js` n'importe ni ne nomme un nom de « Ce qui part » de `docs/refonte-v28.md` — `check_neuf`.
- Les règles de `.claude/rules/` qui décrivaient l'ancien se réécrivent pour décrire le neuf (le 4 nov., les règles encodaient l'interface d'avant, et chaque session y revenait).
- Les clés de sauvegarde ne bougent pas (`check_sauvegardes`).

## 5. La mesure, avant la PR

`node scripts/check_refonte.mjs <le devis>` : le jeu (js/, index.html, sw.js) retire au moins une ligne pour deux qu'il ajoute, style.css fait moins de la moitié du diff, chaque nom de « Ce qui part » est parti, chaque fichier de « Ce qu'il touche » est dans le diff. Rouge : ce n'est pas encore une refonte ; on continue, on ne baisse pas la borne. Puis les juges du terrain : au Rogue, `check_scene` et `essai_run` (un serveur statique d'abord ; `node scripts/check_scene.mjs http://localhost:8000 <dossier>` laisse une capture par scène), `check_run` et `check_neuf` ; partout, `check_mort` et `tout.mjs`.

## 6. La PR

Son corps dit, en trois listes : **ce qui est parti**, **ce qui est neuf**, **ce qui est resté et pourquoi** ; puis la ligne du verdict de `check_refonte`. La décision va dans `docs/decisions.md` (le pourquoi, ce qui a été écarté), l'entrée au journal, un fichier neuf de `docs/journal/entrees/` (la règle en tête du journal de `LIVRAISON.md`).
