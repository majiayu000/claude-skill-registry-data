---
name: play-data-safety-code-audit
description: "Audit an Android app's Play Data Safety declaration (and privacy policy) against the code that actually uploads — enumerate the client's real write targets and RPC arguments, map each to a declared category, and avoid the field-name matching that reports dozens of false gaps. Use before submitting the form, after adding any sync/telemetry call, or when privacy docs and code may have drifted."
---

# Auditing a Data Safety declaration against the code

The form is a legal statement about what leaves the device. It drifts silently:
someone adds one column to a sync call and no document changes. A reviewer finds
that, you don't.

## The wrong check (produces confident nonsense)

Matching serialized field names against the document:

```python
fields = re.findall(r'@SerialName\("([a-z_]+)"\)', dtos)
missing = [f for f in fields if f not in doc]   # reports ~60% "undeclared"
```

This reported 28 undeclared fields on an app whose declaration had exactly one
real hole. The form asks for **categories** ("Fitness info — workouts"), never
columns, so `set_index` and `local_id` will never appear in it and their absence
means nothing.

## The check that works

1. **Enumerate what the client actually writes**, including RPCs — an RPC hides
   its payload behind a function name, so grep arguments too:

```bash
rtk grep -on 'from("[a-z_]*")' <cloud sync file>      # table/view targets
rtk grep -n 'rpc(\|"p_[a-z_]*"' <cloud sync file>      # RPC name + parameters
```

   Separate **reads** from **writes**: a leaderboard view the client only reads
   is not collection by that client.

2. **Map each write to a declared category.** Ask per category, not per column:
   is there a section that covers this? Derived numbers (level, XP, streak,
   score) are the usual omission — they feel internal, but they leave the device
   and are typically what a leaderboard ranks on, so they are collected.

3. **Cross-check the other documents.** A hosted privacy policy, an in-repo
   `PRIVACY.md`, a README privacy line and the form answers drift apart
   independently. Grep each for the same category words; a term present in one
   and absent from another is the finding.

4. **Cite code in the declaration.** Each declared type should name the call and
   migration that create it (`CS pushDerivedAggregates()` → `push_aggregates`,
   `M11`). Without that, the next audit restarts from zero.

## Categories that are collected but feel like they aren't

- Derived/aggregate stats pushed for ranking (level, total XP, streak, strength)
- A visibility/privacy setting itself (it is profile info)
- Free-text notes attached to records — check whether a *private* note field is
  excluded in code, and say so explicitly rather than implying all notes upload
- Account identifiers from the auth provider, separate from email

## Claims to verify, not assume

- "Health data is not collected" — prove it: grep the cloud package for the
  health entity names and show zero references.
- "Body measurements stay on device" — same, and confirm no table exists for
  them in the schema.
