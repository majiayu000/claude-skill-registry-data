---
name: design-redesign
description: Audit et modernisation d'un site ou d'une page web existants de {{COMPANY_NAME}} (ou d'un client) sans casser le fonctionnel — détection des patterns IA génériques, diagnostic typographie/couleur/layout/états/contenu, correctifs ciblés par ordre d'impact. Utiliser pour toute refonte, rafraîchissement ou « ce site fait daté / fait IA », en amont d'une réécriture de landing page. Vendorisée depuis taste-skill (redesign-existing-projects, MIT, Leonxlnx) — voir docs/vendored-design2.md.
---

# design-redesign — moderniser l'existant sans le casser

Cette skill traite les **refontes** : un site ou une page existe déjà, il faut l'élever au niveau premium sans réécrire de zéro. Pour un livrable neuf, utiliser `design-direction` + `design-system` + `design-taste`.

## Étape 0 — Charger les tokens de marque (OBLIGATOIRE)

**Charger `01-brand/style-guide.md` — la marque PRIME sur toute recommandation générique de cet audit.**

1. Si la page à refondre appartient à {{COMPANY_NAME}} : le style-guide fournit les valeurs cibles (couleurs, police, radius, interdits visuels). L'audit mesure l'écart entre l'existant et ces tokens.
2. Si la page appartient à un client/prospect externe : **extraire d'abord les tokens de marque existants** (couleurs, type, logo, radius) — ils sont le point de départ, pas une option. Une marque déjà violette reste violette.
3. Lire `01-brand/checklist-pre-composition.md` : les règles anti-style-IA s'appliquent aussi au texte de la page refondue.
4. Lire `01-brand/design-anti-generique.md` : l'audit détecte les patterns « IA générique » de l'existant — et la refonte n'en réintroduit jamais.
5. Si `01-brand/style-guide.md` contient des `{{...}}` et que la cible est la marque du template : s'arrêter et proposer `/start-cockpit`.

## Séquence

1. **Scanner** — lire le code. Identifier le framework, la méthode de styling (Tailwind, CSS vanilla, styled-components…), les patterns actuels.
2. **Classer le mode** — *Préserver* (moderniser sans toucher à la marque) ou *Refondre* (nouveau langage visuel, contenu et IA préservés). Si ambigu, poser UNE question : « préserver la marque existante, ou repartir visuellement de zéro ? »
3. **Diagnostiquer** — dérouler l'audit ci-dessous, lister chaque pattern générique, point faible et état manquant.
4. **Corriger** — appliquer des améliorations ciblées avec la stack existante. Ne jamais réécrire de zéro.

## Audit de design

### Typographie
- Fontes par défaut du navigateur ou Inter partout → remplacer par une fonte de caractère (Geist, Outfit, Cabinet Grotesk, Satoshi) — **sauf si la marque impose sa police**.
- Titres sans présence → augmenter la taille display, resserrer le letter-spacing, réduire le line-height.
- Body trop large → ~65 caractères max, line-height augmenté.
- Seulement 400 et 700 utilisés → introduire 500/600 pour une hiérarchie subtile.
- Chiffres en fonte proportionnelle sur interface data → `font-variant-numeric: tabular-nums` ou mono.
- Sous-titres tout-en-capitales partout → sentence case (cohérent avec la checklist de marque).
- Mots orphelins en fin de ligne → `text-wrap: balance` / `pretty`.

### Couleur et surfaces
- Fond `#000000` pur → off-black (`#0a0a0a`, `#121212`, navy sombre).
- Accents sursaturés → < 80 % de saturation ; plus d'un accent → en garder un seul.
- Gris chauds et froids mélangés → une seule famille de gris.
- Esthétique « gradient IA violet/bleu » (l'empreinte IA la plus courante) → bases neutres + un accent choisi.
- `box-shadow` générique → ombres teintées de la couleur de fond.
- Flat total sans texture → grain/noise/micro-motifs subtils.
- Direction de lumière incohérente entre les ombres → une seule source.
- Section sombre isolée dans une page claire (ou l'inverse) → soit un vrai dark mode complet, soit une teinte plus foncée de la même palette.
- Sections plates et vides → imagerie de fond (floutée, masquée, faible opacité), motifs, gradients ambiants. Placeholder fiable : `https://picsum.photos/seed/{nom}/1920/1080`.

### Layout
- Tout centré et symétrique → casser avec des marges décalées, des ratios mélangés, des titres alignés à gauche.
- Trois colonnes de cartes égales en features (LE layout IA générique) → zigzag 2 colonnes, grille asymétrique, scroll horizontal, masonry.
- `height: 100vh` → `min-height: 100dvh` (bug viewport iOS Safari).
- Calculs flexbox en pourcentages → CSS Grid.
- Pas de conteneur max-width → 1200-1440px avec marges auto.
- Border-radius uniforme sur tout → varier (plus serré à l'intérieur, plus doux sur les conteneurs) tout en respectant l'échelle du style-guide.
- Aucun chevauchement, aucune profondeur → marges négatives, superpositions.
- Boutons non alignés en bas des groupes de cartes → épingler les CTA en bas de chaque carte.
- Listes de features démarrant à des hauteurs différentes dans un pricing → même Y de départ partout.
- Centrage mathématique optiquement faux (icône + texte, play button) → ajustements optiques de 1-2px.
- Espace blanc manquant → doubler les espacements sur une page marketing.

### Interactivité et états
- Pas de hover sur les boutons → décalage de fond, léger scale ou translate.
- Pas de feedback pressé → `scale(0.98)` ou `translateY(1px)` sur `:active`.
- Transitions instantanées → 200-300ms sur tout élément interactif.
- Focus ring manquant → indicateurs visibles au clavier (exigence a11y, pas une option).
- Pas de loading → skeletons épousant le layout, pas de spinner générique.
- Pas d'empty state → vue « premiers pas » composée.
- Pas d'erreurs → messages inline pour les formulaires, jamais `window.alert()`.
- Liens morts (`href="#"`) → vraie destination ou désactivation visuelle.
- Pas d'indication de page courante dans la nav → styler le lien actif.
- Sauts d'ancre brutaux → `scroll-behavior: smooth`.
- Animations sur `top/left/width/height` → `transform` + `opacity`.

### Contenu
- « John Doe » → noms réalistes et variés ; chiffres trop ronds (`99.99%`, `50%`) → données organiques (`47,2 %`).
- Noms d'entreprises placeholder (« Acme Corp », « Nexus ») → noms contextuels crédibles.
- Clichés de copie IA → appliquer la section 2 de `01-brand/checklist-pre-composition.md` (vocabulaire mort, parallélismes négatifs, cadratin) ; en anglais, bannir aussi « Elevate », « Seamless », « Unleash », « Game-changer », « Delve ».
- Points d'exclamation dans les messages de succès → supprimer ; « Oups ! » → direct (« La connexion a échoué. Réessayez. ») ; voix passive → active.
- Dates de blog toutes identiques, même avatar partout, Lorem Ipsum → corriger systématiquement.

### Patterns de composants
- Carte générique (bordure + ombre + fond blanc) → bordure seule, OU fond seul, OU espacement seul.
- Toujours un bouton plein + un ghost → introduire des liens texte/tertiaires.
- FAQ en accordéon systématique → liste côte à côte, aide cherchable, disclosure inline.
- Carrousel de témoignages 3 cartes + points → mur masonry, posts sociaux intégrés, citation unique tournante.
- Pricing en 3 tours → mettre en avant l'offre recommandée par la couleur et l'emphase, pas la hauteur.
- Modales pour tout → édition inline, panneaux latéraux, sections dépliables.
- Footer ferme-à-liens 4 colonnes → simplifier aux chemins principaux + liens légaux.

### Iconographie
- Lucide/Feather exclusifs (le choix IA par défaut) → Phosphor, Heroicons ou set custom.
- Fusée pour « lancement », bouclier pour « sécurité » → métaphores moins évidentes.
- Épaisseurs de trait incohérentes → un seul strokeWidth ; favicon manquant → l'ajouter.
- Photos stock « équipe diverse » → vraies photos, candides, ou style d'illustration cohérent (voir `01-brand/assets/index.md` avant de générer quoi que ce soit).

### Qualité de code
- Soupe de div → HTML sémantique (`<nav>`, `<main>`, `<article>`, `<section>`).
- Styles inline mélangés aux classes → tout dans le système de styling du projet.
- Largeurs en pixels codées en dur → unités relatives.
- Alt manquants → décrire le contenu ; jamais `alt="image"`.
- `z-index: 9999` → échelle propre dans les variables.
- Code mort commenté → supprimer ; imports fantômes → vérifier `package.json`.
- Meta manquants → `<title>`, description, `og:image`, partage social.

### Omissions stratégiques (ce que l'IA oublie)
Liens légaux (confidentialité, mentions), navigation retour, page 404 brandée, validation de formulaires côté client, lien « aller au contenu », bannière cookies si juridiction l'exige.

## Techniques d'upgrade (à piocher selon le besoin)

- **Typo** : fontes variables animées (graisse au scroll), transitions contour→rempli, text mask reveals.
- **Layout** : grille cassée / asymétrie calculée, maximisation du blanc, piles de cartes en parallax, split-screen scroll.
- **Motion** : smooth scroll avec inertie, entrées en cascade (jamais tout monté d'un coup), spring physics au lieu d'easing linéaire, reveals pilotés par le scroll (utiliser les squelettes GSAP canoniques de la skill `design-taste` §6).
- **Surfaces** : vrai glassmorphism (bordure interne 1px + ombre interne), spotlight borders, grain overlay fixe `pointer-events-none`, ombres teintées.

## Priorité des correctifs (impact max, risque min)

1. **Swap de fonte** — plus grosse amélioration instantanée, risque minimal
2. **Nettoyage de palette** — retirer les couleurs criardes ou en conflit
3. **États hover/active** — l'interface prend vie
4. **Layout et espacement** — grille propre, max-width, padding cohérent
5. **Remplacement des composants génériques** — swap des patterns clichés
6. **États loading/empty/erreur** — l'impression de fini
7. **Polish de l'échelle typographique** — la touche premium finale

## Ce qui ne change JAMAIS silencieusement

Sans validation humaine explicite : structure d'URL / slugs, labels de navigation principale, noms et ordre des champs de formulaire (casse l'analytics et l'autofill), logo/wordmark, textes légaux et de consentement. **La migration SEO est le risque n°1 d'une refonte** : relever les pages qui rankent, les meta, le structured data avant de toucher quoi que ce soit (la skill `seo` et le plugin claude-seo aident).

## Règles

- Travailler avec la stack existante. Aucune migration de framework ou de librairie de styling.
- Ne rien casser : tester après chaque changement.
- Vérifier le fichier de dépendances avant tout nouvel import ; vérifier la version Tailwind (v3 vs v4) avant de toucher la config.
- Changements petits, ciblés, relisibles — pas de grandes réécritures.
- Préserver la voix de la copie sauf demande de réécriture ; ne jamais régresser les acquis d'accessibilité (focus, alt, clavier, contraste) ni renommer ce dont le tracking dépend.

---

*Vendorisée et adaptée depuis [taste-skill](https://github.com/Leonxlnx/taste-skill) de Leonxlnx (skill `redesign-existing-projects`, licence MIT). Attribution et procédure de re-synchronisation : `docs/vendored-design2.md`.*
