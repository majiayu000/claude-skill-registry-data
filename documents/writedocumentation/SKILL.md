---
name: writeDocumentation
description: Write or update duplojs-utils documentation pages (FR/EN) including API function pages, namespace index pages, and guides, following the repo's structure, MonacoTSEditor examples, required sections, and prev/next metadata.
---

# Documentation du projet

## Identifier le type de page

- Utiliser ces chemins comme source de verite.
- Choisir le format de page avant de rediger.
- Toujours maintenir la doc dans les deux langues (FR et EN) et garder les sections synchronisees.

Chemins:

- `docs/{fr,en}/index.md`: pages home.
- `docs/{fr,en}/v1/guide/*.md`: guides.
- `docs/{fr,en}/v1/api/{namespace}/index.md`: sommaire + presentation du namespace.
- `docs/{fr,en}/v1/api/{namespace}/{function}.md`: documentation d'une fonction.
- `docs/{fr,en}/v1/api/{namespace}/{concept + function}.md`: cas specifiques (rare).
- `docs/examples/v1/api/{namespace}/{function}/tryout.doc.ts`: exemple simple.
- `docs/examples/v1/api/{namespace}/{function}/otherExample.doc.ts`: cas specifiques.

## Respecter les regles des exemples

- Ecrire les commentaires en anglais.
- Utiliser des noms de variables de plus de 2 caracteres.
- Wrapper les structures avec plus d'un element (retours a la ligne, un element par ligne).
- Utiliser `foldLines` dans `MonacoTSEditor` pour replier du code long si besoin.
- Le `height` depend du nombre de lignes visibles: `(nbLines * 21px) + 30-50px de marge`.
- Compter une ligne pliee comme une seule ligne visible.
- Les index `foldLines` commencent a 0 (index de ligne).
- Importer uniquement depuis `@duplojs/utils` (jamais de chemin relatif).

Exemple:

```md
<MonacoTSEditor
  src="/examples/v1/api/<namespace>/<function>/tryout.doc.ts"
  majorVersion="v1"
  height="300px"
  :foldLines="[3, 7]"
/>
```

## Contenu des exemples (*.doc.ts)

- Les exemples doivent etre simples et didactiques.
- Eviter de montrer plusieurs fonctions dans un meme exemple sauf si le contexte l'exige.
- Pour les fonctions avec predicate (filter, find, when, equal, etc.), garder un contexte minimal et ajouter un `ExpectType` pour rendre le type explicite (utile en mobile).
- Pour les fonctions predicate/type-guard, utiliser un `if` + `ExpectType` comme ici: `docs/examples/v1/api/array/is/tryout.doc.ts`.
- Si un exemple necessite des types declares en amont (ex: pattern match), les replier via `foldLines` et les compter comme une seule ligne visible: `docs/examples/v1/api/pattern/match/builder.doc.ts`.
- Les `ExpectType` ne doivent jamais etre plies: afficher le type complet.
- Pour les exemples Clean avec contexte DDD, replier un namespace complet si besoin (ex: `User`): `docs/examples/v1/api/clean/repository/tryout.doc.ts`.

Templates d'exemples disponibles (a adapter):

- `assets/example-predicate-template.md` (base type-guard)
- `assets/example-transformer-template.md` (transformer simple)
- `assets/example-combinator-template.md` (combiner simple)
- `assets/example-context-predicate-template.md` (predicate avec contexte minimal)
- `assets/example-types-folded-template.md` (types declares en amont + foldLines)
- `assets/example-clean-folded-namespace-template.md` (namespace Clean replie)

## Rediger une page API (fonction)

- Partir du template `assets/api-function-template.md`.
- Copier/coller la description courte dans `description` du frontmatter.
- Inclure la version currifiee si elle existe.
- Ajouter "Voir aussi" avec des liens voisins ou proches.
- Ajouter "Sources" seulement si une reference externe est utile.
- Pour les cas specifiques, utiliser `docs/{fr,en}/v1/api/{namespace}/{concept + function}.md` et des exemples dedies dans `docs/examples/v1/api/{namespace}/{function}/`.
- Quand une page est ajoutee, mettre a jour le sommaire du namespace (`docs/{fr,en}/v1/api/{namespace}/index.md`) et reajuster les liens `prev`/`next` des pages voisines pour inserer la page correctement.

Format obligatoire:

- Frontmatter YAML: `outline`, `prev`, `next`, `description`.
- Contenu: `# NomDeLaFonction`, description courte, exemple interactif, syntaxe, parametres, valeur de retour, voir aussi.

## Cas speciaux a garder en tete

- Pages avec comparatifs ou multi-exemples (ex: DataParser object): regrouper par sous-sections claires, utiliser plusieurs MonacoTSEditor et des grilles si besoin.
- Pages d'index riches (ex: Clean primitives): structurer en sections (intro, exemples, liste d'API, operateurs) et garder une progression narrative.

## Templates de namespaces speciaux

- Utiliser `assets/api-namespace-dataparser-template.md` pour `docs/{fr,en}/v1/api/dataParser/index.md`.
- Utiliser `assets/api-namespace-clean-template.md` pour `docs/{fr,en}/v1/api/clean/index.md`.
