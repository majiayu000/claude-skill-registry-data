---
name: hol4
description: HOL4 proof development pipeline - planning, sketching, and proving phases. (project)
---

# HOL4 Proof Pipeline Skills

Three-phase proof development methodology:

## /hol4-plan
Interactive proof planning. Creates mathematical argument with validated assumptions.
See [plan.md](plan.md)

## /hol4-sketch
Translate plan to HOL4 sketch. Creates SML with cheats + task files for subagents.
See [sketch.md](sketch.md)

## /hol4-prove
Fill in cheats and complete proofs. Interactive or autonomous mode.
See [prove.md](prove.md)

## Autonomous Execution

```bash
python hol_planner.py --goal "prove theorem X"
python hol_sketch.py --plan plan.md --workdir /path
python hol_proof_agent.py --task TASK_foo.md
python hol_pipeline.py --theorem X --workdir /path  # end-to-end
```

## Methodology Prompts

Full prompts in `prompts/hol4/`:
- `planner.md` - Planning methodology
- `sketch_impl.md` - Sketching methodology
- `proof_agent.template.md` - Proving methodology
