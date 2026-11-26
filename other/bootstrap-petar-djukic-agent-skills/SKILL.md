---
name: "bootstrap"
description: "I'm starting a new project and need you to help me create the initial documentation."
---

# bootstrap command

Apply this command workflow. Treat any text after its invocation as the command input.

# Command: Bootstrap Project

I'm starting a new project and need you to help me create the initial documentation.

First, read **docs/constitutions/design.yaml** to understand the documentation format rules for VISION and ARCHITECTURE documents.

Then ask me questions to understand:
1. What problem I'm trying to solve
2. What the solution will do
3. What success looks like
4. What the major components are
5. How those components fit together
6. Key design decisions and why

Based on my answers, write two documents:

## VISION.yaml

Capture the project's purpose, goals, and success criteria following the format rules in docs/constitutions/design.yaml.

## ARCHITECTURE.yaml

Capture the major components, their responsibilities, the interfaces between them, and the design decisions that constrain them, following the format rules in docs/constitutions/design.yaml.

Write both files to the `docs/` directory. Do not create any issues, epics, or tasks — documentation only.

## Validation

After writing the documents, run the repo's consistency check — **`mage audit`**, or **`mage analyze`** in repos that name the target that way — to check for broken references or missing fields.

Fix any issues before finalizing.

---

Start by asking me questions to understand the project.
