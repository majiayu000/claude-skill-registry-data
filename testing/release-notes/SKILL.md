---
name: release-notes
description: >
  Produces a Slack-ready QA guide (guide de recette) for pilots, from a git diff between two tags.
  Focuses on cross-cutting attention points, risk zones, and side effects — not ticket acceptance criteria.
  Trigger on: "génère la release note", "guide de recette", "note de release vX.XX",
  "prépare la recette pour vX.XX", "qu'est-ce qu'on teste pour cette release".
  Requires git access and optionally the slack-notify skill to post the result.
---

## Purpose

Produce a **Slack-ready QA guide** for pilots (testers). This guide **does not reproduce the acceptance criteria of Jira tickets** — pilots already know how to test each ticket. Its value lies elsewhere:

- Provide the global context of the release (what changed, the scope)
- Flag **cross-cutting attention points**: zones touching multiple tickets, silently changing behaviors, edge cases to watch
- Identify **potential side effects**: regressions in existing features not described in the tickets

Think like a **QA architect** reading the full diff and anticipating what could break — not like a scribe copying tickets.

---

## Step 1 — Fetch commits

```bash
git log --pretty=format:"%h %s" <tag-from>..<tag-to-or-HEAD>
```

If the user does not specify tags, ask: "Depuis quel tag ? (ex: `v2.20.64-hotfix`)"

### Feature branch merges

When a commit looks like `Feature: X (#NNN)` or `feat: X (#NNN)` without an `IDF-XXXX` ref, it is likely a **feature branch merge commit** containing sub-commits. Always drill into it:

```bash
git log --pretty=format:"%h %s" <merge-hash>^1..<merge-hash>
```

In the `✨ FEATURES` section, give each feature branch its own **bold title line** (not a bullet) with audiences, followed by a flat list of its tickets. End with a **Autres tickets** bold title for remaining individual commits:

```
**[Feature name]** · 👤 Jeune / 🏪 Partenaire
- [IDF-XXXX](url) — short title
- [IDF-XXXX](url) — short title

**Autres tickets**
- [IDF-XXXX](url) — short title
```

Do not list the feature branch merge commit itself.

---

## Step 2 — Classify ALL commits (exhaustiveness is mandatory)

**Golden rule: every commit must appear in exactly one of the lists below. No commit can be lost.**

### List A — Features & bugs (commits with `IDF-XXXX`)

Group by ticket: multiple commits on the same `IDF-XX` → one single item.
Distinguish:

- **Feature** (`feat`) → `✨ FEATURES` section
- **Bug** (`fix`) → `🐛 CORRECTIONS` section
- **Refactor / chore with IDF-** → feature or bug depending on ticket context; if uncertain, classify as feature

### List B — AI & tooling (commits related to AI, agent skills, AGENTS.md)

Commits that advance AI integration in the team's workflow: new skills, AGENTS.md, agent documentation, AI-generated characterization tests, Copilot/Claude tooling.

→ `🤖 IA & OUTILLAGE` section

### List C — Continuous improvements (other commits without `IDF-XXXX`)

Commits without a ticket reference that improve the platform: refactors, performance, technical tooling, debt, small UX improvements without an associated ticket.
Some may be visible (e.g. better error handling, perceived perf), others not.

→ `🔧 AMÉLIORATIONS` section

### List D — Ambiguous (commits without `IDF-XXXX` but resembling a visible feature or bug)

**Do not classify these alone.** Before producing the guide, present the ambiguous commits to the user and ask explicitly for each one:

> "Ces commits n'ont pas de ticket IDF- mais semblent avoir un impact visible. Peux-tu me dire s'ils vont dans Nouveautés, Corrections ou Améliorations techniques ?"

Wait for the answer before continuing. Do not guess, do not ignore.

### Commits to exclude (do not count toward exhaustiveness)

- Automatic merge commits (`Merge pull request #NNN`, `Merge branch '...'`)
- Lock file updates (`pnpm-lock.yaml`, `package-lock.json`)
- Purely internal dev typo fixes (e.g. "fix typo in mapper")

---

## Step 3 — Analyze the release globally (for the attention sections)

Before writing, identify:

1. **Domains touched** — which libs, which modules (auth, grants, offers, wallet, Keycloak…)
2. **Cross-cutting changes** — modifications impacting multiple features or multiple audiences at once
3. **Risk zones** — refactors, auth changes, data migrations, silently changing behaviors
4. **Probable side effects** — e.g. a Keycloak flow refactor can affect FranceConnect login even if the ticket doesn't mention it

### Item classification in the guide

**→ `🔧 AMÉLIORATIONS` section** if **no `IDF-XXXX` reference** is present in the message AND the commit has no visible UX impact.

**→ ⚠️ / 🔴 / 🟡 sections** if the commit contains an `IDF-XXXX` reference OR describes a user-visible change.

**Edge cases:**

- Commit without `IDF-XX` but with an obvious UX impact → 🟡 or ⚠️ depending on risk
- Commit with `IDF-XX` but purely technical (e.g. `refactor(IDF-1700): cleanup Keycloak module`) → 🔴 (refactor on sensitive domain)

### Risk levels

| Level         | Criteria                                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 🔴 **High**   | Refactor on auth / Keycloak / identity / payment, large multi-PR feat, anything touching registration, login, or sensitive data |
| 🟡 **Medium** | Standard product feature with potential interactions with existing behavior                                                     |

### Audience rules

| Signal in commit                 | Audience      |
| -------------------------------- | ------------- |
| `young`, `jeune`, `app`          | 👤 Jeune      |
| `partner`, `partenaire`          | 🏪 Partenaire |
| `agent`, `back-office`, `agents` | 🧑‍💼 Agent      |

Multiple audiences are possible on the same item.

---

## Step 4 — Jira links

For every `IDF-XXXX` reference found in a commit:
→ URL: `https://zenstudio.atlassian.net/browse/IDF-XXXX`

---

## Step 5 — Produce the guide in Slack format

The guide must start with the Power Ranger opener defined in the `slack-notify` skill (1 sentence, French, subtle Power Rangers lore reference). See that skill for exact rules.

Use the template at `assets/template.md` as the base structure. Key formatting rules:

- Section titles (✨ FEATURES, 🐛 CORRECTIONS, etc.) must be **bold**: e.g. `✨ **FEATURES**`
- The release title must be **bold**: `🚀 **Release vX.XX.XX — Guide de recette**`
- **CONTEXTE** must be **bold** too

**Key rule for ⚠️ / 🔴 / 🟡 sections:**

- Written for **pilots (testers)**, not developers — avoid implementation details, code names, database terms
- Do not rewrite ticket acceptance criteria
- Focus on: what areas are impacted, what could regress, what to re-test beyond the ticket scope
- Tone: "ce changement a des répercussions sur X, pensez à retester Y" — not "la colonne Z est supprimée de la table W"
- All information for one bullet must be on a single line (no nested sub-items)

### Intro phrase for `🔧 AMÉLIORATIONS`

Pick one of the following (or generate a similar one in the same spirit):

> _Cette release embarque également des améliorations qui renforcent la robustesse et la performance de la plateforme :_

> _En parallèle des nouveautés, cette release consolide les fondations techniques de la plateforme :_

> _Cette release intègre aussi plusieurs chantiers qui améliorent la stabilité et la maintenabilité :_

**Rule:** positive and dynamic. Adapt if improvements concern a specific domain (e.g. "…renforcent la robustesse du module d'authentification"). Do not write "nothing visible" or "invisible to users".

---

## Formatting rules

### When posting via the `slack-notify` skill (MCP)

The MCP `conversations_add_message` accepts `text/markdown` by default and converts automatically. Use **standard Markdown**:

- Links: `[IDF-1670](https://zenstudio.atlassian.net/browse/IDF-1670)`
- Bold: `**text**`
- Italic: `_text_`
- Bullet: `-`
- Section headers: no `#` — use emojis as separators
- Line breaks between sections: one blank line is enough

**⚠️ Slack collapses single newlines.** Every line that must be visually separate needs a **blank line after it** — including title lines, the opener, "Diff depuis :", and section headers. Without a blank line, the next line is appended inline.

Example — correct:

```
🚀 **Release vX.XX.XX — Guide de recette**

Diff depuis : `<tag>`

**CONTEXTE**
...
```

**⛔ What causes an `invalid_blocks` error and is FORBIDDEN via MCP:**

- `---` (horizontal dividers) — generates an unsupported block, the message fails
- Nested lists / indented sub-items (e.g. a `-` followed by an indented `  →`) — Slack Block Kit does not support nesting, the message fails
- If you need to add sub-information to a list item, include it inline on the same line, separated by `—`

**Golden rule: all lists must be flat (single depth level).** When in doubt, avoid any Markdown construct that generates more than one level of nested blocks.

**Default: always produce the guide in standard Markdown** — the MCP `conversations_add_message` accepts `text/markdown` and converts correctly. Do not use Slack mrkdwn (`*bold*`, `<url|text>`, `•`) — use standard Markdown at all times.

---

## Constraints

- Never reproduce the acceptance criteria of a Jira ticket
- Do not include: automatic merge commits, lock file updates, internal dev typo fixes
- If multiple commits relate to the same `IDF-XX`, merge them into a single item
- If no item fits a section, omit the section entirely
- The `🤖 IA & OUTILLAGE` section is optional — include it only if the release contains commits related to AI, agent skills, or AGENTS.md
- The `🔧 AMÉLIORATIONS` section is optional — omit it if there are no technical commits without a Jira ref
- The ⚠️ and 🔴 sections are the most important — if the release is quiet, they can be empty or absent
