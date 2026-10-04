---
name: doc-spec
description: Store a feature spec.md in the central spec registry (default ~/.claude/spec-registry/<service>/, override with $CLAUDE_DOC_HOME for team-shared registries), or list the specs registered for the current repo's service. For vibe-coding / standalone flows where the SDD pipeline's /sdd:mr did not publish a spec. Run `/sdd:doc-spec <path>` to store a spec file, or `/sdd:doc-spec list` to inspect this service's specs.
argument-hint: "[path-to-spec.md | list]"
allowed-tools: Read, Bash(cp:*), Bash(mkdir:*), Bash(ls:*), Bash(find:*), Bash(git rev-parse:*), Bash(git branch:*), Bash(test:*), Bash(grep:*), Bash(head:*), Bash(sed:*), Bash(tr:*), Bash(basename:*)
---

# Spec Registry


---

## Why this exists

In the SDD pipeline, `/sdd:mr` already publishes the feature spec to the registry
(it calls `spec-publish.sh` when a `.specwork/_spec/<slug>-spec.md` exists). This
skill is the **standalone / vibe-coding** counterpart: when you wrote a spec by
hand (or outside the pipeline) and never ran `/sdd:mr`, `/sdd:doc-spec` pushes that
file into the same registry so `/sdd:doc-spec-query` can read it.

Authoring a spec is still the SDD pipeline command `/sdd:spec`. `doc-spec` is only the
**registry side** of the spec lifecycle: it takes an existing `spec.md` and stores it,
the counterpart to `/sdd:doc-spec-query` reading it back.

It is a **store-only** wrapper — it does not generate a spec from your diff. The
file you point at is copied verbatim. For best `/sdd:doc-spec-query` results the spec
should follow the canonical SDD sections (`## Summary`, `## Behavior`, `## Scope`,
`## Implementation Context`, `## Safe Constraints`, `## Open Questions`), but this
skill never rewrites or enforces them.

---

## Modes

| Invocation | Action |
|------------|--------|
| `/sdd:doc-spec <path>` | **Store mode** — copy the given spec file into `spec-registry/<service>/`. |
| `/sdd:doc-spec` (no arg) | **Auto-detect** — store the active pipeline spec (`.specwork/_spec/<slug>-spec.md` for the current branch) if one exists; otherwise stop with usage. |
| `/sdd:doc-spec list` | **List mode** — print the specs registered for the current repo's service. Read-only. |

Reject any other argument with a usage message.

---

## Registry Path

All registry I/O resolves through a single environment variable, exactly like
`/sdd:doc-catalog`, `/sdd:doc-adr`, and `/sdd:doc-spec-query`:

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/spec-registry"
```

- **Default** (no env var set): `~/.claude/spec-registry/`.
- **Override**: `export CLAUDE_DOC_HOME=/path/to/registry-root` — e.g. a cloned
  GitLab repo for team-shared specs. The skill writes/reads under
  `$CLAUDE_DOC_HOME/spec-registry/`.

Specs are keyed by service exactly like ADRs:
`spec-registry/<service>/<slug>-spec.md`. The `<service>` key is derived the same
way `/sdd:doc-catalog` and `/sdd:doc-adr` derive it, so the `spec-registry/<service>/`
key lines up with `adr-registry/<service>/`.

---

## List Mode

Run when the argument is `list`. This is **scoped to the current repo's service** — it
prints only that service's specs and exits before any store logic runs. (To ask
questions across every service, use `/sdd:doc-spec-query`.)

1. Detect the service the same way Store Mode does (see Step 2): `spring.application.name`
   → `docs/service-info.md` heading → git repo basename, lowercased.
2. List that service's specs:

```bash
SERVICE="<detected-service>"
DIR="${CLAUDE_DOC_HOME:-$HOME/.claude}/spec-registry/$SERVICE"

if [ ! -d "$DIR" ] || ! ls "$DIR"/*-spec.md >/dev/null 2>&1; then
  echo "No specs registered for $SERVICE."
  echo "Store one with /sdd:doc-spec <path>, or run the SDD pipeline through /sdd:mr."
  exit 0
fi

echo "Specs for $SERVICE in $DIR:"
for spec in "$DIR"/*-spec.md; do
  echo "  $(basename "$spec")"
done
```

After listing, exit. Do not proceed to the store steps below.

---

## Store Mode

| Step | Action |
|------|--------|
| 1 | Resolve the spec file to store (argument path, or auto-detect) |
| 2 | Detect the service name (same order as `/sdd:doc-catalog`) |
| 3 | Normalize the destination filename to end in `-spec.md` |
| 4 | Copy into `spec-registry/<service>/` |
| 5 | Confirm, and remind about canonical structure for `/sdd:doc-spec-query` |

### Step 1 — Resolve the spec file

- **Argument given**: treat `$ARGUMENTS` as a path. If the file does not exist,
  stop:

  ```
  Spec file not found: <path>
  Pass the path to a spec markdown file: /sdd:doc-spec docs/my-feature-spec.md
  ```

- **No argument**: look for an active pipeline spec for the current branch:

  ```bash
  BRANCH="$(git branch --show-current)"
  SPEC="$(find .specwork/_spec -name "*-spec.md" -type f 2>/dev/null | head -1)"
  ```

  If found, use it. If not, stop with usage (do not guess at random files):

  ```
  Nothing to publish. Pass a spec file path:

    /sdd:doc-spec docs/my-feature-spec.md

  Or run this from a project with an active SDD pipeline (.specwork/_spec/).
  ```

### Step 2 — Detect the service name

Try in order (first hit wins) — the **same order** `/sdd:doc-catalog`, `/sdd:doc-adr`,
and `spec-publish.sh` use, so the service-catalog, adr-registry, and spec-registry
all agree on one key per service:

1. `spring.application.name` from `src/main/resources/application.yml` /
   `.yaml` (or `application.properties`) — authoritative for Spring services.
2. the first `# <ServiceName>` heading of `docs/service-info.md` (kebab-cased).
3. git repo basename:
   ```bash
   git rev-parse --show-toplevel | xargs basename
   ```

Lowercase the result to kebab-case. If nothing resolves, use `unknown`.

### Step 3 — Normalize the destination filename

`/sdd:doc-spec-query` only discovers files matching `*-spec.md`, so the destination name
**must** end in `-spec.md`:

- If the source basename already matches `*-spec.md`, keep it.
- Otherwise derive a slug and append `-spec.md`:
  - Prefer the current branch name with its type prefix stripped
    (`feature/payment-retry` → `payment-retry`).
  - Else use the source basename without its extension.
  - A bare `spec.md` must not become `spec-spec.md` — fall back to the branch
    slug, or ask the user for a slug if neither a branch nor a meaningful
    basename is available.

Result: `DEST_NAME="<slug>-spec.md"`.

### Step 4 — Copy

```bash
REGISTRY="${CLAUDE_DOC_HOME:-$HOME/.claude}/spec-registry"
DEST="$REGISTRY/<service>"
mkdir -p "$DEST"
cp "<spec-file>" "$DEST/<DEST_NAME>"
```

This is a plain copy into the local-or-shared registry. It does **not** commit
anything to the project repo.

### Step 5 — Confirm

After the copy succeeds, list the specs now registered for that service so the
user sees the result:

```bash
ls -1 "$DEST"/*-spec.md 2>/dev/null | xargs -n1 basename | sort
```

Then print:

```text
Published: <spec-file> → ~/.claude/spec-registry/<service>/<DEST_NAME>

<service> now has:
  <slug-a>-spec.md
  <slug-b>-spec.md

Run /sdd:doc-spec-query to ask feature/spec questions across services.
```

If the published spec is missing canonical sections, add a one-line note (do not
fail): "Tip: `/sdd:doc-spec-query` reads `## Summary`, `## Behavior`, `## Scope`,
`## Safe Constraints`, and `## Open Questions` — add them for richer answers."

---

## Rules

- Store-only — never generate or rewrite the spec; copy it verbatim.
- Never commit anything to the project repo (it is a `cp` into the registry).
- Destination filename must end in `-spec.md` or `/sdd:doc-spec-query` will not find it.
- The `<service>` key must match `/sdd:doc-catalog` / `/sdd:doc-adr` so all registries align.

---

## Related Skills

- `doc-spec-query` — reads every spec in the registry and answers cross-service questions
- `mr` (sdd bundle) — publishes the pipeline spec automatically after creating the MR
- `spec` (sdd bundle) — authors the `spec.md` this registry stores
- `doc-catalog` / `doc-adr` — same create-and-store pattern for catalogs and ADRs
