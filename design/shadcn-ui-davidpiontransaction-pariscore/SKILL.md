---
name: shadcn-ui
description: >-
  Automatisation UI pour PariScore via shadcn/ui (v4 CLI + MCP server). Installation,
  génération et personnalisation de composants alignés sur le design system dark navy /
  vert néon (--accent #00e676). Couvre l'inventaire des 48 composants déjà installés dans
  src/components/ui/, le mapping tokens shadcn ↔ DESIGN_CHARTER.md, les commandes CLI v4
  (add/init/migrate/eject), le serveur MCP shadcn, et le workflow de migration du legacy
  vanilla (pariscore.html) vers React/shadcn. Conçu pour React 19 + Next.js 16 + Tailwind v4.
origin: pariscore
metadata:
  author: pariscore
  version: "1.0.0"
  target_agent: frontend
  stack:
    - shadcn/ui v4 (new-york, base radix, RSC, lucide)
    - React 19 + Next.js 16 (App Router)
    - Tailwind CSS v4 (@theme inline, oklch, tw-animate-css)
---

# shadcn/ui — Automatisation UI PariScore

Skill de référence pour **installer, générer et personnaliser** des composants
shadcn/ui dans PariScore, en respectant le design system dark navy / vert néon.

shadcn/ui n'est pas une librairie installée — **le code source des composants vit dans
`src/components/ui/`**. Tu en es propriétaire. Ce skill automatise la distribution.

---

## ⚡ Démarrage rapide (TL;DR)

```bash
# Installer un nouveau composant (ex: data-table n'existe pas encore)
npx shadcn@latest add data-table

# Liste les composants déjà présents (48 installés)
ls src/components/ui/

# Prévisualiser avant d'installer
npx shadcn@latest view accordion

# Initialiser le MCP shadcn (déjà fait — voir .mcp.json)
npx shadcn@latest mcp init
```

**Règle d'or** : après `add`, **vérifier toujours** que le composant respecte le
mapping tokens (section 3). shadcn livre des valeurs neutres par défaut ; il faut les
aligner sur la palette PariScore.

---

## 1. Configuration du projet (déjà en place)

### 1.1 `components.json`

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

**Détecté par la CLI** : `Next.js 16.1.1` (next-app) · Tailwind v4 · `src/` dir · RSC · TS ·
icon library `lucide` · base `radix`.

### 1.2 Inventaire — 48 composants installés

`src/components/ui/` contient (tous en `.tsx`) :

```
accordion.tsx          alert-dialog.tsx      alert.tsx             aspect-ratio.tsx
avatar.tsx             badge.tsx             breadcrumb.tsx        button.tsx
calendar.tsx           card.tsx              carousel.tsx          chart.tsx
checkbox.tsx           collapsible.tsx       command.tsx           context-menu.tsx
dialog.tsx             drawer.tsx            dropdown-menu.tsx     form.tsx
hover-card.tsx         input-otp.tsx         input.tsx             label.tsx
menubar.tsx            navigation-menu.tsx   pagination.tsx        popover.tsx
progress.tsx           radio-group.tsx       resizable.tsx         scroll-area.tsx
select.tsx             separator.tsx         sheet.tsx             sidebar.tsx
skeleton.tsx           slider.tsx            sonner.tsx            switch.tsx
table.tsx              tabs.tsx              textarea.tsx          toast.tsx
toaster.tsx            toggle-group.tsx      toggle.tsx            tooltip.tsx
```

**Manquants notables** (à installer si besoin) : `data-table`, `combobox`, `date-picker`,
`field`, `empty`, `spinner`, `kbd`, `item`, `item-group`, `button-group`, `native-select`,
`input-group`.

---

## 2. Commandes CLI v4 (référence)

| Commande | Rôle | Exemple PariScore |
|---|---|---|
| `add <comp>` | Ajoute un composant | `npx shadcn@latest add data-table` |
| `add <comp> -o` | Écrase un composant existant | `npx shadcn@latest add button -o` |
| `add <comp> --dry-run` | Simule sans écrire | `npx shadcn@latest add data-table --dry-run` |
| `view <comp>` | Prévisualise le code source | `npx shadcn@latest view date-picker` |
| `diff <comp>` | Compare local vs upstream | `npx shadcn@latest diff button` |
| `init` | Initialise `components.json` (déjà fait) | — |
| `migrate radix` | `@radix-ui/react-*` → package unifié `radix-ui` | `npx shadcn@latest migrate radix` |
| `migrate icons` | Migration librairie d'icônes | — |
| `migrate rtl` | Props physiques → logiques (`ml-4`→`ms-4`) | — |
| `eject` | Inline `shadcn/tailwind.css`, retire la dépendance | **Irréversible — éviter** |
| `info` | Affiche la config détectée | `npx shadcn@latest info` |

### 2.1 Mise à jour d'un composant

```bash
# Voir ce qui a changé depuis la dernière install
npx shadcn@latest diff button

# Réinstaller la version upstream (écrase)
npx shadcn@latest add button -o
```

⚠️ **`-o` écrase tes personnalisations**. Toujours `diff` avant, et sauvegarder les
modifs locales si tu en as.

### 2.2 Migration Radix unifié (recommandée à terme)

Le projet utilise encore les packages individuels (`@radix-ui/react-*`, ~25 packages dans
`package.json`). shadcn pousse désormais le package unifié `radix-ui`. Quand tu fais une
màj majeure :

```bash
npx shadcn@latest migrate radix
```

Cela réécrit les imports `import * as AccordionPrimitive from "@radix-ui/react-accordion"`
→ `import * as AccordionPrimitive from "radix-ui"`.

---

## 3. Design System — Mapping tokens shadcn ↔ PariScore

**C'est la partie la plus importante.** shadcn livre des couleurs neutres (gris oklch).
PariScore a un design system riche (dark navy `#0b0e17` + vert néon `#00e676` +
glassmorphism). Référence : **`DESIGN_CHARTER.md`**.

### 3.1 Tokens shadcn → palette PariScore

Les composants shadcn utilisent les variables CSS définies dans `src/app/globals.css`
(`:root` et `.dark`). Pour aligner sur la charte PariScore, le mapping conceptuel est :

| Token shadcn (`globals.css`) | Doit refléter (DESIGN_CHARTER) | Remarque |
|---|---|---|
| `--background` | `--bg` `#0b0e17` (dark navy) | Fond page |
| `--card` | `--bg2` `#0e121e` | Fond carte |
| `--popover` | `--bg3` `#131722` | Fond dropdown/dialog |
| `--primary` | `--accent` `#00e676` (vert néon) | CTA principal |
| `--primary-foreground` | `--bg` `#0b0e17` | Texte sur vert néon |
| `--secondary` | `--bg4` `#161c2a` | Secondaire |
| `--muted-foreground` | `--text3` `#94a3b8` | Texte muted |
| `--destructive` | `--red` `#ff3856` | Erreur |
| `--border` | `rgba(255,255,255,0.08)` | Bordure standard |
| `--accent` | `--accent-bg` `rgba(0,230,118,0.12)` | Fond accent (badges) |

⚠️ **Note** : `globals.css` contient actuellement les valeurs neutres par défaut de shadcn
(`oklch(1 0 0)` en `:root`, `oklch(0.205 0 0)` en `.dark`). La charte PariScore (dark navy
+ vert néon) **n'est pas encore reportée** dans `globals.css`. C'est un travail de
convergence à faire (voir section 6).

### 3.2 Couleurs fonctionnelles (à exposer en Tailwind)

La charte définit des couleurs sémantiques qui ne sont pas dans le scope shadcn par défaut.
Pour les utiliser dans les composants, soit :

- **Option A (recommandée)** : ajouter des entrées dans le bloc `@theme inline` de
  `globals.css` :
  ```css
  @theme inline {
    --color-success: oklch(0.72 0.19 149);   /* #00e676 */
    --color-warning: oklch(0.83 0.17 80);    /* #fbbf24 */
    --color-info:    oklch(0.75 0.15 220);   /* #29b6f6 */
  }
  ```
  → utilisable comme `bg-success`, `text-warning`, etc.

- **Option B** : importer les variables legacy `--green`/`--amber`/`--red`/`--blue` de
  `pariscore.html` dans `globals.css` et les référencer via `var()`.

### 3.3 Glassmorphism / blur / z-index

La charte interdit les valeurs en dur (`blur(Xpx)`, `z-index: N`, `font-family: '...'`).
Quand tu personnalises un composant shadcn :
- Blur → `var(--cf-blur-light|medium|heavy)` ou classes `.cf-u-glass-*`
- z-index → `var(--cf-z-floating|panel|overlay)` ou classes `.cf-u-z-*`
- Font → `var(--font-head|body|mono)` (jamais `'Inter'` en dur)

Valider avec : `node scripts/validate-css-conventions.js`

---

## 4. Serveur MCP shadcn — automatisation agentique

Le serveur MCP shadcn est déclaré dans `.mcp.json` sous la clé `shadcn`. Il permet à
l'agent de **lister, rechercher et installer** des composants sans commande shell.

### 4.1 Outils MCP disponibles

| Outil | Rôle |
|---|---|
| `list_components` | Catalogue complet des composants |
| `get_component_metadata` | Props, dépendances, usage d'un composant |
| `get_component` | Récupère le code source |
| `get_component_demo` | Exemple d'implémentation |
| `list_blocks` / `get_block` | Blocks complets (dashboard, login, sidebar…) |
| `get_project_registries` | Registries du projet |
| `list_items_in_registries` / `view_items_in_registries` | Items de registry tiers |
| `search_items_in_registries` | Recherche cross-registry |

### 4.2 Workflow agentique type

Quand on te demande "ajoute un composant X" :

1. **`get_component_metadata`** pour comprendre deps + props
2. **Vérifier** si deps déjà présentes (`grep "radix-ui" package.json`)
3. **Installer** : soit `npx shadcn@latest add X`, soit `get_component` + `Write` manuel
4. **Aligner le design** : appliquer le mapping tokens (section 3)
5. **Valider** : `npx tsc --noEmit` + `node scripts/validate-css-conventions.js`

### 4.3 Initialisation (déjà faite)

```bash
# Déjà configuré dans .mcp.json. Pour ré-initier sur un autre client :
npx shadcn@latest mcp init --client <claude|cursor|cline|windsurf>
```

---

## 5. Patterns de personnalisation PariScore

### 5.1 Ne jamais modifier `src/components/ui/*` pour du style métier

Les fichiers de `src/components/ui/` sont la **couche shadcn brute**. Les personnalisations
métier vont dans `src/components/` (composés) :

```tsx
// ❌ MAUVAIS : modifier src/components/ui/button.tsx pour ajouter une variante "bet"
// ✅ BON : créer src/components/bet-button.tsx
import { Button, ButtonProps } from "@/components/ui/button"
import { cn } from "@/lib/utils"

export function BetButton({ className, ...props }: ButtonProps) {
  return (
    <Button
      className={cn(
        "bg-[var(--accent)] text-[var(--bg)] hover:bg-[var(--accent-dim)]",
        "shadow-[var(--cf-glow-emerald)]",
        className
      )}
      {...props}
    />
  )
}
```

### 5.2 Variantes via cva (dans un composant composé)

```tsx
import { cva } from "class-variance-authority"

const statBadgeVariants = cva(
  "inline-flex items-center rounded-[var(--cf-radius-chip)] px-2 py-0.5 text-[var(--cf-fs-sm)]",
  {
    variants: {
      tone: {
        green: "bg-[var(--accent-bg)] text-[var(--green)]",
        amber: "bg-[var(--amber-soft)] text-[var(--amber)]",
        red:   "bg-[var(--coral-soft)] text-[var(--coral)]",
      },
    },
    defaultVariants: { tone: "green" },
  }
)
```

### 5.3 XSS-safe (vs legacy vanilla)

Le legacy `pariscore.html` nécessitait `_jsStr()` pour échapper les `${}` dans `onclick`.
**En React/shadcn, l'échappement est natif** (JSX). C'est un argument majeur pour la
migration. Ne jamais réintroduire de `dangerouslySetInnerHTML` avec du contenu non échappé.

---

## 6. Migration legacy → React/shadcn

Le legacy vanilla (`pariscore.html` ~8507 lignes, `server.js` ~7578 lignes) migre vers
React/shadcn. Mapping des patterns legacy → shadcn :

| Pattern legacy (`pariscore.html`) | Équivalent shadcn |
|---|---|
| `<div class="modal">` custom + overlay | `Dialog` / `Sheet` / `Drawer` |
| `<div class="card">` custom | `Card` (+ `CardHeader/Content/Footer`) |
| `<div class="badge">` custom | `Badge` |
| `<div class="tab">` custom | `Tabs` |
| `<select>` natif | `Select` |
| Tooltips custom (`title=`) | `Tooltip` |
| Toasts custom | `Sonner` (déjà installé) |
| Dropdown custom | `DropdownMenu` |
| `onclick="openX('${id}')"` + `_jsStr` | `onClick={() => openX(id)}` (natif, sûr) |
| Accordion custom | `Accordion` |
| Command palette (⌘K) custom | `Command` + `Dialog` |

### 6.1 Convergence design system

Étapes pour aligner `globals.css` (neutre shadcn) sur la charte PariScore (dark navy) :

1. Remplacer les valeurs `:root` et `.dark` de `globals.css` par la palette PariScore
   (convertir `#0b0e17` etc. en oklch, ou utiliser hex via `@theme`)
2. Ajouter `--color-success/warning/info` dans `@theme inline`
3. Importer les variables `--cf-*` (blur, z-index, radius) depuis la charte
4. Valider : `node scripts/validate-css-conventions.js`
5. Tester composant par composant en dark mode

⚠️ **Gros chantier** — à découper. Voir `DESIGN_CHARTER.md` §12 et le rapport
`AUDIT_HALLMARK_PARISCORE_2026-07-13.md`.

---

## 7. Checklist qualité (avant commit)

Après avoir installé/modifié un composant shadcn :

```bash
# 1. TypeScript compile
npx tsc --noEmit

# 2. ESLint
bun run lint

# 3. Conventions CSS (blur/z-index/font en dur)
node scripts/validate-css-conventions.js

# 4. Build Next.js
bun run build
```

**Vérifier** :
- [ ] Imports via alias `@/components/ui/...` (pas de chemins relatifs)
- [ ] `cn()` utilisé pour les fusions de classes
- [ ] Pas de couleurs en dur hors variables (`var(--...)`)
- [ ] Dark mode fonctionnel (tester `.dark`)
- [ ] Accessibilité préservée (ARIA, focus, clavier)
- [ ] Pas de `dangerouslySetInnerHTML` sans sanitization

---

## 8. Ressources

- **`DESIGN_CHARTER.md`** — charte graphique complète (palette, typo, glass, z-index)
- **`src/app/globals.css`** — tokens shadcn actuels (à converger)
- **`components.json`** — config shadcn du projet
- **`src/lib/utils.ts`** — `cn()` (clsx + tailwind-merge)
- **Docs officielles** : https://ui.shadcn.com/docs
- **CLI v4 changelog** : https://ui.shadcn.com/docs/changelog
- **Skill complémentaire** : `stitch-build-shadcn` (génération design → code via Stitch)
- **Skill connexe** : `design-system-unify` (unification du DS legacy)
- **Skill connexe** : `react-nextjs-patterns` (patterns App Router)

---

## 9. Pièges courants (PariScore)

1. **Oublier `src/`** — la config pointe vers `src/app/globals.css`, `src/components/ui/`,
   `src/lib/`. Ne pas créer de `app/` ou `components/` à la racine.
2. **`add -o` sans `diff`** — écrase les personnalisations locales. Toujours `diff` d'abord.
3. **Couleurs neutres shadcn** — par défaut `oklch(0.205 0 0)` (gris). PariScore veut du
   navy `#0b0e17`. Ne pas laisser les valeurs par défaut.
4. **`transition: all`** — interdit par la charte (§10.2). Toujours expliciter les props.
5. **z-index en dur** — interdit (§8.3). Utiliser `var(--cf-z-*)`.
6. **Modifier `ui/*` pour du métier** — créer un composé dans `src/components/` à la place.
7. **Package Radix fragmentés** — 25+ packages `@radix-ui/react-*`. Envisager
   `migrate radix` vers le package unifié.
8. **React 19 + Next 16** — certains composants peuvent nécessiter `"use client"`. Vérifier
   si le composant utilise des hooks/état (Dialog, Tooltip… = client).
9. **Sonner vs toast/toaster** — `sonner.tsx` ET `toast.tsx`+`toaster.tsx` sont installés.
   Préférer **Sonner** (moderne) pour les nouveaux dev. Le legacy toast est déprécié.
10. **`sharp` rebuild** — le `postinstall` rebuild `better-sqlite3` + `sharp`. Si un `add`
    échoue silencieusement, vérifier `npm rebuild`.
