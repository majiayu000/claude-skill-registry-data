---
name: "Artefact: Research"
description: "Research a focus (a tool, a practice, a field of candidates) and render the findings as a verified, source-cited HTML artefact in one of a fixed set of formats."
when_to_use: "When a question needs actual research (docs read, repos inspected, terms checked) and the answer is worth keeping as a page rather than a chat reply: is this tool worth adopting, which of these fits, what does the free tier actually give me, catalogue the options in this space."
model: fable
effort: high
metadata:
  glyph: ᚠ
  family: artefact
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Agent", "AskUserQuestion", "WebFetch", "WebSearch", "Artifact", "Bash(open:*)", "Bash(mkdir:*)", "Bash(find:*)", "Bash(git:*)", "Bash(grep:*)", "Bash(ls:*)"]
argument-hint: '"<focus>" <target> <format> [source | "src1,src2"]'
---

Research a focus and render what was found as an HTML artefact. The research is the expensive part; the artefact is the honest record of it, so every claim on the page carries a source or a visible `unverified` mark.

Worked example of the format bar, when working in `~/.claude`: `~/.claude/docs/artefacts/swamp-club.html` (`"swamp club free tier" resource assess`). Worth a look before writing HTML there, but not a prerequisite: Step 4 below and `references/formats.md` already state the full contract, and `artefact-conventions` Step 2 finds and reads whatever existing artefacts a project has on disk regardless.

## Step 1: Parse `$ARGUMENTS`

Positional, in this order. Quote the focus; the rest are bare words.

| # | Arg | Type | Values |
|---|-----|------|--------|
| 1 | `focus` | string, required | The question or subject, in plain words |
| 2 | `target` | enum, required | `resource` `practice` `field` |
| 3 | `format` | enum, required | `assess` `compare` `list` `primer` `brief` |
| 4 | `source` | string or comma-separated list, optional | Domains, repo URLs, paths; see Step 2 |

**Target** says what kind of thing is under the lens:

- `resource`: one nameable thing with a maintainer: a tool, library, service, plan, dataset
- `practice`: a way of working with no single owner: a pattern, technique, convention, workflow
- `field`: a space containing many candidates, where the subject is the space itself

**Format** says the shape of the page. Section schemas are in `references/formats.md`; read the one you need in Step 4.

| Format | One line | Fits target |
|--------|----------|-------------|
| `assess` | One subject: what it is, what it costs, verdict on fit against the user's actual projects | resource, practice |
| `compare` | Two to six named candidates on stated criteria; a recommendation with the losing options kept visible | resource, practice, field |
| `list` | Catalogue of candidates in a space, each with the same fixed fields; filterable, no verdict beyond a shortlist | field |
| `primer` | Teach the subject: prerequisites first, one anchor concept, then deltas; for learning, not deciding | practice, field |
| `brief` | Current state of the subject at a date: what changed, what is stable, what to watch; short | resource, field |

Invalid pairs (`field assess`, `resource primer` of a tool that has docs) get one line saying why and the nearest valid pair, then stop.

Missing or unparseable required args: ask once with `AskUserQuestion`, one question per missing arg, then continue.

- [ ] All three required args resolved and the pair is valid
- [ ] `source` split into a list (empty list when absent)

## Step 2: Resolve sources

`source` **restricts** where evidence comes from; it never merely suggests.

- **Given**: read only those. A domain means its docs and pricing pages; a repo URL means README, licence, releases, issues; a local path means the files under it. Web search is allowed only to locate pages *within* the given sources.
- **Absent**: you choose. Default order: the subject's own docs and repo, then independent coverage (issues, changelogs, third-party write-ups), then the user's own code under `~/code` when the format has a fit section. Web search freely.

Either way, keep a running **source ledger**: every URL or path actually read, with the date. It becomes the footer. A page read but not cited still belongs in the ledger; a claim with no ledger entry is `unverified` by definition.

Vendor-only evidence is a finding, not a footnote: when no independent source turned up, the page says so in the constraints or method section (the reference artefact does this in one sentence).

- [ ] Ledger started before the first fetch
- [ ] Restriction honoured when `source` was given

## Step 3: Research

Split the work by where the evidence lives, and run the two halves in parallel:

- **External evidence** (docs, repo, registries, independent coverage): delegate to one `general-purpose` agent. The prompt names the format's schema sections as required headings, demands the exact URL and a verbatim quote for every load-bearing fact, and ends with a mandatory **source ledger** (every URL read, one per line, with what it gave) plus a **could-not-find list**. Return raw findings, not prose. Keeping the fetches out of the main context is what leaves room to write the page.
- **Local evidence** (the `~/code` inventory, per-repo second passes): do it inline with Bash. One survey loop over every git repo (last commit, 90-day commits and authors, the dependency in question, files importing it, rival libraries present), then targeted greps on the candidates that surfaced.

Read until the format's schema is filled or the sources run out, whichever comes first. Two rules that separate research from summarising:

1. **Quote the load-bearing sentence.** Pricing gates, licence carve-outs, rate limits, "only when the server is running": copy the words, in a `blockquote.ev`, with the page cited beside it. Paraphrase is where errors creep in.
2. **Name what you could not find.** A limit that no page states, a claim with a single vendor source, a question two readings of the docs leave open: each becomes an explicit `unverified` chip on the page (artefact-conventions, epistemic honesty). Absence of a documented limit is not absence of a limit.

For `assess` and `compare`, fit against real projects is required when the sources allow it: inventory the candidate repos (`git log` recency, stack, who commits), and for each say fits / stretch / no fit with the reason. The reference artefact's Strand III is the model: the verdict names one project to spike first, a time estimate for the spike and the condition under which the spike should be abandoned.

- [ ] External research delegated with ledger and could-not-find list required
- [ ] Local survey run inline before the agent returns, so neither waits on the other
- [ ] Every load-bearing claim quoted, not paraphrased
- [ ] Every gap marked, none smoothed over

## Step 4: Render

Follow `artefact-conventions` (announce, location, existing aesthetic, shared rules). Then:

1. Read `references/formats.md`, the section for the chosen format. Its sections are the page's sections, in that order; drop a section only when the sources gave nothing for it, and say so in one line where it would have sat.
2. **Masthead**: kicker `{Target} {format} · {date}`, title, one-paragraph standfirst that already states the answer, then a statline of research counts (pages read, candidates assessed, repos checked, whatever the format makes real). Counts come from the ledger, not from memory.
3. **Verdict box first**, for every format except `primer`: the reader who stops after the masthead has the answer. `primer` opens with its anchor concept instead.
4. **Legend** for the chip set the format uses (`fits` / `stretch` / `no fit` / `unverified` for assess; the format schema names the others).
5. Sections as collapsible `<details>` past the conventions' threshold, with the rail table of contents and expand/collapse controls.
6. **Footer**: the source ledger as a closed `<details>`, every entry a link, plus the method in two sentences (what was read, what was not, when).

Location: `<project-root>/docs/artefacts/research-{slug}.html`, then publish with the `Artifact` tool (favicon `🔬`, description = the standfirst's first sentence). In `~/.claude` the artefact joins the existing aesthetic (`warren-report.html`, `swamp-club.html`); elsewhere, Step 2 of `artefact-conventions` decides.

- [ ] Verdict readable without opening any `<details>`
- [ ] Ledger footer present, all entries linked
- [ ] `artefact-conventions` checklist run

## Step 5: Report

File path, artefact URL, the verdict in one line and the count of `unverified` marks with what each one is waiting on. If the verdict recommends a spike, end with its first action.
