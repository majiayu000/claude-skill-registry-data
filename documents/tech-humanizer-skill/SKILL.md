---
name: tech-humanizer-skill
description: Use this skill when the user asks to humanize, rewrite, de-AI, polish, or detect AI writing in documents, emails, chat messages, pull request text, release notes, technical docs, or other prose. It removes AI-writing markers while preserving technical terminology, reports AI-marker density with concrete fixes, and learns the user's wording preferences, domain terms, and recurring writing habits over time. Don't use for grammar correction unrelated to AI markers, original content generation, fact-checking source material, or translating between languages.
version: 2.4.0
author: ClydeShen
license: MIT
---

# tech-humanizer-skill

Turn AI-shaped prose into credible human writing without flattening useful technical language.

Use this skill for three jobs:

- **Humanize**: rewrite documents, emails, messages, technical docs, PR descriptions, release notes, and similar prose.
- **Detect**: estimate AI-marker density and give targeted rewrite suggestions.
- **Learn style**: maintain a local writing profile for user preferences, domain terms, syntactic DNA, and recurring corrections.

## Load Order

**Preflight (do not skip):** before any rewrite of technical text, actually read the references — do not apply the skill from memory. At minimum load `references/ai-style-lexicon.json`, `references/technical-terms.json`, `~/.tech-humanizer/user-profile.json` if one exists (personal writing habits, shared across all projects), and the project's `writing-profile.json` if one exists (domain terms local to this project only). Working from memory is how plain verbs get over-formalized (`get` -> `retrieve`) and protected terms get lost.

Read only what the task needs:

- Humanizing (RECURSE): read `references/bucket-quickref.md`.
- Humanizing or detection (detail): read `references/ai-markers.md`.
- Humanizing output: also read `references/rewrite-playbook.md` and `references/final-rubric.md`.
- Channel-specific rewrites: read `references/channel-style.md`.
- User states the audience's language level or non-native status: also read `references/reader-level.md`.
- Text with citations, links, Markdown, HTML, wiki markup, or source claims: read `references/source-and-markup-integrity.md`.
- Strict marker lookup or scripted scanning: read `references/ai-style-lexicon.json`.
- Technical or product text: also read `references/technical-terms.json`.
- User asks about profile behavior or persistent learning: read `references/profile-schema.md`.
- Terminology alignment: read `CONTEXT.md`.
- Detection reports: use `assets/detection-report-template.txt` when the user needs a structured report.
- Validating this skill as a repository maintainer: run `python scripts/validate.py`.

## Core Principles

- Preserve exact technical terms, product names, acronyms, code identifiers, CLI flags, API names, and domain-specific jargon unless the user explicitly asks to change them.
- Replace AI markers with specific, grounded, author-like language. Do not merely swap one fancy word for another.
- Prefer direct claims over ceremonial framing, vague attribution, generic importance claims, and assistant-style service language.
- Match the target channel: a Slack message should sound different from a client report, release note, or engineering design doc.
- Keep the user's intent and risk posture. Do not soften warnings, remove constraints, or alter commitments.
- Prioritize authentic technical voice over detector evasion. Do not artificially inflate perplexity or burstiness scores to game AI detectors; natural sentence-length variation and precise word choice are legitimate writing goals.

## Voice Profiles (per scenario)

Humanizing has two layers: **removing AI markers is universal** (every output gets it); **voice is per scenario** (selected by scenario classification — see workflow step 1). There is no single global target voice. A dry, unapologetic engineering voice is right for a design doc and wrong for a casual chat reply (reads cold) or a client email (reads rude).

Each channel carries its own short voice profile. See `references/channel-style.md` for the per-channel profiles; the main ones:

- **Team chat / casual** -> warm, brief, natural shorthand, one clear next step.
- **Client email** -> professional, courteous, clear ask, no padding.
- **Technical doc / design doc / PR review** -> *Senior Engineer Voice* (below).
- **Release notes** -> neutral, factual, user-visible change first.

### Senior Engineer Voice (one profile among several)

The positive target for **engineering and technical** channels only — not a universal default.

- **Lead with the constraint, not the category.** Do not say "there are performance considerations." Say "this will timeout after 30s under load."
- **Opinions without apology.** A senior engineer takes positions. "I would use Postgres here" not "one option is Postgres."
- **Incomplete is fine when incomplete is true.** Leave open questions open. Do not resolve ambiguity the user did not resolve.
- **Repetition over rotation.** Use the same precise term twice rather than inventing a synonym. "The cache" is always "the cache."
- **Dry beats enthusiastic.** Understatement signals confidence. "This works" is stronger than "this is a powerful solution."

Syntactic DNA governs rhythm and passage-level structure (sentence length, punctuation habits, pacing, what this user characteristically leads with). The selected voice profile governs content decisions (claim scoping, position-taking, warmth) where syntactic_dna is silent. The two mostly operate on separate axes; where they do overlap (e.g., what to lead with), a captured syntactic_dna habit for this specific user wins over the generic voice profile default.

## Humanize Workflow (STRIP -> PROTECT -> DRAFT -> RECURSE)

1. **Classify the scenario** -- This is the first decision and it drives everything after it: **register and voice**. If the user names the channel, use it. Otherwise infer from signals; do not default to technical documentation.

   **Signal checklist** (read the input, not the request):
   - **Length**: a line or two -> chat; multiple paragraphs -> doc/email.
   - **Greeting / sign-off present** ("Hi X", "Thanks,") -> email or message, not a doc.
   - **Platform cues**: Slack/Teams shorthand, @mentions -> chat; "## headings", code fences -> technical doc; "## Changed/Fixed" -> release notes.
   - **Person**: heavy 2nd person to an external reader -> client email; 1st-person team voice -> chat/PR.
   - **Question vs statement**: a request/ask -> message or email; a record of decisions -> design doc.
   - **Audience**: teammate, reviewer, client, end user, or public reader.

   **Disambiguate within engineering voice.** Technical doc, Design doc/RFC, PR description, and PR review comment all share Senior Engineer Voice, so "## headings, code fences" alone under-determines which one this is. Break the tie with structure, not just tone:
   - **PR description**: what changed / why / how it was tested; often has a diff or file list as context.
   - **PR review comment**: short (1-3 sentences), addressed to a specific line or change, names a requested action.
   - **Design doc / RFC**: contains a decision, named alternatives, or a tradeoffs section; written before the change exists, not after.
   - **Technical doc**: describes how something works or how to use it; no "why we chose X over Y" framing.

   If two channels still tie after this check, ask which one rather than silently picking. Do not default to technical documentation.

   Map the scenario to its voice profile (see **Voice Profiles**) and load that channel's section from `references/channel-style.md`. Removing AI markers (STRIP) is universal regardless of scenario.

   **Reader language level (separate axis, explicit only).** If the user states the audience's English level or non-native status (e.g., "for a B1 team", "readers are non-native engineers"), also load `references/reader-level.md` and apply it alongside the channel voice -- it adjusts sentence structure only, never technical-term density. Never infer a reader's language level from the text itself; apply this axis only when the user states it.

2. **STRIP** -- Remove unconditionally on every pass: I1 (assistant service language), I2 (knowledge-cutoff disclaimers), I3 (placeholder residue), I4 ceremonial openers where they add no meaning, M1-M3 (markup leaks, broken citations, internal tokens). Also remove regardless of score: emoji (remove entirely), em dashes (replace with comma, colon, or parentheses), curly quotes (replace with straight ASCII quotes), S12 decorative unicode enumeration glyphs -- bullet dots, circled numbers, geometric arrows -- (replace with standard Markdown lists). See severity **High** in `references/ai-markers.md`.

   **Product copy channels:** Do not invent product names or brands not present in the source draft. If the draft has no product name, frame the product descriptively — e.g., "this double-walled travel mug," not an invented brand like "CommuterShield." A source pattern that describes a human example "adding a product name" licenses descriptive framing only; it is not permission to invent a name. Remove product-copy formula phrases (Perfect for, Ideal for, Introducing, Designed for) as AI markers.

3. **PROTECT** -- Load `references/technical-terms.json`, the project's `writing-profile.json` (`domain_terms`), and `user-profile.json` (`syntactic_dna` and other personal fields, when present). Lock protected terms and apply explicit preferences. Also lock verbatim-required phrases before drafting: safety instructions, legal scope terms, the draft's central claim. See `references/rewrite-playbook.md § Verbatim Preservation` and `§ User Correction Handling`.

   **Generic skill, per-project terms.** The skill ships only generic terms in `references/technical-terms.json`. Project-specific vocabulary lives in the per-project `writing-profile.json` under `domain_terms`, which **extends** (does not replace) the generic list — the two are merged at load time, with `domain_terms` winning on conflict. Never add project-specific vocabulary, personas, or document types to the skill's own references, and never write `domain_terms` to `user-profile.json` — it stays project-local.

   **Clinical/legal/safety terminology:** When a reference provides specific professional terms (e.g., "prescribing clinician", "hold harmless", "sentence-length diversity"), treat those as required verbatim — do not substitute colloquial or near-synonym equivalents. Reference terms take priority over synonyms in the draft: if the reference says "prescribing clinician," use that exact phrase even if the draft says "your doctor." These terms carry precision the author chose deliberately.

4. **DRAFT** -- Rewrite with lead-fronting, active voice, and channel fit. Load `references/rewrite-playbook.md`, `references/final-rubric.md`, and `references/channel-style.md` when the channel is clear. Load `references/source-and-markup-integrity.md` when sources or markup matter.

   **Voice (limited):** Vary sentence length; lead with facts or actions; prefer one concrete detail over abstract triples; use first person only when the channel and profile allow. Do not invent facts, metrics, or anecdotes.

   **Channel-fit voice:** For forum and conversational channels, write as a participant making a felt observation — not an analyst explaining. Let rhythm and phrasing demonstrate the point rather than describe it. Vary sentence length aggressively: the gap between the shortest and longest sentence in a passage should span at least 6 words. Include at least one sentence under 8 words and at least one over 15 words. For casual explanation channels with a directional opinion in the source, explain the causal connection between mechanism and effect — commit to the position rather than hedging. Stating only the outcome ("can feel less distinctive") is neutral; naming the cause ("the model always picks what's most probable, so the result regresses toward plausible rather than distinctive") commits to a position.

   **Study claim scoping:** When source material references a specific corpus, study, or named author, keep every empirical claim scoped to that source. Preserve comparison entities from the draft (e.g., do not replace "ChatGPT" with "other writing"). Do not add evaluative conclusion sentences that generalize beyond the stated findings.

   **Claim Scoping:** narrow unsupported absolute-certainty claims. See `references/rewrite-playbook.md § Absolute Certainty to Scoped Claim` for the three-condition test and a worked example.

   **Evidence gate:** Strengthen claims that have citations or supplied data. Delete filler hedging (it is important to note). Do not soften security warnings, legal qualifiers, or user-stated commitments.

   **SNR guideline:** Aim for 15-25% word reduction in AI-padded technical drafts by removing preamble, restatement, and ceremonial hedging. Do not cut to hit a number. Every sentence earns its length.

5. **RECURSE** -- Score with `references/bucket-quickref.md` using weighted points per detected marker: Structure 5 pts, Tone 2 pts, Vocabulary 2 pts, Formatting 1 pt. Refine surgically when:
   - paragraph score >= 5 pts, or
   - document score >= 12 pts.
   Repair the highest-scoring bucket first. Maximum **3 passes**. Stop when below threshold.
6. **Final check** -- Run `references/final-rubric.md`. Revise if any required gate fails.
7. **Capture learning signals** -- Before returning, check the user's messages from this turn against the four trigger types defined in **Style Learning** below. This check is mandatory every turn, not only when the user says "learn my style." Completion criterion: all four trigger types have been explicitly checked against this turn's messages -- if none apply, that is a checked no-op, not a skipped step. Write the resulting profile entry before moving to step 8.
8. **Return** the rewritten text only (silent output). Append a Changes list only if the user asked for explanation.

### Humanize Output

Default output is only the rewritten text.

If the user asks for explanation, append:

```text
Changes:
- "<original>" -> "<replacement>": <brief reason>
```

## Style Learning

The skill builds `syntactic_dna` in `user-profile.json` (`~/.tech-humanizer/`, shared across every project) from two kinds of evidence: the user's own conversation messages (2+ complete sentences, 30+ words triggers sampling), and documents or pasted text the user explicitly flags as their own writing. A flagged document is worth actively asking for -- when a user wants their voice learned quickly rather than over several sessions, ask them to paste or share a few paragraphs they wrote themselves. The skill extracts descriptive structural observations, not numeric measurements, spanning both sentence-level rhythm (length variation, punctuation habits, pacing) and passage-level habits (what the user leads with, how they sequence claim and justification, where caveats land). A pattern is committed to `syntactic_dna` only after 3 independent observations agree -- see `references/profile-schema.md` **Syntactic DNA sourcing rules** for what counts as independent.

See **Voice Profiles** above for how syntactic_dna and the selected voice profile interact, and `references/profile-schema.md` for the full schema.

Explicit preferences (word choices, corrections to skill output) are written to `user-profile.json` immediately when stated. Domain terms are written to the project's `writing-profile.json` instead — see **PROTECT** above.

**Check built-ins before writing the profile.** If the correction is already covered by a rule in `references/ai-markers.md` or `references/ai-style-lexicon.json` (for example, rejecting a decorative unicode bullet — S12), apply that rule and skip the profile write. Only genuinely personal patterns belong in the profile.

**The four trigger types** checked by workflow step 7: a correction, a revert, a restatement of skill output, and a self-flagged writing sample. On any of these, write an `observations` entry (with a `confidence` field). Observations accumulate cheaply and promote to a `preference` or `syntactic_dna` entry once confidence or agreement crosses the threshold (the 3-observation rule still governs `syntactic_dna`). A **revert** specifically records a `do_not_change` (negative preference) so the reverted change does not recur — generalize to the class the correction implies, not the single literal instance, and capture the pattern, the reason, and examples. See `references/profile-schema.md`.

Example: the user reverts `get -> retrieve` back to `get`. Write a `do_not_change` entry: pattern `get -> retrieve`, reason "plain verb, not jargon", examples `["get the project number"]`. A future session reads it as a first-class block, not a comment.

Sampling never applies to text submitted for humanization -- that text may be AI-generated and proves nothing about the user's own voice, no matter how it is delivered (typed, pasted, or uploaded).

## Error Handling

- **Draft has no AI markers**: Return the draft unchanged and note it is already clean.
- **Channel is unknown**: Infer the scenario from the signal checklist in workflow step 1 (length, greeting/sign-off, platform cues, person, audience) and select its voice profile. Do not default to the technical documentation register. When the scenario genuinely cannot be inferred, fall back to a neutral, factual register (never senior-engineer) and, if the choice would materially change the rewrite, ask or hedge rather than silently picking a voice.
- **`user-profile.json` or `writing-profile.json` is missing or malformed**: Proceed without that file's preferences. Do not create either file until the user gives an explicit preference (`user-profile.json`) or domain term (`writing-profile.json`).
- **Technical term not in `references/technical-terms.json`**: Treat unfamiliar domain terms as protected unless the user identifies them as AI marker vocabulary.
- **Source claim cannot be verified**: Flag as source-integrity issue. Do not rewrite it to sound confident. See `references/source-and-markup-integrity.md`.
- **Verbatim phrase conflicts with a detected AI marker**: Verbatim preservation wins. Copy the phrase as-is and adjust surrounding prose instead.
