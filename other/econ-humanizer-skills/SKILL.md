---
name: econ-humanizer-skills
description: Polish, rewrite, or review Chinese and English economics papers, abstracts, introductions, empirical sections, literature reviews, conclusions, and policy implications to remove AI-sounding prose while preserving academic meaning. Use when the user asks to 去除AI味, humanize, 降低AI痕迹, 学术润色, match economics journal style, imitate reference papers, or revise text using local folders named 参考论文 or reference papers.
---

# Econ Humanizer Skills

## Purpose

Edit economics writing so it reads like a real academic paper rather than generic AI prose. Preserve the author's claims, evidence, citations, variables, model logic, and uncertainty. Do not optimize for AI detectors; improve scholarly specificity and style.

## Invocation Modes

Support two calling styles.

1. **Direct invocation mode**, modeled after the simple invocation style of `Humanizer-zh`:
   - User may call: `$econ-humanizer-skills ...`.
   - Infer the working language from the draft, the target section, and any stated outlet/register. Do not require the user to specify Chinese or English.
   - Read `references/humanizer-principles.md`.
   - If the main output should be Chinese, also read `references/econ-style-zh.md`.
   - If the main output should be English, also read `references/econ-style-en.md`.
   - If the draft is bilingual, keep the user's apparent target language; if unclear, follow the language of the section being revised.

2. **Reference-paper mode**:
   - Use when the project root contains `参考论文/` or `reference papers/`, or when the user asks to "参考里面的文章语言格式".
   - Do not require the user to mention reference papers in the prompt; if a supported reference folder exists, use it automatically when helpful.
   - Treat the user's current workspace or project root as the reference-paper root. Do not use the installed skill directory as the project root.
   - Read `references/reference-paper-mode.md`.
   - If needed, run `scripts/extract_reference_snippets.py` to inspect local PDF samples.
   - Prefer reference papers in the same language and section type as the user's draft. If no subfolders exist, infer language from filenames and extracted text.

If local reference papers are available, combine direct invocation with matching reference papers for cadence, section conventions, and phrasing. The skill still infers the output language automatically.

## Workflow

1. **Classify the task**
   - Identify language: Chinese, English, or bilingual.
   - Identify section: abstract, introduction, literature review, theory/hypotheses, data, empirical strategy, results, mechanism, robustness, heterogeneity, conclusion, or policy implications.
   - Identify target outlet/register if stated: Chinese journal style, English applied economics, working paper, policy brief, thesis chapter.

2. **Diagnose before rewriting**
   - Mark AI-sounding patterns: inflated significance, vague attribution, formulaic transitions, stacked threes, generic conclusions, over-polished symmetry, and unsupported causal claims.
   - Mark economics-specific weaknesses: missing data period, sample, variables, identification strategy, result magnitude, standard errors/significance, mechanism, limitations, or citation anchors.

3. **Rewrite with evidence discipline**
   - Replace abstractions with concrete research objects: data, period, sample, model, treatment, outcome, coefficient, margin, mechanism, or named literature.
   - Keep causality proportional to identification. Use "shows/estimates/indicates/is associated with" when the design does not justify "causes".
   - Keep citations and terminology intact unless they are clearly malformed.
   - Preserve quotation marks carefully when they mark cited concepts, policy names, variable labels, questionnaire wording, coined terms, or phrases the author is deliberately treating as terms of art. Remove or change quotation marks only when they are clearly decorative, inconsistent, or misleading.
   - Do not invent data, papers, estimates, robustness tests, or mechanisms. If a claim needs evidence that is missing, flag it in brackets or in notes.

4. **Run the second-pass audit**
   - Ask: "What still sounds AI-generated or unlike an economics paper?"
   - Remove remaining generic polish, slogan-like transitions, decorative adjectives, and conclusion padding.
   - Check that the final rewrite has a plausible economics-paper rhythm for the selected language.

## Output Format

Default output:

```text
问题诊断:
- ...

润色稿:
...

修改说明:
- ...
```

If the user asks for direct replacement only, output only the revised text.

For long papers, work section by section and keep a short "需要作者确认" list for facts, estimates, or citations that cannot be inferred from the draft.

## Guardrails

- Do not promise to bypass AI detectors.
- Do not make prose more casual unless the target is a blog, essay, or policy commentary.
- Do not flatten legitimate academic terminology.
- Do not casually remove quotation marks around deliberate concepts or cited wording.
- Do not remove all formulaic economics phrases. Phrases like "研究发现", "进一步研究发现", "we estimate", and "we find" are normal when followed by concrete content.
- Do not copy sentences from reference papers. Use them only to infer structure, level of specificity, and cadence.
