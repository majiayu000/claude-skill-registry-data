---
name: tribos-site-design-system
description: Système de design FIXE du site tribos.evey.run, « Noir & Blaze » (noir chaud, orange, visuels 3D Cinematic du renard). À lire AVANT toute modification visuelle du site, même petite - nouvelle section ou page, composant, couleur, police, image, animation, libellé de bouton - et avant tout « refais le site ». On fait évoluer ce système, on ne repart jamais de zéro.
---

# Système de design du site Tribos : « Noir & Blaze »

Fixé le **14 octobre 2026**, après deux refontes successives. Ce fichier existe
pour une seule raison : que la prochaine session ne perde pas ce qui a été
validé. Il fait foi pour le site ; `assets/css/tribos.css` en est
l'implémentation. **Toute règle, tout jeton, tout composant ajouté l'est dans
les deux fichiers, dans le même commit.**

Ce que l'utilisateur a validé, à ne pas défaire sans son accord explicite :

- le **noir chaud et l'orange** de l'ancien site (pas de bleu nuit) ;
- le **hero** actuel : renard 3D qui salue sur un sentier au coucher du soleil,
  texte à gauche, chapitres Sport / Groupe / Progression à droite ;
- les **visuels 3D Cinematic** du renard canonique (`assets/cine/`) ;
- la **nouvelle icône** de l'app (renard blanc en relief sur orange) comme logo.

## 1. Lecture du design

*Landing grand public d'une app de sport entre amis (bêta), en français et au
tutoiement, pour des 18-35 ans qui veulent s'y remettre à plusieurs. Langage
sport-tech premium, sombre et chaleureux. Socle : HTML/CSS/JS écrits à la main,
Geist, Phosphor, animations CSS et IntersectionObserver. Le produit se montre
tel qu'il est : vraies captures iOS et widgets de l'app reconstruits à
l'identique, posés en cartes blanches sur le noir.*

Réglages (skill `design-taste-frontend`) : **DESIGN_VARIANCE 7**,
**MOTION_INTENSITY 6**, **VISUAL_DENSITY 4**. Une seule page sombre, aucune
section claire, aucune bascule de thème.

## 2. Les trois couches

1. **Le noir** de la page (`--bg`) et ses surfaces graphite : l'interface.
2. **L'orange** : un accent unique (`--accent`) et une surface d'affiche,
   `.blaze` (dégradé orange profond), réservée à quelques moments par page.
3. **L'artwork Cinematic 3D** : le renard canonique en montagne au coucher du
   soleil, livré en images (`assets/cine/`) qui ne portent jamais de texte.

Les couches ne se mélangent pas : pas de texte dans une image, pas d'image
« décorative » sans rôle, pas de dégradé orange plein écran derrière du texte
courant.

## 3. Jetons

Valeurs exactes dans `:root` de `tribos.css`. Ne pas en créer de nouveaux sans
les ajouter ici.

| Rôle | Jeton | Valeur | Usage |
|---|---|---|---|
| Fond de page | `--bg` | `#0D0B09` | noir chaud, partout |
| Bande alternée | `--bg-2` | `#131110` | rare |
| Surface | `--surface` | `#1A1613` | tuiles, panneaux |
| Surface haute | `--surface-2` | `#221D19` | scène du groupe, survol |
| Filet | `--line` / `--line-strong` | blanc chaud à 8 % / 16 % | séparateurs, bordures |
| Texte fort | `--text` | `#F6F1EA` | titres, gras (jamais `#FFF`) |
| Texte courant | `--text-body` | `#BEB5AA` | paragraphes |
| Texte discret | `--text-muted` | `#A09385` | légendes (5,9:1 sur `--bg`) |
| Accent | `--accent` | `#F3730A` | aplats, CTA, états actifs (AppTheme.primary) |
| Accent clair | `--accent-hi` | `#FF8A2A` | survol, mot orange des titres |
| Orange en petit texte | `--accent-text` | `#FFA25C` | liens, petites mentions (9,9:1) |
| Encre sur orange | `--on-accent` | `#221000` | tout texte posé sur `--accent` |
| Blaze | `--blaze-mid` `--blaze-deep` `--blaze-lo` `--blaze-hi` | `#C2410C` `#9A3607` `#571C02` `#F58022` | dégradé `.blaze` |
| Texte sur blaze | `--on-blaze` / `--on-blaze-dim` | blanc / blanc 92 % | |

Typographie : `--step--1` à `--step-5` (échelle fluide). Espacement : `--s-1`
(0,25rem) à `--s-10` (8rem). Rayons : **pill** pour tout ce qui se clique,
`--r-card` 18px pour les cartes et tuiles, `--r-media` 26px pour les médias,
téléphones et grands panneaux. Ombres : `--shadow-1` à `--shadow-3`, `--glow`
(orange, CTA au survol uniquement). Mouvement : `--ease`, `--ease-film`,
`--motion` (multiplicateur, 0 en mouvement réduit). Grain : `.grain`, fixe,
5 %.

Pile de z-index : grain 1, dock mobile 44, menu 45, nav 50, lien d'évitement
100. Rien d'autre.

## 4. Typographie

- **Une seule famille pour le site : Geist** (titres en 700, interlettrage
  serré), et **Geist Mono 500** pour les surtitres et certains chiffres. Pas de
  serif, pas d'italique synthétisé.
- **Exception unique, les widgets de l'app** (`.appui`) : ils sont dans les
  polices de l'app, **Montserrat** (titres, chiffres) et **Roboto** (corps),
  déclarées dans `tribos.css` (bloc `.appui`) et produites par
  `tools/build-fonts.py`. Jamais ailleurs sur le site.
- Rôles fixes :
  - h1 du hero : jusqu'à 6rem, 3 lignes courtes, `-0,047em` ;
  - `.h2` : les temps forts (Comment ça marche, Un objectif tout le groupe,
    l'inscription) ;
  - `.h2-s` : les sections de soutien (l'app, les points, la FAQ) ;
  - `.lede` : une phrase, 46ch max ; corps à 1,62 d'interligne.
- **Le mot orange** d'un titre : `<em class="lit">`, couleur `--accent-hi`,
  penché par `skewX(-8deg)`. Un seul par titre, et seulement là où il porte le
  sens (« tes potes », « ton entreprise »).

## 5. Couleur et contraste

- **Un seul accent : l'orange.** Le bleu « défi » et le vert n'existent que dans
  les widgets de l'app (`.appui`), jamais sur un lien, un bouton ou un état du
  site.
- **Un widget est une image de l'app** : `role="img"` et un `aria-label` qui dit
  ce qu'il montre. À l'intérieur, les couleurs de l'app telles qu'elles sont
  livrées (orange sur blanc compris) ; la règle AA s'applique au texte du site
  autour, qui dit la même chose en clair.
- **Blanc ou ivoire sur `#F3730A` : interdit** (2,9:1). Sur un aplat orange, le
  texte est `--on-accent`.
- Orange comme petit texte : `--accent-text`, jamais `--accent`.
- Sur `.blaze` : le texte ne se pose que sur les zones profondes (blanc ≥ 5:1) ;
  le coin chaud reçoit le bouton ivoire, jamais une ligne de texte. Les panneaux
  chargés de petit texte prennent `.blaze.blaze-deep`.
- Sur l'artwork : texte seulement sur le voile de `.scene`, mesuré. Tout texte
  du site passe **AA** (4,5:1, ou 3:1 au-delà de 24px), mesuré de 390 à 2560px.

## 6. Composants

Classes de `tribos.css`, dans l'ordre du fichier. Réutiliser avant d'inventer.

| Composant | Classes | Règles |
|---|---|---|
| Navigation | `.nav` `.brand` `.nav-links` `.menu-panel` | transparente sur l'image d'ouverture, verre noir une fois collée ; logo = icône de l'app à 32px ; une ligne, 72px |
| Boutons | `.btn` + `.btn-primary` / `.btn-light` / `.btn-ghost`, `.btn-sm` `.btn-lg` | orange = action principale sur fond noir ; ivoire = nav et tout bouton posé sur l'orange ; ghost = secondaires (partage) ; jamais sur deux lignes |
| Scène | `.scene` `.scene-media` `.hero` `.hero-copy` `.hero-chapters` | image plein cadre + voile mesuré ; texte au tiers gauche ; recadrage portrait sur mobile (`.is-stacked`) |
| Bandeau de scène | `.scene-band` (`.is-top` en haut de page) + `.scene-band-body` | le plan passe seul, le titre suit sur le noir ; pour la fin de l'accueil et le haut des pages secondaires |
| Générique | `.marquee` | une seule par page, les programmes, sous le hero |
| Manifeste | `.statement` + `blockquote[data-scrub]` | centré, mots allumés au passage (timeline CSS), pleine force sans support |
| Séquence | `.sequence` `.sequence-steps` `.sequence-step` `.stage` `.stage-art` `.sequence-screens` | iPhone épinglé sur la scène « horizon », étapes sur un rail (nœuds et segments orange au fil de la lecture, pas de numéros) ; seule la scène découpe, jamais une boîte intérieure (l'ombre du téléphone dessinait un rectangle) |
| iPhone | `.device` `.device-bleed` | vraies captures iOS seulement (`tools/build-ios.py`), barre d'état comprise ; le cadre ajoute le bord titane et la Dynamic Island, rien d'autre ; `-bleed` : l'écran sort par le bas |
| Bento | `.bento` `.tile` + `.tile-shot` `.tile-accent` `.tile-board` `.tile-appui` `.tile-points` `.tile-defi` `.tile-streak` `.tile-photo` `.tile-split` | six cellules, six contenus ; chaque tuile une matière (lueur + iPhone, orange, graphite + widget, forêt) ; `.tile-split` met texte et widget côte à côte dès 600px de tuile ; halo qui suit le pointeur |
| Groupe | `.split` `.split-media` `.split-stage` `.ui-group` `.split-body` | l'en-tête de l'écran groupe hors du téléphone : bannière « Les Loups » + carte d'objectif qui en sort (18px de recouvrement), inclinée au pointeur |
| Points | `.stats` `.stats-note` `.nots-split` `.nots` | grands chiffres sans carte ; « ne fait pas » en deux colonnes, le seul « oui » en orange |
| Apps compatibles | `.sync` `.sync-copy` `.soon` `.sync-hub` `.sync-core` `.sync-lines` `.sync-apps` `.sync-legal` | l'icône Tribos au centre, les apps sur deux anneaux, un fil vers le centre ; des noms, jamais de logos ; pastille « Bientôt » tant que rien n'est livré (voir § 12) ; nuage de noms sur téléphone |
| Salles partenaires | `.partners` `.partners-copy` `.partner-grid` `.partner-slot` (`.is-empty`) | invitation + grille de 6 emplacements (3 x 2) ; la première case dit « Ta salle ici », les autres un + ; un logo prend une case quand un partenariat est signé |
| Affiche orange | `.blaze` (`.blaze-deep`) `.band` `.band-inner` | 2 ou 3 par page au plus |
| FAQ | `.faq-split` `.faq-head` `.faq` `.faq-more` | titre épinglé à gauche, réponses à droite ; `<details>` natif |
| Inscription | `.finale` `.finale-body` `.signup` `.signup-head` `.signup-support` `.assurances` `.signup-next` | panneau blaze profond qui monte sur le pied du dernier plan ; formulaire à droite |
| Formulaires | `.form` `.form-inline` `.field` `.chips` `.chip` `.consent-note` `.form-status` `.honeypot` | label au-dessus (ou `sr-only` en ligne) ; erreurs sous le champ ; aucune case précochée |
| Pied de page | `.footer` `.footer-grid` `.footer-mark` `.footer-bottom` | colonnes calmes, mot-symbole « Tribos » géant presque noir |
| Pages secondaires | `.page-hero` `.page-head` `.feature-rows` `.feature-row` `.timeline` `.timeline-step` `.invite` `.testflight` `.doc` | même grammaire que l'accueil |
| Widgets de l'app | `.appui` + `.ui-card` `.ui-streak` `.ui-stat` (`.ui-points`, `.ui-sessions`, `.ui-band`) `.ui-board` `.ui-row` `.ui-group` `.ui-banner` `.ui-goal` `.ui-chat` `.ui-msg` `.ui-ava` | reconstruits depuis le code de l'app (fichier cité sur chaque bloc) : mêmes polices, couleurs, rayons, marges, à la taille de l'iPhone 6,9" ; graisses = celles que l'app affiche (voir § 12) ; données du groupe de démo « Les Loups » ; icônes Material de l'app (`assets/appui/icons.svg`) |
| Dock mobile | `.cta-dock` | un lien, jamais un champ |

## 7. Composition des pages

Une famille de mise en page apparaît **une seule fois** par page.

**Accueil** : hero (scène) → générique → manifeste → Comment ça marche
(séquence) → Ce qu'il y a dans l'app (bento) → Un objectif, tout le groupe
(groupe) → Des points (chiffres + ne fait pas) → Tes autres apps compteront
aussi (hub, « Bientôt ») → Les salles partenaires (emplacements) → Ensemble on
est plus forts (affiche blaze) → FAQ (deux colonnes) → dernier plan +
inscription (blaze profond) → pied de page.

**Entreprises** : bandeau sommet + titre → lignes de raisons → frise → affiche
blaze. **Merci** : bandeau sommet + titre → encart iPhone (blaze profond) →
invitation → taille du groupe → la suite. **404** : bandeau sentier + titre.
**Pages légales** : en-tête + `.doc`, sans image.

Surtitres (eyebrows) : **deux sur l'accueil** (hero et inscription, avec la
pastille « en direct »), un en tête de chaque page secondaire. Jamais de
numéro de section (« 01 · Sport »), jamais de surtitre au-dessus de chaque
titre. La pastille d'état `.soon` (« Bientôt », point creux) n'est pas un
surtitre : une seule par page, là où une fonction annoncée n'existe pas
encore.

## 8. Images

- **Artwork** : preset `tribos-da-3d-cinematique`. Masters dans
  `.context/src/cine/` (non versionnés), variantes produites par
  `tools/build-cine.py` dans `assets/cine/` (AVIF + WebP, JPEG de secours) :
  `sentier` (hero, 404, carte sociale), `sommet` (fin de l'accueil,
  entreprises, merci), `horizon` et `foret` (paysages sans renard, fonds de
  la scène du téléphone et de la tuile du chat).
- Les masters actuels sont **provisoires** (upscales x4 des visuels des mails) :
  les remplacer par des rendus 21:9 4K générés avec `tools/cine-generate.py`
  et `tools/cine-prompts/`, sans changer les noms ni les emplacements.
- **Jamais de texte sur le renard**, jamais de texte dans une image, jamais de
  photo de stock comme décor, jamais d'illustration BD ou 2D, jamais l'ancien
  loup (d'où l'absence de la carte « Séance du jour », qui le porte). Seules
  photos admises : celles du groupe de démo (avatars de Max, Alex, Lena et
  bannière, CC0), et seulement **dans** les widgets et les captures.
- **Logo** : l'icône de l'app (`assets/brand/app_icon.png` du dépôt
  `justeozan/Tribos`), déclinée par `build_brand()` de
  `tools/build-assets.py` (nav, favicons, icône Apple, 192, 512). Après un
  changement d'icône dans l'app : la recopier dans `.context/src/brand/` et
  relancer cette étape, puis la carte sociale (`tools/build-og.mjs`).
- **Captures de l'app** : `tools/build-ios.py` découpe l'écran des planches
  App Store du dépôt de l'app (`store/app-store/`, app iOS en version release,
  compte de démo, barre d'état 9:41) dans `assets/app/ios-*`, et produit les
  avatars, la bannière et les icônes des widgets dans `assets/appui/`. Jamais
  retouchées à la main, jamais une capture de débogage (ruban DEBUG, images
  pas encore chargées). Pour rafraîchir : rejouer la chaîne de captures de
  l'app (`docs/app-store.md` § 6), recopier les planches dans
  `.context/src/ios/`, relancer le script. Les anciennes captures Android
  (`tools/build-assets.py`, `picker`, `player`, `groupe`...) ne servent plus.

## 9. Mouvement

Chaque animation a une raison, et toutes tombent à zéro en mouvement réduit.

| Animation | Raison |
|---|---|
| Push-in de l'image d'ouverture, parallaxe des scènes | ouverture et profondeur du plan |
| Apparition des blocs, cascade des mots des titres | ordre de lecture |
| Mots du manifeste allumés au passage | rythme de lecture |
| Écrans de la séquence, rail qui se remplit | état : l'étape en cours |
| Classement qui bouge, objectif qui se remplit, compteurs | preuve du produit |
| Entrée des widgets (jours qui s'allument, courbe tracée, barres, messages) | l'app qui se dessine, une fois |
| Noms des apps qui apparaissent, fils vers le centre | ce qui viendra se brancher |
| Halo des tuiles, aimant du CTA, éclats au survol | retour au pointeur |
| Générique | ampleur du catalogue |

Interdits : écouteur `scroll`, animation de `width`/`height`/`top`, boucle
infinie sans contenu, curseur personnalisé. Seuls `transform`, `opacity` et
`filter` s'animent. Une exception documentée : la barre segmentée de
l'objectif du groupe (13px, quatre segments) anime `flex-grow`, comme l'app. Le contenu ne dépend jamais d'une timeline de défilement
pour exister (le manifeste reste lisible sans).

## 10. Textes

Tutoiement ; apostrophe typographique (’) ; espace fine insécable
(`&#8239;`) avant ; : ! ? ; **aucun tiret cadratin ni demi-cadratin** ; aucun
chiffre, témoignage ou fonction inventés (vérifier contre l'app). Dans un
widget, le texte est celui de l'app, à la lettre (« continue ! » avec l'espace
de l'app) ; les noms de programme à tiret (« Jour 2 — Haut du corps ») ne
paraissent que dans les captures, jamais en texte du site. Libellés
fixes : « Je rejoins la bêta » pour envoyer, « Rejoindre la bêta » pour aller au
formulaire. Les textes de référence vivent dans `.context/copy.md`.

## 11. Règles techniques

- Site statique sans dépendance ni build ; `node tools/dev-server.mjs 8000`.
- Le script inline du `<head>` est **identique octet pour octet** sur toutes
  les pages : son empreinte est dans la CSP de `netlify.toml`.
- Nouvelle règle CSS : à la fin de son bloc dans `tribos.css`, avec les jetons
  existants, et décrite ici si c'est un composant.
- Images : `loading="lazy"` sauf au-dessus de la ligne de flottaison,
  `width`/`height`, `alt` en français ou `alt=""` décoratif.
- Pour les captures de contrôle, un Chrome sans tête sur son **propre** port
  (`--remote-debugging-port=0`) : jamais le port 9222, qu'un navigateur de la
  machine peut déjà utiliser.

## 12. Widgets, apps compatibles, salles partenaires

**Widgets de l'app** (`.appui`). La demande est « les mêmes que dans l'app » :
une recréation approximative a déjà été refusée. Donc : partir du fichier
Flutter du widget (`lib/screens/home/widgets/*`, `group/widgets/*`,
`group_screen.dart`), reprendre ses valeurs en pixels logiques, puis comparer
à la même échelle avec la planche App Store correspondante. Les **graisses**
sont celles que l'app affiche, pas celles que son code demande : un style
Roboto rendu gras par `copyWith()` garde la famille à graisse unique de
google_fonts, si bien que « Points x2 », « 100 », les noms du classement et du
chat sortent en 400 ou 500 ; les styles Montserrat à graisse explicite sortent
tels qu'écrits. Figma (`yKWOPBwjUkDptgwN7XP9TQ`, page Mockup) sert de
référence de style, pas de contenu : il est en anglais, son défi compte des
pas et son groupe un classement, ce que l'app ne fait pas.

**Apps compatibles.** Aujourd'hui l'app ne lit aucune autre app (pas de
HealthKit, pas de Health Connect, pas d'API Strava ; la politique de
confidentialité le dit). La section l'annonce donc au futur, sous la pastille
« Bientôt », avec des **noms** et non des logos : le badge « Works with Apple
Health » et le logo « Compatible with Strava » ne s'emploient qu'une fois
l'intégration livrée, selon leurs chartes. Google Fit n'y figure pas (ses API
s'arrêtent fin 2026) : Android passe par Health Connect, et Google Health
remplace les apps Fitbit et Google Fit. Quand une intégration est livrée :
mettre à jour la politique de confidentialité, la réponse de FAQ « Ça marche
avec Strava ou ma montre ? » (et son double JSON-LD dans le `<head>`), le
texte de la section ; retirer `.soon` quand tout est livré ; le badge officiel,
non modifié, peut alors remplacer le nom.

**Salles partenaires.** Aucun partenariat n'existe : six emplacements vides,
aucun nom de marque, un bouton « Devenir salle partenaire » vers l'adresse de
contact du support. Partenariat signé, avec accord écrit pour le logo : son
fichier (SVG ou PNG monochrome ivoire, 40px de haut environ) remplace le
contenu d'un `.partner-slot`, la classe `.is-empty` tombe ; les cases restantes
gardent la grille entière (3 x 2).

## 13. Check-list avant de livrer

- [ ] Palette : seulement les jetons ; un seul accent ; aucun blanc sur orange.
- [ ] Contraste AA mesuré sur tout texte posé sur image ou sur blaze (390,
      1280x720, 1440, 1920, 2560).
- [ ] Hero intact ; aucun texte sur le renard ; aucun texte dans les images.
- [ ] Une famille de mise en page par section, pas de répétition ; pas de trois
      cartes identiques en ligne ; bento sans cellule vide.
- [ ] Surtitres : deux sur l'accueil, aucun numéroté.
- [ ] Zéro tiret cadratin ; apostrophes et espaces fines ; aucun chiffre inventé.
- [ ] CTA sur une ligne ; libellés fixes ; nav sur une ligne.
- [ ] Mobile : aucune page plus large que l'écran (le dock doit rester visible).
- [ ] Mouvement réduit : tout reste lisible et immobile.
- [ ] Script du `<head>` inchangé.
- [ ] Widgets comparés à la planche App Store, à la même échelle.
- [ ] Rien d'annoncé comme « compatible » ou « partenaire » qui n'existe pas
      dans l'app ou par contrat.

## 14. Faire évoluer le système

1. Partir de ce fichier, jamais d'une page blanche. Réutiliser un composant
   existant avant d'en créer un.
2. Un changement de palette, de police, de hero ou de logo se décide **avec
   l'utilisateur** ; le noter dans l'historique ci-dessous.
3. Mettre à jour ce fichier et `tribos.css` dans le même commit.

## 15. Historique des décisions

- **2026-08** : affiche noire et orange (panneaux « blaze », photos CC0).
- **2026-10-14** : passage au preset Cinematic 3D, interface bleu nuit. Retour
  utilisateur : images et hero très appréciés, mais préférence pour le noir et
  l'orange d'avant, et un site jugé « pauvre et vieux » sous le hero.
- **2026-10-14, v2 « Noir & Blaze »** (ce système) : noir chaud et blaze
  d'origine, hero et visuels 3D conservés, sections refaites en familles
  distinctes (séquence sur rail, bento à matières, chiffres, FAQ en deux
  colonnes, inscription en blaze), nouvelle icône de l'app comme logo.
- **2026-10-14, v2.1** : retour utilisateur « pas propre », widgets « pas du
  tout les mêmes que ceux de l'app ou de Figma ». Captures iOS de l'App Store
  dans un cadre iPhone (fini le ruban DEBUG, les vignettes vides et le
  rectangle d'ombre), widgets reconstruits depuis le code de l'app dans ses
  polices, bento à six cellules, en-tête du groupe hors du téléphone. Ajouts
  demandés : apps de sport compatibles (annoncées « Bientôt », l'app n'en lit
  aucune) et emplacement pour les salles partenaires (vide, aucun partenariat
  à ce jour).
