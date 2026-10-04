---
name: medium-writer
description: Medium-native long-form research, author-assistance, writing, editing, review, topic discovery, publication matching, and packaging workflow. Use when creating, outlining, researching, revising, auditing, or packaging Medium stories, essays, tutorials, reviews, explainers, comparisons, case studies, publication submissions, Medium 长文, Medium 选题, Medium Topics, or Medium publishing packs that need original author perspective, narrative craft, relevant topics, responsible AI disclosure, and reader-centered distribution readiness.
---

# Medium Writer

## Goal

Help an author turn original experience, expertise, notes, research, or a defensible idea into a Medium-native story that rewards the reader's time.

This skill reuses the parent `writer` workflow for fact checking, source discipline, humanization, local images, and optional Cloudflare R2 delivery, but it does not treat Medium as a generic SEO blog, a LinkedIn article host, or an automated content-distribution channel.

Medium-native work prioritizes:

- a clear reason this author should tell this story;
- an original insight, experience, experiment, case, or synthesis;
- a title, subtitle, and preview image that accurately represent the story;
- narrative movement and section-to-section continuity;
- reader value over traffic capture, product promotion, or keyword coverage;
- relevant Medium Topics and a realistic Publication fit;
- transparent AI assistance and image labeling;
- a publishing pack separated from the public story.

Default language follows the user's request. Medium's current distribution guidance treats English and non-English stories differently, so record the target language and do not imply equal eligibility for General Distribution or Boost without current verification.

## Platform Routing

| Destination | Workflow |
|---|---|
| Medium story, essay, tutorial, review, or Publication submission | Use this skill |
| LinkedIn Article, newsletter, or LinkedIn thought leadership | Use `../linkedin-writer/SKILL.md` |
| Google-first website article | Use `../SKILL.md` |
| Chinese WeChat Official Account article | Use `../wechat-writer/SKILL.md` |

If the user says only “Medium article,” default to a Medium story published from the author's profile. Recommend a Publication only after checking its current theme, submission rules, open status, and story fit.

## Required References

Read every relevant file completely before acting:

- Medium search, Topic discovery, current topic seeds, and Publication research: `references/medium-topic-research.md`
- New story, rewrite, or reusable result format: `references/medium-article-template.md`
- Editorial review, distribution readiness, and revision gate: `references/medium-review-rubric.md`
- Current claims, comparisons, or fact-heavy subjects: `../references/fact-check-and-style.md`
- Final natural-language edit after factual and structural revision: `../references/humanization.md`
- Local images, file packaging, and optional R2 delivery: `../references/output-packaging.md`
- R2 upload tasks only: `../references/r2-image-upload.md` and `../references/r2-security.md`

Do not load unrelated references merely because they exist.

## Medium AI Authorship and Disclosure Boundary

Medium currently distinguishes human-created writing, AI-assisted writing, and primarily AI-generated writing. This skill is an author-assistance and editorial workflow, not a way to disguise automated writing as human work.

Apply these rules:

1. Build the story around user-provided experience, expertise, examples, decisions, observations, or an explicitly approved editorial thesis whenever possible.
2. Never invent first-hand experience, emotions, scenes, dialogue, customers, experiments, failures, results, or personal stakes.
3. If generated prose from this workflow remains in the story, add a clear AI-assistance disclosure within the first two paragraphs, following Medium's current policy.
4. If images were generated or materially modified by AI, identify that in each affected image caption.
5. Do not mark a primarily AI-generated story as paywall-ready. Medium currently excludes primarily AI-generated writing from Partner Program paywall eligibility.
6. Do not call any draft “Boost-ready.” Boost is a Medium curation decision, and current guidance emphasizes human-created work, first-hand experience, originality, value, and craft.
7. Humanization may improve readability but must not erase required disclosure, manufacture an author voice, or simulate lived experience.
8. If the author has not supplied enough original material, deliver a research brief, interview prompts, outline, and clearly labeled working draft that requires substantive author revision before publication.

The publishing pack must record:

- author material supplied;
- AI assistance used;
- required disclosure text;
- human review status;
- paywall eligibility status: `not eligible`, `needs author verification`, or `eligible based on verified human authorship`;
- Boost status: always `not claimed` unless Medium has already assigned a verified badge after publication.

## Other Non-Negotiable Boundaries

1. Do not invent data, sources, quotes, product capabilities, prices, rankings, or Publication acceptance.
2. Do not copy another Medium writer's hook, structure, story, metaphor, examples, voice, or ending.
3. Do not call a Topic hot, trending, or popular from one story or one search result.
4. Do not use irrelevant Topics or mass mentions to chase distribution.
5. Do not produce link roundups, affiliate-first reviews, PR copy, or product announcements disguised as editorial stories.
6. Disclose affiliations, affiliate relationships, product ownership, sponsorship, or other material interests.
7. Do not guarantee indexing, General Distribution, Boost, Publication acceptance, earnings, reads, or engagement.
8. Writing, generating images, uploading assets, submitting to a Publication, applying a paywall, and publishing are separate permissions.

## Medium Story Brief

Before research or writing, create or infer a brief in 14 lines or fewer and save it as `medium-brief.md`:

- Author and authority basis: supplied experience, expertise, research, or viewpoint.
- Target reader: who they are and why they would choose this story.
- Reader tension: the unresolved problem, feeling, decision, or curiosity.
- Core idea: the one insight or transformation the story must deliver.
- Reader after-state: what changes in understanding, feeling, or action.
- Story type: essay / tutorial / explainer / review / comparison / case study / reported analysis / listicle.
- Original contribution: what is new beyond a search summary.
- Primary Medium Topic: the clearest discovery category.
- Supporting Topics: up to four, each with a direct content reason.
- Publication target: named Publication or profile-only; unknown is acceptable.
- Evidence requirement: 3-6 factual or comparative claims to verify.
- Narrative material: scenes, examples, data, code, screenshots, or approved anecdotes.
- Target length: determined by the story; normally 900-2,000 words for substantial nonfiction, not a platform rule.
- AI/disclosure status: assistance type, required disclosure, and author-review requirement.

Make conservative assumptions when information is missing. Ask only when authorship material, thesis, target reader, or permission to use personal material is materially ambiguous.

## Working Modes

### Continuous mode (default)

Run `brief -> topic research -> evidence -> outline -> draft -> audit -> rewrite -> humanize -> package`. Deliver a reviewed local draft and state the author-review and disclosure requirements.

### Topic-radar mode

When the user asks what to write, generate and rank topic opportunities only. Do not turn every topic into a shallow story.

### Interview-first mode

Use this when the story needs lived experience but the user supplied only a topic. Produce 5-10 precise questions that can elicit scenes, decisions, mistakes, sensory details, evidence, and changed beliefs. Pause only if the missing answers would determine the truth of the story.

### Interactive mode

Pause at the shortlist or outline when the user explicitly asks to choose first.

### Audit mode

If the user asks only for review, do not overwrite the draft. If they ask to improve it, preserve the original, apply fixes, and re-audit.

## End-to-End Workflow

### 1. Create an isolated story directory

Use:

```text
writer/medium-writer/output/<story-slug>/
```

This Medium-specific output directory overrides the parent writer's default `writer/output/<article-slug>/` location. Prefer a short ASCII, hyphen-separated slug under 80 characters. Do not mix multiple stories in one folder.

Recommended working files:

```text
medium-brief.md
medium-topic-map.md
source-ledger.md
outline.md
draft.md
article-medium.md
medium-audit.md
medium-publishing-pack.md
image-plan.md
```

Create only what the task needs. Keep `draft.md` separate from `article-medium.md`.

`article-medium.docx` is optional and should be created only when the user requests Word handoff or offline editorial review. A `.docx` is not a native Medium publishing requirement.

### 2. Research Medium search, Topics, and Publications

Read `references/medium-topic-research.md` completely.

Research across:

- Medium search suggestions and result pages when accessible;
- established Medium Topic pages and their adjacent Topics;
- recent recommended stories, Staff Picks, and relevant Publications;
- Publication submission guidelines, topic requirements, read-time rules, image/subtitle requirements, and paywall conditions;
- original or authoritative external sources;
- the author's existing stories, audience interests, comments, support questions, or approved experiences.

Record query, date, surface, directly observed signal, editorial inference, and evidence strength in `medium-topic-map.md`.

Separate:

- **Observed on Medium:** visible Topic, recurring question, story angle, Publication pattern, or reader language.
- **External evidence:** primary report, official documentation, search demand, or source material.
- **Author advantage:** experience, access, data, case, or viewpoint this writer can legitimately add.
- **Editorial inference:** a proposed story angle that still needs validation.

Never convert Topic follower counts, story counts, claps, or recommendation placement into guaranteed demand.

### 3. Select Topics as editorial labels

Medium currently allows up to five Topics per story. Choose only relevant Topics:

- one broad reader-interest Topic;
- one field or craft Topic;
- one specific subject or technology Topic;
- one intent or outcome Topic when useful;
- one audience, experience, or adjacent Topic only when the body supports it.

Use fewer than five when additional Topics would dilute the story. Topic spamming can restrict distribution.

For every Topic, record:

- exact Topic name;
- why it describes the public story;
- which section supports it;
- whether it is broad, specific, or adjacent;
- whether it was verified as an available Medium Topic.

### 4. Evaluate Publication fit

Do not select a Publication solely by follower count.

Check:

- editorial theme and recent stories;
- target reader and tone;
- submission guidelines and whether submissions are open;
- whether the author is approved, following, or eligible to submit;
- required subtitle, image, topic match, read time, or paywall state;
- exclusivity, canonical, licensing, or prior-publication conditions;
- expected review status and editing control;
- whether the story adds something the Publication has not just published repeatedly.

Record `best fit`, `possible fit`, or `profile-first`, with evidence. Never claim acceptance before the Publication editor approves the story.

### 5. Build the source and authorship ledger

Create `source-ledger.md` for fact-heavy, current, comparative, reported, product, health, legal, financial, or policy-related stories.

Record for each material item:

- claim or narrative element;
- type: fact / inference / editorial judgment / user-provided experience / generated suggestion;
- source, date, URL, or user-provided provenance;
- status: `verified`, `user_provided`, `needs_verification`, `softened`, `removed`, or `unsupported`;
- intended section;
- caveat, expiry risk, or disclosure need.

Generated suggestions cannot become personal experience. Unsupported material cannot enter the final story.

### 6. Choose a Medium-native story architecture

Select one primary architecture:

- Personal essay: scene -> tension -> reflection -> changed understanding -> resonant ending.
- Practitioner essay: observed problem -> experience/evidence -> insight -> implications -> takeaway.
- Tutorial: reader problem -> prerequisites -> guided build -> failure points -> verification -> next step.
- Explainer: concrete question -> intuitive model -> evidence/examples -> misconception -> application.
- Review: use context -> criteria -> observed strengths -> limitations -> reader-specific judgment.
- Comparison: decision stakes -> criteria -> scenario comparison -> trade-offs -> conditional recommendation.
- Case study or teardown: context -> decision -> execution -> result/evidence -> what transfers -> what does not.
- Reported analysis: current signal -> thesis -> evidence -> competing interpretation -> implications.
- List essay: unifying thesis -> substantial items -> progression -> synthesis; not a link farm.

Avoid forcing every story into “introduction, benefits, challenges, future.”

### 7. Create the outline

Save `outline.md` with:

- kicker, title, and subtitle directions;
- opening scene, tension, or claim and its provenance;
- central thesis or emotional movement;
- 3-7 main sections;
- evidence, example, or experience assigned to each section;
- section-to-section transition logic;
- counterpoint, limitation, or unresolved question;
- optional image purpose and placement;
- ending turn: the final insight, action, image, or question;
- author material still needed.

If the user requested a full draft, continue without waiting unless missing author material would require fabrication.

### 8. Draft for reading continuity

Read `references/medium-article-template.md` completely.

The first 100-150 words should establish:

- a real scene, tension, question, claim, or decision;
- why this author or evidence can illuminate it;
- what kind of journey or value the reader can expect.

Then:

- keep most paragraphs to 1-5 sentences;
- use section headings to mark genuine turns, not keyword slots;
- make each section change the reader's understanding;
- use examples, scenes, code, evidence, or practical checks instead of abstract claims;
- vary paragraph and section length naturally;
- include uncertainty, limits, or a competing interpretation where it improves trust;
- keep promotion subordinate to the story and disclose it;
- end with an earned insight, image, decision, or question rather than a generic summary.

Do not add an FAQ unless the story format genuinely benefits from it. Do not add a “Key Takeaways” block to a personal essay unless the author wants that register.

### 9. Use images selectively

Medium's current guidance says images, if used, should add value. A poor cover is worse than no cover.

- Do not force one image after every H2.
- Default to one featured-image direction and 0-3 in-body visuals according to information need.
- Use original photography, attributable diagrams, screenshots with permission, or editorial visuals that clarify the story.
- Add alt text and image credits.
- Label every AI-generated or AI-assisted image in its caption.
- Set a focal-point note for the featured image because Medium may crop previews.
- Do not create fake UI, fabricated data charts, fake logos, awards, customers, or documentary scenes.

Keep local relative paths first. Upload only when public URLs are needed and a valid local R2 configuration exists.

### 10. Fact-check and run the authorship gate

Verify all objective claims, comparisons, dates, products, policies, and high-risk advice. Then ask:

- Which passages contain the author's actual experience or original analysis?
- Which passages were generated or substantially shaped by AI?
- Is required disclosure present within the first two paragraphs?
- Did humanization accidentally remove or weaken disclosure?
- Are AI-generated images captioned?
- Is the draft primarily AI-generated and therefore not paywall-eligible under current Medium policy?
- Does the draft need substantive author revision before it can honestly represent the writer?

Record the result in `medium-audit.md` and `medium-publishing-pack.md`.

### 11. Audit, revise, and humanize

Read `references/medium-review-rubric.md` completely. Score:

- author reason and authenticity;
- originality and insight;
- reader value;
- narrative architecture;
- evidence and trust;
- prose craft and readability;
- title/subtitle/preview integrity;
- Topic and Publication fit;
- policy and publishing completeness.

Resolve blocking and high-impact issues directly. Then read `../references/humanization.md` and improve cadence, specificity, transitions, and voice without inventing experience or hiding AI assistance.

Run the deterministic audit:

```bash
node writer/medium-writer/scripts/audit-medium-markdown.mjs \
  writer/medium-writer/output/<story-slug>/article-medium.md \
  --pack writer/medium-writer/output/<story-slug>/medium-publishing-pack.md \
  --topic "<primary Medium Topic>" \
  --ai-assisted
```

Add `--ai-images` when the package contains generated or materially AI-assisted images.

The script checks Markdown and publishing-pack signals only. It cannot verify authorship, factual accuracy, originality, Publication acceptance, distribution, or Boost eligibility.

### 12. Build the Medium publishing pack

Save `medium-publishing-pack.md` separately. Include:

- public story title, subtitle, and optional kicker;
- optional custom preview title and subtitle;
- primary and supporting Topics, maximum five, each with rationale;
- Publication recommendation, fit evidence, submission requirements, and current status;
- featured image, alt text, credit, caption, and focal-point note;
- in-body image credits and AI labels;
- canonical/import setting for republished work;
- author material and human review status;
- AI assistance disclosure text and required placement;
- paywall eligibility assessment;
- Boost status: `not claimed` or verified post-publication status;
- email-to-subscribers and schedule decision;
- excerpt or social share copy;
- sources, affiliation, sponsorship, and affiliate disclosure;
- post-publication measurement plan;
- exact publication state.

Do not put internal Topic rationales, Publication notes, paywall analysis, or audit results in the public story body.

### 13. Package and hand off

A normal complete Medium story package contains:

```text
writer/medium-writer/output/<story-slug>/
├── article-medium.md
├── medium-brief.md
├── medium-topic-map.md
├── source-ledger.md
├── outline.md
├── medium-audit.md
├── medium-publishing-pack.md
└── image-plan.md
```

Add `draft.md`, images, `article-medium.docx`, compressed R2 copies, or `image-urls.json` only when needed.

The final response should state:

- selected story idea, reader, and author contribution;
- exact paths to article, topic map, source ledger, audit, and publishing pack;
- verified-claim count and remaining limits;
- AI assistance/disclosure and human-review status;
- images generated, planned, or uploaded;
- Publication submission and publication state;
- that no external submission or publication occurred unless explicitly authorized and verified.

## Medium Distribution Model

Treat distribution as a platform decision, not an output promise:

- Network Distribution: baseline matching to followers of the writer and/or Publication.
- General Distribution: broader interest-based matching when eligible.
- Boost: additional human-curated distribution for selected high-quality stories.

Optimize for reader trust, originality, experience, value, and craft. Do not write to a checklist that claims to guarantee Boost.

## Post-Publication Learning Loop

When the user asks to evaluate a published story, use current Medium Stats rather than predictions.

Review what is available:

- presentations, views, and reads;
- feed clickthrough and read ratio when enough data exists;
- clappers, highlighters, responders, followers, and subscribers;
- Medium vs external traffic sources;
- reader interests and Topic affinity;
- Publication, feature, or Boost badges;
- qualitative responses, highlights, and recurring questions;
- earnings only when the story is eligible and the user asks.

There is no universal good feed clickthrough or read ratio. Compare the author's stories over time, by format and audience, rather than inventing benchmark targets.

Use the results to update:

- title/preview clarity;
- opening promise;
- section depth or length;
- Topic selection;
- Publication fit;
- next-story questions.

## Completion Gate

- The brief identifies author material, reader tension, original contribution, and AI/disclosure status.
- Topic research separates observations, external evidence, author advantage, and editorial inference.
- No more than five relevant Topics are selected, with body support for each.
- Publication fit is evidence-based and acceptance is not implied.
- Material claims and personal elements have traceable provenance.
- The title, subtitle, and featured image accurately represent the story.
- The opening establishes a real tension and reader promise.
- Sections create narrative or intellectual movement.
- The story adds experience, evidence, method, or original synthesis beyond a search summary.
- Images add value, include alt text and credit, and label AI generation when applicable.
- Required AI disclosure appears within the first two paragraphs.
- Paywall eligibility and Boost status are stated conservatively.
- Editorial review passes the rubric and deterministic warnings are resolved or explained.
- Public story, draft, audit, and publishing pack remain separate.
- No upload, submission, paywall change, or publication occurred without authorization.
