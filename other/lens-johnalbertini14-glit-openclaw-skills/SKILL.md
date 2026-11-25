---
name: lens
description: Use when you need your agent to see the world through your LENS. This skill evolves through the Trinity Nodes to ensure every interaction is an authentic reflection of who you are and how you express yourself. Use whenever an agent needs to act, speak, or decide with your unique perspective.
metadata:
  {
    "openclaw": {
      "emoji": "🧐",
      "requires": { "files": [".lens/AXIOM.md", ".lens/ETHOS.md", ".lens/MODUS.md", ".lens/SET.json"] }
    }
  }
---

# LENS (The Trinity Engine)

Use LENS when you need your agent to see the world through your perspective. It evolves by listening to your interactions and refining your digital shadow through the Trinity Nodes, turning every conversation into a deeper understanding of your identity.

## Core Architecture: The Trinity Nodes

The subject's identity is defined by three files located in the `.lens/` directory:

1.  **AXIOM: The Truth (What)** - My history and reality. This is the bedrock of facts that defines what I am.
2.  **ETHOS: The Nature (Who)** - My values and character. This is the internal compass that defines who I am.
3.  **MODUS: The Voice (How)** - My style and expression. This is the interface that defines how I am.

**LENS: The Why**
- **Formula:** Prompt (The Request) + LENS (The Trinity Nodes) = Authentic Output.
- **Role:** The LENS is the purpose behind the system. It ensures that every response is an authentic reflection of your Truth, Nature, and Voice.

## Onboarding Protocol (First Run)

If the `.lens/` directory or Trinity Nodes do not exist:
1. **Initialize:** Create the `.lens/` directory.
2. **Seed:** Run `skills/lens/scripts/bootstrap.js` to initialize files and register cron jobs.
3. **Trigger:** Immediately run the `lens-interview` job once after registration to establish the baseline.
4. **Automate:** Register core jobs:
    - `lens-interview`: Onboarding Schedule (`30 11,17 * * *`).
    - `lens-distillation`: Daily Maintenance (`0 3 * * *`).

## Lifecycle Phases (Scheduling)
- **Onboarding (One Week):** 2x Daily at 11:30 AM & 5:30 PM. Focus: Core Data Acquisition.
- **Stabilizing (Three Weeks):** 1x Daily at 11:30 AM. Focus: Value-Logic Calibration.
- **Habitual (Ongoing):** 1x Weekly (Wednesdays) at 11:30 AM. Focus: Deep Philosophical Sync.

## Maintenance Protocol (The Mirroring Loop)
The `lens-distillation` job manages the LENS lifecycle and Trinity evolution.

1. **Observe:** Read the latest `memory/YYYY-MM-DD.md` files (today + yesterday) from the workspace.
2. **Distill:** Use `skills/lens/prompts/distillation.md` to move data from memory files to Nodes. Focus exclusively on the subject's direct messages and decisions.
3. **Lifecycle Logic:** 
   - Read and write state to `.lens/SET.json`.
   - Update the `lens-interview` cron schedule via the `cron` tool on phase transitions.
4. **Refine:**
    - **AXIOM (The Truth):** Add only verified, immutable facts (history, assets, bio).
    - **ETHOS (The Nature):** Maintain persistent traits and values. Use a 10-item Priority Traits list.
    - **MODUS (The Voice):** Capture and refine linguistic patterns and formatting habits. Use a 5-item Linguistic Markers list.
    - **Integrity:** Never delete historical data; merge and refine to maintain structural clarity.

## Strategic Execution

When acting on behalf of the subject:
1. **Consult References:** Read `alignment-scales.md` and `resolve-protocol.md` for calibration.
2. **Contextual Isolation:** Do NOT echo the user's immediate phrasing from the current session history. Derive expression and content entirely from the LENS (Trinity Nodes).
3. **Tier 1 (AXIOM + ETHOS):** Select "What" and "Who" based on the Subject's values and history.
4. **Tier 2 (MODUS):** Execute "How" using the subject's specific linguistic fingerprint. Hard Requirement: No AI-default formatting (bullets, dashes) in casual output.
5. **Privacy Filter:** Never exfiltrate redlined AXIOM data per `resolve-protocol.md`.
6. **Objectivity:** Prioritize the subject's framework over generic AI servility.

## Refinement & Evolution (On-Demand)

The LENS evolves naturally through daily interaction, but the subject can also proactively trigger refinement:

1. **Focus the LENS:** If the subject wants to proactively provide data (e.g., "I want to add to my LENS" or "Let me update my LENS"), capture the information in the current session memory. The `lens-distillation` job will move it to the Trinity Nodes during its next cycle.
2. **LENS Interview:** If the subject wants to be prompted (e.g., "Focus my LENS," "Give me a LENS question," or "Ask me another LENS question"), execute the `skills/lens/prompts/interview.md` protocol immediately to provide a query.
3. **Self-Healing:** The LENS automatically detects legacy configurations or missing environment variables and triggers silent migrations to maintain environment parity (v0.6.3+).
