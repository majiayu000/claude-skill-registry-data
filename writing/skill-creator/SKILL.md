---
name: skill-creator
description: User-invoked skill author. Writes or edits a skill (the frontmatter, the body, and any reference files) in the Agent Skills format, under the house writing pattern, and sized to fit the per-skill context budget. Invoked explicitly as `/skill-creator <what the skill should cover>`. Not for deciding whether an oversized skill should be split, which is the user's call.
user-invocable: true
---

# skill-creator

**Write one skill that conforms to the Agent Skills format, the house writing pattern, and the context budget. You are the author: settle the scope, write `SKILL.md`, add references only where they are needed, then report the size.**

This skill is explicit-invoke only (`/skill-creator`). It covers an edit to an existing skill as well as a new one, in which case Steps 1 and 2 are skipped wherever the name and the frontmatter already hold.

## Invocation

```
/skill-creator <what the skill should cover>
```

The argument is the subject. Everything else (the name, the structure, the size) is worked out below.

## Where the skill goes

`.agents/skills/<name>/` in the current directory by default. Create the directories if they are missing.

Another location is used when the invocation names one, such as a preset's `skills/` directory or a path outside the project. The basename of that directory is still the skill's `name`, wherever it lands.

## How a rule is written

A skill body is written under the prose discipline in `AGENTS.md`, because a skill is read the way an instruction file is read. Where `AGENTS.md` cuts rationale unless it is load bearing, a rule's reason is always load bearing and stays.

The subject of a rule is the thing being written rather than the writer, in the present tense and with no addressee. "A build has exactly two stages" rather than "write exactly two stages", because a property can be checked against the finished work while an instruction only covers the case it names.

Every rule carries the reason it exists, in the same sentence or the next one. A rule with a reason attached is followed far more often than a bare instruction, and the reason is what lets an agent extend the rule to a case the skill never anticipated.

A rule runs to one or two sentences of prose. The first states the property and the second gives the reason or names what breaks without it.

One sentence carries one idea. A sentence that has taken on a second idea splits at the point the second one starts.

A negative states the property rather than forbidding the act. "The final stage runs as a fixed non-root user" rather than "do not run as root", since the property still holds in the case the prohibition forgot to name.

`MUST`, `CRITICAL`, ALL-CAPS and `!!` stay out of the body. Emphasis belongs in the `description`, where it does routing work; in the body, emphasis without an adjacent reason reads as anxiety, and an anxious prompt produces a hedging agent.

A non-ASCII character appears only where the character is the artifact, such as a box-drawing directory tree or a glyph the tool being documented prints. Decoration, emoji, curly quotes and em dashes are none of those.

## What a body looks like

The H1 is the skill's name, and the line directly under it is a bold thesis naming what the finished work looks like when the skill has been followed. A thesis that describes what the skill is about instead tells the reader nothing the `description` did not already say.

A model-routed skill titles its H1 in Title Case and a user-invocable one uses its own slug, so an invocable skill's heading reads back as the command the user typed.

Where a heading is in Title Case, articles, conjunctions and short prepositions stay lowercase. Capitalizing them produces `Pragmas That Do Not Persist` and `Choosing Cursor Or Offset`, which read as the title of a work rather than the name of a section.

A section of rules is written as prose paragraphs rather than a bulleted list. A bullet list carries parallel items of one kind, and a rule set formatted as a list reads as a checklist and gets skimmed instead of applied.

A table carries a closed set of facts the agent checks rather than reasons about, such as field names, a catalog of valid values, a per-language mapping or a budget. It also carries a comparison the reader reads across, such as two approaches measured against the same four properties.

A criterion stays prose, because an inventory standing in for a criterion silently becomes the whole of that rule.

A code block shows the shape the rule produces and sits directly under that rule. Blocks collected into a section of their own have each lost the rule they belong to.

## Workflow

### Step 1: Settle the name and the scope

State in one line what the skill is for and when an agent should reach for it. That line becomes the seed of the `description`, so it is worth getting right before any body text exists.

The name has to satisfy the format: 1-64 characters, lowercase letters, digits and single hyphens, no leading or trailing hyphen, and identical to the directory it lives in. A mismatch between `name` and the directory makes the skill invalid rather than merely untidy.

### Step 2: Write the frontmatter

```yaml
---
name: <matches the directory>
description: <what it does, when to use it, and how it is invoked>
user-invocable: <true when the user calls it by name, false when the model routes to it>
---
```

| Field | Required | Constraint |
|---|---|---|
| `name` | yes | 64 chars or fewer, lowercase alphanumeric and hyphens, matches the directory |
| `description` | yes | 1024 chars or fewer, states both what the skill does and when to use it |
| `license` | no | License name, or the name of a bundled license file |
| `compatibility` | no | 500 chars or fewer; only when the skill needs specific tools or an environment |
| `metadata` | no | String-to-string map for anything outside the spec |
| `allowed-tools` | no | Space-separated pre-approved tools; experimental, support varies |

A value carrying a colon followed by a space, such as `for every project type: the header`, is wrapped in double quotes. YAML reads that bare colon as a key separator and the block stops parsing. A skill whose frontmatter does not parse is skipped at discovery without an error anywhere, so it never loads and nothing says why.

The `description` is the only part loaded before activation, so it is doing routing work rather than summary work. It takes one of two shapes, decided by `user-invocable`:

```
false: <what it covers> - <the concrete parts>. Use when <situation>, <situation>, or <situation>. Triggers on <literal file names, symbols, flags>.

true: <what it produces>. Invoked explicitly as `/<name> <argument>`. Not for <neighbour>, <neighbour>.
```

`Triggers on` names the literal strings that appear in a prompt or a file, and those literals are what routing matches against. A description that only says what the skill is about leaves the model guessing about when.

A user-invocable skill carries no `Triggers on`, because nothing should route to it and an incidental mention of the subject would otherwise activate it. It carries `Not for` instead, which is what keeps a neighbouring skill's work from landing in this one, and it is the clause most often dropped.

### Step 3: Write the body

Write the rules first and the examples after. A body that overruns its budget is truncated from the end, and an example is the cheaper half to lose.

One example per rule is enough, and it is the positive case. Describing what success looks like beats enumerating failure, and a prohibition against a mistake the model was not going to make can anchor it toward that mistake.

An example anchors format and never scope. A template, a file shape, or a sample of the output the rule produces is what an example is for; a list of the cases the rule covers is a boundary rather than an example, and it silently becomes the whole of the rule. State the rule as the test it applies, then let the example show what the answer looks like.

Write a prohibition only for a failure that has actually been observed. Rules invented in anticipation of a failure are the ones that get ignored, and they cost budget that a real rule needs.

### Step 4: Add references only where they earn it

Default to a self-contained `SKILL.md`. Reference files are never auto-loaded (the agent has to choose to read one, and often doesn't), so a rule that lives in a reference is a rule that may never be seen.

A reference earns its place when the material is bulk that would otherwise blow the budget (a long template, a table of domain checks) and something other than a prose suggestion forces the read: an explicit step in the workflow, or a sub-agent handed the path directly.

When references are used:

- They live in `references/` beside `SKILL.md` and are cited as `./references/<file>.md`, one level deep. Relative paths work in every client; deep chains do not.
- Every reference file is listed under a `## Start here: required reading` section in the body, marked as read-always or read-before-a-named-sub-task. A reference no one is told to read is dead weight.

```markdown
## Start here: required reading

**Always:**
- `./references/<patterns>.md`: the patterns every task in this skill follows

**When scaffolding a new command:**
- `./references/<templates>.md`: full file templates
```

### Step 5: Check the frontmatter, the characters, and the size

Every finished skill is checked before it is reported, however obviously correct it looks. `yq` alone passes a file that breaks the writing rules, so all three checks run:

```
yq --front-matter=extract -e '.name, .description' .agents/skills/<name>/SKILL.md
[ "$(yq --front-matter=extract -r .name SKILL.md)" = "$(basename "$PWD")" ] && echo name-matches-dir
rg -n '\bMUST\b|\bCRITICAL\b|!!' .agents/skills/<name>/
python3 -c "import io,sys;print(sorted({c for c in io.open(sys.argv[1],encoding='utf-8').read() if ord(c)>127}))" .agents/skills/<name>/SKILL.md
```

A non-zero exit from `yq` names the line and column that broke, and the fix is quoting the value it points at. Reading the block instead of parsing it is what lets a colon through.

The last command prints every non-ASCII character in the file. A box-drawing character in a directory tree is the artifact and stays; an em dash, a curly quote, or an emoji is decoration and comes out.

The body is loaded in full on activation, and after a compaction each skill re-attaches at its first 5,000 tokens under a shared 25,000-token budget. Past that cap the tail is dropped silently, so a skill that overruns loses content without saying so.

Keep `SKILL.md` under roughly 4,500 tokens (about 18,000 characters, well under 500 lines), which leaves headroom under the re-attach cap.

When the finished draft is over the limit, report the size and what the largest sections are, and stop there. Whether an oversized skill is trimmed or split into two is the user's call. Splitting on your own produces skills nobody asked for and a name the user has to live with.

Close by reporting the path written, the token or character count, and the reference files created, if any.

## Worked example

A request for a skill covering the project's database migration process:

```markdown
---
name: db-migrations
description: Database migrations for this project - file naming, the up and down pair, and backfilling a live table. Use when adding a migration, changing a schema, or reviewing a migration in a diff. Triggers on migrations/, ALTER TABLE, CREATE INDEX, up.sql, down.sql, and a backfill script.
user-invocable: false
---

# DB Migrations

**One deploy is additive and the next is destructive, never both at once, with every index built concurrently and every backfill batched.**

## Rules

A migration is additive in one deploy and destructive in the next. A rollback of a single deploy must not lose data the previous version wrote, and a column dropped in the same deploy that stopped writing it takes that data with it.

An index on a populated table is created concurrently. A plain `CREATE INDEX` holds a write lock for the length of the build, which on a live table is an outage.

...
```

Written to `.agents/skills/db-migrations/SKILL.md`, 2,100 characters, no references needed.
