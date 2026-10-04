---
name: orbit-uat-agent
description: Natural-language UAT runner — Stagehand / Browser Use style. Reads the plugin code, infers user flows, generates plain-English test steps ("log in as admin → open Settings → fill API Key → save → verify saved"), executes via Playwright + AI-resolved selectors that survive UI changes. Self-heals when the DOM shifts. Use whenever the user wants UAT without writing specs, says "test my plugin", "run UAT", "natural language test", "auto-generate flows".
argument-hint: <plugin-path>
---

# 🪐 orbit-uat-agent — The brainless UAT runner

> Why write Playwright selectors that break on every redesign?
> Describe the flow in English. The agent figures out the rest.

This is the skill that makes UAT actually brainless for non-engineers on the user's team.

---

## Runtime — fetch live before auditing (DO THIS FIRST)

Before generating tests:

1. **Fetch in parallel** to ground the agent in current best-practice:
   - https://www.browserbase.com/stagehand → current Stagehand primitives
   - https://playwright.dev/docs/intro → current Playwright API
   - https://github.com/browserbase/stagehand/blob/main/README.md → integration patterns

2. **Synthesize**: which primitive (`act`, `extract`, `observe`, `agent`) fits which step type?

3. **Apply** — generate test scripts using today's recommended Stagehand API.

---

## What it does

### 1. Reads the plugin
- Parses PHP for menu pages (`add_menu_page`, `add_submenu_page`)
- Parses for shortcodes, blocks, REST routes, AJAX actions
- Parses for forms (input fields, save buttons, validation hooks)
- Reads any existing user-flow docs (`docs/user-flows.md` if present)

### 2. Generates flows in English
For each detected user-facing surface, creates a flow:

```
Flow: "Save plugin settings"
Steps:
  1. Log in to WP-Admin as administrator
  2. Click "My Plugin" in the admin nav
  3. Verify the Settings page loaded
  4. Fill the "API Key" field with "test-uat-key-001"
  5. Click "Save Settings"
  6. Verify a success notice appears containing "Settings saved"
  7. Reload the page
  8. Verify the API Key field still shows "test-uat-key-001"
```

Each step is an English sentence — no CSS selectors, no XPath.

### 3. Executes via Stagehand (or fallback)

```js
import { Stagehand } from "@browserbase/stagehand";

const stagehand = new Stagehand({
  env: "LOCAL",  // or BROWSERBASE for cloud
  modelName: "claude-sonnet-4-6",
});
await stagehand.init();

// Each English step → AI-resolved action
await stagehand.page.act("Log in to WP-Admin as administrator");
await stagehand.page.act("Click 'My Plugin' in the admin nav");
await stagehand.page.act("Fill the 'API Key' field with 'test-uat-key-001'");
await stagehand.page.act("Click 'Save Settings'");

const success = await stagehand.page.observe("a success notice containing 'Settings saved'");
if (!success) throw new Error("Save success notice not visible");

await stagehand.page.reload();
const value = await stagehand.page.extract({
  instruction: "the value currently in the API Key field",
  schema: z.object({ apiKey: z.string() }),
});
expect(value.apiKey).toBe("test-uat-key-001");

await stagehand.close();
```

### 4. Self-heals on DOM changes
**Whitepaper intent:** Traditional Playwright tests break when devs rename a button. AI-resolved selectors survive — "Save Settings" still finds the new `data-cy="save-settings"` button as long as the visible text or role is similar.

When a step fails, the agent:
- Re-tries with broader matching (role-based, text-similarity)
- Logs which selector strategy actually worked (so a future dev can codify it if they want determinism)
- Falls back to manual instruction if all strategies fail

### 5. Hybrid mode (deterministic + AI)
Stable flows (login, save, navigate) use deterministic Playwright selectors for speed. Volatile flows (custom widget canvas, modal interactions) use AI primitives. ~$0.01-0.05/test in LLM cost — pennies vs the dev hours saved on test maintenance.

```js
// Deterministic for known-stable
await page.fill("#user_login", "admin");
await page.fill("#user_pass", "password");
await page.click("#wp-submit");

// AI for volatile
await stagehand.page.act("Drag the My Hero widget into the page canvas");
```

---

## Why this is the brainless agent

The user's team — a designer, a PM, a junior QA — can run:

```
/orbit-uat-agent ~/plugins/my-plugin
```

And get:
- Auto-generated test plan in English
- Tests run + record screenshots / video per step
- Pass / fail report with the specific step that failed (in English)
- A flaky-test self-heal try before reporting failure

No selector-writing, no Playwright knowledge, no CSS expertise. Just: does the plugin work the way a real user would expect?

---

## Output

```markdown
# UAT Agent Report — my-plugin · 2026-04-30 (Stagehand v3.x, fetched today)

## Flows tested: 14
- ✅ Save plugin settings (8 steps, 12s)
- ✅ Reset settings to defaults (5 steps, 7s)
- ❌ Bulk-import via CSV (failed at step 5)
   → Step 5 was: "Click the Import CSV button"
   → No element matched that description.
   → Tried 3 strategies: aria-label, role+text, visible text near upload input
   → Manual screenshot: reports/uat-agent/flow-bulk-import-step5-failure.png
   → Suggestion: button label may have changed. Inspect the page manually.
- ✅ ... (11 more)

## Self-healed
- 2 selectors auto-recovered after DOM changes (settings-tab, support-link)

## Cost
- 47 LLM calls @ $0.01-0.05 each = $0.94 total
```

---

## Configure flows manually (override auto-generated)

If the auto-detected flows miss something, write a YAML:

```yaml
# uat-flows.yaml
flows:
  - name: "Buy a product"
    steps:
      - "Go to /shop/"
      - "Click on a product card"
      - "Click 'Add to cart'"
      - "Go to /checkout/"
      - "Fill billing details with realistic-looking data"
      - "Pick the test payment method"
      - "Click 'Place order'"
      - "Verify a 'Thank you' message appears"
```

Then:
```bash
/orbit-uat-agent ~/plugins/my-plugin --flows uat-flows.yaml
```

---

## Stagehand vs Playwright vs Browser Use — which does the agent pick?

| Tool | Picks when |
|---|---|
| **Stagehand** | Default — best balance of AI + determinism, native Playwright fallback |
| **Playwright (raw)** | Stable flows where user has existing specs |
| **Browser Use** | Long-form agentic flows ("complete checkout end-to-end with realistic data") |
| **testRigor** | Enterprise / on-rails "describe what to test in English, no code" — paid tier |

The agent picks based on flow complexity. The user doesn't pick.

---

## Pair with

- `/orbit-do-it` — the brainless orchestrator that calls this skill
- `/orbit-uat-elementor` / `-gutenberg` / `-woo` / `-forms` / `-membership` — typed UAT templates (deterministic Playwright)
- `/orbit-visual-regression` — pixel-diff after the AI-resolved tests pass (catches "looks different even though it works")

---

## Smoke test

Input: vanilla WP install with a Hello Dolly plugin activated.
Expected output:
- Detects 1 flow ("Verify Hello Dolly shows a quote in WP-Admin nav")
- 1 test passes
- 0 cost (single LLM call < $0.05)

---

## Sources & Evergreen References

### Live sources (fetched on every run)
- [Stagehand homepage](https://www.browserbase.com/stagehand) — primitives: act / extract / observe / agent
- [Stagehand docs](https://docs.stagehand.dev/) — current API (versions move fast)
- [Playwright docs](https://playwright.dev/docs/intro) — base selectors / locators
- [Browser Use](https://browser-use.com/) — alternative agent framework

### Comparative research
- [Stagehand vs Browser Use vs Playwright (2026)](https://www.nxcode.io/resources/news/stagehand-vs-browser-use-vs-playwright-ai-browser-automation-2026)

### Embedded fallback (if all live fetches fail)
- Stagehand: 4 primitives (`act`, `extract`, `observe`, `agent`); Playwright-compatible
- Cost model: ~$0.01-0.05/task with cache reuse; sub-100ms after first run
- Hybrid pattern: deterministic Playwright for stable flows + AI for volatile

### Last reviewed
2026-04-30 — re-fetch on every run; static rules used only on offline fallback
