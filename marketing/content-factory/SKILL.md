---
name: content-factory
description: Generate SEO-optimized blog articles using the Content Factory pipeline
---

# Content Factory Skill

This skill enables Claude to generate professional, SEO-optimized blog articles for any domain using the Content Factory API.

## Capabilities

- Generate articles with specified topics and target keywords
- Monitor generation progress in real-time
- Publish completed articles with preview and PR links
- Discover content opportunities by analyzing competitors

## Parameters

- **domain**: The user's website domain (required) - e.g., "mlai.au"
- **topic**: The article topic or title (required) - e.g., "How to Find a Technical Co-Founder"
- **target_keyword**: SEO target keyword (optional) - e.g., "find technical cofounder"
- **competitors**: List of competitor domains for discovery mode (optional)
- **confirmed**: Boolean flag indicating user has accepted the disclaimer (optional - internal use)

## Workflow

### Step 1: Extract Parameters
Parse the user's request to identify:
- Their domain (from context or ask if not provided)
- The topic they want to write about
- Any specific keywords they mentioned

If the user is vague (e.g., "write me some content"), ask clarifying questions:
- "What's your website domain?"
- "What topic would you like to cover?"

### Step 2: Confirm Before Starting
Before starting generation, confirm the details with the user:
```
I'll generate an article for {domain} about "{topic}" targeting "{target_keyword}".
Sound good? 👍
```

### Step 3: Start Generation
Use the `generate_article` function from `client.py` to start the job.

The function returns a `job_id` which is used to track progress.

### Step 4: Monitor Progress
Poll the job status and update the user with progress milestones:
- 🔍 **Researching** (0-20%) - Analyzing competitors and gathering data
- 📋 **Strategizing** (20-40%) - Creating content brief and outline
- ✍️ **Writing** (40-80%) - Drafting the article content
- ✨ **Optimizing** (80-90%) - SEO optimization and polish
- 🚀 **Publishing** (90-100%) - Creating PR and preview

Only send updates when progress changes significantly (every 20% or major step change).

### Step 5: Report Success
When complete, provide the user with:
- 👀 **Preview URL** - Cloudflare preview link
- 💻 **PR URL** - GitHub Pull Request for review
- Summary of what was created

Example success message:
```
🎉 Article Published!

👀 Preview: https://preview.mlai.au/articles/how-to-find-a-cofounder
💻 Pull Request: https://github.com/mlai-au/mlai.au/pull/42

Review the content and merge the PR when you're ready!
```

## Response Style

- Use encouraging language during progress updates
- Celebrate completion with enthusiasm
- Provide clear links and actionable next steps
- Use emojis appropriately to convey status
- Keep the Australian casual tone (mate, no worries, ripper, etc.)

## Error Handling

If generation fails:
1. Apologize briefly
2. Explain what went wrong (if known)
3. Suggest trying again or reaching out for help

Example:
```
Sorry mate, ran into a snag with that article generation. 
The AI writer seems to be having a moment. Mind trying again in a few? 🤔
```
