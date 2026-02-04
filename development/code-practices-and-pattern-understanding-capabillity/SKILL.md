---
name: Code Practices and Pattern Understanding Capabillity
description: Understand the already-done code, including best practices, linting, structure, patterns, etc, by reading it smartly, catching up the necessary context to implement features, or fix bugs.
---

# Instructions

- [MUST DO] You must read the `.claude/skills/code_understander/references/[artifact].reference.md` for the respective artifact. This file contains the artifact implementation details and rules, and you MUST READ the respective artifact reference before calling the `generate` skill.

- [MUST DO] You must, when it's time to implement the feature/fix, use the `generate` skill. Always use this skill to generate files.

WHENEVER your objective is to **Create new features**, **Fix problems surgically**, or **Understand the project structure**, you MAY need to read some files. Use this SKILL references folder for that. They provide everything you need. However, ONLY if you need necessary/additional context for the implementation, because the skill should already provide sufficient context for you: As a fallback, you can always read the files, in the FOLLOWING ORDER, one by one: (Use it as the worst scenario, last option).

Order to read as a fallback (if the gained context isn't sufficient):

- Read `src/infra/database/prisma/schema.prisma` to get context about the application's database tables.
- Read the `@shared` bounded-context in the domain layer, at `src/domain/@shared`. Read all entities, value-objects, either patterns, and everything residing there.
- Read each entity and value-object related to the change you were assigned to make, in `src/domain/[bounded-context]/enterprise/entities` and `src/domain/[bounded-context]/enterprise/value-objects`.
- Read the main use cases for such entity, in `src/domain/[bounded-context]/application/use-cases`.
- Read the `@shared` module of the HTTP layer in `src/http/@shared`. Read everything residing there.
- Read each file type related to the change you were assigned to make, in `src/http/[module]`: controllers, guards, schemas, decorators, pipes, enums, services, and presenters, except tests.
- Lastly, consult the specific file for your task to edit, identified during this process of reading and context discovery through the general application files. If it is a new file (feature creation), start implementing the new files organizing them appropriately and following the application logic.
