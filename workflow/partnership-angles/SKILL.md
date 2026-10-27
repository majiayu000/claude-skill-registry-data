---
name: partnership-angles
description: >
  Internal /ace:partnership-video step — Propose three pitch angles from research.
user-invocable: false
disable-model-invocation: false
---

# Partnership Angles

Ground every one of the three library narrative templates (`day-in-the-life`, `the-scale-gap`, `trust-travels`) against the research and Connect-fit memo produced for a specific prospect, yielding three complete, citable, pitch-able angles. This skill is the terminal artifact of the propose-phase — it writes `angles.yaml` and stops; the orchestrator presents the angles to the operator and waits for a selection before proceeding to production. This skill runs inline at level 0; it does not dispatch `Agent`.

## Inputs

Pipeline-only: a step of a `/ace:partnership-video` run; it reads that run's research.

| Source | Artifact | Used for |
|---|---|---|
| `partnership-research` | `ACE/partnerships/<slug>/research/deep-research.md` | Cited org profile: scale, model, geography, expansion thesis |
| `partnership-research` | `ACE/partnerships/<slug>/research/connect-fit.md` | Connect/Dimagi capability-fit memo for this prospect |
| Phase 1 profile | `ACE/partnerships/<slug>/prospect.yaml` | Prospect identity, sector, target geography, contact |
| ACE repo (versioned) | `templates/partnership-narratives/*/narrative.yaml` | The three reusable narrative templates (durable library) |

## Products

- `ACE/partnerships/<slug>/runs/<run-id>/angles.yaml` — three grounded narrative angles (propose-phase terminal artifact)
- `ACE/partnerships/<slug>/runs/<run-id>/run_state.yaml` — Phase Write-Back: `phases.angles.*`

## Process

1. **Read the research artifacts and prospect context.**

   Read the following from Drive via `drive_read_file`:
   - `ACE/partnerships/<slug>/research/deep-research.md`
   - `ACE/partnerships/<slug>/research/connect-fit.md`
   - `ACE/partnerships/<slug>/prospect.yaml`

   If either research file is missing, **halt with an actionable error**: "Partnership angles requires `research/deep-research.md` and `research/connect-fit.md`. Run `partnership-research` first."

   Extract from `prospect.yaml`:
   - `name` — display name of the prospect org
   - `target_geography` — the expansion thesis geography
   - `sector` — health / MNCH / agriculture / etc.
   - `slug` — used for all path construction below

2. **Load the three narrative templates from the library.**

   The library is at `templates/partnership-narratives/` in the ACE repo. The three narrative IDs are:
   - `day-in-the-life`
   - `the-scale-gap`
   - `trust-travels`

   Each `narrative.yaml` defines: `id`, `title`, `thesis`, `emotional_beat`, `hero`, `primary_capability`, and seven beats (`hook`, `cycle`, `handoff`, `scene`, `problem`, `product`, `impact`), where each beat has an `intent` and a `words` budget.

   These templates are the source of truth for the arc structure. **Do not invent narrative arcs.** The skill's job is to ground the library intents with prospect-specific cited facts — not to author new narratives.

3. **For each of the three narrative templates, produce a grounded angle object.**

   For each narrative template, produce a grounded angle with the following fields:

   ```yaml
   angle_id: <narrative-id>          # e.g. day-in-the-life
   title: <narrative title>
   logline: >                        # one sentence: what this angle says to THIS prospect
     <prospect-specific logline>
   thesis: <narrative thesis>
   hero: <narrative hero>
   emotional_beat: <narrative emotional_beat>
   primary_capability: <narrative primary_capability>
   beats:
     hook: <grounded one-liner: specific cited fact from the research that accomplishes the intent>
     cycle: <grounded one-liner>
     handoff: <grounded one-liner>
     scene: <grounded one-liner>
     problem: <grounded one-liner>
     product: <grounded one-liner>
     impact: <grounded one-liner>
   grounded: true | false
   grounding_notes: >               # cite the specific research fact(s) behind each beat;
     <per-beat source trace>        # if grounded: false, name the missing fact(s)
   ```

   **Grounding rules (design §3, §8 — no inferred backstory):**

   - A beat is **grounded** when a specific fact in `deep-research.md` or `connect-fit.md` directly supports what the beat's `intent` demands. The fact must be citeable (traceable to a source in the research report).
   - If a beat cannot be grounded — the research lacks the fact the intent requires — the beat text must say so explicitly: *"[UNGROUNDED — missing: <description of the missing fact>]"*. Do NOT invent a plausible-sounding fact to fill it.
   - Set `grounded: true` only if **all seven beats** are grounded with real cited facts. Set `grounded: false` if any beat was left ungrounded, and name the missing fact(s) in `grounding_notes`.
   - A narrative that is `grounded: false` is still included in `angles.yaml` — the operator can decide whether to pursue additional research or skip it. Do not silently drop it.
   - **Fabrication is the cardinal failure.** A fabricated statistic, invented partnership, or invented program history in a prospect-facing artifact is the worst possible outcome. When in doubt: mark ungrounded, do not guess.

   **Distinctness rule:** The three grounded angles must lean on *different* research facts and different capabilities. If two angles ground the same beat with the same fact, the grounding is wrong — go deeper in the research to find differentiated evidence.

4. **Write `angles.yaml` to the run folder.**

   Resolve the run folder via `drive_create_folder` with `findOrCreate: true` (parent = the `runs/<run-id>/` folder for this partnership run). Write `angles.yaml` via `drive_create_file`. Record the returned Drive `file_id`.

   The YAML structure:

   ```yaml
   prospect_slug: <slug>
   generated_at: <ISO timestamp>
   angles:
     - angle_id: day-in-the-life
       ...
     - angle_id: the-scale-gap
       ...
     - angle_id: trust-travels
       ...
   ```

5. **Inline QA (binary — run before writing the phase write-back).**

   Verify all of the following. Record which checks pass and which fail — the write-back in step 6 is ALWAYS written regardless of outcome (the eval gate reads `phases.angles.verdict` from `run_state.yaml`; skipping the write-back would make the eval gate invisible to the orchestrator):

   - **`angles_file_exists`**: `angles.yaml` was written and a `file_id` was returned.
   - **`exactly_three_angles`**: `angles.yaml` contains exactly 3 angle entries.
   - **`angle_ids_match_library`**: The three `angle_id` values are exactly `day-in-the-life`, `the-scale-gap`, `trust-travels`.
   - **`all_seven_beats_present`**: Each angle has all 7 beat keys (`hook`, `cycle`, `handoff`, `scene`, `problem`, `product`, `impact`).
   - **`grounded_or_flagged`**: For every beat in every angle, either the text is a grounded one-liner OR the text contains `[UNGROUNDED` — no silent blanks.

6. **Write the Phase Write-Back to `run_state.yaml`** (always — both pass and fail paths).

   Write `phases.angles.*` to `ACE/partnerships/<slug>/runs/<run-id>/run_state.yaml` via `update_yaml_file` with `merge: 'deep'` (a partial nested patch of `phases.<phase>` requires `deep` — `two-level` silently drops sibling keys; see CLAUDE.md § Gotchas):

   **QA pass path** (`verdict: pass`):
   ```yaml
   phases:
     angles:
       status: done
       verdict: pass
       completed_at: <ISO timestamp>
       summary_artifact: angles.yaml
       steps:
         research_read: done
         narratives_loaded: done
         angles_grounded: done
         inline_qa: done
         write_back: done
       products:
         angles_file_id: <file_id from step 4>
         grounded_count: <0–3>    # number of angles where grounded: true
   ```

   **QA fail path** (`verdict: fail`): write the write-back first, then halt with the failed check names surfaced.
   ```yaml
   phases:
     angles:
       status: incomplete
       verdict: fail
       completed_at: <ISO timestamp>
       summary_artifact: angles.yaml
       steps:
         research_read: done
         narratives_loaded: done
         angles_grounded: done
         inline_qa: fail
         write_back: done
       products:
         angles_file_id: <file_id from step 4>       # may be null if angles_file_exists check failed
         grounded_count: <0–3>
       qa_failures:
         - <failed-check-id>                          # one entry per failed check
   ```

   After writing the write-back on the fail path, halt with an actionable operator error naming the failed checks.

## MCP Tools Used

- Google Drive: `drive_read_file`, `drive_create_folder`, `drive_create_file`, `update_yaml_file`

Note: The narrative library is read from the ACE repo filesystem at skill runtime — it is not stored in Drive. The three `narrative.yaml` files under `templates/partnership-narratives/` are consumed as-is; no MCP call is needed to load them.

## Mode Behavior

- **Auto:** Run all steps, ground all three angles, write `angles.yaml` and the phase write-back, stop. The orchestrator presents the angles to the operator; the operator selects one. No render happens in this skill.
- **Review:** Same as Auto. The propose-phase gate is at the orchestrator level (the operator picks an angle), not inside this skill.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-06-06 | Initial version. Propose-phase terminal artifact skill for the partnership-video pipeline. Inline QA (no separate -qa skill), merge: deep write-back. | ACE team |
