---
name: tech-product-landing
description: >
  Build production-grade landing pages for software/CLI tools, developer libraries, and technical products.
  Uses the "Maxsim-style" design system: dark theme, blue accent glows, framer-motion animations, geometric
  hero grid, marquee tech stack, tabbed docs, and timeline how-it-works sections.
  Trigger when user says "create a landing page for my software", "build a product site", "make a landing page
  like maxsim-flutter", "developer landing page", or "CLI tool website". Stack: Vite + React + TypeScript +
  Tailwind CSS v4 + Framer Motion + Lucide React.
---

# Tech Product Landing Page

This skill produces landing pages by copying the **complete maxsim-flutter source** from `assets/template/`
and adapting the content for the target product. The design, animations, and structure stay identical —
only the data arrays and product-specific strings change.

## Step 1: Scaffold & Install

```bash
npm create vite@latest <project-name> -- --template react-ts
cd <project-name>
npm install motion lucide-react clsx tailwind-merge
npm install -D tailwindcss @tailwindcss/vite @types/node
```

## Step 2: Copy Template Files

Read and copy every file from `assets/template/` to the new project, preserving directory structure:

```
assets/template/
├── index.html
├── vite.config.ts
├── tsconfig.json
├── vite-env.d.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── lib/utils.ts
    └── components/sections/
        ├── Navbar.tsx
        ├── Hero.tsx
        ├── Features.tsx
        ├── HowItWorks.tsx
        ├── TechStack.tsx
        ├── Docs.tsx
        └── Footer.tsx
```

## Step 3: Content Replacements

All `// ADAPT:` comments in the template mark the exact locations to change. Summary:

### Global string replacements

| Find | Replace with |
|------|-------------|
| `maxsim-flutter` | your product name |
| `maystudios/maxsim-flutter` | your GitHub repo (`org/repo`) |
| `"maxsim-flutter"` (npm package in vite.config.ts) | your npm package name |
| `__MAXSIM_VERSION__` | rename to `__YOUR_PRODUCT_VERSION__` (3 files: vite-env.d.ts, Hero.tsx, Footer.tsx) |

### `index.html`
- `<title>` and `<meta name="description">`

### `vite.config.ts`
- `fetchNpmVersion("maxsim-flutter")` → your npm package name
- Or remove the fetch and use: `const version = "1.0.0";`
- Rename `__MAXSIM_VERSION__` define key

### `index.css`
- `--color-accent: #3b82f6` → your brand color (blue=dev tools, green=SaaS, purple=AI)
- Update `--color-accent-light` to a lighter shade

### `Navbar.tsx`
- `navLinks` array: add/remove sections to match your page
- Brand name in the `<a>` element
- GitHub URL (2 locations: desktop + mobile)

### `Hero.tsx`
- `FLIP_WORDS` — 4–5 power words for your product
- Eyebrow label text (`"CLI Tool"` → your category)
- `h1` product name
- Subtitle prefix (`"AI-Powered Flutter "`)
- Description paragraph
- `command` variable in `TerminalBlock` (your install command)
- GitHub `href` in CTA buttons

### `Features.tsx`
- Replace `features` array with 6 items:
  ```tsx
  { icon: IconName, title: "...", description: "..." }
  ```
- Import icons from `lucide-react` (`strokeWidth={1.5}` always)

### `HowItWorks.tsx`
- Replace `steps` array with 4 items (install → create → use → ship pattern):
  ```tsx
  { number: "01", title: "...", description: "...", code: "your-cli command" }
  ```

### `TechStack.tsx`
- Replace `flutterStack` / `cliStack` arrays with your actual tech (8–12 total items)
- Rename the arrays and their category labels if needed

### `Docs.tsx`
- Replace all tab content functions with your actual documentation
- Typical tab structure: Getting Started, Commands/API, Options/Modules, Config, Advanced Topic
- Keep `CodeBlock`, `DocHeading`, `DocText` utilities — they're universal
- Update `TabId` type and `tabs` array with your tab names

### `Footer.tsx`
- Product name, tagline, copyright string
- `EXTERNAL_LINKS` array: GitHub URL, npm URL (or replace with your links)

## Design Tokens

Defined in `src/index.css` under `@theme inline`:

| Token | Default | Guidance |
|-------|---------|----------|
| `--color-accent` | `#3b82f6` blue | Change per brand |
| `--color-accent-light` | `#60a5fa` | Lighter accent shade |
| Everything else | zinc dark scale | Keep as-is |

## Version Global (`__MAXSIM_VERSION__`)

The live site fetches the npm version at build time via `vite.config.ts`. For a new product:
1. Change `fetchNpmVersion("maxsim-flutter")` to your package name
2. Or hard-code: `const version = "1.0.0";`
3. Rename the define key from `__MAXSIM_VERSION__` to something like `__MY_TOOL_VERSION__`
4. Update `vite-env.d.ts` declaration
5. Update usages in `Hero.tsx` and `Footer.tsx`

## Checklist

- [ ] All `maxsim-flutter` string references replaced
- [ ] Version global renamed and configured
- [ ] `index.html` title and description updated
- [ ] Accent color changed (if needed)
- [ ] `FLIP_WORDS` reflect product value props
- [ ] Terminal command shows real install/init command
- [ ] 6 features with relevant lucide icons
- [ ] 4 how-it-works steps with real commands
- [ ] Tech stack badges list actual dependencies
- [ ] Docs tabs contain real documentation
- [ ] GitHub and npm links are correct
- [ ] Footer copyright and tagline updated
