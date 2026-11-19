---
name: pick-the-best-ai-model
description: A sourced shortlist of which AI models your app should ship or call, for every kind of model it uses and every device class it runs on, with a clear Add, Replace, Keep, Later or Remove call for each. Use when you say "pick the right models", "which model should we use", "which models should ship", "is there a better model for this", "refresh our model list" or "model research".
---

# Pick the right AI models for your app

Research which models an app should offer, on facts read from real sources, and turn the result into decisions
the user can approve. Then, once approved, write those picks into the app's model list. This skill adds no app
feature and no schema, and never edits the app's code or model list on its own.

## 1. Learn what the app already does

Before any research, find out from the code (ask only for what the code cannot tell you):

- **Kinds of model** the app uses: chat, vision, image generation or editing, video, voice (text to speech),
  transcription (speech to text), embeddings, rerankers, computer use, or others.
- **Where each runs:** on the device (phone, desktop, browser) or through a hosted API. Note the runtime or format
  (for example llama.cpp and GGUF, MLX, ONNX, Core ML, transformers, diffusers, a provider SDK).
- **The current list** of models: a catalog file (`models.json`, a config, a constants file), entries kept in code,
  and any rules that pick a default per device. Read the rules themselves, not just the list.
- **Device classes:** for on-device apps, the memory tiers that matter (for example phones with 6, 8, 12 and 16 GB,
  desktops from 8 to 128 GB). For hosted models, the limits that matter instead (latency, context length, rate
  limits, cost per call).
- **What the user cares about:** quality, speed, size, licence for commercial use, languages, privacy (local only
  or cloud allowed), and anything that rules a model out. Write these down; they decide every call below.
- **Never offer list.** Ask whether any kind of model is excluded (for example uncensored or abliterated
  variants). Filter them out of every list.

## 2. Build the pool of candidates

For each kind of model, gather everything that could reasonably ship:

1. Everything the app lists today, as the baseline.
2. New and trending open-weight models from Hugging Face. Run from this skill's folder:

   ```bash
   node scripts/hf-candidates.mjs --task <pipeline tag> [--library gguf|mlx|onnx|...] \
     [--max-params <billions>] [--since <YYYY-MM-DD>] [--exclude "<never-offer regex>"] [--sort trending]
   ```

   It uses the public API, needs no key, and prints a table with size, licence, gated or not, release date,
   downloads and a link. Run it per kind, and again sorted by `downloads` to catch proven models.
3. Hosted models from the providers the app supports, when cloud is allowed. Read each provider's own model page.
4. Recent launches the user or their news sources mention.

Keep, for each candidate: id, name, maker, kind, size (total and active parameters), the build or quantization
you would ship, download size, the smallest memory tier that runs it well, licence and whether commercial use is
allowed, release date, and the source of every fact.

## 3. Score each kind on one benchmark

Use **one public benchmark per kind**, so models of a kind compare on the same scale. Name it, link it, and record
the date you read it. Good defaults (check they are still current):

| Kind | Benchmark |
|---|---|
| Chat, vision | Artificial Analysis Intelligence Index, or LMArena |
| Image | Artificial Analysis text-to-image arena (Elo) |
| Video | Artificial Analysis text-to-video arena (Elo) |
| Voice | Artificial Analysis text-to-speech arena (Elo) |
| Transcription | Hugging Face Open ASR leaderboard (average word error rate) |
| Computer use | OSWorld-Verified (success rate) |
| Embeddings | MTEB leaderboard |

**Facts are read from the page, never estimated.** A model that is not on the board shows "not listed". If you
match a model to a board entry by name and the match is not exact, mark it as matched by name. Release dates come
from the model card or the maker's announcement, else the Hugging Face repo's creation date.

## 4. Pick per device class

For each kind and each device class (or each hosted-model use case), name the pick for **Fast**, **Balanced**
and **Best**: the smallest model that is good enough, the best value, and the best that still runs well. Follow
the app's own picking rules where they exist, and say where your pick differs from what the rules would choose.
A model that only just fits the memory tier does not run well; leave headroom for the app and the system.

## 5. Write the decisions

One decisions table per kind, using `references/decision-table.md`. Each row is one model and one call:

- **Add**, **Replace** (name what it replaces), **Keep**, **Later** (worth it, not yet) or **Remove**.
- Gain against what it replaces, with the benchmark number for both.
- Cost: download size, the smallest phone and desktop that run it well, or the cost per call for hosted models.
- Effort: S, M or L, and what the work is (catalog entry only, a new runtime feature, a companion model, and so on).
- Platforms today and after.
- Licence and commercial use.
- Risks (gated repo, licence limits, memory pressure, runtime support not yet confirmed).
- Sources, each linked and dated.

Present it as a page the user can sort and read: a local HTML file, or a markdown file if that is all you can
make. If your agent can publish private pages (for example Claude's Artifacts), publish it there and give the
link. For a board the user can drag picks around on, keep their choices in the page's own storage and never
overwrite them when you refresh the pool.

## 6. Ship the approved picks

Only after the user approves, and only the picks they approved:

1. Read the app's model list format and its README or schema notes. Keep its structure, version field and any
   sections you were not asked to change.
2. Write each approved model's entry in that format. Bump any updated-at field.
3. Commit named files only, on the branch the user names. Push only when they say so.
4. Tell the user in a few bullets what changed per device class.

## Refreshing later

Re-run steps 2 to 5. Keep the user's earlier choices as they are; show new candidates and changed benchmark
numbers as new rows, with the date they were read.
