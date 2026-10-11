---
name: push-downstream
description: >-
  Publish XYZ-forge into its standalone downstream repos (XYZ-mini, XYZ-skills-army-mini,
  AgentChorus-Skill) with the one embedded-manifest publisher, utils/py/xyz_mini_sync.py (GH-589,
  GH-955). XYZ-forge is the upstream for all of them. Target one repo, several, or all in one run;
  preview first, then apply and push on one confirmation. Trigger on "/push-downstream",
  "/push-to-xyz-mini", "publish to mini", "sync XYZ mini", "publish skills army", "publish agent
  chorus", "refresh the downstream repos", "push the standalone repos". Manual, operator-invoked.
---

# push-downstream

Publish XYZ-forge → its standalone child repos. **XYZ-forge is the upstream for every one of them**
(GH-955 reversed GH-882's 2026-10-01 decision for Skills Army HQ). The publisher owns every guarantee;
this skill is the operator flow around it. Read `utils/py/xyz_mini_sync.py` for the manifests and the
contract.

| Target | Child repo | Local checkout (default, or env) |
|---|---|---|
| `xyz-mini` (default) | HiQS-Labs/XYZ-mini | `../XYZ-mini` or `$XYZ_MINI_REPO` |
| `skills-army-mini` | HiQS-Labs/XYZ-skills-army-mini | `../XYZ-skills-army-mini` or `$XYZ_SKILLS_ARMY_MINI_REPO` |
| `agent-chorus` | HiQS-Labs/AgentChorus-Skill | `../AgentChorus-Skill` or `$AGENT2AGENT_STANDALONE_REPO` |

## Preconditions

- You are in an XYZ-forge clone whose HEAD is what you intend to publish. Any branch is sanctioned:
  the tool records `source_branch` in each child's `.xyz-forge-revision` and warns when it is not
  `development`; re-publish from `development` after the branch lands to re-baseline. The source must
  be clean (`--allow-dirty` exists but is recorded in the child commit).
- Each selected child has a local checkout on branch `main`, clean, with no unpushed non-sync commits.

## Flow

1. **Preview** (writes nothing). One target, several, or all:

   ```bash
   python3 utils/py/xyz_mini_sync.py                                  # xyz-mini
   python3 utils/py/xyz_mini_sync.py --target agent-chorus --target skills-army-mini
   python3 utils/py/xyz_mini_sync.py --target all
   ```

   Read each target's plan line (files to copy, paths to delete). A refusal (exit 2) names the exact
   reason; fix it at the source, never work around it. Exit 4 means the secret scan fired. A
   multi-target run keeps going past a failed target, prints one `downstream: <target>: exit N` line
   each, and exits with the worst code.

2. Show the operator the plans and ask once: "publish this?"

3. On yes, apply and push the same selection:

   ```bash
   python3 utils/py/xyz_mini_sync.py --target all --push
   ```

   Exit 0 means each child's commit exists locally **and** its `origin/main` read back equal to it.
   Exit 3 means a commit or push failed; the local commit is retained and a rerun retries the push.

4. Read back and report per child: `git -C <child> log -1 --stat` and the pushed SHA.

`--dest PATH` overrides the checkout location for exactly one `--target`. `--check` is the read-only
managed-parity check the child CI runs (exit 1 on drift); it never writes.

## Changing what ships

Edit the target's manifest tuple in `utils/py/xyz_mini_sync.py` in a forge PR. Dropping an entry
deletes it from the child on the next publication (the child's `MANIFEST.txt` records what the last
run wrote); adding one ships it. Child files the tool did not publish survive. Seeds (XYZ-mini's
`TODO.md`) are copied once. `adapted` entries are XYZ-mini's exception path for mini-owned bytes,
governed by `mini/ORIGIN.md` and `mini/ADAPTATIONS.md`. The contract tests are
`test/gh589-xyz-mini-sync.sh` and `test/gh620-skills-army-mini-sync.sh`.

**Adding a new child repo** is a new entry in `TARGETS` (manifest, env var, sibling dir name, log
prefix). A child that already has files but no `MANIFEST.txt` needs one reviewed setup commit in the
child listing the paths the forge will own; the ownership guard refuses to overwrite anything else.

**One-time setup for AgentChorus-Skill** (GH-955; run once, after the GH-955 PR has merged). Both
checkouts must be clean and current: the forge at the commit you will publish, the child on `main`.

```bash
# in the XYZ-forge clone: write the child's MANIFEST.txt (its 13 payload paths, one per line, sorted)
python3 utils/py/xyz_mini_sync.py --target agent-chorus --print-manifest \
  | python3 -c 'import json,sys; print("\n".join(sorted(d for _, d, _m in json.load(sys.stdin))))' \
  > ../AgentChorus-Skill/MANIFEST.txt
# in the child: drop the retired publisher's two files, commit, push
git -C ../AgentChorus-Skill rm -q .xyz-canonical-revision skills/agent-chorus/publish-manifest.tsv
git -C ../AgentChorus-Skill add MANIFEST.txt
git -C ../AgentChorus-Skill commit -m "chore: hand ownership to XYZ-forge's central publisher (GH-955)"
git -C ../AgentChorus-Skill push origin main
# back in the forge clone: the first central publication (preview first, as in Flow)
python3 utils/py/xyz_mini_sync.py --target agent-chorus --push
```

The setup commit's own CI run fails by design: the old workflow still reads the removed
`.xyz-canonical-revision`. The first publication replaces that workflow in the same commit. The
migration is done only when the child CI is green at the first published SHA.

## What this skill never does

Automatic or scheduled runs, force pushes, history rewrites, or hand edits inside a child checkout.
Inbound vendoring (child → forge) does not exist: changes land in XYZ-forge first.
