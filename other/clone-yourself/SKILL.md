---
name: clone-yourself
description: >-
  Build a private local "<your-name>-clone" skill that makes your AI work and sound like you: your writing
  voice, how you decide, judge work and report, and how you talk, learned from your own agent rules, notes and
  sent writing. Use when someone wants to clone themselves, make their AI think like them, or turn their
  working style into a reusable skill.
---

# Clone Yourself

Build `<first-name>-clone`: a local skill that answers as the user, in the first person, with their opinions and their phrasing. A good clone feels like the person, not like a policy document. It has three layers:

| Layer | What it holds | Comes from |
|---|---|---|
| Voice | how they write | `clone-my-voice` (their `my-voice` skill) |
| Judgment | how they decide, judge work, report, what they ban | `scripts/extract_rules.py` on their agent rules and notes |
| Persona | how they talk, what annoys them, phrases they really use, what they care about | their own sent writing plus their answers |

Everything stays on the user's machine. Never upload samples, rules, memory files or the generated clone to Edge, a repository or any other service. The scripts use the standard library only and make no network calls.

## 1. Voice

Run the `clone-my-voice` workflow, with its local-only rules, to create or reuse their `my-voice` skill. The clone points to it instead of copying it.

## 2. Judgment

Ask which folders hold their rules, and for a short list of people, clients and companies that appear in them. Then run:

```bash
python3 scripts/extract_rules.py [their paths] --aggressive --redact-words "Ana,Northwind,..." --out ./clone-work
```

`--redact-words` removes the names they list, wherever they appear (also inside `name-api` or `name_sync`). `--aggressive` also removes every other capitalised word in the middle of a sentence, except well-known tools and languages. Use both by default: single-word names are what pattern matching misses.

It also reads the usual places by default (`~/.claude/CLAUDE.md`, project `CLAUDE.md` and `AGENTS.md`, Cursor rules, `~/.claude/projects/*/memory/*.md`, `~/.codex/AGENTS.md`); add `--no-defaults` to read only what they name. It keeps imperative rule lines, redacts emails, URLs and domains, IP addresses, phone numbers, handles, money, long numbers, file paths and multi-word names, drops rules that only make sense with a private fact attached, dedupes, and sorts rules into decide / judge / report / bans / format / persona. It prints counts only.

If the agent runs on a hosted model, ask before reading `clone-work/rules.json` or using `--show`, because that sends the redacted rule text to the model. Offer to let the user read it themselves instead.

Turn the strongest rules (highest `count`) into a short proposed profile: about 10 rules, grouped, each tagged with its source file name. The user confirms or edits; set `"confirmed": true` on the ones they keep. Redaction is a safety net, not a guarantee: read every kept rule for names or private facts before confirming.

## 3. Persona

This layer is what makes the clone feel like a person. Build it from the user's own sent writing (the samples `clone-my-voice` used) and the `persona` rules, then ask the user to correct it:

- **How they talk:** register in chat vs in public, length, capitalization, humour, how direct they are.
- **Phrases they actually use:** only phrases that appear more than once in their own writing. Never invent catchphrases.
- **What annoys them:** what they correct, ban or complain about repeatedly.
- **What they care about:** what they push for in decisions.
- **How they push back and how they say no.**

No names, no quotes that identify another person, no private facts. Save the confirmed version as `clone-work/persona.json`:

```json
{"talk": ["..."], "phrases": ["..."], "annoys": ["..."], "cares": ["..."],
 "example": "> **User:** ...\n>\n> **Sam:** ..."}
```

The example is one short synthetic exchange in their real rhythm.

## 4. Build

```bash
python3 scripts/build_clone.py --rules clone-work/rules.json --persona clone-work/persona.json \
  --name Sam --tasks "startup tasks" --pronoun they --out ~/.claude/skills
```

Use the agent's skills folder (`~/.claude/skills/`, `~/.codex/skills/`, or the configured Cursor location; ask if unclear). It writes `sam-clone/SKILL.md`, `references/rules.md` and `references/persona.md` from `templates/`, uses only confirmed rules, refuses to overwrite without `--force`, and runs the checker.

## 5. Verify

`build_clone.py` runs `scripts/check_clone.py`, which validates the front matter and scans every file for emails, URLs, phone numbers, handles, money, paths and names. Fix every hit; it exits non-zero until clean. Allow the user's own first name with `--allow Sam`.

Then test side by side: three prompts the user picks, each answered with and without the clone. The clone's answers should be in the first person, short, opinionated and in their phrasing. If an answer reads like a consultant memo, tighten `persona.md` and rebuild.

Finish with:

`✓ <first-name>-clone created locally. Your AI can now work like you. Turn on Edge local ranking (EDGE_LOCAL_SKILLS=1) and Edge offers it whenever a task needs your judgment.`
