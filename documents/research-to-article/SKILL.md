---
name: research-to-article
description: Turn a topic and public source set into a source-traceable article package with claim mapping, metadata, links, a finished draft, and verification notes. Use when a user asks for a researched article, educational post, analysis, comparison, explainer, source-backed commentary, SEO or answer-focused article, or a publication-ready draft rather than a research brief.
---

# Research to Article

Build a finished article from current evidence while keeping facts, analysis, recommendations, and unresolved claims visibly separate.

## 1. Define the article contract

- Confirm the topic, audience, practical purpose, time window, desired length, publication type, and required point of view.
- Identify the intended output: editorial package, full draft, revision, or verification pass.
- Use `research-brief-curator` instead when the user wants only a digest, reading queue, or research brief.
- Preserve an approved angle unless new evidence makes it inaccurate or misleading.

## 2. Build the source and claim map

- Browse current public sources whenever the topic includes facts that may have changed.
- Read [references/source-quality.md](references/source-quality.md) before selecting evidence.
- Prefer primary sources, official documentation, original research, standards, transcripts, and direct creator material.
- Record every material claim with its source, publication date, event date when different, evidence role, and limitations.
- Separate sourced fact from analysis, inference, scenario, and recommendation.
- Keep conflicting facts visible until a stronger source or explicit qualification resolves them.

## 3. Prepare the editorial package

- Use [assets/article-package-template.md](assets/article-package-template.md).
- Define the title, practical angle, slug, meta description, audience need, outline, internal-link opportunities, call to action, source credits, and Link Map.
- Include only sections supported by the source map or clearly labeled as analysis.
- Ask for a material editorial decision only when the evidence supports multiple incompatible directions.

## 4. Draft with evidence discipline

- Put the useful answer early and explain why the evidence matters.
- Cite material claims close to the wording they support.
- Attribute preview, reported, estimated, disputed, or creator-tested information precisely.
- Keep quotations short, necessary, and attributed. Prefer paraphrase with a direct source link.
- Do not invent facts, quotes, statistics, examples presented as real, source access, product behavior, consensus, or outcomes.
- Do not turn a single example, testimonial, or small study into a universal claim.

## 5. Verify the article package

- Recheck names, dates, links, numerical claims, quotations, credits, title, slug, meta description, and Link Map.
- Mark claims that remain `qualified`, `inference`, `unsupported`, or `stale` and revise or hold them.
- Confirm the final draft distinguishes fact, analysis, and recommendation.
- Report the evidence cutoff date and any source that could not be accessed.

## 6. Respect the publication boundary

Return the article package and verification state. Do not publish, modify a website, submit indexing requests, or update an external system. If the user later authorizes website implementation, hand the finished package to the appropriate website workflow and verify the affected surfaces with `website-change-verifier`.
