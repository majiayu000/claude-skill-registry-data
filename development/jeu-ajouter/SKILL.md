---
name: jeu-ajouter
description: Ajoute un ou plusieurs jeux à la collection du site (CSV PriceCharting, pochettes, données générées), à partir de titres ou d'une image/capture de la collection. Utilise le skill jeu-recherche pour trouver les ids. À utiliser quand l'utilisateur dit qu'il a acquis/ajouté des jeux à sa collection.
---

# Ajouter des jeux à la collection

Flux du projet (voir `docs/data-flow.md`) : `data/pricecharting/collection.csv` →
`npm run data:import` → `data/generated/games.json`; pochettes via `npm run covers:sync`
(télécharge `public/covers/pc-<id>.jpg`, cache dans `data/cache/covers.json`).

## Étapes
1. **Identifier les jeux** : invoque le skill `jeu-recherche` (titre ou image) pour obtenir
   l'id PriceCharting, le titre exact et la console de chaque jeu. Si l'entrée est une
   image, relève aussi l'état et le prix affiché.
2. **Vérifier les doublons** : cherche l'id dans `collection.csv` (`grep "^<id>,"`). Si le jeu
   est déjà là, ne l'ajoute pas (demande si c'est un 2e exemplaire).
3. **Ajouter les lignes** à la fin de `data/pricecharting/collection.csv`, format
   (colonnes : `id,product-name,console-name,price-in-pennies,include-string,condition-string,sku,notes,cost-basis-in-pennies,quantity,date-entered,date-purchased,grading-company,grading-cert-id,folder`) :
   ```
   19567,Dirt 2,Xbox 360,2154,"Item, Box, and Manual",,,,,1,2026-11-06,2026-11-06,,,
   ```
   - `price-in-pennies` : prix affiché × 100 (ex. C 21.54 → 2154) ; vide si inconnu.
   - `include-string` : CIB → `"Item, Box, and Manual"` ; boîte sans manuel →
     `"Item and Box"` ; loose → `"Item only"`.
   - `date-entered` / `date-purchased` : date du jour (AAAA-MM-JJ). `quantity` : 1.
4. **Retirer des recherchés (obligatoire, pour chaque jeu ajouté)** : vérifie si le jeu figure
   dans `data/pricecharting/wanted.csv`, par id (`grep "^<id>," wanted.csv`) **et** par titre
   (`grep -i "<mots-clés du titre>" wanted.csv`, car une ligne peut avoir un autre id ou aucun
   id). Si trouvé, supprime la ligne (ex. `sed -i '/^<id>,/d' wanted.csv`) et mentionne-le dans
   le message de commit et dans ton rapport à l'utilisateur. Un titre proche mais d'une autre
   édition (ex. `[Platinum Hits]` vs standard) : demande avant de supprimer.
5. **Pochettes et données** (réseau requis, ~1 s par jeu) :
   ```bash
   npm run covers:sync
   npm run data:import
   ```
   Contrôle `data/reports/missing-covers.csv` et `uncertain-cover-matches.csv` : un jeu ajouté
   ne doit pas y figurer ; sinon vérifie l'id.
6. **Valider** : `npm run validate` puis `npm test` (et `npm run build` si modif de code).
7. **Commit + push** (message en français, ex. « Ajoute N nouvelles acquisitions ») : ajoute
   `data/`, `public/covers/`. Pousse la branche et, si l'utilisateur veut publier sur GitHub
   Pages, assure-toi que ça arrive sur `main` (voir `.github/workflows`).

## Pièges connus
- Sans id, l'entrée reçoit un id `gen-<hash>` et n'a pas de pochette PriceCharting : toujours
  fournir l'id.
- Garder les éditions entre crochets telles que PriceCharting les écrit.
