---
name: huggingface
description: Inspect and manage robotics datasets, models, Jobs, and Spaces on Hugging Face.
---

# Hugging Face

The Hub is an artifact boundary. Know exactly what is crossing it, under which
identity and revision, before transferring data or changing remote state.

## Inspect first

- Check the installed `hf` CLI and the relevant command group's live help.
  Commands and hosted services evolve faster than this skill.
- Inspect the repository card, file tree, revision, license, access state, and
  transfer size before downloading or planning around an artifact.
- For robot data, also verify embodiment, task, observation/action schema,
  cameras, timing, episode structure, and format version.
- Pin an immutable revision when the artifact feeds a reproducible build,
  fixture, evaluation, or training run.

## Treat remote changes as real changes

- Use an existing authenticated identity or a secure browser/device login. Do
  not place tokens in prompts, source, shell history, or logs.
- Before creating or uploading, establish the destination owner, repository
  type, visibility, local source, changed paths, and whether deletion is
  involved.
- Starting Jobs is paid remote compute. Establish the current hardware,
  command, timeout, outputs, secrets, and cost exposure before submission.
- Inspect a Space's metadata, build logs, and runtime logs before restarting or
  changing hardware.
- A Space is an optional hosted presentation layer, not a requirement for using
  Hub datasets or models. Most Docker Spaces can also be run locally; keep the
  application portable when self-hosting or another service is plausible.
- After a mutation, inspect the remote result rather than trusting the local
  command's intent.

## Go deeper only when needed

- For current CLI shapes, Dataset Viewer endpoints, and mutation preflights,
  read [references/hub-operations.md](references/hub-operations.md).
- LeRobot owns dataset structure, processors, training, and evaluation; this
  skill owns the Hub boundary around those artifacts.
- Data owns source selection. Use integration for service packaging, network,
  health, and self-hosting boundaries; use the relevant deployment skill for
  provider mechanics when a Space is not the chosen runtime.
- Use the current [Hugging Face documentation](https://huggingface.co/docs)
  and live CLI help as the source of truth for volatile flags and services.

## Done

- The intended artifact, revision, identity, destination, and remote result are
  all verified, with no credential exposed and no unapproved paid or
  destructive action.
