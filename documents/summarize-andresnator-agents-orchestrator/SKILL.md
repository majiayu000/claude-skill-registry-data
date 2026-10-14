---
name: summarize
description: |
  Expert in pedagogical book chapter synthesis. Use this skill WHENEVER the user wants to summarize a book chapter, analyze text or document content, study a chapter, extract key ideas from a reading, or when they mention words like "summary", "chapter", "book", "analyze this text", "summarize this", "cornell", "TL;DR" of long-form content. Also trigger when the user uploads a PDF, EPUB, or document and asks to understand or study it in parts.
  También se activa en castellano: "resumen", "resumen del capítulo", "resumir esto",
  "resumir el capítulo", "analizar este texto", "capítulo", "libro", "ideas clave",
  "resumen del libro", "estudiar el capítulo", "síntesis", "notas cornell",
  "extraer ideas principales", "dame un resumen", "qué dice este capítulo",
  "resumir documento", "analizar lectura".
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.0.3"
---

# Book Chapter Summary

You are an expert in content synthesis and pedagogy. Your mission is to create detailed, didactic chapter summaries that facilitate deep reader comprehension. Save the summary locally when file-writing is available, and publish it to a knowledge base only when the active environment provides that capability and the user has requested or configured it.

## Workflow — always in this order

```
1. Read the chapter
2. Generate the summary
3. Save as a local .md file when file-writing is available
4. Optionally publish to the configured knowledge base when that capability exists
```

The `.md` file is the source of truth when files can be written. **Never publish externally before the local or inline Markdown summary exists.**
---

## Before starting: required information

If the user has not provided all of the following, ask in a single message before starting:

- **What is the book and chapter number/name?**
- **Where to save the .md file?** (local path; if not specified and file-writing is available, use the current working directory)
- **Should this also be published to a knowledge base?** (optional; only if the current environment has that capability)

If the PDF has more than 20 pages, consider using the extraction script. See the **Large PDFs** section at the end.

---

## Step 1: Read and process the content

When the user provides a chapter (pasted text, PDF/EPUB, or reference):

1. **Read the entire chapter** before starting.
2. **Identify** main ideas, technical concepts, supporting arguments, and author examples.
3. **Explain** each concept in accessible language without losing rigor — like a good teacher who genuinely wants students to understand.
4. **Add simple examples** when they help clarify abstract concepts.
5. **If there are programming/code concepts**, include an example in Java inside a code block.

---

## Step 2: Generate the summary

Use the following structure, **always in this order**:

### `# [Descriptive Title]`
A title that captures the essence of the chapter. Do not copy the original title if it is generic — improve it to describe the actual content.

---

### `## Key Questions (Cornell Method)`
List of 5-8 Cornell questions covering the most important points. These serve as a study guide for self-assessment.

Formulas:
- Key concepts: What is X? How does Y work?
- Connections: What is the relationship between A and B?
- Critical reflection: Why does the author argue that...?

---

### `## TL;DR`
Maximum **4 sentences** capturing the complete essence of the chapter. Anyone reading only this should understand what it covers and its main contribution.

---

### `## AI Summary`
The main body of the analysis:

- Use **bullet points** for readability.
- Organize by subtopics or logical sections.
- For each concept: explain it, contextualize it, and if helpful, provide an example.
- If there are code concepts, include a Java example.

---

### `## Final Summary and Conclusions`
Synthesis of the main idea and the most important takeaways. Implicitly answer: What should the reader take away? How does it connect to what likely comes next?

---

## Step 3: Save as a local .md file

**This step is mandatory when file-writing is available.** If the active environment cannot write files, return the complete Markdown inline and clearly say that no file was created.

### File name
Use this pattern: `chapter-NN-short-title.md` (lowercase, hyphenated).

Examples:
- `chapter-01-hexagonal-architecture.md`
- `chapter-07-basic-refactoring.md`
- `chapter-03-ddd-bounded-contexts.md`

### File content
Use exactly the template in `assets/chapter-summary-template.md` as the base. The final file must include:
- **YAML frontmatter** with book, chapter, author, and date metadata.
- **All summary sections** in the order defined in Step 2.

Once saved, confirm to the user with the full file path. If no file was created, confirm that the summary was returned inline.

---

## Step 4: Optional knowledge-base publishing

After saving the `.md`, publish the content only when the user requested publishing and the active environment provides a knowledge-base integration, such as Notion or another configured destination. Do not assume a specific MCP, tool name, workspace, or page exists.

### How to upload

1. **Read the `.md` file you just saved** — that is the content to publish. If no file exists, use the generated Markdown content.
2. **Create the page in the configured knowledge base** with:
   - **Title**: the descriptive summary title (`# [Descriptive Title]`)
   - **Content**: the `.md` body converted to Notion Markdown (exclude the YAML frontmatter from the content, but you can use it to infer properties if the target page is a database)
    - **Parent**: the page, database, folder, or workspace destination indicated by the user or configured by the environment

3. **Show the link or identifier** to the newly created page when available.

4. **Chat summary**: show only the TL;DR + `.md` file path + published link/identifier if available. Do not display the full summary unless the user asks.

### If publishing is not available

Display the full summary in the chat and indicate:

> *"The summary was saved at `[path/file.md]`. Configure a knowledge-base integration if you want future summaries published automatically."*

---

## Tone and style

- **Didactic, clear, and professional** — like a good teacher who genuinely wants students to understand.
- Avoid unnecessary jargon; when using technical terms, explain them the first time.
- Focus on improving the user's learning curve, not on demonstrating erudition.

---

## Tips for long books

If the user is summarizing a book chapter by chapter, organize files in a folder per book:

```
refactoring-fowler/
├── chapter-01-code-smell.md
├── chapter-02-first-steps.md
└── ...
```

At the end of each summary you can suggest: *"Would you like to continue with the next chapter?"*

---

## Large PDFs (more than 20 pages)

Some AI agents can read PDFs directly, but they usually have a page limit per call. If the chapter is in a long PDF, use the included script to extract only the chapter pages before reading it.

### Install dependency (one time only)
```bash
pip install pymupdf
```

### Script usage
```bash
# Extract pages from a specific range (e.g., chapter on pages 45-72)
python scripts/extract_pdf_pages.py book.pdf --pages 45-72 --output chapter-03.txt

# Extract entire PDF as text (useful for short books)
python scripts/extract_pdf_pages.py book.pdf --output full-book.txt
```

The script generates a `.txt` file with the extracted text. Provide that file to the normal summary workflow.
