---
name: spec-scaffold
description: Process any SDD (Specification-Driven Development) operations related to creating or updating specification documents. Always use this skill when dealing with specifications, e.g. constitution, specification document, architecture-related documents, roadmap, glossary, etc.
allowed-tools: Read, Grep, Glob, Explore, Bash(cp:*), TodoWrite
---

# Spec Scaffold

## Instructions

1. Identify the type of specification document is working on (e.g., constitution, architecture decision record).
2. Read the manual and templates provided for the specific document type before proceeding.
3. Making a plan to gather necessary information from the user or existing documentation to fill out the template.
    - Use TodoWrite to outline the steps needed to complete the document.
    - Ensure each steps in manual is covered in the plan.
4. Take one of following actions to create/update the document
    - No existing document: MUST use `cp [template_path] [destination_path]` to copy the template to the desired location.
    - Existing document needs updates: Read the existing document, identify sections that need modification, and update them accordingly.
5. According to the plan and manual, gather required information using AskUserQuestion tool if necessary.

## Document Relationship

Following are independent for each other, do not make references between them.

- Constitution: The foundational document that outlines the project's purpose, governance, and decision-making processes.
- Specification: Detailed descriptions of features, user stories, and acceptance criteria.
- Architecture: Overview of the project's architecture, design patterns, and technology stack.

Following are referenced by specification documents.

- Glossary: A collection of terms and definitions used throughout the specifications to ensure consistency and clarity.

Following are referenced by roadmaps.

- Specification: Each feature or milestone in the roadmap should link to its corresponding specification document for detailed information.

## Manual

- [Constitution](./references/constitution.md): How to write a project constitution.
- [Specification](./references/specification.md): How to write a specification document.
- [Roadmap](./references/roadmap.md): How to use roadmaps to track project progress.
- [Glossary](./references/glossary.md): The ubiquitous terms used in the project specifications.
- [Architecture](./references/architecture.md): How to document architecture and design decisions.

## Templates

- [constitution.md](./templates/constitution.md): Constitution template should be used to create project constitutions.
- [specification.md](./templates/specification.md): Specification template should be used to create specification documents.
- [roadmap.md](./templates/roadmap.md): Roadmap template should be used to initiate project roadmaps.
- [glossary.md](./templates/glossary.md): Glossary template should be used to create project glossaries.
- [architecture.md](./templates/architecture.md): Architecture template should be used to document architecture decisions.
- [adr.md](./templates/adr.md): Architecture Decision Record (ADR) template should be used to document specific architecture decisions.

## References

- [GitHub's Specification-Driven Development](https://github.com/github/spec-kit/blob/main/spec-driven.md)
