---
name: marketing-ops-hub
description: This skill should be used when starting the work day for marketing and PR work, planning content production, managing campaigns, organizing media relations, or coordinating multi-platform content distribution. Use it for daily content planning, automated content creation with agents, campaign coordination, and productivity reporting. Integrates with Linear MCP and other marketing skills (brand-voice-guardian, twitter-thread-creator, media-outreach-coordinator, multi-brand-manager, launch-campaign-orchestrator).
---

# Marketing Operations Hub

## Overview

This skill transforms Linear into your marketing and PR command center, helping you replicate the productivity of an entire PR agency. It orchestrates content production workflows with AI agents, manages multi-platform campaigns, and coordinates with your other marketing skills for seamless execution.

## Core Workflows

### 1. Daily Content Production Planning

**Trigger:** "Start my work day"

**Workflow:**

1. **Show today's content deadlines** - Query Linear for content due today, organized by:
   - Publishing time/platform
   - Content type (blog, social, press, email)
   - Campaign association
   - Current status (needs research, drafting, review, ready to publish)

2. **Analyze production capacity** - Review time blocks available for content work

3. **Prioritize content queue** - Recommend which content to tackle first based on:
   - Deadlines and publishing schedule
   - Campaign dependencies (launch sequences, etc.)
   - Content complexity vs available time blocks
   - Platform-specific timing (optimal posting times)

4. **Create time-boxed schedule** - Present daily plan with specific time blocks:
   - 9-10am: Research and outline [content]
   - 10-11:30am: Draft [content]
   - 11:30am-12pm: Adapt to social platforms
   - etc.

**Agent Usage:** Launch a planning agent with Task tool (subagent_type: general-purpose) to:
- Fetch all content deadlines from Linear
- Analyze dependencies and campaign sequencing
- Calculate time requirements per content piece
- Generate optimized time-boxed schedule

**Example interaction:**
```
User: "Start my work day"
Assistant: I'll plan your content production day. Let me check today's deadlines...

Today's Content Deadlines (3 items):
📝 Blog: "How to Scale Your Startup" - Due 2pm
🐦 Twitter thread on AI trends - Due 4pm
📰 Press release for Product X - Due EOD

Recommended Schedule:
⏰ 9:00-11:00am: Draft blog post (2hr block)
⏰ 11:00-12:00pm: Use twitter-thread-creator to adapt blog to thread
⏰ 1:00-2:00pm: Review and publish blog
⏰ 2:00-3:30pm: Draft press release
⏰ 3:30-4:00pm: Final review + publish thread
⏰ 4:00-5:00pm: Press release final polish with brand-voice-guardian

Ready to start?
```

### 2. Content Creation Pipeline with Agents

**Trigger:** "Create [content type]" or "Start content production for [topic]"

**Workflow: 4-Stage Content Production**

#### Stage 1: Research & Outline
- Launch research agent to gather information
- Identify key points, data, quotes
- Create structured outline
- Define target audience and messaging angle

#### Stage 2: Draft Generation
- Launch drafting agent to create first draft
- Apply brand voice guidelines (integrate with brand-voice-guardian)
- Include SEO considerations
- Generate multiple angle options if needed

#### Stage 3: Content Adaptation
- Adapt master content for multiple platforms:
  - **Blog → Social:** Use twitter-thread-creator for Twitter
  - **Blog → Press:** Transform for media pitch with media-outreach-coordinator
  - **Single brand → Multi-brand:** Adapt voice with multi-brand-manager
- Maintain core message across platforms
- Optimize format for each channel

#### Stage 4: Editing & Polish
- Launch editing agent for final review
- Check against brand guidelines with brand-voice-guardian
- Verify technical accuracy
- Optimize headlines and calls-to-action
- Final approval from you before publishing

**Agent Coordination:** Use Task tool with multiple agents in sequence:
1. Research agent gathers and structures information
2. Drafting agent creates content
3. Adaptation agents customize for platforms (may run in parallel)
4. Editing agent polishes and validates

**Example interaction:**
```
User: "Create a blog post about our new AI feature"
Assistant: I'll run you through the full content production pipeline.

Stage 1 - Research & Outline:
[Launches research agent to gather product info, competitive landscape, customer quotes]
Done! Here's the outline... [shows structure]

Stage 2 - Draft Generation:
[Launches drafting agent]
Draft complete! [shows blog post]

Stage 3 - Content Adaptation:
Should I adapt this for other platforms?
- Twitter thread (twitter-thread-creator)
- Media pitch (media-outreach-coordinator)
- Multi-brand versions (multi-brand-manager)

Stage 4 - Polish:
[Launches brand-voice-guardian to validate voice]
Ready for your final review!
```

### 3. Campaign Management & Coordination

**Trigger:** "Plan campaign for [product/announcement]" or "Review active campaigns"

**Workflow:**

1. **Define campaign scope** - Identify:
   - Campaign type (product launch, announcement, thought leadership, event)
   - Timeline and key dates
   - Channels and platforms
   - Content needed (blog, social, press, email, etc.)

2. **Create campaign structure in Linear** - Set up:
   - Campaign project with milestones
   - Content issues for each deliverable
   - Dependencies and sequencing
   - Due dates based on campaign timeline

3. **Generate content calendar** - Plan when each piece publishes:
   - Pre-launch teasers
   - Launch day content
   - Post-launch follow-ups
   - Cross-platform sequencing

4. **Coordinate with launch-campaign-orchestrator** - For major launches:
   - Use launch-campaign-orchestrator for multi-platform campaigns
   - Integrate timing and messaging
   - Track campaign progress

**Agent Usage:** Launch a campaign planning agent to:
- Create Linear structure (project, issues, labels)
- Generate content calendar
- Identify all needed deliverables
- Set up dependencies and timeline

**Example interaction:**
```
User: "Plan campaign for our Q1 product launch"
Assistant: I'll set up a comprehensive campaign structure.

Campaign Overview:
- Launch date: March 15
- Platforms: Blog, Twitter, LinkedIn, Press
- Duration: 2-week runway + 1-week post-launch

Creating Linear structure...
✅ Created "Q1 Product Launch" project
✅ Created 12 content issues
✅ Set up dependencies and milestones

Content Calendar:
📅 March 1: Teaser blog post
📅 March 5: Twitter thread (value prop)
📅 March 10: Media outreach begins
📅 March 15: LAUNCH (blog, press release, social blitz)
📅 March 18: Follow-up case study
📅 March 22: Results and learnings post

Want me to start drafting any of this content?
```

### 4. Content Triage & Ideas Management

**Trigger:** "Triage content ideas" or "Organize my content backlog"

**Workflow:**

1. **Fetch untriaged items** - Query Linear for:
   - Content ideas without labels
   - Inbound requests without assignment
   - Media opportunities without response
   - Campaign ideas without project association

2. **Categorize each item** - For each, determine:
   - **Content type:** Blog, social, press, email, video script, etc.
   - **Platform:** Where it will be published
   - **Campaign:** Which campaign it supports (if any)
   - **Stage:** Idea, brief, in-progress, ready, published
   - **Priority:** Urgent (deadline), high (current campaign), medium (backlog), low (future)

3. **Route appropriately** - Assign to workflow:
   - Immediate content production (today's deadlines)
   - Current campaign queue
   - General backlog
   - Archive/reject (out of scope)

4. **Update Linear** - Apply labels, set deadlines, add to projects

**Agent Usage:** Launch a triage agent to:
- Process multiple ideas/requests in batch
- Apply consistent categorization
- Suggest priorities based on campaigns and deadlines
- Update Linear with recommendations for your approval

**Triage Criteria:** Load `references/content_triage.md` for guidelines on:
- Content type classification
- Priority assignment for marketing work
- Platform and campaign routing
- Content lifecycle stages

### 5. Marketing Productivity Reports

**Trigger:** "Generate content report" or "Show my marketing productivity"

**Workflow:**

1. **Define report scope:**
   - Daily: What content was published today
   - Weekly: Content produced, campaigns progressed
   - Monthly: Productivity metrics and trends
   - Campaign-specific: Progress on specific campaign

2. **Fetch and analyze data:**
   - Content published (by type, platform, campaign)
   - Content in pipeline (by stage)
   - Time spent per content type
   - Campaign milestones completed

3. **Generate metrics:**
   - Content velocity (pieces per week)
   - Platform distribution (% on each channel)
   - Campaign progress (% complete)
   - Content adaptation ratio (1 blog → X social posts)

4. **Format report** with actionable insights

**Agent Usage:** Launch a reporting agent to:
- Aggregate Linear data across time period
- Calculate productivity metrics
- Identify trends and bottlenecks
- Generate formatted report

**Report Templates:** Load `references/marketing_reports.md` for formats like:
- Daily content production summary
- Weekly marketing productivity report
- Campaign status update
- Monthly content metrics

## Linear Organization Structure

### Recommended Setup for Marketing Work

**Projects:**
- **Active Campaigns** - One project per major campaign
- **Content Production** - Ongoing content not tied to campaigns
- **Media Relations** - Press outreach and journalist relationships
- **Ideas & Backlog** - Future content and campaign ideas

**Labels (Content Types):**
- `blog-post` - Long-form blog content
- `social-post` - Twitter, LinkedIn, etc.
- `twitter-thread` - Multi-tweet threads
- `press-release` - Official press announcements
- `media-pitch` - Journalist outreach
- `email-campaign` - Newsletter or promotional emails
- `video-script` - YouTube, product demos
- `case-study` - Customer stories

**Labels (Platforms):**
- `twitter` - Twitter content
- `linkedin` - LinkedIn content
- `blog` - Company blog
- `press` - Media/press coverage
- `email` - Email marketing

**Labels (Content Stages):**
- `idea` - Concept phase
- `brief` - Outlined, ready for production
- `drafting` - Being written
- `review` - In review/editing
- `ready` - Approved, ready to publish
- `published` - Live
- `promoted` - Post-publish promotion phase

**Labels (Priority):**
- `urgent` - Deadline today
- `high` - This week's deadlines
- `medium` - Next week or general backlog
- `low` - Future ideas, no rush

**Custom Views to Create:**
- "Today's Deadlines" - Filter: assigned to you, due date = today
- "This Week's Content" - Filter: due this week, grouped by content type
- "Campaign Pipeline" - Filter: by campaign project, grouped by stage
- "Ideas Inbox" - Filter: stage = idea, no project assigned

See `references/linear_setup_guide.md` for detailed setup instructions.

## Integration with Marketing Skills

This skill coordinates with your other marketing skills:

### brand-voice-guardian
**When:** Final polish stage of content production
**How:** Automatically invoke for brand voice validation before publishing
**Trigger:** "Validate this content" or auto-check in Stage 4 of pipeline

### twitter-thread-creator
**When:** Adapting blog content to Twitter (Stage 3)
**How:** Transform long-form to thread format
**Trigger:** "Create Twitter thread from this blog post"

### media-outreach-coordinator
**When:** Press relations and journalist pitches
**How:** Create personalized media pitches for campaigns
**Trigger:** "Create media pitch for [topic]"

### multi-brand-manager
**When:** Content needs versions for multiple brand identities
**How:** Adapt voice and messaging for different brands
**Trigger:** "Create multi-brand versions"

### launch-campaign-orchestrator
**When:** Coordinating major product launches
**How:** Multi-platform campaign sequencing
**Trigger:** "Plan campaign for [product]" → delegates to launch-campaign-orchestrator for complex launches

## Linear MCP Integration

This skill leverages the Linear MCP server tools for all Linear API interactions. The MCP tools provide:
- Issue querying and filtering
- Issue creation and updates (creating content issues, campaigns)
- Label and project management
- Custom view creation
- Due date management

**Setup:** Ensure Linear MCP is installed with:
```bash
claude mcp add --transport http linear-server https://mcp.linear.app/mcp
```

**Authentication:** The MCP server handles Linear authentication. You may need to authorize the connection on first use.

## Best Practices

### Daily Workflow
1. **Start day:** "Start my work day" to see deadlines and get time-boxed schedule
2. **Content production:** Use 4-stage pipeline for any new content
3. **Quick triage:** Process new ideas/requests as they come in
4. **End of day:** Quick report to track what shipped

### Time-Boxed Content Production
- Block specific time for each content piece
- Research/outline: 30min - 1hr
- Drafting: 1-2hrs depending on length
- Adaptation: 30min per platform
- Polish: 30min

### Agent Coordination
- Let agents handle research, drafting, and adaptation
- You focus on strategic decisions and final approval
- Run adaptation agents in parallel (blog → Twitter + LinkedIn simultaneously)
- Always do final human review before publishing

### Campaign Planning
- Set up campaign in Linear before starting content production
- Create all content issues upfront with dependencies
- Use due dates to enforce publishing sequence
- Review campaign progress weekly

## Quick Reference

**Start work day:**
"Start my work day" → Shows today's content deadlines with time-boxed schedule

**Create content:**
"Create blog post about [topic]" → Runs 4-stage production pipeline with agents

**Adapt content:**
"Adapt this to Twitter" → Uses twitter-thread-creator
"Create media pitch" → Uses media-outreach-coordinator

**Campaign management:**
"Plan campaign for [product]" → Sets up Linear structure + content calendar

**Triage ideas:**
"Triage content ideas" → Processes backlog and organizes

**Generate report:**
"Show my marketing productivity" → Weekly content metrics and trends

**Validate content:**
"Validate brand voice" → Uses brand-voice-guardian