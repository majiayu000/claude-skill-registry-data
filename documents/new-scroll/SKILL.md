---
name: new-scroll
description: Iroh writing a new scroll for the library. Use for authoring or modifying a skill, writing or editing a SKILL.md, "create a skill", "add a skill to the plugin", "improve this skill's description", "split this skill into references", or a workflow you keep repeating that no skill captures yet. Covers frontmatter, description triggers, progressive disclosure, references and scripts, and skills that load the same way on Claude Code and Codex.
---

# A new scroll for the library

Iroh carried a library in his head and shared only what the moment called for. A good scroll is the same. It says exactly when to open it, gives the essential teaching on the first page, and keeps the long commentary in the back for the reader who needs it. You own the scroll's voice.

## Steps

1. **Check the library first.** Search the existing skills for one that already covers the workflow. Extend it instead of writing a near-duplicate. Write a new skill only for a workflow you keep hitting that no skill captures.
2. **Collect concrete triggers.** Write down three to five real requests that should load the skill, in the words a user would type, including any old command names people already use. These become the description.
3. **Plan the contents.** For each trigger, ask what an agent would otherwise rewrite or rediscover each time. Code it rewrites goes in `scripts/`. Long reference material it rereads goes in `references/`. Files copied into the output go in `assets/`. Create only the folders you use.
4. **Write the frontmatter.** See [Frontmatter](#frontmatter).
5. **Write the body.** See [The body](#the-body). Write it through `tea-time`.
6. **Validate.** See [Validate](#validate). In this plugin, that means registering the skill, regenerating the tables, and running the validator.
7. **Test it if it is structural.** A skill that changes what an agent does (steps, routing, a checklist, a script) gets a behavior test. Run `pai-sho` on it before you promote it. A purely stylistic skill skips this step. Record `skip: subjective` in the todolist.
8. **Ship it.** Hand to `yip-yip`.

## Frontmatter

Both Claude Code and Codex read a skill from `skills/<name>/SKILL.md` and decide whether to load it from two frontmatter fields. Use exactly these two so both runtimes read the file the same way.

```yaml
---
name: new-scroll
description: Iroh writing a new scroll for the library. Use for authoring or modifying a skill, ...
---
```

- **`name`** equals the directory name. Lowercase words joined by hyphens.
- **`description`** is one line, under 1024 characters. Both runtimes keep every skill's description in context all the time, so every word costs. Say what the skill does and when to use it, then list the trigger phrases from step 2 in quotes. Include the old command name when the skill replaces one ("Use for babysit, /babysit, get this green") so old habits still work.
- In this plugin, the description opens with the character theme, then the plain trigger words.
- Do not wrap the description across lines or quote it with YAML block syntax. The validator reads one `key: value` line.

A weak description says "Helps with PRs." A strong one names the job and the exact phrases ("Use for opening a pull request, 'ship it', 'open a PR', 'write the PR description'").

## The body

**Progressive disclosure.** A skill loads in three levels. The frontmatter is always in context. The SKILL.md body loads when the skill triggers. Files in `references/` and `scripts/` load only when the body sends the agent to them. Put each piece of information at the lowest level that still gets it read when it is needed.

- Keep SKILL.md the quick path. The steps, the rules, and the reply contract belong there. Aim for under about 2,000 words.
- Move long detail (full catalogs, rubrics, schemas, worked examples, edge cases) to `references/<topic>.md`. Link it from SKILL.md with a relative Markdown link to `references/<topic>.md`, and say when to read it. `tea-time` is a working example.
- Keep references one level deep. A reference file does not send the reader to a third file for the core of its content.
- Put each fact in one place. Do not repeat a reference's content in SKILL.md.
- For a reference over about 10,000 words, give grep patterns in SKILL.md so the agent can find the part it needs.

**Scripts.** A script earns its place when the same code would be rewritten each time or when the result must be deterministic. Scripts run with plain `node` or `sh`, with no npm dependencies. Give the exact command to run, with the path relative to the skill, and say what its output means.

**Writing.**

- Open with a one-paragraph character framing, as the other skills here do. Everything after it is plain.
- Write imperative instructions to the agent that will run the skill. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one.
- When in doubt, delete. Keep only prose that changes a decision. Match the tone to the scope.
- Point at structural sources (types, READMEs, config, a validator) instead of restating them. When you write the same instruction a second time, encode it in a check instead (Encode Lessons in Structure, Fire in `four-elements`).
- Delegate to other skills by name. Do not restate them. Write a skill name in backticks after a routing word ("Run `seismic-sense`", "Hand to `yip-yip`"). The validator checks that each one exists.
- End with a **Reply** section that names what the final answer contains.

**Two runtimes.** Write in Claude Code tool names. A skill that dispatches subagents, asks fixed-choice questions, or uses task tools adds this line near the top, with the relative path fixed for the file's depth.

```markdown
On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.
```

- A skill loads as `team-avatar:<name>` on Claude Code and as `$<name>` on Codex.
- Dispatch a character with `subagent_type: "team-avatar:<character>"`. Codex has no agent types, so the codex reference says how to spawn the same character.
- Name models through the avatar-setup sheet lines (for example "Iroh's model from the avatar-setup sheet", or the `panel` line for a review panel). Do not hard-code a model, and do not invent a sheet line.
- Never write a path outside the skill that only exists on one machine. Use paths relative to the skill file.

## Validate

For any skill, check these before you ship.

- The frontmatter has `name` and `description`, and `name` matches the directory.
- Every file the skill links or names exists.
- Every cross-skill reference resolves to a real skill.
- Every script runs with the command the skill gives.
- The text has no long dash characters.

When the skill belongs to this plugin, also do these three things from the repository root.

1. Register the skill in `plugins/team-avatar/team.json`. Add `{ "name": "<name>", "owner": "<character>", "from": [] }` to `skills`. The owner is the character whose discipline fits.
2. Regenerate the roster tables and the agents' skill lines.

   ```bash
   node scripts/generate-team-avatar.mjs
   ```

3. Run the validator and fix every line it prints.

   ```bash
   node scripts/validate-team-avatar.mjs
   ```

   It prints `team-avatar OK` with the skill and agent counts when everything passes.

If the owner's agent file should load the skill by default, add a `Load` line to the hand-written part of `agents/<character>.md`. Never edit between the `<!-- team:... -->` markers. The generator owns those.

To try the skill in a live session, run `claude --plugin-dir plugins/team-avatar` from the repository root and type one of the trigger phrases. On Codex, add the local checkout as a plugin marketplace, as the plugin README describes, and invoke `$<name>`. Check that the skill loads from the phrase alone.

## Reply

A summary of the skill, the key design decisions (what went in SKILL.md, what went in references, what you left out), and the validation output.
