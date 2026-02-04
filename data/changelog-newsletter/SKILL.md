---
name: changelog-newsletter
description: Transform technical changelog entries into user-friendly newsletter content for email, blog posts, and release notes. Use when converting CHANGELOG.md files, git commit logs, or release notes into customer-facing communications.
---

# Changelog Newsletter Creator

## Overview

Convert technical changelog entries into engaging, user-friendly newsletter content suitable for email campaigns, blog posts, and release notes pages. This skill helps translate developer-focused change descriptions into benefits-oriented content for end users.

## Quick Start

Provide a changelog file or list of changes, and specify the desired output format (email, blog post, or release notes page). The skill will:
1. Identify change types (features, fixes, improvements, breaking changes)
2. Rewrite technical descriptions in user-friendly language
3. Organize content by impact and importance
4. Format for the target medium

## Detailed Instructions

### Step 1: Parse Changelog Input

Accept changelog entries in various formats:
- **Markdown CHANGELOG.md files** (Keep a Changelog format)
- **Git commit logs** (structured or conventional commits)
- **Raw change lists** (bullet points or paragraphs)
- **Release notes** (existing technical documentation)

Identify and categorize:
- New features
- Bug fixes
- Improvements/enhancements
- Breaking changes
- Deprecations
- Security updates

### Step 2: Transform to User-Friendly Language

Apply these transformation principles:

**Technical → User-Friendly:**
- "Fixed null pointer exception in payment processor" → "Resolved an issue that could cause checkout to fail"
- "Implemented OAuth2 authentication flow" → "Added secure single sign-on with your favorite services"
- "Optimized database query performance" → "Made the app faster and more responsive"
- "Deprecated legacy API endpoints" → "Upgrading our system for better reliability (action required)"

**Focus on benefits, not implementation:**
- What problem does this solve for users?
- What can users now do that they couldn't before?
- How does this improve their experience?

### Step 3: Organize by Priority and Impact

Structure content by user impact:

1. **Headline Features** - Major new capabilities
2. **Improvements** - Enhanced existing features
3. **Fixes** - Resolved issues (group similar fixes)
4. **Coming Changes** - Deprecations or upcoming breaking changes

Prioritize what users care about most:
- Visible changes over internal improvements
- Fixes for common pain points
- Features that enable new workflows

### Step 4: Format for Target Medium

#### Email Newsletter Format

Structure:
```
Subject: [Product Name] - [Month] Update: [Key Highlight]

Hi [Name],

[Opening paragraph - highlight 1-2 biggest changes]

🎉 What's New
[2-3 major features with benefits]

✨ Improvements
[3-5 enhancements, can be brief bullets]

🔧 Fixes
[Group related fixes, don't list every bug]

📢 Coming Soon
[Preview next release or important notices]

[Call to action - try new features, read docs, etc.]
```

Use:
- Emoji sparingly for visual breaks
- Short paragraphs (2-3 sentences max)
- Bold for feature names
- Links to documentation or demo videos

#### Blog Post Format

Structure:
```markdown
# [Month/Quarter] Update: [Compelling Title]

[Engaging introduction - story or user pain point]

## [Major Feature Name]

[Description with benefits, use case, example]
[Screenshot or demo link]

## Other Improvements

- **[Feature]**: [Brief benefit-focused description]
- **[Feature]**: [Brief benefit-focused description]

## Bug Fixes and Performance

We've resolved several issues including:
- [High-impact fix with user benefit]
- [Group of related fixes]

## What's Next

[Roadmap preview or upcoming features]

---
[Footer with links to changelog, docs, support]
```

Use:
- Headers for major sections
- Images or screenshots where helpful
- Code examples only if absolutely necessary
- Links to detailed documentation

#### Release Notes Page Format

Structure:
```markdown
## Version X.Y.Z - [Date]

### New Features
- **[Feature Name]**: [User-friendly description with benefit]
- **[Feature Name]**: [User-friendly description with benefit]

### Improvements
- [Enhancement with benefit]
- [Enhancement with benefit]

### Bug Fixes
- Fixed: [Description of resolved issue]
- Resolved: [Description of resolved issue]

### Breaking Changes
⚠️ **Action Required**
- [Change description and migration instructions]

### Deprecation Notices
- [What's being deprecated and timeline]
```

Use:
- Consistent formatting
- Version and date clearly marked
- Breaking changes prominently highlighted
- Links to migration guides

## Examples

### Example 1: Technical Changelog to Email Newsletter

**Input (Technical Changelog):**
```
## v2.4.0
- Added GraphQL API endpoint for user queries
- Fixed race condition in WebSocket connection handler
- Implemented rate limiting middleware
- Updated React to v18.2.0
- Removed deprecated /api/v1/users endpoint
```

**Output (Email Newsletter):**
```
Subject: Product Update - Faster API & Important Changes

Hi there,

We've shipped some exciting improvements this month, including
a more powerful way to query data and better performance across
the board.

🎉 What's New

New Data Query Options
You can now fetch exactly the data you need with our enhanced
API, making your integrations faster and more efficient.

✨ Improvements

- More reliable real-time features with improved connection handling
- Better performance and protection with smart rate limiting
- Updated to the latest React for improved speed and stability

📢 Action Required

Legacy API Sunset: The old /api/v1/users endpoint has been
removed. Please update your integrations to use /api/v2/users.
See our migration guide: [link]

Questions? Reply to this email or check our docs: [link]
```

### Example 2: Git Commits to Blog Post

**Input (Git Commits):**
```
feat: add dark mode toggle to settings
fix: resolve infinite loop in notification polling
perf: lazy load dashboard widgets
fix: correct timezone handling in date picker
docs: update API authentication guide
```

**Output (Blog Post):**
```markdown
# April Updates: Dark Mode & Performance Boost

We've been listening to your feedback, and this month's update
delivers two of your most-requested improvements.

## Dark Mode is Here

You can now switch between light and dark themes in Settings.
Easy on the eyes during late-night work sessions, and easier
on your battery too.

## Faster Dashboard Loading

Your dashboard now loads widgets as you need them, making the
initial page load noticeably faster—especially if you have
lots of customizations.

## Fixes & Improvements

- Notifications now update smoothly without hiccups
- Date and time pickers now correctly handle your timezone
- Updated API docs with clearer authentication examples

Try out dark mode today and let us know what you think!
```

### Example 3: Technical Release Notes

**Input (Internal Changes):**
```
- Migrated to PostgreSQL 15
- Implemented Redis cache layer
- Added Datadog APM instrumentation
- Fixed memory leak in background job processor
- Updated all dependencies to latest stable versions
```

**Output (User-Facing Release Notes):**
```markdown
## Version 3.1.0 - January 15, 2025

### Improvements

- **Faster Performance**: We've upgraded our infrastructure
  to deliver faster page loads and quicker response times.

- **Better Reliability**: Enhanced monitoring helps us catch
  and fix issues before they affect you.

- **Improved Stability**: Resolved a background processing
  issue that could cause delays in scheduled tasks.

### Technical Updates

- Database and caching infrastructure upgrades
- Dependency updates for security and performance

As always, we're working behind the scenes to make the product
faster and more reliable.
```

## Best Practices

### Writing User-Friendly Content

1. **Lead with benefits** - Answer "What's in it for me?"
2. **Use active voice** - "You can now..." not "Users are able to..."
3. **Be specific** - "3x faster" not "improved performance"
4. **Group related items** - Don't list 20 individual bug fixes
5. **Avoid jargon** - No database names, framework versions, or architecture details unless necessary

### Handling Different Change Types

**Features:**
- Emphasize new capabilities and use cases
- Include examples or screenshots when possible
- Link to tutorials or documentation

**Bug Fixes:**
- Focus on the user impact, not the technical cause
- Group similar fixes together
- Only highlight fixes for issues users likely experienced

**Breaking Changes:**
- Make them prominent (use warning emoji or styling)
- Explain what users need to do
- Provide migration guide links
- Give timeline if applicable

**Internal/Infrastructure:**
- Translate to user benefits (speed, reliability, security)
- Group under "Improvements" or "Performance"
- Don't list every dependency update

### Tone and Style

- **Conversational but professional** - friendly without being overly casual
- **Enthusiastic about improvements** - celebrate wins
- **Honest about issues** - acknowledge and explain fixes
- **Respectful of user time** - be concise

## Common Issues and Solutions

**Too many minor changes to list:**
Group them by category and summarize. For example: "Fixed several issues with form validation" instead of listing 8 individual input field bugs.

**Highly technical changes:**
Focus on the outcome, not the implementation. "Improved security" rather than "Implemented bcrypt password hashing with salt rounds."

**Breaking changes requiring action:**
Always include: what's changing, why it matters, what users need to do, and when they need to do it by.

**Nothing user-facing this release:**
If it's all internal improvements, frame it as: "Behind-the-scenes improvements for better performance, security, and reliability."

## Additional Considerations

### Segmentation
Consider creating different versions for different audiences:
- **End users**: Focus on features and user-visible fixes
- **Developers/API users**: Include API changes, SDK updates
- **Admins**: Highlight security, compliance, configuration changes

### Linking Strategy
Always link to:
- Detailed documentation for complex features
- Migration guides for breaking changes
- Video demos or screenshots for visual features
- Full changelog for technical details

### Timing
- **Email newsletters**: Monthly or quarterly summaries
- **Blog posts**: Major releases or significant feature launches
- **Release notes**: Every release, even minor ones
