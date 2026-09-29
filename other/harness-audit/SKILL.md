---
name: harness-audit
description: >-
  Audit an agent's harness against the four rings: containment, guides,
  sensors, permissions. Use when the user asks whether their agent setup is
  safe, wants a review of sandboxing / permissions / hooks / AGENTS.md
  guardrails, or asks what a bad session could break. Read-only: reports the
  blast radius and a hardening list, changes nothing. Do NOT use for context
  layout (context-audit) or cost routing (gate-check).
---

# Audit the four rings

Theory: [The four rings](https://undefined-ui.github.io/second-brain-os/#course-4-harness/the-four-rings)
and [Harness practice](https://undefined-ui.github.io/second-brain-os/#course-4-harness/harness-practice).
Build from the outside in: containment, guides, sensors, permissions. The
order matters because each ring must hold when every ring inside it fails —
a guide can be ignored, a sensor can miss, an approval can be misclicked;
a wall does not care.

## Core rule

Report and rank; never harden anything yourself. The audit's one organising
question is the blast radius: describe the worst session possible under the
current setup and what it costs. If the user asks you to apply fixes
afterwards, that is a normal edit session, not this skill.

## Workflow

1. **Ring one — containment: what can it physically reach?** Where does the
   agent run: the user's checkout or a worktree/container? Which credentials
   are in its environment — a read-only database user or the application's?
   Open internet or an allowlist? Real API keys or test keys? The finding is
   one sentence: "the worst session deletes X and spends Y."
2. **Ring two — guides: what does it read before acting?** Find CLAUDE.md /
   AGENTS.md and tool descriptions. Every line should be a rule the agent
   can act on — flag philosophy, history, and anything over roughly a page.
   Flag missing rules for the repo's real landmines (migrations, generated
   files, deploy scripts).
3. **Ring three — sensors: what fires when it errs?** Is there one command
   (`make check` or equivalent) that runs tests, linter and types? Does the
   harness run it automatically after edits — a hook — or does correctness
   depend on the model remembering? A sensor the model must invoke
   voluntarily is a guide, not a sensor.
4. **Ring four — permissions: what still needs a human?** List what is
   auto-approved. The irreversible set — push to main, deploy, spend,
   delete data, send messages — should need a person; everything reversible
   inside the walls should not. Flag both failure modes: irreversible
   actions auto-approved, and reversible ones prompting so often the user
   rubber-stamps (approval fatigue is a hole in this ring, not a virtue).
5. **Check the order.** The classic smell is an inner ring doing an outer
   ring's job: a prompt line saying "never touch prod" where a credential
   should have been removed. Rules in guides that could be walls belong in
   ring one.

## Output format

```
Harness audit — <project>
blast radius: <the worst session in one sentence>

ring 1 containment  <held | open>  <finding>
ring 2 guides       <held | open>  <finding>
ring 3 sensors      <held | open>  <finding>
ring 4 permissions  <held | open>  <finding>

Hardening list, outermost first:
1. ...
```

Rank fixes outside-in — a wall before a better prompt, a sensor before a
politer rule. Close by restating the blast radius as it would be after
fix 1 alone.
