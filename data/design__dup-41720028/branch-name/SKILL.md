---
name: branch-name
description: When naming Git branches, provide guidelines on the recommended branch naming conventions for the project.
---

## Basic Policy

- Prioritize branch names that clearly indicate their purpose at a glance
- Use a structure of prefix + `/` + identifier
- Use lowercase and kebab-case for the identifier
- Do not use characters other than alphanumeric and allowed symbols

## Prefix List

- `feat`: Add new features
- `fix`: Fix bugs in existing features
- `hotfix`: Urgent fixes that need immediate deployment
- `refactor`: Refactoring without changing functionality
- `chore`: Non-functional tasks such as dependency updates and CI configuration adjustments
- `docs`: Adding or modifying documentation (not related to functionality)
- `test`: Adding or modifying test code (not related to functionality)
- `release`: Release preparation tasks

## Identifier Naming Rules

- Keep branch names short and meaningful
- Connect words using kebab-case
- Include the issue number at the beginning if the branch is based on an issue
- Write identifiers in English