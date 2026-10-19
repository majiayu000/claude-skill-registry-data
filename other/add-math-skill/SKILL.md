---
name: add-math-skill
description: Add math skills to the Mathiz skill graph (the curriculum DAG that renders as the treasure map). Use when extending the curriculum — new skills, strands, or grade levels.
---

# Extending the skill graph

The graph in `internal/skillgraph/seed.go` IS the curriculum and the treasure
map: strands are islands, prerequisite edges are the fog of war, skills are
dig spots. 56 skills today, grades 3–5, 5 strands.

## Adding a skill

Append to the seed slice:

```go
{
    ID:            "kebab-case-stable-id",   // never rename: it's the owner-scoped data key
    Name:          "Kid-Facing Name",        // shows on the map spot
    Description:   "One sentence for the question-generation prompt.",
    Strand:        StrandFractions,          // island; new strands need AllStrands() + StrandDisplayName()
    GradeLevel:    4,                        // 3–5 (grade-2 content lives under G3)
    CommonCoreID:  "4.NF.B.3",
    EstimatedMins: 15,
    Keywords:      []string{"..."},          // steer the LLM prompt
    Prerequisites: []string{"existing-id"},  // at least one, unless replacing THE root
    Tiers:         DefaultTiers(),           // learn: 8 problems @75%, prove: 6 @85%/30s
}
```

## Hard rules

- **Exactly one root skill** (empty `Prerequisites`). `Validate()` panics in
  `init()` on cycles, dangling prereq IDs, or duplicate IDs — a bad seed
  kills every binary and test in the repo.
- **IDs are forever**: mastery snapshots, events, and spaced-rep state key on
  skill ID per child. Renaming orphans learner data (the stats/notebook
  code skips unknown IDs, so old data silently disappears).
- Prereqs may cross strands. Grade level is metadata for map layout and
  planner ordering — unlocking is purely prerequisite-driven.

## Verify

```bash
go test ./internal/skillgraph/            # validation + graph tests FIRST
go test ./internal/...                    # planner/session tests exercise the graph
```

Check the map renders sanely: the new spot appears on its island in the
`/play` UI (grade badge, locked until prereqs mastered) — the `saas-e2e`
skill has the browser flow. No frontend changes are needed for new skills;
islands and spots render from the API.

New strands additionally need: `Strand` constant + `AllStrands()` +
`StrandDisplayName()` in `internal/skillgraph/skill.go` (the map and
dashboard group by these).

Question generation needs no changes — prompts are built from the skill's
Name/Description/Keywords/Tier automatically. Consider whether
`internal/problemgen/mathcheck.go` can recompute answers for the new skill's
question style (pure-arithmetic patterns only; non-computable questions pass
through silently).
