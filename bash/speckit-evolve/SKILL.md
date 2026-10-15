---
name: "speckit-evolve"
description: "Cluster the recorded instincts and promote the ones that have earned it into something durable — a skill, a hook, a constitution amendment or a CLAUDE.md line — then retire the instincts the promotion absorbed. Use when instincts pile up in one domain, or when a habit keeps proving itself and should be enforced instead of suggested."
argument-hint: "Optional: a domain to evolve (testing, harness, git, spec-flow)."
compatibility: "Node 18+. Proposes; writes only what the user approves."
metadata:
  author: "speckit-demo"
  source: "adapted from ECC's /evolve — instincts cluster into skills (github.com/affaan-m/ECC)"
user-invocable: true
disable-model-invocation: false
model: sonnet
---

## User Input

```text
$ARGUMENTS
```

## The promotion ladder

An instinct is the weakest form of knowledge this repo keeps: a suggestion that
fades. Evolving one means deciding what it should have been all along.

| Destination | When it fits |
|---|---|
| **A gate** (`.claude/hooks/`, registered in `registry.json`) | The behaviour is mechanical and its absence is detectable. Strongest promotion — an enforced rule cannot be forgotten |
| **A constitution principle** (`/speckit-constitution`) | It is a project-wide value with consequences, not a technique |
| **A CLAUDE.md working agreement** | It is a convention a reader needs, but no gate can check it |
| **A skill** (`.claude/skills/`) | It is a repeatable multi-step workflow, not a single behaviour |
| **Nothing — stays an instinct** | It is still situational, or has fired once |

## Phase 1 — Read what is there

```bash
node .claude/scripts/instincts.mjs list --all
node .claude/scripts/instincts.mjs decay --days 30
```

`decay` is run first on purpose: an instinct nothing has reinforced in a month
loses confidence, and one under 0.3 retires itself. Do not promote what is
fading — report it as a candidate for deletion instead.

## Phase 2 — Cluster

Group the active instincts by `domain`, then look for:

- **3+ instincts in one domain** that share a subject → likely one skill or one
  hook covering all of them.
- **A single instinct with confidence ≥ 0.8 and 3+ reinforcements** → it has
  outgrown being a suggestion; promote it on its own.
- **Two instincts that contradict each other** → do not promote either. Report
  the contradiction and ask which one is true; the loser gets retired.

Report each cluster with: the instincts in it, the destination you propose from
the ladder, and one sentence on why that rung and not the one above it.

## Phase 3 — Promote what the user approves

For each approved cluster:

1. Write the destination artifact — the hook (plus its `registry.json` entry and
   `.claude/settings.json` wiring, then `node .claude/scripts/doctor.mjs --bless-hooks`),
   the skill, or the CLAUDE.md / constitution edit.
2. A new gate needs a colocated `*.spec.ts` beside it before it is wired, like
   every other gate here.
3. Retire the instincts it absorbed, so the same knowledge is not in two places
   with two confidences:

   ```bash
   node .claude/scripts/instincts.mjs retire <id>
   ```

4. Run `npm test && npm run lint && node .claude/scripts/doctor.mjs`, then report what
   moved where.

## Rules

- Promote to the **highest rung that fits**, never higher. A gate that cannot
  mechanically detect the failure is a gate that fires wrongly, and a wrong gate
  gets disabled — which loses the knowledge entirely.
- Never promote an instinct the user has not seen and approved.
- Never delete an instinct file here; `retire` marks it and `/speckit-config-gc`
  is where deletion happens, with a trash directory and a log.
