---
name: skill-router-registry
description: "Route rough user tasks to the best available Codex skill with minimal token use, maintain a lightweight local skill index, and optionally discover new GitHub skills for review. Use when the user asks which skill/tool/workflow should handle a task, wants automatic skill selection after question framing, wants a GitHub skill registry, or wants periodic discovery of new skills without loading every SKILL.md into context."
---

# Skill Router Registry

## Purpose

Use this as a single top-level routing skill:

```text
rough user task -> tiny intent frame -> skill metadata lookup -> selected skill -> execution -> feedback updates route preference
```

Default behavior: route with minimal context. Do not load many full skill files. Do not auto-install untrusted GitHub skills.

## Tiny Router

Use this by default:

```text
Route:
- Task type:
- Best skill:
- Why:
- Confidence:
- Next action:
```

Keep it under 120 English words or 180 Chinese characters when possible.

## Routing Algorithm

1. Classify the task type.
2. Check current session skills first.
3. Search the local skill index if available.
4. Return top 1 skill when confidence is high.
5. Return top 2-3 candidates when confidence is medium.
6. Ask one clarification question when confidence is low.
7. Load the chosen skill only after selection.

## Task Types

Use these coarse types before fine routing:

- coding / debugging / review / refactor
- research / literature / citation / evidence
- writing / editing / translation
- video / image / design / frontend
- data / document / PDF / spreadsheet
- automation / reminder / monitoring
- planning / decision / learning
- domain-specific tools

## Token Budget Rules

- Never load the full registry into context.
- Never load more than one full `SKILL.md` by default.
- Use metadata summaries first: name, description, domains, triggers, trust.
- Use top 5 candidate metadata at most.
- Load references only if the selected skill requires them.
- If no skill fits, fall back to `question-to-prompt-pack` or normal task framing.

## Confidence Routing

| Confidence | Behavior |
|---|---|
| High | choose one skill and proceed |
| Medium | show 2-3 candidates and recommend one |
| Low | ask one clarification question or use question framing |

## Registry Index

A local index should store compact records:

```text
id
name
description
source
path_or_url
domains
task_types
trigger_phrases
tools_required
risk_level
trust_level
summary
last_seen
```

The index is for routing only. It is not proof that a skill is safe to install.

## GitHub Discovery

Discovery is offline from the current answer path:

- daily scan: check known repos for changed commits or new `SKILL.md`
- weekly scan: parse changed skills and update index
- manual scan: user-triggered refresh

Discovery must not automatically install or execute skills. Unknown skills go to review.

For manual metadata discovery, run `scripts/discover_skill_metadata.py` on a user-approved local folder or GitHub repository. It must write compact review records only.

## Trust and Safety

Trust levels:

- `trusted`: official or user-approved source
- `review`: known community source, needs inspection
- `unknown`: do not install or run automatically

Flag risk when a skill:

- runs shell commands
- installs dependencies
- asks for secrets
- changes auth/config files
- downloads remote code
- has vague or malicious-looking instructions

## Feedback Loop

After routing or execution, use lightweight feedback only when calibrating:

```text
Was this the right skill?
A. Yes, keep this route
B. Close, but choose a more specific skill next time
C. Wrong skill
D. No skill needed; answer directly
```

Use feedback to adjust thread-level routing preference. Do not claim permanent memory unless persistent storage exists and the user requests it.

## Scripts

- `scripts/build_local_index.py`: build an index from installed local skills.
- `scripts/search_skill_index.py`: search the compact index for candidate skills.
- `scripts/discover_skill_metadata.py`: scan local or GitHub `SKILL.md` metadata for review; never install or execute.
- `scripts/check_registry_rules.py`: verify this skill keeps routing and safety rules.

## References

- `references/registry-schema.md`: index schema and trust model.
- `references/routing-policy.md`: routing rules, token budget, and fallback behavior.
- `references/github-discovery.md`: discovery sources and update cadence.
