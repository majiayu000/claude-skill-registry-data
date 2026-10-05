---
name: skill-builder
version: 1.0.0
description: |
  Meta-skill. Turns a repeated workflow (or "make this into a skill" / "turn
  what we just did into a skill") into a correct, house-style SKILL.md written
  to the canonical location. Elicits name + purpose + triggers + inputs + steps
  + outputs + gotchas, generates valid frontmatter with STRONG trigger phrases
  (so auto-invocation actually fires), decides CLAUDE.md-vs-Skill, runs a
  validation checklist (Windows paths, no secrets, runnable steps), and offers
  to register a /command alias + a one-line MEMORY.md pointer.

  Tuned for SkynetLabs: this is the consistent mint-press so every new skill
  matches the existing house pattern (fanout-ship / upwork-proposal /
  code-audit-fanout style).

  Trigger when user says: "build a skill", "make a skill", "new skill",
  "skill-builder", "/skill-builder", "turn this into a skill", "turn what we
  just did into a skill", "save this workflow as a skill", "I keep doing X,
  make it repeatable", or describes a workflow they repeat by hand.

  Auto-trigger heuristic: user describes a multi-step procedure they have run
  ≥2 times and asks to "save", "reuse", "templatize", or "make repeatable".
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# skill-builder — the SkynetLabs skill mint-press

Goal: produce a SKILL.md a future session will actually auto-invoke and follow,
matching the house style of the skills already in `~/.claude/skills/`.
Not a doc. A loadable procedure.

## First thing to do (every run): triage CLAUDE.md vs Skill

Before writing anything, classify the request (lesson from `claude-code-mastery.md`):

- **Facts that are ALWAYS true** (deploy targets, credentials location, host quirks,
  client names, fixed conventions) → belongs in `CLAUDE.md`, NOT a skill.
  Say so and offer to append to the right CLAUDE.md instead. Stop.
- **A procedure you'd otherwise re-paste / re-explain** (a multi-step workflow with
  inputs and outputs) → this is a skill. Proceed.
- Mixed? Split: facts → CLAUDE.md, procedure → skill that _references_ the facts.

> Rule of thumb: "CLAUDE.md = facts always true; Skill = procedures you'd re-paste."
> A skill that's just a list of facts will bloat context for zero leverage.

## Inputs to elicit

If the user already described the workflow (or said "turn what we just did into a
skill"), MINE the conversation first — don't re-ask what you can infer. Then fill
gaps with ONE batched `AskUserQuestion`. Capture all 7:

1. **name** — kebab-case, ≤ 3 words, verb-y if it's an action (`cv-tailor`,
   `ghl-video-drip`). Must be unique vs existing skills (glob to check).
2. **one-line purpose** — what it does + for whom, in one sentence.
3. **trigger phrases** — 5-9 literal phrases a user would type, INCLUDING the
   `/name` slash form. These drive auto-invocation — weak triggers = dead skill.
4. **inputs** — what the user must provide each run (a file? a URL? a JD? a topic?).
5. **steps** — the ordered procedure. The load-bearing part. Get the real steps,
   including the order-matters gotchas.
6. **outputs** — the artifact(s) produced + WHERE they're written (absolute path).
7. **gotchas** — the hard-won traps ("NVENC broken → libx264", "videoUrl in col 6
   not col 5", "this host = manual ZIP not GitHub auto-deploy"). These are gold —
   bake every one in.

If the user is vague, ask for the steps before generating. Never invent a procedure.

## House style (extracted from fanout-ship / upwork-proposal / code-audit-fanout)

Match this exactly:

### Frontmatter

```yaml
---
name: <kebab-case> # MUST equal the folder name
version: 1.0.0 # start here; bump on real change
description: | # pipe block, multi-paragraph
  <2-4 line prose blurb: what it does, the win, the mechanism>

  <optional second paragraph: who it's tuned for / distilled-from receipt>

  Trigger when user says: "<phrase>", "<phrase>", "/<name>", ... (5-9 literal)

  Auto-trigger heuristic: <one concrete condition> (optional but preferred)
license: MIT
compatibility: claude-code
allowed-tools: # ONLY tools the steps actually use — least privilege
  - Read
  - Write
  - Edit
  - ...
---
```

The `description` is the single most important field — it's all a future session
sees when deciding whether to load the skill. Pack it with literal trigger phrases.

### Body sections (use the ones that fit; this is the menu, not a mandate)

- `# <name>` + one-line goal restatement
- `## When to use` — USE when ALL true / SKIP when (bullet lists)
- `## Inputs` — what the user supplies; what to ask if missing
- `## The N-step recipe` or `## Workflow` — numbered, runnable, with code blocks
- `## Templates` — paste-and-go blocks (orchestrator prompt, output format)
- `## Output format` — the exact structure to emit
- `## Files` — list of helper files in the skill folder (only if they exist)
- `## Failure modes + fixes` — a `| Failure | Cause | Fix |` table
- `## Anti-patterns` — `❌` bullets
- `## Quality checklist` — `[ ]` items to self-verify before delivering
- `## Cost model` — when worth it / when to skip (for heavy/parallel skills)

Density: terse, imperative, concrete numbers and real paths. No filler, no "this
powerful skill will help you". Arrows (`→`) for flows. Receipts where they exist
("distilled from batch7 2026-05-30").

## The recipe

### 1. Triage (CLAUDE.md vs Skill)

Per section above. If facts-only → redirect to CLAUDE.md and stop.

### 2. Elicit the 7 inputs

Mine the conversation, then one batched `AskUserQuestion` for gaps.

### 3. Check name is free

```
Glob: ~/.claude/skills/<name>/SKILL.md
```

If it exists → confirm overwrite or pick a new name. Also glob `**/<name>/SKILL.md`
in case it's nested under a plugin pack.

### 4. Generate the SKILL.md

Write house-style frontmatter + body. Trigger phrases must include `/<name>` and
5-9 natural phrases. `allowed-tools` = least privilege (only what steps use). Keep
all gotchas as explicit rules in body.

### 5. Write to canonical location

```
~/.claude/skills/<name>/SKILL.md
```

This is canonical. NOTE: `~/.claude/commands/<name>.md` ALSO registers
`/<name>` — custom commands are merged into skills — but `skills/<name>/SKILL.md`
is the house standard. Use it unless the user explicitly wants a bare command.

### 6. Validate (run the checklist below)

### 7. Offer the two add-ons

- **`/command` alias** — the skill name already gives `/<name>`. Only create a
  separate `commands\<name>.md` if the user wants a different alias or a thin
  wrapper. Ask before creating.
- **MEMORY.md pointer** — offer to append ONE line to your memory manifest
  (`~/.claude/.../memory/MEMORY.md`) so the skill is
  discoverable later. Keep it to the manifest format (one line, per memory-hygiene
  rule — manifest only, no dump).

## Validation checklist (run before declaring done)

- [ ] `name:` in frontmatter == folder name == kebab-case
- [ ] `description:` is a pipe block with a prose blurb
- [ ] `Trigger when user says:` line present with 5-9 literal phrases incl. `/<name>`
- [ ] Auto-trigger heuristic present (or consciously omitted)
- [ ] `allowed-tools` lists ONLY tools the steps use (least privilege)
- [ ] Steps are runnable — no hand-wave; order-matters gotchas called out
- [ ] All paths are absolute or `~/`-relative, OS-appropriate
- [ ] PowerShell-safe commands where shell is shown ($null not /dev/null, $env:VAR)
- [ ] NO secrets / API keys / tokens hardcoded — reference where they live instead
- [ ] Every gotcha the user gave is encoded as an explicit rule
- [ ] Output artifact path is explicit and absolute
- [ ] Frontmatter is valid YAML (pipe block indented, no tabs)
- [ ] Not facts-only (would belong in CLAUDE.md) — it's a real procedure

## Output format (what to report after writing)

```
SKILL CREATED: <name>
Path: ~/.claude/skills/<name>/SKILL.md
Triggers: <list>
Tools: <allowed-tools>
Validation: <N/N checks passed, or list failures>
Add-ons offered: /command alias? <y/n>  MEMORY.md pointer? <y/n>
Reload note: new skills register on next session — /clear or restart to pick it up.
```

## Adopting a loose skill file

A common first use: an unfiled-but-good `SKILL.md` is sitting somewhere outside the
canonical skills tree (e.g. a Desktop or Downloads folder), so no session can
auto-invoke it. **Filing it is a canonical use of skill-builder.**

To adopt it:

1. Read the loose `*-SKILL.md`. Check its frontmatter `name:` and whether it's
   already house-style — often minimal rework is needed.
2. Create folder `~/.claude/skills/<name>/`.
3. Write the content to `~/.claude/skills/<name>/SKILL.md`
   (verify name == folder == kebab-case).
4. Run the validation checklist against it. (If it references helper files under
   `prompts/`, `templates/`, `references/` that don't exist yet — either create
   stubs or strip the `## Files` section so it doesn't promise missing files.)
5. Offer a one-line MEMORY.md pointer.
6. Remove any stale copies only after confirming the filed version reads back
   correctly — ask first.

## Failure modes + fixes

| Failure                       | Cause                                         | Fix                                                              |
| ----------------------------- | --------------------------------------------- | ---------------------------------------------------------------- |
| New skill never auto-invokes  | Weak/missing trigger phrases in `description` | Add 5-9 literal phrases incl. `/<name>` + auto-trigger heuristic |
| Skill loaded but ignored      | `name:` ≠ folder name                         | Make them identical, kebab-case                                  |
| Context bloat, zero leverage  | It was facts, not a procedure                 | Move to CLAUDE.md; delete the skill                              |
| Steps not reproducible        | Vague "do the thing" steps                    | Re-elicit real commands + order-matters gotchas                  |
| Secret leaked into skill file | Hardcoded key/token                           | Replace with pointer to where the secret lives                   |
| `/command` doesn't appear     | New skill not loaded this session             | `/clear` or restart — skills register at session start           |
| Path breaks on this box       | Unix paths / forward slashes                  | Windows absolute paths, backslashes, PowerShell-safe             |
| Duplicate skill               | Didn't glob for existing name                 | Glob `**\<name>\SKILL.md` before writing                         |

## Anti-patterns

- ❌ Writing a skill for facts that belong in CLAUDE.md
- ❌ Thin trigger list (1-2 phrases) → skill is invisible to auto-invocation
- ❌ Granting all tools "to be safe" → grant only what steps use
- ❌ Inventing steps the user never confirmed
- ❌ Dropping the user's hard-won gotchas to keep it short — gotchas are the value
- ❌ Writing to a random folder instead of `.claude/skills/<name>/`
- ❌ Unix paths / `/dev/null` on a Windows box
- ❌ Re-asking inputs already stated in the conversation
- ❌ Promising `## Files` helpers that don't exist

## Cost model

- Cheap: one file write + a few globs. Worth it any time a workflow recurs ≥2×.
- The leverage is downstream: a well-triggered skill saves the re-prompt cost on
  every future run and keeps idle token cost at ~0 (loads only when invoked).
- Skip only for true one-offs you'll never repeat.

---

**House references:** `~/.claude/skills/fanout-ship/SKILL.md`,
`~/.claude/skills/upwork-proposal/SKILL.md`, and
`~/.claude/skills/code-audit-fanout/SKILL.md` (once filed) are the
canonical style exemplars. When in doubt, copy their density and structure.
