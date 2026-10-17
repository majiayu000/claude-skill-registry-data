---
name: repo-public-profile-polish
description: Reviews a public GitHub repository’s profile and landing-page presentation across its README, repository description, topics, homepage and demo links, screenshots, social preview, and visible trust signals. Use when the user asks to polish a repository profile, improve its first impression, make a project recruiter- or contributor-friendly, or audit how a repository appears to new visitors.
license: MIT
compatibility: Portable Agent Skill. Requires repository file access. Live repository metadata, public pages, screenshots, and link validation require network access.
metadata:
  category: repo-readiness
  task_type: review
  audience: open-source-maintainers-and-portfolio-developers
  tags:
    - github
    - readme
    - repository-metadata
    - screenshots
    - demos
    - portfolio
    - first-impression
  status: draft
  side_effects: network
---

# Repository Public Profile Polish

## Purpose

Review how a public repository presents itself to someone encountering it for the first time.

The skill evaluates the repository as a public-facing project page rather than only as a collection of source files. It checks whether visitors can quickly understand:

- what the project is
- what problem it solves
- who it is for
- whether it appears maintained
- where they can see it working
- how they can install or use it
- why they should trust or explore it further

The default workflow is review-only. It may inspect public repository metadata and validate links, but it must not change remote repository settings, push commits, deploy demos, or publish releases unless a separate implementation workflow is explicitly requested.

## When to use this skill

Use this skill when:

- The user asks to improve or polish a GitHub repository page.
- The user wants a repository to make a stronger first impression.
- A project is being prepared for recruiters, hiring managers, contributors, users, or portfolio visitors.
- The repository description, topics, homepage URL, demo link, screenshots, or README may be incomplete or inconsistent.
- The user asks whether a repository looks professional, credible, current, or easy to understand.
- The user wants recommendations for the visible public presentation of an open-source project.
- A technically solid repository is difficult to evaluate without reading its source code.
- The user asks for a “10-second review,” “GitHub profile audit,” “README polish,” or “public repo presentation review.”

Do not use this skill when:

- The main task is source-code quality, architecture, security, or maintainability review.
- The user needs a complete npm publishing audit.
- The task is specifically about GitHub Pages deployment configuration.
- The user needs a deep accessibility audit of the demo itself.
- The request is primarily an SEO or structured-data implementation.
- The repository is private and no repository files, screenshots, or metadata have been provided.
- The user only wants a README written from scratch without reviewing the surrounding repository presentation.

## Review principles

Apply these principles throughout the review.

### Review as an outsider

Start with the repository landing page before deeply inspecting the source.

Record what a visitor can understand without already knowing the project. Do not allow information discovered later in the codebase to hide weaknesses in the public presentation.

### Prefer evidence over taste

Tie findings to observable evidence such as:

- missing or vague repository description
- broken demo URL
- outdated screenshot
- missing installation example
- inconsistent project naming
- excessive badges before the project explanation
- unclear supported environments
- empty or generic topics
- screenshots that do not show the actual product

Avoid vague findings such as “the README could look better.”

### Respect the repository type

Adjust expectations based on whether the repository is:

- an application
- a JavaScript or TypeScript library
- a command-line tool
- a component package
- a design-system package
- a documentation project
- a monorepo
- a proof of concept
- an archived project
- a portfolio case study

A library may need API examples more than a full visual demo. An application usually benefits from screenshots and a working live preview.

### Do not reward decoration without clarity

Badges, banners, screenshots, animations, and logos are useful only when they improve understanding or trust.

Do not recommend visual clutter merely to make the repository appear busy.

## Inputs to inspect

Inspect the repository’s public page and relevant local files.

### Public repository metadata

Inspect when available:

- repository name
- owner or organization
- repository description
- homepage URL
- live demo URL
- repository topics
- social preview image
- visibility
- archived status
- default branch
- license shown by the host
- latest release or package link, when relevant
- public issue and contribution surfaces
- rendered README
- visible repository navigation

When GitHub CLI access is available, metadata may be inspected with a command equivalent to:

```bash
gh repo view --json name,description,homepageUrl,repositoryTopics,licenseInfo,isArchived,defaultBranchRef,url
```

Do not assume that the local README reflects the currently published remote repository.

### Repository files

Inspect relevant files such as:

- `README.md`
- localized or alternative README files
- `package.json`
- `pyproject.toml`
- `Cargo.toml`
- `go.mod`
- `LICENSE`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `docs/`
- `examples/`
- `example/`
- `demo/`
- `demos/`
- `public/`
- `assets/`
- `screenshots/`
- `.github/`
- `.github/workflows/`
- deployment configuration
- package or release configuration

Inspect source code only as needed to verify the project’s purpose, supported features, current UI, or setup instructions.

### Public URLs

Validate relevant URLs when network access is available:

- homepage
- live demo
- documentation
- package registry
- release page
- issue tracker
- contribution guide
- screenshot and media assets
- external examples

Record redirects, authentication requirements, missing pages, mixed project names, broken assets, and stale destinations.

## Workflow

1. Establish the repository context

   Identify:

   - project type
   - intended audience
   - primary use case
   - likely visitor
   - current maturity
   - whether the repository is actively maintained, experimental, archived, or a portfolio project
   - the main action a visitor should take

   Possible primary actions include:

   - open the live demo
   - install the package
   - read the documentation
   - inspect an example
   - evaluate the developer’s work
   - contribute
   - report an issue

   Do not invent positioning that is unsupported by the repository.

2. Perform a cold first-impression scan

   Inspect the public repository landing page before reading the implementation deeply.

   Answer:

   1. What does the project appear to be?
   2. What problem does it solve?
   3. Who appears to be its intended user?
   4. Is there an obvious live demo or usage example?
   5. Does the project look current and maintained?
   6. Is the next action obvious?
   7. What creates doubt or friction?

   Write a short “10-second impression” using only information visible near the top of the repository page.

   If the project cannot be understood quickly, identify exactly what information is missing or buried.

3. Review repository metadata

   Check the repository’s visible metadata.

   Repository name

   Verify that the name:

   - is readable
   - matches the product or package name
   - is used consistently in the README and package metadata
   - avoids unexplained abbreviations
   - does not imply functionality the project does not provide

   Do not recommend renaming an established package without acknowledging compatibility and discoverability costs.

   Description

   Verify that the description:

   - explains what the project does
   - is specific rather than promotional
   - includes the project’s important differentiator when useful
   - avoids repeating only the repository name
   - can be understood without opening the README
   - is short enough to scan cleanly
   - is consistent with the README and package description

   Provide a replacement description when the current one is missing or weak.

   Homepage or demo URL

   Verify that the homepage field:

   - points to the most useful public destination
   - loads successfully
   - is not an obsolete deployment
   - matches the current project
   - does not send users to an unrelated personal homepage
   - uses HTTPS when available

   For an application or visual component, prefer the live demo or documentation site that best explains the project.

   For a package, the best destination may be documentation, examples, or a focused demo rather than a generic landing page.

   Topics

   Verify that topics:

   - describe the technology, problem, and use case
   - help relevant visitors discover the project
   - avoid generic or misleading terms
   - do not duplicate near-identical variants
   - include important accessibility or framework terms when genuinely supported
   - remain focused rather than becoming a keyword dump

   Return a recommended topic set when useful.

   Social preview

   Check whether the repository has a useful social preview image.

   A good social preview should:

   - clearly identify the project
   - remain readable at small sizes
   - avoid excessive text
   - use current branding
   - avoid screenshots that become illegible when cropped
   - not expose private data, development URLs, tokens, or personal information

   Treat the social preview as optional but valuable for portfolio and launch-oriented repositories.

4. Review the README opening

   Evaluate the first visible section of the rendered README.

   It should usually establish:

   - project name
   - one-sentence value proposition
   - current status when important
   - visual proof or a concise usage example
   - live demo or documentation link
   - primary installation or exploration action

   Check whether the opening is weakened by:

   - a wall of badges
   - a large decorative logo before any explanation
   - vague slogans
   - repeated headings
   - excessive table-of-contents content
   - internal implementation detail
   - outdated warnings
   - no visible example
   - multiple competing calls to action

   Recommend a clearer opening order when needed.

   A common effective order is:

   1. Project name
   2. One-sentence explanation
   3. Small set of relevant status badges
   4. Screenshot, demo, or minimal usage example
   5. Primary links
   6. Key capabilities
   7. Installation or quick start

   Adapt this order to the repository rather than enforcing it mechanically.

5. Review README comprehension

   Check whether a visitor can find:

   - what the project does
   - why it exists
   - main capabilities
   - installation instructions
   - minimal usage example
   - supported environments
   - important limitations
   - demo or example links
   - documentation links
   - maintenance status
   - license
   - contribution guidance, when contributions are expected

   Check that examples match the current public API and package name.

   Flag:

   - stale commands
   - renamed exports
   - obsolete screenshots
   - references to deleted files
   - undocumented prerequisites
   - inconsistent terminology
   - sample code that cannot be copied successfully
   - overly long feature inventories without examples
   - important warnings hidden near the bottom

   Do not turn the README into complete API documentation when dedicated documentation already exists.

6. Review screenshots and visual evidence

   For applications, components, visual tools, or portfolio projects, inspect available screenshots and media.

   Check whether they:

   - show the current interface
   - demonstrate the project’s main value
   - are readable in the rendered README
   - use consistent framing and dimensions
   - avoid excessive empty space
   - avoid cropped menus, tooltips, or important content
   - include both context and useful detail
   - represent light and dark themes when both are supported
   - include mobile or responsive views when relevant
   - avoid exposing private data
   - use meaningful alternative text
   - load from stable repository paths
   - remain understandable without animation

   Prefer a small number of strong screenshots over a gallery of nearly identical images.

   Flag screenshots that:

   - show an outdated version
   - use placeholder content that makes the project look unfinished
   - are compressed beyond readability
   - depend on an external temporary image host
   - contain development errors or browser chrome that distracts from the project
   - show only decorative hero artwork without demonstrating functionality

   For non-visual libraries, visual proof may instead be:

   - a concise code example
   - terminal output
   - an architecture diagram
   - a before-and-after example
   - a small API flow
   - a compatibility table

   Do not penalize a non-visual project for lacking conventional UI screenshots.

7. Review live demos and examples

   Open all prominent demo and example links when network access is available.

   Check:

   - whether the page loads
   - whether assets load from the correct base path
   - whether the project name matches the repository
   - whether the demonstrated version appears current
   - whether the primary interaction works
   - whether the page explains what to try
   - whether source code for the example is easy to locate
   - whether the demo works without undocumented setup
   - whether mobile layout is usable when relevant
   - whether keyboard interaction is possible for interactive projects
   - whether errors appear in the visible page or browser console, when inspection tools are available

   For GitHub Pages deployments, watch for:

   - incorrect absolute asset paths
   - missing repository base paths
   - broken chunk URLs
   - case-sensitive path errors
   - stale deployment output
   - links that work locally but not under the repository subdirectory

   Do not perform a full functional QA or accessibility audit unless explicitly requested. Report obvious failures that damage the public first impression.

   When no live demo exists, determine whether one is appropriate.

   Do not automatically require a live demo for:

   - low-level utilities
   - backend-only libraries
   - build tooling
   - experimental research
   - archived projects
   - packages that are better demonstrated through code examples

8. Review trust and maintenance signals

   Inspect visible signals that help a visitor decide whether the project is credible.

   Relevant signals may include:

   - clear license
   - recent and meaningful repository activity
   - current installation instructions
   - working CI badges
   - release or version information
   - supported environments
   - changelog
   - contribution guidance
   - issue templates
   - security policy
   - maintenance-status notice
   - roadmap or project status
   - authorship and attribution
   - package registry link
   - documentation link

   Do not recommend every possible community file.

   Only recommend files that match the project’s maturity and intended collaboration model.

   Flag misleading signals such as:

   - passing badges for obsolete workflows
   - “production ready” language without supporting evidence
   - version badges that disagree with package metadata
   - contribution invitations on an abandoned repository
   - an active-looking README for an archived project
   - broken coverage or CI badges
   - installation commands for an unpublished package

9. Check cross-surface consistency

   Compare the public metadata, README, package metadata, screenshots, demo, and documentation.

   Check for consistency in:

   - project name
   - package name
   - description
   - version
   - logo
   - terminology
   - feature claims
   - browser or runtime support
   - installation command
   - primary URL
   - author information
   - license
   - maintenance status

   A mismatch between surfaces is usually more damaging than a minor omission because it makes the project appear stale or unreliable.

10. Score the public profile

    Score each category from `0` to `3`.

    | Score | Meaning |
    |---:|---|
    | `0` | Missing, broken, or seriously misleading |
    | `1` | Weak, incomplete, or difficult to understand |
    | `2` | Adequate and usable, with visible improvement opportunities |
    | `3` | Clear, current, credible, and well presented |

    Score these categories:

    1. Repository metadata
    2. README opening and positioning
    3. Visual proof or usage evidence
    4. Demo and public links
    5. Trust and maintenance signals
    6. Cross-surface consistency

    Maximum score: `18`.

    | Total | Assessment |
    |---|---|
    | `15–18` | Polished public profile |
    | `11–14` | Credible, but needs targeted refinement |
    | `6–10` | Rough presentation that hides project quality |
    | `0–5` | Not ready for meaningful public evaluation |

    The score supports prioritization. It is not an objective measure of technical quality.

    Critical failures may override the numerical score, including:

    - broken primary demo
    - misleading project description
    - empty or unusable README
    - screenshots showing a different project version
    - unsafe information exposed in screenshots
    - installation instructions that do not work
    - repository metadata pointing to an unrelated destination

11. Prioritize recommendations

    Classify recommendations as:

    - `P0 — Broken or misleading`: prevents correct evaluation or sends visitors to a broken destination
    - `P1 — High-impact first impression`: materially improves understanding, credibility, or exploration
    - `P2 — Useful polish`: improves scanning, consistency, or presentation
    - `P3 — Optional enhancement`: valuable but not necessary for readiness

    Prefer the smallest set of high-impact improvements.

    Do not bury broken links or unclear positioning beneath cosmetic recommendations.

12. Separate local and remote changes

    Clearly distinguish between:

    Repository file changes

    Examples:

    - update `README.md`
    - add committed screenshots
    - fix documentation links
    - add a status notice
    - improve example files
    - update package description

    Remote repository settings

    Examples:

    - change repository description
    - update homepage URL
    - add topics
    - upload social preview
    - archive or unarchive the repository
    - change repository visibility

    Do not claim that remote metadata was changed unless an authorized remote action was actually performed.

    The review-only skill must recommend remote changes rather than applying them.

## Output format

Return the review using this structure:

```md
## Verdict

**Assessment:** Polished | Credible but needs refinement | Rough presentation | Not publicly ready

One concise paragraph explaining the result.

## 10-second impression

What a new visitor is likely to understand immediately, what remains unclear, and the most important source of friction.

## Scorecard

| Area | Score | Evidence |
|---|---:|---|
| Repository metadata | 0–3 | ... |
| README opening and positioning | 0–3 | ... |
| Visual proof or usage evidence | 0–3 | ... |
| Demo and public links | 0–3 | ... |
| Trust and maintenance signals | 0–3 | ... |
| Cross-surface consistency | 0–3 | ... |
| **Total** | **0–18** | ... |

## Findings

| Priority | Surface | Issue | Evidence | Recommended fix |
|---|---|---|---|---|
| P0–P3 | ... | ... | ... | ... |

## Recommended public metadata

**Description**

> Exact recommended repository description.

**Homepage or demo**

Recommended URL or destination, with rationale.

**Topics**

`topic-one`, `topic-two`, `topic-three`

**Social preview**

Keep, replace, add, or omit, with a concise recommendation.

## README opening recommendation

Provide the recommended information order.

Include exact replacement wording for the project introduction when the current wording is weak.

Do not rewrite the complete README unless the user requested a full rewrite.

## Screenshot and demo plan

- Keep:
- Replace:
- Add:
- Remove:
- Demo fixes:

## Recommended changes

### Repository files

- [ ] ...

### Remote repository settings

- [ ] ...

## Validation

- [ ] Repository purpose is understandable without reading source code.
- [ ] Repository description matches the project.
- [ ] Homepage or demo link works.
- [ ] Topics are specific and relevant.
- [ ] README opening provides an obvious next action.
- [ ] Screenshots or examples represent the current project.
- [ ] Installation and usage examples match the current API.
- [ ] Public links resolve successfully.
- [ ] Project name and description are consistent across surfaces.
- [ ] Remote-setting recommendations are separated from file changes.

## Blocked or unverified checks

- List metadata, links, screenshots, or remote surfaces that could not be inspected.

If implementation was explicitly requested, add:

## Changes made

| File | Change | Reason |
|---|---|---|
| `...` | ... | ... |

## Remaining remote changes

- ...
```

Never represent recommendations as completed changes.

## Quality bar

The task is complete only when:

- The public repository landing page was reviewed before deep source inspection.
- The review is tailored to the actual repository type and audience.
- The repository description, topics, homepage, README, screenshots, and demo were all considered.
- Every `P0` and `P1` finding includes observable evidence.
- Broken, missing, outdated, and merely optional items are distinguished.
- Recommended metadata includes exact wording rather than vague advice.
- Demo and documentation links were validated when network access was available.
- Screenshots were evaluated as evidence of the project rather than decoration.
- The review distinguishes repository files from remote GitHub settings.
- Recommendations do not turn the README into an unnecessarily large marketing page.
- The final result identifies the smallest high-impact set of changes.
- Unavailable or unverified information is clearly marked.
- No remote repository setting was changed without an explicitly authorized workflow.

## Edge cases

### No remote repository access

Review local files and provided screenshots.

Mark repository description, topics, homepage, social preview, rendered README, and public links as unverified unless they were supplied separately.

### Repository has no README

Treat this as a major public-presentation problem unless the repository is intentionally empty or machine-generated.

Recommend a minimal README structure based on the project type.

### Repository is a monorepo

Review:

- the root repository profile
- the root README
- package-level documentation
- navigation between packages
- whether the main public entry point is obvious

Do not require every package README to duplicate the root documentation.

### Repository is archived

Check whether the archived state is visible and honestly explained.

Recommend a replacement, successor, or maintenance-status notice when available.

Do not recommend active-maintenance signals for an intentionally archived project.

### Repository is work in progress

Recommend an explicit status notice and realistic expectations.

A clear experimental label is better than making an unfinished project appear production-ready.

### Project has no meaningful visual interface

Use code examples, terminal output, diagrams, before-and-after samples, or API flows as public proof.

Do not require decorative screenshots.

### Demo requires authentication or paid infrastructure

Check whether a public preview, recorded walkthrough, sandbox, seeded account, or local example would communicate the project safely.

Do not recommend exposing real credentials.

### Screenshots contain private or unsafe information

Treat exposed personal data, internal URLs, secrets, tokens, customer data, or private messages as a critical issue.

Recommend removing or replacing the asset immediately.

### Generated README or documentation

Identify the source template or generator before proposing edits.

Avoid editing generated output when the source should be changed instead.

### Repository intentionally has minimal documentation

Respect a deliberately narrow repository, but verify that its purpose and basic use are still understandable.

Minimal does not mean ambiguous.

## Related skills

- `github-pages-readiness`
- `release-readiness-review`
- `npm-publish-readiness`
- `demo-index-docs-enhancer`
