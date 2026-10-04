---
name: coding-agents
description: Delegate coding tasks to autonomous AI coding agent CLIs — Claude Code, OpenAI Codex, GitHub Copilot CLI, and
  OpenCode. Covers installation, auth, print mode, interactive PTY sessions, PR reviews, parallel work, and pitfalls for all
  four agents.
version: 1.0.0
author: Hermes Agent (curator consolidation)
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Coding-Agent
    - Claude
    - Codex
    - Copilot
    - OpenCode
    - PR
    - Refactoring
    - Automation
    related_skills:
    - hermes-agent
    - multi-agent-research
    - obsidian-vault-cluster-operations
    - gemini-vault-worker
lane: koenigin
reasoning_effort: xhigh
---
# Coding Agents — Autonomous AI CLI Orchestration

Delegate coding tasks to AI coding agent CLIs. Four agents are covered:

| Agent | Provider | Install | Best For |
|-------|----------|---------|----------|
| **Claude Code** | Anthropic | `npm i -g @anthropic-ai/claude-code` | Deep reasoning, large codebases, MCP |
| **Codex** | OpenAI | `npm i -g @openai/codex` | Fast execution, `--full-auto` sandbox |
| **Copilot CLI** | GitHub | pre-installed on this system | ACP integration, GitHub-native |
| **OpenCode** | Any provider | `npm i -g opencode-ai` | Provider-agnostic, local Ollama |
| **Gemini CLI** | Google | `npm i -g @google/gemini-cli` | Gemini-3-Pro/Flash via OAuth (Google AI Pro Abo) **oder** API-Key, multimodal, 1M context |

## When to use

Use this skill when you need to delegate a coding task to an autonomous AI CLI rather than do it yourself. Typical triggers:

- One-shot code edits, refactors, or new features in an existing repo
- PR review of a diff that is too large or noisy for inline reading
- Batch fixing of issues (e.g. sweep a list of `TODO`s across files)
- Sweeping a long log/build output through a coding agent for triage
- Running agents in parallel on independent tasks (one per worktree)

**Do not use this skill** for chat-only Q&A, doc writing without code changes, or anything that does not need a coding agent — handle those directly.

## Common Patterns (All Agents)

### Print Mode (Preferred for One-Shots)
```
<agent> -p "Fix the auth bug in src/auth.py" --allowedTools "Read,Edit" --max-turns 10
```
Non-interactive, exits when done, no PTY needed. Preferred for automation.

### Interactive PTY Mode (Multi-Turn)
```
tmux new-session -d -s agent -x 140 -y 40
tmux send-keys -t agent 'cd /project && <agent>' Enter
tmux send-keys -t agent 'Your task' Enter
tmux capture-pane -t agent -p -S -50  # monitor
```

### Parallel Work
Run multiple agents simultaneously in separate tmux sessions or background processes for batch work.

---

## Claude Code

See `references/claude-code.md` for the full reference. Key points:
- **Print mode:** `claude -p "task" --allowedTools "Read,Edit" --max-turns 10`
- **Interactive:** Requires tmux. Handle trust dialog (Enter) and permissions dialog (Down+Enter).
- **JSON output:** `--output-format json` returns structured result with `session_id`, `total_cost_usd`.
- **Session resume:** `--resume <id>` or `--continue` for most recent.
- **PR review:** `git diff main...branch | claude -p "Review this diff" --max-turns 1`
- **MCP:** `claude mcp add <name> -- <cmd>` with scopes: `-s user`, `-s local`, `-s project`.
- **Pro-Plan Reality (CRITICAL):** Pro/OAuth läuft auf 5h-Session-Limits, nicht Token-Billing. `--max-budget-usd` unter $2 killt mitten im Output (Fable 5 blieb stumm bei $0.50, Output verloren). **KEIN Budget-Limit für Read-only/Analyse-Tasks.** Siehe `references/claude-pro-plan-budget.md`.
- **Fable 5:** Verfügbar via `--model sonnet-5-20260622` (Display-Name "Fable 5", Flag ist anders). Neuestes & größtes Modell. Best für Analyse/Inventur. Kein Budget-Cap setzen.
- **Model-Naming:** `claude -m` zeigt "Fable 5" / "Opus 4.8" / "Sonnet 5", aber `--model` braucht `sonnet-5-20260622` — Diskrepanz zwischen Display und Flag.
- **Skills vorladen:** Claude Code hat keinen Skill-Zugriff — Briefing muss `skill_view()` + Inhalt embedded enthalten.
- **Output retten:** Wenn `--max-budget-usd` mittendrin killt, Output liegt im `/tmp/`-File vom `cat >` des Briefings. `cat` prüfen statt neu starten.

## Codex

See `references/codex.md` for the full reference. Key points:
- **One-shot:** `codex exec "task"` — exits when done.
- **Background:** `codex exec --full-auto "task"` with `background=true, pty=true`.
- **Sandbox:** `--full-auto` (sandboxed), `--yolo` (no sandbox), `--sandbox danger-full-access` (for service contexts).
- **PR review:** Clone to temp, `codex review --base origin/main`.
- **Parallel:** Use git worktrees + separate Codex processes.
- **Pitfalls:** Requires `pty=true`. Must run inside a git repo. `--max-turns` not supported.

## Copilot CLI

See `references/copilot-cli.md` for the full reference. Key points:
- **Print mode:** `copilot -p "task" --allow-all`
- **ACP mode:** `copilot --acp --stdio` for `delegate_task(acp_command="copilot")`.
- **Auth:** `COPILOT_GITHUB_TOKEN` in `~/.hermes/.env` or interactive `/login`.
- **Model:** `copilot --model <model>` or `~/.copilot/config.json`.
- **Pitfalls:** ACP mode requires auth first. VS Code ACP extension needs separate config.

## OpenCode

See `references/opencode.md` for the full reference. Key points:
- **One-shot:** `opencode run "task"` — no PTY needed.
- **Interactive:** `opencode run --continue <id>` or `opencode` with `background=true, pty=true`.
- **Ollama:** Use `ollama launch opencode --model <name>` (NOT `opencode run --model ollama/<name>`).
- **Session resume:** `opencode -c` (last) or `opencode -s <id>` (specific).
- **PR review:** `opencode pr 42`.
- **Pitfalls:** `/exit` is NOT a valid command — use Ctrl+C (`\x03`). PATH may differ (`npm root -g`). Ollama requires `ollama launch opencode`.

## Gemini CLI

See `references/gemini-cli.md` for the full reference. Key points:
- **Two auth modes:** `oauth-personal` (Google-Account-Login → nutzt Google AI Pro/Ultra-Abo-Kontingent, **kein API-Billing**) **oder** `gemini-api-key` (separater AI-Studio-Key → eigenes Free-Tier/Pay-as-you-go). Default der `.env` ist `gemini-api-key` — vor Login `settings.json` patchen wenn OAuth gewünscht.
- **Print mode (read-only):** `gemini -p "task"` — **KEINE Schreibwerkzeuge aktiv**. Gemini sagt ehrlich "I have no tools for this" wenn du es nach Datei-Operationen fragst. Same pattern as Claude/Codex.
- **YOLO mode (Schreibzugriff):** `gemini --yolo -p "task"` — aktiviert write_file, replace, run_shell_command. **Ohne `--yolo` = kein Schreiben.** Immer mit Scope-Restriktion koppeln.
- **Scope-Restriktion:** `--include-directories "/path/to/vault"` — limitiert Datei-Zugriff. **Pflicht bei Vault-Work**.
- **Vault-Worker Subagent-Pattern:** `--yolo` + `--include-directories` + timeout 600 + Pattern-7-Verifikation. MiniMax-Biene dispatchen, die Gemini-CLI mit Briefing + Plan aufruft. Gemini erstellt Satelliten-Notes und patcht additive "Verbindet zu"-Sektionen. Respektiert Anti-Pattern-Listen (MOCs, Zero-Content, verbotene Folder). Vorher Backup + nachher Pattern-7-Cross-Check. Siehe `references/gemini-cli.md` → "Vault-Worker Subagent Pattern".
- **Model flag:** `gemini -m gemini-2.5-flash` (fast) **oder** `-m gemini-2.5-pro` **oder** `-m gemini-3.1-pro-preview` (latest, User-Präferenz).
- **No PTY needed** for `-p` or `--yolo` mode — unlike Codex/Claude.
- **Pitfalls (kritisch):** OAuth-URL **NICHT durch Hermes-Background-Terminal rendern** — `%20` und `code_challenge` werden gemangelt, Browser bekommt kaputten URL, Google antwortet "Request malformed". Lösung: User startet `gemini` (oder `NO_BROWSER=true gemini` mit `pty=true`) selbst in seinem Terminal und holt den Code manuell. `head -40` auf den CLI-Output killt sie mit "non-interactive" — ohne `pty=true` keine URL. Pro-Preview-Modelle können >90s für eine Antwort brauchen → `timeout 240-600` setzen. YOLO-mode ohne Scope-Restriktion = voller Shell-Zugriff — `--include-directories` setzen.

## Cross-Agent Pitfalls

1. **All interactive agents need tmux** — raw PTY mode has issues with prompt_toolkit.
2. **Always set `workdir`** — keeps agents focused on the right project.
3. **Budget-Strategie je nach Auth-Methode** — Für API-Token-Pläne: `--max-budget-usd` + `--max-turns` setzen. Für **Pro/OAuth (5h Sessions):** Budget-Caps für Analyse/Audit-Tasks WEGLASSEN (`--max-budget-usd` killt mitten im Output). `--max-turns` weiterhin setzen (Default 10, Max 30). "C sei am anfang jetzt nich geizig" — bei Analyse großzügig starten.
4. **Monitor with `tmux capture-pane`** — look for `❯` prompt (waiting) or `●` (working).
5. **Clean up tmux sessions** — `tmux kill-session -t <name>` when done.
6. **Git repo required** for Codex and recommended for all others.
7. **Parallel sessions must use separate workdirs** — avoid git conflicts.

## References

- `references/claude-code.md` — Full Claude Code reference (modes, flags, MCP, hooks, CLAUDE.md)
- `references/codex.md` — Full Codex reference (modes, sandbox, parallel worktrees)
- `references/copilot-cli.md` — Full Copilot CLI reference (modes, ACP, VS Code)
- `references/opencode.md` — Full OpenCode reference (modes, Ollama, session management)
- `references/gemini-cli.md` — Full Gemini CLI reference (OAuth vs API-Key, models, NO_BROWSER flow, URL-Mangling-Falle)
- `references/parallel-hive-triage.md` — Fable Schwarm: parallel Claude Haiku instances as bash background processes for Triage/Analyse

## Support Scripts (in `~/.hermes/scripts/`)

- **`gemini-smoke.sh`** — Canonical Gemini-CLI verification: checks binary, settings.json, `GEMINI_API_KEY` in `.env`, OAuth token fallback, runs a live 30s API call. Use after any auth/setup change.

## Worker-Tool Selection (Queen → Worker → Tool)

**Architectural mental model (CRITICAL — read first):**

```
Yuno (Queen, MiniMax-M3)
   │  plans, routes, consolidates
   ▼
Subagent Worker (MiniMax-M3 — die "Worker-Biene")
   │  has isolated terminal + toolset
   ▼
External Tool-CLI (gemini / claude / codex / opencode / copilot)
   │  invoked via shell
   ▼
Backend LLM (Gemini-Flash, Claude-Sonnet-5, GPT-5, Llama, ...)
```

**The "Worker-Biene" ist der Hermes-Subagent** (MiniMax-M3 Prozess). External CLIs sind **Werkzeuge**, nicht selbst Bienen. Beim Subagent-Dispatch zeigt der Header `Model: MiniMax-M3` weil Hermes das Model an Kinder vererbt — das ist die Biene; das via CLI aufgerufene Backend-LLM ist nur eines ihrer Werkzeuge.

**Common confusion to avoid:** When a subagent's header says `Model: MiniMax-M3`, it does NOT mean "Gemini (or Claude/Codex) is one of our worker bees". It means "the Hermes Subagent process is the bee, running on MiniMax-M3, and it called an external CLI as a tool". The external LLM never appears in the Hermes dispatch header — it's behind the CLI. Don't confuse these two levels when reporting results to the user; this was explicitly corrected mid-session (2026-07-05).

### Auth Fallback Chain (gemini-cli, learned 2026-07-05)

The Gemini CLI silently falls back between auth sources in this order:

1. **`GEMINI_API_KEY`** in `~/.gemini/.env` (if set, mode = `gemini-api-key`)
2. **OAuth access_token** in `~/.gemini/oauth_creds.json` (if no key, even when `settings.json` says `gemini-api-key`)
3. Fail with `API_KEY_INVALID` (HTTP 400)

Implication: even if you switch `settings.json` to `gemini-api-key` for safety, leaving the OAuth token on disk still lets the CLI work via OAuth. To force key-only mode, either delete `oauth_creds.json` or remove the OAuth lines from `.env` AND delete the token file. Verify effective auth with `bash ~/.hermes/scripts/gemini-smoke.sh` (checks both sources).

### Code Assist API Deprecation (CRITICAL, 2026-07-05)

Google deprecated the "Gemini Code Assist for individuals" OAuth backend. As of 2026-07-05, `oauth-personal` login flow on Gemini CLI 0.49.0 returns:

> "This client is no longer supported for Gemini Code Assist for individuals. To continue using Gemini, please migrate to the Antigravity suite of products: https://antigravity.google"

The OAuth token is still saved to `oauth_creds.json` (the CLI completes the flow), but it can't be redeemed against the Code Assist API until Antigravity migration completes. **Workaround for now**: use `gemini-api-key` mode with an AI Studio key. New products land at https://antigravity.google — watch for the successor CLI/extension.

### Routing-Matrix (Welches Tool für welchen Task?)

| Task-Typ | Best Tool | Begründung |
|---|---|---|
| **Default — alle Coding-Tasks** | `gemini-3.1-pro-preview` (`gemini -m ... -p "..."`) | **User-Präferenz 2026-07-05: IMMER 3.1 Pro Preview.** Reasoning-stärkstes Modell, Tradeoff: langsamer (timeout 180-300s) |
| **Quick code snippet (wenn Speed wichtiger als Reasoning)** | `gemini-2.5-flash` | Schnellste Antwort (12s), nur auf explizite User-Anweisung wenn Flash gewünscht |
| **Obsidian Vault-Strukturierung (Cross-Links, Satelliten, Analyse)** | `gemini-3.1-pro-preview` → via Subagent-Biene | 1M Context erfasst gesamten Vault auf einmal. Besseres Reasoning für Cross-Cluster-Verknüpfungen als MiniMax. Siehe `obsidian-vault-cluster-operations` Pattern 9. |
| **Hard reasoning, multi-step refactor** | Claude Code (Sonnet 5) ODER `gemini-3.1-pro-preview` | Beide stark; Claude wenn MCP/Repo-Integration nötig, Gemini wenn standalone reasoning |
| **Sandboxed auto-edit** | Codex (`codex exec --full-auto`) | Eingebauter Sandbox, Git-Repo-Pflicht |
| **GitHub-native PR review** | Copilot CLI | `copilot pr 42` ist direkt |
| **Local offline (kein Cloud)** | OpenCode + Ollama | Komplett lokal, kein API-Kontingent nötig |
| **Multimodal (Bilder, PDFs)** | Gemini CLI | Native multimodal stark, kein Extra-Tool nötig |
| **Coding ohne Cloud-Kontingent (Sparkurs)** | OpenCode + Ollama | Kostenlos, langsamer, aber unlimited |

### Default-Aufruf (für Quick-Tasks)

```bash
# Standard: Gemini 3.1 Pro Preview (User-Präferenz 2026-07-05)
# timeout hoch genug setzen — Pro-Preview braucht >90s für reasoning-schwere Aufgaben
timeout 240 gemini -m gemini-3.1-pro-preview -p "<task>"
```

**Nur auf explizite Anweisung** auf Flash wechseln (`gemini-2.5-flash`, timeout 60), z. B. wenn der User Speed vor Reasoning priorisiert.

### Verification Script (canonical helper)

After any Gemini auth/setup change, run the bundled smoke test to verify both auth sources AND that the CLI actually answers:

```bash
bash ~/.hermes/scripts/gemini-smoke.sh
```

Checks: gemini binary present, settings.json auth mode, `GEMINI_API_KEY` in `.env`, OAuth token fallback in `oauth_creds.json`, live 30s API call to `gemini-2.5-flash`, exit code, word count, subagent-readiness. Green = ready as a worker tool. Use this instead of hand-rolling a one-off test.
```

### Subagent-Dispatch-Pattern (für Worker-Bienen)

```python
delegate_task(
    goal="Führe aus: timeout 240 gemini -m gemini-3.1-pro-preview -p '<task>' und berichte stdout+exit-code.",
    role="leaf"
)
```

Der Worker-Subagent (MiniMax-M3) führt den Gemini-Aufruf aus, sammelt das Ergebnis, und liefert es zurück an die Queen. So kombiniert man: **MiniMax-Biene als Worker + Gemini-CLI als Tool** für maximale Token-Effizienz (kein MiniMax-Reasoning-Token-Verbrauch für die Tool-Antwort selbst).

### Pro-Abo-Haushalts-Tipp

Da das Google AI Pro Abo ein **Kontingent** hat (nicht unlimited):
- **User-Präferenz (2026-07-05):** IMMER `gemini-3.1-pro-preview` verwenden. Das ist das reasoning-stärkste Modell, kostet aber mehr Kontingent als Flash.
- Tradeoff akzeptieren: Pro-Preview kann >90s brauchen → `timeout 240` oder höher setzen.
- **Flash nur als Fallback** wenn explizit gewünscht oder bei Timeouts (`gemini-2.5-flash`).
- **Telemetrie deaktivieren** (spart Log-Traffic): `DISABLE_TELEMETRY=1` in `~/.gemini/.env`
