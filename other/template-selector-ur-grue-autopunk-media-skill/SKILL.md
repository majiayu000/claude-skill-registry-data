---
name: template-selector
description: "Recommend the right skill bundle, agent, and workflow sequence for a new project — so media professionals can start producing instead of browsing a 394-skill library."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.5
tags: [workflow, project-setup, skill-selection, onboarding, navigation]
---

# Template Selector

## What This Skill Does

Takes a project description and recommends which skills, agents, and workflow sequence to use — turning a 394-skill library into a short, ordered checklist for your specific project.

## When To Use This Skill

- You are starting a new media project and do not know which skills from this library apply to your format
- You have a deadline and want the fastest path from concept to deliverable without browsing categories
- You are working in a format you have not used before (first podcast, first newsletter, first documentary pitch) and want a guided starting point
- Your project crosses formats (a documentary with a companion podcast and social campaign) and you need skills from multiple categories wired into a single workflow
- You are onboarding a colleague or collaborator who has never used the skill library and want to hand them a ready-made toolkit for the project

## What You Need To Provide

**Required:**

- Project type or medium (documentary, magazine feature, podcast, YouTube channel, newsletter, investigation, PR campaign, data story, screenwriting project, radio programme, social media campaign)
- Primary deliverables (what you need to produce by the end)
- Deadline or timeline (even a rough one: "three weeks", "six months", "ongoing weekly")

**Optional:**

- Team size (solo, small team, large production)
- Experience level with this format (first time, some experience, veteran)
- Whether you have existing material to work from (a treatment, rough footage, interview transcripts, a dataset)
- Budget constraints that affect scope (no travel budget, no external contributors, etc.)
- Distribution channels (broadcast, streaming, print, web, email, social platforms)
- Whether the project has a companion format (podcast + newsletter, documentary + social campaign)

## How the Assistant Approaches This

The assistant works through these steps in order. The goal is a focused recommendation, not a catalogue of everything the library offers.

1. **Parses the project description** to identify the primary format, secondary formats, production stage (are you starting from scratch or picking up mid-project?), and any constraints that narrow the skill selection.

2. **Selects the primary skill bundle** from the Project Type Reference table below, then adjusts it: removes skills that do not apply (no scripting skills if you already have a finished script), adds cross-category skills if the project spans formats (research skills for an investigation, social media skills for a distribution push).

3. **Sequences the skills into production phases** — pre-production, production, post-production, distribution — so you know what to use when. Each phase lists the skills in the order you would realistically reach for them. Skills you need repeatedly (like copy-editor or fact-check-prompt) are marked as recurring rather than pinned to one phase.

4. **Recommends an agent** if one exists for this project type and the scope justifies it. Agents bundle 4-6 skills into a single automated run, so they make sense for projects where you want a complete package in one pass. If no agent fits, the recommendation says so and suggests running the skills individually.

5. **Generates a starter project-memory template** — a structured document you paste into your project folder to track decisions, sources, deadlines, and style choices across sessions. The template is pre-filled with sensible defaults for your project type and marked with placeholders where you fill in your specifics.

6. **Adjusts for experience level.** If the user is new to a format, the recommendation adds brief context for each skill ("what this does for you"), flags which skills to run first, and notes where the agent can handle multiple steps at once. For experienced users, the recommendation is leaner: skill names, phase groupings, and the workflow table, without explanations of what each skill does.

7. **Adjusts for team size.** Solo operators get every skill in the bundle because they cover every role. Teams get the same skills but with a note on who runs each one (the producer, the writer, the editor), so the skill list doubles as a task assignment sheet.

## Project Type Reference

The table below maps common project types to their recommended skill bundles and agents. Each bundle is a starting point; the assistant adjusts it based on your specific inputs.

### Documentary / Factual TV

**Typical scope:** 15-25 skills across development, production, and distribution. Projects range from a single-film pitch to a multi-season series bible.

| Phase | Recommended Skills |
|---|---|
| Development | `logline-creator`, `pitch-treatment-writer`, `series-bible-generator`, `character-arc-planner` |
| Pre-production | `interview-question-generator`, `subject-research-brief`, `production-schedule-writer`, `archival-footage-brief`, `production-budget-estimator` |
| Research | `topic-background-brief`, `person-biography-brief`, `event-chronology-builder`, `legislative-history-researcher` |
| Scripting | `scene-breakdown-writer`, `commentary-writer`, `narrator-voice-adapter`, `animated-explainer-script` |
| Post-production | `rough-cut-notes`, `chapter-timestamps` |
| Business | `broadcaster-pitch-writer`, `co-production-brief`, `grant-proposal-writer`, `one-sheet-writer` |
| Localization | `festival-synopsis-writer`, `dubbing-script-adapter` |
| **Agent** | `documentary-development-agent` (logline through broadcaster pitch in one run) |

### Magazine Feature / Long-Form Journalism

**Typical scope:** 12-18 skills. Heaviest in the research and editing phases, lighter in distribution.

| Phase | Recommended Skills |
|---|---|
| Ideation | `story-angle-finder`, `headline-writer`, `source-research-brief`, `expert-finder-brief` |
| Research | `topic-background-brief`, `debate-summary-writer`, `statistics-researcher`, `claim-fact-checker`, `coverage-review-brief` |
| Writing | `reportage-structure`, `lede-writer`, `sidebar-fact-box-writer`, `feature-article-writer`, `column-voice-adapter` |
| Editing | `copy-editor`, `fact-check-prompt`, `structure-checker`, `libel-risk-checker`, `text-condenser` |
| Distribution | `headline-ab-variants-writer`, `social-post-ab-variants-writer`, `publication-timing-advisor` |
| **Agent** | `magazine-editor-agent` (ideation through edited draft) |

### Podcast Series

**Typical scope:** 10-14 skills. The recurring production cycle (record, edit, publish, promote) means fewer total skills but heavier reuse.

| Phase | Recommended Skills |
|---|---|
| Pre-production | `episode-concept-generator`, `guest-research-brief`, `interview-question-builder` |
| Scripting | `solo-episode-script`, `intro-outro-writer`, `ad-read-script` |
| Post-production | `transcript-cleanup`, `show-notes-generator`, `episode-summary-writer` |
| Distribution | `caption-writer`, `thread-writer`, `publication-timing-advisor` |
| Business | `podcast-media-kit-generator`, `sponsorship-pitch-writer`, `guest-outreach-email` |
| **Agent** | `podcast-producer-agent` (concept through show notes in one run) |

### YouTube Channel

**Typical scope:** 12-18 skills. SEO and analytics skills matter more here than in any other format.

| Phase | Recommended Skills |
|---|---|
| Pre-production | `niche-video-idea-generator`, `seo-title-optimizer`, `thumbnail-concept-brief`, `hook-generator` |
| Scripting | `full-script-writer`, `b-roll-shot-list`, `call-to-action-generator`, `shorts-script-adapter` |
| Post-production | `description-seo-writer`, `chapter-timestamps`, `community-post-generator` |
| Strategy | `content-calendar-planner`, `audience-persona-builder`, `ab-title-test-brief` |
| Business | `sponsorship-email-writer`, `youtube-media-kit-generator`, `brand-deal-pitch-writer` |
| **Agent** | `youtube-channel-operator-agent` (idea through publish-ready package) |

### Newsletter

**Typical scope:** 10-14 skills. Strategy-heavy at launch, then settles into a tight weekly cycle of 3-4 recurring skills.

| Phase | Recommended Skills |
|---|---|
| Strategy | `niche-positioning-brief`, `content-arc-planner`, `newsletter-audience-segmenter`, `target-audience-definer` |
| Writing | `edition-writer`, `subject-line-writer`, `welcome-email-writer`, `re-engagement-email-writer`, `reader-response-writer` |
| Growth | `landing-page-copy-writer`, `referral-copy-writer` |
| Monetization | `paid-tier-pitch-writer`, `sponsorship-rate-card` |
| Distribution | `publication-timing-advisor`, `social-post-ab-variants-writer` |
| **Agent** | `newsletter-launch-agent` (positioning through launch-ready package) |

### Investigation / Accountability Journalism

**Typical scope:** 15-20 skills. Research and legal phases are unusually deep. The writing phase is often the shortest part of the project.

| Phase | Recommended Skills |
|---|---|
| Research | `source-research-brief`, `foia-request-writer`, `eu-document-access-builder`, `document-analysis-summary`, `investigation-timeline-builder` |
| Fact-checking | `claim-fact-checker`, `source-verification`, `statistics-verifier`, `source-credentials-checker` |
| Data | `data-story-finder`, `data-outlier-finder`, `dataset-summary-brief`, `methodology-explainer` |
| Writing | `feature-article-writer`, `reportage-structure`, `sidebar-fact-box-writer` |
| Legal review | `libel-risk-checker`, `legal-risk-checker`, `gdpr-note-writer`, `rights-clearance-checklist` |
| **Agent** | `investigative-reporter-agent` (source mapping through publication-ready draft) |

### PR / Communications Campaign

**Typical scope:** 10-15 skills. Crisis prep skills are included by default because campaigns that succeed also attract scrutiny.

| Phase | Recommended Skills |
|---|---|
| Strategy | `platform-strategy-brief`, `target-audience-definer`, `spokesperson-briefing-note` |
| Press office | `press-release-writer`, `media-alert-writer`, `boilerplate-writer` |
| Media relations | `journalist-pitch-email`, `follow-up-email-writer`, `thank-you-email-writer` |
| Content | `op-ed-writer`, `speech-writer`, `internal-memo-writer` |
| Crisis prep | `crisis-statement-writer`, `holding-statement-writer`, `faq-document-writer` |
| **Agent** | `pr-crisis-response-agent` (for crisis scenarios specifically) |

### Data Story / Data Journalism

**Typical scope:** 12-16 skills. The visualization phase is where this format diverges most from traditional journalism.

| Phase | Recommended Skills |
|---|---|
| Acquisition | `foi-data-request`, `scraper-brief`, `data-cleaning-brief`, `pdf-table-extractor-brief` |
| Analysis | `data-story-finder`, `data-outlier-finder`, `basic-statistics-calculator`, `statistics-explainer`, `polling-analysis-writer` |
| Visualization | `chart-type-advisor`, `chart-description-writer`, `infographic-brief`, `chart-labels-writer`, `data-table-formatter` |
| Writing | `data-viz-narrative-writer`, `methodology-explainer`, `data-footnote-writer` |
| Quality | `data-corrections-writer`, `fact-check-prompt` |
| **Agent** | `data-journalism-investigator-agent` (dataset through publication-ready story) |

### Screenwriting Project

**Typical scope:** 8-12 skills. Development-heavy, with a distinct revision cycle that other formats lack.

| Phase | Recommended Skills |
|---|---|
| Development | `logline-writer`, `treatment-writer`, `beat-sheet-builder`, `character-profile-writer` |
| Scripting | `scene-writer`, `dialogue-polisher` |
| Revision | `coverage-report-writer`, `script-notes-writer` |
| Business | `one-pager-writer`, `elevator-pitch-writer`, `cold-outreach-email-writer` |
| **Agent** | None currently available. Run skills individually. |

### Radio / Audio Programme

**Typical scope:** 8-12 skills. Scripting is the heaviest phase. News programmes and documentaries use different subsets.

| Phase | Recommended Skills |
|---|---|
| Pre-production | `programme-brief-writer`, `running-order-builder`, `interview-cue-sheet-writer` |
| Scripting | `bulletin-script-writer`, `presenter-link-writer`, `documentary-narration-writer`, `stand-up-script-writer` |
| News packages | `package-script-writer`, `clip-selection-brief`, `two-way-brief-writer` |
| Strategy | `podcast-to-radio-adapter`, `pitch-to-broadcaster` |
| **Agent** | None currently available. Run skills individually. |

### Social Media Campaign

**Typical scope:** 8-12 skills. Often a companion to a larger project rather than a standalone effort. If the campaign supports a documentary, newsletter, or podcast, combine this table with the primary format's table.

| Phase | Recommended Skills |
|---|---|
| Strategy | `platform-strategy-brief`, `hashtag-strategy-writer`, `target-audience-definer`, `content-calendar-planner` |
| Content | `caption-writer`, `thread-writer`, `carousel-script-writer`, `short-form-video-brief` |
| Visual | `social-media-visual-batch`, `thumbnail-concept-brief`, `cover-image-pipeline` |
| Testing | `ab-social-post-tester`, `headline-ab-variants-writer` |
| Cross-promotion | `cross-promotion-pitch`, `tag-keyword-generator`, `seo-meta-description-writer` |
| **Agent** | None currently available. Combine with format-specific agent if the campaign supports a larger project. |

### Cross-Category Skills (Added to Any Project)

These skills are not tied to a single project type. The assistant adds them when the project description calls for them.

| Need | Skills |
|---|---|
| Editing (any text) | `copy-editor`, `proofreader`, `redundancy-checker`, `tone-consistency-checker`, `structure-flow-checker` |
| Research (any topic) | `topic-background-brief`, `expert-identifier`, `claim-fact-checker`, `debate-summary-writer` |
| Legal review | `libel-risk-checker`, `legal-risk-checker`, `image-rights-checker`, `gdpr-note-writer` |
| Translation | `subtitle-translator`, `voice-over-translator`, `translation-glossary-creator`, `cultural-adaptation-brief` |
| Image creation | `editorial-photo-prompt`, `cinematic-shot-prompt`, `mood-board-brief`, `cover-image-pipeline` |
| Audience & distribution | `target-audience-definer`, `platform-distribution-advisor`, `publication-timing-advisor`, `audience-feedback-summariser` |
| Business & pitching | `elevator-pitch-writer`, `cold-outreach-email-writer`, `collaboration-proposal-writer`, `award-submission-writer` |

### Multi-Format Projects

When a project spans two or more formats, the assistant merges their skill tables and removes duplicates. Common multi-format combinations:

- **Documentary + companion podcast:** Merge the documentary and podcast tables. Shared research skills (e.g., `subject-research-brief`, `interview-question-generator`) appear once. The podcast table adds `show-notes-generator` and `episode-summary-writer` for repurposing documentary interviews as podcast episodes.

- **Newsletter + social media campaign:** The newsletter table drives the editorial cycle. The social media table adds distribution and testing skills (`caption-writer`, `thread-writer`, `ab-social-post-tester`) that promote each edition.

- **Investigation + data story:** Merge the investigation and data journalism tables. The investigation table provides the sourcing and legal review framework. The data story table adds visualization and methodology skills for the quantitative elements.

- **YouTube + podcast (same content, different formats):** Start with the YouTube table (more skills due to SEO and visual requirements). Add `transcript-cleanup`, `show-notes-generator`, and `episode-summary-writer` from the podcast table for the audio-only version.

- **PR campaign + data story:** The PR table provides the outreach and messaging framework. The data story table adds `chart-type-advisor`, `infographic-brief`, and `methodology-explainer` for evidence-backed press materials. The combined bundle is especially useful for policy organisations releasing original research.

- **Magazine investigation + documentary development:** Start with the investigation table (deeper research and legal review). Add the documentary development skills (`logline-creator`, `pitch-treatment-writer`, `series-bible-generator`) for the screen adaptation. Run the `documentary-development-agent` after the investigation's writing phase is complete.

The project-memory template for multi-format projects combines sections from both formats and adds a **Format Coordination** section tracking which deliverables feed into which output channel.

## Output Format

The recommendation has four sections, delivered in this order:

**1. Skill Bundle** — A numbered list of 8-15 skills, grouped by production phase, with one line explaining why each is included. Skills are listed in the order you would use them. Recurring skills (used in multiple phases) are noted.

**2. Agent Recommendation** — One paragraph. Names the agent if one fits, explains what it covers, and notes what you would still need to do manually. If no agent fits, says so plainly.

**3. Workflow Sequence** — A timeline or phase list mapping the skills to your stated deadline. For a three-week project, this might be "Week 1: strategy and research skills. Week 2: writing and editing skills. Week 3: distribution and testing skills." For an ongoing project (weekly newsletter, YouTube channel), it maps to the recurring production cycle instead.

**4. Starter Project-Memory Template** — A markdown document, ready to paste, with these sections pre-filled for the project type:

```
# Project Memory — [Project Type]

## Project
- **Working title:**
- **Format:**
- **Target audience:**
- **Deadline / cadence:**
- **Team:**

## Editorial Decisions
- **Tone and register:**
- **Point of view:**
- **House style notes:**

## Sources and Contacts
| Name | Role | Status | Notes |
|------|------|--------|-------|

## Key Dates
| Milestone | Date | Owner |
|-----------|------|-------|

## Skill Log
| Skill Used | Date | Notes |
|------------|------|-------|

## Open Questions
-
```

The template sections vary by project type. Below are the type-specific sections added to the base template for each format. The assistant includes only the sections relevant to the project.

**Documentary / Factual TV** adds:
- Characters & Contributors (name, role in story, interview status, release form)
- Locations (name, access status, permit required, visual notes)
- Archive Sources (institution, collection, rights status, request date)
- Episode / Act Structure (for series or multi-act films)

**Magazine Feature / Investigation** adds:
- Source Log (name, affiliation, on/off record, contact date, follow-up status)
- Document Register (document, source, date obtained, verification status)
- Fact-Check Tracker (claim, source, verified yes/no, checked by)

**Podcast Series** adds:
- Episode Tracker (episode number, guest, topic, record date, publish date, status)
- Recurring Segments (name, duration, description)
- Guest Pipeline (name, topic fit, outreach status, confirmed date)

**YouTube Channel** adds:
- Video Pipeline (title, status, script done, filmed, edited, published)
- SEO Tracker (target keyword, search volume, current ranking)
- Sponsorship Calendar (sponsor, video, deliverables, payment status)

**Newsletter** adds:
- Edition Calendar (edition number, date, theme, status)
- Subscriber Milestones (milestone, target date, actual)
- Sponsorship Pipeline (sponsor, contact, status, notes)

**Data Story** adds:
- Dataset Inventory (name, source, date obtained, format, cleaned)
- Methodology Log (decision, rationale, date)
- Chart Inventory (chart ID, type, data source, status)

**PR Campaign** adds:
- Media List (outlet, journalist, beat, pitch status, response)
- Message Matrix (audience, key message, proof point, channel)
- Coverage Log (outlet, date, headline, sentiment, reach)

**Screenwriting** adds:
- Character Bible (name, arc, first appearance, notes)
- Draft History (draft number, date, page count, major changes)
- Coverage & Feedback (reader, date, verdict, key notes)

**Radio / Audio** adds:
- Running Order (item, duration, presenter, source, status)
- Audio Assets (clip name, source, duration, rights cleared)
- Contributor Schedule (name, role, availability, segment)

Tone: direct, practical, no preamble. The recommendation reads like a production memo from a colleague who knows the library, not a product brochure.

## How to Use the Recommendation

This section is for users who receive the recommendation and want to know what to do next.

**Step 1: Save the project-memory template.** Copy the template from the recommendation into a file in your project folder. Name it `PROJECT-MEMORY.md` or whatever your team uses for project context files. Fill in the placeholders with your specifics before starting work.

**Step 2: Work through the skill bundle in order.** Start with the first skill in the first phase. Copy its SKILL.md file into a new Claude conversation, provide the inputs it asks for, and save the output. Move to the next skill. You do not need to run every skill in one sitting; the phases exist so you can pause between them.

**Step 3: Use the agent if one is recommended.** If the recommendation names an agent, you can run it instead of the individual skills it bundles. The agent produces multiple outputs in one run. Skills not covered by the agent still need to be run individually, and the recommendation tells you which ones.

**Step 4: Update the project-memory template as you go.** Log each skill you run, record editorial decisions, and track sources. The template becomes more useful the more you put into it. In future sessions, paste the updated project-memory template at the start of the conversation so the assistant has full context on your project's state, decisions made so far, and what remains to be done.

**Step 5: Revisit the recommendation when the project scope changes.** If you add a companion format (a podcast for your documentary, a social campaign for your newsletter), run this skill again with the updated project description. The new recommendation will merge the skill tables.

## Quality Criteria

- [ ] Every recommended skill exists in the library and is referenced by its correct kebab-case name
- [ ] Skills are sequenced in a realistic production order, not alphabetically or arbitrarily
- [ ] The recommendation includes only skills the user will plausibly need — no padding to make the list look thorough
- [ ] The agent recommendation is honest: names one if it fits, says "none available" if it does not, never forces a match
- [ ] The workflow sequence maps to the user's stated timeline or cadence, not a generic template
- [ ] The project-memory template includes sections specific to the project type, not just a copy of the generic template
- [ ] The full recommendation is under 600 words (excluding the project-memory template), so it reads as a checklist, not a document
- [ ] For multi-format projects, skill tables are merged and duplicates removed rather than listing skills twice
- [ ] The project-memory template's open questions are specific to the project described, not generic placeholder questions
- [ ] Each skill in the bundle has a one-line explanation tied to this specific project, not a generic description copied from the skill file
- [ ] Output is free of generic AI-template phrasing — no "delve into," "navigate the complexities of," Latinate filler verbs ("utilize," "facilitate," "leverage" where a plainer verb fits), restate-the-question intros, summary-of-the-summary closes, or em-dash overuse

## Example

### Input

I'm launching a weekly newsletter about climate policy for a European audience. Solo operation, writing and producing everything myself. First issue needs to go out in three weeks. I have a background in environmental journalism but have never run a newsletter before. I want to build a paid subscriber base eventually, but launching free first. Distribution will be email plus LinkedIn reposts.

### Output

**Skill Bundle**

*Strategy (Week 1)*

1. `niche-positioning-brief` — Define your angle within the crowded climate-policy space. Separates you from generalist climate newsletters and pure-science ones.
2. `target-audience-definer` — Pin down who reads this: EU policy staffers, NGO comms teams, climate-beat journalists, or informed citizens. The answer shapes everything else.
3. `content-arc-planner` — Map your first 8-10 editions so you are not starting from zero each week. Build thematic arcs that reward returning readers.

*Writing (Week 2)*

4. `edition-writer` — Write your pilot edition. Use this skill each week going forward.
5. `subject-line-writer` — Generate and test subject lines. Open rates live or die here, especially for a new list with no brand recognition.
6. `welcome-email-writer` — The first email a new subscriber receives. Sets tone and expectations.
7. `copy-editor` — Run every edition through this before sending. Solo operations have no second pair of eyes; this is yours. *(Recurring: use weekly.)*

*Growth and Launch (Week 3)*

8. `landing-page-copy-writer` — Write your signup page. Needs to convert cold LinkedIn traffic in under 10 seconds of reading.
9. `referral-copy-writer` — Set up a referral programme from day one, even if the list is tiny. Easier to build the habit early.
10. `linkedin-post-writer` — Adapt each edition into a LinkedIn post that drives signups. *(Recurring: use weekly.)*

*Later (Month 2+)*

11. `paid-tier-pitch-writer` — When you are ready to launch paid subscriptions, use this to write the upgrade pitch.
12. `sponsorship-rate-card` — When you have enough subscribers to attract sponsors.
13. `audience-feedback-summariser` — Once you have reader replies worth analysing. *(Recurring: use monthly.)*
14. `re-engagement-email-writer` — For subscribers who stop opening. Relevant after 6-8 weeks.

**Agent Recommendation**

Use the `newsletter-launch-agent`. It runs `niche-positioning-brief`, `edition-writer`, `subject-line-writer`, `welcome-email-writer`, and `landing-page-copy-writer` in sequence and produces a complete launch package in one pass. You still need to run `content-arc-planner` separately beforehand (the agent does not cover editorial planning), and `copy-editor` after each edition (the agent writes but does not copy-edit). For your LinkedIn distribution, run `linkedin-post-writer` manually each week.

**Workflow Sequence**

| Week | Focus | Skills |
|------|-------|--------|
| 1 | Positioning and planning | `niche-positioning-brief`, `target-audience-definer`, `content-arc-planner` |
| 2 | Write pilot edition and onboarding emails | `edition-writer`, `subject-line-writer`, `welcome-email-writer`, `copy-editor` |
| 3 | Build signup infrastructure and launch | `landing-page-copy-writer`, `referral-copy-writer`, `linkedin-post-writer` |
| Ongoing (weekly) | Write, edit, distribute | `edition-writer`, `subject-line-writer`, `copy-editor`, `linkedin-post-writer` |
| Month 2+ | Growth and monetization | `paid-tier-pitch-writer`, `sponsorship-rate-card`, `audience-feedback-summariser` |

**Starter Project-Memory Template**

```markdown
# Project Memory — Weekly Newsletter

## Project
- **Working title:** [Your newsletter name]
- **Format:** Weekly email newsletter (free tier, paid tier planned for Month 2+)
- **Target audience:** [European climate-policy audience — refine after running target-audience-definer]
- **Cadence:** Weekly, every [day]
- **Launch date:** [3 weeks from today]
- **Solo/team:** Solo

## Editorial Decisions
- **Tone and register:** [Informed but accessible — policy-literate readers, not scientists]
- **Point of view:** [First person / editorial we / neutral briefing — decide in Week 1]
- **House style notes:** EU institution names in full on first mention, acronym after. Temperatures in Celsius. Currency in EUR unless quoting USD-denominated sources.
- **Standard edition length:** [800-1200 words — adjust after pilot]
- **Recurring sections:** [e.g., lead story, policy tracker, one chart, reading list]

## Edition Calendar
| Edition # | Date | Theme / Angle | Status |
|-----------|------|---------------|--------|
| 1 (pilot) | | | Planned |
| 2 | | | Planned |
| 3 | | | Planned |
| 4 | | | Planned |
| 5 | | | Planned |
| 6 | | | Planned |
| 7 | | | Planned |
| 8 | | | Planned |

## Sources and Contacts
| Name | Role / Org | Expertise | Notes |
|------|-----------|-----------|-------|

## Subscriber Milestones
| Milestone | Target Date | Actual |
|-----------|-------------|--------|
| First 100 subscribers | | |
| First 500 subscribers | | |
| Paid tier launch | | |

## Sponsorship Pipeline
| Sponsor | Contact | Status | Notes |
|---------|---------|--------|-------|

## Skill Log
| Skill Used | Date | Notes |
|------------|------|-------|

## Distribution Channels
| Channel | Format | Frequency | Notes |
|---------|--------|-----------|-------|
| Email (primary) | Full edition | Weekly | |
| LinkedIn | Adapted post | Weekly, same day as email | |

## Performance Tracking
| Edition # | Open Rate | Click Rate | New Subscribers | Unsubscribes | Notes |
|-----------|-----------|------------|-----------------|--------------|-------|

## Open Questions
- What day of the week gets the best open rates for this audience?
- Which LinkedIn format drives more signups: long-form post or short teaser with link?
- When is the right subscriber count to launch the paid tier?
- Should the newsletter include original reporting, curation of existing sources, or a mix?
- What is the right balance between EU-level policy and national-level coverage?
```

## Known Limitations

- Recommends only skills that exist in this library. If your project needs capabilities the library does not cover (video editing instructions, audio mixing guidance, ad buying strategy), the recommendation will have gaps it cannot fill.
- The Project Type Reference covers ten broad formats. Hybrid or niche formats (interactive documentary, live-event journalism, branded content series) require more interpretation, and the skill mapping may be less precise.
- Cannot assess your actual proficiency. A first-time podcaster and a veteran producer get different explanations, but the skill selection itself does not change much — the library does not have beginner and advanced versions of the same skill.
- The workflow timeline is a rough guide based on typical production cadences. It does not account for approval bottlenecks, external dependencies (waiting for interview confirmations, data requests), or team availability.
- Agent recommendations reflect the agents currently available (8 agents as of this version). As new agents are added to the library, this skill's reference table needs manual updating to stay accurate.
- The recommendation assumes a standard production workflow (pre-production, production, post-production, distribution). Projects with non-linear workflows (iterative prototyping, agile content development, reactive newsroom production) may need the phases reordered or collapsed.
- Skill names in this file reference the library as it stood at the time of writing. If skills are renamed or restructured, the reference tables here may point to outdated names.

## Related Skills

- [copy-editor](../copy-editor/SKILL.md) — the most commonly recommended cross-category skill; appears in nearly every bundle
- [target-audience-definer](../../audience-distribution/target-audience-definer/SKILL.md) — frequently the first skill in any bundle
- [platform-distribution-advisor](../../audience-distribution/platform-distribution-advisor/SKILL.md) — useful when the recommendation needs distribution guidance beyond what the project type table covers
- [content-arc-planner](../../newsletter/strategy/content-arc-planner/SKILL.md) — editorial planning for recurring formats (newsletters, podcast series, YouTube channels)
- [niche-positioning-brief](../../newsletter/strategy/niche-positioning-brief/SKILL.md) — strategy foundation for newsletter projects
- [tone-consistency-checker](../tone-consistency-checker/SKILL.md) — cross-category editing skill recommended for multi-author or multi-format projects
- [structure-flow-checker](../structure-flow-checker/SKILL.md) — useful across all text-heavy project types
- [publication-timing-advisor](../../audience-distribution/publication-timing-advisor/SKILL.md) — distribution timing for any format with a publish schedule
- [audience-feedback-summariser](../../audience-distribution/audience-feedback-summariser/SKILL.md) — recurring skill for analysing reader or viewer responses over time
