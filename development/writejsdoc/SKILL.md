---
name: writeJsDoc
description: Write or update duplojs-utils JSDoc documentation files under jsDoc/{namespace}/{function}/, including index.md structure, @example includes, and example.ts usage patterns (classic, curried, and predicate overloads).
---

# JSDoc du projet

## Emplacement des fichiers

- `jsDoc/{namespace}/{function}/index.md`: contenu JSDoc de la fonction.
- `jsDoc/{namespace}/{function}/example.ts`: exemples utilises par les balises `{@include ...}`.

## Structure obligatoire de `index.md`

Respecter l'ordre exact:

1. Description de la fonction:
   - 1.1 Description courte
   - 1.2 Description des styles d'appel supportes (classique et currifie)
   - 1.3 Description du comportement
2. Exemple d'utilisation (utiliser `{@include ...[lineStart,lineEnd]}`)
3. `@remarks` (optionnel)
4. `@see` au moins un lien vers la doc en ligne version EN
5. `@namespace` ajouter le namespace de référence (domain Array === A, Clean === C, DataParser === DP ou DPE, etc.). Exception : le domaine common n’a pas de namespace (import depuis la racine de la lib). (ce fier au fichier `scripts/index.ts`)
 
## Regles pour `example.ts`

- Les exemples doivent etre importes via la balise `{@include namespace/function/example.ts[lineStart,lineEnd]}`.
- `example.ts` doit contenir au moins 3 exemples couvrant les cas courants.
- Eviter d'ajouter du bruit: chaque exemple doit rester simple et didactique.
- Utiliser `@scripts` pour les imports dans les exemples JSDoc (comme dans les exemples du projet).
- Si la doc est deja ecrite, s'inspirer des exemples dans `docs/examples/v1/api/` pour composer les cas JSDoc.
- L'objectif des exemples JSDoc est de montrer un panel d'usage tres simple (pas de cas complexes).

## Overloads predicate

Certaines fonctions ont des overloads predicate (classique + currifie):

- Le mentionner dans la description courte et dans la section des styles d'appel.
- Ajouter un exemple `if` pour la version predicate classique.
- Ajouter un exemple `pipe + when` pour la version predicate currifiee.

## Templates disponibles

- `assets/index-template.md`
- `assets/example-template.md`
