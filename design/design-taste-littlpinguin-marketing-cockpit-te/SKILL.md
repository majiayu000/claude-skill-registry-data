---
name: design-taste
description: Protocole d'exécution anti-slop pour tout livrable web de {{COMPANY_NAME}} — landing pages, pages statiques, portfolios, sections marketing. Trois curseurs paramétriques (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY), inférence du langage design depuis le brief, squelettes GSAP canoniques, bans typographiques et pre-flight check strict. Utiliser en complément de design-system (tokens) et landing-page (structure) chaque fois qu'un rendu web risque de ressembler à du template IA générique. Vendorisée depuis taste-skill v2 (MIT, Leonxlnx) — voir docs/vendored-design2.md.
---

# design-taste — protocole d'exécution anti-slop

Cette skill ne choisit pas un style : elle empêche l'exécution de ressembler à du design généré. Elle s'applique aux landing pages, pages marketing, portfolios et redesigns. Pas aux dashboards denses, tables de données ou product UI multi-étapes (utiliser un design system officiel pour ça).

## Complémentarité avec les skills design du template

| Skill | Rôle | Quand |
|---|---|---|
| `ui-ux-pro-max` (plugin) | **Base de données de choix** : 161 palettes, 57 paires de fontes, 50+ styles | « Quel style/palette/fonte pour ce produit ? » |
| `design-system` | Génère les tokens sémantiques sous contrainte de marque | Avant de coder un livrable web |
| `design-direction` | Choix de la direction visuelle d'un livrable | En amont, phase de cadrage |
| **`design-taste`** (cette skill) | **Protocole d'exécution** : curseurs, hard rules, anti-tells, pre-flight | Pendant et après l'écriture du code |
| `design-redesign` | Audit + modernisation d'un existant | Refonte d'une page/site déjà en ligne |

Ordre type : `design-direction` → `design-system` → production (landing-page, slides…) **avec cette skill comme garde-fou** → pre-flight check.

## Étape 0 — Charger les tokens de marque (OBLIGATOIRE)

**Charger `01-brand/style-guide.md` — la marque PRIME sur les curseurs et sur toute règle esthétique de cette skill.**

1. Lire `01-brand/style-guide.md` : couleurs, police, radius, gradient, style d'illustration, interdits visuels.
2. Lire `01-brand/checklist-pre-composition.md` : règles anti-style-IA et typographiques de la marque — en cas de conflit avec les bans de cette skill, **la checklist de marque fait foi** (ex. : la checklist autorise le demi-cadratin `–` ; le ban absolu de cette skill ne porte alors que sur le cadratin `—`).
   Lire aussi `01-brand/design-anti-generique.md` : la doctrine design anti-générique du template — même logique de préséance (marque > doctrine > bans de cette skill).
3. Classer : dimension **verrouillée par la marque** (couleur primaire, police, radius fournis par le style-guide → interdiction d'y déroger, même si un ban ci-dessous suggère autre chose) vs **libre** (le style-guide est muet → cette skill s'applique pleinement).
4. Si `01-brand/style-guide.md` manque ou contient des `{{...}}` : s'arrêter et proposer `/start-cockpit`.

Exemple de préséance : la règle « LILA » ci-dessous décourage le violet par défaut — mais si la marque est violette, elle reste violette (c'est l'override prévu).

---

## 1. Lecture du brief (avant tout code)

Ne jamais sauter vers une esthétique par défaut. Lire d'abord :

1. **Type de page** — landing (SaaS / consumer / agence / événement), portfolio, redesign (préserver vs refondre), éditorial.
2. **Mots d'ambiance** du brief — « minimaliste », « Linear-style », « premium », « brutaliste », « éditorial », « B2B sérieux »…
3. **Signaux de référence** — URLs, screenshots, concurrents nommés.
4. **Audience** — c'est elle qui choisit l'esthétique, pas votre goût.
5. **Contraintes silencieuses** — accessibilité renforcée, secteur régulé, confiance d'abord. Elles PRIMENT sur la préférence esthétique.

**Déclarer une « lecture design » en une ligne avant de générer** : *« Je lis ceci comme : \<type de page> pour \<audience>, langage \<ambiance>, penchant vers \<famille esthétique ou design system>. »*

Si le brief est ambigu : poser **une seule** question de clarification (jamais une rafale). Si l'inférence est confiante, déclarer la lecture et avancer.

**Discipline anti-défaut** : jamais de gradient violet-IA, de hero centré sur mesh sombre, de trois cartes features identiques, de glassmorphism générique partout, de micro-animations en boucle sur tout, de Inter + slate-900 par réflexe. Ce sont les défauts du modèle — s'en écarter délibérément selon la lecture.

## 2. Les trois curseurs

Après la lecture design, fixer trois valeurs. Toute décision de layout, motion et densité en découle.

- **`DESIGN_VARIANCE`** — 1 = symétrie parfaite, 10 = chaos artistique
- **`MOTION_INTENSITY`** — 1 = statique, 10 = cinématique / physique
- **`VISUAL_DENSITY`** — 1 = galerie d'art / aéré, 10 = cockpit / données denses

Baseline : `8 / 6 / 4`. Overrides conversationnels, jamais silencieux.

### Inférence lecture → curseurs

| Signal du brief | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| minimaliste / calme / éditorial / Linear-style | 5-6 | 3-4 | 2-3 |
| premium consumer / luxe / Apple-y | 7-8 | 5-7 | 3-4 |
| joueur / expérimental / Awwwards / agence | 9-10 | 8-10 | 3-4 |
| landing / portfolio / site marketing (défaut) | 7-9 | 6-8 | 3-5 |
| confiance d'abord / secteur public / régulé / a11y critique | 3-4 | 2-3 | 4-5 |
| redesign — préserver | = existant | +1 | = existant |
| redesign — refondre | +2 | +2 | = existant |

### Définitions techniques

- **VARIANCE 1-3** : grille symétrique 12 colonnes, paddings égaux, centré. **4-7** : chevauchements (`margin-top: -2rem`), ratios d'image variés, titres alignés à gauche. **8-10** : masonry, colonnes fractionnaires (`2fr 1fr 1fr`), grandes zones vides (`padding-left: 20vw`). **Override mobile obligatoire** : niveaux 4-10 collapsent en une colonne stricte sous 768px.
- **MOTION 1-3** : `:hover`/`:active` seulement. **4-7** : transitions fluides (`cubic-bezier(0.16,1,0.3,1)`), cascades d'entrée, uniquement `transform`/`opacity`. **8-10** : chorégraphie scroll (GSAP ScrollTrigger ou CSS `animation-timeline`). `window.addEventListener('scroll')` est un ban dur.
- **DENSITY 1-3** : `py-32` à `py-48`, très aéré. **4-7** : `py-16` à `py-24`. **8-10** : paddings serrés, filets 1px au lieu de cartes, `font-mono` obligatoire pour les chiffres.

## 3. Brief → design system

Si le brief correspond à un système officiel, installer le **paquet officiel**, ne pas recréer son CSS : Material (`@material/web`), Fluent (`@fluentui/react-components`), Carbon (`@carbon/react`), Polaris (Shopify), Atlaskit, Primer (GitHub), `govuk-frontend`/`uswds` (secteur public), Bootstrap 5.3 (MVP rapide), Radix Themes, shadcn/ui (jamais en état par défaut), Tailwind v4 (défaut indé/SaaS moderne). **Un seul système par projet.**

Si le brief est une **esthétique** sans paquet officiel (glassmorphism, bento, brutalisme, éditorial, dark tech, aurora, typographie cinétique) : CSS natif + Tailwind, en étant honnête en commentaire sur ce qui est approximation (ex. « Liquid Glass » web = approximation glassmorphism, il n'existe pas de `liquid-glass.css` officiel Apple).

## 4. Stack et conventions par défaut

- **Framework** : React/Next.js, Server Components par défaut. Tout composant avec motion/scroll/pointer = feuille isolée `'use client'`.
- **Styling** : Tailwind v4 (plugin `@tailwindcss/postcss`, pas `tailwindcss` dans postcss.config).
- **Animation** : Motion (`import { motion } from "motion/react"`). Jamais `useState` pour des valeurs continues (souris, scroll) → `useMotionValue` / `useTransform` / `useScroll`.
- **Fontes** : `next/font` ou `@font-face` auto-hébergé + `font-display: swap`. Jamais de `<link>` Google Fonts en production.
- **Icônes** : Phosphor > HugeIcons > Radix > Tabler. Lucide sur demande explicite seulement. **Jamais de SVG d'icône dessiné à la main.** Une famille par projet, `strokeWidth` global.
- **Emoji** : découragés dans le code et le texte visible (cohérent avec la checklist de marque §3).
- **Layout** : conteneur `max-w-[1400px] mx-auto` ; `min-h-[100dvh]` jamais `h-screen` ; CSS Grid plutôt que calculs flexbox en pourcentages.
- **Dépendances** : vérifier `package.json` avant tout import ; sortir la commande d'installation d'abord.

## 5. Directives d'exécution (correction de biais)

### 5.1 Typographie
- Display : `text-4xl md:text-6xl tracking-tighter leading-none`. Body : `text-base leading-relaxed max-w-[65ch]`.
- Sans par défaut : Geist, Outfit, Cabinet Grotesk, Satoshi (Inter seulement si demandé ou brief neutre/a11y). **Si la marque impose une police, elle s'impose.**
- **Discipline serif** : le réflexe « brief créatif = serif » est le tell IA le plus testé. Serif acceptable uniquement si la marque la nomme, ou si l'univers est authentiquement éditorial/luxe/patrimoine ET justifiable. `Fraunces` et `Instrument Serif` bannis comme défauts. Emphase dans un titre = italique/gras de la MÊME fonte, jamais un mot serif injecté dans un titre sans-serif.
- **Dégagement des descendantes en italique** : mot italique avec `y g j p q` en display → `leading-[1.1]` minimum + réserve `pb-1`.

### 5.2 Couleur
- Max 1 couleur d'accent, saturation < 80 % par défaut. **Règle LILA** : pas de violet-IA/gradients néon par défaut — sauf si la marque est violette (override assumé, exécuté avec intention).
- **Verrou de cohérence couleur** : un accent choisi = utilisé sur TOUTE la page. Pas de CTA bleu surgissant en section 7 d'un site gris chaud.
- **Ban palette premium-consumer** : le réflexe beige/crème + laiton/terre-cuite/ocre + espresso pour tout brief artisan/bien-être/luxe est banni comme défaut (c'est LA palette IA du secteur). Alternatives à faire tourner : luxe froid (argent/chrome), forêt (vert profond + os + ambre), noir + tan, cobalt + crème, terracotta + ardoise, monochrome + un seul pop saturé. Override uniquement si la marque nomme ces couleurs.
- Une seule famille de gris (chaude OU froide) par projet.

### 5.3 Layout — hard rules (échouer l'une = livrable cassé)
- **Le hero tient dans le viewport initial** : titre ≤ 2 lignes desktop, sous-texte ≤ 20 mots et ≤ 4 lignes, CTA visible sans scroll. Un titre hero sur 4 lignes est une erreur de taille de police, pas de longueur de texte.
- **Discipline de pile hero (max 4 éléments texte)** : eyebrow OU brand strip (zéro ou un), titre, sous-texte, CTAs (1 primaire + max 1 secondaire). Bannis dans le hero : mini-tagline sous les CTA, micro-strip de confiance, teaser pricing, liste de features, rangée d'avatars. Padding haut max `pt-24`.
- Le mur de logos « Trusted by » vit SOUS le hero, jamais dedans.
- **Anti-centrage** : hero centré évité si `DESIGN_VARIANCE > 4` (split 50/50, asymétrie, structures scrollées). OK pour brief manifeste/éditorial.
- **Navigation** : une seule ligne desktop, hauteur ≤ 80px.
- **Retenue des eyebrows** (règle la plus violée en test) : maximum 1 eyebrow (label uppercase tracking au-dessus d'un titre de section) pour 3 sections, hero compris. Check mécanique : compter les `uppercase tracking` ; si count > ceil(nbSections / 3), échec. À la place : rien — le titre suffit.
- **Ban split-header** : « gros titre à gauche + petit paragraphe explicatif flottant à droite » comme en-tête de section = banni par défaut. Empiler verticalement (titre puis body max-w 65ch).
- **Cap zigzag** : max 2 sections consécutives en alternance image/texte. La 3e = échec pre-flight. Casser avec une pleine largeur, un bento, une marquee.
- **Répétition de famille de layout** : une famille (3 cartes, citation pleine largeur, split texte/image…) apparaît au plus UNE fois par page ; ≥ 4 familles différentes pour 8 sections.
- **Bento** : exactement autant de cellules que de contenus (jamais de tuile vide) ; 2-3 cellules minimum avec vraie variation visuelle (image, gradient de marque, motif) — pas 6 cartes blanc-sur-blanc.
- Collapse mobile explicite par section pour tout multi-colonnes.

### 5.4 Surfaces, états, formulaires
- Cartes uniquement quand l'élévation exprime une vraie hiérarchie ; sinon `border-t`, `divide-y`, espace négatif. Ombres teintées de la couleur de fond, jamais noir pur.
- **Verrou de forme** : UNE échelle de border-radius par page (tout-carré, tout-doux 12-16px, ou tout-pilule), ou une règle documentée appliquée partout.
- États complets obligatoires : loading (skeletons épousant le layout final, pas de spinner), empty (composé, indique comment remplir), erreur (inline pour formulaires), feedback tactile (`:active` → `scale-[0.98]`).
- **Contraste CTA obligatoire** : chaque bouton lisible sur son fond (WCAG AA 4,5:1 ; 3:1 pour ≥ 18px). Boutons fantômes sur photo → scrim ou bordure. **Le libellé d'un CTA tient sur une ligne** (3 mots max). **Un seul libellé par intention** sur la page (pas « Contactez-nous » + « Parlons-en » + « Écrivez-nous »).
- Formulaires : label AU-DESSUS de l'input, erreur dessous, jamais de placeholder-comme-label. Contraste AA sur placeholders, focus rings, helpers.

### 5.5 Images et assets visuels
Priorité : **1)** outil de génération d'images s'il existe (dans ce template : skill `image-generation`, après consultation de `01-brand/assets/index.md` — un asset existant se réutilise, il ne se régénère pas) ; **2)** vraies photos (`https://picsum.photos/seed/{seed-descriptif}/{w}/{h}`, sources de marque) ; **3)** en dernier recours, slots placeholder étiquetés (`<!-- TODO: photo hero produit, 1600x1200 -->`) et le dire à l'utilisateur.
- Même un site minimaliste a besoin de 2-3 vraies images. Une page 100 % texte n'est pas du minimalisme, c'est un travail incomplet.
- **Fake screenshots en `<div>` bannis** (faux dashboard, fausse task-list, faux terminal) : vraie capture, image générée, vrai mini-composant, ou rien.
- Mur de logos : vrais SVG (Simple Icons : `https://cdn.simpleicons.org/{slug}`) ou monogramme SVG généré pour une marque inventée — jamais de wordmarks en texte brut. **Logo wall = logos et rien d'autre** (pas de label de catégorie sous chaque logo).
- SVG décoratifs dessinés à la main : fortement découragés hors demande explicite.

### 5.6 Densité de contenu et copie
- Forme par défaut d'une section : titre court (≤ 8 mots) + sous-paragraphe (≤ 25 mots) + un visuel OU un CTA.
- Pas de sections data-dump (table de 20 lignes sur une page marketing) : top 3-5 + lien « tout voir », carrousel, ou autre page. Liste > 5 items = autre composant (grille de cartes, tabs, pills scroll-snap, chunks groupés), pas un `<ul>` plus long avec un filet sous chaque ligne.
- **Auto-audit de copie obligatoire avant livraison** : relire chaque chaîne visible ; réécrire tout ce qui est grammaticalement cassé, à référent flou, ou qui « sonne LLM profond ». Une phrase plate vaut mieux qu'une phrase mignonne-mais-fausse. (La checklist de marque §2 et la skill `copy-editing` complètent ce point.)
- **Chiffres faussement précis bannis** : `92 %`, `4,1×` inventés pour l'esthétique = non. Soit une vraie donnée sourcée (`_sources/reports/`, messaging-framework), soit explicitement étiqueté mock.
- Citations : ≤ 3 lignes, attribution nom + rôle (+ entreprise), vrais guillemets typographiques.
- **Verrou de thème** : la page a UN thème (clair, sombre ou auto). Aucune section n'inverse le mode en plein scroll (exception : un « color block story » délibéré, une fois par page).

## 6. Motion — squelettes canoniques GSAP

**Motion motivée obligatoire** : chaque animation se justifie en une phrase (hiérarchie, narration, feedback, transition d'état). « Ça faisait joli » = suppression. **Marquee : max une par page.** « Motion annoncée = motion livrée » : si `MOTION_INTENSITY > 4` la page bouge vraiment, sinon baisser le curseur à 3 et livrer un statique propre.

### 6.A Sticky-stack (pile de cartes au scroll)

Échec classique : le trigger part à mi-scroll au lieu de s'épingler en haut. Correctif : `start: "top top"`.

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // épingler en haut du viewport
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div key={i} className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center">
          {card}
        </div>
      ))}
    </div>
  );
}
```

Points critiques : `start: "top top"`, `pin: true`, chaque carte sauf la dernière est épinglée, le scale/opacity est piloté par le trigger de la carte SUIVANTE.

### 6.B Pan horizontal (scroll-hijack)

Échec classique : l'animation démarre avant l'épinglage, l'utilisateur voit une demi-slide. Même correctif : `start: "top top"`, épingler le wrapper, scruber la piste interne.

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",
          end: () => `+=${distance}`,                    // longueur de scroll = déplacement horizontal
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">{children}</div>
    </section>
  );
}
```

### 6.C Reveal en cascade (alternative légère, sans pinning)

Pour « les éléments apparaissent en entrant dans le viewport », préférer Motion `whileInView` — garder GSAP pour le vrai pin/scrub.

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

### 6.D Patterns d'animation interdits
- `window.addEventListener("scroll", ...)` — banni (jank, pas de batching). Utiliser `useScroll()` (Motion), ScrollTrigger, IntersectionObserver ou CSS scroll-driven animations.
- Calculs de progression avec `window.scrollY` en state React ; boucles `requestAnimationFrame` qui touchent le state React → motion values.
- Jamais GSAP/Three.js et Motion mélangés dans le même arbre de composants.

## 7. Garde-fous performance et accessibilité

- Animer UNIQUEMENT `transform` et `opacity`. `will-change` avec parcimonie.
- **`prefers-reduced-motion` obligatoire** pour tout `MOTION_INTENSITY > 3` : boucles infinies, parallax, scroll-hijack et physique magnétique collapsent en statique.
- **Dark mode** : concevoir les deux modes dès le départ (sauf éditorial imitant l'imprimé, ou décision de marque). Une stratégie de tokens par projet (`dark:` OU variables CSS). Jamais de `#000000` ni `#ffffff` purs. Hiérarchie et fidélité de marque équivalentes dans les deux modes. Tester les deux avant de livrer.
- Core Web Vitals : LCP < 2,5s (hero en `priority`/preload), INP < 200ms, CLS < 0,1.
- Grain/noise uniquement sur pseudo-éléments `fixed inset-0 pointer-events-none` — jamais sur un conteneur scrollable.
- Échelle de z-index documentée, pas de `z-[9999]` arbitraires.

## 8. Tells IA (patterns interdits)

Complète la section 2 de `01-brand/checklist-pre-composition.md` (qui couvre le texte) avec les tells **visuels** :

- **Visuel/CSS** : glows néon, noir pur, accents sursaturés, gradient-text sur les gros titres, curseurs souris custom.
- **Layout** : trois cartes features identiques ; paddings mathématiquement parfaits sans intention.
- **Contenu** : « John Doe »/avatars œufs ; chiffres trop ronds (`99.99%`) ; noms de marque slop (« Acme », « Nexus », « SmartFlow ») ; verbes creux (« Elevate », « Seamless », « Unleash »).
- **Micro-labels** : eyebrows numérotés (`001 · Capabilities`, `00 / INDEX`) ; labels de version dans le hero (`V0.6`, `BETA`) hors brief de lancement ; pagination `01 / 4` sur les images ; point médian `·` rationné (max 1 par ligne de métadonnées) ; points de statut colorés décoratifs.
- **Copie marketing** : « Quietly trusted by », labels poétiques (« From the field », « On our desks »), strips météo/locale (« LIS 14:23 · 18°C »), micro-méta-phrases sous les eyebrows, étiquettes d'étapes génériques (« Step 1 / Step 2 » — le verbe d'action EST le label).
- **Décoration** : pills/tags posés sur les photos ; crédits photo décoratifs (« Field study no. 12 ») ; footers de version (`v1.4.2`) sur page marketing ; strip mono-caps en bas de hero (`DESIGN · BUILD · SHIP`) ; texte vertical pivoté ; **scroll cues bannis** (« ↓ scroll », « Scroll to explore ») ; `border-t` + `border-b` sur chaque ligne d'une longue liste ; barres de progression avec piste de fond comme visuel comparatif.
- **Tiret cadratin (`—`)** : banni partout dans le rendu (titres, body, citations, boutons, alt). Conformément à la checklist de marque §2b : demi-cadratin `–`, virgule, deux-points, parenthèses ou reformulation.

## 9. Pre-flight check final

À dérouler avant de livrer le code. **Une case qui ne se coche pas honnêtement = le livrable n'est pas fini.**

- [ ] Tokens `01-brand/style-guide.md` chargés et respectés (dimensions verrouillées intactes) ?
- [ ] Lecture design déclarée en une ligne ; curseurs explicités et motivés ?
- [ ] Design system officiel choisi si applicable, esthétique étiquetée honnêtement sinon ?
- [ ] **Zéro cadratin `—`** visible ; règles typo de la checklist de marque respectées (pas de point final sur les titres, sentence case) ?
- [ ] Un seul thème sur la page ; un seul accent ; une seule échelle de radius ?
- [ ] Contraste AA sur chaque CTA et champ de formulaire ; aucun libellé de CTA qui wrappe ; une intention = un libellé ?
- [ ] Hero : ≤ 2 lignes de titre, ≤ 20 mots de sous-texte, ≤ 4 éléments texte, CTA visible, `pt-24` max ?
- [ ] Eyebrows ≤ ceil(nbSections / 3) ; pas de split-header ; ≤ 2 zigzags consécutifs ; ≥ 4 familles de layout ; bento sans cellule vide et avec variation visuelle ?
- [ ] Vraies images (génération ou picsum-seed ou slots étiquetés) ; zéro fake screenshot en div ; logos SVG réels ; logo wall sans labels ?
- [ ] Copie auto-auditée ; pas de chiffres inventés ; citations ≤ 3 lignes attribuées ?
- [ ] Motion motivée, livrée si annoncée, `prefers-reduced-motion` partout au-dessus de 3, squelettes GSAP conformes (`start: "top top"`, `pin: true`), zéro `addEventListener('scroll')`, cleanups `useEffect` stricts ?
- [ ] Dark mode testé dans les deux modes ; `min-h-[100dvh]` ; collapse mobile explicite ?
- [ ] États loading/empty/erreur fournis ; icônes d'une seule famille autorisée ; aucun tell de la section 8 ?
- [ ] Core Web Vitals plausibles ; un seul design system dans l'arbre ?

---

*Vendorisée et condensée depuis [taste-skill](https://github.com/Leonxlnx/taste-skill) de Leonxlnx (skill `design-taste-frontend` v2, licence MIT). Attribution, périmètre retenu et procédure de re-synchronisation : `docs/vendored-design2.md`.*
