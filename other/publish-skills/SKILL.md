---
name: publish-skills
license: MIT
description: Publish agent skills AND MCP servers to every marketplace, plugin directory, and registry — security-scan for private data, validate with `gh skill`, cut a release, wire the Claude /plugin and Codex marketplaces, publish an MCP server to the official MCP Registry (mcp-publisher + server.json), and prep the curated / monetized stores (Buda Marketplace, Agensi, OpenClaw ClawHub) and review-gated directories (ChatGPT App Directory, Anthropic Connectors + Desktop Extensions/.mcpb). Use when the user wants to publish, release, list, 上架, or distribute agent skills, plugins, or MCP servers to skills.sh / SkillsMP / Claude Code / Codex / the MCP Registry.
disable-model-invocation: false
allowed-tools: Bash(gh:*), Bash(git:*), Bash(python3:*), Bash(unzip:*), Bash(mcp-publisher:*), Bash(mcpb:*), Bash(codex:*), Bash(brew:*), Read, Write, Edit, Grep, Glob
user-invocable: true
metadata:
  category: platform
  tags:
    - risk:gated-write
    - surface:github
---

# Publish Skills

Publish a repo of agent skills (the open `SKILL.md` format) to the agent-skills marketplaces. The repo is the unit of publishing: make it public, validate, cut a release, and the auto-indexers (skills.sh, SkillsMP, claudeskills.info) pick it up. Then optionally wire the Claude `/plugin` marketplace and submit to the curated stores.

**Golden rule: security first.** These repos often carry a local App-in-Skill with real data (emails, ledgers, tokens). Never publish it. Confirm private data is gitignored and scan tracked files before anything goes public.

Run steps in order. Stop and surface anything a step can't resolve safely.

---

## Step 1 — Security scan (blocking)

Publishing is outward-facing and hard to reverse. Verify BEFORE any push/release.

```bash
# 1a. Private runtime state must be gitignored, never tracked
grep -nE '\.data/|\.cache/|config\.local|\.env|exports/' .gitignore    # expect these ignored
git ls-files | grep -iE '\.data/|\.cache/|config\.local|\.env|\.pem|\.key' && echo "!!! TRACKED PRIVATE FILE — stop" || echo "clean: no private files tracked"

# 1b. Scan tracked files for real secrets / PII (tune patterns per repo)
git ls-files | while read f; do
  grep -HnaiE '(sk_live|sk_test|pk_live|bearer [A-Za-z0-9]|-----BEGIN|api[_-]?key["'"'"' :=]+[A-Za-z0-9]{16})' "$f" 2>/dev/null
done | grep -vE 'example\.com|_env"|password_env|api_key_env|REPLACE_WITH' | head
```

- Config templates must use `example.com`, `Your Name`, and `*_env` references — never real hosts, addresses, or key values.
- Third-party skills the user installed (e.g. a tracked `.agents/skills/<other>/`) must NOT be republished — untrack + gitignore them:
  `git rm -r --cached .agents && printf '\n.agents/skills/\n' >> .gitignore`

Only proceed when 1a and 1b are clean.

## Step 2 — Validate & fix (`gh skill`)

GitHub's official tooling validates against the agentskills.io spec and discovers `skills/*/SKILL.md`, `*/SKILL.md`, and `plugins/{scope}/skills/*/SKILL.md`.

```bash
gh skill publish --dry-run          # validates ALL skills; one error blocks the whole release
```

Common fixes:
- **Invalid frontmatter YAML** (`mapping values are not allowed…`): a description contains an unquoted `colon: space`. Wrap the whole `description` value in double quotes.
- **name ≠ directory name**: rename so `name:` matches the folder.
- **Missing `license`**: add a root `LICENSE` (MIT is typical) and `license: MIT` to each skill's frontmatter.
- **Body > 500 lines** (context-efficiency warning): move large blocks (JSON schemas, long examples) into `references/*.md` and leave a one-line pointer.
- **Install metadata present** (`metadata.github-*`): `gh skill publish --fix` strips it; review, then commit.

Re-run `--dry-run` until it prints `ok` (a lone tag-protection warning is fine here — handled in Step 5).

## Step 3 — Publish (public repo + release)

```bash
# Ensure the repo is public (auto-indexers only see public repos)
gh repo view <owner>/<repo> --json visibility,isPrivate

# Discovery topics — feed SkillsMP / claudeskills.info / GitHub search
gh repo edit <owner>/<repo> --add-topic agent-skills --add-topic claude-skills \
  --add-topic codex-skills --add-topic skill-md --add-topic ai-agents

# Commit any pending clean changes, then cut a release
git add -A && git commit -m "Publish skills" && git push
gh skill publish --tag vX.Y.Z        # creates the GitHub release the ecosystem recognizes
```

After this: `npx skills add <owner>/<repo>` and `gh skill install <owner>/<repo>` both work; `gh skill search <name>` confirms indexing (may take minutes-to-days).

## Step 4 — Claude Code `/plugin` marketplace

Expose the same skills to Anthropic's `/plugin` system WITHOUT restructuring the flat `skills/*/` layout: one bundle plugin whose `source` is the repo root and whose `skills` array points at each skill dir (`strict: false`). Write `.claude-plugin/marketplace.json`:

```json
{
  "name": "<owner>-skills",
  "owner": { "name": "<Full Name>", "url": "https://github.com/<owner>" },
  "metadata": { "description": "…", "version": "X.Y.Z" },
  "plugins": [
    {
      "name": "<owner>-skills",
      "description": "…",
      "version": "X.Y.Z",
      "license": "MIT",
      "category": "productivity",
      "tags": ["agent-skills"],
      "source": "./",
      "strict": false,
      "skills": ["./skills/skill-a", "./skills/skill-b"]
    }
  ]
}
```

Validate JSON, then document in the README:
```
/plugin marketplace add <owner>/<repo>
/plugin install <owner>-skills
```
Keep the plugin `name` stable across releases so existing users don't break. This adds only the manifest — it does not create a `plugins/` dir, so it won't collide with `gh skill` discovery.

## Step 5 — Tag protection (immutable releases)

Marketplaces trust releases that can't be rewritten. Create a ruleset targeting tags with **Restrict updates + Restrict deletions** (GitHub UI: Settings › Rules › Rulesets › New ruleset → Target: Tags → pattern `v*`). Verify:

```bash
gh api repos/<owner>/<repo>/rulesets --jq '.[] | "\(.name): \(.enforcement) [\(.target)]"'   # want: active [tag]
gh skill publish --dry-run    # the tag-protection warning should be gone (prints `ok`)
```

Enforcement must be **active** (a disabled ruleset still warns).

## Step 6 — Curated / manual marketplaces (need the user's login)

These can't be fully automated — prepare the artifacts, hand off the click.

**Agensi** (agensi.io, curated, ~70% creator revenue): build a clean zip per skill from tracked files only (never the working tree — avoids private `.data/`):
```bash
mkdir -p dist/agensi
git archive --format=zip --prefix=<skill>/ -o dist/agensi/<skill>.zip HEAD:skills/<skill>
unzip -Z1 dist/agensi/<skill>.zip | grep -iE '\.data/|\.cache/|\.env' && echo "!!! sensitive" || echo clean
```
Then the user: sign up → connect Stripe Connect → Creator Dashboard → Submit a Skill → upload zip → price → passes 8-point security scan.

**Buda Marketplace** ([buda.im/docs/sell-skills](https://buda.im/docs/sell-skills), monetized, GitHub-App based — no zip, reads the repo directly). Uses this repo's existing `skills/*/SKILL.md` layout as-is (also lists `agents/*/AGENTS.md` and `teams/*/TEAM.md`); each `SKILL.md` needs only `name` + `description` frontmatter, which become the listing. The user:
1. Developer Portal → **Plugin Repos** → **Connect GitHub** → install the Buda GitHub App, granting the repo (private is fine; Buda asks only `Contents: Read-only` and never stores source).
2. **Add Repository** → pick from dropdown → Buda scans and populates **My Listings** as `pending`.
3. Per listing set **Pricing tier** (free / one-time / subscription) and the **Publish** toggle.
4. Review is brief — usually approved within ~24h (`pending` → `published`). Push changes, then click **Sync** to update all listings; users get the latest on next install. Payouts are monthly, less Buda's platform fee.

**OpenClaw ClawHub** (clawhub.ai): community listing — submit the public repo URL.

**Codex / OpenAI** (`openai/plugins`, curated, PR-based): the old `openai/skills` is deprecated. Fork `openai/plugins`, add `plugins/<name>/.codex-plugin/plugin.json` + `skills/<name>/SKILL.md` (match an existing plugin's manifest, e.g. `build-web-apps`), push a branch to the fork. **OpenAI restricts PR creation from external accounts** (GraphQL/REST 403→404), so don't try to open it programmatically — hand the user a one-click compare URL:
`https://github.com/openai/plugins/compare/main...<owner>:plugins:<branch>?expand=1`

## Step 7 — MCP servers → registries & directories (only if you ship an MCP server)

Steps 1-6 publish a **SKILL.md repo**. If what you're shipping also exposes an **MCP server** (e.g. an
app's `/api/mcp`), it has its own channels. [`busabase/skills`](https://github.com/busabase/skills) is
the reference — one repo feeds `skills` + Claude Code + Codex marketplaces **+ the MCP Registry**.
Templates (`server.json`, `.mcp.json`, `.codex-plugin/plugin.json`, `.mcpb` manifest) and the full
per-channel review checklists live in [`references/mcp-and-directories.md`](./references/mcp-and-directories.md).

**Zero-review — do now:**

- **Official MCP Registry** (`registry.modelcontextprotocol.io`) — a metadata catalog pointing at your
  hosted server/package. Add a `server.json`, then:
  ```bash
  brew install mcp-publisher
  mcp-publisher login github        # → io.github.<user>/*   (own the repo)
  # or: mcp-publisher login dns --domain <domain> --private-key <KEY>   # → com.<domain>/*
  mcp-publisher publish             # validates + publishes; live instantly, reactive moderation only
  ```
  Versions are immutable — bump `version` to update. Automate on `v*` tags with `login github-oidc`.
- **Codex marketplace** — `codex plugin marketplace add <owner>/<repo>` (self-serve, zero-review; an
  alternative to the `openai/plugins` PR route in Step 6). **Verified layout (Codex is strict):** the
  marketplace file must be `.agents/plugins/marketplace.json`, and each plugin a **subdir**
  `plugins/<name>/` (`source.path: "./plugins/<name>"`) holding its own `.codex-plugin/plugin.json`
  (`"skills": "./skills/"`). On install Codex bundles **only files inside the plugin subdir** — symlinks
  and `../` escapes are silently dropped — so the skill must be a **real copy** at
  `plugins/<name>/skills/<name>/SKILL.md`, synced from the canonical `skills/<name>/`. A root-level
  `marketplace.json` or root `.codex-plugin/` does **not** resolve. (Codex `.mcp.json` also differs from
  Claude Code's — see below.) Full templates in the references file.
- **Claude Code** — already wired in Step 4; its `/plugin` also carries a bundled MCP via `.mcp.json`.

**Review-gated — second wave** (worth it once the product has a public HTTPS MCP server + OAuth + a
privacy policy). Prep the checklist in the references file, then hand off the submit:

- **ChatGPT App Directory** (Apps SDK) — MCP-server-as-app; identity verification + working demo login
  with sample data (signup-to-test = rejected) + stability. Submit in the OpenAI Developer Platform.
- **Anthropic Connectors directory** — remote MCP; Team/Enterprise org, 11-step form, privacy policy
  mandatory (missing = instant reject), must own the API/domain, tools need `readOnlyHint`/`destructiveHint`.
- **Anthropic Desktop Extensions** — `.mcpb` bundle (`mcpb init` → `mcpb pack`), test on Windows + macOS.

## Distribution cheat-sheet

| Channel | Artifact | Gate | Command / action |
| --- | --- | --- | --- |
| GitHub skill index | SKILL.md repo | none | `gh skill search <name>` |
| skills.sh / SkillsMP / claudeskills.info | SKILL.md repo | none | `npx skills add <owner>/<repo>` |
| Claude Code `/plugin` | `.claude-plugin/marketplace.json` | none | `/plugin marketplace add <owner>/<repo>` |
| Codex marketplace | `.agents/plugins/marketplace.json` + `plugins/<name>/` | none | `codex plugin marketplace add <owner>/<repo>` |
| Official MCP Registry | `server.json` | none (ownership proof) | `mcp-publisher publish` |
| Agensi | zip | 8-point scan | `dist/agensi/*.zip` + Stripe |
| Buda Marketplace | `skills/*/SKILL.md` repo | ~24h review | connect GitHub App → set pricing → publish |
| OpenClaw ClawHub | plugin/repo | review (hidden until verified) | repo URL |
| Codex / OpenAI curated | fork + PR | curated | compare URL (user opens) |
| ChatGPT App Directory | MCP server | **hard human review** | OpenAI Developer Platform |
| Anthropic Connectors | remote MCP | **hard human review** | submission form |
| Anthropic Desktop Extensions | `.mcpb` | human review | `mcpb pack` + form |

## Notes

- The whole repo publishes together — `gh skill publish` fails if ANY skill has an error, so keep every skill valid.
- Bump the release tag on every publish so indexers and `/plugin` users get the update.
- This skill can publish the repo it lives in (dogfood): run Steps 1-5 against `<owner>/<repo>` = this repo.
- Steps 1-6 are the SKILL.md-repo track; Step 7 is a separate MCP-server track — do it only when an MCP server is part of what you ship. The four zero-review channels (skills index, Claude Code, Codex, MCP Registry) ship today; the human-reviewed directories are a deliberate second wave.
- **Never hand-maintain the Codex skill copy.** The canonical skill is `skills/<name>/`; the Codex
  `plugins/<name>/skills/<name>/` is *build output* (Codex can't symlink/`../`-escape). Wire
  `scripts/sync-codex-plugins.sh` as a pre-commit hook (+ optional CI drift check) so the copy
  regenerates from canonical and can never go stale — script + hook in the references file.
