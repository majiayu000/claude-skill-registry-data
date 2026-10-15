---
name: "che-archeology"
description: "Infers project Intent and Roadmap from git history and merged PRs. Invoke when starting with an existing project to align it with the Specflow SDLC."
---

# Che Archeology (History Inference)

> **SHARED REFERENCES:**
> - SDLC Specflow Phase 1 & 2: `engineering-contracts` Rule 15
> - Path resolution: `che` CLI (`che compute_paths`, `che ensure_dirs`)

This skill performs a "historical scan" of a repository to reconstruct its strategic backbone. It bridges the gap between legacy development and the Specflow-driven Che SDLC.

---

## §0 PURPOSE

To automatically populate `intent.md` and `roadmap.md` for existing projects by analyzing commit patterns, PR descriptions, and README evolution.

---

## §1 WORKFLOW

### Step 1: Data Collection
1. **Git Log**: Run `git log --reverse --pretty=format:"%h | %as | %s %b"`.
2. **PR Metadata**: Run `gh pr list --state merged --json number,title,body,createdAt --limit 100`.
3. **README Evolution**: Check the earliest versions of `README.md`.

### Step 2: Semantic Clustering
1. Group commits and PRs into "Windows" (e.g., blocks of 2-4 weeks or major feature pushes).
2. For each window, identify:
   - Primary Focus (e.g., "Authentication", "Payment Integration").
   - Milestone achieved.

### Step 3: Blueprint Reconstruction
1. **Infer Intent**: Analyze the first 10-20 commits and initial README.
   - *Why* was this project started?
   - *Who* are the target users?
2. **Infer Roadmap**: Cluster the windows into high-level Phases.
   - Phase 1: Foundations.
   - Phase 2: Core Features.
   - Phase 3: Enhancements.

### Step 4: Artifact Generation
Draft the following artifacts in memory:
- `intent.md`: Vision, Problem Statement, Success Criteria.
- `roadmap.md`: Chronological phases with IDs, Titles, and delivered Features.

### Step 5: Approval & Persistence
1. Show the draft to the user.
2. Upon approval, save to `CHE_PROJECT_DIR` (`project/` inside the project folder).

---

## §2 QUALITY GATES
- **Accuracy Check**: Do the inferred phases match major architectural shifts?
- **Lean Check**: Avoid over-fragmenting the roadmap. Stick to 3-5 major phases.
