---
name: user-action-edge-cases
description: Use when finishing anything that depends on external state a person controls - a file, a record, a folder.
---

## The rule

Anything you depend on that a user can touch will get renamed, moved, deleted, and duplicated. If your code assumes a fixed path or a single copy, it breaks the first time the user does something ordinary. Before you finish, run those four actions through your head.

## Fires when

Your code reads, writes, or depends on a file, a record, a document, or any state the user can edit outside your code.

## How to apply

For each thing you depend on, ask the four questions: renamed? moved? deleted? duplicated?

Prefer finding things by type or id over a hardcoded path or name. Decide what happens in each case instead of assuming it won't happen.

## Worked example

Your app stores its settings in a file at a hardcoded path. It works on your machine. Then a user renames the file, and the app silently writes a fresh one with defaults, losing their config. Or they copy the project folder, and now two copies fight over the same path. Looking the file up by a stable marker instead of a fixed name, and handling "not found" and "more than one" on purpose, turns four silent bugs into defined behavior.

## Red flags

| Thought | Reality |
|---|---|
| "The file is always at this path" | Until the user moves it. |
| "There's only ever one" | Until they duplicate it. |
| "They won't rename it" | They will. |
