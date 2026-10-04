---
name: log-decision
description: >
  Drafts a structured document, called a DR, that captures the reasoning behind a significant
  decision. Use when the user invokes /log-decision. Use it also when the conversation reaches a
  decision about architectural trade-offs or technology choices, or reaches anything the user calls
  "hard to reverse", "locked in", or "a big commitment". In those cases, suggest a DR without waiting
  to be asked.
argument-hint: "[decision title]"
allowed-tools: [Read, Glob, Edit, Write, AskUserQuestion]
---

# Log Decision

Help the user capture a Decision Record for a significant decision that is costly to change.

When the user invokes `/log-decision` with an argument, use `$ARGUMENTS` as the title. With no argument, ask for a title. When the conversation triggered this skill instead, say something like: _"This looks like a significant decision. Would you like me to draft a Decision Record (DR)?"_ Wait for confirmation before you proceed.

> **Not sure yet?** If the user is still exploring options, or has not settled on a direction, suggest `/decide` instead. That skill is a thinking partner for working through the problem before anyone documents it.

## Execution steps

### 1. Gather information

Use `AskUserQuestion` for each question, and ask about one topic area at a time. Do not present every field at once. Start with the essentials. Ask about an optional field only when the user is engaged in that level of detail.

**If the user has just come from a `/decide` session**, the conversation already holds three of the fields. Those are the Context and Problem Statement, the Forces and Constraints, and the Considered Options. Confirm the key points instead of asking again, and move straight to the Decision field and to any gap.

**Essentials**, which are always required:

| Field | Guidance |
|---|---|
| **Title** | A short phrase that names the problem and the solution, such as "Use PostgreSQL as primary datastore" |
| **Context and Problem Statement** | Which situation led to this decision, and which problem it solves. Note any relevant code location or work item that gives context. |
| **Considered Options** | Which alternatives the user evaluated. Aim for at least two. Give a brief description, the pros, and the cons for each one. Stay objective, and represent a rejected option fairly. |
| **Decision** | Which option the user chose, and why. Prefer the **Y-Statement format**: _"In the context of [situation], facing [concern], we decided [option], to achieve [quality], accepting [downside]."_ Free-form prose also works. |

**Depth**, which you ask about only when the conversation has not covered it:

| Field | Guidance |
|---|---|
| **Forces and Constraints** | Which requirements, assumptions, forces, or constraints shaped the decision |
| **Consequences** | The ramifications, both positive and negative |
| **More Information** | Extra evidence, links, or related decisions. Include links to PRs, issues, and external resources such as docs, RFCs, and benchmarks, where they apply. |

**Metadata**, which you ask about only when provenance or governance matters:

| Field | Guidance |
|---|---|
| **Status** | One of these values, with `proposed` as the default. `draft` means being written and not ready for review. `proposed` means complete and open for review or approval. `rejected` means reviewed and not adopted. `adopted` means accepted and in effect. `retired` means once adopted and no longer active, with no replacement. `superseded` means replaced by a newer decision. |
| **Date** | The date of the decision, with today as the default |
| **Decision-makers** | Who took part in making the decision |
| **Consulted** | Who was consulted, in two-way communication |
| **Informed** | Who is kept up to date, in one-way communication |

Never assume. Ask whenever something is ambiguous.

### 2. Determine the DR directory and the next number

1. Look for an existing DR directory in the project root, in this priority order: `docs/decisions/`, then `adr/`, then `.decisions/`.
2. When none of the three exists, use `docs/decisions/` and create it.
3. Scan the existing files that match `DR-*.md` to find the highest sequence number, then use `N + 1`. Start at `0001` when no file exists.
4. While you scan, note any DR whose title or content looks related to the current decision. Report those to the user, so they can reference or supersede them.

### 3. Derive the file name

- Kebab-case the title, strip the special characters, and truncate it to roughly 50 characters.
- Use the format `DR-NNNN-kebab-title.md`.
- For example: `DR-0003-use-postgresql-as-primary-datastore.md`.

### 4. Write the DR file

Read the template from `${CLAUDE_SKILL_DIR}/assets/dr-template.md`. Fill every section with the information you gathered. For an optional section with no content, remove the section and its `<!-- This is an optional element. Feel free to remove. -->` comment. Leave no placeholder text.

Include markdown links wherever they help: to the PRs or issues that motivated the decision, to external docs such as RFCs, benchmarks, and vendor pages, and to related DRs. Use a relative path for a link between DR files. Use a full web URL for every other link.

If the status is `superseded`, find the DR that this one supersedes. Add a "Superseded by [DR-NNNN](path)" note to its `## More Information` section, and append that section when it is absent. Then reference that DR in the `## More Information` section of the new file.

A DR outlives the conversation that produced it, and a reader opens it months later with none of that context. Write short sentences in the active voice, define a term that such a reader can miss at its first use, and cut filler. Keep the Y-statement shape of the Decision section, and keep every link and quoted value exactly as it is. When a plain-English writing skill such as `simple-english` is available, invoke it and apply its rules to the draft, before you write the file.

After you write the file, tell the user the file path and a one-line summary of the decision. Do not offer to improve the DR unless the user asks.
