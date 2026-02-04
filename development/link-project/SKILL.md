---
name: link-project
description: Add project repository links to PROJECTS.md when user mentions completing, starting, or sharing a hands-on project. Use when user references external repos or implementation work.
allowed-tools: Read, Edit
---

# Link Project

When the user mentions a project repository they've built:

## Instructions

1. Read the current PROJECTS.md file

2. Determine the appropriate category:
   - **Machine Learning** - Classic ML algorithms, supervised/unsupervised learning
   - **Deep Learning** - Neural networks, computer vision, NLP models
   - **AI Engineering** - LLM applications, agents, RAG systems
   - **ML Systems & Production** - MLOps, deployment, monitoring, data pipelines
   - **Software Engineering** - General software projects, tools, libraries
   - **Other** - Anything that doesn't fit above

3. Add the project link in format:
   ```markdown
   - [Project Name](repo-url) - Brief description of what it does/demonstrates
   ```

4. Maintain organization:
   - Group by category (create category header if it doesn't exist)
   - Within each category, newest projects at the bottom
   - Keep descriptions concise (one line)

## Examples

```markdown
## Deep Learning

- [CNN Image Classifier](https://github.com/user/cnn-classifier) - From-scratch CNN implementation for CIFAR-10
- [Transformer from Scratch](https://github.com/user/transformer) - Educational implementation of attention mechanism

## AI Engineering

- [RAG Document QA](https://github.com/user/rag-qa) - Retrieval-augmented generation system with vector database
```

## Edge Cases

- If PROJECTS.md is empty: Create basic structure with category headers
- If project fits multiple categories: Use primary category or ask user
- If repo URL not provided: Ask user for the link
- If description not clear: Ask user what the project demonstrates
