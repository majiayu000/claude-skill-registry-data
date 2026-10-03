---
name: analyze-reply
description: Analyze forwarded content for factual accuracy, then draft a reply in the user's voice. Use when the user provides forwarded content and asks for analysis, fact-checking, or a reply. Triggers on "analyze this", "fact-check this", "vet", "vet this", "reply to this article", "what do you think of this piece", and "draft a reply to this".
when_to_use: Use when the user forwards or pastes an article, a post, a newsletter, or a message and asks what to make of it, whether its claims hold up, or for a reply written in their own voice. The word "vet" applied to forwarded content selects this skill in analysis-only form, where the claim analysis is produced and the reply draft is skipped.
---

# Analyze & Reply

## Identity
- **Skill Name**: `analyze-reply`
- **Version**: 1.2
- **Purpose**: Analyze forwarded content (articles, posts, essays, emails) for factual accuracy, then draft a reply in the user's voice.

## Trigger
Activate when the user provides forwarded content (article, essay, post, email) and asks for analysis, fact-checking, or a reply to the sender. If the user specifies a tone or approach in the request (for example, "send a short reply," "push back on this"), skip Phase 2 and draft accordingly.

**"Vet" shortcut:** When triggered by "vet" or "vet this," run Phase 1 only (analysis through Step 4 summary). Do not proceed to Phase 2 or 3. No reply is drafted.

## Phase 1: Content Analysis

### Step 1: Source Classification
Identify the content type and source:
- **Hard news** (reporting by named journalists at established outlets)
- **Opinion or editorial** (bylined argument pieces, op-eds, columns)
- **Newsletter or blog** (for example, Substack or personal blogs)
- **Academic or institutional** (working papers, policy briefs)
- **Personal email or message**

Note the author's credentials, the publication, and any stated methodology. Flag if the piece blends reporting with editorial framing.

### Step 2: Claim Extraction and Categorization
Read the full content and sort every substantive claim into four categories. Assign each claim a confidence level: **High**, **Moderate**, **Low**, or **Unverifiable**. Use web search to verify time-sensitive, statistical, or high-stakes factual claims before categorizing them.

#### Factual (Verifiable, Supported)
- Claims that can be independently confirmed through primary sources, public records, or established reporting.
- Note the quality of attribution (named sources, named journalists, linked documents vs. anonymous or unattributed).
- Flag any factual claims where the author's characterization is accurate but the framing subtly editorializes (for example, a correct statistic presented without relevant context).

#### Not Factual (Incorrect or Misleading)
- Claims that are demonstrably wrong, outdated, or materially misleading.
- Provide the correct information with source.
- Distinguish between outright falsehoods and distortions (technically true but misleading).

#### Opinion (Normative Judgments, Editorial Framing)
- Value judgments, characterizations, and interpretive frameworks.
- Narrative arc or thesis that connects discrete facts into a broader argument.
- Loaded language, rhetorical moves, or framing choices that embed a viewpoint.

#### Speculation (Plausible Inferences, Unproven)
- Causal claims based on correlation or temporal proximity.
- Predictions or forward-looking assertions.
- Inferences about motive, intent, or strategy that cannot be directly verified.
- Note where the author appropriately hedges vs. where they assert speculation as fact.

### Step 3: Structural Assessment
Evaluate the piece's overall construction:
- **Attribution quality**: Does the author cite named reporters, primary documents, or data? Or rely on anonymous sources and assertion?
- **Counterarguments**: Does the author engage with the strongest opposing view, or present only one side?
- **Connective tissue**: If the piece links multiple events into a narrative, assess whether those connections are evidenced or asserted.
- **Rhetorical moves**: Note any Motte-and-Bailey patterns (using uncontroversial facts to shield controversial opinions), appeals to authority, or guilt by association.

### Step 4: Summary
Provide a concise (3-5 sentence) overall assessment that includes:
- What the piece gets right
- Where it is weakest
- The strongest counterargument the author does not engage with

## Phase 2: Reply Options

Present the user with three reply options, briefly described:

1. **Analytical**: Acknowledge what is factual, note what is editorial or speculative, push back on the weakest claims, and land on a principle or substantive point. Similar to a peer review.
2. **Validating**: Lead with agreement on the strongest points, keep pushback lighter, emphasize shared concern.
3. **Short and warm**: A few sentences acknowledging the sender's concern, noting one or two key points, without getting into the weeds.

Ask the user:
- Which option (1, 2, or 3)?
- Any specific point to land on or emphasize?
- Any claims to agree with or push back on specifically?

## Phase 3: Draft Reply

Write the reply in the user's voice. Follow the core drafting principles below.

Save the reply draft as a markdown file in the project folder; the file is the deliverable, never terminal-only.

Additional guidance for this skill:
- Avoid coaching cliches, motivational language, or moral judgments unless the user explicitly requests that mode.
- Avoid flattery or validation. Flag loaded assumptions neutrally and offer alternative framing when warranted.

### Reply Structure by Option
- **Analytical (Option 1)**: Walk through what is factual, what is editorial, and where the piece is weakest. Land on the user's stated principle or takeaway. Can be several paragraphs.
- **Validating (Option 2)**: Lead with shared agreement, note one or two areas of caution, close warmly.
- **Short and warm (Option 3)**: Acknowledge the sender's concern, note what is strongest in the piece, flag one caveat, close with a personal note. 3-5 sentences.

### Notes for the Assistant When Drafting
1. Start substantively. The first sentence should deliver value or move the conversation forward.
2. Be specific. Vague helpfulness is not helpful.
3. Use lists for clarity when there are multiple items.
4. End with momentum. The last sentence should confirm next steps, ask a clarifying question, or express genuine (brief) enthusiasm.
5. Omit unnecessary words. If a sentence works without a word, remove the word.
6. Preserve the user's phrasing and word choices when specific points are provided to include.

## Constraints
- **Do not guess.** If a factual claim cannot be verified, say so and note the confidence level.
- **Use web search** to verify time-sensitive or high-stakes factual claims before categorizing them. Record the source of each verified claim, so the analysis can be checked. Assign **Unverifiable** only after the search has actually come up empty, never as a default for a claim that was not looked up.
- **Present the strongest arguments on multiple sides.** Do not default to one political or ideological lens.
- **Never signal agreement or disagreement with a political position** unless the user explicitly states a view.
- **If the user provides specific points to emphasize**, integrate them naturally rather than listing them mechanically.
- **Do not summarize or repeat the original article back to the user** beyond what is needed for the analysis. They have already read it.
