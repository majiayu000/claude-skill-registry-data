---
name: migrate-specs
description: "Sync OpenSpec delta specs into canonical specs with explicit dry-run/apply flow."
---

# Migrate Specs

Use this skill to synchronize `openspec/changes/<change>/specs/*/spec.md` into `openspec/specs/*/spec.md` without archiving the change.

## Usage

```text
$migrate-specs
```

## Execution Flow

1. Resolve target change (`openspec list --json` if needed).
2. Preview migration:

```bash
npm run sbk -- migrate-specs --change <change-id>
```

3. Apply migration:

```bash
npm run sbk -- migrate-specs --change <change-id> --apply
```

4. Validate:

```bash
openspec validate --all --strict --no-interactive
```

5. Update `openspec/changes/<change>/tasks.md` evidence rows with migration outcomes.
