---
name: docs-discoverability-audit
description: Reviews repository documentation and documentation websites for human and search discoverability. Use when the user asks why documentation is difficult to find, navigate, understand, or index, or wants an audit of README entry points, documentation hierarchy, internal links, page titles, headings, URLs, duplicate pages, sitemaps, canonical URLs, or technical documentation SEO.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: docs-seo
  task_type: review
  audience: technical-documentation-maintainers
  tags:
    - documentation
    - seo
    - discoverability
    - information-architecture
    - internal-linking
    - technical-seo
  status: draft
  side_effects: none
---

# Documentation Discoverability Audit

## Purpose

Audit technical documentation as a connected information system rather than reviewing isolated pages.

The skill determines whether developers, evaluators, contributors, and search engines can:

- discover the documentation
- identify the correct page
- understand what each page covers
- move between related topics
- distinguish current guidance from outdated or duplicate content
- reach installation, usage, API, examples, troubleshooting, and contribution information without unnecessary searching

The skill combines documentation information architecture, repository navigation, content findability, internal linking, and technical SEO checks.

It is review-first. It should not rewrite documentation or modify files unless the user explicitly requests implementation.

## When to use this skill

Use this skill when:

- The user asks for a documentation SEO audit.
- A repository has documentation, but users struggle to find the correct page.
- The README and documentation website do not provide clear entry points.
- Documentation pages appear disconnected, duplicated, or inconsistently named.
- The user wants to improve documentation navigation or internal linking.
- The user wants to check titles, headings, URLs, canonical links, sitemaps, or indexability.
- A package or open-source project needs better search and GitHub discoverability.
- A documentation migration may have introduced broken links, redirects, or duplicate URLs.
- The user wants to know which documentation pages should be created, merged, renamed, redirected, or removed.
- The repository contains generated API documentation that must connect cleanly with manually written guides.

Do not use this skill when:

- The user only wants individual meta titles or descriptions written.
- The user only wants prose edited for grammar or tone.
- The task is limited to generating a sitemap or robots file.
- The user wants a full website content strategy unrelated to technical documentation.
- The user wants implementation without first understanding the existing documentation structure.
- A more specific skill already covers the request, such as a README-only review or demo-page enhancement.

## Inputs to inspect

Inspect the smallest relevant set of available files.

### Repository entry points

- `README.md`
- package or workspace README files
- repository description and topics, if provided
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `LICENSE`
- `package.json`
- package manager workspace configuration

### Documentation content

- `docs/`
- `documentation/`
- `guides/`
- `examples/`
- `demo/`
- `website/`
- `content/`
- `pages/`
- generated API reference directories
- versioned documentation directories
- migration guides
- troubleshooting pages
- FAQ pages

### Navigation and routing

- sidebar configuration
- navigation configuration
- route definitions
- content collections
- redirects
- rewrites
- breadcrumb configuration
- previous and next page configuration
- documentation search configuration

Examples may include:

- `astro.config.*`
- `docusaurus.config.*`
- `sidebars.*`
- `.vitepress/config.*`
- `mkdocs.yml`
- `next.config.*`
- framework route files
- CMS schema or navigation files

### Search and indexing files

- `sitemap.xml`
- sitemap generators
- `robots.txt`
- canonical URL configuration
- page-level `noindex` rules
- redirect configuration
- structured data, when present
- `llms.txt`, when present
- generated HTML, when available
- deployment configuration that affects URLs or status codes

### Optional external evidence

Use external data only when it is available or explicitly requested:

- analytics landing-page reports
- internal site-search queries
- Search Console exports
- crawl reports
- broken-link reports
- user feedback
- issue tracker reports
- live deployed documentation

Do not claim that a page is indexed, ranking, or receiving traffic without external evidence.

## Audit principles

Apply these principles throughout the review.

### One clear owner per topic

Each important topic should have one primary page.

Supporting pages may link to it, but multiple pages should not compete to be the authoritative explanation of the same subject.

### Repository and website navigation must agree

README links, website navigation, package metadata, examples, and API documentation should point toward the same current documentation structure.

### Important pages must have entry points

A technically correct page is still difficult to discover when it is absent from the README, navigation, relevant guides, examples, and related pages.

### Page purpose must be immediately clear

A page title, primary heading, introduction, and URL should consistently communicate:

- what the page covers
- who it is for
- when it should be used
- what prerequisite knowledge is expected

### Search optimization must remain useful

Do not recommend:

- keyword stuffing
- repetitive headings written only for search engines
- duplicate pages targeting minor keyword variations
- misleading titles
- unsupported structured data
- artificial word-count expansion
- large volumes of low-value generated documentation

Useful documentation is the primary SEO strategy.

## Workflow

### 1. Establish the documentation context

Determine:

- what the project or package does
- who uses it
- whether it is a library, application, API, plugin, framework, CLI, or service
- where the documentation is published
- whether documentation is repository-only or has a dedicated website
- whether multiple versions are maintained
- whether generated API documentation exists

Identify likely user groups, such as:

- first-time evaluators
- developers installing the package
- developers implementing a feature
- developers troubleshooting a problem
- maintainers and contributors
- recruiters or technical reviewers

Do not invent personas that are unsupported by the repository.

### 2. Identify core documentation intents

Build a list of the questions the documentation must answer.

Common intents include:

- What does this project do?
- Is it appropriate for my use case?
- How do I install it?
- What is the smallest working example?
- How do I configure it?
- What public API is available?
- How do individual features work?
- How do I integrate it with another tool?
- What accessibility or browser support does it provide?
- How do I troubleshoot common failures?
- How do I migrate between versions?
- How do I contribute?
- Where can I see a live example?

Use repository evidence to add or remove intents.

### 3. Inventory documentation entry points

Record every major entry point, including:

- repository README
- package registry links
- documentation homepage
- primary navigation
- sidebar navigation
- footer documentation links
- demo index
- example pages
- API reference
- contribution documentation
- issue templates
- package metadata links

For each entry point, determine:

- what audience it serves
- what destination it promotes
- whether the destination is current
- whether the link label is descriptive
- whether important documentation is missing
- whether multiple entry points disagree

### 4. Build a documentation map

Create a concise hierarchy of the existing documentation.

Group pages into functional areas such as:

- overview
- installation
- getting started
- concepts
- guides
- configuration
- API reference
- examples
- integrations
- accessibility
- troubleshooting
- migration
- contribution

Mark pages that are:

- orphaned
- duplicated
- misplaced
- overly broad
- too fragmented
- missing from navigation
- accessible only through search
- reachable only from another deep page
- outdated or version-ambiguous

Do not assume that every repository needs every documentation category.

### 5. Review README-to-documentation flow

Check whether the README helps a visitor move from evaluation to implementation.

Review:

- project summary
- primary use case
- feature summary
- installation path
- minimal example
- documentation links
- demo links
- API links
- support and troubleshooting links
- contribution links

Identify where the README:

- duplicates long documentation unnecessarily
- provides no clear next step
- links to a generic homepage instead of the relevant guide
- uses vague labels such as “Learn more”
- points to obsolete pages
- overwhelms users with too many equal-priority links

The README does not need to contain all documentation. It must route users to it effectively.

### 6. Review page-level findability

For each important page, inspect:

- page title
- primary heading
- URL or slug
- introductory paragraph
- heading hierarchy
- table of contents
- anchor identifiers
- link text
- terminology
- code example labels
- previous and next links
- related-page links

Check whether:

- the title and H1 describe the same topic
- the page answers its primary question near the beginning
- headings use terms users are likely to recognize
- URLs remain understandable outside the navigation context
- anchors are stable and meaningful
- links describe their destination
- abbreviations are introduced before being used heavily
- competing terminology is used consistently

Do not force exact keyword repetition when natural language is clearer.

### 7. Review navigation and internal links

Determine whether users can move through related documentation without returning to the homepage.

Check for:

- links from overview pages to detailed guides
- links from guides to relevant API reference
- links from API reference to usage examples
- links from error messages or troubleshooting pages to solutions
- links between related concepts
- links from examples back to explanatory documentation
- breadcrumb accuracy
- sidebar hierarchy
- current-page indication
- previous and next page logic
- broken fragment links
- links to renamed or removed pages

Flag important pages with too few relevant inbound links.

Do not recommend adding unrelated links merely to increase link counts.

### 8. Review technical indexability

When relevant files or a live build are available, inspect:

- whether documentation pages produce meaningful HTML
- page status codes
- canonical URL handling
- sitemap coverage
- robots directives
- page-level `noindex`
- duplicate URL variants
- trailing-slash consistency
- uppercase and lowercase URL variants
- redirect chains
- redirects from moved documentation
- versioned documentation URLs
- pagination or filtered-page indexing
- JavaScript-only content that may not appear in generated HTML

Classify findings carefully:

- Confirmed: directly supported by files, generated output, or live response.
- Likely: strongly suggested by configuration but not tested on a deployed site.
- Unknown: requires deployment, crawl, or search-platform data.

Never report an indexing problem as confirmed solely because a page performs poorly in a local content review.

### 9. Review duplication and topic ownership

Identify:

- multiple getting-started guides
- installation instructions that disagree
- API guidance duplicated across README and docs
- versioned pages without clear version labels
- examples that contain undocumented behavior
- old migration guides appearing as current documentation
- copied pages with only minor wording differences
- duplicate URLs caused by routing or deployment configuration

For each duplicate set, recommend one of:

- keep one canonical page
- merge pages
- clarify separate intents
- redirect an obsolete page
- add a version label
- remove the page from navigation
- preserve the page but mark it as historical

Do not recommend deletion when the page may still serve migration, compatibility, or archival needs.

### 10. Evaluate content usefulness

Check whether high-value documentation includes the information necessary to complete the task.

Depending on the page, this may include:

- prerequisites
- installation commands
- imports
- minimal markup or configuration
- expected output
- option descriptions
- defaults
- lifecycle behavior
- accessibility behavior
- error states
- cleanup or destruction behavior
- browser or runtime constraints
- complete examples
- troubleshooting guidance
- links to deeper reference material

Distinguish between:

- a discoverability problem
- a missing-content problem
- an unclear-writing problem
- an implementation problem
- a technical indexing problem

Do not group all documentation weaknesses under “SEO.”

### 11. Prioritize findings

Use these priorities:

- **Blocker** — prevents access, indexing, or correct use of essential documentation.
- **High** — significantly obstructs a major user journey or creates conflicting guidance.
- **Medium** — causes avoidable confusion or weakens navigation and topic clarity.
- **Low** — useful polish with limited effect on task completion.

Prioritize changes that improve multiple journeys, such as:

- establishing one authoritative getting-started guide
- repairing the primary README documentation path
- adding missing redirects
- connecting guides, examples, and API reference
- removing accidental `noindex`
- clarifying version ownership

Avoid arbitrary numerical SEO scores unless the user explicitly requests a defined scoring model.

### 12. Recommend the smallest coherent change set

Group recommendations into:

1. Critical corrections
2. Navigation and information architecture
3. Page-level improvements
4. Technical SEO corrections
5. Optional future enhancements

For each recommendation, specify:

- affected file or route
- current problem
- proposed change
- expected user benefit
- validation method

Do not propose a full documentation rewrite when targeted restructuring will solve the problem.

### 13. Apply changes only when requested

If the user asks for implementation:

- make the smallest safe edits first
- preserve valid existing URLs where possible
- add redirects before renaming published routes
- avoid breaking external links
- update navigation and internal references together
- regenerate derived files only through the project’s existing workflow
- do not deploy or modify remote services without explicit approval

If implementation was not requested, return recommendations only.

### 14. Validate the result

Validation may include:

- confirming README links resolve
- checking navigation destinations
- checking local route generation
- checking heading and title uniqueness
- checking canonical configuration
- checking sitemap inclusion
- checking robots directives
- checking redirect destinations
- checking important page inbound links
- checking fragment identifiers
- running an existing documentation build
- running an existing link checker

Do not install new tools or dependencies without approval.

## Output format

Return the review using this structure:

```md
## Summary

State:

- overall discoverability condition
- strongest part of the documentation
- most important weakness
- recommended first action

## Documentation map

| Area | Primary page or entry point | Audience | Status | Notes |
|---|---|---|---|---|

## Findings

| Priority | Area | Finding | Evidence | Impact | Recommendation |
|---|---|---|---|---|---|

## Orphaned, duplicate, or unclear pages

| Page | Classification | Problem | Recommended action |
|---|---|---|---|

## Recommended change plan

### 1. Critical corrections

- ...

### 2. Navigation and information architecture

- ...

### 3. Page-level improvements

- ...

### 4. Technical SEO

- ...

### 5. Optional enhancements

- ...

## Files to create or edit

| File or route | Proposed change | Reason |
|---|---|---|

## Validation

- [ ] Primary README documentation links resolve.
- [ ] Important documentation pages have clear entry points.
- [ ] Titles, H1 headings, and URLs communicate page purpose.
- [ ] Navigation and internal links use current destinations.
- [ ] Duplicate topics have clear ownership.
- [ ] Canonical, sitemap, robots, and redirect behavior were checked where evidence was available.
- [ ] Confirmed findings are separated from assumptions requiring live verification.
```

If files were changed, replace `Files to create or edit` with:

```md
## Changes made

| File | Change | Validation |
|---|---|---|
```

## Quality bar

The task is complete only when:

- The review is based on the actual repository or documentation provided.
- Major documentation audiences and intents are identified.
- Important entry points are mapped.
- Findings cite specific files, routes, headings, links, or configuration.
- Documentation issues are separated from technical SEO issues.
- Confirmed problems are separated from likely or unverified problems.
- Orphaned and duplicate pages are identified when evidence permits.
- Recommendations are ordered by impact.
- Recommendations preserve stable published URLs where practical.
- The review avoids keyword stuffing and speculative search claims.
- The review does not recommend structured data without a valid matching content type.
- The output explains what to change and how to validate it.
- No files or external systems are modified unless the user explicitly requests implementation.

## Edge cases

### Repository-only documentation

When no documentation website exists:

- focus on README navigation
- inspect relative links
- inspect package metadata URLs
- inspect GitHub heading anchors
- review links between package directories in a monorepo
- do not report missing website SEO infrastructure as a defect

### Private or authenticated documentation

For private documentation:

- prioritize navigation, information architecture, terminology, and internal search
- do not recommend public indexing
- treat `noindex` or authentication as intentional unless evidence suggests otherwise

### Versioned documentation

For multiple versions:

- identify the default version
- check version labels
- check canonical behavior
- check links between versions
- preserve historical documentation needed for maintenance
- avoid redirecting all old pages blindly to the newest version

### Generated API documentation

For generated reference pages:

- inspect the generator configuration
- connect reference pages to conceptual guides
- avoid manually editing generated output
- recommend changes at the source or generator level

### Single-page documentation sites

For client-rendered documentation:

- inspect whether meaningful content exists in generated HTML
- distinguish client-side navigation from indexability
- verify deployed behavior before making definitive indexing claims

### Monorepos

For monorepos:

- identify package-level and root-level documentation responsibilities
- avoid duplicating the same installation and usage guidance across every package
- ensure root navigation helps users reach package-specific documentation

### Multilingual documentation

For multilingual sites:

- inspect language navigation
- check whether translated pages represent equivalent topics
- identify missing or stale translations
- do not assume automatic translation is appropriate
- verify language-specific canonical and alternate configuration only when available

### No live deployment access

When only repository files are available:

- report configuration findings
- identify what must be verified after deployment
- do not claim actual search-engine indexing, ranking, or HTTP behavior

## Related skills

- `demo-index-docs-enhancer`
- `repo-public-profile-polish`
