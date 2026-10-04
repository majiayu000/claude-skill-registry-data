---
name: apply-best-practice-profile
description: Use when the user wants to activate a named set of best practices for a paradigm or methodology — e.g., "use OOP", "set profile to clean-architecture", "apply TDD practices", "switch to functional style".
source: Grimoire project conventions; XDG Base Directory Specification (freedesktop.org)
tags: [profile, preference, oop, functional, tdd, clean-architecture, paradigm, activation]
related: [pin-best-practice-preference, discover-best-practices, resolve-best-practice-conflict]
---

# Apply Best Practice Profile

Activate one or more named practice profiles, pinning their skills as preferences for the current scope.

## Why This Is Best Practice

**Adopted by:** Every major developer toolchain uses profile-based configuration: VS Code profiles, ESLint shared configs (`eslint-config-airbnb`), Prettier shared configs, TSConfig presets. Grimoire practice profiles apply the same model to best practice activation.
**Impact:** Individual skill pinning is correct for explicit, intentional choices. Profile activation is correct for paradigm-level choices where the set of practices is well-established and the user's intent is the paradigm, not any specific skill.
**Why best:** Tags already exist on every skill. `profiles = ["oop"]` activates all skills tagged `oop` with no configuration file required. Users who need curation create one flat TOML file. Array order handles priority — the user controls conflict resolution by ordering profiles.

Sources: XDG Base Directory Specification (freedesktop.org); Grimoire `docs/profiles.md`

## Steps

### 1. Detect the requested profile names

From settings:
```toml
# grimoire.toml
profiles = ["clean-architecture", "tdd"]
```

Or from natural language:

| User says | Profile name |
|---|---|
| "use OOP", "OOP best practices", "object-oriented" | `oop` |
| "functional", "FP style", "functional programming" | `functional` |
| "clean architecture", "hexagonal", "ports and adapters" | `clean-architecture` |
| "TDD", "test-driven", "test first" | `tdd` |
| "12-factor", "12 factor app", "cloud-native" | `12-factor` |

If multiple paradigms are named ("clean architecture and TDD"), collect all names as an ordered list (ask the user to confirm priority order if unclear).
If ambiguous, ask the user to name the profiles.

---

### 2. Resolve each profile independently

**Grimoire-first (preferred):** If grimoire MCP is connected, call `grimoire_context` → `resolved_profiles[name]` gives the already-computed skill list for each profile (5-step file search + 4-layer composition already applied). Or run `grimoire profile list` — it shows the resolved skill list per active profile. Use these lists directly. Do NOT re-implement the resolution chain.

**Fallback (grimoire not installed):** For each name, check in this order (first match wins):

1. `.grimoire/profiles/<name>.toml` — project-level
2. `~/.grimoire/profiles/<name>.toml` — user-level
3. `.grimoire/profiles/default.toml` — project-level fallback
4. `~/.grimoire/profiles/default.toml` — user-level fallback
5. Tag query — all installed skills where `tags` contains `<name>`

If a TOML file is found, read its `[[skills]]` list.
If no file is found and the tag query returns no skills for a name, **stop immediately** — do not guess or invent a profile. Output:
```
Profile not found: [profile-name]
Available profiles: [list installed profiles, or 'none installed — run /discover-best-practices to see what's available']
```
Do not continue resolving remaining profiles while a named profile is unresolvable — surface the error first so the user can correct the name or install the missing profile.

---

### 3. Merge and deduplicate skill lists

**If using grimoire ground truth:** `resolved_profiles` already provides per-profile ordered skill lists. Walk the profiles in settings array order — add each skill name once (first occurrence wins on duplicate). Skip to Step 4.

**Manual merge:**
Combine all resolved skill lists in array order (first profile = highest priority):

- **Exact duplicate** (same skill name in two profiles): keep once, record both sources
- **No automatic conflict detection** — array order determines priority at pin time

Build the merged list, preserving order (first-profile skills first, then second-profile skills not already present, etc.).

---

### 4. Present the unified skill list for confirmation

```
Profiles: clean-architecture (11 skills), tdd (4 skills) → 14 skills total (1 duplicate collapsed)

  apply-solid-principles          [clean-architecture, tdd]  ← requested by both
  apply-domain-based-naming       [clean-architecture]
  apply-domain-driven-design      [clean-architecture]
  apply-protected-variations      [clean-architecture]
  apply-indirection               [clean-architecture]
  apply-polymorphism              [clean-architecture]
  apply-information-expert        [clean-architecture]
  apply-pure-fabrication          [clean-architecture]
  apply-controller-pattern        [clean-architecture]
  apply-low-coupling              [clean-architecture]
  apply-high-cohesion             [clean-architecture]
  apply-test-driven-development   [tdd]
  write-unit-test                 [tdd]
  design-test-pyramid             [tdd]

Priority: clean-architecture > tdd (array order)
Scope: [s] session  [p] project  [g] global
```

Default to session — no prompt needed. Infer scope from context:
- User says "save", "persist", "always", "for this project" → ask once to confirm scope
- No such signal → apply as session silently

---

### 5. Pin all skills

For each skill in the merged list, call `pin-best-practice-preference` at the confirmed scope.
Pass the full ordered list as the `practices` array — index 0 = first-profile skill = highest conflict priority.

**User-decline branch:** If at any point (during confirmation in Step 4 or after) the user says "skip [skill-name]" or "not [skill-name]", remove that skill from the application sequence and continue with the remainder. Do not require full re-invocation to skip one skill. Acknowledge the skip inline:
```
Skipping [skill-name] — continuing with remaining [n] skills.
```

---

### 6. Confirm activation

```
✓ 2 profiles applied (14 skills, 1 duplicate collapsed) — scope: session

  Priority: clean-architecture > tdd

To persist: run "save my session preferences"
To adjust:  unpin or override individual skills
```

## Common Mistakes

**Treating missing TOML as an error.** No profile file is fine — the tag query is the primary mechanism. Only stop if both the file lookup and tag query return nothing for all requested profiles.

**Forgetting array order matters.** `profiles = ["a", "b"]` and `profiles = ["b", "a"]` produce different conflict behavior. Always confirm priority with the user when taking from natural language input.

## When NOT to Use

- **When the user wants one specific skill** — use `pin-best-practice-preference` directly
- **When no profile matches and no skills are tagged** — help the user define a custom profile in `.grimoire/profiles/`
