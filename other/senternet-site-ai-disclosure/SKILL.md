---
name: senternet-site-ai-disclosure
description: Interview the user about their AI usage, then create a voluntary AI Disclosure page that sits alongside Privacy and Terms.
---

# AI Disclosure Page

Create an **AI Disclosure** page — a plain-language, honest account of where and how AI shows up in the product, the company, and the site. It sits in the footer next to Privacy and Terms, but unlike those it is **voluntary**: a transparency commitment, not a legal requirement. The goal is to tell the public the parts most companies leave out.

This skill works by **interviewing the user** across the categories the public tends to care about, then writing the page from their answers. The user can **pass on any question** — silence on a topic is fine, and a passed category is simply omitted rather than papered over with filler.

## How AI disclosure differs from Privacy/Terms

- **Privacy/Terms** are legal documents about data handling and obligations.
- **AI Disclosure** is a voluntary, human-voiced explanation of *how AI is used* — in the product's features, in how the product is built, in the visuals, and in how the site is optimized.
- Link the two: the AI Disclosure should point to the Privacy Policy for "the formal data-handling rules," and avoid restating legal terms.

Reference implementation: Premail's `/ai-disclosure` page (`src/pages/AIDisclosurePage.tsx`).

## Step 1 — Interview the user

Ask the questions below, grouped by category. **Tell the user up front that every question is optional** and they can say "pass" or "skip" on anything they'd rather not disclose — the page only covers what they choose to share. Ask category by category, not all at once. Use their existing product context (`.agents/product-marketing-context.md` if present) to pre-fill what you already know and confirm rather than ask cold.

Use the `AskUserQuestion` tool for the high-level "which categories apply" pass, then follow up conversationally on the categories they keep.

### Category A — AI inside the product (features users interact with)
- Does the product use AI in features the user touches? If so, what does each AI feature do?
- Which models/providers power it (e.g. Anthropic Claude, OpenAI, a local model)? Does the user bring their own key, or is it built in?
- Where does user content go when AI runs — to a third-party provider directly, through your servers, or processed locally?
- What does the AI in the product **never** do? (e.g. never trains on user data, never sells it, never acts without a configured rule.)
- Is there human oversight / a way for users to see, understand, and correct AI decisions?

### Category B — AI in how the product is built
- Does the developer/team use AI coding assistants to write, review, or refactor code?
- Is AI used for documentation, support drafts, or marketing content?
- Crucially: is any **user/private data** ever fed into the AI tools used to build the product? (Usually the answer is an emphatic no — state it.)

### Category C — AI-generated visuals
- Are images, illustrations, icons, designs, or page layouts AI-generated or AI-assisted? To what extent — starting points refined by hand, or shipped as-is?

### Category D — How the site is built/optimized
- Is the site built/optimized with reusable AI skills or tooling (e.g. the open `senternet-site-skills`)? Link to the repo if public.

### Category E — Posture statements
- Data/training stance: a one-line "we do/don't use your data to train models."
- Changes commitment: will the page be kept updated as AI usage evolves?
- Contact: an email for AI-related questions (e.g. `ai@DOMAIN`).

For any category the user passes on, **omit that `<section>` entirely** — do not write "We don't disclose this." A shorter, honest page beats a padded one.

## Step 2 — Detect the site's conventions

Before writing the page, match what the site already does for Privacy/Terms pages:

- **MetaTags import path** — check an existing legal page (`grep -r "import.*MetaTags" src/pages`). Some sites use `@/components/MetaTags`, others `../components/MetaTags`.
- **Styling** — copy the wrapper/heading classes from the existing `PrivacyPage.tsx` so the AI Disclosure matches (e.g. `max-w-3xl mx-auto px-6 py-16`, muted-text CSS vars).
- **Share image extension** — `.png` vs `.webp` (check `scripts/generate-share-images.mjs`).
- **Last-updated date** — use today's date in the site's existing format.

## Step 3 — Create the page component

`src/pages/AIDisclosurePage.tsx`. Build sections **only for the categories the user kept**. Write in the product's voice (first person "I" for a solo developer, "we" for a team — match Privacy/Terms). Template (Premail-derived — trim sections the user passed on):

```tsx
import { MetaTags } from '@/components/MetaTags'

export default function AIDisclosurePage() {
  return (
    <>
      <MetaTags
        title="AI Disclosure - APPNAME"
        description="How APPNAME uses AI — from the tools used to build it to the models inside the product. Written for transparency."
        image="/share/ai-disclosure.png"
      />
      <main className="max-w-3xl mx-auto px-6 py-16 text-[var(--color-text)]">
        <h1 className="text-4xl font-bold mb-2">AI Disclosure</h1>
        <p className="text-sm text-[var(--color-text-muted)] mb-12">Last updated: MONTH DD, YYYY</p>

        <p className="mb-8 text-[var(--color-text-muted)]">
          {/* Intro: why this page exists, that it's a voluntary ongoing commitment,
              and a link to the Privacy Policy for formal data-handling rules. */}
          … see the{' '}
          <a href="/privacy" className="underline hover:text-[var(--color-text)]">Privacy Policy</a>.
        </p>

        {/* Category A — only if AI is in the product */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">AI inside APPNAME</h2>
          {/* What each AI feature does; which models/providers; where content goes;
              a "what AI never does" bullet list; human oversight. */}
        </section>

        {/* Category B */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">AI in how I build APPNAME</h2>
          {/* Coding assistants, docs/support/marketing; explicit no-user-data line. */}
        </section>

        {/* Category C */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">AI-generated visuals</h2>
        </section>

        {/* Category D */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">How I optimize my sites</h2>
        </section>

        {/* Category E */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Changes to this disclosure</h2>
        </section>
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Contact</h2>
          {/* mailto:ai@DOMAIN */}
        </section>
      </main>
    </>
  )
}
```

Writing guidance:
- **Plain language, honest, specific.** Name the actual models and providers. Say where data goes in concrete terms.
- **Lead with what AI never does** in any user-data section — it's what readers most want to know.
- **Don't oversell.** "AI helps me move faster; it does not replace human judgment" reads better than hype.
- Keep it skimmable: `<h2>` per category, `<h3>` for sub-topics, bullet lists for the "never does" guarantees.

## Step 4 — Wire it in (the three-file rule + footer + share image)

This is a new route, so all three route files must be updated together:

1. **`src/App.tsx`** — lazy-import and add the route next to Privacy/Terms:
   ```tsx
   const AIDisclosurePage = lazy(() => import('@/pages/AIDisclosurePage'))
   // …
   <Route path="/ai-disclosure" element={<AIDisclosurePage />} />
   ```
2. **`scripts/prerender.mjs`** — add `'/ai-disclosure'` to `ROUTES`, near `'/privacy'` and `'/terms'`.
3. **`scripts/generate-sitemap.mjs`** — add `{ path: '/ai-disclosure', changefreq: 'yearly', priority: '0.3' }`, matching the Privacy/Terms entries.

Then:

4. **Footer** (`src/components/Layout.tsx` or wherever the footer links live) — add `{ to: '/ai-disclosure', label: 'AI Disclosure' }` right after Privacy and Terms. If the footer groups links under category headings, place it in the **Legal** group alongside Terms and Privacy (don't append it to an unrelated column). If the footer is still a flat row but adding this link pushes it past ~4–5 entries, take the opportunity to split it into grouped columns (Legal / Product / Company) as described in `/senternet-site-design`.
5. **`scripts/generate-share-images.mjs`** — add a share-image block so the page has an OG image:
   ```js
   {
     file: 'ai-disclosure',
     title: 'AI Disclosure',
     subtitle: 'How APPNAME uses AI, transparently.',
     isHome: false,
   },
   ```

## Step 5 — Verify

- `npm run build:prod` succeeds and `/ai-disclosure` appears in the prerender output as a non-empty route.
- The footer link navigates to the page.
- The page links to `/privacy` and does not duplicate legal language.
- Every section on the page corresponds to a category the user actually answered — no filler for passed topics.

## Framework: Next.js track

The interview and the page content are unchanged. Placement: `app/ai-disclosure/page.tsx` with its own `export const metadata`, plus an entry in `config/routes.mjs`.

Like Privacy and Terms, this page is usually `noindex` — set `robots: { index: false, follow: true }` in its `metadata` and mark it `indexable: false` in the manifest in the same change, so it renders and stays reachable by direct link without being advertised in the sitemap.

See `/senternet-site-framework` for the full convention map.
