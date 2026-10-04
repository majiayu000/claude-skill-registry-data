---
name: article-audit
description: Audit a complete article against all criteria — voice markers, SEO/GEO requirements, section architecture, source citation quality, pillar alignment, and CTA. Returns per-criterion scores, specific failing passages, and a prioritized revision list. Use before publishing any article, or to diagnose why an article isn't performing.
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Audit this article: $ARGUMENTS

$ARGUMENTS should be either: (a) a file path to an existing article markdown file, or (b) the article content pasted directly. If neither, ask the user to provide the article.

---

## What This Audit Covers

Six audit dimensions, each scored independently:

1. **Voice Fidelity** -- Author's voice markers scored 0.0-1.0 each + failure mode check
2. **Section Architecture** -- mandatory sections present, word counts in range, order correct
3. **SEO Requirements** -- keyword placement, H structure, meta fields, URL slug, internal links
4. **GEO Requirements** -- definition anchor quality, entity disambiguation, citation quality, FAQ presence
5. **Source Citation** -- passages grounded in the author's actual source material, citations formatted correctly, no invented quotes
6. **Pillar & Funnel Alignment** -- pillar assignment correct, CTA present and linked, no orphan content

---

## Dimension 1: Voice Fidelity

Read {{VOICE_GUIDE}} for the author's defined voice markers, weights, and targets. Score each marker 0.0-1.0 based on presence, density, and authenticity.

For each voice marker defined in the guide:
- Score it against the defined target threshold
- Quote the specific passages that carry (or fail to carry) this marker
- Note the weight assigned to this marker

### Overall Voice Coherence Score

Calculate the weighted average using the weights from {{VOICE_GUIDE}}.

**Target: defined in {{VOICE_GUIDE}} (typically >=0.75).** Below the target, the article should not publish before revision.

### Failure Mode Check

Read the failure modes from {{VOICE_GUIDE}} and flag any that appear. Common failure modes include:

- [ ] **Off-brand vocabulary** -- words or phrases specifically flagged in the voice guide
- [ ] **Wrong register** -- tone doesn't match the author's characteristic voice
- [ ] **Rushing to practice** -- application appears before depth and meaning are established (before the 60% mark)
- [ ] **Missing first-person narrative** -- no "I've seen...", "Let me walk you through...", "My experience..."
- [ ] **Generic motivational language** -- "You've got this!" "Believe in yourself!" "Start your journey today!"
- [ ] **Structural anti-patterns** -- any rhetorical patterns flagged as prohibited in the voice guide

---

## Dimension 2: Section Architecture

Check that all mandatory sections are present, in the correct order, and within word count range.

| Section | Required | Word Count Target | Check |
|---------|----------|-------------------|-------|
| Opening hook (no heading) | Yes | 150-250 | Present? Starts with question/reframe (not a quote)? Keyword in first 100 words? |
| **H2: What Is [Term]?** | Yes | 200-350 | Present? Definitional? GEO-ready? |
| **H2: Stakes/Problem** | Yes | 250-400 | Present? Diagnosis + historical parallel? |
| **H2: Core Teaching x 2-4** | Yes | 600-1,200 total | Present? Multiple H3s? H2s as questions? Sources cited? |
| **H2: Common Misunderstandings** | Yes | 300-500 | Present? 2-3 H3s? Dissolution not just negation? |
| **H2: Foundational Evidence** | Yes (may merge) | 200-350 | Evidence woven? Not used as proof-text? |
| **H2: What This Means in Practice** | Yes | 250-400 | Present? Prose not steps? Application earned? |
| **H2: How This Connects** | Tier 1 required, others optional | 150-250 | Present (Tier 1)? Internal links? |
| CTA / Formation Invitation | Yes | 100-200 | Present? One CTA? Strong close? |
| FAQ | Optional but recommended | 200-400 | Present? 3-5 Q&As? Complete standalone answers? |

**Total word count check:**
- Tier 1: 3,500-4,500 -- flag if outside range
- Tier 2: 2,200-3,200 -- flag if outside range
- Tier 3: 1,500-2,200 -- flag if outside range

**Order check:** Sections must follow the sequence above. Application (Section 7) must come after Core Teaching (Section 4). Flag if not.

---

## Dimension 3: SEO Requirements

Score pass/fail for each item:

**H Structure:**
- [ ] Primary keyword in H1 (article title)
- [ ] Primary keyword appears within first 100 words of body
- [ ] Primary keyword in at least one H2
- [ ] H2s mirror real search queries ("What Is X?", "How Does X Work?", "Why Does X Matter?")
- [ ] H3s are genuine sub-points, not just continuations

**Keyword distribution:**
- [ ] Primary keyword: natural density, not stuffed (flag if appears more than once every 100 words)
- [ ] 3-5 semantic variants present in body
- [ ] GEO disambiguation phrase present: "{{AUTHOR_NAME}} [concept]" or "{{AUTHOR_NAME}} developed..."

**Meta fields (check if present in frontmatter):**
- [ ] `meta_title` -- 50-60 characters, leads with keyword, ends with `-- {{AUTHOR_NAME}}`
- [ ] `meta_description` -- 140-160 characters, includes keyword, contains question or tension
- [ ] `slug` -- short, keyword-anchored, lowercase, hyphens, no stop words

**Internal links:**
- [ ] Minimum 3 internal links (to related articles, pathways, or courses)
- [ ] Maximum 8 internal links
- [ ] Anchor text is natural and descriptive (not "click here" or "read more")

---

## Dimension 4: GEO Requirements

Score pass/fail:

**Definition Anchor (Section 2):**
- [ ] Clean opening definition sentence (20-30 words, complete, crisp)
- [ ] Self-contained -- a reader can understand the concept from this section alone
- [ ] Entity disambiguation: attributes the concept to {{AUTHOR_NAME}} explicitly
- [ ] Does not open with "According to {{AUTHOR_NAME}}..." (too academic) -- embed the attribution naturally

**Factual specificity:**
- [ ] Historical examples include specific numbers, dates, or locations (not vague)
- [ ] Framework components are named precisely (not generalized)

**First-person authoritative statements:**
- [ ] At least 2 first-person passages (increases GEO citation rate)
- [ ] Statements are grounded in known biographical facts or source material (not invented)

**Citation quality:**
- [ ] Sources cited in correct format: `*Source Title* -- [Section Reference]`
- [ ] No invented quotes or paraphrases without attribution
- [ ] Direct quotes are verbatim from source material (not close paraphrases presented as quotes)

**FAQ:**
- [ ] FAQ section present (optional but recommended -- flag if absent)
- [ ] Each Q&A is complete and self-contained
- [ ] Questions reflect real search phrasing

---

## Dimension 5: Source Citation

- [ ] Article draws on the author's actual source material, not general knowledge alone
- [ ] At minimum 1-2 direct citations from {{CONTENT_CORPUS}} (blockquotes or close-referenced paraphrases)
- [ ] Citations use the correct format
- [ ] No invented quotes (flag any author-attributed statement not verifiable in source material)
- [ ] Sources cited are appropriate to the pillar

If the article cites the author without a source reference, flag each instance for verification.

---

## Dimension 6: Pillar and Funnel Alignment

- [ ] Article is clearly assigned to one of the defined pillars
- [ ] Topic fits the pillar assignment (not cross-pillar confusion)
- [ ] One primary CTA present, linking to a pathway or course
- [ ] CTA is appropriate to the pillar (not a random cross-sell)
- [ ] No orphan content -- the article connects to something deeper in the funnel
- [ ] If Tier 2/3: link to the Tier 1 pillar page is present

---

## Audit Output Format

Return the audit as:

---

# Article Audit: [Article Title or File Path]

**Overall Readiness:** [PUBLISH READY / NEEDS REVISION / MAJOR REVISION REQUIRED]
**Word Count:** [actual] / [target range]
**Tier:** [1/2/3] -- **Pillar:** [name]

---

## Voice Fidelity Scores

| Marker | Score | Target | Status |
|--------|-------|--------|--------|
| [Voice Marker 1] | 0.X | [target] | PASS / FAIL |
| [Voice Marker 2] | 0.X | [target] | PASS / FAIL |
| [etc.] | | | |
| **Overall Coherence** | **0.X** | **[target]** | **PASS / FAIL** |

**Failure modes found:**
- [List specific failures with quoted passages]

---

## Section Architecture

| Section | Present | Word Count | Status | Notes |
|---------|---------|------------|--------|-------|
| Opening hook | Y/N | [N] | PASS/FAIL | |
| What Is [Term]? | Y/N | [N] | PASS/FAIL | |
| [etc.] | | | | |

---

## SEO Score: [X]/[total checks] passing

**Failures:**
- [specific items failing, with what's needed to fix]

---

## GEO Score: [X]/[total checks] passing

**Failures:**
- [specific items failing]

---

## Source Citation: [GROUNDED / WEAK / UNVERIFIED]

**Issues:**
- [specific unattributed or suspect passages]

---

## Pillar & Funnel: [ALIGNED / MISALIGNED]

**Issues:**
- [specific alignment problems]

---

## Priority Revision List

Rank issues by impact (fix these first):

1. **[CRITICAL]** [Issue] -- [What to do to fix it]
2. **[HIGH]** [Issue] -- [Fix]
3. **[MEDIUM]** [Issue] -- [Fix]
4. **[LOW]** [Issue] -- [Fix]

---

## Publish Decision

**[PUBLISH READY]** -- All dimensions pass. Ready to go.

**[NEEDS REVISION]** -- Minor issues. Fix the Priority Revision List items, then publish.

**[MAJOR REVISION REQUIRED]** -- Voice coherence below target, or multiple mandatory sections missing, or source citations unverifiable. Significant rewrite needed before this article should go live.
