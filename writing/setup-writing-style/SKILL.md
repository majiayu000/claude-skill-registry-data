---
name: setup-writing-style
description: "Build or recalibrate a private, evidence-based writing-style profile from text the user explicitly places in scope. Use when the user asks to analyze/capture their voice across future writing, compare samples, or create a reusable style profile; extract observable traits without copying distinctive passages or silently persisting personal data. Do not activate merely to draft one email or WhatsApp message—use message-writer, which may apply an already approved profile. Never scan unrelated conversations, mail, cloud files, or repositories automatically. Turkish triggers: yazım tarzı oluştur, kişisel üslup rehberi, örneklerden ses tonu çıkar."
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

## Optional local measurements

Run `scripts/stylometry.py` only on user-authorized local text files when simple, quantitative checks help compare samples. It reports mechanical signals such as length, punctuation, lexical repetition, register indicators, and a cautious pairwise comparison. Treat it as supporting evidence, not authorship proof or a psychological profile. For Turkish or mixed-language samples, mark language-sensitive measures as lower confidence.

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

Draft two or three short test pieces for different intended audiences. Compare against a neutral baseline using authenticity, clarity, factual preservation, appropriateness, and privacy. Use a blind comparison when practical. The user is the final judge; revise only from explicit corrections, not the assistant's self-score.

## Save and apply

If persistence is requested, use the active host's documented user-owned skill/profile mechanism or deliver a standalone file. Do not assume a slash command, upload button, provider path, or automatic activation. Never overwrite an existing profile without a diff, backup, and approval.

When applying the profile, preserve facts and task constraints; style must not invent experiences, commitments, endorsements, or emotions. State when the evidence is too sparse to imitate reliably.
