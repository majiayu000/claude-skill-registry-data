---
name: deslop
description: "Edit Ascribe's prose so it says what a thing does: the docs in docs/content/, the site's pages in site/home/content/, the README, and the packages' descriptions. Finds the patterns models write in place of a fact (\"serves as\", \", ensuring…\", \"robust\", \"it's important to note\", vague attribution, \"not X, but Y\") and fixes them without stripping the conditions docs need. Use when asked to deslop, de-AI, tighten, or edit a page for tone, when reviewing prose a model drafted, or before opening a pull request that adds or rewrites a page."
---

# Deslop Ascribe's prose

The rule is the house style's: say what a thing does. Most of what reads as AI writing is a model saying something vaguer than the fact it had: "serves as" where "is" was true, "ensuring consistency" where a mechanism should be named, "robust" where a limit should be stated. In docs, those aren't matters of taste. They change what a reader believes about the software. Fix them because they're wrong or empty, not because they sound like a model.

The research behind this skill is [AI writing tells in technical docs](../../../project-docs/reports/AI%20writing%20tells%20in%20technical%20docs.md). Three of its findings shape everything below:

- **Measurements support few tells.** Evaluative words ("delve", "showcase", "crucial") and tacked-on "-ing" clauses are measured at several times the human rate. Most other tells, including "not X, but Y", have never been measured, and none has been measured in docs.
- **Word lists go stale.** Each model has its own favorite words, so this skill names kinds of word, not a list to grep for and forget.
- **Over-correcting is its own tell, and it breaks docs.** A pass that deletes every hedge, adverb, and contrast strips "usually", "unless", and "pass the path, not its contents", which are conditions the reader needs.

## What not to touch

- Code blocks, code spans, commands, and output from `@snippet`.
- Frontmatter, directive lines, `{phrase}` keys, link targets, and ids.
- Anything under `docs/content/_generated/`: fix its source instead.
- The headline and the opening sentence in `design/words.toml`, which every surface is tested against. Changing them is a decision for `project-docs/brand/story.md`.
- A fact you can't check. If a sentence is vague because the fact is missing, ask, or leave a note in your report; don't invent the specific.

## The pass

Work through a page in this order. Facts come first, because a wrong flag costs a reader more than any phrase.

1. **Check what the toolchain can.** Run `cargo run -q -p ascribe-cli -- check <file> --format concise`. For every command, flag, key, and directive the page names, confirm it exists: `--help`, `docs/content/_generated/`, or `cargo run -q -p ascribe-cli -- model docs`. An example's output should come from a `@snippet` of a tested file, not be typed in.
2. **Fix what hides meaning.** These are always worth an edit. See [Hides meaning](#hides-meaning).
3. **Fix what slows the reader.** See [Slows the reader](#slows-the-reader).
4. **Fix formatting that breaks scanning.** See [Breaks scanning](#breaks-scanning).
5. **On the site and the README, fix the rhetoric.** See [Site and README copy](#site-and-readme-copy).
6. **Reread what you changed.** Every condition and every fact the sentence had is still there. You haven't introduced a new pattern: a rewrite that turns three hedges into three short declaratives can be just as uniform. Run the check again, and `cargo run -q -p ascribe-cli -- check --config docs` (or `--config site/home`) before you finish.

A single hit is rarely worth an edit on its own. Look for density: three evaluative words in a paragraph, a ", ensuring" on every other sentence, bold labels on every list.

## Hides meaning

Fix each one by stating the fact it stands in for. If you don't know the fact, that's the finding.

| Pattern | Before | After |
|---|---|---|
| "Serves as", "acts as", "functions as" where "is" is true | The `[consumer]` table serves as the bridge to Astro. | The `[consumer]` table is what `@ascribed/astro` reads: the site's address, base path, and profile. |
| A trailing "-ing" clause claiming a benefit | Ascribe reads the file each build, ensuring examples stay current. | Ascribe reads the file each build, so the example is whatever the file holds now. |
| "Associated with", "related to" where a relation exists | the addresses associated with a build | the addresses a build published |
| An evaluative word where a spec belongs: robust, seamless, powerful, comprehensive, flexible, efficient | a robust check for broken links | a check that reports a link to a missing file or heading |
| An unspecific caveat: "it's important to note", "keep in mind", "note that" | It's important to note that results may vary. | With two builds and neither named `site`, `[editor] build` is required. |
| Stacked or templated hedges over deterministic behavior | This may typically cause the check to fail. | The check fails. |
| One thing called by several names | workspace … project … environment | project, every time |
| A list padded to three | fast, reliable, and scalable | Name what's true, however many that is. |

**Keep** a word when it's the precise one: "ensure the port is free" is an instruction, "critical section" is a term. **Keep** a hedge that carries real uncertainty, once: "usually", "unless you pass `--force`". The fault is the templated or stacked one.

## Slows the reader

| Pattern | Fix |
|---|---|
| Signposting and meta-commentary: "In this section, we'll…", "Here's what you need to know", "Let's" | Delete it and start with the content. The house style has no "let's". |
| A page that opens with a pointer: "Part of the [reference]…", "The commands that…" | Open with a sentence that says what the page covers; put the pointer second. |
| A first sentence that restates its heading: "## Caching" then "Caching is a feature that…" | Start with what the heading's thing does. |
| A summary closer: "In summary", "Overall", a recap paragraph | Delete it, or replace it with the next step. |
| Vague attribution: "teams report", "studies show", "developers love" | Cite the source, as a link, or state the claim without attribution, or cut it. `project-docs/reports/` holds the research the site cites. |
| A paragraph that adds no fact | Ask what the reader learned. If nothing, cut it. |
| A sentence over about 40 words, chained with commas and "which"; one that lists more than three things, or has more than one "which"; a paragraph over 120 words | Make it a list, or two sentences. Outside `contracts/`, the docs have no sentence over 45 words and no paragraph over 120. |

**Page type decides some of these.** The content model declares each page's type:

- A **tutorial** may open with its goal ("This tutorial builds…") and may close with one sentence on what the reader built. Nothing else may.
- A **how-to** opens with the task and puts its procedure in `@steps`.
- A **reference** page is plain description: no goal sentence, no closer, no persuasion.

## Breaks scanning

| Pattern | Fix |
|---|---|
| Bold scattered through prose | Bold only a UI label or a term at its definition. |
| A bold label on every list item, restating its own sentence | Drop the labels and let the sentences stand. A real term or option list keeps its `**Term**` labels, as Microsoft's guide prescribes. |
| A heading per paragraph, or headings that hold only headings | Merge the sections. |
| Several notes in a row, or a note that's ordinary prose | Keep the one that warns of something; fold the rest into the text. |
| Emoji in headings or lists | Remove them. |
| Title-case headings | Sentence case. |
| Em dashes | The house style uses none. Use a colon, a comma, parentheses, or a new sentence. |

Three items in a list is fine. A three-word adjective string in a sentence is the pattern.

## Site and README copy

The landing page, Why Ascribe, Credits, the README, and the packages' descriptions persuade, so the essay rhetoric shows up there. A technical reader discounts all of it.

| Pattern | Before | After |
|---|---|---|
| "Not X, but Y" against a claim nobody made | Ascribe isn't just a linter, it's a toolchain. | Ascribe checks pages, builds them, and previews them. |
| An aphoristic closer | What it lowers is the cost of leaving, not the risk of depending. | Ascribe is still a young dependency. |
| A staged reveal or a self-answered question | The result? Faster reviews. | Reviewers read the rendered page. |
| A false range | from solo writers to enterprise teams | Say who it's for. |
| Puffery and stakes: unlock, elevate, game-changing, best-in-class, effortless | Unlock a seamless docs experience. | Say the feature. |
| Strategy language from `story.md` leaking into copy | What leads changes with the reader. | Where to start depends on what you do. |

Two rules from `project-docs/brand/story.md` also apply: the site names no other tools, and every claim has something built behind it that a command's output can show.

A contrast that informs stays: "a link names the page's file, not its address" tells the reader what to write.

## A quick scan

These find candidates, not faults. Read each hit in its sentence.

```sh
grep -rnEi --include='*.md' "serves as|acts as a|, ensuring|associated with|it's important to note|keep in mind|worth noting|in summary|in conclusion|let's|delve|seamless|robust|powerful|leverage|utilize|crucial|pivotal|comprehensive|unlock|—" docs/content site/home/content README.md | grep -v _generated
```

Vale can hold some of these permanently, and an Ascribe check could hold the page-structure ones; issue [#1287](https://github.com/ascribed-dev/ascribe/issues/1287) tracks that. Until a rule is tuned on these pages, treat a hit as a suggestion.

## When asked to review rather than edit

Report findings by group, in the order of the pass, each with `path:line`, the sentence, and the rewrite. Say which ones you couldn't fix because a fact is missing. Don't report a single weak hit, such as one hedge or one three-item list, as a finding.
