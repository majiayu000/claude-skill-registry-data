---
name: quorum
description: 14-member multi-AI deliberation system. Use when users want multiple AI perspectives, say "summon the council", "get a quorum", or need collective intelligence on complex decisions.
---

# Quorum

> 14-member multi-AI deliberation with structured ethical analysis

## Overview

Quorum gathers opinions from 14 AI participants across a **3-stage deliberation process**:

1. **Technical Council** (7 members) - Diverse cognitive perspectives on the problem
2. **Ethical Sub-Chairs** (6 members) - Analysis through ethical frameworks
3. **Chairman** (1) - Final synthesis with transparency section

## Architecture

```
THE CHAIRMAN (Opus 4.5) - Final Arbiter
    │
    ├── Stage 1: TECHNICAL COUNCIL (7 experts)
    │   ├── The Architect (GPT-5.2) - Strategic systems thinking
    │   ├── The Scholar (Codex-Max) - Deep technical analysis
    │   ├── The Sprinter (Codex-Mini) - Pragmatic speed
    │   ├── The Diplomat (Sonnet 4) - Balanced human factors
    │   ├── The Monk (Haiku 4.5) - First principles
    │   ├── The Oracle (Gemini Pro) - Research synthesis
    │   └── The Scout (Gemini Flash) - Pattern recognition
    │
    ├── Stage 2: ETHICAL SUB-CHAIRS (6 frameworks)
    │   ├── The Utilitarian - Consequentialism (outcomes)
    │   ├── The Kantian - Deontology (duties)
    │   ├── The Aristotelian - Virtue Ethics (character)
    │   ├── The Pragmatist - Pragmatism (what works)
    │   ├── The Guardian - Care Ethics (harm prevention)
    │   └── The Machiavelli - Realpolitik (power dynamics)
    │
    └── Stage 3: CHAIRMAN SYNTHESIS
        └── Verdict + Dissenting Views + "What Might Be Missed"
```

## Trigger Conditions

This skill activates when:
- "Summon the council"
- "Get a quorum on this"
- "What do other AIs think?"
- "Multiple perspectives please"
- "quorum"

## Usage

### Direct Execution

```bash
~/.claude/skills/quorum/scripts/quorum.sh "Your question here"
```

### CLI Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show usage information |
| `-v, --verbose` | Show detailed error output |
| `-n, --dry-run` | Preview without running |
| `-b, --no-blind` | Show real model names to chairman |
| `-o, --output-dir DIR` | Save reports to directory |

## Output Files

Generates three markdown files:
- `quorum-minutes_TIMESTAMP.md` - Full deliberation
- `quorum-ethics_TIMESTAMP.md` - Ethical synthesis
- `quorum-chairman-report_TIMESTAMP.md` - Final verdict

## Chairman's Report Structure

1. **Battle Lines** - Points of disagreement
2. **Ethical Spectrum** - Framework analysis
3. **Pressure Test** - Challenging arguments
4. **Uncomfortable Truths** - What's avoided
5. **The Verdict** - Recommendation
6. **Dissenting Views** - Minority positions
7. **What Might Be Missed** - Transparency
8. **Confidence** - HIGH/MEDIUM/LOW
9. **Open Items** - Remaining questions

## Configuration

Edit `quorum.config.yaml` to customize members, commands, and settings.

## Requirements

CLI tools must be installed:
- `codex` - OpenAI Codex CLI
- `gemini` - Google Gemini CLI
- `claude` - Anthropic Claude CLI

## Cost

~14 API calls per session. With subscription plans, no additional costs.
