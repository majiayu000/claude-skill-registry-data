---
name: setup
version: 3.1.0
description: "Create a new Compound Marketing instance for your company. Trigger with /setup. Asks your company name, scaffolds a standalone repo with all skills and brain templates, then walks you through configuring everything."
---

# Compound Marketing Setup

Run `/setup` to create a new, fully configured Compound Marketing instance for your company. This is the first thing a user does after cloning compound-marketing.

## Overview

1. Ask company name, location, preferred AI runtime, and any existing notes folder to connect
2. Run the generator script to scaffold everything
3. Scrape the website (optional) to pre-fill brain files
4. Import reference documents from `incoming/` (optional) to pre-fill brain files
5. Walk through brain file configuration interactively
6. Set up integrations (analytics, image gen, meeting notes)
7. User opens the new repo in their preferred runtime and starts working

---

## Step 1: Company Name

Ask the user:

> What's your company name?

Then derive the default path: `../[company-slug]-marketing/` (lowercase, hyphenated, sibling of the current directory).

Ask:

> I'll create your Compound Marketing instance at `[path]`. Good, or would you prefer a different location?

---

## Step 1b: Runtime Preference

Ask the user:

> Which AI coding agent do you primarily use?
> 1. **Claude Code** (Anthropic) — default
> 2. **Codex** (OpenAI)

This determines which runtime is "primary" — the canonical source for skills and instruction files. Both runtimes are always scaffolded; the primary just governs sync direction.

Store the choice as `claude` or `codex`.

---

## Step 1c: Knowledge Source (Optional)

Ask the user:

> Do you keep working notes somewhere you want me to read every session, like an Obsidian vault with meeting notes, people profiles, and clippings? If so, what's the folder path?

If they give a path:
- Expand `~` and confirm the folder exists. If it doesn't, ask again or skip.
- It must not be inside the target path from Step 1. The notes stay where they are; the new repo only points at them.
- Store it as `[knowledge-dir]`.

If they don't have one, leave `[knowledge-dir]` empty and move on.

---

## Step 2: Create the Repo

Run the generator script to scaffold the new repo:

```bash
./scripts/create-instance.sh "[company-name]" "[target-path]" "[runtime]" "[knowledge-dir]"
```

Where `[runtime]` is `claude` or `codex` from Step 1b, and `[knowledge-dir]` is the folder from Step 1c (omit the argument if there isn't one).

This script:
- Creates the directory structure
- Copies all skills into both `.claude/skills/` and `.agents/skills/` (hardlinked)
- Generates both `CLAUDE.md` and `AGENTS.md` (identical except title and path references)
- Writes `.compound-marketing.yml` with the primary runtime setting
- Copies brain templates with `[FILL IN]` placeholders
- Copies Vale styles, settings, .gitignore
- If a knowledge folder was given: grants Claude Code read access in `.claude/settings.local.json` (`permissions.additionalDirectories`, gitignored) and lists it under `knowledge_sources:` in `.compound-marketing.yml`
- Initializes git with an initial commit

If the script doesn't exist or fails, do the same work manually:
- `mkdir -p` the directory tree
- Copy skills into both `.claude/skills/` and `.agents/skills/`
- Generate both `CLAUDE.md` and `AGENTS.md`
- Write `.compound-marketing.yml` with `primary_runtime: [claude|codex]` (plus `knowledge_sources: ["[knowledge-dir]"]` if set)
- If a knowledge folder was given, write `.claude/settings.local.json` with `{"permissions": {"additionalDirectories": ["[knowledge-dir]"]}}`
- Copy brain/, styles/, PRODUCT.md, INDEX.md, .vale.ini, .claude/settings.json, .env.example, .gitignore
- `git init && git add -A && git commit -m "Initial setup: [Company] Compound Marketing instance"`

**All remaining steps operate on files in the NEW repo, not the compound-marketing source repo.**

---

## Step 2a: Index the Knowledge Source (if set)

Skip if there's no `[knowledge-dir]`.

If `qmd` isn't installed (`command -v qmd`), tell the user and offer to install it:

> QMD isn't installed. It lets me search your notes instead of reading them one by one, which matters for a large vault. Want me to install it? (`npm install -g @tobilu/qmd`, needs Node.js)

If they agree and `npm` is available, run the install. If they decline or there's no `npm`, tell them the instance will search notes with grep and they can install QMD later, then skip the rest of this step.

Once `qmd` is available, check `qmd collection list` for a collection already pointing at `[knowledge-dir]`. If none, offer:

> Want me to index your notes with QMD so I can search them instead of reading files one by one?

If they agree, run `qmd collection add "[knowledge-dir]" --name [company-slug]-notes`, then `qmd embed`. Indexing can take a few minutes on a large vault.

---

## Step 2b: Personalize README

Replace `[COMPANY]` in the new repo's `README.md` with the actual company name. Also replace `[this-repo]` in the Getting Started section with the repo's directory name.

This is a silent step — do it automatically, no need to confirm with the user.

---

## Step 3: Company Basics

Ask the user:

1. What does your product do? (one sentence)
2. What category are you in? (e.g., "observability", "developer tools", "AI security")
3. Who's your target customer? (e.g., "mid-market SaaS companies", "enterprise security teams")
4. What's your website URL?

**Optional follow-ups (ask if the user seems engaged, skip if they want speed):**
- Founded when? Where?
- Funding status? (bootstrapped, seed, Series A, etc.)
- Team size?
- Deployment model? (SaaS, on-prem, hybrid)

Confirm the basics back in a summary table. Ask if anything needs correction.

## Step 3b: Website Scrape

If the user provided a website URL, offer:

> Want me to read your website and pull in product details, messaging, and feature info? This can save a lot of manual entry.

If they agree:
- Fetch the homepage and key pages (about, product/features, pricing if public)
- Extract: product description, features, value props, customer logos, integrations, pricing tiers
- Use this to pre-fill brain files in the following steps (truth.md, positioning, etc.)
- Always show what you extracted and confirm before writing — never silently inject scraped content into brain files

If they decline, continue with manual entry.

---

## Step 3c: Import Reference Documents (Optional)

Ask the user:

> Do you have any existing documents you'd like me to reference? Things like messaging frameworks, product overviews, brand guidelines, competitive analyses, or pitch decks. If so, drop them in the `incoming/` folder and I'll use them to pre-fill your brain files.

If they have files:
1. List the files found in `incoming/` and confirm which ones to read
2. Read each file and extract relevant information: product facts, positioning language, personas, competitive intel, brand details
3. Map extracted content to the appropriate brain files (truth.md, positioning-and-messaging.md, competitive.md, personas.md, brand-guide.md)
4. **Always show what you extracted and confirm before writing.** Never silently inject content from reference documents into brain files.
5. Note: reference documents are raw inputs, not verified claims. Extracted facts go into brain files as starting points; the user confirms accuracy.

If they also did the website scrape in Step 3b, merge both sources. Where they conflict, ask the user which version is correct.

If they have no files, move on.

Either way, mention that `/brain-ingest` runs this same import anytime later, from `incoming/` or straight from connected sources like email, Google Drive, or SharePoint.

---

## Step 4: Fill truth.md

Using the answers from Steps 1, 3, and any imported reference documents (Step 3c), fill in `[new-repo]/brain/truth.md`:
- Replace `[FILL IN]` placeholders with the user's answers
- Leave `[FILL IN]` for anything they didn't provide
- Do NOT invent information

Show the user the updated file and confirm.

---

## Step 5: Positioning Quick-Start

Ask the user:

1. What's the #1 problem your product solves? (the pain, not the feature)
2. What do customers use today instead of you? (the status quo or competitors)
3. Why doesn't the status quo work? (what's broken about current approaches)
4. What makes your approach different? (your key differentiator, in plain language)
5. Name 2-3 direct competitors.

Fill in the core sections of `brain/positioning-and-messaging.md`:
- Market Problem / Category Framing (from questions 1-3)
- Short Definition (from company basics + question 1)
- Positioning Statement (assembled from all answers)

Fill in `brain/competitive.md`:
- Market Category
- Direct Competitors (names and initial positioning)

Leave detailed sections as `[FILL IN]`. Tell the user: "I've filled in the foundation. Run `/product-marketing` later to flesh out messaging pillars and the full competitive landscape."

---

## Step 6: Persona Quick-Start

Ask the user:

1. Who's the primary buyer? (title and role)
2. Who champions the purchase internally? (title and role)
3. Who evaluates the product technically? (title and role)

Fill in `brain/personas.md` with the three personas. Leave "Top Problems" and "What They Need" as `[FILL IN]`.

---

## Step 7: Brand Configuration

If the user provided a website URL in Step 3, offer automatic extraction first:

> Want me to extract your brand colors, fonts, and spacing from your website? I can pull them automatically using `/design-extract`.

If they agree, run the design-extract skill (it installs `designlang` if needed, scrapes the site, and populates `brand-guide.md`).

If they decline or have no website, fall back to manual entry:

1. Do you have a brand guide? (colors, fonts, etc.)
2. If yes: primary brand colors? (hex codes if available)
3. Dark or light design defaults?

**If they have details:** fill in `brain/brand-guide/brand-guide.md`.
**If not:** tell them the brand guide is there when they're ready, and move on.

---

## Step 8: Vale Vocabulary

Using the company name and product name:

1. Update `styles/config/vocabularies/Brand/accept.txt` with brand terms
2. Rename `styles/Brand/` to use the company name
3. Update `.vale.ini` to reference the renamed directory

---

## Step 9: CLAUDE.md Personalization

Ask: "Want to add your name to the Human Authority section, or any brand-specific writing rules? Or is the default good?"

Update CLAUDE.md (and AGENTS.md — keep them in sync) in the new repo if they want changes.

---

## Step 10: Integrations (Optional)

Show the user what integrations are available and ask which ones they want to set up:

> Compound Marketing can connect to these services for analytics, image generation, and meeting notes. Which do you use?

| Service | What it powers | Required? |
|---------|---------------|-----------|
| **Codex CLI** | Image generation (`/image-gen`, blog, thumbnails) via `codex login` with a ChatGPT account. No API key | Recommended |
| **Google AI Studio** | Backup image generation (Nano Banana) when the Codex CLI isn't available | Optional |
| **HubSpot** | Email, page, and campaign analytics | Optional |
| **LinkedIn** | Post and page analytics | Optional |
| **X / Twitter** | Post analytics | Optional |
| **YouTube** | Channel and video analytics | Optional |
| **Granola** | Meeting notes for case studies and brain updates | Optional |

For each service they want to connect:
1. Tell them where to get the API key/token (the instructions are in `.env.example`)
2. Have them copy `.env.example` to `.env` if not already done
3. Have them fill in the relevant values

If they don't want to set up any integrations now, tell them: "You can set these up anytime by editing `.env` — the instructions are in `.env.example`."

---

## Step 11: Brain Health Check

Run the `/brain-health` skill in "setup mode" (skip the interactive offer to start filling files). This shows the user exactly where they stand and what to do next.

The brain-health dashboard replaces the old flat list of "still to fill in" files. It shows completeness per file and maps each gap to the skill that fills it.

---

## Step 12: Finish & Try It Now

Commit all the configuration changes:

```bash
cd [new-repo]
git add -A
git commit -m "Configure brain files for [Company]"
```

Present (adapt the commands based on the runtime they chose — `/` for Claude, `$` for Codex):

```
Setup complete. Your Compound Marketing instance is at: [path]
Primary runtime: [Claude Code | Codex]
Knowledge source: [knowledge-dir | none]

Brain files configured:
  truth.md, positioning-and-messaging.md, competitive.md,
  personas.md, brand-guide.md

Both runtimes scaffolded:
  [primary dir]/skills/ (primary)    [secondary dir]/skills/ (mirrored)
  [PRIMARY].md (primary)             [SECONDARY].md (mirrored)

To start working:
  cd [path]
  [claude | codex]
```

Then offer to try the system right now:

> Want to take it for a spin? Pick one:
>
> 1. **Write a blog post** — I'll draft a post using your positioning and voice (run `/blog`)
> 2. **Run a competitive analysis** — I'll research a competitor and build a comparison page (run `/wf-competitive-positioning`)
> 3. **Skip for now** — You can start anytime with the skills below

If they pick an option, route to that skill immediately. If they skip, show the skill reference:

```
Single tasks:
  /blog              Write a blog post
  /copywriting       Write landing page copy
  /social-content    Create social media posts
  /case-studies      Write a customer case study
  /marketing-ideas   Generate marketing tactics

Full workflows (multi-step pipelines):
  /wf-blog-distribute          Write a post and distribute across channels
  /wf-landing-page             Build a page end-to-end (copy → design → CRO → SEO → tracking)
  /wf-campaign-launch          Plan and run a multi-channel campaign
  /wf-competitive-positioning  Research competitors and build comparison pages
  /wf-case-study-pipeline      Customer conversation → case study → distribution
  /wf-repurpose                Fan existing content out to social, email, and ads
  /wf-seo-sprint               SEO audit → topic cluster → batch of optimized posts
  /wf-ad-campaign              Paid ads from strategy through creative and testing

Brain building:
  /tone-mapping      Build your voice profile from writing samples
  /design-extract    Extract brand colors and fonts from your website
  /brain-ingest      Pull facts from email, Drive, SharePoint, and docs
  /brain-health      Check brain file completeness anytime

Utilities:
  /analytics         Check marketing performance
  /tagore            Strip AI patterns from any prose
  /sync-skills       Sync skills between runtimes
  /start             Start a session (loads context)
  /brief             End a session (checkpoint work)
```

---

## Rules

- All file writes happen in the NEW repo, never in compound-marketing
- Never invent information the user didn't provide
- Show what you'll write and confirm before saving
- If the user wants to skip a step, skip it. Leave placeholders.
- If the user gives a website URL, offer to read it and extract info (with approval)
- Keep the pace brisk. Don't over-explain.
- If the target directory exists, stop and confirm before doing anything
- Never write into the knowledge source folder
