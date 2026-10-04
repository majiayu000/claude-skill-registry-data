---
name: reasoning-effort-throttle
description: Stop paying for deep reasoning on easy turns by setting a modest default reasoning effort and escalating per task. Use when the user runs a reasoning model in an agent and the bill is dominated by output or thinking tokens, or asks about reasoning_effort, thinking budgets, or why a cheap model is still expensive to run.
---

# Don't pay for deep thinking on easy turns

Reasoning effort is mostly output tokens, and output tokens are usually the expensive direction, so the effort knob is often the single biggest lever on an agent's bill, bigger than switching models. A cheap model at maximum effort can out-spend a mid model at low effort. Your job is to set a sane default, define when escalation is earned, and validate the config actually says what the user thinks it says.

## Steps

1. Confirm the user's harness supports per-task effort control. The worked example is Hermes (levels: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, switchable at runtime with `/reasoning xhigh`, no restart); Claude Code, the Claude API's thinking budgets, and most agent runtimes have an equivalent. If theirs doesn't, effort throttling means routing between the same model's endpoints at different configured efforts.
2. Set the default one notch below the maximum the user has been running, not at the bottom. The reference setup (as of 2026-06): DeepSeek V4 Flash at $0.098/M in, $0.196/M out on OpenRouter; default `high`, reserve `xhigh` for turns that earned it. Check current prices before quoting.
3. Define "earned" concretely so escalation is a rule, not a mood: a failed first attempt, a task the user tagged hard, a step with irreversible consequences. Everything else runs at the default.
4. Run the proof below; it validates the config parses and the effort level is one the harness actually accepts (a typo'd level silently falls back to a default you didn't choose). The example uses ruby's stdlib YAML parser; if ruby isn't on the machine, any YAML parser serves, since the point is proving the file parses and the level is a real one.
5. After a week, check what fraction of the bill is output tokens at each effort level. If `xhigh` turns are more than ~10-20% of traffic, either the work is genuinely hard (fine, see `advisor-call-budget` for the next lever) or the escalation rule is too loose.

## Prove it

```bash verify
cat > config.yaml <<'YAML'
model:
  provider: openrouter
  model: deepseek/deepseek-v4-flash
agent:
  reasoning_effort: high
YAML
ruby -ryaml -e '
allowed = ["none","minimal","low","medium","high","xhigh"]
c = YAML.load_file("config.yaml")
m = c["model"] || {}; a = c["agent"] || {}
abort "BAD: no model set" unless m["model"].to_s.length > 0
re = a["reasoning_effort"].to_s
abort "BAD: reasoning_effort #{re.inspect} is not a valid level" unless allowed.include?(re)
puts "throttle OK: " + m["model"] + " with default reasoning_effort=" + re + " (escalate per task, not globally)"
'
```

## Guardrails

- Leaderboard entries named "Max" and "High" are frequently the same model at different effort settings, not different models. Check before concluding a model got beaten.
- The savings are workload-dependent. Effort throttling pays when traffic is mostly easy turns with occasional hard ones; a workload that is uniformly hard just needs the effort, and pretending otherwise trades money for silent quality loss.
- CI-style validation proves the config, never the spend. The only honest savings number comes from comparing the bill before and after, same workload.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [A one-line reasoning-effort throttle](https://flowstacks.xyz/workflows/hermes-deepseek-v4-flash-effort-throttle)</sub>
