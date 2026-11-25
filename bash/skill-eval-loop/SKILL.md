---
name: skill-eval-loop
description: Prove whether a candidate skill actually improves agent performance before adopting it - blind A/B evals on reconstructed real tasks, a three-tier adoption gate, and production rechecks. Use when asked to "eval this skill", "does this skill help", "test this skill before installing", "run the auto-improve loop", or "recheck probationary skills". Takes candidates from skill-miner; runs locally with the user's own agent CLI and models.
---

# skill-eval-loop

The proof half of the auto-improve loop. skill-miner finds pain and candidates;
this skill decides what earns a place in the fleet. Everything runs locally -
the user's own machine, own agent CLI, own models, own tasks.

## The loop

```bash
python3 scripts/brief.py <clusters.json> --index 0 [--knowledge-gap]   # theme -> eval brief
for n in 1 2 3; do
  FORGE_SAMPLE=$n bash scripts/run_eval.sh <brief.json> without ""     # baseline arm
  #   ...or <incumbent> instead of "" to make the baseline the skill already
  #   installed for this trigger, which is what adoption competes with
  FORGE_SAMPLE=$n bash scripts/run_eval.sh <brief.json> with <skill>   # candidate arm
  python3 scripts/judge.py <brief.json> --sample $n                    # blind A/B + verify
done
python3 scripts/aggregate.py <brief.json>                              # strict majority
python3 scripts/gate.py <brief.json> <skill> [--adopt-dir DIR] [--probation --failure-rate R]
python3 scripts/recheck.py --sources claude,opencode,codex --dry-run  # weekly review, decides nothing
```

Or hands-free end to end:

```bash
bash scripts/forge.sh --mode corrections --memory ~/.claude/projects/<proj>/memory   # recommended
bash scripts/forge.sh --mode corrections --dry-run          # stop before eval spend
bash scripts/forge.sh --brief briefs/x.json --skill-dir drafts/y --samples 3   # eval only
bash scripts/forge.sh --brief briefs/x.json --skill-dir drafts/y --rival ~/.claude/skills/z
```

`forge.sh`: mine -> brief -> match -> score -> (draft) -> N samples per arm -> judge ->
aggregate -> gate. `FORGE_ADOPT_DIR` stages adoptions instead of installing to
`~/.agents/skills`.

## Knowledge-gap briefs (where skills win)

`brief.py --knowledge-gap` builds a task from a correction theme where the user's OWN
rules decide quality: realistic fixtures (a thread, notes, logs), a prompt in the user's
style that does not state the rules, and a Python verify of objective rule properties
(length caps, forbidden phrases, numbers not in the notes). Rules never go in fixtures,
so only a skill can carry them. The verify is self-tested before the brief is written:
it must pass the model's good example and fail its bad example, or the brief is rejected.

Brief fields: `{id, prompt, setup, verify, rubric, output}`. `verify` runs in the workdir
and exits 0 on acceptable output. When the deliverable is the agent's final chat reply,
verify reads it from `$FORGE_FINAL`.

## Runs on your own machine

No sandbox service, no account. Needs `python3`, `bash`, and a logged-in agent CLI -
`FORGE_AGENT=claude` (default), `codex` or `opencode` - so evals use your own
subscription or API key and your own session logs. Works on
macOS (falls back to `gtimeout` or a perl alarm when `timeout` is missing) and Linux,
or on your own cloud box. To watch and drive it in a browser, use **skill-cockpit**.

## The blind is enforced, not assumed

`judge.py` sees two anonymous slots, a random mapping kept on disk, each arm's final
message and its file list. Three things keep the arm identity out of that prompt, and
`tests/test_judge.py` pins all three on fixtures.

**The skill is found, not skipped by path.** Every runner installs the candidate
somewhere different (`.claude/skills`, `.agents/skills`, `.opencode/skill`), and the
manifest skipped the Claude path by name, so a Codex or OpenCode arm listed
`.agents/skills/<skill>/SKILL.md` in the judge's own prompt. The skill is now located by
its `SKILL.md` inside the arm's dot-directories and its whole subtree is dropped, so a
fourth runner cannot leak the same way. A `SKILL.md` the agent wrote as its deliverable
is not in a dot-directory and stays in the manifest.

**An arm that names the skill makes the pair invalid.** Hiding the files does nothing if
the agent writes "following the li-post-fede skill". That is not a blind verdict, so it
is recorded as invalid rather than as a win. None of the 45 real sample verdicts on the
live corpus ever named a skill, so this refuses nothing that has already been decided.

**A verdict the judge did not state readably is refused by name.** `"Run A (with the
skill)"` used to fall through to a tie, and a tie is enough for `--probation` to install
the skill: an unreadable reply could adopt something nothing had judged. The reply is
also parsed to the end of the first complete object, so a judge that answers and then
keeps talking still parses (the same defect `score.py` lost two real scores to).

## Optional: run the arms in containers (Harbor)

`run_eval.sh` runs both arms in directories on this machine. `run_eval_harbor.sh` takes
the same three arguments and writes the same layout, but hands each arm to
[Harbor](https://github.com/harbor-framework/harbor), which builds a container per trial
and injects the skill with `--skill`. `judge.py`, `aggregate.py` and `gate.py` read
either runner unchanged.

```bash
uv tool install harbor                      # once
FORGE_HARBOR_SUDO=1 \                       # where the docker socket needs root
  scripts/run_eval_harbor.sh brief.json with ~/.claude/skills/li-post-fede
```

**It buys the blind, not the budget.** In a without arm handed no skill none is injected, so
Harbor creates no skills directory and the container never receives the files. Probed on
a real run with the token-free `oracle` agent: the with arm's container holds
`/harbor/skills/<skill>/SKILL.md`, the without arm's has no `SKILL.md` and no directory
named `skill*` anywhere on its filesystem. The local runner instead put both arms under
one host tree and relied on the manifest to hide the skill, which is the thing that
leaked. Two properties of the generated task keep that true and `tests/test_harbor_task.py`
pins both: `environment.skills_dir` is never set (setting it creates the directory in
*both* arms, so the without arm gets an empty one the with arm has content in), and the
instruction is the brief's prompt verbatim, so it cannot say what Harbor's own
`hello-skills` example says: "You have a skill installed called ...".

**It also buys a second runner.** Twenty-four Harbor agents declare
`capabilities.skills`, including `codex`, `opencode`, `gemini-cli` and `cursor-cli`, and
each one knows its own install path. That is the knowledge `run_eval.sh` had to hardcode
and got wrong.

**Tokens come from a subscription, not an API key.** Harbor drops `ANTHROPIC_API_KEY`
when `CLAUDE_FORCE_OAUTH` is truthy and uses `CLAUDE_CODE_OAUTH_TOKEN`; Codex takes the
ChatGPT login through `CODEX_FORCE_AUTH_JSON=1`. The runner looks for the Claude token in
AgentWallet first, as `anthropic/oauth-token/claude-code`, which is where a long-lived
`claude setup-token` belongs. Failing that it reads the access token the CLI already keeps
in `~/.claude/.credentials.json` and refreshes by itself, so a host where nobody can finish
a browser login still runs. That file is only ever read; an expired token is treated as no
token, because the alternative is an opaque failure deep inside the container.
`FORGE_AGENT=codex` turns `CODEX_FORCE_AUTH_JSON` on the same way and stops if
`~/.codex/auth.json` is unreadable, rather than letting Harbor quietly fall back to an
`OPENAI_API_KEY`: that fallback does not error, it bills a key or runs unauthenticated and
resurfaces as a task failure that reads like the skill's fault. Set `CODEX_FORCE_AUTH_JSON=0`
to choose the API key deliberately.
The runner reads the token into the process and exports it, never passes it as an
argument, and under `sudo` names the variables that may cross rather than using `-E`.
This saves the API bill; it does not raise the weekly cap, which is the limit the loop
actually hits.

**A sudo run hands the job tree back.** With `FORGE_HARBOR_SUDO=1` Harbor writes its
whole jobs directory as root, and the step that pulls the workdir and the session log
into the arm runs as the invoking user. The first real container pair died there on a
`PermissionError` reading the agent's own transcript, with the run already paid for, so
the runner now chowns `$META/jobs` back before anything reads it.

**Keep it on local Docker.** `CODEX_FORCE_AUTH_JSON` uploads a live `auth.json` into the
sandbox and the OAuth token rides in the container environment, so Harbor's cloud
providers (Daytona, Modal, Blaxel) would ship a working credential to a third party.
Parallelism is the one Harbor feature this loop should not take.

**The objective gate stays on the host.** The generated task's verifier writes reward 0,
meaning "not scored"; the brief's `verify` is run by `judge.py` in the arm's workdir, the
same way it is for a local arm. A skill proven under Harbor has to be comparable to the
ten already adopted under the local runner, and two implementations of the gate would
make the two corpora measure different things.

## Three-tier gate

- **ADOPT** - with-arm wins the strict majority of blind samples AND passes verify AND
  makes no more tool errors than baseline. One sample is noise: run 3.
- **PROBATION** - eval is a clean tie but the production failure is real and
  costly. Context-rot failures (buried rules, long sessions, mid-flow shortcuts)
  CANNOT be reproduced in one-shot evals: frontier models pass fresh small tasks
  with or without a skill. Probation installs the skill with a 7-day recheck date.
- **REJECT** - everything else. Losers are recorded in `ledger.jsonl` and never
  re-evaled.

Neither adoption is available on fewer than two valid samples, whatever the winner
says. Three samples exist so that one lucky run cannot adopt a skill, and dropping the
invalid ones can quietly undo that: the majority is counted over valid samples, so a
brief that loses two of three to an invalid verdict is deciding on one run. That is not
hypothetical. `run-to-publishable-result` was adopted 2-1, and two of those three
samples were pairs whose with-arm never loaded the skill. Strip them and the adoption
rests on a single sample, which the majority rule was written to prevent.

## recheck.py (weekly)

Re-mines recent sessions and compares each skill's failure session-rate against its
adoption baseline. Dropped >=30% -> `adopt-confirmed`. No drop -> the skill is
uninstalled (symlinks unlinked, the copy moved to `$FORGE_ROOT/revoked/`) and the ledger
records `revoked`. Adopted skills get a 14-day recheck, probation 7: winning a rebuilt
eval task is not the same as reducing failures in real sessions.

Knowledge-gap skills have no tool-error signature to count, so they are measured on the
user's own corrections: `corrections.py --no-llm` re-extracts correction episodes and the
rate of corrections about that theme is compared on both sides of the adoption date, with
one matcher. A recheck never needs a model call.

Run `--dry-run` first on any machine where skills are installed: it prints every decision
and uninstalls nothing. Run it where the user actually types - a box that only runs
headless agents has no corrections to count, and the recheck will say so rather than
guess.

**A recheck never confirms or revokes on absent evidence.** No baseline, no recorded
signature, a baseline of zero, or too few sessions on either side of the adoption all
produce SKIP. The first version read "no signature" as a 0% failure rate and would have
confirmed three skills that had never been measured; the inverse bug would have
uninstalled six working skills because a rate of zero cannot drop by 30%.

Three more refusals come from watching the correction metric behave on real logs:

- **Less than five days of sessions since adoption -> SKIP.** A skill adopted this
  morning has no production record, and half a day of work cannot show a rate change.
- **Theme words that are common across all corrections are dropped before matching**,
  and a signature left with fewer than two distinct words is refused. Ordinary words
  ("post", "reply", "status") match nearly every correction, which returns noise
  wearing the costume of a measurement.
- **A signature matching on more than 20 distinct words is refused as too broad.**
  Whatever rate that produces is about vocabulary, not about one theme. On real data
  a signature lifted from a whole skill body matched 33-43% of all sessions; the three
  signatures mined as themes matched 5-18%.

A signature lifted from the skill's own description is refused on sight, however narrow it
looks. Width cannot tell prose from a theme: extending the stopword list pulled three
such signatures from 35-42 distinct words to 18-20, under the cap, without making one of
them more about a single theme. They describe the skill, not the mistake, so a verdict
from one would uninstall a working skill on the strength of its own marketing. Mine a
real theme with theme.py instead.

A single theme word is enough to count an episode when that word is rare in the corpus
(under an eighth of episodes); otherwise two must match.

**The denominator holds only sessions that could have carried a correction.** An episode
needs a previous user turn and a previous assistant turn, so a one-shot question cannot
produce one however badly it went. Counting those measures the window's mix of work
instead of the skill, and that mix moves: across the real adoption date the share of
single-turn sessions fell from 70% of the window to 6%, which by itself took the raw rate
from 22% to 75%. The verdict reads a rise like that as the skill making the agent worse,
so the shipped denominator was one week away from revoking ten working skills over a
change in what the days looked like. The floor is the extractor's own, not a tuned one,
and on two independently mined corpora it discarded no session that carried an episode.

The floor does not make what is left comparable, because the rate keeps climbing with
length past it - 0% at two turns, 92% past twelve. So each window's expected rate is read
off session lengths alone and the two are compared **using the same factor the verdict
turns on**: if length by itself can move the rate that far, there is nothing left for the
skill to be measured by, and the recheck says so. Tying the guard to that factor instead
of giving it a threshold of its own is deliberate - it fires exactly when the confound is
big enough to produce the verdict. On the real corpus the shipped denominator shifts
2.5-3.5x depending on the adoption date, and the floored one 1.1-1.2x.

**A rate that improved while the skill was never loaded confirms nothing.** Every guard
above asks whether the rate moved; none of them asked whether the thing under test ever
ran. A skill only reaches the model when it is loaded, so a drop across a window that
never loaded it is a drop with some other cause - a quiet week, the theme not coming up,
the work moving on - and writing `adopt-confirmed` on it records a win the skill had no
part in. The session index now carries the skills each session loaded, and a drop with
zero loads is a SKIP. Not a revoke: a skill that never ran has not failed, it has had no
chance, so the entry stays due for a window that does load it. Every verdict carries the
count either way, because a confirmation that says how many times the skill actually ran
is evidence and one that cannot is a rate with a story attached.

This is not hypothetical here, and measuring it properly took two passes. The first read
300 sessions from the user's own home and found the seven skills adopted on 17 Sep loaded
**zero** times, which turned out to be the wrong corpus: those skills are installed only
under root's home, so nothing in that corpus could have loaded them whatever their
descriptions said. Re-measured on root's own 300 sessions, where they are installed and
where the recheck timer actually runs, the zero mostly holds and now means something. Six
of the seven have not been loaded once in the 16 to 20 sessions since adoption; the
seventh, which existed before the loop adopted it, was loaded once. In the same corpus
twenty other skills were loaded forty times between them, so the zero is about those six
and not about whether loads get recorded at all. Without this guard the 1 Oct recheck
could have confirmed all of them on a rate that moved for reasons none of them touched.

**Which is why a zero says which kind of zero it is.** Nothing loaded it has two causes
that look identical in the count and need opposite fixes: the skill is installed where
the sessions ran and the model passed it over, which is a description problem, or it is
not installed in a root those sessions could reach, which is plumbing and says nothing
about the skill. `installed()` checks the same two roots `uninstall()` would clear and
the SKIP message names which case it is. A negative there is weaker than a positive, since
the recheck sees its own roots and not those of whoever typed the sessions, so it only
ever colours the message and never decides one.

The descriptions turned out not to be the obvious culprit either: all six name task
triggers rather than the error they prevent, which is the failure mode this loop already
warns about. What three of them share instead is that their trigger is the agent's own
closing message, and a model does not stop to look for a skill before replying. That is a
live question, not a conclusion.

```bash
python3 scripts/recheck.py --usage    # loads since adoption, per open entry, decides nothing
```

`--usage` asks the load question early, while a zero is still fixable, and covers every
open entry rather than only the ones a date has come due for. It is the hand measurement
above turned into a command, sorted so the zeros come first.

The count reads low rather than high when it is wrong, which is the right way round for
something that can only withhold a confirmation. Codex transcripts record no skill call
at all, so a window that is mostly Codex reads zero however much the skill ran, and that
costs a SKIP and a later recheck, never a revoke. Both other spellings had to be read off
real sessions rather than assumed: Claude Code calls the tool `Skill` and names the skill
in `skill`, OpenCode calls it `skill` and names it in `name`. The first version of the
parser read only Claude's, and downstream that does not look like a parse bug - it looks
like a skill nobody used.

`tests/test_recheck.py` pins all of it down on fixtures - stdlib only, no model calls,
no network - including the symlinked uninstall, both zero-evidence skips, the recency
guard, the length floor and shift guard, a real drop, the same drop withheld when
nothing loaded the skill, and each kind of zero naming itself.
`../skill-miner/tests/test_corrections.py` pins every spelling
the loads are read from. Every case in both is a bug that reached real data first.

## backfill.py

`backfill.py` gives already-adopted skills something to be measured by: skills forged
from hand-written briefs carry no failure record, so the recheck would skip them
forever. It lifts the theme back out of the installed SKILL.md - the front-matter
description plus the user's own quoted corrections - and writes it onto the ledger row
tagged `derived_from: skill_md:<path>`. That is a matcher, never a measurement, and the
recheck's guards still decide whether it is good enough to use. `--apply` backs the
ledger up first; `--redo` re-derives signatures it wrote before.

## theme.py: when the skill has no theme worth measuring

`backfill.py` lifts a theme out of a skill's own prose, and for voice and format skills
that prose is long and ordinary: matched against real sessions those signatures claimed
33-43% of every correction the user ever made, so the recheck refuses them, correctly
and permanently. `theme.py` looks for the theme where it actually lives, in the
corrections themselves: seed from the skill, pull the episodes those seeds match, rank
the words those episodes keep returning to, then check the result is narrow, still on
the skill's subject, has a baseline before the adoption date, and is not the same
matcher another skill already has.

Expect it to refuse. Against 136 real correction episodes it derived nothing for seven
adopted skills, each for a different stated reason, and that is the finding rather than
a bug: a voice skill is corrected in words too ordinary to separate from every other
correction.

More correction history looked like the fix, so it was tried: a corpus of 340 episodes
across 296 sessions, two and a half times the size. It derived nothing there either,
and on the way it exposed two bugs the smaller corpus had hidden. So the answer does
not turn on corpus size, and a looser matcher would only return a number about the
vocabulary. Six things it took to get here, all pinned in `tests/test_theme.py`:

- **Ranking by lift is the textbook answer and carries zero information here.** In a
  136-episode corpus almost every content word inside a 30-episode subset appears
  nowhere else, so every candidate scored the identical lift of n_all/n_seed. Ranking
  now uses within-theme document frequency, which the corpus can actually support.
- **Statistics cannot tell filler from subject.** The first signatures out of the new
  ranking were "but can dont have", then "post real" - each passing every check while
  being about nothing. Fixed by extending the recheck's stopword list with English and
  German function words (the user corrects in both) and requiring at least four
  recurring words.
- **A corpus-driven theme can drift off the skill entirely.** For a skill about reusing
  existing assets it derived a real, coherent topic cluster about one website's pages.
  The derived words now have to overlap what the skill says it is about.
- **Overlapping the description is not enough, and the same case proves it.** A
  description names its subject once and spends the rest on context, so "find", "posts"
  and "visuals" were all in it while "reuse", "existing" and "assets" appeared 0-1 times
  in the whole corpus. Rarity cannot separate those either: at 136 episodes every seed
  word sits under the rare threshold. The overlap now has to include the thing the skill
  is *named* after, matched on a shared prefix so `german-umlauts` still matches the
  corpus word "umlaute".
- **A floor set as a share of the seed gets worse as the corpus grows.** Tripling the
  corpus took one skill's seed from 58 episodes to 135, so a 20% floor moved from 11 to
  27 while its most distinctive word only moved from 6 to 15: the theme word was
  discarded for being outnumbered by a seed that was too broad to begin with. The floor
  is now absolute, and the breadth it was standing in for is refused directly, one step
  earlier, by `MAX_SEED_SHARE`.
- **Two skills can pass every check and be one matcher.** On the 340-episode corpus four
  of them returned the same share and the same before/after counts to the episode,
  because all four were matching one generic cluster of content work. Comparing the
  signatures word by word misses it - two of the four shared 3 words out of 17, a
  Jaccard of 0.18 - because synonyms read as distinct vocabularies. Compared on the
  sessions each one actually matches, the same pair overlaps 74% and both are refused.

`--apply` writes the signature tagged `derived_from: corrections:<n> episodes`, so it
is never mistaken for a hand-written one, and the recheck still applies every one of
its own refusals to whatever comes out. A signature that passes the statistics and
fails inspection does not get applied.

## deploy.sh

`deploy.sh [--to host]` copies these skills from a checkout to an install root and
verifies each tree by digest. The loop forges skills for other tasks and had no way to
ship itself: a laptop running a three-day-old `mine.py` failed only when the timer
fired, with `unrecognized arguments: --sources`.

## Hard rules (all learned from real eval failures)

- **Blind judging is non-negotiable.** Arm identity lives in
  `mapping.private.json`; the judge sees only slot A/B.
- **Both arms failing verify means the brief is broken** - judge marks the eval
  `invalid`, never picks a winner over two broken runs. Fix the eval, not the loop.
  Twice in a row also stops the brief, because a gate nothing passes costs half an
  hour per arm to keep saying so. Not on the first: one such sample cannot tell an
  unpassable gate from a strict but passable one that this pair missed, and the
  next sample under the second is a verdict that stopping would have thrown away.
  `invalid_code` separates the two invalid verdicts, because the other one is
  chance and the next pair may well be blind, so it never stops anything.
- **An arm whose agent never started is a runner fault, and the record has to say so.**
  A Harbor binary that was not on the sudo PATH made both arms exit 127 in two seconds
  with empty transcripts. Every downstream check read that as work: verify failed in
  both arms, so the verdict came back `both_arms_failed_verify`, whose own text says
  "fix the brief, not the loop". The brief was fine, and the loop said this twice,
  spending a judge call on two empty workdirs each time. `invalid_code: arm_never_ran`
  now names it, and the check runs before the blind mapping is drawn and before the
  model is called. It needs all three signs together - a non-zero runner exit, an
  empty transcript, and no final message - because each alone has an innocent reading:
  a timeout after real work, a runner that writes no transcript, an agent that only
  edited files. Unlike a failing gate this stops the brief on the first sample, since
  a runner that could not launch an agent will not launch one on sample two either.
  Those three signs were read off a Harbor arm and they missed the next one. When the
  CLI itself fails it still writes its init line to the transcript and still writes a
  final message, the failure text, so an arm can be dead with neither an empty
  transcript nor a missing final message. Both arms of the first rival pair came back
  exit 1 with `Failed to authenticate: OAuth session expired and could not be
  refreshed` as their answer, and nothing above fired. That pair survived only because
  the judge's own model call was failing on the same credential; with a working judge
  it would have been scored as two agents answering the brief with the same sentence,
  and the loop would have blamed the brief a third time. The second reading catches
  it: `run_eval.sh` copies the CLI's error into `run.json` and `-o` writes the same
  text to `final.txt`, so a final message that starts with the runner's recorded
  error is the runner talking and not the agent. Compared by prefix, because
  `run.json` keeps 300 characters. A timeout after real work still reads as a real
  arm: its error comes from stderr and no agent answer opens with it. The reason text
  says which of the two shapes it saw, so nobody goes looking for a missing file over
  an expired credential.
- **Guard the directory the judge reads from, not the one the agent writes in.** Both
  runners refused to start when the arm's workdir already existed and said nothing
  about `<arm>.meta` next to it, which is the half the verdict is actually built from:
  `final.txt`, `transcript.jsonl`, `run.json`. The run truncates three of those and
  never touches the fourth, because only the codex arm writes `final.txt` at all, so a
  run into a `.meta` an earlier pass left behind is judged on the earlier pass's
  answer. That is the failure above with the evidence pointing the other way. There a
  dead arm answered with the runner's own error and could be caught by reading it;
  here it answers with a real reply a real agent really wrote, and nothing downstream
  can tell. The workaround in use was renaming the brief, which puts two ids in the
  ledger for one question, so the refusal now says to delete the sample dir instead.
  It refuses rather than cleans: the earlier run is evidence until somebody has read
  it.
- **A verify that reads prose punishes the arm that explains itself.** A brief checked
  the agent's reply for banned fonts and failed the arm that had the skill, on its own
  sentence saying AX41 has no Arial. The skill's whole effect is to make an agent state
  which faces it chose, so the better the skill worked the more certainly the check
  failed it, and the pair was filed as `both_arms_failed_verify`: two Opus runs, and a
  clear win recorded as the brief being too hard. Check the delivered artifact, and
  where the brief asks for it in the reply, check the delivered document inside the
  reply and not the sentences around it. Strip comment spans before matching, not
  comment lines: the line that failed was the fourth line of a `/* ... */` listing the
  faces that were rejected, and a per-line test sees only the opening. Fixed, the same
  two stored replies score with-arm clean and without-arm five real violations.
- **A with-arm that never loaded the skill is not a with-arm.** Installing a skill in
  the arm does not load it; the model still chooses it from its description, exactly as
  in production. When it does not choose it, both arms ran the same task with the same
  model and the same tools, and whatever the judge preferred it was one run over
  another. Scored as a win it credits a skill that never executed, which is precisely
  the defect the production recheck fixed on its own side while this side kept doing
  it: three of 39 real with-arms, in both of the briefs whose skill was then adopted.
  The pair is marked `invalid` with `invalid_code: skill_never_loaded`, and it stops
  nothing - the next sample may well load it.
- **A skill handed to a container is installed, even though the host workdir is empty.**
  The installed-skill scan walks the arm's workdir, and `run_eval_harbor.sh` never puts
  the skill there: it resolves it into `<arm>.meta/skill/<name>` and hands that to
  Harbor, which mounts it inside the container. So every Harbor with-arm read as an arm
  with no skill installed, and two of the three integrity checks went quiet on it. With
  no installed name, the never-loaded check cannot fire and the blindness check has
  nothing to match, which means no Harbor pair could ever have been refused for either.
  The first real one proved it: `skills_installed {"with": []}` for an arm whose own
  container transcript carries a `skill_listing` naming the skill. The scan now also
  reads what the runner handed over, and the workdir copy still wins where both exist,
  because that is the tree the agent actually read.
- **A silent arm outranks a gate both arms failed.** `both_arms_failed_verify` used to
  win that tie and its text says "fix the brief, not the loop", which on the first
  Harbor pair was advice about a brief the local runner passes three times out of
  three: with-arm 91, 82 and 88 words against a baseline's 310, 312 and 280, under the
  same 150-word gate. The Harbor with-arm wrote 194 because it never loaded the skill,
  and that skill's entire job is to make the reply short, so the gate did not fail
  independently of the silent arm, it failed because of it. A gate never once tested
  with the skill in place says nothing about the brief. Which code comes out also
  decides whether the brief survives: two `both_arms_failed_verify` in a row stop the
  run, so a skill that keeps failing to load would retire its own eval with the log
  blaming the brief, while `skill_never_loaded` stops nothing. The verify failure stays
  in the reason rather than being dropped, because the two facts together are what says
  the gate is still unmeasured.
- **A win over an empty machine is not the comparison adoption rests on.** Every arm
  the loop has run had one skill installed on the with side and none on the without
  side; the skill is then adopted into a fleet of 314 where several others answer the
  same trigger, and there the model picks between them. The gap is measurable: the
  seven skills adopted so far load 18 of 21 times in their own evals, where each is the
  only skill installed for the trigger, and once in 189 real sessions. Not the only
  skill on the machine, which is what this said until the inventories were read: the
  AX41 CLI offers every arm 18 bundled skills and Harbor's image 13, so the candidate
  already competes with a dozen-odd generic ones. It competes with none that answer
  its own trigger, and that is the whole of the gap. On the same subject,
  `fede-linkedin-post` was loaded 8 times in 1041 recent sessions while `li-post-fede`,
  installed in the same two roots, was loaded 0. `--rival PATH` installs the incumbent
  in the baseline arm, which is the head-to-head the adoption actually needs.
  The baseline is then held to the same bar as the candidate: a rival the model never
  loaded makes the pair `invalid_code: skill_never_loaded` naming that arm, because a
  baseline that ignored its skill is the empty machine again. Every ledger row carries
  `baseline_skills`, read off the run rather than off the flag, and `--rival` against a
  baseline that installed nothing stops the gate rather than recording a contest that
  did not happen. An empty list is the honest reading of every row written before the
  field existed, and the adopt line says "over an empty baseline" out loud.
- **A guard that reads a field nobody writes refuses everything, and its tests will not
  say so.** The `--rival` check above shipped reading `skills_installed` off the
  aggregate verdict. `judge.py` writes that field per sample, `aggregate.py` did not
  carry it, and `gate.py` reads only the aggregate - so the check read an absent field
  as an empty baseline and refused every head-to-head it was ever given, for eleven PRs,
  with the one message no operator can act on: rerun an eval whose samples were already
  right. The first real one was a 3-0 whose three samples each record the incumbent
  installed and loaded in the baseline arm; the queue log ends `END rival rc=1`. Four
  tests covered the guard and all four passed, because each one hands `gate.py` a
  verdict dict the test built, carrying a key no producer writes. A fixture that
  fabricates its producer's output tests the consumer against a format, not against the
  system. Where two scripts meet over a file, one test has to run both - `RivalEndToEnd`
  is that test. And a verdict that does not record what the arms were given is not a
  verdict that records an empty baseline: the two readings get different messages now,
  because only one of them is fixed by re-aggregating, which re-reads the stored samples
  and spends no eval. The field is read off every sample rather than the valid ones, and
  samples that disagree about what an arm was given stop the aggregate instead of being
  merged, since those are two experiments and not one comparison.
- **An incumbent the model never reaches for is a result, not a sample to rerun.** With
  the guard above working, three head-to-heads ran and two produced no verdict: the
  skill installed in the baseline arm was not loaded, in 3 of 3 samples for one brief
  and 2 of 3 for the other, each time installed alone on the machine, on a task its own
  description claims. `gate.py` answered both with "fix whatever invalidated the others
  and rerun the brief" - which names the candidate, and asks for an hour an arm to
  reproduce something that was not a fault. Nothing about those runs was wrong. What
  they measured is the production zero this loop keeps finding weeks later in real
  sessions, reproduced inside the eval where it can be worked on, and it is a
  measurement of the incumbent rather than of the candidate. `aggregate.py` now counts
  silent arms per side into `arms_never_loaded`, the gate says which skill was passed
  over and drops the rerun instruction when that is the reason, and the count rides onto
  the ledger row so the pattern accumulates. Two details carry the honesty: the count is
  derived from the three facts the sample verdict already stores rather than from a new
  field, so it answers for runs already in the archive and costs no eval; and
  `never_used_its_skill` is called by both stages rather than restated in the second,
  because the rule that invalidates a pair and the rule that explains a missing verdict
  must not drift into disagreeing about one run. A runner that records no skill call at
  all is never counted - that zero is unknowable, and a finding invented by a transcript
  format is worse than no finding.
- **Picking a rival by reading two descriptions is the method this loop already
  disproved.** `run-to-publishable-result` was paired against `tldr-replies` because
  both read as end-of-turn status-message skills. It loads 3 of 3 on its own brief and 0
  of 3 as the baseline on the other, so two triggers that a reader cannot tell apart are
  not one trigger to the model. Same failure as matching themes by word overlap: the
  description is not the behaviour.
- **Read what the agent was offered, not only what you installed.** Every other check in
  `judge.py` reads the harness's own installs, so they all agree with each other by
  construction, and none of them can see an ambient copy: a skill already on the host or
  baked into the container image is advertised to both arms and installed by neither.
  The without-arm is then a second with-arm and the pair measures nothing. Nothing has
  gone wrong yet and the measurement is what says so rather than a guess - all 53
  real without-arms on AX41 whose runner writes an inventory were read, and not one
  advertised the skill its pair was testing. The reason this said, when it shipped, is
  the wrong one: it argued that adoption ends in deployment and the loop's own four
  skills sit in `~/.agents/skills` exactly the way an adopted skill will, so the first
  recheck over a deployed skill would read as a skill that stopped working. Measured
  since, that mechanism does not fire. `run_eval.sh` launches the CLI with
  `--setting-sources project,local`, which never loads the user scope: those four
  skills and eighteen others sit in the eval user's own `~/.agents/skills` and not one
  of the twenty-two was offered to any of the 100 archived arms. What the loop deploys
  is invisible to what the loop measures. The live ways in are the ones left - a skill
  baked into a container image, a project-scope install under the run root, a workdir
  the harness populated twice - and the guard is worth having for those, not for the
  one it was written about. `advertised_skills` reads the inventory
  per runner, off two shapes that are both in `runs/` today: the host CLI writes a
  `skills` list on the `system/init` line, the SDK CLI inside Harbor a `skill_listing`
  attachment with `names`. A runner that writes neither returns `None`, which is an
  unknown inventory and not an empty one - Codex records no listing at all, and reading
  its silence as "offered nothing" would clear every Codex baseline unchecked. What the
  baseline was handed is subtracted first, because `--rival` and the populated-fleet
  baseline both give it a skill on purpose. `invalid_code: baseline_had_the_skill`
  stops the brief on the first sample the way `arm_never_ran` does: an ambient install
  is still there for samples 2 and 3.
- **An arm the clock killed is not an arm that failed the brief.** Both leave a
  non-zero verify and a final message, and `both_arms_failed_verify` swallowed the
  difference - its reason line says "fix the brief, not the loop", and no rewrite of a
  brief buys it more time. `edge-launch-intro-scene-ax41` is the pair that showed it:
  sample 1 had both arms exit 0 and both fail verify, a gate nobody passes; sample 2
  had the without-arm finish in 1130s and the with-arm killed at the 1200s cap,
  mid-sentence on "Now rendering...". Both were filed under the same code, and the two
  together tripped the two-in-a-row rule and retired the brief with a message blaming
  it. Only one of the two was a measurement. `invalid_code: arm_timed_out` fires on
  exit 124 (`timeout(1)`) or 142 (the perl `alarm` fallback's SIGALRM), and only when
  that arm also failed verify: an agent cut off at the cap whose work still passes the
  brief's own gate is done by the only definition the brief offers, and throwing that
  pair away would discard a real verdict over the runner's bookkeeping. `run_eval.sh`
  records the cap it ran under as `timeout_s`, so the reason can name it - 1200s on a
  brief that renders video is a different problem from 1200s on one that edits a file.
  In `forge.sh` it is its own streak: it does not count as a failed gate and it does
  not clear one, because it says nothing either way about whether the brief is
  passable. Two in a row still stops the run, since a brief that cannot finish inside
  the cap will not finish inside it on the third try. One pair in the archive has a
  cut-off arm and it is the one that showed this, so nothing else on the record was
  miscoded - which is why the fix is a guard for the next one rather than a rescoring
  of the last 45.
- **A zero load is only evidence where the runner records loads.** Claude Code emits a
  `Skill` tool call with the name in `skill`, OpenCode a `skill` part with the name in
  `state.input.name`, and Codex records nothing at all. Enforcing on a Codex zero would
  invalidate every Codex sample the loop ever runs, so the check carries whether the
  zero is knowable and declines to fire when it is not. Guessing at these spellings has
  produced the same bug three times here, most recently in the measurement that found
  this one: a first pass over the archive reported six silent arms and three of them
  were OpenCode arms that had loaded the skill under a spelling the grep did not know.
- **The eval's own load rate rides on the ledger row.** `skill_loads` counts how often
  the model reached for the skill when it had it, over every sample rather than the
  valid ones - a sample thrown out *for* never loading it is the clearest instance of
  the thing being counted. It decides nothing. It is the eval-side answer to the
  question `recheck.py --usage` asks of real sessions weeks later, available at
  adoption instead of on the recheck date.
- **Evals need headroom and pressure.** Toy tasks don't reproduce real failures.
  But note the one-shot ceiling: recoverable single-turn errors never show skill
  value - only silent-wrong-output and knowledge-gap failures discriminate.
- **Copy skills with `cp -rL`** - production skills are often symlinks; a plain
  copy gives the with-arm a dangling link and a silent no-skill run.
- **Verify only what the prompt explicitly asks**, tolerate formatting variation.
- **Share one baseline across candidates** for the same brief: copy `without` +
  `without.meta` per sample instead of re-running it.
- Budget: each sample is two headless agent runs. `FORGE_MODEL`, `FORGE_TIMEOUT`,
  `FORGE_SAMPLE` control cost and layout. Default sonnet, 1200s.

State: `$FORGE_ROOT` (default `~/skill-forge`) - runs/, ledger.jsonl.
