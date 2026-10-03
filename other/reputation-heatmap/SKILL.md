---
name: reputation-heatmap
description: "Separate healthy mystique from rumor, overreach, parasocial risk, or brand harm, then output a response playbook. Use when Codex needs to map public narrative risk around a creator, celebrity, or founder without amplifying gossip or turning risk review into panic."
---

# Reputation Heatmap

Use this skill when you need a structured response playbook for rumor, mystique, parasocial pressure, or broader brand risk around a public figure.

Default product shape: a compact macOS `MenuBarExtra` utility with a source-aware popover for signal intake, risk mapping, and playbook export and an optional settings/history window.

## Quick Start

1. Confirm the subject, target audience, and source window.
2. Gather only public or user-authorized material into a working set.
3. Produce a `response-playbook` with the default sections below.
4. If the user wants a richer product concept, keep it menu bar first and native to SwiftUI.

## Accepted Inputs

- press coverage, community chatter, rumor summaries, and brand concern lists
- notes about what is confirmed, unconfirmed, private, or already addressed
- community moderation reports or escalation logs
- existing communication principles, legal constraints, or no-comment boundaries

## Output Artifact

Primary artifact: `response-playbook`

Default sections:
- Heatmap of low, medium, and high-risk signals
- Confirmed versus unconfirmed narrative map
- Response modes: address, clarify, monitor, or do not amplify
- Escalation thresholds and owners
- No-response rules and red lines for privacy or safety

## Workflow

### Gather Sources

- Inventory the current signals and label what is verified, speculative, or private.
- Separate audience concern from opportunistic rumor spread.
- Capture the communication and legal boundaries before suggesting any response.

### Distill Signal

- Map each signal by severity, confidence, and amplification risk.
- Differentiate healthy mystique from unresolved confusion or reputational harm.
- Reject any tactic that would launder a rumor by repeating it unnecessarily.

### Build The Artifact

- Export a playbook with response mode, threshold, owner, and no-response guidance.
- Show where silence protects privacy better than clarification.
- Flag situations that need legal, PR, or human leadership review immediately.

### Mac Product Shape

- Prefer `MenuBarExtra` with these primary actions:
  - `Add Signals`
  - `Map Risk`
  - `Review Thresholds`
  - `Export Playbook`
- Keep the popover between 320 pt and 380 pt wide with grouped sections, clear source status, and a strong export action.
- Use a lightweight settings or history window only for source rules, saved exports, or weighting controls.

### Safety Boundaries

- Work only from public or user-authorized material.
- Do not assist with stalking, covert profiling, rumor laundering, harassment, or minors-focused manipulation.
- Do not help with defamation, retaliation, doxxing, or any strategy that amplifies unverified rumors for engagement.

## Example Prompts

- `Use $reputation-heatmap to turn this press chatter and community concern list into a response playbook with thresholds and no-response rules.`
- `Use $reputation-heatmap to separate healthy mystique from real founder-brand risk and tell me what to address, monitor, or leave alone.`

## Resources

- `references/product-spec.md`: product surface, SwiftUI layout, artifact template, icon direction, and first-run behavior.
