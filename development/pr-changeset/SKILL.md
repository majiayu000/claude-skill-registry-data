---
name: pr-changeset
description: Create changesets for package changes in pull requests. Use whenever you modify code in any package (packages/*). Required before committing changes to packages. Handles versioning with patch for bug fixes, minor for features, and major only when explicitly requested.
allowed-tools: Write, Read, Bash, Grep, Glob
---

# PR Changeset Skill

This skill helps you create proper changeset files when making changes to packages in the monorepo. **You MUST use this skill whenever you modify code in any package.**

## When to Use

- **ALWAYS** when modifying files in `packages/*`
- Before committing changes to any package
- When creating or updating a pull request that affects packages
- Even for small changes (typo fixes, documentation updates in packages)

## Versioning Rules

### Patch (bug fixes only)

- **Use for**: Bug fixes, typos, documentation fixes, minor refactors that don't change behavior
- **Format**: Maximum 2 lines
- **Example**:
  ```
  Fix validation error in text field when value is null
  ```

### Minor (feature improvements)

- **Use for**: New features, enhancements, non-breaking API changes
- **Format**: Explain the new feature and any steps required to implement it
- **Example**:

  ```
  Add support for custom field validation functions

  You can now pass a custom validation function to field configs:

  fields: {
    email: text({
      validation: {
        custom: async (value) => {
          if (!value.endsWith('@company.com')) {
            throw new Error('Must use company email')
          }
        }
      }
    })
  }
  ```

### Major (breaking changes)

- **Use for**: Breaking API changes, removed features, changed behavior
- **ONLY when user explicitly requests a major version bump**
- **Format**: Detailed explanation of breaking changes and migration steps
- **Example**:

  ```
  BREAKING: Remove deprecated `useAuth` hook

  The `useAuth` hook has been removed. Use `useSession` instead:

  // Before
  const { user } = useAuth()

  // After
  const { data: session } = useSession()
  const user = session?.user
  ```

## Instructions

### Step 1: Identify Changed Packages

1. Run `git status` or `git diff` to see which packages were modified
2. List all packages that have changes in `packages/*/src/` or `packages/*/package.json`

### Step 2: Determine Version Bump Type

For each changed package, ask yourself:

- **Is this a bug fix?** → Use `patch`
- **Is this a new feature or enhancement?** → Use `minor`
- **Is this a breaking change?** → Only use `major` if user explicitly requested it, otherwise ask user

### Step 3: Create Changeset File

Changesets are stored in `.changeset/` directory with random names. Use this format:

**File name**: `.changeset/[random-words].md`

- Generate random filename like: `brave-lions-smile.md`, `quiet-trees-dance.md`
- Use 3 random dictionary words separated by hyphens
- Must end with `.md`

**File format**:

```markdown
---
'@opensaas/package-name': patch
---

Brief description of the change
```

**For multiple packages**:

```markdown
---
'@opensaas/stack-core': minor
'@opensaas/stack-ui': patch
---

Description of changes affecting both packages
```

### Step 4: Write the Changeset Description

**For patch versions** (bug fixes):

- Maximum 2 lines
- State what was fixed
- Be concise and clear

**For minor versions** (features):

- Explain what the feature does
- Provide code examples showing how to use it
- Include any configuration or setup steps
- Show before/after if applicable

**For major versions** (breaking changes):

- Clearly mark as BREAKING
- Explain what changed and why
- Provide migration guide with before/after code examples
- List any removed or changed APIs

## Template

Use this template when creating changeset files:

### Patch Template

```markdown
---
'@opensaas/stack-[package]': patch
---

[One line describing the bug fix]
```

### Minor Template

```markdown
---
'@opensaas/stack-[package]': minor
---

[Feature description]

[Usage example with code]
```

### Major Template

```markdown
---
'@opensaas/stack-[package]': major
---

BREAKING: [What changed]

[Detailed explanation of the breaking change]

Migration guide:
// Before
[old code]

// After
[new code]

[Any additional steps required]
```

## Examples

### Example 1: Patch (Bug Fix)

File: `.changeset/calm-eagles-rest.md`

```markdown
---
'@opensaas/stack-core': patch
---

Fix validation error in text field when value is null
```

### Example 2: Minor (New Feature)

File: `.changeset/brave-lions-smile.md`

```markdown
---
'@opensaas/stack-ui': minor
---

Add dark mode support to AdminUI component

You can now enable dark mode by passing the `theme` prop:

<AdminUI
  context={context}
  config={config}
  theme="dark"
/>

Or use system preference:

<AdminUI
  context={context}
  config={config}
  theme="system"
/>
```

### Example 3: Multiple Packages (Minor)

File: `.changeset/quiet-trees-dance.md`

```markdown
---
'@opensaas/stack-core': minor
'@opensaas/stack-auth': minor
---

Add support for custom session fields in access control

You can now access custom session fields in access control functions:

// In authConfig
authConfig({
sessionFields: ['userId', 'email', 'role', 'tenantId']
})

// In access control
access: {
operation: {
query: ({ session }) => {
return { tenantId: session.tenantId }
}
}
}
```

### Example 4: Major (Breaking Change) - Only if explicitly requested

File: `.changeset/ancient-stars-fall.md`

```markdown
---
'@opensaas/stack-core': major
---

BREAKING: Remove `getContext()` synchronous variant

The synchronous `getContext()` function has been removed. All context creation is now async.

Migration guide:

// Before
const context = getContext({ userId })

// After
const context = await getContext({ userId })

Make sure to add `async` to any functions that call `getContext()`:

// Before
function myAction() {
const context = getContext({ userId })
}

// After
async function myAction() {
const context = await getContext({ userId })
}
```

## Common Mistakes to Avoid

1. **Don't use major unless explicitly requested**
   - Even significant features should be minor if they don't break existing code
   - Ask user first if you think a major bump is needed

2. **Don't make patch descriptions too long**
   - Keep it to 2 lines maximum
   - Just state what was fixed

3. **Don't forget to include code examples for minor changes**
   - Users need to understand how to use new features
   - Show concrete examples, not just descriptions

4. **Don't create changesets for examples or non-package changes**
   - Only create changesets for files in `packages/*`
   - Changes to `examples/*` don't need changesets

5. **Don't use vague descriptions**
   - Bad: "Fix bug"
   - Good: "Fix validation error in text field when value is null"

6. **Don't forget to list all affected packages**
   - If your change affects multiple packages, list them all
   - Use the same version bump type for related changes

## Workflow

When working on a PR:

1. Make your code changes
2. **Before committing**, use this skill to create a changeset
3. Verify the changeset file was created in `.changeset/`
4. Commit both your changes AND the changeset file
5. Push to the PR branch

## Troubleshooting

**Q: Should I create one changeset per package or one for all changes?**
A: Create one changeset that lists all affected packages. Only create multiple changesets if you have unrelated changes.

**Q: What if I'm not sure if it's patch or minor?**
A: Ask yourself: "Does this add new functionality or just fix existing functionality?" New = minor, fix = patch.

**Q: What if the change is both a feature and a bug fix?**
A: Use minor (the higher version bump). Mention both aspects in the description.

**Q: Do I need a changeset for documentation changes in packages?**
A: Yes, if the docs are in `packages/*/src/` or affect the package. Use patch. Changes to example documentation don't need changesets.

## Important Notes

- The changeset CLI doesn't work in this environment, so you must manually create the `.changeset/*.md` files
- Version bumping and publishing happens automatically in CI via changesets GitHub Action
- Every PR that changes package code MUST include a changeset file
- The monorepo uses pnpm workspaces - make sure package names match `package.json`
