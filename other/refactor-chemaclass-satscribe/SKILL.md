---
description: Refactor code safely — establish a green baseline, change in small steps, keep tests passing
argument-hint: "[file-or-description]"
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash(vendor/bin/phpunit *), Bash(composer *), Bash(git diff:*)"
---

# Refactor

Refactoring changes structure, never behavior. If behavior must change, that's a feature — use `/tdd` instead.

## Before touching anything

1. **Tests must exist** for the code being changed. If they don't, write characterization tests first — capture what the code *does* today, not what it should do.
2. **Establish a green baseline**:
   ```bash
   composer test
   ```
   Never refactor on red.

## Steps

3. **Name the smell** before choosing a technique.

   | Smell | Move |
   |---|---|
   | Long method | Extract method |
   | Large class (> 200 lines) | Extract collaborator |
   | Long parameter list (> 3) | Introduce a `Transfer` object |
   | Duplicated logic | Extract to a shared method or Domain value object |
   | Feature envy | Move the method to the data's owner |
   | Primitive obsession (`string $txid` everywhere) | Value object in `Domain/Data/` |
   | Growing `switch` on a type | Interface + implementations, bound in the provider |
   | `new` inside business logic | Inject the interface, bind in the ServiceProvider |
   | Query in an Action | Move it into the repository |
   | Comment explaining *what* | Rename until the comment is redundant |

4. **One refactoring at a time.** Run the narrow test after each:
   ```bash
   vendor/bin/phpunit tests/Unit/<Module>/
   ```

5. **Watch the layer boundaries while moving code** — extracting a class is the moment things drift. Interfaces land in `Domain/`, policy in `Application/`, adapters in `Infrastructure/`. Anything extracted from Domain must stay Laravel-free.

6. **Update the binding** if an extraction introduced a new interface.

7. **Full gate + style**:
   ```bash
   composer fix
   composer test
   ```

8. **Commit with `ref:`** — small and atomic, one refactoring per commit.

## Constraints

- Public behavior stays identical — tests must pass **unchanged**. Editing a test to make a refactor pass means the behavior changed.
- Do not mix a refactor with a feature or a fix in the same commit.
- Extracting a class for its own sake is not an improvement — name the smell it removes.
