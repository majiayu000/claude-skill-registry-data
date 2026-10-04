---
name: review-best-practice-profile
description: Use when the user wants to validate a practice profile before using or sharing it — e.g., "review my profile", "validate my-team.toml", "check this profile before sharing".
source: Grimoire project conventions; XDG Base Directory Specification (freedesktop.org)
tags: [profile, review, validation, quality, contributor]
related: [write-best-practice-profile, apply-best-practice-profile, share-best-practice-profile]
---

# Review Best Practice Profile

Validate a `.grimoire/profiles/<name>.toml` file — check format, verify skills exist, surface conflicts.

## Why This Is Best Practice

**Adopted by:** Every package registry runs validation before publish — npm, PyPI, and Cargo all reject malformed manifests at submission time. ESLint's `--print-config` resolves and validates the final config before running. Grimoire profile review applies the same gate: catch issues before a profile is shared and depended on.
**Impact:** A profile with a broken skill name silently activates nothing for that entry — no error, no warning at runtime. Review at authoring time surfaces these before they reach team members who depend on the profile.
**Why best:** Review at publish time costs 30 seconds. Debugging why a profile silently skipped three skills in production costs 30 minutes. The gate is the right place.

Sources: XDG Base Directory Specification (freedesktop.org); npm publish validation; Grimoire `docs/profiles.md`

## Steps

### 1. Locate the profile file

User provides name or path. Search order if only a name is given:

1. `.grimoire/profiles/<name>.toml` — project-level
2. `~/.grimoire/profiles/<name>.toml` — user-level
3. `<name>.toml` — current directory

If not found, report checked locations and stop.

**Multi-location conflict:** If the profile name matches files at more than one location (e.g., both project-level and user-level), note it before proceeding: 'Found [name].toml at [path1] (project) and [path2] (user). Reviewing [path1] — project takes precedence. To review the other, provide the full path.' Do not silently pick one without telling the user.

---

### 2. Parse TOML

If the file is malformed TOML, report the parse error with line number and stop:
```
✗ Parse error at line 7: expected '=' after key
```

---

### 3. Check required fields

| Field | Required | Check |
|---|---|---|
| `name` | yes | non-empty string |
| `[[skills]]` | yes | at least one entry |
| `skills[].name` | yes | non-empty string for each entry |
| `description` | no | warn if absent (helpful for sharing) |

---

### 4. Check each skill name

For each `skills[].name`, check it exists in installed grimoire skills:
- **Found**: mark ✓
- **Not found**: mark ⚠ with install hint

---

### 5. Check for skill conflicts

Read the `related:` frontmatter of each found skill. If two skills in the profile list each other as conflicting (or share a known-conflicting tag pairing), flag as warning. This is a soft check — conflicts are context-dependent.

**Conflict detection mechanism:** Two skills conflict if:
1. They prescribe contradictory behavior for the same trigger (e.g., two formatting skills with opposing rules)
2. One skill's tags or description explicitly contradicts another's (e.g., 'prefer immutability' vs 'prefer mutation for performance')
3. The user has a pinned preference for one practice that this profile would override

For each detected conflict, show: '[skill-A] ↔ [skill-B]: [reason they conflict] — cannot apply both simultaneously.'

**Example conflicts (anchors for judgment):**
- `apply-functional-programming` ↔ `apply-oop-principles` — mutually exclusive paradigms when applied globally to the same codebase
- `prefer-immutability` ↔ a performance practice requiring mutation — philosophy conflict on data handling
- `enforce-strict-types` ↔ `prefer-duck-typing` — type system philosophy conflict

Use these as calibration anchors when evaluating novel skill pairs.

---

### 6. Report result

```
Profile: my-team (4 skills)

  ✓ Format valid
  ✓ description present
  ✓ apply-solid-principles        — found
  ✓ apply-domain-driven-design    — found
  ⚠ apply-twelve-factor-app       — not installed
    Install: grimoire --skill engineering/architecture/apply-twelve-factor-app
  ✓ apply-kiss-principle          — found

Result: PASS with 1 warning

Next: /share-best-practice-profile my-team
```

If errors exist (missing required fields, zero valid skills), result is `FAIL`.

**FAIL is advisory, not a blocker:** A FAIL result means the profile has issues worth fixing before sharing, but the user can still apply it. After showing the FAIL findings, offer: 'Fix issues before applying? [y] or apply anyway? [n]'. Never silently block application.

## Common Mistakes

**Skipping review before sharing.** A profile that works locally (all skills installed) may fail for others if skill names are not canonical. Review against the published skill list, not just what is locally installed.
