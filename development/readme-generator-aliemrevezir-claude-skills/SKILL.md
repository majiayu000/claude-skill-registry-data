---
name: readme-generator
description: >
  Generate a comprehensive, developer-friendly README.md in English by analyzing the project structure and source code. This skill scans the repository to understand the project's purpose, technical implementation, and setup requirements. Use this when a user asks to create, initialize, or update a README file for their project.
allowed-tools:
  - Bash
  - Read
---

# README Generator Skill

This skill automates the creation of high-quality, developer-friendly README.md files in English by performing a deep analysis of the local codebase.

## Workflow

1.  **Project Discovery**:
    *   List files in the root directory to identify the project type (e.g., `package.json` for Node.js, `requirements.txt` or `pyproject.toml` for Python, `go.mod` for Go).
    *   Identify the project name and primary programming languages.

2.  **Code Analysis**:
    *   Read entry point files (e.g., `index.js`, `main.py`, `src/App.tsx`) to understand the core logic.
    *   Identify key dependencies and their roles.
    *   Scan for configuration requirements like environment variables (`.env.example`).

3.  **Content Generation**:
    *   Draft the README in English with a professional yet "dev-friendly" tone.
    *   Include the following mandatory sections:
        *   **Project Title**: Clear and concise.
        *   **Description**: A "What it does" section explaining the value proposition.
        *   **Technical Overview**: A brief explanation of the internal architecture and code structure.
        *   **Features**: Bullet points of key functionalities.
        *   **Prerequisites**: Tools or versions needed (e.g., Node.js v18+).
        *   **Installation**: Step-by-step setup commands.
        *   **Usage**: Examples of how to run or use the project.
        *   **Contributing**: Basic guidelines for others to help.
        *   **License**: Default to MIT if not specified, or detect existing LICENSE file.

## Guidelines for Claude

*   **Tone**: Use active voice and developer-centric language. Avoid overly corporate jargon.
*   **Formatting**: Use clear Markdown hierarchy (H1 for title, H2 for sections). Use code blocks for all terminal commands and code snippets.
*   **Accuracy**: Do not hallucinate features. Only document what is actually present in the code or explicitly requested by the user.
*   **Context**: If the project is complex, create a "Directory Structure" section to help users navigate the source code.

## Examples

### Example 1: User asks for a new README
**User**: "Can you create a README for this project?"
**Claude**: (Uses `ls` and `Read` to explore) "I've analyzed your Python FastAPI project. I'll generate a README.md that covers the async endpoints, Pydantic models, and Docker setup I found."

### Example 2: Updating an existing project
**User**: "Update my readme to reflect the new auth changes."
**Claude**: (Scans `src/auth` and `middleware`) "I see you've added JWT authentication. I will update the 'Usage' and 'Technical Overview' sections of the README.md to include these security details."

## Technical Overview Section Requirements
When writing the "Technical Overview" part of the README:
*   Mention the core frameworks used.
*   Briefly describe how data flows through the application (e.g., "The application uses a Redux-Saga pattern to handle asynchronous side effects...").
*   Highlight specific design patterns if they are prominent (e.g., Factory pattern, Middleware, etc.).