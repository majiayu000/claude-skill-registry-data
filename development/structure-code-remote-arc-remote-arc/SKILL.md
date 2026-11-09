---
name: structure-code
description: Organise code the way a careful engineering team would - clear module boundaries, one job per file, folders grouped by domain, one source of truth for permissions, config, errors, text and flags, and no dead code left behind. Use this whenever you create a file, module, package, service, component or folder, add a feature that spans several files, or touch code that is already too large, in any language, even if the task only asks for behaviour.
---

# Structure code

Code that works can still be expensive to change. Left alone, agents add to
whichever file is open until it is thousands of lines long, drop every new file
into one folder, let any module import any other, and copy the same rule, constant,
permission check or error text into every place that needs it. Each copy drifts.
Each of these makes the next change slower and riskier, for people and for the next
agent. This skill applies to every layer: services, APIs, jobs, command-line tools,
libraries and user interfaces.

## When to use

Any change that adds code. Apply it to the code you add or touch. To reorganise
existing code without changing behaviour, follow `refactor-safely` as well. For
specific layouts, read `references/backend.md` for services and APIs and
`references/frontend.md` for a user interface.

## Steps

1. **Learn the project's structure first.** Read the architecture or contributing
   docs, the lint and build config and the top-level source folders. Find where it
   already keeps entry points, domain logic, data access, external clients,
   config, shared helpers and tests. The project's own convention wins over this
   skill. Copy the pattern of the nearest well-organised module, not the nearest
   file.

2. **Place each new piece before you write it.** Write a short list of the files
   you will add or change, and why each lives there:

   | Kind of code | Belongs in |
   | --- | --- |
   | Entry points: routes, handlers, commands, jobs, views | A thin layer that parses input, calls the domain and shapes output |
   | Business rules and decisions | Domain modules with no framework, transport or storage imports |
   | Reading and writing stored data | One data-access module per table, collection or aggregate |
   | Calls to another service or API | One client per service, which owns its timeouts and retries |
   | Settings and secrets | One config module that reads and validates them at startup |
   | Rules used in many places | One shared module that owns that rule (step 6) |
   | Interface text and styles | The message catalog and a style file per feature |

3. **Keep each file to one job.** Aim for under 300 lines in a hand-written file.
   Past 500, split it before you add more. Split by responsibility, such as entry
   point, rules, data access and formatting, never by cutting a file in half.
   Generated files, fixtures and data files are exempt. The same applies to
   functions: one that needs a long comment to explain its sections is several
   functions.

4. **Group folders by domain.** When a folder holds more than about 15 files,
   group them into subfolders by feature or domain, such as `billing/` and
   `devices/`, not by kind, such as `utils/` and `helpers/`. Use the same domain
   names in every layer, including tests, messages and styles, so that one search
   finds everything about a feature. Do not add a level of nesting that holds one
   file.

5. **Keep dependencies pointing one way.** Entry points depend on domain modules,
   and domain modules depend on interfaces for storage and outside services, never
   the reverse. Shared code depends on nothing feature-specific. Do not create an
   import cycle. If two features need the same thing, move it down into a shared
   module instead of importing one feature from the other.

6. **Give every cross-cutting rule one source of truth.** Each of these gets one
   named module, function or table, and every caller uses it:

   - Permissions: `can(user, "billing:manage")`, not `user.role === "owner"`
   - Config and environment: read and validated in one place, never ad hoc
   - Error codes: one list, each mapped to a status and a message in one place
   - Constants and limits, such as plans, quotas and timeouts
   - Feature flags, kept apart from permissions
   - Logging, metrics and audit events, through one helper with a fixed shape
   - User-facing text, through the message catalog, one file per language

   A copied condition drifts, and then two places disagree. Checks in a user
   interface are for display only. The server must still check every request, so
   follow `secure-change` for that side.

7. **Pass shared context explicitly.** Values that many layers need, such as the
   current user, request id, language or a database handle, travel through one
   context object, dependency injection or a provider. Do not reach for a hidden
   global or a module-level singleton that tests cannot replace. State used by one
   module stays in that module.

8. **Guard the edges.** Validate and convert input once, where it enters the
   system, into typed values. Inside, trust those types instead of re-checking
   everywhere. Convert outside errors into your own error codes at the client that
   received them.

9. **Remove what you replace.** When new code takes over from old code, delete the
   old module, its routes, data access, config, messages, styles, tests and
   fixtures, and redirect or deprecate old URLs and APIs. Dead code left beside new
   code gets copied by the next agent.

10. **Update the map.** If the project documents its modules, such as in an
    architecture file or a README, update it in the same change.

11. **Check the shape of your diff.** List the line counts of the files you added
    or grew, and any new imports between features. Search your diff for repeated
    conditions, raw constants, environment reads outside config, and user-facing
    text outside the catalog. Fix what you added, then follow `verify-and-report`.

## Stop and ask when

- The project's convention conflicts with this skill and you cannot tell which the
  user wants.
- Placing the code well means moving a lot of existing code. Propose a separate
  refactor and do the task in the existing structure.
- A split would change a public API, exported names or a stored format.
- The project has no config module, message catalog or permission helper, and
  adding one would mean a new dependency or a wide change.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Add the feature to the open file | Files grow to thousands of lines | Place it by step 2 |
| Put every new file in one folder | Nobody can find anything | Group by domain at about 15 files |
| Create `utils/` for everything | It becomes a second, unowned codebase | Put helpers in the domain that owns them |
| Query the database from a handler | Rules and storage tangle together | Go through the domain and data access |
| Copy a role check or a limit | Copies drift apart | Use the one shared rule |
| Read an environment variable inline | Missing config fails late, in production | Read it in the config module |
| Hard-code interface text | It cannot be translated or reused | Add a catalog key per language |
| Import one feature from another | Hidden coupling and cycles | Move the shared part down |
| Keep the old version "just in case" | It gets copied and maintained | Delete it and redirect |
| Reorganise the whole repository | Unreviewable, and out of scope | Structure what you touch |

## Example

Task: "Let owners change their subscription plan."

Weak plan: "Add a `/plan` endpoint to `server.js` and a button to the settings
page."

Strong plan:

```markdown
Files:
- api/billing/change-plan.ts: parse input, call the domain, map errors
- billing/plans.ts: which changes are allowed (the domain rule)
- billing/billing-store.ts: read and write the subscription row
- clients/payments.ts: the payment provider call, with timeout and retry
- auth/permissions.ts: add "billing:manage" for owners; the API and UI call can()
- errors.ts: PLAN_CHANGE_NOT_ALLOWED with its status and message key
- ui: page, hook and styles in billing/ folders; text in locales/en and locales/es
- architecture doc: add the billing module
Not changed: server.js only gains the route.
```

## Report

```markdown
Placement: <each new file and why it lives there>
File sizes: <touched files with lines before -> after>
Dependencies: <new imports between modules, and their direction>
Shared sources used: <permissions, config, errors, flags, messages>
Removed: <old code and data deleted, and redirects added>
Seen but not changed: <structure problems outside this task>
```
