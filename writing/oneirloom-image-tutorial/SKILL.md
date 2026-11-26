---
vendored_from: https://github.com/PigeonAI-Yang/oneirloom
name: oneirloom-image-tutorial
description: Write, expand, or polish illustrated image-generation tutorials with concrete prompt examples and inspected results. Use for teaching articles, section-by-section expansion, and tutorial copy editing; not for a standalone image prompt or reference-image reconstruction.
triggers:
  - oneirloom-image-tutorial
  - oneirloom
  - image
  - tutorial

---

# Image-generation tutorial writing

Read the [shared interaction contract](../oneirloom/references/interaction-contract.md) before the first substantive response unless its unchanged content is already available. For person prompts, including new images and grid panels, read [person defaults and proportions](../oneirloom/references/person-prompts.md).

Produce a tutorial the author can teach from and the reader can follow. The deliverable is an article with explanatory images, not a list of prompt keywords or a production report.

## When to use

- Write, expand, or polish an illustrated image-generation tutorial: a new teaching article, section-by-section expansion, or copy editing
- Not for a standalone image prompt or reference-image reconstruction; those stay with the main skill and `oneirloom-visual-analysis`

## Start from the current article

- Inherit the intended readers, language, author voice, subject, image tool, existing files, and accepted revisions. For this collection, default to natural Chinese in the author's first-person voice unless the user chooses otherwise. Keep instruction files in English.
- Read the current publishing source and a representative section before editing. Preserve the established output path and existing material. A request to polish wording does not request a new outline, new images, or new model tests.
- Choose the actual scope: a new tutorial, deeper explanations across existing sections, or prose revision. If the user gives one shallow section as an example while asking to expand the article, apply the requested depth to every relevant section.
- Use a reference article to understand its teaching progression and presentation. Write original explanations and examples. Do not append unsolicited inspiration or independent-production footers; preserve attribution required for quotations or licensed material and follow explicit source-credit requests.

## Plan teaching depth before drafting

For each teaching subsection, identify the reader's question, the meaningful alternatives, the image needed to show their difference, and the detail the reader should inspect. Keep this planning internal unless requested.

Cover these functions in connected prose, without forcing identical headings or paragraph counts:

1. Explain the choice in everyday language and when it is useful.
2. Contrast alternatives or distinguish commonly confused concepts.
3. Show how to express the choice in a prompt, with a short editable example or a complete prompt as appropriate.
4. Direct the reader to visible details in the illustration.
5. Explain a relevant miss and a practical next adjustment, using actual evidence when available.

Select breadth for the topic rather than repeating one easy comparison. Read [references/teaching-depth.md](references/teaching-depth.md) when planning a substantial tutorial or expanding shallow sections. It offers examples, not mandatory chapter counts. Do not freeze a previous article's subject, 16-chapter outline, model, seed, room, or image count into the next tutorial.

## Write in the author's voice

- Let the author teach the reader directly. Vary sentence openings; first person does not mean starting every paragraph with the same phrase.
- Use idiomatic Chinese for a Chinese article. Replace management language, invented technical metaphors, translated noun chains, empty claims of sophistication, and repetitive disclaimers with the concrete thing the reader should write or look at.
- Explain necessary photography or model terms on first useful mention. Prefer a visible description to unexplained terminology. Do not remove an accurate technical term merely to substitute a less precise euphemism.
- Preserve instructional substance during polishing. Rewrite the title, headings, body, captions, image labels, and explanatory prompt fragments as needed; do not reduce a detailed lesson to a shorter keyword list.
- Distinguish an image-model prompt, an excerpt meant to replace part of a prompt, and an instruction to a writing assistant. Tell readers where each belongs.
- Keep original prompts quoted as actually used byte-for-byte in the run records. In the article, either quote those prompts verbatim or clearly label a revised version that has not been tested. A prose revision alone does not establish a new generation result.
- Match the requested article language. Do not impose the parent skill's standalone bilingual-prompt layout on an entire tutorial. Supply additional prompt languages only when the lesson or user requires them.
- Keep file paths, queue logs, internal task records, and unrelated tool-operation details out of the lesson. Include settings only when they help the reader reproduce or understand the example.

## Make each illustration teach something

- Give every teaching subsection a relevant explanatory figure. Introductory and closing paragraphs do not need decorative filler. Reuse an existing figure only when it genuinely answers that subsection's question.
- Explain what to compare and where to look. A gallery of attractive pictures with generic captions does not demonstrate a lesson.
- Use the user's selected image tool and established workflow when generation is requested. Confirm the live workflow before running it; preserve its configuration and unrelated queued work. Do not replace it with a different service merely because that service is available.
- Generate only missing or unsuitable demonstrations within the authorized scope. Reuse credible current images and observations for wording-only revisions. If generation is unavailable, complete independent writing and image planning, and identify missing illustrations rather than claiming a finished illustrated tutorial.
- Personally inspect each selected output before describing its effect. Compare the requested result with the visible result, including unwanted changes to the person, clothes, room, crop, or lighting. A successful queue response proves only that a job ran.
- Preserve the full submitted prompt, model/workflow, seed when relevant, dimensions, and original image. Store generation identifiers or history when the tool exposes them; do not invent unavailable metadata.
- For comparisons, keep unrelated conditions similar where practical. If multiple things changed, explain that the images compare two approaches rather than proving a single word caused the difference. A shared seed alone proves neither identity preservation nor a controlled experiment.
- After a clear miss, revise the relevant description or framing and inspect again. If the same important miss persists after two focused revisions, reconsider available controls or label the limitation; do not keep adding synonyms indefinitely.
- Describe misses plainly. A cropped wrist cannot prove sleeve length; a palm on an armrest does not prove the whole forearm rests there. Keep useful partial examples only with accurate captions. Never present a requested feature as observed merely because it appears in the prompt.
- Use layout tools for labels, comparison boards, and resizing. If a crop, retouch, or other edit contributes to the apparent success, disclose it. Do not present post-processing as direct prompt compliance.

## Update and check the actual deliverable

Use the existing source and build/export process. For revisions, update all current editions requested or already maintained for the article, such as HTML, Markdown, and its downloadable image package. Keep archives separate from current copies.

Before delivery, check:

- Every requested chapter received the requested treatment, and every teaching subsection has an appropriate figure.
- Captions and explanations agree with inspected images, with limitations stated near the relevant example rather than repeated as generic warnings.
- Copyable prompts contain the intended text, quoted actual prompts still match their records, and prompt excerpts are identified as excerpts.
- Images load, labels fit, and supported links, copy controls, and image enlargement work. Inspect a rendered page when the delivery is HTML; check a narrow viewport when mobile reading is part of the existing format.
- Current downloadable copies contain the same revision as the main article.

Report the edited artifact and decisive checks briefly. Distinguish structural validation, visual inspection, and actual generation. Do not call an illustration plan a completed image test.

## Related skills

Load only branches needed by the current work. For new generation, use the relevant model adapter and medium branch. For reading source images, use `oneirloom-visual-analysis`; for camera/crop and lighting lessons, use `oneirloom-camera-composition` and `oneirloom-color-light`; for a persistent mismatch, use `oneirloom-result-diagnosis`. Find them by skill name, with sibling directories as the repository fallback.

When available, apply `technical-writing` and `unslop` to prose. Their general defaults do not replace the requested first-person voice, article depth, or the user's image-tool choice. Honor any instruction that the Primary must write and operate personally.
