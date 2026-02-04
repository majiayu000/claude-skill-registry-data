---
name: user-onboarding
description: Guide new users through setting up a Kurt project - understand their goals, map content sources, discover topics with clustering, and organize their knowledge base.
---

# User Onboarding Workflow

## Overview

Guide users through setting up their first Kurt project with a structured 7-step workflow:
1. Understand user's intent (what they want to accomplish)
2. Create named project directory and documentation
3. Map content sources (discover URLs without fetching)
4. Compute topic clusters automatically
5. Refine clusters with user input
6. Extract reusable rules from content (optional)
7. Plan concrete next steps based on intent and clusters

**When to use this skill:**
- User is new to Kurt and needs to get started
- Starting a new content intelligence project
- User asks "how do I get started" or "help me set up"

**Important principles:**
- **Progressive disclosure**: Ask one question at a time, show results before proceeding
- **Interactive**: Get user confirmation at each major step
- **Time-aware**: Map is fast (seconds), clustering is moderate (10-30s), fetching is slow (minutes)
- **Don't fetch content until Step 6**: Discovery is cheap, fetching is expensive

## Workflow Steps

### Step 1: Understand User Intent

The first step determines what the user wants to accomplish. This creates context for the entire project.

**Question to ask:**
> What are you looking to accomplish with Kurt? Choose one:
>
> a) Update core product positioning + messaging (on website or internally)
> b) Write new marketing assets (e.g., for a product launch)
> c) Make sure technical docs + tutorials are up-to-date (and update or remove stale content)
> d) Nothing specific, just looking to get set up for a future writing project
> e) Something else (please describe)

**What happens next:**
- If **a/b/c/e**: Ask user to name the project and describe their goals
- If **d**: Create a general-purpose project setup

**Project naming guidelines:**
- Use kebab-case: `product-messaging-refresh` not `Product Messaging Refresh`
- Be specific: `q4-launch-content` not `marketing`
- Keep it short: 2-4 words maximum

### Step 2: Create Project Structure

Once we understand the intent, create a project folder and documentation.

**Actions:**
```bash
# Create project directory
mkdir -p projects/<project-name>

# Create project documentation
# File: projects/<project-name>/project.md
```

**project.md template:**
```markdown
# <Project Name>

## Goal
<User's description of what they want to accomplish>

## Intent Category
<a/b/c/d/e from Step 1>

## Content Sources
<Will be filled in Step 3>

## Topic Clusters
<Will be filled in Step 4>

## Next Steps
<Recommended actions based on project type>
```

### Step 3: Identify Content Sources

Help the user map their existing content landscape.

**Question to ask:**
> Let's start mapping your content sources. Please provide URLs for:
>
> - Company homepage (e.g., https://example.com)
> - Technical docs homepage (if applicable)
> - Blog or news section (if applicable)
> - Any other important root pages for your work
>
> You can provide multiple URLs, one per line.

**What happens next:**

For each URL provided:

1. **Map the sitemap** (discover URLs without fetching):
   ```bash
   kurct content map <url>
   ```

2. **Show discovery results:**
   ```bash
   kurt content list --url-prefix <url> --status NOT_FETCHED
   ```

3. **Update project.md** with discovered sources:
   ```markdown
   ## Content Sources

   ### <domain-name> (<count> URLs discovered)
   - Source: <url>
   - Discovered: <date>
   - Status: Mapped, not fetched
   ```

**Important:**
- Don't fetch content yet! Discovery is fast (~seconds), fetching is slow (~minutes)
- Review discovered URLs with the user before batch fetching
- Multiple sitemaps can be mapped in parallel

### Step 4: Compute Topic Clusters

Use Kurt's clustering feature to automatically discover content topics.

**Question to ask:**
> I've discovered <total-count> URLs across your content sources. Let's analyze them to discover topic clusters.
>
> Would you like to:
> a) Analyze all discovered content
> b) Focus on a specific domain (e.g., just the blog)
> c) Filter by URL pattern (e.g., only /docs/)

**Actions based on choice:**

**Option a - All content:**
```bash
# Cluster all fetched documents
kurt cluster compute --url-contains ""
```

**Option b - Specific domain:**
```bash
# Cluster documents from specific domain
kurt cluster compute --url-prefix https://example.com/
```

**Option c - URL pattern:**
```bash
# Cluster documents matching pattern
kurt cluster compute --url-contains /blog/
```

**Show results:**
```bash
# Display clusters in a table
kurt cluster list
```

**Update project.md:**
```markdown
## Topic Clusters

Analyzed <N> documents and identified <M> clusters:

1. **<Cluster Name>**
   - Description: <cluster description>
   - Example URLs: <3-5 example URLs>

2. **<Cluster Name>**
   ...
```

### Step 5: Refine and Customize

Help users refine their clusters and plan next steps.

**Questions to guide refinement:**

> Review the topic clusters above. Do they match your expectations?
>
> Common refinements:
> - Are there clusters that should be combined?
> - Are there topics you expected but didn't see?
> - Should we filter out any content types (e.g., press releases, legal pages)?

**Actions for refinement:**

**Re-cluster with filters:**
```bash
# Example: Exclude certain URL patterns
kurt cluster compute --url-prefix https://example.com/blog/ --url-contains -press-release
```

**Fetch specific content:**
```bash
# Fetch documents from a specific cluster to review
kurct content fetch --url-contains <cluster-topic-keyword>
```

**Manual cluster adjustment:**
- Guide user to edit cluster names/descriptions in project.md
- Suggest which clusters align with their project goal (from Step 1)

### Step 5.5: Extract Rules (Optional)

Before planning content work, optionally extract reusable rules from existing content.

**Question to ask:**
> Would you like to extract reusable writing rules from your content? This creates:
> - **Style guides** - Voice, tone, and writing patterns
> - **Structure templates** - Document organization and format
> - **Personas** - Audience targeting profiles
> - **Publisher profile** - Company messaging and brand context
>
> Options:
> a) Yes, extract rules now (helps ensure consistency in content creation)
> b) Skip for now (can extract later when needed)

**If user chooses (a), guide them through extraction:**

**5.5.1: Extract Publisher Profile**
```bash
# Extract organizational context from company pages
writing-rules-skill publisher --auto-discover
```

**5.5.2: Extract Style Guides**
```bash
# Identify content clusters with consistent style
# Ask: Which clusters should we extract style patterns from?
# Example: "Let's extract style from your blog posts and technical docs"

# Extract from specific content types
writing-rules-skill style --type technical-docs --auto-discover
writing-rules-skill style --type blog --auto-discover

# Can run multiple extractions for different styles
# Example: Technical docs style + Blog post style + Marketing style
```

**5.5.3: Extract Structure Templates**
```bash
# Identify content types with consistent structure
# Ask: Which content formats should we create templates for?
# Example: "Let's extract structure from tutorials and API docs"

# Extract from specific content types
writing-rules-skill structure --type tutorial --auto-discover
writing-rules-skill structure --type api-reference --auto-discover

# Can run multiple extractions for different structures
# Example: Tutorial structure + API reference structure + Landing page structure
```

**5.5.4: Extract Personas**
```bash
# Identify clusters targeting distinct audiences
# Ask: Which audiences does your content target?
# Example: "Let's extract personas from developer docs and business blog"

# Extract from audience-specific content
writing-rules-skill persona --audience-type technical --auto-discover
writing-rules-skill persona --audience-type business --auto-discover

# Can extract multiple personas if content targets different audiences
```

**Update project.md with extracted rules:**
```markdown
## Style Guidelines
- Technical documentation style: `rules/style/technical-documentation.md` (extracted: YYYY-MM-DD)
- Conversational blog style: `rules/style/conversational-blog.md` (extracted: YYYY-MM-DD)

## Structure Templates
- Quickstart tutorial: `rules/structure/quickstart-tutorial.md` (extracted: YYYY-MM-DD)
- API reference: `rules/structure/api-reference.md` (extracted: YYYY-MM-DD)

## Target Personas
- Developer persona: `rules/personas/technical-implementer.md` (extracted: YYYY-MM-DD)
- Business decision-maker: `rules/personas/business-decision-maker.md` (extracted: YYYY-MM-DD)

## Publisher Profile
- Company profile: `rules/publisher/publisher-profile.md` (extracted: YYYY-MM-DD)
```

**Quality checks:**
- ✓ Minimum 3-5 documents per extraction for reliable patterns
- ✓ Content should be consistent within each extraction set
- ✓ Auto-generated names are descriptive and clear

**If insufficient content:**
```
⚠️ Only 2 documents found for technical documentation style extraction.

Options:
- Fetch more content first: kurct content fetch --url-contains /docs/
- Proceed with caveat (may have less reliable patterns)
- Skip extraction for now
```

### Step 6: Plan Next Steps

Based on the project intent, discovered clusters, and extracted rules (if any), recommend concrete actions.

**For intent (a) - Update positioning/messaging:**
```markdown
## Recommended Next Steps

1. **Fetch current messaging content**
   ```bash
   kurct content fetch --url-prefix https://example.com/product/
   ```

2. **Extract entities and claims**
   - Understand current positioning claims
   - Identify competitor mentions
   - Map product features mentioned

3. **Analyze gaps**
   - Compare clusters to desired positioning
   - Identify missing topics
   - Find stale or conflicting messaging
```

**For intent (b) - Write marketing assets:**
```markdown
## Recommended Next Steps

1. **Fetch existing launch assets**
   ```bash
   kurct content fetch --url-contains /launch/
   ```

2. **Review similar past launches**
   - Find cluster: "Product Launches" or "Announcements"
   - Extract common patterns and messaging

3. **Build content brief**
   - Use clusters to identify themes
   - Extract claims and positioning from existing content
```

**For intent (c) - Update technical docs:**
```markdown
## Recommended Next Steps

1. **Fetch all documentation**
   ```bash
   kurct content fetch --url-prefix https://docs.example.com/
   ```

2. **Identify stale content**
   - Documents with old published_date
   - Clusters with few or outdated examples
   - Broken internal links

3. **Map doc structure**
   - Use clusters to understand current organization
   - Identify gaps in coverage
   - Plan updates by cluster
```

**For intent (d) - General setup:**
```markdown
## Recommended Next Steps

1. **Explore your content landscape**
   ```bash
   # Review discovered clusters
   kurt cluster list

   # Fetch high-priority content
   kurct content fetch --url-prefix <important-domain>
   ```

2. **When ready to start a specific project**
   - Re-run this onboarding skill
   - Choose a specific intent (a/b/c/e)
   - Focus on relevant clusters
```

**Update project.md with next steps** and mark the onboarding as complete.

## Example Complete Workflow

**User input:**
- Intent: (b) Write new marketing assets for Q4 product launch
- Project name: `q4-launch-content`
- Content sources:
  - https://www.example.com
  - https://blog.example.com
  - https://docs.example.com

**Workflow execution:**

```bash
# Step 2: Create project
mkdir -p projects/q4-launch-content
# Create project.md with goal

# Step 3: Map content sources
kurct content map https://www.example.com
kurct content map https://blog.example.com
kurct content map https://docs.example.com

# Review discovered URLs (347 total)
kurt content list --status NOT_FETCHED

# Step 4: Compute clusters
kurt cluster compute --url-contains ""

# Results: 8 clusters identified
# - Product Features (45 documents)
# - Customer Stories (23 documents)
# - Technical Guides (67 documents)
# - Company News (34 documents)
# - Pricing & Plans (12 documents)
# - Security & Compliance (28 documents)
# - API Reference (89 documents)
# - Blog Posts (49 documents)

# Step 5: Refine - User wants to focus on product-related clusters
kurt cluster compute --url-contains product

# Step 6: Plan next steps
# Recommended: Fetch "Product Features" and "Customer Stories" clusters
# Extract entities and claims to understand current messaging
```

**Final project.md:**
```markdown
# Q4 Launch Content

## Goal
Create marketing assets for our Q4 product launch, focusing on new AI capabilities and enterprise features.

## Intent Category
b) Write new marketing assets

## Content Sources

### www.example.com (178 URLs discovered)
- Source: https://www.example.com
- Discovered: 2024-01-15
- Status: Mapped, not fetched

### blog.example.com (89 URLs discovered)
- Source: https://blog.example.com
- Discovered: 2024-01-15
- Status: Mapped, not fetched

### docs.example.com (80 URLs discovered)
- Source: https://docs.example.com
- Discovered: 2024-01-15
- Status: Mapped, not fetched

## Topic Clusters

Analyzed 347 documents and identified 8 clusters:

1. **Product Features** (45 documents)
   - Core product capabilities and feature descriptions
   - Examples: /product/ai-features, /features/enterprise

2. **Customer Stories** (23 documents)
   - Case studies and success stories
   - Examples: /customers/acme-corp, /case-studies/

...

## Next Steps

1. **Fetch product-related content**
   ```bash
   kurct content fetch --url-contains /product/
   kurct content fetch --url-contains /features/
   ```

2. **Extract positioning elements**
   - Run entity extraction on product pages
   - Identify current feature claims
   - Map competitor mentions

3. **Analyze past launches**
   - Review "Company News" cluster for previous launch patterns
   - Extract messaging themes
   - Identify successful positioning approaches
```

## Workflow Guidelines

**Progressive Disclosure:**
- Ask one question at a time
- Show results before moving to next step
- Let users review and confirm before proceeding

**Error Handling:**
- If `kurct content map` finds no sitemap, suggest `kurct content add <url>` instead
- If clustering returns 0 clusters, suggest fetching content first with `kurct content fetch`
- If user provides invalid project name, suggest kebab-case alternative

**Customization:**
- Users can skip clustering if they already know their content structure
- Users can re-run clustering with different filters
- Users can manually create/edit project.md

**Time Expectations:**
- Mapping sitemaps: seconds per domain
- Computing clusters: ~10-30 seconds for 100-500 documents
- Fetching content: ~0.4-0.6s per document in batch mode

## Quick Reference

| Step | Command | Purpose |
|------|---------|---------|
| 1. Understand intent | (Interactive Q&A) | Determine project goal |
| 2. Create project | `mkdir projects/<name>` | Set up project structure |
| 3. Map sources | `kurct content map <url>` | Discover content URLs |
| 4. Compute clusters | `kurt cluster compute --url-prefix <url>` | Identify topics |
| 5. Refine | `kurt cluster compute --url-contains <pattern>` | Adjust clustering |
| 6. Plan next steps | Update project.md | Document recommendations |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No sitemap found" | Use `kurct content add <url>` to add URLs manually |
| "No clusters created" | Fetch content first: `kurct content fetch --url-prefix <url>` |
| Clustering takes too long | Start with a subset: `--url-prefix https://example.com/blog/` |
| Too many clusters | Re-cluster with more specific URL filter |
| Too few clusters | Expand URL filter or fetch more content |

## Next Skills to Use

After onboarding completes, recommend these skills:

- **ingest-content-skill**: Fetch and manage document content
- **document-management-skill**: Query, filter, and analyze documents
- **project-management-skill**: Add sources/targets, check rule coverage, track progress
- **writing-rules-skill**: Extract additional writing rules (style, structure, persona, publisher) as needed
- **content-writing-skill**: Create content with comprehensive lineage tracking
- **research-skill**: Set up project monitoring and research workflows
