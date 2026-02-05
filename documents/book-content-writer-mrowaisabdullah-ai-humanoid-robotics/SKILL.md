---
name: book-content-writer
description: specialized agent for writing high-quality, educational technical content for Docusaurus books. Focuses on clarity, engagement, and technical accuracy using modern documentation standards.
category: content
version: 1.0.0
---

# Book Content Writer Skill

## Purpose

Transform chapter outlines and topics into polished, production-ready documentation chapters. This skill ensures all content is:
- **Educational:** Clear explanations with progressive complexity.
- **Engaging:** Uses active voice, real-world examples, and interactive elements.
- **Docusaurus-Native:** Leverages Admonitions, Tabs, Code Blocks, and MDX components effectively.
- **Consistent:** Follows the established "Minimalist Professional" tone of the book.

## When to Use This Skill

Use this skill when:
- You have a chapter outline (from `book-structure-generator`) and need the actual content.
- You need to rewrite existing documentation to match the book's quality standards.
- You are expanding a rough draft into a full chapter.
- You need to generate code examples and explanations for a specific technical topic.

## Core Capabilities

### 1. Content Generation

**Input:**
- Chapter Title
- Target Audience (e.g., Beginner, Advanced)
- Key Learning Objectives
- Outline/Rough Notes

**Output:**
A complete Markdown file (`.md` or `.mdx`) containing:
- **Introduction:** Hook the reader, state what they will learn.
- **Prerequisites:** (If applicable) What is needed before starting.
- **Core Content:** Structured with clear H2/H3 headings.
- **Code Examples:** Fully commented, copy-pasteable code blocks.
- **Visual Aids:** Placeholders for diagrams/images with descriptive alt text.
- **Summary/Next Steps:** Recap and transition to the next topic.

### 2. Docusaurus Feature Integration

Automatically utilizes Docusaurus features to enhance readability:

*   **Admonitions:**
    ```markdown
    :::note
    Useful context that isn't critical to the main flow.
    :::

    :::tip
    Best practices or shortcuts.
    :::

    :::warning
    Common pitfalls or things to avoid.
    :::
    ```

*   **Tabs (for multi-language/OS examples):**
    ```jsx
    import Tabs from '@theme/Tabs';
    import TabItem from '@theme/TabItem';

    <Tabs>
      <TabItem value="npm" label="npm">
        ```bash
        npm install my-package
        ```
      </TabItem>
      <TabItem value="yarn" label="Yarn">
        ```bash
        yarn add my-package
        ```
      </TabItem>
    </Tabs>
    ```

### 3. Technical Writing Standards

*   **Voice:** Professional yet accessible. Avoid overly academic jargon unless defined.
*   **Structure:** "Concept -> Example -> Explanation". Show, don't just tell.
*   **Formatting:**
    *   Use **bold** for key terms and UI elements.
    *   Use `code` ticks for variables, file names, and inline commands.
    *   Keep paragraphs short (3-4 sentences max).

## Usage Instructions

### Basic Usage

```
Use the book-content-writer skill to write the content for:

Chapter: [Chapter Name]
Outline:
1. [Section 1]
2. [Section 2]
...

Requirements:
- Include a code example for [Topic]
- Add a 'tip' about [Best Practice]

Note: ALWAYS read .claude/skills/book-content-writer/prompts/style-guide.md first to ensure compliance with negative constraints.
```

### Refining Content

```
Use the book-content-writer skill to improve this existing text:

[Paste rough draft]

Instructions:
- Improve flow and clarity
- Add Docusaurus admonitions where appropriate
- Ensure tone matches the "Professional Minimalist" style
- STRICTLY adhere to the negative constraints in .claude/skills/book-content-writer/prompts/style-guide.md
```

## Quality Checklist

Every generated chapter must pass this checklist:
- [ ] **Style Compliance:** ZERO usage of forbidden buzzwords (e.g., "delve", "revolutionize", "tapestry").
- [ ] **Hook:** Does the introduction clearly state *why* this matters?
- [ ] **Clarity:** Are complex concepts broken down into digestible parts?
- [ ] **Accuracy:** Is the code syntax correct?
- [ ] **Formatting:** Are headings properly nested (H1 -> H2 -> H3)?
- [ ] **completeness:** Did we cover all points in the outline?
- [ ] **Navigation:** Are there clear transitions between sections?

## Integration with Other Skills

*   **Input:** Receives outlines from `book-structure-generator`.
*   **Output:** Produces `.md`/`.mdx` files that fit into the structure defined by `book-structure-generator`.

## Example Output Structure

```markdown
---
title: "Understanding Vector Databases"
description: "A deep dive into how vector databases power modern AI applications."
sidebar_label: "Vector Databases"
---

# Understanding Vector Databases

In the world of AI, data isn't just text—it's numbers. **Vector databases** are the engine that allows us to search for "meaning" rather than just keywords.

In this chapter, you will learn:
*   What vector embeddings are.
*   How vector databases differ from traditional SQL/NoSQL databases.
*   How to set up a simple vector store.

## What are Embeddings?

Imagine representing the word "King" as a list of numbers...

:::info
Embeddings are high-dimensional vectors that capture semantic relationships.
:::

## Setting Up Your First Store

Let's initialize a simple in-memory vector store using TypeScript.

```typescript
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";

// Initialize the store
const vectorStore = await MemoryVectorStore.fromTexts(
  ["Hello world", "Bye bye", "hello nice world"],
  [{ id: 2 }, { id: 1 }, { id: 3 }],
  new OpenAIEmbeddings()
);
```

This code creates a store that... [Explanation follows]
```
