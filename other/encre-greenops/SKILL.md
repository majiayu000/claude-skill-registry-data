---
name: encre-greenops
description: Revue de sobriété numérique (GreenOps) du design system de Paul Perigault. À charger pour relire ou écrire du JavaScript client, une police, une image, une dépendance d'exécution, un budget ou une mesure de poids, une estimation carbone, l'usage de l'offre gratuite Cloudflare (`tools/benchmark/`, `apps/docs/e2e/perf.spec.ts`, #102) ; à la demande « revue greenops », « sobriété Encre », « combien pèse cette page ». Propre au projet, web statique.
---

# Encre : revue GreenOps

Issue : [#178](https://github.com/PaulPerigault/design-system/issues/178). Sources du dépôt :
`AGENTS.md`, ADR-0006 (décision 5), D-030, D-036, `packages/css/src/fonts.css`,
`apps/docs/e2e/perf.spec.ts`, `tools/benchmark/measure.mjs`, [#102](https://github.com/PaulPerigault/design-system/issues/102).
Sources externes : section « Sources ». Ce skill est de la méthode, pas une preuve : « prouvé »
seulement si une source l'établit ; sinon « convention » ou « préférence ».

## Principe (préférence de Paul)

GreenOps est un principe, pas un plafond. Le poids se **mesure**, s'**affiche** et se **signale** ;
il ne fait jamais échouer la CI par défaut. Un seuil ne bloque que si Paul le pose explicitement.
Aucune fonctionnalité n'est retirée pour gagner des octets : on réduit ce qui est inutile, pas ce
qui sert.

**Décision prise (D-106)** : les budgets bloquants de `perf.spec.ts` sont devenus des mesures
affichées, et ADR-0006 décision 5 est amendée. Rien ne bloque la CI sur le poids ; en revue,
signaler une hausse sans la qualifier de motif de refus. Outils : `npm run benchmark:weight` (poids
des pages et des paquets, carbone), page « Sobriété ».

## Comment l'utiliser

- Phrase de déclenchement : « revue greenops de `<page, paquet ou PR>` » (ou `/encre-greenops`).
- Mesurer d'abord, juger ensuite ; citer outil, réglage, date, `fichier:ligne`.
- Sortie : trois sections (À signaler, À améliorer, Ce qui tient). Jamais « bloquant » sans seuil
  posé par Paul ; jamais « écologique » ou « vert » sans mesure et méthode.

## Poids : par page et par ressource

- Mesurer par page et par type (HTML, CSS, JS, police, image, `.wasm`), en octets transférés
  (compressés) et en octets décodés ; dire lequel.
- Outils existants : `perf.spec.ts` (JS gzip, fichiers de police, sous bridage mobile) et
  `tools/benchmark/measure.mjs` (`resources()`, `transferSize` ; 0 sans `Timing-Allow-Origin` :
  « inconnu », pas « nul »). Le rapport de poids par page et par paquet est `tools/benchmark/weight.mjs` (#102).
- Afficher : un tableau page, ressource, octets, date, dans la PR ou le bilan. Signaler : une
  hausse notable entre deux mesures, sans échec de CI.
- Le chiffre de poids est un fait ; sa lecture (« lourd ») est une préférence tant qu'aucun seuil
  n'est posé. WSG 3.1 demande de se fixer des objectifs mesurables ; il ne donne aucun chiffre.

## Zéro JavaScript par défaut

- Composants sans JS par défaut (`AGENTS.md`) ; le comportement est opt-in (`behaviors`).
- Relire : un `<script>` ajouté, une bibliothèque cliente, une hydratation sans besoin, un effet
  qui pourrait être du CSS ou du HTML natif (`details`, `dialog`, `popover`).
- WSG 3.2, 3.11, 3.12 : retirer le code inutilisé, limiter calculs et mises à jour du DOM, réduire
  les dépendances. Même sous la barre, un JS sans usage reste à justifier par écrit.

## Polices

- Auto-hébergées, Atkinson Hyperlegible Next et Mono variables, sous-ensembles latin et latin-ext,
  `font-display: swap` (`fonts.css`). Corps et chasse fixe : deux familles (ADR-0002).
- Relire : une troisième famille, un axe de variable inutile, une graisse non utilisée, un
  jeu de caractères hors français et anglais, une police servie depuis un hôte tiers.
- WSG 2.11 : polices système si possible, nombre et complexité limités, sous-ensembles.

## Images

- Au plus juste : seulement si elle sert la page (WSG 2.9), dimensions et format adaptés à
  l'écran, chargement différé hors du premier écran, texte alternatif (`encre-design`).
- Graphiques en SVG statique au build (ADR-0007) : pas d'image raster pour un tracé de données.
- L'étape #91 mesure les images ; aucun seuil n'existe tant que Paul n'en pose pas.

## Estimation carbone : méthode et limites

- Aucune méthode n'est « prouvée » par défaut. Une estimation porte son nom de modèle, sa version,
  ses paramètres et sa date ; sans cela, ne pas publier le chiffre.
- Retenu à l'étape #102 : SWD v4 (`tools/benchmark/carbon.mjs`, D-106). Autres modèles, pour mémoire :
  - SWD v4 (Sustainable Web Design) via CO2.js : modèle descendant, trois segments (centres de
    données 22 %, réseaux 24 %, appareils 54 %), intensité mondiale 494 gCO2e/kWh, ajustable ;
    CO2.js l'utilise par défaut (documentation) ; ses auteurs disent qu'il ne sert pas à trouver
    quoi optimiser et que les sources divergent. Hypothèses à écrire : visiteurs de retour et cache.
  - OneByte (The Shift Project, via CO2.js) : frontière plus étroite (centres de données et réseau) ;
    les deux modèles donnent des résultats différents, ne jamais comparer d'un modèle à l'autre.
  - SCI (Green Software Foundation) : SCI = (E × I + M) / R, un **taux** par unité fonctionnelle
    à définir (une page vue), pas un total ; exclut les compensations ; le périmètre est choisi par
    l'auteur. Demande des données d'énergie que le dépôt n'a pas : usage à documenter.
- Afficher une fourchette ou une méthode, pas un chiffre isolé ; écrire « estimation », jamais
  « émet ». Changer de version de modèle change les chiffres : refaire l'historique.

## Offre gratuite Cloudflare (surveiller, ne pas bloquer)

- Previews par l'intégration Git de Cloudflare Pages (D-036) ; le projet est déclaré en OpenTofu
  (aucun `apply` par un agent).
- Limites du plan gratuit lues dans la documentation : 500 builds par mois, 20 000 fichiers par
  site, 25 MiB par fichier, 100 règles `_headers`. Requêtes de fichiers statiques gratuites et
  illimitées ; la bande passante n'est pas mentionnée sur la page lue : [À VÉRIFIER].
- Surveiller : builds du mois (previews par PR, D-036), nombre de fichiers publiés (index
  `pagefind` compris), taille du plus gros fichier. Signaler à l'approche
  d'une limite ; ne rien retirer.

## Dépendances d'exécution

- Aucune dépendance d'exécution inutile ; chaque ajout est justifié par écrit (ADR-0006,
  décision 5). `tokens` et `guards` n'en ont aucune à l'exécution (`AGENTS.md`).
- Relire une PR de dépendance : poids installé, poids livré au client, alternative native.
  Complète `encre-securite` (mainteneur, provenance, scripts d'installation).

## Checklist vérifiable

1. Poids mesuré par page et par ressource, outil et date notés, octets transférés ou décodés dits.
2. Aucun `<script>` client nouveau sans justification écrite ; aucune dépendance d'exécution neuve.
3. Polices : deux familles, sous-ensembles latin ; aucune police tierce.
4. Images : seulement utiles, dimensionnées, différées hors premier écran.
5. Estimation carbone : modèle, version, paramètres, date, limites ; sinon aucun chiffre.
6. Offre gratuite : builds, fichiers, plus gros fichier relevés.
7. Aucun échec de CI ajouté ; aucune fonctionnalité retirée pour gagner des octets.

## Sources

Consultées le 2026-10-30. Niveaux : norme, convention, préférence. Texte paraphrasé, jamais copié.

| Source                                                | URL                                                                                                | Niveau       |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------ |
| Green Software Foundation, SCI v1.1.0                 | https://sci.greensoftware.foundation/                                                              | convention   |
| ISO/IEC 21031:2024 (SCI)                              | [À VÉRIFIER] page ISO en 403 ; statut ISO lu seulement dans des tiers                              | [À VÉRIFIER] |
| Sustainable Web Design, estimation des émissions v4   | https://sustainablewebdesign.org/estimating-digital-emissions/                                     | convention   |
| CO2.js, modèles d'estimation                          | https://developers.thegreenwebfoundation.org/co2js/models/overview/                                | convention   |
| RGESN 2024 (Arcep, Arcom, ADEME), annonce du 17 mai   | https://www.arcep.fr/actualites/actualites-et-communiques/detail/n/environnement-rgesn-170524.html | convention   |
| W3C, Web Sustainability Guidelines (Group Note Draft) | https://www.w3.org/TR/web-sustainability-guidelines/                                               | convention   |
| Cloudflare Pages, limites                             | https://developers.cloudflare.com/pages/platform/limits/                                           | convention   |
| Cloudflare Pages, tarification des requêtes           | https://developers.cloudflare.com/pages/functions/pricing/                                         | convention   |

« Convention » : guide ou documentation d'éditeur, non normatif. Le RGESN (78 critères, publié en
2024 d'après l'annonce de l'Arcep) est un référentiel public, dont la valeur contraignante n'est pas
précisée sur la page lue ; ses critères ne sont pas repris ici. Les WSG sont un brouillon de note,
non approuvé par le W3C (daté du 16 octobre 2026 à la lecture) : à citer comme travail en cours.
Aucune étude n'est citée ; aucun chiffre d'impact n'est avancé, hors les paramètres des modèles.
