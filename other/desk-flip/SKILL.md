---
name: desk-flip
description: Autopsy a stuck project, extract salvageable artifacts, and route to a fresh start via $bootstrap-repo reset or new-repo bootstrap
type: execution
version: v0.6
required_conventions: [alignment-page]
argument-hint: "<project-path>"
---

# Desk Flip

Invoke as `$desk-flip`.

Autopsy a stuck project, extract salvageable artifacts (lessons, valid specs, non-code assets), and route the user to a fresh start either in a new repo or by resetting the existing repo with `$bootstrap-repo --reset-existing`.

Always desk-flip. If the user invoked it, the decision to restart is already made. Do not offer incremental migration or attempt to fix the old project in place.

## Process

1. **Identify the stuck project.**
   - Accept an optional project path from the invocation arguments; default to the current working directory.
   - Verify the target is a git repo with existing code, not an empty repo.
   - If the project appears to already use the new workflow (file-backed specs, prototype-first artifacts, healthy structure), warn the user and confirm before proceeding.

2. **Survey the project.**
   - Read `AGENTS.md`, `CLAUDE.md`, `README.md`, `package.json` or equivalent manifest, and directory structure when present.
   - Read `tasks/`, `specs/`, and `docs/` directories if they exist.
   - Scan recent git history (last ~50 commits) for commit patterns and timeline.
   - Read any existing `tasks/lessons.md` or post-mortem docs.

3. **Run the autopsy.**
   - **Lessons extraction:** What went wrong? Look for evidence of failure modes: infrastructure before prototype, late testing, chat-driven alignment drift, scope creep, untestable architecture. Cite specific commits, files, or timeline evidence.
   - **Spec/design extraction:** Identify specs, designs, research docs, interview logs, and product briefs that capture valid domain knowledge or user needs, regardless of whether the implementation matched. Mark each as `valid`, `partially valid`, or `stale` with a one-line rationale.
   - **Asset inventory:** Find non-code assets worth preserving: icons, images, copy, API contracts, design tokens, brand assets, research documents.

   Do not extract code, dependencies, database schemas, or infrastructure config.

4. **Write the autopsy report.**
   - Produce `desk-flip-report.md` in the project root with these sections:

   ```markdown
   ## Project Summary
   What the project was and what state it's in now.

   ## What Went Wrong
   Specific failure modes with evidence (commits, files, timeline).

   ## Salvageable Specs & Designs
   List with file paths, validity status, and one-line descriptions.

   ## Salvageable Assets
   Non-code assets with file paths.

   ## Lessons for the Fresh Start
   Actionable guidance for the new project to avoid the same mistakes.

   ## Recommended Bootstrap Input
   A condensed brief suitable as input to $bootstrap-repo.
   ```

5. **Choose the fresh-start path.**
   - If the user explicitly wants a new repository, route to `$bootstrap-repo <condensed brief>`.
   - If the user wants to keep the existing repository, or the current repo name, remotes, issues, deployment linkage, or local tooling are valuable, route to `$bootstrap-repo --reset-existing <condensed brief>`.
   - For in-place reset, state that `$bootstrap-repo --reset-existing` must archive the old implementation under `archive/` before writing the fresh bootstrap docs. It must not delete the old code outright.
   - The archive should preserve old implementation and documentation evidence without treating it as reusable foundation code or active source-of-truth docs. The fresh start should continue only from a high-level concept seed derived from the report, plus lessons captured in the report.

6. **Present and route.**
   - Show the user a terminal summary of the report.
   - Recommend the appropriate `$bootstrap-repo` command with the recommended bootstrap input from the report.
   - Do not create the new repo or run `$bootstrap-repo`; the user does this.
   - After bootstrap, route product/app restarts into the research-first alignment workflow using the high-level concept seed as input: `$customer-discovery` to define who this is for, `$competitive-analysis` to map the market, `$journey-map` to map lifecycle and task flow, `$positioning` to lock the product direction, `$user-flow-map` to map screen flow, `$ux-variations [specific-user-flow]` to explore progression branches, `$ui-interview [specific-ux-variation]` to render and approve/reject a branch mockup, then prototype work, `$uat --variant-evaluation`, and `$consolidate-prototypes` before `$spec-interview` or `$roadmap`. Use `$ui-interview --requirements-only` and `$ux-variations --layout-mode` only when the user explicitly needs a fixed content contract and layout-only alternatives.
   - If the business-discovery or customer-lifecycle packs are not enabled in the fresh repo, recommend `npx skillpacks install business-discovery` and `npx skillpacks install customer-lifecycle` before the research sequence.

## Output

```markdown
Desk-flipped: <project name>
- Report: desk-flip-report.md written to <project-path>
- Specs extracted: <count> (<valid>/<partial>/<stale>)
- Assets found: <count>
- Lessons captured: <count>

**Next work:** Reset the existing repo by archiving old implementation files, or create a new repo if the user prefers a separate fresh start
**Recommended next command:** $bootstrap-repo --reset-existing <condensed brief from report>
```

## Constraints

- **Read-only during desk-flip**: no modifications to existing files, no archival, no branch creation. The only file written by this skill is `desk-flip-report.md`.
- Do not carry forward code, dependencies, infrastructure, old research, old specs, or old task docs from the old project as active files.
- Do not create the new repo or invoke `$bootstrap-repo`; the user handles that transition.
- Do not commit or push; the report is informational, not a meaningful mutation to ship.
- Do not delete, archive, or rename anything in the old repo during desk-flip. Only the downstream `$bootstrap-repo --reset-existing` step may perform archival after the user chooses that route.
- If the project has no specs, docs, or meaningful git history, produce the report anyway but note the thin evidence in each section.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/desk-flip-{topic}.html`.

## Default Shipping Contract

- Do not commit or push. The only side effect is `desk-flip-report.md` written to the project root.
- **Default next-step routing:** when reporting completion, include the two-line pair `**Next work:** <specific task>` and `**Recommended next command:** $bootstrap-repo --reset-existing <brief>` for in-place restarts, or `$bootstrap-repo <brief>` only when a separate new repo is explicitly the right path.
- **Post-bootstrap route:** include in the report that the fresh project should proceed from the high-level concept seed to `$customer-discovery`, then `$competitive-analysis`, `$journey-map`, `$positioning`, `$user-flow-map`, `$ux-variations [specific-user-flow]`, `$ui-interview [specific-ux-variation]`, and prototype work. Mention `npx skillpacks install business-discovery`, `npx skillpacks install customer-lifecycle`, or `npx skillpacks install product-design` first if those packs are not enabled.
