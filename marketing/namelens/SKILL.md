---
name: namelens
description: Research and stress-test open-source project names, from collision checks to launch-ready decisions. Use when the user asks to name or rename a project, compare candidate names, screen GitHub or package namespace risk, verify language or mythology claims, or improve SEO/GEO clarity. Perform live web and registry research, separate brand from category descriptor, classify collisions, and return one evidence-backed recommendation.
---

# NameLens

Research and stress-test open-source project names, from collision checks to launch-ready decisions.

NameLens helps builders generate project names, check naming collisions, evaluate GitHub and package namespace risk, and choose names that are memorable, searchable, and easy to spread.

Treat naming as four connected problems:

1. **Positioning** — what promise, outcome, and personality should the name signal?
2. **Transmission** — can people read, say, hear, spell, type, and remember it?
3. **Search ownership** — can users and machines distinguish and rediscover it?
4. **Namespace fit** — can it work across the repository, command, package, app, domain, and other surfaces that matter?

A clever word without research is only a hypothesis.

## Default behavior

- Respond in the user's language.
- Use **Standard mode** unless the user requests a quick brainstorm or a launch-level clearance pass.
- Extract constraints from the conversation before asking questions. Proceed with labeled assumptions when missing details are not decisive.
- Require live web or browser access for current collision, registry, domain, handle, language-usage, and preliminary trademark checks. Without live access, generate candidates but mark all such findings **UNVERIFIED**.
- Browse before calling a name clear, unused, available, safe, ownable, or low-collision.
- Prefer official registries, official product pages, source repositories, reputable dictionaries, and official trademark databases.
- Cite material collision and linguistic evidence and state the research date.
- Separate the **distinctive brand** from the **category descriptor**. Let the descriptor carry explicit keywords.
- Reject a beautiful name that fails a critical namespace or creates a serious same-category collision.
- Never invent or exaggerate a foreign-language etymology.
- Never present preliminary research as legal or trademark clearance.
- End with one recommended winner, not an unranked cloud of options.

## Operating checkpoints

- **CHECKPOINT: Scope escalation.** Before switching from Quick or Standard mode to Deep mode, state the added checks, added uncertainty, and why the stakes justify deeper research.
- **CHECKPOINT: Critical conflict.** If a top candidate has a red same-category, registry, app-store, domain, or trademark signal, pause the recommendation and explain the cost before keeping it in contention.
- **STOP: Clearance language.** If the user asks whether a name is available, safe, trademark-safe, or legally clear, do not answer yes. Return only preliminary research status and remaining official checks.
- **STOP: Missing live access.** If live web, registry, or official database access is unavailable, do not classify any candidate as Green. Mark collision, namespace, domain, handle, trademark, and language-usage findings as **UNVERIFIED**.

## Modes

### Quick

Use for early exploration.

- Create 12–18 candidates across at least four naming lanes.
- Research the general web, GitHub, and one critical registry or store.
- Return a top 3, an avoid list, and remaining checks.

### Standard

Use by default.

- Create 30–50 raw candidates and research 12–20 serious finalists.
- Use at least five genuinely different naming lanes.
- Check exact and category searches, GitHub, critical registries, realistic variants, pronunciation, and target-language meaning.
- Return a ranked top 5, one winner, two backups, and launch-ready identity fields.

### Deep

Use before a public launch, commercial campaign, fundraising, or expensive rename.

- Create 50–100 raw candidates and research 20–30 finalists.
- Add phonetic variants, domains, social handles, app stores, local-market searches, and preliminary trademark screening.
- Return an evidence log, risk register, top 5, winner, backup, and reservation checklist.
- State that professional trademark clearance is required for commercial launch, fundraising, paid advertising, app-store release, or any name with a relevant trademark signal.

## Output contract by mode

Use this table as the minimum report contract. Add detail only when it changes the decision.

| Mode | Required sections | Required checks | Required ending |
|---|---|---|---|
| Quick | decision, brief assumptions, top 3, avoid list, remaining checks | web, GitHub, one critical registry or store | one provisional winner plus unverified checks |
| Standard | decision, brief, search scope/date, naming lanes, candidate matrix, finalists, rejected names, launch identity | exact/category search, GitHub, critical registries, variants, pronunciation, target-language meaning | one winner, two backups, reservation checklist |
| Deep | decision, brief, search scope/date, evidence log, risk register, candidate matrix, top 5, rejected names, launch identity | Standard checks plus phonetic variants, domains, handles, app stores, local-market search, preliminary trademark databases | one winner, backup, reservation checklist, professional-clearance note |

If any required check cannot run, keep the section and mark the affected fields **UNVERIFIED** rather than deleting the section.

## Workflow

### 1. Build the naming brief

Extract:

- project type: CLI, library, package, app, API, SaaS, agent, protocol, content brand, or other
- core job and user outcome
- primary audience and technical sophistication
- target markets and languages
- launch surfaces that actually matter
- desired tone and associations
- naming preferences and forbidden styles
- length, character, pronunciation, or suffix constraints
- likely future scope
- risk tolerance: experimental open source versus commercial brand

Summarize the brief in a compact block and label assumptions.

### 2. Identify critical naming surfaces

Do not check every platform mechanically. Rank the surfaces by consequence.

Typical priorities:

- **CLI OSS:** command, GitHub repository, package/module path, Homebrew or installer ecosystem, exact web query
- **Library:** package registry, import/module name, repository, documentation query
- **Consumer app:** spoken recall, app stores, domain, social handles, target-language safety, trademark risk
- **B2B/SaaS:** credibility, category collision, domain, trademark risk, international extensibility
- **Content brand:** memorability, social handles, domain, topic-query ambiguity, pronunciation

A missing `.com` may be acceptable for an open-source CLI. An occupied exact package name may not be.

### 3. Build semantic territories

Map the project through four layers:

1. **Function:** search, route, compare, compress, trace, explain
2. **Outcome:** clarity, speed, proof, focus, reach, confidence
3. **Metaphor:** beacon, thread, lens, compass, key, bridge, loom
4. **Personality:** sharp, calm, trusted, curious, local, bold

Also list semantic traps: generic category nouns, misleading claims, narrow provider references, saturated startup suffixes, and names that imply unsupported features.

### 4. Generate candidates across independent lanes

Use at least five lanes so the output is not twenty spellings of one root:

- clear compound
- suggestive real word
- pronounceable coined construction
- verified cross-language root
- concrete object, craft, process, role, or natural metaphor
- terse contrarian technical form
- myth or literature only when the mapping is real and saturation is acceptable

Read `references/naming-patterns.md` when generating linguistic, coined, or mythic names.

Generate broadly first. Do not research every raw idea; prune obvious failures before the expensive checks.

### 5. Prune with transmission and platform tests

Before live research, remove names that fail basic use:

- hard to pronounce after one reading
- hard to spell after hearing once
- awkward or error-prone as a command
- dependent on capitalization or punctuation
- too generic to become a distinct entity
- visually confusable with a strong neighbor
- trapped in one initial feature or provider
- based on a false or unverifiable linguistic story
- incompatible with a critical registry's naming rules or normalization

Treat character counts as heuristics, not laws. Short is useful only when the name remains distinctive and pronounceable.

### 6. Research live collisions

Read `references/collision-research.md` before checking finalists.

For each serious candidate, inspect the relevant subset:

1. exact web query
2. brand plus category query
3. brand plus technical form such as CLI, app, API, SDK, agent, or library
4. GitHub exact and same-category results
5. critical package registry, app store, or distribution surface
6. joined, spaced, hyphenated, plural, and likely misspelled forms
7. phonetic neighbors when word of mouth matters
8. original script and romanization for cross-language candidates
9. domain and social handles only when launch-critical
10. official trademark databases for commercial or high-risk work

Classify what you find, not merely whether a string appears:

- active same-category product
- inactive or weak same-category project
- unrelated exact entity
- dominant person, place, medicine, protocol, or company
- critical namespace collision
- close visual or spoken neighbor

Stop investing in a candidate once a critical red collision makes it non-viable, unless it is useful as a comparison.

### 7. Evaluate without fake precision

Use evidence-backed ordinal judgments rather than decorative decimal scores.

Rate each researched candidate:

- semantic fit: Strong / Medium / Weak
- memorability and transmission: Strong / Medium / Weak
- search ownership: Strong / Medium / Weak / Unknown
- critical namespace fit: Clear / Workaround / Blocked / Unverified
- cross-language safety: Clear / Concern / Unverified
- extensibility: Strong / Medium / Weak
- collision risk: Green / Yellow / Red / Unverified
- naming difficulty: Low / Medium / High

Interpret collision risk:

- **Green:** no obvious active same-category exact collision found in the checks performed; critical checked namespaces appear workable
- **Yellow:** unrelated exact matches, weak projects, close spellings, or a non-critical occupied surface
- **Red:** active same-category product, blocked critical namespace, dominant conflicting entity, serious language problem, or strong legal concern
- **Unverified:** a required check could not be completed

A red candidate cannot win unless the user explicitly accepts the conflict and the report explains the cost.

### 8. Perform an adversarial review

Try to break every top candidate:

- Can someone pronounce it after reading it once?
- Can someone spell it after hearing it once?
- Does autocorrect or speech recognition distort it?
- Is it awkward in a shell command, import, URL, or conversation?
- Does it resemble an established product, person, place, medicine, or protocol?
- Does it create an embarrassing or negative association in a target language?
- Does it lock the project to one source, model, platform, or feature?
- Can search engines distinguish it without excessive qualifiers?
- Would the maintainer still be comfortable saying it publicly in three years?

Downgrade names that survive only through explanation.

### 9. Design the SEO/GEO identity system

Do not stuff all category keywords into the brand. Use:

```text
[Distinctive brand] — [clear category descriptor for audience and outcome]
```

Evaluate:

- entity distinctiveness
- exact-query ambiguity
- stable spelling and capitalization
- compatibility with a clear category descriptor
- likely `brand + category` searches
- consistency across repository, package metadata, README, docs, and website

Treat GEO as entity clarity and citation readiness, not a ranking trick. Favor one stable definition, explicit capabilities, visible evidence, structured documentation, and genuinely useful content. Never promise SEO or generative-engine ranking.

### 10. Deliver a decision, not just ideas

Read `references/output-template.md` before the final response.

At minimum include:

1. decisive recommendation
2. compact naming brief and assumptions
3. search scope and date
4. candidate matrix with origin, pronunciation, ordinal evaluation, collision status, difficulty, and main risk
5. top 3–5 with clear trade-offs
6. rejected or dangerous names and why
7. launch-ready identity fields
8. remaining verification and reservation steps

For the winner provide:

- display name
- pronunciation
- repository slug
- CLI command or package name when applicable
- category descriptor
- one-sentence entity definition
- tagline
- GitHub About or store description
- SEO title pattern
- recommended topics or keywords
- collision wording and unresolved checks

Use this cautious wording:

> In the searches performed on YYYY-MM-DD, no obvious active same-category exact collision was found.

Do not write:

> The name is available or legally safe.

## Foreign-language and mythology rules

- Verify original script, dictionary form, literal meaning, pronunciation, romanization, and modern usage.
- Distinguish a direct word from an inflected form, clipping, or root-inspired invention.
- Search both original script and romanization.
- Check slang, surnames, places, medicines, companies, and products in target markets.
- Label modified forms as “inspired by” rather than mistranslating them.
- Penalize famous mythological names already saturated in software.
- Prefer a less famous but meaningful motif over Atlas, Apollo, Athena, Hermes, Loki, Odin, Thor, or Prometheus merely because it sounds grand.

## Evidence discipline

For each finalist preserve:

- query, registry, or database checked
- date checked
- exact versus near match
- category relevance
- activity signal when visible
- confidence: High / Medium / Low

If live browsing is unavailable, proceed with ideation but label all collision, namespace, domain, handle, trademark, and language-usage findings **UNVERIFIED**.

## Failure handling

| Trigger | Action | Required output label |
|---|---|---|
| Live web or registry checks fail | Continue with candidate generation only; do not claim collision safety | `UNVERIFIED` |
| Official dictionary or native-language evidence is missing | Remove the etymology claim or label the name as invented/root-inspired | `language_unverified` |
| A critical namespace is blocked | Reject the candidate unless the user explicitly accepts a workaround | `Blocked` |
| A strong same-category collision appears | Stop researching that candidate as a winner and use it only as contrast | `Red` |
| User wants a quick brainstorm but asks for availability | Use Quick mode, check only the most critical surface, and state the remaining checks | `partial_screen` |
| User asks for legal, trademark, or investment-grade clearance | Provide preliminary signals only and direct them to official registers or professional review | `not_legal_clearance` |

## Do-not-do blacklist

- Do not output a list of names without a final recommendation.
- Do not treat an unsearched name as available, safe, clear, ownable, or low-risk.
- Do not use decorative decimal scores or unverifiable ranking math.
- Do not invent Latin, Japanese, Greek, mythological, or minority-language meanings.
- Do not hide a blocked package, command, repository, domain, app listing, or trademark signal.
- Do not let the brand carry every SEO keyword; put explicit category terms in the descriptor.
- Do not recommend a name that depends on capitalization, punctuation, or a false pronunciation to work.
- Do not continue polishing a red candidate unless the user explicitly chooses the conflict.

## Reference loading

- Read `references/naming-patterns.md` for candidate construction, linguistic roots, phonetic tests, and mythology safeguards.
- Read `references/collision-research.md` for search order, platform priorities, risk classification, and evidence standards.
- Read `references/output-template.md` immediately before producing a Standard or Deep report.
- Read `examples/search-cli-retrospective.md` when the task resembles an open-source search/CLI project or the user asks for a process retrospective.
