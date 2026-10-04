---
name: person-researcher
description: Research a specific person for hyperpersonalized outreach using their public activity
tags: [research, person-intel, personalization, prospecting]
---

# Person Researcher

Researches a specific person's public activity and presence for hyperpersonalized outreach. Finds their LinkedIn posts, conference talks, articles, Twitter activity, career trajectory, and interests. The output feeds into `message-generator` Tier 3 personalization.

## Prerequisites

- WebSearch tool available
- Person's name (required) and at least one of: company, title, LinkedIn URL, email domain
- Optional: `agency.config.json` for service context (to identify relevant conversation topics)

## Phase 0: Intake

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[].name` and `icp.segments[].titles` to know which topics are relevant to the agency's pitch.
3. Accept parameters:
   - `name` -- (required) full name of the person
   - `company` -- (recommended) their current company
   - `title` -- (optional) their job title
   - `linkedin_url` -- (optional) direct LinkedIn profile URL
   - `email` -- (optional) for additional search context
   - `depth` -- `quick` (3-5 searches) | `standard` (8-12 searches) | `deep` (15+ searches). Default: `standard`

## Phase 1: LinkedIn Activity

WebSearch queries:
- `"{{name}}" site:linkedin.com/in` -- find their profile
- `"{{name}}" "{{company}}" site:linkedin.com/posts` -- find their posts
- `"{{name}}" "{{company}}" site:linkedin.com/pulse` -- find their articles

Extract:
- **Profile URL**: Their LinkedIn profile link
- **Current title and company**: Verify against provided data
- **Recent posts** (last 3-6 months):
  - Topic / subject of each post
  - Date (approximate)
  - Key points or opinions expressed
  - Engagement level (if visible in snippets)
- **Articles published**: LinkedIn Pulse articles or newsletter posts
- **Activity themes**: What topics do they post about most? (e.g., ecommerce trends, marketing, leadership, hiring)

## Phase 2: Conference Talks and Podcast Appearances

WebSearch queries:
- `"{{name}}" "{{company}}" "speaker" OR "keynote" OR "panelist" OR "conference"`
- `"{{name}}" "{{company}}" "podcast" OR "episode" OR "interview"`
- `"{{name}}" "{{company}}" site:youtube.com`

Extract:
- Conference names and dates
- Talk titles and topics
- Podcast names and episode details
- YouTube videos (talks, interviews, webinars)
- Key quotes or positions taken

## Phase 3: Written Content

WebSearch queries:
- `"{{name}}" "{{company}}" "blog" OR "article" OR "wrote" OR "author"`
- `"{{name}}" site:medium.com`
- `"{{name}}" "{{company}}" site:substack.com`

Extract:
- Blog posts (personal or company blog)
- Medium articles
- Substack newsletters
- Guest posts on industry publications
- Topics and themes of their writing

## Phase 4: Twitter/X Activity

WebSearch queries:
- `"{{name}}" "{{company}}" site:twitter.com OR site:x.com`
- `from:@possible_handle "{{company}}"` (if handle can be inferred)

Extract:
- Twitter/X handle
- Recent tweets (topics, opinions, retweets)
- Engagement style (thought leader, curator, responder, lurker)
- Followers count (if visible)
- Notable threads or viral tweets

## Phase 5: Career Trajectory

WebSearch queries:
- `"{{name}}" "joins" OR "appointed" OR "promoted" OR "new role" OR "announces"`
- `"{{name}}" "{{company}}" "previously at" OR "former" OR "ex-"`
- `"{{name}}" site:crunchbase.com OR site:angel.co`

Extract:
- Current tenure at company (how long?)
- Previous companies and roles
- Career progression pattern (agency to brand, brand to brand, startup founder, etc.)
- Recent job change (within last 6 months = high relevance signal)
- Board positions or advisory roles
- Investments or startup involvement

## Phase 6: Shared Interests and Connections

WebSearch queries:
- `"{{name}}" "{{company}}" "award" OR "recognition" OR "achievement"`
- `"{{name}}" "{{agency_founder_name}}" OR "{{agency_name}}"` -- check for existing connections
- `"{{name}}" "{{company}}" hobby OR passion OR volunteer OR community`

Extract:
- Mutual connections (if any with the agency team)
- Shared alma mater, city, or industry events
- Personal interests visible in public profiles (sports, causes, hobbies)
- Awards or recognitions
- Community involvement

## Phase 7: Synthesize Personalization Hooks

From all research, generate 3-5 specific, actionable personalization hooks. Each hook should be:

1. **Specific**: Reference a real post, talk, or event, not a generic trait
2. **Recent**: Prefer hooks from the last 3 months
3. **Relevant**: Connect to the agency's services where possible
4. **Natural**: Sound like something a human would notice and mention
5. **Non-creepy**: Avoid referencing personal/family details, locations, or anything that feels invasive

Good hooks:
- "Your LinkedIn post about the challenges of scaling a D2C brand resonated, especially the point about checkout friction."
- "Saw your talk at ShopifyConnect about mobile commerce, we've been working on exactly that with our clients."
- "Congrats on the move to BrandX, exciting time to be building their ecommerce presence."

Bad hooks:
- "I saw you went to Stanford." (too generic, feels stalkerish)
- "I noticed you live in Brooklyn." (personal, irrelevant)
- "You seem really passionate about ecommerce." (vague, could apply to anyone)

## Phase 8: Output

Return structured JSON:

```json
{
  "name": "Jane Doe",
  "title": "Head of Ecommerce",
  "company": "BrandX",
  "linkedin_url": "https://linkedin.com/in/janedoe",
  "twitter_handle": "@janedoe",
  "recent_posts": [
    {
      "platform": "LinkedIn",
      "topic": "Mobile conversion optimization for D2C brands",
      "date": "2024-01-10",
      "key_point": "Argued that most D2C brands lose 40% of mobile shoppers at checkout",
      "url": "https://linkedin.com/posts/..."
    },
    {
      "platform": "LinkedIn",
      "topic": "The role of UGC in building brand trust",
      "date": "2023-12-20",
      "key_point": "Shared data showing UGC increases conversion 2.4x vs brand content",
      "url": "https://linkedin.com/posts/..."
    }
  ],
  "talks_or_appearances": [
    {
      "event": "D2C Summit 2023",
      "topic": "Building a conversion-first product page",
      "date": "2023-11-15",
      "url": "https://youtube.com/..."
    }
  ],
  "articles": [
    {
      "title": "Why Your Shopify Store Needs a CRO Audit",
      "publication": "Medium",
      "date": "2023-10-05",
      "url": "https://medium.com/..."
    }
  ],
  "career_notes": "Joined BrandX 8 months ago from CompetitorY where she was Senior Marketing Manager. Career trajectory: agency (3 years) -> brand-side marketing (4 years) -> ecommerce leadership.",
  "interests": ["Mobile commerce", "UGC marketing", "Sustainable packaging", "Women in tech"],
  "mutual_connections": [],
  "personalization_hooks": [
    "Reference her LinkedIn post about mobile checkout friction -- directly relevant to CRO services",
    "Mention her D2C Summit talk about conversion-first product pages -- show you've done homework",
    "She joined BrandX 8 months ago -- likely still building her stack and open to agency partners",
    "Her Medium article about CRO audits makes her a warm lead -- she already believes in the value",
    "Connect over the UGC conversation -- share a relevant case study about UGC impact on conversion"
  ],
  "outreach_tone_recommendation": "Peer-to-peer, reference shared expertise in CRO. She's knowledgeable, so lead with specifics, not basics.",
  "researched_at": "2024-01-15T14:30:00Z",
  "depth": "standard",
  "search_count": 10
}
```

## Phase 9: Confidence Assessment

Rate the research quality:
- **HIGH confidence**: Found LinkedIn profile, recent posts, career data, and multiple personalization hooks
- **MEDIUM confidence**: Found profile and some activity, but limited recent posts or content
- **LOW confidence**: Common name, ambiguous results, minimal public presence

If LOW confidence, note which searches were ambiguous and suggest the user verify the LinkedIn URL directly.

## Example Usage

Trigger phrases:
- "Research this person before I reach out"
- "Find info on [name] at [company]"
- "Person intel for [name]"
- "What can you find about [name] for personalization?"
- "Prep outreach research on [name]"

```
User: Research Jane Doe, Head of Ecommerce at BrandX
Assistant: [runs 8-12 WebSearches across LinkedIn, Twitter, conferences, articles, returns structured JSON with personalization hooks]
```

```
User: Quick lookup on this LinkedIn profile: linkedin.com/in/janedoe
Assistant: [runs 3-5 focused searches using the profile as anchor, returns condensed research]
```
