---
name: snyk-agent-scan
description: "Inventory and risk-score the agent surface installed on a host: MCP server configs, skills directories and the tools, prompts and resources each server exposes. Use when auditing a developer workstation or CI image for agent tooling that can reach files, secrets or the network. Not for reviewing agent source in a repo (use agentic-radar) or probing an LLM endpoint (use garak)."
---

# Snyk Agent Scan

Snyk Agent Scan walks the places agent clients keep their configuration, connects to each MCP server it finds, lists the tools, prompts and resources that server advertises, scans nearby skill directories, and asks a verification service to score the result. It answers a host question: what agent capability is installed here, and does any of it look hostile.

On this host: `snyk-agent-scan` 0.6.9, pipx-installed at `~/.local/bin/snyk-agent-scan`, python package `agent_scan`. Cosmetic quirk worth knowing: its `usage:` lines and argparse errors print the program name `omp`, not `snyk-agent-scan`. Grep help output with that in mind.

## When to use

| Goal | Command | Note |
| --- | --- | --- |
| Default inventory of every known client config | `snyk-agent-scan` | same as `scan` with no paths |
| Inventory one config file | `snyk-agent-scan scan ./mcp.json` | still prompts before starting a stdio server |
| List tools without verification | `snyk-agent-scan inspect ./mcp.json` | no analysis call, no risk scores |
| Machine-readable output | `--json` | one JSON object keyed by config path |
| Audit another user's home | `--scan-all-users` | reads every home directory it can |
| MCP only, skip skill files | `--no-skills` | skills are scanned by default |
| Gate CI on findings | `--ci --dangerously-run-mcp-servers` | non-zero exit on risk or runtime failure |
| Push results to Snyk Evo | `snyk-agent-scan evo --push-key ...` | external service |
| Install runtime hooks | `snyk-agent-scan guard install` | modifies client configuration |

## Prerequisites

- `snyk-agent-scan help` prints `Snyk Agent Scan v0.6.9`. There is no `--version`; it exits with `unrecognized arguments`.
- Default state path is `~/.mcp-scan`; override with `--storage-file` to keep runs isolated.
- Default verification endpoint is `https://api.snyk.io/hidden/mcp-scan/analysis-machine?version=2026-07-10`. Any real scan sends entity descriptions there unless you pass `--analysis-url` pointing somewhere you control. Plan for that before the first run.
- Stdio servers are local subprocesses and are launched only after an interactive consent prompt, or without prompting when `--dangerously-run-mcp-servers` is set.
- Scanning is not read-only in the filesystem sense: skills are read in full, including any secrets in their scripts, before redaction and upload.
- Client discovery covers `claude code`, `claude desktop`, `cursor`, `vscode`, `windsurf`, `codex`, `gemini cli`, `amp`, `kiro`, `opencode`, `antigravity`, `amazon_q`, `openclaw`. Paths are per platform; a client that is not installed is simply absent.

## Core invocations

```sh
# 1. version and command surface
snyk-agent-scan help
snyk-agent-scan scan --help

# 2. default inventory: every known config on the host, rich text
snyk-agent-scan

# 3. one config file, results kept in an isolated state file
snyk-agent-scan scan --storage-file /tmp/agent-scan.db ./mcp.json

# 4. JSON for scripting, MCP servers only
snyk-agent-scan scan --json --no-skills --storage-file /tmp/agent-scan.db

# 5. inventory without contacting anything or uploading anything
snyk-agent-scan inspect --json ./mcp.json

# 6. target a client that is not in a default location
snyk-agent-scan scan ~/.config/some-agent/mcp.json

# 7. explicit consent for stdio servers during a rich-text scan
snyk-agent-scan scan --storage-file /tmp/agent-scan.db ./mcp.json
# prompts: Allow Agent Scan to start '<server>'? [y/N]

# 8. non-interactive run, which launches every discovered server
snyk-agent-scan scan --dangerously-run-mcp-servers --suppress-mcpserver-io true \
  --storage-file /tmp/agent-scan.db --json

# 9. bound the run: cap how long one hung server can stall it
snyk-agent-scan scan --server-timeout 20 \
  --storage-file /tmp/agent-scan.db --json --no-skills

# 10. audit every local user's agent surface (root or sudo)
snyk-agent-scan scan --scan-all-users --json --storage-file /tmp/all-users.db

# 11. keep full descriptions when a tool description looks like a payload
snyk-agent-scan scan --print-full-descriptions --json --storage-file /tmp/full.db

# 12. CI gate with an explicit ignore list
snyk-agent-scan scan --ci --dangerously-run-mcp-servers --json \
  --ignore-risks untrusted_content,destructive_capabilities \
  --storage-file /tmp/ci.db ./mcp.json
```

## Flags that matter

| Flag | Effect | Note |
| --- | --- | --- |
| `--storage-file` | state and result database | default `~/.mcp-scan` |
| `--analysis-url` | verification server | still one JSON API; version pinned to 2026-07-10 |
| `--verification-H` | extra header sent to the verifier | for a self-hosted endpoint with auth |
| `--json` | JSON instead of rich text | keyed by config path |
| `--skills` / `--no-skills` | scan skill directories too | enabled by default |
| `--scan-all-users` | every home directory | reads other users' agent configs and skills |
| `--dangerously-run-mcp-servers` | launch stdio servers without consent | the honest name: it runs third-party code |
| `--suppress-mcpserver-io` | hide server stderr | keeps noisy servers out of the report |
| `--server-timeout` | seconds per server | a hung server otherwise stalls the run |
| `--checks-per-server` | no-op | retained for backward compatibility; does not change behaviour |
| `--print-full-descriptions` | do not truncate descriptions | needed when triaging prompt-injection descriptions |
| `--ci` | non-zero exit on findings or failures | requires `--dangerously-run-mcp-servers` |
| `--ignore-risks` | comma list of risk names | see taxonomy below |
| `--ignore-failure-codes` | CI-only | rejected without `--ci` |
| `--config-file` | YAML defaults | CLI flags win |
| `--mcp-oauth-tokens-path` | OAuth token store | only needed for authenticated remote MCP |
| `--control-server`, `--control-server-H`, `--control-identifier` | report to Agent Monitor | multiple pairs allowed |
| `--push-key`, `--machine-id` | Snyk Evo push identity | prefer environment over argv |

**What it finds.**

- **MCP servers** from each client's config: transport (`stdio` or remote), command, args, env, and the tools, prompts and resources the server advertises.
- **Skills**: directories holding a `SKILL.md` (frontmatter must parse, with name and description) plus their scripts and assets. A flat `*.md` command file counts as a single-file skill.
- **Risk indexes** from the verification service. MCP server risks: `prompt_injection_tool_desc`, `untrusted_content`, `private_data`, `destructive_capabilities`. Skill risks: `prompt_injection_skill_instructions`, `suspicious_download_url`, `malicious_code`, `insecure_credential_handling`, `secret_detection`, `direct_money_access`, `third_party_content_exposure`, `unverifiable_dependencies`, `modifying_system_services`, `missing_skill_md`.
- **Runtime failures** as first-class results: a server that will not start, returns invalid JSON-RPC, or is declined by the operator is reported with an error category rather than silently ignored.

Triage order: `destructive_capabilities` and `malicious_code` first (the tool can delete or execute), then `prompt_injection_tool_desc` (the description is instruction-shaped and the agent will read it), then `private_data` and `secret_detection`. A hit is a question about the server, not proof of compromise: read the advertised description and the skill file before you act.

## Workflow

1. **Decide whether anything may leave the host.** If not, run `inspect` only, or point `--analysis-url` at an internal instance. A default scan uploads descriptions to Snyk.
2. **Take the inventory first.** `inspect --json` shows what exists, without consent prompts or verification. This is the map.
3. **Read the server list before allowing contact.** A stdio server is a command that will run with your privileges. Unknown binary plus `--dangerously-run-mcp-servers` is remote code execution by design.
4. **Run the verified scan on the subset you care about.** Pass explicit config paths, keep `--server-timeout` small, keep `--storage-file` per project.
5. **Keep one state file per project and compare the JSON between runs.** A new server, a new tool, or a rewritten tool description is the signal, not the absolute score.
6. **Triage by reachability.** A filesystem server under a project sandbox is different from one running as your user with `$HOME` in scope; record the actual filesystem and credential reach.
7. **Fix by removal or replacement.** Remove the config entry, or pin a known-good version; do not "ignore" a risk you cannot explain in `--ignore-risks`.

## OPSEC and telemetry

- A default `scan` transmits MCP server names, commands, tool and prompt descriptions to `api.snyk.io`. Redaction covers environment values, CLI argument values, headers, URL query parameters and traceback paths, and it is heuristic - a secret inside a tool description or a skill script is still sent.
- `--scan-all-users` reads other users' homes. On a shared host that is a privacy boundary and usually requires authorization.
- Launching stdio servers executes third-party code with your privileges; `--suppress-mcpserver-io` hides the output but not the execution.
- `guard install` rewrites agent client configuration to add hooks. Know how to `guard uninstall` before installing.
- `evo` and `--control-server` push results to external services with a push key; treat the key as a credential and keep it out of argv.
- Reports contain full command lines and skill file paths. Store them like evidence.

## Failure modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| `omp: error: unrecognized arguments: --version` | binary has no version flag | use `snyk-agent-scan help` |
| `scan --json` exits 1 with no stdout | verification endpoint unreachable or all servers failed | `--verbose --print-errors`, check `--analysis-url`, read stderr |
| Empty output on a valid config | nothing discovered or no risks to print | `--show-full-discovery`, re-check the path |
| `Skipped by user consent` in results | interactive prompt declined | rerun and answer `y`, or use `--dangerously-run-mcp-servers` deliberately |
| `Invalid JSON` JSON-RPC error for a server | the command is not an MCP server, or writes to stdout | point at the real server binary |
| `--ignore-failure-codes` rejected | used without `--ci` | add `--ci`, or drop the flag |
| Skills missing from results | `--no-skills` set, or no `SKILL.md` frontmatter | drop the flag, validate frontmatter |
| Run takes minutes | many servers, each awaiting its own timeout | lower `--server-timeout`, scan fewer paths |

## Verification

```sh
snyk-agent-scan help | head -3
# Snyk Agent Scan v0.6.9, then a blank line, then "usage: omp ..."

snyk-agent-scan inspect --json --skills ./mcp.json | head -20
# {"<path>": {"client": ..., "servers": [{"name": ..., "error": {...}}], "skills": []}}

snyk-agent-scan scan --help | grep -E 'storage-file|analysis-url|--ci'
# the flags above exist in this build
```

Evidence to keep: the storage file, the JSON output, the list of config paths scanned, and whether the run contacted a remote verifier.

## Related skills

- [agentic-radar](../agentic-radar/SKILL.md) for source-level review of an agent application
- [ai-security-testing](../ai-security-testing/SKILL.md) for the wider AI-target triage flow
- [garak](../garak/SKILL.md) when the finding needs behavioural confirmation against a model
- [model-file-audit](../model-file-audit/SKILL.md) when an agent ships a model artefact
