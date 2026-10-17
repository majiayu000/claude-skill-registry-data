---
name: writing-heuristics
description: Deterministic technical writing heuristics, anti-slop rules, and Google Developer Style enforcement engine
version: 1.0.0
---

# Writing Heuristics and Style Discipline

Apply these deterministic rules to all technical documentation, architecture specs, pull request descriptions, and agent communications.

## Canonical Rules Summary

### Ban Throat Clearing (`ban-throat-clearing`)
- **Severity**: `error` | **Confidence**: 1 | **Handling**: Autofixable
- **Rule**: Disallow conversational throat-clearing, pre-announcements, and sycophantic greetings at the beginning of prose paragraphs.
- **Rationale**: Technical documentation should communicate essential information directly without introductory conversational fluff.
- **Pass**: "To configure the client, supply your API key in the environment."
- **Fail**: "Certainly! In this section, we will delve into configuring the client."

### Ban Filler Adverbs and Slop Words (`ban-filler-adverbs`)
- **Severity**: `warning` | **Confidence**: 0.85 | **Handling**: Manual rewrite
- **Rule**: Flag empty buzzwords, filler adverbs, and hyperbolic adjectives that dilute technical precision.
- **Rationale**: Vague superlatives weaken the authority and density of engineering prose.
- **Pass**: "This update reduces memory overhead by 40%."
- **Fail**: "This game-changing update seamlessly and essentially eliminates overhead."

### Avoid First-Person Plural (`avoid-first-person-plural`)
- **Severity**: `warning` | **Confidence**: 0.9 | **Handling**: Manual rewrite
- **Rule**: Flag first-person plural pronouns ('we', 'us', 'our', 'let\'s') in technical instructions.
- **Rationale**: Technical docs should focus on the reader and the system, avoiding ambiguous institutional 'we'.
- **Pass**: "Install dependencies before starting the service."
- **Fail**: "We recommend that you install dependencies first."

### Use Second Person or Imperative Mood (`use-second-person`)
- **Severity**: `warning` (Advisory) | **Confidence**: 0.8 | **Handling**: Manual rewrite
- **Rule**: Encourage direct second-person address ('you') or direct imperative mood; flag third-person passive abstraction ('the developer must...').
- **Rationale**: Direct instructions are clearer and more actionable than abstract descriptions of what an anonymous persona should do.
- **Pass**: "You can configure the timeout in config.json."
- **Fail**: "The developer should configure the timeout in config.json."

### Use Active Voice (`active-voice`)
- **Severity**: `warning` | **Confidence**: 0.8 | **Handling**: Manual rewrite
- **Rule**: Flag passive voice constructs (auxiliary verb + past participle + optional 'by' agent) in technical instructions.
- **Rationale**: Active voice makes the actor clear and sentences more concise.
- **Pass**: "The scheduler triggers the backup job nightly."
- **Fail**: "The backup job is triggered nightly by the scheduler."

### High Assertion Density and Metric Grounding (`assertion-density`)
- **Severity**: `warning` | **Confidence**: 0.8 | **Handling**: Manual rewrite
- **Rule**: Flag qualitative performance assertions lacking concrete quantitative metrics or specific technical mechanisms.
- **Rationale**: Unbacked assertions like 'vastly superior' or 'incredible speed' lack engineering utility without concrete measurements.
- **Pass**: "This refactoring reduces query latency from 120ms to 18ms by caching query plans."
- **Fail**: "This refactoring provides vastly superior performance and incredible speed."

### State Condition Before Action (`condition-before-action`)
- **Severity**: `warning` | **Confidence**: 0.75 | **Handling**: Manual rewrite
- **Rule**: State prerequisites or conditions before the imperative command rather than trailing after.
- **Rationale**: Putting the condition first prevents the reader from executing an action before discovering it applies only conditionally.
- **Pass**: "To reload configuration, send SIGHUP to the process."
- **Fail**: "Send SIGHUP to the process if you want to reload configuration."

### Heading Sentence Case (`heading-sentence-case`)
- **Severity**: `error` | **Confidence**: 0.95 | **Handling**: Autofixable
- **Rule**: Enforce Sentence case for all markdown headings (h1-h6) while preserving acronyms and code identifiers.
- **Rationale**: Google Developer Style mandates sentence case for all headings and section titles.
- **Pass**: "## Deployment configuration and setup"
- **Fail**: "## Deployment Configuration And Setup"

### Descriptive Link Text (`descriptive-links`)
- **Severity**: `error` | **Confidence**: 1 | **Handling**: Manual rewrite
- **Rule**: Flag generic or non-descriptive link anchor text ('here', 'click here', 'link', 'this page').
- **Rationale**: Links must describe their target destination so readers understand where the link leads without surrounding context.
- **Pass**: "See the [PostgreSQL Connection Pooling Guide](docs/db.md)."
- **Fail**: "For connection pooling, click [here](docs/db.md)."

### Serial Oxford Comma (`serial-comma`)
- **Severity**: `warning` (Advisory) | **Confidence**: 0.85 | **Handling**: Manual rewrite
- **Rule**: Encourage using the serial Oxford comma before the coordinating conjunction in lists of three or more items.
- **Rationale**: Oxford commas prevent ambiguity in enumerations.
- **Pass**: "Supports JSON, YAML, and TOML formats."
- **Fail**: "Supports JSON, YAML and TOML formats."

### Ordered vs Unordered Sequences (`ordered-sequences`)
- **Severity**: `warning` (Advisory) | **Confidence**: 0.75 | **Handling**: Manual rewrite
- **Rule**: Advises using bulleted lists instead of numbered lists when list items are static descriptive points rather than chronological steps.
- **Rationale**: Numbered lists imply mandatory sequential order; unordered bullet lists represent parallel properties or options.
- **Pass**: "1. Clone the repository.\n2. Install dependencies.\n3. Run the test suite."
- **Fail**: "1. High performance.\n2. Modular design.\n3. Comprehensive documentation."

## Suppression Syntax

To suppress a rule locally with an audit trail:
```markdown
<!-- heuristics-disable rule-id author="username" reason="Rationale for exemption" until="YYYY-MM-DD" -->
Exempted text here
<!-- heuristics-enable rule-id -->
```

## CLI Enforcement
To check documentation in this repository:
```bash
node skills/writing-heuristics/bin/lint-heuristics.js check docs/
```
