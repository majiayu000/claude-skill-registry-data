---
name: academic-writing
description: Write or edit academic journal paper content matching a specific researcher's writing style. Use when drafting, revising, trimming, or polishing any part of an academic paper (Abstract, Introduction, Related Work, System Architecture, Methods, Results, Discussion, Limitations and future work, Conclusion). Use it for any prose meant for a paper, even a single paragraph. Triggers on requests to write paper sections, improve academic prose, draft manuscripts, rewrite paragraphs for journals, cut a section to a word budget, act on co-author comments about manuscript prose, or adapt content for peer-reviewed publication. Covers geomatics, environmental science, GIS, remote sensing, and related domains but the style principles apply broadly.
---

# Academic Writing Skill

Produces academic journal text matching the author's established style, analyzed from 11 published papers (2019-2026).

## How this skill is organized

This file holds what applies to every sentence you write: the hard rules, then the prose rules from voice down to word choice. Four reference files hold what applies only to a specific task. Read the ones the task needs.

| File | Read it when |
|---|---|
| [references/section-patterns.md](references/section-patterns.md) | Drafting or revising any named section (Abstract, Introduction, Related Work, System Design, Methods, Results, Discussion, Conclusions), reporting results, or applying document-wide formatting (abbreviations, numbers, captions, cross-references, headings). Each section entry gives its purpose, structure, length, and common faults, compiled from published writing guides and the author's reviews |
| [references/citations.md](references/citations.md) | Attaching, verifying, or renumbering citations, or formatting a reference list |
| [references/formalization.md](references/formalization.md) | Writing Methods, or defining any metric, operation, or structural property |
| [references/rewrites.md](references/rewrites.md) | Applying any prose rule below and needing the worked before/after pairs behind it |
| [references/phrase-bank.md](references/phrase-bank.md) | Needing a sentence template from the author's own papers |
| [references/docx-build.md](references/docx-build.md) | Writing or changing a script that builds the Word manuscript from Markdown: native equations (with [scripts/docx_equations.py](scripts/docx_equations.py)), equation numbering, figure and table layout |
| [references/checklist.md](references/checklist.md) | Before delivering any draft or revision. Mandatory. |

## Workflow

The author works in a loop: Claude drafts, the author comments, Claude revises. The steps below exist to make the first draft close to final, so the loop converges in one or two rounds.

1. If not specified, ask which section is being written and the target journal. The venue affects formatting conventions, word limits, and whether the double-blind anonymity rules apply. Read the paper plan, if one exists, for the storyline and the section's word budget.
2. Read the reference files the task calls for, per the table above. For any named section, read that section's entry in [references/section-patterns.md](references/section-patterns.md) in full before drafting.
3. **Plan before prose.** Write down the section's one-sentence message, the three to five points that carry it, and the details deliberately left out (see **Storyline and selection**). For a new section, or a restructure, show this plan to the author before drafting.
4. Draft or revise applying the rules below. **A revision also selects.** Keep every fact that passes the storyline test, and keep its meaning exact. Remove the details that fail it, even when the author wrote them or supplied them in notes: benchmark numbers in an Introduction, implementation details outside the system description, metrics that do not support the Results claim, single-event examples in Limitations. After the draft, list each removed detail in one line with where it belongs (Methods, a table, the supplementary material, or nowhere), so the author can restore it.
5. **Run the precision pass** (see **Precision** under Word Choice) sentence by sentence. Passing the checklist does not make a sentence precise.
6. Run [references/checklist.md](references/checklist.md), then the **academic-humanizer** skill to strip residual AI tells (over-claiming, intensifiers, clause-stacking, connective overuse) while preserving the evidence-bound academic voice. Report the word count against the budget.
7. **When the author comments, generalize the correction.** A comment on one sentence names a fault that recurs, so find every instance of the same fault in the section and fix them all in the same revision. When a correction teaches something these rules do not yet cover, propose adding it to [references/rewrites.md](references/rewrites.md).

## Hard rules

These are absolute. They hold in every section and need no judgment call. Everything after this section is guidance requiring judgment.

| Never | Instead |
|---|---|
| Semicolons | Two complete sentences |
| Em dashes (—) | Commas, restructuring, or two sentences |
| Colons in prose sentences | Rewrite as a complete natural sentence. **Exception**: before displayed equations and formal definitions |
| The modals "would", "could", "may", "might", and phrases built on them ("maybe", "might be", "could potentially") | The plain indicative, which states the general truth directly ("a checker that consumes them recomputes the answers"). For possibility, "can" or "does not necessarily" ("may fail to help" becomes "does not necessarily help"). Reserve "can" and "generally" for genuine scientific uncertainty |
| "I" | "We", "This study", "This paper" |
| Bullet points or numbered lists in the paper body | Flowing paragraphs, with inline markers ("First, ... Second, ...") for enumeration |
| Parentheses or brackets for supplementary or explanatory phrases | Integrate into full sentences. Parentheses are reserved for exactly four uses: (e.g., ...), (i.e., ...) always with the comma, citations, and abbreviations at first use |
| A fronted prepositional or scope-setting phrase with no comma | "For GPT-5.4-nano, the length control...", "On aggregation, the tool...". Mid-clause occurrences (after "while", "because") need no comma |
| Invented numbers, results, DOIs, authors, or page ranges | Verify, or say the detail is unavailable |

## Storyline and selection

A paper tells one story, and every section serves it (Mensh and Kording 2017). Detail is selected for that story. Completeness is not a reason to include anything.

- **State the section's message in one sentence before drafting**, then list the points the message needs, typically three to five. Everything outside that list is a candidate for deletion, for the supplementary material, or for the code repository.
- **Test each detail before keeping it.** Does the reader need it to understand, reproduce, or believe the central claim? If removing it changes nothing the reader concludes, cut it. Implementation details fail this test by default in the Introduction, the system description, and the Discussion: parameter values that do not affect the results, internal module names, edge-case handling, and the order in which the work was done.
- **Trim by removing whole minor points, never by shaving words from every sentence.** Shaving leaves choppy, imprecise sentences and saves little length. A trimmed section keeps fewer points and explains each one fully.
- **Give each level of detail one home.** The Introduction stays general, Related Work carries the specific findings of prior studies, the system description carries components and design, the experimental design carries conditions and metrics, Results carries the numbers, and the Discussion carries meaning. A number or detail appears in one section only, except that the Abstract and Conclusion restate the key results.
- **Write for a reader who does not know the work.** Define every term at first use, and limit the number of open threads the reader must hold.
- **Respect the word budget.** Know the venue limit and the per-section budget before drafting, count after drafting, and stay within about 10% of the budget.

### Section essentials

The core rule of each section, so it applies even before [references/section-patterns.md](references/section-patterns.md) is read. The full entries there take precedence.

| Section | Core rule |
|---|---|
| Abstract | Gap, what the study presents, approach, one or two key numbers, one direct implication sentence, within the venue limit |
| Introduction | General statements with grouped citations and no benchmark numbers. Components of the approach, never implementation. Objectives as "The first is ..., the second is ..., and the third is ..." |
| Related Work | Group studies by approach: one sentence describes the approach and cites two or three studies together in one parenthesis "(A et al. 2020, B et al. 2022)". A group holding a single study means the grouping is too fine, so merge it into a broader approach. Author-as-subject citations only for the one or two studies the paper positions against. Each thread closes on a plainly stated gap |
| System Architecture | Components that carry the contribution, in the order data flows, with a one-sentence rationale each. No file names, polling intervals, retry policies, formats, or configuration |
| Methods | Only methods whose results are reported, conditions named by their manipulation, metrics defined in prose by what they measure |
| Results | One claim per experiment. Report only the metrics that support it, detailed numbers in the table, no interpretation, identical condition names throughout |
| Discussion | Open with the general claim, then the mechanism, then one or two key studies, then the implication. No restated numbers |
| Limitations | Each limitation stated softly as scope of the current study, each mapped one-to-one, in order, to a concrete future direction. No single-event examples, no "further research is needed" |
| Conclusion | One paragraph of 150-200 words: what was done, findings as answers, implication, specific future work. Nothing new |

## Voice and Tone

- Use **third person** or **first person plural**.
- **Report findings in measured, neutral terms.** State the measured result ("low accuracy", "below chance", "frequent errors", "moderate accuracy") and cut editorial intensifiers and judgment words. Confidence means stating the finding plainly, not amplifying it. The number or comparison carries the weight, and an added intensifier reads as subjective. The specific tells ("poorly", "struggle", "cannot reliably", rhetorical "even" or "only", emphatic "do") are listed in the banned-words table.

## Sentence Structure

- **Write continuous sentences, not strings of short comma-separated components.** A sentence that accumulates inserted fragments (an appositive, a trailing "so ..." result, a "while ..." tack-on, a parenthetical-style aside set off by commas) forces the reader to reassemble it. Restructure into one flowing clause chain with real subjects and verbs, or split into two full sentences. Check every rewrite for this before delivering, because it is recurring reviewer feedback.
- **Say it the simplest direct way, and do not stack subordinate clauses.** This is the companion to the rule above and the two work together. Do not fragment a sentence into inserted pieces, and do not stack clauses to avoid fragmenting. The target in both directions is a plain sentence with a real subject and verb. Two or more subordinate clauses in one sentence (whose, which, that, since, where) is the signal to split it, and a trailing qualifier appended with "and we will ..." usually belongs in its own sentence. Simple here means plain structure and plain word choice, not informal tone.
- **Vary sentence length.** Acceptable range is 15-50 words, with occasional longer sentences in Methods.
- Favor **complex sentences** with subordinate clauses in Introduction and Discussion, where an argument genuinely has dependent parts. In Methods and Results, prefer the plain declarative, since a method reads as a sequence of things done.
- **State claims directly; avoid nominalized or inverted constructions.** An abstract subject hides the claim, so "The guarantees that make a DGGS valuable are the transitivity of..." becomes "A DGGS is valuable because containment is transitive...". The cleft is the same fault and slips through most often, so any sentence built on "is what", "is that", or a fronted "What ..." gets rewritten as plain subject-verb-object.
- **Keep in-sentence example lists parallel and self-explanatory.** Items must share one grammatical form and one level of generality. Never place a general capability ("reason about geography") in the same list as its own sub-examples, since the general term subsumes them. Every item must be understandable on first read without the reader guessing what it means.
- **Negate with the verb, not with a noun phrase.** The tells are a sentence opening "No X does Y", a verb whose object is "no ..." ("carries no relation to"), and a trailing "with no ... attached". Write "the standards do not make a grid cell the feature of interest". The test is whether the sentence would be spoken that way. Ordinary uses of "no", "none", and "without" are fine and must be left alone, so this governs the construction and not the word.
- **Cut qualifiers already implied by the verb.** "Infers these relations without computing them" is redundant because inferring already excludes computing. If the verb entails the qualifier, delete the qualifier.
- **Avoid same-root repetition within a sentence and across adjacent sentences.** After any word swap, re-scan the sentence and its neighbors for new collisions (replacing "checks ... checked" can create "verification ... verified"). Distribute distinct verbs across neighboring sentences (determined / computed / verified / evaluated).

### Defensive framing (highest priority)

Defensive writing is the single most reliable AI tell in academic prose. A reviewer registers it before being able to name it, and a manuscript that reads as machine-written loses credibility regardless of its content. The goal is not to eliminate contrast entirely but to push it low enough that no reader can detect a pattern.

- **Assert positively. Do not define a claim by what it is not.** The recurring shapes are the appended negation ("X, not Y"), habitual "rather than", "instead of", and "as opposed to", the inversion "it is not that A, but that B", the pre-emptive disclaimer ("this is a case study, not a general law"), and the concessive opener ("While X holds, ..."). In almost every case the positive half already carries the meaning, so delete the negative half and let the claim stand.
- **Budget the contrasts across the manuscript.** Roughly one per major section, and only where the contrast is itself the finding: a comparison against a named baseline, a distinction the field routinely conflates, or a scope boundary the reader would otherwise get wrong. Every other occurrence loses its negative half. Count them before delivering.
- **Where a contrast must stay, recast it so the connective disappears.** "computed rather than estimated" becomes "computed directly from the cell geometry". The information survives and the defensive shape does not.
- **Do not append a corrective fragment to a finished sentence.** A sentence that closes with a comma and a qualifier ("..., though only at coarse resolutions", "..., not a claim about all grid systems") reads as pre-empting a reviewer. Fold the scope into the sentence's own subject and verb, or move it to the Limitations subsection, where each caveat appears exactly once.
- **Do not defend the method before reporting it.** Justifying a design choice against alternatives that no one raised ("we did not use a quadtree because ...") signals anxiety. State what was done and why it fits the problem, and reserve alternatives for the Discussion, where a comparison is expected.

## Paragraph Structure

- **Topic sentence first**: each paragraph opens with its main claim or purpose. **Evidence and detail in the middle**: supporting data, citations, or elaboration. **Link at the end**: a transition or implication that connects to the following paragraph.
- **Target 4-8 sentences per paragraph** in Introduction and Discussion, shorter in Methods. If a paragraph is one or two sentences, or two or three lines on the page, or a subsection is broken into many small paragraphs, merge them into fewer, fuller paragraphs. The author tends to over-split, so check every paragraph break in text the author wrote too. A short subsection reads best as a single paragraph. Keep a short paragraph standalone only when it carries a distinct point that merging would dilute.

Openers:

- **Make each paragraph opener follow naturally from the preceding paragraph.** A topic sentence that drops in cold ("Facts+CoT (C2) improves accuracy unevenly...") reads like a bullet point that is then elaborated. Tie it to what came before with a transitional phrase, a named contrast, or the next item in an established sequence ("The remaining prompting condition, Facts+CoT (C2), ...").
- **Spell out referents in a paragraph opener.** Do not open a paragraph with anaphora that leans on the previous paragraph ("A DGGS can supply both"), because across a paragraph boundary the antecedent is too weak. Write out what the words refer to ("both the structure and the verification").
- **Do not open a paragraph with a very short sentence** that is then elaborated, whether conclusory ("The cost is concentrated and concrete.") or a framing count ("Two qualifications bound this result."). This is a common AI tell. Lead with the substantive sentence instead, folding any framing into it (for example, start with the first qualification and signal the second with "also").
- **Do not open a section with a paragraph that only summarizes the subsections that follow.** A section lead-in earns its place only when it carries content not repeated below, such as framing, a foundational definition, or a message that spans the subsections. If it just lists what each subsection covers, cut it and let the subsections speak.

Cohesion:

- **Each sentence must connect to the one before it and the one after it.** A paragraph of individually true, individually well-written sentences still fails when the reader cannot see how they relate, and this is the most common complaint on otherwise clean drafts. The cause is almost always a sentence that opens a new grammatical subject and leaves the relation for the reader to reconstruct. Three repairs, in order of preference: **carry a noun forward** from the previous sentence and make it the new subject, **point back with a demonstrative that names what it points at**, or **state the relation with a connective that carries meaning**, never "In addition" or "Also", which signal one more item in a list and are the weakest available link when the real relation is cause, consequence, or contrast. The diagnostic: read only the first four words of each sentence in order. If that sequence alone does not trace the argument, the links are missing.
- **Every sentence must do a job the argument would miss, and a concession has to be stated as one.** Two sentences that each carry a fact can still read as isolated, because the reader cannot see what work they are doing. The usual cause is an unstated concession: a fact was included to acknowledge a counter-case, but the acknowledgement was left implicit, so the sentence looks like a stray observation. Name the concession and let the next sentence answer it. The diagnostic: delete the sentence and read the paragraph. If the argument does not notice, the sentence is either filler or in the wrong place. A concession earns its place only against an objection a reviewer will raise from the cited literature. Defending against an alternative nobody has proposed is the separate fault covered under Defensive framing, and it reads as anxiety rather than rigour.
- **Put old information first and new information last.** Readers take the start of a sentence as the topic, which links back to what they already know, and give the most weight to its end, the stress position (Gopen and Swan 1990). Open with the carried-forward noun and close with the point the sentence exists to make. Keep the subject and its verb close, because material between them reads as an interruption.
- **Do not join two different kinds of fact with "and".** Pairing a scope limitation with a performance measurement in one sentence makes the reader feel the seam without being able to name it. Group facts of the same kind into one sentence, give a different kind its own sentence, and link the two.

## Word Choice

### Precision (highest priority)

The author reads every content word and asks what it denotes. A sentence can be free of banned words, defensive shapes, and hard-rule violations and still fail on every word, so the checklist does not certify precision. Precision means each word admits one reading in context and that reading is true of the system and the evidence. Plain words are preferred to fancy ones, but plainness does not excuse inexactness.

- **Choose the plainest accurate word, and weigh every word before proposing it.** For each content word, ask whether a plainer word says the same thing exactly ("represent", "define", "specify", "use", "provide"). If it does, use it. Fancy or technical-sounding verbs ("instantiate", "expose", "contribute recovery"), software jargon ("checkpointer", "quality gate", "oracle", "engineering stack", "runtime", "artifact", "unattended"), and opaque abstractions ("enumerate over the spatial dimension", "analytical retrieval") all fail this test. Also reject a plain word that carries a reserved meaning in the venue's field: in GIScience, "data model" means vector versus raster or object versus field models, so a heading about how datasets are stored uses "DGGS-indexed data". Plainest does not mean least exact: when the plain word claims something false, choose the next plainest true one ("represent" over "define" when the fields do not define the dimensions).
- **Test every content word against what it denotes in the study.** For each noun, verb, adjective, and interrogative, ask what exactly it names and whether a reader in the field takes it to mean something else. "The spatial accuracy of an LLM agent" fails twice, because spatial accuracy in GIScience means the positional accuracy of coordinates, and an agent has no positional accuracy. The intended claim is "the reliability of spatial reasoning by LLM agents".
- **Choose the word that names the mechanism.** "Depends on where its spatial relations are computed" names a location when the claim concerns a method. The exact version is "depends on whether spatial relations are inferred by the LLM or computed from cell identifiers". Interrogatives (where, how, whether) and prepositions carry meaning and get the same test.
- **Name objects by their technical names.** "Cell corners" becomes "the vertex coordinates of the cell polygons". In a general claim, generalize the domain instance to its class, so "facility points" becomes "points".
- **Name experimental conditions by what each one does.** A condition label must describe its manipulation truthfully. "Coordinate grounding" contradicts itself when that condition has no grounding, so the pair becomes "DGGS-grounded" and "coordinate inference". Name results by the experiment that produced them ("the results of the grounding experiment", not "the grounding results").
- **Keep internal vocabulary out of the prose.** Codebase and lab terms ("runtime", "harness", "run store", "world channel", "wake") and generic software roles ("dispatcher", "daemon", "job queue") are not journal vocabulary. The same holds for result labels coined in the lab ("the ablation results"), which become "the results of the ablation experiment". Ask whether a reviewer outside the project knows the term. If not, name the actor in field terms ("GridMind determines the recipients") or define the term once and keep it. Never reuse a term the paper has reserved for a defined concept, such as "channel" for anything outside the defined communication channels.
- **Prefer the literal verb to the figurative one.** "The prevailing response couples LLMs with external spatial computation" has no checkable word: response to what, couples how, which computation. The literal version says who does what: "recent studies connect LLM agents to external tools that compute spatial relations". Figurative verbs to replace include couple, tackle, drive, shape, unlock, fuel, and "let" constructions ("lets agents act"), which read as casual. Write "allows", "enables ... to", or make the actor the subject.
- **Write the general claim generally, then narrow.** The opening sentence of a Discussion subsection states the finding beyond this study ("depends on whether spatial relations are inferred by the LLM or received as facts computed from a known spatial topology"), and later sentences give the study's specifics.
- **Run the precision pass sentence by sentence, never by scanning.** For each sentence, (1) mark each content word, (2) state what it denotes in this study, (3) replace it if its field meaning differs, if it is figurative, or if the reader must guess its referent, and (4) confirm the sentence claims exactly what the evidence shows, no broader and no vaguer. Then reread the paragraph, because a replaced word can break a neighbouring sentence.

### Preferred vocabulary

- Research verbs: "determined", "quantified", "evaluated", "investigated", "examined", "explored", "revealed", "indicated", "assessed".
- Describing system capabilities or what the paper does: "presents", "introduces", "demonstrates" (the application of X), "integrates", "enables", "supports", "achieves", "highlights", "reflects".
- Comparing to prior work in the Discussion: "aligns with", "is consistent with".
- Methods and tools: "adopted", "employed", "utilized" (not "used" repeatedly).
- Causal relationships: "contributed to", "resulted in", "led to".
- Transitions: "nonetheless", "however", "in contrast", "in addition", "furthermore", "accordingly", "consequently", "overall". Use "namely" to specify or clarify within a sentence.
- **Vary transitions.** Do not start sentences with "Additionally" or "Moreover" excessively, and do not repeat the same transition word in consecutive paragraphs.

### Banned words and phrases

Rows are grouped: filler phrases, then reporting tone, then over-claiming, then word swaps, then AI vocabulary, then constructions and naming. The last four rows index a construction rule explained above; the row is the lookup, the section is the reasoning.

| Do not write | Write instead |
|---|---|
| "So", "Basically", "Actually" as transitions | Formal transitions from the list above |
| "It is worth noting that", "It should be noted that" | State the point directly |
| "Together, ..." or "Taken together, ..." opening a summary sentence | Start with the subject ("The three turns demonstrate...") |
| Filler connectives ("therefore", "thus", "as such") when the sentence stands without them | Cut them |
| "poorly", "struggle(s) with", "cannot reliably" when reporting findings | The measured result: "with low accuracy", "remain unreliable on", "frequent errors in" |
| Rhetorical "even" or "only" attached to a finding ("cannot compose even two relations", "only moderate accuracy") | Drop the intensifier and state the finding ("frequent errors when composing pairs of relations", "moderate accuracy") |
| Emphatic "do/does" before a verb ("the examples do help") and unquantified degree adverbs ("well below", "far below", "at once") | Drop the emphasis or state the magnitude ("remain below ceiling", a number) |
| "significantly" without a statistical test; empty intensifiers ("strong results", "extensive experiments") | A specific number, range, or neutral verb |
| Casual or promotional phrasing ("a case study, not a general law", cost asides like "for less than two dollars") | Cut, or restate neutrally |
| "prove", "demonstrate", "establish", "confirm" for empirical claims | "show", "provides evidence". Exception: "demonstrates" is fine for what the paper does ("this paper demonstrates the application of X"), just not for empirical findings |
| "yet" | "but", "however", or a new sentence |
| "yield" | "produce", "give", "result in" |
| "check(s)", "checked" as the workhorse word for validation in prose | "verify/verification", "determine", "evaluate", professional but plain |
| "supply", "supplied" | "provide", "given" |
| "pair(s)/paired with" as a verb meaning "put together" ("pairs grids with agents", "a chain paired with a cell") | "combines", "integrates", or restructure ("consists of A and B"). Keep "pair" only for genuine two-element objects (pairs of relations, region pairs, chain-condition pairs) and fixed statistical terms ("paired test") |
| "elicit", "elicitation" for getting answers from a model | "request", "prompt for", "prompting strategies" |
| "serves as", "emerged as" | The copula: "is", "are" |
| "anchor", "anchoring" (overused) | "ground", "base on", "guided by", "tie to", "computed from" |
| "thrust" for a research direction | "direction", "line of work", "objective", "aim" |
| AI-favorite words: "leverage", "delve", "realm", "pivotal", "underpin", "harness" (noun), "seamless", "robust" without a metric, "intricate", "landscape" only as a metaphor (the research or data landscape, never physical terrain), "tapestry", "showcase", "underscore", "myriad" | The plainer word that says the same thing; keep one only when it carries real meaning |
| Shortened model or product names in prose ("Nano", "mini" alone) | The full registered name at least once per paragraph ("GPT-5.4-nano"); short forms only where the paper has established them |
| Noun-phrase negation ("No X does Y", "carries no relation to", "with no uncertainty attached") | Verb negation. See **Negate with the verb** under Sentence Structure |
| Negative-contrast constructions ("X, not Y", "X rather than Y", "instead of Y", "as opposed to Y", "it is not that A, but that B", "While X, ...") | Drop the negative half and state X. See **Defensive framing** |
| Evaluative comparatives with no metric ("has moved furthest", "the harder ones to build on", "the most advanced") | The named state or deficiency the source reports. See **Replace evaluative comparatives** under Terminology and Claims |

## Terminology and Claims

Fixing terms:

- **Fix each key term at first use** and keep it consistent. Do not let a term drift across sections. Keep organizational-author abbreviations consistent too: if an abbreviation's first-use definition is removed, update every downstream use so it is not left undefined.
- **Gloss a load-bearing term by stating its defining property at first use.** "Congruent" should arrive with "each parent cell is exactly the union of its child cells", so the reader learns the property, not just the label.
- **Name the object, not the shorthand, in structural relations.** Write "the union of its child cells" and "the sum of its child values", not "the union/sum of its children", and say precisely what is unioned or summed. Bare shorthand ("children") may pass deep in technical sections, so judge each occurrence.

Choosing terms:

- **Use commonly accepted terminology, not coinages or niche phrases.** Terms like "locative language" or "chaining spatial relations" force the reader to guess. Prefer the field's standard term, or plain accurate words when no standard term exists. The same applies to verbs: an uncommon verb ("delegated to models") loses to a plain exact one ("performed by"). Plain English means simple, accurate word choice, not informal tone.
- **Name the paper's recurring concepts with the terms mainstream papers already use.** A term repeated throughout the paper (the agent's turn, its memory, its set of actions, the record of a run) must be the one readers know from the literature, because a private term on every page makes the paper read as foreign. Before settling such a term, search how recent papers in the field name the concept and adopt the dominant term: "action space" for the set of actions an agent can take, "activation" for an agent's turn in an event-driven system, "event log" for the record of messages and state changes, "structured state" for memory with fixed fields, "role system prompt" for standing instructions per kind of agent, "large-scale multi-agent system" for systems of hundreds of agents. Keep a coinage only when no field term exists or the field term means something else (for example "policy" means the decision function in agent research, so it cannot name a prompt).
- **Define every coined or project-specific term at first use and keep it.** A term the paper introduces (a named channel, condition, or component) needs a one-sentence definition by its defining property where it first appears, and then the same wording everywhere. A term the author decided to keep, such as a defined component name, is not reopened later.
- **Replace a term everywhere the reader sees it.** A terminology change covers the prose, the figure and table captions, table header and body cells (main text and supplementary), the axis and legend labels of plotted figures (regenerated from their scripts), and the text inside drawn figures. Grep every source and check the rebuilt documents before reporting the change done. Watch for collisions: a new term can clash with an existing label (renaming "wake" to "activation" required renaming the action "Activate child" to "Enable child"). Code identifiers quoted as identifiers stay unchanged.
- **Fit field terms to the target venue.** A framing term native to a neighboring field (for example, "Digital Earth" in a GIScience journal) signals the wrong audience. Use the venue's own register for umbrella terms.
- **Do not carry metaphors or codenames from the experiments, codebase, or internal notes into the paper.** A vivid internal label (a "ladder" of model variants, a "hero" run) reads as informal. Replace it with a neutral academic term ("variant sequence") and keep the internal name only in code and filenames.
- **Avoid informal collective nouns and borrowed jargon.** Colloquial counts like "trio", "duo", or "the big three" should be the plain form ("the three undeclared-unit datasets"). Terms borrowed from another field's methodology, such as an experimental "arm" (clinical trials), read as jargon, so prefer "condition", "configuration", or "variant". When unsure whether a word is standard terminology or a metaphor, treat it as a metaphor and choose the plain academic term.

Making claims checkable:

- **Every abstract noun phrase must be checkable.** If a phrase requires the reader to reconstruct what it points at, it is not written yet. "The data model above the grid" became "the data model that gives cell values their types, units, and relationships". This is the most frequent failure in compressed prose, because compression is what strips the words that made the noun concrete.
- **Write what the source measured, not what the field believes.** Before writing any superlative or adoption claim, find the sentence in the source that supports it. If the source says something narrower, the narrower version is the claim.
- **Replace evaluative comparatives with the property the source names.** "Storage has moved furthest in practice" states a judgment a reader cannot check. Write the named state or deficiency instead ("storage is the most developed layer"). The rewrite is usually the same length and always more informative.
- **Every claim carries a number, a citation, or a mechanism.** Do not write vague claims without evidence ("X is very important").
- **Do not assert background claims the argument does not need.** A contestable historical or contrastive framing (for example, "spatial reasoning once handled by deterministic geometric methods is being ...") invites objections without carrying the point. State what is, and what the evidence shows, and drop the framing.
- **Do not let phrasing imply exclusivity.** "Decisions depend on X and Y" reads as depending only on X and Y. Keep the head noun general (for example, "operations over spatial units") and place the paper-specific instances after "such as", where they read as examples and not an exhaustive list.

## Anonymity for Double-Blind Review

- When the target venue uses double-blind review, never reveal author identity. Do not write "our prior work", "our previous pipeline", or "we previously showed" about the group's own published work.
- Cite the group's own prior work in the third person, exactly like any other source ("a recent effort harmonized the inventories ... (Li et al., 2026)").
- Sweep every section, not just the Introduction. Common leak sites are the abstract, related-work positioning, methods provenance ("our tools"), and the discussion ("in our prior pipeline").
