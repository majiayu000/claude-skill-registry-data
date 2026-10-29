---
name: ai-slop-preflight
description: Audit LaTeX manuscripts before arXiv or journal submission for unchecked AI artifacts, hallucinated or unsupported citations, conversation residue, AI-flavored prose, missing disclosure, provenance gaps, and compliance with current publisher/community expectations for AI-assisted scientific writing.
---

# AI Slop Preflight

## Purpose

Use this skill before arXiv upload, journal submission, public posting, or circulation of a manuscript that may have been edited, checked, drafted, searched, coded, or reviewed with AI assistance. The goal is not to "detect AI"; the goal is to remove concrete evidence of unchecked generation, verify every scholarly dependency, and make human responsibility and provenance clear.

For venue-specific work, read `references/publisher-ai-policies.md` before acting. Treat policies as time-sensitive: if the submission is imminent, verify the current arXiv/journal instructions on the web.

## Non-Negotiable Checks

1. **Citation existence.** Every `\cite`, bibliography entry, DOI, arXiv id, theorem attribution, and historical claim must match a real scholarly record from arXiv, DOI/Crossref, MathSciNet, zbMATH, DBLP, publisher pages, journal archives, or author-hosted sources.
2. **Citation support.** A real paper is not enough. Check that the cited result actually supports the sentence where it is cited. Flag "standard", "well-known", "classical", "state of the art", and "best known" claims unless a precise source is present.
3. **No conversation residue.** Remove text such as assistant apologies, "here is", "let me know", prompt fragments, reviewer-chat language, hidden comments addressed to an agent, TODO placeholders, or meta-comments about drafting.
4. **No generic AI prose.** Replace fashionable but imprecise wording with standard mathematical prose. Words such as "proof spine", "mechanism", "stratum", "sector", "gate", "boundary", "certificate", "assay", "proof debt", "proof package", "seamless", "pivotal", "delve", "realm", "landscape", and "opens avenues" are not banned, but they must be mathematically defined or replaced by the actual theorem, obstruction, example, reduction, or construction.
5. **Human responsibility.** AI systems are not authors, coauthors, proof sources, or authorities. Human authors remain responsible for correctness, completeness, attribution, code, data, and all claims.
6. **Disclosure decision.** If AI use was substantive, add a disclosure in the location required by the venue, usually acknowledgments, methods, cover letter, or a tool/computational-resource statement. Include tool/model, date or version when known, task performed, affected material, and how humans verified it. Light grammar or spelling assistance may be treated differently by some publishers, but uncertain cases should be disclosed.
7. **Math-community standard.** For AI-assisted mathematical results, make reviewing easier: identify what was AI-suggested, what was independently checked, what artifacts are available, and whether any proof has been formalized, computationally verified, or checked by external experts. Avoid press-release style claims for unreviewed results.

## Workflow

1. **Collect the manuscript surface.** Identify the root `.tex`, included `.tex` files, `.bib` files, appendices, generated PDF, tables, figures, code outputs, and any AI-use notes.
2. **Run the static scanner.**
   ```bash
   python3 .claude/skills/ai-slop-preflight/scripts/ai_slop_preflight.py main.tex
   ```
   If the script lives only in the skill directory, run it from there and pass the project root or manuscript path. Treat its output as leads, not a clean bill of health.
3. **Audit citations manually.** Build a table with columns `key`, `manuscript location`, `claim`, `verified record URL`, `metadata match`, `claim support`, and `action`. Every row must end in `verified`, `revised`, `removed`, or `needs author decision`.
4. **Check provenance of results.** For each main theorem, lemma, computational claim, example, dataset, or figure, verify the source: human derivation, cited source, proof assistant, script, or reproducible computation. Do not leave a result whose only source is an AI transcript.
5. **Rewrite the prose.** Search abstracts, introductions, conclusions, dashboards, and remarks for vague AI-ish summaries. Replace them by precise statements of hypotheses, conclusions, methods, limitations, and dependencies.
6. **Prepare disclosure.** If AI assistance was used substantively, draft a concise disclosure. Mention model/tool names and versions if known, the type of assistance, and the human verification process. Do not cite an AI tool as a scholarly source.
7. **Compile and inspect.** Build the PDF, inspect the rendered abstract/introduction/conclusion/references, and confirm no comments, broken references, undefined citations, placeholders, or hidden AI residue remain.

## Report Format

Produce an `AI_PREFLIGHT_REPORT.md` or equivalent section with:

- **Decision:** `blocking`, `major revisions`, `minor revisions`, or `clear`.
- **Blocking issues:** hallucinated references, missing citation support for central claims, conversation residue, fabricated data, placeholder arguments, unsupported theorem claims, or missing required disclosure.
- **Citation audit:** the verification table described above.
- **Prose audit:** removed/replaced phrases and unresolved style concerns.
- **Disclosure audit:** whether AI use must be disclosed and the exact text proposed.
- **Verification audit:** which proofs/computations were independently checked and which still depend on author judgment.

Do not mark the manuscript ready while any bibliography entry is unverified, any citation does not support its local claim, any AI/meta conversation text remains, or any substantive AI use lacks the disclosure required by the target venue.
