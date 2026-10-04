---
name: tested-fallback
description: Pin an open-weights fallback model with a tested-on date and real smoke prompts, so a pulled or deprecated model is a two-minute config swap instead of a lost week. Use when the user worries a model could vanish or be deprecated, builds anything important on one model, or asks about model failover and resilience.
---

# A backup you never ran is a hope

Models vanish for reasons outside anyone's control: export controls pulled Fable 5 days after launch, and ordinary deprecation calendars retire models constantly. The user's exposure isn't "will it happen" but "how big is the blast radius when it does". Your job is to shrink that radius to a one-line config change, and to refuse the most common self-deception in this area: a fallback that's listed but has never actually been run.

## Steps

1. Route through an OpenAI-compatible gateway `base_url` rather than a hard-wired provider endpoint, so the swap is a config edit, not a code change.
2. Name the primary model. Then pin a fallback that satisfies all four conditions:
   - **different** from the primary (obvious, and still worth checking),
   - **open-weights**: a hosted proprietary fallback can be recalled by the same forces that took the primary; open weights cannot be un-published,
   - **a `tested_on` date**: when the user last actually ran it,
   - **the smoke prompts they ran**: the 2-5 prompts that represent the work that matters.
3. If any of the four is missing, the config is not done. In particular: if they have never run the fallback, run the smoke prompts now (or schedule it), then record the date. Do not write a `tested_on` date for a test that didn't happen.
4. Run the proof below; it refuses a fallback that is untested, hosted-only, or identical to the primary.
5. Put the rehearsal on a schedule (monthly is fine): re-run the smoke prompts through the fallback, update `tested_on`. Keep prompts and context in a portable form so the switch is copy-paste, not a rebuild.

## Prove it

```bash verify
cat > failover.json <<'JSON'
{
  "base_url": "https://openrouter.ai/api/v1",
  "primary": "anthropic/claude-fable-5",
  "fallback": {
    "model": "z-ai/glm-5.2",
    "open_weights": true,
    "tested_on": "2026-07-01",
    "smoke_prompts": ["summarize this ticket", "extract the invoice fields", "draft a reply in my voice"]
  }
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("failover.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
if (!c.base_url) bad("no gateway base_url (route through a gateway, do not hard-wire a model)");
if (!c.primary) bad("no primary model set");
const f = c.fallback || {};
if (!f.model) bad("no fallback model set");
if (f.model === c.primary) bad("fallback must differ from the primary");
if (f.open_weights !== true) bad("fallback must be open-weights (a hosted fallback can be recalled too)");
if (String(f.tested_on || "").split("-").length !== 3) bad("fallback needs a tested_on date (a backup you never ran is a hope)");
if (!Array.isArray(f.smoke_prompts) || f.smoke_prompts.length < 1) bad("fallback needs at least one smoke prompt you actually ran");
console.log("failover OK: primary " + c.primary + ", tested open-weights fallback " + f.model + " (tested " + f.tested_on + ", " + f.smoke_prompts.length + " smoke prompt(s))");
'
```

## Guardrails

- Open-weights does not mean frontier. The biggest open models need serious hardware; the realistic fallback is a smaller open model or a cheap cloud host, not a home rig matching a flagship. Set that expectation when you pin it.
- The gateway is itself a dependency: one more company whose terms can change. It shrinks switching time; it does not remove risk. Say so.
- Never build anything important on a preview model; previews get the shortest-notice removals. Prefer generally-available models with a published deprecation policy.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Route through a gateway with a tested open-weights fallback](https://flowstacks.xyz/workflows/model-failover-tested-open-fallback)</sub>
