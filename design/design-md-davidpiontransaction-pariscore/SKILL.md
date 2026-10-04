---
name: design-md
description: >-
  Use when the user wants the UI to look like a known brand or product (Vercel, Linear,
  Stripe, Apple, Spotify, OpenAI, Cursor, Supabase...) — "make it look like X", "build a
  page in the style of Y", "dark theme like Z", or any UI generation that should follow a
  specific design language. Applies a DESIGN.md (Google Stitch format) from the local
  collection at `.agents/design-md/` (74 brands) to the project. Also use when the user
  mentions DESIGN.md, getdesign.md, or awesome-design-md.
---

# DESIGN.md — Bibliothèque de Design Systems (awesome-design-md)

Collection locale de **74 DESIGN.md** extraits de vrais sites (repo upstream
[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md), MIT).

Un `DESIGN.md` est un document design system au format **Google Stitch** :
thème visuel, palette + rôles, typographie, composants, layout, profondeur, do's/don'ts,
responsive et prompts prêts à l'emploi. C'est du markdown — l'agent le lit et génère une
UI cohérente avec la marque choisie.

## Emplacement de la collection

```
.agents/design-md/<marque>/DESIGN.md   ← 74 marques (voir catalogue ci-dessous)
.agents/design-md/README.md            ← catalogue + lien upstream getdesign.md
```

⚠️ **Ne pas éditer les fichiers de la collection** — ils sont un miroir de l'upstream.
Pour rafraîchir : retélécharger le tarball upstream et réécrire `.agents/design-md/`.

## Catalogue (74 marques)

| Catégorie | Marques |
|---|---|
| AI & LLM | claude, cohere, elevenlabs, minimax, mistral.ai, ollama, opencode.ai, replicate, runwayml, together.ai, voltagent, x.ai |
| Dev tools & IDE | cursor, expo, lovable, raycast, superhuman, vercel, warp |
| Backend & DevOps | clickhouse, composio, hashicorp, mongodb, posthog, sanity, sentry, supabase |
| Productivity & SaaS | cal, intercom, linear.app, mintlify, notion, resend, zapier |
| Design & Creative | airtable, clay, figma, framer, miro, webflow |
| Fintech & Crypto | binance, coinbase, kraken, mastercard, revolut, stripe, wise |
| E-commerce & Retail | airbnb, meta, nike, shopify, starbucks |
| Media & Consumer | apple, hp, ibm, nvidia, pinterest, playstation, spacex, spotify, theverge, uber, vodafone, wired |
| Automotive | bmw, bmw-m, bugatti, ferrari, lamborghini, renault, tesla |
| Retro (nostalgie) | dell-1996, nintendo-2001 |

## Workflow d'application

1. **Choisir la marque** (ou laisser l'utilisateur choisir dans le catalogue).
2. **Lire** `.agents/design-md/<marque>/DESIGN.md` en entier.
3. **Adapter à PariScore — RÈGLE D'OR** : le design system existant de PariScore
   (`DESIGN_CHARTER.md`, `COMPONENTS.md`, tokens shadcn/ui dark navy `#0b0e17` +
   accent vert néon `#00e676`) reste la **source de vérité**. Le DESIGN.md externe est
   une **source d'inspiration** : on en reprend la structure visuelle (mood, composants,
   layout, typo si compatible) mais on **mappe ses tokens sur les tokens existants**.
   Un rebrand complet (remplacement des tokens) n'arrive que si l'utilisateur le demande
   explicitement.
4. **Mapper les composants** : utiliser les vrais composants de `COMPONENTS.md`
   (src/components/ui/*) — ne jamais inventer de noms.
5. **Appliquer** : coder la page/le composant demandé en respectant la direction visuelle
   (densité, rayon, ombres, espacements, états) du DESIGN.md choisi.

## Prompts prêts à l'emploi (à transmettre à l'agent)

```
Construis [page/écran] en suivant le design language de [marque] :
- Lis `.agents/design-md/<marque>/DESIGN.md` (sections palette, typo, composants, layout)
- Mappe les tokens sur le design system PariScore (DESIGN_CHARTER.md) — pas de rebrand sauf demande explicite
- Utilise les composants existants listés dans COMPONENTS.md
- Respecte les do's/don'ts et le comportement responsive du DESIGN.md
```

## Vérification

- Comparer le rendu aux sections « Color Palette & Roles » et « Typography Rules » du
  DESIGN.md choisi (swatches hex, hiérarchie de polices).
- Vérifier les états des composants (hover, active, disabled, focus) contre la section
  « Component Stylings ».
- Pas de token fantaisiste : chaque couleur/rayon/ombre doit venir du DESIGN.md choisi
  ou des tokens existants de DESIGN_CHARTER.md.