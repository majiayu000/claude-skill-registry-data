---
name: pai-sho
description: Iroh's Pai Sho, testing a strategy against a real opponent before trusting it. Use for eval, /eval, "test this skill change", "does this prompt change behavior", "A/B this skill", "will agents actually follow this", or before promoting any skill, structure, or prompt change that is meant to change what an agent does. Runs blinded candidates on several models, one blinded judge, and checks the real transcripts.
---

# Iroh's Pai Sho

Iroh never trusted a strategy he had only imagined. He played it across the board against a real opponent, watched what actually happened, and only then believed it. A skill change is a strategy. Before you promote it, play it against agents that do not know they are being watched. You own the experiment design. Plan, blind, run, and synthesize.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Run this from the top-level session. A dispatched character cannot dispatch candidates. If you are one, stop and report that the eval needs the top-level session.

## Blinding

These rules are non-negotiable. A leak makes the result worthless.

- None of these words appear in any directory, file, or prompt a candidate sees: eval, test, judge, experiment, rubric, score, compare, benchmark, candidate, arena, pai-sho.
- The candidate prompt looks like an organic user request. State the goal, not the meta.
- No chain-eliciting cues. Do not ask a candidate to list which skills, principles, or files it applied. Ask for design notes in general, and grade chain-following from the shape of the work, not from self-report.
- Sanitize directory and slug names. Use project-shaped names a user might pick.
- Do not tell a candidate that other candidates exist.
- The judge may know it is judging. It sees outputs only by sanitized label, never by model name.
- To compare two variants, one judge scores both sets in a single pass on one scale, blind to which set each output came from.

## Steps

1. **Frame.** State the variant under test and the behavior that counts as success. Write the rubric, three to six concrete criteria, for the judge only. Hold it back from candidates.
2. **Set up sanitized environments.** Give each candidate its own working directory with the variant in place. Plant the context an organic task would have, such as a project skeleton and the skills a candidate would naturally read. For a two-variant comparison, build one set of directories per variant from the same skeleton.
3. **Write one organic prompt.** Write what a user would type. Leak nothing about what is measured.
4. **Spawn the candidates in parallel.** Use one Agent call per candidate, all in one message, with `run_in_background: true`. Run them on different models from the `panel` line of the avatar-setup sheet. Dispatch each as the character whose discipline fits the organic task, with `subagent_type: "team-avatar:<character>"` and the model passed explicitly. Never dispatch Toph for a task that edits files. Each candidate works in its own sanitized directory with the same prompt. Pick each reasoning effort for the job with the Agent tool's `effort` parameter. If a candidate produces nothing, continue with the rest and note the dropout.
5. **Spawn one blinded judge.** Wait until every candidate has finished. Pick a model from the `panel` line that did not run as a candidate, preferring a different model family from the candidates. If every panel model ran as a candidate, use the `strongest` line and say that judge independence was reduced. Dispatch the judge as Toph, who is read-only. The judge sees the rubric and the outputs by sanitized label, scores each criterion for each output, and names the strongest output with its reasons. It runs while you do steps 6 and 7.
6. **Verify the chain from transcripts, not self-report.** Read each candidate's local transcript. On Claude Code, it lives in the per-project transcripts directory, `~/.claude/projects/<encoded-cwd>/`, where `<encoded-cwd>` is this session's working directory with its path separators turned into `-` (for example `-Users-me-repo`). On Codex, read the session's rollout files under `${CODEX_HOME:-~/.codex}/sessions/`. Never glob across every project. That crosses workspace boundaries and reads private chats from unrelated projects. Note which files each candidate actually opened. Grade chain-following from the files it really read and the shape of its work, never from its own claims.
7. **Read every output yourself, end to end.** Score each against the rubric, criterion by criterion. Then compare with the judge's verdict. Agreement is strong signal. Disagreement means a model is biased or the rubric is ambiguous. Read both rationales and decide which. If the candidates diverge wildly, the frame or the prompt was underspecified. Fix it and run again rather than averaging the noise.
8. **Explain the number before you trust it.** A score is a measurement. Before you call the variant better, rule out that it measured something else, such as a leak in the prompt, a planted file that gave the answer away, or one candidate failing for an unrelated reason (Explain the Number, Earth in `four-elements`).

## Rules

- Never promote a structural skill change on intuition alone. Promote it on this result, or say why the eval could not run.
- A variant that wins on the judge but loses on the transcripts did not win. The transcripts show what the agent did.

## Reply

The variant under test, the rubric, notes for each candidate (model, what it read, what it produced, any dropout), the judge's verdict, your own synthesis and where it differs from the judge, and a recommendation on whether to promote the variant. Write it through `tea-time`.
