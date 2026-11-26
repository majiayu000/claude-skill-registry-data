---
name: claude-md-from-profile
description: Generates the project's CLAUDE.md block FROM operator-profile.yaml - floor first (what the AI does not decide), then where things live, the rules of done and the flow. Idempotent, signed; refuses to overwrite a hand-edited block
---

> **Auto-Trigger:** When creating or changing `operator-profile.yaml`; when opening a project that has a profile and no CLAUDE.md; when a project's AI ignores a gate the profile declares
> **Keywords:** "claude.md", "generate claude.md", "project instructions", "operator profile", "operator-profile", "floor", "what the AI does not decide", "regenerate block", "signature"
> **Priority:** HIGH
> **Tools:** Bash, Read
> **Related doctrine:** `rules/partial-autonomy-slider.md` (the HOW MUCH axis - `autonomy.by_action`), `rules/gateguard.md` (protected paths, blocked families), `rules/verification-before-completion.md` (the rules of done).

# claude-md-from-profile - CLAUDE.md is born from the profile, not the other way round

`operator-profile.yaml` already says everything that matters: which action is level 0, which
path is protected, which command family is blocked, where the inbox and the logs live, what
"done" requires. But the profile is read by **hooks and scripts** - the AI that opens the project
reads **CLAUDE.md**. Without this skill the two diverge in silence: the hook blocks what
CLAUDE.md never said was forbidden, and the AI learns to work around the gate instead of
respecting it.

This skill generates a **marked block** inside CLAUDE.md, with the floor in the first section.
What the person wrote outside the markers is never touched.

## When NOT to Activate
- The project has no `operator-profile.yaml` - create the profile first (`cp profile.example.yaml operator-profile.yaml`). The script refuses to generate from a profile that does not exist, and there is no hidden default.
- You want to write prose in CLAUDE.md - write it **outside** the markers; inside them the content is derived and will be regenerated.
- The block was hand-edited on purpose and you have not yet decided whether the edit goes to the profile - settle that first; `--force` erases the edit.

## Contract

**INPUT:** an `operator-profile.yaml` (found from the cwd, via `OPERATOR_PROFILE=`, or via `--profile`). No key is mandatory - a section without data is omitted, not invented.

**OUTPUT:** a block `<!-- operator-kit:claude-md:begin -->` … `<!-- operator-kit:claude-md:end -->` written to `./CLAUDE.md` (or `--out`). The last line of the block is the **signature** (profile hash + date). The example profile generates the block with a warning on the first line.

**EXIT CODES**

| Exit | Meaning |
|---|---|
| 0 | block written (new/replaced) or **no-op** - CLAUDE.md was already up to date with the profile |
| 1 | the existing block was **hand-edited** (signature does not match). Nothing written. See the diff with `--dry-run`; to overwrite, `--force` |
| 2 | usage or invalid profile: no profile found, unreadable YAML, PyYAML missing, unknown flag |
| 3 | the machine refused to write `CLAUDE.md` - the whole content is in `INSTRUCOES-DO-CLAUDE.md` next to it; rename it |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `operator-profile.yaml` | Reads | the single source of the block |
| `CLAUDE.md` (or `--out`) | Writes - **only between the markers** | the generated block; text outside the markers is preserved byte for byte |
| `INSTRUCOES-DO-CLAUDE.md` | Writes (only on exit 3) | fallback when writing to `CLAUDE.md` is refused |

## Process
1. **See what would come out** before writing - `--dry-run` prints the whole block to stdout and touches nothing.
2. **Generate** at the project root: `python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_md_from_profile.py"`. If CLAUDE.md already exists, the block goes at the **top**, before the person's text.
3. **Read the floor** that came out (`## WHAT YOU DO NOT DECIDE`). If something there is wrong, the fix is **in the profile**, never in the block - regenerate afterwards.
4. **Put it in the project setup** (SessionStart hook, `make setup`, whatever exists): running it again is cheap and idempotent - exit 0 with `no-op` when nothing changed.
5. **On exit 1**, someone hand-edited the block. Compare with `--dry-run`, carry what is worth keeping into the profile, and only then `--force`.

## Executed examples

The four below were really run (2026-09-22) in a temporary directory with
`profile.example.yaml` copied as `operator-profile.yaml` - zero effect on a real
project. The output is the real one.

**1 · First generation - CLAUDE.md is born:**

```
$ python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_md_from_profile.py"
claude_md_from_profile: block new in CLAUDE.md (source: operator-profile.yaml)
$ echo $?
0
```
<!-- executed: 2026-09-22 · exit=0 -->

The block starts with the floor, and the floor comes from the profile, key by key - each line
says where it came from:

```
## WHAT YOU DO NOT DECIDE
- **rm_live_code**: level 0 (`autonomy.by_action.rm_live_code`). You PROPOSE, you do not execute. The person authorises.
- Any write to `settings*.json` falls into an automatic human gate (`autonomy.sensitive_paths_auto_gate`). Do not route around it.
- `src/**` is protected (`guardrails.protected_paths`): do not delete, do not move, do not mass-rewrite.
- Branch `main` is protected (`guardrails.protected_branches`): never push directly, never force.
- The command family **git-push-force** is BLOCKED (`guardrails.block_families`). Urgency is not an exception.
```

**2 · Run again without changing anything - the idempotence proof:**

```
$ python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_md_from_profile.py"
claude_md_from_profile: CLAUDE.md is already up to date with operator-profile.yaml (no-op)
$ echo $?
0
```
<!-- executed: 2026-09-22 · exit=0 -->

No-op, not "replaced": the file is not rewritten, the mtime does not move, and a
SessionStart hook can call this every session without dirtying `git status`.

**3 · Someone hand-edited the block - the refusal:**

```
$ sed -i 's/## THE FLOW/## THE FLOW (mexi aqui)/' CLAUDE.md
$ python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_md_from_profile.py"
claude_md_from_profile: the block in CLAUDE.md was HAND-EDITED (the signature does not match). Not overwriting. See what would change with --dry-run; to overwrite anyway, --force.
$ echo $?
1
```
<!-- executed: 2026-09-22 · exit=1 -->

The signature is a hash of the block's content: any byte changed between the
markers makes the script stop. That is what keeps an automatic regeneration from silently
erasing a fix someone made by hand and has not yet carried into the profile.

**4 · Profile that does not exist - there is no hidden default:**

```
$ python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_md_from_profile.py" --profile does-not-exist.yaml
claude_md_from_profile: unreadable profile ([Errno 2] No such file or directory: 'does-not-exist.yaml'). I do not fix it blind - correct the YAML.
$ echo $?
2
```
<!-- executed: 2026-09-22 · exit=2 -->

## Proof

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/claude_md_from_profile.py" --self-test   # -> self-test OK · exit 0
```

The self-test covers: the example profile generates the warning on line 1 and the floor comes
**before** the inventories; an empty profile generates a valid block without inventing a
section; the person's content outside the markers survives `new` and `replaced` byte for
byte; the second run is `no-op`; a hand edit inside the block is `refused` and `--force`
overrides it; the signature changes when the profile changes.

**Operational success criterion:** the AI that opens the project reads, in CLAUDE.md, the same
level-0 list that the autonomy hook blocks - `grep -c "level 0" CLAUDE.md` equal to the
number of actions with `level: 0` in the profile.

## Known failures / limits
- Generates **only the block**. Project description, code conventions, test commands: those belong to the person, outside the markers. The skill does not write what the profile does not know.
- Automatic profile discovery walks up from the cwd to the root; in a monorepo with two profiles, the closest one wins. Use `--profile` when that matters.
- Requires PyYAML (the profile is YAML). Without it, exit 2 with the message - there is no fallback parser.
- The text the script writes is ASCII by choice (no accents): the block goes into the system prompt of any harness, and some still trip on encoding. The profile's **values** go in as they are - the script does not transliterate what is yours.
- The file's EOL belongs to the person: a `CLAUDE.md` in CRLF stays CRLF after the block, and the signature matches in both cases. Without that, every file saved by a Windows editor would be "hand-edited" forever.
