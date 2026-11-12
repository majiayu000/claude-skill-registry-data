---
name: equilibrer
description: "Mesure l'équilibre d'un sujet du Rogue (la run en carte, ses portes et son plafond, le banc et ses pièces, le marché, le duel, l'élite, les histoires) avec les juges du dépôt, en paires, et propose un réglage chiffré. Ne change rien sans accord."
argument-hint: "[sujet : carte | portes | banc | marché | histoires | duel | run | <nom d'un coach ou d'une pièce>]"
user-invocable: true
---

# Équilibrer — le Rogue, mesuré

Le sujet : `$ARGUMENTS` (vide : la run et le banc, `mesure_run` puis `check_pouvoirs`).

## 1. Lire avant de mesurer

- `.claude/rules/rogue.md` : les bornes du sujet (les Coupes des trois robots sur 64 graines, la première Coupe du malin à la run 3 ou plus tard, la présence de 30 à 50 % d'une pièce et ses bornes sur un acte, les 60 % du duel, les bornes de l'élite, la borne en victoires d'une réponse d'histoire).
- `docs/refonte-v28-4.md` (« Le banc remesuré », « Ce qui reste ouvert ») et `docs/decisions.md` (« tu peux exploser le jeu ») : ce qui est déjà mesuré et ce qui reste ouvert. Les lignes d'équilibre de « À faire » dans `PLAN.md` datent de l'ancien Rogue.
- Le code du sujet : la constante qui le règle, son fichier. Les leviers de la run sont l'objet `RUN` de `js/run.js` (la cible `CIBLES` 7·8·9, le plafond `RACHAT`, les étapes d'édition `ETAPES`, les bandes, les jetons du marché) ; **2 ❤️** ne se règle pas (JP, 7 nov. 2026).

## 2. Choisir le juge le plus court qui répond

| Sujet | Juge | Le court | Le plein |
|---|---|---|---|
| run, carte, portes | `check_run` · `mesure_run` | `node scripts/check_run.mjs` (10 s) · `GRAINES=8 FILS=2 node scripts/mesure_run.mjs` (les bornes s'impriment sans se juger) | `GRAINES=64 FILS=3 node scripts/mesure_run.mjs` (cinq à six minutes ; jamais plus de 3 fils ici) ; `REGLAGES='{"RACHAT":0.6}'` essaie un levier de `RUN` sans toucher au code |
| banc, une pièce, un coach | `check_pouvoirs` · `check_relais` | `MESURE=0 N=20` (une demi-minute, sans les bornes) · `PIECES=a,b` | `FILS=3 node scripts/check_pouvoirs.mjs` (huit minutes) · `node scripts/check_relais.mjs` (deux minutes) |
| un moment (le `quand` d'une pièce) | `check_moments_si` | `node scripts/check_moments_si.mjs` (30 s) | le même |
| duel, élite | `check_duel` · `check_elites` | `N=200` · une seconde | `N=1200` (une minute) |
| marché | `check_packs` · `check_run` | une demi-minute · 10 s | `mesure_run` avec `REGLAGES` (les jetons d'un match, d'une porte passée) ; les robots y achètent une pièce, jamais une pochette : ce que vaut une pochette dans une run ne se mesure pas encore |
| histoires | `check_histoires` · `check_mots` · `check_effets` | quelques secondes · `IDS=d:<histoire>` pour cibler | `check_effets` (une vingtaine de minutes) |

Dis la commande et sa durée avant de la lancer. Plus de cinq minutes : demande d'abord. Un repère se juge sur plusieurs graines (64 pour `mesure_run` ; sous 32, rien ne se juge), jamais sur une seule. Un écart entre deux robots demande plus : à 64 graines un écart de Coupes a ±6 de bruit, à 128 un écart de cibles tenues ±7 ; « lire paie » et « exploser le jeu » se jugent à 384 (`GRAINES=384 FILS=3 ROBOTS=malin,chiffre node scripts/mesure_run.mjs`, une quinzaine de minutes). Un résultat au bord du bruit se rejoue sur des graines neuves avant de se proposer : le 11 nov. 2026, un levier « gagnant » sur 128 graines ne l'était plus sur les 128 suivantes.

## 3. Lancer et lire

`node scripts/<juge>.mjs` avec ses variables. Cite le verdict tel que `verdict.mjs` l'imprime : les lignes rouges, les chiffres contre leurs bornes.

## 4. Rapporter

En français québécois, avec les mots du vocabulaire :

```
## Équilibre — <sujet> (<date>, <commit>)

Mesuré : <commande> — <durée>, <N, graines>

| Ce qu'on mesure | Borne | Mesuré | État |
|---|---|---|---|
| <pièce, plan, levier de la run…> | <±V, Coupes sur 64…> | <mesuré [intervalle]> | sous la borne / au-dessus / mort / piège |

**Le problème** : <une phrase, chiffrée>
**Le réglage proposé** : `<CONSTANTE>` (<fichier>) de <avant> à <après> — effet attendu : <V, Coupes>
**La preuve** : <le juge, et ce qu'il doit dire après>
**À trancher par JP** : <s'il y a lieu>
```

« Mort » : ne se voit jamais dans la feuille d'un soir où il joue. « Piège » : le prendre fait perdre.

## 5. Appliquer, seulement si JP dit oui

Un réglage à la fois. Puis : `VERSION_MOTEUR` monté dans `js/game.js` si un match ne se rejoue plus pareil, et `EMPREINTE=ecrire node scripts/check_empreinte.mjs` ; le juge relancé ; `node scripts/tout.mjs` et `node scripts/check_mort.mjs` ; une entrée courte au journal de `LIVRAISON.md` (et dans `docs/journal/AAAA-MM.md`) ; une décision neuve dans `docs/decisions.md`.

Pour un avis de design (est-ce le fun, est-ce un vrai choix), passe la main à l'agent `rogue-design` ; pour l'argent de la run, à `rogue-economie`.
