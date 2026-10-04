---
name: help
description: >-
  Show all available Studio Engine commands with descriptions. Displays
  command list organized by category, current edition features, and quick
  start guide. Use when the creator asks "help", "commands", "what can I do",
  or "how does this work".
allowed-tools:
  - Read
  - Glob
---

# Help

Display all available commands and quick start guide.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Read `creator.yaml` — load name, profile.type, technical_level, workflow_style, language
2. Read `STATE.yaml` — version, products count
3. **Load UX stack (in order):**
   - `references/ux-experience-system.md` §1 Context Assembly, §2.1 Experience Level Scaling, §2.2 Archetype-Aware
   - `references/ux-vocabulary.md` — translate type names and pipeline terms
   - `references/quality/engine-voice-core.md` — vocabulary, three tones, ✦ signature, six anti-patterns, error voices
   - `references/quality/engine-voice.md` — brand DNA, box frame (load only when rendering the PRO edition box frame, a peak moment)
5. **Adapt output** based on creator context:
   - Non-dev → use human type names from ux-vocabulary.md, non-dev pipeline terms
   - Beginner → show full pipeline with descriptions
   - Expert → compact reference, skip obvious descriptions
   - No creator.yaml → warm welcome, suggest /onboard

## Core Instructions

Detect edition first, then display:

```
MyClaude Studio Engine v{version from STATE.yaml} — Command Reference

**IMPORTANT:** Read `creator.yaml → profile.type`. If NOT developer, use the non-dev descriptions below. If developer, use dev descriptions.

**Developer descriptions:**

| Code | Command | Description | Next |
|------|---------|-------------|------|
| ON | /onboard | Set up creator profile | → /scout or /create |
| SC | /scout [domain] | Research domain + recommend setup | → /create |
| MA | /map [topic] | Extract domain knowledge | → /create |
| CR | /create [type] | Scaffold product with DNA | → /fill |
| FI | /fill [slug] | Guided content filling | → /validate |
| VA | /validate [opts] | 7-stage quality check | → /package |
| TE | /test [slug] | Sandbox test (worktree) | → /validate |
| PA | /package [slug] | Bundle triple manifest | → /publish |
| PU | /publish [slug] | Ship to marketplace | done |
| IM | /import [slug] | Bring existing skills in | → /validate |
| TH | /think [topic] | Brainstorm, evaluate, decide | — |
| EX | /explore [query] | Marketplace intel + gaps | — |
| AE | /aegis | Security audit + hardening | — |
| ST | /status | Dashboard + next actions | — |
| HE | /help | This reference | — |

**Non-developer descriptions (all other profile.type values):**

| Command | What it does | Next step |
|---------|-------------|-----------|
| /onboard | Set up your profile | → /scout or /create |
| /scout [domain] | Research your domain before building | → /create |
| /map [topic] | Capture your expertise | → /create |
| /create [type] | Start a new product | → /fill |
| /fill [slug] | Add your knowledge to the product | → /validate |
| /validate | Check quality before sharing | → /publish |
| /test [slug] | Try it out in a safe sandbox | → /validate |
| /package [slug] | Prepare for sharing | → /publish |
| /publish [slug] | Share on the marketplace | done |
| /import [slug] | Bring in existing work | → /validate |
| /think [topic] | Brainstorm or compare options | — |
| /explore [query] | See what others have built | — |
| /aegis | Check code for security issues | — |
| /status | See your dashboard | — |
| /help | This reference | — |

QUICK START (for developers):
  /onboard → /scout {domain} → /create → /fill → /validate → /package → /publish

QUICK START (for non-developers — use when profile.type != developer):
  /onboard → /scout {domain} → /create → /fill → /validate → /publish
  (research → draft → refine → verify → launch)

Type any code or command to execute. Example: "CR skill" = "/create skill"

{if PRO}
PRO AGENTS (active):
  Forge Master         → orchestrates multi-agent creation flows
  Domain Cartographer  → deep domain analysis (/map)
  Product Architect    → architecture decisions (/create)
  Quality Sentinel     → MCS-2/3 deep review (/validate)
  Market Scout         → marketplace intelligence (/publish)
{/if}
```

### Persona-Aware Recommendations

After the command table, read `creator.yaml` → `profile.type`. Add a personalized recommendation:

**If marketer/agency:**
```
Recommended for you: /create minds → build an expert advisor for your domain
                     /create system → build a complete marketing toolkit
See example: references/exemplars/brand-voice-studio/
```

**If developer/prompt-engineer:**
```
Recommended: /create skill → build a reusable tool
             /create squad → build a team of specialized agents
See examples: references/exemplars/code-health-check/
```

**If domain-expert/operator:**
```
Recommended: /create minds → package your expertise as an advisor
             /create workflow → automate a step-by-step process
```

**If hybrid or unknown:**
```
Recommended: /scout {your domain} → discover what to build first
```

**If no creator.yaml exists:** Show default quick start without recommendations. Append: "Run /onboard to personalize recommendations."

### Platform Principles (show on request)

If creator asks "platform principles", "how does Claude Code work", "optimization tips", or "why does my product cost tokens", display:

```
10 Platform Principles — How Anthropic's Claude Code Processes Your Product:

 1. Put critical rules LAST — Claude pays more attention to the end of files
 2. Scope your rules with paths: frontmatter — zero cost when user edits unrelated files
 3. Write directives, not suggestions — your rules ARE law (override semantics)
 4. claude-md = expensive (always loaded) — every char costs tokens every turn
 5. @include depth limit is 5 — deeper files silently ignored
 6. hooks in projectSettings can't set permissions — use localSettings
 7. Products compile once per session — changes need /clear or new session
 8. Model sees WHERE your product came from — project vs personal authority
 9. Only text files work in @include — binary files silently ignored
10. Structure by cognitive function — Identity→Knowledge→Execution→Constraints→Output

Full details: references/platform-principles-summary.md
Source evidence: references/cc-platform-contract.md §1-§9
```

### Type Reference (show on request)

If creator asks "what types are there?" or "show me all types", display:

```
13 Product Types:

For individuals: skill, agent, minds, claude-md, output-style
For teams:       squad, system, workflow
For builders:    application, design-system, hooks, statusline
For curators:    bundle

Run /create to pick the right one for your goal.
```

---

## Anti-Patterns

1. **Wall of text** — Keep it scannable. One line per command.
2. **Stale info** — Always read STATE.yaml dynamically, don't hardcode.
3. **Missing commands** — If new skills exist in .claude/skills/ that aren't listed, mention them.
