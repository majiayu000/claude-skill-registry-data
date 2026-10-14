---
name: browser-fallback-skill
description: >-
  Route browser work across agent toolsets — probe a managed desktop-browser
  toolset read-only before any mutating call, fall back to independent
  automation stacks on disconnect, verify-then-handoff for show-the-user
  intents. Harness values in references/. Triggers: browser.disconnected,
  no desktop browser connected, browser toolset, probe before tabs.open,
  desktop browser attach, browser fallback.
license: Apache-2.0
compatibility: opencode
metadata:
  harness: "opencode"
category: OpenCode Meta
---

# Skill: browser-fallback-skill

## What I do

- Gate on toolset presence: a managed desktop-browser toolset appearing in the session catalog does NOT mean its backing client is attached.
- Probe the managed toolset read-only before any mutating call — never let an open/preview call be the first touch.
- On a disconnect verdict: never retry (retries cannot attach the client); fall back to independent browser automation stacks.
- Show-the-user intents: verify the page via the fallback stack (load check + screenshot), report what was seen, hand off the URL plus how to attach the client.
- Automation intents (screenshots, DOM/console inspection, viewport checks): route straight to an independent stack; skip the managed toolset entirely.
- Re-probe at use time — catalogs and client attachments change mid-session; never latch.

## When to use me

- Before the first call to a managed desktop-browser toolset in any task.
- After any "no desktop browser connected" / client-not-attached failure.
- When deciding which browser stack serves a given intent.

Not for: e2e test-suite authoring (use the project's test conventions); MCP server installation; tool permission configuration.

## Method (decision rules)

1. **Gate**: no browser-automation toolset in the session catalog → inert, stop. Catalog presence is necessary, never sufficient.
2. **Classify intent**: show-the-user (the user must see it) vs automation (the agent verifies or inspects).
3. **Automation intent** → independent stack directly. Done.
4. **Show-the-user intent** → read-only probe of the managed toolset FIRST — cheap, side-effect free, never a mutating call.
5. **Probe reports disconnect** → no retry. Load the harness side file (table below) for that harness's probe and fallback pairs; verify the target via the fallback stack; report findings; give the user the URL and the attach step.
6. **Long task** → re-probe at each new use; attachment is session-lifetime-mutable.

## Harness values (load rule)

| Read | When | Use |
|------|------|-----|
| `references/opencode.md` | session runs in OpenCode, or the managed toolset is `browser.*` | probe method, mutating first-touches to avoid, disconnect signature, fallback stack pairs, doc citations |

Another harness with a managed browser toolset and no side file: discover locally — identify one read-only catalog call, the mutating calls, and the installed independent stacks — then contribute `references/<harness>.md` copying this file's skeleton.

## Hard rules

- One probe per intent resolution; a disconnect verdict stands for the task unless the user says they attached the client.
- If unsure whether a call is read-only, treat it as mutating and find a cheaper probe.
- Never build detection on undocumented env or interface signals — they vanish without notice; the probe is the contract.
