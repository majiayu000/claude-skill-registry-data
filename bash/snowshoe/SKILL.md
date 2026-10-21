---
name: snowshoe
description: >-
  Snowshoe is a personal comprehension map of a git repository that shows where your
  understanding went stale after a pull and helps you catch up. Requires Bun.
  Install the `snowshoe` CLI: bun add -g @igorkravcenko/snowshoe.
  After pull or catch-up: drain via work next (init / routine refresh / routine advance,
  then complete claimed steps). In the map PTY or when studying the map
  (SNOWSHOE_MODE=learn): talk about the tree using map view / map status. Learn
  re-entry reprints the landed floor after a wiped-context break. Combined mode
  (map UI / UI terminal open while draining): read both drain.md and learn.md. Read
  install.md only if the snowshoe binary is missing.
---
> **What this is (for humans):** Snowshoe keeps a local map of how well you understand each part of a git repo. After a pull it shows which parts changed under you, and your agent walks you through catching up — or you explore the map in a browser UI.

# Snowshoe skill

Assume **`snowshoe` is on PATH**. Always pass `--json` and parse the result.

The install binary is **`snowshoe`** (call this).

If this working repo is missing the skill files under the harness skills dir, run
`snowshoe skill install --json --skills-path <harness-skills-dir>` (e.g. `.cursor/skills`
for Cursor). Opt-in; not part of `init`. Prefer `snowshoe help --json` over guessing flags. Root `--help` is human usage, not the agent index.

Drive the CLI. Do not write the ledger yourself. Do not start `map serve` unless the human asked.

If **this turn** they asked to mark, expand, enrich, fix, detail, or cancel named node(s) (or “this node”): `snowshoe map mark --json --slug <slug> --kind detail` (or `expand` / `enrich` / `fix`; `map detail mark` queues `detail`). Do not mark a tour of the tree. Then continue the drain/learn branch.

Read sibling files after the checks below. Default: **one** of `drain.md` or `learn.md`. **Combined** mode (below) may read **both**. Do not open `install.md` unless `snowshoe` is missing.

## 1. Binary

If `command -v snowshoe` fails, read **`install.md`** in this same folder — only then.

After following it, run `command -v snowshoe` again:

- Still missing → **STOP**. The binary often needs a **new shell** after global install or `bun link`. Tell the human how to re-check; do not start drain or learn.
- Now present **and** this turn already classified drain, learn, or combined → go to **Intent** and open that file.
- Now present **but** they only asked to install, or intent is still unclear → ask once: drain, learn, combined, or stop.

## 2. Intent

Classify in this order:

1. The **user prompt that invoked this skill**.
2. Nearby user text **this turn only** (not the rest of the thread).
3. If text is still empty: `SNOWSHOE_MODE=learn` → learn. Other/empty mode does not override an explicit drain prompt.
4. Else **drain**.

| Drain-adjacent | Learn | Combined |
|---|---|---|
| after pull, catch up, drain, `work next`, marked nodes, complete queue | study / explain the map, “what is this node”, look at the map, map PTY agent, `re-entry` | map UI open / UI terminal + keep draining while studying/learning in the **same** session |
| | `SNOWSHOE_MODE=learn` when (1)–(2) are empty | same-session foreground learn/map conversation **and** background `work next --wait` |

Explicit drain in the prompt beats env **unless** combined signals apply.

**Combined** when this turn (or the live map session) clearly has map UI / UI terminal / map PTY **and** keep-draining / catch-up / `work next --wait` together. Or if user explicitly asks for combined mode. Then read **both** `drain.md` and `learn.md`.

If drain and learn appear without a combined signal → ask one line which branch, or take the first/stronger signal. Then read only that file.

## 3. Branch

- Combined → read **`drain.md`** and **`learn.md`**
- Learn → read **`learn.md`**
- Drain (default) → read **`drain.md`**

### Combined session rules

- Background: one `snowshoe work next --json --wait` (optional `--wait-timeout 0`). Foreground: learn/map conversation in the same session / map PTY / UI terminal — do **not** kill the background waiter to study the map.
- Align with `drain.md` interactive `--wait`: at most **one** waiter; gates/work return immediately; when the waiter returns work, handle it then restart the waiter; never start a second waiter.

## 4. Optional feedback

`snowshoe feedback add --json` (stdin `{ "text": "…", "command": "optional" }`) appends a local note about Snowshoe. Use only if the tool is unclear, frustrating, or you have a concrete idea. Not required. Do not log secrets or lease tokens. Then continue drain, learn, or combined.
