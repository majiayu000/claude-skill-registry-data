---
name: rseng-citation-metadata
description: >-
  Covers making research software citable and contributors credited: writing
  CITATION.cff, describing software with CodeMeta (codemeta.json), minting
  DOIs and ORCIDs, and tracking contributors of every kind. Use when the user
  asks how to make software citable, add CITATION.cff or codemeta.json, obtain
  a DOI, ensure contributors get credit, or mentions CFF, CodeMeta, ORCID,
  CRediT or persistent identifiers. Use PROACTIVELY when generated code draws
  on a publication, website or existing code (credit it at the code site and
  in the references), at release preparation, and when citation files are
  edited. (Verifying references you cite: rseng-citation-hygiene; versioning
  schemes and the DOI-minting release: rseng-publishing-releasing.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Making research software citable and credited

Use this skill when someone wants their research software to be cited,
discovered, and formally recognised: adding a citation file, writing
machine-readable metadata, getting a persistent identifier, or building an
evidence base of who contributed. Software has no title page, so the
information needed to cite it is often hard to find - a citation file and
structured metadata are what let both humans and tools cite the exact work
correctly. Advise concrete files in the repository
root, not abstractions.

## Start here: what a citable project needs

For most projects, recommend all four in the repository root:

1. `CITATION.cff` - machine-readable citation metadata.
2. `codemeta.json` - richer discovery/interoperability metadata.
3. A DOI from an archive like Zenodo, minted per release.
4. A `CONTRIBUTORS` file - human-readable team record alongside the
   machine-readable ones.

A software citation itself should carry: title, the specific version used,
authors/creators, a DOI or other stable link, and the repository URL - the
version matters for reproducibility.

## Write a CITATION.cff file

The Citation File Format is a structured plaintext (YAML) format; a valid
`CITATION.cff` in the repo root is reused automatically by GitHub, Zenodo,
and Zotero. Do not hand-craft the syntax from
memory - point the user at the CFFINIT generator, or start from the official
example and validate with cffconvert.

Checklist of core fields to populate:

- `cff-version` - the CFF schema version (e.g. `1.2.0`).
- `message` - the "please cite as" instruction.
- `title` - the official software name.
- `authors` - each with `given-names`, `family-names`, and an `orcid` where
  available; an author may instead be a `name` for an organisation.
- `version` - the release being cited.
- `date-released` - the release date.
- `doi` - the release or concept DOI once minted.
- `repository-code` - the source repository URL.
- `license` - an SPDX identifier.
- If a paper should be cited instead of, or alongside, the software, add a
  `preferred-citation` block pointing to the article and its DOI.

Minimal shape to adapt (validate before committing):

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: Your Software Name
version: 1.0.0
date-released: 2026-01-15
doi: 10.5281/zenodo.1234567
repository-code: https://github.com/yourusername/your-repo
license: MIT
authors:
  - given-names: First
    family-names: Author
    orcid: https://orcid.org/0000-0002-1825-0097
    affiliation: University of Edinburgh
```

Tell the user to generate with CFFINIT and validate with cffconvert rather
than trusting a hand-edited file.

## Describe the software with CodeMeta

`codemeta.json` is a JSON-LD metadata standard (extending Schema.org) that
travels between archives and registries - Zenodo, FigShare, InvenioRDM, and
Software Heritage can ingest it, so metadata is not re-entered when getting a
DOI. Recommend it whenever discovery,
interoperability, or DOI minting is in play. Match the type of metadata to
the goal: citation metadata for academic credit, versions and dependencies
for reproducing an analysis, keywords and descriptions for discoverability.

Field checklist for a complete record:

- `name`, `description`, `version` - identity and release.
- `author` and `contributor` - each a `Person` with `givenName`,
  `familyName`, and an ORCID as `identifier`.
- `license` - an SPDX URL (e.g. `https://spdx.org/licenses/MIT`).
- `codeRepository` and `issueTracker` - where the code and issues live.
- `programmingLanguage`, `softwareRequirements` - stack and dependencies.
- `identifier` - the software's own DOI once archived.
- `referencePublication` - the related article, with its DOI as
  `identifier`, when there is a paper to cite.
- `funder` - as an `Organization` with an identifier such as a Crossref
  Funder ID.
- `keywords`, `dateCreated`, `dateModified` - discovery and freshness.

Generate it with the CodeMeta Generator (form-based) or SOMEF (from README
and docs), then always review it by hand to add ORCID iDs and funder detail,
and validate the JSON-LD.
Keep it current: update on every new version or contributor.

## Identify and version the software

Uniquely identifying software and each version underpins reproducibility,
citation, and long-term access. Combine
methods rather than treating them as alternatives:

- Semantic Versioning (`MAJOR.MINOR.PATCH`) for human-readable release
  identity - apply it consistently across GitHub tags and distribution
  artifacts like Docker images.
- A DOI for a globally unique, citable reference that plugs into academic
  systems - the right choice for research software.
- Git commit hashes and cryptographic checksums for exact development
  snapshots and integrity, where relevant.

If the project is registered in a repository or registry, a persistent
identifier is often created automatically; the awesome-research-software-
registries list helps find a suitable one.

### Getting a DOI from Zenodo

Zenodo issues a **concept DOI** for the project as a whole plus a **release
DOI** per version - cite the release DOI for reproducibility, the concept DOI
to refer to the project generally.

For GitHub-hosted code:

1. Create or link a Zenodo account to the GitHub account.
2. Enable the repository under Zenodo's GitHub settings so each release is
   archived automatically.
3. Draft a new release on GitHub; Zenodo archives it and mints a DOI.
4. Copy the DOI badge (Markdown form) into the repository README.

For GitLab-hosted code, the path differs:
provide a `codemeta.json`, get a Zenodo token with publishing scopes, and add
eOSSR or gitlab2zenodo to the GitLab CI pipeline so a release triggers an
automatic Zenodo deposit and DOI. Note gitlab2zenodo needs a `.zenodo.json`
converted from `codemeta.json` (eossr can do this).

## Credit and recognition

Software contributions - maintenance, bug fixes, review, documentation - are
routinely invisible in publication-centric assessment. Making them creditable
needs structured metadata linking people to specific work via persistent
identifiers. Advise:

- Reward actions over roles: record verifiable, specific activities (a bug
  fix, a feature, a test-suite improvement) rather than static labels like
  "Developer". Still map roles with CRediT or the Contributor Roles Ontology
  where automated systems or institutions need them.
- Get every contributor an ORCID so identity flows into professional records
  without manual work.
- Make the software findable and citable via a DOI first - a contribution no
  one can point to will not be counted.
- Prefer tools that capture credit automatically from the workflow: APICURON
  for validated contribution events on ORCID profiles, BIP! Scholar for reuse
  and popularity indicators from OpenAIRE Graph metadata.

For a career or assessment case, pair quantitative reach (package-manager
downloads on PyPI or CRAN, dependency graphs, citing papers) with narrative
on technical complexity and scientific impact; check whether the institution
or funder recognises software as an output; and add a "Credit and
Recognition" section to the Software Management Plan, tracking contributions
from the start rather than retrospectively.

Validate citation files in CI: the cffconvert GitHub Action checks
CITATION.cff on every push, so a malformed file fails fast instead of
surfacing at publication time (pattern from the NLeSC python-template).

## Follow the contributors, proactively

Contributor records rot silently: people join, review, triage and
document, and the citation files still name the two founders. Track
contributions and suggest updates rather than waiting to be asked:

- Watch ALL contribution kinds, not just commits: merged PRs and
  their reviewers, substantive issue triage, documentation and
  support work - the all-contributors categories exist because
  commit logs miss the classically uncredited work.
- Harvest authorship from commit METADATA: author/committer fields,
  `Co-authored-by:` trailers and `.mailmap` are the machine-readable
  record - names pasted into commit prose or file headers are not
  (rseng-version-control-review); fix wrong-place practice at the
  source before fixing citation files.
- Diff activity against `CITATION.cff`, `codemeta.json` and
  CONTRIBUTORS; report who is active but unrecorded (and recorded
  but never active - possibly fine, possibly a paste error).
- Suggest at natural checkpoints: release prep (before the DOI
  freezes the author list), citation-file edits, a contributor's
  first merged PR.
- Respect policy and people: who counts as author vs acknowledged
  contributor is project policy (rseng-community-governance); adding
  someone needs their consent and preferred name/ORCID; never
  remove or reorder without explicit agreement. The agent proposes
  with evidence; humans decide.
- Automate the memory: the all-contributors bot records categorized
  contributions as they happen; a release-checklist item makes the
  check routine (rseng-publishing-releasing).

## Credit what the code came from

Crediting flows both ways: the sources that INFORM generated or
hand-written code deserve the same rigor as the project's own
citability. Whenever a website, publication, algorithm description,
existing codebase, or a Q&A answer shapes code, record it in every
place a future reader will look:

- At the code site: a short comment where the adaptation lives -
  source URL or DOI, what was taken (algorithm, approach, snippet),
  and the source's license whenever actual code was copied or
  ported. If code was copied, license compatibility must be checked
  first (rseng-license-compliance); incompatible source license means
  reimplement from the description, not copy.
- In the references: load-bearing sources - the paper whose method
  the code implements, software that was adapted - belong in
  CITATION.cff `references` entries (type, title, authors, DOI/URL)
  and in the project documentation's references section, not only
  in a comment.
- In the AI declaration: when an agent generated the code, the
  aidecl.yaml component notes name the sources it drew on
  (rseng-ai-declaration) - provenance of the inputs, not just the
  tool.
- Honestly: omitting a source that materially shaped the code
  misrepresents the work's originality (rseng-honesty), and a cited
  source must actually support what it is cited for
  (rseng-fact-checking).

There is no file pattern that reveals an uncredited source, so no
mechanical check exists - this is a discipline to apply AT
GENERATION TIME, and a review question afterwards (rseng-code-review:
"where did this method come from, and does the code say so?").

## Working with this skill

The generated references.md beside this file lists the source material
and pointers.

Learn more (verified):
  - https://citation-file-format.github.io - Citation File Format
    (CITATION.cff) home
  - https://codemeta.github.io - the CodeMeta project for software
    metadata
  - https://force11.org/info/software-citation-principles-published-2016/ -
    FORCE11 software citation principles
  - https://orcid.org - persistent identifiers for researchers


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - deposit metadata reuses codemeta
- rseng-citation-hygiene - verifying outbound references
- rseng-community-governance - authorship policy decisions
- rseng-fair-software - metadata implements findability
- rseng-publishing-releasing - DOI minting at release
- rseng-software-reuse - citing adopted software
- rseng-version-control-review - authorship harvested from commit metadata

<!-- related-skills:end -->
