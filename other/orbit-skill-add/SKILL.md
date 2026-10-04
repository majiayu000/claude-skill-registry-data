---
name: orbit-skill-add
description: Meta-skill — generate a new `/orbit-*` skill following the Orbit pattern. Asks for the skill's purpose, scaffolds a SKILL.md with frontmatter + sections (purpose, quick start, what it checks, examples, output format, pair-with), and registers it in SKILLS.md. Use when the user says "add a skill", "create new orbit skill", "extend orbit", or has spotted a use case the existing 44 skills don't cover.
---

# 🪐 orbit-skill-add — The skill that creates skills

Orbit is designed to grow. This is the meta-skill that helps you contribute new `/orbit-*` skills following the established pattern — so the next one matches the rest.

---

## When to use this

You spotted a gap. Examples:
- "Orbit has no `/orbit-elementor-version-compat` — there should be one"
- "WPML is huge but no `/orbit-wpml-compat`"
- "Hosting-specific compat (WP Engine, Kinsta) isn't covered"
- "Need a Stripe / PayPal integration test"

Also useful for forking Orbit into a private suite for your own org's WP plugins.

---

## Quick start

Tell the wizard what you want:

> "I want a skill that audits my plugin's compatibility with the Polylang translation plugin."

The wizard will ask:
1. Skill name (`orbit-polylang-compat`)
2. One-sentence purpose
3. Trigger phrases (`"polylang"`, `"WPML alternative"`, etc.)
4. Plugin types it applies to (Theme / WC / SEO / generic)
5. Existing tools it wraps (PHPCS sniff? a Playwright spec? a WP-CLI command?)
6. Pair-with skills

It scaffolds:
- `skills/orbit-polylang-compat/SKILL.md` (the skill file)
- An entry in `SKILLS.md`
- Optional: a script in `scripts/check-polylang.sh`
- Optional: a Playwright spec template

---

## SKILL.md template

```markdown
---
name: orbit-<name>
description: One-paragraph purpose. Trigger phrases for invocation. What's the input, what's the output?
---

# 🪐 orbit-<name> — <short tagline>

<3-line description: what this skill does, when to use it, what it produces>

---

## Quick start

```bash
<one-command invocation>
```

Output: `reports/<name>-<timestamp>.md`.

---

## What it checks

### 1. <Aspect>
```php
// ❌ Bad pattern
<code>

// ✅ Good pattern
<code>
```

### 2. <Next aspect>
...

---

## Output format

```markdown
# <Name> — [Plugin]

## Summary
| ... | ... |

## Critical / High / Medium / Low findings
[file:line, code, fix per finding]
```

---

## Common findings + fixes

| Finding | Fix |
|---|---|
| ... | ... |

---

## Pair with `<related-skill>`

<How they complement each other>

---

## When to run

- Trigger 1
- Trigger 2

---

## Hard rules

- Rule 1
- Rule 2
```

---

## Naming conventions

| Pattern | Use for |
|---|---|
| `orbit-<thing>` | Specific tool / topic (orbit-multisite, orbit-cron-audit) |
| `orbit-<thing>-test` | Behavioural test (orbit-uninstall-test) |
| `orbit-<thing>-fuzzer` | Active probe / fuzz (orbit-rest-fuzzer) |
| `orbit-<thing>-compat` | Compatibility audit (orbit-cache-compat, orbit-multisite) |
| `orbit-<thing>-validate` | Schema / format validator (orbit-block-json-validate) |
| `orbit-<thing>-audit` | Read-only review (orbit-pm-ux-audit) |

Stick to the pattern — it makes discovery via `/orbit` predictable.

---

## What every Orbit skill must have

1. **Frontmatter** with:
   - `name` — exactly matching the directory name
   - `description` — invocation triggers + one sentence purpose
2. **Quick start** — one command that does the thing
3. **What it checks** — the rules / patterns / metrics
4. **Output format** — what users get back
5. **Common findings + fixes** — practical, code-level
6. **Pair-with** — which existing Orbit skill complements it
7. **Hard rules** — what NOT to do (security / safety / ethical)

If your skill omits any of these, it's not done.

---

## Length sweet spot

- **Minimum**: ~80 lines (a stub)
- **Sweet spot**: 150-300 lines
- **Maximum**: ~500 lines (split into multiple skills if longer)

Goal: a senior WP dev reads the skill in 2 minutes and knows exactly when + how to invoke it.

---

## Test the new skill

```bash
# Symlink into Claude Code skills folder
ln -s ~/Claude/orbit/skills/orbit-<name> ~/.claude/skills/orbit-<name>

# Restart Claude Code

# Try invocation
# In Claude Code: /orbit-<name>
# Should appear in autocomplete and execute the prompt.
```

---

## Add to SKILLS.md

After creating the SKILL.md, register it in `SKILLS.md` so it shows up in the master list:

```markdown
| `/orbit-<name>` | <one-line purpose> | <when to use> |
```

---

## Add to install.sh

`install.sh` already auto-symlinks every `skills/orbit-*` folder. No code change needed — just commit the new folder and the next `bash install.sh --update` picks it up.

---

## Update the master /orbit dispatcher

Edit `skills/orbit/SKILL.md` to include the new skill in the right category section. This is the menu users see when they type `/orbit`.

---

## PR checklist

When submitting a new skill upstream:

- [ ] `skills/orbit-<name>/SKILL.md` exists with all 7 required sections
- [ ] Listed in `SKILLS.md`
- [ ] Mentioned in the right category of `skills/orbit/SKILL.md` master menu
- [ ] Sample command works end-to-end on a clean wp-env site
- [ ] No false positives in test runs
- [ ] No external API keys required (or if needed, opt-in clearly)
- [ ] Severity rules align with Orbit's: Critical/High/Medium/Low
- [ ] PR description includes: motivation (what gap), reference (link to incident / standard), example output

---

## Roadmap of suggested skills (60+ candidates)

See `SKILL-ROADMAP.md` for the full list — pick any unclaimed item to contribute. Examples:

- `/orbit-elementor-compat` — vs specific Elementor versions
- `/orbit-wpml-compat`, `/orbit-polylang-compat` — translation plugin compat
- `/orbit-edd-license`, `/orbit-freemius-compat` — monetisation SDKs
- `/orbit-stripe-test`, `/orbit-paypal-test` — payment integration
- `/orbit-schema-test` — Schema.org structured data
- `/orbit-page-speed-insights` — Google PSI integration
- `/orbit-ssr-test` — server-side rendering for blocks
- `/orbit-mutation-test` — Infection PHP for test quality
- `/orbit-license-server` — license server stub for testing
- ... (full list in roadmap)

---

## Hard rules

- ❌ Never duplicate an existing skill — extend it.
- ❌ Never bind a skill to a paid service unless it's optional + clearly flagged.
- ❌ Never write a skill that requires a live production site.
- ✅ Every skill is local-first — runs against wp-env, no cloud deps.
- ✅ Every skill produces a report file in `reports/` — never terminal-only.
- ✅ Every skill has a clear severity model — no "soft fail" without rationale.
