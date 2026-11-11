---
name: prompt-residue-sweep
description: Lightly review finished human-readable prose such as READMEs, SKILL.md files, documentation, essays, code comments, and docstrings for prompt residue from drafting discussions. Report small exact excerpts and minimal replacements or deletions without rewriting the artifact or changing executable code.
---

# Prompt Residue Sweep

Inspect a finished text artifact for drafting or conversation context that does
not belong in the artifact itself. Report only clear, localised findings. Do not
perform a general prose review or rewrite.

## 1. Establish scope

1. Read the requested artifact and enough surrounding text to understand its
   purpose, audience, and voice. For repository work, inspect only the named
   file(s) or explicitly requested scope.
2. Examine human-readable prose, including comments and docstrings in source
   files. Leave executable code, identifiers, syntax, configuration values,
   machine-readable data, and quoted source material untouched.
3. Treat the artifact as a standalone deliverable for its intended reader,
   who has not participated in the conversation that produced it.

## 2. Identify residue

Look for traces of the drafting process that do not help the intended reader:

### Simple cases

- References to the user's request, a previous answer, model behaviour, or
  earlier iterations (for example, "as discussed" or "I added this because").
- Explanations of why a section, format, or approach was chosen during drafting,
  instead of instructions or information relevant to the finished artifact.
- Conversational transitions, self-references, or reassuring commentary carried
  over from the authoring exchange.
- Comparisons with abandoned alternatives that have no enduring explanatory or
  operational value.
- Instructions about editing, expanding, or organizing the artifact embedded in
  instructions for using it. Flag these when artifact maintenance is outside the
  section’s purpose; preserve them in explicit maintenance guidance.
- References to specific people, products, tools, or workflows carried over from
  the drafting discussion when the underlying guidance is general. Preserve
  names where genuine dependencies or compatibility requirements exist.

### Complex cases

- Correct content with residual framing:
  A technically correct passage may still contain residue when its
  framing answers a drafting concern rather than serving the intended reader.
  - Look for unnecessary reassurance, contrasts, or explanations attached
    to otherwise useful requirements.
  - Distinguish the enduring information or requirement from its conversational framing.
    Preserve the requirement; remove or rephrase only the residue.
  - Do not flag legitimate explanations, compatibility constraints, or
    design rationale merely because they provide context.

- Unwarranted requirements:
  Look for explanations, caveats, or technical facts from the drafting
  discussion that have been presented as requirements or design decisions
  without a clear purpose in the finished artifact.
  - Distinguish established decisions from background knowledge,
    implementation consequences, and end-user guidance.
  - Preserve genuine constraints and decisions. Remove or relocate
    material that does not serve the artifact's intended purpose.
  - Do not infer new requirements merely to justify retaining a passage.
  - Check for redundant prohibitions or precautions that merely restate
    established responsibilities or pre-empt unlikely alternatives. Where
    such wording expresses a useful requirement or operational
    consequence, prefer stating it directly in a neutral tone. Flag only
    when the negative framing lacks an independent architectural,
    operational, or safety purpose and appears to reflect drafting residue.

### Useful Boundary Tests

#### Reader Test

Normally keep it if it passes the reader test:

- Would this passage make sense and provide value to someone who never saw the
  drafting conversation?
- Is this passage addressed to the reader performing the artifact’s stated task
  (as opposed to the person drafting or maintaining the artifact?)

Do **not** flag material merely for being explanatory, verbose, or stylistically
imperfect. Preserve useful design rationale, meaningful operational constraints,
explicit decision records, legitimate authorial voice, quotations, examples, and
texts about prompting where such language is the subject. When uncertain, omit
the finding rather than inventing a stylistic problem.

#### Redundancy Test

Examine negative constraints, exclusions, precautions and scope limitations for unnecessary specification.

Apply a counterfactual deletion test: would removing the statement permit a materially different, reasonable interpretation or implementation?

Flag statements that merely negate behaviour already excluded by the positive requirements, repeat established component responsibilities, or preempt unspecified future features without establishing a meaningful boundary. Preserve constraints that resolve genuine ambiguity, establish deliberate scope decisions, or protect correctness, security or operational reliability.

## 3. Propose minimal corrections

1. Admit only high-confidence residue with a clear, local fix.
2. Select the shortest exact source span that identifies the issue; include a
   full sentence only when a shorter excerpt would be ambiguous.
3. Prefer deletion when the surrounding text already states the useful
   content. Otherwise suggest the smallest coherent replacement,
   including adjacent sentences when necessary, that preserves useful
   meaning, technical accuracy, and the author's voice.
4. Do not propose section rearrangements, broad paraphrasing, added content,
   terminology changes, or rewrites of unrelated passages.
5. Combine overlapping findings. Stop when further findings become speculative,
   repetitive, or ordinary copy-editing. Do not pad the result.

## 4. Report

Return a concise numbered list, in document order. For each finding, show:

- **Location:** file and line (when known), or a brief section reference.
- **Found:** the exact, minimal quoted span.
- **Suggested:** a minimal replacement, or **Delete**.

Use a short explanation only when the reason is not obvious. If no convincing
residue appears, say: **No clear prompt residue found.**

Do not modify files by default. Only apply the listed, localised corrections
when the user explicitly requests edits; leave all other text and formatting
unchanged. Do not create reports, backups, scripts, or auxiliary files unless
requested.

Optionally note consequential borderline passages deliberately retained, with a brief rationale, separately from confirmed findings.
