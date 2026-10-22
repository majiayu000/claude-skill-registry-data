---
name: website-content
description: Write or update content for Mick Pletcher's personal website. Trigger when Mick asks to write, rewrite, or update any section of his personal site including About, Projects, Skills, Blog integration, AI and homelab showcase, health and sports, contact copy, landing page sections, SEO descriptions, or project writeups. Tone is polished and professional, closer to LinkedIn than the blog, but still first-person and direct. Avoid corporate-speak. No emojis. Avoid em dashes in final website copy.
version: 1.1.0
---

# Website Content

## Intent

Write and refine content for mickpletcher.com using the established site voice, section structure, and project positioning.

## Use When

- The user explicitly asks for `website-content`.
- The request matches the triggers or workflow described below.
- The task benefits from a reusable, structured output instead of a one-off answer.

## Do Not Use When

- Do not use for code implementation, unrelated websites, blog posts, or content that requires invented project facts.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

## Constraints

- Do not fabricate missing facts, measurements, dates, sources, or user context.
- Keep output aligned with Mick's direct, practical communication style unless the skill says otherwise.
- Preserve safety, legal, medical, financial, and operational boundaries stated in this file.
- Prefer concise, usable output over broad explanation.

Write polished, first-person website copy for Mick Pletcher's personal site.

## Site Sections

| Section | Purpose |
| --- | --- |
| About / Bio | Professional identity, builder background, athlete, traveler |
| Projects Portfolio | Container home, trading systems, Proxmox homelab and automation work |
| AI / Homelab Showcase | Self-hosted AI infrastructure and automation stack |
| Skills / Resume | Technical competencies and career highlights |
| Blog Integration | Links to and summaries of `mickitblog.blogspot.com` |
| Health / Sports | Endurance athletics and current training |
| Contact | Professional contact copy |

## Tone and Voice

- Polished but personal
- First-person throughout
- Specific over vague
- Confident without sounding inflated
- No filler phrases or AI-sounding language
- No emojis
- Avoid em dashes in final website copy
- Active voice preferred

## Source Material

Use these facts selectively based on the section being written. Do not dump them all into every section.

**Professional**

- Automation Engineer at CBIZ
- Specializes in PowerShell, C#, SCCM, Intune, Azure AD, and endpoint security
- Co-founder of the Nashville PowerShell User Group
- Microsoft MVP Alumni
- Technical blog at `mickitblog.blogspot.com` with more than one million readers

**Builder / Maker**

- Building an off-grid container home in Stewart County, Tennessee
- Started with two 40-foot high cube containers and plans to expand further
- Solo build including welding and metal fabrication
- Upgrading from 500W to a 15kW solar target for energy independence

**Tech / AI**

- Self-hosted AI infrastructure on a Proxmox homelab
- Runs n8n automation pipelines, local LLMs, and MCP servers
- Builds algorithmic trading systems around the current mixed-stack `Trading` repo using PowerShell, Python, backtesting, journaling, schedulers, and execution tooling

**Athlete / Adventurer**

- Endurance athlete across cycling, triathlons, and strength training
- Summited Kilimanjaro at 19,341 feet
- Visited 33 plus countries and targeting 50
- Speaks Spanish

## Section Templates

### About / Bio

Use a short version for hero or intro sections and a longer version for dedicated About pages.

### Project Writeup

Structure project writeups in three parts:

1. what it is and why it exists
2. what was built and how it works
3. what is in progress or coming next

### Featured Projects

The default featured projects are:

- Container home build
- Trading systems and automation stack
- Proxmox homelab and n8n workflows

## Page Type Modes

Infer the page type from the request and shape the copy accordingly:

- `home page`: lead with who Mick is and the one or two strongest proof points; every sentence has to earn its spot above the fold
- `about page`: fuller arc across professional, builder, and athlete identities, still selective rather than exhaustive
- `service page`: what Mick builds, who it helps, and evidence it works; concrete deliverables over capability adjectives
- `project page`: follow the three-part project writeup structure with current status stated honestly
- `contact page`: short, direct, and clear about what kinds of contact are welcome

## Proof And Specificity Checks

Before finishing any section, replace unbacked claims with evidence:

- every capability claim should point to a project, repo, number, or outcome from the source material
- prefer "automated reporting across 4,000+ endpoints" over "extensive automation experience"
- if a claim has no available proof, cut it or scope it down rather than leaving it vague

## Copy Length Variants

When layout constraints are unknown or the user asks, provide the same section in two lengths: a `concise` version (1 to 2 sentences per block, suitable for cards and hero sections) and a `detailed` version (full paragraphs for dedicated pages). Both must carry the same facts; the concise version cuts context, not specifics.

## SEO Patterns

For meta descriptions:

- target roughly 150 to 160 characters
- be specific
- avoid filler

For page titles:

- keep them clean and readable
- prefer role plus identity over slogans

## Quality Checklist

- Tone is polished but personal
- First person is used consistently
- Specific details and tools are present
- No emojis or final-copy em dashes
- No filler language
- Section length matches the use case
- SEO descriptions stay concise
- Content reflects more than just the day job

## Reference File

- `reference/copy-library.md` contains reusable copy blocks for site sections

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- The page, audience, and what the content needs to accomplish.

Example prompts:

- `Use website-content to rewrite the homepage copy for mickpletcher.com in my voice.`
- `Draft service page content for my site that explains what I build without sounding salesy.`
- `Show me an example prompt for using this skill to update a specific page.`

