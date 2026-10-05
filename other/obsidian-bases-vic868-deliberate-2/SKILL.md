---
name: obsidian-bases
description: Create and edit Obsidian Bases (.base files) with valid YAML schemas, filters, formulas, properties, summaries, and views. Use for database-like Obsidian views or when the user mentions Bases, .base files, table/card/list views, filters, formulas, or summaries.
license: MIT
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "1"
  copilot-upstream-revision: "a1dc48e68138490d522c04cbf5822214c6eb1202"
---

# Obsidian Bases

## Workflow

1. Read the existing <code>.base</code> file before editing it.
2. Define global scope with <code>filters</code>.
3. Add computed values under <code>formulas</code> only when needed.
4. Configure property display names and one or more views.
5. Validate YAML, formula references, quoting, and date/duration operations.
6. Open or query the Base in Obsidian when the CLI is available.

## Schema

~~~yaml
filters:
  and:
    - 'file.ext == "md"'
    - 'status != "archived"'

formulas:
  days_until_due: 'if(due, (date(due) - today()).days, "")'

properties:
  status:
    displayName: Status
  formula.days_until_due:
    displayName: "Days Until Due"

summaries:
  mean_rounded: 'values.mean().round(2)'

views:
  - type: table
    name: Active
    limit: 50
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - status
      - formula.days_until_due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average
~~~

Views may be <code>table</code>, <code>cards</code>, or <code>list</code>.
A <code>map</code> view depends on compatible map support.

## Filters and properties

Filters may be a single expression or recursively nested <code>and</code>,
<code>or</code>, and <code>not</code> objects. Property namespaces are:

- note properties: <code>status</code> or <code>note.status</code>
- file metadata: <code>file.name</code>, <code>file.path</code>,
  <code>file.folder</code>, <code>file.ctime</code>, <code>file.mtime</code>,
  <code>file.tags</code>, <code>file.links</code>, and
  <code>file.backlinks</code>
- formulas: <code>formula.days_until_due</code>

Use <code>file.hasTag()</code>, <code>file.hasLink()</code>,
<code>file.hasProperty()</code>, and <code>file.inFolder()</code> for indexed
file relationships. The <code>this</code> value refers to the Base itself, the
embedding note, or the active file depending on where the Base is rendered.

## Formula rules

- Guard optional properties with <code>if()</code>.
- Date subtraction returns a Duration, not a number. Access
  <code>.days</code>, <code>.hours</code>, or another numeric field before
  calling number methods such as <code>.round()</code>.
- Every <code>formula.X</code> used by a view or property configuration must
  have a matching <code>X</code> entry under <code>formulas</code>.
- Wrap formulas containing double quotes in YAML single quotes.
- Quote YAML strings containing special characters, especially colons and
  leading punctuation.

Read [Functions reference](references/FUNCTIONS_REFERENCE.md) for function and
type-specific operations, and [Examples](references/EXAMPLES.md) for complete
task-tracker and daily-notes Bases.

## Validation checklist

- The document parses as YAML and has a <code>views</code> list.
- View <code>order</code>, <code>groupBy</code>, and summaries reference defined
  note, file, or formula properties.
- Formula quoting is balanced and duration math accesses a numeric field.
- Embedded view names match exactly: <code>![[My Base.base#View Name]]</code>.

## Attribution

Adapted from <code>kepano/obsidian-skills</code> at revision
<code>a1dc48e68138490d522c04cbf5822214c6eb1202</code>. See <code>LICENSE</code>.
