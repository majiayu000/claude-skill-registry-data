---
name: encre-rust
description: Conventions Rust et WebAssembly du design system de Paul Perigault. À charger pour écrire ou relire un crate (`crates/pp-color`, `crates/pp-data`, crates `-wasm`), un `Cargo.toml`, `rust-toolchain.toml`, `deny.toml`, un test de parité TypeScript/Rust, un `proptest`, le build ou le poids d'un `.wasm`, ou les étapes #88, #89, #90, #98, #99 ; à la demande « revue Rust », « Rust Encre », « conventions des crates ». Propre au projet.
---

# Encre : conventions Rust et WebAssembly

Issue : [#178](https://github.com/PaulPerigault/design-system/issues/178). Sources du dépôt :
ADR-0006 (décision 4), ADR-0007 (parité de `pp-data`), ADR-0005, D-030, `AGENTS.md`, `encre-securite`.
Sources externes : section « Sources ». Ce skill est de la méthode, pas une preuve : « prouvé »
seulement si une source l'établit ; sinon « convention » ou « préférence ». Aucun crate n'existe
encore au 2026-10-30 : les règles ci-dessous sont celles de l'ADR, à appliquer dès l'étape 7a (#88).

## Comment l'utiliser

- Phrase de déclenchement : « revue Rust de `<crate, PR ou fichier>` » (ou `/encre-rust`).
- Lire le code avant de juger ; citer `fichier:ligne`. Sortie : Critique, À améliorer, Ce qui tient.
- En cas d'écart avec ADR-0006 ou D-030, la source du dépôt gagne.

## Architecture des crates (ADR-0006, décision 4)

- Espace de travail Cargo à la racine ; `crates/pp-color` (OKLCH, sRGB, gamut, contraste WCAG 2 et
  APCA) et `crates/pp-data` (agrégation, quantiles, sous-échantillonnage).
- Un crate métier est du **Rust pur**, sans dépendance à `wasm-bindgen`. La liaison WebAssembly vit
  dans un crate `-wasm` mince (conversion des types, aucune logique). Raison : un futur back Rust ou
  Go réutilise le crate sans le glue JavaScript. `wasm-bindgen` relie Rust et JavaScript et peut
  générer des types TypeScript (guide wasm-bindgen).
- Sens des dépendances comme côté TypeScript : le crate `-wasm` dépend du crate métier, jamais
  l'inverse. Une logique dans un crate `-wasm` est une erreur de revue.
- Logique pure, dépendances injectées, comme en TypeScript (`AGENTS.md`). Les limites de taille du
  dépôt (fichier, fonction, complexité) s'appliquent au Rust ; on découpe, on ne relève rien.
- Aucun nombre magique : constantes nommées (seuils, coefficients OKLCH), avec leur source en
  commentaire. Un coefficient de norme cite la norme.

## Outillage bloquant

- `rust-toolchain.toml` épinglé. Contrôles (ADR-0006) : `cargo fmt --check`,
  `cargo clippy -- -D warnings -W clippy::pedantic` (pedantic **en refus**), `cargo test`,
  `cargo audit`, `cargo deny`.
- Clippy classe `pedantic` comme groupe strict, à faux positifs assumés, où l'`#[allow]` ciblé est
  normal ; `restriction` ne s'active pas en bloc (documentation Clippy). Règle du dépôt : un
  `#[allow]` porte une raison écrite, sur l'élément le plus petit, jamais au niveau du crate.
- `cargo audit` lit `Cargo.lock` contre la base RustSec. `cargo deny` fait quatre contrôles :
  `licenses`, `bans` (crates interdits, doublons), `advisories` (failles, crates non maintenus ou
  retirés), `sources` (origine). **Bloquants dès le premier crate**, pas après.
- Vérification locale : `cargo fmt --check`, `cargo clippy` et `cargo test` suffisent à la machine de
  Paul ; `cargo audit` et `cargo deny` s'installent à part. S'ils manquent, le dire, ne pas les
  déclarer verts : la CI reste juge.

## Aucun panic, erreurs typées

- Hors tests : ni `panic!`, `unwrap`, `expect`, `unreachable!`, `todo!`, ni indexation `v[i]`
  non vérifiée. Utiliser `get`, `first`, les itérateurs, `?`.
- Préférence de mise en œuvre : activer au niveau du crate `#![deny(clippy::unwrap_used,
clippy::expect_used, clippy::panic, clippy::indexing_slicing)]`, avec `#![cfg_attr(test,
allow(...))]`. Ces lints sont du groupe `restriction` : on les cite un par un, jamais en groupe.
- Erreurs typées : un `enum` par crate (ou `thiserror`), jamais `String` ni `Box<dyn Error>` à
  l'interface publique. Les variantes décrivent la cause (`OutOfGamut`, `InvalidHue`,
  `EmptyDataset`), pas le message.
- Validation aux bords : une fonction publique vérifie ses entrées (nombres finis, plages, longueurs)
  et rend `Result` ; les API Guidelines rangent la vérification des arguments sous « Dependability ».
  Documenter `# Errors` pour chaque `Result` publique et `# Panics` si un panic reste possible.
- Un crate `-wasm` convertit l'erreur du crate métier en erreur de frontière ; il ne la perd pas.

## `unsafe` interdit (règle validée par Paul)

- `#![forbid(unsafe_code)]` en tête de **chaque** crate, `-wasm` compris. `forbid` ne se contourne
  pas par un `allow` local, ce que `deny` permet (documentation rustc).
- Une exception demande ⚖️ de Paul, avant le code : le bloc `unsafe` porte un commentaire qui énonce
  le contrat. Le `forbid` du crate ne s'abaisse pas : il devient `deny`, et un `#[allow(unsafe_code)]`
  ne couvre que le module concerné, dans la même PR. `--cap-lints` peut aussi abaisser un `forbid`.
- Une dépendance qui contient de l'`unsafe` se juge à la revue de dépendance (mainteneur, usage,
  poids), pas à la règle ci-dessus, qui ne vise que le code du dépôt.

## Tests : unitaires, propriétés, parité

- Une brique = un test au minimum (`AGENTS.md`). Tests unitaires à côté du code ; tests d'intégration
  dans `tests/`.
- `proptest` pour les propriétés : une propriété vérifie une règle sur beaucoup d'entrées générées et
  réduit (shrinking) toute entrée en échec à un cas minimal (proptest book). Propriétés prévues par
  l'ADR : aller-retour OKLCH, bornes du gamut. Les fichiers `proptest-regressions/` se **commitent** :
  ils rejouent les échecs passés (proptest book).
- Parité avec la référence TypeScript, bloquante en CI : le TypeScript reste la référence tant que la
  parité n'est pas établie. Mêmes vecteurs d'entrée des deux côtés (fichier de vecteurs partagé).
  - `pp-color` : écart ≤ **1e-6** sur les composantes, ratio de contraste arrondi identique
    (ADR-0006).
  - `pp-data` : écart ≤ **1e-9 en relatif** (ADR-0007), confirmé en V4a (D-097) : écart mesuré
    nul sur les quantiles et l'agrégation (D-098), indices LTTB identiques.
- Aucun gain de performance n'est exigé, aucune régression n'est tolérée (D-030) : temps de
  chargement mesuré avant et après, non dégradé.

## Le `.wasm` : poids, provenance, build

- Compilé **en CI**, jamais commité. Publié dans le paquet npm (`@paulperigault/color`, puis celui de
  `pp-data`) avec la provenance npm ; même chaîne que les autres paquets (voir `encre-securite`).
- Provenance : empreinte SHA-256 du `.wasm` enregistrée par le build, SBOM de la release qui couvre
  aussi les crates (`Cargo.lock` y entre). Empreinte et SBOM : mise en œuvre à décider à l'étape 8
  (#90) ; ne pas déclarer cette provenance acquise avant.
- Poids budgété et **signalé** (mesure affichée, voir `encre-greenops`) ; un seuil ne bloque que si
  Paul le pose. Le dire dans la PR : poids avant, poids après.
- Build Cloudflare **sans Rust** : ni `rustup` ni `cargo` ; il consomme le paquet publié. Relire :
  aucune étape de `build` du site n'appelle `cargo` ou `wasm-pack`.
- Le WebAssembly du site s'exécute au build (Node) (ADR-0007) ; côté navigateur, la CSP n'autorise que
  `'wasm-unsafe-eval'`, jamais `'unsafe-eval'` (voir `encre-securite`).

## Machine de Paul

- Chaîne `windows-gnu` (`x86_64-pc-windows-gnu`) ; `cargo` est dans `~/.cargo/bin`. Les chemins et
  fins de ligne diffèrent de Linux : ne jamais coder un chemin ni un séparateur en dur.
- La CI Linux est la référence. Un test vert en local sans la CI ne prouve rien (flottants,
  `libm`, fins de ligne des vecteurs). Vérifier d'abord `cargo test` en local, conclure avec la CI.

## Relire une PR de crate

1. `#![forbid(unsafe_code)]` présent ? Aucun `wasm-bindgen` dans un crate métier ?
2. Un `unwrap`, `expect`, `panic!`, `v[i]` hors test ? Un `#[allow]` sans raison ?
3. Erreurs typées à l'interface publique, `# Errors` documenté ?
4. Parité et propriétés testées, vecteurs partagés, seuil cité ?
5. `.wasm` : poids avant et après, build Cloudflare sans Rust, aucun binaire commité ?
6. `cargo fmt`, `clippy`, `audit`, `deny` verts ; sinon dire lesquels n'ont pas tourné.

## Sources

Consultées le 2026-10-30. Niveaux : norme, étude, convention, préférence.

| Source                                   | URL                                                                      | Niveau     |
| ---------------------------------------- | ------------------------------------------------------------------------ | ---------- |
| Rust API Guidelines, checklist           | https://rust-lang.github.io/api-guidelines/checklist.html                | convention |
| Documentation Clippy, groupes de lints   | https://doc.rust-lang.org/clippy/lints.html                              | convention |
| Guide wasm-bindgen (nouvelle adresse)    | https://wasm-bindgen.github.io/wasm-bindgen/                             | convention |
| The Proptest Book, introduction          | https://proptest-rs.github.io/proptest/intro.html                        | convention |
| Proptest, persistance des échecs         | https://proptest-rs.github.io/proptest/proptest/failure-persistence.html | convention |
| RustSec et `cargo audit`                 | https://rustsec.org/                                                     | convention |
| cargo-deny, les quatre contrôles         | https://embarkstudios.github.io/cargo-deny/checks/index.html             | convention |
| rustc, niveaux de lint (`forbid`/`deny`) | https://doc.rust-lang.org/rustc/lints/levels.html                        | norme      |

L'ancienne adresse `rustwasm.github.io/docs/wasm-bindgen/` ne sert plus que l'avis de déménagement.
Le guide wasm-bindgen ne décrit pas le glue JavaScript sur la page lue : l'affirmation est limitée
aux types TypeScript. Les quatre lints (`unwrap_used`, `expect_used`, `panic`, `indexing_slicing`)
sont dans `restriction` selon la réponse de l'outil de lecture, pas selon le texte de la page Clippy,
qui ne les liste pas : [À VÉRIFIER] dans la liste des lints Clippy.
Aucun texte n'est copié : tout est paraphrasé. Aucune étude citée : les seuils 1e-6 et 1e-9 sont
des choix de l'ADR, pas des résultats externes.
