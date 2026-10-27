---
name: switch-model
description: Switch the OpenCode model that implements or reviews (harness.json), safely - live ids, the right login, high effort, the family rule, and a one-word probe before anything is written. Use when the user wants another implementer or reviewer model, when a model keeps failing (exit 3, early stops, Bad Request), or before trying a new model on real tasks.
---

# /switch-model: change the implementer's or the reviewer's model

Each role runs its OpenCode chain, then Claude: today, GLM-5.3 Flash on Z.AI implements, then
MiMo V2.6 Flash on Go (then Sonnet), and GPT-5.6 Luna on the direct OpenAI route reviews (then
Opus). The user decided this on 2026-10-02 (L27) and on 2026-10-04 (L42, L51). A switch changes one role's model; it is the user's decision, so you
propose it and the user says yes.

1. **Why.** Name the reason: a measured failure (the run logs, the measurement comments), a
   cheaper or better candidate, or the user's request. A model that failed once on a strange task
   is not yet a reason (L14).
2. **What runs now.** `node tools/harness/switch-model.mjs --show`.
3. **Candidates, live** (L25), never from memory:
   - implementers on the Go subscription: `opencode models opencode-go`;
   - the direct routes, with their own logins: `opencode models openai`, and so on.

   Leave out a model of the other role's family (the reviewer is never the implementer's family),
   and models already ruled out in `docs/lessons.md` (L27: Go's own GPT-6 Luna returns
   `Bad Request` in long loops). `--show` lists the models on watch (L35): registered candidates,
   each with a `watch` note in `harness.json` on what to look for, which the runner prints when it
   runs one; their measured runs are the best reason to switch.
4. **Dry run with a probe:**
   `node tools/harness/switch-model.mjs --role implementer|reviewer --model PROVIDER/ID --probe --dry-run`.
   - It checks the id against OpenCode's list in the scripts' data directory. On exit 3, give
     the user the login command it prints; the user runs it.
   - The effort, unless `--variant` gives one: `high` for a light model; for a heavy one (Sol,
     GLM-5.3, MiMo V2.6 Pro, Opus) `low`, else `medium`, else the lowest OpenCode offers (L54).
     `max` is refused.
   - It shows the family and refuses the other role's. `--force` is only for when the user is
     switching both roles.
   - The probe is one billed one-word call at that effort.
5. **Ask.** Show the user the before and after lines and the probe's time, with your
   recommendation. Switch only on their yes.
6. **Switch.** Run the same command without `--dry-run` (and without `--probe`, which already
   passed). Then commit `harness.json` on `main` with the reason and the probe in the message
   (L6, L25). Keep the old model's entry: an explicit `--model` can still use it. A model on watch
   keeps its note through the switch; only the user's decision removes it.
7. **Watch the first run** on the new model. That means the log's tail and, for a reviewer, the
   posted review. Afterwards, add a line to the task's measurement comment (process.md §9).
   Switch back the same way if it fails.

Exits: 0 switched (or shown, or a dry run); 1 refused (the family rule, or a taken name); 2 usage;
3 OpenCode, the login or the probe failed, and nothing was written.
