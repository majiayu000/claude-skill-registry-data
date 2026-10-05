---
name: context-budget
description: "Audit actual context consumption and routing overhead across instructions, skill metadata and bodies, tool schemas, agent definitions, conversation output, and project files. Use when context feels crowded, many capabilities were added, a long task needs a budget, or the user asks what is consuming context and where safe savings exist. Turkish triggers: bağlam bütçesi, token tüketimi, hangi beceri ne kadar yer kaplıyor, context audit."
---

# Context Budget

Measure before recommending changes. Report estimates as estimates and keep the audit read-only unless the user separately authorizes edits.

## 1. Discover the active host

Identify the current runtime, project root, active configuration, instruction chain, available tools, and skill discovery roots from local evidence. Do not assume that every file present on disk is loaded.

If the runtime exposes its real context limit or tokenizer, use it and cite the source. Otherwise report the limit as unknown and avoid invented utilization percentages or free-token counts.

## 2. Inventory by loading behavior

Classify components instead of summing every file equally:

| Layer | Typical cost | Audit method |
|---|---|---|
| Always-visible metadata | Skill names/descriptions, agent summaries, routing metadata | Count actual discovered entries and metadata text |
| Injected instructions | System, user, project, and host instruction files | Follow the active instruction chain |
| On-demand bodies | Skill bodies and references | Count only activated or explicitly loaded material |
| Tool schemas | Available tool and connector definitions | Use exposed schema size when available; otherwise label the estimate |
| Conversation and outputs | Prompts, responses, command output, attachments | Identify the largest retained blocks |
| External artifacts | Files referenced by path but not loaded | Do not count until read into context |

Detect exact duplicates, same-name divergent variants, redundant instruction coverage, oversized descriptions, broken references, and verbose command output.

## 3. Estimate conservatively

Use this order:

1. runtime-provided token count;
2. provider tokenizer verified for the active model family;
3. character-based estimate for mixed text or code;
4. word-based estimate for prose.

State the method and an uncertainty band. Do not assign a universal fixed cost per tool or assume a fixed context window.

Separate:

- physical files from logical discovered entries;
- exact duplicates from divergent same-name variants;
- potential overhead from confirmed loaded overhead;
- metadata cost from on-demand skill body cost.

## 4. Prioritize by value, not size alone

Score each recommendation on:

- context saved;
- functional value preserved;
- trigger precision gained;
- breakage risk;
- reversibility.

Prefer deduplication, shorter routing descriptions, lazy references, narrower triggers, and output filtering before deleting useful capability.

## 5. Report

Provide:

1. host and counting method;
2. confirmed versus estimated overhead by layer;
3. exact duplicates and divergent collisions;
4. highest-cost items with paths or sources;
5. ranked recommendations with expected benefit and risk;
6. items that need runtime verification;
7. a re-audit command or procedure.

Never claim a precise free-context percentage when the active limit or loaded prompt is unavailable.

## Boundaries

- Do not edit, disable, uninstall, or delete during an audit.
- Do not treat a large skill library as fully injected if the host uses metadata routing and on-demand bodies.
- Do not recommend removal solely because a file is long; check trigger frequency and unique capability.
- Use context-optimization for quality-preserving reductions during an active task.
