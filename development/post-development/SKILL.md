---
name: post-development
description: Orchestrate app launch preparation - SEO, screenshots, personas, ads, articles, landing pages
allowed-tools: Bash, Read, Write, Glob, Grep, Task
---

# Post-Development Skill

This skill enables comprehensive post-development preparation for app launches, including marketing materials, SEO, and content generation.

## When to Use

Use this skill when:
- Preparing an application for launch
- Creating marketing materials for an app
- Generating SEO data for public pages
- Creating personas and marketing strategies
- Generating social media ads
- Writing showcase articles
- Designing landing pages

## Capabilities

### 1. Project Analysis
- Detect project type and tech stack
- Discover public routes
- Extract product information from docs

### 2. SEO Analysis (`/pd-seo`)
- Generate meta tags for all pages
- Create keyword strategies
- Produce Open Graph specifications
- Generate sitemap

### 3. Screenshot Capture (`/pd-screenshots`)
- Capture all public pages
- Multiple viewports (desktop, tablet, mobile)
- Light and dark mode
- Focus on key sections

### 4. Persona Creation (`/pd-personas`)
- Create detailed buyer personas
- Develop marketing strategies
- Generate CTAs for all channels

### 5. Ad Generation (`/pd-ads`)
- Instagram, Facebook, LinkedIn, Twitter
- Multiple ad formats per platform
- A/B variations

### 6. Article Writing (`/pd-articles`)
- 3 showcase articles
- Different angles (story, tutorial, case study)
- SEO optimized

### 7. Landing Pages (`/pd-landing`)
- Persona-specific designs
- All sections specified
- Copy and image recommendations

## Usage

### Initialize
```
/post-dev init --base-url http://localhost:3000
```

### Run All Tasks
```
/post-dev run
```

### Run Specific Task
```
/post-dev run --task seo
```

### Check Status
```
/post-dev status
```

## Output Directory Structure

```
.post-development/
├── post-development.json     # Master plan
├── seo/
│   ├── pages/               # SEO data per page
│   └── assets/              # Favicon, OG image specs
├── screenshots/
│   ├── desktop/
│   ├── tablet/
│   └── mobile/
├── personas/
│   ├── personas/            # Individual persona files
│   ├── strategies/          # Marketing strategies
│   └── cta/                 # CTA collections
├── ads/
│   ├── instagram/
│   ├── facebook/
│   ├── linkedin/
│   └── twitter/
├── articles/
│   ├── article-1/
│   ├── article-2/
│   └── article-3/
└── landing-pages/
    └── [persona-name]/
```

## Task Dependencies

Tasks run in dependency order:
1. `seo` → no dependencies
2. `screenshots` → no dependencies  
3. `personas` → depends on `seo`
4. `ads` → depends on `personas`, `screenshots`
5. `articles` → depends on `personas`, `screenshots`
6. `landing` → depends on `personas`, `screenshots`, `articles`

## Requirements

- **For screenshots:** Playwright installed (`npm install -D playwright`)
- **For screenshots:** App running at baseUrl
- **For articles:** Screenshots completed first
- **For landing pages:** All prior tasks completed

## Example Workflow

```bash
# 1. Initialize project
/post-dev init --base-url http://localhost:3000

# 2. Run everything
/post-dev run

# 3. Or run tasks individually
/post-dev seo
/post-dev screenshots
/post-dev personas
/post-dev ads
/post-dev articles
/post-dev landing

# 4. Check progress anytime
/post-dev status
```
