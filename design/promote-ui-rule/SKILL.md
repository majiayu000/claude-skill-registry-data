---
name: promote-ui-rule
description: |
  Promote a recurring UI mistake from the journal (JOURNAL.md and JOURNAL/*.md) into an automated guard rule
  in architecture-guard.rules.json. The promotion is gated: requires 3+ journal
  entries tagged `ui-evolution + recurring-mistake` matching the same pattern.
  Use when: the user says `/promote-ui-rule`, "promote this UI rule", "the
  designer keeps catching X, automate the check", or after a code review
  surfaces the third occurrence of the same UI anti-pattern.
user_invocable: true
---

# /promote-ui-rule — Designer-feedback → guard-rule lifecycle

Convert a recurring UI mistake into an automated `architecture-guard.py` rule.
The lifecycle is deliberately human-mediated — there are no silent rule rewrites.

## Step 1: Scan the journal for promotion-eligible entries

Read `.claude/registries/JOURNAL.md` (the Universal root) and every `.claude/registries/JOURNAL/*.md` domain file, and grep for entries that satisfy ALL of:

- `Tags:` line contains BOTH `ui-evolution` AND `recurring-mistake`
- Lesson describes a check expressible as a regex (e.g. "use text-on-surface-variant not text-neutral-X" — a substring or class match)
- Three or more separate dated entries describe the SAME underlying pattern (count by the regex skeleton, not the exact title)

If fewer than 3 matching entries exist for any single pattern, **BLOCK promotion**. Tell the user:

> "Promotion gated. Found N entries tagged `ui-evolution + recurring-mistake` matching this pattern. Need 3+. Returning without writing."

The gate exists so isolated one-off mistakes don't bloat the guard.

## Step 2: Confirm the rule shape with the user

For the eligible pattern, derive a draft rule definition:

```json
{
  "id": "<kebab-case-id>",
  "regex": "<python-regex>",
  "applies_to": "html|ts|scss|any",
  "scope": "all|<one application name from the frontend.roots slot>",
  "suggestion": "<replacement-guidance-with-token-name>",
  "exception_seeds": []
}
```

Present the draft to the user via `AskUserQuestion` with these fields editable:

1. **Rule id** — kebab-case, globally unique (suggest `<offending-class>-banned-<scope>`).
2. **Regex** — the actual pattern the guard will match. Default: `\b<bad-class>\b`. Let the user refine.
3. **Applies to** — html / ts / scss / any. Default: infer from the journal entries' source contracts.
4. **Scope** — `all`, or one application name from the `frontend.roots` slot of `.claude/project-profile.md`. Default: `all` unless a single `app:<name>` sub-tag dominates the matching entries.
5. **Suggestion** — replacement guidance. Default: pull from the most recent journal entry's `Lesson:` field.
6. **Exception seeds** — optional comma-separated file-path substrings to exempt. Default: empty.

## Step 3: Append the rule to architecture-guard.rules.json

Use `Edit` to append the new rule object to the `rules` array in the project's `.claude/hooks/architecture-guard.rules.json`. Validate before writing:

- `id` must not collide with any existing rule's `id` (re-read the file fresh).
- `regex` must compile under Python's `re` module.
- `applies_to` must be one of the four allowed values.

If any validation fails, report the failure and HALT — do not write a partial entry.

## Step 4: Verify the rule fires (and the kill switch still works)

Construct a one-line test snippet that should trigger the new rule. Find the guard hook (the plugin root first, then the project's copy), and feed it the payload directly.

```bash
GUARD=
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/.claude/hooks/architecture-guard.py" ]; then GUARD=$CLAUDE_PLUGIN_ROOT/.claude/hooks/architecture-guard.py
elif [ -f "${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/architecture-guard.py" ]; then GUARD=${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/architecture-guard.py
fi
[ -n "$GUARD" ] || { echo "architecture-guard.py not found: tried \$CLAUDE_PLUGIN_ROOT/.claude/hooks/architecture-guard.py and the project's .claude/hooks/architecture-guard.py"; exit 1; }
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}" py -3 "$GUARD" <<'EOF'
{"tool_name":"Write","tool_input":{"file_path":"<path-matching-scope>","content":"<test-snippet>"}}
EOF
```

Confirm:
- Exit code 2 (blocked) — the rule fires.
- Block message cites `external:<rule-id>` — the right rule.
- With `CLAUDE_ARCH_GUARD=off` set, the same payload exits 0 — the kill switch still works.

If any of those three checks fail, REVERT the JSON write and report the failure.

## Step 5: Record the promotion in the journal

Use the `/journal-add` skill to append a single entry:

```markdown
### YYYY-MM-DD — UI rule promoted: <rule-id>
- **Trigger:** manual
- **Source contract:** N/A
- **Lesson:** Promoted recurring UI mistake `<bad-class>` into automated guard rule `<rule-id>` after N journal entries documented the pattern.
- **Apply when:** future code review encounters the same anti-pattern — point at `architecture-guard.rules.json` rather than asking the author to fix manually.
- **Tags:** ui-evolution, rule-promoted, automation
- **Areas:** ui-design-system, ui-component-shared
```

## Step 6: Report done

Summarize for the user:

> "Promoted rule `<rule-id>` to architecture-guard.rules.json after N matching journal entries. Verified the rule fires on `<test-snippet>` and that `CLAUDE_ARCH_GUARD=off` still bypasses. Journal entry appended."

## Hard constraints

- **NEVER edit `architecture-guard.py`** — the rule lives in JSON, not Python. The hook loads the JSON at scan time.
- **NEVER promote without the 3+ journal entry gate.** No exceptions, no overrides — the gate IS the design.
- **NEVER write a rule without an `exception_seeds` field**, even if empty. Future-proof: the field is the only escape hatch when the rule is over-broad.
- **NEVER touch `architecture-guard.rules.json` outside this skill** without first running the validation steps in Step 4.
