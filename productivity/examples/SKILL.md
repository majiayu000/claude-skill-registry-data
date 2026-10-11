---
name: examples
description: This skill should be used when the user wants a worked end-to-end Taiga example or walkthrough — "show me a full Taiga workflow", "example of setting up a project in Taiga", "how do I run sprint planning via the API", "end-to-end bug triage example", or wants to see several Taiga API calls chained together for a real scenario.
---

# Taiga Worked Examples

End-to-end scenarios that chain real Taiga REST calls. Each scenario lives in `references/scenarios/`. They assume the `setup` skill has run (so `TAIGA_API_URL` and `TAIGA_AUTH_TOKEN` are set) and reuse the conventions from `common-operations` (resolve → read → write, include `version` on edits).

## Scenarios

| Scenario | File | What it demonstrates |
|----------|------|----------------------|
| Bootstrap a project | `references/scenarios/bootstrap-project.md` | Login → create project from a template → invite members → set up statuses |
| Sprint planning | `references/scenarios/sprint-planning.md` | Create a sprint → add stories → break into tasks → track stats |
| Bug triage | `references/scenarios/bug-triage.md` | Discover classifiers → file an issue → assign/comment/attach → resolve |
| Reporting & export | `references/scenarios/reporting.md` | Search → filtered lists → project & sprint stats → full export |

## How to use

Pick the scenario closest to the user's goal, open its file, and adapt the IDs (project, status, user) to the live instance. When an exact endpoint or field is unclear, open the matching `api-reference` `references/*.md` file. When a call fails, switch to `troubleshoot`.

<example>
User: "Walk me through standing up a new project in Taiga and adding my team."
→ Open `references/scenarios/bootstrap-project.md` and run it, substituting the team emails and template.
</example>

<example>
User: "I need to plan next sprint in Taiga from these 5 stories."
→ Open `references/scenarios/sprint-planning.md`; create the milestone, then bulk-assign the stories to it.
</example>