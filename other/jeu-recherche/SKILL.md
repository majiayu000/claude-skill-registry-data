---
name: jeu-recherche
description: Identifie un jeu vidéo sur PriceCharting à partir d'un titre (ou d'une image/capture/liste où on lit des titres) et retourne l'id PriceCharting, le titre exact, la console et le prix. À utiliser avant d'ajouter un jeu à la collection (skill jeu-ajouter) ou quand l'utilisateur veut juste savoir quel id/prix correspond à un jeu.
---

# Recherche d'un jeu sur PriceCharting

Source unique du projet : PriceCharting (ids, titres, prix, pochettes).

## Entrée
Un titre, ou une image (capture de collection PriceCharting, photo de boîte). Pour une
image, lis visuellement chaque titre, console, état (CIB, loose…) et prix affiché.

## Étapes
1. Pour chaque jeu, lance (depuis la racine du dépôt) :
   ```bash
   npm run pc:search -- "<titre>" --console="Xbox 360" --limit=5
   ```
   Sortie : `id <TAB> titre <TAB> console <TAB> prix CIB`.
2. Choisis le candidat dont **le titre et la console correspondent exactement**
   (attention aux éditions entre crochets : `[Limited Edition]`, `[Platinum Hits]`,
   et aux versions PAL : `pal-…` n'est pas la version NTSC). Si le titre du
   candidat diffère de celui de l'utilisateur, utilise le titre PriceCharting.
3. Si aucun résultat : réessaie avec un titre plus court (sans sous-titre ni édition).
   Si toujours ambigu, **demande à l'utilisateur** plutôt que de deviner.
4. Dans une capture PriceCharting, le lien du titre pointe déjà vers la fiche : si
   l'utilisateur donne l'URL `…/game/<console>/<slug>`, ouvre-la pour lire l'id.

## Sortie attendue
Un tableau : titre saisi → id PriceCharting, titre exact, console, état, prix (si connu).
Signale tout doute (édition, région). Ne modifie aucun fichier : c'est le rôle de `jeu-ajouter`.
