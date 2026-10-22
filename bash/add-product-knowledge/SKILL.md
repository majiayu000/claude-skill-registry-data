---
name: add-product-knowledge
model: claude-sonnet-5-5
category: context-indexing
description: Add a new entry to the product knowledge base. Wizard-guided — prompts for category, title, and content, then writes a structured markdown file and rebuilds the manifest.
argument-hint: "[title]"
userInvocable: true
allowed-tools: "Read, Write, Bash(source:*), Bash(echo:*), Bash(yq:*), Bash(jq:*), Bash(find:*), Bash(git:*), Bash(date:*), Bash(mkdir:*), Bash(rm:*), Bash(mv:*), Bash(mktemp:*), Bash(tr:*), Bash(sed:*), Bash(grep:*), Bash(awk:*), Bash(timeout:*), Bash(xargs:*), Bash(basename:*), Bash(sort:*), Bash(cd:*), AskUserQuestion, Bash(cat:*)"
---

# Add Product Knowledge

Add a new entry to the product knowledge base used by the `product-expert` agent.

## Purpose

Use this skill to capture product context mid-conversation — after a requirements session, after debugging a complex domain flow, or when you learn something about the product that should be preserved for future sessions.

The `product-expert` agent reads all `.md` files in the configured `product-knowledge` directory. This skill creates a properly-structured file and updates the manifest so the new entry is immediately searchable.

## Arguments

```bash
/add-product-knowledge                  # Full wizard
/add-product-knowledge Payment Flow     # Pre-fill title, wizard for rest
```

## Context

Arguments: $ARGUMENTS

---

## Configuration

```bash
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi

# STRICT, never resolve_artifact_typed. This skill WRITES into the product
# knowledge base, and the advisory resolver fabricates a path for an install
# that never configured one — an existing but empty directory, so the write
# would land somewhere nobody set up and the `-d` check below would happily
# pass. Same rule /archive-requirements gates on.
if _RESOLVED=$(resolve_artifact_strict product-knowledge .); then
  IFS='|' read -r KB_PATH _TYPE <<< "$_RESOLVED"
else
  _RC=$?
  case "$_RC" in
    2|3) echo "ERROR: no product knowledge base is configured for this project." >&2 ;;
    *)   echo "ERROR: the product-knowledge configuration is invalid (resolver exit $_RC) — see the message above." >&2 ;;
  esac
  exit 1
fi

# Configured, but not necessarily created yet. That is a different report from
# "not configured": the fix is a mkdir, not a configuration change.
if [[ ! -d "$KB_PATH" ]]; then
  echo "ERROR: knowledge base is configured but its directory does not exist: $KB_PATH" >&2
  exit 1
fi

# Echo them. Each bash block below is a SEPARATE Bash tool call and shell state
# does not survive between calls, so a value resolved here and not printed is
# invisible to every block that follows.
echo "KB_PATH=$KB_PATH"
echo "TYPE=$_TYPE"
```

**Shell state does not survive between Bash tool calls, so no block below may
read `$KB_PATH` or `$_TYPE` from this one.** Every later block writes them as
PLACEHOLDERS — `<KB_PATH printed above>` and `<TYPE printed above>` — which you
substitute with the literal values this block printed, before the command runs.
This is the same pattern `/rebuild-requirements-index` and the `product-expert`
agent use.

Why it matters: a `$KB_PATH` that is unset in a later call makes
`"$KB_PATH/{category}/$SLUG.md"` expand to `/{category}/$SLUG.md` — an absolute
path at the filesystem root, which is the same "write lands somewhere nobody
set up" failure the strict gate above exists to prevent, reintroduced one block
later.

> A `: "${KB_PATH:?…}"` guard is NOT the fix, and is worse than the bug: in a
> block where the variable was never set it fires every time, so every step
> after the gate aborts. And it cannot be combined with substitution either —
> `${/path/to/kb:?}` is a bad substitution, not a guarded literal. Substituting
> the value is what makes the block correct; there is no variable left to
> guard.

**Why strict here and advisory elsewhere.** `/load-context` and
`/rebuild-index` READ this artifact and keep the advisory resolver: an empty
default directory is a fine answer for a listing. Writing is different — a
write gated on a fabricated path puts content in a directory the project never
opted into. The split is by question, not by caller.

If the location type is `git`, sync before writing:

```bash
[ -n "<KB_PATH printed above>" ] || exit 1
git -C "<KB_PATH printed above>" pull --ff-only 2>/dev/null || true
```

The emptiness test is not optional: **`git -C ""` is a documented no-op**, so an
empty substitution would run `git pull` in whatever repository the session is
currently in — and `2>/dev/null || true` would hide it.

Run it **only when the printed `TYPE` is `git`**. Decide that from the Configuration
block's output, not from a shell test: `$_TYPE` is unset here, so
`[[ "$_TYPE" == "git" ]]` is always false and a git-backed KB would never be
pulled before the write — silently.

---

## Workflow

### Step 1: Resolve title

Parse `$ARGUMENTS`. If non-empty, treat the full string as the initial title suggestion.

If `$ARGUMENTS` is empty, use `AskUserQuestion`:

```
What do you want to document?
(e.g. "Payment Flow Architecture", "Auth Token Lifecycle", "Subscription Tier Rules")
```

Store as `{title}`.

### Step 2: Choose category

List existing categories (subdirectories of `$KB_PATH`):

```bash
find "<KB_PATH printed above>" -mindepth 1 -maxdepth 1 -type d -not -name '.*' \
  | xargs -I% basename % | sort
```

Use `AskUserQuestion` with up to 4 existing categories as options. The tool shows
no more than 4 and always adds its own free-text "Other" field, so do not spend a
slot on "other"; with more than 4 categories, name the rest in the question text:

> If the user picks "other" and types a category, it is free text like the
> title. Require `[a-z0-9-]` before it is used as a path component — reject
> anything else and ask again rather than sanitising silently, so the directory
> they get is the one they named.

```
Category for "{title}":
1. architecture
2. api
3. business-rules
4. data-models
(Other: type a category, existing or new)
```

Store as `{category}`. A name typed in the free-text field is the category.

### Step 3: Gather content

Use `AskUserQuestion`:

```
What should this entry document?

You can:
- Describe it in plain text (I'll structure it)
- Paste existing notes or diagrams
- Say "from conversation" to extract from our current discussion
```

Store as `{raw_content}`.

If the user says "from conversation", extract the most relevant product/domain insight from the current conversation context — focus on business rules, architecture patterns, API contracts, data models, or workflow states. Exclude code-level details (those belong to `archaeologist`).

### Step 4: Structure the content

Based on `{category}`, produce structured markdown using the appropriate template:

**architecture** — system components, integration patterns, service boundaries, data flow
**api** — endpoints, request/response shapes, auth requirements, rate limits
**business-rules** — domain logic, validation rules, workflow states, edge cases
**data-models** — entity definitions, field constraints, relationships, lifecycle
**other** — freeform with headings derived from the content

Keep it factual and cite evidence where possible. No speculation. If something is uncertain, mark it `*(unverified)*`.

### Step 5: Derive filename

**The title is free text the user typed, so it never reaches a command line.**
Write it to a file through a quoted heredoc — the quoted delimiter disables
every expansion inside it, so `$( )`, backticks and quotes pass through as inert
characters — then slugify the FILE:

```bash
mkdir -p -m 700 "$HOME/.claude/tmp"
cat > "$HOME/.claude/tmp/pk-title.txt" <<'PK_TITLE_EOF'
{title}
PK_TITLE_EOF
SLUG=$(tr '[:upper:]' '[:lower:]' < "$HOME/.claude/tmp/pk-title.txt" | tr '\n' '-' | sed 's/[^a-z0-9]/-/g; s/--*/-/g; s/^-//; s/-$//')
rm -f "$HOME/.claude/tmp/pk-title.txt"
echo "SLUG=$SLUG"
```

> The `rm -f` matches what the category block below already does. The file
> lives at a fixed name in a shared `$HOME/.claude/tmp`, so one left behind is
> the title the *next* run slugifies should that run's write fail — a silent
> wrong answer rather than an error. It is deleted after the slugify reads it,
> not before.

> Never build the slug as `SLUG=$(echo "{title}" | …)`. Substituted into a
> double-quoted string, a title of `a";id;"` closes the quote and runs `id`; one
> containing `$(…)` or backticks is executed by the very command substitution
> that was supposed to be slugifying it. The heredoc delimiter is quoted for
> exactly that reason and must stay quoted.

> The `tr '\n' '-'` is load-bearing: `sed` works a line at a time, so a title
> pasted across two lines would otherwise produce a SLUG containing a newline.
> Everything downstream treats the slug as `[a-z0-9-]` by construction — it is
> substituted into paths and branch names on that basis — so it has to be
> single-line by construction too, not merely usually.
>
> `$SLUG` comes out restricted to `[a-z0-9-]`, which is what makes it safe to
> substitute below — and why the slug, never the title, is what later blocks
> carry.

`$SLUG` does not survive this block either — read it from the output and
substitute it, exactly like `KB_PATH`. The destination path is therefore
derived **inside** each block that needs it, never carried across:

**VALIDATION** — `{category}` becomes a directory name and is the one value here
constrained by prose alone: the user may type a new one when they pick "other".
`{slug}` is `[a-z0-9-]` because it was slugified and `KB_PATH` is
resolver-checked, but nothing has checked this.

It cannot be validated where it is used. `case "{category}" in` puts the free
text on a command line to test it — a category of `a";id;"` closes the quote and
runs `id` before the `case` is ever evaluated. Validating a value by
substituting it is the same defect as using it. So it goes through a file like
every other free-text value here, is checked there, and only the CHECKED value
travels onward:

```bash
mkdir -p -m 700 "$HOME/.claude/tmp"
cat > "$HOME/.claude/tmp/pk-category.txt" <<'PK_CAT_EOF'
{category}
PK_CAT_EOF
CATEGORY="$(cat "$HOME/.claude/tmp/pk-category.txt")"
rm -f "$HOME/.claude/tmp/pk-category.txt"

# LC_ALL=C: [!a-z0-9-] is collation-dependent, and under some locales uppercase
# falls inside the range and passes.
case "$(LC_ALL=C printf '%s' "$CATEGORY")" in
  *[!abcdefghijklmnopqrstuvwxyz0123456789-]*|''|-*|*-)
    echo "ERROR: unsafe category — expected kebab-case [a-z0-9-], no slashes or dots" >&2
    exit 1 ;;
esac
echo "CATEGORY=$CATEGORY"
```

Every later block substitutes `<CATEGORY printed above>`, which is now a checked
value, exactly as it does for `KB_PATH` and `SLUG`. `{category}` itself must not
appear in a command again.

```bash
DEST="<KB_PATH printed above>/<CATEGORY printed above>/<SLUG printed above>.md"
if [[ -f "$DEST" ]]; then
  # Show the user what's there and ask: overwrite, rename, or cancel
  echo "EXISTS: $DEST"
fi
```

### Step 6: Write the file

Write `<KB_PATH printed above>/<CATEGORY printed above>/<SLUG printed above>.md` with this
structure (`$DEST` was defined in an earlier block and does not survive to
here):

```markdown
---
tags: [{derived tags}]
---

# {title}

{structured content}
```

Tags are inferred from the title and content — use 3–6 short lowercase terms.

Create the category directory if it doesn't exist:

```bash
# A wrong or missing substitution must fail here: an empty KB_PATH makes
# this create a category directory next to `/`, which succeeds silently.
[ -n "<KB_PATH printed above>" ] && [ -d "<KB_PATH printed above>" ] || exit 1
mkdir -p "<KB_PATH printed above>/<CATEGORY printed above>"
```

### Step 7: Rebuild manifest

Invalidate the manifest so `product-expert` picks up the new file immediately:

```bash
MANIFEST="<KB_PATH printed above>/manifest.json"
if [[ -f "$MANIFEST" ]]; then
  # Touch last_updated to force product-expert to rebuild on next read
  _TMP=$(mktemp) && jq '.last_updated = "1970-01-01T00:00:00Z"' "$MANIFEST" > "$_TMP" \
    && mv "$_TMP" "$MANIFEST"
fi
```

### Step 8: Commit (git locations only)

If the `TYPE` printed by the Configuration block is `git`, follow the sanctioned KB-write
pattern in full:
[`${CLAUDE_PLUGIN_ROOT}/shared/kb-write-pattern.md`](../../shared/kb-write-pattern.md).
**Both** `git commit` (Call 2) and `git push` (Call 3) must **lead their own
Bash tool calls** so the guard engages — for the push that means resolving the
branch inline in the push argument, on one line, since shell variables do not
survive across Bash tool calls. Prefix the push with `NEXUS_KB_WRITE=1
SECURITY_AUDITOR_BYPASS=1` (both logged to stderr — that WARN is the tripwire);
do **not** call `record-audit.sh`:

```bash
# Call 1 — stage. Every path is a literal substituted from earlier output;
# DEST and MANIFEST were derived in their own blocks and do not survive to here.
[ -n "<KB_PATH printed above>" ] || exit 1
cd "<KB_PATH printed above>" || exit 1
git add -- "<CATEGORY printed above>/<SLUG printed above>.md"
# Only if it exists: `git add` aborts on an unmatched pathspec and stages
# NOTHING, so naming an absent manifest.json would silently drop the new file
# from the commit. An `if` block, not `[ -f … ] && …`: that form is the last
# command here, so on the first entry ever added — when no manifest exists yet
# — the test is false and the whole call exits 1.
if [ -f manifest.json ]; then
  git add -- manifest.json
fi
```
The commit subject carries the user's title, so it goes through a quoted
heredoc too — `-m "…{title}…"` would put free text back on a command line:

```bash
mkdir -p -m 700 "$HOME/.claude/tmp"
cat > "$HOME/.claude/tmp/pk-commit-msg.txt" <<'PK_MSG_EOF'
docs(product-knowledge): add {title}
PK_MSG_EOF
```

> Call 2 — commit leads the call (credential scan).

```bash
git commit -F "$HOME/.claude/tmp/pk-commit-msg.txt" && rm -f "$HOME/.claude/tmp/pk-commit-msg.txt"
```

**Anchor and verify the working directory before the push.** The push leads its
own call and therefore carries no `cd`, so it inherits whatever cwd is current —
and there is a user pause between these calls. A drifted cwd sends a
double-bypass push at the user's own repository, with branch protection AND the
audit gate disabled. The pattern above requires this call:

```bash
[ -n "<KB_PATH printed above>" ] || exit 1
cd "<KB_PATH printed above>" || exit 1
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 1
```

> Call 3 — push must lead, on ONE line, so the guard engages and logs the bypass WARNs.

```bash
NEXUS_KB_WRITE=1 SECURITY_AUDITOR_BYPASS=1 git push origin -- "$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' | grep . || timeout 10 git ls-remote --symref origin HEAD 2>/dev/null | awk '/^ref:/{sub("refs/heads/","",$(2));print $(2);exit}' | grep . || echo master)"
```

### Step 9: Confirm

```
✓ Knowledge base entry created

  File:     {category}/{slug}.md
  Title:    {title}
  Tags:     {tags}
  Location: <KB_PATH printed above>/<CATEGORY printed above>/<SLUG printed above>.md

The product-expert agent will pick this up on the next invocation.
Run /rebuild-index product-knowledge to rebuild the full manifest now.
```
