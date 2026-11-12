---
name: voice
description: >
  The house writing voice for claude-wiki-pages — how to write prose that a
  newcomer actually wants to read and an engineer can trust. Defines two
  registers (explanatory and engineer), the rule for choosing between them, the
  LLM-artifact blocklist, the vocabulary and register-separation rules the doc
  gate enforces, and how to write a wiki page. Trigger when writing or
  editing any doc, README, guide, or wiki page, or when an agent asks "what
  voice should I write in", "how should this note read", or invokes
  /claude-wiki-pages:voice. Reference, not action — it teaches how to write,
  it does not write for you.
allowed-tools: Read
disable-model-invocation: true
---

# Voice — how we write here

Write so a curious newcomer keeps reading and an engineer keeps trusting. Plain words for the
ideas, exact words for the mechanics. Never sound like a brochure or a generated summary.

## When to read this

Read it before you write or edit any prose: a README, a guide, a design doc, an ADR, a section
intro, or a wiki page. The schema in [`skills/init/template/CLAUDE.md`](../init/template/CLAUDE.md)
still owns frontmatter and structure; this skill owns the words. That is the schema authority — do
not cite the retired `docs/vault-example/`. The canonical term list is
[`docs/GLOSSARY.md`](../../docs/GLOSSARY.md) — it wins any vocabulary question. When you name an
authoritative path in prose, it must resolve today; a stale authority path is a register failure,
not just a typo.

## Pick a register by audience

Every paragraph is aimed at someone. Decide who, then pick the register.

**Explanatory register** — for anyone learning what the thing is or why it matters: README intros,
getting-started, the guides, and the "what / why" opening of any doc. Write like you're explaining
it to a sharp friend at a whiteboard.

- Short, concrete sentences. One idea each.
- Active voice. Talk to the reader as "you".
- Lead with the point, then support it. No throat-clearing.
- Show, don't label: a real example beats the word "powerful".
- A little personality is good. Dryness is not the goal; clarity is.
- **Gloss a term on first use, then commit to it.** The first time a glossary term appears on a
  page, gloss it inline in a half-sentence — "the vault (your knowledge directory)" — then use the
  canonical term every time after. Don't coin a synonym to dodge the term; gloss it. Spell out an
  acronym on first use ("Map of Content (MOC)"), then use the short form.
- **One new term per sentence.** Precise is not the same as dense. If a sentence needs three
  glossary terms, it belongs in the engineer register or wants splitting.
- **Close with the one next step.** End a getting-started or onboarding section by naming the single
  next action — `/claude-wiki-pages:wiki`, the one advertised verb — not a menu. `:onboarding` and
  `:doctor` are below-the-fold secondaries, never co-equal. The documented adoption failure is a
  section that ends with "you're set up" instead of the next verb.

**Engineer register** — for the reader who has to build, operate, or audit: architecture, design
docs, ADRs, SECURITY, reference sections, contracts. Precision outranks simplicity here.

- Use the exact glossary term, every time. No loose synonyms.
- Ground claims in paths, contracts, and gates — say where it's enforced.
- Terse beats chatty. Cut the adjective if the noun already carries it.
- Still no filler: precise is not the same as padded.

When a doc serves both, open in the explanatory register and shift to engineer register as it goes
deep. The README hero is explanatory; the threat model is engineer.

## The LLM-artifact blocklist

These read as machine-written. Cut them in both registers.

- **Em-dash drama.** Stacking em-dashes for rhythm. Use a period or a comma.
- **Filler openers.** "It's worth noting", "It's important to note", "Let's dive in", "In today's
  world", "At the end of the day".
- **Hype adjectives.** powerful, seamless, robust, effortless, cutting-edge, leverage, utilize,
  unlock, supercharge. Name the concrete behavior instead.
- **The "not just X, it's Y" frame.** And its cousin "more than just".
- **Hedge stacks.** "generally typically usually" piled together. Commit or cut.
- **Over-bolding.** Bold for one or two real signals per section, not every noun.
- **Echo summaries.** A closing sentence that restates the heading it sits under. (A sentence that
  points *forward* to the next verb or page is not an echo — that one is required in newcomer prose.)
- **Robotic triads.** Forced three-part parallelism where two items, or four, is the honest count.
- **Provenance as adjective.** "authoritative source", "definitive reference", "the canonical truth
  on X", "well-established fact". State the predicate and let `sources` / `confidence` speak.
- **Inline re-definition.** Re-explaining a term that already has its own page or a
  `docs/GLOSSARY.md` row instead of `[[wikilinking]]` to it. The gate catches banned strings, not
  duplicated definitions — this one is on you.

## Vocabulary and registers (the gate enforces this)

[`scripts/validate-docs.sh`](../../scripts/validate-docs.sh) checks the words, not just the links.
Tone edits must keep it green:

The gate's banned and discoverability lists are the source of truth — read them in
`scripts/validate-docs.sh` (`BANNED_STRINGS`, `SEO_LEAK`); do not re-list them here, that would
fork them. The summaries below are reminders, not the list.

- **Glossary terms are canonical.** Use the term in `docs/GLOSSARY.md`; don't coin a synonym. New
  term? Add the glossary row first.
- **Keep the registers apart (Check 1, `SEO_LEAK`).** Discoverability words belong only in the
  README tagline, `plugin.json`, and `marketplace.json` — read the `SEO_LEAK` list in
  `scripts/validate-docs.sh` for the exact strings. Anywhere else, use the technical term ("vault",
  "wiki", "ingest"; "raw content" for source material). A marketing word on a technical surface
  fails the build.
- **No retired terms (Check 0, `BANNED_STRINGS`).** The `BANNED_STRINGS` list in
  `scripts/validate-docs.sh` is the source of truth. Retired marketing synonyms and old
  `llm-wiki-*` skill names are banned outside `CHANGELOG.md` / `docs/adr/`. Reword by the real
  verb (`ingest`, `query`).
- **Namespace slash commands (Checks 3/4).** Always write the full prefix — `` `/claude-wiki-pages:ingest` ``
  — never the bare short form, and only reference a command that resolves to a real skill/agent/command.
- **Layer names are Title Case (Check 2).** Write "Layer 1 — Data" (Title Case with the canonical name),
  not a lowercased informal synonym.
- **Counts are load-bearing (Check 5d).** A stated count must match reality, and the repo's own
  "23 vs 24 vs 25 skills" drift shows how fast it rots. Prefer "single-responsibility skills" over a
  hard number; state a count only where a diagram or table needs one.

The glossary's Technical/Discoverability split governs *which words* a surface may use; this skill's
explanatory/engineer split governs *how* you write for a reader. Both apply at once.

## Writing a wiki page

A wiki page is a typed page an engineer reads to learn one thing. Same voice, applied to the vault:

- **Open with the class definition** in plain language — name what the page *is* when that
  disambiguates: a `concept` page opens "X is a …"; an `entity` page of `entity_type: tool` opens
  "X is a tool that …". One sentence that carries the ontology, not a second frontmatter.
- **The opening sentence stands alone.** A reader who follows zero links still learns what the page
  is. Links add depth; they do not carry the definition.
- **Stay in the engineer register for the body.** Exact terms, typed content, no marketing. The
  vault is not a landing page.
- **Never assert an uncited fact.** Every non-source claim names its `sources`. If you cannot cite a
  `raw/...` file via `_sources/`, do not write the sentence — flag it for ingest instead.
- **Provenance language is factual.** "Derived from `raw/...`" — state the source, don't sell the
  claim. Confidence and `sources` are facts, not adjectives.
- **One fact, one home.** Say it once on its own page; everywhere else, wikilink to it. Don't
  restate a definition you can link.
- **End a synthesis or query answer with a `## Sources` heading** — cite each consulted page as a
  `[[wikilink]]` plus its raw path, numbered, no prose between citations. The Sources list is a
  record, not a paragraph.
- **Match the template.** The page is an instance of its ontology class; write to its template, not
  around it.

> Before: "This clearly proves X is the best approach."
>
> After: "X. Derived from [[Source Note]] (`raw/foo.md`); confidence 0.6."

## Before / after

Explanatory:

> Before: "claude-wiki-pages is a powerful, seamless plugin that leverages a robust four-layer
> architecture to unlock effortless note organization — more than just a wiki."
>
> After: "You curate the sources. The plugin maintains the wiki, and hooks check the schema on every
> write. Four layers, each catching a different kind of mistake."

Engineer:

> Before: "It's worth noting that the firewall generally tends to confine writes, which is a really
> important security feature for keeping things safe."
>
> After: "`firewall.sh` confines every write to the resolved vault (`PreToolUse`, fail-closed). A
> write outside the vault is blocked before it lands — see [SECURITY.md](../../SECURITY.md)."

## The one check

Read it aloud. If it sounds like a person who understands the system explaining it on purpose, ship
it. If it sounds like a press release or a generated abstract, rewrite it.

For a wiki page, one more read: could a reader follow every claim back to a `raw/` source, and is
every term that has its own page a `[[wikilink]]` rather than a re-definition? That is the
provenance-and-single-sourcing equivalent of the aloud test.
