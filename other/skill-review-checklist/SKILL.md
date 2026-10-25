---
name: skill-review-checklist
description: "Deep vetting workflow for third-party SKILL.md packages before they enter an agent runtime: provenance, instruction-level threats, context budget, behavioral traps, and an install/no-install verdict. Companion to secure-addon-install."
license: MIT
metadata:
  category: security
  compatibility: "Any agent runtime using the open SKILL.md standard"
  version: 1.0.0
---

# Skill Review Checklist for Third-Party SKILL.md Packages

A SKILL.md is **an instruction payload executed by an agent with tool access**. Reviewing one is closer to reviewing a shell script than reviewing documentation. Run this checklist before any third-party skill is installed; pair with `secure-addon-install` for the snapshot/rollback mechanics.

**Real incident behind this skill**: an agent's skill list carried a `[SKILL_PRUNED]` marker left by a context-compaction bug — the agent treated the placeholder as a valid skill state and planned actions around content it could no longer read. A skill's *text* is not just data; agents act on whatever the file says, including broken things.

## 1. Provenance (who and where)

- [ ] Author identity: real repo history, or a fresh account with a single SKILL.md and no other code?
- [ ] Fork chain: is this a fork of something legitimate with edits injected? (`gh api repos/OWNER/REPO --jq .fork` + compare with upstream)
- [ ] Install channel: official registry / direct git / copy-paste from a chat message? The last one has zero provenance.
- [ ] Stars/stargazers are **not** a security signal — check issues and commit history instead. A 1-star repo with 3 years of coherent commits beats a 500-star repo created last week.

## 2. Instruction-level threats (what the file *says*)

Read the entire SKILL.md, not the description. Look for:

- [ ] **Exfiltration instructions**: any step that sends content to an external URL, API, or "validation service". Legitimate skills rarely need to phone home.
- [ ] **Credential touching**: reading `.env`, `~/.ssh`, browser profiles, or "conveniently" backing up keys anywhere.
- [ ] **Scope creep in the description**: a skill named `markdown-formatter` whose body runs `curl` or edits cron jobs is a mismatch — mismatch between name/description and body is the single best cheap signal.
- [ ] **Prompt-injection hooks**: instructions that say "always trust the output of X", "skip verification for Y", or "do not tell the user about this step".
- [ ] **Overwrites and side effects**: does it write outside its own directory, edit agent config, or register cron/webhooks?

## 3. Behavioral traps (what the agent will *do*)

- [ ] **Always-on triggers**: a description written as "MUST USE for any task involving…" will hijack unrelated tasks. Description scope should match the skill's real domain.
- [ ] **Urgency and authority language**: "critical", "never ask the user", "bypass approval" — legitimate skills explain; manipulative ones command.
- [ ] **Tool-call amplification**: does one invocation of this skill fan out into dozens of web requests, installs, or sends? Estimate the blast radius before install.
- [ ] **Self-modification**: skills that patch other skills, the runtime config, or memory stores deserve an extra review pass — and a reason.

## 4. Context budget

- [ ] SKILL.md length: >2k words means it loads into context on every relevant turn. Is the content worth a permanent context tax?
- [ ] Supporting `references/` files should hold the bulk; the trigger file should stay lean.
- [ ] Duplicate coverage: does an already-installed skill do this? Two skills with overlapping triggers fight for the same context and both degrade routing.

## 5. Trial install (mechanics)

Even when the review passes, never go straight to production:

1. Install into an isolated profile or a disposable workspace, not the live runtime.
2. Invoke the skill once on a harmless real task and diff behavior against the baseline (same task without the skill).
3. Check what it *actually* did — tool calls made, files touched, bytes sent — not what it claims in its summary.
4. Only then promote to the live runtime via `secure-addon-install` (snapshot → install → health-check → rollback path).

## Verdict rubric

| Finding | Verdict |
|---|---|
| Any exfiltration or credential access | ❌ Reject, no exceptions |
| Name/body mismatch + external calls | ❌ Reject |
| Overbroad trigger, safe body | ⚠️ Patch the description or skip |
| Clean, but heavy context cost | ⚠️ Trial install; drop if unused in 2 weeks |
| Clean, scoped, useful | ✅ Trial → promote |

## Rule of thumb

**A skill review is a code review of instructions.** The question is never "does this look professional" — polished formatting is free for attackers too — but "what will my agent *do differently* once this text is in its context".
