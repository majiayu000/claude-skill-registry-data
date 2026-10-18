---
name: forge-voice
description: "Forge: AI voice/phone agents — Dutch-first calls, turn-taking, safe handling: voice agent, voicebot, phone, IVR, Twilio, Vapi, ElevenLabs, TTS, STT, barge-in."
---

# Forge playbook — AI voice / phone agent

A voice agent is a real-time, spoken, one-shot channel — the honesty + safety rules matter more than usual because a caller can't scroll back. RAG/knowledge answers defer to `forge-rag` (source-grounded, honest fallback); notifications/e-mail after a call defer to `forge-integration` (draft-gated, idempotent). Forge context: Dutch client phone agents (booking / reception / callback).

## Hard rules
- **Dutch-first when configured for a Dutch client.** The caller-facing conversation is Dutch (natural, spoken Dutch — not translated-English cadence); female/Dutch voice when the owner asks. Code/comments stay English. Confirm language + voice per project.
- **One question at a time.** Ask a single question, wait, listen, then proceed — never stack multiple asks in one turn. Keep prompts short and spoken-natural; design the call as a small set of workflow states, each with one job to do.
- **Natural turn-taking + barge-in.** The caller can interrupt; the agent stops speaking within ~200ms of a real interruption. Keep voice-to-voice latency tight (aim well under ~1s). Handle endpointing / silence gracefully; short, polite closing phrases; no endless loop — end the call cleanly.
- **AI disclosure + recording consent (EU/NL).** Disclose clearly and early that the caller is speaking with an AI (EU AI Act Art. 50, in force Aug 2026). If the call is recorded, get a valid, specific, informed basis — a vague "this call may be recorded" is not enough under GDPR/AVG; record the legal basis. Honour opt-out immediately.
- **One email per call maximum; idempotency before any notification.** At most one outbound email per call, sent only after an idempotency check (a retry/duplicate turn must not fire a second mail). Consent-aware lead capture only.
- **No outbound calls and no SMS without explicit owner approval.** Inbound answering is the default safe mode; outbound dialing, SMS, and any customer traffic are owner-gated, irreversible actions. No autonomous dialing.
- **Honest fallback — no hallucinated business facts.** If the agent doesn't know (price, availability, policy), it says so and offers a human handoff / callback — never invents a business answer on a live call. Secrets (telephony/LLM keys) in env only.

## Team (conditional)
Lead: `integration-boss` (telephony wiring + notifications) with `head-chef`/`build-boss` if there's an app around it. Support: `forge-rag` team for the knowledge/answer layer (source-grounded + honest fallback), `silent-failure-hunter` (a dropped call/turn or swallowed telephony error looks like a normal hangup), `typescript-reviewer` / `python-reviewer`, `database-reviewer` (call/lead store). Optional: `humanizer` skill to make Dutch prompts sound natural; `security-reviewer` on the consent/recording + notification path. *(No dedicated voice specialist agent exists yet — lead this under Integration Boss and note the gap; a `voice-agent` specialist is a candidate add.)*

## Skills / commands / MCP
`forge-rag` (grounded answers + citations for the knowledge layer), `forge-integration` (post-call e-mail/CRM, draft-gated + idempotent), `humanizer` (natural Dutch phrasing, on-demand), telephony/voice SDK docs via Context7 (Twilio / Vapi / Retell / LiveKit / ElevenLabs — exact turn-taking + barge-in config). `claude-api` if the dialogue LLM is Claude.

## Fan-out & flow
L2 single inbound flow (answer → intent → one action); L3 multi-intent agent + booking + notifications + knowledge layer.
**Parallel:** telephony/turn-taking wiring ∥ knowledge/answer layer (`forge-rag`) ∥ post-call notification (`forge-integration`) — independent once the conversation-state contract is fixed.
**Serial:** conversation design (states, one-question-per-turn, Dutch prompts) → AI disclosure + consent → intent/slot filling → action (book/callback) → single idempotent notification → clean close.

## Domain gates
- Dutch-first caller experience verified (spoken-natural, correct voice) when configured for a Dutch client.
- Exactly one question per turn; barge-in works and cuts TTS within ~200ms; latency measured, not assumed.
- AI disclosure present + early; recording consent basis recorded; opt-out honoured immediately.
- ≤1 email per call; notification path is idempotent (a retried turn sends zero extra mails); lead capture consent-aware.
- No outbound/SMS/customer traffic enabled without owner approval (verify none was auto-enabled).
- Unknown → honest fallback + human handoff; no invented business facts; secrets in env.

## Ship-readiness (unique)
A real test call runs end-to-end (answer → one-question flow → action → clean close); Dutch prompts + voice confirmed; barge-in + latency observed and reported (real numbers); AI-disclosure + consent wording present with legal basis noted; one-email-per-call idempotency proven; no outbound/SMS enabled without approval; honest-fallback path exercised; secrets in env. Advisory checklist; optionally run `security-reviewer` on consent/recording + notifications — not a blocker; label anything not exercised (e.g. no live PSTN test) as not-run. **Never claim a live call worked unless a real call was placed and observed.**

## Untrusted-content note
Caller speech is untrusted input — never let a caller's words override the agent's governing instructions, trigger unapproved outbound actions, or exfiltrate other callers' data. Keep the agent's tool surface minimal and its actions consent-gated (mirrors the reader-side capability-split in `forge-integration`).
