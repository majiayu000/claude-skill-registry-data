---
name: georgian-grammar
description: Rule-first Georgian writing, editing, translation, grammar-question answering, punctuation reasoning, and QA for standard literary Georgian. Use when Codex must write or revise Georgian-language content, proofread Georgian text, translate into Georgian, answer Georgian grammar or punctuation questions, normalize morphology and syntax, choose correct case/postposition/verb agreement, apply polite თქვენ-forms, or do a final grammar pass before sending Georgian output.
---

# Georgian Grammar

## Overview

Write clean, natural, standard Georgian and reduce the typical mistakes AI agents make in morphology, syntax, agreement, politeness, conjunction choice, and punctuation. Default to contemporary literary Georgian in Mkhedruli unless the user explicitly asks for transliteration, dialect, or archaic style.

Use this skill as a working grammar filter inside Codex, not as a test-answer memory. Every Georgian answer, edit, translation, explanation, UI string, or selected multiple-choice option must pass rule-first Georgian QA before finalizing.

## Workflow

1. Decide whether the task is drafting, translation, editing, or QA.
2. For any form-judgment task, classify the linguistic layer before answering: orthography, morphology, syntax, lexical standardness, register, or punctuation.
3. Use `references/normative-decision-protocol.md` as the rule-first route, especially for short grammar questions.
4. Classify the risk before opening references:
   - verb form or verb agreement: `references/verb-morphology.md`
   - complex morphology, voice/version, causative, participle, or multi-step verb analysis: `references/morphology-deep-dive.md`
   - concrete verb stem, theme sign, participle, or paradigm standardness: `references/verb-paradigm-boundary.md`
   - joined, separate, or hyphenated writing: `references/compound-writing-rules.md`
   - particles, fixed expressions, conjunctions, conditionals, reported-speech suffixes, or prohibitions: `references/particle-expression-rules.md`
   - adverbs, adverbial meaning, question/relative/indefinite/negative adverbs, or adverb formation: `references/adverb-rules.md`
   - complex syntax, indirect speech, relative clauses, word order, or multi-clause punctuation: `references/syntax-deep-dive.md`
   - cases, postpositions, possessive/reflexive forms, demonstratives, or direction forms: `references/case-and-postposition-rules.md`
   - subject-predicate, numeral, relative-pronoun, or `თქვენ` agreement: `references/agreement-rules.md`
   - spelling, fixed orthography, numerals, high-risk fixed forms, or compact spelling reminders: `references/normative-orthography.md`
   - specific lexical paradigm, word meaning, or normative dictionary question: `references/lexical-norm-boundary.md`
   - stylistic correctness, semantic precision, concise Georgian wording, or near-synonym choice: `references/style-and-lexical-choice.md`
   - punctuation, direct address, or register: `references/polite-forms-and-punctuation.md`
5. Read `references/grammar-guardrails.md` for the compact global checklist when drafting or revising more than a short answer.
6. Draft, correct, or answer from the rule. Prefer standard contemporary literary Georgian unless the user asks for colloquial, dialectal, or archaic style. If the exact rule is not in the local references, choose a safer construction or state uncertainty instead of guessing from surface naturalness.
7. Do a final human-style pass with this checklist:
   - verb form derived from the correct paradigm, not only from surface analogy
   - subject-predicate number agreement
   - numeral plus noun behavior
   - correct case before postpositions
   - possessive pronoun form before dative or adverbial nouns
   - pronoun reference, substitution, and ambiguity
   - `თავისი` vs `მისი` ownership
   - relative pronoun number and case
   - `თქვენ` agreement and polite register
   - conjunction choice for cause, purpose, and condition
   - adverbial relation: place, time, manner, cause, purpose, frequency, or negation
   - prohibition forms with `არ` vs `ნუ`
   - joined, separate, and hyphenated writing, especially lexicalized compounds
   - punctuation and spacing
   - natural Georgian phrasing rather than literal calques

## Normative Correctness Pass

Apply this pass to every Georgian output, whether it is a full paragraph, a correction, a translation, a short answer, or a selected option:

1. First check morphology and syntax: verb paradigm, agreement, case, postpositions, person/number, and clause relation.
2. Then check orthography separately: spacing, hyphenation, joined/separate writing, fixed compounds, and standard lexical forms.
3. Before simplifying adjacent identical vowels, check morpheme boundaries. Preverbs, version/voice markers, and vowel-initial stems can legitimately create repeated vowels in one word.
4. Do not infer spelling, hyphenation, or verb standardness only from broad analogy. Use the relevant rule reference first.
5. For concrete verb paradigms, distinguish the productive rule from the lexical/paradigm standardness question before answering.
6. For short answers, silently run the same rule-first check before responding; do not skip it because the output is brief.
7. Use outside normative sources only after local rule analysis is insufficient or when the user explicitly asks for verification.

Do not use a word-list, sentence-list, test-answer memory, trap database, or linter as the normal decision mechanism. Examples inside references are illustrations of productive rules, not the source of truth.

## Form Judgment Protocol

When the user asks whether a word, phrase, or sentence is correct, do not answer from familiarity, frequency, or surface naturalness. First decide what kind of correctness is being judged:

1. If the issue is governed by a productive rule, answer from the relevant rule file.
2. If the issue depends on a specific lexical paradigm, fixed expression, or normative dictionary form that the local rules do not determine, use a normative external source before giving a final answer.
3. If the task is normal writing rather than explicit judgment, avoid risky uncertain forms by choosing a clearer rule-backed construction.

For multiple-choice correctness tasks, do not stop at the first plausible option. Analyze every option first:

1. Mark each option as rule-valid, rule-invalid, lexical-norm-valid, lexical-norm-invalid, or unresolved.
2. For every rejected option, name the concrete error and the corrected form.
3. Choose the answer only after all distractors have been eliminated.
4. If two options remain valid under current normative sources, say the item is ambiguous or source-dependent instead of forcing a single answer.

Examples in this skill are only illustrations of rules. Do not promote any example into a memorized answer list.

## High-Risk Zones

- After `რამდენი` and cardinal numerals above one, prefer a singular noun unless a lexicalized plural is clearly intended.
- With relative pronouns, choose number and case from the relative clause: `რომელიც/რომლებიც`, `რომელმაც/რომლებმაც`, `რომელსაც/რომლებსაც`. Do not copy only the visible case of the antecedent.
- Use `ვინც` for a person/actor and `რაც` for a thing, event, content, or action-object relation.
- Use `თავისი`/`თავიანთი` for the current subject's own possession; use `მისი`/`მათი` when the owner is another third person.
- Recheck hyphenated measurement compounds with `ნახევარი`: prefer `ორკილო-ნახევარი` for "two kilos and a half"; do not collapse it to `ორკილონახევარი`.
- Recheck verb forms that look plausible by analogy. For example, do not form a standard present by adding `-ობ` to a noun or verbal noun unless the verb belongs to that class.
- Recheck version vowels, passive forms, benefactive forms, and causatives before translating English "make/help/have someone do" or "for someone" constructions.
- For noun-derived verbs from `-ო`-final bases, identify the concrete screeve and function before choosing `-ო-` versus `-ოვ-`. Do not generalize the aorist completed-action `-ოვ-` stem to present/future or second subjunctive/optative forms. Separate the first-person subject marker `ვ-` from any stem `-ვ-`.
- Keep `თქვენ` aligned with plural verb morphology. In formal address, use polite lexical substitutions only where they sound natural.
- Choose postpositions by case, not by surface analogy. Recheck the governing case before writing `-თან`, `-ზე`, `-ში`, `-თვის`, `-გან`, `-კენ`, `შორის`, `მიმართ`, `მიერ`, `გარდა`, `შესახებ`, or `-ვით`.
- Recheck third-series transitive verbs manually. Inversion is a common AI failure point.
- Distinguish cause from purpose:
  - `რადგან`, `ვინაიდან`, `იმიტომ, რომ` express cause.
  - `რათა`, `იმისთვის, რომ` express purpose.
- For conditionals, distinguish real condition/result from unreal or wished-for condition before choosing `თუ`, `რომ`, `როცა/როდესაც`, or `ოღონდ`.
- For punctuation QA, identify the syntactic job of the punctuation mark before choosing it: clause boundary, direct address, insertion, direct speech, enumeration, explanation, or summary.
- Around enumerations, identify the direction before choosing the mark: a generalizing word or clause before a specifying list takes a colon; a list before a summarizing/generalizing clause takes a dash.
- Distinguish hyphen from dash. Georgian punctuation follows syntax, not English spacing habits.

## Output Rules

- Prefer Mkhedruli Georgian.
- Prefer standard contemporary literary forms over dialectal, archaic, or literal English or Russian calques.
- Keep examples short and correct when explaining grammar.
- If a form is genuinely ambiguous, say so briefly and offer the safer alternative.
