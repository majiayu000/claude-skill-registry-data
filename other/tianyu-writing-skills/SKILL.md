---
name: tianyu-writing-skills
description: Tianyu's private writing skill for AI conference papers, distilled from hzwer & DingXiaoH's "Writing AI Conference Papers" handbook. Use whenever drafting, restructuring, revising, or polishing an academic AI/ML paper or any of its parts (abstract, introduction, related work, method, experiments, rebuttal), running a pre-submission check, or self-reviewing a draft against common reviewer complaints and questionable experimental practices.
---

# Tianyu's Writing Skills — AI Conference Papers

Distilled from [hzwer/WritingAIPaper](https://github.com/hzwer/WritingAIPaper) (authors: hzwer, DingXiaoH).
Full original texts live in this skill's `references/` directory:

- `references/writing-ai-paper-handbook.md` — the complete handbook (structure, introduction formula, readability, checklists, review process, conference list).
- `references/not-good-ideas.md` — catalogue of questionable practices to avoid (and to self-audit against).

Read the reference files when the user asks for the full checklist, the conference list, or a deep self-audit; otherwise apply the distilled rules below directly.

## 1. Before writing: pin down the core idea

- The key contribution of a paper falls into exactly one of three categories — identify which one, state it early, and build the paper around it:
  - **Insight**: you explain something that is already there.
  - **Performance**: you do something better.
  - **Capability**: you do something that could not be done before.
- Refine one or two core ideas until they are memorable and shareable. Great-but-unoriginal ideas should not be described in detail.
- Discovering new phenomena and sharing new ideas matter more than raw performance gains. Experimental results are evidence of a discovery, not the contribution itself.
- Do not undersell the work: tell the ResNet-style story (pose a problem → abstract the underlying principle → propose the solution → verify), not a parts-list of borrowed components.
- Prefer simple, effective solutions (Occam's razor) that will generalize to future scenarios over convoluted tricks tuned for immediate validation.

## 2. Structure: three self-complete levels

Abstract → Introduction → Main body. Each level tells the complete research story; each is an expansion of the previous one. Draft the main body first.

- Write for the target audience: present the valuable findings, not the tortuous research process.
- Around the contribution statements, deliver a solid results section: comparative and ablation experiments that visibly support each claimed contribution. Be honest — never overclaim.

### Introduction formula (three moves)

1. **Establish a research territory** — show the area is important, central, and problematic.
2. **Find a niche** — indicate a gap in previous research or extend prior knowledge.
3. **Occupy the niche** — state the purpose, research questions, principal findings, value, and paper structure.

Additional rules: keep the reader uppermost in mind; surface the novel and interesting parts as early as possible; give the most space to original ideas; respect predecessors (affirm their contributions before noting shortcomings); consider a "page-one figure" that captures the paper's core.

### Related work

Pick three or four most relevant topics and trace the historical evolution under each. The mediocre approach recounts correct history; the better approach explains how each line of work relates to yours and how you improve on it. Never merely list others' negatives. Verify classification/pioneer claims against the related-work sections of the cited papers, then rewrite the section from the angle that highlights what is unique about this paper.

## 3. Readability: optimize four measurable properties

Prioritize clarity over style in every sentence.

### Logical strength
- Never misuse connectives. "To this end" requires an actual stated end; "First / Second / Last" imposes order that must really exist. Connectives smooth existing logic — they must never fabricate it.

### Defensibility
- Assume every sentence will be challenged. Back claims with references and facts: "Problem A results in ... [1,2,3], which is critical to ... because ... [6,7,8]."
- Calibrate causal language to the evidence: "is attributed to" requires prominent direct evidence; "may be explained by" fits indirect evidence such as visualizations. Stay objective; never exaggerate.

### Confusion time (minimize "hmm → oh" gaps)
- Explain a concept immediately where it is introduced ("We propose XXX, implemented as a two-layer MLP"), or cite where it is explained.
- Resolve relative-pronoun ambiguity; break long ambiguous sentences into short ones — much of the readership is non-native and fancy syntax earns nothing.
- Start paragraphs with topic sentences so a skimming reader still gets the main information.

### Information density
- Get to the point immediately; skip history lessons and anything most readers already know.
- Balance text and visuals; move long hyperparameter/experimental detail to the appendix.
- Keep analysis physically close to its chart, name the chart ("Table 5") in the analyzing sentence, and make every caption self-contained (theme + key conclusion + abbreviation expansion).
- Design tables so the intended comparison is explicit — repeat a baseline row if needed. Unclear tables annoy reviewers; inelegant ones do not.

## 4. Checklists

### Detail checklist (during polishing)
- Charts alone tell a complete story and are self-explanatory; figure text/legends large enough.
- Symbols, abbreviations, and references are consistent throughout.
- Level of detail is right in both text and charts; important information sits in prominent positions.
- Tables read fast: column grouping, bolding, redundancy removed.
- Reproducibility: details and key code in the appendix.

### Last-few-hours checklist (before submission)
- Numbers copied correctly; search for "?" to catch broken LaTeX refs; formulas complete.
- Every chart mentioned in the text, mention order matches appearance order; captions grammatical, ending with a period.
- Charts vectorized; no figures outside the main-body pages; subtitle capitalization unified.
- Anonymity verified (including acknowledgments, code, demos). **Page count correct — avoid desk reject.**

## 5. Self-review before submission

Audit the draft against the common negative review comments (details in `references/writing-ai-paper-handbook.md`): unprofessionalism (missing key references, misaligned experimental setup), validity doubts (results defying common sense, overclaiming), disrespecting prior work (stale baselines, unsupported criticism), lack of novelty (weak story, incremental feel), poor presentation (grammar, missing details), and disagreement on approach (justify the technical route with experiments or literature).

Then audit the experiments against `references/not-good-ideas.md` — unfair compute/hyperparameter advantages, hidden tweaks, page-filling incremental designs, and cherry-picked evaluation (reporting only favorable metrics/datasets, misaligned test protocols, overfit test sets). Anything on that list must be either removed or explicitly disclosed.

Remember Fei-Fei Li's rule: **badly written papers get bad reviews, period** — leave time for writing, and rewrite until it is as polished as you can make it.

## 6. How to apply this skill

- **Drafting**: follow §1–§2 to lock the core idea and skeleton before producing prose; draft the main body first, then the introduction by the three-move formula, then the abstract.
- **Revising/polishing**: sweep the draft once per property in §3, then run the §4 checklists.
- **Self-review / pre-submission**: run §5 and report findings as a reviewer would, each with the offending location and a concrete fix.
- Preserve the author's voice and LaTeX/Markdown formatting; make surgical edits and explain the reason for each substantive change.
