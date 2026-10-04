---
name: cli-recorder
description: Use when authoring a CLI session recording for the cli-recorder skill. Translates a user's intent ("video of installing kubectl") into a valid recipe.toml through interactive Q&A.
---

# CLI Recorder — Recipe Author

Help users turn an idea ("a video of installing kubectl on macOS", "a tour of git rebase -i") into a valid `recipe.toml` for the `feinschnitt record` command.

## Quick Start

```
/record "a tour of git rebase -i"
```

See [`references/steps.md`](references/steps.md) for per-step detail and examples.

## When to use

User says "create a recording for X" / "record a demo of Y", invokes `/record`, or has a video idea but no recipe file yet.

## Hard gate

Do NOT run the recorder. Do NOT scaffold the surrounding Remotion video. Stop after the recipe is written and validated. The user runs `feinschnitt record` themselves once they're happy.

## Process

```
1. Discover intent           → What CLI? What's the audience? What's the takeaway?
2. Pick a profile            → claude-code | generic | interactive-tui
3. Sketch the steps          → 3-9 beats; each beat ≈ one screen of action
4. Resolve modal/interactive → which steps need dismiss keys, pattern waits, pauses
5. Tune cadence              → typing_wpm, idle compression, idle_time_limit
6. Write the recipe          → ${CLAUDE_PROJECT_DIR}/.recordings/recipes/<name>.recipe.toml
7. Show + validate           → display the file; offer a dry-run for verification
```

Apply **one question at a time** — prefer multiple choice over open-ended. The
storyboard is the step labels; sketch those before the `text` content. Validate
the written recipe against `schema/recipe.schema.json` before declaring done.

## References

- [`references/steps.md`](references/steps.md) — per-step detail, anti-patterns, label examples
- `schema/recipe.schema.json` — full validation surface; `profiles/*.toml` — profile presets
