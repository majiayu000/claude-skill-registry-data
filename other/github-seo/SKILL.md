---
name: github-seo
description: >-
  v1.3.1 — Use when a GitHub project needs to be found: search-engine ranking, AI/LLM
  citability, GitHub-internal discovery, and registry presence. Runs a
  weighted 100-point audit, records a tracked scorecard, then closes the highest-value gap
  round after round until the score is a fully evidenced 100/100, and maintains it after.
---

# GitHub SEO

Make a repository findable by the people and the machines that are already
looking for what it does — and keep it that way. This skill is a **scored,
repeatable loop**, not a one-shot cleanup: every run re-measures the project
against the same rubric, so two agents a month apart produce comparable numbers.

## Project instructions first

Read the repository's own `AGENTS.md` and `CLAUDE.md` before editing anything;
they outrank this skill for ownership, routing, deployment, and local policy.
Follow the independently selected `worktree` and `commits` skills for
isolation and commit → merge → reapply delivery, and `testing`, `logging`, and
`docs` for applicable engineering checks. This skill does not restate their policy; it only adds what is specific to
discoverability work.

## Owner-wide SEO workflow

For mikaeltorni's repositories, the private `seo_optimization` repository is
the single source of truth for SEO audits, workflows, and scorecards. Target
repositories may contain this reusable dispatch prompt, but they must not carry
`docs/seo-scorecard.md` or a copied owner-wide SEO policy. Read and update the
matching `scorecards/<repository>.md` in `seo_optimization` instead.

## Non-negotiables

- **Never inflate the score.** A criterion earns points only from evidence you
  recorded this round. "Looks fine" is zero.
- **Never fake a signal.** No invented benchmarks, no features that do not
  exist, no testimonials, no star or follow exchanges, no mass-mention issues or
  pull requests on unrelated repositories. Those are penalties, not wins.
- **Never keyword-stuff.** Every keyword must land in a sentence a human would
  have written anyway. Text that reads like SEO bait scores worse than plain
  prose, and the rubric penalizes it.
- **Never change program behavior** in the name of discoverability. This skill
  edits documentation, metadata, packaging descriptors, and site assets. Code
  changes are in scope only when they are required to make a documented claim
  true, and then they follow the normal test-first loop.
- **Never rename the repository, change its visibility, or delete existing
  topics/links on your own.** Those break inbound links and are the user's call.
  Propose them under *Pending user actions* instead.
- **Never publish anything on the user's behalf** — no posts, submissions, pull
  requests to other people's lists, or messages — without explicit approval in
  the current conversation. Draft them, record them, and wait.
- **Never add continuous integration.** Do not create or restore
  `.github/workflows/`, GitHub Actions, or any other CI/CD pipeline, and do not
  add a CI or build-status badge to a README. CI earns no points in this rubric
  and is not a discoverability signal. The one exception is CI a repository
  already inherited from an upstream project it was forked from: leave those
  workflows and their badges exactly as upstream ships them, and never delete
  them to satisfy this rule. If the user asks for CI explicitly in the current
  conversation, that request wins.
- **Never build a static docs site on your own.** Do not create or restore
  `index.html` or any other HTML page, `sitemap.xml`, `robots.txt`, `llms.txt`,
  `_config.yml`, Jekyll/Pages scaffolding, or a GitHub Pages deployment, and do
  not link a `github.io` URL from a README or the About homepage. A site is a
  publication the owner must ask for; when the owner's project instructions rule
  it out, score section `F` and row `D2` as `N/A` and normalize over the rest.
  README-embedded diagrams and a social preview image are repository assets, not
  a site — keep those.

## Where the score lives

For mikaeltorni's repositories, one tracked scorecard per repository lives in
the private `seo_optimization/scorecards/` directory. It is the memory that
makes the loop continuous. Every run reads the matching central scorecard
first, then rewrites it with freshly verified numbers and appends one history
row. Never create `docs/seo-scorecard.md` in a target repository. Never delete history rows, and never copy a previous round's score forward without re-verifying it.

The file has exactly these sections:

```markdown
# SEO Scorecard — <repo name>

- Canonical URL: <https://github.com/owner/repo>
- Round: <n>   Date: <YYYY-MM-DD>   Score: <total>/100 (<earned>/<applicable max> raw, <penalties> penalty)
- Verdict: <in progress | perfect (maintenance) >

## Keyword model
| Role | Terms | Why |
| --- | --- | --- |
| Primary | ... | the one query this project should win |
| Secondary | ... | 3–6 adjacent queries |
| Long-tail | ... | 5+ specific problem phrasings |
| Confusable with | ... | projects/terms we must disambiguate from |

## Criteria
| ID | Criterion | Max | Score | Evidence | Gap / next action |
| --- | --- | --- | --- | --- | --- |
| A1 | ... | 3 | 3 | `gh repo view --json description` → "..." | — |

## Not applicable
| ID | Reason |
| --- | --- |

## Penalties
| ID | Penalty | Points | Evidence |
| --- | --- | --- | --- |

## Pending user actions
| Action | Why it needs the user | Exact command / draft |
| --- | --- | --- |

## Round history
| Round | Date | Score | What changed |
| --- | --- | --- | --- |
```

## Work Loop

Run these steps in order, every invocation, including the ones where you expect
nothing to have changed.

1. **Set up isolation** under the selected `worktree` skill before the first
   repository edit. It owns the physical project/task layout and branch naming.
2. **Recon the project as it really is.** Read the code entry points, the
   package manifest, the CLI/API surface, and the existing README. You cannot
   write a truthful description of software you have not looked at, and every
   later claim must be traceable to something you read.
3. **Read the existing central scorecard** for the repository when it exists.
   Use it for history and for the keyword model, never as a substitute for
   measuring.
4. **Build or refresh the keyword model.** Derive the primary keyword from what
   the project *does* for *whom*, not from what sounds impressive. Check the
   terms against reality: search them, look at what the top results are, and
   note the projects you will be confused with. A primary keyword you cannot
   plausibly rank for is worse than a narrower one you own.
5. **Audit and score every criterion** in the rubric below, from scratch,
   recording evidence per criterion. Use the commands in *Measuring*.
6. **Write the central scorecard** with the new numbers before changing
   anything else, so the round's starting point is on record.
7. **Pick the work.** Order the open gaps by `weight × gap × confidence`, and
   take the top item that you can complete and verify now. Anything that needs
   the user goes to *Pending user actions* instead of blocking the round.
8. **Implement one Feature at a time**, following the selected `commits` skill.
   Apply `testing` checks during implementation and document changed behavior
   through `docs`.
9. **Verify the change is real.** Run the install/quickstart commands you just
   wrote. Fetch the links you just added. Render the Markdown. A README that
   claims a command works is a defect until you have run it.
10. **Deliver**: commit in the worktree, merge into the default branch with
    `git merge --no-ff` from the live checkout, and reapply/reload whatever
    consumes the change. Repeat per Feature — do not batch a whole round into
    one merge.
11. **Re-audit from scratch and re-score.** Append the history row with the new
    total and a one-line summary of what changed.
12. **Loop.** Go back to step 7 while the total is below 100 and any gap is
    actionable. There is no deadline: a smaller, fully verified improvement
    always beats a larger unverified one. Stop only on the stop condition below.

### Stop condition

The work is *perfect* when **all** of these hold in the current round:

- the normalized total is 100,
- there are zero penalties,
- every applicable criterion has evidence recorded this round,
- every N/A carries a reason, and
- a second, independent re-audit — re-running the measurements rather than
  re-reading the scorecard — reproduces 100.

Then set `Verdict: perfect (maintenance)` and switch to **maintenance mode**: on
each later invocation, re-measure everything, fix any drift (dead links, stale
claims, expired badges, a release that aged out), and append a history row even
when the score is unchanged.

While the total is below 100, "nothing to do" is not a valid outcome. If every
remaining gap genuinely requires the user, say so explicitly and list each one
under *Pending user actions* with the exact command or draft text ready to
approve.

## Scoring rules

- Each criterion scores **0**, **half** (rounded down to the nearest 0.5), or
  **full**. Half credit means the artifact exists but fails part of its "full
  credit requires" clause.
- **Evidence or zero.** Acceptable evidence is a file path with a line range, a
  command with its actual output, or a URL you actually fetched this round.
- **N/A** is only for criteria that cannot apply to this project — no registry
  exists for the ecosystem, the project is intentionally private, the repository
  has no user-facing surface. Record the reason. N/A points leave the
  denominator; they are never awarded.
- **Normalized total** = `round(100 × (earned − penalties) ÷ applicable_max)`,
  floored at 0. Report the raw numbers alongside it.
- Penalties are subtracted once each, no matter how many instances — but list
  every instance in the evidence column so they all get fixed.

## The rubric — 100 points

### A. Repository identity and metadata — 15

- **A1 (3) About description.** Full credit requires: 50–350 characters, first
  clause states what the project does, contains the primary keyword, names the
  audience or the problem, no leading filler ("A tool that…"), no emoji-only
  content, and it matches the README's first sentence in substance.
- **A2 (4) Topics.** Full credit requires: 8–20 GitHub topics, every one
  genuinely descriptive; includes the primary keyword, the implementation
  language, the platform/ecosystem, the domain, and at least two long-tail
  terms; all lowercase-hyphenated; prefer topics that already exist on GitHub
  over invented ones.
- **A3 (2) Homepage URL.** Full credit requires: the About homepage points at
  the docs site, or the registry page, or the latest release — a live URL that
  answers "where do I start", not a duplicate of the repo URL.
- **A4 (3) Name fit.** Full credit requires: the repository name is readable,
  unambiguous, carries or clearly implies the primary keyword, and matches the
  package/CLI/binary name users will type. Score the fit honestly; if a rename
  is warranted, propose it under *Pending user actions* — never rename.
- **A5 (3) Social preview.** Full credit requires: a 1280×640 social preview
  image is set, the project name is legible at thumbnail size, and it says what
  the project does rather than being decoration.

### B. README above the fold — 15

"Above the fold" is what a reader sees before scrolling: roughly the first 40
rendered lines.

- **B1 (3) H1.** Full credit requires: exactly one H1, containing the canonical
  project name plus a short descriptor that carries the primary keyword.
- **B2 (3) Value proposition.** Full credit requires: a single sentence inside
  the first 160 characters of prose that a search engine or an assistant can
  lift verbatim as the description — concrete, specific, no marketing adjectives.
- **B3 (2) Badges.** Full credit requires: 2–6 badges that carry information
  (license, released version/registry, supported platform, activity), all
  resolving, none redundant. Never add a CI/build-status badge.
- **B4 (3) Visual proof.** Full credit requires: a screenshot, GIF, or diagram
  above the fold showing the project in use, with alt text that describes what
  is happening (not "screenshot" or "demo").
- **B5 (2) Instant start.** Full credit requires: the install command and a
  three-line "first useful result" example are visible above the fold, and both
  run as written.
- **B6 (2) Navigation.** Full credit requires: a table of contents or a compact
  link row when the README exceeds ~150 lines; below that length, credit is
  full without one.

### C. README depth and keyword coverage — 15

- **C1 (3) Required sections.** Full credit requires all present and
  substantive: Features, Installation (with prerequisites), Usage/Examples,
  Configuration, Troubleshooting or FAQ, Contributing, License.
- **C2 (3) Heading semantics.** Full credit requires: one H1, no skipped
  levels, and headings that are keyword-bearing noun phrases ("Installing on
  Ubuntu", not "Setup" or "Misc") — they become the page's anchor links and the
  snippets assistants quote.
- **C3 (3) Keyword coverage.** Full credit requires: the primary keyword in the
  H1, in the first paragraph, and in at least two H2s; at least five
  secondary/long-tail terms each used once in a heading or a sentence that reads
  naturally. Repetition beyond what the prose needs is stuffing — see P1.
- **C4 (2) Runnable examples.** Full credit requires: every fenced block is
  language-tagged, and every command block is copy-pasteable verbatim against a
  clean install (real paths, no unexplained placeholders).
- **C5 (2) Accessible references.** Full credit requires: descriptive alt text
  on every image, descriptive anchor text on every link (never "here"), and no
  broken links or images.
- **C6 (2) Positioning.** Full credit requires: an explicit "what this is / what
  this is not", an alternatives comparison, or a "use this when…" block, so a
  searcher can self-qualify in one read.

### D. AI and LLM discoverability — 10

- **D1 (3) Question-shaped FAQ.** Full credit requires: at least five headings
  phrased as the questions users actually ask, each answered in a
  self-contained 2–4 sentence paragraph that makes sense quoted alone.
- **D2 (2) `llms.txt`.** Full credit requires: `llms.txt` at the repository root
  (and served at the docs-site root when one exists) giving the one-line
  definition, install command, primary entry points, and links to the canonical
  pages. Score `N/A` where the owner's project instructions rule `llms.txt` out
  of scope, and never create the file there.
- **D3 (2) Definitional sentence.** Full credit requires: one sentence of the
  form "*Name* is a *category* that *does X* for *audience*", placed early and
  repeated verbatim in the About text and `llms.txt`.
- **D4 (2) Disambiguation.** Full credit requires: if the name collides with
  other software, products, or common words, the README's first paragraph, the
  About text, and the topics all disambiguate it explicitly.
- **D5 (1) Machine-readable metadata.** Full credit requires: `CITATION.cff` or
  a package manifest whose `description`/`keywords` agree with the About text
  and the keyword model — no three-way drift.

### E. Repository health and trust signals — 10

- **E1 (3) License.** Full credit requires: a LICENSE file GitHub recognizes as
  a specific SPDX license, and the same license named in the README and manifest.
- **E2 (2) Community files.** `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and
  `SECURITY.md` present and specific to this project.
- **E3 (2) Templates.** Issue templates and a pull request template under
  `.github/`.
- **E4 (3) Community Standards.** GitHub's community profile checklist reports
  every item complete.

Continuous integration is deliberately absent from this rubric; see *Never add
continuous integration* under *Non-negotiables*.

### F. Docs site and technical SEO — 10

Score N/A only when the project genuinely should not have a public page — which
includes an owner policy that rules static docs sites out of scope. When the
whole section is N/A, so are the site-shaped parts of any other row; normalize
over the remaining points instead of scoring a missing site as a gap.

- **F1 (2) Published site.** A docs site (GitHub Pages or equivalent) on a
  stable canonical URL, linked from the About homepage.
- **F2 (2) Titles and descriptions.** Every page has a unique `<title>` of ≤60
  characters and a `<meta name="description">` of 120–160 characters.
- **F3 (2) Share cards.** Open Graph and Twitter card tags with an image, so a
  pasted link renders as a card.
- **F4 (2) Crawlability.** `sitemap.xml` and `robots.txt` present and correct,
  and every page carries a `<link rel="canonical">`.
- **F5 (2) Structured data.** JSON-LD for `SoftwareApplication` or
  `SoftwareSourceCode`, plus `FAQPage` on the FAQ, validating without errors.

### G. Packaging and registry presence — 10

- **G1 (3) Published artifact.** The project is installable from its ecosystem's
  registry (PyPI, npm, crates.io, AUR, Docker Hub, a marketplace, or a signed
  release asset) — N/A only when no such channel exists.
- **G2 (3) Registry metadata mirrors the repo.** Description, keywords or
  classifiers, homepage, repository link, and long description all match the
  keyword model and the About text.
- **G3 (2) Releases.** Tagged, semantically versioned releases with
  human-readable notes, and a CHANGELOG that a user can skim.
- **G4 (2) Install parity.** The README's install instructions match the
  published artifact exactly, verified by running them.

### H. Backlinks and cross-links — 10

- **H1 (3) Own-network cross-links.** Every related repository the same owner
  controls links to this one with descriptive anchor text, and this one links
  back. This is the highest-value link work available without asking anyone.
- **H2 (3) Directories and lists.** At least two relevant awesome-lists,
  registries, or directories list the project — or a submission is drafted and
  recorded with its URL and status.
- **H3 (2) Canonical write-up.** A post, docs page, or pinned discussion that
  explains the project and links back with descriptive anchor text.
- **H4 (2) Profile surfaces.** Pinned on the owner's GitHub profile when it is a
  flagship project, and named in the profile README.

### I. Freshness and engagement — 5

- **I1 (2) Activity.** Commits within the last 90 days, and no stale "coming
  soon" or "work in progress" claims that are no longer true.
- **I2 (1) Release cadence.** A release within the last 12 months, or an
  explicit "stable and complete" statement in the README.
- **I3 (1) Triage.** No issue or pull request left without a response for more
  than 30 days.
- **I4 (1) Entry point.** A pinned issue or discussion that points new users at
  the quickstart.

## Penalties

Subtract each once, and list every instance in the evidence column.

| ID | Penalty | Points |
| --- | --- | --- |
| P1 | Keyword stuffing — repetition beyond what the prose needs, keyword lists, hidden text | −5 |
| P2 | Claims the code does not support — nonexistent features, fabricated benchmarks or testimonials | −5 |
| P3 | Badge wall (more than 8) or badges that error, 404, or show "unknown" | −3 |
| P4 | Topic spam — topics that do not describe the project, or added to ride unrelated traffic | −3 |
| P5 | Artificial engagement — star/follow exchanges, mass-mention issues or PRs, unsolicited mass messaging | −5 |
| P6 | Broken links or missing images in the README or docs site | −2 |

## Measuring

Prefer real measurements over inspection. These are starting points; adapt them
to the ecosystem and record whatever you actually ran.

```bash
# Repository metadata (About text, topics, homepage, license, activity)
gh repo view --json name,description,repositoryTopics,homepageUrl,licenseInfo,pushedAt,stargazerCount

# Community Standards checklist
gh api repos/{owner}/{repo}/community/profile

# Releases and tags
gh release list --limit 10 && git tag --sort=-creatordate | head

# README structure: heading tree, image alt text, link text
rg -n '^#{1,6} ' README.md
rg -n '!\[[^]]*\]' README.md
rg -n '\[(here|this|link|click here)\]' -i README.md

# Every link in the README, checked for real
rg -o 'https?://[^)"< ]+' README.md | sort -u | while read -r url; do
  printf '%s %s\n' "$(curl -sS -o /dev/null -w '%{http_code}' -L --max-time 20 "$url")" "$url"
done

# Docs-site head tags, when a site exists
curl -sS <site-url> | rg -n '<title>|name="description"|og:|twitter:|rel="canonical"|application/ld\+json'
```

When `gh` is unavailable or unauthenticated, fall back to `git remote -v` plus
`curl https://api.github.com/repos/{owner}/{repo}` and say so in the evidence.

## Applying remote metadata

The About description, topics, and homepage live on GitHub, not in the tree.
Changing them is a metadata write, not a push of history, and it is in scope —
but it is still the user's repository:

- Record the **before** value in the scorecard evidence before you change it.
- Apply with `gh repo edit --description ... --homepage ... --add-topic ...`.
- **Add** topics; only remove one when it is provably wrong, and log the removal.
- If `gh` is unauthenticated, or the repository belongs to someone else, or the
  user has asked you not to touch the remote, put the exact command under
  *Pending user actions* instead.
- Never touch visibility, the repository name, default branch, or archived state.

## Anti-patterns

- Rewriting a README into marketing copy. Developers bounce off superlatives;
  they stay for a precise first sentence and a command that works.
- Chasing a keyword the project cannot honestly own. Rank for the narrow query
  you deserve, then widen.
- Adding sections to satisfy the rubric while leaving them empty. An empty
  "Roadmap" scores worse than no roadmap, because it dates the project.
- Treating stars as the goal. The rubric measures findability and clarity; stars
  are a lagging side effect, and manufacturing them is P5.
- Editing generated files, vendored code, or the docs of a dependency.
- Declaring victory from the scorecard instead of from a fresh measurement.

## Definition of Done

Alongside the applicable selected engineering skills:

- [ ] The matching `seo_optimization/scorecards/<repository>.md` exists in the
      central SEO repository, is committed, and its numbers come from
      measurements taken this round.
- [ ] Every criterion is 0 / half / full with evidence, or N/A with a reason.
- [ ] Penalties are listed with every instance, or explicitly none.
- [ ] Every claim added to the README, About text, or site is true of the code
      as it is today.
- [ ] Every command written into the docs was executed as written this round.
- [ ] Every link and image added was fetched and returned a success status.
- [ ] Work that needs the user is listed under *Pending user actions* with the
      exact command or draft, and nothing was published on their behalf.
- [ ] A history row was appended with the round number, date, total, and what
      changed.
- [ ] Each Feature was committed in the worktree, merged into the default branch
      with `git merge --no-ff`, and reapplied.
- [ ] The report states the score before and after, the largest remaining gap,
      and whether the stop condition was met.
