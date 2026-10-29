---
name: conventions-maintainer
description: Maintain machine-wide agent conventions in ~/.agents/AGENTS.md and ~/.agents/docs. Use for adding, pruning, restructuring, or validating guidance, including generated docs; keep AGENTS a small router and topic docs focused on local policy.
---

# Conventions Maintainer

Read `writing-for-agents` for context pointers, information hierarchy, and
completion criteria. Maintain the human-edited chezmoi source under
`home/dot_agents/`; `~/.agents/` is the rendered target.

## Workflow

1. **Locate the owner.** Read `home/dot_agents/AGENTS.md`, the relevant topic
   docs, and any source that generates a rendered doc. Keep repo-specific
   instructions in the owning repository. For `~/.agents/docs/slack.md`, edit
   `home/.chezmoitemplates/agent-slack-base.md` or its private overlay. Finish
   when every instruction being changed has an identified source and audience.

2. **Place each meaning once.** Use this hierarchy:

   - Put preferences and guardrails needed before acting on nearly every task in
     `home/dot_agents/AGENTS.md`, the always-loaded kernel and router.
   - Put policy for an identifiable task branch in an existing focused file
     under `home/dot_agents/docs/`. Give a new branch its own doc only when it
     earns a new pointer; keep filenames stable and obvious.
   - Put an independently triggered executable workflow in a model-invoked
     skill. Keep machine-specific policy in the convention doc and the
     workflow in the skill.
   - Leave cheaply discoverable facts in repo configuration, the environment,
     tool `--help`, or upstream docs. Cache a fact only when lookup is expensive
     and its refresh owner is clear.

   Finish when each changed meaning has one authoritative home and every
   must-follow rule remains reachable before the task that needs it.

3. **Write the route and destination.**

   - **Pointer.** Front-load the task condition, name each distinct branch once,
     and use the exact rendered `~/.agents/docs/<topic>.md` path. For example:
     ``- Git or GitHub work: `~/.agents/docs/git.md` ``. Group related pointers
     in `AGENTS.md`; keep identity and explanation in the target doc.
   - **Topic doc.** State its trigger and record the local delta: preferences,
     authorization boundaries, private topology, generated-file ownership, and
     gotchas the environment does not reveal. Let content choose the sections;
     use `Defaults`, `Workflow`, `Safety`, or `Completion` only when each carries
     real material. Co-locate each rule with its reason, caveats, and exact
     formats. End ordered work on a checkable, exhaustive completion criterion.
     Include commands when their exact local shape is part of the contract;
     otherwise point to version-matched `--help`, upstream docs, or the owning
     skill.

   Finish when every disclosed branch has a clear route and each topic doc can
   be followed without reconstructing scattered rules.

4. **Prune and verify.**

   - **Prune.** Remove no-op instructions, stale field manuals, generic
     motivation, discoverable command lists, and duplicated skill content.
     State the desired behavior positively; retain explicit prohibitions for
     hard guardrails. Split only when a real branch or sequence boundary earns
     another pointer.
   - **Verify.** Reread every changed instruction file end to end, inspect
     pointer targets or their generation paths, and search touched topics for
     duplicated or contradictory guidance. Confirm each ordered step ends on a
     checkable, exhaustive criterion. After changing `AGENTS.md` or a convention
     doc, run `just test-python -p test_convention_pointers.py`. For generated
     paths, run the relevant chezmoi preview; for a packaged skill, use the
     package check from `agent-skill-management`.

   Finish when the relevant checks pass and every changed convention has one
   home, a reliable route, and no unresolved contradiction.

Report the changed sources and routing decisions, checks run, and any unresolved
pointer, generation, or ownership question.
