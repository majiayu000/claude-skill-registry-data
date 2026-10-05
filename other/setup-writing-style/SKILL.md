---
name: setup-writing-style
description: Build a private, evidence-based writing-style profile from text the user explicitly provides, then test it on drafts without copying distinctive passages or.
license: MIT
---

# Writing Style Profile

## Consent and privacy

Use only samples the user placed in scope. Explain what will be extracted and where any profile will be saved. Do not read unrelated conversations, mail, cloud drives, or repositories. Redact secrets and sensitive identifiers; prefer local storage outside shared/versioned folders. Persistence requires explicit approval for the exact path and content.

## Analyze

Use several representative samples when possible and separate stable habits from topic/format effects. Record observable traits:

- sentence/paragraph length and rhythm;
- formality, directness, warmth, humor, hedging;
- openings, transitions, calls to action, sign-offs;
- vocabulary, punctuation, formatting, emoji, and bilingual behavior;
- audience-dependent variations;
- patterns to avoid.

Do not infer personality, health, politics, protected traits, or private facts. Do not preserve long verbatim excerpts; store short evidence notes and synthetic examples.

## Profile format

```markdown
# Writing Style Profile
Use for: drafts the user will send or publish
Do not use for: the assistant's own factual answers unless requested

## Core traits
## Structure and rhythm
## Tone by audience
## Vocabulary and formatting
## Do / avoid
## Synthetic examples
## Uncertain or conflicting signals
## Source scope and last review date
```

## Validate

Draft two or three short test pieces for different intended audiences. Compare against a neutral baseline using a rubric for authenticity, clarity, factual preservation, appropriateness, and privacy. The user is the final judge. Revise the profile from explicit corrections, not the assistant's self-score.

## Save and apply

If persistence is requested, use the active host's documented user-owned skill/profile mechanism or deliver a standalone file. Do not assume a slash command, upload button, provider path, or automatic activation. Never overwrite an existing profile without a diff, backup, and approval.

When applying the profile, preserve facts and task constraints; style must not invent experiences, commitments, endorsements, or emotions. State when the evidence is too sparse to imitate reliably.
