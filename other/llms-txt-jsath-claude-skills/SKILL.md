---
name: llms-txt
description: "Writes and publishes an llms.txt for a business website: reads the site, pulls out what the business does, who it serves, how it helps and the key pages, writes the file in the llmstxt.org format, validates it with an included checker, and puts it live at yoursite.com/llms.txt with a check that it is served correctly. Honest that llms.txt is a proposal and does not guarantee rankings. Use when someone says write my llms.txt, add llms.txt to my site, help AI tools understand my business, or how do I show up in ChatGPT or Claude answers. Best in Claude Code (or Codex) with access to the site's code; can also just write the file for you to upload."
---

# llms.txt for your website

`llms.txt` is a short plain-text file at the root of your site (`yoursite.com/llms.txt`) that tells AI tools, in a few lines, what your business does, who it serves, how you help, and which pages hold the details. It is written in Markdown so both people and AI read it easily.

By Johann (@johannships). This is the guide from my llms.txt reel.

## Be honest about what it does

- llms.txt is a **proposal** ([llmstxt.org](https://llmstxt.org)), not an adopted web standard. AI tools are not required to read it.
- It **does not guarantee** you rank, appear in ChatGPT or Claude answers, or get recommended. Nobody can promise that.
- What it does do: any tool or agent that looks for it gets an accurate, short description of your business in one place, written by you, instead of guessing from your pages.
- It takes about ten minutes and costs nothing, which is why it is worth doing. Keep the rest of your site clear too.

Say this to the user before starting, and never write "this will make you rank" in anything you produce.

## Inputs

- The website URL. Required.
- In Claude Code or Codex: the site's code folder, if they have one, so the file can be added and deployed.
- Optional: anything the site does not say but should (service area, hours, what you do not do).

## Steps

### 1. Read the site

Fetch `/sitemap.xml` (or `/sitemap_index.xml`) and the home page. From those, pick the 5 to 20 pages that matter to a customer: services or products, pricing, about, FAQ, contact, booking, locations. Skip legal pages, tag pages, old blog posts and anything behind a login.

Read each chosen page. Note only what the site actually says. If something important is missing (service area, hours, who it is for), ask the user. Never invent it.

### 2. Write the file

Format from the spec, in this order:

1. `# Business name` (the only required part)
2. `> One or two sentences`: what you do, for whom, where. This is the line an AI is most likely to quote, so make it plain and specific.
3. A few short lines or bullets with no headings: service area, hours, how to contact or book, what you do **not** do.
4. `## Section` headings, each a list of links: `- [Page name](https://full-url): what is on that page`
5. `## Optional` last, for pages an AI can skip (blog, careers).

Start from `templates/llms.txt` (a made-up plumbing business). Rules:
- Full `https://` URLs, pages that return 200, the live domain.
- Plain words. No slogans, no "best in town", no keywords stuffed in. Write it as if explaining the business to a new employee.
- Facts only from the site or the user. No prices, numbers or claims the site does not show.
- Usually 20 to 60 lines. Shorter is fine.
- If the site already has `.md` versions of pages, link those; the spec suggests them. Do not create them unless asked.

### 3. Check it

```bash
python3 scripts/check_llms_txt.py llms.txt --check-links
```

Aim for 0 errors. Fix warnings unless there is a reason not to. (The checker is strict: some large sites' files use extra headings or plain bullets and fail it. Yours should not need to.)

### 4. Put it live at the root

The file must be reachable at `https://yoursite.com/llms.txt`.

| Site type | Where the file goes |
|---|---|
| Next.js, Vite, Astro, most React sites | `public/llms.txt`, then deploy |
| Plain HTML / static host | The site's root folder, next to `index.html` |
| WordPress | The site root via your host's file manager or SFTP, or an SEO plugin that can generate llms.txt if yours has that feature |
| Hosted builders (Shopify, Wix, Squarespace, Webflow) | Check your platform's help for "llms.txt" or "upload a file to the root". If it cannot serve a file at that path, tell the user rather than putting it somewhere else |

In Claude Code: add the file, run the build, and commit. Deploy only when the user says so.

### 5. Prove it is live

```bash
curl -sI https://yoursite.com/llms.txt | head -5        # expect 200 and text/plain or text/markdown
python3 scripts/check_llms_txt.py https://yoursite.com/llms.txt --check-links
```

If it returns HTML (your home page or a 404 page), it is not live yet.

## Output

1. The `llms.txt` contents.
2. Checker result (errors and warnings).
3. Where it was placed and, if deployed, the live check result.
4. Anything the user should add (missing facts you did not invent).
5. One line: "llms.txt helps AI tools describe you accurately; it does not guarantee rankings."

## Keep it current

Update it when services, prices, hours or key pages change. A wrong llms.txt is worse than none.

## A prompt you can paste into Claude Code or Codex without installing the skill

```
Read my website at [URL] (start with /sitemap.xml and the home page) and write an llms.txt for it following llmstxt.org:
an H1 with the business name, a one or two sentence blockquote saying what we do, for whom and where,
a few plain lines on service area, hours, how to contact us and what we do not do,
then H2 sections that list the key pages as "- [Name](full URL): what is on it", with blog and careers under "## Optional".
Use only facts that are on the site. Ask me for anything missing.
Save it as public/llms.txt (or the site root if there is no public folder) and show me how to check it is live.
```
