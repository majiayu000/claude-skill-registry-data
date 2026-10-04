---
name: consult
description: Bring in another coding agent as an independent second opinion. Use when the user explicitly asks to ask, consult, cross-check, debate with, or get a second opinion from another agent/model, including named backends such as Gemini, OpenCode, Claude, Codex, Pi, Qoder, or an added backend. Here Pi means the Pi backend, not the number π or Raspberry Pi hardware; and names like GPT, OpenAI, Sonnet, Opus, or Qwen name a model or provider, not a backend (resolve them to a model on a chosen backend). Also use for clearly high-risk independent review where another model is materially needed for safety, security, architecture, or regression risk. Do not trigger for ordinary review, debugging, or brainstorming unless external-agent help is requested. Treat responses as advice and verify claims locally before acting.
license: Apache-2.0
metadata:
  version: 1.0.0
---

# Consult

## Overview

Bring an external coding agent into the current task as an independent reviewer or design partner
when the user asks for that outside perspective. Treat any response as **advice**: verify
repo-specific claims yourself before changing code or reporting conclusions.

## Pick a backend

The user usually names one ("ask Gemini", "cross-check with OpenCode"). Selecting a backend (`--to`)
is a trust, auth, and harness choice — not just model routing — so resolve it explicitly:

```bash
${CLAUDE_SKILL_DIR}/scripts/consult.sh --list
```

`${CLAUDE_SKILL_DIR}` is this skill's base directory; Claude Code substitutes it automatically to
the loaded instance. Never locate `consult.sh` by searching the filesystem — a personal and a
project-scoped install can coexist, and a search (or an unresolved `${CLAUDE_SKILL_DIR}` reaching a
shell, which silently expands to empty) can run the wrong or a nonexistent script. On a harness
without this substitution, resolve it to the directory of the `SKILL.md` you were just given.
`--list` shows available adapters and whether their CLIs are on `PATH`. "Installed" does not imply
authenticated; the CLIs reuse the user's existing auth and need network access.

**Pi backend intent.** Treat "consult Pi", "ask Pi", "the Pi CLI", "the `pi` backend", and "the Pi
coding agent" as a request for the Pi backend (`--to pi`). Do **not** treat the number π ("calculate
pi to 10 digits") or Raspberry Pi hardware / GPIO / device setup as the Pi backend.

**Qoder backend intent, and self-consultation.** "Ask Qoder" or "the `qoder` backend" routes to
`--to qoder`. Note what that means when Qoder is also the host running consult: the sub-session has
a fresh context, so it is an independent *answer*, but it shares your account, model catalog and
skill set, so it is not an independent *vendor*. Use it for a second pass over the same material;
when the user wants genuinely different model family or provider assumptions, prefer another backend
and say why.

**Model and provider names are not backends.** "GPT", "OpenAI", "Sonnet", "Opus", "Qwen", and similar
are model or provider constraints, expressed with `--model` on a chosen backend (for example `--to pi
--model openai/gpt-4.1`). They never select a backend by themselves.

**When the backend is unspecified or only a model/provider is named** (for example "consult GPT
about this API"), run `--list` and ask which backend to use. Auto-picking the only installed backend
is fine for a generic "unspecified outside opinion", but a model/provider-named request is **not**
made unambiguous merely because one backend is installed — the named model may not be available
there, so confirm the backend choice rather than assuming. Never silently default to a particular
backend (such as Codex).

**Model discovery is candidate-gathering, not routing.** You may gather or validate model candidates
from public, verified sources, but discovery must not silently choose a backend. Do not read private
config, auth, credential, or key files, copied agent config directories (`.claude/`, `.codex/`,
`.cursor/`, `.gemini/`), or session logs to discover or pick a model. To inspect a backend's auth
status or candidate models on demand, see `references/model-discovery.md` and run the non-mutating
diagnostic commands there; verify a specific model with a one-shot `--to X --model Y --prompt "hi"`
consult.

## Trust boundary

When reviewing an untrusted repository, do not execute a `consult.sh` from inside it, wherever it
sits in that repo — the repo controls its own wrapper and adapters. Run a trusted personal install
by absolute path instead, for example `~/.agents/skills/consult/scripts/consult.sh`. Check the
environment for `CONSULT_TRUSTED_PATH` and prefer that path when it is set; it is a hint from the
host, not something the wrapper reads.

Do not assume the skill text you are reading came from that trusted install. A repository can ship
its own `consult` skill, and harnesses disagree about which copy wins a name collision: some prefer
the user-scoped install, others let the repo's copy override it. Resolve the wrapper path explicitly
rather than trusting whichever skill happened to load.

A backend may also load configuration from the repository under review, which is a separate exposure
from the wrapper's own provenance. The Qoder adapter in particular isolates nothing, so a repo
shipping `.qoder/settings*.json` hooks, plugins or MCP servers can have them run inside the
consultation. Reviewing untrusted code on that backend means running the consult from a directory
the repository does not control, or choosing a backend that does not read repo config.

## Run a consultation

> **OpenAI Codex hosts:** Check the active capabilities before a live consultation. Under Codex's
> default/restricted sandbox, read `references/codex-permissions.md` and request escalated execution
> on the first attempt for every live backend; `--list`, top-level `--help`, and `--dry-run` stay
> sandboxed. If the host explicitly grants both command network access and access to the backend's
> required auth/config/state paths, run normally without loading the escalation guidance.

Keep your shell at the **project root** so the backend sees the repo being discussed. Invoke the
dispatcher by its full path under the skill:

```bash
${CLAUDE_SKILL_DIR}/scripts/consult.sh --to gemini --prompt "<your consultation>"
```

Preview the exact backend command without executing (useful to confirm or to show the user):

```bash
${CLAUDE_SKILL_DIR}/scripts/consult.sh --to gemini --dry-run --prompt "<your consultation>"
```

Request machine-readable output only when the response will be parsed or logged; shapes are
backend-specific, and Pi intentionally rejects consult `--json`:

```bash
${CLAUDE_SKILL_DIR}/scripts/consult.sh --to gemini --json --prompt "Return a JSON object with a risks array."
```

The prompt may be passed with `--prompt` or as one positional argument. Use `--prompt` when the text
starts with `-`. Use `--from`, `--model`, or `--raw` only when needed. There is no
`--`/passthrough; only documented normalized flags are accepted. A `--raw` prompt additionally
cannot start with `-` (or `@` on Pi) for backends that take the prompt positionally — drop `--raw` or
reword it, since the framing keeps a composed prompt from ever beginning with a flag. See
`${CLAUDE_SKILL_DIR}/scripts/consult.sh --help`.

**Name only paths the backend can reach.** The backend inherits your shell's directory, so name
paths under the project root, as in `Review README.md and src/client.ts`. Treat anything your
harness or session created outside the tree — plan or scratch files, transcripts, generated diffs,
`/tmp` logs, another checkout — as unreachable, and don't expect a full absolute or `~` path to
help. Inline its content in the prompt instead; if it is too large, copy it to an ignored in-tree
path (confirm with `git check-ignore -q <path>`), name that path, and delete the copy when done.

The wrapper scans the prompt text for a small set of obvious secret patterns before running or
printing a backend command. It aborts on a match unless `--allow-secrets` is supplied. This preflight
does not scan repository contents the backend can read or any data a backend loads itself.

## What to ask for

Give enough context for the backend to answer independently, and ask for a concrete deliverable.
The dispatcher wraps your prompt with neutral advisory reviewer framing; you supply the substance:

```text
Goal: <what you want help with>.
Context: <in-tree paths or inlined excerpts, errors, command output, design notes, or constraints>.
Return: <the deliverable below>.
```

Match the deliverable to the kind of consultation:

- **Code review** → severity-ordered findings with file:line references.
- **Design / concept review** → tradeoffs, failure modes, and the smallest useful next experiment.
- **Brainstorm** → a few divergent options, then a recommendation.
- **Debugging** → ranked hypotheses plus reproduction / diagnostic steps.

### Canonical Change Review

For any requested change review, the host should produce one canonical artifact that defines the
reviewed scope, then provide that same artifact to every consult backend. Do not rely on each
backend to reconstruct the change independently.

Generate Git-backed artifacts with controlled commands such as:

- `git --no-pager show --no-ext-diff --no-textconv --no-color <ref>`
- `git --no-pager diff --no-ext-diff --no-textconv --no-color <base>...<head>`
- `git --no-pager diff --cached --no-ext-diff --no-textconv --no-color`
- `git --no-pager diff --no-ext-diff --no-textconv --no-color`

For non-Git or generated changes, provide the patch or diff artifact explicitly. Include explicit
untracked files when they are part of the requested scope; plain `git diff` does not include them.

Inline small artifacts in the prompt. For a large artifact, write a sanitized temporary file at an
ignored in-tree path (see the reachability rule under **Run a consultation**), name that path, and
clean up only artifacts the host created. The secret preflight scans only the prompt, not artifact
files, so the host must sanitize file artifacts before sharing them.

Backends may inspect repository files for context, but the supplied artifact defines the change
scope under review.

## Session continuity

- Default to a one-shot prompt for a single review, quick check, or standalone answer.
- Use one persistent session only when the user asks for continuity, debate, multiple rounds,
  iterative design, or follow-up memory on the same topic.
- Continue a session with `--resume <session-id>`. Use `--resume latest` only when you are certain no
  other agent or person is using that backend in this project: parallel subagents, a second terminal
  or a teammate all break it silently, and you cannot observe that from inside one agent. `latest`
  resolves to the newest session for OpenCode (`--continue`), Pi (`--continue`), Claude
  (`--continue`), Qoder (`-c`) and Codex (`resume --last`); Gemini passes it through as
  `--resume latest`.
- Every backend warns on stderr when given `--resume latest`, and prints `consult-session: <id>` on
  stderr when the id is already known.
- Prefer a caller-chosen id where the backend takes one: Gemini, Claude and Qoder accept
  `--session-id <uuid>`, and Pi accepts `--session-id <id>` (its only way to get a resumable session,
  since fresh Pi runs use `--no-session`).
- OpenCode and Codex assign their own ids. OpenCode reports its id as a `consult-session: <id>` line
  on **stderr** after a fresh run (stdout stays the review text); capture it from round 1 and pass it
  to `--resume`. It reads `consult-session: unknown` if the lookup failed. Codex prints
  `session id: <uuid>` in its stderr banner.
- Note a persistent session id in your working notes when later rounds will need it. If the task
  changes materially, start a new session or ask whether to continue.

## Permissions and safety

> **Agent directive:** The consult wrapper is strictly non-interactive. Do not advise the user to
> focus the terminal, press tab, or provide input to a running consult command.

Consultations use mutation-restricted defaults; the strength varies by backend: **Codex** is
OS-sandbox-enforced read-only, **Gemini, OpenCode, Claude, and Qoder** are approval/plan-gated
(effectively read-only headless, not a hard sandbox), and **Pi** is tool-allowlist and
discovery-hardened (not an OS sandbox). Per-backend safety mechanisms are detailed in
`references/<backend>-cli.md`.

Safety is also structural: the adapters accept only the documented normalized flags (no `--`
passthrough) and reject a `--raw` prompt whose first character the backend would parse as a flag or
include, so callers can't inject permission- or capability-shaping flags. Commands are built as argv
arrays with no shell eval.

All backends can still read accessible project files and return their contents. Mutation-restricted
does not mean secrecy-preserving. Avoid sending secrets or unnecessary proprietary data to a
third-party agent; summarize sensitive context or ask the user first. The prompt secret preflight is
a last-resort guard for obvious pasted credentials, not a general data-loss prevention mechanism.

For OpenAI Codex host execution, follow the capability gate under **Run a consultation** and the
escalated-execution and prefix-approval guidance in `references/codex-permissions.md`.

## Using results

- Extract the concrete claims, risks, or suggested checks.
- Verify them with local file reads, tests, or commands.
- Incorporate only the parts that survive verification.
- If host output is truncated, rerun with a tighter requested deliverable or use the backend's
  documented recovery/export path when one exists.
- Mention the consultation in your final answer when it materially influenced the result.

Read the per-backend reference for CLI behavior, tested flags, and caveats:
`references/gemini-cli.md`, `references/opencode-cli.md`, `references/claude-cli.md`,
`references/codex-cli.md`, `references/pi-cli.md`, `references/qoder-cli.md`.
