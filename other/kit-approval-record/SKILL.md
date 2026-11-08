---
name: kit-approval-record
kind: pattern
rule: kit-approval
description: Pattern of rule kit-approval. Load when the owner answered about a kit mockup or a showcase — the ready-made question, the record lines and what is done with a refusal.
---

# Recording the owner's approval of a kit edit

Pattern of the rule `kit-approval`.

## When to use

- A Figma frame of a kit edit is measured and is about to be shown to the owner.
- The showcase of a kit edit has every state and is about to be shown.
- The owner answered.

## The question

One question, with the link and nothing to choose from: «Макет: <ссылка на кадр Figma>. Одобряете?»
For the showcase: «Витрина: <адрес истории>, совпадение с макетом <число>. Одобряете?»

## The answer

An approval goes into the task folder's approvals.md word for word, between « and »:

```markdown
- **Макет:** «да, одобряю» — https://www.figma.com/design/<file>?node-id=<node>
- **Совпадение:** 48 из 48 чисел
- **Витрина:** «одобряю витрину»
```

## The match before the showcase question

1. The values of every layer of the block are read from Figma into a JSON file, one key per value:
   `<element>.<property>` — width, height, gaps, radius, colours, font size, weight, line height.
2. The same keys are measured in the showcase story of the whole block, or of the whole page, by
   `getComputedStyle` and `getBoundingClientRect`, into a second file.
3. `node tools/kit-match.mjs numbers <figma.json> <showcase.json>` names every miss and prints the
   match line. A miss is fixed in the code until it prints N of N.
4. `node tools/kit-match.mjs overlay <figma.png> <showcase.png> <diff.png>` draws the divergence
   frame; it goes to the owner with the showcase question.

A refusal is not written. The frame or the code is fixed, and the same question is asked again.

## Check

```bash
node tools/check-kit-approval.mjs
```

It names every missing line and every quote the owner did not write. The archive record takes both
lines verbatim when the task folder is taken apart.
