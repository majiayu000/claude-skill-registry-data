---
name: senternet-site-vite-setup
description: Scaffold a production-ready Vite + React + TypeScript site.
---

# Vite + React + TypeScript Site Setup

Initialize a production-ready Vite + React + TypeScript project for a marketing site.

This is the `vite` track — static output on Firebase Hosting, with Puppeteer prerendering for crawlers. It is the default track and the right one for most marketing sites. If the site needs server rendering, route handlers, middleware, or on-demand regeneration, use `/senternet-site-nextjs-setup` instead. `/senternet-site-framework` has the decision guidance and the convention map between the two.

## Steps

1. Ask the user which local dev port to use. Default is `3000`. Explain that they may want a different port if they run multiple sites locally (e.g. 3001, 3002, 3003). Use their answer as `$PORT` throughout the rest of the setup.

2. Scaffold the project with Vite using the React + TypeScript template:
   ```bash
   npm create vite@latest $SITE_NAME -- --template react-ts
   cd $SITE_NAME
   npm install
   ```
   Replace `$SITE_NAME` with the project directory name (e.g. `myapp-site`).

3. Install core dependencies:
   ```bash
   npm install react-router-dom
   npm install -D puppeteer sharp
   ```

4. Update `vite.config.ts` with:
   - Path alias `@/` → `src/`
   - `outDir: 'build'` (not the default `dist` — Firebase and prerender scripts expect `build/`)
   - `manualChunks: { 'vendor-react': ['react', 'react-dom', 'react-router-dom'] }` for parallel chunk loading
   - `build.target: 'esnext'`
   - Dev server port from `PORT` env var with the user-chosen default (`$PORT`)
   - An `htmlPlugin` that rewrites `VITE_BASE_URL` into meta tag `content` and canonical `href` attributes at build time, and conditionally injects or strips the GA block based on `VITE_GA_ID`

   The htmlPlugin should also inject `<link rel="modulepreload">` tags for all JS chunks so the browser fetches them from `<head>` rather than waiting for the `<script>` at end of body.

5. Set up `src/main.tsx`:
   - Use `hydrateRoot` (not `createRoot`) so React attaches to pre-rendered DOM without replacing it — this keeps LCP from the initial HTML paint
   - Dispatch `new Event('app-ready')` after hydration so the prerender script knows the page is ready
   - Add a 1s fallback timeout that also dispatches `app-ready`

6. Set up `src/App.tsx` with React Router:
   - Use `BrowserRouter` + `Routes` + `Route`
   - Add a catch-all `<Route path="*">` that redirects to `/`
   - Lazy-load page components with `React.lazy` + `Suspense`
   - Add a `ScrollToTop` component that resets scroll on navigation, and render it inside `BrowserRouter` (above `Routes`). Without this, React Router preserves the scroll position across route changes — so clicking a link while scrolled to the bottom of one page lands the user partway down the next page. This is a consistent, easy-to-miss bug on new sites, so it must always be wired up.
     ```tsx
     import { useEffect } from 'react';
     import { useLocation } from 'react-router-dom';

     function ScrollToTop() {
       const { pathname } = useLocation();
       useEffect(() => {
         window.scrollTo(0, 0);
       }, [pathname]);
       return null;
     }
     ```
     Note: it must live *inside* `<BrowserRouter>` because it depends on `useLocation`. If the site uses hash links for in-page anchors, key the effect on `pathname` only (not `hash`) so anchor jumps still work.

7. Create `.env.development` and `.env.production` files:
   ```
   VITE_BASE_URL=http://localhost:$PORT
   VITE_GA_ID=
   ```
   and
   ```
   VITE_BASE_URL=https://www.yoursite.com
   VITE_GA_ID=G-XXXXXXXXXX
   ```
   If the repo already has a non-empty `VITE_GA_ID` in `.env.production`, preserve it during upfit runs and do not overwrite it with the placeholder. Only use `G-XXXXXXXXXX` as the initial scaffold value when no Measurement ID has been established yet.

8. Update `package.json` scripts:
   ```json
   {
     "dev": "vite --port $PORT",
     "build": "tsc -b && vite build",
     "build:prod": "tsc -b && vite build --mode production && node scripts/prerender.mjs",
     "preview": "vite preview"
   }
   ```

9. Add `tsconfig.json` with strict mode and path alias for `@/`.

10. Create `src/index.css` with Tailwind CSS v4 import:
   ```css
   @import "tailwindcss";
   ```
   Install Tailwind:
   ```bash
   npm install -D tailwindcss @tailwindcss/vite
   ```
   Add `@tailwindcss/vite` to the vite plugins array.

11. Create `scripts/` directory for build helpers.

12. Create `public/` with `favicon.png`, `favicon.svg`, `favicon.ico`, and `apple-touch-icon.png` placeholders.

13. Create `src/assets/` for optimized images.

14. Write `.site-framework.json` in the project root so every later skill and every upfit run knows which track this site is on without re-deriving it:
    ```json
    {
      "framework": "vite",
      "renderMode": "static-prerender",
      "host": "firebase-hosting"
    }
    ```

## Output

When complete, the project should:
- Run `npm run dev` without errors
- Build with `npm run build` without TypeScript errors
- Have the `@/` alias working for imports
- Have React Router wired up with at least a home route
- Be ready for Firebase Hosting, GA, prerender, and all other site skills to be layered on top
