---
name: agents-md
description: Writes and edits the rules in an instruction file, whether that is `AGENTS.md`, the `CLAUDE.md` symlinked to it, or a preset's `AGENTS.partial.md`. Covers the bullet a rule lands as, how its reason and its exception attach, which rules earn a place, where a new one goes, and when a rule replaces an existing bullet instead of joining it. Invoked explicitly as `/agents-md <the rule or the change>`, and applies on its own whenever the deliverable is a rule in one of those files. Not for a skill body, which `skill-creator` owns, and not for a standalone document, which `write-document` owns.
user-invocable: true
---

# agents-md

**A rule that lands as one bullet in the section that already owns its domain, carries its own reason and its own exception, and either replaces an overlapping bullet or is not added at all.**

An instruction file is `AGENTS.md`, the `CLAUDE.md` symlinked to it, or a preset's `AGENTS.partial.md`. The rules below hold for all three. Which file a change belongs in is settled by the scope the rule holds for, which the request names rather than this skill.

## What a rule looks like

Every rule is one bullet under an H2 heading, and the file is a flat list of those bullets rather than prose. A rule inside a paragraph is read as background and a rule on its own line is read as a rule.

A rule addresses the agent directly, usually in the imperative. "Never use em-dashes" and "Cut rationale unless load bearing" are the form that gets followed. This is the one place an instruction file inverts a skill body, which states a property of a finished artifact instead, because an instruction file governs behavior rather than describing a thing.

A bullet runs one to three sentences. The first is the rule and the rest carry its reason, the failure it prevents, or its exception.

An absolute carries its exception in the same bullet. "Never commit directly to `main`, unless explicitly approved for a single operation" holds, while the same rule with its exception in another section is applied absolutely or skipped entirely, and which of the two happens varies by session.

A rule names literal strings rather than describing them. `"In order to" is "to"` is a test the agent applies the same way every time, and "avoid wordy constructions" is interpreted freshly on every session.

Emphasis is close to absent. Bold on a phrase is worth spending once or twice in a whole file, and a rule that seems to need it needs its reason stated instead.

The prose rules already in the file govern the rules written into it. A file that forbids em dashes, restatement and throat-clearing forbids them in its own new bullets first.

## Which rules earn a place

A rule earns its place by changing what the agent does. A rule describing behavior the agent already produces is loaded on every session, costs context every time, and changes nothing.

A rule is written for a failure that happened, in the terms of what went wrong. A rule invented against an imagined failure is the one that gets skipped, and it dilutes the rules next to it.

One bullet carries one rule. A second sentence giving that rule's reason belongs in it; a second sentence introducing another rule means the bullet is two bullets.

A caveat that changes the outcome is never dropped to make a bullet shorter, because the shortened rule is then wrong in exactly the case the caveat covered.

## Where a rule goes

A new rule goes in the H2 section that already owns its domain. A new section is created only when no existing section does, since a rule filed under a heading that does not describe it is found only by reading the whole file.

A rule sits next to the rules it interacts with, so that a reader who finds one finds the rest of them.

A partial carries H2 sections and nothing above them. It is spliced into a file that already has its own opening, so an H1 or a preamble written into a partial appears twice in the composed file.

## Editing what is already there

Most changes to an instruction file are edits rather than additions. The section that owns the domain is read in full before anything is added to it, because the rule being added is usually already there in weaker words.

A rule that overlaps an existing one replaces that bullet rather than joining it. Two bullets covering the same ground leave the agent to pick between them, and the weaker one wins often enough to matter.

Nothing outside the rule being changed is touched. A tightened word in a neighbouring bullet is invisible in review and changes what the agent does on every later session.

A rule that is being removed is removed rather than softened. A rule with its teeth pulled still costs its context and now describes behavior nobody wants.

## Worked example

A request to add a rule about database migrations, as it arrived and as it lands.

```markdown
Before:

  It is very important that you should always try to make sure that database migrations are handled carefully, and you should probably avoid doing anything destructive. This is CRITICAL!

After:

- A migration is additive in one deploy and destructive in the next, never both at once, because a rollback of a single deploy must not lose data the previous version wrote.
```

The throat-clearing, the hedges and the shouting come out. What is left is one bullet, in the imperative, carrying a literal test the agent can apply and the reason the test exists.
