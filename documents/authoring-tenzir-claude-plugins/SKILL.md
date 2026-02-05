---
name: authoring
description: Author documentation for Tenzir projects. Use when creating or updating tutorials, guides, explanations, reference, or integrations.
---

# Authoring Documentation

Author documentation for Tenzir projects following the Diátaxis framework.

## Diátaxis Framework

Tenzir documentation uses the Diátaxis framework, which organizes content into
four quadrants based on user needs:

| Section          | Purpose                   | Reader question          |
| ---------------- | ------------------------- | ------------------------ |
| **Tutorials**    | Learning-oriented lessons | "I want to learn"        |
| **Guides**       | Goal-oriented how-tos     | "I want to accomplish X" |
| **Explanations** | Understanding-oriented    | "I want to understand"   |
| **Reference**    | Information-oriented      | "I need facts"           |

See [diataxis.md](./diataxis.md) for the decision tree and section guidelines.

## Integrations

Separately from Diátaxis, **Integrations** documents third-party products:
"How do I use X with Tenzir?"

Organized by vendor/category: `integrations/<category>/<product>.mdx`

## Directory Structure

Documentation content lives at `src/content/docs/` relative to the documentation root.

```
src/content/docs/
├── tutorials/      # Learning-oriented projects
├── guides/         # Task-oriented how-tos
├── explanations/   # Conceptual understanding
├── reference/      # Technical specifications (some auto-generated)
└── integrations/   # Third-party products by vendor
```

## File Format

- Use `.mdx` for new files
- Add frontmatter with `title` and `description`
- Use `tql` as the language identifier for TQL code blocks

See [format.md](./format.md) for frontmatter and code block details.

## Writing Style

Invoke `prose:technical-writing` for detailed style guidance.

## Workflow

1. Run `/docs:write` to create or update documentation
2. Run `/docs:review` to check completeness and style
3. Create a PR using `git -C .docs` and `gh pr create --repo tenzir/docs`
