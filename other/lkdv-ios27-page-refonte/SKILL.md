---
name: lkdv-ios27-page-refonte
description: Use when redesigning, migrating, or auditing any LKDV application page (clubs, carnets, groupes, evenements, explorer, materiel, messagerie) to match the consolidated Oct 24 2026 Compte + Communauté v3 + Carnet Profile grammar (zero main-page scroll, 406px r24 card, in-card DrawerShell, inline PostGlassPanel feed, 3D MapLibre split, and strict measured tokens).
---

# LKDV iOS 27 Liquid Glass (Oct 24 Consolidated) — Skill de Refonte & Adaptation Métier

Guide technique et architectural de référence pour décliner la grammaire mesurée de **`/compte`** (v20 modulaire) et **`/communaute`** (v3 « Pour toi » + `PostGlassPanel`) sur les pages de l'application (`/clubs`, `/clubs/[id]`, `/carnets`, `/groupes`, `/evenements`, etc.).

> **Principe Directeur :** On conserve **100 % de la forme, de la géométrie et des tokens mesurés** des éléments de `/compte` et `/communaute`, mais **on adapte intelligemment le contenu et la disposition métier** à chaque page. La scène principale est **strictement interdite au scroll global (`100dvh`, `overflow: hidden`)** : l'écran principal reste ultra-simple et épuré, et toute la richesse fonctionnelle est distribuée dans les **drawers en place dans la carte (`DrawerShell` / `SlotShell`)**, les **sous-drawers (`.lkdv-drawer-secondary` 30px)** et les **panneaux de post superposés (`PostGlassPanel`)**.

---

## 1. Invariants Absolus (Règles non négociables)

1. **Zéro modification dans `/compas`** : `src/app/compas/**` et `src/features/compas/**` ne doivent jamais être modifiés ni importer de code des refontes.
2. **Zéro scroll de page principale (`100dvh` verrouillé)** :
   - Le châssis principal (`.phone`) occupe `100dvh` avec `overflow: hidden` et un split **Carte Haute (60%) / Carte 3D MapLibre Basse (40%)** (et mode `.mapbig` `172px / 1fr`).
   - Seul l'intérieur de la carte (`.card-scroll`), du volet actif d'un drawer (`.lkdv-drawer-pane.active`) ou du corps d'un panneau de post (`.lkdv-post-panel-body`) peut scroller (`overscroll-behavior: contain`).
3. **Une seule barre de navigation basse (`.tb` `402 × 48px`)** :
   - La route doit être déclarée dans `HIDE_CHROME_PREFIXES` de `src/components/mobile-nav/MobileNavWrapper.tsx` pour éviter toute double barre de navigation.
4. **Le Drawer EST la Carte (aucun modal plein écran, aucun voile sombre, aucun titre, aucune croix)** :
   - Ouvrir un drawer remplace le contenu de la carte hôte (`406 × n`, `border-radius: 24px`, calé via `syncCardBounds()`).
   - Il ajoute uniquement une **poignée `.grab` (`18px`, barre `40 × 4px`)**, une **capsule haute `.lkdv-capsule` (`378 × 48px`, icônes seules)** et, si nécessaire, une **sous-capsule flottante `.ig-tabs-float` (`30px`, bas-droite, icônes seules)**.
   - Fermeture par : clic/swipe sur la poignée `.grab`, re-clic sur l'icône active, touche `Échap`, ou clic sur la carte 3D.
5. **Sélecteurs 100 % Icônes Seules** :
   - Aussi bien dans la capsule haute `48px` (`.lkdv-capsule` / `.segc.lg-tabs`) que dans la sous-capsule flottante `30px` (`.ig-tabs-float .ig-tabs`) et la barre basse `.tb` `48px` : **icônes SVG pures (18–19px) uniquement**, aucun libellé texte visible. `role="tablist"`, `role="tab"`, `aria-label` et `aria-selected` sont obligatoires.
6. **Système de Post Partagé (`PostGlassPanel` + `post-system.css`)** :
   - Quand une carte intègre un fil d'actualité (comme sur Communauté ou Club), chaque post utilise `.lkdv-feed-post` (carré `1:1` média ou `.lkdv-feed-post--text` verre Compte).
   - Les commentaires et le partage ne s'ouvrent **jamais** dans une feuille plein écran : ils s'ouvrent en **panneau verre superposé au post (`.lkdv-post-panel-slot`)** démarrant `8px` sous le header du post (`--post-panel-top: 64px`), laissant toujours la pastille auteur `.pmi-author` et le bouton `···` visibles et cliquables.
   - Swipe horizontal sur le post = bascule Commentaires ↔ Partage ; swipe bas = ferme le panneau.
7. **Matériau Liquid Glass Clair exclusif & Palette Forest** :
   - Aucun mode sombre, jamais de `rgba(0,0,0)` brut, jamais d'orange `#E4501C`, jamais d'aplat vert plein `#17402C` sur les boutons d'onglets des drawers (utiliser `--pg` et la lentille verre).
8. **Sécurité & Vérité des données** :
   - Profils publics chargés en 2 étapes via `fetchPublicProfilesWith(supabase, userIds)` (`@/lib/queries/publicProfilesCore`).
   - Échappement XSS systématique (`esc()`) dans tout HTML runtime.
   - Compteurs réels (requêtes `count` ou lignes réelles, jamais de métriques inventées).

---

## 2. Tokens Mesurés (Source de Vérité 430 × 932)

Aucune valeur hors de ces tokens mesurés sur `/compte` et `/communaute` ne doit être inventée :

| Élément / Token | Valeur Mesurée | Origine (`13-comparatif-compte-communaute.md`) |
|---|---|---|
| **Largeur colonne / Gouttière** | Viewport `430px`, gouttière **`12px`** | Carte Compte à `x = 12` sur `430` |
| **Carte principale (`.card.cs`)** | Largeur **`406px`** (`430 - 2×12`), **`border-radius: 24px`**, padding `14px` | `.card.cs` sur `/compte` |
| **Verre de carte & panneau** | `linear-gradient(180deg, rgba(255,255,255,.486), rgba(255,255,255,.384))` + `blur(25.2px) saturate(1.8) brightness(1.05)` | `.card.cs` & `post-system.css` |
| **Ombre de carte** | `inset 0 1px 0 rgba(255,255,255,.95), inset 0 -1px 1px rgba(255,255,255,.4), 0 0 0 .5px rgba(23,43,36,.10), 0 8px 22px rgba(23,43,36,.10)` | `.card.cs` |
| **Top Bar (`.head`)** | Hauteur **`56px`** (`8 + 40 + 8`), pilule identité/contexte **`40px`** + boutons ronds `.gbtn` **`38 × 38px`** (`r=50%`) | `/compte` & `/communaute` |
| **Avatar / Blason / Cover** | **`66 × 66px`** (`r=50%` profil ou `r=18px` blason club / couverture carnet) | `.ig-avi-wrap` |
| **Cellules Statistiques (`.ig-stat`)** | 3 boutons cliquables **`101 × 39px`**, **`border-radius: 14px`** | Ouvrent chacune un drawer ou volet dédié |
| **Typo Statistique** | Valeur : **`19px / 700`** (`letter-spacing: -0.38px`) · Libellé : **`10.5px / 500`**, `#56665d`, **sans majuscules** | `.num` & label Compte |
| **Titre dans la carte** | **`19px / 700`** (plafond typographique strict de la carte) | `.card.cs` |
| **Bio / Description** | **`12px / 1.3`**, couleur `#56665d`, 2–3 lignes max | `.ig-bio-text` |
| **Actions rapides / Cercles (`.ig-hl`)** | Bloc `72 × 56px` : **cercle `44 × 44px`** + libellé **`9px / 500`** dessous | Highlights / Actions rapides Compte |
| **Enveloppe Flux / Grille dans carte** | `border-radius: 22px` (`.ig-grid-wrap` ou conteneur de flux interne) | Dans `.card.cs` |
| **Post inline (`.lkdv-feed-post`)** | Carré `1:1` (média) ou auto plafonné (`.lkdv-feed-post--text`), `r=22px` (en carte) ou `28px` (en fil), auteur `.pmi-author` (avatar `28px`, nom `12/600`, meta `10.5`), bouton `···` `34×34`, capsule actions **`116 × 40px`** (boutons `34×34 r=50%`) | `CommunityFeedPost.tsx` & `post-system.css` |
| **Panneau Post (`PostGlassPanel`)** | `.lkdv-post-panel-slot` à `top: 64px` (`8px` sous le header du post), verre Compte, swipe G/D (Commentaires ↔ Partage), composer pilule `36px` + envoi `34px` en bas | `PostGlassPanel.tsx` |
| **Poignée de Drawer (`.grab`)** | Zone **`18px`** en haut de la carte-drawer, barre **`40 × 4px`**, `rgba(23,43,36,.35)` | `#sheet .grab` |
| **Capsule de Drawer (`.lkdv-capsule`)** | **`378 × 48px`** (`406 - 2×14`), lentille **`74 × 40px`** (`calc((100% - 6px)/var(--n))`), **icônes 18px seules**, transition `420ms cubic-bezier(.32,.72,0,1)` | `DrawerShell.tsx` / `SlotSelector.tsx` |
| **Sous-capsule flottante (`.ig-tabs-float`)** | Hauteur **`30px`**, largeur `calc(var(--n)*44px + 5px)`, lentille `25px`, `right: 10px; bottom: 10px`, **icônes seules** + zone tactile `44px` (`::after`) | `DrawerShell.tsx` & `.ig-tabs-float` |
| **Barre basse (`.tb`)** | **`402 × 48px`** à `x = 14` (`min(100% - 28px, 500px)`), lentille `40px`, icônes seules | `AccountBottomBar` / `.tb` |
| **Couleurs d'encre** | Encre primaire `#17402c` / `#172B24` · Muted `#56665d` · Like `#e0245e` · Fond `#cfd6c8` (`account-bg.webp`) | Socle partagé |

---

## 3. Architecture Type : Adapter la Forme Compte + Communauté à un Nouveau Métier (ex. Club)

### Principe d'Adaptation (Même Forme, Disposition & Contenu Métier Adaptés)

Au lieu de copier-coller le contenu d'un profil personnel, chaque page recompose les **briques canoniques** de `/compte` et `/communaute` autour de son usage réel, tout en gardant **zéro scroll sur la page principale** :

```
┌──────────────────────────────────────────────────────────┐  Viewport 100dvh (overflow: hidden)
│  Dynamic Island (#island) + Status                       │
│  Top Bar 56px : [Pilule Sélecteur/Membre 40px] [🔍38][+38]│
│ ┌──────────────────────────────────────────────────────┐ │  Carte 406px, r=24, verre .cs (Zone 60%)
│ │ ┌──────┐   [ 101×39 ]    [ 101×39 ]    [ 101×39 ]    │ │  Blason 66px (r18) + 3 cellules stats 19/700
│ │ │ 66px │    Membres       Sorties       Km / Défis   │ │  Chaque stat ouvre directement son Drawer !
│ │ └──────┘                                             │ │
│ │  Nom du Club (19/700) · Massif · Badge vérifié       │ │  Méta 11/10.5 muted + Bio 12/1.3 (2 lignes)
│ │  (⚡44)     (🏕️44)     (🎒44)     (🏆44)     (➕44)  │ │  Cercles 44px + label 9px → ouvrent Drawers
│ │  ┌────────────────────────────────────────────────┐  │ │
│ │  │ FIL D'ACTU DU CLUB (remplace la grille 3×3 !)  │  │ │  Scroll interne confiné dans la carte
│ │  │ ┌────────────────────────────────────────────┐ │  │ │  Cartes .lkdv-feed-post (1:1 ou texte verre)
│ │  │ │ (av28) @auteur · Spot · 2h             ··· │ │  │ │  + PostGlassPanel (Commentaires ↔ Partage)
│ │  │ │                                            │ │  │ │    en swipe horizontal directement sur le post
│ │  │ │                        ╭ ♥34  💬34  ➤34 ╮ │ │  │ │
│ │  │ └────────────────────────────────────────────┘ │  │ │
│ │  └────────────────────────────────────────────────┘  │ │
│ │                                    ╭ 📰  ⊞  📅 ╮    │ │  Sous-sélecteur flottant 30px (.ig-tabs-float)
│ └──────────────────────────────────────────────────────┘ │  (ex: Fil d'actu / Grille Médias / Prochain RDV)
│ ┌──────────────────────────────────────────────────────┐ │
│ │  CARTE 3D MAPLIBRE VIVANTE (Zone 40% ou .mapbig)     │ │  Traces GPX du club, camps de base, membres,
│ │  [Poignée .mgrab]  [Callouts verre]  [Contrôles .mctl]│ │  météo massif, synchronisation avec le fil
│ └──────────────────────────────────────────────────────┘ │
│  ╭────────── Barre basse .tb (402 × 48px) ──────────╮    │
└──────────────────────────────────────────────────────────┘
```

### Anatomie de la Carte quand un Drawer est ouvert (`DrawerShell` en place)

Dès qu'on clique sur une cellule stat (`101×39`), un cercle d'action (`44px`), la pilule de la Top Bar ou un bouton de la barre basse :
- La carte garde exactement ses dimensions (`406 × n`, `r=24`, `syncCardBounds()`),
- Son contenu est remplacé par `DrawerShell` :
  - **En haut** : Poignée `.grab` (`18px`) + Capsule `.lkdv-capsule` (`378 × 48px`, icônes seules) permettant de basculer entre les grands volets du drawer (ex: *Cordée & Membres*, *Sorties & Camps*, *Matériel Mutualisé*, *Défis & Trace*, *Gouvernance & Réglages*).
  - **Au centre** : Piste horizontale `.lkdv-drawer-track` avec scroll interne confiné dans `.lkdv-drawer-pane.active`.
  - **En bas à droite** : Sous-capsule flottante `.ig-tabs-float.lkdv-drawer-secondary` (`30px`, icônes seules) pour filtrer le volet actif (ex: dans *Sorties* : `[À venir] [Passées] [Proposer]` ; dans *Matériel* : `[Disponible] [Emprunté] [Demandes]` ; dans *Membres* : `[Tous] [Guides/Encadrants] [Proches]`).

---

## 4. Composants Partagés à Réutiliser (Ne jamais dupliquer)

1. **Drawers & Volets en place dans la carte** :
   - `src/components/compte/drawer/shell/DrawerShell.tsx` (`DrawerShell`, `DrawerSkeleton`, `DrawerError`, `DrawerEmpty`, `DRAWER_SHELL_CSS`)
   - `src/components/compte/drawer/SlotShell.tsx` & `SlotSelector.tsx`
2. **Système de Post & Panneau Commentaires/Partage en place** :
   - `src/features/posts/ui/PostGlassPanel.tsx`
   - `src/features/posts/ui/post-system.css`
   - `src/features/community/feed/CommunityFeedPost.tsx`, `PostCommentsPanel.tsx`, `PostSharePanel.tsx`
3. **Carte 3D & Contexte Géospatial** :
   - `src/components/compte/map/CompteMap.tsx`, `CompteMapHud.tsx`, `CompteMapCallout.tsx`, `useCompteMapContext.ts`
4. **Navigation & Chrome** :
   - `src/components/mobile-nav/MobileNavWrapper.tsx` (masquer la nav globale si `.tb` est présent)

---

## 5. Workflow de Refonte & Vérification en 5 Étapes

1. **Audit & Design d'Adaptation** :
   - Identifier ce qui reste sur la carte principale (ultra-épuré, zéro scroll de page) et ce qui est réparti dans les Drawers (`48px` capsule) et Sous-Drawers (`30px` sous-capsule).
2. **Contrat de Tests (TDD)** :
   - Vérifier les tokens mesurés (`406px`, `r=24px`, `.gbtn` `38px`, `.ig-stat` `101×39`, cercles `44px`, capsule `378×48` icônes seules, sous-capsule `30px`, `PostGlassPanel` `top: 64px`, `0` scroll document, `0` diff dans `/compas`).
3. **Implémentation Modulaire** :
   - Construire les volets avec `DrawerShell` et le flux avec `PostGlassPanel` + `post-system.css`.
4. **Vérification Visuelle Côte à Côte (Playwright 430 × 932)** :
   - Prendre systématiquement une capture `430 × 932` de `/compte`, `/communaute` et de la page refondue (carte fermée, panneau post ouvert, drawer ouvert, sous-drawer actif, carte 3D déployée) et comparer les géométries `getBoundingClientRect()`.
5. **Validation & Déploiement** :
   - `npx tsc --noEmit`, `npx vitest run`, `npm run build`, push sur `main`.
